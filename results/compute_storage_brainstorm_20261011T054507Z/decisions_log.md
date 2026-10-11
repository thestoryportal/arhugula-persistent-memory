# HW1 operator decisions

Recorded at 2026-10-11T05:49:07Z using `date -u`. Times below are recording times unless a source gives the original choice time. No new operator answer has arrived in HW1 yet.

## Prior direction supplied verbatim by MAESTRO

Recorded 2026-10-11T05:49:07Z; original statement time not supplied.

> "Let's launch a fresh Codex brainstorming session to dig deeper on how to leverage these resources and what the architecture looks like. All in the context of what the current architecture is and is planned."

Meaning: design discussion only. No build or connection authorization.

Recorded 2026-10-11T05:49:07Z; original statement time not supplied.

> "Let's flesh this out in the fresh Codex brainstorming session."

Meaning: investigate the friend's Mac as an option; no remote access or experiment authorization.

## Prior research-engine choices verified in source

Original choice time: approximately 2026-10-11 04:31 UTC, per results/research_engine_brainstorm_20261011T032049Z/operator_phase1_choices_20261011.md:1–13. Recorded 2026-10-11T05:49:07Z.

> "On this Mac, free edition (Recommended)"

> "Small fixed cap, anytime (Recommended)"

The new MAESTRO brief reports the operator wants the engine on the Intel Mac. Hosting must be amended; original size/memory and session-only choices are the starting point, with Intel-wide budgets still to discuss.

## Reported choice without an original verbatim answer

MAESTRO reports that the operator selected all five Intel roles: second copy of memit, Codex builders, research engine, Drive transfers, phone dashboard. No fabricated quotation or original choice timestamp is assigned. Recorded 2026-10-11T05:49:07Z.

## Open question 1

Will the Intel Mac usually stay powered on and connected to the M3? Options: usually connected / only during active use / not decided. Recommendation: usually connected if practical. Awaiting the operator's answer; no default is recorded as a decision.

## HW1 choice 1 — Intel normally available

Recorded 2026-10-11T05:50:41Z using `date -u`.

> "Yes most of the time if not always. Unless of course I travel somewhere with my M3, which happens rarely."

Decision: design for a normally powered and connected Intel Mac, with rare M3 travel as a supported disconnected condition. This does not authorize a setup action.

Next section presented for approval: separate local working copies and the machine roles (approach A recommended; direct shared-memit work is approach B). No section approval yet.

## HW1 choice 2 — Separate copies; storage optimization essential

Recorded 2026-10-11T05:55:58Z using `date -u`.

> "A. And we must consider how storage is very well managed across all available resources so we do not run into blocks due to running out of space. A very optimized sotrage plan is essential."

Decision: approve section 1 approach A. Treat storage management across all resources, including avoidance of disk-full blocks, as a binding design requirement. No automatic deletion or implementation authorization is inferred.

Next choice: selective steady-state local retention (recommended), copy everything everywhere, or Drive-heavy retention.

## HW1 choice 3 — Selective storage; research access concerns

Recorded 2026-10-11T06:02:09Z using `date -u`.

> "A...so Drive would be archival? And what needs to be archived occurs dynamically and automated? But, what if archival Drive data is perhaps valuable for the science engine? And would limiting what is given to the Intel running the science research engine constraining its ability to dig deep and ideate? Will all of the data tbe contained in the Ontology and DuckDB and all nodes can use it and if particular data is needed for the science research engine on the Intel to conduct its work is it requested/sent after it runs these Ontoogy, Neo and DuckDB queries?"

Decision: storage approach A approved. The rest of the answer raises questions about dynamic archival, research completeness, shared access and fetching bulk after queries. It does not yet approve specific automated retrieval or deletion behavior. Section 3 explains a proposed complete searchable library and controlled artifact retrieval.

## HW1 choice 4 — Searchable library and requested bulk

Recorded 2026-10-11T06:06:06Z using `date -u`.

> "Yes"

Question approved: "Does this arrangement—complete searchable research records, with large files brought back when needed—match what you want?"

Decision: approve section 3 intended architecture. The explained automatic inventory/archive-copy/verification and distinct removal permission are retained; exact automated retrieval limits and implementation are not granted. Next: copy schedule, followed by capacity/retention choices.

