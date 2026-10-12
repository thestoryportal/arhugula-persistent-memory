#!/usr/bin/env python3
"""D-ML-1 operand harvest. Import is model-free; launch only through the shell gate."""
import argparse
import contextlib
import copy
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import sys

W = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(W))
from tools import mathlab_runtime as R

BAND = [4, 5, 6, 7, 8]
A1, A2, A7 = "A1_single", "A2_coherent2", "A7_coined_coined"
MINT = ["mint1_s0", "mint1_s1", "mint1_s2"]
CTX_SHA = "8638d12c6d5844168e1577a459103fa309bcf995fc1225df7e716de11a87cdc9"
MODEL_ID = "Qwen/Qwen2.5-3B"
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
BASE = "results/c10u_mint2/r3/"
RECORD_SHAS = ["ade8ba1678dc45850168ff8303afd28359b33c1c7a9f0731feee1143eca2c8f9",
               "ab4cc4ec22fd1f595d489f889d1d7ea15c12b5ebf6664b9d7a8fa80819b8ad6f",
               "626750bc4d23f3a90e2246e442ba38b587fcab9909da57e9f50999ff3c54bb62"]
TARGET_SHAS = ["2b1ba55514cb7abd4b23e48424e4556a029c6f1ad70a7102f49e79e1173e8938",
               "a931e80572e8f62983cc6e45d7c47a0d5e2a59d0b7513cef2059900cb3b16003",
               "88c8e6a5928a4140988b27f8d33abae860cac1cdc5a7949b67f8566758f28e35"]
STEP0_SHAS = ["2afbfcc45b72ef9384dcd3ec627ac82a0d811a9c133ed26f41c046e96724192b",
              "9636dde8c29ed3f14c1cfee7d2ac2af0f8a5549c530a219a7f36725ccacc38c6",
              "0eb81cf9824a65cfe37bd5f5618f6ea19552f761c77cbe9dfd3553b3da026dab"]
AUDIT_SOURCES = ["experiments/track_c/c10u_mint2_arms.py", "experiments/track_c/c10l_mint_lib.py",
                 "experiments/track_c/c10e_bandknob.py", "configs/screens/g6_screen_qwen3b.json",
                 "configs/screens/g6_screen_qwen3b_v2.json"]


def cpu_copy(tensor):
    return tensor.detach().cpu().clone()


