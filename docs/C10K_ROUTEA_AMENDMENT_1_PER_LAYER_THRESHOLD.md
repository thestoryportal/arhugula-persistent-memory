# Route A — Amendment 1: per-layer null-space threshold (deviation D8) — pre-registered before any edit

**Parent prereg:** `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` (D-C10k-route-a, committed `ceeaff8`). **Date:** 2026-10-04. **Trigger:** the pre-registered projector gate halted the chain (`results/c10k_route_a/projectors.json`, commit `ec714f1`). **No edit has run.**

## 1. What the gate found (EVIDENCE-SHOWS)

With upstream's single `nullspace_threshold = 0.02` applied to the normalised 3B covariance (prereg D4), on the same calibration keys for every layer (200 held-out Wikipedia articles → 2,000+ down_proj inputs; the 24 A1 last-prompt-token edit keys):

| layer | dims/11008 | protection ‖P·k_wiki‖/‖k_wiki‖ (≤ 0.5) | survival ‖P·k_edit‖/‖k_edit‖ (≥ 0.2) |
|---|---|---|---|
| L4 | 10245 | 0.495 | 0.533 |
| L5 | 9155 | 0.433 | 0.473 |
| L6 | 8452 | 0.431 | 0.359 |
| L7 | 7862 | 0.414 | 0.342 |
| **L8** | 6567 | 0.361 | **0.177 ✗** |

The threshold sweep (`results/c10k_route_a/projector_threshold_sweep.json`, one SVD per layer, thresholds 0.005–0.1, same keys) shows both ratios rise monotonically with the threshold at every layer, and the survival curve falls with depth:

| threshold | L4 p/s | L5 p/s | L6 p/s | L7 p/s | L8 p/s |
|---|---|---|---|---|---|
| 0.005 | 0.254/0.322 ✓ | 0.200/0.250 ✓ | 0.198/0.190 ✗s | 0.165/0.159 ✗s | 0.103/0.055 ✗s |
| 0.01 | 0.366/0.436 ✓ | 0.285/0.355 ✓ | 0.286/0.268 ✓ | 0.268/0.241 ✓ | 0.199/0.101 ✗s |
| **0.02** (shipped) | 0.495/0.533 ✓ | 0.433/0.473 ✓ | 0.431/0.359 ✓ | 0.414/0.342 ✓ | 0.361/**0.177** ✗s |
| 0.03 | 0.565 ✗p | 0.535 ✗p | 0.538 ✗p | 0.511 ✗p | **0.465/0.241 ✓** |
| 0.05 | ✗p | ✗p | ✗p | ✗p | 0.577 ✗p |

**No global threshold passes both bounds on all five layers** (`thresholds_passing_all_layers: []`). The only value that passes L8 (0.03) breaches protection on L4–L7.

## 2. I-INFER

The A1 edit keys are last-prompt-token inputs on *fictional* subjects; with depth their energy concentrates in the directions Wikipedia text also uses (the "protected" subspace), so a projector strict enough to protect L8's general knowledge also removes most of the edit. This is the known AlphaEdit tension (preservation vs. plasticity) showing up layer-wise on a small base model with keys that upstream's Instruct-7B tuning never saw. It is not evidence about AnyEdit's windows or targets; it is about where the null space sits on this model.

## 3. The amendment (deviation D8) — rule fixed before any outcome is seen

**Per-layer threshold by minimal departure from the shipped value:** each band layer keeps upstream's `0.02` unless the gate fails there, in which case that layer takes the **next larger sweep value that passes both bounds**; if none does, the prereg stays halted. Applied to the sweep: **L4–L7 = 0.02 (shipped), L8 = 0.03.** The bounds (protection ≤ 0.5, survival ≥ 0.2) are **not** moved. The selection uses calibration keys only; no A1/A2/A7 outcome has been computed.

Why this rule and not "maximise protection" (smallest threshold meeting survival: 0.005/0.005/0.01/0.01/0.03): the latter departs from the shipped method on every layer and makes the port a re-tuning; the minimal-departure rule changes one number on one layer and keeps the result comparable to upstream's own setting. The maximise-protection variant is pre-registered as a **sensitivity cell** (R1-S) to be run on A1/A2 only if time allows, diagnostic only.

Implementation: `nullspace_threshold` becomes a per-layer list in the launcher's projector stage (`--thresholds 0.02,0.02,0.02,0.02,0.03`); the hparams file is unchanged (upstream's class holds a scalar; the module never reads it — `P` is built by the launcher, exactly as the official runner's `get_project` builds it from the scalar). The method-port packet records the per-layer values and the gate ratios.

## 4. What this changes in the prereg's verdict table

Nothing in §4 of the parent prereg changes. Every result under D8 is labelled "per-layer threshold (D8)" in its scope string. A PASS-LEAD remains a mechanism lead; a FAIL remains scoped to this port *and these thresholds*. The follow-up sensitivity pass in the parent FAIL clause gains the per-layer threshold as one more axis.

## 5. Advisor

`tools/claude_advisor.sh` on this amendment before the projector stage is re-run: `logs/claude_c10k_route_a_amendment1_review.md`.
