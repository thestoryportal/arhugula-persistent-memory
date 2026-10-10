# Lab View v2 spec: fold map of the Astra and advisor reviews

Date: 2026-10-08. Inputs: `results/labviz_v2_spec_astra.md` (GPT-6-Astra, 11 findings + 52-row claim table) and `results/labviz_v2_spec_advisor.md` (advisor, 16 findings + 44-row claim table), both FIX-FIRST. Outputs: `docs/LABVIZ_V2_SPEC.md` (Status: "v2, folded from the Astra and advisor reviews (2026-10-08)") and `results/labviz_v2_codex_brief.md`. Program decisions 1–17 of the fold prompt were applied as given; "D<n>" below names them.

All re-verification was python-free (`jq`, `grep`, `sed`, `awk`, `perl`, `ls`, `wc`, `shasum`, `node`/`npx`). New data commands are in spec §3.9. Every JSON-source leaf of the spec §6 example was resolved with `jq` (35 OK, 0 mismatches; 7 more point at Lab View tables that do not exist yet), every document-source quote with `sed -n` (12 OK, plus 1 rule citation), and every listed SHA-256 with `shasum` (12 OK).

## Astra findings

| ID | Finding | Disposition | Where |
|---|---|---|---|
| A1 | Card contract fails its own tests (bare numbers, uncited doc leaves, derived leaves without inputs, rounded values) | Folded (D1): four typed leaves, structural whitelist, full precision, `sources[]` with SHA-256 for every file incl. reader records and Lab View tables, per-type validation | spec §6; §1; §3 intro; brief rule 2, test 1 |
| A2 | Item 8 shows B0's statistic on B; joins by count alone | Folded (D2, D3): B = `−0.3162875387734472` from `.readings.B.spearman_G_edge`; joins on family, recipe, arm, seed, replicate and `pass_sha256` / `p1_eval.sha256`; wrong-reader fixture (`F_r0_mint1_s0` vs `F_r1_mint1_s0`, both 46); C10U binding reading named | spec §3.1, §3.3, §5 items 1 and 8; brief tests 3, 8 |
| A3 | Context rules do not implement coverage (folder paths, braces, first D-ID, curated edges) | Folded (D9): brace expansion, D-ID grammar, explicit experiment → decision rule (anchor, else sole ID, else unknown), ties unknown, typed edges, fixtures for rows `:19`, `:25`, `:58`, `:59`, `:60`, basename `run.json`, `c10u_mint2/r2/`, a tie; `status_now` kept apart from era framing | spec §11.1, §11.2, §11.5; brief build 3, test 11 |
| A4 | Label and gate semantics left to the builder | Folded (D5, D6): complete label → class table (every recorded string, command in §3.9); complete per-family gate table (C10V, C10U, C10W) with reference arm, comparator, applicability (G4 every training frame, G7 matched shuf, O-A7-canon G1–G6), missing-value behaviour; ✓/✗ only from recorded booleans; consistency, boundary and mismatch tests; configuration PASS never promoted | spec §5 items 1 and 3, §10 point 1; brief rule 6, tests 4, 5 |
| A5 | Brief contradictions (report path, `built_utc` vs identical bytes, scrubber vs player; exemption checks; child python) | Folded (D13): report path allowed; `built_utc` removed, determinism defined; Phase 1 scrubber vs Phase 3 player distinguished; launcher SHA-256 and exempt lines tested; no child process | spec §2.3, §4 row d, §5 item d, §6; brief rules 3–5, build 15, test 19 |
| A6 | Recorded stimulus treated as unavailable; bind order and role | Folded (D8): precedence recorded → SHA-bound → missing; recorded `.stimulus` in 57 files (c10b–c10q), `c10s_solvefeas/run.json:.held_out_forms`; role/order binding; permuted-template fixture; hparams and `config.json` bound by recorded SHA / revision | spec §3.4, §3.5, §3.6, §4 row a, §5 item a; brief build 7, test 7 |
| A7 | Comparison needs an eligibility contract; units and write kinds | Folded: join by subject, answer, template, scoring kind; never by row index; fixtures; predicted, injection, replay and sandbox values kept off RECORDED rulers | spec §5 items 4, 5; brief build 9–10, test 18 |
| A8 | Sandbox leakage: dedicated evaluator, actual prompts tested, all tries recorded | Folded (D16): production `eval_arm` (`c10e_bandknob.py:358`, `:491`, `:363–365`) forbidden; separate fact set and disjoint locality probes; captured-prompt tests; hashes and every try recorded and cited; near-duplicates reviewed by hand | spec §12.1, §12.3, §12.4 |
| A9 | Sandbox scheduling and restore | Folded (D16): never with a coordinator or armed chain, lock file, request-time admission, queue cancellation, per-try runtime cap, restore verified on every path with all parameters and buffers, hooks/caches/RNG/mode reset or worker discarded; controls signed off with types, finite ranges, layer combinations; cache-identity settings fixed; Phase 4 tests | spec §12.2, §12.4, §10 point 6 |
| A10 | Screenshot criteria measure appearance, not usability | Folded (D13, D14): vocabulary test scoped to `data-region="content"`, one forbidden list; scripted tap/keystroke tasks, URL state, keyboard/touch; 360 px, 200 % zoom, WebKit; rendered text size via boxes incl. SVG, no canvas text; composited contrast incl. marks and focus rings; target rectangles; loaded bytes from the request log; program session reviews, Codex self-checks | spec §4A.2, §4A.4, §4A.5; brief build 16, tests 12, 14 |
| A11 | Replay fidelity wording; granular coverage; subject position; EXPLORATORY | Folded (D15): "re-creation; recorded outcomes matched"; NOT EVIDENCE on views, exports and cards; attention pass labelled separately; historical internal playback marked NOT FEASIBLE; top-16 units called a summary; subject position = key-extraction location, ΔW acts on every token (`C10V_LAYERPICK_PREREG.md:50`); EXPLORATORY added globally; `observations.sandbox[]` | spec §2.4, §4 rows b/d and limits, §5 items b/c/d, §6, §7.3, §7.5, §7.6, §4A.1 |
| A-close | "Nothing is NOT FEASIBLE" overstates recoverability | Folded: §4 limits rewritten; row d carries a NO tier | spec §4 |

