# C10K Official-Upstream AnyEdit C10 Gate - Preregistration

**Decision-ID:** `D-C10k-anyedit-official-upstream`
**Date:** 2026-06-27
**Class:** source-faithful external method gate; can-fail; C10-informative if controls pass.
**E2e-map cell:** §8 write engine and §8.9 L2 behavioral firing for Genesis Layer-4 `domain_concept`; fixed deployment target remains `local Intel CPU + batch writes` after offline edit.
**North-star contract:** C10 is OPEN/BLOCKING unless an in-weight method can express project-coined multi-word semantic values. A Git/index/side-store fallback is not an F1 closure under the operator's stated contract.
**Scope:** official `jianghoucheng/AnyEdit` source at commit `057a77f185f7ffb55818f6bd9add37f43bb447e7`; isolated upstream-compatible environment; stock-upstream anchor, A1/A2 easy controls, and hard A7 run in one session; A7 interpreted only if stock anchor and A1/A2 pass.

## Hypothesis

The local C10h/C10J AnyEdit failures may be local integration/transplant failures rather than AnyEdit-method failures. A source-faithful official-upstream AnyEdit session should be able to show whether AnyEdit can actively edit easy C10 controls and, conditionally, whether it rescues the hard project-coined multi-word value class.

Falsifiable claim:

> In an upstream-compatible environment using official AnyEdit algorithm modules, official AnyEdit can recover C10 A1/A2 held-out behavior and, in the same source-faithful session, lift hard A7 project-coined multi-word held-out full-sequence behavior to a usable in-weight read level.

## F1 Decision Meaning

- **PASS on A7 after controls pass:** official-upstream AnyEdit has a C10 mechanism-rescue lead. If the run is on Qwen2.5-7B, this is not C10 closure; it licenses faithful 3B/Q4/CPU follow-up.
- **A1/A2 PASS but A7 FAIL:** source-faithful official AnyEdit did not rescue the hard C10 class under this setup. C10 remains OPEN/BLOCKING and may move toward `not-ready` for in-weight project-coined multi-word values.
- **A1/A2 FAIL or stock anchor FAIL:** no A7 interpretation; diagnose environment/source/data-adapter only.
- **INVALID:** no science update.

Bounded hybrid remains an engineering escape hatch only, not an F1 closure, unless the spec/operator contract changes.

## Bias Boundary

Prior local-transplant results are used only as failure-mode context:

- local C10h/C10J wrappers can pass token/no-op gates while active controls fail;
- local wrapper failures do not count against official upstream AnyEdit;
- hard A7 can be run for efficiency in the same loaded session, but its result is interpretable only if stock source anchor and A1/A2 controls pass.

## Stage Covered By This Prereg

This prereg covers the full official-upstream C10K session: Stage 0 source-faithfulness anchor, Stage 1 A1/A2 controls, and Stage 2 conditional hard A7.

### Stage 0 - Environment, Source, and Stock Anchor

1. Do not rent A100-class hardware without explicit operator sign-off for that action. The operator has expressed willingness to spend GPU money, but the exact rental action remains a separate go/no-go.
2. Create an isolated upstream-compatible environment. Prefer A100 80GB or equivalent if Qwen2.5-7B/Llama3-8B is used because upstream README states `One A100 80G GPU` and the official runner loads models without local fp16/VRAM edits.
3. Resolve the README/model dependency contradiction before science runs. The README pins `transformers==4.23.1`, but shipped Qwen2.5 and Llama3 configs require later transformers releases. Record whether the README is stale, what version actually loads the selected shipped config, and how that was determined. Guessing caps the run at INVALID/HALTED.
4. Run the zero-cost model-config desk check before any rental: determine whether upstream ships a Qwen2.5-3B config. Preference order is **Qwen2.5-3B if shipped > smallest faithful shipped config > Qwen2.5-7B/A100**. If no 3B config ships, record that as an attribution limitation before any 7B run. If no shipped config can run under the README-pinned dependency set, record that contradiction and require Claude advisor approval before proceeding to C10 data.
5. Run upstream import/CLI smoke until `python3 -m experiments.evaluate_uns --help` or equivalent import path succeeds.
6. Run a stock-upstream reproduction/anchor before any C10 adapter: execute the official runner on an upstream-supported stock dataset/config at small size, save raw output, and compare to upstream-reported metric if available. If no published expected number is available, label this a source-run anchor rather than a reproduction and require Claude advisor approval before C10 interpretation.
7. Record upstream commit, remote URL, hparams file, package versions, GPU type, model revision, and all dependency deviations.
8. Method-port packet must include `vram_patches_applied: false` for PASS. Local 24GB tricks such as alternate eigensolvers, diagonal-add shortcuts, or deletion/reordering of projectors invalidate source-faithfulness unless preregistered and advisor-reviewed as a separate non-official port.