def tensor_sha(tensor):
    return hashlib.sha256(tensor.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def digest_tensor(digest):
    import torch
    return torch.tensor(list(bytes.fromhex(digest)), dtype=torch.uint8)


def capture_operands(locals_):
    import torch
    values = {k: cpu_copy(locals_[k]) for k in ("zs", "K", "Kf", "rf", "resid", "cur", "upd")}
    ca = cpu_copy(locals_["ca"])
    zero = not bool(torch.count_nonzero(ca))
    R.require(zero, "CACHE", "science write cache must be exactly zero")
    values["ca_norm"] = torch.linalg.vector_norm(ca.double())
    values["ca_sha256"] = digest_tensor(tensor_sha(ca)); values["ca_zero"] = torch.tensor(zero)
    del ca
    Pi = cpu_copy(locals_["Pi"])
    R.require(Pi.dtype == torch.float32, "PROJECTOR", "projector must be native fp32")
    # An orthogonal projector's trace is its integral retained-null-space count.
    values["Pi_null_n"] = torch.trace(Pi.double()).round().to(torch.int64)
    values["Pi_sha256"] = digest_tensor(tensor_sha(Pi))
    for j in range(4):
        values[f"Pi_probe{j}"] = Pi @ torch.randn(Pi.shape[0], generator=torch.Generator().manual_seed(j))
    del Pi
    update = values.pop("upd")
    values["upd_precast"] = update
    values["upd_norm"] = torch.linalg.vector_norm(update.double())
    values["upd_sha256"] = digest_tensor(tensor_sha(update))
    return values


class EditObserver:
    def __init__(self, H, completed=None, failed=None):
        self.H = H
        self.original = H.my_edit
        self.edit_code = self.original.__code__
        self.shape_code = H.upd_matrix_match_shape.__code__
        self.writes = []; self.current = None; self.arm_override = None
        self.completed = completed; self.last_capture_count = 0
        self.failed = failed; self.failed_writes = []

    @staticmethod
    def coverage_passes(captures, return_count):
        return [(r["i"], r["layer"]) for r in captures] == list(enumerate(BAND)) and return_count == 1

    @classmethod
    def validate_coverage(cls, captures, return_count):
        R.require(cls.coverage_passes(captures, return_count),
                  "CAPTURE", "write must have exactly five ordered captures and one return")

    def preserve_failed(self, write, error):
        write.update(diagnostic_only=True, analysis_eligible=False, artifacts=[],
            coverage=dict(captures=write["captures"], return_count=write["return_count"],
                          expected_captures=[dict(i=i, layer=l) for i, l in enumerate(BAND)],
                          expected_return_count=1, passed=self.coverage_passes(write["captures"], write["return_count"])),
            error=dict(type=type(error).__name__, code=getattr(error, "code", None), message=str(error)))
        self.failed_writes.append(write)
        if self.failed is not None:
            try:
                self.failed(write)
            except Exception as persistence_error:
                write["persistence_error"] = dict(type=type(persistence_error).__name__, message=str(persistence_error))
                raise error from persistence_error

    def failure_details(self):
        return [{k: v for k, v in write.items() if k not in ("capture_tensors", "returned_native_tensors")} for write in self.failed_writes]

    def profile(self, frame, event, arg):
        matching = (event == "call" and frame.f_code is self.shape_code and frame.f_back is not None
                    and frame.f_back.f_code is self.edit_code)
        returning = event == "return" and frame.f_code is self.edit_code
        if not matching and not returning: return
        # This is deliberately the first check on every matching event.
        law5 = self.H._LAW5_DEFAULT_CTX
        R.require(self.current is not None and law5 == (self.current["tag"] == "law5"), "CAPTURE", "LAW#5 tag changed within a write")
        if returning:
            self.current["return_count"] += 1
            return
        local = frame.f_back.f_locals
        row = dict(i=local["i"], layer=local["layer"])
        if not law5:
            R.require([r["subject"] for r in local["requests"]] == self.H.FICTION and len(self.H.FICTION) == 24,
                      "SUBJECT", "science request order must be the frozen 24 subjects")
            tensors = capture_operands(local)
            if self.current["arm"] != A7: tensors.pop("upd_precast")
            self.current.setdefault("capture_tensors", []).append(tensors)
        self.current["captures"].append(row)

    def call(self, *args, **kwargs):
        previous = sys.getprofile()
        R.require(previous is None, "PROFILER", "preexisting profiler is forbidden")
        law5 = self.H._LAW5_DEFAULT_CTX
        arm = "law5" if law5 else self.arm_override
        if arm is None:
            requests = args[1] if len(args) > 1 else kwargs["requests"]
            values = {r["subject"]: r["target_new"]["str"].lstrip() for r in requests}
            arm = next((a for a, v in self.H.ARMS.items() if values == v), "unknown")
        write = dict(arm=arm, tag="law5" if law5 else "science", captures=[], return_count=0)
        self.current = write
        try:
            try:
                sys.setprofile(self.profile)
                result = self.original(*args, **kwargs)
            except Exception as error:
                sys.setprofile(previous)
                self.preserve_failed(write, error)
                raise
            finally:
                sys.setprofile(previous)
            if not law5:
                import torch
                write["native_norm_producer"] = dict(torch_version=str(torch.__version__), cpu_threads=torch.get_num_threads())
                write["returned_native_norms"] = {}; write["returned_native_tensors"] = {}
                for layer, values in (result.items() if isinstance(result, dict) else []):
                    native = values.get("delta_norm") if isinstance(values, dict) else None
                    if native is not None:
                        native = float(native)
                        write["returned_native_norms"][str(layer)] = native if math.isfinite(native) else None
                        write["returned_native_tensors"][f"returned.l{layer}.n_native"] = torch.tensor(native, dtype=torch.float64, device="cpu")
                for row, tensors in zip(write["captures"], write.get("capture_tensors", [])):
                    # A layer-keyed return cannot identify any occurrence of a duplicate layer.
                    if sum(r["layer"] == row["layer"] for r in write["captures"]) == 1:
                        native = write["returned_native_tensors"].get(f"returned.l{row['layer']}.n_native")
                        if native is not None: tensors["n_native"] = native
            if not self.coverage_passes(write["captures"], write["return_count"]):
                self.preserve_failed(write, R.Halt("CAPTURE", "write must have exactly five ordered captures and one return"))
            self.validate_coverage(write["captures"], write["return_count"])
            if "capture_tensors" in write:
                write["tensors"] = {f"l{row['layer']}." + k: v
                    for row, tensors in zip(write["captures"], write.pop("capture_tensors")) for k, v in tensors.items()}
            write.pop("returned_native_tensors", None)
            self.last_capture_count = len(write["captures"])
            self.writes.append(write)
            if self.completed is not None: self.completed(write)
            return result
        finally:
            self.current = None

    @contextlib.contextmanager
    def bound(self):
        R.require(self.H.my_edit is self.original, "PROFILER", "edit was already rebound")
        self.H.my_edit = self.call
        try:
            yield self
        finally:
            self.H.my_edit = self.original


def persist_failed_write(run_dir, write):
    path = Path(run_dir) / "diagnostic_captures" / ("partial_write_" + R.utc_tag() + ".pt")
    path.parent.mkdir(parents=True, exist_ok=True)
    ref = dict(path=str(path), diagnostic_only=True, analysis_eligible=False, status="writing")
    if "native_norm_producer" in write: ref["native_norm_producer"] = write["native_norm_producer"]
    write["artifacts"].append(ref)
    tensors = {f"c{i}.l{row['layer']}." + k: v
        for i, (row, values) in enumerate(zip(write["captures"], write.get("capture_tensors", []))) for k, v in values.items()}
    tensors.update(write.get("returned_native_tensors", {}))
    ref.update(R.save_tensors(path, tensors))
    with path.open("rb") as source:
        os.fsync(source.fileno())
    ref["status"] = "saved"
    write.pop("capture_tensors", None)
    write.pop("returned_native_tensors", None)


def stage_harvest_halt(run, error, observer=None):
    code = error.code if isinstance(error, R.Halt) else "HARVEST-ERROR"
    return R.stage_halt(W, run.directory, code, str(error), step=1,
        details={"projection": run.budget.last_projection, "gates": run.gates,
                 "failed_writes": observer.failure_details() if observer is not None else []})


@contextlib.contextmanager
def lab_pinned_contexts(H, ctx, expected_digest):
    namespace = H.get_context_templates.__globals__
    R.require("CONTEXT_TEMPLATES_CACHE" in namespace and R.json_digest(ctx) == expected_digest,
              "CONTEXT", "expected template digest or engine cache binding missing")
    previous = namespace["CONTEXT_TEMPLATES_CACHE"]
    namespace["CONTEXT_TEMPLATES_CACHE"] = copy.deepcopy(ctx)
    try:
        yield ctx
        R.require(namespace["CONTEXT_TEMPLATES_CACHE"] == ctx, "CONTEXT_PIN_DRIFT", "template cache drifted")
    finally:
        namespace["CONTEXT_TEMPLATES_CACHE"] = previous


def frozen_records(root=W):
    records = {}; provenance = {"seed_sources": {}}
    for seed, arm in enumerate(MINT):
        record_path = Path(root) / BASE / f"F_r0_mint1_s{seed}.json"
        step_path = Path(root) / BASE / f"step0/F_r0_mint1_s{seed}.json"
        target_path = Path(root) / BASE / f"zs/F_r0_mint1_s{seed}.pt"
        records[arm] = None
        identity = dict(record={"path": str(record_path), "sha256": None},
                        step0={"path": str(step_path), "sha256": None},
                        target={"path": str(target_path), "sha256": None}, passed=False)
        try:
            records[arm] = R.read_json(record_path)
            identity["record"]["sha256"] = R.sha_file(record_path)
            step = R.read_json(step_path)
            identity["step0"]["sha256"] = R.sha_file(step_path)
            identity["target"]["sha256"] = R.sha_file(target_path)
            identity["passed"] = (identity["record"]["sha256"] == RECORD_SHAS[seed]
                                  and identity["step0"]["sha256"] == STEP0_SHAS[seed]
                                  and identity["target"]["sha256"] == TARGET_SHAS[seed] == step["zs_file_sha256"])
        except (OSError, ValueError, KeyError) as error:
            identity["reason"] = str(error)
        provenance["seed_sources"][arm] = identity
    multi_path = Path(root) / BASE / "F_r0_multi_snone.json"
    records["multi"] = R.read_json(multi_path)
    provenance["multi"] = {"path": str(multi_path), "sha256": R.sha_file(multi_path)}
    R.require(provenance["multi"]["sha256"] == "0ec55d879fc592512ed437099c522cf94d652ab54b7d85f1ccc2781b34a637ab",
              "CONTEXT", "multi record source identity changed")
    R.require(provenance["seed_sources"][MINT[0]]["record"]["sha256"] == RECORD_SHAS[0],
              "CONTEXT", "the authoritative frozen s0 /ctx source is missing or changed")
    context_arm = MINT[0]
    provenance["context_source_arm"] = context_arm
    provenance["context_source"] = dict(provenance["seed_sources"][context_arm]["record"], json_pointer="/ctx")
    ctx = records[context_arm]["ctx"]
    provenance["ctx_sha256"] = R.json_digest(ctx)
    provenance["c10x_context_sha256"] = hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
    provenance["contexts_shared"] = provenance["ctx_sha256"] == CTX_SHA and records["multi"]["ctx"] == ctx and all(
        records[a]["ctx"] == ctx for seed, a in enumerate(MINT)
        if provenance["seed_sources"][a]["record"]["sha256"] == RECORD_SHAS[seed])
    return records, provenance


def p2_equivalent(current, saved):
    keys = ("ok", "checks", "changed", "inventory_n", "plain_n", "rows")
    return (current.get("ok") is True and current.get("changed") == []
            and current.get("inventory_n") == 2376 and current.get("plain_n") == 396
            and all(current.get(k) == saved.get(k) for k in keys))


def lookup_contract(base, minted, contexts, requests, lookup):
    details = []
    for request in requests:
        for template in [t for group in contexts for t in group]:
            form = template.format(request["prompt"]); subject = request["subject"]
            prefix, suffix = form.split("{}")
            word = subject
            if prefix:
                R.require(prefix.endswith(" "), "TOKENISATION", "engine lookup prefix lacks trailing space")
                prefix = prefix[:-1]; word = " " + subject.strip()
            base_ids = base([prefix, word, suffix])["input_ids"]
            minted_ids = minted([prefix, word, suffix])["input_ids"]
            left = lookup(base, [form], [subject], "last")[0][0]
            right = lookup(minted, [form], [subject], "last")[0][0]
            details.append(dict(template=form, subject=subject, substring_ids=base_ids, subject_last=left,
                                label="RECONSTRUCTED", passed=base_ids == minted_ids and left == right))
    return dict(passed=all(r["passed"] for r in details), rows=details)


def tokenizer_identity(tokenizer):
    backend = copy.deepcopy(tokenizer.backend_tokenizer)
    backend.no_padding(); backend.no_truncation()
    return backend.to_str()


def tokenisation_contract(H, records, contexts, root=W, eligible=None):
    from transformers import AutoTokenizer
    from huggingface_hub import try_to_load_from_cache
    sys.path.insert(0, str(Path(root) / "experiments/track_c"))
    U = importlib.import_module("c10u_mint2_arms")
    M = importlib.import_module("c10l_mint_lib")
    from rome.repr_tools import get_words_idxs_in_templates
    sources = {name: R.sha_file(Path(root) / name) for name in AUDIT_SOURCES}
    eligible = list(MINT) if eligible is None else eligible
    source_ok = all(all(records[a]["identity"]["source_sha256"].get(name) == sha for name, sha in sources.items()) for a in eligible)
    result = {"parts": {"audit-source-identity": {"passed": source_ok, "observed": dict(sources=sources, checked_arms=eligible)}}}
    if not source_ok:
        result["passed"] = False; return result
    identity_ok = H.ID == MODEL_ID and H.REV == MODEL_REV
    tokenizer_files = {}
    for name in ("tokenizer.json", "tokenizer_config.json"):
        path = try_to_load_from_cache(MODEL_ID, name, revision=MODEL_REV, cache_dir=str(Path(root) / "hf_cache/hub"))
        R.require(isinstance(path, str) and Path(path).is_file(), "TOKENISATION", "pinned tokenizer file missing: " + name)
        tokenizer_files[name] = dict(path=path, sha256=R.sha_file(path))
    # A fresh tokenizer verifies the live harness tokenizer against its pinned identity.
    base = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REV, local_files_only=True)
    identity_ok = identity_ok and tokenizer_identity(H.tok) == tokenizer_identity(base)
    result["parts"]["a-pinned-tokenizer"] = dict(passed=identity_ok, observed=tokenizer_files)
    if not identity_ok:
        result["passed"] = False; return result
    prompts, _, _ = U.audit_prompts(H, M, Path(root))
    for arm in eligible:
        record = records[arm]; minted = copy.deepcopy(base)
        try:
            ids = M.register(minted, record["minted_words"])
            registration_ok = ids == record["minted_ids"]
            p2 = U.p2_audit(base, minted, record["minted_words"], ids, record["values"], H.FICTION,
                            U.FRAME_SUBJECTS, contexts, prompts, "mint1", "F")
            requests = [H.req(H.CANON, subject, record["values"][subject]) for subject in H.FICTION]
            substrings = lookup_contract(base, minted, contexts, requests, get_words_idxs_in_templates)
            result["parts"]["b-registration-" + arm] = dict(passed=registration_ok, observed=ids)
            result["parts"]["c-audit-" + arm] = dict(passed=p2_equivalent(p2, record["admission"]["P2"]), observed=p2)
            result["parts"]["d-substrings-" + arm] = dict(passed=substrings["passed"], observed=substrings)
        except (ValueError, SystemExit, AssertionError) as error:
            result["parts"]["tokenisation-" + arm] = dict(passed=False, observed=str(error))
    result["passed"] = all(p["passed"] for p in result["parts"].values())
    return result


