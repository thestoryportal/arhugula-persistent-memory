VERDICT: FIX-FIRST

`S` = `docs/LABVIZ_V2_SPEC.md`; `B` = `results/labviz_v2_codex_brief.md`. No files changed; no model, tokenizer or torch loaded. No `-o` path was supplied, so the review is returned here.

1. **BLOCKING — Non-C10 badges contradict the role contract.** **S:283,442–470; B:81.** R5 requires its recorded `CHARACTERIZATION` badge, but every non-C10 configuration reaches “role not in table; no label chip.” **Exact change:** “The C10 role table governs C10 cards only. Non-C10 cards display their own sourced label/status and measure, without the C10 goal.” Add R5 and G6.1 badge tests.

2. **BLOCKING — Gate fixtures still require nonexistent data.** **S:530,542,557; B:112–113.** Five C10U UNDERFIT arm readings have no `.gates`; only **49**, not 84, booleans exist across twelve arm readings. C10W’s prescribed `.u.<arm>` also fails for `A7_canon`: that key is absent; the reader uses `.u.A7_coined_coined` for paired MMLU (`c10w_oracle_read.py:326–328`). **Exact change:** require consistency for every *present* boolean; separately test all five missing-gate readings for no glyph/no invented outcome. Specify the canonical control’s actual U reference.

3. **BLOCKING — The brief retains execution contradictions.** **B:39–50,92,100,130.** Tests must invoke jq, but test 19 forbids child-process calls in **all** `tools/labviz/*.py`, including the required test module. “Nothing else” may change, yet browser installation and Matplotlib explicitly write under `/private/tmp`, and WebKit installation ordinarily writes its browser cache elsewhere. **Exact change:** restrict the subprocess prohibition to the production builder and its runtime dependencies; allow jq in tests. Explicitly allow the two named temporary directories and set `PLAYWRIGHT_BROWSERS_PATH` inside the browser-review directory.

4. **SHOULD — Leaf equality does not validate derived meaning.** **S:662,722–734,771–783,1005; B:100–101.** The example’s `scale.max=55.42212677001953` resolves correctly but is already smaller than C10V B0·A2’s **55.45940399169922**. Its configured-layer derivation omits the tested layer from `inputs`; derived context examples omit the complete edge chain required by §11.2. **Exact change:** compute `scale.max` over the declared eligible population, include every derivation operand, and supply the complete context-edge dependencies. Test an over-maximum control card and broken derivation inputs.

5. **SHOULD — Phase-1 requirements still lack explicit tests.** **S:183,567,570,643–649; B:98–130.** Add fixtures for hparams/model-revision mismatch, predicted/injection values excluded from recorded scales, newest-written-card selection, recorded-event ordering, and unchanged-output mtimes/picture-render calls. Byte-identical output alone does not verify write-on-change. Also test G6.1/R5 record contents, beyond the vocabulary blacklist. **Codex cannot yet implement the entire contract without resolving contradictions and supplying missing acceptance cases.**

6. **SHOULD — Readability measurement conflates text boxes with font size.** **S:402; B:93.** Range/line-box or glyph-box height is not rendered font size; leading and font metrics can accept undersized text or reject compliant text. **Exact change:** measure computed font size multiplied by rendered transform scale, with boxes used for clipping/layout checks. Include 12px text with generous leading and transformed SVG fixtures.

7. **NIT — Two new claims and one retained caption need correction.** **S:258:** parenthesize `(.oracle_p1_A7_configuration|{label,gates}), .p1_eval.sha256`; the current command prints `null` for the hash. **S:281:** CORPUS/22’s header names both the predictor file and `d1_concentration_sweep_result*.json`; define header-glob handling instead of claiming only the predictor is named. **S:474,502:** replace LEAD’s “not yet repeated” with “promising under this test; see replication,” since the binding mint1 result was replicated.

