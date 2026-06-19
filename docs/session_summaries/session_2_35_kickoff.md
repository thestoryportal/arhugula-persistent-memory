# S2.35 Kickoff — Llama-vs-Qwen Internal-Stage z-Geometry Probe (CORRECTED harness; supersedes the S2.34 BOS-fix premise)

Session type: Execution (pod-side). Re-issues the S2.34 scientific goal on a CORRECTED basis. The S2.34 "BOS off-by-one fix" premise is FALSIFIED (see below). Diagnostic arm — produces a mechanism localization, no clear/hold verdict.

## What changed since the (now-void) S2.34 kickoff — READ FIRST
S2.34 re-diagnosed the S2.33 halt and found there is **no BOS lookup bug**. Lookup **index 3 (` plays`, the token after the subject) is canonical** — the promoted session 2.24 run (`t1_alpha_memit_s224.ipynb`) uses it and reproduces v1.5 §3 (loss 18.145, avg-prob 1.39e-08). The actual S2.33 defect was a **missing leading space on the target string** in a *direct* `compute_z` call, which bypassed the space-prepend in `execute_memit` (`memit_main.py:80-82`). Full evidence: `architecture_profile/s234_halt_diagnostic.json`.

Net effect on the plan: the lookup is NOT to be touched; the only harness change is the target string. Otherwise the scientific goal (Llama-vs-Qwen z-geometry + Qwen entanglement Probe B) stands unchanged.

## Read order
- session_2_34_summary_block.md (this re-diagnosis; load-bearing)
- architecture_profile/s234_halt_diagnostic.json (corrected root cause + canonical reference; SUPERSEDES s233_halt_diagnostic.json — do NOT act on s233's root cause)
- t1_alpha_memit_s224.ipynb cell 10 (canonical request construction: target = " " + object) + its compute_z stdout (the index-3 / §3-reproducing reference)
- framework_finding v1.6 §2.2 (Qwen convergence numbers) + §3.4 (entanglement thread → Probe B)
- framework_finding v1.5 §3 (Llama-stall / Qwen-converge endpoints — THE correctness gate)
- memit-patches-canonical v2.6 (P-VRAM-CPU-SOLVE live; engine left patched, UNMODIFIED)
- cfb-v3 + probe-set-v3 (held verbatim)

## First actions at entry
1. Engine fingerprint gate: `sha256(memit/memit_main.py) == 5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770`; `grep -c "_cov_cpu" memit/memit_main.py == 3`. Mismatch → HALT. (Do NOT patch repr_tools/compute_z; the lookup is correct.)
2. Kernel hygiene: HF_HOME=/workspace/hf_cache before any HF import; os.chdir(ENGINE_ROOT) before `from memit import`; clean kernel.
3. Pad-token (C-S232-2): Llama base pad_token=None → set pad=eos before any compute_z dispatch.
4. Hparams from /workspace/architecture_profile/meta-llama_Llama-3.1-8B.json (DOTS not underscores); override band → [4,5,6,7,8] (D-S233-BAND-1); assert v_loss_layer==31, band==[4,5,6,7,8], z_layer==8.

## The corrected harness fix (first technical step — cheap, do before the expensive trajectory)
- Build the request with the canonical target form: `target_new.str = " guitar"` (LEADING SPACE), matching s224 cell 10 and execute_memit:80-82. Equivalently, in the direct-compute_z harness, prepend a space when `target_new.str[0] != " "`.
- Sanity at the cheap level BEFORE the 25-step run: confirm `find_fact_lookup_idx` prints `Lookup index found: 3` and `Token:  plays` (canonical — unchanged), and confirm the rendered rewriting sentence ends `…instrument of<|begin_of_text|>` (NOT `…<|begin_of_text|>g`).

## HARD GATE (LAW #3) — run BEFORE any data is trusted or the Qwen arm starts
- Re-run the Llama Bo Jackson→guitar direct compute_z trajectory. Step-0 must land near loss ~18.1 / avg-prob ~1.4e-08 and endpoints near v1.5 §3 (first avg-prob ~1.6e-08, last ~1e-4, loss ~17.96→~9.35).
- Miss by >1 order of magnitude → harness still wrong → HALT (one-fix-then-halt discipline).

## Scope after the gate clears
1. Llama-3.1-8B z-trajectory capture, all 25 steps (cfb-v3-001), corrected harness. Lookup index 3 (canonical).
2. Qwen2.5-7B trajectory capture, matched config (band [4,5,6,7,8], v_loss_layer 27 [native, D-S233-LAYERMATCH-1], z_layer 8; P-VRAM-CPU-SOLVE required — verify _cov_cpu path engaged for the wide intermediate). Apply the same target-space discipline.
3. Entanglement Probe B (Qwen-only): per-layer delta-norm contribution vs same-subject biographical drift (v1.6 §3.4 thread).

## Deliverables at close
- session_2_35_summary_block.md
- z_convergence_trace_llama_vs_qwen.json (raw per-step trajectories — primary mechanistic evidence)
- framework_finding v1.7 (ADDITIVE, conditional on probe result): internal-stage localization (where Llama stalls / Qwen converges, step-resolved) + entanglement-layer finding.
- Resolve the deferred manifest merge (D-S233-MANIFEST-1 / D-S234-MANIFEST-1): merge the two divergent reproducibility manifests to a verified union; write S2.33 + S2.34 + S2.35 entries into the merged manifest. Until merged, NO manifest writes.

## Carried decisions (stand)
- D-S234-1/2/3 (re-diagnosis: index 3 canonical; target-space fix; engine untouched) — from S2.34.
- D-S233-LAYERMATCH-1 (native v_loss_layer per model), D-S233-BAND-1 (band override), D-S233-CAPTURE-METHOD-1 (direct compute_z, no weight write).
- Deferred: manifest merge.

## Specialist routing
memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (close artifacts). validation-contract-architect inactive.

APPROVE-TO-PROCEED:
