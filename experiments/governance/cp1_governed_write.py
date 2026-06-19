#!/usr/bin/env python3
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""
cp1_governed_write.py — CHECKPOINT 1: governed, IN-PIPELINE MEMIT write (viability prototype).

WHAT CP1 PROVES (and does NOT prove)
------------------------------------
OPEN question (CORPUS 03/06, CP1): we proved the edit MATH + OFFLINE serving + the
decoupled bridge. We did NOT prove a MEMIT compile running as a FIRST-CLASS, IN-PIPELINE
step behind a Patch Authorization Gate / Commit Executor, with ledger entries, that
*fails cleanly*. The spec wants exactly this (§9.10 Commit Executor, §10.2 Gate, §11.5 2PC);
it ELIMINATED n8n (D70) precisely for not hosting "multi-minute GPU-bound MEMIT compile as a
first-class step." Our earlier bridge ran the compile OUT-OF-BAND — as a production path that
is a C16 violation ("direct filesystem writes to .vindex bypass the gate"). CP1 closes that gap.

SCOPE (operator decision, 2026-06-18): PARAMETRIC-ONLY. CP1 gates+commits the .vindex
(parametric) write and proves clean-fail atomicity ON THAT SIDE. The Commit Executor's
*defining* dual-medium property (§9.10: simultaneous Git+engine write, D46 Git-first ordering)
is represented here only as a STRUCTURAL PLACEHOLDER (git_prepare step, no-op) and is
explicitly DEFERRED TO G1. CP1 must NOT be read as proving dual-medium 2PC.

The NEW thing under test (everything else is already banked: A1-A5, L-BRIDGE):
  (T-POS)  authorized patch -> in-step GPU compile -> overlay applied -> post-write probe
           -> PREPARED + COMMITTED emitted, chain intact.
  (T-GATE) bad signature / tampered patch-hash / out-of-scope -> HARD REJECT, NO compile,
           NO COMMITTED, WRITE_REJECTED logged. (A gate that only ever passes is not a gate.)
  (T-ATOM) authorized patch but compile THROWS mid-step -> PREPARED stays, NO COMMITTED,
           base .vindex bytes unchanged, no overlay mounted. (THE n8n question.)
  (T-DET)  same patch twice -> identical overlay hash; no LLM in the executor loop (C-OR2).

HONEST STUBS (flagged, not hidden):
  * Orchestrator signing key is HMAC-SHA256 (symmetric) standing in for the spec's asymmetric
    Orchestrator key (§10.5). Sufficient to test the Gate's signature/replay/scope logic; real
    asymmetric signing is a G2 concern.
  * Post-write probe is a BEHAVIORAL read-back (`larql run`) standing in for the spec's
    mandatory L1 SELECT storage read-back (§8.9) — because SELECT capability is exactly what
    CP2 has not yet proven. Flagged CP2-dependent.
  * git_prepare() is a no-op placeholder for the dual-medium write (G1).

