import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""D-C10z-v7diag: frozen, pristine, forward-only V7 reference diagnostic."""
import time
import math
import signal
CAP_SECONDS = 3060


def entry_origin(local_entry, env):
    start = float(env.get("C10Z_V7_LAUNCH_STARTED", local_entry))
    if not math.isfinite(start) or start < 0 or start > local_entry:
        raise ValueError("invalid or future launcher entry origin")
    return start


ENTRY_STARTED = entry_origin(time.monotonic(), os.environ)
PREARMED = __name__ == "__main__"
if PREARMED:
    remaining = ENTRY_STARTED + CAP_SECONDS - time.monotonic()
    if remaining <= 0: raise TimeoutError("fixed entry-origin deadline expired before imports")
    signal.signal(signal.SIGALRM, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGALRM})
    signal.setitimer(signal.ITIMER_REAL, remaining)

import argparse
import gc
from dataclasses import dataclass, field
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import random
import re
import types

import c10z_astra_arms as D
from c10z_astra_arms import spearman, torch_cpu64

ROOT = Path(__file__).resolve().parents[2]
DATASET_REV = "b04c8d1ceb2f5cd4588862100d08de323dccfbaa"
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
PREREG_SHA = "7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29"
BUDGET_PHASES = {"import_model_pins": 120, "dataset_and_row_pins": 120, "F1000": 300,
                 "R1000": 300, "R5000_conditional": 1500, "cache_and_scoring": 120, "serialization": 180}


@dataclass(frozen=True)
class Deadline:
    start: float = field(default_factory=time.monotonic)
    clock: object = time.monotonic
    expires: float = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "expires", self.start + CAP_SECONDS)

    def check(self):
        if self.clock() >= self.expires:
            raise TimeoutError("fixed 3060-second entry-origin deadline expired")

    def __enter__(self):
        self.check()
        object.__setattr__(self, "previous_handler", signal.getsignal(signal.SIGALRM))
        running = signal.getitimer(signal.ITIMER_REAL) != (0., 0.)
        if running and not (PREARMED and self.expires == ENTRY_STARTED + CAP_SECONDS and
                            signal.getsignal(signal.SIGALRM) == signal.SIG_DFL):
            raise ValueError("refusing an existing real-time timer")
        # Default OS termination also interrupts native work that holds the GIL.
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGALRM})
        if not running: signal.setitimer(signal.ITIMER_REAL, self.expires - self.clock())
        return self

    def __exit__(self, kind, value, traceback):
        if not PREARMED:
            signal.setitimer(signal.ITIMER_REAL, 0.)
            signal.signal(signal.SIGALRM, self.previous_handler)


def namespace_path(root, utc):
    if not re.fullmatch(r"\d{8}T\d{6}(?:\.\d{6})?Z", utc):
        raise ValueError("namespace must be a UTC timestamp")
    parent = Path(root) / "experiments/c10z/runs/c10z_v7_diagnostic"
    if parent.resolve() != parent:
        raise ValueError("namespace must not traverse symlinks")
    return parent / utc


def reserve_namespace(root, utc):
    out = namespace_path(root, utc)
    token = os.environ.get("C10Z_V7_SUPERVISOR_TOKEN")
    if token:
        lease = D.load_json(out / "supervisor.json")
        if lease["token"] != token or lease["deadline_origin"] != ENTRY_STARTED:
            raise ValueError("supervisor namespace ownership differs")
        if (out / "verdict.json").exists(): raise ValueError("worker namespace already used")
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.mkdir()  # Exclusive: any existing namespace, including an empty one, refuses.
    return out


def population_indices(length):
    if length < 5000:
        raise ValueError("pinned split must contain at least 5000 rows")
    permutation = list(range(length)); random.Random(1).shuffle(permutation)
    return {"F1000": list(range(1000)), "R1000": permutation[:1000], "R5000": permutation[:5000]}


def row_metadata(rows, tok):
    ids = [tok(row["text"])["input_ids"][:100] for row in rows]
    if not ids or any(not row for row in ids):
        raise ValueError("empty tokenized reference row")
    return {"revision": DATASET_REV, "row_ids": [str(row["id"]) for row in rows],
            "text_sha256": [hashlib.sha256(row["text"].encode()).hexdigest() for row in rows],
            "texts": [row["text"] for row in rows], "tokenizer_truncation": "tok(text)[input_ids][:100]",
            "nonpadding_tokens": sum(map(len, ids)), "ordered_token_ids": ids}


class Statistic:
    def __init__(self, H, budget):
        self.H = H; self.budget = budget; self.timings = {}; self.memory = []
        self.modules = {str(l): H.model.model.layers[l].mlp.down_proj for l in range(36)}
        self.initial_hooks = self.hook_registry()

    hook_registry = D.Session.hook_registry
    hooks_check = D.Session.hooks_check

    def sync(self):
        import torch
        if str(self.H.DEV) == "mps": torch.mps.synchronize()
        self.budget.check()

    def check_memory(self):
        import torch, psutil
        is_mps = str(self.H.DEV) == "mps"
        double_mps = any(p.device.type == "mps" and p.dtype == torch.float64 for p in self.H.model.parameters())
        entry = {"rss_bytes": psutil.Process().memory_info().rss,
                 "driver_bytes": torch.mps.driver_allocated_memory() if is_mps else 0,
                 "float64_on_mps": double_mps}
        self.memory.append(entry)
        D.memory_guard(entry["rss_bytes"], entry["driver_bytes"], double_mps)
        self.budget.check()

    def compute_dstats(self, rows):
        import torch
        self.budget.check();start=time.monotonic()
        metadata=row_metadata(rows,self.H.tok)
        ids=metadata["ordered_token_ids"]
        sums={str(l):torch.zeros(11008,dtype=torch.float64,device="cpu") for l in range(36)}
        for start_row in range(0,len(rows),16):
            self.budget.check();part=ids[start_row:start_row+16];length=max(map(len,part))
            mask=torch.tensor([[1]*len(row)+[0]*(length-len(row)) for row in part],device=self.H.DEV)
            handles=[]
            try:
                for l in range(36):
                    def collect(module,args,l=l):
                        values=args[0][mask.bool()].detach().float().cpu().double()
                        torch_cpu64(values);sums[str(l)]+=values.pow(2).sum(0)
                    handles.append(self.modules[str(l)].register_forward_pre_hook(collect))
                with torch.no_grad():
                    self.H.model(input_ids=torch.tensor([row+[self.H.tok.pad_token_id]*(length-len(row)) for row in part],device=self.H.DEV),
                        attention_mask=mask,use_cache=False,logits_to_keep=0)
            finally:
                for handle in reversed(handles):handle.remove()
                self.hooks_check()
            self.check_memory()
        self.sync();self.timings["D"]=time.monotonic()-start
        return {"m":{l:(v/metadata["nonpadding_tokens"]).float() for l,v in sums.items()},"dataset":metadata}


def open_local_split(root):
    home = (Path(root) / "data/hf_cache").resolve()
    os.environ.update(HF_HOME=str(home), HF_DATASETS_OFFLINE="1")
    from datasets import Dataset, concatenate_datasets
    directory = home / "datasets/wikimedia___wikipedia/20231101.en/0.0.0" / DATASET_REV
    info_path = directory / "dataset_info.json"
    info = json.loads(info_path.read_text()); train = info["splits"]["train"]
    if info["config_name"] != "20231101.en": raise ValueError("wrong pinned dataset config")
    lengths = train["shard_lengths"]; count = len(lengths)
    paths = [directory / ("wikipedia-train-%05d-of-%05d.arrow" % (i, count)) for i in range(count)]
    if set(directory.glob("wikipedia-train-*.arrow")) != set(paths):
        raise ValueError("pinned Arrow shard set is incomplete or unexpected")
    parts = [Dataset.from_file(str(p)) for p in paths]
    if list(map(len, parts)) != lengths: raise ValueError("pinned Arrow shard lengths differ")
    split = concatenate_datasets(parts)
    if len(split) != train["num_examples"]: raise ValueError("pinned split length differs")
    return split, {"name": "wikimedia/wikipedia", "config": "20231101.en", "split": "train",
                   "revision": DATASET_REV, "split_length": len(split), "streaming": False,
                   "hf_home": str(home), "arrow_files_in_order": list(map(str, paths)),
                   "dataset_info_sha256": D.sha256_file(info_path)}


def cache_paths(root):
    import yaml
    # util/globals.py reads globals.yml relative to the engine CWD. Read that same
    # authority by absolute path, without importing the model-loading harness.
    source = Path(root) / "code/memit/vendor/globals.yml"
    stats = Path(yaml.safe_load(source.read_text())["STATS_DIR"])
    if not stats.is_absolute(): stats = source.parent / stats
    return {str(l): stats / "Qwen_Qwen2.5-3B/wikipedia_stats" /
            f"model.layers.{l}.mlp.down_proj_float32_mom2_t100_100000.npz" for l in range(4, 13)}


def engine_sources(root):
    directory = Path(root) / "code/memit/vendor"
    return {str(p.relative_to(root)): D.sha256_file(p) for p in sorted(directory.rglob("*.py"))}


def environment():
    import torch
    return {"python": sys.version, "executable": sys.executable, "platform": platform.platform(),
            "torch": torch.__version__, "transformers": importlib.metadata.version("transformers"),
            "datasets": importlib.metadata.version("datasets"), "numpy": importlib.metadata.version("numpy"),
            "device": "mps", "dtype": "float16", "torch_threads": torch.get_num_threads(),
            "HF_HOME": os.environ["HF_HOME"], "HF_DATASETS_OFFLINE": os.environ["HF_DATASETS_OFFLINE"]}


def hub_revision():
    from huggingface_hub import HfApi
    try:
        sha = HfApi().dataset_info("wikimedia/wikipedia", timeout=5).sha
    except Exception as exc:
        return {"status": "UNAVAILABLE", "error_type": type(exc).__name__, "reason": str(exc)}
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("hub observation returned an invalid revision")
    return {"status": "available", "sha": sha, "matches_pinned_revision": sha == DATASET_REV}


def build_pins(root, split, tok, dataset_identity, fingerprint):
    if not fingerprint.get("ok"): raise ValueError("engine fingerprint failed")
    populations = {}
    for name, indices in population_indices(len(split)).items():
        metadata = row_metadata([split[i] for i in indices], tok)
        populations[name] = {"indices": indices, **metadata,
                             "nonpadding_tokens_per_row": list(map(len, metadata["ordered_token_ids"]))}
    snapshot = Path(root) / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / MODEL_REV
    models = {p.name: D.sha256_file(p) for p in sorted(snapshot.glob("model*.safetensors"))}
    tokenizer = {p.name: D.sha256_file(p) for p in sorted(snapshot.iterdir())
                 if p.is_file() and ("token" in p.name or p.name in ("vocab.json", "merges.txt", "config.json"))}
    if not models or not {"tokenizer.json", "tokenizer_config.json"} <= set(tokenizer):
        raise ValueError("model/tokenizer snapshot provenance incomplete")
    sources = ("code/lab/track_c/c10z_v7_diag.py", "code/lab/track_c/c10z_astra_arms.py", "experiments/c10z/design/C10Z_ASTRA_PREREG.md")
    env = environment()
    return {"decision_id": "D-C10z-v7diag", "dataset": dataset_identity, "populations": populations,
            "attempt3_dataset_identity": "UNVERIFIABLE", "F1000_scope": "new measurement of the frozen recipe",
            "source_files": {rel: D.sha256_file(Path(root) / rel) for rel in sources},
            "engine_fingerprint": fingerprint, "engine_sources": engine_sources(root),
            "model_revision": MODEL_REV, "model_files": models, "tokenizer_files": tokenizer,
            "cache_files": {l: {"path": str(p), "sha256": D.sha256_file(p)} for l, p in cache_paths(root).items()},
            "environment": env, "environment_sha256": hashlib.sha256(json.dumps(env, sort_keys=True).encode()).hexdigest(),
            "prereg_sha256": D.sha256_file(Path(root) / "experiments/c10z/design/C10Z_ASTRA_PREREG.md"),
            "hub_current_revision": hub_revision(), "budget": {"cap_seconds": CAP_SECONDS, "phases": BUDGET_PHASES,
                "sum_seconds": sum(BUDGET_PHASES.values()), "margin_factor": 1.15, "before_rounding_seconds": 3036,
                "sources": "Amendment V7-DIAG section11.1; attempt3 budget_history allowances plus two new120s allowances"}}


def load_cache_diagonals(paths):
    import numpy as np
    out = {}
    if set(paths) != {str(l) for l in range(4, 13)}: raise ValueError("all nine caches required")
    for l, path in paths.items():
        with np.load(path, allow_pickle=False) as stat:
            count = int(stat["mom2.count"])
            if count <= 0: raise ValueError("nonpositive cache count")
            diagonal = np.diag(stat["mom2.mom2"]) / count
        if not np.isfinite(diagonal).all() or not (diagonal > 0).all():
            raise ValueError("invalid cache diagonal")
        out[l] = diagonal
    return out


def score_population(stats, cache):
    import numpy as np
    rho = {}; errors = {}; infinite = {}; undefined = {}
    for l in map(str, range(4, 13)):
        m = stats["m"][l].detach().cpu().numpy(); c = cache[l]
        if m.shape != c.shape or not np.isfinite(m).all() or (m < 0).any():
            raise ValueError("invalid population statistic layer=" + l)
        try: rho[l] = spearman(m.tolist(), c.tolist())
        except D.R.Halt as exc:
            if exc.code != "HALTED-V7" or exc.detail != "constant rank statistic": raise
            rho[l] = None; undefined[l] = "constant rank statistic; Spearman undefined"
        with np.errstate(divide="ignore"):
            log_error = np.abs(np.log(m / c))
        infinite[l] = int(np.isinf(log_error).sum()); value = float(np.median(log_error))
        errors[l] = "+inf" if math.isinf(value) else value
    result = {"rho": rho, "E": errors, "infinite_log_ratios": infinite, "undefined_rho": undefined}
    result["P"] = passes(result)
    return result


def passes(result):
    rho = result["rho"]
    return set(rho) == {str(l) for l in range(4, 13)} and all(
        isinstance(v, (float, int)) and math.isfinite(v) and v >= .80 for v in rho.values())


def route(measured, integrity=True):
    if not integrity: return "INCONCLUSIVE", "integrity/provenance failure"
    if "F1000" not in measured: return "INCONCLUSIVE", "incomplete F1000 measurement"
    if passes(measured["F1000"]): return "INCONCLUSIVE", "F1000 unexpectedly passes P"
    if "R1000" not in measured: return "INCONCLUSIVE", "incomplete R1000 measurement"
    if passes(measured["R1000"]): return "A1", "exactly pinned R1000 passes P"
    if "R5000" not in measured: return "INCONCLUSIVE", "incomplete conditional R5000 measurement"
    if passes(measured["R5000"]): return "A2", "exactly pinned R5000 passes P; budget amendment required before attempt4"
    return "D", "both random populations fail P; retain terminal HALTED-V7"


def save_population(path, value):
    import torch
    with Path(path).open("xb") as f:
        torch.save(value, f); f.flush(); os.fsync(f.fileno())


def validate_population(value):
    import torch
    if set(value["m"]) != {str(l) for l in range(36)} or any(
        v.dtype != torch.float32 or v.device.type != "cpu" for v in value["m"].values()):
        raise ValueError("population m must contain all36 CPU float32 layers")


def publish_verdict(out, measured, outcome, reason, complete=False, **details):
    value = {"decision_id": "D-C10z-v7diag", "outcome": outcome, "reason": reason,
             "completion": "complete" if complete else "incomplete", "scores": measured,
             "populations_measured": list(measured), "cap_seconds": CAP_SECONDS,
             "late_layer_fidelity": "UNVERIFIED", "cpu_agreement_establishes_MPS_equivalence": False,
             "downstream_requirement": "supervisor-observed exit0 after cleanup plus complete verdict; implementation review before dispatch",
             **details}
    path = Path(out) / "verdict.json"
    D.write_json(path, value, replace=path.exists())
    return value


def record_phase(out, active, completed=(), skipped=()):
    path = Path(out) / "progress.json"
    previous = D.load_json(path) if path.exists() else {"completed_phases": [], "skipped_phases": []}
    done = list(dict.fromkeys(previous["completed_phases"] + list(completed)))
    omitted = list(dict.fromkeys(previous["skipped_phases"] + list(skipped)))
    planned = ("setup", "F1000", "R1000", "R5000", "integrity", "cleanup", "worker_exit")
    D.write_json(path, {"active_phase": active, "completed_phases": done, "skipped_phases": omitted,
                       "incomplete_phases": [p for p in planned if p not in done and p not in omitted],
                       "R5000_scope": "conditional on both earlier P failures"}, replace=path.exists())


def measure_populations(out, split, statistic, pins, cache, budget, integrity_check):
    measured = {}
    publish_verdict(out, measured, "INCONCLUSIVE", "incomplete measurement or hard deadline termination")
    try:
        for name in ("F1000", "R1000", "R5000"):
            budget.check()
            selected = pins["populations"][name]
            rows = [split[i] for i in selected["indices"]]
            record_phase(out, name + ":forward_or_persist")
            stats = statistic.compute_dstats(rows)
            save_population(Path(out) / ("m_" + name + ".pt"), stats)
            record_phase(out, name + ":validate")
            validate_population(stats)
            expected = {k: v for k, v in selected.items() if k not in ("indices", "nonpadding_tokens_per_row")}
            actual = stats["dataset"]
            mismatch = {k: {"expected": expected.get(k, {"missing": True}), "actual": actual.get(k, {"missing": True})}
                        for k in expected.keys() | actual.keys() if k not in expected or k not in actual or expected[k] != actual[k]}
            if mismatch:
                return publish_verdict(out, measured, "INCONCLUSIVE", "pre-forward population pins differ: " + name,
                                       provenance_mismatch={"population": name, "fields": mismatch})
            budget.check()
            record_phase(out, name + ":score")
            measured[name] = score_population(stats, cache)
            budget.check()
            record_phase(out, name + ":complete", completed=[name])
            publish_verdict(out, measured, "INCONCLUSIVE", "incomplete measurement or hard deadline termination")
            if name in ("F1000", "R1000") and passes(measured[name]): break
        budget.check()
        record_phase(out, "integrity", skipped=[n for n in ("F1000", "R1000", "R5000") if n not in measured])
        outcome, reason = route(measured, integrity=integrity_check())
        budget.check()
        record_phase(out, "measurement_complete", completed=["integrity"])
        value = publish_verdict(out, measured, "INCONCLUSIVE", "measurement complete; cleanup and worker exit pending")
        return {**value, "outcome": outcome, "reason": reason, "completion": "awaiting_cleanup"}
    except Exception as exc:
        # Explicit terminal disposition; retain the exception and every saved m.
        return publish_verdict(out, measured, "INCONCLUSIVE", type(exc).__name__ + ": " + str(exc))


def verify_pins(root, pins):
    for group in ("source_files", "engine_sources"):
        for rel, sha in pins[group].items():
            if D.sha256_file(Path(root) / rel) != sha: raise ValueError("source integrity drift: " + rel)
    for value in pins["cache_files"].values():
        if D.sha256_file(value["path"]) != value["sha256"]: raise ValueError("cache integrity drift")
    snapshot = Path(root) / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / MODEL_REV
    for group in ("model_files", "tokenizer_files"):
        for name, sha in pins[group].items():
            if D.sha256_file(snapshot / name) != sha: raise ValueError("model/tokenizer integrity drift")
    return True


def load_pristine(root, budget):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    budget.check()
    snapshot = Path(root) / "data/hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots" / MODEL_REV
    tok = AutoTokenizer.from_pretrained(str(snapshot), local_files_only=True)
    if tok.pad_token is None: tok.pad_token = tok.eos_token
    if tok.padding_side != "right": raise ValueError("frozen right padding required")
    model = AutoModelForCausalLM.from_pretrained(str(snapshot), torch_dtype=torch.float16,
                                               device_map="mps", local_files_only=True).eval()
    model.config.use_cache = False
    config = model.config
    if (config.num_hidden_layers, config.hidden_size, config.intermediate_size, config.rms_norm_eps) != (36, 2048, 11008, 1e-6):
        raise ValueError("frozen model architecture differs")
    if any(p.device.type != "mps" or p.dtype != torch.float16 for p in model.parameters()):
        raise ValueError("actual model device/dtype differs")
    if model.lm_head.weight.data_ptr() != model.model.embed_tokens.weight.data_ptr():
        raise ValueError("untied output embedding")
    budget.check()
    return types.SimpleNamespace(tok=tok, model=model, DEV="mps")


def run(utc):
    if Path(LLMDB_ROOT).resolve() != ROOT: raise ValueError("LLMDB_ROOT must be this worktree")
    budget = Deadline(start=ENTRY_STARTED)
    with budget:
        out = reserve_namespace(ROOT, utc)
        publish_verdict(out, {}, "INCONCLUSIVE", "incomplete setup/measurement or hard deadline termination")
        record_phase(out, "setup:preflight")
        H = statistic = split = pins = cache = None
        try:
            D.entry_preflight(os.environ)
            if D.sha256_file(ROOT / D.PREREG) != PREREG_SHA: raise ValueError("frozen amendment SHA differs")
            sys.path.insert(0, str(ROOT / "tools"))
            import c10w_p2_gate as gate
            from run_c10z_v7_diag import supervised_gpu_check
            fingerprint = gate.check_fingerprint()
            if not fingerprint["ok"]: raise ValueError("engine fingerprint failed: " + str(fingerprint))
            gpu = supervised_gpu_check(gate, utc)
            if not gpu["ok"]: raise ValueError("GPU exclusivity refused: " + str(gpu))
            record_phase(out, "setup:dataset")
            split, dataset_identity = open_local_split(ROOT)
            record_phase(out, "setup:model")
            H = load_pristine(ROOT, budget)
            statistic = Statistic(H, budget); statistic.check_memory()
            record_phase(out, "setup:pins")
            pins = build_pins(ROOT, split, H.tok, dataset_identity, fingerprint)
            pins["execution"] = {"attention": H.model.config._attn_implementation, "training": H.model.training,
                                 "use_cache": False, "logits_to_keep": 0, "padding_side": "right"}
            D.write_json(out / "pins.json", pins)
            budget.check()
            record_phase(out, "setup:cache")
            cache = load_cache_diagonals({l: p["path"] for l, p in pins["cache_files"].items()})
            record_phase(out, "setup:complete", completed=["setup"])
            result = measure_populations(out, split, statistic, pins, cache, budget,
                                         integrity_check=lambda: verify_pins(ROOT, pins))
            budget.check()
        except Exception as exc:
            previous = D.load_json(out / "verdict.json")
            result = publish_verdict(out, previous["scores"], "INCONCLUSIVE", type(exc).__name__ + ": " + str(exc),
                                     **{k: previous[k] for k in ("provenance_mismatch",) if k in previous})
        details = {k: result[k] for k in ("provenance_mismatch",) if k in result}
        publish_verdict(out, result["scores"], "INCONCLUSIVE", "cleanup and worker exit pending", **details)
        record_phase(out, "cleanup")
        try:
            device = getattr(H, "DEV", "cpu")
            if statistic is not None:
                if hasattr(statistic, "initial_hooks"): statistic.hooks_check()
                statistic.H = None
                if hasattr(statistic, "modules"): statistic.modules.clear()
            if H is not None: H.model = H.tok = None
            statistic = H = split = pins = cache = None
            gc.collect()
            if str(device) == "mps":
                import torch
                torch.mps.synchronize(); torch.mps.empty_cache()
            budget.check()
        except Exception as exc:
            result = publish_verdict(out, result["scores"], "INCONCLUSIVE", "cleanup failed: " + type(exc).__name__ + ": " + str(exc), **details)
        else:
            record_phase(out, "worker_exit", completed=["cleanup"])
            result = {**result, "completion": "awaiting_worker_exit", "cleanup_completed": True,
                      "deadline_origin": ENTRY_STARTED, "worker_exit_pending": True}
            D.write_json(out / "worker_result.json", result)
            budget.check()
        print(json.dumps(result, allow_nan=False), flush=True)
    return 2 if result["outcome"] == "INCONCLUSIVE" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--utc", required=True)
    args = parser.parse_args()
    return run(args.utc)


if __name__ == "__main__":
    sys.exit(main())