### Stage 1 - C10 A1/A2 Easy Controls

1. Create C10 A1/A2 `UnKE`-format data only. The adapter may write `data/UnKE/final_data_v3.json` for the isolated run, but must not change upstream algorithm modules.
2. Round-trip at least one stock UnKE item and two C10 A1/A2 items through the adapter/tokenizer before GPU run, recording prompts, answers, token IDs, and decoded text.
3. Run the official upstream runner or a minimal launcher that imports official upstream algorithm modules unchanged.
4. Use `alg_name=AlphaEdit_ARE` first because it is the official AnyEdit + AlphaEdit path closest to the local AlphaEdit/MEMIT line. `MEMIT_ARE` may be a secondary diagnostic only.
5. Preserve upstream metrics/output fields, and independently compute the C10 binding metric (`para_full` full-sequence exact match plus first-token/conditional diagnostics) from the same generated outputs.
6. Emit per-unit records with subject, target, canonical prediction, paraphrase prediction, exact-match booleans, token IDs, locality/bystander outputs, and any available active trace.

### Stage 2 - Conditional Hard A7 In Same Session

1. Create C10 hard A7 `UnKE`-format data in the same adapter style, using project-coined multi-word semantic values from the C10 line.
2. Round-trip A7 records before GPU run: prompt, paraphrase, answer, answer token IDs, decoded answer, and any `sub_question`/bystander prompts.
3. Run A7 in the same upstream environment/session for efficiency.
4. Interpret A7 only if Stage 0 stock anchor passes and Stage 1 A1/A2 controls pass. If either control gate fails, A7 output is diagnostic-only and cannot support a C10 claim.

No Q4, CPU-serving, or 3B-transfer claim is licensed by this prereg.

## Binding Metrics

Primary easy-control metric:

- A1 held-out paraphrase full-sequence exact match (`para_full`) >= 80%.
- A2 held-out paraphrase full-sequence exact match (`para_full`) >= 80%.

Primary hard C10 metric, interpreted only if controls pass:

- A7 held-out paraphrase full-sequence exact match (`para_full`) >= 85% for a C10 mechanism-rescue lead. The A7 bar is intentionally higher than the 80% easy-control floor because A7 is the hard rescue claim; it needs a clear usability margin, while A1/A2 are only port-liveness controls.

Full-sequence exact match is the read-correctness metric. Canonical prompt fit, first-token accuracy, conditional P(full|first), target probability, logit deltas, and update norms are diagnostics. Locality/bystander metric is upstream `sub_question`/neighborhood generation exact-match or semantic-preservation score when available, plus the C10 `described as` bystander prompt family; a drop greater than 5.0 points from pre-edit to post-edit caps the result at PARTIAL unless advisor accepts a source-faithful upstream metric as the only available locality read.

## PASS / PARTIAL / FAIL / INVALID Thresholds

- **PASS - OFFICIAL_A7_MECHANISM_RESCUE_LEAD:** all of the following hold:
  - Stage 0 source/environment packet complete;
  - stock-upstream reproduction/anchor gate passes or receives explicit Claude approval as sufficient source-faithfulness anchor;
  - dependency/model version choice is documented rather than guessed;
  - official upstream algorithm modules are unchanged, or every deviation is declared and advisor-reviewed;
  - `vram_patches_applied: false` in the method-port packet;
  - upstream metrics are preserved and C10 metrics are computed from the same raw generations;
  - A1 and A2 `para_full >= 80%` on held-out paraphrases;
  - A7 `para_full >= 85%` on held-out paraphrases;
  - per-unit records exist and `tools/experiment_gate.py check-result` does not refuse stats for aggregate-only output;
  - method-port packet passes `tools/experiment_gate.py audit-method-port`;
  - locality/bystander degradation is not materially worse than the preregistered threshold;
  - no-op/inertness or equivalent source-faithful null edit passes;
  - Claude advisor returns `PROCEED`, or all `FIX-FIRST` items are resolved.
