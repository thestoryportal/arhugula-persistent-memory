import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""Diagnostic only: pristine Z0 shape comparisons; no editing or telemetry.

The operator launches MPS measurement. Import and --help never load a model.
CPU coverage lives in c10z_astra_selftest.Z0ProbeTests.
"""
import argparse
import datetime
import hashlib
import importlib
import json
from pathlib import Path
import re
import time
from types import SimpleNamespace

import c10z_astra_arms as D

ROOT = D.ROOT


def validate_output(out):
    out = Path(out)
    namespace = ROOT / "results/c10z_astra_z0_probe"
    if not out.is_absolute() or out.parent != namespace or out.resolve() != out:
        raise ValueError("out dir must be absolute under results/c10z_astra_z0_probe/<UTC>/ without symlinks")
    if not re.fullmatch(r"\d{8}T\d{6}(?:\.\d{6})?Z", out.name):
        raise ValueError("out dir must have a UTC YYYYMMDDTHHMMSS[.ffffff]Z name")
    datetime.datetime.strptime(out.name, "%Y%m%dT%H%M%S.%fZ" if "." in out.name else "%Y%m%dT%H%M%SZ")
    if out.exists() or out.is_symlink():
        raise FileExistsError("refusing existing probe out dir: " + str(out))
    return out


def read_inputs():
    source = ROOT / "results/c10z_astra_attempt2"
    run = D.load_json(source / "run.json")
    path = source / "context_templates.json"
    raw = path.read_bytes(); sha = hashlib.sha256(raw).hexdigest()
    if sha != run.get("context_templates", {}).get("sha256"):
        raise ValueError("context template sha256 does not match attempt2 run.json")
    templates = D.Session.flatten_templates(json.loads(raw))
    pristine = D.load_json(source / "pristine_hash.json")["H_pristine"]
    return templates, {"attempt_dir": str(source), "context_templates_sha256": sha,
        "run_sha256": D.sha256_file(source / "run.json"), "H_pristine": pristine,
        "attempt_id": run.get("attempt_id")}


def make_session(H, templates):
    # Avoid Session.__init__: it writes pristine records and installs edit wrappers.
    s = D.Session.__new__(D.Session)
    s.H = H; s.arms = dict(H.ARMS); s.templates = list(templates)
    s.modules = {str(l): H.model.model.layers[l].mlp.down_proj for l in range(36)}
    s.memory = []; s.checks = {}; s.telemetry = None
    s.budget = SimpleNamespace(check=lambda: None)
    s.initial_hooks = s.hook_registry()
    return s


def load_session(templates):
    D.entry_preflight(os.environ)
    os.environ.update(LLMDB_ROOT=str(ROOT), LLMDB_DEVICE="mps", HF_HOME=str(ROOT / "hf_cache"), C10Z_TELEMETRY="0")
    import torch
    torch.manual_seed(0)
    H = importlib.import_module("c10e_bandknob")
    p = next(H.model.parameters())
    if str(H.DEV) != "mps" or p.device.type != "mps" or p.dtype != torch.float16:
        raise ValueError("probe requires the driver's MPS fp16 model")
    if (H.ID != "Qwen/Qwen2.5-3B" or H.REV != "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b" or
        H.model.config.num_hidden_layers != 36 or H.model.config.hidden_size != 2048 or
        H.model.config.intermediate_size != 11008 or H.model.config.rms_norm_eps != 1e-6):
        raise ValueError("probe model identity/architecture differs from the driver")
    if H.model.lm_head.weight.data_ptr() != H.model.model.embed_tokens.weight.data_ptr():
        raise ValueError("probe requires the driver's tied output embedding")
    if len(H.FICTION) != 24 or set(H.ARMS) != set(D.R.ARMS):
        raise ValueError("probe fact/arm population differs from the driver")
    H.model.config.use_cache = False
    return make_session(H, templates)


def model_hashes(model):
    parameters = hashlib.sha256(); buffers = hashlib.sha256()
    for _, value in model.named_parameters(): parameters.update(D.tensor_bytes(value))
    for name, value in model.named_buffers():
        buffers.update((name + str(value.shape) + str(value.dtype)).encode())
        buffers.update(D.tensor_bytes(value.reshape(-1)))
    return parameters.hexdigest(), buffers.hexdigest()


def capture_forward(s, action):
    """Capture actual rotary input IDs, including the broadcast shape, without supplying IDs."""
    seen = []
    def capture(module, args, kwargs):
        ids = kwargs.get("position_ids", args[1] if len(args) > 1 else None)
        if ids is None: raise ValueError("model rotary call did not expose position_ids")
        seen.append(ids.detach().cpu().clone())
    previous = s.initial_hooks
    handle = s.H.model.model.rotary_emb.register_forward_pre_hook(capture, with_kwargs=True)
    s.initial_hooks = s.hook_registry()
    try:
        value = action()
        if len(seen) != 1: raise ValueError("expected exactly one rotary position_ids call")
        return value, seen[0]
    finally:
        handle.remove(); s.initial_hooks = previous; s.hooks_check()


def position_row(ids, row, batch_size, width):
    if tuple(ids.shape) not in ((1, width), (batch_size, width)):
        raise ValueError("unexpected rotary position_ids shape: " + str(tuple(ids.shape)))
    return ids[0 if ids.shape[0] == 1 else row].tolist()


def diff_statistics(native, other):
    import torch
    a = torch.as_tensor(native, dtype=torch.float64, device="cpu")
    b = torch.as_tensor(other, dtype=torch.float64, device="cpu")
    diff = (a - b).abs()
    if not diff.numel() or not bool(torch.isfinite(diff).all()):
        raise ValueError("empty or nonfinite diagnostic differences")
    return {"max": float(diff.max()), "median": float(torch.quantile(diff, .5)),
            "p95": float(torch.quantile(diff, .95))}


def measure(s, expected_pristine=None, native_mask="none"):
    import torch
    if native_mask not in ("none", "ones"): raise ValueError("native_mask must be none or ones")
    started = time.monotonic(); before, buffers_before = model_hashes(s.H.model)
    if expected_pristine is not None and before != expected_pristine:
        raise ValueError("loaded model does not match attempt2 H_pristine")
    hash_seconds = time.monotonic() - started
    batch = s.make_batch(D.R.A7, [t.format(s.H.CANON) for t in s.templates])
    n_rows = len(batch["input_ids"]); width = batch["T_pad"]
    obs, batch_ids = capture_forward(s, lambda: s._observe(batch, None, True, None))
    timings = {"initial_hash_s": hash_seconds, "batch_s": obs["forward_seconds"],
               "batch1_s": 0., "native_prefix_s": 0., "full_sequence_s": 0.}
    positions = []
    identity = {(r["fact"], r["q"]): k for k, r in enumerate(batch["requirements"]) if r["view"] == 0}

    def native(ids):
        input_ids = torch.tensor([ids], device=s.H.DEV)
        kwargs = {"attention_mask": torch.ones_like(input_ids)} if native_mask == "ones" else {}
        with torch.no_grad():
            return s.H.model(input_ids, use_cache=False, logits_to_keep=0, **kwargs).logits[0]

    for i, target in enumerate(batch["target_ids"]):
        identity_row = i * 6; prompt = batch["prompt_ids"][identity_row]
        single = dict(batch)
        single["input_ids"] = [batch["input_ids"][identity_row]]
        single["attention_mask"] = [batch["attention_mask"][identity_row]]
        single["requirements"] = [dict(batch["requirements"][identity[(i, q)]], row=0) for q in range(len(target))]
        # Keep T_pad and the exact mask/indices: this control changes batch dimension only.
        obs1, batch1_ids = capture_forward(s, lambda: s._observe(single, None, True, None))
        timings["batch1_s"] += obs1["forward_seconds"]
        full_tokens = prompt + target[:-1]
        s.sync(); t = time.monotonic()
        full, full_ids = capture_forward(s, lambda: native(full_tokens))
        s.sync(); timings["full_sequence_s"] += time.monotonic() - t
        used_batch_ids = position_row(batch_ids, identity_row, n_rows, width)
        used_batch1_ids = position_row(batch1_ids, 0, 1, width)
        used_full_ids = position_row(full_ids, 0, 1, len(full_tokens))
        for q, y in enumerate(target):
            ri = identity[(i, q)]; req = batch["requirements"][ri]; index = req["index"]
            prefix = prompt + target[:q]
            s.sync(); t = time.monotonic()
            prefix_logits, prefix_ids = capture_forward(s, lambda: native(prefix))
            s.sync(); timings["native_prefix_s"] += time.monotonic() - t
            tgt = torch.tensor([y], device="cpu")
            lead = float(D.margin_leads(prefix_logits[-1][None, :], tgt)[0][0])
            full_lead = float(D.margin_leads(full[index][None, :], tgt)[0][0])
            batch_lead = float(obs["leads"][ri]); batch1_lead = float(obs1["leads"][q])
            a = torch.tensor(lead, dtype=torch.float64, device="cpu")
            diffs = {"native_minus_batch": float(a - batch_lead), "native_minus_batch1": float(a - batch1_lead),
                     "native_minus_full": float(a - full_lead)}
            window_start = max(0, index - 8); window_end = min(len(full_tokens), index + 9)
            context = full_tokens[window_start:window_end]
            positions.append({"fact": i, "subject": s.H.FICTION[i], "view": 0, "q": q, "row": identity_row,
                "index": index, "target_id": y, "target_text": s.H.tok.decode([y]),
                "native_lead": lead, "batch_lead": batch_lead, "full_lead": full_lead, "batch1_lead": batch1_lead,
                "native_max_abs_logit": float(prefix_logits.detach().to(device="cpu", dtype=torch.float32).abs().max()),
                "native_logits_dtype": str(prefix_logits.dtype),
                "diffs": diffs, "abs_diffs": {k: abs(v) for k, v in diffs.items()},
                "padding_side": "right", "batch_attention_mask_sum": sum(single["attention_mask"][0]),
                "batch1_attention_mask_sum": sum(single["attention_mask"][0]),
                "batch_attention_mask": single["attention_mask"][0],
                "native_attention_mask_sum": len(prefix), "full_attention_mask_sum": len(full_tokens),
                "native_full_mask_argument": None if native_mask == "none" else "ones",
                "batch_position_ids": used_batch_ids, "batch1_position_ids": used_batch1_ids,
                "native_position_ids": position_row(prefix_ids, 0, 1, len(prefix)), "full_position_ids": used_full_ids,
                "position_id": used_batch_ids[index], "batch1_shape": [1, width],
                "native_shape": [1, len(prefix)], "full_shape": [1, len(full_tokens)],
                "token_context": {"start": window_start, "scored_index": index, "ids": context,
                                  "text": s.H.tok.decode(context)}})
            del prefix_logits
        del obs1, full
    del obs
    t = time.monotonic(); after, buffers_after = model_hashes(s.H.model)
    timings["final_hash_s"] = time.monotonic() - t; timings["total_measure_s"] = time.monotonic() - started
    if before != after or buffers_before != buffers_after:
        raise ValueError("weights changed (parameters or buffers); diagnostic refuses, without restoring")
    native_leads = [r["native_lead"] for r in positions]
    summaries = {"native-batch": diff_statistics(native_leads, [r["batch_lead"] for r in positions]),
                 "native-batch1": diff_statistics(native_leads, [r["batch1_lead"] for r in positions]),
                 "native-full": diff_statistics(native_leads, [r["full_lead"] for r in positions])}
    full_batch = diff_statistics([r["full_lead"] for r in positions], [r["batch_lead"] for r in positions])
    return {"schema": "c10z_astra_z0_probe/v1", "diagnostic_only": True, "scientific_verdict": False,
        "telemetry": False, "seed": 0, "device": str(s.H.DEV), "dtype": str(next(s.H.model.parameters()).dtype),
        "native_mask": native_mask, "attn_implementation": s.H.model.config._attn_implementation,
        "batch_shape": [n_rows, width], "batch_position_ids_shape": list(batch_ids.shape),
        "padding_side": "right", "tokenizer_padding_side": s.H.tok.padding_side,
        "batch1_control": "one identity row at unchanged original padded width, mask, and indices",
        "statistics_dtype": "torch.float64", "statistics_device": "cpu", "quantile_interpolation": "linear",
        "weights_unchanged": True, "weights_before_sha256": before, "weights_after_sha256": after,
        "buffers_before_sha256": buffers_before, "buffers_after_sha256": buffers_after,
        "z0_sigma_shape": summaries["native-batch"]["max"], "z0_full_sigma": full_batch["max"],
        "full-batch": full_batch, "summary": summaries, "positions": positions,
        "worst_10": sorted(positions, key=lambda r: r["abs_diffs"]["native_minus_batch"], reverse=True)[:10],
        "timing": timings}


def run(out, native_mask="none"):
    started = time.monotonic(); out = validate_output(out)
    templates, inputs = read_inputs()
    out.mkdir(parents=True, exist_ok=False)
    t = time.monotonic(); s = load_session(templates); load_seconds = time.monotonic() - t
    record = measure(s, expected_pristine=inputs["H_pristine"], native_mask=native_mask)
    record.update(inputs=inputs, templates=templates, out_dir=str(out),
        measured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        sources={p: D.sha256_file(ROOT / p) for p in (
            "experiments/track_c/c10z_astra_z0_probe.py", "experiments/track_c/c10z_astra_arms.py",
            "experiments/track_c/c10z_astra_read.py", D.HARNESS, D.PREREG)},
        model_id=s.H.ID, model_revision=s.H.REV)
    record["timing"].update(model_load_s=load_seconds, total_before_serialization_s=time.monotonic() - started)
    D.write_json(out / "probe.json", record)
    print("C10Z_Z0_PROBE_DIAGNOSTIC " + str(out / "probe.json"), flush=True)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir", type=Path, help="fresh absolute results/c10z_astra_z0_probe/<UTC>/ directory")
    parser.add_argument("--native-mask", choices=("none", "ones"), default="none",
                        help="native/full forward attention mask; none matches the unchanged driver Z0")
    args = parser.parse_args()
    return run(args.out_dir, native_mask=args.native_mask)


if __name__ == "__main__": sys.exit(main())