## Advisor findings

| ID | Finding | Disposition | Where |
|---|---|---|---|
| V1 | Badge ignores the arm's role; `.class` not shown | Folded (D2) with one change: the role set is the program's {binding, control, reference, shuffled-control, canon-control}; the advisor's proposed `oracle` role is **not** added, because the C10W oracle status is carried verbatim by `verdict.json:.class` on every C10W card and the oracle A7 configuration is the experiment's binding measurement | spec §5 item 1 (role table); brief test 3 |
| V2 | C10U label read from a non-binding file | Folded (D4): `r3_read_after_replicateF.json` only (`CORPUS/54_C10U_MINT2.md:5`, `docs/C10U_MINT2_PREREG.md:190`, registry `:58`); test: `mint1_s0` shows `LEAD` | spec §3.3, §4 row 1; brief data sources, test 3 |
| V3 | "434 of 434 unchanged" misreads C10W | Folded (D7) with the program's wording; restore checks cited (`c10w_oracle_read.py:313`, `:319`) | spec §3.2, §3.5, §4 row b, §5 item b; brief test 10 |
| V4 | Derived ✓/✗ with no recorded gate; C10W reference arm | Folded (D5): derived reference line without glyph; "not judged yet"; reference `recipes.closedform` (87.56). Found while folding: P1 does hold recorded booleans for the `oracle_p1`·A7 configuration in `interim_reader_configuration_v2.json` (named by `CORPUS/55…:24`), so that configuration shows interim ✓/✗; the other P1 configurations do not | spec §3.2, §4 row 3, §5 item 3; brief test 5 |
| V5 | Item 8 uses B0's statistic | Folded (D3), test asserts the path | spec §5 item 8; brief test 8 |
| V6 | §6 breaks its own leaf rule; `built_utc` | Folded (D1) | spec §6; brief rules 2, 4 |
| V7 | Brief/spec contradictions (C10 strip vs test 11, two word lists, card location, rebuild claim, sign-off tables) | Folded (D12, D13): content-region scope, one list; cards in `site/cards/`; §8 corrected; labels/gates transcribed from the spec, `contexts.json` DRAFT pending review | spec §4A.4, §5 item 10, §8, §10; brief rules 5–6 |
| V8 | Builder ingests everything under `results/` | Folded (D10) | spec §9.1, §8; brief build 2, test 16 |
| V9 | 60 s rebuild during GPU jobs | Folded as a measured budget, not a pass/fail timing test: write-on-change, skip unchanged images, warm/cold time and RSS budget measured and reported, premise stated. A hard timing assertion in the unit tests is **not** added: wall time and RSS depend on machine load, so such a test would be flaky; D13 asks for "measured and reported" | spec §2.3; brief rule 4, deliverable |
| V10 | `links.json` by family folder; CORPUS body check | Folded (D11): keyed by record or phase directory, longest key wins, P2 unmapped; header (first 12 lines) check | spec §4 row 6, §5 item 6; brief test 17 |
| V11 | No non-C10 inventory; era rule; "D1" ambiguous | Folded: §3.10 (G6.1, D1, B3N, R5, with fields and tiers); explicit experiment → era in `contexts.json`, test each of 54 rows; "D1" defined as the capacity-law line (CORPUS/22) | spec §3.10, §4A.4 #6, §11.5; brief tests 11, 12 |
| V12 | Design-criteria measurability; decorrelated review; Playwright; task test | Folded (D14). Playwright finding stated (spec §4A.5): not installed as a resolvable package (`npx --no-install playwright --version` refuses, wants 1.64.0); stale npx-cache copies 1.59-alpha/1.60.0/1.61.1; `~/Library/Caches/ms-playwright` has chromium-1208/1243, headless shells, ffmpeg-1011, no WebKit; install under `/private/tmp/labviz-review/` | spec §4A.4 #3, #5, #7, §4A.5; brief build 16 |
| V13 | Generated-text caption; seal_audit rows | Folded: "right/wrong is the test's recorded scoring rule"; 22 rows, filter `id` starting `T` | spec §3.2, §3.6, §5 item a |
| V14 | Sandbox: leakage, scheduling, restore, gauges, exposure, schema, cache settings | Folded (D16), with one part **rejected**: checking sandbox hashes "against C10W's recorded `frozen_parameter_hashes_before`". Those hashes are of the float32 upcast (`train/*.json:.dtype` = "float32"; `c10w_oracle_train.py:168` loads fp16 then `.float()`), while the MEMIT path runs float16 (`pass1.json:.model.dtype`), so they are not a direct reference; the spec instead hashes every parameter and buffer at load as the session's pristine identity and leaves a cross-check to the open-point-6 sign-off. Everything else folded: T01 = CANON excluded, seal-audit lists applied, every try logged and cited, exit-3 risk and lock file, `torch.equal` probe after restore, values only on gauges, 127.0.0.1 + Tailscale + token, `observations.sandbox[]`, `mom2_*` fixed | spec §12, §6 |
| V15 | Leaf verifier's jq grammar | Folded: grammar `.k`, `["k"]`, `[n]`; ≥ 50-leaf cross-check with the `jq` binary | spec §6; brief test 1 |
| V16 | Citation drift; t-branch quote | Folded: claim rows below; era example quotes "5/5 consistency PASS" verbatim (`t_branch_decision_document_v1_4.md:35`) | spec §11.2 |
| V-tiers | Item a "SHA-bound for C10V and older" overstated | Folded (D8): SHA in 136 files at 2026-10-08 (advisor counted 133); older runs use recorded stimulus or show "not transcribed" | spec §3.6, §4 row a |