def replay_admission(shared_passed, seed_passed):
    arms = {arm: "ADMITTED" if shared_passed and seed_passed.get(arm, False) else "INVALID-REPLAY" for arm in MINT}
    return dict(shared_passed=bool(shared_passed), arms=arms, admitted=[a for a in MINT if arms[a] == "ADMITTED"])


def source_snapshot(root=W):
    root = Path(root)
    names = [*AUDIT_SOURCES, "docs/MATHLAB_PREREG.md", "configs/hparams/qwen25_3b_memit_hparams.json",
             "memit_dry_run/memit/globals.yml", "tools/mathlab_admit.py", "tools/mathlab_runtime.py",
             "tools/mathlab_harvest.py", "tools/mathlab_events.py", "tools/c10w_p2_gate.py", "tools/engine_fingerprint.py"]
    names += [str(p.relative_to(root)) for p in (root / "memit_dry_run/memit").rglob("*.py")]
    return {name: R.sha_file(root / name) for name in names}


def norm_agreement(tensors, norms):
    rows = {}
    for layer in BAND:
        expected = norms.get(str(layer), {}).get("delta_norm"); actual = tensors.get(f"l{layer}.n_native")
        expected = float(expected) if expected is not None else None
        actual = float(actual) if actual is not None else None
        expected = expected if expected is not None and math.isfinite(expected) else None
        actual = actual if actual is not None and math.isfinite(actual) else None
        error = abs(actual - expected) / expected if actual is not None and expected is not None and expected > 0 else None
        error = error if error is not None and math.isfinite(error) else None
        rows[str(layer)] = dict(actual=actual, expected=expected, relative_error=error,
                               passed=error is not None and error <= 1e-3)
    return dict(passed=all(r["passed"] for r in rows.values()), layers=rows,
                interpretation="Norm consistency, not tensor identity")


