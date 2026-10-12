Verdict: FIX-FIRST

**Single most important fix:** a validity failure in a *candidate* recipe (B0, B or Bshuf) must mark that recipe INVALID and let the pass continue. Today it HALTs the whole pass (`c10v_layerpick_arms.py:527–531`, and again at `:543–544`). With the current code, a B0 control drop below 68, which H-V2 predicts, stops the run before B and Bshuf are evaluated. The step then has no reading.

Reviewer: Claude (independent implementation review, D-C10v-layerpick v2). Date: 2026-10-07. Spec: `docs/C10V_LAYERPICK_PREREG.md` (v2 FROZEN).

**Evidence base.**
- I ran `.venv/bin/python -B experiments/track_c/c10v_layerpick_selftest.py`: 34/34 OK in 1.50 s, synthetic only.
- I read every line of the driver, the reader and the harness (`c10e_bandknob.py`), plus the relevant selftest bodies (`:120–180, :320–357, :564–630, :760–807`).
- I checked engine `compute_z` for any use of `hp.layers` (none; the layer is a parameter) and checked `memit_main.py:21,305–323` (the context cache the driver pins).
- I read `c10p_twopass_arms.py:30–42` (the frame-probe precedent) and `c10l_covgeom_step0.py:39–40,88,132–137` (the ρ formulas).
- I inspected `results/c10q_stacked/passS.json`.
- No model, torch-on-MPS or GPU job was run, and I made no git state change.

---

## What checks out (lines checked)

- **LAW#3 order (check 2).** I traced `runtime_stage` (`arms.py:475–555`). The sequence is: preflight fingerprint (`:89–94`), then load the harness, then `compute_P`, then the selector recomputation (no write), then `prepare_arm` for A (z solves only), then `law5_checks` (i)–(v) (`:510`), then `law5.json`, then live recipe A (`:514`), then `validate_recipe(A)` with the envelope para [5,18], canon [5,10] and A1/A2 ≥ 68 (`read.py:184–185, :246–249`), with HALT on a miss (`:515–518`). Only after that come the `*_started.json` marker (`:521`) and B0/B/Bshuf (`:524–526`). The known baseline is gated before any candidate arm. The `passS.json` historical reference is preflight only; the binding LAW#3 check is the same-process A. Correct.
- **LAW#5 seams (check 3).**
  - (i): the real `H.run_law5` runs through the wrapper. The wrapper bypasses on `_LAW5_DEFAULT_CTX` (`arms.py:268–269`), and the code requires 0 override hits (`:343`).
  - (ii) and (iii): two original-path writes and one active full-band wrapper write, on identical restored weights with targets pinned through `Z_OVERRIDE` (`:346–355`).
  - (iv): one request at layer 8 against `my_edit` with `layers=[8]` and `[P[4]]` (`:357–364`). The reader also asserts `projector_indices == [4]` (`read.py:142–144`).
  - (v): the two largest groups, composed descending, against lone writes from restored weights, with targets solved at each assigned layer (`:366–385`).
  - The fault sensitivity is real. The synthetic harness makes deeper keys depend on shallower weights (`selftest.py:138–145`). Reversed order and a wrong projector index both fail (`selftest.py:329–339`).
- **Restore coverage (check 3, out-of-band layers).**
  - Every map is restricted to {4..8} by `R.groups` (`read.py:57`, `MAP_LAYERS`), so no arm can edit outside the snapshot set of `snap_layers`/`restore_layers` (`c10e_bandknob.py:150–159`; `hp.layers = [4..8]` from the base file).
  - `run_recipe` restores 4–8 before every arm (`c10e:473`), and `runtime_stage` restores before every recipe (`arms.py:525`) and in `finally` (`:555`).
  - Single-layer lone writes restore exactly the one layer they edit (`arms.py:360, :382`, `{l: base[l]}` with `ghp.layers=[l]`).
  - The standing engine check `apply_memit_to_model(copy=False)` edits `hp.layers` (4–8), and `run_law5` restores it (`c10e:427, :439`).
  - No leak path found.
