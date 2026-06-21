# Memory Index

## ⭐ START HERE (fresh session) — read `/workspace/SESSION_BOOTSTRAP.md` FIRST.
## ⭐⭐ For ANY experimental work — `/workspace/EXPERIMENT_RUNBOOK.md` is the living canonical roadmap+discipline; its §0.3 = single source of "what's next". See [experiment-runbook-is-canonical](experiment-runbook-is-canonical.md).
It re-grounds the whole "LLM-as-Database" program: goal, the months-long experiment arc, what's PROVEN vs OPEN, the next work, working norms, and environment/persistence. (Status 2026-06-18: CP1-3 + G1/G2/G3 all PROVEN-FOR-SCOPE; **G6/G7 is next — the first empirical run that can actually falsify the spec**.) Then read `/workspace/CORPUS/README.md` (evidence single-source-of-truth) and the spec `research_and_specs/llm-as-database-v1_2-integrated-spec.md`. The current state of the program is NOT in this index alone — the bootstrap + CORPUS are authoritative.

## Process & collaboration learnings (how to work — apply across sessions):
- [Read authoritative source fully](read-authoritative-source-fully.md) — consume the governing spec/source end-to-end BEFORE framing load-bearing decisions; grep-excerpts misframed the whole bridge question this session
- [Calibrate confidence: mechanics ≠ contracts](calibrate-confidence-mechanics-vs-contracts.md) — over-claimed repeatedly + got corrected; under-claim, distinguish tested/untested/inferred, call advisor when most confident
- [Exhaust options before "blocked"](exhaust-options-before-blocked.md) — operator's certainty-challenges repeatedly surfaced real no-code wins (ROUTE VERIFY, rollback-by-base, COMPILE, .vlp bridge); re-search, don't re-defend
- [Review has diminishing returns; evidence is binding](review-diminishing-returns-evidence-is-binding.md) — bound investigations; same-model council = confirmation-amplification; use a different model for independence; gather evidence over re-reviewing
- [Operator profile (LLM-as-DB)](operator-profile-llm-as-database.md) — spec owner, learning ML, effective adversarial check; make decisions legible, defer to evidence, deployment target TBD (maybe remote GPU)
- [Standing auth: forward requirements](standing-auth-forward-requirements.md) — infra (disk/downloads/cov-compute/model pulls) is PRE-APPROVED when needed to keep experimenting toward a solution; do it + narrate, don't defer as hidden blocks
- [Prototype tautology trap](prototype-tautology-trap.md) — self-authored contract prototypes (CP1-G3) test your own control-flow, not the contract; build tests that can actually fail (detection/forgery/divergence, not construction/identity/round-trip); call advisor BEFORE authoring the test set; design-viability ≠ empirical evidence — reserve confidence for runs that can falsify (G6/G7)
- [Evidence over scaffolding](evidence-over-scaffolding.md) — when the next experiment is runnable (coded, cached, cheap), RUN it; don't let synthesis/prompt/runbook authoring accrete while empirical evidence stalls (the meta-vs-territory trap, advisor-caught this session)
- [Match metric to the claim](match-metric-to-the-claim.md) — measure the metric matching the claim (top-1 for read-correctness, JS/KL for distributional); never judge two sides of a comparison on different metrics; asymmetric metrics hide failures in the mid-range where falsification lives (G6.1); +Ext3 (A2b): switching metrics can SWAP confounds — condition on pre-state, paired within-unit diff cancels shared bias, pre-screen the eval pool
- [Resolve the gate's real criterion](resolve-the-gates-real-criterion.md) — on a decision gate (esp. under "use your judgment"), answer the gate's ACTUAL criterion not a flattering adjacent one; deferral ≠ license for the ambitious path; treat non-assertion as evidence
- [Verify external artifacts before effort](verify-external-artifacts-before-effort.md) — verify repo-existence / arXiv IDs / "no implementation" claims (clone, WebSearch, fetch abstract) BEFORE they gate an effort estimate; a fabricated arXiv id + unchecked "no public repo" nearly drove a 1–2 day reimplement of a few-hours port (BetaEdit)

## Durable lessons / traps:

- [RunPod durable experiment launch](runpod-durable-experiment-launch.md) — setsid+`python -u` so disconnects don't kill long MEMIT runs
- [RunPod dashboard vs pod metrics](runpod-dashboard-vs-pod-metrics.md) — dashboard GPU/RAM/disk % diverge from nvidia-smi/free/df; trust in-pod tools; GPU memory.used is binding, util% just reflects our own work
- [MEMIT cov-inversion not a hang](memit-cov-inversion-not-a-hang.md) — frozen log + 0/1000 + CPU-busy/GPU-idle is normal compute, not a stall
- [RunPod session disconnect cause](runpod-session-disconnect-cause.md) — context loss = no tmux + no sshd keepalive, not a pod restart
- [EasyEdit assets vendored](easyedit-assets-vendored.md) — /workspace/easyedit_assets parts bin mapped to escape-hatch rungs; usage rules + caveats
- [Gemma 4 rung-4 candidate](gemma4-rung4-candidate.md) — logged model-swap candidate (E4B best fit); eval + Perplexity prompt in /workspace/gemma_rung4_candidate_note.md
- [Deployment target: Intel CPU](deployment-target-intel-cpu.md) — end product must run on operator's local Intel CPU; separates edit-time (GPU/offline) vs inference (CPU); raises GRACE + small-model appeal
- [molab migration assessment](molab-migration-assessment.md) — don't migrate primary workflow (storage + unattended-job blockers); molab niche = interactive Gemma big-model probes; Modal/Lightning better for unattended
- [LARQL & the-mechanism prior art](larql-the-mechanism-prior-art.md) — LARQL (in the spec) = vindex+LQL+CPU-deploy+MEMIT-class write; our same-entity-locality work fills its gap; late-band editing cross-ref; repos in /workspace/external_prior_art
- [BetaEdit official repo](betaedit-official-repo.md) — A3 dependency: lbq8942/BetaEdit (IJCAI 2026) cloned to external_prior_art/BetaEdit; ships our-exact qwen2.5-3b config; solve = AlphaEdit + λ1·Σ + τ-P-refresh (A2 sentinels = low-rank shadow); PORT not reimplement; re-tune for N=100/base; no LICENSE
- [Durable artifact path collision](durable-artifact-path-collision.md) — adding a script mode can silently overwrite a canonical result via the default output-path branch; check path logic, recover by re-running not fabricating
- [Verify canonical-state edits persist](verify-canonical-state-edits-persist.md) — runbook edits from a prior turn were silently absent on a later read; re-read load-bearing state files (esp. §0.3) after editing; keep CORPUS+checkpoint primary
- [Scope gate: batch is the deployment model](scope-gate-batch-is-deployment-model.md) — A3/BetaEdit parked (no headroom on the batch path A1 already solved); Q4_K quantization survival is the real next falsifier; advisor caught a criterion-swap
- [B3/G6.2 PASS: Q4_K_M quantization survival](q4km-quantization-survival-pass.md) — the A1-clean batch in-weight store survives real Q4_K_M (edits 100% vs native 97.4%, CPU inference serves edits); margin confound characterized; E1 deployment loop still untested
- [Repo reorganized — LLMDB_ROOT](repo-reorganized-llmdb-root.md) — 2026-06-18 the flat-root scatter became experiments/configs/results/logs/docs/archive; scripts use LLMDB_ROOT; files NOT at root anymore
- [Bias-ablation = causal attribution](bias-ablation-causal-attribution.md) — to prove a component CAUSES a failure, ablate it in a clean reference model (A7 turned the E1 bias correlation into proven sufficiency)
- [Pass label ≠ promotable claim](pass-label-not-equal-promotable-claim.md) — a mechanical pre-registered PASS is a review starting point, not a PROVEN claim; deep-thinking + cross-model independence can downgrade it to CONFOUNDED (C2-band, CORPUS/21, D-C2band-1)
- [Autonomy ERROR label can mask a completed run](autonomy-error-label-can-mask-completed-run.md) — driver wall-clock can expire between run-finish and staging; check result-JSON mtimes vs the staged timestamp before trusting ERROR/INVALID
- [Codex ChatGPT-OAuth model slug](codex-chatgpt-oauth-model-slug.md) — Codex+ChatGPT-OAuth rejects gpt-5/gpt-5-codex; use gpt-5.5 (the default)
- [Autonomy driver stale-guard deletes result](autonomy-driver-stale-guard-deletes-result.md) — driver unlinks the unit result_json before re-running; back expensive results with source/arm JSONs
- [Pod restart wipes system-python ML stack](pod-restart-wipes-system-python-ml-stack.md) — reinstall transformers==4.51.0 pin (torch survives); use python3.11
- [Commit forward work without asking](commit-forward-work-without-asking.md) — operator standing-auth: commit to local master freely; push/PR still gated
- [Null label can hide a real effect](deterministic-null-label-can-hide-real-effect.md) — inspect the paired sign pattern, not just the verdict string/threshold
- [Single-seed limits generality not significance](single-seed-limits-generality-not-significance.md) — a within-experiment contrast can be real at 1 seed; replication buys generality
- [Control-relation effective cardinality](control-relation-effective-cardinality.md) — check confident+correct+single-tok pool's effective distinct values, not nominal
- [Codex review: embed evidence + medium effort](codex-review-embed-evidence-and-effort.md) — sandbox can't read files; high effort times out ~600s
- [Memory paths & mirror discipline](memory-paths-and-mirror-discipline.md) — live -workspace/memory wiped on restart; mirror is canonical; don't clobber the index
- [Sequential-edit run nondeterminism](sequential-edit-run-nondeterminism.md) — held-out corruption swings ~50pp run-to-run on SAME config (GPU nondeterminism); single-run absolutes unreliable, re-run outliers before believing them
- [Wide-intermediate 7B editing VRAM](wide-intermediate-7b-editing-vram.md) — Qwen2.5-7B in-solve AlphaEdit on 24GB: eigh-not-svd for P, diagonal-add not L2*eye, del Pi before solve, expandable_segments, BLAS=8
- [Calibrate symmetrically; unresolved is a verdict](calibrate-symmetrically-unresolved-is-a-verdict.md) — refuting an over-claim ≠ licensing the opposite null; default correction to UNRESOLVED/weak-lean; read sign pattern not noisy mean
- [Background monitor: no premature read](background-monitor-no-premature-read.md) — don't Read a background sleep's output before it finishes; foreground sleep+check or wait for the task-notification
- [Close-out gate before done](closeout-gate-before-done.md) — every experiment close ends with `tools/closeout_check.py <D-ID>` = ✅ ALL GREEN; canonical-tracker close-out is mechanical, not the operator's job to check
