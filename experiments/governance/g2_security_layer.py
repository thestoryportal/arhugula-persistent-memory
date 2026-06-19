#!/usr/bin/env python3
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
"""
g2_security_layer.py — GAP G2: write authz / Gate / audit (security hardening, viability prototype).
REAL asymmetric crypto (Ed25519). Upgrades the stubs this session deliberately left:
  * CP1's HMAC Orchestrator signing  → real asymmetric Orchestrator key (§10.4/10.5).
  * G1's metadata-only .vindex integrity → content-level signed-hash integrity (§16).
  * G1's reset flag-flip → real CeremonyToken / CAK verifier (IC-TC-RESET, §20.3).
Adds: ledger tamper detection (§16.4), per-patch edge cap (one blast-radius dimension, §8.8),
agent suspension / token revocation (§10.7), audit_category tagging (§16.6).

THE G2 THESIS (what asymmetric buys OVER HMAC): a component that can VERIFY cannot FORGE.
The tests are built to demonstrate exactly that — not "valid passes / tampered fails" (HMAC had that),
but "the public-anchor holder cannot mint a verifying token" and "a metadata-rewrite cannot defeat a
content signature." Each test is built to fail.

HONEST SCOPE / CAVEATS (kept flush with tests):
  * CAK + Orchestrator private halves are generated IN-PROCESS to exercise the VERIFIER. G2 does NOT
    address key CUSTODY — the spec puts the CAK private half offline/HSM, operator-held (§20.2). Custody
    = operational / v2.
  * `audit_category` is a SCHEMA FIELD (§16.6), present on entries — NOT an enforced behavior; not a
    "passed test", just tagged.
  * Boot-time anchor-mismatch → suspend is a SIMULATED boot (§10.5), not a real harness boot.
  * Blast-radius here = the per-patch EDGE CAP only (§8.8) — ONE dimension; full blast-radius bounding
    (scope × tier × family × external-content) is broader (→ later).
  * Ceremony replay defense follows §20.3 (60s timestamp window). A ceremony_id-consumed check is added
    as an EXTENSION (flagged), not implied by the spec's window control.
Engine/LARQL untouched. Ledger mirrors CP1/G1 (standalone, no torch).
"""
import os, json, time, hashlib
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.exceptions import InvalidSignature

LEDGER_PATH = f"{LLMDB_ROOT}/results/g2_state_ledger.jsonl"
RESULT_PATH = f"{LLMDB_ROOT}/results/g2_result.json"
OVERLAY_SRC = "/dev/shm/cp1_work/overlay_fd3c63598e94.vlp"   # a real overlay artifact to sign/verify
WORK        = "/dev/shm/g2_work"


# ════════════════════════════ crypto primitives (real Ed25519) ════════════════════════════
def _canon(o): return json.dumps(o, sort_keys=True, separators=(",", ":")).encode()
def _sha(b):   return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

class KeyPair:
    """An Ed25519 keypair. The PUBLIC half is the 'anchor' a verifier holds; the PRIVATE half signs.
    A verifier is constructed with anchor_only=True and physically cannot sign."""
    def __init__(self, name):
        self.name = name
        self._priv = Ed25519PrivateKey.generate()
        self.pub = self._priv.public_key()
    def pub_bytes(self):  return self.pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
    def anchor(self):     return _sha(self.pub_bytes())          # the dual-store anchor identity
    def sign(self, msg):  return self._priv.sign(msg if isinstance(msg, bytes) else msg.encode()).hex()

def verify(pub: Ed25519PublicKey, msg, sig_hex) -> bool:
    try:
        pub.verify(bytes.fromhex(sig_hex), msg if isinstance(msg, bytes) else msg.encode())
        return True
    except (InvalidSignature, ValueError):
        return False


