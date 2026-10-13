## FRESH SESSION HANDOFF - 2026-10-07 morning (context cleared at the operator's request; step 3 stage 1 RUNNING)

**State in one breath.** Overnight under the operator's standing approval (D-C10r-rulings-8: the program's recommendations are rulings until the operator intervenes; LAWs, halt discipline, reviewers, one GPU run at a time and no merges unchanged). Closed tonight, all through the close-out gate ALL GREEN:
- **CORPUS/51** D-C10s-sharedz ⟨@bee04393⟩: UNDERFIT.
- **CORPUS/52** D-C10s-solvefeas ⟨@7083a102⟩: UNDERFIT-AT-50, objective-stopped; injection 54 vs 72/72 in the unedited model, observation only.
- **CORPUS/53** D-C10t-secondkey ⟨@76a722d3⟩: NULL-LARGE-WRITE; 23 vs 15/72, write ×2.05, prefix spillover.
- **D-C10r-exp2ctl** location control: valid, NO-GAIN-WITHOUT-VALUE-POSITIONS, size confound remains; a candidate note, not CORPUS.

Draft PR #21 carries everything (the operator merges).

**RUNNING NOW:** step 3 **D-C10u-mint2** v3, stage 1 `reproduce` (the LAW#3 gate: mint-1(frozen) ×3), started ~06:50 UTC, ≈ 3–4 h. Command `bash $CLAUDE_JOB_DIR/tmp/run_c10u_stage.sh reproduce`, which wraps `experiments/track_c/c10u_mint2_arms.py reproduce --law3-ref results/c10l_covgeom/run1_armB_identity.json` with LLMDB_ROOT=<worktree>. Stage log `results/c10u_mint2_logs/reproduce.log`: it prints only "completed <job>" lines, with per-job logs in `results/c10u_mint2/logs/`. It ends with `STAGE_EXIT=<rc>`. Check it is alive with `/usr/bin/pgrep -fl c10u_mint2_arms`.
- **When it ends:** run the reader `LLMDB_ROOT=<worktree> .venv/bin/python -B experiments/track_c/c10u_mint2_read.py <worktree>/results/c10u_mint2` and commit the small records (never `results/c10u_mint2/edited`).
- **If LAW#3 passes:** the next stages, one at a time, per ruling D-C10u-budget (runbook §5.2) and the advisor's command list in `results/c10u_mint2_advisor_impl.md`: `frozen` → `v2` → `control` (only if triggered) → `replicate-F` / `replicate-V2` (as triggered) → `p4-save` → the P4 chain.
- **If LAW#3 misses:** HALT, keep the data, and write a diagnostic.
- **During the schedule:** no edits to the c10u files, the C10U prereg or `c10e_bandknob.py`; the first stage pinned their hashes. Then the Codex verdict and CORPUS/54 through the close-out gate, then step 4 (D-C10v-layerpick v2).

**Waiting on the operator:**
1. **The graft decision.** The loop sealing D-C10r-seal v3 + fix round 1 (c922b5c) cannot be probed or launched while any graft-enabled session is attached, because graft rewrites files in repositories on this drive. Recommendation: turn graft off for this project. The probe command is in `results/c10r_seal_codex_fix1.md` §6. Then LAW#3 equivalence, the cleaned-base score, the relaunch.
2. **Install TokenPrint** (a local live visualizer)? Offered, not approved; it must never run during a GPU run.

**Tools:**
- **Codex** runs interactively in tmux pane **%13** (session `codex`). Use the pane id: `-t codex` can resolve to `codex2`. Start each task with `/new`. Briefs name a unique output file; watch for it.
- **Memento's finalize-session** cannot reset this background session (no tmux or iTerm2 transport). Run the program session in tmux or iTerm2 if self-resets are wanted.
- **The Netron structure diagram** is at `visualization/qwen25_3b_2layer_structure.onnx` (gitignored).

**Kickoff prompt for the next session (paste as the first message):**

> Resume the LLM-as-Database program (F1, condition C10) as lead experimentalist. Recall memories c10k-route-a-resume, operator-overnight-autonomy-2026-10-06, operator-decision-scope, plain-language-to-operator and model-and-compute-allocation first. Worktree /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a, branch worktree-c10k-route-a, draft PR #21 (the operator merges). Never cd out; prefix every repo tool with LLMDB_ROOT=<worktree>; use /usr/bin/git; put commands with computed paths in script files. Read the SESSION_CHECKPOINT.md top block first: step 3 D-C10u-mint2 stage 1 `reproduce` may still be running (check `/usr/bin/pgrep -fl c10u_mint2_arms` and results/c10u_mint2_logs/reproduce.log). Continue the step-3 schedule stage by stage under rulings D-C10r-rulings-8 and D-C10u-budget, with Codex (tmux pane %13) for verdicts and the close-out gate for CORPUS/54. Speak to me in plain, non-technical language; bring me only go/no-go and scope decisions, recommendation first. Two decisions are waiting on me: the graft tooling decision for the loop sealing, and the TokenPrint install.