## Claim-table rows marked WRONG

| Row | Claim | Fixed to (verified) |
|---|---|---|
| Astra 16 / advisor 10 | item 8 −0.479 for B | B −0.3162875387734472; B0 −0.47912964570281436 (§3.1, item 8) |
| Astra 32 / advisor 24 | 78 files with `locality_described_as` (and other counts) | at 2026-10-08 06:28 UTC: para_full_hits 121, delta_norms 80, described_as 81, L1 56, per_template_hits 21, losses 14 (§3.4, §4 row 2) |
| Astra 36 | held-out text recorded only in C10W | recorded `.stimulus` in 57 files; `c10s_solvefeas` `.held_out_forms` (§3.4, §3.6) |
| Astra 45 | 1,438 cards; 4,056,930 / 2,580,998 bytes | 1,503 cards; index.html 4,248,295 and data.js 2,722,695 bytes at 06:28 UTC (§4A, §4A.3, §6, §11.4) |
| Astra 48 | six-layer map `:10–17` | `:10–18` (§11.1) |
| advisor 15 | meaning of the 434 hashes | frozen during training only (§3.2, §3.5) |
| advisor 20 | band hashes "before and after" | restore checks, all equal (§3.2) |
| advisor 21 | seal_audit = 20 phrasings | 22 rows: T01–T20, R1, R2 (§3.2, §3.6) |
| advisor 22 | C10U label at `r3_read_after_v2` | `r3_read_after_replicateF.json` (§3.3, §4) |
| advisor 25 | `G_table` / `winning_margins` in 1 file each | 2 each, step0.json and its copy in pass1.json `.step0` (§3.1, §3.4) |
| advisor 35 | runbook §8 `:447–604`, TRACK E `:601`, 76 D-IDs | `:448–608`, `:602`; 73 D-IDs under the §11.1 grammar, 93 with the bare regex (which matches inside words), at 2026-10-08 (§11.1, §11.2) |
| advisor 36 | framework_findings 10 files | 16 at 2026-10-08 (§11.1) |
| advisor 38 | `app.js:50` / `:45` | `app.js:49` (§5 item 4, §11.3) |
| advisor 39 | `pass1_started.json:.identity.created_utc` 02:54 | `.when_utc` 02:54:27; `created_utc` is 02:14 (§7.4) |
| advisor 40 | §6 date "…03:32:38Z" | `2026-10-08T03:32:38.191318+00:00` (§6) |
| advisor 44 (NIT) | J.6 `:172–193` | `:172–203`, H-1…H-30 (§11.1) |
| — (found while folding) | §11.4 "≈ 90 decisions" | ≈ 80 (78 distinct D-IDs across CORPUS, registry, overlay under the grammar) |
| — (found while folding) | P2 "(running)" | at 06:06 UTC P2 holds `HALT.json` (stage p2-eval, "HALT: evaluation process failed"), `eval.json`, `eval_halt.json`, no `verdict.json` (§3.2); recorded as a snapshot, not interpreted |

