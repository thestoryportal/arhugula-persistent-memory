VERDICT: FIX-FIRST

1. **BLOCKING — The run-card contract cannot pass its own tests.** Spec §6, lines 507–595; brief test 1. The example contains bare numbers (`index:0`, `layer:8`), document citations without jq paths, derived leaves without inputs/rule sources, and rounded values where exact equality is required. For example, the recorded layer-8 write is `16.31455421447754`, not `16.31`. **Change:** define separate JSON-source, document-source, derived and missing leaf types; explicitly whitelist structural metadata; preserve full recorded precision and round only during rendering. Validate each type separately. Hash every source used, including reader records and curated tables.

2. **BLOCKING — A specified display attaches B0’s statistic to B.** Spec item 8, lines 440–445; brief test 7. `run.json:.readings.B.spearman_G_edge` is **−0.3162875387734472**; **−0.47912964570281436 belongs to B0**. **Change:** show −0.316 for B and test both recipes independently. More generally, require label/gate joins to match run identity, recipe, arm, seed and replicate, checking recorded hashes where available (`run.json` contains `pass_sha256`). Add a wrong-reader fixture whose counts happen to match: leaf equality alone cannot detect that misassociation. Specify which C10U reading applies: the frozen and after-v2 files disagree on V2’s direction.

3. **BLOCKING — Context rules do not implement the promised coverage.** Spec §11.2, lines 778–795; brief tests 10/12. Registry line 58 names `results/c10u_mint2/r3/`, not the entire family, and its **first D-ID is `D-C10r-rulings-12`**, not `D-C10u-mint2`. Registry lines 19/25 contain brace expressions rather than literal paths. Furthermore, source lines contain `C10`/`§8.9`, not namespaced identifiers such as `cond:C10`; `era:t-branch` is curated. **Change:** define path-pattern expansion and exact experiment-ID parsing; select the experiment’s decision explicitly; resolve ties as unknown; distinguish direct edges from curated/derived edges with cited inputs. Add fixtures for these actual rows, ambiguous basenames and unmatched historical attempts. Separate current status from historical framing.

4. **BLOCKING — Label and gate semantics remain builder decisions.** Spec items 1/3 and §10.1–2; brief build items 5/7. Colour mappings require sign-off but are absent. Only one gauge is tested. C10W G4 requires **every training frame**, and G7 requires the matched shuffled control (`C10W_ORACLE_PREREG.md:354–357`); C10V and C10W also use different perplexity references. **Change:** supply reviewed, version-bound label/gate tables with reference selection, comparator, applicability and missing-value behavior. Test every supported gate, boundary and mismatch. Display recorded booleans; identify arithmetic checks as derived and leave missing recorded outcomes unknown. Never promote a configuration PASS into program success.

5. **BLOCKING — Resolve the brief’s execution contradictions.** Brief lines 37–42 allow no files outside two directories, but line 121 requires `results/labviz_v2_codex_impl.md`. Spec line 514 adds `built_utc`, while brief test 15 requires byte-identical rebuilds. **Change:** explicitly allow the report; define deterministic timestamp behavior; distinguish the recorded-event scrubber from the excluded Phase-3 player. Add exact-content checks for both exempt command lines and the unchanged launcher, plus tests against child Python launches. The exemption strings themselves are correct; preserve them.

6. **BLOCKING — Recorded stimulus text is incorrectly treated as unavailable.** Spec §3.6 and item a say held-out text is recorded only in C10W and prescribe transcription for older records. `results/c10e_bandknob.json:.stimulus` already contains `CANON` and `PTEST`. **Change:** prefer recorded stimulus, then a verified transcription, otherwise missing. Bind template **order and role**, not just string occurrence; use the same identity checks for hparams and model structure. Add a test with permuted templates: today’s text-search test would accept mislabelled hit columns.

7. **SHOULD — Comparison needs an eligibility contract.** Spec item 5 derives “only left/right” counts without defining alignment. **Change:** join by subject, target, template and scoring kind; reject incompatible populations, changed answers and teacher-forced/free-answer comparisons. Test shuffled rows and differing templates. Keep absolute/relative/ratio units separate, and distinguish applied writes from predictions, injection measurements and exploratory writes when choosing scales.