- **PARTIAL - ACTIVE_BUT_NOT_RESCUED:** stock anchor and A1/A2 pass, but A7 is nonzero below 85%, locality is materially degraded, stats/method packet is incomplete, or advisor has unresolved `FIX-FIRST`.
- **FAIL - OFFICIAL_A7_NOT_RESCUED:** stock anchor and A1/A2 pass, but A7 `para_full < 85%` after one localized environment/data-adapter fix and same-gate rerun, with no unresolved source-faithfulness failure explaining the miss.
- **HALTED - CONTROLS_NOT_RECOVERED:** stock anchor passes but A1/A2 controls fail; do not interpret A7.
- **INVALID:** upstream source/commit not recorded; algorithm modules modified without preregistered deviation; missing saved JSON; aggregate-only result; missing per-unit records; hard A7 interpreted before controls pass; environment smoke fails before active edit; model/hparams do not match declared scope.

## Power / MDE

This is a scoped method-gate and mechanism-rescue test, not a broad reliability estimate. Planned sampling unit is per held-out prompt per edited item, clustered by subject/order. Use the existing 24 fictional subjects for A1, A2, and A7 if upstream runtime allows. A smaller run is diagnostic only and cannot produce PASS.

If A1/A2 land in `[80%, 90%)` or A7 lands in `[85%, 90%)`, rerun the corresponding gate once under the same prereg before declaring PASS. A later 3B/Q4/CPU closure addendum must run `tools/power.py` or explicitly justify a scoped pilot.

## Confounders And Controls

| Confounder | How it fakes a result | Control |
|---|---|---|
| Local transplant artifact | A local wrapper failure is mistaken for AnyEdit failure | Use official upstream algorithm modules unchanged; declare adapter-only boundary |
| Environment drift | Modern deps change upstream behavior | Isolated env, exact package versions, stock-upstream anchor before C10 data |
| README/model contradiction | Stale README pin creates false faithfulness | Resolve transformers/model compatibility before run; guess = INVALID/HALTED |
| Hardware workaround | VRAM patches change the method | `vram_patches_applied: false` required for PASS |
| Model mismatch | 7B result is overread as 3B/Q4/CPU closure | 7B PASS is mechanism lead only; C10 closure requires faithful 3B/hard A7/Q4/CPU follow-up |
| Model-size attribution | A 7B PASS is mistaken for proof that local 3B failed only due transplant | Prefer upstream 3B if shipped; if forced to 7B, record that faithful-upstream-on-3B remains open |
| Dataset adapter bug | Prompts/answers malformed in upstream format | Save data JSON, token IDs, decoded text; round-trip stock and C10 records |
| Upstream reproduction failure | C10 run tests broken env rather than AnyEdit | Stock-upstream reproduction/anchor gate before C10 adapter |
| Canonical-only fit | Trained prompt improves while held-out read fails | Binding metric is held-out `para_full`; canonical is diagnostic |
| Under-editing as locality | Edit barely applies but locality is high | Require behavior floor plus active trace/update/logit deltas |
| Over-editing | Behavior gained by damaging unrelated prompts | Record upstream `sub_question`/neighborhood and C10 bystanders; cap at PARTIAL if >5.0 point drop |
| Aggregate-only output | Percentages hide denominator/survivorship | Emit per-unit records and run `check-result` |
| Hard-case leakage | A7 interpreted before controls pass | A7 output diagnostic-only unless stock anchor and A1/A2 pass |

## LAW / Inertness Gates

- Do not edit local `memit_dry_run/memit` science-path primitives for this addendum.
- Do not modify upstream AnyEdit algorithm modules unless a preregistered deviation and Claude advisor review approve it.
- Source-read before run: `experiments/evaluate_uns.py`, `AlphaEdit_ARE/*`, selected hparams, dataset adapter.
- Null/no-op or equivalent inertness check must record no material behavior change and no unintended parameter update in the null path.
- One-fix boundary: after a Stage 1/2 failure, exactly one localized environment/data-adapter compatibility fix is allowed, then rerun the same gate and halt with diagnostic if it still fails.