## Counts

- Findings: Astra 11 (+1 closing remark) and advisor 16 (+1 tier remark) = 29 items. All 29 folded; none rejected outright. 3 have one part rejected with evidence: V1 (the `oracle` role value), V9 (a hard timing test; measured and reported instead), V14 (C10W float32 hashes as the sandbox reference).
- WRONG claim rows: the 16 rows above cover Astra's 5 WRONG rows and the advisor's 13 WRONG/NIT rows (the item-8 and count rows are shared); 2 more stale claims were found and fixed while folding.

## Not verified (python-free limits)

- The §2.3 build budget numbers are program-set and UNMEASURED; Codex measures them.
- The leaf grammar was exercised with `jq` on the §6 example only, not with a python verifier.
- WebKit/Playwright were probed, not installed (no download made).
- Label → class assignments for the non-C10 strings (`CHARACTERIZATION…`, `RESOLVED-BY-SCREENING…`, `MIXED_NONPROMOTIONAL`, `CONTROL_RECOVERY_FAIL`, `base`/`post`/`gguf_*`) are display classes chosen at this fold from the records' own wording; they are in the spec table for the program session to confirm.
- Citations the reviewers marked OK were not all re-run (e.g. `c10e_bandknob.py:277–300`, `:475`; §4A.3 style lines).

## Round 2: Astra delta review (`results/labviz_v2_spec_astra_delta.md`, FIX-FIRST)

Re-verified at 2026-10-08 06:45 UTC with `jq`, `sed`, `grep`, `shasum` and one light python read (`python3 -I`, no model, tokenizer or torch) that confirmed all 27 recorded label strings have a row in the spec's label table.

