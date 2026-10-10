# C10Z ASTRA process 1: HALTED-V4 diagnosis (read-only)

Written 2026-10-08 by a read-only diagnostic subagent. No GPU or model code was run, and no file other than this one was edited. Paths are relative to the worktree root `W`.

## Bottom line

The program hypothesis holds, and the evidence is stronger than expected. ASTRA's recipe A reproduced, **exactly**, a seed-0 baseline the program had already recorded on 2026-10-06: A7 first 40, full 7, canon 7; A1 69; A2 69; described_as 90.38; L3 KL 0.00013; ppl 21.506; LAW#5 Δexpr 0.0011 and Δloc 0.01. Every earlier run that sat inside the envelope was unseeded, so each process drew its own context templates. Seed 0 always draws the same set, `e8605172dce0`, and that set gives A7 first 40. A plain re-run will give 40 again. Option (a) as written cannot be carried out, because the C10W hash `306cb0089ddd…` identifies the oracle's training prompts, not MEMIT context templates.

## Finding 1: which templates ASTRA process 1 used

**They were not recorded anywhere.**
- The engine prints `Cached context templates` (`memit_dry_run/memit/memit/memit_main.py:321`). The first sampling happens inside `run_law5`'s `apply_memit_to_model` call, and that call runs under `contextlib.redirect_stdout(io.StringIO())` (`experiments/track_c/c10e_bandknob.py:422–423`). The print is therefore swallowed: `results/c10z_astra/logs/resident_p1.log` has no such line.
- The driver writes `context_templates.json` only after the gate passes. The gate is at `experiments/track_c/c10z_astra_arms.py:973`, and the write is at `:981` (or `:984` in process 2). `results/c10z_astra/` holds only `halt_p1.json`, `pass_p1.json`, `pristine_hash.json`, `run.json` and `logs/`.
- `halt_p1.json`, `pass_p1.json` and `architecture_profile/c10z_astra_halt_diagnostic.json` (byte-identical to `halt_p1.json`) contain no template, ctx or seed field. `recipes.A` holds only `arms`, `band`, `cov_cache_sha256`, `delta_norms`, `detail`, `hparams`, `law5_gate` and `projector`.
- **This deviates from the prereg.** `docs/C10Z_ASTRA_PREREG.md:122` (§2.6 stage 0 step 2) puts the template freeze and write in step 2, before the step-3 LAW#3 gate (`:123`). The implementation reverses that order.

**Inferred set: `e8605172dce0`.** This is a 12-hex prefix of `sha256(json.dumps(templates))`, the scorer's convention (`experiments/track_c/autoresearch_c10/scorer.py:106`). The set is: `"{}"`, "The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}". It is logged in `results/autoresearch_c10_equivalence.log` and `results/autoresearch_c10_equivalence_rerun.log`.

