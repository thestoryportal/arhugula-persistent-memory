VERDICT: FIX-FIRST

`S` = `docs/LABVIZ_V2_SPEC.md`; `B` = `results/labviz_v2_codex_brief.md`. Reviewed the requested `HEAD~1` diff and underlying files. No files changed; no model, tokenizer or torch loaded. No `-o` pathname was supplied, so the review is returned here.

1. **BLOCKING — New test 27 requires a correct implementation to fail.** **B:141; S:364.** The required calculation gives **9 × 600 / (72 × 5.1) = 14.705882px**, above the 13px minimum. Thus “9pt text in a 5.1-inch figure … fails” contradicts the acceptance formula. The cited renderer uses that figure width and saves without tight-bbox cropping (`tools/labviz/render.py:61,108–109`). **Exact change:** “Use an uncropped 5.1-inch fixture: 6pt text fails at 9.803922px; 9pt text passes at 14.705882px.” Existing 6pt text occurs at `render.py:105`. Preserve the 600px measurement width.

2. **SHOULD — Two Phase-1 behaviors still lack explicit acceptance cases.** **S:352,643; B:124,128–142.** URL reload tests do not establish that selecting a run carries that selection into another view. Likewise, the static wiring requirement includes an animation labelled “diagram, not recorded activity,” but no listed test asserts that distinction. **Exact change:** add browser cases that select a run in Runs, navigate to Inside the model and Compare, and assert the same ID; enable the static animation and assert its disclaimer remains visible. Existing leaf, colouring and screenshot checks do not establish these behaviors.

3. **NIT — The new D1 paragraph corrupts its cited fingerprint and retains an inconsistent introduction.** **S:1034–1036.** The quoted `⟨D-D1-1db8d819⟩` does not occur in `CORPUS/22_D1_CAPACITY_LAW.md:3`; the actual token is `⟨D-D1-1@0db8d819⟩`. Also, “first rule that yields exactly one experiment wins” conflicts with rule 2 deliberately returning documentary context without an experiment. **Exact change:** restore the token and replace the introduction with “Apply in order; stop at the first uniquely resolved context, including a documentary context under rule 2. Ambiguous matches remain unknown.”

**All historical BLOCKING findings are closed in the actual files**, independently of the fold-map assertions. The new blocker above prevents unconditional test-first handoff.

| Historical blocker | Closure in current spec/brief |
|---|---|
| Astra A1; advisor V6 — leaf/schema/precision | **Closed:** S:664–675,827–832; B:101,134. Population exception is now explicit. |
| Astra A2; advisor V5 — B/B0 statistic and joins | **Closed:** S:469,601–602; B:108,122. |
| Astra A3 — context parsing, decisions, ties | **Closed:** S:1020–1040; B:125,142. Minor new wording defect is finding 3. |
| Astra A4 — label/gate contracts | **Closed:** S:447–563; B:103–116. |
| Astra A5; advisor V7 — execution/display contradictions | **Closed:** S:40–42,616; B:32–51,126,133. Report, determinism, served paths and vocabulary scope specified. |
| Astra A6 — recorded stimulus and ordering | **Closed:** S:203–212; B:118–121,136. |
| Advisor V1 — roles/oracle qualification | **Closed:** S:447–469; B:104–110. |
| Advisor V2 — binding C10U reader | **Closed:** S:138–139,475; B:60,107. |
| Advisor V3 — frozen versus restored tensors | **Closed:** S:112,122,636; B:124. |
| Advisor V4 — invented gate verdicts/reference | **Closed:** S:520–563; B:112–116. |
| Delta R2-1 — non-C10 badges | **Closed:** S:468; B:110. |
| Delta R2-2 — nonexistent gates/U reference | **Closed:** S:536,548; B:114–116. |
| Delta R2-3 — jq exception/scratch boundaries | **Closed:** B:36,44,51,133. |
| Delta2 R3-1 — test temporary directory | **Closed:** B:44,51 explicitly precreates and sets `TMPDIR`, with an assertion. |
| Delta2 R3-2 — nonexistent event timestamps | **Closed:** S:655; B:138 separates untimestamped events and tests timezone/index ties. |

**The three partial rejections hold.** V1’s separate `oracle` role is unnecessary while the mandatory non-routing `.class` remains visible (S:467,504). V9 appropriately uses measured performance acceptance instead of flaky timing unit tests; meeting the budget still gates completion (S:42,957). V14 correctly rejects direct float32-training-hash comparison with float16 sandbox tensors (S:1150; `c10w_oracle_train.py:168`).

**Non-C10 colour classes are appropriate.** Characterization and screening labels map to `characterization`; configuration names map to `not-a-verdict`, without chips (S:499–501). None maps to green `pass`. B:111 adds rendered-colour verification. Browser behavior remains **UNVERIFIED**.

**Codex can proceed without resolving the former scientific/schema ambiguities, but cannot satisfy the brief literally until finding 1 is corrected.** Findings 2–3 should accompany that correction. Build performance, browser acceptance and generated-table validation remain implementation-stage checks.