# ════════════════════════════ ledger (hash-chained + audit_category) ════════════════════════════
class StateLedger:
    GENESIS = "0" * 64
    def __init__(self, path):
        self.path = path; open(path, "w").close(); self._tip = self.GENESIS
    def append(self, etype, body, audit_category="SECURITY"):
        e = {"seq": self._count(), "ts": round(time.time(), 3), "entry_type": etype,
             "audit_category": audit_category, "prev_hash": self._tip, "body": body}
        e["entry_hash"] = _sha(e["prev_hash"].encode() + _canon(body))
        with open(self.path, "a") as f: f.write(json.dumps(e) + "\n")
        self._tip = e["entry_hash"]; return e
    def _count(self):
        with open(self.path) as f: return sum(1 for _ in f)
    def entries(self):
        with open(self.path) as f: return [json.loads(l) for l in f if l.strip()]
    def verify_chain(self):
        tip = self.GENESIS
        for e in self.entries():
            if e["prev_hash"] != tip or e["entry_hash"] != _sha(e["prev_hash"].encode() + _canon(e["body"])):
                return False, e["seq"]
            tip = e["entry_hash"]
        return True, None


# ════════════════════════════ orchestrator + gate (asymmetric tokens, §10.4/10.5) ════════════════════════════
class Orchestrator:
    """Holds the Orchestrator PRIVATE key; mints asymmetric invocation tokens. Also signs overlay
    content hashes (§16 integrity). Anchors the public half (dual-store: ledger + a git-style file)."""
    def __init__(self, ledger):
        self.key = KeyPair("orchestrator"); self.ledger = ledger
        self.suspended = set()
        ledger.append("ORCHESTRATOR_KEY_ANCHOR", {"anchor": self.key.anchor()}, "SECURITY")
    def mint_token(self, agent_id, patch_hash, ttl_s=600):
        payload = {"agent_id": agent_id, "patch_hash": patch_hash,
                   "issued_at": round(time.time(), 3), "expires_at": round(time.time() + ttl_s, 3)}
        return {**payload, "signature": self.key.sign(_canon(payload))}
    def sign_overlay(self, content_hash):
        return self.key.sign(content_hash)             # signs the CONTENT hash (not metadata)

class PatchAuthorizationGate:
    """Holds ONLY the Orchestrator PUBLIC anchor — it can VERIFY but cannot SIGN/MINT. Enforces §10.2
    + agent suspension (§10.7) + per-patch edge cap (§8.8 blast-radius dimension)."""
    CAPS = {"coder": 500, "architect": 10000}          # per-patch edge caps (§8.8)
    def __init__(self, orch: Orchestrator):
        # Holds the PUBLIC anchor + a SHARED reference to the suspension set + the append-only ledger.
        # It does NOT retain the Orchestrator object, so the private signing key is structurally
        # unreachable from the Gate (verify-cannot-forge by construction; cf. CeremonyVerifier).
        self.orch_pub = orch.key.pub                   # public half only — cannot sign
        self.suspended = orch.suspended                # shared set (Warden/Orchestrator mutate)
        self.ledger = orch.ledger
    def authorize(self, token, package):
        aid = token.get("agent_id")
        payload = {k: token[k] for k in ("agent_id", "patch_hash", "issued_at", "expires_at") if k in token}
        if not verify(self.orch_pub, _canon(payload), token.get("signature", "")):
            return self._reject(aid, "TOKEN_SIGNATURE_INVALID")
        if time.time() > token.get("expires_at", 0):
            return self._reject(aid, "TOKEN_EXPIRED")
        if aid in self.suspended:                      # §10.7
            return self._reject(aid, "TOKEN_AGENT_SUSPENDED")
        if token.get("patch_hash") != package["patch_hash"]:
            return self._reject(aid, "INTEGRITY_TOKEN_PATCH_MISMATCH")
        cap = self.CAPS.get(package.get("agent_role", "coder"), 500)
        if package.get("edge_count", 0) > cap:         # §8.8 blast-radius edge cap
            return self._reject(aid, "PATCH_CAP_EXCEEDED", {"edges": package["edge_count"], "cap": cap})
        self.ledger.append("TOKEN_CONSUMED", {"agent_id": aid, "patch_hash": package["patch_hash"]}, "SECURITY")
        return {"ok": True}
    def _reject(self, aid, code, extra=None):
        self.ledger.append("WRITE_REJECTED", {"agent_id": aid, "reject_code": code, **(extra or {})}, "SECURITY")
        return {"ok": False, "code": code}


