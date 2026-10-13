VERDICT: PROCEED-WITH-CHANGES
Reviewer: Claude Opus 5.5 advisor (independent), 2026-10-07

# D-C10w-oracle step 5, P1 only: pre-run readiness check (oracle measurement, not a route)

Scope: HEAD 6b7160e, branch worktree-c10k-route-a. I did not read Astra's parallel output. Nothing loaded the model or used MPS.
**Most important thing to do next:** add a projection check before every stage (B2). Without it, a normal-speed preflight or a single underfit leaves a HALT that cannot be resumed and throws away 1.5–4 h of measured work.
Labels: **EV** = evidence I ran or read (cited). **INF** = my inference.

## BLOCKING (both fixable in the launch plan; no code change)

**B1. Every stage launch fails on LLMDB_ROOT (`tools/run_c10w_stage.sh:9–11`).**
- EV: `.claude/settings.json:85` exports `LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory` (the main checkout) into every Bash-tool shell. `env` in this session shows that value.
- Failure: plan step 3 runs `bash tools/run_c10w_stage.sh step0` without overriding it. The launcher prints `HALT: INVALID-ENVIRONMENT` and exits 2 before anything runs. Plan item 5 then stops the run.
- No directory is created, so the failure is harmless. But the run never starts.
- Smallest fix: launch every stage as `LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a bash tools/run_c10w_stage.sh <stage>`.
  - Use the exact string, with no trailing slash. The launcher compares strings against `pwd` (`:8`).
  - The fingerprint command in plan step 2 already does this.

**B2. A budget refusal at a training stage or `p1-eval` HALTs the P1 directory for good, and the plan checks nothing beforehand.**
- EV, mechanism:
  - The guard runs after `directory=p1` is set (`step0.py:364`, `:378`, `:381`, `:394`), so a refusal writes `HALT.json` (`step0.py:408–411`).
  - `latest_directory` then refuses that directory permanently (`read.py:479`).
  - A budget ruling recorded after the refusal cannot resume the run. Recovery means a new `p1-preflight` and all trainings again.
- EV, projection formula (`step0.py:291–300`): preflight wall time + spent training + 38 min × every pending 400-step unit (38 is a floor, never lowered by faster measurements) + a fixed 190 min for eval, against 465 (`read.py:23`, `:117–119`).
- EV, refusal points, computed by calling `S.training_projection` with synthetic records:
  - (a) **`p1-a1` refuses whenever the preflight wall time exceeds 85.00 min.** 85 min projects 465.0 and passes; 85.01 projects 465.01 and is refused. My preflight projection is 65–95 min (A1), so this is a material risk: INF, roughly 1 in 4.
  - (b) **An 800-step retry is refused at realistic times**, inside the same stage (`step0.py:381`). It costs every adapter trained so far.
    - O-A7 underfits after O-A1 (preflight 75 min, 25-min attempts): 543.
    - O-A7-shuf underfits at the end: 527.
    - Only a fast O-A7-canon retry fits (preflight 60 min, 15-min attempts): 447.
- Halting for a ruling is what the prereg requires (§2.9:314, :316). Making that halt permanent is what costs the run.
- Smallest fix (plan):
  1. After `p1-preflight` exits 0, and before each of `p1-a1` … `p1-shuf` and `p1-eval`, compute the projection model-free. Use `S.training_projection("P1", <p1>/preflight.json, [<p1>/train/*.json], {next_unit: 400})` plus the retry case. `step0.py` imports only the standard library and `read.py`.
  2. If either exceeds 465, stop. Get the operator's budget ruling, record it as a runbook §5 D-ID, and place it before dispatching the stage as `<p1>/authorization_P1.json` = `{"P1":{"authorized":true,"recorded_by":"…","recorded_at":"…","budget_minutes":N}}`. That is the schema checked at `step0.py:309–312`.
