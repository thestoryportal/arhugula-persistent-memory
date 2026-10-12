#!/usr/bin/env python3
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""
g1_two_phase_commit.py — GAP G1: dual-medium 2PC + State Ledger + Transaction Controller
+ Circuit Breaker (viability prototype). Builds on CP1; supplies the dual-medium atomicity
CP1 deferred.

WHAT G1 PROVES (and what it does NOT)
-------------------------------------
CP1 proved governed in-pipeline PARAMETRIC write + clean-fail on the .vindex side only. G1 adds
the SECOND medium (Git) and the spec's consistency machinery:
  * §11.5 2PC with D46 ORDERING — Git push FIRST, .vindex mount SECOND (constrains failures to the
    recoverable Git-ahead state; Weights-ahead is made structurally unreachable).
  * §11.15/§16 STATE LEDGER as the consistency substrate — each COMMITTED entry binds the pair
    (git_commit ↔ overlay_hash); divergence = the live mediums disagreeing with that pair.
  * §11.7 TRANSACTION CONTROLLER — SOLE compensation authority (C-TC1). Compensation DIRECTION by
    CONTENT_CLASSIFICATION (C-TC2): Structural → ≤3 mount retries then AUTO git-revert; Layer4_domain
    → ≤5 retries then PARK for human confirm (no auto-revert). Reversal-only (C-CRC-3).
  * §11.8 CIRCUIT BREAKER (D48): 3 consecutive 2PC failures in one task → trip; 5 across tasks /10min
    → trip; DIVERGED → immediate trip. Trip → READ_ONLY (new writes refused). Reset requires a signed
    ceremony whose PRECONDITION is checked (compensation COMPLETED + overlay == last COMMITTED).

The NEW thing under test (CP1 already banked the compile/serve): the dual-medium TRANSACTION machinery.
So failure/divergence tests INJECT faults or corrupt a medium out-of-band; only the happy path and the
dual rollback do a REAL larql APPLY+COMPILE mount.

HONEST SCOPE / STUBS (flagged, CP1 precedent):
  * Compensation in the 2PC-FAILURE path reverts GIT ONLY — because .vindex is written second, so on
    failure it was never mounted (nothing to revert). The .vindex-side reversal is exercised SEPARATELY
    by the dual rollback test (a COMMITTED txn rolled back). Do not read the failure-path tests as
    "atomic dual rollback."
  * Reset ceremony = precondition-checked stub for the full IC-TC-RESET CeremonyToken/CAK flow (§11.8.1)
    → G2/v2. PREPARED-timeout (§11.5.1, 2hr) is untestable in a prototype → DEFERRED. "No self-compensate"
    is construction-asserted (the executor has no revert path), not behaviorally enforced.

