VERDICT: FIX-FIRST

Reviewer: Claude Opus 5.5 advisor. Python-free (`jq`, `grep`, `sed`, `awk`, `ls`, `stat`, `shasum`) and read-only.

## Findings

**1. BLOCKING. The badge ignores the arm's role** (§5 item 1, brief test 3).
- Control arms A1/A2 score 68–71/72 in every C10V recipe. Recipe A has no reading (`run.json:.readings` holds B0, B and Bshuf only). So a B·A1 card would show "68 of 72 (goal 61) · not yet labelled", which reads as a pass waiting for its label.
- The C10W `verdict.json:.class` says "ORACLE MEASUREMENT — not a route; never promotable as a write-engine result". The spec never shows it.
- Change:
  - add an `identity.role` field: binding / control / reference / oracle;
  - show the goal only on binding write-route cards;
  - label control and reference arms "not labelled by design";
  - print `.class` verbatim on C10W cards;
  - add tests for both.

**2. BLOCKING. The C10U label is read from a non-binding file** (§3.3, §4 row 1).
- The three readings disagree on `mint1_s0`: v2 says `LEAD-NOT-REPLICATED`, replicateF says `LEAD`, frozen says `LEAD-NOT-REPLICATED`.
- `CORPUS/54_C10U_MINT2.md:5` and the registry row name `r3_read_after_replicateF.json` as the binding reading. The spec cites v2 (and the wildcard `r3_read_after_*`).
- Change: name one binding reading per family in a data table, cited from the CORPUS header. Test: C10U `mint1_s0` shows `LEAD`.

**3. BLOCKING. "Hash-verified: 434 of 434 unchanged" misreads the C10W records** (§3.5, item b, brief test 9).
- The 434 `frozen_parameter_hashes_*` prove only that the base weights stayed frozen during adapter training.
- The *evaluated* model has ΔW merged into `down_proj` layers 4–8 (7.74…5.61).
- `base_band_hash == final_band_hash == every band_after_hash`. These are LAW#5 *restore* checks (`c10w_oracle_read.py:313`, `:319`), not before/after-write hashes.
- Change: caption "base weights hash-verified frozen during training (434/434); adapter merged into down_proj 4–8 only, by construction; post-eval restore hash-verified". Fix test 9, §3.2 and §3.5.

**4. BLOCKING. A derived ✓/✗ with no recorded gate is a Lab View verdict** (§5 item 3).
- C10W P1 is `INCOMPLETE` with `final_label null`. G1–G6 would still get Lab View–computed marks; for example G3 86.72 vs 87.56 − 3 gives ✓.
- Change: where no recorded boolean exists, show the value and the rule limit only, with no glyph, plus "no recorded gate result". Test this on C10W P1.
- Also: the C10W reference arm is `recipes.closedform.arms.A7_coined_coined` (prereg `:347`), not `recipes.A`.

**5. BLOCKING. The item 8 footer uses B0's statistic** (brief test 7).
- −0.479 is `.readings.B0.spearman_G_edge`. The map is recipe B's, and `.readings.B.spearman_G_edge` = −0.316.
- Test 7 omits the recipe, so it would lock in the wrong pairing.
- Change: read `.readings.B`, and make the test assert the path.

**6. BLOCKING. The §6 schema breaks its own leaf rule; brief tests 1 and 15 conflict with it.**
- Bare values appear outside leaves: `recipe`, `arm`, `binding_arm`, `seed`, `track`, `condition`, `era`, `index`, `layer`, `configured`, `hit_kind`.
- Context leaves use `src {file, line}`, which jq cannot resolve, and one holds a "…"-truncated question.
- Example values fail a literal jq check:
  - date "…03:32:38Z" vs the real `.when_utc` "2026-10-08T03:32:38.191318+00:00";
  - 16.31 vs 16.31455…; also 0.1365, 55.42 and 0.0156.
- `built_utc` changes on every build, so it breaks test 15's "identical bytes".
- Change:
  - whitelist the structural keys;
  - add a doc leaf `{file, line, quote}`, checked by "the line contains the quote";
  - store raw values in leaves and round only in rendering;
  - drop `built_utc`.

**7. BLOCKING. Brief/spec contradictions.**
- **Test 11 vs §4A.1.** Every page carries the status strip and breadcrumb, which today name a C10W stage. So a G6.1 page contains "C10". The forbidden-word lists also differ: §4A.4 #6 forbids "72" and "61"; test 11 forbids "of 72", "goal 61" and "C10". Change: scope the test to the main content region and use one list.
- **Card location.** §5 item 10 writes cards to `results/labviz/cards/`, but `http.server --directory results/labviz/site` cannot serve it, so the "data for this view" links break over Tailscale. Change: write to `site/cards/`, or symlink it as v1 does for `runs`.
- **Rebuilds.** §8 says "the builder does not rebuild during the run", but `tools/labviz_serve.sh:13–19` rebuilds every 60 s.
- **Sign-off tables.** Open points 1 and 5 say the program signs off `labels.json` and `contexts.json`, yet the brief has Codex author them. Change: supply them in the brief, or mark Codex's versions DRAFT pending sign-off.

