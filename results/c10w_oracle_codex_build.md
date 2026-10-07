# D-C10w-oracle — frozen v2.2 build report

Model: GPT-6 (Codex host). Effort: the host did not expose the session effort setting; no more specific model or effort claim is made.
Date: 2026-10-07. Decision-ID: D-C10w-oracle.
Classification: **ORACLE MEASUREMENT — not a route; never promotable as a write-engine result (D-C10r-rulings-3 (2))**.

**Build verdict: PROCEED for the requested model-free build.** All 27 prereg-derived selftests pass. Scientific/runtime status remains **UNVERIFIED**: no model, tokenizer, torch, MPS or GPU code was run. This report supplies prospective stage commands; it does not authorize or claim an experiment run, F1 closure, or write-engine route.

The entire frozen specification was read: `docs/C10W_ORACLE_PREREG.md`, FROZEN v2.2, commit `fb1788b`, SHA-256 `2baeb4e9865dd1080ecb5765652c5eae67336eca6047d93b4f5948545854c344`. Its working-tree bytes match that commit. The verified worktree is `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`, branch `worktree-c10k-route-a`.

## Scope and verification boundary

Created only the five named Python implementation/selftest files, the named stage launcher, and this report. No existing file was edited. The end-of-build SHA-256 sweep found **136 protected files unchanged**, covering the engine, frozen preregistration, existing harness and `.gitignore`. Existing unrelated working-tree changes were left untouched. No mutating Git command was used.

Heavy imports are inside runtime functions, after entry/provenance gates. The selftest installs a finder that rejects imports of torch, transformers, datasets, tokenizers, safetensors and numpy (`experiments/track_c/c10w_oracle_selftest.py:28`). Synthetic records and a small stand-in for gradient-context delegation validate control logic; they are not model results or engine inertness evidence. Child processes used in the selftest are the stdlib-only preflight verifier and launcher **refusal** paths.

Python AST parsing/compilation for all five new Python files and `/bin/bash -n tools/run_c10w_stage.sh` passed. The launcher is executable (0755). No `__pycache__` files were created by these checks.

## Test-first evidence

The selftest was written before the implementation. First invocation of the requested command exited **1**:

```text
FAIL: prereg implementation files absent (expected test-first RED)
  experiments/track_c/c10w_oracle_read.py
  experiments/track_c/c10w_oracle_step0.py
  experiments/track_c/c10w_oracle_train.py
  experiments/track_c/c10w_oracle_eval.py
  tools/run_c10w_stage.sh
```

Subsequent behavioral regressions were also observed RED before correction: insufficiently bound preflight summaries, equal-count/different-row null evidence, an outer no-grad context disabling the unchanged engine's latent optimisation, missing geometry, missing raw frame/mounted evidence, contradictory mounted string counts, and contradictory final restore hashes. These were corrected in the new files. The source-only independent reviewer additionally identified the retry-budget, P1/P2 linkage and raw-gate-summary issues; all identified blocking findings were resolved.

## Preregistration → test → code

All prereg line numbers below refer to the frozen file above. Tests contain their own prereg citations. Each mapping cites the actual implementation boundary exercised; tensor/model operations inside runtime functions remain source-inspected only.

