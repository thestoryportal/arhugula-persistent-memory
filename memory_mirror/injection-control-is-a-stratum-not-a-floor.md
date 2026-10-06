---
name: injection-control-is-a-stratum-not-a-floor
description: "C10 harness (CORPUS/47, D-C10n-ztransport, 2026-10-05): the pre-edit z-injection control spans 42–54/72 over five processes with identical mechanics because compute_z samples context templates per process; pre-register it as a stratum (HIGH ≥ 44 / LOW 38–43, LOW reported not promoted), never as an absolute floor — a floor halted run 1 at 42 < 44"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

The D-C10n-ztransport prereg set an absolute floor on the injection control (≥ 44/72, "P6 reference minus 3–5") from three observations (49, 54, 51); the next two processes came in at 42 and 42 and the first halted the run before the edit. The advisor's fix (amendment N1): keep the true instrumentation gates (fingerprint, LAW#5, A1, edit-only envelope, canon ≥ 22/24, post-restore identity, L3), treat the control level as a measured stratum, always run the cells, and promote only HIGH-CONTROL readings.

**Why:** a per-process quantity will eventually fall outside any floor set from a few observations (the same lesson as CORPUS/44 F-A4 on delta norms), and re-running until a floor passes selects on the gate.

**How to apply:** for any harness quantity that varies per process, pre-register the envelope from all observations as a reporting stratum with A-relative labels, not as a success gate; keep the halted run's artefacts under their own name and record the halt in `architecture_profile/`. See [[c10-edit-collateral-breaks-injected-target]], CORPUS/44 F-A4, CORPUS/47 Method.
