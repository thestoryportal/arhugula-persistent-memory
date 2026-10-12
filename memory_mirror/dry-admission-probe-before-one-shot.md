---
name: dry-admission-probe-before-one-shot
description: For a single-attempt authorized MathLab CPU diagnostic, precheck the read-only mathlab_admit.probe('cpu') so an admission refusal cannot consume the attempt
metadata:
  type: feedback
---

For an authorized MathLab CPU diagnostic using CPU admission, run its read-only admission probe in the foreground first; other run kinds require their own admission probe and frozen gates: `LLMDB_ROOT=$PWD .venv/bin/python -B -c 'import sys;sys.path.insert(0,".");from tools import mathlab_admit as A;d=A.probe("cpu");print(d["allowed"],d["reasons"],d["checks"]["gpu"].get("blocking_processes"))'`. It only verifies the prereg, fingerprint, process/tmux inventory and free memory, and mutates nothing. This precheck grants no run authority and cannot replace the actual run's admission recheck; dispatch only within explicit authorization and after all applicable gates, including the dashboard-poll condition, pass.

**Why:** the diagnostic re-probes admission inside its own run, and "denied or malformed observation is refusal". A refusal inside the run would have used up the one authorized attempt. MAESTRO23 used this pre-check for the NEW-1 FIX5 real diagnostic (2026-10-10, 0c550ae). It returned allowed even though stray Drive fixture shells were alive, and the run then succeeded.

**How to apply:** keep the dispatch command verbatim in a script file. A reviewer's `|| exit "$?"` line would otherwise kill your own shell. Send stdout to scratchpad so the output namespace holds only the files the acceptance criterion lists. Related: [[gpu-gate-refuses-any-venv-python]], [[rerun-never-patch]].