| Prereg requirement | Model-free test | Implementation |
|---|---|---|
| §3:359–368; all configuration labels, 29/30 and 60/61 | `experiments/track_c/c10w_oracle_selftest.py:187` | `experiments/track_c/c10w_oracle_read.py:279`; `experiments/track_c/c10w_oracle_read.py:358`; `experiments/track_c/c10w_oracle_read.py:408` |
| §3:374–384; every final-label table row | `experiments/track_c/c10w_oracle_selftest.py:203` | `experiments/track_c/c10w_oracle_read.py:408` |
| §3:388–397; every routing row and canonical a/b/c split | `experiments/track_c/c10w_oracle_selftest.py:227` | `experiments/track_c/c10w_oracle_read.py:397`; `experiments/track_c/c10w_oracle_read.py:408` |
| §3:372,395; no clean reference → null; locality-cost never P3 | `experiments/track_c/c10w_oracle_selftest.py:248` | `experiments/track_c/c10w_oracle_read.py:408` |
| §3:351–368; G1–G7 boundaries on both sides, all 20 training frames | `experiments/track_c/c10w_oracle_selftest.py:262` | `experiments/track_c/c10w_oracle_read.py:258`; `experiments/track_c/c10w_oracle_read.py:358` |
| §2.7:241–245; LAW#3 inclusive envelope and A1/A2 67/68 | `experiments/track_c/c10w_oracle_selftest.py:292` | `experiments/track_c/c10w_oracle_read.py:148` |
| §2.7:245,249–255; stimulus, strict standing gate, restore/delegation/counters | `experiments/track_c/c10w_oracle_selftest.py:314` | `experiments/track_c/c10w_oracle_read.py:293`; `experiments/track_c/c10w_oracle_eval.py:338` |
| §2.7:250; exact null per-prompt/probe equality | `experiments/track_c/c10w_oracle_selftest.py:338` | `experiments/track_c/c10w_oracle_read.py:157`; `experiments/track_c/c10w_oracle_eval.py:234` |
| §2.5:197; §2.7:249,252; unchanged engine gradient context | `experiments/track_c/c10w_oracle_selftest.py:349` | `experiments/track_c/c10w_oracle_eval.py:16`; `experiments/track_c/c10w_oracle_eval.py:283` |
| §3:368–370; minimum of seeds, seed-gap 15/16, retrain-gap 10/11, band/gate crossings | `experiments/track_c/c10w_oracle_selftest.py:371` | `experiments/track_c/c10w_oracle_read.py:380` |
| §2.2:54; §2.4:186; §3:331–345; own fit gates and matched protocol | `experiments/track_c/c10w_oracle_selftest.py:389` | `experiments/track_c/c10w_oracle_train.py:37`; `experiments/track_c/c10w_oracle_read.py:293`; `experiments/track_c/c10w_oracle_step0.py:328` |
| §2.6:230,232,236; §3:365–370; BIGRAM, PAIRING-SPECIFIC, RETRY800, MERGE-LOSS | `experiments/track_c/c10w_oracle_selftest.py:405` | `experiments/track_c/c10w_oracle_read.py:245`; `experiments/track_c/c10w_oracle_read.py:358`; `experiments/track_c/c10w_oracle_read.py:380` |
| §3:388; canonical READ, seed-gap and merge-loss conditions | `experiments/track_c/c10w_oracle_selftest.py:432` | `experiments/track_c/c10w_oracle_read.py:397` |
| §3:342–345; missing/nonfinite metrics, raw rows and denominators | `experiments/track_c/c10w_oracle_selftest.py:441` | `experiments/track_c/c10w_oracle_read.py:45`; `experiments/track_c/c10w_oracle_read.py:183`; `experiments/track_c/c10w_oracle_read.py:293` |
| §2.4:181–186; exact epoch permutations, 400/800 updates, warmup, 455/456 and 22/23 fit | `experiments/track_c/c10w_oracle_selftest.py:459` | `experiments/track_c/c10w_oracle_train.py:22`; `experiments/track_c/c10w_oracle_train.py:33`; `experiments/track_c/c10w_oracle_train.py:37`; `experiments/track_c/c10w_oracle_train.py:137` |
| §2.2:52; §2.3:70–106; §2.8:264–266; S1–S6 on real constants, S2c/d, shuffle assertion | `experiments/track_c/c10w_oracle_selftest.py:477` | `experiments/track_c/c10w_oracle_step0.py:44`; `experiments/track_c/c10w_oracle_step0.py:58`; `experiments/track_c/c10w_oracle_step0.py:82`; `experiments/track_c/c10w_oracle_step0.py:89` |
| §2.5:192–194; §2.7:241; §2.8:260; entry and raw-bound preflight before loading | `experiments/track_c/c10w_oracle_selftest.py:501` | `experiments/track_c/c10w_oracle_read.py:102`; `experiments/track_c/c10w_oracle_train.py:51`; `experiments/track_c/c10w_oracle_read.py:569` |
| §2.2:54; §2.9:312–316; full retry and forced-mate budget charged before spending | `experiments/track_c/c10w_oracle_selftest.py:539` | `experiments/track_c/c10w_oracle_step0.py:291`; `experiments/track_c/c10w_oracle_step0.py:303`; `experiments/track_c/c10w_oracle_step0.py:328` |
| §2.5:198–203; §2.7:241,253; same-process LAW#3/null ordering, missing adapter and hit counters | `experiments/track_c/c10w_oracle_selftest.py:552` | `experiments/track_c/c10w_oracle_eval.py:16`; `experiments/track_c/c10w_oracle_eval.py:338` |
| §2.9:314–318; §5:439–441; 90-minute, 40-billion-byte, four-hour and 465/448/327 guards | `experiments/track_c/c10w_oracle_selftest.py:575` | `experiments/track_c/c10w_oracle_train.py:42`; `experiments/track_c/c10w_oracle_read.py:109`; `experiments/track_c/c10w_oracle_read.py:113`; `experiments/track_c/c10w_oracle_read.py:117` |
| §2.8:278–285; §2.9:314; §8:532; P2/P3 explicit authorization even under limit | `experiments/track_c/c10w_oracle_selftest.py:588` | `experiments/track_c/c10w_oracle_read.py:122`; `experiments/track_c/c10w_oracle_step0.py:316`; `experiments/track_c/c10w_oracle_read.py:517` |
| §2.10:322–325; §3:344; real JSON round-trip, exclusive output and finite data | `experiments/track_c/c10w_oracle_selftest.py:606` | `experiments/track_c/c10w_oracle_read.py:76`; `experiments/track_c/c10w_oracle_read.py:86`; `experiments/track_c/c10w_oracle_read.py:96`; `experiments/track_c/c10w_oracle_read.py:139` |
| §3:339–342; embedded training evidence must equal its hashed attempt | `experiments/track_c/c10w_oracle_selftest.py:629` | `experiments/track_c/c10w_oracle_read.py:511`; `experiments/track_c/c10w_oracle_read.py:578` |
| §2.6:218,224,233,236; §3:342–345; frame/MMLU/cross/mounted rows reconcile with gate summaries | `experiments/track_c/c10w_oracle_selftest.py:642` | `experiments/track_c/c10w_oracle_read.py:183`; `experiments/track_c/c10w_oracle_read.py:172`; `experiments/track_c/c10w_oracle_read.py:293` |
| §2.8:278–285; §3:339–340; P3 cannot use another P1's replication | `experiments/track_c/c10w_oracle_selftest.py:658` | `experiments/track_c/c10w_oracle_read.py:528`; `experiments/track_c/c10w_oracle_step0.py:316`; `experiments/track_c/c10w_oracle_read.py:517` |
| §2.4:170; §2.7:251; §3:339–345; raw restore/frozen-parameter hashes match passing summaries | `experiments/track_c/c10w_oracle_selftest.py:668` | `experiments/track_c/c10w_oracle_read.py:293`; `experiments/track_c/c10w_oracle_read.py:541`; `experiments/track_c/c10w_oracle_train.py:137` |
| §2.8:278; §2.9:303–316; measured P2/P3 inventory and actual launcher refusal | `experiments/track_c/c10w_oracle_selftest.py:677` | `experiments/track_c/c10w_oracle_read.py:458`; `experiments/track_c/c10w_oracle_step0.py:328` |

