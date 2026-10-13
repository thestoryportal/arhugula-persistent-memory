Reviewer: Claude Opus 5.5 (claude-opus-5-5), independent adversarial advisor pass on `docs/C10X_ENGINEPATH_PREREG.md` v1 DRAFT, 2026-10-07 (method: `tools/advisor_review_prompt.md`; read-only, no GPU, no git state change)
Verdict: FIX-FIRST

Most important: the FE-specific lines of `fe_edit` (cur read at the edited layer, per-layer target lookup, undivided residual) have no reduction check at all — the identity mode turns all three off — so the bug most likely to produce a plausible-looking I-2 NULL is the one the inertness block cannot catch. That gap, together with a LAW#3 gate the reader applies only after the candidate recipes have run and a "pristine" model that `run_recipe` re-snapshots at entry, must be fixed before freeze.

## Answers to the four review questions (each claim cited)

**Q1 — seams without engine modification.** Both arms can be built with the engine unmodified.
- *I-1* uses the existing `Z_OVERRIDE` seam: `my_edit` takes `zs` from the table iff every `(subject, target_new.str)` key is present and `_LAW5_DEFAULT_CTX` is False (`experiments/track_c/c10e_bandknob.py:185–189`). Keys are `(subject, " " + value)` because `req` prefixes the space (`:96–97`). The solver is a new-file copy of `compute_z` (`memit_dry_run/memit/memit/compute_z.py:14–185`), so the engine stays untouched. The copy sits on the science path, which is why X1-(ii) is the right gate.
- *I-2 cannot be expressed through `ARM_HOOKS` or `Z_OVERRIDE`.* `zs` is one matrix reused at every layer (`:189`, `:202`). `cur` is read at `z_layer` (`:197–198`) and the residual is divided (`:204`). All three sit inside `my_edit`'s loop (`:194–217`). I-2 therefore needs a third seam: rebinding the module global `H.my_edit`. That works because `run_recipe` calls `my_edit(...)` by global name (`:489`), and so does `run_law5` (`:433`, under `_LAW5_DEFAULT_CTX = True`, `:430–435`). The precedent is `docs/C10V_LAYERPICK_PREREG.md:51`. The engine functions `fe_edit` calls are used unmodified:
  - `compute_z` at `layer = 4` (`compute_z.py:14–21`, `loss_layer = max(35, 4)`, `:76`);
  - `compute_ks` (`memit_dry_run/memit/memit/compute_ks.py:11–50`);
  - `get_module_input_output_at_words` (`compute_z.py:188–231`).

  The cost is that `fe_edit` is a hand copy of `my_edit:181–221`, so copy drift becomes the main risk (issue 3).
- *Inertness tolerances.* These are specified as relative-L2, tol = max(10 × floor, 1e-4) (prereg §2.4), but the rule has no ceiling (issue 9). The draft's claim that same-shape solves are bit-exact on this Mac is supported: the engine self-distance floor is 0.000e+00 (`results/c10s_sharedz_logs/inertness.log:9`), and the observer floor is 0.0 (`CORPUS/53_C10T_SECONDKEY.md:15`).

**Q2 — readout.** The binding count is the right one. `para_full_n` counts greedy full-sequence id matches over 24 × 3 held-out prompts (`c10e_bandknob.py:52–56`, `:108–117`, `:363`, `:396`). The baseline is same-process recipe A. The LAW#3 envelope is quoted exactly from `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`: para_full [5, 18], canon [5, 10], para_first [42, 59]. Defects:
- the gate fires only after the candidate recipes have run (issue 1);
- several outcomes satisfy two reading rows, or none (issue 4).

**Q3 — the two circulating errors.**
- (a) §0 item 1 states ρ_c correctly as a remaining-residual ratio. That matches `CORPUS/44:43` and `experiments/track_c/c10l_covgeom_step0.py:74–75, 134`.
- (b) §0 item 2 is accurate: `compute_z` places every target id (`compute_z.py:60–65`) and averages over all of them (`:141–150`); z reaches 0.99 (`CORPUS/36_C10_RESIDUAL_COINED_VALUES.md:28`); the weight-solve keys are subject-last only (`compute_ks.py:19–37`).
- Residues of both errors remain:
  - one wrong citation for where the old wording lives;
  - an unscoped "cannot be what FE fixes";
  - a §2.5 prediction phrased as if OverTone *supplies* continuation signal.

  See issues 5 and 6. No gate or label depends on either error.