## HW1 choice 5 — Copy schedule A

Recorded 2026-10-11T06:10:21Z using `date -u`.

> "A"

Question approved: "Which schedule do you prefer?" Option A: research records after accepted updates, large finished data nightly when science permits, earlier protection for irreplaceable data when required by its run. Travel/offline conditions leave the last verified copy clearly age-labelled. No implementation authorization.

Next proposed check: separate numerical space caps and free-space targets.

## HW1 choice 6 — Starting disk caps

Recorded 2026-10-11T06:13:41Z using `date -u`.

> "A"

Question approved: "Use A as the starting space plan?" Intel: recovery400 GB, history100 GB, builders80 GB, analysis staging100 GB, pilot/setup6 GB, at least100 GB free; measure actual formatted capacity and existing use first. memit: about107 GB target free and86 GB warning, retaining every job's peak-write-plus20-GiB admission rule. These ceilings are conditional planning limits, not installation or deletion permission.

Next proposed section: seven daily/four weekly restore points within the agreed history cap, and restore verification.

## HW1 choice 7 — Retention/recovery A

Recorded 2026-10-11T06:15:30Z using `date -u`.

> "A"

Question approved: "Use A for the retention and recovery plan?" Seven daily/four weekly restore points with safe reuse of unchanged content, within100 GB additional unique history. Overflow must be shown rather than silently trimmed; restore known files and an old version into a separate destination; restore from Intel and fetch missing bulk from Drive. No exact deletion or live restore drill authorized.

Next proposed section: Intel code/non-model tests with exact source and return packages, required M3 platform checks, and one initial builder test job at a time.

## HW1 choice 8 — Intel builder A; no local LLMs on Intel

Recorded 2026-10-11T06:19:02Z using `date -u`.

> "A..important context requirement: no local LLM models can run on the Intel, only the M3"

Decision: builder option A approved. Binding constraint: no Intel local model inference/edit/training/embeddings; hosted agent use and non-model data queries/calculations remain distinct. "Only the M3" is treated conservatively as M3-only local LLM authority; no friend model exception is inferred. The scope will be checked when discussing the loan machine.

Next proposed section: Intel databases/builders keep working during M3 science; only work touching the shared M3/memit disk coordinates and pauses.

## HW1 choice 9 — Independent Intel work; transfers yield

Recorded 2026-10-11T06:30:29Z using `date -u`.

> "A"

Question approved: "Approve A for this division of work?" Intel databases/builders continue from their own files while M3 runs science. Large operations that touch memit pause/wait under M3-side coordination. MAESTRO must amend and re-review the rejected same-host specification; no build or reviewer launched in HW1.

Next proposed section: Intel uploads its verified local copies to Drive; phone dashboard displays source-host identity, freshness and unknown/disconnected state.

## HW1 choice 10 — Intel uploads; dashboard includes local views

Recorded 2026-10-11T06:35:31Z using `date -u`.

> "A...and not just the PHONE dashboard, but that andthe local running dashboard. And should the first drive upload run from the Intel so the M3 can still be running science as this first large upload occurs? Even if the data being moved lives on the internal M3 SSD and I beleive some on the external SSD?"

Decision: steady-state Intel Drive route A approved; both phone and local running dashboard views are required. The rest asks whether the first upload should run on Intel and whether it can include files from both M3 disks. HW1 recommends an inventoried verified Intel checkpoint, while preserving/amending the existing consistency and activation review gates. First-upload choice remains pending; no network/copy or credential action authorized.

## HW1 choice 11 — First upload on Intel

Recorded 2026-10-11T06:38:13Z using `date -u`.

> "A"

Question approved: "Use A for the first upload too?" First inventory selected sources on M3 internal/memit, reconcile duplicate/old copies, stage and verify an Intel checkpoint, then upload/verify from Intel. M3 can run science during Intel-local upload. Initial capture/final consistency retain disk/catch-up obligations; MAESTRO must revise/re-review activation before launch. No network, credentials, copy or pause action performed.

Next proposed section: direct cable between owned Macs, independent internet, private phone/local access and device-only access for the friend.

## HW1 choice 12 — Connection plan A

Recorded 2026-10-11T06:42:39Z using `date -u`.

> "A"

