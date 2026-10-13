VERDICT: PROCEED-WITH-CHANGES
Reviewer: GPT-6-Astra high (codex exec, read-only), 2026-10-07 ~15:00 MDT; packet /Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10w_prerun/astra_packet.md

**Next action:** add a budget checkpoint immediately after `p1-preflight` and before every subsequent GPU stage. Waiting until `p1-eval` risks losing the ability to continue the existing P1 directory.

Paths below: `step0.py`, `train.py`, `eval.py`, `read.py`, and `selftest.py` mean `experiments/track_c/c10w_oracle_<name>.py`; `prereg` means `docs/C10W_ORACLE_PREREG.md`.

**BLOCKING items — resolve in the launch plan**

1. **Set the worktree environment for every command.** `tools/run_c10w_stage.sh:9–15`; `read.py:21–22,102–105`; `prereg:192–194`. This review session inherits `LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`, the parent checkout. Setting it only on the fingerprint command does not affect later commands: the first launcher invocation would exit 2. Smallest fix: export the exact worktree root once in the launch shell, or prefix **every** invocation. Explicitly remove all eleven `FORBIDDEN_ENV` variables; even `LLMDB_DEVICE=mps` is rejected.

2. **Budget rulings must precede dispatch, including training dispatch.** `step0.py:291–321,378–394,408–413`; `read.py:474–480`. A projection refusal writes `HALT.json`; subsequent stage selection refuses that directory. Adding authorization afterward cannot resume it through the dispatcher. Smallest fix: calculate the production projection after preflight and each completed training stage; if over allowance, obtain and record the ruling **before** dispatching another stage. The existing `<p1>/authorization_P1.json` mechanism accepts:
   `{"P1":{"authorized":true,"recorded_by":"<actual authority>","recorded_at":"<timestamp>","budget_minutes":<approved limit>}}`.
   Do not manufacture authorization or remove HALT markers. A permitted restart needs a fresh phase directory.

**Changes to the launch plan**

- **Stage names/order are correct.** `read.py:28–33,470–471`; `step0.py:336–406`; `prereg:262–278`. The nine named stages match exactly. Prior training units must have PASS records; evaluation requires all five fitted units; projection requires `eval.json`. The launcher supplies the venv and child arguments. No additional stage argument is missing.

- **Preserve one exact step-0/P1 chain.** `step0.py:267–280,346–353`; `read.py:474–491`. Directory selection means “latest timestamp,” not an explicitly supplied run ID. Do not repeat `step0` or `p1-preflight` while continuing an existing chain. Repeating a completed training stage encounters its existing log and can HALT the directory. The output root was absent during this review.

- **Add a model-free network/cache check before `step0`.** `step0.py:174–179,215–240`. The supplied MMLU prefetch does not eliminate the live `dataset_info("cais/mmlu")` call, which resolves current HEAD rather than requesting the prefetched commit. Network failure occurs after model loading and initial output writes; a changed HEAD can require uncached data. Smallest fix: verify API access from the actual launch environment and compare its returned revision with `c30699e8356da336a370243923dbaf21066bb9fe`; if different, prepare that resolved revision before dispatch. Do not assume offline mode solves this: the harness explicitly sets `HF_HUB_OFFLINE=0` (`experiments/track_c/c10e_bandknob.py:4–5`). Launch-time network availability remains **UNVERIFIABLE** here.

- **Keep both hand tests as mandatory launch gates.** `results/c10w_oracle_fix1_review.md:83–95`; `selftest.py:1174`. Prior evidence records 63/63 selftests and 3/3 torchchecks. My allowed selftest invocation ran 63 tests but exited 1 with 45 errors, including `No usable temporary directory found` under this read-only sandbox. This is **not a reproduced PASS**. Run it in the launch environment with writable temporary storage; retain its result and the torchcheck result. I did not run torchcheck or load a model.

- **Check retry exposure before each training stage.** `step0.py:375–390`; `prereg:54,186,273`. A first fit miss returns 75 and triggers the preregistered fresh 800-update attempt internally; shuffled/A7 matching can require another attempt. These are declared fit retries, distinct from retrying a HALTed stage. Budget inspection only between shell invocations cannot intervene before this internal retry guard.

