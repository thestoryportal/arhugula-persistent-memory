# D-C10z-astra — Codex build report

**Model:** GPT-6 (Codex; the runtime does not expose a more specific model identifier). **Effort:** inherited session setting; its exact value is not exposed. **Independent reviewer:** GPT-6-astra, high effort.

**Date:** 2026-10-07. **Decision-ID:** D-C10z-astra. **Build result:** PASS for the authorized model-free build: the fresh selftest exited 0, ran 50 tests in 25.627 seconds, and printed `C10Z_ASTRA_SELFTEST_PASS tests=50`. The final independent source review returned **PROCEED — model-free build scope**. Native/model execution and scientific acceptance gates remain **UNVERIFIED**.

The replacement brief at `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/codexi_c10z_build_brief.md` governs this report. The earlier draft was discarded. The implementation consists of the four files it names, plus this report. Existing `c10w_*` work is untouched. No model, tokenizer, MPS or GPU path was executed; no stage command below was run. The only test program executed was the authorized CPU selftest.

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`. Branch: `worktree-c10k-route-a`. Both were verified at entry and again at closeout. Git was used read-only. The frozen prereg, harness and engine remain unchanged.

## Specification and test-first evidence

Specification: `docs/C10Z_ASTRA_PREREG.md`, FROZEN v2.2, commit `35db59b`; its full text was read before implementation. Citations below are to that file's current, unchanged line numbers.

The selftest was written before the driver, reader and shell wrapper. Its first run failed with **39 tests and 51 failures**, including missing-implementation assertions. After the initial implementation, **39 tests and 6 failures** exposed inconsistent fixture evidence; the fixtures were corrected to satisfy the independently checked record invariants. Later source-review findings received failing regressions before their fixes, including a **50-test run with 3 failures** at the omission, closeout and TTL boundaries. The final fresh run below passes all 50 tests. These are build checks, not a model experiment.

The independent numeric references are in the selftest and do not call the production routine whose answer they check: scalar/loop joint-matrix assembly, ridge and column updates, preferred-direction calculations, null-space floor/median arithmetic, and fp32-add/fp16-store rounding. Import guards prevent the selftest from importing the model-bearing harness, transformers or datasets (`experiments/track_c/c10z_astra_selftest.py:24`). The test never constructs the runtime-only `Session`.

## Prereg item → test → implementation

In this table, `c10z_astra_arms.py`, `c10z_astra_read.py` and `c10z_astra_selftest.py` are all under `experiments/track_c/`; `run_c10z_stage.sh` is under `tools/`. Each citation gives a file and its actual line anchor. CPU tests check the public numeric/reader/transport contracts on synthetic tensors and records. Model-dependent methods are additionally inspected in source; their native behavior is UNVERIFIED.

| Preregistered item | Test and source anchor | Implementation anchor |
|---|---|---|
| LAW#3 must run/read before new-writer observation or candidate work; exact inclusive A7 and A1/A2 envelope (§2.6, :120–125; V4 :217) | `c10z_astra_selftest.py:459` tests para-full 4/5/18/19, canonical 4/5/10/11, para-first 41/42/59/60 and A1/A2 67/68; ordering at `:658` | `c10z_astra_arms.py:129` (Gates), `:793` (stage0); `c10z_astra_read.py:183` rechecks raw counts |
| Pristine pin, unchanged source identity, complete manifest and fresh immutable attempts (:121, :137, :215–216, :224) | `c10z_astra_selftest.py:386` rejects altered populations/manifest inputs; `:765` verifies frozen prereg, immutable JSON output and no model-bearing imports | `c10z_astra_arms.py:296` source hashes, `:324` fingerprint/pristine import boundary, `:1144` manifest, `:1177` process-2 validation, `:1192` comparison before baseline; `c10z_astra_read.py:371` |
| Wrapper delegation during standing LAW#5, no inherited harness knobs, no premature candidate or out-of-order stage (:118, :127–133; V2/V9 :216/:222) | `c10z_astra_selftest.py:658`; `:579` invalidates each required V* gate; runtime wrapper inspected | `c10z_astra_arms.py:65`, `:138`, `:144`, `:640`, `:698`; `c10z_astra_read.py:456` |
| All 36 layers restored in finally, restore hook last, initial hook registry restored before eval (:64, :129; Z6 :153; V3 :216) | `c10z_astra_selftest.py:741` exercises synthetic full-layer restore after action/write/eval/hook exceptions and a nonempty initial registry; `:436` tests terminal close failure | `c10z_astra_arms.py:153`, `:381`, `:396`, `:401`, `:409`, `:640`, `:692`, `:1277` |
| Six fixed views, ordered IDs, right-padded 144-row batch, valid requirement positions, native head/cache settings (:72–73, :99–101, :137) | `c10z_astra_selftest.py:386`, `:347`, `:398`; reader population invariants on complete synthetic records | `c10z_astra_arms.py:433`, `:454`, `:1116`, `:1151`; `c10z_astra_read.py:135`, `:371`, `:421` |
| CPU float64 G/preferred directions, null-space D, nonsymmetric joint A and ridge (:74–78) | `c10z_astra_selftest.py:681` independent NumPy/scalar assembly and solve; `:719` independent floor and even median; `:398` scalar active control | `c10z_astra_arms.py:162`, `:170`, `:182`, `:194`, `:931`, `:967` |
| Target-excluded competitor, deficit, deterministic SemCon ranking, token count once per fact (:73, :75) | `c10z_astra_selftest.py:719`, `:347`, `:398` | `c10z_astra_arms.py:210`, `:221`, `:240`, `:254`, `:529` |
| Exact fp32 add / fp16 store, fixed S, ≤10 writes and additional final observation (:79–80) | `c10z_astra_selftest.py:681`, `:719`, `:398`; writer loop inspected | `c10z_astra_arms.py:264`, `:705` |
| Z0 spread, Z1 native head reconstruction, Z2 evaluator agreement including zero-checked refusal (:147–149; V5 :218) | `c10z_astra_selftest.py:347`, `:398`, `:579`, `:386`, `:416` | `c10z_astra_arms.py:859`, `:977`, `:1127`; `c10z_astra_read.py:192`, `:242`, `:456` |
| Z3 identity through full writer, Z4 assembly identity, Z5 footprint, Z7 independent locus and nonzero native reference (:150–155) | `c10z_astra_selftest.py:681`, `:398`, `:579`; actual model controls source-inspected, not executed | `c10z_astra_arms.py:535`, `:977`, `:1019`, `:1048`, `:1116`, `:1127`; `c10z_astra_read.py:192` |
| V6 finite science; V7 all cached-layer Spearman; V8 G Cholesky (:157, :219–220) | `c10z_astra_selftest.py:681`, `:579`, `:765` | `c10z_astra_arms.py:894`, `:967`, `:1303`; `c10z_astra_read.py:43`, `:192`, `:456` |
| Full binding decomposition, F0 separately in six views, F1 all fact/view/depth/subject cells, relation and subject-free raw probes (:161–165) | `c10z_astra_selftest.py:386`, `:506`, `:560`, `:324` reject missing/inconsistent raw populations and forged summaries | `c10z_astra_arms.py:560`, `:584`, `:602`, `:635`, `:765`, `:785`, `:1215`; `c10z_astra_read.py:248`, `:261`, `:282`, `:345`, `:421` |
| FIT exact integer comparison 20m≥19M; positive-identity and actual canonical 22/23; strict >0 and inclusive ≥5 (:230–234) | `c10z_astra_selftest.py:480`; malformed/forged fit evidence `:324` | `c10z_astra_read.py:74`, `:82`, `:135`, `:566` |
| Exhaustive disjoint T1–T5 and U, a=5…18, n=0…72, both side-gate states; n18/19/29/30, g9/10 (:249–261) | `c10z_astra_selftest.py:493` independently enumerates the partition | `c10z_astra_read.py:314`, `:566` |
| G1–G5 equality and next failing value; G4 28/29; G7 hZ=hA+1 vs +2 for every individual cell; G0 A1/A2 67/68 (:239–245) | `c10z_astra_selftest.py:506` | `c10z_astra_read.py:261`, `:296`, `:566` |
| Z-band capacity quotient/remainder/cap; fit→capacity→locality→BAND decision order; all BAND numeric boundaries (:112, :282–286) | `c10z_astra_selftest.py:542`, `:719`, worked rows 15–21 at `:811` | `c10z_astra_arms.py:249`, `:254`; `c10z_astra_read.py:332` |
| W1 realized final fp16 relative-column norm; even-population median; .55 equality, zero-original-column cases (:210, :272) | `c10z_astra_selftest.py:560`, `:324`, worked rows 11/23 at `:811` | `c10z_astra_arms.py:275`, `:304`, `:1292`; `c10z_astra_read.py:67`, `:90`, `:121`, `:320` |
| Subject-free fact counted once across depths; A+1 equality/A+2 failure (:273) | `c10z_astra_selftest.py:560`, worked row 12 at `:811` | `c10z_astra_read.py:282`, `:320` |
| W2 any completed Z write >3600 s; equality passes, including stage-2 A1/A2/Z-band (:274) | `c10z_astra_selftest.py:560`, `:422` | `c10z_astra_arms.py:659`, `:692`, `:705`; `c10z_astra_read.py:566`, `:592` |
| K1/K2 exact survival, explicit causally correct NOT-RUN/NOT-EVALUATED; incomplete reproduction distinct from invalid records (:265–267) | `c10z_astra_selftest.py:605`, `:451`, `:422`, `:436` | `c10z_astra_arms.py:1252`, `:1263`, `:1366`, `:1474`; `c10z_astra_read.py:584`, `:592`, `:618` |
| R1 carrier/round identity and ≤1e-3 error, zero-delta rules; R2 difference 2/3; R3 disagreement 3/4; lower-label/qualifier union and LEAD/PARTIAL aggregation (:278–280) | `c10z_astra_selftest.py:605`, `:324`, `:422`, worked row 8 at `:811` | `c10z_astra_arms.py:279`, `:304`, `:318`; `c10z_astra_read.py:150`, `:614`, `:618`, `:640` |
| 5400-second stage-0–1 bound starts before import; immutable optional launch ceilings; separate stage-2 origins; stage-3 origin before process-2 import; earliest applicable deadline; projection refusal and actual expiration (:196, :225) | `c10z_astra_selftest.py:632`, `:338`, `:368` | `c10z_astra_arms.py:82`, `:324`, `:1335`, `:1366`, `:1436`; `c10z_astra_read.py:456`, `:658` |
| Synchronized stage-1 round 120/121 s; later completed stages retain original A7 round check (:198, :225) | `c10z_astra_selftest.py:362`, `:632`, worked row 24 at `:811` | `c10z_astra_arms.py:78`, `:705`; `c10z_astra_read.py:456` |
| Memory exactly 40 GiB total / 32 GiB driver, next byte fails; no float64 MPS (:190, :223) | `c10z_astra_selftest.py:632`, `:579`, `:681` | `c10z_astra_arms.py:73`, `:162`, `:390`; `c10z_astra_read.py:456` |
| Records round-trip through real strict writer; no silently reused pass/manifest; runtime HALT overrides earlier partial success (:137, :204, :224) | `c10z_astra_selftest.py:765`, `:324`, `:338`, `:368` | `c10z_astra_arms.py:43`, `:1228`, `:1342`, `:1366`; `c10z_astra_read.py:658` |
| One externally requested stage per invocation, continuity of process 1, verified terminal close and bounded failed-worker wait (§2.6) | `c10z_astra_selftest.py:658`, `:368`, `:436`; shell source inspection | `tools/run_c10z_stage.sh:3`; `c10z_astra_arms.py:144`, `:1366`, `:1436`, `:1474` |
| Every §3.6 worked input row, copied verbatim (:290–313) | `c10z_astra_selftest.py:784` (literal rows), `:811` (24 generated cases); row-22 full-reader rejection additionally at `:416` | Real `c10z_astra_read.py:592` / `:640`; conditional row-22 partition at `:566`. See Objections for the incompatible full-reader requirement. |
| Corrected premise: ρc is remaining residual; compute_z scores all targets while the weight solve uses subject-last keys (:28–29; requirement-map #9 :21) | Source/read-only premise, not a new measured result or numeric ASTRA gate | Unchanged `c10e_bandknob.py:181` and the frozen prereg; no alternative ρc readout or engine modification introduced |

## LAW#4 source reads and resulting seams

The following harness/engine seams were read with line numbers before authoring their callers. They are source evidence, not executed model evidence.

| Source read | Consequence in this build |
|---|---|
| `experiments/track_c/c10e_bandknob.py:67` (`tgt_ids`), `:71` (`first_tok`), `:83` (`js`), `:96` (`req`), `:101` (`predict`), `:109` (`full_seq_match`), `:121` (`string_match`), `:134` (`teacher_forced_pertok`) | Preserve leading-space target IDs, id-sequence prompt/prefix construction, unmodified greedy binding evaluation and its exact count population. |
| `experiments/track_c/c10e_bandknob.py:150` / `:155` (`snap_layers` / `restore_layers`) and `:458` (`run_recipe`) | Harness restoration covers only its 4–8 band; the new driver therefore snapshots/restores every one of the 36 down projections and verifies after each arm/finally. |
| `experiments/track_c/c10e_bandknob.py:166` (`compute_P`), `:181` (`my_edit`), `:415` (`run_law5`) | Recipe A and standing LAW#5 delegate to the original path. The wrapper uses the existing module-global seam and delegates under `_LAW5_DEFAULT_CTX`; no engine edit function implements ASTRA. |
| `experiments/track_c/c10e_bandknob.py:224` / `:259` (stimuli/locality), `:304` (`sentence_nll`), `:311` / `:319` (`axes_pre` / `axes_post`), `:342` (covariance hashes), `:358` (`eval_arm`) | Retain the exact arms, evaluator, locality axes and covariance provenance; attach additional raw probes after the LAW#3 gate. |
| `experiments/track_c/c10p_twopass_arms.py:30` (`FRAME_SUBJECTS`) and `:36` (`frame_probe`) | Use its six unedited subjects in each fitted view; native calls are not run in this build. |
| `memit_dry_run/memit/memit/memit_main.py:240` (`get_cov`), `:304` (`get_context_templates`); context-cache ordering in `execute_memit` at `:100` | Freeze the engine's identity-plus-five-template population, validate covariance/statistic provenance, and reload the same template file in process 2 before baseline. |
| `memit_dry_run/memit/util/nethook.py:19`, `:117`, `:361`, `:371` (`Trace`, `TraceDict`, module/parameter access); `memit_dry_run/memit/util/hparams.py:12` (`from_json`) | Use the unmodified TraceDict API for independent key capture and the installed hparams interface; record/check hook registries. |
| `tools/engine_fingerprint.py:39` | Call its existing fingerprint gate and require the pinned main-source digest and three `_cov_cpu` sites. |
| `.venv/lib/python3.11/site-packages/transformers/models/qwen2/modeling_qwen2.py:47` (MLP), `:220` (RMSNorm forward), `:231` (decoder; forward read through :279), `:470` (model forward), `:771` (LM-head forward), installed transformers 4.51.0 | Use the native fp16 module/cast order and full head shapes. The last-layer nonzero reference computes projection, residual addition, norm and head; model parity remains UNVERIFIED until an authorized run. |

## Implementation decisions

1. **Authority and validation (:204, :208, :224).** Frozen settings have one reader-side representation; the driver uses that representation. The reader recomputes FIT counts, probe-cell counts, binding decompositions, W1, H_out and cross-process evidence from raw rows and serialized final weights. Asserted booleans, counts or certificates cannot substitute for their evidence. HALT validation precedes all candidate labels.

2. **Native observation and independent nonzero reference (:73, :148, :155).** Freeze `use_cache=false` and `logits_to_keep=0`. Captures become CPU float32 at hooks; every solve/G operation is CPU float64. Maintain original competitors for fidelity/reference comparisons. Z7's independent control uses retained full layer-35 K and pre-MLP R, independently constructed fp16 W_ref and the full native projection/residual/norm/head. The diagnostic x+ΔWk approximation does not establish parity. A correct finite nonlinear lead change need not equal γ.

3. **Exact arithmetic and write authority (:74–80, :210, :272).** Use a nonsymmetric joint A, the stated ridge, an arithmetic even-population median for D and W1, fixed score/layer/neuron tie ordering, and one fp32 addition followed by one fp16 store per selected column per round. The last deployed fp16 weights, not intended summed updates, determine W1 and reproduction. Round count counts writes; the post-loop observation does not add a round.

4. **Output bytes and infinity (:137, :272, :278).** Store sorted selected-column identities and compressed `zlib-base64-fp16-le` old/new column snapshots. H_out hashes the canonical sorted (layer,column) list followed by the uncompressed final fp16 bytes; compression is not part of overlay identity. The reader independently decodes snapshots and checks footprint/count/hash/norm evidence. The mathematically required zero-original/changed-column +∞ ratio is represented by the explicit string `POSITIVE-INFINITY`; arbitrary nonfinite scientific JSON values still HALT. Zero/unchanged has ratio 0.

5. **LAW#3 and deferred baseline measurements (:120–125).** The baseline arm hook saves edited band weights and restores all 36 weights without running additional forwards. D, G, candidate observations and new probes remain behind the complete LAW#3 gate. Deferred baseline probes temporarily install the saved baseline snapshots; they do not repeat a baseline solve. Held-out keys/leads for transfer are read after the final candidate write and cannot tune a later update.

6. **Hook and restore closeout (:129, :152–153).** Record the full module hook registry, a superset of the named down-projection/norm modules. Assert registry parity before the original eval_arm call, after observation and after restoration. Each recipe/check restores in finally; restore_hook is last. Closeout errors HALT. A terminal K1 or stage-2 response waits for verified process close, so a late restore/close failure cannot publish success.

7. **Manifest and immutable inputs (:137).** Bind ordered requests/IDs/masks/shapes, model and pristine identity, all required tokenizer/hparams/screens/covariance inputs, complete engine identity, source/settings/versions/backend, and D dataset revision/rows/text hashes/nonpadding counts. Process 2 validates the same manifest and sources before baseline work, then compares loaded pristine/model/tokenizer/environment identities before its baseline. D and G files are copied byte-for-byte from the validated process-1 files, preserving their hashes across processes.

8. **One stage per shell invocation; one model lifetime per pass (:126–133).** Stage 0 launches an owned resident process 1. Stages 1 and 2 are separate calls submitting the next request to that same process. A fresh process 2 internally repeats stages 0–2 as the definition of external stage 3. Stage 3 requires clean K2 and verified closed process 1. The shell never chains stages or applies `set -e` to a multi-stage run. File heartbeat leases bound a failed-worker wait without a process-table probe or signal.

9. **Budget scope and publication (:196–198, :225).** Stage-0–1 origin precedes model import; idle time between its two calls counts. Stage-2/3 launch durations are positive, immutable, recorded inputs before process 1 starts; absent inputs refuse the corresponding expansion. Process-2 stage-3 origin precedes its import, stage-2 origins start separately on each entry, and the earliest active deadline governs. Positive recorded scheduling allowances cover unknown required components; measured anchors are whole-pass figures. Synchronize round and component timing, include validation/probes/serialization/restoration in projections, and enforce elapsed deadlines independently with a watchdog. Publication is serialized; terminal HALT evidence overrides an earlier passing stage record.

10. **Stage/replication omissions (:265–280).** Derive each NOT-RUN reason from the actual K1/K2 result or absent launch ceiling. A completed process-2 K1 stop retains its measured label; omitted-arm R1 is NOT-EVALUATED and adds REPRO-INCOMPLETE. A measured R1 failure on a common arm still adds NOT-REPRODUCIBLE, even if other arms are omitted. R1/R2/R3 are recomputed; numeric behavioral agreement does not replace artifact identity or the stored overlay hash. W2 applies to every completed Z write, including stage-2 arms and band attribution.

11. **Worked-row conflict (:149, :208, :311).** Preserve row 22's exact conditional classification in the real reader's classifier, and separately require the full reader to HALT on its contradictory observation/evaluator evidence. The frozen prereg is unchanged. The objection below documents why both requested full-reader outcomes cannot hold simultaneously.

## Independent review

A fresh GPT-6-astra reviewer ran at **high** effort using an explicit source/adversarial review prompt. Claude CLI authentication was probed read-only and returned `loggedIn=false`, auth method none, exit 1; consequently this was a GPT-family fallback review, **not an out-of-family Claude review**.

Initial design/implementation findings and the targeted rereview were addressed with regressions. The final review returned:

> PROCEED — model-free build scope. No remaining deterministic blocker found in the targeted rereview.

Its residual checks covered W2 on all arms, incomplete replication alongside measured R1 failure, watchdog publication, causal omission validation and K1 waiting for verified close. The reviewer ran neither tests nor model code. The final fresh CPU run below fulfills its model-free completion condition. Its required row-22 disclosure is retained.

## Selftest command and full PASS output

Actual invocation (from the verified worktree):

```sh
/opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10z_astra_selftest.py
```

The underlying test command is exactly `.venv/bin/python -B experiments/track_c/c10z_astra_selftest.py`; rtk is the required command wrapper. Exit status: **0**. Complete unabridged output:

```text
test_00_implementation_exists (__main__.SpecTests.test_00_implementation_exists)
Prereg :204: actual driver, reader and stage wrapper exist. ... ok
test_band_boundaries_ordered (__main__.SpecTests.test_band_boundaries_ordered)
Prereg :112, :284: fit -> capacity -> locality -> three exhaustive BAND rows. ... ok
test_budget_origins_prestart_deadlines_round_memory (__main__.SpecTests.test_budget_origins_prestart_deadlines_round_memory)
Prereg :190, :196–198: 5400 seconds, scopes, unknown allowance, exact memory. ... C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 5400.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.0}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 1.0, "ceiling_s": 5400.0}}}
C10Z_PROJECTION {"origins": {"stage01": 100.0}, "ceilings": {"stage01": 5400.0, "stage2": 60.0, "stage3": 6000.0}, "components_s": {"remaining": 1.001}, "scopes": {"stage01": {"elapsed_s": 5399.0, "remaining_s": 1.001, "ceiling_s": 5400.0}}}
ok
test_completed_stage2_keeps_stage1_round_ceiling (__main__.SpecTests.test_completed_stage2_keeps_stage1_round_ceiling)
Prereg :198, :225: completed stage2 still checks stage1 A7 timing. ... ok
test_cpu_joint_algebra_independent_reference (__main__.SpecTests.test_cpu_joint_algebra_independent_reference)
Prereg :76, :78–80, :151: nonsymmetric solve, scalar-loop independent assembly. ... ok
test_cpu_null_weight_margin_fp16_selection (__main__.SpecTests.test_cpu_null_weight_margin_fp16_selection)
Prereg :75, :77–80, :210: independent floor/median, excluded competitor, fp32 add. ... ok
test_fit_count_boundaries (__main__.SpecTests.test_fit_count_boundaries)
Prereg :210, :230–234: exact integer FIT, positive 22/23, canonical 22/23. ... ok
test_fixed_competitor_and_native_reference_contract (__main__.SpecTests.test_fixed_competitor_and_native_reference_contract)
Prereg :155: native gathered logits, fixed competitor, finite last-layer path. ... ok
test_json_real_writer_and_frozen_sources (__main__.SpecTests.test_json_real_writer_and_frozen_sources)
Prereg :137, :204, :219, :224: round-trip, immutable outputs, finite science. ... ok
test_k1_k2_omissions_and_replication (__main__.SpecTests.test_k1_k2_omissions_and_replication)
Prereg :265–280: valid early stops != V12, lower labels, R2/R3 boundaries. ... ok
test_known_answer_scalar_and_native_fp16_reference (__main__.SpecTests.test_known_answer_scalar_and_native_fp16_reference)
Prereg :155: independent scalar A/ridge/columns and native finite reference. ... ok
test_law3_both_sides (__main__.SpecTests.test_law3_both_sides)
Prereg :123, :217: all inclusive envelope edges, and A1/A2 67/68. ... ok
test_manifest_population_and_post_instrument_tampering (__main__.SpecTests.test_manifest_population_and_post_instrument_tampering)
Prereg :137, :147–155, :224: complete inputs, missing controls, post-write evidence. ... ok
test_omission_reasons_follow_K1_K2 (__main__.SpecTests.test_omission_reasons_follow_K1_K2)
Prereg :265–267: every unrun expansion is recorded with its actual stopping reason. ... ok
test_ordering_and_stage_transport (__main__.SpecTests.test_ordering_and_stage_transport)
Prereg :120–125, :127–133, :218: no early observation, ordered one-stage requests. ... ok
test_raw_evidence_over_asserted_fit_write_and_repro (__main__.SpecTests.test_raw_evidence_over_asserted_fit_write_and_repro)
Prereg :224, :230, :272, :278: reject forged counts, bytes and certificates. ... ok
test_restore_finally_and_nonempty_hook_registry (__main__.SpecTests.test_restore_finally_and_nonempty_hook_registry)
Prereg :129, :152–153: all36 tensors restored after write/eval/hook failures. ... ok
test_side_gate_boundaries_and_populations (__main__.SpecTests.test_side_gate_boundaries_and_populations)
Prereg :239–245: every side gate equality passes, next value fails; no pooling. ... ok
test_table_T_exhaustive_and_integer_boundaries (__main__.SpecTests.test_table_T_exhaustive_and_integer_boundaries)
Prereg :249–261: independent exhaustive T1–T5, n18/19/29/30 and g9/10. ... ok
test_terminal_K1_wrapper_waits_for_close_error (__main__.SpecTests.test_terminal_K1_wrapper_waits_for_close_error)
Prereg :129, :265: terminal K1 response waits for verified close, propagates error. ... ok
test_terminal_halt_overrides_earlier_complete_pass (__main__.SpecTests.test_terminal_halt_overrides_earlier_complete_pass)
Prereg :196, :225: stage2 hard halt invalidates earlier stage1 pass. ... ok
test_transport_wait_publication_and_worker_failure (__main__.SpecTests.test_transport_wait_publication_and_worker_failure)
Prereg :126–139, :196: resident continuity, completed response, bounded failed wait. ... {"label": "PARTIAL", "next_stage": 2}
ok
test_ttl_every_Z_arm_and_incomplete_actual_repro_failure (__main__.SpecTests.test_ttl_every_Z_arm_and_incomplete_actual_repro_failure)
Prereg :267, :274, :278: any Z TTL, and omitted plus failed R1 retain both flags. ... ok
test_w1_even_median_w2_subject_free (__main__.SpecTests.test_w1_even_median_w2_subject_free)
Prereg :210, :272–274: even median, exact W1/W2, depth OR and +1 boundary. ... ok
test_worked22_validity_precedes_conditional_label (__main__.SpecTests.test_worked22_validity_precedes_conditional_label)
Prereg :149, :208, :311: contradictory raw canonical evidence HALTs before labels. ... ok
test_worked_01 (__main__.SpecTests.test_worked_01)
Prereg :290: n = 18, FIT ... ok
test_worked_02 (__main__.SpecTests.test_worked_02)
Prereg :291: n = 18, U (φ_μ = 0.80) ... ok
test_worked_03 (__main__.SpecTests.test_worked_03)
Prereg :292: n = 21, g = 9 (a = 12) ... ok
test_worked_04 (__main__.SpecTests.test_worked_04)
Prereg :293: n = 25, a = 16, g = 9 ... ok
test_worked_05 (__main__.SpecTests.test_worked_05)
Prereg :294: n = 22, g = 10, gates, FIT; stage 2 G0 holds, W1 0.4 (above the paper's SemCon range; reported, not a qualifier) ... ok
test_worked_06 (__main__.SpecTests.test_worked_06)
Prereg :295: n = 22, g = 10, G7 fails 3 (view, fact, depth) gates ... ok
test_worked_07 (__main__.SpecTests.test_worked_07)
Prereg :296: n = 29, gates, FIT; stage 2 Z-A1 = 67/72 ... ok
test_worked_08 (__main__.SpecTests.test_worked_08)
Prereg :297: n = 30, gates, FIT, W1 0.3; p2 n = 29, both processes clean ... ok
test_worked_09 (__main__.SpecTests.test_worked_09)
Prereg :298: n = 31, gates, U (φ_0^id = 22) ... ok
test_worked_10 (__main__.SpecTests.test_worked_10)
Prereg :299: n = 24, g = 6, U ... ok
test_worked_11 (__main__.SpecTests.test_worked_11)
Prereg :300: n = 33, gates, FIT, W1 1.4 ... ok
test_worked_12 (__main__.SpecTests.test_worked_12)
Prereg :301: n = 26, gates, subject-free hits A + 4 ... ok
test_worked_13 (__main__.SpecTests.test_worked_13)
Prereg :302: recipe A A7 = 19/72 ... ok
test_worked_14 (__main__.SpecTests.test_worked_14)
Prereg :303: Z3 (d): one greedy generation differs ... ok
test_worked_15 (__main__.SpecTests.test_worked_15)
Prereg :304: stage 2: n = 26, Z-band FIT, gates clean, capacity matched, n_b = 23 ... ok
test_worked_16 (__main__.SpecTests.test_worked_16)
Prereg :305: stage 2: n = 26, Z-band clean, n_b = 20 ... ok
test_worked_17 (__main__.SpecTests.test_worked_17)
Prereg :306: stage 2: n = 40, Z-band clean, n_b = 28 ... ok
test_worked_18 (__main__.SpecTests.test_worked_18)
Prereg :307: stage 2: n = 26, Z-band U (φ_μ = 0.61), n_b = 14 ... ok
test_worked_19 (__main__.SpecTests.test_worked_19)
Prereg :308: stage 2: n = 26, Z-band FIT, Z-band G7 fails, n_b = 24 ... ok
test_worked_20 (__main__.SpecTests.test_worked_20)
Prereg :309: stage 2: n = 22, Z-band clean, n_b = 17 ... ok
test_worked_21 (__main__.SpecTests.test_worked_21)
Prereg :310: stage 2: Z-band FIT, T = 144, B_Z = 2,304 > 2,200 ... ok
test_worked_22 (__main__.SpecTests.test_worked_22)
Prereg :311: n = 22, g = 10, gates, φ_μ = 0.958, φ_0^id = 24, actual `canon_full_n` = 0 ... ok
test_worked_23 (__main__.SpecTests.test_worked_23)
Prereg :312: n = 26, gates, FIT, W1 = 0.55 exactly ... ok
test_worked_24 (__main__.SpecTests.test_worked_24)
Prereg :313: stage 1: a synchronized round takes 121 s ... ok
test_z2_ambiguous_and_all_validity_gates (__main__.SpecTests.test_z2_ambiguous_and_all_validity_gates)
Prereg :149, :212–225: zero checked Z2 HALTs; V1–V13 each enforced. ... ok

----------------------------------------------------------------------
Ran 50 tests in 25.627s

OK
C10Z_ASTRA_SELFTEST_PASS tests=50

```

## SHA-256 and unchanged-source checks

These four implementation digests were taken after the final code changes and the fresh passing selftest:

| New file | SHA-256 |
|---|---|
| `experiments/track_c/c10z_astra_arms.py` | `a652306f1b6e6633ca3297c03508da7eb82e36e98cf8b2cb7306c9c86cc1f00c` |
| `experiments/track_c/c10z_astra_read.py` | `97a46b56d44422916e83df51b09f94c24845950fee501aa741ed70ec66dc0a76` |
| `tools/run_c10z_stage.sh` | `64edcae5a999ba8e503ba642ec282440b7bd0e1d2136cdacf853f1f2e598b879` |
| `experiments/track_c/c10z_astra_selftest.py` | `96dd8e99e094305d90b66b766b75a0c69c1aded36e4722eafef0cad59629ab1d` |

The fifth new file is this report, `results/c10z_astra_codex_build.md`. Its full-file SHA-256 is emitted after the final write in the completion message and verification output; embedding that digest in the file itself would change the bytes being hashed. No extra sidecar is created.

The protected-file digests match their pre-build values:

| Protected file | SHA-256 |
|---|---|
| `docs/C10Z_ASTRA_PREREG.md` | `38f8b68cc2f82d78e0689bff18bfa44f7600e2fe7b1484b07b4e1e88e267b072` |
| `experiments/track_c/c10e_bandknob.py` | `1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695` |
| `memit_dry_run/memit/memit/memit_main.py` | `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` |
| `.gitignore` | `1a758c5e371f3dcb077d72ff9cb2501a8ebc7de6442e04fdddd42d099f807b44` |

A final `git diff --exit-code -- docs/C10Z_ASTRA_PREREG.md experiments/track_c/c10e_bandknob.py memit_dry_run/memit .gitignore` returned **0** with empty output. No mutating git command ran. Graft lookup used explicit no-refresh/no-ignore-write guards; it did not change .gitignore. The original source-reading/fingerprint identities remain evidence; no model-based LAW#3/LAW#5 result is claimed.

## Objections

1. **Frozen row 22 conflicts with Z2 and the mandatory decision order.** At prereg :311, row 22 has φμ=0.958, all 24 identity facts positive, and actual `canon_full_n=0`, but prescribes PARTIAL-UNDERFIT-STAGE1. Under :149, any non-ambiguous checked fact is driver-positive while evaluator-false. Thus any nonempty checked population fails Z2; an all-ambiguous population also fails because zero checked facts is explicitly not a pass. Section 3's :208 order requires HALT before FIT/labels. The build cannot honestly make a full valid reader accept those raw facts and also enforce V5. Test `:811` preserves the exact prescribed label through the real conditional classifier; test `:416` supplies the same contradictory record to the full reader and expects **HALTED-V5**. The other 23 worked rows use the full reader/read_run. The frozen source was not edited and this is not silently counted as a successful full-reader validation of row 22.

2. **Native/runtime claims remain UNVERIFIED under the brief.** The authorized CPU tests establish synthetic numeric, record, decision and transport boundaries. They do not establish model loading, MPS shape/head parity, live memory/runtime feasibility, actual process continuity, empirical Z0–Z7, baseline LAW#3, standing LAW#5, cross-process regeneration, locality, spillover, route adoption or F1 closure. No live stage has run. This is the intended build-only scope, not scientific evidence.

3. **There is no demonstrated per-stage completion estimate.** The prereg :194–200 supplies measured whole-pass anchors and an elapsed ceiling; new ASTRA/D/G/control/probe/hash costs are UNMEASURED. The implementation's positive scheduling allowances are recorded projections, not measured Mac timings or a guarantee of finishing within 90 minutes. No gate is dropped to make the projection fit.

## Exact stage-0–1 commands and expected wall-clock

These commands are **operator handoff only**, after the queue/go conditions of prereg §6. They were not executed. Use the same fresh default `results/c10z_astra/` attempt for both calls. Neither command sets a stage-2/3 ceiling; without ceilings recorded before stage 0, those later expansions refuse. Do not invent those budget values from the withdrawn 4.1-hour estimate.

First, stage 0:

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
bash tools/run_c10z_stage.sh 0
```

After stage 0 exits **0** and reports `{"stage0":"READY"}`, invoke stage 1 separately while process 1 remains resident:

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
bash tools/run_c10z_stage.sh 1
```

Per prereg :194–200, the measured anchors are **approximately 34 minutes for a whole three-arm harness pass** and **approximately 23 minutes for a whole behavior run**. They are not per-arm or separate stage-0/stage-1 estimates. New setup, controls, expanded probes and serialization/restoration costs are UNMEASURED. The expected operational envelope is the **combined 5,400-second (90-minute) hard elapsed ceiling**, starting before model import, including time between the two calls. Completion inside that ceiling is not established. A stage-1 synchronized round may take at most **120 seconds**; exactly 120 passes, more than 120 produces HALTED-BUDGET. Every projection and actual elapsed deadline remains binding.

## Session handoff / context-save

This handoff is kept in the named report to preserve the brief's artifact boundary. No separate global checkpoint or memory update was written.

- Worktree/branch: verified `c10k-route-a` / `worktree-c10k-route-a`; no state-changing git.
- Authorized artifacts: the four new implementation files and this report; protected prereg/engine/harness unchanged; `c10w_*` untouched.
- Verification: fresh authorized CPU selftest **50/50 PASS**, exit 0, 25.627 seconds; final GPT-6-astra/high review **PROCEED for model-free build**.
- Scientific state: no run records or live result claimed; all native scientific acceptance remains UNVERIFIED.
- Next action: operator queue/go decision and a fresh stage-0 call, followed by the separate stage-1 call above; ceilings for optional expansions must already be fixed before stage 0.
- Interpretation to retain: row 22 is a conditional label example that cannot satisfy full-record Z2 validity; preserve the full-reader HALTED-V5 regression and the unchanged prereg.

