S2.34 Kickoff — BOS-Lookup Fix + Llama-vs-Qwen Internal-Stage Geometry Probe (resume)

Session type: Execution (pod-side). Resumes the S2.33 diagnosed halt. Diagnostic, not a verdict arm — produces a mechanism localization, no clear/hold verdict.

Predecessor: S2.33 — HALT_DIAGNOSED. Llama compute_z trajectory capture surfaced a BOS off-by-one in subject-last fact-lookup for the direct (out-of-pipeline) compute_z call: Llama-3 tokenizer auto-prepends <|begin_of_text|> (id 128000) at index 0; GPT-J-authored repr_tools subject-index path does not subtract for it; subject_last resolves to ' plays' (idx 3) not ' Jackson' (idx 2). Trajectory non-canonical (endpoints miss v1.5 §3 by ~3 OOM). No data promoted. Two cheap fixes ruled out; confirmed NOT a documented patch.

Scope: Fix the lookup, clear the correctness gate, then complete BOTH probe arms in one session:
1. Fix the BOS off-by-one so find_fact_lookup_idx lands on the subject-last token, then re-run the Llama Bo Jackson→guitar compute_z trajectory capture (all 25 steps, or fewer if early-break).
2. HARD GATE: Llama endpoints must reproduce framework_finding v1.5 §3 (first avg-prob ~1.6e-08, last ~1e-4, loss ~17.96→~9.35) before any data counts or the Qwen arm runs.
3. Qwen2.5-7B trajectory capture, matched config (band [4,5,6,7,8], v_loss_layer 27, z_layer 8; P-VRAM-CPU-SOLVE required).
4. Entanglement Probe B (Qwen-only): per-layer delta-norm contribution vs same-subject biographical drift (v1.6 §3.4 thread).

Read order:
- session_2_33_summary_block.md (predecessor close; §3 bug detail + §6 resume steps are load-bearing)
- /workspace/architecture_profile/s233_halt_diagnostic.json (full bug state + corrupted trajectory for diffing) — on NV, not KB
- framework_finding v1.6 §2.2 (Qwen convergence numbers to reproduce) + §3.4 (entanglement thread → Probe B)
- framework_finding v1.5 §3 (the Llama-stall / Qwen-converge endpoints — THE correctness gate)
- t_branch v1.4 §4'''' (Axis 2 routed; Axis 3 breadth deferred)
- memit-patches-canonical v2.6 (P-VRAM-CPU-SOLVE live; the engine is left patched)
- cfb-v3 + probe-set-v3 (held verbatim)

First actions at entry:
1. Engine state PATCHED: grep -c "_cov_cpu" memit/memit_main.py = 3; SHA = 5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770. If a fresh pod reset it, re-apply via patch -p0 from cpu_solve_patch.diff (C-S232-1: normal-format, NOT git apply).
2. Kernel hygiene: HF_HOME=/workspace/hf_cache before any HF import; os.chdir(ENGINE_ROOT) before from memit import; clean kernel.
3. Pad-Token: Llama base pad_token=None — apply pad=eos before any compute_z dispatch (C-S232-2).
4. Load hparams from /workspace/architecture_profile/meta-llama_Llama-3.1-8B.json (DOTS not underscores); override band to [4,5,6,7,8] (D-S233-BAND-1; JSON carries stale [2,3,4,5,6]); assert v_loss_layer==31, band==[4,5,6,7,8], z_layer==8.

The fix (first technical step):
- READ-ONLY: cat -n rome/repr_tools.py — locate get_words_idxs_in_templates (the subject-index computation find_fact_lookup_idx delegates to for subject_last). Determine how/whether it accounts for a prepended BOS.
- Most likely fix: tokenize the lookup with add_special_tokens=False so no BOS is prepended at the lookup step. Confirm at the index level (find_fact_lookup_idx returns the ' Jackson' index) BEFORE re-running the expensive trajectory.
- If the fix is a source change to the science path, apply in-session-patch-isolation discipline (C-S232-CPUSOLVE-1 lineage): isolate against a known result before promoting any data produced under it.

Deliverables at close:
- session_2_34_summary_block.md
- z_convergence_trace_llama_vs_qwen.json (the raw per-step trajectories — primary mechanistic evidence)
- framework_finding v1.7 (ADDITIVE, conditional on probe result): internal-stage localization (where Llama stalls / Qwen converges, step-resolved) + entanglement-layer finding.
- Resolve the deferred manifest merge (D-S233-MANIFEST-1): merge the two divergent reproducibility manifests to a verified union; write S2.33 + S2.34 entries into the merged manifest.

Carried decisions (stand): D-S233-LAYERMATCH-1 (native v_loss_layer per model), D-S233-BAND-1 (band override), D-S233-CAPTURE-METHOD-1 (direct compute_z, no weight write). Deferred: D-S233-MANIFEST-1 (manifest merge).

Specialist routing: memit-specialist (primary), state-consistency-theorist (secondary), framework-spec-writer (artifact authoring). validation-contract-architect inactive.

Open decision surfaced for entry: if reading repr_tools shows the canonical pipeline handles BOS correctly only in the full-pipeline call path (not the isolated one), decide whether to (a) keep the direct-compute_z method with the add_special_tokens=False fix, or (b) switch to driving the trajectory through execute_memit (which self-restores weights, invariant per memit_main lines 230–233) so the lookup runs through the exact canonical path. Recommend (a) if the index-level fix reproduces v1.5 §3 endpoints; fall back to (b) if it does not. Resolve at the gate.