The full freeze/training/probe paths are implemented but intentionally unexecuted:

| Prereg item | Code and verification boundary |
|---|---|
| §2.8:262–271; step 0 items 0–7 | `experiments/track_c/c10w_oracle_step0.py:215`: entry, actual value/target maps and head/modifier eligibility, training-input and held-out hashes, S1–S6, copied S7, frozen MMLU, answer-token checks, fingerprint, nonzero seam. Seal/entry/shuffle logic is tested; acquisition/tokenisation and tensor gates are source-only. |
| §2.3:139–164; completed S7 adjudications | `experiments/track_c/c10w_oracle_step0.py:126` copies all 22 frozen ACCEPT reasons and the recorded historical substitutions/rejections, with the frozen GPT-6-Astra/high attribution. No new adjudication or template selection occurs. |
| §2.4:168–188; LoRA, loss, fit and frozen scope | `experiments/track_c/c10w_oracle_train.py:71`, `experiments/track_c/c10w_oracle_train.py:114`, `experiments/track_c/c10w_oracle_train.py:128`, `experiments/track_c/c10w_oracle_train.py:137`. Actual fp16-load/fp32-upcast, MPS forward/backward, clipping/AdamW, parameter hashing and safetensors remain unrun. |
| §2.6:221–224; immutable MMLU-200, five dev examples, token checks | `experiments/track_c/c10w_oracle_step0.py:174`, `experiments/track_c/c10w_oracle_eval.py:130`. Test/dev only, full commit, ordered identities/cache hashes, seed 20261007, exact prompt bytes/ids, four distinct single-token answers, suffix concatenation and paired discordance are implemented. HF acquisition and actual five-shot forwards are unrun. |
| §2.6:216–236; every probe on U/closed form/oracle | `experiments/track_c/c10w_oracle_eval.py:201`, `experiments/track_c/c10w_oracle_eval.py:118`, `experiments/track_c/c10w_oracle_eval.py:126`, `experiments/track_c/c10w_oracle_eval.py:159`, `experiments/track_c/c10w_oracle_eval.py:179`, `experiments/track_c/c10w_oracle_eval.py:246`, `experiments/track_c/c10w_oracle_eval.py:264`. Reader gates and raw-record reconciliation are tested; all actual forwards and covariance diagnostics are unrun. |
| §2.7:254; nonzero serialisation/application seam | `experiments/track_c/c10w_oracle_step0.py:137` uses the trainer's actual wrapper and serializer with distinct fixed nonzero A/B for each of five layers at both ranks; compares each against an independently merged CPU matrix. No CPU tensor seam was run in this build. |
| §2.9:316–318; synchronized timing and actual driver samples | `experiments/track_c/c10w_oracle_train.py:137`, `experiments/track_c/c10w_oracle_eval.py:78`, `experiments/track_c/c10w_oracle_step0.py:303`. Arithmetic limits and full retry cost are tested; throughput and allocation samples are unmeasured. |
| §2.10:322–325; immutable phase files, classification and tracking check | `experiments/track_c/c10w_oracle_read.py:76`, `experiments/track_c/c10w_oracle_read.py:483`, `experiments/track_c/c10w_oracle_read.py:578`, `experiments/track_c/c10w_oracle_step0.py:267`. Exclusive writer/tracking rejection are tested on temporary synthetic files. The eventual scientific artifacts do not yet exist. |

