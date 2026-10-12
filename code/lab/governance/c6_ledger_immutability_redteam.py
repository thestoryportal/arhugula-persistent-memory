import os, sys, json, time
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
sys.path.insert(0, f"{LLMDB_ROOT}/experiments/governance")

# ============================================================================
# C6 — Ledger-immutability red-team (D-C6L-1).  Pre-reg: docs/C6_LEDGER_IMMUTABILITY_REDTEAM_PREREG.md
#
# ⚠ This is a PROPERTY DEMONSTRATION + a SPEC-LEVEL finding, NOT an "empirical red-team."
# K1/K2/K4/K5 outcomes are fully predictable from reading verify_chain (and K1 is already a
# stated caveat in CORPUS/11). The harness only confirms the known property holds against the
# REAL G2 code path and that a concrete, custody-compatible fix works. The actual finding is K6,
# resolved by reading the spec (the W3 self-undermining tension), not by this rig.
#
# Reuses the REAL G2 ledger so the demo runs against the actual mechanism, not a strawman.
# ============================================================================
from g2_security_layer import StateLedger, _sha, _canon, KeyPair, verify  # the actual G2 code

GENESIS = StateLedger.GENESIS

# ---- helpers operating on the on-disk ledger file (attacker has FILE WRITE only) ----
def read_raw(path):
    with open(path) as f: return [json.loads(l) for l in f if l.strip()]

def write_raw(path, entries):
    with open(path, "w") as f:
        for e in entries: f.write(json.dumps(e) + "\n")

def rechain(entries):
    """Recompute prev_hash + entry_hash for every entry from the constant GENESIS root,
    using the SAME _sha/_canon verify_chain uses. This is the keyless rewrite primitive."""
    tip = GENESIS
    for e in entries:
        e["prev_hash"] = tip
        e["entry_hash"] = _sha(e["prev_hash"].encode() + _canon(e["body"]))
        tip = e["entry_hash"]
    return entries

def build_operational_ledger(path):
    """A plausible operational window INCLUDING a W3 INTEGRITY_VIOLATION_EMERGENCY entry —
    the spec's own compromised-Orchestrator response (§16.2). The attack will target it."""
    L = StateLedger(path)
    L.append("PROJECT_INITIATED", {"retention": "PROJECT_LIFETIME"}, "LIFECYCLE")
    L.append("ORCHESTRATOR_KEY_ANCHOR", {"anchor": "pub-abc"}, "SECURITY")
    L.append("PREPARED", {"txn": "t1", "pkg_hash": "h1"}, "CONSISTENCY")
    L.append("COMMITTED", {"txn": "t1", "overlay_hash": "o1"}, "CONSISTENCY")
    # the W3 emergency entry that flags the compromise (the thing a compromised writer wants gone):
    L.append("INTEGRITY_VIOLATION_EMERGENCY",
             {"reason": "orchestrator_self_authorization_detected", "evidence": "ledger-bypass at seq 3"}, "SECURITY")
    L.append("PREPARED", {"txn": "t2", "pkg_hash": "h2"}, "CONSISTENCY")
    L.append("COMMITTED", {"txn": "t2", "overlay_hash": "o2"}, "CONSISTENCY")
    return L

# ---- Defense D: CT-style Signed Tree Head (STH). Offline key (private half NOT held by the
#      ledger writer/Gate) signs (seq, tip). Same offline-custody model the spec uses for the CAK
#      (§20.2). STHs live OUT-OF-BAND (attacker has ledger-file write only). ----
class STHService:
    def __init__(self):
        self.key = KeyPair("STH_OFFLINE")       # offline; attacker cannot sign
        self.pub = self.key.pub
        self.heads = []                          # out-of-band store
    def checkpoint(self, path):
        es = read_raw(path)
        seq = len(es); tip = es[-1]["entry_hash"] if es else GENESIS
        msg = _canon({"seq": seq, "tip": tip})
        self.heads.append({"seq": seq, "tip": tip, "sig": self.key.sign(msg)})
    def verify_with_sth(self, path):
        """verify_chain() AND reconcile against the latest signed head (covers operational window)."""
        L = StateLedger.__new__(StateLedger); L.path = path; L._tip = GENESIS  # wrap existing file
        chain_ok, brk = L.verify_chain()
        if not chain_ok:
            return False, f"chain-break@seq{brk}"           # catches naive (A4)
        if not self.heads:
            return True, "no-sth"
        sth = max(self.heads, key=lambda h: h["seq"])
        if not verify(self.pub, _canon({"seq": sth["seq"], "tip": sth["tip"]}), sth["sig"]):
            return False, "sth-signature-invalid"           # attacker can't forge this
        es = read_raw(path)
        # rollback / truncation: current length < last signed seq
        if len(es) < sth["seq"]:
            return False, f"rollback: len {len(es)} < signed seq {sth['seq']}"
        # history rewrite: recompute tip over the first sth.seq entries; must equal the signed tip
        tip = GENESIS
        for e in es[:sth["seq"]]:
            tip = _sha(e["prev_hash"].encode() + _canon(e["body"]))
        if tip != sth["tip"]:
            return False, "history-rewrite: tip@seq != signed STH"
        return True, "ok"

