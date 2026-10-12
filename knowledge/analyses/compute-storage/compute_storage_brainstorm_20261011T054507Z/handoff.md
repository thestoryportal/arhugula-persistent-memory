# HW1 handoff — fresh successor required

Saved 2026-10-11T06:49:57Z, using `date -u`.
Reason: MAESTRO reports approximately39% context left. HW1 stopped new work immediately; only these save/handoff writes followed. No live process, experiment, transfer or tool cell is in flight.

## Authority, scope and exact files

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`
Verified session branch: `worktree-c10k-route-a`.
Only writable output folder: `results/compute_storage_brainstorm_20261011T054507Z/`.

- Design: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/design.md`
- Quoted operator choices and UTC recording times: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md`
- This handoff: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/compute_storage_brainstorm_20261011T054507Z/handoff.md`

Only these design/log/handoff files were written. No git writes, install, network configuration, SSH, transfers, model/experiment runs, long-lived processes, deletion or tmux changes. Read-only repo/file metadata and web/Perplexity checks were performed. No subagents were spawned. Do not run implementation or a reviewer in this brainstorming assignment; MAESTRO owns later briefs/reviews/commits.

## Binding context rule — restated for every successor

Watch Context N% left for this session and every orchestrated session. Start a new piece of work only at >=60% left. At <=40%, or on ANY "Context compacted", stop starting work; save design.md and decisions_log.md; write a handoff here containing done/open/single next step/exact paths and restate this rule. Report a line starting `HW1 HANDOFF`. Never continue through compaction or finish an in-flight test afterward. MAESTRO starts a fresh successor.

## Method and communication

The required skill was read at `/Users/robertrhu/.codex/superpowers/skills/brainstorming/SKILL.md`. Follow its collaborative brainstorming process with the original HW1 overrides: save design/log section by section here only; no commit, no writing-plans terminal transition, no spec-reviewer subagent or visual companion. One question per message;2–3 valid approaches where helpful, recommendation first; short plain-language design sections with a check after each. User works from a phone. Explain technical concepts by what they do; avoid dense networking vocabulary.

The asynchronous question UI was invisible to the operator at the start. From then on all questions have been written directly in the final reply. Continue that practice; do not use the hidden question UI. The initial `+++++` was not an answer and no choice was inferred from it.

RTK rule: prefix shell commands with `/opt/homebrew/bin/rtk`; use `proxy` for exact source reads/writes. The first graft discovery attempt failed with `env: node: No such file or directory`; no graph answer or savings was obtained. Do not install/upgrade anything. Repo user instructions say graft disabled; use direct known sources/rg as appropriate while honoring current higher-priority tool instructions.

## Completed operator decisions —13 choices in decisions_log.md