## LAW#4 source reads and unchanged seams

Harness/engine functions used were read with line numbers before authoring their callsites. Load-bearing source spans:

- `experiments/track_c/c10e_bandknob.py:25–48`: fixed model/revision loading; `:51–61`: CANON/PTEST/subjects; `:67–68`: target IDs.
- `c10e_bandknob.py:96–97`: request construction; `:100–143`: prediction, greedy full match, decoded startswith and teacher-forced continuation; `:146–163`: weight naming, snapshot, restore and locality.
- `c10e_bandknob.py:166–178`: five CPU covariance projectors; `:181–221`: original closed-form edit and float32 update applied to fp16 weights; `:224–250`: actual value maps.
- `c10e_bandknob.py:311–355`: unchanged axes/covariance hashes; `:358–400`: `eval_arm`, its per-prompt vectors and denominators; `:415–455`: standing LAW#5 gate and stimulus-leak report; `:458–509`: recipe setup, restored arm loop, hooks and return.
- `experiments/track_c/c10p_twopass_arms.py:30–42`: the six exact FRAME_SUBJECTS and same-frame probe convention.
- `memit_dry_run/memit/memit/memit_main.py:25–60`: engine application; `:240–284`: `get_cov`; `:287–323`: shape matching and context templates.
- `memit_dry_run/memit/memit/compute_z.py:1` (entire function read): latent optimization needs gradients, including `loss.backward()` at `:171`; the new wrapper leaves the original recipe's gradient context intact.
- `memit_dry_run/memit/util/device.py:18–22`: resolver; inherited overrides are rejected before setting the internally fixed MPS device.
- `memit_dry_run/memit/util/hparams.py:12–16`: `MEMITHyperParams.from_json` loading; `tools/engine_fingerprint.py:34–36`: pinned fingerprint and three covariance-CPU sites.

