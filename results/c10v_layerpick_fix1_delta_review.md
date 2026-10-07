Verdict: FIX-FIRST

Item 1 (c)–(f): candidate B0/B/Bshuf validity failure → INVALID for that recipe, pass continues, pass record written — FIXED — arms.py:528–537, :549–550; read.py:172 (`recipe_integrity`), :248–257 (`recipe_validity`), :291–313 (`pass_integrity`/`pass_validity`) — test_real_stage_candidate_control_invalid_continues_and_roundtrips, test_real_stage_candidate_full_string_invalid_continues_and_roundtrips, test_real_stage_candidate_invalid_does_not_mask_integrity_halt (discriminating: yes)
Item 1 (b): recipe A keeps control and FULL_STRING failures as a HALT (LAW#3) — FIXED in code, NOT TESTED — arms.py:518–521 → read.py:260–264 — test_real_stage_order_law5_and_baseline_before_any_marker (discriminating: no; see BLOCKING N1)
Item 2 / ruling: pass1 runs the published map, records `selection_agreement_n`, no PASS1_FIXED_MAP halt — FIXED — arms.py:508–511 (gate removed), :543 — test_real_pass1_published_map_agreement_and_measured_delta_roundtrip (discriminating: yes)
Item 3 / ruling: δ stays as frozen (in-process measurement; 0.0 is valid) — FIXED (no code change, as ruled) — read.py:74 unchanged; arms.py:541 carries `step0.delta` into the pass record — test_real_pass1_published_map_agreement_and_measured_delta_roundtrip (discriminating: yes)
Item 4 / ruling: "nearest 8" = the layer nearest 8 among those within δ of the winner — FIXED (boundary convention: see ADVISORY A1) — read.py:81–82 — test_margin_delta_below_at_above_and_nearest8_tie, test_nearest8_contenders_and_margin_immediate_float_boundaries (discriminating: yes)
Item 5 / ruling: identity field renamed `preflight_controls_reference` — FIXED — arms.py:79, :115, :119; read.py:117–120 — test_preflight_controls_reference_identity_roundtrip_and_drift (discriminating: yes)
Item 6 (brief item 6): original-path LAW#5 writes must take exactly one override hit — FIXED — arms.py:321–322 — test_original_capture_requires_one_override_hit_and_restores (discriminating: yes)
Item 7 (brief item 6): (iv)/(v) unassigned band layers stay bit-identical — FIXED — arms.py:365, :381 — test_law5_singleton_and_multigroup_reject_any_unassigned_write (discriminating: yes)
Item 8 (brief item 6): Bshuf labels carry `-CONTROL-ONLY`; exit code keyed on `base_label` — FIXED — read.py:386–388, :464 — test_bshuf_control_only_labels_roundtrip_and_invalid_exit (discriminating: yes)

## Method

- Read the review (`results/c10v_layerpick_advisor_impl.md`), the ruling (`EXPERIMENT_RUNBOOK.md:345`, item (2), D-C10v-implfix), the Codex brief (`/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codex_c10v_fix_brief.md`), the prereg §2–§3 (`docs/C10V_LAYERPICK_PREREG.md:30–36, :58–75`) and the full diff (566 lines). The brief's item 6 explicitly ordered review items 6, 7 and 8, so those are in scope. Item 9 was not ordered and was not done.
- Ran the worktree selftest: 43/43 OK. No model, GPU or git state change.
- Ran a mutation test. I copied the three files into a scratch mirror root (`/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10v_mut/root`, with the other sources symlinked), applied 24 single-point mutants (`mutate.py` there) and recorded which tests fail. The unmutated baseline was green before and after.
  - Killed: candidate validity re-halting (in the loop and at persist); reader ignoring validity; control `<` → `<=`; dropping either validity reason; restoring PASS1_FIXED_MAP; pass1 running the fresh map; a δ floor; nearest-8 → 8; nearest-8 → runner-up; strict contender inclusion; strict margin; old field name; dropping the override pin or weakening it to `>= 1`; dropping either scope check; dropping the Bshuf suffix; exit code keyed on `label`.
  - **Survived:** M1g (the live recipe A gate calls `recipe_integrity` instead of `validate_recipe`), M1i (`validate_recipe` no longer calls `recipe_validity`), and M1h (the reader's `pass_integrity` checks A with `recipe_integrity` only).
- Checked the override-pin semantics against the harness. `my_edit` increments `Z_OVERRIDE_HITS` once per call when every key is overridden (`experiments/track_c/c10e_bandknob.py:186–188`). So `== 1` is correct for every original-path `capture_write` call: (ii) 24 requests in one call, the (iv) lone write, and the (v) per-group lone writes (`arms.py:349–350, :363, :388`).

## BLOCKING new defects

**N1. The diff removed the only test of the control and FULL_STRING HALT path and added none for recipe A, so the LAW#3 control gate is now unguarded.**

- **What changed.** Before the fix, the corrupt-record list tested `CONTROL_A1_single`, `CONTROL_A2_coherent2` and `FULL_STRING` through `validate_recipe` (old selftest :583, :602–603). That is the same function the live recipe A gate calls. The diff correctly removes those entries for B. However, after the split, recipe A's control and FULL_STRING HALT exists only because `validate_recipe` composes `recipe_integrity` with `recipe_validity` (read.py:260–264), and nothing tests that.
- **Why the existing test misses it.** The only live-A test (`test_real_stage_order_law5_and_baseline_before_any_marker`, selftest :930–932) sets `para_full_n = 67` without rewriting the detail rows. It therefore halts on `SUMMARY_COUNTS` and asserts only the prefix `"LIVE_LAW3"` (verified: `validate_recipe` on that fixture raises `SUMMARY_COUNTS: A1_single`).
- **Effect.** Mutants M1g and M1i both pass the whole suite. Under either one, a recipe A with A1 or A2 below 68, or a string/id divergence, would pass live LAW#3. arms.py:522 would then stamp `validity = {"ok": True}` on it, and the candidates would be read against an invalid baseline. This is ruling item 1(b) (the advisor's fix (b): "For recipe A, keep both as a HALT (LAW#3)").
- **Exact change** (`experiments/track_c/c10v_layerpick_selftest.py`, in `test_real_stage_order_law5_and_baseline_before_any_marker`). Replace
  ```python
  baseline = pass_fixture()["recipes"]["A"]; baseline["arms"][R.ARMS[0]]["para_full_n"] = 67
  with patch.object(D, "law5_checks", return_value=proof_fixture()), patch.object(D, "run_one_recipe", return_value=(baseline, {})) as recipes:
      self._assert_halt(lambda: runtime_stage(root, out, "pass1", pass_fixture()["fingerprint"]), "LIVE_LAW3")
      recipes.assert_called_once()
  ```
  with
  ```python
  for arm, gate in ((R.ARMS[0], "LIVE_LAW3: CONTROL_A1_single"), (R.ARMS[1], "LIVE_LAW3: CONTROL_A2_coherent2"),
                    (R.ARMS[2], "LIVE_LAW3: FULL_STRING: A7_coined_coined")):
      rec = pass_fixture()
      if arm == R.ARMS[2]: rec["recipes"]["A"]["arms"][arm].update(para_full_string=0.0)
      else: set_score(rec, "A", arm, 67)
      baseline = rec["recipes"]["A"]
      with patch.object(D, "law5_checks", return_value=proof_fixture()), patch.object(D, "run_one_recipe", return_value=(baseline, {})) as recipes:
          self._assert_halt(lambda: runtime_stage(root, out, "pass1", pass_fixture()["fingerprint"]), gate)
          recipes.assert_called_once()
      (out / "law5.json").unlink()
  ```
- **Verified in scratch.** The unmodified code passes 43/43 with this change, and M1g and M1i are now killed. The proposed file is `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10v_mut/proposed/c10v_layerpick_selftest.py`. It also contains the A3 addition below.

## ADVISORY

- **A1 (item 4 boundary, not result-changing in practice).**
  - **The inconsistency.** The contender set uses `row[j] >= winner − δ` (read.py:81), so a gap of exactly δ makes a layer a contender. The margin rule on the next line treats a gap of exactly δ as resolved (`margin >= delta` → the winner counts). The brief said "ties by the prereg's margin rule", and the advisor asked for the margin semantics to be kept consistent. The new test pins the inclusive form (`(0.625, 6)` at selftest :264), so it asserts what the code does rather than the margin convention.
  - **Why it rarely matters.** It bites only when δ > 0 and a third layer lands exactly at winner − δ, which is a float coincidence. When δ = 0, the near-set is never consulted.
  - **Change for consistency.** Use `row[j] > row[order[0]] - delta` and flip that test case to expect 5. Alternatively, record the inclusive choice as an operator ruling.
- **A2. `validity` is a second authority that nothing cross-checks.**
  - arms.py:522 hard-codes `{"ok": True, "reasons": []}` for A, and :537 stores the computed value for candidates.
  - The reader recomputes validity (read.py:311) and never compares it with the stored field, so a drifted field would go unnoticed.
  - Suggest computing A's value (`R.recipe_validity(baseline)`, required to be empty) instead of hard-coding it, and having `pass_integrity` require `rec["validity"] == {"ok": not r, "reasons": r}` with `r = recipe_validity(rec)`.
- **A3. M1h survives (reader side).** If `pass_integrity` checked A with `recipe_integrity` only, a record with an invalid recipe A would still let candidates read normally. The driver halts first, so this is defence in depth only. A one-line guard kills it: in `test_controls_and_baseline_envelope_boundaries`, for `name == "A"`, assert `R.candidate_reading(rec, "B")["base_label"] == "INVALID"` iff n < 68 (verified in scratch).
- **A4. `para_full == round(100·para_full_n/72, 1)` moved from integrity to validity.** That expression is a summary self-consistency check, not a science outcome, and it moved because it sits inside the FULL_STRING expression (read.py:252–254). A corrupted percent now reads INVALID instead of HALT. The outcome is still fail-safe (no credit), and the binding count uses `para_full_n`. Optionally split it back into `recipe_integrity`.
- **A5. Diagnostic names still say LAW#3.** `LAW3_REFERENCE` (read.py:120), `LAW3_REFERENCE_DRIFT` (arms.py:80), the `law3_reference()` loader and `--law3-ref` all still use the old name. The ruling renamed only the field, so this is within scope. A later rename would stop a reader of a halt diagnostic from mistaking it for the binding LAW#3 gate.
- **A6. Review item 9 not addressed.** It was not ordered: the reader's scope string still does not say that the locality gates are read on A7 only (read.py:407).
- **A7. Reader exit code 2 is ambiguous.** It now covers both an expected scientific INVALID candidate (read.py:464) and a reader integrity failure (:466–467). Any script that treats 2 as a crash will mis-handle a valid run where B0 is INVALID. The meaning is unchanged from before, but the case is now reachable.
- **Nothing else changed.** The rest of the diff is confined to the rulings and brief item 6. The added `import numpy as np` (arms.py:335) is needed by the scope checks. The pass2 test patch of `recipe_integrity` (selftest :1043) follows the split. No engine, harness or prereg file was touched.