## Method-Port Faithfulness

Required packet: `logs/c10k_anyedit_official_upstream_method_port_packet.json`

Required fields:

- upstream repository and commit;
- remote URL;
- exact algorithm path (`AlphaEdit_ARE` primary);
- exact hparams file and content hash;
- model ID and revision;
- GPU type and memory;
- Python/package versions;
- dependency/model compatibility justification;
- Qwen2.5-3B config desk-check result;
- declared deviations from upstream README requirements;
- `vram_patches_applied` (must be `false` for PASS);
- whether upstream algorithm files were modified (`false` required for PASS unless addendum-reviewed);
- stock-upstream anchor path and verdict, explicitly one of `reproduction`, `source_run_anchor`, or `failed_anchor`;
- C10 data adapter path and first-record readback;
- active trace fields available from upstream path: token IDs, answer/loss masks, lookup/edit positions, target norms, delta/update norms, logit deltas, behavior;
- per-unit A1/A2/A7 records;
- `a7_interpretable: true` only if stock anchor and A1/A2 pass.

## Planned Artifacts

- Prereg: `docs/C10K_ANYEDIT_OFFICIAL_UPSTREAM_PREREG.md`
- Environment/source packet: `logs/c10k_anyedit_official_upstream_env.json`
- Qwen2.5-3B config desk check: `logs/c10k_anyedit_3b_config_desk_check.log`
- Stock-upstream reproduction/anchor output: `results/c10k_anyedit_stock_upstream_anchor.json`
- C10 upstream data adapter: `results/c10k_anyedit_unke_c10_data.json`
- Run log: `logs/c10k_anyedit_official_upstream.log`
- Raw upstream output: `results/c10k_anyedit_official_upstream_raw.json`
- Normalized per-unit result: `results/c10k_anyedit_official_upstream_c10.json`
- Stats report: `logs/experiment_gate/c10k_anyedit_official_upstream_c10_stats.json`
- Method-port packet: `logs/c10k_anyedit_official_upstream_method_port_packet.json`
- Advisor review: `logs/claude_c10k_anyedit_official_upstream_prereg_review.md`

## Advisor / Cross-Family Review

Required review points:

1. Claude advisor review of this prereg before environment build or GPU run.
2. Explicit operator sign-off before renting A100-class hardware.
3. Claude advisor review after any Stage 0/1/2 failure that would require changing model, hparams, dependencies, or algorithm path.
4. Claude advisor review before any 3B/Q4/CPU closure addendum.
5. Claude advisor review before any verdict/CORPUS write if a later closeout occurs.

Review is input, not evidence. Saved artifacts and preregistered criteria bind.

## Abort Criteria

Abort and write a diagnostic if any of the following occur:

- official upstream repo/commit cannot be recorded;
- upstream command/import cannot run in the isolated env;
- the run requires modifying upstream algorithm modules before controls;
- stock-upstream reproduction/anchor gate fails before C10 adapter;
- the actual compatible transformers/model version cannot be justified;
- C10 data adapter cannot be read back or tokenized as intended;
- selected model cannot fit on selected hardware without unapproved source/VRAM modifications;
- output is aggregate-only and cannot be normalized to per-unit records;
- A7 is interpreted before stock anchor and A1/A2 PASS;
- any result is used to recommend bounded hybrid as F1 closure without explicit operator/spec acceptance.

## Outcome Consequence Map

- **7B or other upstream large-model A7 PASS after controls pass:** C10 mechanism-rescue lead only. It does not close C10 because the fixed target was Qwen2.5-3B/Q4/CPU; closure still requires faithful 3B route, hard A7 behavior, and downstream serving checks. It also leaves the attribution question open: local 3B failure may have been transplant-related, model-size-related, or both.
- **Official upstream A7 FAIL after stock anchor and A1/A2 pass:** strong negative evidence against this AnyEdit path for C10; C10 remains OPEN/BLOCKING and may move toward `not-ready` for in-weight project-coined multi-word values.
- **Stock-upstream reproduction/anchor FAIL:** no AnyEdit science update; environment/source-faithfulness failure only.
- **Local adapter/wrapper FAIL before official algorithm active behavior:** no method evidence; fix once or halt.