def baseline_gates(arms):
    checks = {A1: arms[A1]["para_full_n"] >= 68 and arms[A1]["para_n"] == 72,
              A2: arms[A2]["para_full_n"] >= 68 and arms[A2]["para_n"] == 72,
              A7: (5 <= arms[A7]["para_full_n"] <= 18 and 42 <= arms[A7]["para_first_n"] <= 59
                   and 5 <= arms[A7]["canon_full_n"] <= 10 and arms[A7]["para_n"] == 72 and arms[A7]["canon_n"] == 24)}
    return dict(passed=all(checks.values()), arms=checks)


def fresh_before_mint(fresh_gate, replay):
    R.require(fresh_gate()["passed"], "LAW3", "fresh baseline gates must pass before any mint replay")
    return replay()


def parity_trial(H, hp, requests, P, original, observed, zs, pristine):
    import torch
    old_z = H.Z_OVERRIDE
    H.Z_OVERRIDE = {(r["subject"], r["target_new"]["str"]): zs[:, i] for i, r in enumerate(requests)}
    try:
        snapshots = []
        for fn in (original, observed.call):
            H.restore_layers(hp, pristine)
            cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in hp.layers]
            fn(hp, requests, P, cache)
            snapshots.append({l: cpu_copy(v) for l, v in H.snap_layers(hp).items()})
        before = {l: cpu_copy(v) for l, v in pristine.items()}; rows = {}
        for l in hp.layers:
            exact = torch.equal(snapshots[0][l], snapshots[1][l])
            u, o = snapshots[0][l].double() - before[l].double(), snapshots[1][l].double() - before[l].double()
            denominator = float(torch.linalg.vector_norm(u))
            error = float(torch.linalg.vector_norm(o - u)) / denominator if denominator else None
            rows[str(l)] = dict(branch="torch.equal" if exact else "relative-delta", relative_error=error,
                                passed=exact or error is not None and error <= 1e-6)
        return dict(passed=observed.last_capture_count == 5 and all(r["passed"] for r in rows.values()),
                    capture_count=observed.last_capture_count, layers=rows)
    finally:
        H.restore_layers(hp, pristine); H.Z_OVERRIDE = old_z


