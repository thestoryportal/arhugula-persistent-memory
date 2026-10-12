# Astra review r1 — compute and storage architecture (Intel Mac, friend's Mac, Drive)

You are the program's independent cross-family reviewer. Work read-only: read and search only; do not create, edit or run anything else.

## Context
The operator brainstormed with two Codex sessions (HW1, then HW2) how to use three new resources: their 2019 Intel MacBook Pro (16 GB, 1 TB, Sonoma, Thunderbolt to the M3), a friend's M1/M2 on another home network (loan not yet confirmed), and Google Drive. The operator approved the design at 07:03:36Z (`decisions_log.md`, choice 15, quoted verbatim) and added a binding requirement: one durable plan must reconcile this design with earlier designs and queued builds before any affected build is dispatched. Nothing has been built, installed, connected or run.

Subjects (all in `results/compute_storage_brainstorm_20261011T054507Z/`):
- `design.md` (sha256 3f77e6382fb776b1851fc6ca125d30edaec9771e32e58139a08e501dc6b05ce1), sections 1-14.
- `integration_plan.md` (sha256 ca0963075e40d1cd69bc0dba7c09cff0d1b391d7044d8d6d34484d2048103da0).
- `decisions_log.md` (sha256 69362fe7c326b14b2fdf3f9ff512798f2b1cffa02598141bc8fd4480dd38875c): the 15 operator choices. These are settled.

If you pass it, MAESTRO records the decision, revises the research-engine phase-1 spec for Intel hosting, and works through the integration plan before dispatching any build it touches.

## Review for
1. Does design.md faithfully carry every one of the 15 choices, with nothing contradicting them and no section still marked PROPOSED or open that the log shows settled?
2. Does anything conflict with binding repo rules: CLAUDE.md (LAWs 1-3 before any machine's data counts, storage discipline and its three tiers, the M3 internal SSD is not an archive, deletions need exact-path operator approval, only MAESTRO commits/pushes/merges), DISCIPLINE.md, and `EXPERIMENT_RUNBOOK.md` §3.3/§3.3a?
3. Specific points MAESTRO wants judged:
   a. Section 4's Intel space limits (400 + 100 + 80 + 100 + 6 GB, at least 100 GB free) on a 1 TB disk whose formatted size and current use are unmeasured. Is the arithmetic sound, and is "inventory before locking" stated as a hard precondition?
   b. Section 7 moves the research engine to the Intel Mac and keeps it running while the M3 runs science; only work touching memit or M3 disks waits. Astra r3-r5 returned NO-GO on the same-host "science goes first" contract (`results/research_engine_phase1_20261011/astra_spec_r3_verdict.md`, `_r4_`, `_r5_`). Which of those findings does the move genuinely remove, and which survive (for example, Intel reads from memit over the cable during a science run)? Does the design say each surviving one must be answered?
   c. Section 8: the first Drive upload stages through the Intel Mac. Does it keep every obligation in `results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/activation_plan_v4.md` (write pause, final catch-up, full content check, the operator's three OKs, caps), or does it quietly drop or weaken one?
   d. Section 6: Intel builders hand back patch + hashes + RED/GREEN evidence, and M3-native checks rerun on the M3. Can a result produced only on Intel reach a commit without an M3 rerun where the stack differs (no PyTorch for Intel macOS after 2.2)?
   e. Sections 8 and 12: the dashboard must never read Intel process lists as if they were the M3's, and new collectors must not trip the M3 Python launch gate (`tools/c10w_p2_gate.py:22-84`). Is that enforceable as written, or only intended?
   f. Sections 10-11 and the fallback: the friend's Mac may run models, the Intel Mac may not. Do LAWs 1-3 gate its data before it counts? Does any core service, recovery duty or science schedule depend on the loan?
   g. integration_plan.md: compare its observed queue with the live `work_queue` in `docs/program_state.json` and the plans it names. Does it miss an overlapping plan or queued build, and is its completion table something MAESTRO can actually check?

## Deliverable
Markdown to stdout, exactly this shape:
```
# Astra r1 verdict — compute and storage architecture
Verdict: GO | GO-WITH-CONDITIONS | NO-GO
## Findings
F1. [severity: blocking|condition|note] <one-sentence defect>. Evidence: <file>:<line> vs <file>:<line>. Consequence: <what goes wrong>.
## Required changes before MAESTRO acts on the design
R1. <exact change, checkable>
## What I checked and did not check
```
Ground every finding in a line you read; an ungrounded concern is a `note` and says so.

Do NOT produce: re-arguments of the operator's choices (Intel roles, no local models on Intel, copy schedule, space limits, the conditional trial), stylistic rewrites, a rewritten design, or generic advice such as "consider adding monitoring".