The inference rests on three points:
- **Same seed and call order.** The autoresearch scorer calls `torch.manual_seed(0)` before it imports the harness (`scorer.py:47–52`). It then runs `compute_P`, then `run_law5` (`:96–100`), which is where the first sampling happens. ASTRA follows the same order: `c10z_astra_arms.py:506` seeds, then imports `c10e_bandknob`, then runs recipe A (`compute_P`, then LAW#5, then the arms; see the order in `resident_p1.log`).
- **The seed reproduces the set across processes.** `results/autoresearch_c10_equivalence.json` records `seed_reproduces_templates: true` and `e8605172dce0` in two processes. Every later seed-0 sandbox run carries the same hash (table below).
- **An exact match on all twelve fields.** The harness's own `H.run_recipe` produced these values under seed 0 (`results/autoresearch_c10_equivalence.json` → `scorer_vs_run_recipe`):

| | A7 para_first_n | A7 para_full_n | A7 canon_full_n | A7 string | described_as | L3 | L3 KL | ppl post | A1 | A2 | LAW#5 Δexpr / Δloc |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ASTRA p1 (`halt_p1.json` `recipes.A`; `resident_p1.log`) | 40 | 7 | 7 | 7 | 90.38 | 30/30 | 0.00013 | 21.506 | 69 | 69 | 0.0011 / 0.01 |
| Seed-0 equivalence, 2026-10-06 | 40 | 7 | 7 | 7 | 90.38 | 30/30 | 0.00013 | 21.506 | 69 | 69 | 0.0011 / 0.01 |

No other run in `results/` has LAW#5 = (0.0011, 0.01) together with these counts.

Status: **inferred with very high confidence; not directly observed.** A direct confirmation needs a short model process: seed 0, import the harness, call `get_context_templates`, hash the result. That falls outside this read-only task.

## Finding 2: prior recipe-A / LAW#3 reproductions

"Seeded" here means the global torch RNG was seeded. The harness does not seed it (no `manual_seed` in `c10e_bandknob.py`). Nor do the C10W evaluator (`c10w_oracle_eval.py`), the C10T, C10Q or C10V drivers, or the C10U driver; C10U uses only a local `torch.Generator` (`c10u_mint2_arms.py:722`). `generate_fast` samples with top-k multinomial (`memit_dry_run/memit/util/generate.py:113–119`).

| Run (record) | Seeded? | Templates | A7 first / full / canon | A1 / A2 |
|---|---|---|---|---|
| CORPUS/37, 38, 39 baselines (A4 text, `docs/C10L_COVGEOM_SPARSEBAND_PREREG.md:117–119`) | no | sampled per process, unrecorded | 54, 52, 56 / 10, 8, 15 / 6–7 | ≥68 |
| C10L run1 baseline (`results/c10l_covgeom/run1_armB_identity.json`) | no | sampled, not logged | 54 / 13 / 7 | pass |
| C10L run2 baseline (`run2_armC_set48.json`) | no | sampled, not logged | 45 / 10 / 6 | pass |
| C10L run3 baseline (`run3_armC2_set78.json`) | no | sampled, not logged | 52 / 13 / 9 | pass |
| C10K R0 baseline (`results/c10k_route_a/R0_baseline.json`, in %) | no | sampled | 55 / 10 / 8 | 68 / 71 |
| C10Q single-edit reference (`CORPUS/50_C10Q_STACKED_SOLVE.md:14`) | no | sampled, **logged** `c7dabbe7c25a` (`results/c10q_stacked/logs_run.log:9`) | 52 / 12 / 8 | 70 / 71 |
| C10T r2 single-key arm (`results/c10t_secondkey_r2/pass1.json`) | no | sampled, logged `39432debe475` | 51 / 15 / 7 | 70 / 70 |
| C10U r1, r2, r3 F A7-multi(frozen) (`results/c10u_mint2/{,r2/,r3/}F_r0_multi_snone.json`) | no | **pinned** per attempt (`ctx`, `ctx_sha256`): `d85cf034bc85`, `177b1887c64d`, `44a0d3d9712c` | 55/10/8, 52/10/9, 53/14/8; r3 replicate F_r1 with the same pinned set: **53/14/8, identical** | — |
| C10V recipe A (`results/c10v_layerpick/pass1.json`) | no | **pinned**, sampled in step 0 (`7f182fa35b1e`, `ctx_sha256` 91c1a4e7…), loaded in pass 1 (`c10v_layerpick_arms.py:138–143`) | 45 / 11 / 9 | pass |
| C10W P1 preflight / P1 eval / P2 attempt 1 / P2 eval, closed form (`results/c10w_oracle/p1_*/preflight_eval.json`, `eval.json`; `p2_*/attempt1_halted/eval.json`, `eval.json`) | no | sampled, **never logged** | 54/16/8, 52/9/9, 54/10/8, 54/11/7 | 71 / 71 (P2) |
| Autoresearch seed-0 equivalence and sandbox baseline (`results/autoresearch_c10_equivalence{,_2026-10-06T0815}.json`; `…/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json`, saved tensors bitwise-equal: `c30664a9…`) | **seed 0** | `e8605172dce0` | **40 / 7 / 7** (3 processes) | 69 / 69 |
| **ASTRA p1** | **seed 0** | unrecorded; inferred `e8605172dce0` | **40 / 7 / 7** | 69 / 69 |

On C10W `TEMPLATE_SHA 306cb0089ddd…`: this hash covers the 20 **oracle-training prompt templates** (`experiments/track_c/c10w_oracle_step0.py:19–28`; asserted at `c10w_oracle_selftest.py:488` as `sha_text("\n".join(S.TEMPLATES))`). It does not cover MEMIT context templates. C10W's closed-form recipe sampled the engine context templates per process, unseeded and unlogged; `grep -rl "Cached context" results/c10w_oracle*` returns nothing.

Unseeded spread of A7 para_first across about 13 draws: **45–56**. The seed-0 draw, 40, sits 5 below the lowest unseeded draw. para_full (7) and canon (7) are inside the envelope; only para_first misses, by 2 counts.

## Finding 3: earlier runs on seed-0-sampled templates

Yes. The C10R autoresearch program ran on them throughout 2026-10-06, all with `seed 0` and templates `e8605172dce0`:
- Bitwise-baseline processes: the equivalence check at 08:15 and again at 11:46, plus the sandbox baseline at 13:11. All three gave 40/7/7 and 69/69. The program already knew these values: `SESSION_CHECKPOINT.md:521` lists "first_token 40" as the frozen baseline row, and `results/autoresearch_c10_sandbox_probe.md:210` repeats it.
- Ten agent-edited sandbox and replay runs carry the same hash. Their counts differ only because their edits differ.

ASTRA is therefore the fourth seed-0 process to give 40.

## Finding 4: does anything else in ASTRA's recipe A differ?

I compared `halt_p1.json` `recipes.A` against the closed-form recipe in `results/c10w_oracle/p2_20261008T034226_086980Z/eval.json` (`recipes.closedform`, `environment`):
- **Same:**
  - hparams path (`configs/hparams/qwen25_3b_memit_hparams.json`; benchmark source SHA `4225cc6a…`)
  - band [4–8] and projector `nullspace`
  - all five `cov_cache_sha256` values (`cov equal True`)
  - model revision `3aab1f19…`, fp16, MPS (ASTRA requires these at `c10z_astra_arms.py:508–513`)
  - engine SHA `d941a9fb…`, `_cov_cpu 3`
  - arms, stimuli (24 FICTION, mean_ntok 5.5), and the PTEST eval prompts (unmodified harness)
- **Inherited knobs:** ASTRA refuses `N_EDIT`, `C10_SUBJECT_OFFSET`, `C10_CTX_TEMPLATES` and the others (`c10z_astra_arms.py:28`).
- **Different:** only what depends on the templates. LAW#5 Δexpr/Δloc is 0.0011/0.01 in ASTRA versus 0.0002/0.91 in C10W, and these values move with every draw (see the LAW#5 column across runs). The A7 per-layer delta norms differ by 0.2–4%; the 4.35% cross-process spread is documented in CORPUS/44 F-A4.
- **Environment drift is ruled out**, because ASTRA matches the 2026-10-06 seed-0 run exactly. That run used the same harness path (`H.run_recipe` and `my_edit`) on the same machine.

There is no evidence of any difference other than the template draw.

## Finding 5: what the prereg says about V4, and what a re-run would do

- **The prereg has no remedy for a V4 halt.** §3 V4 (`docs/C10Z_ASTRA_PREREG.md:217`) states the envelope. Stage-0 step 3 (`:123`) says a miss writes the baseline-only record and exits. §5 (`:321–322`) says the runs made "are kept as data, not promoted", under the generic "one speculative fix after a `cat -n` read, then HALT" rule. It does not say whether to re-run, amend or abandon.
- **The seed rationale was wrong.** The seed row (`:103`) says "nothing stochastic is expected". But the engine views (D-2, `:349`) come from stochastic `generate_fast`, and the seed fixes which draw those views are. Reproducibility for process 2 already comes from the frozen template file and its SHA in `H_in` (`:122`, `:133`, `:137`), not from the seed.
- **The seed is wired into the records.** `seed: 0` is part of the manifest (`c10z_astra_arms.py:1339`), and `:1366` requires `parts["seed"]==0` under HALTED-V12.
- **A re-run under seed 0 is expected to reproduce 40 exactly.** `REPRODUCIBILITY.md:26` says cross-process bit-exact weights do not hold, but that line dates from the GPU era. On this Mac's MPS, the evidence runs the other way: three seed-0 processes gave bitwise-identical saved tensors and the same template hash, and the C10U r3 pinned-template replicates gave identical counts. `REPRODUCIBILITY.md` should be updated for MPS; this note does not change it.

## Options

**(a) Pin to the "C10W step-0 template set".** Not executable as stated: that set does not exist (Finding 2). A variant, **(a′)**, pins a different logged engine set that has an in-envelope baseline:
- **C10Q `c7dabbe7c25a` (52/12/8).** ASTRA's own benchmark already freezes this exact set as its `TEMPLATES`, chosen before V4 was seen (`c10z_astra_benchmark.py:34–40`; `templates_source results/c10q_stacked/logs_run.log:9`; benchmark `inputs.templates_sha256 d6c7c700…`).
- **C10V `7f182fa35b1e` (45/11/9).** Already used as a pinned cross-process recipe-A input.

Assessment:
- **For:** both sets are engine-sampled, so the substance of D-2 holds. Templates then come from a file (C10U and C10V precedent). The C10Q choice carries pre-observation provenance inside the ASTRA record.
- **Against:** any choice made after seeing V4 fail selects inputs conditional on the baseline outcome. The templates are also the writer's views, so the swap changes the candidate's inputs, not only the gate. It needs a dated amendment plus a GPT-6-Astra pass.
- **Fishing risk:** moderate if the rule is "the set ASTRA's benchmark already froze"; high if it is "pick a set that passes".

**(b) Drop the seed and take one unseeded draw.**
- **For:** this matches how every envelope observation was produced, and process 2 stays reproducible through the frozen file.
- **Against:**
  - Process 1 is no longer reproducible by seed.
  - It needs a code change: the seed is part of the manifest and the reader requires `seed==0` (`c10z_astra_arms.py:1339`, `:1366`).
  - A re-draw after a failure is a re-roll in form. Expect roughly a 1-in-13 or worse chance of a second V4 miss, given the observed tail.
  - Each draw costs a recipe-A run (2,040 s allowance).
- **Fishing risk:** low only if exactly one draw is committed to before it is made, and its outcome is final.

**(c) Re-run unchanged.** This will reproduce 40 and halt V4 again, at about 34 minutes or more of GPU time. It has no value.

**(d) Deeper diagnosis first.** Finding 4 shows no difference beyond the templates, so a broad harness hunt is not warranted. One residual gap is worth closing: confirming that ASTRA's draw really is `e8605172dce0`. That is a few minutes of model time with no edit.

**(e) An option I am adding: amend V4 so a seeded run is judged against its own known baseline.**

The amendment would read: "V4 passes if recipe A is inside [42, 59] / [5, 18] / [5, 10], **or** reproduces exactly the pre-existing seed-0 recipe-A record (`results/autoresearch_c10_equivalence.json` `scorer_vs_run_recipe`: A7 40/7/7, A1 69, A2 69)."

- **For:**
  - This is LAW#3 in its literal sense: a known-baseline reproduction against a characterized value for this exact configuration, recorded two days before ASTRA launched.
  - The criterion is stricter than the envelope (an exact match).
  - It does not change the seed, the views or any candidate input, and it widens nothing for other configurations.
- **Against:**
  - It still amends a gate after the gate failed, which is the classic forking-path pattern, so it needs a dated amendment, an advisor pass and a GPT-6-Astra pass.
  - ASTRA would run on the lowest-first-token template draw on record. It is single-draw, and process 2 reuses the same frozen file, so "replicated" never tests sensitivity to the template draw. That has to be stated as a limitation on any LEAD.

## Recommendation, with risks

1. **Treat this as a gate-specification error, not a harness fault.** ASTRA reproduced a characterized seed-0 baseline bit-for-behavior. The envelope was derived from unseeded draws and does not cover the seed-0 draw. Halting was correct under the frozen text.
2. **Fix the recording gap no matter which option is chosen.** Write `context_templates.json` and its SHA before the LAW#3 gate, as prereg §2.6 step 2 already requires. This is an implementation-to-prereg conformance fix, not a science-path change.
3. **Prefer (e).** If the operator or reviewers reject a gate amendment, prefer (a′) with the C10Q set, chosen because the ASTRA benchmark already froze it before observation. Reject (c). Treat (b) as the weakest: it needs code changes, carries re-roll optics and risks a second miss.
4. **Before relaunching, optionally run the few-minute no-edit confirmation from (d)**, so the amendment cites an observed template hash instead of an inferred one.

Risks:
- **For (e):** a reviewer may judge any post-failure gate change to be fishing. A LEAD would be conditional on one atypical template draw. Disclose both.
- **For (a′):** the candidate's views change after a failure.
- **For all options:** the A4 envelope under-covers the real draw distribution. With 13 unseeded draws at 45–56 plus seed 0 at 40, other preregs that copy [42, 59] (C10X `:132`, C10Y `:189`) inherit the same exposure.

Any option is an operator and review decision. Record it as a D-ID with a dated prereg amendment before relaunch.