The runtime wrapper stores the original `H.my_edit` object and delegates to it for the closed form and standing LAW#5 gate. To record the original closed-form update without rewriting/reimplementing it, the evaluator observes the existing `upd` at harness line 216 with a temporary trace; it observes setup completion at line 471. The harness source hash is frozen and the trace is removed in `finally` (`experiments/track_c/c10w_oracle_eval.py:283`). No engine/harness file was edited.

## Implementation decisions

1. **Training/evaluation separation (§2.3:106, §2.7:241).** Training consumes the frozen training JSON and a minimal preflight certificate. Its source contains neither the held-out template variable nor a harness import. A separate stdlib-only reader process verifies the certificate against the hashed raw preflight: baseline counts, exact null rows/probes, strict standing gate, counters and restore hashes (`experiments/track_c/c10w_oracle_train.py:51`; `experiments/track_c/c10w_oracle_read.py:541`; `experiments/track_c/c10w_oracle_read.py:569`). The fitting process does not ingest held-out prompt bytes. An unrelated but correctly hashed JSON file cannot satisfy the gate.
2. **Seal is the frozen list (§2.3:70–164).** No template substitution/search is performed. S1–S6 operate on AST-read real constants and both G6 screen files; S7 copies the completed frozen judgments. Frozen sources include the harness, trainer/evaluator/reader, hparams, frame source, screens, fingerprint script, model config and tokenizer files (`experiments/track_c/c10w_oracle_step0.py:215`).
3. **Warmup and exact EM (§2.4:181–186).** Update index 0 uses zero LR, indices 1–19 ramp, index 20 reaches 3e-4, then stays constant. Training always completes the declared 400/800 updates. End-of-attempt batched teacher-forced full-target argmax is the prereg's greedy-equivalent fit check; it never chooses a held-out hyperparameter.
4. **Fresh retries and matched controls (§2.2:54, §2.4:186, §2.9:312–316).** Return 75 denotes the sole eligible underfit retry. A fresh child starts the 800-update protocol from the base; both records remain. If either member requires 800 updates, its mate uses/retrains to 800. Before each launch, the phase projection charges every completed attempt, the entire proposed fresh attempt, the required matched retry and the remaining units. HALT after a second fit miss or any budget failure.
5. **Recorded authorization format (§2.8:278–285, §2.9:314, §8:532).** Files are separate and immutable: `<P1-dir>/authorization_P2.json` and `authorization_P3.json`. Each contains its phase key with `authorized: true`, `recorded_by`, `recorded_at`, exact `p1_eval_sha256` and `p1_verdict_sha256`, and optional explicit `budget_minutes`. An over-limit P1 budget ruling is recorded separately in `authorization_P1.json` under `P1.budget_minutes`. No authorization is created by this build. P3 additionally requires valid replicated r16 eligibility from a P2 attached to this exact P1, including frozen source/attempt/adapter hashes (`experiments/track_c/c10w_oracle_step0.py:316`; `experiments/track_c/c10w_oracle_read.py:528`).
6. **Original engine behavior (§2.5:196–204, §2.7:249–252).** The unchanged recipe executes with gradients available for its latent optimization. Only explicit scoring/mutation/tensor comparison blocks use no-grad. The closed-form trace records diagnostics without changing the solver, context, weights application or original function object.
7. **Raw data binds labels (§2.7:250–253, §3:339–345).** Counts reconcile with raw hit vectors; frame/MMLU/cross/mounted evidence is mandatory, and MMLU paired discordance is recomputed against U. Training evidence embedded in eval must equal the hashed original attempt. Restore/frozen-scope hashes must match their passing summaries. Mounted/string contradictions invalidate before MERGE-LOSS or canonical READ can affect routing (`experiments/track_c/c10w_oracle_read.py:293`; `experiments/track_c/c10w_oracle_read.py:511`).
8. **Same-seed agreement (§2.8:283).** Agreement compares actual greedy output token sequences up to the frozen target length, prompt by prompt, including incorrect predictions. It is not equality of success bits. Every agreement bit, numerator /72, count difference and per-layer delta cosine is recorded (`experiments/track_c/c10w_oracle_eval.py:338`).
9. **Timing, memory and geometry (§2.6:225–236, §2.9:314–318).** The four-hour eval clock includes pre-model checks/loading. Per-attempt synchronized projections include the final fit pass and account for elapsed loading/hashing work. MPS driver samples and CPU process RSS remain separate. Covariance diagnostics transfer to CPU before float64 casts and run serially. Norm ratio is reported, never a LARGE-WRITE gate.
10. **One stage per invocation and closeout (§2.8, §2.10, §5).** The shell execs exactly one dispatcher stage; every attempt is a fresh process. P1 ends with a measured projection and explicit stop. P2/P3 evals write their reader verdicts. HALT records/diagnostics are exclusive; no canonical checkpoint/evidence/ledger is rewritten in this build. Session handoff is retained in this named report to honor the brief's new-files-only scope.