1. Intel normally remains powered/connected; M3 travel is rare. Design for independent operation during disconnection.
2. Separate working copies: M3 keeps MAESTRO/science, memit stays attached to M3, Intel is support host. Intel recovery copies are separate from editable builder files.
3. Selective storage: current science on memit; independent recovery/useful support data on Intel; retained large finished material on Drive. Storage optimization across all resources is essential to avoid space blocks.
4. All admitted research records must remain discoverable even when bulk is on Drive. Ontology defines record meaning; DuckDB holds admitted metrics; Neo4j holds reviewed connections; full original records and exact artifact locations remain accessible. Required bulk is requested for a named analysis, checked for space/permission, retrieved and held while needed. Pilot remains five source chains; whole-program/shared-service expansion is future reviewed work. Automatic inventory/archive copying/verification is intended within approved limits; exact-path deletion permission is distinct.
5. Copy schedule A: small records after accepted updates; useful completed bulk nightly when science permits; earlier copying when irreplaceable-run durability requires it. Interrupted/offline state shows old verified copy and age.
6. Approved starting Intel disk limits, decimal GB:400 current recovery,100 extra unique history,80 builder work/tools,100 temporary analysis/transfer data,6 pilot/setup, and at least100 normally free. Actual formatted capacity/OS/current use must be inventoried before locking deployment. memit target100 GiB free (~107 GB), warning80 GiB (~86 GB), with binding every-job projected peak additional writes+20 GiB. Quotas do not override actual free space or frozen preregs.
7. Retention A: seven daily/four weekly restore points within100 GB extra unique history; safely reuse unchanged content. Overflow must be shown, not silently trimmed. Verify restores including an older version into a separate destination. Intel first, Drive for missing bulk; science gates before resuming science.
8. Intel writes code/runs compatible non-model tests; required M3 native/science-stack checks remain explicit and run in science-safe windows. Exact source base, patch, hashes and RED/GREEN evidence return to MAESTRO; MAESTRO alone incorporates/commits/merges. Start one builder test job at a time, widen after measurement. **Binding: no local LLM runs on Intel.** Hosted agent services and non-model calculations are distinct. Never copy the M3 virtual environment or downgrade science pins.
9. Intel research databases/builders continue during M3 science using Intel-local copies; operations touching memit/M3 disks wait/pause under M3-side coordination. No blanket termination of Intel databases on a science launch. Existing gate exemptions stay unchanged. MAESTRO must amend/review the same-host research-engine spec and dispose of every Astra finding; moving hosts does not turn NO-GO into GO.
10. Intel uploads verified local copies to Drive. Dashboard includes **phone AND local running views**, not merely phone. Show actual source-host identity, snapshot age, free space/copies and UNAVAILABLE on lost observation; never read Intel ps as if it were M3 ps. New collectors must not recreate the Python launch gate problem.
11. First large Drive upload also uses Intel. Inventory selected data from M3 internal disk and memit, distinguish duplicates/old mirrors/unique data, create and verify an Intel checkpoint, then internet upload/check from Intel while M3 can do science. Initial capture still reads M3 disks; existing write-pause/final catch-up/full content-check obligations must be preserved or explicitly revised/reviewed. No promise of zero downtime or a short pause. M3 internal SSD remains excluded as an archive destination.
12. Connection A: local Thunderbolt transfer link; each owned Mac keeps its own internet path; phone/local view on Intel; optional private device-only friend access with separate account, no joined home networks or public router exposure. No actual setup authorized/performed.
13. Friend scope clarification A: friend's Apple Silicon Mac **may run models**, Intel **may not**. Operator will verify availability/constraints within the next24 hours. This supersedes the conservative earlier M3-only interpretation; no job/connection has been authorized.

The approved broad choices were shown to the operator in short replies. Additional technical implementation suggestions in the long draft are proposals for MAESTRO, not independently approved hidden decisions. In particular: numerical Intel support-memory targets, a small automatic retrieval allowance, exact transfer pause latency, native Intel dependency selection and detailed worker interfaces still require future measured/frozen briefs. Do not report them as commissioned or granted.

## Current unanswered question — the SINGLE next step

A fresh successor should resume with the pending question below and wait for the operator's answer. Do not invent a choice or start another section first.

Last reply presented:

> Recorded: friend's Apple Silicon Mac may run models; Intel may not.
>
> For the loan, I recommend A: an initial one-week trial—or the shorter period your friend offers:
>1. Check the machine, software and available resources.
>2. Reproduce a known baseline before trusting new data.
>3. Independently re-check one important result.
>4. Consider additional parallel work only after that succeeds.
>
> B: after the baseline checks, use it for new queued tests first. That produces new data sooner, but gives less direct confirmation of an existing result.
>
> When you check availability, the useful facts are chip, memory, macOS version, free disk, quiet hours, his own workloads and loan duration. Those determine whether it can handle editing or mainly smaller model read tests.
>
> **Approve A as the conditional trial plan?**

This remains unanswered. `design.md` section11 is PROPOSED. MAESTRO's context-steering message is not approval.

## Other open matters / remaining design work

After the trial answer, complete only the remaining design/approval work:

- Friend inventory is due from the operator within24 hours of his answer (recorded2026-10-11T06:47:30Z); chip M1/M2, memory, macOS/free disk/quiet hours/loan duration/owner workloads are unknown. Do not ask for them as if immediately available or stall a conditional architecture on them. The eventual workload and exact result depend on these facts; baseline-first trial branches can be designed now. No3B edit fits are assumed at8/16 GB. No automatic7B/model-family change.
- Section11 proposes one week from agreed commissioning, shorter if offered; one local model job at a time on that host. Required order: source/stack/model identity and budget; engine fingerprint; applicable determinism/null/inertness; known-baseline reproduction with preregistered endpoints; one authorized replication; verified complete return before extra jobs. A compiled readback-only check does not independently reproduce editing. Fresh outputs, no private credentials, owner can revoke, return results before access ends, exact cleanup approvals.
- Add a concise risks/failure/acceptance and MAESTRO handoff section; user asked risks and what must be approved. Much detail already exists across sections; consolidate instead of adding redundant systems. Keep later implementation acceptance distinct from design approval and fixture/static evidence distinct from host/scientific acceptance.
- Surface genuine remaining operator decisions only: friend-scope/trial question first; any proposed new spend/storage changes/exact deletions/credential setup/live runs are separately gated. Routine implementation choices belong to MAESTRO's future briefs. No unapproved automatic history deletion or remote access.
- Self-review the full draft for stale PROPOSED/open lines, contradictions, citations, placeholder language and valid arithmetic. The top discussion-sequence list is still a working list. Historical alternative tables may remain history but must not contradict the chosen design. Spec-reviewer subagent explicitly skipped.
- Ask the operator to review/approve the finished written design. Only after explicit final approval send `HW1 DESIGN READY FOR MAESTRO` plus exact design path. Do not invoke writing-plans or commit. No final design approval has occurred.

