---
title: AnyEdit is the best remaining C10 rescue, not an assumed fix
date: 2026-06-26
decision: D-C10g-strengthlayers <D-C10g-strengthlayers@d691acab>
---

AnyEdit/per-token editing is the best remaining technical rescue for C10 because
the failure localized to multi-token continuation / W-realization rather than
compute_z. That makes the prior-art direction mechanistically matched, and FABLE
may be an adjacent stronger lead. It is still not a production-ready conclusion:
the port must clear held-out-paraphrase full-sequence exact match, A1/A2
controls, same-relation batch behavior, and Q4_K_M/CPU serving before C10 can be
closed.
