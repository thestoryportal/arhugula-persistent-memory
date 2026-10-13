VERDICT: FIX-FIRST

`S` = `docs/LABVIZ_V2_SPEC.md`; `B` = `results/labviz_v2_codex_brief.md`. Reviewed the requested `HEAD~1` diff and underlying records. No files changed; no model, tokenizer or torch loaded. No `-o` pathname was supplied, so the review follows here.

1. **BLOCKING — R2-3’s temporary-file boundary remains incomplete.** **B:44–51,132.** The browser caches and jq exception are fixed, but the required test command sets no `TMPDIR`. Existing tests use unqualified `tempfile.TemporaryDirectory()` at `tools/labviz/test_labviz.py:202,224,269,280`. This session’s `TMPDIR` is `/var/folders/p7/s31_tv0s2wd81chns8v7gsyw0000gn/T/`, outside both allowed scratch directories. **Exact change:** precreate `/private/tmp/labviz-review/test-tmp/` and add `TMPDIR=/private/tmp/labviz-review/test-tmp` to the required test command. Assert fixture paths stay there. This repairs the remaining execution contradiction without broadening write permission.

2. **BLOCKING — The new timestamp-only ordering requires unrecorded timestamps.** **S:649–655; B:137.** C10W training `.losses[]` contains only `{step,loss}`; `.step_seconds[]` contains durations. The trainer records no absolute loss-event timestamps (`c10w_oracle_train.py:198–211`). Terminal markers can also be untimestamped: `results/c10w_oracle_logs/p1-eval.log:2` is just `STAGE_EXIT=0`. **Exact change:** “Sort timestamped events by normalized UTC, then source path and source position. Display untimestamped events separately in source/step order, labelled ‘time not recorded’; do not infer absolute times from durations, filenames or mtimes.” Add real loss/marker fixtures, equivalent timezone timestamps and an array-index tie-breaker.

3. **SHOULD — The new population pointer needs an explicit schema exception.** **S:666–671,799–802,829–834; B:101,133.** `scale.max.population` contains `{src:{file,path}}`, without the `value` required by a JSON-source leaf. Meanwhile, `inputs` contains only the winning observation, although the rule requires every operand. The intended population mechanism is understandable, but the literal validation contracts disagree. **Exact change:** explicitly define population references as schema metadata; population-based derivations omit `inputs`, resolve the complete operand list, validate its leaves and recompute exclusively from that list. Test the example itself, a removed population member and an incorrect maximum.

4. **SHOULD — Acceptance coverage remains incomplete.** **S:364,562,580; B:115,131,139.** Added tests 21–26 address the previous omissions, but explicit cases remain missing for changed answers or different fact populations in Compare; missing/non-finite gate inputs suppressing reference lines; and saved-picture text meeting 13px at 600px width. **Exact change:** add those fixtures and checks. Also make the D1 header-glob test assert the resulting documentary context, not merely four filesystem matches: D1 has no registry experiment row (**S:286,1036–1038**).

5. **NIT — Canonical-control citation points to the ordinary configuration.** **S:548.** `c10w_oracle_read.py:361` evaluates ordinary A7. The canonical control actually receives the same references at **:397–403**. **Exact change:** cite `:403` for the canonical-control claim; retain `:361` for ordinary A7. The prescribed reference values are correct.

The blocker audit below distinguishes implementation instructions from fold-map assertions. **Codex cannot yet satisfy the entire brief without resolving findings 1–2; finding 3 should be settled before writing the verifier.**

| Original BLOCKING finding | Closure in the actual files |
|---|---|
| Astra A1; advisor V6 — leaf contract | Substantially repaired at **S:664–675,829–834; B:101**; new population exception remains finding 3. |
| Astra A2; advisor V5 — statistic/joins | Closed: **S:469,601–602; B:108,121**. |
| Astra A3 — context parsing | Original parsing/decision/tie defects closed: **S:989,1022–1042; B:124**. D1 acceptance gap is finding 4. |
| Astra A4 — labels/gates | Closed: **S:446–563; B:103–115**; all 71 present booleans independently recomputed. |
| Astra A5; advisor V7 — execution/display contradictions | Report, determinism, served cards, vocabulary scope and draft tables repaired: **S:40–42,403,616,974; B:36–51,91,132**. Temporary-fixture exception remains finding 1. |
| Astra A6 — stimulus | Closed: **S:183,203–212; B:117–120,135**. |
| Advisor V1 — roles/oracle status | Closed: **S:446–469; B:104–110**. |
| Advisor V2 — binding C10U reader | Closed: **S:138–139,475; B:60,107**. |
| Advisor V3 — frozen/restore hashes | Closed: **S:112,636; B:123**. |
| Advisor V4 — invented gate verdicts | Closed: **S:520–563; B:113–115**. |
| Delta R2-1 — non-C10 badges | Closed: **S:446,468; B:82,110**. |
| Delta R2-2 — nonexistent gate data | Closed: **S:536,548,563; B:114–115**. |
| Delta R2-3 — execution contradictions | jq and browser-cache portions closed at **B:36,44,93,132**; temporary test fixtures remain open. |