## Source/evidence map and caution points

Primary sources read: CLAUDE.md (laws, Merging50–54, storage56–61), DISCIPLINE.md, docs/SPEC_E2E_GROUND_TRUTH.md, selected runbook§0.3/§3.3/§3.3a (storage271–280), research-engine design108–121 and other relevant spans, phase1_spec_v5.md (host/resource/publication/AC/commissioning choices), Astra r3/r4/r5 NO-GO excerpts, activation_plan_v4.md, tools/c10w_p2_gate.py22–84, repository notes for niceness/Tailscale. Draft has file:line references. Initial tool outputs often truncated large reads: verify precise spans needed for final claims, rather than treating clipped output as full coverage. No file>200 KB was read whole; runbook is ~474 KB. Never read bulk results or launch validators/model tools in HW1.

- Research-engine approved design: `results/research_engine_brainstorm_20261011T032049Z/design.md`; phase spec: `results/research_engine_phase1_20261011/phase1_spec_v5.md`. Original choice file `operator_phase1_choices_20261011.md:5–13` says on M3, Neo4j Community/session-only,5 GB data and2 GB Neo4j memory. New Intel location needs an explicit amendment by MAESTRO; its ARM/OS/Homebrew pins are not Intel/Sonoma acceptance. Do not modify original files.
- Drive plan: `results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/activation_plan_v4.md`; line314–316 write-pause/final catch-up/full check still binding until revised. Preserve existing day/bandwidth cap and three operator OKs. No new Intel credential consent or automatic activation implied.
- Read-only df observed memit439458956 KiB total/78323856 KiB available,83% used (~419.1/74.7 GiB). The320 GB project figure is MAESTRO's brief measurement; not recomputed. Intel1 TB/16 GB/Sonoma is operator-reported; actual free space/disk type/health unknown.
- `.venv/lib/python3.11/site-packages/torch-2.8.0.dist-info/METADATA:3` and transformers-4.51.0.dist-info/METADATA:3 verify installed version metadata, no import/model. Perplexity and official PyTorch release notes confirm Intel macOS official PyTorch stops2.2.x: https://pytorch.org/blog/pytorch2-2/ . Intel no-local-model rule is categorical regardless of technical compatibility.
- Directory-only probe confirmed `/Users/robertrhu/Backups/memit` exists. `tools/backup_mirror.sh:20–23` names the old internal destination. Size/content/freshness not inspected. Its header calling internal storage durable is superseded by current storage policy; report discrepancy, do not fix that file.
- Apple direct cable docs: https://support.apple.com/guide/mac-help/use-ip-over-thunderbolt-to-connect-mac-computers-mchld53dd2f5/mac . Tailscale single-machine sharing/quarantine: https://tailscale.com/docs/features/sharing (verified body425–436). No live connectivity/host support/speed measured. Use ordinary Mac SSH over private connection; do not assume Tailscale SSH-server availability/policy.
- CORPUS/17 describes a cheap compiled-artifact readback candidate (~1.8 GiB Q4); its Intel-target/historical assumptions are retired. M3 B3 reference in runbook is later; exact candidate/prereg/endpoints not yet selected. REPRODUCIBILITY.md header remains pod-era. Treat a readback test as readback, not full edit replication.

Private memory registry `/Users/robertrhu/.codex/memories/MEMORY.md:42–43` was used early to preserve backup host/fixture boundaries, with no memory edits. If you rely on that private memory, final response requires the prescribed memory citation block. Repository memory_mirror files are ordinary source citations, not private-memory entries. No private rollout summary was read.

## Delivery state

Design/log saved; conditional trial unanswered; final design NOT approved. No `HW1 DESIGN READY FOR MAESTRO` yet. No implementation tasks/checks started. This handoff is the terminal action for the current session.
