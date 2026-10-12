---
name: rerun-builder-tests-host-tmpdir
description: Builder (Codex) green runs use TMPDIR=/private/tmp; rerun on the host's default /var/folders TMPDIR and on Linux CI — symlinked/OS-specific paths hide there
metadata:
  type: feedback
---
Codex builders run tests with `TMPDIR=/private/tmp`. The host's default TMPDIR is `/var/folders/...`, behind the `/var -> /private/var` symlink. On 2026-10-10 the git-automation suite was "56 PASS" for the builder but failed 1+1 on every host rerun: the test fixture kept an unresolved temp root (fixed by `.resolve()` in `tests/test_git_automation.py`). The same day the first GitHub Actions run failed on `os.stat().st_birthtime` (macOS-only) in `tools/dashboard_experiment.py:291`, which no local run can catch. Again later that day: NEW-1 FIX2 was "182/182" in codexmb15's receipt, but `test_stalled_launch_returns_within_bound_and_late_handle_cleans_once` failed 9 of 10 host runs (late-handle cleanup not done when checked). A timing test that passes in the sandbox is not proof that it passes reliably.

**Why:** "all green" from a builder is evidence about the builder's environment, not the host's or CI's.

**How to apply:** when verifying a build, rerun its suites with the shell's default TMPDIR (do not copy the builder's env prefix), and treat the first live CI run as a separate verification step. If a test fails only on the host, check path resolution first; if it is a timing test, run it alone 10–20 times before calling it flaky or fixed. Related: [[codex-sandbox-no-network]].