- **Retain dispatcher logs and exit status.** `step0.py:275–283,399–406`. Child logs are automatic, but `p1-project` runs directly in the dispatcher. Preserve its outer log too, and use the background process’s actual exit status before advancing.

- **Keep the P1 stop and complete HALT recording.** `prereg:448,532`; `step0.py:399–413`. Stop after `p1-project`; P2/P3 remain unauthorized. On HALT, preserve diagnostics and update the checkpoint as §5 requires. The dispatcher writes a diagnostic but does not update `SESSION_CHECKPOINT.md`.

**Budget projection — question 4**

The evidence does **not** establish that a normal run will probably exceed 465 minutes. Training throughput is explicitly unmeasured; the 20–38-minute attempt estimate assumes 2–4 effective fp32 TFLOP/s (`prereg:289–312`). The older ≈33-minute harness anchor does not measure this fp32 trainer or the expanded evaluation (`results/research_pass_2026-10-06/hypotheses.md:8`).

The implemented admission calculation is exact (`step0.py:291–300`):

`preflight minutes + all completed-attempt minutes + max(38, slowest normalized 400-step attempt) × pending 400-step equivalents + 190`.

Consequences, reproduced by calling that pure function without model imports:

| Scenario | Projected P1 minutes | Default admission |
|---|---:|---|
| Preflight 70; no training yet | 450 | Pass |
| Preflight 85; no training yet | 465 | Pass |
| Preflight 86; no training yet | 466 | Refuse before `p1-a1` |
| Preflight 85; five completed 38-minute attempts | 465 | Pass |
| Preflight 85; five completed 45-minute attempts | 500 | Refuse |
| Preflight 85; five completed 60-minute attempts | 575 | Refuse |

**My conditional planning projection:** 335–465 minutes of actual P1 work using the preregistered assumptions; 360–465 minutes in the admission calculation at eval entry because it always reserves 190 minutes for eval. Neither is a measured forecast. At the upper estimate there is zero headroom. One 45-minute first attempt with an 85-minute preflight already projects 500 minutes before `p1-a7`.

A conservative refusal can occur even when eventual runtime would fit: an 86-minute preflight immediately projects 466, although five 20-minute trainings plus a 165-minute eval would total 351. This is a projection-policy stop, not scientific failure (`step0.py:291–312`; `prereg:314–316`).

The 90-minute attempt guard is independent: increasing the P1 budget does not relax it (`train.py:42–48,155–161,213–217`). Likewise, an admitted eval can still exceed its separate four-hour guard; 465 is not a continuously enforced aggregate wall-clock deadline (`read.py:113–119`; `eval.py:77–82`). The cheapest uncertainty-reducing measurement is the already-authorized preflight followed, if admitted, by `p1-a1`—then inspect measured times before continuing.

**Advisories**

- **Offline trainer cache:** required tokenizer/config/index files and both weight shards currently exist at the pinned model snapshot. The previous review verified offline resolution (`results/c10w_oracle_fix1_review.md:38,95`). Trainers force that cache and offline mode before importing Transformers (`train.py:148–151`). No missing model file was identified; this review did not repeat a model load.
- **Identity checks:** current prereg SHA matches `read.py:20`; engine fingerprint freshly PASSed with SHA `d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65` and three `_cov_cpu` sites (`tools/engine_fingerprint.py:34–47`).
- **Recheck GPU exclusivity at launch.** The earlier absence observation is not a reservation; serialization is an operator obligation, not enforced by this launcher (`tools/run_c10w_stage.sh:1–15`; `prereg:271`).
- **Read results through the reader.** A validation failure can leave PASS-labelled `eval.json` alongside HALT evidence; exit status and revalidation bind (`eval.py:456–464`; `results/c10w_oracle_fix1_review.md:47–54`).
- **F1 scope is preserved:** this measures an oracle beside the write engine; P1 alone yields no final scientific label or routing (`prereg:15–23,532`). No frozen design change is recommended.

Graft: one failed invocation; no token savings reported.