- **Grouping and solve semantics.**
  - Groups run descending, 8 down to 4, with empty groups skipped (`read.py:58–59`).
  - `hp` is deep-copied with only `layers` changed (`arms.py:292`). Projectors are `P[l−4]` taken from the recipe's single `compute_P` (`:293–294`, via `cached_P` at `:437–439`).
  - The cache is a fresh float32 CPU zero tensor per group (`:295`). Override keys are built per group (`:296`).
  - Hits are required to equal the number of groups (`:302`), and the reader checks the same (`read.py:186–190`).
  - The ΔW is Σ over groups and layers of Frobenius norms (`read.py:330–332`; distinct groups have distinct layer keys, so `norms.update` cannot overwrite).
- **Proxy algebra.** `g_from_keys` (`arms.py:152–162`) computes `X = S(I+S)⁻¹` via `solve((I+S)ᵀ, Sᵀ)ᵀ`. That equals `my_edit`'s `ΔW K` by push-through (`Kᵀ P (KKᵀP + I)⁻¹ K = S(I+S)⁻¹` for symmetric P). The ρ readouts match `c10l_covgeom_step0.py:88,132–137`: z is repeated across paraphrases, and each denominator is that fact's own pristine residual.
- **Labels (check 4).**
  - Base labels are INVALID, LEAD, PARTIAL, TRADEOFF and NULL. They are exhaustive and mutually exclusive (`read.py:319–357`).
  - Boundaries: `18 < n` (18 → NULL, 19 → PARTIAL when gain ≥ 10), `n < 30` / `n ≥ 30`, gain ≥ 10, `ratio > 1.5` (1.5 itself → no LARGE-WRITE), L3 ≥ 29, L1 and frame ≤ A+1, `described_as` ≥ A−3, perplexity ≤ A+0.5.
  - Each boundary is on the prereg's side and is tested at the threshold and on both sides of it (`selftest.py` ThresholdTests).
  - A LEAD-sized count with A ≤ 18 implies gain ≥ 12, so the missing gain test on LEAD is harmless.
- **Persistence (check 5).**
  - `write_json` (`arms.py:35–44`) uses exclusive create and compares the reread bytes and parse against a parse of the *serialised payload*. The c10u false HALT (in-memory object with tuples compared against the reloaded JSON) cannot recur.
  - I checked every persisted structure for tuples: `LAYERS` is always wrapped in `list(...)` (`:282, :351`), group layers are `[l]`, and `subjects` is `list(H.FICTION)`. None leak.
  - Every numeric output is converted with `float()`/`.tolist()` (numpy scalars do not reach `json.dumps`). `allow_nan=False` is set.
  - Stage outputs are exclusive. `OCCUPIED_OUTPUTS` covers dangling symlinks (`:47–48`). pass2 reads only the same directory's pass1, checked by hash and identity (`:481–487`). A retry must use a fresh `--out-dir`, which has no step0 to inherit.
- **Compute and memory (check 7).**
  - One model copy only.
  - All float64 work is numpy on CPU: `g_from_keys`, HSIC, `activation_rows` (after `.cpu()`), `relative_distances`. `as_numpy` always calls `.cpu().float()` first. No float64 runs on MPS.
  - Largest transients:
    - The float64 copy of an 11008² projector in `g_from_keys` (`arms.py:155`), ≈ 0.97 GB per call.
    - ΔW float32 snapshots, ≈ 90 MB per layer × 5 per capture, explicitly `del`'d.
    - The HSIC pairwise tensor, 24 × 24 × 11008 float64 ≈ 50 MB.
  - Nothing comes close to 48 GB.

---

## Numbered items

### 1. BLOCKING: candidate-recipe validity failures HALT the pass; the prereg says INVALID for that recipe