Claim checks below used read-only Python/JSON, hashing and source inspection; no build or browser test ran. `W` denotes `results/c10w_oracle/p1_20261007T223707_598959Z/`.

| # | New/changed concrete claim | Source checked | Result |
|---|---|---|---|
| 1 | TemporaryDirectory citations | `tools/labviz/test_labviz.py:202,224,269,280` | **OK:** all four use unqualified `TemporaryDirectory()`. |
| 2 | Test command bounds temporary files | B:44,51 | **OK:** directory creation, `TMPDIR` and assertion specified; execution unrun. |
| 3 | Loss observations lack timestamps | `W/train/A7_coined_coined_s0_r16.json:.losses[0]` | **OK:** only `step:10`, `loss:7.706562042236328`. |
| 4 | Forty loss points | All five `W/train/*.json:.losses` | **OK:** 40 each. |
| 5 | Four hundred step durations | Same files, `.step_seconds`; trainer:207–208 | **OK:** 400 each; elapsed durations. |
| 6 | Bare terminal marker | `results/c10w_oracle_logs/p1-eval.log:2` | **OK:** `STAGE_EXIT=0`, no timestamp. |
| 7 | Recorded timezone example | `results/c10w_oracle_logs/p2-eval.gate.20261007T222229.91288.json:.at` | **OK:** `2026-10-07T22:22:29-06:00`. |
| 8 | Canonical-control reference citation | `experiments/track_c/c10w_oracle_read.py:403` | **OK:** passes closedform A7 and U A7. |
| 9 | Ordinary A7 citation | Same reader:361 | **OK:** ordinary configuration uses those references plus control. |
| 10 | No U canonical key | `W/eval.json:.u` | **OK:** A1, A2, A7, A7_shuf; no A7_canon. |
| 11 | D1 inventory | `results/d1_*.json` | **OK:** 18 files. |
| 12 | D1 header-glob expansion | `results/d1_concentration_sweep_result*.json` | **OK:** four files. |
| 13 | Five D1 records explicitly named | `CORPUS/22_D1_CAPACITY_LAW.md:3` | **OK:** four glob matches plus predictor-map file. |
| 14 | D1 anchored decision | Same header:3 versus S:1036 | **WRONG quotation:** actual `⟨D-D1-1@0db8d819⟩`. |
| 15 | B1 row does not name D1 result paths | `docs/EXPERIMENT_REGISTRY.md:19` | **OK:** B1 paths; documentary reference to CORPUS/22. |
| 16 | Different comparison populations | `results/r5_paraphrase_robustness.json:.rows.NOVEL_single`; C10V detail | **OK:** 16 versus 24 facts. |
| 17 | Saved-picture fixture dimensions/font | `render.py:18,61,108–109`; arithmetic | **WRONG expected outcome:** 9pt becomes 14.705882px and passes. |
| 18 | Replacement failing font | `render.py:105`; same arithmetic | **OK:** 6pt becomes 9.803922px and fails. |
| 19 | Updated example JSON-source values | S §6 example, all existing source paths | **OK:** 34/34 exact. |
| 20 | Updated example document citations | Same example | **OK:** 19/19 quotes and values match. |
| 21 | Updated example recorded hashes | Same example `sources[]` | **OK:** 12/12; generated-source placeholders remain unverified. |
| 22 | Population-pointer repair | S:668,797–800; B:134 | **OK:** `{file,path}` metadata, no `inputs`; explicit full-list validation. |
| 23 | Absolute-norm inventory | Recursive numeric `delta_norm` beneath `delta_norms`, with specified exclusions | **OK:** 1,183 values in 80 files; no JSON parse failures. |
| 24 | Shared maximum | `results/c10h_anyedit_pilot.json:.recipes.anyedit_window1.delta_norms.A7_coined_coined["8"].delta_norm` | **OK:** `113.7967300415039`, scan maximum. |
| 25 | C10V counterexample to former maximum | `results/c10v_layerpick/pass1.json:.recipes.B0.delta_norms.A2_coherent2["8"].delta_norm` | **OK:** `55.45940399169922`. |
| 26 | C10U gate coverage | `results/c10u_mint2/r3_read_after_replicateF.json:.F.arms,.V2.arms` | **OK:** 49 booleans; five specified readings lack gates. |
| 27 | Non-C10 content fixtures | G6.1 `.records,.rungs`; R5 `.arms,.templates.P_test` | **OK:** 100/3; four arms/three templates. |
| 28 | Label-table coverage | Enumerated specified label keys across result JSON | **OK:** all 27 distinct strings represented; none assigned `pass`. |
| 29 | Float32 training-hash rejection | `W/train/*.json:.dtype`; trainer:168 | **OK:** float32, explicit `.float()` upcast. |
| 30 | Launcher preservation hash | `tools/labviz_serve.sh` | **OK:** matches B:35 exactly. |

Graft: no successful call; no savings reported.