Engine UNMODIFIED (LAW#1). All governance is our-own-code wrapping the recipe.
"""
import os, sys, io, json, math, time, hmac, hashlib, base64, contextlib, shutil, subprocess, traceback
import numpy as np

# ---- engine import (must set path + chdir before importing memit, per s247) ----
ENGINE_ROOT = f"{LLMDB_ROOT}/memit_dry_run/memit"
sys.path.insert(0, ENGINE_ROOT)
os.environ.setdefault("HF_HOME", f"{LLMDB_ROOT}/hf_cache")
os.environ.setdefault("HF_HUB_OFFLINE", "0")
import torch

# ---- paths / constants ----
MODEL_DIR   = "/dev/shm/qwen3_model"
HPARAMS     = f"{LLMDB_ROOT}/configs/hparams/qwen3_06b_memit_hparams.json"
FROZEN_BASE = "/dev/shm/qwen3.vindex"            # frozen base vindex (positive control verified)
LARQL       = f"{LLMDB_ROOT}/external_prior_art/larql/target/release/larql"
WORK        = "/dev/shm/cp1_work"                # scratch for overlays + compiled vindexes
LEDGER_PATH = f"{LLMDB_ROOT}/results/cp1_state_ledger.jsonl"
RESULT_PATH = f"{LLMDB_ROOT}/results/cp1_result.json"
NULL_THRESH = 5e-3
SEED        = 1234
DOWN_TMPL   = "model.layers.{}.mlp.down_proj.weight"


# ════════════════════════════════════════════════════════════════════════════
#  STATE LEDGER  (§11.15 / §16) — append-only, hash-chained (Merkle-style prev_hash)
# ════════════════════════════════════════════════════════════════════════════
def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

class StateLedger:
    """Append-only JSONL. Each entry carries prev_hash + entry_hash = sha256(prev_hash+body).
    Tamper/break in the chain is detectable by verify_chain(). Token replay is detected by
    scanning for a prior TOKEN_CONSUMED with the same token_id (§10.2 pre-check #3)."""
    GENESIS = "0" * 64

    def __init__(self, path):
        self.path = path
        open(self.path, "w").close()          # fresh ledger per CP1 run (forensic isolation)
        self._tip = self.GENESIS

    def append(self, entry_type, body):
        entry = {"seq": self._count(), "ts": round(time.time(), 3),
                 "entry_type": entry_type, "prev_hash": self._tip, "body": body}
        entry["entry_hash"] = _sha(entry["prev_hash"] + _canon(body))
        with open(self.path, "a") as f:
            f.write(_canon(entry) + "\n")
        self._tip = entry["entry_hash"]
        return entry

    def _count(self):
        with open(self.path) as f:
            return sum(1 for _ in f)

    def entries(self):
        with open(self.path) as f:
            return [json.loads(l) for l in f if l.strip()]

    def token_consumed(self, token_id):
        return any(e["entry_type"] == "TOKEN_CONSUMED" and e["body"].get("token_id") == token_id
                   for e in self.entries())

    def verify_chain(self):
        tip = self.GENESIS
        for e in self.entries():
            if e["prev_hash"] != tip:
                return False, f"prev_hash break at seq {e['seq']}"
            if e["entry_hash"] != _sha(e["prev_hash"] + _canon(e["body"])):
                return False, f"body tampered at seq {e['seq']}"
            tip = e["entry_hash"]
        return True, "chain intact"

    def has(self, entry_type, **match):
        for e in self.entries():
            if e["entry_type"] == entry_type and all(e["body"].get(k) == v for k, v in match.items()):
                return True
        return False


# ════════════════════════════════════════════════════════════════════════════
#  ORCHESTRATOR + TOKENS (§10.4, §10.5)  — HMAC stand-in for asymmetric key (flagged)
# ════════════════════════════════════════════════════════════════════════════
class Orchestrator:
    """Mints invocation-scoped single-use tokens, Orchestrator-signed. The token is a WITNESS
    to governance state at issuance (§10.4): it binds agent_id, the patch_hash, the write-scope
    hash, and a TTL. Anchored once in the ledger as ORCHESTRATOR_KEY_ANCHOR (§10.5 dual-store —
    here single-store stub)."""
    def __init__(self, ledger, write_scopes, ttl_s=600):
        self._key = hashlib.sha256(b"cp1-orchestrator-signing-key-STUB").digest()
        self.ledger = ledger
        self.write_scopes = write_scopes          # {agent_id: WriteScopeDefinition}
        self.ttl_s = ttl_s
        self.write_scope_hash = _sha(_canon(write_scopes))
        ledger.append("ORCHESTRATOR_KEY_ANCHOR",
                      {"key_fingerprint": _sha(self._key.hex()), "write_scope_hash": self.write_scope_hash})

    def _sign(self, payload: dict) -> str:
        return hmac.new(self._key, _canon(payload).encode(), hashlib.sha256).hexdigest()

    def mint_token(self, agent_id, patch_hash, ttl_s=None):
        payload = {"token_id": _sha(f"{agent_id}{patch_hash}{time.time()}")[:24],
                   "agent_id": agent_id, "patch_hash": patch_hash,
                   "write_scope_hash": self.write_scope_hash,
                   "issued_at": round(time.time(), 3),
                   "expires_at": round(time.time() + (ttl_s or self.ttl_s), 3)}
        return {**payload, "signature": self._sign(payload)}

    def verify_sig(self, token) -> bool:
        payload = {k: token[k] for k in token if k != "signature"}
        return hmac.compare_digest(self._sign(payload), token.get("signature", ""))


# ════════════════════════════════════════════════════════════════════════════
#  PATCH AUTHORIZATION GATE (§10.2, C16, C-GATE)  — mandatory & exclusive
# ════════════════════════════════════════════════════════════════════════════
class GateReject(Exception):
    def __init__(self, code, detail=""):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail

class PatchAuthorizationGate:
    """No patch reaches the write engine without passing ALL checks in sequence (§10.2).
    Failure at any check is HARD rejection; partial write prohibited. The Gate is the ONLY
    entrance to the Commit Executor in this program (C16: there is no other code path that
    invokes compile)."""
    def __init__(self, orch: Orchestrator, ledger: StateLedger):
        self.orch, self.ledger = orch, ledger

    def authorize(self, token, package):
        patch_hash = package["patch_hash"]
        agent_id   = token.get("agent_id")
        try:
            # --- pre-checks (§10.2) ---
            if not self.orch.verify_sig(token):
                raise GateReject("TOKEN_SIGNATURE_INVALID")                      # #1
            if time.time() > token.get("expires_at", 0):
                raise GateReject("TOKEN_EXPIRED")                                # #2
            if self.ledger.token_consumed(token["token_id"]):
                raise GateReject("TOKEN_REPLAY")                                 # #3
            if token.get("write_scope_hash") != self.orch.write_scope_hash:
                raise GateReject("WRITE_SCOPE_HASH_MISMATCH")                    # #4
            # --- core checks (§10.2 #9-#11) ---
            if token.get("patch_hash") != patch_hash:
                raise GateReject("INTEGRITY_TOKEN_PATCH_MISMATCH")              # identity<->patch binding
            actual = _sha(_canon(package["patch_body"]))
            if actual != patch_hash:                                            # #11 Integrity
                raise GateReject("INTEGRITY_HASH_MISMATCH",
                                 f"declared {patch_hash[:8]} != actual {actual[:8]}")
            scope = self.orch.write_scopes.get(agent_id)
            if scope is None:
                raise GateReject("UNKNOWN_AGENT")
            self._scope_check(scope, package["patch_body"])                      # #10 Scope
        except GateReject as r:
            self.ledger.append("WRITE_REJECTED",
                               {"token_id": token.get("token_id"), "agent_id": agent_id,
                                "patch_hash": patch_hash, "reject_code": r.code, "detail": r.detail})
            raise
        # ACCEPT: emit single-use consumption record (§10.2 #3 basis for future replay check)
        self.ledger.append("TOKEN_CONSUMED",
                           {"token_id": token["token_id"], "agent_id": agent_id, "patch_hash": patch_hash})
        return True

    @staticmethod
    def _scope_check(scope, body):
        if body["tier"] not in scope["tiers"]:
            raise GateReject("SCOPE_TIER_FORBIDDEN", body["tier"])
        if body["content_classification"] not in scope["classifications"]:
            raise GateReject("SCOPE_CLASSIFICATION_FORBIDDEN", body["content_classification"])
        for r in body["edits"]:
            if r["relation"] not in scope["relations"]:
                raise GateReject("SCOPE_RELATION_FORBIDDEN", r["relation"])


# ════════════════════════════════════════════════════════════════════════════
#  WRITE ENGINE — the recipe compile (alpha_edit, band [4-8]) hosted IN-STEP
# ════════════════════════════════════════════════════════════════════════════
class RecipeEngine:
    """Loads Qwen3-0.6B once; computes the null-space projector P from CACHED covariances
    (D20 orthogonal-projection safeguard); runs in-solve AlphaEdit for a patch. This is the
    GPU-bound compile the spec wants hosted as a first-class pipeline step. Deterministic:
    seeded, cached covs, no sampling in the solve."""
    def __init__(self):
        cwd = os.getcwd(); os.chdir(ENGINE_ROOT)        # engine reads globals.yml + stats dirs relative to cwd
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            from memit.memit_hparams import MEMITHyperParams
            from memit.memit_main import get_cov, get_context_templates
            self._get_context_templates = get_context_templates
            self.hp = MEMITHyperParams.from_json(HPARAMS)
            self.L = self.hp.layers
            self.tok = AutoTokenizer.from_pretrained(MODEL_DIR)
            if self.tok.pad_token is None:
                self.tok.pad_token = self.tok.eos_token
            self.model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, torch_dtype=torch.float16).to("cuda").eval()
            self.WN = lambda layer: f"{self.hp.rewrite_module_tmp.format(layer)}.weight"
            print("  [engine] computing P from cached covariances ...", flush=True)
            self.P = []
            for layer in self.L:
                cov = get_cov(self.model, self.tok, self.hp.rewrite_module_tmp.format(layer),
                              self.hp.mom2_dataset, self.hp.mom2_n_samples, self.hp.mom2_dtype).cuda().float()
                U, S, _ = torch.linalg.svd(cov, full_matrices=False)
                idx = (S < NULL_THRESH).nonzero(as_tuple=True)[0]
                self.P.append((U[:, idx] @ U[:, idx].T).cpu())
                del cov, U, S; torch.cuda.empty_cache()
            self.ctx = get_context_templates(self.model, self.tok)
            self.base_band = self._snapshot()           # frozen base band (for restore + change-detect)
        finally:
            os.chdir(cwd)

    def _snapshot(self):
        npd = dict(self.model.named_parameters())
        return {layer: npd[self.WN(layer)].detach().clone() for layer in self.L}

    def _restore(self):
        with torch.no_grad():
            npd = dict(self.model.named_parameters())
            for layer in self.L:
                npd[self.WN(layer)][...] = self.base_band[layer]

    def compile_patch(self, edits, fault=None):
        """Run the recipe for `edits` (list of {prompt, subject, target}). Returns band down_proj
        numpy arrays for the edited model. `fault='mid_compile'` raises after the first band layer
        is mutated (atomicity test: a partially-applied in-memory edit MUST NOT leak to a commit).
        Always restores base band before returning/raising."""
        from memit.memit_main import upd_matrix_match_shape
        from memit.compute_z import compute_z, get_module_input_output_at_words
        from memit.compute_ks import compute_ks
        torch.manual_seed(SEED); np.random.seed(SEED)
        if os.environ.get("CP1_DETERMINISTIC") == "1":
            # best-effort cross-process bit-reproducibility (GPU FP). warn_only so a non-deterministic
            # kernel degrades gracefully instead of aborting the compile.
            torch.use_deterministic_algorithms(True, warn_only=True)
            torch.backends.cudnn.deterministic = True; torch.backends.cudnn.benchmark = False
        cwd = os.getcwd(); os.chdir(ENGINE_ROOT)
        try:
            requests = [{"prompt": e["prompt"], "subject": e["subject"],
                         "target_new": {"str": e["target"]}} for e in edits]
            cache = [torch.zeros(self.P[0].shape[0], self.P[0].shape[0]) for _ in self.L]
            npd = dict(self.model.named_parameters())
            zl = self.L[-1]
            with contextlib.redirect_stdout(io.StringIO()):
                zs = torch.stack([compute_z(self.model, self.tok, r, self.hp, zl, self.ctx) for r in requests], dim=1)
                for i, layer in enumerate(self.L):
                    K = compute_ks(self.model, self.tok, requests, self.hp, layer, self.ctx).T
                    cur = get_module_input_output_at_words(
                        self.model, self.tok, zl, context_templates=[r["prompt"] for r in requests],
                        words=[r["subject"] for r in requests], module_template=self.hp.layer_module_tmp,
                        fact_token_strategy=self.hp.fact_token)[1].T
                    tgt = (zs - cur); tgt = tgt.repeat_interleave(K.size(1) // tgt.size(1), dim=1)
                    resid = tgt / (len(self.L) - i)
                    Pi = self.P[i].cuda(); ca = cache[i].cuda(); Kg = K.float().cuda(); rg = resid.float().cuda()
                    A = Pi @ (Kg @ Kg.T + ca) + 1.0 * torch.eye(Kg.shape[0], device="cuda")
                    B = Pi @ Kg @ rg.T
                    upd = torch.linalg.solve(A, B).T.cpu()
                    del Pi, ca, Kg, rg, A, B; torch.cuda.empty_cache()
                    upd = upd_matrix_match_shape(upd.float(), npd[self.WN(layer)].shape)
                    with torch.no_grad():
                        npd[self.WN(layer)][...] += upd.to(npd[self.WN(layer)].device, npd[self.WN(layer)].dtype)
                    if fault == "mid_compile" and i == 0:
                        raise RuntimeError("INJECTED FAULT mid-compile (after band layer 0 mutated)")
            # extract edited band down_proj as little-endian f32 numpy [hidden, inter]
            band = {}
            for layer in self.L:
                band[layer] = npd[self.WN(layer)].detach().to(torch.float32).cpu().numpy().astype("<f4")
            return band
        finally:
            self._restore()                              # in-memory model returns to frozen base
            os.chdir(cwd)


# ════════════════════════════════════════════════════════════════════════════
#  COMMIT EXECUTOR (§9.10, §11.5) — deterministic, non-reasoning, sole writer
# ════════════════════════════════════════════════════════════════════════════
def band_to_vlp(band, path):
    """Package edited band down_proj columns as a LARQL .vlp (full-band down_vector overrides) —
    the SAME proven format as the bridge (s252b). Returns the overlay hash (determinism witness)."""
    ops = []
    for layer in sorted(band):
        W = band[layer]                                  # [hidden, inter]
        for F in range(W.shape[1]):
            col = np.ascontiguousarray(W[:, F])
            ops.append({"op": "update", "layer": int(layer), "feature": int(F),
                        "down_vector_b64": base64.b64encode(col.tobytes()).decode()})
    patch = {"version": 1, "base_model": "qwen3", "base_checksum": None,
             "created_at": "1970-01-01T00:00:00Z", "description": "CP1 in-pipeline MEMIT overlay",
             "author": "cp1_commit_executor", "tags": ["cp1"], "operations": ops}
    blob = _canon(patch)
    json.dump(patch, open(path, "w"))
    return _sha(blob), len(ops)

def dir_checksum(d):
    """Order-stable checksum over a vindex directory's bytes (atomicity witness for the frozen base)."""
    h = hashlib.sha256()
    for name in sorted(os.listdir(d)):
        p = os.path.join(d, name)
        if os.path.isfile(p):
            h.update(name.encode())
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
    return h.hexdigest()

class CommitExecutor:
    """Single, deterministic, NON-REASONING writer (no LLM in this loop — C-OR2). Receives a
    GATE-AUTHORIZED package only. 2PC-shaped: PREPARE -> [git placeholder] -> compile -> mount ->
    probe -> COMMITTED. ANY exception in Phase 2 leaves PREPARED with NO COMMITTED and mounts
    nothing (clean-fail atomicity)."""
    def __init__(self, engine: RecipeEngine, ledger: StateLedger):
        self.engine, self.ledger = engine, ledger
        os.makedirs(WORK, exist_ok=True)

    @staticmethod
    def git_prepare(package):
        """STRUCTURAL PLACEHOLDER for the dual-medium write (§11.5 D46 Git-first). DEFERRED TO G1.
        CP1 is parametric-only; this is a no-op so the pipeline shape is Commit-Executor-shaped."""
        return {"git": "DEFERRED_TO_G1"}

    def execute(self, package, fault=None):
        ph = package["patch_hash"]
        # ---- Phase 1: PREPARE ----
        self.ledger.append("PREPARED", {"patch_hash": ph, "agent_id": package["agent_id"],
                                        "classification": package["patch_body"]["content_classification"]})
        base_ck_before = dir_checksum(FROZEN_BASE)
        out_vindex = os.path.join(WORK, f"compiled_{ph[:12]}.vindex")
        vlp = os.path.join(WORK, f"overlay_{ph[:12]}.vlp")
        try:
            # ---- Phase 2a: dual-medium placeholder (G1) ----
            self.git_prepare(package)
            # ---- Phase 2b: IN-STEP GPU-bound MEMIT compile (the n8n question) ----
            t0 = time.time()
            band = self.engine.compile_patch(package["patch_body"]["edits"], fault=fault)
            compile_s = round(time.time() - t0, 1)
            # ---- Phase 2c: package overlay + MOUNT on frozen base (APPLY + COMPILE) ----
            overlay_hash, n_ops = band_to_vlp(band, vlp)
            shutil.rmtree(out_vindex, ignore_errors=True)
            self._larql_apply_compile(FROZEN_BASE, vlp, out_vindex, fault=fault)
            # ---- Phase 2d: post-write probe (BEHAVIORAL stand-in for L1 SELECT — CP2-dependent) ----
            probe = self._probe(out_vindex, package["patch_body"]["probe"])
            if not probe["pass"]:
                raise RuntimeError(f"POST_WRITE_PROBE_FAIL: {probe}")
            # ---- COMMITTED ----
            ck_after = dir_checksum(FROZEN_BASE)
            self.ledger.append("COMMITTED",
                               {"patch_hash": ph, "overlay_hash": overlay_hash, "n_overrides": n_ops,
                                "compiled_vindex": out_vindex, "compile_seconds": compile_s,
                                "probe": probe, "frozen_base_unchanged": ck_after == base_ck_before})
            return {"status": "COMMITTED", "overlay_hash": overlay_hash, "compile_seconds": compile_s,
                    "probe": probe, "out_vindex": out_vindex}
        except Exception as e:
            # clean-fail: forensic record, NO COMMITTED, mount discarded, base untouched
            shutil.rmtree(out_vindex, ignore_errors=True)
            self.ledger.append("WRITE_FAILED",
                               {"patch_hash": ph, "error": str(e),
                                "frozen_base_unchanged": dir_checksum(FROZEN_BASE) == base_ck_before})
            return {"status": "FAILED", "error": str(e)}

    @staticmethod
    def _larql_apply_compile(base, vlp, out, fault=None):
        if fault == "mid_mount":   # SYNTHETIC: raises BEFORE the subprocess (tests exception->no-commit
            raise RuntimeError("INJECTED FAULT during mount (APPLY/COMPILE)")  # cleanup, not a real partial mount)
        stmt = f'USE "{base}"; APPLY PATCH "{vlp}"; COMPILE CURRENT INTO VINDEX "{out}";'
        r = subprocess.run([LARQL, "lql", stmt], capture_output=True, text=True, timeout=600)
        if r.returncode != 0 or not os.path.isdir(out):
            raise RuntimeError(f"LARQL_MOUNT_FAIL rc={r.returncode} err={r.stderr[-400:]}")

    @staticmethod
    def _probe(vindex, probe_spec):
        """L2-class behavioral read-back. Stand-in for the mandatory L1 SELECT storage probe
        (§8.9) pending CP2. Confirms the edited fact fires in inference on the COMPILED vindex."""
        r = subprocess.run([LARQL, "run", vindex, probe_spec["prompt"], "-n", "2"],
                           capture_output=True, text=True, timeout=300)
        out = (r.stdout or "").strip()
        return {"prompt": probe_spec["prompt"], "expect": probe_spec["expect"],
                "got": out[:60], "pass": probe_spec["expect"].lower() in out.lower(),
                "probe_class": "behavioral_L2_standin_for_L1_SELECT(CP2-dependent)"}


# ════════════════════════════════════════════════════════════════════════════
#  PACKAGE BUILDER + TEST HARNESS
# ════════════════════════════════════════════════════════════════════════════
def make_package(agent_id, edits, probe, tier="incremental", classification="layer4_domain"):
    # deep-copy edits/probe so per-package tampering can't mutate a caller's shared objects
    body = {"tier": tier, "content_classification": classification, "larql_syntax_version": "1.1",
            "edits": json.loads(json.dumps(edits)), "probe": dict(probe), "declared_importance": "CORE"}
    return {"agent_id": agent_id, "patch_hash": _sha(_canon(body)), "patch_body": body}

def main():
    print("="*70); print("CP1 — governed IN-PIPELINE MEMIT write (parametric-only; dual-medium -> G1)")
    print("="*70, flush=True)
    ledger = StateLedger(LEDGER_PATH)
    # Write Scope Definitions (§10.8): the Coder may write layer4_domain knowledge, incremental tier.
    write_scopes = {
        "coder-agent": {"tiers": ["incremental"], "classifications": ["layer4_domain"],
                        "relations": ["has_capital"]},
        "rogue-agent": {"tiers": ["incremental"], "classifications": ["layer4_domain"],
                        "relations": ["has_capital"]},
    }
    orch = Orchestrator(ledger, write_scopes)
    gate = PatchAuthorizationGate(orch, ledger)
    print("\n[load] loading Qwen3-0.6B + computing P (cached covs) ...", flush=True)
    engine = RecipeEngine()
    execu = CommitExecutor(engine, ledger)
    print("[load] engine ready.\n", flush=True)

    # The authorized edit: France capital -> Berlin (same single-edit used in the proven bridge).
    edits = [{"prompt": "The capital of {} is the city of", "subject": "France",
              "target": " Berlin", "relation": "has_capital"}]
    probe = {"prompt": "The capital of France is", "expect": "Berlin"}

    results = {}

    # ---------- T-POS: authorized end-to-end ----------
    print("── T-POS: authorized patch -> in-step compile -> mount -> probe ──", flush=True)
    pkg = make_package("coder-agent", edits, probe)
    tok = orch.mint_token("coder-agent", pkg["patch_hash"])
    gate.authorize(tok, pkg)                              # raises if rejected
    pos = execu.execute(pkg)
    print(f"   -> {pos.get('status')} overlay={pos.get('overlay_hash','')[:12]} "
          f"compile={pos.get('compile_seconds')}s probe={pos.get('probe',{}).get('got','')!r}", flush=True)
    results["T_POS"] = {"status": pos["status"],
                        "committed": ledger.has("COMMITTED", patch_hash=pkg["patch_hash"]),
                        "prepared": ledger.has("PREPARED", patch_hash=pkg["patch_hash"]),
                        "probe_pass": pos.get("probe", {}).get("pass"),
                        "overlay_hash": pos.get("overlay_hash"), "compile_seconds": pos.get("compile_seconds")}

    # ---------- T-DET: determinism (same patch -> same overlay hash) ----------
    print("\n── T-DET: determinism (recompile same patch) ──", flush=True)
    pkg2 = make_package("coder-agent", edits, probe)
    tok2 = orch.mint_token("coder-agent", pkg2["patch_hash"])
    gate.authorize(tok2, pkg2)
    det = execu.execute(pkg2)
    same = det.get("overlay_hash") == pos.get("overlay_hash")
    print(f"   -> overlay#2={det.get('overlay_hash','')[:12]} identical={same}", flush=True)
    results["T_DET"] = {"overlay_hash_1": pos.get("overlay_hash"), "overlay_hash_2": det.get("overlay_hash"),
                        "deterministic": same}

    # ---------- T-GATE: three rejections, NO compile/commit ----------
    # NOTE: each negative test uses a DISTINCT edit so its patch_hash never collides with an
    # already-COMMITTED hash (a collision would falsely trip the "was it committed?" check).
    print("\n── T-GATE: gate must reject (bad sig / tampered hash / out-of-scope) ──", flush=True)
    gate_cases = {}
    g_edit = lambda subj, tgt, rel="has_capital": [{"prompt": "The capital of {} is the city of",
                                                    "subject": subj, "target": tgt, "relation": rel}]
    g_probe = {"prompt": "x", "expect": "x"}
    # (a) bad signature
    badpkg = make_package("coder-agent", g_edit("Spain", " Oslo"), g_probe)
    bad = orch.mint_token("coder-agent", badpkg["patch_hash"]); bad["signature"] = "deadbeef"
    try: gate.authorize(bad, badpkg); gate_cases["bad_signature"] = "ACCEPTED(!)"
    except GateReject as r: gate_cases["bad_signature"] = r.code
    # (b) tampered patch: hash + token minted over CLEAN body, then body mutated -> actual != declared
    tam = make_package("coder-agent", g_edit("Greece", " Lima"), g_probe)
    ttok = orch.mint_token("coder-agent", tam["patch_hash"])   # token witnesses the clean patch_hash
    tam["patch_body"]["edits"][0]["target"] = " Madrid"        # tamper AFTER hashing -> integrity mismatch
    try: gate.authorize(ttok, tam); gate_cases["tampered_hash"] = "ACCEPTED(!)"
    except GateReject as r: gate_cases["tampered_hash"] = r.code
    # (c) out-of-scope: rogue patch targeting a relation outside its Write Scope
    oos = make_package("rogue-agent", g_edit("Poland", " Nairobi", rel="has_population"), g_probe)
    otok = orch.mint_token("rogue-agent", oos["patch_hash"])
    try: gate.authorize(otok, oos); gate_cases["out_of_scope"] = "ACCEPTED(!)"
    except GateReject as r: gate_cases["out_of_scope"] = r.code
    # (d) token replay (§10.2 #3): a single-use token re-presented after consumption
    rep = make_package("coder-agent", g_edit("Egypt", " Tokyo"), g_probe)
    rtok = orch.mint_token("coder-agent", rep["patch_hash"])
    gate.authorize(rtok, rep)                                   # first use -> TOKEN_CONSUMED recorded
    try: gate.authorize(rtok, rep); gate_cases["token_replay"] = "ACCEPTED(!)"
    except GateReject as r: gate_cases["token_replay"] = r.code
    # (e) token expired (§10.2 #2): TTL already elapsed at presentation
    exp = make_package("coder-agent", g_edit("Germany", " Lima"), g_probe)
    etok = orch.mint_token("coder-agent", exp["patch_hash"], ttl_s=-1)
    try: gate.authorize(etok, exp); gate_cases["token_expired"] = "ACCEPTED(!)"
    except GateReject as r: gate_cases["token_expired"] = r.code
    print(f"   -> {gate_cases}", flush=True)
    # none of the rejected patches may have produced a COMMITTED (distinct hashes -> sound check)
    rejected_committed = any(ledger.has("COMMITTED", patch_hash=p["patch_hash"])
                             for p in [badpkg, tam, oos, rep, exp])
    results["T_GATE"] = {"rejections": gate_cases, "any_rejected_committed": rejected_committed,
                         "all_rejected": all(v != "ACCEPTED(!)" for v in gate_cases.values())}

    # ---------- T-ATOM: fault mid-step -> PREPARED, NO COMMITTED, base unchanged ----------
    # Two sub-cases, each a DISTINCT edit: (1) fault during the GPU compile (the n8n question),
    # (2) fault during the mount (APPLY/COMPILE) AFTER a clean compile.
    print("\n── T-ATOM: inject faults (mid-compile, mid-mount) ──", flush=True)
    atom = {}
    for tag, fault, subj, tgt in [("mid_compile", "mid_compile", "Japan", " Cairo"),
                                  ("mid_mount", "mid_mount", "Italy", " Lisbon")]:
        base_before = dir_checksum(FROZEN_BASE)
        apkg = make_package("coder-agent", g_edit(subj, tgt),
                            {"prompt": f"The capital of {subj} is", "expect": tgt.strip()})
        atok = orch.mint_token("coder-agent", apkg["patch_hash"])
        gate.authorize(atok, apkg)
        af = execu.execute(apkg, fault=fault)
        atom[tag] = {"status": af["status"],
                     "prepared": ledger.has("PREPARED", patch_hash=apkg["patch_hash"]),
                     "committed": ledger.has("COMMITTED", patch_hash=apkg["patch_hash"]),
                     "frozen_base_unchanged": base_before == dir_checksum(FROZEN_BASE),
                     "error": af.get("error", "")[:80]}
        print(f"   [{tag}] -> {atom[tag]['status']} prepared={atom[tag]['prepared']} "
              f"committed={atom[tag]['committed']} base_unchanged={atom[tag]['frozen_base_unchanged']}", flush=True)
    results["T_ATOM"] = {"cases": atom,
                         "all_clean_fail": all(c["prepared"] and not c["committed"] and c["frozen_base_unchanged"]
                                               and c["status"] == "FAILED" for c in atom.values())}

    # ---------- ledger chain integrity ----------
    ok, msg = ledger.verify_chain()
    results["LEDGER_CHAIN"] = {"intact": ok, "msg": msg, "n_entries": len(ledger.entries())}
    print(f"\n[ledger] chain {msg}; {len(ledger.entries())} entries", flush=True)

    # ---------- VERDICT ----------
    verdict = {
        "T_POS  (authorized -> COMMITTED + probe)": results["T_POS"]["committed"] and results["T_POS"]["probe_pass"],
        "T_DET  (deterministic overlay)":            results["T_DET"]["deterministic"],
        "T_GATE (all rejected, none committed)":     results["T_GATE"]["all_rejected"] and not results["T_GATE"]["any_rejected_committed"],
        "T_ATOM (clean-fail: PREPARED, NO COMMITTED, base safe)": results["T_ATOM"]["all_clean_fail"],
        "LEDGER (chain intact)":                     results["LEDGER_CHAIN"]["intact"],
    }
    results["VERDICT"] = verdict
    results["scope_and_caveats"] = {
        "scope": "PARAMETRIC-ONLY governed in-pipeline MEMIT write. Dual-medium 2PC (Git+.vindex, "
                 "D46 Git-first ordering, Transaction Controller, compensation) DEFERRED TO G1.",
        "n8n_question": "Execution-MODEL fit PROVEN: a synchronous non-reasoning executor hosts the "
                        "GPU compile in-process as a blocking first-class step (what n8n's HTTP/node "
                        "model could not, D70). Compile here was single-fact ~1s; multi-minute/batch "
                        "compile DURATION + scale = G6, NOT validated here.",
        "determinism": "Governance sense (C-OR2: non-reasoning, no LLM, in-process repeatable) HOLDS "
                       "(T-DET bit-identical within process). Cross-PROCESS overlay bytes are NOT "
                       "bit-reproducible (GPU FP; root cause = non-deterministic mem-efficient attention "
                       "backward in compute_z). Not a C-OR2 requirement; spec compaction (§8.10) is "
                       "itself a full MEMIT re-run verified BEHAVIORALLY, not by hash. Ledger overlay_hash "
                       "anchors STORED-artifact integrity, not recompile-reproducibility.",
        "probe": "Post-write probe is BEHAVIORAL (L2-class, larql run) standing in for the mandatory "
                 "L1 SELECT storage read-back (§8.9) — pending CP2 query-schema capability.",
        "stubs": "Orchestrator signing = HMAC (symmetric) stub for the asymmetric Orchestrator key "
                 "(§10.5, G2). git_prepare = no-op placeholder (G1). mid_mount fault = SYNTHETIC "
                 "(raises before subprocess). C16 'gate is sole path' holds by HARNESS CONSTRUCTION, "
                 "not structural enforcement. frozen_base_unchanged = base is a read-only input, "
                 "NOT a 2PC-atomicity proof.",
    }
    json.dump(results, open(RESULT_PATH, "w"), indent=2)
    print("\n" + "="*70); print("CP1 VERDICT")
    for k, v in verdict.items():
        print(f"   [{'PASS' if v else 'FAIL'}] {k}")
    print("="*70)
    print(f"all_pass={all(verdict.values())}  -> {RESULT_PATH}", flush=True)

if __name__ == "__main__":
    main()