## Exact selftest command and full PASS output

Executed from the verified worktree via `/opt/homebrew/bin/rtk proxy`, which forwards the underlying command:

```sh
.venv/bin/python -B experiments/track_c/c10w_oracle_selftest.py
```

Exit status: **0**. Full output of the final run:

```text
test_G1_to_G7_both_sides (__main__.OracleTests.test_G1_to_G7_both_sides)
§3 lines 351–368: equality passes for every locality/forgetting boundary. ... ok
test_P2_P3_authorization_even_under_projection_limit (__main__.OracleTests.test_P2_P3_authorization_even_under_projection_limit)
§2.8,2.9,8 lines278,280,285,314,532: no implicit post-P1 approval. ... ok
test_P3_replication_must_belong_to_authorized_P1 (__main__.OracleTests.test_P3_replication_must_belong_to_authorized_P1)
§2.8,3 lines278–285,339–340: another P1's replication cannot enable rank64. ... ok
test_all_final_label_table_rows (__main__.OracleTests.test_all_final_label_table_rows)
§3 lines 374–384: every row, including both PARTIAL/FAIL antecedents. ... ok
test_bigram_pairing_retry_and_merge_loss_qualifiers (__main__.OracleTests.test_bigram_pairing_retry_and_merge_loss_qualifiers)
§2.6,3 lines230,232,236,365–370: exact qualifier thresholds and exception. ... ok
test_canonical_read_conditions_and_merge_loss (__main__.OracleTests.test_canonical_read_conditions_and_merge_loss)
§3 line388: canonical seed gap, fit, G1–G6 and merge gap, no exception. ... ok
test_configuration_labels_and_integer_count_boundaries (__main__.OracleTests.test_configuration_labels_and_integer_count_boundaries)
§3 lines 359–368: every label, 29/30 and 60/61, through real reader. ... ok
test_embedded_training_evidence_must_equal_hashed_attempt (__main__.OracleTests.test_embedded_training_evidence_must_equal_hashed_attempt)
§3 lines339–342: a valid file hash cannot authenticate different embedded fit/steps. ... ok
test_entry_preflight_and_training_provenance_precede_model_load (__main__.OracleTests.test_entry_preflight_and_training_provenance_precede_model_load)
§2.5,2.7 lines192–194,241,260: no inherited knob or mismatched certificate. ... ok
test_eval_seam_order_missing_adapter_and_hit_counters (__main__.OracleTests.test_eval_seam_order_missing_adapter_and_hit_counters)
§2.5,2.7 lines198–203,241,253: trained dispatch gated before application. ... ok
test_fit_matched_controls_steps_and_provenance (__main__.OracleTests.test_fit_matched_controls_steps_and_provenance)
§2.2,2.4,3 lines54,186,331–345: own fit, exact matching, incomplete INVALID. ... ok
test_guards_projection_memory_and_eval_wall_boundaries (__main__.OracleTests.test_guards_projection_memory_and_eval_wall_boundaries)
§2.9,5 lines314–318,439–441: equality passes; guards are HALT,not FAIL. ... ok
test_law3_envelope_all_endpoints_and_controls (__main__.OracleTests.test_law3_envelope_all_endpoints_and_controls)
§2.7 lines 241–245: inclusive 4/5/18/19,4/5/10/11,41/42/59/60,67/68. ... ok
test_no_gate_clean_reference_and_locality_cost_never_p3 (__main__.OracleTests.test_no_gate_clean_reference_and_locality_cost_never_p3)
§3 lines 372,395: empty clean rank set -> null, never costly substitution. ... ok
test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate (__main__.OracleTests.test_null_per_prompt_swap_cannot_hide_behind_counts_or_certificate)
§2.7 line250: every per-prompt hit must match, even with equal aggregate counts. ... ok
test_pure_P1_reprojection_and_real_launcher_refusal (__main__.OracleTests.test_pure_P1_reprojection_and_real_launcher_refusal)
§2.8,2.9 lines278,303–314,316: measured P2/P3 inventory,stage entry refuses. ... ok
test_recipe_delegation_keeps_original_engine_gradient_context (__main__.OracleTests.test_recipe_delegation_keeps_original_engine_gradient_context)
§2.5,2.7 lines197,249,252: unchanged engine-parity recipe, including compute_z gradients. ... ok
test_records_exclusive_roundtrip_and_nonfinite_halt (__main__.OracleTests.test_records_exclusive_roundtrip_and_nonfinite_halt)
§2.10,3 lines322–325,344: real writer, append-only, every JSON classification. ... ok
test_replication_minimum_seed_and_same_seed_boundaries (__main__.OracleTests.test_replication_minimum_seed_and_same_seed_boundaries)
§3 lines 368–370: min-of-two,15/16,10/11,band and each gate crossing. ... ok
test_required_metrics_counts_finiteness_and_denominators (__main__.OracleTests.test_required_metrics_counts_finiteness_and_denominators)
§3 lines342–345: missing/nonfinite/incorrect denominators never pass. ... ok
test_required_probe_rows_and_gate_summaries_cannot_diverge (__main__.OracleTests.test_required_probe_rows_and_gate_summaries_cannot_diverge)
§2.6,3 lines218,224,233,342–345: raw frame, MMLU and cross-score evidence is required. ... ok
test_restore_and_frozen_scope_require_actual_hash_evidence (__main__.OracleTests.test_restore_and_frozen_scope_require_actual_hash_evidence)
§2.4,2.7,3 lines170,251,339–345: contradictory hashes invalidate passing summaries. ... ok
test_retries_charged_before_each_fresh_process (__main__.OracleTests.test_retries_charged_before_each_fresh_process)
§2.2,2.9 lines54,312,314–316: full retry and forced mate cost before spending. ... ok
test_routing_every_row_and_canonical_split (__main__.OracleTests.test_routing_every_row_and_canonical_split)
§3 lines 388–397: PASS(a,b,c), PARTIAL(a,b,c), FAIL, no routing. ... ok
test_seal_real_constants_S1_to_S6_and_shuffled_map (__main__.OracleTests.test_seal_real_constants_S1_to_S6_and_shuffled_map)
§2.2,2.3 lines52,70–104,106,264–266: real constants without importing H. ... ok
test_stimulus_law5_strict_restore_delegation_and_counters (__main__.OracleTests.test_stimulus_law5_strict_restore_delegation_and_counters)
§2.7 lines 245,249–255: strict LAW5 and exact process manifest counters. ... ok
test_training_schedule_exact_seed_steps_warmup_and_fit (__main__.OracleTests.test_training_schedule_exact_seed_steps_warmup_and_fit)
§2.4 lines181–186: N-specific epochs,1000*seed+epoch,400/800 updates. ... ok

----------------------------------------------------------------------
Ran 27 tests in 5.036s

OK
C10W_ORACLE_SELFTEST PASS: 27 tests; model-free; oracle measurement, not a route
```