**All three partial rejections hold.** V1 needs no separate `oracle` role while the non-routing `.class` remains mandatory (**S:467,504**). V9 reasonably substitutes measured acceptance for flaky timing assertions; meeting the budget still gates completion (**S:42,959**). V14 correctly rejects direct comparison of float32 training hashes with float16 sandbox tensors (**S:1152; trainer:168**).

**Non-C10 colours are appropriate:** characterization/screening labels use `characterization`; configuration names use `not-a-verdict`, without chips (**S:499–501**). None maps to green. **B:111** now tests rendered colours; browser behaviour remains UNVERIFIED.

Claim checks were read-only Python/JSON, source inspection and jq; no build or browser tests ran.

| # | New/changed concrete claim | Source checked | Result |
|---|---|---|---|
| 1 | G6.1 status text | `docs/EXPERIMENT_REGISTRY.md:13` | OK: `SPLIT (cross-entity FALSIFIED)` |
| 2 | G6.1 contents | `results/g6_scale_n_result.json:.records,.rungs` | OK: 100 records, 3 rungs |
| 3 | R5 badge | `results/r5_paraphrase_robustness.json:.label` | OK: `CHARACTERIZATION` |
| 4 | R5 four arms | Same file, `.arms` | OK: NOVEL_single, PRIOR_single, PRIOR_multi_same, PRIOR_multi_para |
| 5 | R5 recorded questions/answers | Same file, `.templates.P_test,.rows.NOVEL_single[0]` | OK: three templates; `ptest_hits` and `ptest_obs` present |
| 6 | Twelve C10U readings | `results/c10u_mint2/r3_read_after_replicateF.json:.F.arms,.V2.arms` | OK: 6 + 6 |
| 7 | C10U gate population | Same objects, present `.gates` | OK: 7 readings × 7 = 49 |
| 8 | Five readings lack gates | Same file | OK: F modifier_s0/s1/s2; V2 mint2_s1/s2 |
| 9 | C10U binding LEAD | Same file, `.F.arms.mint1_s0.label` | OK: `LEAD` |
| 10 | C10W U-reference keys | `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:.u` | OK: A1_single, A2_coherent2, A7_coined_coined, A7_shuf; no A7_canon |
| 11 | Canonical reference citation | `c10w_oracle_read.py:361,397–403` | Value correct; canonical call is at :403 |
| 12 | Present gate arithmetic | C10V reading/pass1; C10U reading/r0 records; C10W interim/eval | OK: all 15 + 49 + 7 booleans agree |
| 13 | Absolute-norm inventory | Recursive numeric `delta_norm` beneath `delta_norms`, excluding Lab View/chat exports | OK: 1,183 values in 80 files |
| 14 | Shared maximum | `results/c10h_anyedit_pilot.json:.recipes.anyedit_window1.delta_norms.A7_coined_coined["8"].delta_norm` | OK: `113.7967300415039`, scan maximum |
| 15 | C10V B0·A2 exceeds former scale | `results/c10v_layerpick/pass1.json:.recipes.B0.delta_norms.A2_coherent2["8"].delta_norm` | OK: `55.45940399169922` |
| 16 | D1 inventory | `results/d1_*.json` | OK: 18 files |
| 17 | D1 header glob | `CORPUS/22_D1_CAPACITY_LAW.md:3`; `results/d1_concentration_sweep_result*.json` | OK: 4 matches |
| 18 | D1 header coverage | Same header, plus predictor-map path | OK: 5 named files; 13 others |
| 19 | Corrected jq precedence | Executed **S:258** filter | OK: emits configuration object and non-null `f8886427…bd60f` hash |
| 20 | C10W reading/eval binding | Interim `.p1_eval.sha256`; adjacent eval bytes | OK: SHA-256 matches |
| 21 | Example JSON values | Every existing JSON-source example leaf | OK: 35/35 exact |
| 22 | Expanded example quotations | Every existing document-source example leaf | OK: 19/19 |
| 23 | Expanded example hashes | Existing files in example `sources[]` | OK: 13/13 |
| 24 | Derived context chain | Registry :60 → overlay :22 → F1 :71 / e2e :14 | OK: cited decision, section, condition and layer present |
| 25 | Label-table completeness | Enumerated label/final_label/base_label/count_label/direction strings | OK: all 27 recorded strings represented |
| 26 | Training observations | P1 `train/*.json:.losses,.step_seconds` | OK: each has 40 losses and 400 durations; no absolute event timestamps |
| 27 | Timestamped terminal markers | `results/c10w_oracle_logs/p1-eval.log:2` | Counterexample: untimestamped `STAGE_EXIT=0` |
| 28 | Allowed test scratch paths | **B:51**, existing `TemporaryDirectory()` calls, current `TMPDIR` | FAIL: default fixture directory lies outside allowlist |

🌱 graft reported ~84,345 tokens saved (~$0.05), 1 successful call.