- Operator decision to take now:
  - Recommended: size N once the measured preflight time is known, as the projection plus one matched 800-step pair (+152 min under the code's floor).
  - Alternative: accept that any underfit ends this P1.

## Changes to the launch plan (non-blocking)

**C1. Freeze the frozen inputs for the length of P1.**
- EV: `load_frozen` re-hashes the prereg against `PREREG_SHA` (`read.py:20`, `:486`), and every source listed at `step0.py:242–255`. It runs at every dispatch (`step0.py:346`), in the trainer (`train.py:140`) and in the eval (`eval.py:355`).
- Do not fold this review or Astra's into `docs/C10W_ORACLE_PREREG.md` §7. Record them in the runbook or checkpoint.
- Keep Codex sessions off these files: `c10e_bandknob.py`, `c10p_twopass_arms.py`, `configs/hparams/qwen25_3b_memit_hparams.json`, `configs/screens/g6_screen_qwen3b*.json`, `tools/engine_fingerprint.py`.
- A mismatch caught at dispatch is refused before `directory` is set, so it is recoverable by reverting. It still stalls the run.

**C2. Never dispatch a stage twice or out of order.** Each case below writes `HALT.json` into the P1 directory, even after a passing eval:
- a repeat `p1-eval`: "stage log exists" (`step0.py:277`);
- a repeat training stage: "training record already exists" (`train.py:146`, in the child);
- a repeat `p1-project`: "record exists" (`read.py:83`);
- a training stage launched while its predecessor is still running: "prior training unit incomplete" (`step0.py:373`).

Before launching the next stage, wait for the backgrounded launcher process itself to exit 0. Then confirm `STAGE_EXIT=0` in `<p1>/<stage>.log` and that no `HALT.json` exists.

**C3. Re-check that the GPU is free at each launch, not only at 14:45.**
- EV: step 3 is currently a parent (pid 2262) plus a child (pid 16167) (`ps`). Wait for the parent to exit.
- Run `pgrep -fl "c10u_mint2|ollama|autoresearch"` immediately before `step0` and before each stage. The rule is §2.8:273.

**C4. Cross-family implementation review.**
- EV: §5:448 requires the cross-family reviewer at the implementation review. Both implementation reviews on file are by Claude Opus (`results/c10w_oracle_advisor_impl.md:5`, `results/c10w_oracle_fix1_review.md:5`). The builder was Codex GPT-6 (`results/c10w_oracle_codex_build.md:3`).
- Before `step0`, record a ruling that Astra's parallel pre-run check discharges this requirement, or run that review. Otherwise the P1 record is procedurally open.

**C5. Put the operator's go on record before `step0`** (§5:448: "runs only on the operator's go"), with a timestamp, together with the selftest and torchcheck output.
- The torchcheck is CPU-only (every tensor in `torchcheck.py:30–50` is on `device="cpu"`), so it can run now.

## Advisories and answers

**Q1 — stage names, order and inputs: they match.**
- EV: the plan's nine stages equal `stage_names()` for P1 (`read.py:469–471`). Training order equals `TRAIN_UNITS["P1"]` (`read.py:28`, `:31`) and §2.8:274–278.
- Enforcement:
  - earlier units must have PASSed (`step0.py:370–373`);
  - the eval needs all five trainings (`read.py:499–508`);
  - `p1-project` needs `eval.json`;
  - `p2-*` and `p3-*` are refused without an authorization file, before any directory is created (`step0.py:353–356`).
- No stage takes an argument. The only environment input is LLMDB_ROOT (B1). The only optional file is `authorization_P1.json` (B2).

**Q2 — false HALTs and stale state.**
- EV, step 0 dependencies:
  - `HfApi().dataset_info("cais/mmlu").sha` returned `c30699e8356da336a370243923dbaf21066bb9fe` from this sandbox today. That equals the pre-fetched revision.
  - I replicated `freeze_mmlu` offline on the cached arrow files: 14042 test rows / 285 dev rows, letter token ids [362], [425], [356], [422], and 0 of 200 failures on the `Answer:` suffix concatenation check. Prompt length is median 505 tokens, max 2295.
  - Model-free, the step-0 audits pass: S1–S5 `ok`, template SHA, the S3 table, 22 S7 verdicts, and the S6 trainer-source check.
- EV, offline trainer: with `HF_HOME=<worktree>/hf_cache` and `HF_HUB_OFFLINE=1`, the tokenizer, config, index and both shards (3.97 GB and 2.20 GB) resolve at `MODEL_REV`.
- Residual risk: step 0 needs the network. A failure there HALTs only its own step-0 directory, and a fresh `step0` sorts later and is used instead (`read.py:476–478`). The model weights were not loaded here: UNVERIFIED for `.float()` after `device_map="mps"` (`train.py:168`).
- EV, stale state: none.
  - `results/c10w_oracle` does not exist.
  - `architecture_profile/` exists.
  - The frozen files are unmodified relative to HEAD, and the prereg SHA-256 `2baeb4e9…` matches `read.py:20`.
  - Adapters are ignored by `.gitignore:25` (`git check-ignore`).
- EV, gates: fingerprint PASS (`d941a9fb…`, `_cov_cpu` 3). Selftest 63/63 with both LLMDB_ROOT values.

**Q3 — prereg requirements missing from the plan.** These are C3, C4 and C5, plus the budget-ruling record in B2. The P1 re-projection and stop rule (§2.8:278) are automated at `step0.py:399–406`.

**Q4 — will the 465 limit refuse a normal run? (INF)**
- Projection, actual wall time:
  - preflight 65–95 min (centre about 75);
  - training 10–20 min per attempt, 5 attempts = 50–100 min;
  - P1 eval 125–175 min;
  - total 240–370 min.
- Code projection at `p1-eval`: preflight + spent + 190 ≈ 305–385 min, which passes.
- So `p1-eval` is unlikely to be refused, unless a training attempt runs past 38 min or a retry occurs. The binding refusal points are `p1-a1` (preflight > 85 min) and any retry (B2).
- Basis:
  - (i) One full harness pass (A1 + A2 + A7 with setup and LAW#5) takes 33 min on this machine: three passes ran 02:15–03:54 (`CORPUS/50_C10Q_STACKED_SOLVE.md:3`). A 2-arm recipe with 24 z-captures took 24.5 min (`results/c10u_mint2/r3/F_r0_multi_snone*` mtimes 11:16:05 → 11:40:34).
  - (ii) The preflight adds, by my count of `eval.py:119–208`:
    - U on four maps plus the null arm;
    - per map, about 1,100 short forwards plus a 131k-token MMLU pass;
    - probes and geometry on each closed-form arm.
  - (iii) Trace overhead: `recipe_trace` drops non-target frames (`eval.py:319–320`), but a call event still fires for every Python call in a recipe. On a dispatch-bound 36-layer Qwen2 forward on CPU (my benchmark), tracing made it 1.30× slower. I applied that as an upper factor on recipe time.
  - (iv) Training FLOPs: about 7.4e12 per step (the backward pass computes input gradients only, because the base is frozen), × 400 steps. At an assumed 3–6 TFLOP/s effective fp32 that is 8–17 min, plus 2–3 min for load, hashing and the fit check. No MPS training has been measured on this machine (§2.9 says so).
- The 4-h eval limit (`read.py:113–114`) keeps at least 65 min of margin at the top of my eval range.

**A-HW.** EV: `system_profiler` reports an Apple M3 Max with a 40-core GPU and 48 GB. CLAUDE.md and §2.9 say "M3 Pro". Record the actual chip in the P1 record and CORPUS. Training throughput is likely better than §2.9's 2–4 TFLOP/s assumption.
