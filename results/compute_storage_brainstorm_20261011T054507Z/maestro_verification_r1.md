# MAESTRO verification r1 — compute/storage design (2026-10-11)

Method: a fresh read-only subagent read decisions_log.md, design.md and integration_plan.md in full, opened 40 cited lines, recomputed the arithmetic and compared the integration plan with the live work_queue. MAESTRO36 re-opened each defect it reported before accepting it.

Subject at review: design.md sha256 3f77e6382fb776b1851fc6ca125d30edaec9771e32e58139a08e501dc6b05ce1 (the operator-approved text).

## Result: faithful to all 15 operator choices; 7 defects, all fixed in design.md "Post-review amendments"
- Coverage: every choice 1–15 is carried; none weakened or contradicted.
- Arithmetic: Intel caps 400+100+80+100+6 = 686 GB, +100 GB free = 786 GB of a decimal 1000 GB disk, conditional on measured capacity (design.md:81,154,165). memit 100 GiB = 107.37 GB, 80 GiB = 85.90 GB. No wrong numbers.
- Queue: all 8 work_queue items are named in integration_plan.md. None missed.
- Defects (confirmed by MAESTRO at EXPERIMENT_RUNBOOK.md:274/277/279 and tools/backup_mirror.sh:17–23):
  1–2. design.md:24, :89 cited runbook:277 for the +20 GiB rule; it is at 274.
  3–4. design.md:33, :263 cited runbook:279 (the §3.4 heading); the Drive text is at 273–276.
  5. design.md:275 cited backup_mirror.sh:20–23; the default source/destination are at 17–18.
  6–7. design.md:136, :307 still asked section checks the log had answered (choices 4, 12, 13). Astra F6 found the same.
- Not a defect: work_queue says "four Intel Mac roles", the design says five; the same set, with Drive transfers and the dashboard counted as one or as two.