Question approved: "Approve A as the connection plan?" Local Thunderbolt transfer path, independent internet on owned Macs, shared Intel phone/local dashboard view, optional device-only private friend access and a separate research account without private credentials. Design approval only; no network/SSH/install performed.

Next question: does M3-only local-model wording include the friend, or may that Apple Silicon worker be a temporary separately gated exception?

## HW1 choice 13 — Friend may run models; inventory within24 hours

Recorded 2026-10-11T06:47:30Z using `date -u`.

> "A...and will verify availability and constraints in the next 24 hours."

Question approved: "Does the M3-only model rule also apply to your friend's Apple Silicon Mac?" Option A: Intel prohibited; friend may run a carefully bounded model re-check if memory/availability suit it. This explicitly clarifies the earlier "only the M3" wording. Operator will verify the friend's availability/constraints in the next24 hours; no invented hardware/hours or run authorization.

Next proposed section: one-week conditional trial, baseline first, one selected replication next, only later extra jobs.

## Session boundary — MAESTRO context directive

Recorded 2026-10-11T06:49:57Z using `date -u`.

MAESTRO reports about39% context left and directs an immediate HW1 handoff. No architecture answer is inferred from this steering message. The last operator-facing question, "Approve A as the conditional trial plan?", remains UNANSWERED. No new design work started after the directive. See handoff.md.

## HW2 choice 14 — Conditional trial A with a no-loan fallback

Recorded 2026-10-11T06:55:50Z using `date -u`.

> "A...thsi is tenative if I am able to finalize using that resource. But let's plan as if it is an option but if we find it isn't have a fallback"

Decision: approve trial A conditionally, subject to finalizing access to the friend's Mac. Plan for the option without making any core service, recovery obligation or promised science schedule depend on it. Add a fallback: the owned M3 retains serialized model work; Intel continues its approved non-model support roles; cross-device confirmation remains open without another device. The fallback and consolidated risks/acceptance/MAESTRO sections are presented for whole-design review. No connection, credential, model run or implementation authorization is inferred.

## HW2 choice 15 — Whole design approved; durable integration required

Recorded 2026-10-11T07:03:36Z using `date -u`.

> "Very important consideration as we proceed wit this design: there are several previous design plans and build in the queue that this design and others before it cross over into each other. So we must ensure that there is a durable cross cutting concerns, conflicts, collisions, and deign implementation plan that brings them all together seamlessly. I approve this session's design."

Decision: approve this session's assembled design, including the conditional friend trial and no-loan fallback. Add a binding cross-cutting integration requirement: one durable plan must reconcile this architecture with earlier designs, queued builds, shared interfaces/paths/resources, prior approvals and review findings before affected implementation is dispatched. HW2 creates integration_plan.md as the source-backed seed and explicit completion contract; MAESTRO owns live queue/owner reconciliation, amendments, binding review and canonical propagation. No install, connection, credential move, deletion, Git mutation or science run is authorized by design approval.

## Amendment 16 — choice 6 resized to the measured disk (MAESTRO36 question)

Recorded 2026-10-11T07:42:54Z using `date -u`.

The 07:40Z inventory (results/intel_setup_20261011/inventory_20261011T0740Z.txt) found a 512 GB SSD (500.0 GB container, 482.5 GB free), not 1 TB. Choice 6's caps (686 GB + 100 GB free) do not fit. Operator answer to "How should we fit it?": "A: Shrink to fit (Recommended)".

Decision: same priorities, smaller limits (decimal GB): 250 current recovery copy, 50 extra unique history, 40 builder work/tools, 50 temporary analysis/transfer, 6 pilot/setup, at least 80 kept free; 476 GB in all against 482.5 GB measured free. The recovery copy holds what cannot be rebuilt; finished bulk stays on Drive (choice 3). Choice 7's retention scheme now fits within 50 GB of history; overflow is shown, never silently trimmed. memit thresholds and the every-job projected peak + 20 GiB rule are unchanged.

## Amendment 17 — FileVault stays off on the Intel Mac

Recorded 2026-10-11T07:42:54Z using `date -u`.

Operator answer to "Turn encryption on?": "Leave it off". The Intel Mac comes back by itself after a restart; its disk, including the research-data copy and any later Drive login, is readable by whoever holds the laptop. The Drive credential decision (activation's separate operator OK) must restate this.

