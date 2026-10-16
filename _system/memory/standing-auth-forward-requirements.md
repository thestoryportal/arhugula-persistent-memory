---
name: standing-auth-forward-requirements
description: "Operator standing approval: forward infra (downloads, cov compute, model pulls) is pre-approved; deletions follow runbook 3.3/3.3a with a per-path ask"
metadata:
  type: feedback
---

The operator's explicit goal is to **surface a solution to the LLM-as-Database spec no matter the work required**. Any **forward requirement** needed to continue experimenting toward that solution is **PRE-APPROVED**: model downloads, hours-long covariance computation, standing up new models, disk housekeeping that creates no deletion, etc. (`_system/governance/OPERATING-MODEL.md` § CURRENT OPERATING MODEL item 2: "Infra … is pre-approved when needed within authorized scope — do it and narrate it"). The original 2026-06 grant also covered deleting stale pod artifacts; deletions now follow `_system/governance/STORAGE.md` § Storage discipline — reclaim candidates in runbook §3.3/§3.3a may be *proposed* without a HALT, but each deletion runs only after a per-path operator approval ([[approved-deletes-ask-then-rmtree]]). Regenerable bulk is the exception: MAESTRO reclaims it autonomously (operator 2026-10-15, [[approved-deletes-ask-then-rmtree]]).

**Why:** these requirements, if deferred or framed as "blocked pending your OK," become **hidden blocks the operator might miss** — which stalls the program. The operator would rather I just do them.

**How to apply:** when a path to a solution needs infra work, DO IT (and say I'm doing it) — don't stop and ask permission for routine forward requirements. Still surface them transparently in the narration so they're visible. Reserve HIL gates for genuine science/design *direction* choices and the items `_system/governance/OPERATING-MODEL.md` § CURRENT OPERATING MODEL item 2 lists, NOT for the infra cost of pursuing it. See [[operator-profile-and-standing-directive]], [[disk-budget-before-dispatch]].
