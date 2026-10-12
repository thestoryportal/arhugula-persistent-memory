---
name: sandbox-green-is-not-host-green
description: Codex sandbox skips/denies /bin/ps, osascript and osacompile; a builder's GREEN is sandbox-only until MAESTRO reruns the suite on the host
metadata:
  type: feedback
---

2026-10-10 (MAESTRO27): two builder suites reported GREEN and both failed when MAESTRO reran them on the host. Drive locked release (MB32/MB34): 151/0 fail in the sandbox (18 osascript tests skipped); on the host, 3 failed because every osacompile->osadecompile round trip appends a newline (`a19749d`). NEW-1 recorder (MB33): 14/14 pure tests in the sandbox; on the host, 14 of 34 failed — `/usr/bin/date` does not exist on macOS (`/bin/date`), and a df parse was broken (`c99b475`).

**Why:** the Codex workspace-write sandbox denies setuid `/bin/ps` and cannot run native AppleScript, so every test that touches them skips or is never run, and the builder cannot see the failures.

**How to apply:** for any build touching processes, osascript or absolute system paths, brief the builder to write a host runner (`run_tests.sh LABEL red|green`, provenance per run) and stop at "READY FOR MAESTRO RUN". MAESTRO runs it, from the niceness-0 `tmux -L new1` server when niceness matters, before calling anything GREEN or committing it as done. Related: [[background-shell-niceness-10]], [[record-provenance-per-test-run]].