8. **SHOULD — Sandbox leakage prevention needs an explicit execution path before Phase 4.** Spec §12.1/§12.3 promises the existing harness while forbidding protected questions. But `c10e_bandknob.py:491` calls `eval_arm`, which evaluates `PTEST` at lines 363–365. **Change:** approve a dedicated sandbox evaluator using only its sealed question set; forbid the production scoring path. Test the actual prompts reaching generation, teacher forcing, observers and logs—not merely template-string overlap. Record question-set hashes and all tries; separately review near-duplicate phrasings. Later preregistration does not erase adaptive exposure to the same facts or locality instruments.

9. **SHOULD — Sandbox scheduling and restoration need stronger Phase-4 admission gates.** Spec §12.4 checks idleness at startup; `c10w_p2_gate.py:43–54` is a process snapshot, not an atomic reservation. Idle timeout does not bound an active try or queue. §12.1 hashes only selected matrices after normal completion. **Change:** require exclusive scheduler ownership through teardown, science-priority queue cancellation, per-try runtime/resource bounds and request-time admission. Restore in failure paths; verify all parameters/buffers and reset hooks, RNG, caches and mode before reuse, or discard the worker. Sign off control types, finite ranges, layer ordering/combinations and cache identities. Test timeout, exception, concurrent launch and out-of-scope mutation.

10. **SHOULD — Screenshot criteria partly measure appearance, not usability.** Spec §4A.4–5; brief tests 11/13. Screenshots cannot establish tap counts, URL-state persistence or payload; computed font size misses canvas text and transformed SVG. The required 360px layout is never rendered. “Two keystrokes” cannot generally identify an experiment. The whole-page C10 blacklist also conflicts with the persistent current-status strip and legitimate connections. **Change:** scope vocabulary checks to run/model content; add scripted navigation and selection tasks, 360px and zoom cases, keyboard/touch checks and Safari/WebKit coverage. Measure rendered text, composited contrast, target rectangles and initial loaded bytes. Check chart/focus contrast as well as text.

11. **SHOULD — Qualify replay fidelity and granular coverage.** Spec §4, §7.5 and item c. Matching final counts cannot establish historical internal trajectories; top-16 MLP units are a summary, not all elements. Item c locates the edit “at” the subject position, although the resulting matrix change acts at every token (`C10V_LAYERPICK_PREREG.md:50`). **Change:** always say “re-creation; recorded outcomes matched,” retain NOT EVIDENCE on exports and cards, and label attention-pass differences separately. Describe subject position as the key-extraction location. Mark exact historical internal playback unavailable; sampled internal summaries are REPLAY/NEW. Add EXPLORATORY to the global evidence-status schema and prevent sandbox values entering scientific badges, gates or scales.

All ten items, four additional asks, historical context, usability and sandbox have destinations. NOW is broadly justified for recorded summaries; NEW/REPLAY is appropriate for internal observations. “Nothing is NOT FEASIBLE” overstates recoverability of historical detail.

Claim checks below used permitted read-only commands. No Python, model, browser or tests ran; no files were changed. Live inventory differences are snapshots, not necessarily original-author errors.