def conversion_selftest(device):
    import torch
    x = torch.arange(96, dtype=torch.float16, device=device).reshape(4, 6, 4)
    before = x.cpu().clone(); results = []
    for name, view in [("offset", x[1:]), ("last-position", x[0, -1]),
                       *[("chunk" + str(i), v) for i, v in enumerate(x.chunk(3, 1))], ("transposed", x.transpose(0, 2))]:
        reference = view.cpu(); captured = cpu_copy(view)
        results.append(dict(view=name, passed=torch.equal(reference, captured) and torch.equal(before, x.cpu())))
    return dict(device=str(device), passed=all(r["passed"] for r in results), views=results)


def prompt_specs(H):
    specs = []
    groups = [("CANON", H.FICTION, [H.CANON]), ("PTEST", H.FICTION, H.PTEST),
              ("described_as", H.FICTION, ["{} is described as"]),
              ("L1", H.L1_COUNTRIES, [H.CANON]), ("L3", H.L3_COUNTRIES, [H.CANON])]
    for kind, subjects, templates in groups:
        for f, subject in enumerate(subjects):
            for j, template in enumerate(templates):
                specs.append(dict(key=f"p{len(specs):03d}", kind=kind, subject_id=f, template_id=j,
                                  subject=subject, template=template, text=template.format(subject)))
    return specs