**8. SHOULD. The builder ingests everything under `results/`** (`build.py:387–420`).
- Future `results/replays/`, `results/sandbox/` and telemetry `.jsonl` files would become RECORDED cards.
- Change: in Phase 1, exclude them and route any NOT EVIDENCE or EXPLORATORY record to `observations`, with a fixture test.

**9. SHOULD. The 60 s rebuild runs during GPU jobs.** v2 writes about 1,400 cards per pass, which can disturb the science runs' wall-time and RSS guards (INVALID-BUDGET, EXCEEDS-TTL). Change:
- write a file only when its content changes;
- skip images whose inputs are unchanged;
- add a test for the warm-rebuild time and RSS ceiling;
- state in §2.3 the premise behind the exemption.

**10. SHOULD. `links.json` maps by family folder.**
- `"results/c10w_oracle/": "CORPUS/55"` would caption P2 runs with the P1 interim result.
- Its test checks the CORPUS *body* for the D-ID, but `D-C10u-mint2` occurs in 53, 54, 55, 00–03 and README.
- Change: map by run directory, and check the header's first 12 lines.

**11. SHOULD. Non-C10 science has no inventory.**
- §3 covers only the C10 families, yet D-C10r-labviz-4 asks for all historical science, and test 11 renders a G6.1 page (`g6_scale_n_result.json`: `config`, `records`, `rungs`).
- Change:
  - add a §3.10 with recorded fields and per-item tiers for at least G6.1, D1, B3N and R5;
  - assign experiment → era explicitly in `contexts.json`, with a test that each of the 54 rows gets exactly one era;
  - disambiguate "D1" in §4A.4 #6.

**12. SHOULD. Design-criteria measurability.**
- **#3 font size.** Computed `font-size` of SVG text inside a scaled `viewBox` is the nominal size, not the rendered size. Measure the rendered box (`getBoundingClientRect`, or the `getScreenCTM` scale), and forbid text drawn on a canvas.
- **#5 contrast.** Resolve the effective (non-transparent) ancestor background.
- **Decorrelated review.** Codex cannot decorrelate its own build. Assign the review to the program session.
- **Playwright.** It is not installed; only the chromium builds are cached. Name an install directory outside the restricted paths, such as `/private/tmp/labviz-review/`.
- **Task test.** Add one: from Home, reach C10's status and one link it shares with D1 in 4 taps or fewer.

**13. SHOULD. Fact-panel and stimulus details.**
- `generated[1]` " Vindex Vaskul," is scored `full:true` for "Vindex Vask". Caption it: "right/wrong is the test's recorded scoring rule".
- `seal_audit.json:.rows` has 22 rows: T01–T20 plus the reserves R1 and R2. Filter on `id` starting with `T`.

**14. SHOULD (blocking for Phase 4). Sandbox, §12.**
- **Leakage.**
  - Template non-overlap is too weak. Sandbox questions paraphrase "capital of X" on the same 24 facts as the held-out three.
  - Change: score on a separate fictional fact set, or at least apply the C10W seal audit (banned bigrams and words) against the held-out three.
  - Log every try. A prereg "motivated by sandbox" must cite all tries of the session.
  - CANON is training template T01, which conflicts with §12.3.
- **Scheduling.**
  - A gate refusal is `exit 3` (`run_c10w_p2_stage.sh:16`). An idle sandbox server can therefore halt an unattended chain.
  - Change: re-check before *every* try, use a lock file shared with the coordinators, and never run while an overnight chain is armed.
- **Restore.**
  - Before the first try, hash all `down_proj` 4–12, ideally all 434 tensors against C10W's recorded `frozen_parameter_hashes_before`.
  - After each restore, re-run the pristine probe (`torch.equal`).
- **Gauges.** There is no same-process reference arm, so show values only, with no ✓/✗.
- **Exposure.** Bind to localhost or Tailscale and require a token. The Lab View server binds 0.0.0.0.
- **Schema.** Add `observations.sandbox[]` to §6.
- **Settings.** Forbid any settings change that alters cache identity (`mom2_n_samples`, `mom2_dtype`, `mom2_dataset`).

**15. SHOULD. The leaf verifier's jq grammar.** The verifier reimplements jq in python. Define the grammar (`.k`, `["k"]`, `[n]`) and cross-check about 50 leaves with the `jq` binary.

**16. NIT. Citation drift** (rows marked WRONG in the table below). `contexts.json` must quote the t-branch `:35` text verbatim ("5/5 consistency PASS"), not paraphrase it as "facts cleared out of 5".

**Tiers and scope.**
- Tiers are honest except two:
  - (b) "hash-verified" (finding 3);
  - (a) "SHA-bound for C10V and older": the current SHA appears only in the c10s, c10t, c10u, c10v and c10w records (133 files), so older runs will show "not transcribed".
- Every operator requirement is covered. Non-C10 historical science is covered structurally but not yet tiered (finding 11).