**Q4 — budget.** Feasible on the M3 Pro; my estimate is ≈ 2.9 h for process 1 (issue 13).
- One `compute_z` solve takes ≈ 7 s: three solves in 21 s (`results/c10s_sharedz_logs/inertness.log:9`).
- One three-arm harness recipe including stacked extras takes 1826–2031 s (`results/c10q_stacked/logs_run.log:52, 82, 112`), so ≈ 26–30 min without the extras.
- fp16 / no-float64-on-MPS is respected: the harness solve is fp32 on CPU (`c10e_bandknob.py:205–211`), and the engine's float64 work is on CPU (`memit_main.py:191–203`).

## Issues (priority order)

### 1. BLOCKING — LAW#3 is read after the candidate arms have already run

**Defect.** CLAUDE.md LAW#3 requires the known baseline to reproduce "BEFORE any new data is trusted or any new arm is run". The draft does not do this:
- recipe A is cell 4, after cells 1–3 have solved and injection-screened every candidate target (prereg §2.7, lines 92–95);
- I-2 and I-1 then run immediately after A in the same `run_recipe` sequence;
- the envelope is checked only by the reader afterwards ("a run is labelled only by the reader", §2.8).

A miss would cost ≈ 1 h of candidate GPU time and leave candidate data on disk from a run with an unreproduced baseline. Recipe A needs nothing from cells 1–3: `my_edit` solves its own z (`c10e_bandknob.py:190–191`), and `run_recipe` snapshots and restores its own weights (`:461`, `:473`, `:506`).

**Fix — replace the §2.7 Process 1 list items 1–4 with:**
> 1. Recipe A first: `H.run_recipe("A", HP_BASE)` with `Z_OVERRIDE = None`, `FE_STATE = None` (original path; its own z solve; G inside). **In-driver LAW#3 gate, before anything else runs:** A's A7 `para_full_n` ∈ [5, 18]/72, `canon_full_n` ∈ [5, 10]/24, `para_first_n` ∈ [42, 59]/72, A1 ≥ 68/72, A2 ≥ 68/72 (`CORPUS/44:39`); a miss writes `pass1.json` with recipe A only, writes the halt diagnostic of §5 and exits non-zero — no candidate target is solved and no candidate recipe runs. The reader re-checks the same numbers.
> 2. Targets (engine z_8 for the injection reference, engine z_4 and replay, OverTone z_8^OT); hashes, fits, steps, norms.
> 3. Inertness X1-(i)–(iv), X2-(ii)–(vii). Any failure → HALT.
> 4. Injection screen (§2.5).
> 5. Recipes I-2 then I-1 (`H.run_recipe` twice), each with A1, A2, A7, the full readout, locality, probes and diagnostics.

**Also change in §3:** "LAW#3 known-baseline gate (recipe A; a miss → HALT, no candidate recipe is read)" → "LAW#3 known-baseline gate (recipe A; enforced in the driver before any candidate target or recipe runs, §2.7 step 1; re-checked by the reader)".

### 2. BLOCKING — "unedited/pristine" is not guaranteed; `run_recipe` re-snapshots whatever weights it finds

**Defect.** `run_recipe` sets `base_snap = snap_layers(hp)` at entry (`c10e_bandknob.py:461`). Every per-arm restore (`:473`) and the final restore (`:506`) go back to that snapshot, not to the loaded model. `pre_axes` and the `described_as` baselines are measured on the same state (`:471`, `:476`).

Several cells write to the band weights outside `run_recipe`:
- X1-(iv), X2-(ii) and X2-(iii) each apply ΔW (prereg §2.4, lines 85–87);
- cell 3's injection screen is declared to run on the "unedited model" (§2.5, line 95);
- cell 1's targets are declared "on the pristine model before any write" (§2.2 step 1).

If any of these writes is left applied — an exception path, or a restore that is missing or ordered wrong — two things happen silently: every later recipe treats the edited model as its baseline, and every later locality delta is measured against it. The draft has no check that would catch this.

**Fix — add to §2.4 as a new bullet and to the §3 validity list:**
> - **W0 pristine-weight identity (all cells).** Immediately after the harness import, the driver takes `PRISTINE = H.snap_layers(hp)` for layers 4–8 and records the SHA-256 of each tensor's bytes. Before cell 1, before each X-check that writes, after each X-check that writes (after its restore), before cell 3, before each `H.run_recipe` call and after the last one, the driver recomputes the five hashes; any mismatch → HALT (diagnostic: which cell, which layer). Every X-check that writes restores from `PRISTINE` (not from a local snapshot) and zeroes its own cache.

