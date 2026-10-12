# memory_mirror audit — 2026-10-10

Operator request: "Run an additional audit on the current MEMORY.md to identify stale, duplicate, bloated, incorrect, misleading, etc entries."

Method: mechanical checks by MAESTRO3, then three read-only reviewers (54 indexed notes; 57 + 58 unindexed notes) under one brief (`brief.md`) requiring a file:line or command citation for every non-KEEP verdict. MAESTRO3 spot-checked the highest-impact claims (marked ✔ below) against the repo.

## Structural
- 169 notes, 54 indexed — **115 notes (68%) invisible from the index**.
- 27 notes with missing/invalid frontmatter (mostly the `anyedit-*` June pilot cluster).
- 18 of 54 index lines exceed 200 characters; lines 47–54 are mostly `⟨D-ID@hash⟩` ledger tokens with no behavioral cue.
- Duplicate index topics: two LLMDB_ROOT notes, two GPU-gate notes.
- Fixed in 145bd3f: 26 live notes never mirrored; the close-out sync check pointed at the pod path and skipped silently.

## Proposed actions (all 169)
keep 34 · fix-text 63 · de-index 14 · merge 16 · retire 42 — per-note rows with evidence in `audit_*.md`.

## Actively wrong or dangerous (verified ✔)
- ✔ `commit-forward-work-without-asking.md` — commit to `master` + ff-merge; contradicts the binding push-to-branch / never-merge rule.
- ✔ `verify-external-artifacts-before-effort.md` — its core example (BetaEdit arXiv 2605.09285 "fabricated") is false; the paper is real (IJCAI 2026). Runbook row 295 repeats it.
- ✔ `c10-mint2-r3-provisional-no-direction.md` — says r3 ratification pending; CORPUS/54:3 records ratification 2026-10-07.
- ✔ `c10k-route-a-resume.md` (21.9 KB, index line 8) — "step 1 HALTED, loop PAUSED"; step 1 closed UNDERFIT (CORPUS/51); wrong PR (#21 is the open one).
- `llm-as-database-program-overview.md` — says the engine is gitignored; `git ls-files memit_dry_run` = 143 tracked files ✔.
- `deployment-target-intel-cpu.md`, `operator-profile-llm-as-database.md` (deployment "TBD, remote GPU OK"), `betaedit-official-repo.md` (A3 "going ahead"; runbook:148 PARKED), `autoresearch-editing-loop-per-fork.md` (wrong model/effort), three pod-era Codex notes (gpt-5.5, /workspace), `background-monitor-no-premature-read.md` (foreground sleep, now blocked).
- LLMDB_ROOT origin: it is exported by `.claude/settings.json:85`, not a shell profile (no hit in ~/.zshrc/.zprofile/.zshenv ✔); two notes blame the login shell.
- `backup-via-memitbackup-app.md` calls the internal-SSD mirror durable; ✔ its last run (2026-10-09 17:56) ended FATAL on a benign rsync exit 24 and none has logged since.
- `disk-budget-before-dispatch.md` says gdrive pending (authorized 2026-10-10).

## Outside memory (verified ✔)
- ✔ `.codex/config.toml:46` — Perplexity MCP points at `/workspace/tools/perplexity_mcp_from_restore.py`; `/workspace` does not exist.
- ✔ `EXPERIMENT_RUNBOOK.md:225` — mirror instruction still copies `/root/.claude/projects/-root/memory` → `/workspace/memory_mirror/` (both pod paths).
- Runbook §0.3 generated block still says native builds are blocked on Command Line Tools (fixed 2026-10-07) — fix in `docs/program_state.json`.
- Runbook lines 146, 238, 860 link notes proposed for retirement.
- `docs/AUTORESEARCH.md:20` describes the pre-v13 launcher.
