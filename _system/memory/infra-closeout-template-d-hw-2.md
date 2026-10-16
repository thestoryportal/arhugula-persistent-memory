---
name: infra-closeout-template-d-hw-2
description: Infra (non-science) decision close-outs pass closeout_check by copying D-HW-2's tracker pattern; delegate to a Sol builder with the gate as acceptance
metadata:
  type: project
---
Infra decisions (R2 drive sharing, hardware, backups) need the same `code/gates/closeout_check.py` ALL GREEN as science, across all 12 trackers, but have no CORPUS/NN writeup. D-HW-2 passes the gate and is the template: one grouped row per tracker (D-IDs + one-line verdict + pointer to runbook §13), the D-ID prepended to `current_latest` in `program/program_state.json` (renders program/STATUS.md, _index/program-state.md, program/scorecard.md), never a restated copy. MAESTRO63 (2026-10-12) closed D-R2C-A1/R9–R13/REDESIGN/ADOPT this way via an idle Sol drafter in ~4 min (c52a3f46), then reran the gate ×8 itself.

**Why:** the gate reads like science-only work, so infra decisions sat unregistered (R2's whole arc was MISSING in 12 trackers at adoption).

**How to apply:** at each infra arc close, brief a builder: "copy D-HW-2's pattern; python exact-anchor edits; never edit GENERATED blocks; acceptance = closeout_check ALL GREEN per ID". A one-line JSON field diff looks like a replacement: compare lengths before calling it a regression. Related: [[model-and-compute-allocation]]; `_system/governance/OPERATING-MODEL.md`; [[sol-for-sweeps-astra-for-gates]] (Claude auto-memory, not _system/memory/).