| # | Spec claim | Check: source/path or command | Result |
|---|---|---|---|
| 1 | C10V decision ID | `jq '.decision_id' results/c10v_layerpick/pass1.json` | **OK:** `D-C10v-layerpick` |
| 2 | C10V model/revision/device | Same file, `.model` | **OK:** Qwen2.5-3B, `3aab1f19…`, float16, mps |
| 3 | Fingerprint and LAW#5 pass | Same file, `.fingerprint.ok,.law5.ok,.law5.standing` | **OK:** true/true; standing deltas 0.0003/0.03 |
| 4 | Two context groups | Same file, `.ctx` | **OK:** identity group plus five prefixes |
| 5 | Four recipes, all bands 4–8 | Same file, `.recipes` keys and each `.band` | **OK:** A/B0/B/Bshuf; all `[4,5,6,7,8]` |
| 6 | A7 counts 11/12/12/10 | Same file, each recipe’s `.arms.A7_coined_coined` | **OK:** all out of 72 |
| 7 | B canonical 7/24 | Same file, `.recipes.B.arms.A7_coined_coined` | **OK:** 7/24 |
| 8 | Described-as A/B0/B/Bshuf | Same file, respective `.locality_described_as` | **OK:** 90.0/90.11/86.17/87.37 |
| 9 | B0 writes only layer 8 | Same file, `.recipes.B0.delta_norms.A7_coined_coined` | **OK:** sole key `"8"`; norm 55.42212677001953 |
| 10 | B writes 4.85/16.13/27.69/9.71/16.31 | Same file, `.recipes.B.delta_norms.A7_coined_coined` | **OK:** stated rounded norms for layers 4–8 |
| 11 | First B fact | Same file, `.recipes.B.detail.A7_coined_coined[0]` | **OK:** Zorbland, Vindex Vask, 4 tokens, three true hits |
| 12 | 192 residual-ratio paths | `jq '[paths\|select(.[-1]=="rho_per_prompt")]\|length' results/c10v_layerpick/pass1.json` | **OK:** 192 |
| 13 | B/B0 labels and binding counts | `results/c10v_layerpick/run.json:.readings` | **OK:** both NULL, binding 12; Bshuf NULL-CONTROL-ONLY, 10 |
| 14 | B described-as gate fails | Same file, `.readings.B.locality_gates` | **OK:** described_as false; other four true |
| 15 | B0 write ratio/correlation | Same file, `.readings.B0` | **OK:** 0.6435379892895584 / −0.47912964570281436 |
| 16 | Item-8 B display correlation −0.479 | Same file, `.readings.B.spearman_G_edge` | **WRONG:** −0.3162875387734472; −0.479 belongs to B0 |
| 17 | B layer-8 summary | Same file, `.readings.B.by_layer["8"]` | **OK:** facts 2, para_full 0, edges_3of3 0 |
| 18 | Selector dimensions and first row | `results/c10v_layerpick/step0.json:.G_table` | **OK:** 24×5; rounded row 0.832/0.932/0.948/0.922/0.924 |
| 19 | Margins/repeat interpretation | Same file plus `c10v_layerpick_read.py:71–92` | **OK:** 2×24; first margin 0.01560226080429905 |
| 20 | Selector READY/reproduced | Same file, `.status,.map_reproduced,.delta,.concentration` | **OK:** READY/true/0/15 |
| 21 | C10W training 40 losses/400 times | `results/c10w_oracle/p1_*/train/A7_coined_coined_s0_r16.json` | **OK:** step 10 loss 7.706562; step 400 loss 0.000411302 |
| 22 | Fit 480/480, 434 hashes each side | Same file, `.fit`, `.frozen_parameter_hashes_before`, `.frozen_parameter_hashes_after` | **OK:** 480/480; 434/434; unchanged true |
| 23 | Adapter training time 523.35s | Same file, `.wall_seconds` | **OK:** 523.3518295418471 |
| 24 | P1 recipe/count samples | `results/c10w_oracle/p1_*/eval.json:.recipes` | **OK:** three named recipes; oracle 70/72, closedform 9/72, canon 2/72 |
| 25 | Oracle locality/MMLU samples | Same file, `.recipes.oracle_p1.arms.A7_coined_coined` | **OK:** 86.72; L3 30/30; ppl 21.755→21.081; quiz 118/200, net loss 4 |
| 26 | Recorded generated text sample | Same arm, `.extra.generated` | **OK:** 72 entries; visit-template sample `" Vindex Vaskul,"` exists |
| 27 | P1 verdict incomplete | `results/c10w_oracle/p1_*/verdict.json` | **OK:** final_label null, INCOMPLETE, OPEN/BLOCKING, f1_changed false |
| 28 | Six P2 train records | `jq` over `results/c10w_oracle/p2_*/train/*.json` | **OK:** six; each PASS, 40 losses, frozen unchanged |
| 29 | C10U multi sample | `results/c10u_mint2/r3/F_r1_multi_snone.json:.arm` | **OK:** 14/72, binding 14, described_as 88.22; 24 curve rows |
| 30 | 119 files with para_full_hits | Spec §3.9 `grep -rl` command, excluding `/labviz/` | **OK:** 119 |
| 31 | 78 files with delta_norms | Same command with `"delta_norms"` | **OK:** 78 |
| 32 | 78 files with locality_described_as | Same command with `"locality_described_as"` | **WRONG currently:** 79 |
| 33 | Model dimensions/config | Pinned Qwen `config.json`, fields listed in §3.5 | **OK:** 36/2048/11008; heads 16/2; silu; epsilon 1e−6; vocab 151936; tied embeddings |
| 34 | Hparams citations/defaults | `configs/hparams/qwen25_3b_memit_hparams.json:2–18` | **OK:** layers, subject_last, down_proj, norm/tied head and sandbox defaults match |
| 35 | Harness source hash | `shasum -a 256 experiments/track_c/c10e_bandknob.py`, compared with pass1 identity | **OK:** `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` |
| 36 | Held-out text recorded only in C10W | `jq '.stimulus\|{CANON,PTEST}' results/c10e_bandknob.json` | **WRONG:** older C10E records both canonical and three rewordings |
| 37 | 54 registry rows and field counts | `grep -c '^\| \*\*'`; `awk -F'\|'` over those rows | **OK:** 54; NF 10×36, 9×16, 11×1, 12×1 |
| 38 | Machine registry has 20 rows | `jq 'length' docs/experiment_registry.json` | **OK:** 20; top level is an array |
| 39 | Goal 61/72 and 15 evaluation entries | `docs/c10_scoreboard.json`; `docs/c10_evaluations.json` | **OK:** 61/72; 15; final ID evaluation-14 |
| 40 | Two Lab View exemptions | `tools/c10w_p2_gate.py:25–26`; `tools/labviz_serve.sh:7,10,15` | **OK:** exact stated builder/server arguments; regex permits executable path prefixes |
| 41 | Gauge floor citation | `docs/C10V_LAYERPICK_PREREG.md:74` | **OK:** same-process A−3; 90−3=87 |
| 42 | §4A.3 small-text audit | `tools/labviz/style.css:17,19,26,36,47` | **OK:** .8rem/.8rem/.78rem/12px/.9rem |
| 43 | §4A.3 layout audit | Same file, `:11,33,41–42,50` | **OK:** 1200px container, 570px tower, fixed goal positions, two-column grid |
| 44 | §4A.3 image-font audit | `tools/labviz/render.py:18,61,78,94,102,105` | **OK:** 5.1-inch figure; 9/8/6pt settings |
| 45 | 1,438 cards and exact site bytes | `grep -o 'class="run"' …/index.html \| wc -l`; `wc -c` | **WRONG currently:** 1,440; index 4,059,160 bytes; data.js 2,582,147 |
| 46 | Module script/single picker audit | `tools/labviz/index.html:6,33` | **OK:** module script and one select; browser behavior not executed |
| 47 | §11.3 C10 hardcoding | `build.py:193,202,230–236,494–496`; `render.py:28–35,114–121`; `index.html:36` | **OK:** listed wording, score selection, log filter and 72-scale present |
| 48 | Six-layer map cited at :10–17 | `docs/SPEC_E2E_GROUND_TRUTH.md:10–18` | **WRONG range:** sixth layer, Orchestration, is line 18 |
| 49 | C10 condition links §8.9 | `docs/F1_DETERMINATION.md:71` | **OK:** both appear in the condition row |
| 50 | Caches cover layers 4–12 | `ls covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/` | **OK:** nine down_proj cache filenames; contents not opened |
| 51 | No C10Z output/telemetry implementation yet | `ls results/c10z_astra`; specified `grep -nE` on arms source | **OK:** directory absent; no telemetry-name matches |
| 52 | C10Z telemetry prereg citations | `docs/C10Z_ASTRA_PREREG.md:467–476,554–604` | **OK:** opt-in, four kinds, corrected inertness scope, timing fields and layer indexing |