## SHA-256 of every new implementation file

These hashes cover the final bytes tested above (the report is the checksum container and cannot contain its own byte-for-byte hash).

| New file | SHA-256 |
|---|---|
| `experiments/track_c/c10w_oracle_step0.py` | `fbccdc1cf43ff1bfd45f0bc7a5286e8536f0009f17b0f613fb42ca9a31dd2f1b` |
| `experiments/track_c/c10w_oracle_train.py` | `d742ed537282f972f28888639b65dcd7a636681a3f5057bbff4e49db04675eee` |
| `experiments/track_c/c10w_oracle_eval.py` | `5314d2f53d3afc211298ce4f11f880f307b695b26a6b46bb7fea05c567374f60` |
| `experiments/track_c/c10w_oracle_read.py` | `bbaca40788719fe6416d4c924b321831ae0e87e7ebfa73ba4a522e85cfb5e193` |
| `experiments/track_c/c10w_oracle_selftest.py` | `35931374d133b28a34f21388f42d5f5232af60ac9c09542afdea452f2aa275b3` |
| `tools/run_c10w_stage.sh` | `07e0e2805681b53f45d6d4742ed40ab306e5f7c84a1f23373498d155b898cfb6` |

## Review and Objections

**Objections: none unresolved within the permitted model-free build scope.** The fresh-context reviewer `/root/design_review` returned **PROCEED** after inspecting the final provenance, raw-metric, restore/frozen-scope and nonzero-seam fixes. Its final narrow disposition was: “PROCEED — the narrow changes are sound on inspection.”

