---
name: injection-control-is-a-stratum-not-a-floor
description: Only prereg-approved nuisance-control quantities become reporting strata; process variability never waives instrumentation, known-baseline or identity gates.
metadata:
  type: feedback
---

The D-C10n-ztransport prereg set an absolute floor on the injection control (≥ 44/72, "P6 reference minus 3–5") from three observations (49, 54, 51); the next two processes came in at 42 and 42 and the first halted the run before the edit. The advisor's fix (amendment N1): keep the true instrumentation gates (fingerprint, LAW#5, A1, edit-only envelope, canon ≥ 22/24, post-restore identity, L3), treat the control level as a measured stratum, always run the cells, and promote only HIGH-CONTROL readings.

**Why:** a per-process quantity will eventually fall outside any floor set from a few observations (the same lesson as CORPUS/44 F-A4 on delta norms), and re-running until a floor passes selects on the gate.

**How to apply:** only for nuisance controls explicitly approved by a prereg amendment, record the envelope as reporting strata with A-relative labels; process variation alone does not demote an instrumentation, baseline or identity gate; keep the halted run's artefacts under their own name and record the halt in `architecture_profile/`. See [[c10-edit-collateral-breaks-injected-target]], CORPUS/44 F-A4, CORPUS/47 Method.