Engine/LARQL UNMODIFIED. Ledger primitives mirror cp1_governed_write.StateLedger (kept standalone here
so G1 needs no torch/GPU).
"""
import os, json, time, hmac, hashlib, shutil, subprocess

# ---- paths ----
FROZEN_BASE = "/dev/shm/qwen3.vindex"
OVERLAY     = "/dev/shm/cp1_work/overlay_fd3c63598e94.vlp"   # reused CP1 France->Berlin band overlay
LARQL       = f"{LLMDB_ROOT}/external_prior_art/larql/target/release/larql"
WORK        = "/dev/shm/g1_work"
GIT_REPO    = "/dev/shm/g1_work/repo"
ACTIVE_PTR  = "/dev/shm/g1_work/active.json"                 # the .vindex "what is mounted" pointer
LEDGER_PATH = f"{LLMDB_ROOT}/results/g1_state_ledger.jsonl"
RESULT_PATH = f"{LLMDB_ROOT}/results/g1_result.json"


# ════════════════════════════ ledger (hash-chained; mirrors CP1) ════════════════════════════
def _canon(o): return json.dumps(o, sort_keys=True, separators=(",", ":"))
def _sha(s):   return hashlib.sha256(s.encode()).hexdigest()

class StateLedger:
    GENESIS = "0" * 64
    def __init__(self, path):
        self.path = path; open(path, "w").close(); self._tip = self.GENESIS
    def append(self, etype, body):
        e = {"seq": self._count(), "ts": round(time.time(), 3), "entry_type": etype,
             "prev_hash": self._tip, "body": body}
        e["entry_hash"] = _sha(e["prev_hash"] + _canon(body))
        with open(self.path, "a") as f: f.write(_canon(e) + "\n")
        self._tip = e["entry_hash"]; return e
    def _count(self):
        with open(self.path) as f: return sum(1 for _ in f)
    def entries(self):
        with open(self.path) as f: return [json.loads(l) for l in f if l.strip()]
    def verify_chain(self):
        tip = self.GENESIS
        for e in self.entries():
            if e["prev_hash"] != tip or e["entry_hash"] != _sha(e["prev_hash"] + _canon(e["body"])):
                return False, f"break at seq {e['seq']}"
            tip = e["entry_hash"]
        return True, "intact"
    def last(self, etype):
        m = [e for e in self.entries() if e["entry_type"] == etype]
        return m[-1] if m else None
    def has(self, etype, **match):
        return any(e["entry_type"] == etype and all(e["body"].get(k) == v for k, v in match.items())
                   for e in self.entries())
    def detect_prepared_bypass(self):
        """C-TPC4: a COMMITTED whose txn_id has NO matching PREPARED = a ledger-bypass security
        incident. Returns the set of offending txn_ids (empty = clean)."""
        prepared = {e["body"].get("txn_id") for e in self.entries() if e["entry_type"] == "PREPARED"}
        return {e["body"].get("txn_id") for e in self.entries()
                if e["entry_type"] == "COMMITTED" and e["body"].get("txn_id") not in prepared}


# ════════════════════════════ git medium (syntactic) ════════════════════════════
def _git(*args, check=True):
    r = subprocess.run(["git", "-C", GIT_REPO, *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()

def git_head():
    return _git("rev-parse", "HEAD")

def git_commit_files(files: dict, msg, fault=None):
    """Write files into the repo + commit. fault='git_fail' simulates a Git-medium failure
    (D46 first-step failure → the .vindex step must NOT run)."""
    if fault == "git_fail":
        raise RuntimeError("INJECTED Git-medium failure (Phase-2 step 1)")
    for rel, content in files.items():
        p = os.path.join(GIT_REPO, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(content)
    _git("add", "-A")
    _git("-c", "user.email=cx@harness", "-c", "user.name=commit-executor", "commit", "-q", "-m", msg)
    return git_head()

def git_revert_to(commit):
    _git("reset", "--hard", commit)


# ════════════════════════════ .vindex medium (parametric) ════════════════════════════
def read_active():
    return json.load(open(ACTIVE_PTR)) if os.path.exists(ACTIVE_PTR) else None

def write_active(d):
    json.dump(d, open(ACTIVE_PTR, "w"))

def overlay_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def vindex_mount(overlay, git_commit, ledger_seq, real_compile=False, fault=None, retries=1):
    """Mount = make `overlay` the active parametric state on the FROZEN base. The atomic COMMIT POINT
    is the active-pointer flip, which happens ONLY on success — so a failed mount leaves NO active state
    (Weights-ahead unreachable). `real_compile` runs a true larql APPLY+COMPILE; failure tests inject
    `fault` and never reach the flip. Returns (overlay_hash, compiled_vindex_or_None)."""
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            if fault == "mount_fail":
                raise RuntimeError(f"INJECTED .vindex mount failure (attempt {attempt}/{retries})")
            oh = overlay_hash(overlay)
            compiled = None
            if real_compile:
                compiled = os.path.join(WORK, f"compiled_{oh[:12]}.vindex")
                shutil.rmtree(compiled, ignore_errors=True)
                stmt = f'USE "{FROZEN_BASE}"; APPLY PATCH "{overlay}"; COMPILE CURRENT INTO VINDEX "{compiled}";'
                r = subprocess.run([LARQL, "lql", stmt], capture_output=True, text=True, timeout=600)
                if r.returncode != 0 or not os.path.isdir(compiled):
                    raise RuntimeError(f"LARQL mount rc={r.returncode} {r.stderr[-200:]}")
            # COMMIT POINT: atomic active-pointer flip (only on full success)
            write_active({"overlay_hash": oh, "overlay": overlay, "git_commit": git_commit,
                          "ledger_seq": ledger_seq, "compiled": compiled})
            return oh, compiled
        except Exception as e:
            last_err = e
            shutil.rmtree(os.path.join(WORK, "compiled_partial"), ignore_errors=True)
    raise RuntimeError(f"mount failed after {retries} attempts: {last_err}")

def vindex_rollback_to_base():
    if os.path.exists(ACTIVE_PTR): os.remove(ACTIVE_PTR)   # no active overlay = serve frozen base


# ════════════════════════════ circuit breaker (§11.8) ════════════════════════════
class CircuitBreaker:
    def __init__(self, ledger):
        self.ledger = ledger; self.state = "WRITE_ENABLED"
        self._task_consec = {}      # task_id -> consecutive failures
        self._recent_fail_ts = []   # cross-task failure timestamps (10-min window)
    def on_success(self, task_id): self._task_consec[task_id] = 0
    def on_failure(self, task_id):
        self._task_consec[task_id] = self._task_consec.get(task_id, 0) + 1
        now = time.time(); self._recent_fail_ts = [t for t in self._recent_fail_ts if now - t < 600]
        self._recent_fail_ts.append(now)
        if self._task_consec[task_id] >= 3:           return self.trip("CONSECUTIVE_FAILURE", "CONSISTENCY")
        if len(self._recent_fail_ts) >= 5:            return self.trip("CROSS_TASK_FAILURE", "CONSISTENCY")
        return None
    def trip(self, reason, category):
        if self.state != "CIRCUIT_TRIPPED":
            self.state = "CIRCUIT_TRIPPED"
            self.ledger.append("CIRCUIT_TRIPPED", {"reason": reason, "category": category})
        return reason
    def admit_write(self):
        return self.state == "WRITE_ENABLED"
    def reset(self, compensation_completed, current_overlay_hash, last_committed_overlay_hash):
        """IC-TC-RESET precondition-checked stub: for CONSECUTIVE/CROSS_TASK, admit only if compensation
        COMPLETED and the live overlay matches the last COMMITTED entry (§11.8.1 admission branch)."""
        ok = compensation_completed and current_overlay_hash == last_committed_overlay_hash
        if not ok:
            self.ledger.append("CIRCUIT_RESET_REJECTED",
                               {"reason": "precondition_unmet",
                                "compensation_completed": compensation_completed,
                                "overlay_match": current_overlay_hash == last_committed_overlay_hash})
            return False
        self.state = "WRITE_ENABLED"
        self.ledger.append("CIRCUIT_RESET", {"audit_category": "GOVERNANCE"})
        return True


# ════════════════════════════ transaction controller (§11.7) — SOLE compensator ════════════════════════════
class TransactionController:
    def __init__(self, ledger, breaker):
        self.ledger, self.breaker = ledger, breaker
        self.parked = {}   # txn_id -> {git_commit, baseline_commit, classification}  (sanctioned in-flight)
    def compensate(self, txn, classification, baseline_commit):
        """Called by the executor on Git-ahead failure (Git committed, .vindex mount failed). Direction
        by C-TC2. Reversal-only (C-CRC-3). Returns a status dict."""
        if classification == "structural":
            git_revert_to(baseline_commit)              # ≤3 retries already spent in the mount; auto-revert Git
            self.ledger.append("ABORTED", {"txn_id": txn, "classification": classification})
            self.ledger.append("COMPENSATION_COMPLETED",
                               {"txn_id": txn, "direction": "git_auto_revert", "git_now": git_head()})
            return {"status": "COMPENSATED", "git_reverted": True}
        else:  # layer4_domain → PARK, no auto-revert; human confirm required
            self.parked[txn] = {"git_commit": git_head(), "baseline_commit": baseline_commit,
                                "classification": classification}
            self.ledger.append("PARKED",
                               {"txn_id": txn, "classification": classification,
                                "state": "AWAITING_OPERATOR", "git_ahead_commit": git_head()})
            return {"status": "AWAITING_OPERATOR", "git_reverted": False}
    def operator_confirm_revert(self, txn):
        """HIL: operator authorizes the Git revert for a parked Layer4 txn."""
        p = self.parked.pop(txn)
        git_revert_to(p["baseline_commit"])
        self.ledger.append("COMPENSATION_COMPLETED",
                           {"txn_id": txn, "direction": "git_revert_operator_confirmed", "git_now": git_head()})
        return {"status": "COMPENSATED", "git_reverted": True}
    def reconcile(self):
        """Divergence detection: compare the LIVE mediums (git HEAD, active overlay) against the last
        COMMITTED ledger pair. A mismatch NOT explained by a sanctioned parked txn = DIVERGED → trip.
        Parked Layer4 (git-ahead) is sanctioned in-flight (§11.8.1) and must NOT false-trip."""
        c = self.ledger.last("COMMITTED")
        if not c: return {"diverged": False, "reason": "no_committed_baseline"}
        want_git = c["body"]["git_commit"]; want_oh = c["body"]["overlay_hash"]
        live_git = git_head(); active = read_active(); live_oh = active["overlay_hash"] if active else None
        # a parked txn legitimately advances git beyond the last COMMITTED — sanctioned, skip it
        sanctioned_git = {p["git_commit"] for p in self.parked.values()}
        git_div    = (live_git != want_git) and (live_git not in sanctioned_git)
        vindex_div = (live_oh != want_oh)
        if git_div or vindex_div:
            self.ledger.append("DIVERGENCE_DETECTED",
                               {"git_expected": want_git[:12], "git_live": live_git[:12],
                                "overlay_expected": want_oh[:12], "overlay_live": (live_oh or "none")[:12],
                                "side": "git" if git_div else "vindex"})
            self.breaker.trip("DIVERGED_STATE", "CONSISTENCY")
            return {"diverged": True, "side": "git" if git_div else "vindex"}
        return {"diverged": False}


# ════════════════════════════ commit executor (§9.10/§11.5) — sole dual writer ════════════════════════════
class CommitExecutor:
    def __init__(self, ledger, tc, breaker):
        self.ledger, self.tc, self.breaker = ledger, tc, breaker
    def execute(self, package, real_compile=False, fault=None):
        txn = package["txn_id"]; cls = package["classification"]
        if not self.breaker.admit_write():
            self.ledger.append("WRITE_REJECTED", {"txn_id": txn, "reason": "CIRCUIT_TRIPPED"})
            return {"status": "REJECTED_READ_ONLY"}
        baseline_commit = git_head()
        retries = 3 if cls == "structural" else 5
        # ---- Phase 1: PREPARE ----
        self.ledger.append("PREPARED", {"txn_id": txn, "classification": cls, "baseline_commit": baseline_commit})
        # ---- Phase 2 step 1: GIT FIRST (D46) ----
        try:
            git_commit = git_commit_files(package["files"], f"txn {txn}", fault=fault if fault == "git_fail" else None)
        except Exception as e:
            # Git failed → .vindex NEVER attempted → no orphan, clean abort (Weights-ahead unreachable)
            self.ledger.append("ABORTED", {"txn_id": txn, "phase": "git_first", "error": str(e)[:80],
                                           "vindex_attempted": False})
            self.breaker.on_failure(txn)
            return {"status": "ABORTED_GIT_FIRST", "vindex_attempted": False}
        # ---- Phase 2 step 2: .vindex SECOND ----
        try:
            oh, compiled = vindex_mount(package["overlay"], git_commit, ledger_seq=self.ledger._count(),
                                        real_compile=real_compile,
                                        fault=fault if fault == "mount_fail" else None, retries=retries)
        except Exception as e:
            # Git-ahead → hand to TC (executor NEVER self-compensates)
            comp = self.tc.compensate(txn, cls, baseline_commit)
            trip = self.breaker.on_failure(txn)
            return {"status": "VINDEX_FAILED", "compensation": comp, "tripped": trip, "error": str(e)[:80]}
        # ---- COMMITTED (pair git <-> overlay) ----
        self.breaker.on_success(txn)
        self.ledger.append("COMMITTED", {"txn_id": txn, "git_commit": git_commit, "overlay_hash": oh,
                                         "classification": cls, "compiled_vindex": compiled})
        return {"status": "COMMITTED", "git_commit": git_commit, "overlay_hash": oh, "compiled": compiled}


# ════════════════════════════ harness ════════════════════════════
def fresh_world():
    shutil.rmtree(WORK, ignore_errors=True); os.makedirs(GIT_REPO, exist_ok=True)
    _git("init", "-q"); _git("config", "user.email", "x@y"); _git("config", "user.name", "x")
    open(os.path.join(GIT_REPO, "README"), "w").write("genesis\n")
    _git("add", "-A"); _git("-c", "user.email=x@y", "-c", "user.name=x", "commit", "-q", "-m", "genesis")
    vindex_rollback_to_base()

def serve(vindex, prompt):
    r = subprocess.run([LARQL, "run", vindex, prompt, "-n", "2"], capture_output=True, text=True, timeout=300)
    return (r.stdout or "").strip()

def pkg(txn, cls, target_city="Berlin"):
    return {"txn_id": txn, "classification": cls,
            "files": {f"src/{txn}.py": f"# {txn}\nCAPITAL='{target_city}'\n",
                      f"patches/{txn}.larql": f"BEGIN TRANSACTION; INSERT ... COMMIT;"},
            "overlay": OVERLAY}

def main():
    print("=" * 72); print("G1 — dual-medium 2PC + State Ledger + Transaction Controller + Circuit Breaker")
    print("=" * 72, flush=True)
    fresh_world()
    ledger = StateLedger(LEDGER_PATH)
    breaker = CircuitBreaker(ledger); tc = TransactionController(ledger, breaker)
    ex = CommitExecutor(ledger, tc, breaker)
    R = {}

    # T-HAPPY — real mount, paired ledger
    print("\n── T-HAPPY: PREPARE → git FIRST → vindex mount SECOND → COMMITTED (real APPLY+COMPILE) ──", flush=True)
    h = ex.execute(pkg("t-happy", "structural"), real_compile=True)
    served = serve(h["compiled"], "The capital of France is") if h.get("compiled") else ""
    c = ledger.last("COMMITTED")
    R["T_HAPPY"] = {"status": h["status"], "git_committed": h.get("git_commit") == git_head(),
                    "paired": bool(c and c["body"]["git_commit"] and c["body"]["overlay_hash"]),
                    "served": served[:40], "serves_edit": "berlin" in served.lower()}
    print(f"   -> {R['T_HAPPY']}", flush=True)

    # T-D46-GITFAIL — Git step fails → vindex NEVER attempted (Weights-ahead unreachable)
    print("\n── T-D46: git-first FAILS → vindex never attempted, clean abort, no active overlay ──", flush=True)
    active_before = read_active()
    g = ex.execute(pkg("t-gitfail", "structural"), fault="git_fail")
    R["T_D46_GITFAIL"] = {"status": g["status"], "vindex_attempted": g.get("vindex_attempted"),
                          "active_unchanged": read_active() == active_before,
                          "aborted_logged": ledger.has("ABORTED", txn_id="t-gitfail")}
    print(f"   -> {R['T_D46_GITFAIL']}", flush=True)

    # T-COMP-STRUCT — Structural + mount fail → ≤3 retries → AUTO git-revert
    print("\n── T-COMP-STRUCT: structural mount-fail → ≤3 retries → TC AUTO git-revert ──", flush=True)
    base_commit = git_head()
    s = ex.execute(pkg("t-struct", "structural"), fault="mount_fail")
    R["T_COMP_STRUCT"] = {"status": s["status"], "comp": s["compensation"]["status"],
                          "git_back_to_baseline": git_head() == base_commit,
                          "no_commit": not ledger.has("COMMITTED", txn_id="t-struct"),
                          "comp_logged": ledger.has("COMPENSATION_COMPLETED", txn_id="t-struct")}
    print(f"   -> {R['T_COMP_STRUCT']}", flush=True)

    # T-COMP-L4-PARK — Layer4 + mount fail → ≤5 retries → PARK, no auto-revert; then operator confirms
    print("\n── T-COMP-L4: layer4 mount-fail → ≤5 retries → PARK (no auto-revert) → operator confirms ──", flush=True)
    base_commit = git_head()
    l = ex.execute(pkg("t-l4", "layer4_domain"), fault="mount_fail")
    git_after_park = git_head()
    parked_no_revert = (git_after_park != base_commit) and ledger.has("PARKED", txn_id="t-l4")
    conf = tc.operator_confirm_revert("t-l4")
    R["T_COMP_L4"] = {"status": l["status"], "parked_git_still_ahead": parked_no_revert,
                      "no_auto_revert": parked_no_revert,
                      "operator_revert_ok": conf["git_reverted"] and git_head() == base_commit}
    print(f"   -> {R['T_COMP_L4']}", flush=True)

    # T-ROLLBACK-DUAL — a COMMITTED txn rolled back on BOTH mediums (the only vindex-side reversal)
    print("\n── T-ROLLBACK-DUAL: COMMITTED → git-revert + vindex→base → serve base = France→Paris ──", flush=True)
    base_commit = git_head()
    rc = ex.execute(pkg("t-roll", "structural"), real_compile=True)
    # roll back: git revert + flip vindex to base
    git_revert_to(base_commit); vindex_rollback_to_base()
    ledger.append("COMPENSATION_COMPLETED", {"txn_id": "t-roll", "direction": "dual_medium_rollback"})
    served_base = serve(FROZEN_BASE, "The capital of France is")
    R["T_ROLLBACK_DUAL"] = {"committed_first": rc["status"] == "COMMITTED",
                            "git_rolled_back": git_head() == base_commit,
                            "vindex_at_base": read_active() is None,
                            "serves_original": "paris" in served_base.lower(), "served_base": served_base[:40]}
    print(f"   -> {R['T_ROLLBACK_DUAL']}", flush=True)

    # T-DIVERGE — out-of-band git commit (§11.13) AND vindex pointer flip → DIVERGED → trip
    print("\n── T-DIVERGE: out-of-band git commit + vindex-pointer flip → DIVERGED_STATE → immediate trip ──", flush=True)
    fresh_world(); ledger2 = StateLedger(LEDGER_PATH); breaker = CircuitBreaker(ledger2)
    tc = TransactionController(ledger2, breaker); ex = CommitExecutor(ledger2, tc, breaker)
    ex.execute(pkg("t-div", "structural"), real_compile=False)          # COMMITTED baseline (pointer-only mount)
    committed_git = ledger2.last("COMMITTED")["body"]["git_commit"]
    # (a) git-side out-of-band corruption (§11.13)
    open(os.path.join(GIT_REPO, "rogue.txt"), "w").write("out-of-band human edit\n")
    _git("add", "-A"); _git("-c", "user.email=h@h", "-c", "user.name=human", "commit", "-q", "-m", "out-of-band")
    rec_git = tc.reconcile()
    # (b) vindex-side: restore git consistency first (isolate), then flip active pointer to a DIFFERENT hash
    git_revert_to(committed_git)
    breaker_v = CircuitBreaker(ledger2); tc_v = TransactionController(ledger2, breaker_v)
    a = read_active(); a["overlay_hash"] = "deadbeef" * 8; write_active(a)
    rec_vx = tc_v.reconcile()
    R["T_DIVERGE"] = {"git_oob_detected": rec_git["diverged"] and rec_git["side"] == "git",
                      "git_tripped": breaker.state == "CIRCUIT_TRIPPED",
                      "vindex_flip_detected": rec_vx["diverged"] and rec_vx["side"] == "vindex",
                      "vindex_tripped": breaker_v.state == "CIRCUIT_TRIPPED"}
    print(f"   -> {R['T_DIVERGE']}", flush=True)

    # T-PARK-NOT-DIVERGE — a sanctioned parked Layer4 must NOT false-trip the divergence check
    print("\n── T-PARK-NOT-DIVERGE: sanctioned Layer4 park (git-ahead) must NOT trip DIVERGED ──", flush=True)
    fresh_world(); ledger3 = StateLedger(LEDGER_PATH); breaker = CircuitBreaker(ledger3)
    tc = TransactionController(ledger3, breaker); ex = CommitExecutor(ledger3, tc, breaker)
    ex.execute(pkg("t-base", "structural"), real_compile=False)          # COMMITTED baseline
    ex.execute(pkg("t-park", "layer4_domain"), fault="mount_fail")        # parks (git ahead, sanctioned)
    breaker_chk = breaker.state                                           # may be tripped by the failure counter, not divergence
    rec = tc.reconcile()
    R["T_PARK_NOT_DIVERGE"] = {"parked": ledger3.has("PARKED", txn_id="t-park"),
                               "reconcile_not_diverged": not rec["diverged"],
                               "no_diverged_state_entry": not ledger3.has("CIRCUIT_TRIPPED", reason="DIVERGED_STATE")}
    print(f"   -> {R['T_PARK_NOT_DIVERGE']}", flush=True)

    # T-CIRCUIT — 3 consecutive failures one task → trip → READ_ONLY → reject → precondition-checked reset
    print("\n── T-CIRCUIT: 3 consec fails → trip → READ_ONLY → reject → reset(precondition) → resume ──", flush=True)
    fresh_world(); ledger4 = StateLedger(LEDGER_PATH); breaker = CircuitBreaker(ledger4)
    tc = TransactionController(ledger4, breaker); ex = CommitExecutor(ledger4, tc, breaker)
    good = ex.execute(pkg("t-seed", "structural"), real_compile=False)    # one COMMITTED to anchor reset precondition
    last_oh = ledger4.last("COMMITTED")["body"]["overlay_hash"]
    trips = []
    for i in range(3):
        r = ex.execute({"txn_id": "t-circ", "classification": "structural", "files": pkg("t-circ", "structural")["files"],
                        "overlay": OVERLAY}, fault="mount_fail")
        trips.append(breaker.state)
    rejected = ex.execute(pkg("t-after", "structural"), real_compile=False)
    # reset precondition (§11.8.1): BOTH arms must gate — compensation-completed AND overlay==last COMMITTED.
    bad_reset_comp    = breaker.reset(compensation_completed=False, current_overlay_hash=last_oh,    last_committed_overlay_hash=last_oh)
    bad_reset_overlay = breaker.reset(compensation_completed=True,  current_overlay_hash="WRONG"*12, last_committed_overlay_hash=last_oh)
    good_reset        = breaker.reset(compensation_completed=True,  current_overlay_hash=last_oh,    last_committed_overlay_hash=last_oh)
    resumed = ex.execute(pkg("t-resume", "structural"), real_compile=False)
    R["T_CIRCUIT"] = {"trip_logged": ledger4.has("CIRCUIT_TRIPPED", reason="CONSECUTIVE_FAILURE"),
                      "write_rejected_when_tripped": rejected["status"] == "REJECTED_READ_ONLY",
                      "bad_reset_comp_refused": bad_reset_comp is False,
                      "bad_reset_overlay_refused": bad_reset_overlay is False,
                      "good_reset_admitted": good_reset is True,
                      "resumed_committed": resumed["status"] == "COMMITTED"}
    print(f"   -> {R['T_CIRCUIT']}", flush=True)

    # T-TPC4 — ledger-bypass DETECTION (not just "my code writes PREPARED first")
    print("\n── T-TPC4: fabricate a COMMITTED with NO matching PREPARED → detector must flag it ──", flush=True)
    lb = StateLedger("/dev/shm/g1_work/bypass_test.jsonl")
    lb.append("PREPARED", {"txn_id": "legit"}); lb.append("COMMITTED", {"txn_id": "legit"})   # legit pair
    lb.append("COMMITTED", {"txn_id": "smuggled"})                                              # bypass: no PREPARED
    bypass = lb.detect_prepared_bypass()
    R["T_TPC4"] = {"detected": "smuggled" in bypass, "legit_not_flagged": "legit" not in bypass,
                   "bypass_set": sorted(bypass)}
    print(f"   -> {R['T_TPC4']}", flush=True)

    # T-LEDGER — every 2PC has PREPARED (C-TPC4); chain intact (use the richest ledger, ledger4)
    ok, msg = ledger4.verify_chain()
    committeds = [e for e in ledger4.entries() if e["entry_type"] == "COMMITTED"]
    preds = {e["body"]["txn_id"] for e in ledger4.entries() if e["entry_type"] == "PREPARED"}
    all_have_prepared = all(c["body"]["txn_id"] in preds for c in committeds)
    R["T_LEDGER"] = {"chain_intact": ok, "all_committed_have_prepared": all_have_prepared,
                     "n_entries": len(ledger4.entries())}
    print(f"\n[ledger] chain {msg}; every COMMITTED has PREPARED={all_have_prepared}", flush=True)

    # ---- verdict ----
    V = {
        "T_HAPPY (git-first→vindex-second→COMMITTED pair, serves edit)":
            R["T_HAPPY"]["status"] == "COMMITTED" and R["T_HAPPY"]["paired"] and R["T_HAPPY"]["serves_edit"],
        "T_D46 (git-fail→vindex untouched, Weights-ahead unreachable)":
            R["T_D46_GITFAIL"]["vindex_attempted"] is False and R["T_D46_GITFAIL"]["active_unchanged"],
        "T_COMP_STRUCT (≤3 retries→auto git-revert, no commit)":
            R["T_COMP_STRUCT"]["git_back_to_baseline"] and R["T_COMP_STRUCT"]["no_commit"],
        "T_COMP_L4 (park, NO auto-revert; operator-confirm reverts)":
            R["T_COMP_L4"]["no_auto_revert"] and R["T_COMP_L4"]["operator_revert_ok"],
        "T_ROLLBACK_DUAL (COMMITTED→dual rollback→serves original Paris)":
            R["T_ROLLBACK_DUAL"]["git_rolled_back"] and R["T_ROLLBACK_DUAL"]["vindex_at_base"] and R["T_ROLLBACK_DUAL"]["serves_original"],
        "T_DIVERGE (git-OOB + vindex-flip → DIVERGED → trip)":
            R["T_DIVERGE"]["git_oob_detected"] and R["T_DIVERGE"]["git_tripped"] and R["T_DIVERGE"]["vindex_flip_detected"],
        "T_PARK_NOT_DIVERGE (sanctioned park ≠ divergence)":
            R["T_PARK_NOT_DIVERGE"]["reconcile_not_diverged"] and R["T_PARK_NOT_DIVERGE"]["no_diverged_state_entry"],
        "T_CIRCUIT (trip→READ_ONLY→reject→both reset arms gate→resume)":
            R["T_CIRCUIT"]["write_rejected_when_tripped"] and R["T_CIRCUIT"]["bad_reset_comp_refused"]
            and R["T_CIRCUIT"]["bad_reset_overlay_refused"] and R["T_CIRCUIT"]["good_reset_admitted"]
            and R["T_CIRCUIT"]["resumed_committed"],
        "T_LEDGER (chain intact; every COMMITTED has PREPARED)":
            R["T_LEDGER"]["chain_intact"] and R["T_LEDGER"]["all_committed_have_prepared"],
        "T_TPC4 (fabricated COMMITTED-without-PREPARED is DETECTED)":
            R["T_TPC4"]["detected"] and R["T_TPC4"]["legit_not_flagged"],
    }
    R["VERDICT"] = V
    R["scope_and_caveats"] = {
        "scope": "Dual-medium 2PC (Git+.vindex) with D46 ordering, TC compensation (C-TC2 asymmetry), "
                 "circuit breaker (D48), Git↔overlay ledger pairing + divergence detection.",
        "compensation_in_failure_path": "reverts GIT ONLY (vindex written second, never mounted on failure). "
                                        "The vindex-side reversal is exercised separately by T_ROLLBACK_DUAL.",
        "divergence_detection_asymmetry": "GIT side = real content (`git rev-parse HEAD` != recorded commit). "
                                          "VINDEX side = METADATA consistency (active-pointer's self-reported "
                                          "overlay_hash != ledger field) — NOT artifact integrity (overlay not "
                                          "re-hashed). Content-level vindex integrity = G2/G6.",
        "rollback_test": "T_ROLLBACK_DUAL serves FROZEN_BASE directly (immutable; always Paris). It proves "
                         "the COMPOSITION 'pointer removed (active is None) AND base independently serves "
                         "original', NOT an end-to-end serve-through-resolver after rollback.",
        "reset_stub": "Reset = precondition-checked stub for the full IC-TC-RESET CeremonyToken/CAK flow "
                      "(§11.8.1) → G2/v2. BOTH precondition arms are now exercised (compensation-completed + "
                      "overlay==last-COMMITTED).",
        "other_stubs": "PREPARED-timeout (§11.5.1, 2hr) DEFERRED (untestable in a prototype). 'No "
                       "self-compensate' is CONSTRUCTION-ASSERTED (the executor has no revert path) — NOT in "
                       "the verdict, not behaviorally enforced. Cross-task 5-in-10min trip path is coded but "
                       "UNTESTED (headline circuit test exercises the 3-consecutive path).",
    }
    json.dump(R, open(RESULT_PATH, "w"), indent=2)
    print("\n" + "=" * 72); print("G1 VERDICT")
    for k, v in V.items(): print(f"   [{'PASS' if v else 'FAIL'}] {k}")
    print("=" * 72); print(f"all_pass={all(V.values())}  -> {RESULT_PATH}", flush=True)

if __name__ == "__main__":
    main()