**Original BLOCKING findings:** A1/V6 are substantially repaired but remain partial on derived validation (#4), at S:658–814/B:100. A2/V5 close at S:463,595–596/B:107,119. A3’s registry parsing, decision selection and tie rules close at S:1002–1029/B:122; its derived-example inconsistency remains #4. A4 remains partial (#1–2), despite the supplied tables at S:442–557/B:109–113. A5 and V7 remain partial (#3); report location, timestamps, served-card location and content-region scope are fixed at B:38–46,123,130. A6 closes at S:183,203–212/B:115–118. V1’s C10 arm-role protection closes at S:442–463/B:103–105, but its new universal rule causes #1. V2 closes at S:138–139/B:106. V3 closes at S:182,630/B:121. V4 closes at S:514–516/B:113.

**Three partial rejections:** All hold. V1 needs no separate `oracle` role if the mandatory non-routing `.class` remains visible. V9 reasonably uses measured performance acceptance instead of flaky unit timing; S:939 still requires meeting the budget. V14 correctly rejects direct comparison of float32 training hashes with float16 sandbox tensors.

**Non-C10 colours:** S:493–495 maps characterization/screening labels to `characterization` and configuration names to `not-a-verdict`; none maps to green `pass`. These choices are appropriate. Add a rendered-colour assertion so table equality cannot conceal green styling on another class.

Read-only checks verified all **35 existing JSON-source example leaves**, **12 document quotes**, **12 source hashes**, and **71 recorded locality booleans**. Seven example leaves depend on uncreated Lab View tables. Browser/build behavior remains **UNVERIFIED**.

| # | New/changed claim | Source checked | Result |
|---|---|---|---|
| 1 | B correlation is −0.3162875387734472 | `results/c10v_layerpick/run.json:.readings.B.spearman_G_edge` | OK |
| 2 | −0.47912964570281436 belongs to B0 | Same file, `.readings.B0.spearman_G_edge` | OK |
| 3 | Reading binds exact pass1 bytes | Same file, `.pass_sha256.pass1`; SHA-256 of `pass1.json` | OK: `bf8f162a…119f` |
| 4 | Full layer-8 write precision | `results/c10v_layerpick/pass1.json:.recipes.B.delta_norms.A7_coined_coined["8"].delta_norm` | OK: `16.31455421447754` |
| 5 | Full relative-write precision | Same object, `.relative_delta_norm` | OK: `0.13654435355029926` |
| 6 | Exact example timestamp | Same file, `.when_utc` | OK: `2026-10-08T03:32:38.191318+00:00` |
| 7 | Exact selection margin | `results/c10v_layerpick/step0.json:.winning_margins[0][0]` | OK: `0.01560226080429905` |
| 8 | Example scale maximum | `pass1.json:.recipes.B0.delta_norms.A2_coherent2["8"].delta_norm` | **WRONG maximum:** `55.45940399169922` exceeds example’s `55.42212677001953` |
| 9 | Binding C10U mint1 label | `results/c10u_mint2/r3_read_after_replicateF.json:.F.arms.mint1_s0.label` | OK: `LEAD` |
| 10 | Other readers disagree | `r3_read_after_v2.json` and `r3_read_after_frozen.json`, same path | OK: both `LEAD-NOT-REPLICATED` |
| 11 | Replicates share count, not identity | `r3/F_r{0,1}_mint1_s0.json`: `.block,.kind,.seed,.replicate,.arm.para_full_binding_n` | OK: F/mint1/0, replicate 0 versus 1, both 46 |
| 12 | C10U binding authority citation | `CORPUS/54_C10U_MINT2.md:5` | OK: explicitly names replicateF |
| 13 | Every C10U arm has seven gates | Binding reader `.F.arms`, `.V2.arms` | **WRONG:** five lack gates; remaining 49 booleans recompute exactly |
| 14 | C10V gate table | `pass1.json` inputs against `run.json:.readings.*.locality_gates` | OK: all 15 booleans |
| 15 | C10W interim label/gates | `p1_20261007T223707_598959Z/interim_reader_configuration_v2.json:.oracle_p1_A7_configuration` | OK: `PARTIAL-CEILING-LOCALITY-COST`; only G4 false |
| 16 | C10W interim join hash | Same file, `.p1_eval.sha256`; SHA-256 of adjacent `eval.json` | OK: `f8886427…d60f` |
| 17 | Added jq command extracts that hash | S:258, executed as written | **WRONG:** prints `null` |
| 18 | C10W closedform reference | P1 `eval.json:.recipes.closedform.arms.A7_coined_coined.locality_described_as` | OK: `87.56` |
| 19 | C10W gate arithmetic | P1 eval inputs versus interim `.gates` | OK: all seven booleans |
| 20 | Canonical-control U path | P1 `eval.json:.u.A7_canon` | **ABSENT:** use reader’s A7 U reference |
| 21 | Training hashes concern float32 base | P1 `train/A7_coined_coined_s0_r16.json:.dtype,.frozen_parameter_hashes_before,.frozen_parameter_hashes_after`; trainer:168 | OK: float32, 434 hashes each, equal |
| 22 | Band hashes are restore checks | P1 eval `.base_band_hash,.final_band_hash,.recipes[].band_after_hash`; reader:313,319 | OK: all equal |
| 23 | Seal audit contains 22 rows | `step0_20261007T223638_531381Z/seal_audit.json:.rows[].id` | OK: T01–T20, R1, R2 |
| 24 | Generated-answer alignment | P1 oracle A7 `.extra.generated` versus recipe detail and recorded PTEST | OK: all 72 entries align |
| 25 | “Vindex Vaskul,” is scored full | Same generated array, `[1].text,.full` | OK: `" Vindex Vaskul,"`, true |
| 26 | P2 halted without verdict | `p2_20261008T034226_086980Z/HALT.json`; directory inventory | OK: `p2-eval`, evaluation-process failure, no verdict; six train JSONs |
| 27 | G6.1 inventory | `results/g6_scale_n_result.json:.config,.records,.rungs` | OK: N=100, 50 entities, 100 records, three rungs |
| 28 | D1 inventory numbers | `results/d1_concentration_sweep_result.json` | OK: capital-axis gap 0, total-axis gap 50, N=50 |
| 29 | D1 header names only predictor | `CORPUS/22_D1_CAPACITY_LAW.md:3` | **WRONG:** also names concentration-sweep glob |
| 30 | R5 label/text inventory | `results/r5_paraphrase_robustness.json:.label,.templates,.rows.NOVEL_single[0]` | OK: CHARACTERIZATION; recorded templates, hits and answers |
| 31 | Registry row counts | `docs/EXPERIMENT_REGISTRY.md`; `docs/experiment_registry.json` | OK: 54 markdown rows; field counts 10×36, 9×16, 11×1, 12×1; JSON 20 |
| 32 | Launcher identity | SHA-256 of `tools/labviz_serve.sh` | OK: `c90afb9c…a05a4b` |
| 33 | T-branch quotation | `docs/t_branch_decision_document_v1_4.md:35` | OK: “5/5 consistency PASS” |
| 34 | Non-C10 label mappings | R2/R3/R5/R9/R13/R15 JSON label fields versus S:493–495 | OK: characterization or configuration-name classes; no `pass` |

🌱 graft reported ~47,493 tokens saved (~$0.03), 1 successful call.