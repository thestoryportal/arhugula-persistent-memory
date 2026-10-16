---
name: verify-canonical-state-edits-persist
description: "Write load-bearing state files via shell/python and re-read after a delay: Edit-tool writes silently reverted on the pod's network FS (2026-06-18)"
metadata:
  type: feedback
---

**Observed + DIAGNOSED 2026-06-18 (on the RunPod pod, now gone):** ~10 `Edit`/`Write`-tool changes to the runbook (§0.3/§8/§12/§13/§5) each returned success and grep-verified present *moments after*, but **all silently reverted** to the conversation-start snapshot minutes later (every marker grep=0 simultaneously). A controlled test settled the mechanism: a **Bash `>>` append persisted** (survived 20s + fresh re-reads) while the Edit-tool changes stayed reverted — so it was **Edit-tool writes specifically** that didn't stick on that filesystem (a FUSE network FS), not a wholesale external restore. SESSION_CHECKPOINT.md and local-FS memory edits persisted. Re-applying the same edits via **python (`open().write()`) through Bash persisted.** Recurrence on the local memit volume is UNVERIFIED (`_system/governance/STORAGE.md:11`), so the habit stays.

**Why it matters here:** runbook §0.3 is the program's single source of "what's next" ([[experiment-runbook-is-canonical]]). If an edit silently fails to persist, a fresh session re-grounds from a **stale state** and runs the wrong (already-done) experiment.

**How to apply:** (1) For load-bearing state files (`program/program_state.json`, runbook §12/§13, CORPUS, memory index), **write via Bash/python** (`python3 - <<'EOF' … open(fn,'w').write(s)`), not the Edit/Write tools. (2) **Re-verify after a delay or an intervening operation**, not just immediately — the reverted edits looked present right after editing. (3) `program/STATUS.md` (linked from §0.3) is generated from `program/program_state.json` by `code/state/render_state.py --write`, so stale status is fixed by re-rendering from the JSON; SESSION_CHECKPOINT.md + CORPUS remain the primary handoff. (The runbook's 2026-06-18 "PERSISTENCE WARNING" line is a pod-era leftover.) Cousin trap to [[durable-artifact-path-collision]] (there a script silently overwrites a result; here a tool-edit silently doesn't persist — both = a durable write you THINK happened but didn't; verify via a fresh read).
