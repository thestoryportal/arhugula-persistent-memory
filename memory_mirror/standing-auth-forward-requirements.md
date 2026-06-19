---
name: standing-auth-forward-requirements
description: "Operator standing approval — infra/forward requirements (disk, downloads, cov compute, model pulls) are pre-approved when needed to keep experimenting toward a solution; surface them, never defer as hidden blocks"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e1b2ae2b-4a31-42c8-a24d-462bcf751e0d
---

The operator's explicit goal is to **surface a solution to the LLM-as-Database spec no matter the work required**. Any **forward requirement** needed to continue experimenting toward that solution is **PRE-APPROVED**: RunPod disk/memory hygiene (deleting stale artifacts, cleanup), model downloads, hours-long covariance computation, standing up new models, etc.

**Why:** these requirements, if deferred or framed as "blocked pending your OK," become **hidden blocks the operator might miss** — which stalls the program. The operator would rather I just do them.

**How to apply:** when a path to a solution needs infra work, DO IT (and say I'm doing it) — don't stop and ask permission for routine forward requirements. Still surface them transparently in the narration so they're visible. Reserve HIL gates for genuine science/design *direction* choices (which approach to pursue), NOT for the infra cost of pursuing it. This RELAXES the prior over-cautious deferral on disk cleanup / downloads — see [[operator-profile-llm-as-database]]. Destructive/irreversible actions outside the experiment sandbox still warrant a heads-up.
