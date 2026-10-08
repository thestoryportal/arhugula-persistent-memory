---
name: rerun-never-patch
description: Operator standing rule (2026-10-08) — a compromised/halted experiment is always re-run, never read around with a deviation note; program runs autonomously at full rigor
metadata:
  type: feedback
---
When the C10W P2 eval halted on an fp32 diagnostic, I recommended a no-GPU reread of the saved results under a prereg deviation note. The operator chose the GPU rerun and ruled (D-C10w-p2rerun): "never allow an experiment that is corrupted to ever not be rerun. That goes against all scientific rigor and governance ... This science runs with absolute stringent rigor autonomously unless I explicitly ask for something."

**Why:** a reading produced through a patch on a halted record is not the preregistered measurement; rigor and governance require the measurement itself to complete cleanly.

**How to apply:** on any halt or compromised run: diagnose, make one reviewed fix with a failing-first test, and re-run the affected stage(s) in fresh processes — never recommend reading around it. Budget beyond an approved bound: the program may raise it under D-C10r-rulings-14 (measured, recorded with arithmetic, reviewed) — see [[operator-overnight-autonomy-2026-10-06]], but present the rerun as the default. Don't ask the operator routine questions; make the calls (MAESTRO). Related: [[fp32-reductions-over-big-tensors]], [[operator-overnight-autonomy-2026-10-06]].
