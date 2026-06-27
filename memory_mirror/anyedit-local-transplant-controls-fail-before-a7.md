---
date: 2026-06-27
source: D-C10h-anyedit-pilot / D-C10h-anyedit-window50-controls
scope: LLM-as-Database C10 AnyEdit
---

# AnyEdit Local Transplant Controls Fail Before A7

The local AnyEdit-style transplant is not yet an interpretable C10 rescue test. The
small-window pilot (`window_size=1`) passed token-alignment and no-op gates, but
collapsed easy controls: A1/A2 held-out `para_full` went from 93.1/97.2 baseline
to 0.0/0.0, and A7 worsened from 12.5 to 1.4. The follow-up upstream-equivalent
window diagnostic (`window_size=50`, A1/A2 only) also failed controls: A1
`para_full=0.0`, A2 `para_full=0.0`, despite healthy baselines.

Future C10 AnyEdit work must not run or interpret A7 until an active easy-control
edit passes. The only justifiable next step is a bounded parity audit against
official AnyEdit on one A1 subject: compare token IDs, continuation suffix,
loss mask, lookup index, target hidden-state norm, delta/update norms, and
canonical top-1. Permit one clear mismatch/fix and one A1/A2 rerun. If controls
still fail, stop the local transplant route and move the C10 decision toward
accept-bounded / side-store or a separate method lead.