### 3. BLOCKING — the FE-specific code path has no reduction (inertness) check

**Defect.** `fe_edit` differs from `my_edit` in three ways (§2.2 step 3, line 59):
- (a) per-layer targets come from `FE_TARGETS`;
- (b) `cur` is read at `layer`, not at `z_layer` (`:197–201`);
- (c) the residual is not divided (`:204`).

X2-(iii) runs `mode = "identity"`, which by its own definition (line 60) turns all three changes off. It therefore tests only the lines `fe_edit` shares with `my_edit`, and none of (a)–(c). X2-(iv) tests the *replay* reader, not `fe_edit`. Two concrete bug classes would pass every gate in §2.4 and yield an ordinary-looking count:
- `cur` still read at `z_layer` (the copied `:198` argument not changed);
- `FE_TARGETS` rows indexed by list position in the wrong order.

This is what the brief calls "seam present but reduced to identity". The I-2 seam needs a reduction of its *active* path.

**Fix — add to §2.4:**
> - **X2-(vi) FE-path single-layer reduction.** `hp1` = the hparams with `layers = [8]`; `P1 = compute_P(hp1)`; zero cache; A7 24 requests; `FE_TARGETS1[(s, t)] = {8: z_8}` (the engine z_8 of cell 2). `fe_edit(hp1, …, mode = "fe")` against the original `my_edit(hp1, …)` with `Z_OVERRIDE` = the same z_8 table, both from `PRISTINE`: ΔW_8 within the X2-(ii) tolerance. With one layer, (b) reads at 8 = `z_layer`, (c) divides by 1 and (a) looks up m_8 = z_8, so the path is the FE path with the identity reached through its own lines; any distance is a defect in them.
> - **X2-(vii) FE-path structure (catches what X2-(vi) cannot: the layer read and the table index).** `FE_TARGETS` values are dicts keyed by layer integer, never lists; `fe_edit` asserts `set(FE_TARGETS[key]) == set(hp.layers)` and records, per layer, the integer layer it passed to `get_module_input_output_at_words` (must equal `layer`). Inside the I-2 recipe's A7 arm, before layer 4's update (pristine weights), the per-request residual norm `‖M[4] − cur_4‖` equals `‖z_4 − h_4^{(0)}‖` recorded in cell 1 by the independent replay reader within the X2-(iv) tolerance; a mismatch → HALT.
> Predicted halt and its one fix: X2-(vii) mismatch → `cur` read at the wrong layer or the table mis-keyed; diff `fe_edit` against `my_edit:194–204` line by line.

**Also update §2.7 cell 3, §3 validity, §5 HALT list:** "X2-(ii)–(v)" → "X2-(ii)–(vii)" and add "W0".

### 4. BLOCKING — reading rules: one outcome can satisfy two labels or rows, some outcomes satisfy none, and the trigger for process 2 is ambiguous

**Defects.**
- (i) §3 attaches -LARGE-WRITE and -UNDERFIT to LEAD or PARTIAL ("does not pass gate A", lines 123–124). But §2.7 starts process 2 (≈ 3–3.5 h) "only if an arm reads LEAD or PARTIAL" (line 97). A PARTIAL-LARGE-WRITE therefore both triggers a 3-hour replication and cannot pass it. The same outcome also matches two rows of the reading table: "LEAD or PARTIAL, replicated" and "TRADEOFF or -LARGE-WRITE" (lines 131, 134).
- (ii) For I-2, reading row 2 needs injection ≥ reference − 5, and NULL-TARGET-WEAKER needs ≤ reference − 10 (line 95). A deficit of 6–9/72 maps to no row. The I-1 cells of row 3 use a different threshold (≥ 6), so the two columns are not symmetric.
- (iii) An I-2 NULL can carry both -UNDERFIT and NULL-TARGET-WEAKER, and the draft gives no precedence. A NULL with an underfit z_4 that still injects well would fall into row 2 ("spreading is not the wall"), although the target was underfit.
- (iv) If process 1 reads LEAD and process 2 reaches only PARTIAL size, the rule (line 125) gives "-NOT-REPLICATED", which discards a replicated PARTIAL.

