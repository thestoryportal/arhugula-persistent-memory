# Route A — Amendment 1 (v2, revised after advisor review): per-layer null-space threshold (deviation D8) — pre-registered before any edit

**Parent prereg:** `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` (D-C10k-route-a, committed `ceeaff8`). **v1:** committed with the advisor's FIX-FIRST review at `logs/claude_c10k_route_a_amendment1_review.md`. **v2 date:** 2026-10-04; revised the same day after the advisor's FIX-FIRST review of v2 (`logs/claude_c10k_route_a_amendment1_v2_review.md`, items resolved in §9). **No edit has run.** v2 supersedes v1 in full; v1's text is in git history.

## 0. What v2 changes against v1 (advisor FIX-FIRST items, each resolved or scoped)

| advisor item | resolution in v2 |
|---|---|
| 1. L8 pass marginal; selected on the A1 keys it will grade; report per-key spread | §2: bootstrap 95% CI on the 24 A1 keys; 24 **held-out** fictional subjects never used by any arm; per-key min and the fraction of keys under 0.2. Both statistics (per-key mean and aggregate) reported. |
| 2. "Minimal departure from the shipped value" may not hold on a normalised covariance | §3: comparability is established at the source: upstream builds `P` from `stat.mom2.moment()` (`AlphaEdit_ARE/AlphaEdit_ARE_main.py:178`), the same normalised statistic D4 injects (`experiments/track_c/c10k_route_a_launcher.py:124-128`). The *statistic* matches; its *units* do not carry across models, so the rationale is restated as a tie-breaking rule (§3). |
| 3. Rule written after the sweep; grid not fixed | §3 heading now reads **rule chosen post-sweep, pre-edit**. The grid is fixed in v2 before the run that this document reports: `{'4': [0.005, 0.01, 0.02], '8': [0.02, 0.025, 0.03, 0.035]}` on top of the sweep's 0.005/0.01/0.02/0.03/0.05/0.1. |
| 4. Survival measured on the wrong keys (AnyEdit writes several positions per window) | §2: a third survival statistic on the keys AnyEdit actually writes at window_size=1: for each A7 item the last prompt token and every answer-token position but the last (132 keys). |
| 5. Launcher wiring parity | §4: parity is by construction and verified: the gate stacks `P` in `hp.layers` order (`c10k_route_a_gate_v2.py:58,68,78`) and the ported module indexes `P[i]` by the same enumeration (`AnyEdit_mps/AlphaEdit_ARE/AlphaEdit_ARE_main.py:129`). The launcher loads that file verbatim (`--P`), records its basename and hash in every result, and **aborts before any edit** unless the file's full SHA-256 equals `P_sha256` in `projector_gate_v2.json` (`load_P`, `c10k_route_a_launcher.py`); prefix `c27203012b6a`. |
| 6. I-INFER stays labelled; R1-S bounded; §0.3 relevance | §5 unchanged; R1-S withdrawn in favour of the §8 interference control. Route A is D-C10k's successor on the §0.3 C10 falsifier (CORPUS/41 halted Stage 0; Route A is the operator-chosen path). |

**One further correction the v2 gate itself forced (L4).** v1 computed survival and protection as a ratio of mean norms. The parent prereg's D4 wording is the **mean of per-key ratios**. On that statistic L4 at the shipped 0.02 breaches protection (0.544 > 0.5; aggregate 0.495). The same minimal-departure rule therefore moves L4 to the next *smaller* grid value that restores protection: **0.01**. Both statistics are reported everywhere so the two readings can be compared; the prereg's per-key mean is the binding one. **Provenance of the switch:** the parent gate (`stage_projectors`, `c10k_route_a_launcher.py:189`) and v1's sweep (`c10k_route_a_threshold_sweep.py:28`) both computed the *aggregate* ratio of mean norms, which deviates from the parent prereg's D4 wording; v2 restores the pre-registered statistic. The two coincide at L8 (0.177 at 0.02 on both) and differ at L4 (0.495 aggregate vs 0.544 per-key). The L4 move was made with that table visible; the prereg wording forces it, and that is the only reason it is made.

## 1. The rule (deviation D8) — chosen post-sweep, pre-edit

