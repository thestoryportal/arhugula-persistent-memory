# PACKAGE — 🛡️ Warden / AISecOps (Security)
_Run under COUNCIL_PROTOCOL.md. Audit vs CORPUS 05 §Warden. Concern: who authorized this write, how do we know it wasn't tampered, what's the blast radius._

## Your spec contract (audit baseline)
Patch Authorization Gate + signed pass; tokens + Write Scope Definitions per agent; audit trail (§6, §14); Ceremony Authorization / CeremonyToken (§20); least privilege; immutability boundary; tamper detection; external-document provenance (§26).

## Relevant evidence (cite from 01)
- L-BRIDGE: the write artifact is a `.vlp` produced by OUR Python generator (`build_vindex_overlay.py`) from edited weights → `APPLY` → `COMPILE`. Base vindex frozen (L-ROLL).
- L-VERIFY: ROUTE VERIFY abstains on distractors (a safety property for reads).
- Engine + LARQL UNMODIFIED; edits Probe-B (apply+restore) in experiments.

## Standing questions to adversarially answer (almost all GAP — security was out of empirical scope)
1. **Write authorization (G2 — likely BLOCKER for the spec, maybe DEFER for local-experiments)**: nothing in our pipeline authorizes, scopes, or gates the `.vlp` write. No tokens, no Gate, no signed pass. Who is allowed to emit/apply a `.vlp`?
2. **Patch integrity / signing**: `.vlp` is plain JSON, unsigned. No tamper detection. The spec requires signed passes — UNTESTED/absent.
3. **Audit trail**: no audit record of who wrote what when. Spec requires it.
4. **Immutability boundary**: base is frozen (✅ partial) — but the overlay is freely writable; what's the immutability contract for compiled vindexes / the tier stack?
5. **Blast radius**: a malformed/malicious `.vlp` (e.g., our crude-edit corruption, or COMPOSE garbage) bakes into served weights via COMPILE — what detects/contains it pre-serve? (Ties to Validation domain.)

## Seeded gap: G2 (authz, signing, audit, immutability). Confirm these are entirely UNTESTED; rule whether they BLOCK gate-to-local or are DEFER-TO-LOCAL (likely: not needed to *experiment* locally, but BLOCKERS before *production* integration into the agent harness).