| ID | Finding | Disposition | Where |
|---|---|---|---|
| R2-1 (BLOCKING) | Non-C10 badges contradict the role table | Folded: the role table governs C10 cards only (`results/c10*`); non-C10 cards carry no role and show their own sourced label or status and measure (R5 `CHARACTERIZATION` + per-arm rates; D1 verdict sentence; G6.1 registry status `:13` "SPLIT (cross-entity FALSIFIED)"), never the C10 goal; R5 and G6.1 badge tests | spec §5 item 1; brief build 6, test 3 |
| R2-2 (BLOCKING) | Gate fixtures require nonexistent data | Folded: verified 7 of 12 C10U binding-reading arms carry `.gates` (49 booleans); the 5 UNDERFIT readings (`F` `modifier_s0`–`s2`, `V2` `mint2_s1`, `mint2_s2`) have none and must render no glyph and no outcome. C10W U reference is `eval.json:.u.A7_coined_coined` for every configuration incl. O-A7-canon (`.u` keys: A1, A2, A7, A7_shuf; reader `c10w_oracle_read.py:361`, paired check `:326`); canon's reference "A" is closedform·A7. Consistency test covers every present boolean (15 + 49 + 7) | spec §5 item 3; brief test 5 |
| R2-3 (BLOCKING) | Brief contradictions: subprocess ban vs jq in tests; temp dirs; browser cache | Folded: the ban covers the production builder and its run-time modules only; the test module may run `jq`; `/private/tmp/labviz-mpl/` and `/private/tmp/labviz-review/` explicitly allowed, with `PLAYWRIGHT_BROWSERS_PATH=/private/tmp/labviz-review/ms-playwright` and `npm_config_cache=/private/tmp/labviz-review/npm-cache`; Chromium and WebKit installed there | brief rules 3, 5, build 16, test 19 |
| R2-4 (SHOULD) | Derived meaning not validated; `scale.max` wrong population | Folded: `scale.max` is a derived leaf over a declared eligible population (every applied `delta_norm` under `delta_norms` in a RECORDED card), listed in `results/labviz/site/cards/scales.json`; at 06:45 UTC 1,183 values in 80 files, max `113.7967300415039` (`results/c10h_anyedit_pilot.json:.recipes.anyedit_window1.delta_norms.A7_coined_coined["8"].delta_norm`); C10V's own max is B0·A2 `55.45940399169922`. Derived leaves list every operand (structural operands allowed, e.g. the card's `layer`); derived context edges carry the whole chain (example now cites registry `:60` → overlay `:22` → F1 `:71` / e2e `:14`); must-fail fixtures for a removed operand, a removed chain link and an over-maximum card. Example re-verified: 35 JSON leaves OK, 19 document quotes OK, 13 source hashes OK, JSON parses | spec §5 item 4, §6, §3.9; brief test 20 |
| R2-5 (SHOULD) | Missing Phase-1 tests | Folded as brief tests 21–26: predicted/injection values off RECORDED rulers; hparams-SHA and model-revision mismatch; newest-written 3D default; scrubber event ordering (recorded time, then source path, then line, now also in spec item d); write-on-change by mtimes and zero render calls (also in spec §2.3); G6.1 (100 records, 3 rungs) and R5 (4 arms, `ptest_hits`, `ptest_obs`, recorded `P_test`) contents | brief tests 21–26; spec §2.3, item d |
| R2-6 (SHOULD) | Font size measured from boxes | Folded: computed `font-size` × rendered transform scale (`getScreenCTM()` for SVG; CSS transforms, `zoom`, page zoom for HTML); boxes only for clipping/layout; fixtures 12px with large line height (fail), 16px SVG at 0.5 scale (fail), 13px unscaled SVG (pass) | spec §4A.4 #3; brief build 16, test 14 |
| R2-7 (NIT) | `:258` jq precedence; CORPUS/22 header globs; LEAD caption | Folded: command parenthesized and re-run (prints `f8886427…d60f`); CORPUS/22 `:3` names `results/d1_predictor_map_result.json` and `results/d1_concentration_sweep_result*.json` (4 files), so 5 of 18 d1 files match; §11.2 defines header-glob expansion (only `results/…` paths; `logs/d1_*` ignored) with a fixture; LEAD caption is "promising under this test; see replication" | spec §3.9, §3.10, §11.2, §5 item 1 |
| R2-close | Add a rendered-colour assertion | Folded: one chip per class; only `pass` computes green | brief test 4 |

