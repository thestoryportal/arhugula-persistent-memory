# B0 — SELECT-primitive go/no-go: RESULT (honest verdict)

**Date:** 2026-06-22. **Pre-reg:** `docs/B0_SELECT_PRIMITIVE_PREREG.md` (frozen before run). **Artifact:** `results/b0_select_primitive_pilot.json`. **Harness:** `experiments/track_e/b0_select_primitive.py` (g6 primitives, LAW#5 INERT ✓ |Δ|=0.0015, engine `5c0c706a…`). Qwen2.5-3B band[4-8], 8 committed fictional facts, batch single joint solve. **PILOT — n=8, single seed, single relation, clean batch.**

## Raw result
| set | reads | maxprob (mean / min–max) |
|---|---|---|
| **committed** (8 fictional, edited) | 8/8 correct | 0.997 / 0.9935–0.9995 |
| **absent-fictional** (8 fictional, NOT edited) | 0/8 high-conf | 0.118 / 0.043–0.242 |
| **absent-real** (6 real, NOT edited — LEAK probe) | **6/6 correct** | 0.557 / 0.428–0.819 |
| separation best-τ | τ=0.9935 → committed 100% above / absent-fictional 100% below | |
| **Mechanical outcome** | **A_SELECT_PLAUSIBLE** | |

## Honest verdict — A_SELECT_PLAUSIBLE, but heavily CONFOUNDED (mechanical PASS ≠ promotable claim)
A weight-native confidence-gated read is **not obviously impossible** (this rules out a strong OUTCOME-B), but the separation is **NOT a demonstrated SELECT primitive** — it rests on two confounds that the pre-registered mechanical criteria don't control:

1. **Margin-inflation confound (load-bearing).** Committed facts read at 0.997 **by construction** — `compute_z` optimizes the edit target to ~0.99 probability (the known B3 margin-inflation artifact). So the clean τ=0.9935 separates "edited" from "everything else," which is *what editing does*, not an independent retrieval mechanism. The separation must survive **margin dilution at scale** (more edits → lower per-fact margin) and **quantization** (B3 showed edited-margin compression) before it counts as a real read primitive.

2. **The LEAK channel is LIVE (the real finding).** Absent-real facts the model knows but we did NOT commit (France→Paris …) read back **correct 6/6 at maxprob 0.43–0.82.** The store has **no commit-status bit** — it freely returns uncommitted pretrained knowledge. These only fall below τ because τ is pushed to 0.9935 *by the margin confound*. The headroom between the leak ceiling (0.82, Norway) and the committed floor (0.9935) is **thin (~0.17) and confound-dependent** — a more-confident pretrained fact, or a margin-diluted committed fact, collapses it. So "closed-world over committed memory" is a **fragile coincidence of the clean-small-N margin gap**, not a robust weight-native property.

   (Note: absent-*fictional* "abstention" is also partly an artifact — the top-1 tokens are entity-name fragments (" Pl", " V"), i.e. the model continues the unknown token rather than answering. That is not general abstention; for a *known* entity it answers, as the leak probe shows.)

## What B0 decides (and doesn't)
- **GO on Edge B** — do not abandon the read contract; a confidence-gated read is worth pursuing. NOT a clean OUTCOME-B (weight-native read is not impossible).
- **NOT a green light to build the big pool yet.** The decisive question is now sharper than "does SELECT exist": **does the committed-vs-uncommitted margin separation SURVIVE (a) scale/margin-dilution and (b) a hard set of high-confidence uncommitted-known facts?** That is the reframed B1.
- **B1 reframed:** the cleanest database-read falsifier is NOT fictional-entity abstention — it is the **LEAK channel**: does an uncommitted-but-known fact read above the committed threshold once margins are realistic? My absent-real data already shows it's close.

## Medium-of-Obligation implication (Codex D1 / anti-scope-laundering)
SELECT / closed-world is **NOT cleanly `WEIGHTS_MUST_CARRY`.** Best case it is **`HYBRID_ALLOWED`**: in-weight logit readout + a *governance* confidence-threshold — and even then the live leak channel means a true closed-world contract needs an **external commit-status/provenance bit** (the weights don't carry one). This **loops to B3N** (in-weight-vs-side-store) exactly as the advisor predicted. Recorded honestly: weight-native closed-world SELECT is **unshown**; what's shown is a confound-dependent confidence gap at clean small-N.

## Advisor sharpening (folded in — confirms verdict, leans it toward B)
1. **τ=0.9935 flatters.** It's the in-sample `min(committed)`; with committed ~0.997 and absent-fictional all <0.25, *any* τ∈[0.25,0.99] scores 100%/100% — the "headroom 0.17" is less precise than it looks. The absent-fictional arm is near-uninformative (tokenization artifact: top-1s are name fragments " Pl"/" V", i.e. continuing an unparseable proper noun, NOT abstaining on absence).
2. **The only un-confounded signal is the LEAK probe** (known-uncommitted read correct 6/6 at 0.43–0.82). And 0.82 is an **optimistic floor, not a ceiling** — France/Japan/Egypt/Spain are *mid*-confidence retrievals; the read surface faces facts the base model is far more certain about than 0.82 → the committed-vs-leak gap is **thinner than 0.17** before margin dilution.
3. **Honest lean = toward OUTCOME-B, not a neutral GO.** The separation that makes a gate *look* feasible IS the edit margin — the exact quantity B3 showed compresses under quantization and D1 showed dilutes under scale (i.e. it degrades in precisely the deployment condition). Prior into reframed-B1 = "can a hybrid confidence-gate be *rescued* from a likely-negative," not "confirm a promising SELECT."

## ⭐ Next-step reconciliation (Advisor + Codex, 2026-06-22) — CORRECTS the verdict framing above
Both reviewers agree: B0 is NOT enough to promote a *reliability* claim (n=8, 1 seed, 1 relation); and the spec-first **read/query matrix extraction** should start in parallel now (CPU-only, bounded to the read/query slice first). They diverged on whether to run a standalone B1; resolved by the spec-reading discriminator — **no spec clause requires *bare weights* to enforce closed-world reads** (grep-verified: read paradigm = "natively know" + L1-SELECT write-verify + §26 *external* provenance).

**CORRECTION to the verdict above (Advisor):** the leak channel is **the spec's DESIGN, not a threat.** The spec delegates commit-status/provenance to the **State Ledger + `.vindex` + §26**, NOT to bare weights. A model knowing un-committed France→Paris is *expected* (a model with knowledge + edits). So "weights carry no commit-status bit" **CONFIRMS the spec architecture** rather than threatening it.
→ **Disposition (promotable from one pilot — it's an obligation-medium/scoping call grounded in spec text, NOT a reliability claim):** read-time closed-world / commit-status = `GOVERNANCE_MAY_ENFORCE` (ledger-delegated); **the spec UNDER-SPECIFIES the read-time provenance surface → F1 read-contract finding + flagged spec gap.** Loops to B3N.

**Do NOT run a standalone B1.** Its spec-falsifying half (does *committed* knowledge reliably fire + survive **scale** and **quantization** — margin dilution) is the SAME question as the council-#1 falsifier **compaction-CORE-retention-at-scale** → fold it in there as emitted seam metrics, with **Codex's factorial rigor: separate scale-only / quant-only / combined** (the original B1 "quantized+scaled crossing" conflated two variables). The leak-ceiling **membership-predicate** test (can in-weight confidence be a *cheap* closed-world gate, avoiding the ledger?) is an **optimization** question, not a spec requirement (the spec provides the ledger) → parked optional, below the scale falsifier.

**Reconciled next steps:** (1) fold B0 as the governance-delegated disposition + spec gap above; (2) start the **read/query matrix extraction in parallel now** (CPU); (3) **next GPU cycle = compaction-CORE-at-scale** (council #1, already directional-negative) after the stimulus pool, with committed-reliability-under-scale + a quantization arm emitted as seam metrics. **HELD for operator greenlight — not auto-run.**