Each band layer keeps upstream's `0.02` unless a bound fails there on the per-key statistic. A failing layer moves to the **next sweep-grid value in the direction that restores the failing bound** (sweep grid 0.005/0.01/0.02/0.03/0.05/0.1, fixed in `c10k_route_a_threshold_sweep.py` before v1) that passes **all** of: protection ≤ 0.5; A1 survival ≥ 0.2 with bootstrap-CI lower end ≥ 0.2; held-out survival ≥ 0.2; ARE-window survival ≥ 0.2. If no sweep value passes, the prereg stays halted. The finer grid `{'4': [0.005, 0.01, 0.02], '8': [0.02, 0.025, 0.03, 0.035]}` was fixed before this run and is reported for sensitivity only; it does not re-select. The bounds are not moved. No A1/A2/A7 edit outcome has been computed.

Result: **L4 = 0.01, L5 = L6 = L7 = 0.02 (shipped), L8 = 0.03.**

## 2. Gate v2 record (EVIDENCE-SHOWS) — `results/c10k_route_a/projector_gate_v2.json`

Keys per layer: 28545 Wikipedia down_proj inputs (200 held-out articles), 24 A1 last-prompt-token keys, 24 held-out fictional-subject keys (`HELDOUT_FICTION` in `c10k_route_a_gate_v2.py`, disjoint from every arm's subjects, asserted at run time), 132 ARE window-position keys. Bootstrap: 2000 resamples, seed 0. Statistic: mean of per-key ratios (prereg D4 wording); aggregate ratio-of-mean-norms also reported.

### Chosen thresholds

| layer | threshold | dims/11008 | protection per-key (≤0.5) | protection aggregate | A1 survival per-key (≥0.2) | A1 95% CI | A1 min | held-out survival (≥0.2) | held-out CI | ARE-window survival (≥0.2) | ARE min | ARE frac<0.2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L4 | 0.01 | 9470 | 0.419 | 0.366 | 0.436 | [0.433, 0.438] | 0.423 | 0.433 | [0.431, 0.435] | 0.376 | 0.196 | 0.015 |
| L5 | 0.02 | 9155 | 0.432 | 0.433 | 0.473 | [0.472, 0.474] | 0.464 | 0.471 | [0.469, 0.473] | 0.458 | 0.163 | 0.03 |
| L6 | 0.02 | 8452 | 0.431 | 0.431 | 0.359 | [0.356, 0.361] | 0.349 | 0.354 | [0.351, 0.358] | 0.434 | 0.184 | 0.03 |
| L7 | 0.02 | 7862 | 0.421 | 0.414 | 0.343 | [0.338, 0.348] | 0.324 | 0.336 | [0.331, 0.343] | 0.497 | 0.165 | 0.015 |
| L8 | 0.03 | 8368 | 0.451 | 0.465 | 0.242 | [0.236, 0.248] | 0.211 | 0.247 | [0.239, 0.255] | 0.563 | 0.211 | 0.0 |

All five layers pass every bound on the per-key statistic; `gate_ok = true`. The bootstrap CIs resample keys only: they measure between-key spread, not robustness to covariance-estimation noise or to the choice of the 200 articles. Projector file: `logs/c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt` (SHA-256 prefix `c27203012b6a`).

### L4 grid

| threshold | dims | protection per-key | protection aggregate | A1 survival | A1 CI | held-out | ARE-window | ARE frac<0.2 | both bounds |
|---|---|---|---|---|---|---|---|---|---|
| 0.005 | 8645 | 0.301 | 0.254 | 0.322 | [0.320, 0.323] | 0.320 | 0.244 | 0.303 | ✓ |
| 0.01 **(chosen)** | 9470 | 0.419 | 0.366 | 0.436 | [0.433, 0.438] | 0.433 | 0.376 | 0.015 | ✓ |
| 0.02 | 10245 | 0.544 | 0.495 | 0.533 | [0.530, 0.535] | 0.531 | 0.517 | 0.0 | ✗ |

### L8 grid

| threshold | dims | protection per-key | protection aggregate | A1 survival | A1 CI | held-out | ARE-window | ARE frac<0.2 | both bounds |
|---|---|---|---|---|---|---|---|---|---|
| 0.02 | 6567 | 0.354 | 0.361 | 0.177 | [0.173, 0.181] | 0.180 | 0.434 | 0.22 | ✗ |
| 0.025 | 7637 | 0.408 | 0.419 | 0.214 | [0.209, 0.219] | 0.218 | 0.509 | 0.045 | ✓ |
| 0.03 **(chosen)** | 8368 | 0.451 | 0.465 | 0.242 | [0.236, 0.248] | 0.247 | 0.563 | 0.0 | ✓ |
| 0.035 | 8878 | 0.485 | 0.501 | 0.262 | [0.256, 0.269] | 0.269 | 0.602 | 0.0 | ✓ |

**L8 reading.** The v1 rule names the grid it walks: the sweep grid (0.005/0.01/0.02/0.03/0.05/0.1), on which the next value above the failing 0.02 is **0.03**, and 0.03 clears every bound: CI lower end 0.236, held-out 0.247, no key under 0.2. The finer values 0.025 and 0.035 were added in v2 to answer the advisor's question, not to re-select: 0.025 also passes the four conditions (CI lower end 0.209, held-out 0.218) but with 0.125 of A1 keys under 0.2 and every margin inside 0.02 of the bound. L8 stays at **0.03**; 0.025 is recorded as the nearest alternative and not run (R1-S withdrawn, §6). The held-out check is the decisive one: survival on 24 subjects outside every arm (0.247) matches the A1 keys (0.242) to 0.005, so the L8 pass is not specific to the 24 A1 subjects *within the same prompt family* (the held-out subjects use the A1 template). Because held-out survival is itself one of the v2 selection conditions it is a leakage check, not an independent holdout.

**ARE-window reading.** At every layer survival on the positions AnyEdit writes is at least as high as on the last prompt token (L8: 0.563 vs 0.242); the means clear the bound by 0.17 or more. A few individual window positions fall under 0.2 at L4–L7 (minimum 0.163 at L5; 2–4 of 132 keys per layer, 1.5–3%), none at L8. The bound is on the mean (prereg D4); the per-key tail is recorded here so the A7 per-item results can be read against it. The parent gate's last-token proxy was conservative, not flattering.

## 3. Comparability with upstream (resolves advisor item 2)

Upstream `get_project` (`experiments/evaluate_uns.py:262-278`) takes `cov = get_cov(...)`, which returns `stat.mom2.moment()` (`AlphaEdit_ARE/AlphaEdit_ARE_main.py:178`), i.e. `mom2 / count`, then `U, S, _ = svd(cov)` and keeps `S < nullspace_threshold`. D4's `normalised_cov` returns `mom2.mom2 / mom2.count` from the program's cache (`c10k_route_a_launcher.py:124-128`), and `get_project_verbatim` repeats the SVD and the `S < threshold` selection (`:130-134`). The threshold is applied to the same statistic on both sides, but that statistic is an absolute eigenvalue in units of activation variance, and those units are not comparable between a 3B base model and a 7B/8B Instruct model. 0.02 is therefore upstream's number, not upstream's operating point. "Minimal departure from the shipped value" is a deterministic tie-breaking rule, not a comparability claim; the scale-free descriptors of each chosen cutoff (kept-rank fraction, eigen-energy fraction removed) are reported in §8 so the operating points can be compared on their own terms.

## 4. Launcher wiring (resolves advisor item 5)

`c10k_route_a_gate_v2.py` builds one `P` per layer in `hp.layers` order from the same hparams file the run stage uses and saves `torch.stack(Ps, 0)`. The ported module consumes `P[i,:,:]` with `i` the enumeration index over `hparams.layers` (`AlphaEdit_ARE_main.py:129`). The run stage loads the file passed by `--P` unchanged (`c10k_route_a_launcher.py:237,252`) and writes its basename into every result's `scope` string. Parity condition, enforced by the launcher before any edit (`load_P` raises on mismatch): the basename equals `c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt` and the file's full SHA-256 equals `P_sha256` in the gate record (prefix `c27203012b6a`). The old single-threshold `projectors` stage and `results/c10k_route_a/projectors.json` are superseded and not used.

## 5. I-INFER (unchanged, kept out of CORPUS)

The A1 edit keys are last-prompt-token inputs on fictional subjects; with depth their energy concentrates in directions Wikipedia text also uses, so a projector strict enough to protect L8's general knowledge removes most of the edit. L4 shows the opposite edge: the null space is so large at 0.02 that the projector protects too little. Nothing in D8 depends on this explanation.

## 6. What this changes in the prereg's verdict table

Nothing in §4 of the parent prereg changes. Every result under D8 carries "per-layer thresholds (Amendment 1 D8) `c10k_route_a_P_perlayer_0.01-0.02-0.02-0.02-0.03.pt`" in its scope string. A PASS-LEAD remains a mechanism lead; a FAIL remains scoped to this port *and these thresholds*. Scope caveat carried on every result: the per-layer gate does not predict where the joint solve puts the update; the residual is spread across L4–L8 and a weaker L8 survival can push update mass into the other layers. Sensitivity cell R1-S is **withdrawn**: moving L8 from 0.03 to 0.025 slides the layer along the same selectivity line (A1 survival / wiki leakage 0.54 vs 0.52) and would inform nothing; the projected-interference control in §8 replaces it.

## 7. Advisor

v2 review (FIX-FIRST): `logs/claude_c10k_route_a_amendment1_v2_review.md`. Resolutions in §9. The chain runs only after §8's controls are recorded and committed.

## 8. Controls (pre-registered readings; run after this text is committed, results appended below)

Script: `experiments/track_c/c10k_route_a_gate_v2_controls.py` → `results/c10k_route_a/projector_gate_v2_controls.json`. CPU/MPS maths on the keys the gate already extracts; no edit.

**(a) Scale-free cutoff descriptors** per layer at the chosen threshold: kept-rank fraction `dims/11008` and eigen-energy fraction removed `Σ S[S<th] / Σ S`. Descriptive only.

**(b) Projected-interference ratio.** The gate's norm ratios cannot distinguish a projector that removes shared directions from one that attenuates everything: across the grids the selectivity (edit survival / wiki leakage) barely moves (L8: 0.50–0.54; L4: 0.98–1.07), so the threshold slides a layer along a fixed line. The quantity that bears on collateral damage is the interference a unit minimum-norm update on an edit key `k_e` produces on a Wikipedia key `k`: `|k_eᵀ P k| / ‖P k_e‖²`, averaged over edit keys (A1 last-token; ARE window positions) and the 28,545 Wikipedia keys, divided by the same quantity at `P = I`. **Reading, fixed before running:** ratio ≤ 0.5 at every layer → the projection buys protection per unit of edit ("protective"); 0.5 < ratio < 1 → "partial"; ratio ≥ 1 at any layer → "non-protective" at that layer. A non-protective reading does not stop the chain (the port is still the port) but is written into every result's scope and means an A2 PASS cannot be attributed to the null-space projection.

**(c) Key parity (LAW#4).** The ported module takes its keys from a right-padded batch forward of `question + answer` at the window indices computed in `compute_z.py:67-91` (`AlphaEdit_ARE_main.py:88-107`); at `window_size = 1`, `overlap = 0` those indices are the last prompt token and each answer position but the last, which is what the gate's `are_window_keys` reads from single unpadded forwards. The control re-derives the indices from the module's loop, asserts they agree, asserts `padding_side == "right"`, and takes the cosine between batch-padded and single-sequence keys on 3 A7 items at every window position at every layer. **Reading:** positions agree and cosine ≥ 0.99 everywhere → proceed; otherwise HALT (the gate measured a different key distribution from the one the solve uses).

### Results

_(appended after the run)_

## 9. Advisor v2 items → resolution

| item | resolution |
|---|---|
| 1 pre-registration not committed; full hash | this revision, the gate JSON (now carrying `P_sha256`), the launcher and the controls script are committed before the controls run; the chain runs only after the results are committed. `logs/*.pt` is gitignored (2.4 GB); the full hash is in the committed JSON and the file is in the 6-hourly backup set. |
| 2 hash printed, not enforced | `load_P` asserts basename + full SHA-256 against the gate record and `gate_ok`; §4. |
| 3 gate keys vs solve keys | §8(c), HALT rule. |
| 4 "property of the layer" over-claim | §2 narrowed; held-out is a leakage check within the prompt family, not an independent holdout. |
| 5 comparability overstated | §3 rewritten; scale-free descriptors §8(a). |
| 6 statistic-switch provenance | §0: parent gate and v1 sweep used the aggregate; v2 restores the prereg wording; L4 chosen with the table visible because the wording forces it. |
| 7 R1-S uninformative | withdrawn; replaced by §8(b). |
| 8 CIs narrower than real uncertainty | labelled as between-key spread, §2. |
| 9 per-layer gate blind to the joint solve | caveat on every result's scope, §6. |