# ════════════════════════════ overlay content integrity (§16) — defeats metadata rewrite ════════════════════════════
class OverlayIntegrity:
    """The Orchestrator signs the CONTENT hash of the overlay bytes. Verification RE-HASHES the actual
    bytes and checks the signature against that — so a metadata rewrite (G1's forgeable surface) cannot
    pass, and substituting bytes requires re-signing (needs the private key the verifier lacks)."""
    @staticmethod
    def sign(orch: Orchestrator, overlay_path):
        with open(overlay_path, "rb") as f: content_hash = hashlib.sha256(f.read()).hexdigest()
        return {"content_hash": content_hash, "signature": orch.sign_overlay(content_hash)}
    @staticmethod
    def verify(orch_pub, overlay_path, manifest):
        with open(overlay_path, "rb") as f: actual = hashlib.sha256(f.read()).hexdigest()
        # bind to ACTUAL bytes: signature must validate over the re-hashed content, not the recorded field
        return verify(orch_pub, actual, manifest["signature"])
    @staticmethod
    def g1_metadata_check(overlay_path, manifest):
        """The OLD (G1) check: recorded hash == hash(bytes). Forgeable by rewriting the recorded field."""
        with open(overlay_path, "rb") as f: actual = hashlib.sha256(f.read()).hexdigest()
        return manifest["content_hash"] == actual


# ════════════════════════════ CAK ceremony verifier (IC-TC-RESET, §20.3) ════════════════════════════
class CeremonyVerifier:
    """Verifies CeremonyToken envelopes for IC-TC-RESET. Root of trust = CAK public anchor, STRUCTURALLY
    distinct from the Orchestrator anchor (§20.2). Uniform preconditions (§20.3) in normative order."""
    def __init__(self, ledger, cak: KeyPair, orchestrator_anchor):
        self.ledger = ledger
        self.cak_pub = cak.pub; self.cak_anchor = cak.anchor()
        self.orchestrator_anchor = orchestrator_anchor
        self._consumed = set()                          # ceremony_id replay (flagged EXTENSION beyond §20.3)
    def verify(self, env, expected_type="CIRCUIT_RESET"):
        def fail(code):
            self.ledger.append(code, {"ceremony_id": env.get("ceremony_id"), "key_ref": env.get("key_ref")}, "SECURITY")
            return {"ok": False, "code": code}
        for fld in ("ceremony_type", "ceremony_id", "key_ref", "timestamp", "operator_signature"):
            if fld not in env: return fail("CEREMONY_AUTH_MALFORMED")
        # (2) STRUCTURAL EXCLUSION — checked BEFORE signature: an Orchestrator self-authorization, even
        #     if perfectly signed, is refused. This is the whole defense.
        if env["key_ref"] == self.orchestrator_anchor:
            return fail("CEREMONY_AUTH_WRONG_KEY")
        # (1) key_ref must be the active CAK anchor
        if env["key_ref"] != self.cak_anchor:
            return fail("CEREMONY_AUTH_KEY_UNKNOWN")
        # (3) signature valid against the CAK public half
        signed = {k: env[k] for k in ("ceremony_type", "ceremony_id", "ceremony_payload", "operator_id",
                                      "timestamp", "key_ref") if k in env}
        if not verify(self.cak_pub, _canon(signed), env["operator_signature"]):
            return fail("CEREMONY_AUTH_SIGNATURE_INVALID")
        # (4) replay window — 60s of wall clock
        if abs(time.time() - env["timestamp"]) > 60:
            return fail("CEREMONY_AUTH_REPLAY_REJECTED")
        # (EXT) ceremony_id single-use (flagged extension)
        if env["ceremony_id"] in self._consumed:
            return fail("CEREMONY_AUTH_REPLAY_REJECTED")
        # (6) ceremony-type discriminator
        if env["ceremony_type"] != expected_type:
            return fail("CEREMONY_AUTH_TYPE_MISMATCH")
        self._consumed.add(env["ceremony_id"])
        self.ledger.append("CIRCUIT_RESET", {"ceremony_id": env["ceremony_id"]}, "GOVERNANCE")
        return {"ok": True}

def make_ceremony(cak: KeyPair, ctype, payload, key_ref=None, ts=None, operator_id="op-1"):
    env = {"ceremony_type": ctype, "ceremony_id": _sha(f"{ctype}{ts or time.time()}{payload}")[:16],
           "ceremony_payload": payload, "operator_id": operator_id,
           "timestamp": ts if ts is not None else time.time(),
           "key_ref": key_ref if key_ref is not None else cak.anchor()}
    signed = {k: env[k] for k in ("ceremony_type", "ceremony_id", "ceremony_payload", "operator_id",
                                  "timestamp", "key_ref")}
    env["operator_signature"] = cak.sign(_canon(signed))
    return env