**Fix — replace the §3 Qualifiers paragraph, the first sentence of §2.7 Process 2, the replication paragraph and the reading-table rows with:**
> **Qualifiers (applied after the count; a qualified label never triggers process 2 and is never adopted):** **-LARGE-WRITE** if Σ_l ‖ΔW_l‖_F (A7) > 1.5 × A's; **-UNDERFIT** (I-2 only, z_4 fit screen of §2.5 failed). Precedence for an I-2 NULL: -UNDERFIT, then NULL-TARGET-WEAKER, then plain NULL — the first that applies is the reading; the others are recorded.
> **Process 2 (gate A) runs only if an arm reads unqualified LEAD or unqualified PARTIAL.**
> **Replication:** process 2 reproduces a LEAD if its count meets the LEAD rule, and a PARTIAL if it meets the PARTIAL rule (> 18 and gain ≥ 10 over process 2's A); a process-1 LEAD whose process 2 meets only the PARTIAL rule reads **PARTIAL (replicated)**; anything else is -NOT-REPLICATED.
> Reading-table rows (exactly one applies; first match wins): 1 INVALID-CONTROLS; 2 LEAD/PARTIAL replicated, unqualified; 3 any label carrying -LARGE-WRITE, or TRADEOFF; 4 I-2: -UNDERFIT or NULL-TARGET-WEAKER → "uninformative about spreading"; I-1: target injects ≤ reference − 6 → "the reweighted target is worse before any write"; 5 NULL with the target's injection within (reference − 9, +∞) for I-2 / (reference − 5, +∞) for I-1 → the row-2 text of v1; 6 NULL with an I-2 injection deficit of 6–9/72 → "NULL, target-strength not interpreted".

### 5. ADVISORY — premise (a): correct wording, wrong source citation, and an unscoped inference

**Defects.**
- §0 item 1 says the old "3 %" wording survives at `recommended_sequence.md:13`. Line 13 is the "Writing, not training" criterion. The old wording ("aimed squarely at the '3 percent installed' finding") is at `results/research_pass_2026-10-06/recommended_sequence.md:28`.
- The step-6 row and the "Bad: the closed-form spreading itself is the limit" quote are also at `:28`; the draft cites `:26` twice (header line 3 and §0 line 15), and `:26` is the gate-A row.
- §0 item 1 and H-X2-null rely on step 0's *offline* 0.028. `CORPUS/44:43` itself says the behavioural-run value was then unmeasured. The in-harness value now exists: subject-key remaining fraction 0.032650 canonical / 0.233728 held-out (`CORPUS/53_C10T_SECONDKEY.md:62`).
- "The canonical-position residual cannot be what FE fixes here" is I-INFER: a residual norm does not establish behaviour (`CORPUS/44:40`).

**Fix — replace the relevant sentences of §0 item 1 with:**
> "≈ 2.8 % of the canonical residual norm *remains* after the band write in step 0's offline reconstruction (`CORPUS/44:43`), and 0.0327 canonical / 0.234 held-out remain in the harness run of `CORPUS/53_C10T_SECONDKEY.md:62` (baseline arm); `recommended_sequence.md:28` and `prereg_stubs.md:75` still carry the old wording. **I-INFER:** since the canonical keyed-position residual is already ≈ 0.03, FE is unlikely to act through that number here; what it can change is which layers carry the write and hence the collateral change at non-keyed positions and on paraphrases (the held-out residual is still ≈ 0.23)."

Change `recommended_sequence.md:26` → `:28` in the header (line 3) and in §0 "What this experiment can and cannot conclude". In H-X2-null, change "The canonical residual is already ≈ 97 % installed (§0 item 1)" → "The canonical keyed-position remaining residual is already ≈ 0.03 in-harness (`CORPUS/53:62`), ≈ 0.23 held-out".

### 6. ADVISORY — premise (b): the correction is accurate; three residues remain

**Defects.**
- §0 item 2 cites `compute_z.py:68–73` as where "keys are read at the subject's last token". Those lines compute the *z-solve's* intervention index. The weight-solve keys come from `compute_ks.py:19–37` (rewrite-module input, `fact_token`, `[0]`) and harness `c10e_bandknob.py:196`.
- It quotes `CORPUS/45:24` as "59, 66, 51, 19, 34, 20 /72". The denominators are 72, 72, 72, 72, 69, 39.
- §2.5's prediction ("if OverTone supplies continuation signal, positions ≥ 3 rise") reintroduces the framing that the continuation lacks signal. `compute_z` already scores every position (`compute_z.py:60–65`, `:141–150`); OverTone *reweights* that signal.

**Fix:**
- §0 item 2, replace "(`find_fact_lookup_idx`, `compute_z.py:68–73`; `compute_ks.py:19–50`; harness `c10e_bandknob.py:196`)" with "(`compute_ks.py:19–37`, keys at `fact_token = subject_last`; harness `c10e_bandknob.py:196`; the z-solve's own intervention index is the same token, `compute_z.py:68–73`)".
- Replace "59, 66, 51, 19, 34, 20 /72" with "59/72, 66/72, 51/72, 19/72, 34/69, 20/39".
- §2.5, replace the prediction with: "*Prediction for the arc's I-1 reading:* if reweighting the per-token objective of the target changes how the written value continues, the teacher-forced counts at positions ≥ 3 change relative to A; reported per position with its own denominator, not gated."

### 7. ADVISORY — I-1 attribution: OverTone's mechanism is confounded with a lower global fit

**Defect.** The mixture branch activates only when y is the argmax of the mixture (§2.3, line 53). Before that, π_tar = onehot and the loss is the engine's cross-entropy. Once y leads at a position, KL(π_tar ‖ π_θ) is small. The engine's stop rule (`compute_z.py:164–165`, total < 0.05) then fires near the point where y just leads at every position. The draft concedes that the fit at stop is "below 0.99 by design" (line 59).

An I-1 vs A difference therefore mixes the token-heterogeneous reweighting with a uniformly earlier stop. As written, the reading-table row "the target objective is a knob; candidate default for the target solve" over-claims a mechanism.

**Fix:**
- Reading table, I-1 row 1: "the OverTone-objective target (which also stops at a lower fit) is a knob on this harness; whether the gain comes from the per-token reweighting or from the earlier stop is not separated here".
- Optionally add a non-gating diagnostic recipe (≈ 10 min of solves + ≈ 30 min recipe): engine cross-entropy with the solve stopped at the first step where y is top-1 at every scored position. Its count beside I-1 separates the two readings.

### 8. ADVISORY — I-2 attribution: forward replay is confounded with "write the full residual at layer 4"

**Defect.** With the residual undivided and the harness solve realising ≈ 97 % at a layer (issue 5), layer 4 carries almost the whole write. Layers 5–8 see only the propagated shortfall, as the draft itself predicts (§2.5, "FE is expected to concentrate the write at layer 4"). A LEAD would then not distinguish "forward-replayed per-layer targets" from "a single-layer write at layer 4 toward z_4". §7 item 9 records "no FE 'OneLayer' control". The reading table's "the per-layer target construction is a knob" claims more than that design can show.

**Fix:**
- Reading table, I-2 row 1: "FE as a package (z at layer 4, forward-replayed targets, undivided residual) is a knob on this harness; replay vs. single-layer-at-4 is not separated".
- Optionally add the OneLayer control as a fourth recipe: `fe_edit` with `layers = [4]`, `FE_TARGETS = {4: z_4}`, ≈ 30 min, which is within budget.
- In §2.5, write the -LARGE-WRITE prediction now (FE's layer-4 ΔW vs A's layer-4 ΔW, which is fed 1/5 of the residual, `c10e_bandknob.py:204`), so a -LARGE-WRITE qualifier on I-2 cannot be read as a surprise.

### 9. ADVISORY — the tolerance rule needs a ceiling

**Defect.** tol = max(10 × floor, 1e-4) (§2.4, line 79) has no upper bound. A non-zero platform floor, for example after a PyTorch/MPS update, would silently loosen X1-(ii), X1-(iv), X2-(iii) and X2-(vi) by a factor of 10. The measured floors so far are 0.0 (`results/c10s_sharedz_logs/inertness.log:9`; `CORPUS/53:15`).

**Fix — append to the tolerance rule:** "If any measured floor exceeds 1e-4 relative, HALT before any parity check: same-shape arithmetic was expected to be exact on this platform and the floor itself is the anomaly to diagnose."

### 10. ADVISORY — X2-(iv)(a) checks the wrong batch shape

**Defect.** `fe_edit` reads `cur` for all 24 requests in one padded call (`c10e_bandknob.py:197–201`, the `context_templates` list holds 24 prompts). X2-(iv)(a) instead compares the replay against single-request calls (`[CANON], [c]`, line 88). The C10S lesson the draft cites is that batch shape changes fp16 results.

**Fix:** "(a) … equal, within tolerance, to the per-request columns of **one** call `get_module_input_output_at_words(model, tok, l, [CANON]*24, FICTION, hp.layer_module_tmp, "subject_last")[1]` (the batch shape `fe_edit` uses); the single-request reading is recorded beside it."

### 11. ADVISORY — vectorised OverTone loss: keep the X1-(ii) parity exact and NaN-safe

**Defect.** §2.3 relies on `extra ≡ 0` through arithmetic: `(π_tar − onehot)·log π_θ` and `xlogy`. Vectorised over the padded `[P, T, V]` block, the dummy label at masked positions (`compute_z.py:144` gathers index 0 there) still goes through the filter and mixture, and any non-finite intermediate becomes NaN·0 = NaN after `· mask`.

**Fix — add to §2.3:** "`extra` is computed only where `rewriting_targets != −100` and set with `torch.where(mask_bool, extra, 0)` (never multiplied by the mask); the skip branch sets `extra` to exactly 0 with `torch.where(mix, extra_mix, 0)`; `tok_loss` at masked positions is `torch.where(mask_bool, tok_loss, 0)` before the sum."

### 12. ADVISORY — G is described inaccurately, and counter resets are unspecified

**Defect.** §2.4 G says `Z_OVERRIDE` and `FE_STATE` are "unset for its duration". In fact the driver sets both before calling `run_recipe`, and `run_law5` runs inside it (`c10e_bandknob.py:463`). The protection is `_LAW5_DEFAULT_CTX = True` (`:430–435`), which `my_edit` tests (`:186`) and `dispatch` must test. `Z_OVERRIDE_HITS` is also incremented by the X-checks that use `Z_OVERRIDE` outside a recipe (`:187–188`).

**Fix — replace the G bullet with:** "G: the standing `run_law5` INERT inside every recipe (`:463`); during it `FE_STATE`/`Z_OVERRIDE` remain set and the original path is taken because `_LAW5_DEFAULT_CTX` is True (`:430–435`), tested by `my_edit` (`:186`) and by `dispatch` reading `H._LAW5_DEFAULT_CTX` at call time." Add to Counters: "`H.Z_OVERRIDE_HITS` and `FE_CALLS` are reset to 0 immediately before each `H.run_recipe` call and read immediately after it; exact equality (A: 0/0; I-2: 0/3; I-1: 3/0) also detects a LAW#5 call that leaked into a seam."

### 13. ADVISORY — compute: feasible; replace the uncited estimates with measured ones

**Evidence.**
- `compute_z` takes ≈ 7 s (3 solves in 21 s, `results/c10s_sharedz_logs/inertness.log:9`).
- One three-arm recipe takes ≈ 26–30 min; the full c10q pass took 1826–2031 s including the 132–466 s stacked extras (`results/c10q_stacked/logs_run.log:41, 52, 71, 82, 101, 112`).

**Estimate for process 1 after the issue-1 reordering:**

| Cell | Work | Time |
|---|---|---|
| Recipe A | | ≈ 30 min |
| Targets | 216 solves | ≈ 25 min |
| Inertness | 72 reduced OverTone solves + floors + about seven 24-request writes, some evaluated | ≈ 35 min |
| Injection | | ≈ 25 min (draft's C10S figure) |
| I-2 + I-1 recipes | | ≈ 60 min |
| **Total** | | **≈ 2.9 h** |

That fits the 3–3.5 h envelope with little slack. Issue 8's optional control adds ≈ 30 min; issue 7's adds ≈ 40 min.

**Fix — in §2.7 Compute, replace "a harness pass with three arms ≈ 34 min" with:** "a three-arm recipe ≈ 26–30 min (`results/c10q_stacked/logs_run.log:52, 82, 112`, minus the stacked extras at `:41, 71, 101`); one `compute_z` ≈ 7 s (`results/c10s_sharedz_logs/inertness.log:9`)". Also add: "a LAW#3 miss now ends the process after ≈ 30 min (issue 1 of the advisor pass)".

## Drift check and overturning test

Both arms sit on step 6 of the integrated queue: `docs/INTEGRATED_QUEUE_2026-10-07.md:21` ("harness seams only, engine unmodified, LAW#5 inertness first"). That ties them to the live C10 falsifier, so there is no drift. The cheapest test that could overturn the design premise of I-2 needs no write: compare the injection screens of z_4@4 and z_8@8 (already in cell 3). Running that cell before the recipes, as issue 1 already orders, means a NULL-TARGET-WEAKER is known before ≈ 30 min of I-2 recipe time is spent.