def detect_str(ok_intact):  # verify returns INTACT(True) => attack UNDETECTED
    return "UNDETECTED" if ok_intact else "DETECTED"

def main():
    path = f"{LLMDB_ROOT}/results/c6_redteam_ledger.jsonl"
    results = {}

    # ---------- K1: rewrite-then-recompute (keyless) targeting the W3 entry ----------
    build_operational_ledger(path)
    es = read_raw(path)
    w3_idx = next(i for i, e in enumerate(es) if e["entry_type"] == "INTEGRITY_VIOLATION_EMERGENCY")
    # attacker neutralizes the W3 emergency record, then recomputes the whole chain from root
    es[w3_idx]["entry_type"] = "COMMITTED"
    es[w3_idx]["body"] = {"txn": "t1b", "overlay_hash": "o1b"}   # the compromise evidence is gone
    es[w3_idx]["audit_category"] = "CONSISTENCY"
    write_raw(path, rechain(es))
    Lv = StateLedger.__new__(StateLedger); Lv.path = path; Lv._tip = GENESIS
    k1_ok, k1_brk = Lv.verify_chain()
    results["K1_rewrite_recompute"] = {
        "attack": "rewrite+suppress the W3 INTEGRITY_VIOLATION_EMERGENCY entry, recompute all hashes from root (keyless)",
        "verify_chain_intact": k1_ok, "break_at": k1_brk, "outcome": detect_str(k1_ok),
        "predicted": "UNDETECTED", "note": "known property (CORPUS/11 caveat); confirms vs real G2 verify_chain"}

    # ---------- K2: completeness/truncation (same property, reported) ----------
    build_operational_ledger(path)
    es = read_raw(path)
    write_raw(path, es[:4])                      # drop the W3 entry + everything after it
    Lv = StateLedger.__new__(StateLedger); Lv.path = path; Lv._tip = GENESIS
    k2_ok, _ = Lv.verify_chain()
    results["K2_truncation"] = {
        "attack": "drop the suffix (incl. the W3 entry); present the prefix as current",
        "verify_chain_intact": k2_ok, "outcome": detect_str(k2_ok),
        "predicted": "UNDETECTED", "note": "completeness not verified by chain-walk; variant of K1's root property"}

    # ---------- K4: naive edit (CONTROL — must be caught) ----------
    build_operational_ledger(path)
    es = read_raw(path)
    es[w3_idx]["body"] = {"reason": "REDACTED"}  # edit WITHOUT recomputing successors
    write_raw(path, es)
    Lv = StateLedger.__new__(StateLedger); Lv.path = path; Lv._tip = GENESIS
    k4_ok, k4_brk = Lv.verify_chain()
    results["K4_naive_edit_CONTROL"] = {
        "attack": "edit the W3 body WITHOUT recomputing successor hashes",
        "verify_chain_intact": k4_ok, "break_at": k4_brk, "outcome": detect_str(k4_ok),
        "predicted": "DETECTED", "note": "reproduces G2 T-LEDGER-TAMPER; confirms the walk actually runs"}

    # ---------- K5: Defense D (STH-style signed head-anchor) catches K1 and K2 ----------
    sth = STHService()
    build_operational_ledger(path)
    sth.checkpoint(path)                          # sign the head AFTER the operational window
    # replay A1 (rewrite-recompute) on the same file
    es = read_raw(path)
    es[w3_idx]["entry_type"] = "COMMITTED"; es[w3_idx]["body"] = {"txn": "t1b"}; es[w3_idx]["audit_category"] = "CONSISTENCY"
    write_raw(path, rechain(es))
    d_a1_ok, d_a1_why = sth.verify_with_sth(path)
    # replay A2 (truncation) — rebuild + re-checkpoint, then truncate
    sth2 = STHService(); build_operational_ledger(path); sth2.checkpoint(path)
    es = read_raw(path); write_raw(path, es[:4])
    d_a2_ok, d_a2_why = sth2.verify_with_sth(path)
    results["K5_defense_STH"] = {
        "defense": "CT-style Signed Tree Head: offline key (NOT held by ledger writer; same custody as CAK §20.2) signs (seq,tip) out-of-band; verify = chain-walk + reconcile latest signed head + monotonic seq",
        "A1_rewrite_outcome": detect_str(d_a1_ok), "A1_reason": d_a1_why,
        "A2_truncation_outcome": detect_str(d_a2_ok), "A2_reason": d_a2_why,
        "predicted": "DETECTED both", "note": "fix works; offline-key custody is the model the spec already mandates for the CAK"}

    # ---------- K6: the finding — spec audit, split into TWO claims (advisor-refined; read, not run) ----------
    results["K6_spec_finding"] = {
        "claim_A_threat_model_INDEPENDENT": {
            "claim": "The spec mandates NO operational-window cryptographic tamper-evidence for the ledger.",
            "evidence": ["§16.1 Merkle-chain-lite, keyless (entry_hash=SHA(prev||body), entries NOT individually signed — confirmed in G2 code)",
                         "§16.4 integrity = chain-walk from Genesis Seal forward (boot/100/10K-24h) — internal consistency only",
                         "§13.2 Genesis Seal = immutable ROOT anchor (anchors the START)",
                         "§16.7/§27 FINAL_STATE_SNAPSHOT = externally-committed tip hash only at PROJECT_CLOSE",
                         "=> external anchors exist ONLY at root + close; nothing during operation"],
            "status": "CONFIRMED spec-level property (established by reading §16 end-to-end). Elevates CORPUS/11's prototype caveat from 'not modeled here' to 'not specified by the spec'. Solid regardless of threat model.",
            "fix": "CT-style Signed Tree Head: periodic offline-signed (seq,tip) head-anchor + monotonic seq, verified at boot/cadence. Custody-compatible with the CAK offline/HSM model the spec ALREADY mandates (§20.2). K5 demonstrates it closes K1+K2."},
        "claim_B_W3_threat_model_SEAM": {
            "claim": "Under the spec's OWN threat model, the missing operational-window tamper-evidence is security-relevant: the W3 emergency-logging response shares a mutable substrate with its adversary — an UNRECONCILED threat-model seam (NOT a flat contradiction).",
            "logical_vs_filesystem": "W3 (§16.2) defends against LOGICAL Orchestrator compromise (won't mediate W1 honestly -> Gate/TC/Boot-verifier BYPASS it to log INTEGRITY_VIOLATION_EMERGENCY). Defeating W3 via rewrite-recompute (K1) needs FILESYSTEM-level tampering — a DIFFERENT capability.",
            "is_a_clause_covering_it": "§16.5 access control IS the spec's intended ledger-integrity defense (fs-write restricted to Orchestrator/Boot-verifier/Retention-Manager). So a covering mechanism EXISTS — but it does not fully cover this case:",
            "why_not_covered": "§16.5 GRANTS the Orchestrator ledger fs-write, and §16.2 admits the Orchestrator as compromisable. §5 excludes only PHYSICAL host security — a LOGICALLY-compromised Orchestrator running with its normally-granted fs-access needs no physical/host compromise to rewrite the file. The spec never RECONCILES §16.5 (Orchestrator has ledger fs-write) with §16.2 (Orchestrator compromise in-scope) -> the W3 emergency entry meant to flag the compromise lands in the keyless ledger the same component can rewrite/suppress (K1), with the §16.4 walk still INTACT.",
            "status": "UNRECONCILED THREAT-MODEL SEAM (precise, threat-model-scoped). Live, not hypothetical, because §5 carves out only physical compromise."},
        "verdict": "Operational-window ledger tamper-evidence is UNSPECIFIED (claim A); under §16.2's own threat model it is security-relevant because the W3 response shares the substrate (claim B). Recommended backstop = STH head-anchor.",
        "scope_excluded": {
            "A3_fork_equivocation": "distributed-log/CT threat needing independent monitors comparing STHs; multi-machine ledger replication is v2/GAP-18 -> out-of-architecture for single-machine v1.2",
            "timestamp_rewrite__interior_insert_delete": "special cases of K1 (rewrite-recompute)",
            "second_preimage_domain_separation": "low risk: prev_hash is fixed-width 64-hex -> effectively length-delimited",
            "key_custody": "separate C6 sub-item (operational/v2), not addressed here"}}

    verdict = {
        "demo_K1_undetected": results["K1_rewrite_recompute"]["outcome"] == "UNDETECTED",
        "demo_K2_undetected": results["K2_truncation"]["outcome"] == "UNDETECTED",
        "control_K4_detected": results["K4_naive_edit_CONTROL"]["outcome"] == "DETECTED",
        "fix_K5_detects_both": results["K5_defense_STH"]["A1_rewrite_outcome"] == "DETECTED" and results["K5_defense_STH"]["A2_truncation_outcome"] == "DETECTED",
        "finding_K6A_property": results["K6_spec_finding"]["claim_A_threat_model_INDEPENDENT"]["status"][:60],
        "finding_K6B_seam": "UNRECONCILED THREAT-MODEL SEAM",
    }
    out = {
        "experiment": "C6_ledger_immutability_redteam", "decision_id": "D-C6L-1",
        "class": "PROPERTY DEMONSTRATION + SPEC-LEVEL SECURITY FINDING (NOT an empirical red-team; NOT a spec falsification; NOT promotable)",
        "honesty_note": "K1/K2/K4/K5 are predictable from reading verify_chain (K1 = CORPUS/11 caveat); the harness confirms the known property holds against the REAL G2 code + that the fix works. The load-bearing finding is K6, resolved by reading the spec.",
        "ts": round(time.time(), 3),
        "checks": results,
        "verdict_summary": verdict,
        "verdict": ("C6 ledger-immutability — TWO claims. (A, threat-model-INDEPENDENT, solid): the spec mandates NO "
                    "operational-window cryptographic tamper-evidence — keyless chain (§16.1), external anchors only at "
                    "root (§13.2) and close (§16.7/§27); a rewrite-recompute (K1) or truncation (K2) leaves the §16.4 "
                    "chain-walk INTACT. This elevates CORPUS/11's prototype caveat to a confirmed SPEC-level property "
                    "(established by reading §16 end-to-end). (B, threat-model-SCOPED, sharper): the spec never reconciles "
                    "§16.5 (Orchestrator granted ledger fs-write) with §16.2 (Orchestrator compromise in-scope) — and §5 "
                    "excludes only PHYSICAL host security — so a logically-compromised Orchestrator can rewrite/suppress "
                    "the very W3 emergency entry meant to flag it. An UNRECONCILED THREAT-MODEL SEAM, not a flat "
                    "contradiction. Fix = CT-style offline-signed head-anchor (K5 works), custody-compatible with the "
                    "spec's CAK model (§20.2). Moves C6 'verifier-mechanics-proven, not red-teamed' -> 'red-teamed: named "
                    "gap (A) + named seam (B) + named, custody-compatible fix.' Self-authored harness, independence-"
                    "mitigated (vectors cross-checked vs Perplexity/CT literature; run against the real G2 verify_chain). "
                    "Property-demo + spec finding, NOT a spec falsification, NOT promotable."),
        "scope_caveats": "CPU-only; reuses the real G2 StateLedger/verify_chain; threat model = ledger-file write access "
                         "(compromised-Orchestrator/fs, admitted by §16.2 W3). A3/timestamp/2nd-preimage surveyed-and-excluded "
                         "(see K6.scope_excluded). Key custody = separate C6 sub-item. Falsifiable by a spec clause mandating an "
                         "operational-window signed head-anchor that this audit missed.",
    }
    op = f"{LLMDB_ROOT}/results/c6_ledger_immutability_redteam.json"
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(out, open(op, "w"), indent=2)
    print("WROTE", op)
    for k, v in verdict.items(): print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