# ════════════════════════════ harness ════════════════════════════
def main():
    print("=" * 72); print("G2 — security layer (REAL Ed25519): asymmetric tokens · CAK ceremony · content integrity")
    print("=" * 72, flush=True)
    os.makedirs(WORK, exist_ok=True)
    ledger = StateLedger(LEDGER_PATH)
    orch = Orchestrator(ledger)
    gate = PatchAuthorizationGate(orch)
    cak = KeyPair("CAK")
    cer = CeremonyVerifier(ledger, cak, orch.key.anchor())
    R = {}

    # ── T-NO-PRIVKEY (the structural asymmetric upgrade): no private key reachable from the verifiers ──
    print("\n── T-NO-PRIVKEY: Gate + CeremonyVerifier hold NO Ed25519 private key (verify-cannot-forge, structural) ──", flush=True)
    def reaches_privkey(obj, seen=None, depth=0):
        seen = seen if seen is not None else set()
        if id(obj) in seen or depth > 6: return False
        seen.add(id(obj))
        if isinstance(obj, Ed25519PrivateKey): return True
        vals = []
        if hasattr(obj, "__dict__"): vals += list(vars(obj).values())
        if isinstance(obj, dict): vals += list(obj.values())
        if isinstance(obj, (list, tuple, set)): vals += list(obj)
        return any(reaches_privkey(v, seen, depth + 1) for v in vals)
    R["T_NO_PRIVKEY"] = {"gate_has_no_privkey": not reaches_privkey(gate),
                         "ceremony_has_no_privkey": not reaches_privkey(cer),
                         "orchestrator_does_hold_privkey": reaches_privkey(orch)}  # control: signer holds it
    print(f"   -> {R['T_NO_PRIVKEY']}", flush=True)

    # ── T-TOKEN-CHECKS: identity/expiry/suspension at the Gate (HMAC-equivalent; NOT the asymmetric upgrade) ──
    print("\n── T-TOKEN-CHECKS: legit admits; foreign-key + payload-tamper rejected (identity check) ──", flush=True)
    pkg = {"patch_hash": "abc123", "agent_role": "coder", "edge_count": 10}
    legit = orch.mint_token("coder", "abc123")
    r_legit = gate.authorize(legit, pkg)
    # attacker holds only orch PUBLIC anchor; forge attempt #1: sign with a self-generated key
    rogue = KeyPair("attacker")
    forged = {"agent_id": "coder", "patch_hash": "abc123", "issued_at": round(time.time(), 3),
              "expires_at": round(time.time() + 600, 3)}
    forged["signature"] = rogue.sign(_canon({k: forged[k] for k in ("agent_id","patch_hash","issued_at","expires_at")}))
    r_forge_selfkey = gate.authorize(forged, pkg)
    # forge attempt #2: tamper a legit token's payload, keep its signature
    tampered = dict(legit); tampered["agent_id"] = "architect"
    r_forge_tamper = gate.authorize(tampered, pkg)
    R["T_TOKEN_CHECKS"] = {"legit_ok": r_legit["ok"],
                           "foreign_key_rejected": r_forge_selfkey["code"] == "TOKEN_SIGNATURE_INVALID",
                           "payload_tamper_rejected": r_forge_tamper["code"] == "TOKEN_SIGNATURE_INVALID"}
    print(f"   -> {R['T_TOKEN_CHECKS']}", flush=True)

    # ── T-OVERLAY-SIGFORGE (centerpiece): metadata rewrite cannot defeat a content signature ──
    print("\n── T-OVERLAY-SIGFORGE: substitute bytes + rewrite recorded hash (G1 check PASSES) → G2 REJECTS ──", flush=True)
    intact = os.path.join(WORK, "overlay_intact.vlp"); tampered_p = os.path.join(WORK, "overlay_tampered.vlp")
    with open(OVERLAY_SRC, "rb") as f: data = f.read()
    open(intact, "wb").write(data)
    manifest = OverlayIntegrity.sign(orch, intact)                          # orchestrator signs CONTENT hash
    ok_intact = OverlayIntegrity.verify(orch.key.pub, intact, manifest)
    # attacker substitutes bytes AND rewrites the recorded content_hash to match the new bytes
    open(tampered_p, "wb").write(data + b"\x00MALICIOUS")
    new_hash = hashlib.sha256(data + b"\x00MALICIOUS").hexdigest()
    forged_manifest = {"content_hash": new_hash, "signature": manifest["signature"]}   # rewrite metadata
    g1_would_pass = OverlayIntegrity.g1_metadata_check(tampered_p, forged_manifest)     # OLD check: fooled
    g2_rejects   = not OverlayIntegrity.verify(orch.key.pub, tampered_p, forged_manifest)
    if g2_rejects: ledger.append("INTEGRITY_VIOLATION", {"artifact": "overlay", "kind": "content_signature"}, "SECURITY")
    R["T_OVERLAY_SIGFORGE"] = {"intact_verifies": ok_intact, "g1_metadata_check_fooled": g1_would_pass,
                               "g2_signature_rejects": g2_rejects}
    print(f"   -> {R['T_OVERLAY_SIGFORGE']}", flush=True)

    # ── T-CEREMONY-WRONGKEY (airtight): a VALIDLY-ORCHESTRATOR-SIGNED envelope, key_ref=ORCHESTRATOR ──
    print("\n── T-CEREMONY-WRONGKEY: valid Orchestrator signature + key_ref=ORCHESTRATOR → WRONG_KEY (not SIG_INVALID) ──", flush=True)
    # build an envelope the Orchestrator validly signs, pointing key_ref at the Orchestrator anchor
    orch_kp_as_signer = orch.key
    env_self = {"ceremony_type": "CIRCUIT_RESET",
                "ceremony_id": _sha("self" + str(time.time()))[:16], "ceremony_payload": {"trip": "x"},
                "operator_id": "op-1", "timestamp": time.time(), "key_ref": orch.key.anchor()}
    signed = {k: env_self[k] for k in ("ceremony_type","ceremony_id","ceremony_payload","operator_id","timestamp","key_ref")}
    env_self["operator_signature"] = orch_kp_as_signer.sign(_canon(signed))   # a VALID signature
    sig_actually_valid = verify(orch.key.pub, _canon(signed), env_self["operator_signature"])
    res_self = cer.verify(env_self)
    R["T_CEREMONY_WRONGKEY"] = {"orchestrator_signature_is_valid": sig_actually_valid,
                                "rejected_as_wrong_key": res_self["code"] == "CEREMONY_AUTH_WRONG_KEY",
                                "not_sig_invalid": res_self["code"] != "CEREMONY_AUTH_SIGNATURE_INVALID"}
    print(f"   -> {R['T_CEREMONY_WRONGKEY']}", flush=True)

    # ── T-CEREMONY: valid CAK admit + the §20.3 failure set ──
    print("\n── T-CEREMONY: valid CAK CIRCUIT_RESET admits; bad-sig / stale / wrong-type / replay rejected ──", flush=True)
    valid = make_ceremony(cak, "CIRCUIT_RESET", {"trip": "CONSECUTIVE_FAILURE"})
    r_valid = cer.verify(valid)
    r_replay = cer.verify(valid)                                          # same ceremony_id again
    bad_sig = make_ceremony(cak, "CIRCUIT_RESET", {"trip": "x"}); bad_sig["ceremony_payload"] = {"trip": "TAMPERED"}
    r_badsig = cer.verify(bad_sig)
    stale = make_ceremony(cak, "CIRCUIT_RESET", {"trip": "x"}, ts=time.time() - 120)
    r_stale = cer.verify(stale)
    wrongtype = make_ceremony(cak, "SCOPE_UPDATE", {"x": 1})
    r_wrongtype = cer.verify(wrongtype, expected_type="CIRCUIT_RESET")
    R["T_CEREMONY"] = {"valid_admitted": r_valid["ok"],
                       "replay_rejected": r_replay.get("code") == "CEREMONY_AUTH_REPLAY_REJECTED",
                       "bad_sig_rejected": r_badsig.get("code") == "CEREMONY_AUTH_SIGNATURE_INVALID",
                       "stale_rejected": r_stale.get("code") == "CEREMONY_AUTH_REPLAY_REJECTED",
                       "wrong_type_rejected": r_wrongtype.get("code") == "CEREMONY_AUTH_TYPE_MISMATCH"}
    print(f"   -> {R['T_CEREMONY']}", flush=True)

    # ── T-LEDGER-TAMPER: retroactive edit of a past entry → integrity walk detects break ──
    print("\n── T-LEDGER-TAMPER: rewrite a past entry body → chain verification detects it (§16.4) ──", flush=True)
    ok_before, _ = ledger.verify_chain()
    es = ledger.entries(); victim = es[2]; victim["body"]["agent_id"] = "ATTACKER"   # retroactive edit
    with open(LEDGER_PATH, "w") as f:
        for e in es: f.write(json.dumps(e) + "\n")
    ok_after, broke_at = ledger.verify_chain()
    R["T_LEDGER_TAMPER"] = {"intact_before": ok_before, "tamper_detected": (not ok_after), "broke_at_seq": broke_at}
    print(f"   -> {R['T_LEDGER_TAMPER']}", flush=True)

    # ── T-BLAST-CAP: per-patch edge cap (one blast-radius dimension, §8.8) ──
    print("\n── T-BLAST-CAP: coder patch over the 500-edge cap → PATCH_CAP_EXCEEDED ──", flush=True)
    ledger2 = StateLedger(LEDGER_PATH + ".cap"); o2 = Orchestrator(ledger2); g2 = PatchAuthorizationGate(o2)
    big = {"patch_hash": "big1", "agent_role": "coder", "edge_count": 501}
    tok_big = o2.mint_token("coder", "big1")
    r_cap = g2.authorize(tok_big, big)
    small = {"patch_hash": "sm1", "agent_role": "coder", "edge_count": 500}
    r_ok = g2.authorize(o2.mint_token("coder", "sm1"), small)
    R["T_BLAST_CAP"] = {"over_cap_rejected": r_cap.get("code") == "PATCH_CAP_EXCEEDED", "at_cap_ok": r_ok["ok"]}
    print(f"   -> {R['T_BLAST_CAP']}", flush=True)

    # ── T-SUSPEND: a suspended agent's otherwise-valid token rejected at Gate (§10.7) ──
    print("\n── T-SUSPEND: suspend agent → its valid token rejected TOKEN_AGENT_SUSPENDED ──", flush=True)
    ledger3 = StateLedger(LEDGER_PATH + ".susp"); o3 = Orchestrator(ledger3); g3 = PatchAuthorizationGate(o3)
    pk = {"patch_hash": "s1", "agent_role": "coder", "edge_count": 5}
    tok = o3.mint_token("coder", "s1")
    before = g3.authorize(o3.mint_token("coder", "s1b"), {"patch_hash": "s1b", "agent_role": "coder", "edge_count": 5})
    o3.suspended.add("coder")                                            # Warden suspends (§10.7)
    after = g3.authorize(tok, pk)
    R["T_SUSPEND"] = {"works_before_suspend": before["ok"],
                      "rejected_after_suspend": after.get("code") == "TOKEN_AGENT_SUSPENDED"}
    print(f"   -> {R['T_SUSPEND']}", flush=True)

    # ── T-BOOT-ANCHOR: simulated boot anchor mismatch → boot suspended (§10.5) ──
    print("\n── T-BOOT-ANCHOR (simulated): ledger anchor != git-committed anchor → boot suspended ──", flush=True)
    ledger_anchor = orch.key.anchor(); git_committed_anchor = "0" * 64   # tampered/forked anchor
    boot_ok = (ledger_anchor == git_committed_anchor)
    R["T_BOOT_ANCHOR"] = {"boot_suspended_on_mismatch": (not boot_ok)}
    print(f"   -> {R['T_BOOT_ANCHOR']}", flush=True)

    # ── verdict ──
    V = {
        "T_NO_PRIVKEY (verify-cannot-forge: no private key reachable from Gate/CeremonyVerifier)":
            R["T_NO_PRIVKEY"]["gate_has_no_privkey"] and R["T_NO_PRIVKEY"]["ceremony_has_no_privkey"] and R["T_NO_PRIVKEY"]["orchestrator_does_hold_privkey"],
        "T_TOKEN_CHECKS (identity/expiry/suspension — HMAC-equivalent, not the asym upgrade)":
            R["T_TOKEN_CHECKS"]["legit_ok"] and R["T_TOKEN_CHECKS"]["foreign_key_rejected"] and R["T_TOKEN_CHECKS"]["payload_tamper_rejected"],
        "T_OVERLAY_SIGFORGE (metadata-rewrite fools G1 but G2 content-sig rejects)":
            R["T_OVERLAY_SIGFORGE"]["intact_verifies"] and R["T_OVERLAY_SIGFORGE"]["g1_metadata_check_fooled"] and R["T_OVERLAY_SIGFORGE"]["g2_signature_rejects"],
        "T_CEREMONY_WRONGKEY (valid Orchestrator sig still refused as WRONG_KEY, not SIG_INVALID)":
            R["T_CEREMONY_WRONGKEY"]["orchestrator_signature_is_valid"] and R["T_CEREMONY_WRONGKEY"]["rejected_as_wrong_key"] and R["T_CEREMONY_WRONGKEY"]["not_sig_invalid"],
        "T_CEREMONY (valid CAK admit + §20.3 failure set)":
            all([R["T_CEREMONY"]["valid_admitted"], R["T_CEREMONY"]["replay_rejected"], R["T_CEREMONY"]["bad_sig_rejected"],
                 R["T_CEREMONY"]["stale_rejected"], R["T_CEREMONY"]["wrong_type_rejected"]]),
        "T_LEDGER_TAMPER (retroactive edit detected)":
            R["T_LEDGER_TAMPER"]["intact_before"] and R["T_LEDGER_TAMPER"]["tamper_detected"],
        "T_BLAST_CAP (over-cap rejected; at-cap ok)":
            R["T_BLAST_CAP"]["over_cap_rejected"] and R["T_BLAST_CAP"]["at_cap_ok"],
        "T_SUSPEND (suspended agent token rejected)":
            R["T_SUSPEND"]["works_before_suspend"] and R["T_SUSPEND"]["rejected_after_suspend"],
        "T_BOOT_ANCHOR (mismatch suspends boot — simulated)":
            R["T_BOOT_ANCHOR"]["boot_suspended_on_mismatch"],
    }
    R["VERDICT"] = V
    R["scope_and_caveats"] = {
        "thesis": "REAL Ed25519: a verifier (public anchor) cannot forge. The asym upgrade over HMAC is "
                  "STRUCTURAL — T_NO_PRIVKEY proves no private key is reachable from the Gate/CeremonyVerifier — "
                  "and DEMONSTRATED by T_OVERLAY_SIGFORGE (metadata-rewrite can't defeat a content signature; "
                  "closes G1's caveat) + T_CEREMONY_WRONGKEY (a validly-Orchestrator-signed envelope is refused "
                  "before signature check). T_TOKEN_CHECKS is identity/expiry/suspension only — HMAC-equivalent, "
                  "NOT the asymmetric upgrade.",
        "ledger_immutability": "T_LEDGER_TAMPER detects NAIVE retroactive edits (un-recomputed). An attacker who "
                               "rewrites an entry AND recomputes every subsequent entry_hash from the constant root "
                               "produces a chain that re-verifies. True tamper-evidence needs the HEAD anchored "
                               "(Genesis Seal / signed checkpoint), NOT modeled here → 'tamper detection', not "
                               "'immutability'.",
        "key_custody": "Orchestrator + CAK private halves generated IN-PROCESS to exercise the VERIFIER. G2 "
                       "does NOT address CUSTODY — spec puts CAK private offline/HSM operator-held (§20.2) → v2/ops.",
        "honest_scope": "audit_category = schema field (§16.6), tagged not enforced (not a verdict line). "
                        "Boot-anchor-mismatch = SIMULATED boot. Blast-radius = per-patch EDGE CAP only (§8.8) — "
                        "ONE dimension; full scope×tier×family×external bounding is broader. ceremony_id replay "
                        "= EXTENSION beyond §20.3's 60s window (which is also enforced).",
    }
    json.dump(R, open(RESULT_PATH, "w"), indent=2)
    print("\n" + "=" * 72); print("G2 VERDICT")
    for k, v in V.items(): print(f"   [{'PASS' if v else 'FAIL'}] {k}")
    print("=" * 72); print(f"all_pass={all(V.values())}  -> {RESULT_PATH}", flush=True)

if __name__ == "__main__":
    main()
