# 11 — G2: SECURITY LAYER — write authz / Gate / audit (result)
_Run 2026-06-18 on the pod. REAL asymmetric crypto (Ed25519, `cryptography` 3.4.8). Artifacts: `/workspace/experiments/governance/g2_security_layer.py`; result `/workspace/results/g2_result.json`; ledger `/workspace/results/g2_state_ledger.jsonl`. Upgrades CP1's HMAC stub + G1's metadata-only integrity + G1's reset stub; adds audit/immutability/blast-radius._

## The G2 question (from 00 §Known Gaps / 03)
`.vlp` write authorization, signing, audit trail, immutability, blast-radius — UNTESTED. And this session
left three explicit stubs to retire: CP1's **HMAC** Orchestrator signing, G1's **metadata-only** `.vindex`
integrity, and G1's **flag-flip** reset. G2 does them with real asymmetric crypto.

## The thesis (what asymmetric buys OVER HMAC)
A component that can **VERIFY cannot FORGE.** "Valid passes / tampered fails" was already true under CP1's
HMAC — so G2's evidence must show the *structural* upgrade. It rests on three tests; the others are honest
identity/ops checks.

## Measurement → verdict (all 9 PASS; `g2_result.json`)
| Test | What it proves | Result |
|---|---|---|
| **T-NO-PRIVKEY** (headline, structural) | the Gate + CeremonyVerifier hold **no Ed25519 private key** (recursive scan) → verify-cannot-forge by construction; Orchestrator *does* hold it (control) | gate ✗priv, ceremony ✗priv, orchestrator ✓priv | ✅ |
| **T-OVERLAY-SIGFORGE** (headline, closes G1 caveat) | substitute overlay bytes **AND rewrite the recorded `content_hash` to match** (so G1's metadata check PASSES) → G2's signature-over-re-hashed-bytes still **REJECTS** | g1-check fooled=True, g2-sig rejects=True | ✅ |
| **T-CEREMONY-WRONGKEY** (headline, airtight) | an envelope **validly signed by the Orchestrator key**, `key_ref=ORCHESTRATOR`, refused as **`CEREMONY_AUTH_WRONG_KEY`** (structural exclusion *before* signature check), not `SIGNATURE_INVALID` | sig actually valid=True, rejected wrong_key=True | ✅ |
| **T-CEREMONY** (§20.3 set) | valid CAK `CIRCUIT_RESET` admits; bad-sig / stale (>60s) / wrong-type / replayed-id rejected with the spec's codes | all 5 hold | ✅ |
| **T-TOKEN-CHECKS** (HMAC-equivalent) | legit token admits; foreign-key + payload-tamper rejected — *identity/expiry/suspension*, NOT the asym upgrade | all hold | ✅ |
| **T-LEDGER-TAMPER** | a naive retroactive edit of a past entry → chain walk detects the break (§16.4) | detected at seq 2 | ✅ |
| **T-BLAST-CAP** | coder patch over the 500-edge cap → `PATCH_CAP_EXCEEDED`; at-cap admits (§8.8) | both hold | ✅ |
| **T-SUSPEND** | a suspended agent's otherwise-valid token rejected `TOKEN_AGENT_SUSPENDED` (§10.7) | both hold | ✅ |
| **T-BOOT-ANCHOR** (simulated) | ledger anchor ≠ git-committed anchor → boot suspended (§10.5) | suspended | ✅ |

## What G2 PROVES (precise)
- **Verify-cannot-forge is structural, not asserted:** the Gate retains only the Orchestrator *public*
  anchor + a shared suspension set + the append-only ledger — the private signing key is unreachable from it
  (T-NO-PRIVKEY). This is the property CP1's HMAC could not have (its verifier held the symmetric secret).
- **Content-level `.vindex` integrity closes G1's flagged caveat:** the Orchestrator signs the overlay's
  *content* hash; verification re-hashes the *actual bytes* and checks the signature — so the metadata-rewrite
  that would defeat G1's pointer check cannot defeat G2, and substituting bytes requires a private key the
  verifier lacks.
- **CAK ceremony authorization (IC-TC-RESET, §20.3) replaces G1's reset stub:** a structurally-distinct CAK
  root of trust; the **structural exclusion** refuses Orchestrator self-authorization even when the signature
  is valid; the full §20.3 failure set (wrong-key / sig-invalid / stale / wrong-type / replay) fires with the
  spec's codes.
- Plus: per-patch edge-cap rejection (a blast-radius dimension), agent suspension/token revocation, naive
  ledger-tamper detection, simulated boot-anchor-mismatch suspension.

## Honest scope / caveats (claims kept flush with tests)
- **Key custody is NOT addressed.** Orchestrator + CAK private halves are generated **in-process** to
  exercise the VERIFIER. The spec puts the CAK private half offline/HSM, operator-held (§20.2). Custody =
  operational / v2.
- **T-TOKEN-CHECKS is HMAC-equivalent** (identity/expiry/suspension), explicitly NOT the asymmetric upgrade —
  that is carried by T-NO-PRIVKEY + T-OVERLAY-SIGFORGE + T-CEREMONY-WRONGKEY.
- **Ledger = tamper DETECTION, not immutability.** T-LEDGER-TAMPER catches *naive* (un-recomputed) edits; an
  attacker who rewrites an entry AND recomputes every subsequent `entry_hash` from the constant root yields a
  re-verifying chain. True tamper-evidence needs the HEAD anchored (Genesis Seal / signed checkpoint) — NOT
  modeled here.
- **`audit_category`** (§16.6) is a tagged SCHEMA FIELD, not an enforced behavior (no verdict line).
- **Blast-radius** here = the per-patch EDGE CAP only (§8.8) — ONE dimension; full bounding
  (scope × tier × family × external-content) is broader.
- **Boot-anchor** test is a SIMULATED boot. **ceremony_id single-use** is an EXTENSION beyond §20.3's 60s
  window (both enforced).

## Net
G2 is **PROVEN for its scope**: real-Ed25519 asymmetric authorization where the verifier structurally cannot
forge (closing CP1's HMAC stub), content-level overlay integrity (closing G1's metadata caveat), and the CAK
CeremonyToken verifier with airtight structural exclusion (replacing G1's reset stub), plus blast-radius
edge-cap, agent suspension, and naive ledger-tamper detection. Carried forward: **key custody** (offline/HSM,
v2/ops), **anchored-head ledger immutability**, full **multi-dimension blast-radius**, real boot integration.
This closes the security gap G2 named; G3 (validation pipeline) follows.