def capture_prompts(H, specs, layers, run, stage):
    import torch
    from memit.compute_z import find_fact_lookup_idx
    result = {}; handles = []; current = [None]
    def pre(layer):
        def capture(module, inputs): result[f"{current[0]}.l{layer}.k"] = cpu_copy(inputs[0][0])
        return capture
    def post(layer):
        def capture(module, inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            result[f"{current[0]}.l{layer}.h"] = cpu_copy(hidden[0])
        return capture
    try:
        for layer in layers:
            handles.append(H.model.model.layers[layer].mlp.down_proj.register_forward_pre_hook(pre(layer)))
            handles.append(H.model.model.layers[layer].register_forward_hook(post(layer)))
        with torch.no_grad():
            for i, spec in enumerate(specs):
                current[0] = spec["key"]
                tokens = H.tok(spec["text"], return_tensors="pt")
                R.require(tokens["input_ids"].shape[0] == 1, "BATCH", "capture must be one prompt, no padding")
                result[spec["key"] + ".ids"] = cpu_copy(tokens["input_ids"][0])
                index = find_fact_lookup_idx(spec["template"], spec["subject"], H.tok, "subject_last", verbose=False)
                result[spec["key"] + ".subject_last"] = torch.tensor(index, dtype=torch.int64)
                H.model(**tokens.to(H.DEV))
                run.event("progress", stage=stage, done=i + 1, total=len(specs), unit="prompts recorded")
    finally:
        for handle in handles: handle.remove()
    return result


def capture_context_keys(H, hp, ctx, requests, prefix):
    import torch
    result = {}; lengths = [len(g) for g in ctx]; context_n = sum(lengths)
    for layer in hp.layers:
        keys = H.get_module_input_output_at_words(H.model, H.tok, layer,
            context_templates=[t.format(r["prompt"]) for r in requests for group in ctx for t in group],
            words=[r["subject"] for r in requests for group in ctx for t in group],
            module_template=hp.rewrite_module_tmp, fact_token_strategy=hp.fact_token)[0]
        averages = []
        for f in range(len(requests)):
            offset = f * context_n; groups = []
            for n in lengths:
                groups.append(keys[offset:offset + n].mean(0)); offset += n
            averages.append(torch.stack(groups, 0).mean(0))
        result[f"{prefix}.k{layer}.templates"] = cpu_copy(keys)
        result[f"{prefix}.k{layer}.mean"] = cpu_copy(torch.stack(averages, dim=0).T)
    return result


def harvest(run_dir, admission_path):
    run = R.Run(run_dir, 1, "Record inputs to the model's write calculation", 3600, attach=True)
    files = {}; manifest = dict(tier=R.TIER, decision_id="D-ML-1", prereg_sha256=R.PREREG_SHA)
    H = None; hp = None; pristine = None; observer = None
    try:
        R.verify_prereg(W)
        from tools.mathlab_admit import dispatch_check
        admission = dispatch_check(run_dir, "harvest", admission_path)
        run.gate("admission", "Lead queue and machine checks allow the harvest", admission,
                 "allowed", admission["allowed"], fatal=True)
        R.enforce_stop_policy(W, 1, exclude=run_dir)
        with run.stage("setup", "Check inputs and prepare the unchanged harness", 900, alarm=True):
            records, identity = frozen_records(W); ctx = records[identity["context_source_arm"]]["ctx"]
            run.gate("context", "All arms use the frozen historical context templates", identity["ctx_sha256"], CTX_SHA,
                     identity["ctx_sha256"] == CTX_SHA, fatal=True)
            source_start = source_snapshot(W)
            R.require(os.environ.get("C10_CTX_TEMPLATES") is None, "ENVIRONMENT", "C10_CTX_TEMPLATES must be unset")
            for key in ("C10_KEY_LOCUS", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "HP_CANDIDATE", "C10_RECIPES"):
                R.require(key not in os.environ, "ENVIRONMENT", "inherited harness knob: " + key)
            os.environ.update(LLMDB_ROOT=str(W), MODEL_ID=MODEL_ID, MODEL_REV=MODEL_REV,
                              C10_ARMS=",".join((A1, A2, A7)), LLMDB_DEVICE="mps")
            R.require(importlib.metadata.version("torch") == "2.8.0", "VERSION", "harvest requires torch 2.8.0")
            sys.path.insert(0, str(W / "experiments/track_c"))
            H = importlib.import_module("c10e_bandknob")  # The sole model import, after shell admission.
            hp = H.MEMITHyperParams.from_json(H.HP_BASE)
            R.require(hp.layers == BAND and len(H.FICTION) == 24, "BAND", "frozen band or subjects differ")
            pristine = H.snap_layers(hp)
            selftest = conversion_selftest(H.DEV)
            run.gate("conversion-selftest", "Recording offset tensor views preserves values and the source", selftest,
                     "every view bitwise unchanged", selftest["passed"], fatal=True)
            output = R.new_directory(W / "results/mathlab", "harvest")
            specs = prompt_specs(H)
        saved = {}; law5_writes = []
        def completed(write):
            run.gate("coverage-" + write["arm"], "Exactly five layer records in order and one return",
                     dict(captures=write["captures"], returns=write["return_count"]), "(0,4)…(4,8), one return", True)
            if write["tag"] == "law5": law5_writes.append(write); return
            arm = write["arm"]
            if arm.startswith("parity-"): return
            R.require(arm in [A1, A2, A7, *MINT], "ARM", "unknown science arm")
            tensors = write.pop("tensors"); saved[arm] = tensors
            files[f"inloop_{arm}.pt"] = R.save_tensors(output / f"inloop_{arm}.pt", tensors)
            files[f"inloop_{arm}.pt"]["native_norm_producer"] = write["native_norm_producer"]
        observer = EditObserver(H, completed, lambda write: persist_failed_write(run.directory, write))
        old_hooks = list(H.ARM_HOOKS)
        def post_hook(arm, values):
            with run.stage("postedit", "Record the edited model before restoring its weights", 300, alarm=True):
                tensors = capture_prompts(H, [p for p in specs if p["kind"] in ("CANON", "PTEST")], [8], run, "postedit")
                requests = [H.req(H.CANON, c, values[c]) for c in H.FICTION]
                tensors.update(capture_context_keys(H, hp, ctx, requests, "post"))
                files[f"postedit_{arm}.pt"] = R.save_tensors(output / f"postedit_{arm}.pt", tensors)
                if arm == A7:
                    after = H.snap_layers(hp)
                    files["weights_A7.pt"] = R.save_tensors(output / "weights_A7.pt",
                        {f"l{l}.{which}": cpu_copy(v) for which, snap in (("before", pristine), ("after", after)) for l, v in snap.items()})
            return {}
        try:
            with lab_pinned_contexts(H, ctx, CTX_SHA), observer.bound():
                with run.stage("clean", "Record the unedited model one prompt at a time", 300, alarm=True):
                    clean = capture_prompts(H, specs, BAND, run, "clean")
                    requests = [H.req(H.CANON, c, H.ARMS[A7][c]) for c in H.FICTION]
                    clean.update(capture_context_keys(H, hp, ctx, requests, "clean"))
                    files["clean.pt"] = R.save_tensors(output / "clean.pt", clean)
                    del clean
                H.ARM_HOOKS.append(post_hook)
                with run.stage("fresh", "Run three fresh baselines and their evaluations", 1800, alarm=True):
                    fresh = H.run_recipe("baseline", H.HP_BASE)
                run.gate("law5", "The observer preserves the harness's engine comparison", fresh["law5_gate"],
                         {"expr_delta_lt": .05, "loc_delta_lt": 3, "tagged_captures": 5},
                         fresh["law5_gate"]["ok"] and bool(law5_writes), fatal=True)
                gates = baseline_gates(fresh["arms"])
                for arm, passed in gates["arms"].items():
                    run.gate("law3-" + arm, "Fresh measured baseline matches its frozen range", fresh["arms"][arm],
                             {"para_full_min": 68} if arm != A7 else {"para_full": [5, 18], "para_first": [42, 59], "canon": [5, 10]}, passed)
                run.gate("law3", "All fresh baselines pass before mint replay", gates, "all three pass", gates["passed"], fatal=True)
                with run.stage("setup", "Compare observed and unobserved writes on pristine weights", 900, alarm=True):
                    H.restore_layers(hp, pristine); P = H.compute_P(hp)
                    observer.arm_override = "parity-A7"
                    parity = parity_trial(H, hp, requests, P, observer.original, observer, saved[A7]["l4.zs"], pristine)
                    observer.arm_override = None
                    run.gate("observer-parity", "Recording operands leaves the applied write unchanged", parity,
                             "bitwise equal or relative deployed-delta error <= 1e-6", parity["passed"], fatal=True)
                with run.stage("mint", "Check historical replay identity, then record each admitted write", 300, alarm=True):
                    eligible = [a for seed, a in enumerate(MINT) if identity["seed_sources"][a]["record"]["sha256"] == RECORD_SHAS[seed]]
                    tokenisation = tokenisation_contract(H, records, ctx, W, eligible=eligible)
                    for part, check in tokenisation["parts"].items():
                        run.gate("tokenisation-" + part, "Historical and reconstructed tokenisation agree: " + part,
                                 check["observed"], "exact frozen identity", check["passed"])
                    shared_ok = identity["contexts_shared"] and tokenisation["passed"]
                    run.gate("mint-shared-context", "All historical mint records share the same templates", identity["contexts_shared"], True, identity["contexts_shared"])
                    seed_ok = {}; replay_norms = {}
                    for seed, arm in enumerate(MINT):
                        source = identity["seed_sources"][arm]
                        run.gate("mint-source-" + arm, "Historical record and target file identities match", source, "frozen SHA-256s", source["passed"])
                        seed_ok[arm] = False
                        if not shared_ok or not source["passed"]: continue
                        import torch
                        zs = torch.load(source["target"]["path"], map_location="cpu", weights_only=True)
                        R.require(zs.shape == (24, 2048), "TARGET", "historical target rows must follow the frozen subject order")
                        values = records[arm]["values"]; requests_m = [H.req(H.CANON, c, values[c]) for c in H.FICTION]
                        H.restore_layers(hp, pristine)
                        old_z = H.Z_OVERRIDE; observer.arm_override = arm
                        try:
                            H.Z_OVERRIDE = {(c, requests_m[i]["target_new"]["str"]): zs[i] for i, c in enumerate(H.FICTION)}
                            H.my_edit(hp, requests_m, P, [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in BAND])
                            post_hook(arm, values)
                        finally:
                            H.restore_layers(hp, pristine); H.Z_OVERRIDE = old_z; observer.arm_override = None
                        agreement = norm_agreement(saved[arm], records[arm]["recipe"]["delta_norms"]["candidate"])
                        replay_norms[arm] = agreement; seed_ok[arm] = agreement["passed"]
                        run.gate("mint-norm-" + arm, "Replayed layer update norms agree with this seed's record", agreement,
                                 "relative norm difference <= 1e-3; not tensor identity", agreement["passed"])
                        run.event("progress", stage="mint", done=seed + 1, total=3, unit="historical seeds checked")
                    admission_result = fresh_before_mint(lambda: gates, lambda: replay_admission(shared_ok, seed_ok))
        finally:
            H.ARM_HOOKS[:] = old_hooks
            H.restore_layers(hp, pristine)
        source_end = source_snapshot(W)
        run.gate("source-unchanged", "Harness, engine and frozen inputs remained unchanged", source_end, source_start,
                 source_end == source_start, fatal=True)
        outcomes = {a: dict(used_for_calibration=fresh["arms"][a]["para_full_n"],
                           fresh_harvest_count=fresh["arms"][a]["para_full_n"],
                           historical_count_report_only="68–72 across runs; 68 in block F" if a == A1 else ">=70" if a == A2 else "14 in block F; 8–15 across observations") for a in (A1, A2, A7)}
        for arm in MINT:
            historical = records[arm]["arm"]["para_full_binding_n"] if arm in eligible else None
            outcomes[arm] = dict(used_for_calibration=records[arm]["arm"]["para_full_binding_n"] if arm in admission_result["admitted"] else None,
                                fresh_harvest_count=None, historical_count_report_only=historical,
                                historical_source_status="VERIFIED" if arm in eligible else "UNVERIFIABLE")
        reported_norms = {A1: norm_agreement(saved[A1], records[MINT[0]]["recipe"]["delta_norms"]["A1_single"]) if MINT[0] in eligible else
                             {"status": "UNVERIFIABLE", "reason": "seed-0 historical source is unavailable or changed"},
                          A7: norm_agreement(saved[A7], records["multi"]["recipe"]["delta_norms"]["candidate"])}
        command = __import__("subprocess").run(["git", "-C", str(W), "rev-parse", "HEAD"], capture_output=True, text=True)
        R.require(command.returncode == 0 and command.stdout.strip(), "GIT", "cannot record commit identity")
        manifest.update(files=files, prompts=specs, gates=run.gates, identity=identity, source_start=source_start, source_end=source_end,
                        git_commit=command.stdout.strip(), torch_version="2.8.0", fingerprint=admission["checks"]["fingerprint"],
                        covariances=fresh["cov_cache_sha256"], tokenisation=tokenisation, selftest=selftest,
                        replay_admission=admission_result, outcomes=outcomes, fresh_norm_consistency_report_only=reported_norms,
                        mint_norms=replay_norms, subject_indices_label="RECONSTRUCTED")
        R.write_new(output / "manifest.json", manifest)
        R.stage_finding(W, run_dir, "harvest", "Operand harvest completed; math-proxy analysis remains pending")
        run.event("run_finished", outcome="PASS", summary="Operand harvest completed; no behavioural promotion")
        return manifest
    except Exception as error:
        stage_harvest_halt(run, error, observer)
        raise
    finally:
        if H is not None and pristine is not None: H.restore_layers(hp, pristine)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--admission", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    # A driver invocation without the launcher's staged admission never imports the harness.
    result = R.read_json(args.run_dir / "admission.json")
    R.require(result["allowed"] and result["kind"] == "harvest", "ADMISSION", "shell admission missing or refused")
    harvest(args.run_dir, args.admission)


if __name__ == "__main__":
    main()