Round 2 counts: 8 items (3 BLOCKING, 3 SHOULD, 1 NIT, 1 closing ask): 8 folded, 0 rejected. Astra confirmed the three round-1 partial rejections (V1, V9, V14) hold.

## Round 3: Astra delta review 2 (`results/labviz_v2_spec_astra_delta2.md`, FIX-FIRST)

Verified at 2026-10-08 with `jq`, `sed`, `grep`, `shasum` (no python needed this round).

| ID | Finding | Disposition | Where |
|---|---|---|---|
| R3-1 (BLOCKING) | Test command sets no `TMPDIR`; `test_labviz.py:202`, `:224`, `:269`, `:280` use `tempfile.TemporaryDirectory()` (verified) | Folded: `mkdir -p /private/tmp/labviz-review/test-tmp`; the only test command now sets `TMPDIR=/private/tmp/labviz-review/test-tmp`; a test asserts `tempfile.gettempdir()` is under it; `test-tmp/` named in the allowed scratch directory | brief rules 5, 7 |
| R3-2 (BLOCKING) | Time-only ordering needs timestamps the records lack | Folded: verified `.losses[0]` = `{"step":10,"loss":7.706562042236328}`, `.step_seconds[]` are durations, `results/c10w_oracle_logs/p1-eval.log:2` = `STAGE_EXIT=0`, gate `at` carries an offset (`"2026-10-07T22:22:29-06:00"`). Timestamped events sort by UTC-normalised time, then source path, then line or array index; untimestamped events go in a separate track in source/step order, labelled "time not recorded"; no time inferred from durations, names or mtimes; fixtures for real losses and markers, equivalent timezones and index ties | spec item d; brief test 24 |
| R3-3 (SHOULD) | Population pointer vs leaf schema | Folded: population derivations have no `inputs`; `population` is schema metadata `{file, path}` (whitelisted, no `value`); the verifier resolves the full operand list in `scales.json`, validates every operand leaf (with `scales.json`'s own `sources[]`) and recomputes from it alone; must-fail fixtures: a removed population member and a wrong maximum. The example card was updated and re-verified (JSON parses; 34 JSON-source leaves OK, 7 pointing at uncreated Lab View tables; 12 hashes OK); `c10h_anyedit_pilot.json` left the card's `sources[]` because no card leaf cites it any more | spec §6; brief test 20 |
| R3-4 (SHOULD) | Missing acceptance cases | Folded: Compare refuses a changed answer for the same subject and different fact populations (C10's 24 vs R5's 16-row `NOVEL_single`, verified); missing or non-finite gate inputs show no reference line and no glyph; saved pictures checked at 600 px (builder records picture width and text pixel sizes; 9pt in a 5.1-inch figure, `render.py:18`, `:61`, must fail); D1 header-glob test asserts the resulting context: `corpus:22`, `dec:D-D1-1` (`CORPUS/22…:3`, `⟨D-D1-1@0db8d819⟩`), experiment missing ("no registry row names this record"), never `exp:B1-size-term` although registry `:19` cites "CORPUS/22 (B1 §)". §11.2 rule 2 now states that a CORPUS-header match yields a documentary context, not an experiment | spec §4A.2, §11.2; brief tests 5, 18, 27, 28 |
| R3-5 (NIT) | Canonical-control citation | Folded: `c10w_oracle_read.py:403` (verified: `gates(c, p["recipes"]["closedform"]["arms"][A7], p["u"][A7])`) for the canonical control; `:361` kept for ordinary A7 | spec §5 item 3 |

Round 3 counts: 5 findings (2 BLOCKING, 2 SHOULD, 1 NIT): 5 folded, 0 rejected. A brief edit briefly dropped test 26 (a `$1`-then-digit substitution); it was restored from the round-2 text and the 1–28 test numbering re-checked.