The local Claude auth probe returned `loggedIn: false`; the source-only review therefore used a fresh same-family fallback under the advisor-review workflow. This provides weaker independence than the preferred out-of-family Claude review. Neither review nor synthetic tests prove a real training run, MMLU instrument acquisition, actual MPS allocation/throughput, LAW#3 reproduction or LAW#5 tensor parity. Those runtime gates remain **UNVERIFIED** and execute at the prescribed future stages. No scientific label/routing conclusion is issued from this build. C10/F1 remain OPEN/BLOCKING.

## Exact prospective step 0 and P1 commands

**Not executed.** Use these only in a later authorized exclusive compute window satisfying prereg `:273`: no concurrent GPU job, autoresearch paused, Ollama stopped. This build has not inspected or changed those processes. Execute each stage separately, inspect its exit/log/records, and stop on HALT; these lines are not a chained launcher.

```sh
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
export LLMDB_ROOT="$PWD"
tools/run_c10w_stage.sh step0
tools/run_c10w_stage.sh p1-preflight
tools/run_c10w_stage.sh p1-a1
tools/run_c10w_stage.sh p1-a7
tools/run_c10w_stage.sh p1-canon
tools/run_c10w_stage.sh p1-a2
tools/run_c10w_stage.sh p1-shuf
tools/run_c10w_stage.sh p1-eval
tools/run_c10w_stage.sh p1-project
```

Inherited MODEL_ID, MODEL_REV, LLMDB_DEVICE and all eight named harness knobs must be absent; the launcher/entry preflight rejects them rather than silently stripping them. Each child uses the absolute worktree venv and paths before harness chdir.

| Order | Stage | Expected wall-clock from the frozen prereg |
|---|---|---|
| 0 | `step0` | No fixed aggregate estimate is preregistered. Dataset acquisition, tokenizer checks and CPU seam are unmeasured; no invented total. |
| 1 | `p1-preflight` | 70–85 min (§2.9:311). |
| 2 | `p1-a1` | 20–38 min for 400 updates plus fit (§2.9:305). |
| 3 | `p1-a7` | 20–38 min; same fixed attempt protocol. |
| 4 | `p1-canon` | 400 updates on N=24; the prereg's generic per-attempt assumption is 20–38 min, not a measured canonical-specific estimate. |
| 5 | `p1-a2` | 20–38 min. |
| 6 | `p1-shuf` | 20–38 min. A matched retry may also force a fresh 800-update A7 attempt. |
| 7 | `p1-eval` | 165–190 min including U, null, three recipes, all probes/MMLU/mount diagnostics (§2.9:311). Hard four-hour process guard. |
| 8 | `p1-project` | Model-free projection/read; no separate prereg wall-clock estimate. Writes P1 `verdict.json` and stops. |

P1's declared total is **335–465 min**, excluding step 0 and extra retries. A full fresh 800-update retry adds **39–75 min per adapter**, charged in full; a matched pair can require two. The runtime/phase projections may HALT before spending those additional minutes. A 90-minute attempt projection, sampled allocation above 40,000,000,000 bytes, or unruled phase projection over 465/448/327 min is HALT/INVALID-BUDGET, never FAIL-CEILING (§2.9:314–318).

After P1, both P2 and P3 remain stopped until their separate recorded post-P1 authorization exists, even if measured projections are below budget. P2 replication precedes any routing label; P3 runs only for replicated r16 PARTIAL-CEILING or FAIL-CEILING. No next phase, route, model job or canonical evidence update is authorized by this report.