## Claim check

| # | Claim | Result |
|---|---|---|
| 1 | pass1 `.decision_id`, `.model` (3aab1f19…, fp16, mps) | OK |
| 2 | `.recipes.*.band` = [4..8] for A, B0, B, Bshuf | OK |
| 3 | A7 counts A 11, B0 12, B 12, Bshuf 10 /72; A1 68–70, A2 70–71; B·A7 canon 7/24 | OK |
| 4 | described_as A 90.0, B 86.17, B0 90.11, Bshuf 87.37 | OK |
| 5 | B0·A7 delta_norms keys {"8"} = 55.42 | OK |
| 6 | B·A7 4–8 = 4.85/16.13/27.69/9.71/16.31; A·A7 15.86…27.20 | OK |
| 7 | detail[0] Zorbland / Vindex Vask / ntok 4 / tf 9/9 | OK |
| 8 | `rho_per_prompt` 192 paths | OK |
| 9 | run.json labels NULL/NULL/NULL-CONTROL-ONLY; binding 12/12/10; B `described_as:false` | OK |
| 10 | `spearman_G_edge` −0.479 | OK for B0; WRONG as used in item 8 and test 7 (B = −0.316) |
| 11 | step0 G_table 24×5, row 0 0.832…; margins [2][24]; reproduced true; δ 0.0; concentration 15 | OK |
| 12 | hsic layers 4–8 {HSIC_b, per_fact_c, status DIAGNOSTIC} | OK |
| 13 | `sha256(c10e_bandknob.py)` = 1f6be581…e695 = pass1 identity | OK |
| 14 | C10W A7 s0: 40 losses 7.7066→0.000411, 400 step times, fit 480/480, 523.35 s, adapter 4,179,028 B | OK |
| 15 | 434 frozen hash keys = 36×12+2 | OK (count); meaning WRONG (finding 3) |
| 16 | P1 oracle·A7 70/72, 86.72, L3 30/30, ppl 21.755→21.081; closedform 9/72; canon_s0 2/72, L3 12/30 | OK |
| 17 | MMLU 0.59, 118/200, net 4, 13/9 | OK |
| 18 | oracle_p1 ΔW 7.74…5.61; closedform 15.82…27.56 | OK |
| 19 | verdict.json null / INCOMPLETE / OPEN/BLOCKING / false | OK (`.class` omitted by the spec) |
| 20 | base/final band hash = "before and after" | WRONG: restore checks, all equal |
| 21 | seal_audit = 20 training phrasings | WRONG: 22 rows (T01–T20, R1, R2) |
| 22 | C10U label at `r3_read_after_v2` | WRONG: binding reading is replicateF |
| 23 | F_r1_multi_snone 14/72, binding 14, da 88.22 | OK |
| 24 | grep counts: para_full_hits 119, delta_norms 78, per_template_hits 21, losses 12 | OK (described_as 79 and L1 54 now; P2 drift) |
| 25 | G_table and winning_margins in 1 file each | WRONG: 2 each (step0 and pass1) |
| 26 | `update_norm_ratio` 4.94/1.12/1.02/1.017/1.010 | OK |
| 27 | config.json values; `hf_cache` symlink | OK |
| 28 | hparams `:2`, `:5`, `:13`, `:16–18`; §12.2 defaults | OK |
| 29 | c10e `:51`, `:52–56`, `:57–61`, A7 formula → "Vindex Vask"; `:475` | OK |
| 30 | gate exemptions `:21–30` (Lab View `:25–26`); inventory rule `:43–54` | OK |
| 31 | registry 54 rows; 36/16/1/1 field split; R2 is the 12-field row; JSON registry 20 rows | OK |
| 32 | CORPUS E2e-map lines 16 (23, 26–40); 57 entries; D-C10u-mint2 in 53/54/55 | OK |
| 33 | F1_DETERMINATION `:62–71` C1–C10, `:71` §8.9 | OK |
| 34 | runbook `:372`, `:373`, `:375`, `:376` | OK |
| 35 | runbook §8 `:447–604`, TRACK E `:601`, 76 D-IDs | WRONG: `:448–608`, `:602`, 93 |
| 36 | framework_findings 10 files | WRONG: 16 |
| 37 | style.css, render.py and index.html audit lines (§4A.3) | OK |
| 38 | `app.js:50` / `:45` band colouring | WRONG: `:49` |
| 39 | `pass1_started.json:.identity.created_utc` 02:54 | WRONG field: `.when_utc` (created_utc is 02:14) |
| 40 | §6 example date "…03:32:38Z" | WRONG under the leaf rule |
| 41 | covariance caches for layers 4–12 | OK |
| 42 | evaluations 15 entries; entry 14 → CORPUS/56; goal 61 | OK |
| 43 | C10V gate rules reproduce every recorded `locality_gates` boolean | OK (`c10v_layerpick_read.py:346–348`) |
| 44 | J.6 table `:172–193` | NIT: continues to H-22 at `:195` |