- **Where.** `c10v_layerpick_arms.py:526–531`:
  ```python
  recipes[name], _ = run_one_recipe(...)
  try:
      R.validate_recipe(recipes[name], name, step, published)
      ...
  except Exception as exc:
      halt(root, "RECIPE_VALIDITY " + name + ": " + str(exc), recipes=recipes, law5=proof)
  ```
  `:543–544` also refuses to write `pass1.json` unless `pass_validity` is clean for **every** recipe.
- **What the prereg says.** §3, line 66: "Validity (any failure → INVALID **for that recipe**) … A1 ≥ 68 and A2 ≥ 68 **under that recipe** (a control failure is INVALID, never TRADEOFF) … `para_full_string` = `para_full`". H-V2 (line 17) explicitly predicts that the whole-residual single-layer write "costs the controls", with B0 as its control. A control failure under B0 is therefore an anticipated scientific outcome, not a harness defect.
- **Concrete failing input.** The selftest encodes the defect as intended behaviour. `selftest.py:784, 804–806` sets B0's A1 `para_full_n = 67`, asserts a HALT, and asserts that `run_one_recipe` was called only for `["A", "B0"]`. B (the candidate) and Bshuf never run, and `pass1.json` is never written. The step produces no reading, only a HALT diagnostic.
- **Same path for FULL_STRING.** A string-match/id-match divergence in any candidate (`read.py:181–183`) follows the same route. Alternate tokenisations of coined A7 values are plausible under strong single-layer writes.
- **Corollary.** The reader's `candidate_reading → INVALID` branch (`read.py:320–322`) is unreachable from any record the driver can produce. INVALID is tested only on fixtures (`selftest.py:618`).
- **Fix.**
  - (a) Split `validate_recipe` into two functions:
    - `recipe_integrity(...)`: map, `law5_gate`, summary counts versus rows, override groups and hits, write norms, locality/relation/frame/TF/proxy shapes and provenance, covariance. Integrity failure stays a HALT.
    - `recipe_validity(...)`: `CONTROL_A1_single`, `CONTROL_A2_coherent2`, `FULL_STRING`. It returns a list of reasons.
  - (b) For recipe A, keep both as a HALT (LAW#3).
  - (c) For B0/B/Bshuf, run integrity (HALT on failure). Store `rec["validity"] = {"ok": not reasons, "reasons": reasons}` and **continue** to the next recipe.
  - (d) At `:543–544`, require only integrity for every recipe and write `pass1.json` even when a candidate is scientifically INVALID.
  - (e) Leave the reader's `pass_validity`/`candidate_reading` semantics unchanged: they already return INVALID per recipe. Attribution already refuses credit when B0 or Bshuf is invalid (`read.py:341–343`), which is a conservative and acceptable reading.
  - (f) Invert the selftest at `selftest.py:770–806`. B0 A1 = 67 must give: recipes called `["A","B0","B","Bshuf"]`, `pass1.json` and `pass1_complete.json` written, reader B0 = INVALID, and B read normally. Add the same test for a FULL_STRING mismatch under B.

### 2. ADVISORY (high): `PASS1_FIXED_MAP` is a gate the prereg does not have, and it is the likeliest spurious HALT after item 1

- **Where.** `arms.py:506–507`: `R.require(step["map"] == published, "PASS1_FIXED_MAP")`. pass1 recomputes the selector in a **new process** and halts if the map differs from the step0-stage map.
- **What the prereg says.** The map is "written to `step0.json`, hashed into the run record, and fixed" (line 35). The only reproducibility gate is "map reproduced **in-process**" (line 66, step 0's two computations, which the step0 stage already enforces). pass2 tolerates a cross-process disagreement and reports agreement /24 (`:537`); pass1 halts on the same condition. The two paths are inconsistent, and Codex's report does not list this as an ambiguity decision.
- **Why it bites.**
  - The contexts are pinned for pass1 (`arms.py:138–143`), so only cross-process numeric differences remain.
  - δ is measured from two *same-process* repeats over identical cached contexts and inputs, and is very likely exactly 0.0 (see item 3). The margin then absorbs nothing.
  - The prereg's own expectation is "hair-width variation" between layers (line 36). A 1-ULP cross-process difference on any near-tie flips a fact's layer and HALTs pass1 after step0 printed READY.
- **Fix.** Replace the `require` with the pass2 behaviour: run the published map and record `selection_agreement_n` (already computed at `:537`). Alternatively, if the stricter gate is wanted, record it as a prereg amendment before running.

### 3. ADVISORY (prereg-level, for the operator): the measured δ will likely be 0, which makes the margin rule vacuous

- **Where.** `read.py:74`: `delta = max |first − second|` over the two in-process tables. `compute_selector` (`arms.py:169–177`) runs the same `compute_ks` forward passes on the same cached contexts twice in one process. On MPS that is normally bit-identical, so δ = 0.0 and every `margin ≥ 0` qualifies (`read.py:81`).
- **Consequence.** The prereg's stated intent, that hair-width variation is "absorbed by δ" (line 36), will not hold. Hair-width argmax differences become the published map, and B versus Bshuf then compares near-arbitrary assignments.
- **Fix.** This is not an implementation fix, since the code is faithful to line 33. Record it in the run record as `delta_is_zero: true`. Raise with the operator before step 0 whether δ should come from a cross-process or perturbed-context repeat (an amendment).

### 4. ADVISORY (reading changes the map when δ > 0): "takes the layer nearest 8" is implemented as "takes layer 8"

- **Where.** `read.py:81`: `selected[s] = LAYERS[order[0]] if margin >= delta else 8`. This is Codex decision 1.
- **Why it matters.** Prereg line 33 says "a fact whose margin is below δ takes **the layer nearest 8**". The natural reading is the contender (among layers within δ of the max) nearest to 8. If 8 were meant, the text would say "takes layer 8".
- **Concrete case.** Winner 4, runner-up 5, margin < δ. The code assigns 8, which is neither contender; the literal reading assigns 5. Codex's reading pushes every ambiguous fact to 8. That inflates concentration toward the ≥ 20/24 stop rule and makes B more like B0.
- **Fix.** `near = [LAYERS[j] for j in range(5) if row[j] >= row[order[0]] - delta]` (with a strict `<` margin semantics kept consistent); `selected[s] = max(near)`. Add boundary tests. Alternatively, get an operator ruling and record it. This is moot if δ = 0 (item 3).

### 5. ADVISORY: the LAW#3 "historical reference" is not a baseline record

- **Where.** Codex decision 9 and the stage commands pin `results/c10q_stacked/passS.json`. That record's `pass` is `"S"`, its `pass_label` is `"stacked: second edit aimed at z_post"`, and its only recipe is `A7_stacked`. It is the c10q stacked-edit pass, not a baseline-recipe run.
- **Effect.** Not result-changing, because the binding LAW#3 check is the same-process recipe A envelope (item "LAW#3 order" above). But the identity record calls it a LAW#3 reference.
- **Fix.** Point `--law3-ref` at a genuine baseline-recipe record, or rename the field `preflight_controls_reference` and say in the report that it is not the LAW#3 gate.

### 6. ADVISORY: `capture_write` never audits override hits on the original path

- **Where.** `arms.py:311–328`. `H.Z_OVERRIDE_HITS` is reset to 0 (`:314`) but checked only inside the wrapper (`:302`). The floor (ii), lone (iv) and lone (v) writes call the original `my_edit`, which silently falls back to `compute_z` when any key is missing (`c10e_bandknob.py:186–191`).
- **Effect.** The prereg's "targets pinned through `Z_OVERRIDE` so both runs aim at the same z" (line 58) is asserted for the wrapper side only.
- **Fix.** After `call(...)` with `wrapper=False`, `R.require(H.Z_OVERRIDE_HITS == 1, "LAW5_OVERRIDE_PIN")`.

### 7. ADVISORY: (iv) and (v) do not check that unassigned layers stay untouched

- **Where.** `arms.py:362` compares only `wrapped[8]`, and `:383` only each group's own layer. A wrapper defect that also wrote another band layer would pass both checks.
- **Fix.** Add `R.require(all(not np.any(wrapped[l]) for l in R.LAYERS if l != 8), "LAW5_IV_SCOPE")`, and the analogue for `composed` over layers not in `small_map.values()`.

### 8. ADVISORY (minor): Bshuf PARTIAL/LEAD prints a bare label

- **Where.** `read.py:367` skips the replication bookkeeping for Bshuf. A Bshuf "LEAD" therefore prints without a suffix (gate_A is False).
- **Why it matters.** It is easy to misread in a CORPUS fold.
- **Fix.** Append `-CONTROL-ONLY` (or similar) for Bshuf labels.

### 9. ADVISORY (note): locality gates are read on the A7 arm only

- **Where.** `read.py:323–329`.
- **Note.** The prereg (line 74) does not name the arm, and A7 is the binding arm, so this is a reasonable reading. State it in the reader's scope string so the CORPUS entry does not imply that A1 and A2 locality were gated.

---

## Implementation decisions for textual ambiguities (check 6)

| # | Decision | Faithful? | Changes a result? |
|---|---|---|---|
| 1 | Margin below δ goes to 8 | Questionable (item 4) | Yes if δ > 0 |
| 2 | Recipe A uses pre-solved layer-8 z via `Z_OVERRIDE` | Yes: same pristine `compute_z` per request as `my_edit:191`, solved before any write | No (in-process deterministic) |
| 3 | Largest-group tie goes to the higher layer; exact behavioural equality in (iii) | Yes (line 58 "behavioural outputs equal") | Could HALT if MPS is nondeterministic in-process; the floor record would show it |
| 4 | Ratio > 1.5 on a sized count gives TRADEOFF-LARGE-WRITE | Defensible (line 71 lists write-size misses under TRADEOFF); same consequence as line 101 (no gate A) | No |
| 5 | Frame flip means post top-1 is in the edited first tokens | Yes, matches `c10p_twopass_arms.py:36–42` | No |
| 6 | pass2 for any PARTIAL/LEAD on B or B0, including unattributed B | Yes (line 60 literal) | No |
| 7 | Degenerate HSIC/ρ gives null plus a diagnostic | Yes | No |
| 8 | String equality on aggregate counts | Yes (line 66) | No, but see item 1: a mismatch currently HALTs |
| 9 | `passS.json` as the LAW#3 reference | Mislabelled (item 5) | No |
| 10 | Stage safety, markers after LAW#5 + A | Yes | No |
| (unlisted) | Candidate validity goes to HALT | **No** (item 1) | **Yes** |
| (unlisted) | pass1 cross-process map must equal the published map | **No prereg basis** (item 2) | Yes (spurious HALT) |

## Prereg-to-test mapping (check 1)

Every numbered criterion, gate and label in §§2–3 has a selftest that calls the real function: the selector, δ, margin and concentration rules; G against an independent solve; HSIC; the wrapper grouping, projector index, fresh cache and hits; LAW#5 (i)–(v) and fault sensitivity; every locality and write threshold at, inside and outside its boundary; attribution 9/10/11; the replication rules; and persistence round-trips. **Gaps:**
- No test shows a candidate-recipe INVALID flowing through to a written pass and a per-recipe INVALID reading. The existing test asserts the opposite (item 1).
- No test covers pass1 accepting a cross-process map disagreement (item 2).
- No test checks that unassigned layers stay untouched in (iv)/(v) (item 7).

---

**BLOCKING count: 1** (item 1). Fix item 1, fix or amend item 2, and get an operator ruling on items 3 and 4 before step 0. Then re-run the selftest and send this back for a delta review.
