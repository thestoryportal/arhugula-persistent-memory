# HW1 — Compute and storage architecture for MAESTRO

Status: HW1 HANDOFF at approximately39% context, per MAESTRO. Approved architecture choices are recorded; section11 trial choice and final design approval remain open. No implementation authorized or performed.
Last saved: 2026-10-11T06:49:57Z

## Purpose and scope

Use the Intel Mac, a possible temporary Apple Silicon loan, and Google Drive to reduce delays to the M3's science and improve recovery after disk failure. This concerns the research program's support infrastructure and orchestration; it does not establish that the proposed LLM-as-Database product is scientifically ready. The product still has its separate Git and model-weight authorities, validation, security and consistency rules (docs/SPEC_E2E_GROUND_TRUTH.md:7–30). The F1 goal remains proving or falsifying readiness, rather than collecting green checks (DISCIPLINE.md:7–18).

HW1 writes only this folder. No installs, connections, SSH, model runs, experiments, long-lived processes, Git mutation or deletion. MAESTRO owns implementation briefs, reviews, canonical decision IDs and commits. The existing design/spec stays untouched.

## Existing operator direction

The MAESTRO brief reports that the operator already selected all five Intel roles: second copy of memit, Codex builders, research engine, Drive transfers, and phone dashboard. This is accepted direction, not a question to reopen. The detailed boundaries and schedule still need discussion. The possible loan machine is optional; its memory and availability are unknown.

## Grounding checked so far

| Fact | Source and limitation |
|---|---|
| M3 Pro, 48 GB, Apple GPU is the current science host | CLAUDE.md:3; this session did not inspect hardware directly. |
| Science record authority remains Git; model-weight authority in the intended product is distinct | CLAUDE.md:50–54 (Merging), CLAUDE.md:56–61 (Storage discipline); docs/SPEC_E2E_GROUND_TRUTH.md:20,29–30. Storage lines checked against the source in HW1. |
| memit is the working disk; Drive is the remote warehouse; M3 internal storage is not an archive; other named volumes share memit's physical disk | CLAUDE.md:56–61; EXPERIMENT_RUNBOOK.md:271–280. Independent physical disk topology was not inspected. |
| memit has about 419.1 GiB total, 74.7 GiB free, 83% used | Read-only `df -k /Volumes/memit /` observed this session: 439458956 KiB total, 78323856 KiB available. The brief's 320 GB project measurement is attributed to MAESTRO, not recomputed. |
| Work budgets must include projected writes plus 20 GiB free | EXPERIMENT_RUNBOOK.md:277; source policy, not proof of future job admission. |
| Installed package metadata says torch 2.8.0 and transformers 4.51.0 | .venv/lib/python3.11/site-packages/torch-2.8.0.dist-info/METADATA:3; .venv/lib/python3.11/site-packages/transformers-4.51.0.dist-info/METADATA:3. No Python import/model load was performed. |
| Official Intel macOS PyTorch releases stop with 2.2.x | Confirmed with Perplexity and official release notes: https://pytorch.org/blog/pytorch2-2/ ; https://dev-discuss.pytorch.org/t/pytorch-macos-x86-builds-deprecation-starting-january-2024/1690 . This rules out treating the Intel Mac as a drop-in replacement for the current official science environment; it does not rule out all useful CPU science support. |
| M3 admission refuses non-exempt Python and other named competing processes | tools/c10w_p2_gate.py:22–54,73–84; observation failure refuses admission. Moving actual tests off the M3 removes those local processes; merely lowering priority does not. |
| Engine identity, required determinism/inertness checks and known-baseline reproduction apply before science data is trusted | CLAUDE.md:30–34. GPU bit-exact weight reproduction is not promised (CLAUDE.md:31). |
| Approved research-engine phase 1 uses two searchable copies of original records | results/research_engine_phase1_20261011/phase1_spec_v5.md:15–23; original source files and Git remain authoritative. |
| Original phase-1 hosting and budget choice was on the M3 | results/research_engine_brainstorm_20261011T032049Z/operator_phase1_choices_20261011.md:5–13: Neo4j Community, session-only, 5 GB disk and 2 GB Neo4j memory. The 2 GB is not a whole-Intel-machine budget. |
| M3-sharing reservation design is blocked by review | results/research_engine_phase1_20261011/astra_spec_r3_verdict.md:2; astra_spec_r4_verdict.md:2; astra_spec_r5_verdict.md:2. Moving hosts does not itself close unrelated review findings. |
| The existing provisioning pins describe a different machine | results/research_engine_phase1_20261011/phase1_spec_v5.md:244–246: Apple Silicon Homebrew paths, specific OS/builds and dependency identities. Intel/Sonoma provisioning must be reviewed separately; never copy the M3 virtual environment. |
| Drive activation still has explicit checks and operator decisions | EXPERIMENT_RUNBOOK.md:279; results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/activation_plan_v4.md:3,314,362. Relocating transfers must not silently inherit M3-host acceptance. |
| Existing phone connection is described as Tailscale and Termius | memory_mirror/tailscale-remote-access.md:8–12. This is a repository note, not a live network check. Its userspace-mode outbound limitation matters before designing remote worker access. |
| A Thunderbolt cable can carry a network between two Macs | Apple documentation: https://support.apple.com/guide/mac-help/use-ip-over-thunderbolt-to-connect-mac-computers-mchld53dd2f5/mac . Actual cable, connection and speed remain untested. |

## Section 1 — Separate working copies and machine roles

Approval: APPROVED — operator selected A; see decisions_log.md at 2026-10-11T05:55:58Z.

The Intel Mac will normally stay powered on and connected. The M3 occasionally travels; separation must be a normal condition, not a failure that prevents either machine working. Source: operator answer recorded in decisions_log.md at 2026-10-11T05:50:41Z.

Two approaches:

| Approach | Benefit | Trade-off |
|---|---|---|
| A. Separate working copies — recommended | Each Mac uses its own local files. Intel builders and research-engine queries do not keep reading memit while the M3 runs science. Rare travel leaves Intel's existing work and backups available. | Needs space for the Intel copy and clear handoff/version rules. Backups and source updates still cause some transfer load. |
| B. Intel works directly on files shared from memit | Fewer copies and less Intel disk use. | Cable loss interrupts work; bulk tests/database activity still competes for the M3's disk; concurrent edits need coordination. It gives less independence. |

Recommended roles under A:

- M3: MAESTRO and canonical Git operations, science model work, actual M3 host checks.
- memit, directly attached to M3: active science inputs and output bulk under the existing working-tier policy.
- Intel: builders for compatible non-model checks; the research-engine pilot; backups and approved Drive transfers; the phone dashboard. Its backup area and editable builder copies are separate, so builders cannot alter the saved copy.
- Google Drive: retained remote bulk and a copy outside the home, following separately approved activation and verification.
- Friend's Apple Silicon Mac: an optional temporary worker for a bounded package after hardware, owner availability and applicable gates are checked. The operator subsequently allowed a conditional friend-Mac model role; Intel remains prohibited from all local LLM runs. Actual friend jobs still require inventory, reviewed scope and launch permission. No unique authority or only copy lives there.
- M3 internal disk: operating system/tools and specifically budgeted temporary work; no archive role (CLAUDE.md:58–59).

A second Mac's disk is physically separate from memit but still shares the home's risks. A current mirror alone can copy mistakes; earlier versions and restore tests will be addressed in the storage section. The remote machine's owner can read its files even with a separate account; that account limits routine access but does not hide secrets from its administrator.

Operator section check: A approved. Storage across all resources must be optimized to prevent space exhaustion.

## Section 2 — What earns a place on each disk

Approval: APPROVED — operator selected storage approach A at 2026-10-11T06:02:09Z. Detailed automation and retrieval section remains proposed.

Operator requirement: storage must be very well managed across every available resource, with an optimized plan that prevents disk-full blocks. Exact words are in decisions_log.md.

Recommended direction: selective local retention, with verified remote retention for large finished data. The goal is usable science headroom, fast recovery and a bounded copy workload; it is not copying every regenerable file to every machine.

| Storage approach | Benefit | Cost or limitation |
|---|---|---|
| A. Keep what is useful locally — recommended | memit holds current science; Intel holds an independent recovery set and useful finished data; Drive keeps large finished material that must survive. Avoids three copies of every regenerable cache. | Needs an inventory identifying which files are required, recreatable or uniquely valuable, and checks before removal. |
| B. Copy all of memit to Intel and Drive | Easy to describe and restores more without downloads/recomputation. | Copies temporary data and caches too; Intel fills as memit grows and retained versions accumulate; initial Drive copy is slow. It may be useful as an initial safety copy, distinct from the optimized steady-state policy. |
| C. Move finished bulk to Drive with a small Intel recovery set | Most local headroom. | More dependence on connection speed and Drive for restoring large files. Less local recovery capacity. |

Proposed tier responsibilities under A:

- Git keeps code, evidence records, frozen inputs/manifests/hashes, decisions and source identities. MAESTRO owns canonical changes; Intel copies remain subordinate.
- memit holds the current science models, covariance inputs and bulk explicitly needed by the active analysis or a named follow-up. Historic bulk has no automatic right to stay there.
- Intel's disk has separate bounded areas for a protected recovery copy, editable builders, research-engine data, transfer staging and temporary support work. Completed large outputs can temporarily reside there without becoming the only copy. Capacity must be measured after formatting; the stated 1 TB is not treated as 1 TB free. The hardware's actual disk type and health are not yet verified.
- Drive is the durable destination for irreplaceable bulk and approved remote backups. It retains its existing separate activation and content-check gates. A selective archival policy must not silently alter the reviewed full-backup release.
- M3 internal disk keeps operating tools and approved bounded temporary work, without acquiring an archive role.
- The friend's disk is temporary job space only, never the only durable copy or part of required recovery.

Planning guardrails to refine after the tier choice:

1. A single inventory records every bulk item's size, class, responsible run, current verified locations and whether a named analysis still needs it. Totals count staging, versions, logs and temporary peak writes, including all services that share a physical disk.
2. Before a job, compare projected additional peak writes plus the existing 20 GiB reserve with real free space on every affected disk (EXPERIMENT_RUNBOOK.md:277). Plan for concurrent promised writes too; two jobs cannot both spend the same headroom. Unknown size or unavailable observation means wait, not assumed capacity.
3. A warning threshold must occur well before hard admission refusal. The warning triggers a concrete proposed transfer/reclaim list, not automatic deletion. Exact reserve/threshold amounts will be decided after capacity and workload inventories; 20 GiB alone is not a target operating buffer for large tensor jobs.
4. Moving files requires source identities, completed destination verification and a committed record of their location. Uploading is not verification. A failed/partial transfer does not qualify a file for removal.
5. Removal follows the existing protected-path rules and operator approval for the exact path, size and method (CLAUDE.md:60–61). Approved architecture does not preapprove deletions.
6. Backups retain earlier versions within an explicit budget, and never inherit source deletions silently. Freshness and restore checks are shown separately from successful transfer status.

These are design requirements for MAESTRO to review and implement, not existing measured automation. Storage approach A is approved. Backup frequency/version retention, Drive ownership and restore acceptance remain to discuss.

## Section 3 — A complete research library, with large files brought back when needed

Approval: APPROVED — operator answered "Yes" at 2026-10-11T06:06:06Z. This approves the intended library/access architecture; phase-1 expansion, specific retrieval allowances and implementation remain separate.

The Intel research engine must be able to discover relevant admitted research records wherever their supporting bulk resides. Storage placement must not hide a finding or imply a file is scientifically irrelevant. Drive is a durable archive and also a source from which needed data can be brought back. Archive is a storage location, not a scientific exclusion status.

The existing approved design already separates the vocabulary, numeric copy, connection copy and original artifacts (results/research_engine_brainstorm_20261011T032049Z/design.md:110–121):

| Component | Plain-language purpose | What stays accessible locally |
|---|---|---|
| Ontology/vocabulary | Defines what a finding, experiment, measurement or relationship means and what information it must carry | Versioned definitions and checks; it is not the container for every raw file. |
| DuckDB | Searches exact recorded numbers, their setup, limits and sources | Admitted measurements and record/link information. |
| Neo4j | Searches connections among findings, questions, tests, decisions and sources | Reviewed connections, selected summaries and pointers to originals. |
| Original records and file catalog | Lets researchers read the full account and identify exact supporting artifacts | Complete admitted source text/records plus identities, sizes, locations, verification state and retrieval requirements for bulk files. |
| memit, Intel staging or Drive bulk | Holds the large model, tensor and other data files | Bulk exists outside the two databases; selected files are retrieved for a named analysis. |

Completeness means honest full-program coverage in the eventual library, not a claim that every file has already been imported, or that copying all tensors into databases is desirable. The approved pilot still covers five checked source chains; vocabulary and instances are restricted, and tensors are excluded (phase1_spec_v5.md:82–100,116–120). The subsequent whole-program expansion and shared service must be separately scoped/reviewed (original design:227–245). Queries outside pilot coverage say so; they cannot report that nothing is known merely because it was not imported.

Proposed query-to-analysis flow:

1. A researcher asks the Intel service a question. Both databases use the same pinned source snapshot; the answer includes exact records, scope, caveats and original source references (original design:114,119,134–138).
2. If a deeper analysis needs bulk, it produces a request naming the exact files/versions, reason, destination worker, expected download/write/memory/time budget and any scientific authorization required. A missing file or unverified location is explicit.
3. The storage manager checks availability, local space including promised writes, work already using the data and permission. It chooses Intel for compatible CPU-only work, M3 for its science environment, or a loan worker for a separately authorized non-LLM package. The operator clarified at 2026-10-11T06:47:30Z that the friend's Apple Silicon Mac may run separately gated model jobs; Intel remains prohibited. The archive policy does not determine scientific relevance.
4. The authorized transfer worker brings in only the required files and verifies identities before analysis. The researcher holds those files for the task so a cleanup cannot remove them underneath it. The immutable original result stays archived.
5. New analysis outputs and requests return through MAESTRO's staged review workflow. Exploratory ideas, CPU math and actual model experiments remain separately labelled. After the named analysis releases the files, the manager may propose reclaim; actual removal still requires exact-path approval.

Proposed automation split:

- Automatically inventory and classify files at creation, using the producing job's declared artifact policy rather than an agent's guess that data is worthless.
- Automatically identify archival candidates after completed/confirmed reading or an explicitly closed no-claim run, subject to named follow-up/analysis holds and the protected-path policy (runbook:271–277; CLAUDE.md:60–61). Record the complete eligible manifest and rationale.
- Copy and verify through a separately authorized archive job with fixed space/bandwidth/concurrency limits. Never treat an initial successful upload, warning or partial transfer as proof of durability.
- Keep research records and artifact locations searchable after archiving. Rebuild publication only from admitted immutable source identities, with missing coverage visible.
- Small preapproved retrievals may be automatic within a fixed allowance; large retrievals or any model experiment require the existing manager's clearance and relevant authorization. This allowance is a future design choice, not granted by this section.
- Physical removals remain operator-approved by exact path, size and method. Automation prepares the removal decision; it does not silently inherit deletion permission.

All owned workers can eventually query the same controlled research service or consume a clearly dated published snapshot. They need not carry database-server copies. Shared access is a future reviewed service requirement, not an assertion that it exists. The friend's worker receives curated task inputs/answers and returns staged results; it does not receive Drive tokens, GitHub credentials, provider keys or unrestricted access to the research library. A separate account cannot conceal files from the friend's administrator.

Research depth must not be tied to which bulk happens to fit on Intel. Full evidence text, negative results and caveats are needed alongside database queries; recorded metrics and reviewed connections cannot replace reading originals. Analyses that need missing bulk wait explicitly for retrieval. Analysis output from a halted/compromised run remains limited to its reviewed historical scope even if the file is retrievable (phase1_spec_v5.md:134–136).

Section check: approve the intended arrangement of all admitted research records being searchable, with exact large files requested for deeper analysis and copied/removed under distinct permissions?

## Section 4 — Copy frequency and separate Intel space limits

Approval: copy schedule A APPROVED at 2026-10-11T06:10:21Z; starting capacity caps APPROVED at 2026-10-11T06:13:41Z subject to actual capacity inventory; history retention A APPROVED at 2026-10-11T06:15:30Z within the agreed history cap.

Recommended copy schedule: small finalized research records and approved builder handoffs are copied after each accepted update; useful changed bulk is copied nightly when the M3's science coordinator permits disk reads. For newly created irreplaceable bulk, a named run's durability requirement can demand an earlier transfer before it is considered safely retained. A nightly schedule alone cannot meet an immediate durability requirement. Files still being written are not labelled a consistent backup. The Intel machine initiates transfers from a completed manifest; published copies are separate from editable working areas. Source disconnect, copy/verification failure or capacity refusal leaves the old verified checkpoint visible with its age.

Alternative schedules:

| Option | Benefit | Trade-off |
|---|---|---|
| A. Small records after accepted updates; bulk nightly when safe — recommended | Keeps the research library current and bounds large disk reads. | Up to a night's changed bulk can remain unprotected unless a run requires earlier copying; M3 travel or continuous science can delay the job. |
| B. All changed data copied continuously | Shorter normal gap between copies. | Repeated reads and copying changing outputs contend for science disk; active files require a consistent capture mechanism. |
| C. Copies only on request | Least background activity. | Forgotten copies leave a longer recovery gap. |

No policy schedules uploads/second copies against arbitrary live files while assuming they form one coherent run. Completed run manifests and exact source versions define the copied set. A whole-volume backup remains a distinct reviewed job with its own consistency and activation procedure. Incremental transfer means copying only verified changed items while referencing unchanged ones, not deleting destination files to match source removals. Hard links or filesystem clone sharing, if chosen in implementation, must protect immutable backups from builder mutation; no filesystem capability is assumed here.

Approved Intel starting planning caps, decimal GB, subject to post-format capacity/OS/health inventory. Operator approved these caps at 2026-10-11T06:13:41Z:

| Area | Proposed maximum | Reason |
|---|---:|---|
| Current recovery set | 400 GB | Room beyond the brief's 320 GB project estimate without granting unbounded mirroring. Exact included files to be inventoried. |
| Earlier backup versions | 100 GB additional unique data | Protect against an overwritten/deleted file; do not store repeated full 320 GB copies. Retention targets to be settled. |
| Editable builder work and tools | 80 GB | Small source copies, environments and capped receipts; avoid multiplying model caches per builder. |
| Large-file staging and CPU analysis | 100 GB | Temporarily receive a named task's data; larger tasks use reviewed batching or another destination. |
| Research-engine pilot | 5 GB data + <=1 GB separately budgeted provisioning growth | Starting ceilings from phase1_spec_v5.md:207–211,244–246, moved to Intel under a new reviewed host specification. No implied permanent M3 archive. |
| Unassigned free headroom | >=100 GB normally | Space for temporary peaks and operating system updates; not a spendable budget shared independently by several jobs. |

The proposed ceilings total 686 GB plus 100 GB unassigned free headroom, before existing OS/user files. They are ceilings, not reservations to fill each area. Actual formatted capacity and existing usage may require tighter limits. Every job must still pass projected additional peak writes +20 GiB on each physical disk; shared area totals include existing files and temporary duplication. No job may borrow another area's free quota without a reviewed capacity change. Disk usage is measured once per physical pool, not counted as independent space on its volumes.

For memit, approved steady-state target >=100 GiB free (approximately107 GB); warning below80 GiB free (approximately86 GB); retain the binding per-job projected-writes+20 GiB check. Current observation of74.7 GiB free is already below that proposed warning. An eligible transfer/reclaim plan is needed; no removal is authorized here. If the next frozen run needs150 GiB peak additional writes, 100 GiB is insufficient and admission still waits. A run that cannot fit requires its own reviewed storage amendment; this design cannot silently stream or change a frozen preregistration.

The storage manager's inventory distinguishes archival location, scientific retention obligation, active-task holds, backup freshness and restore verification. It displays queued commitments and the minimum remaining headroom after admitted work. Its early warning presents exact candidate paths/bytes/verified copies for MAESTRO and the operator; it never converts a low-space warning into deletion authority. History/staging/log cap exhaustion pauses the responsible support job rather than consuming science headroom.

Copy schedule A approved. Next section check: numerical starting space budgets, followed by version retention/restoration. Alternative to per-area caps: one flexible Intel pool with only a shared free-space floor; simpler allocation but allows builders/backup history to consume each other's room. Recommend per-area caps plus the shared floor, with adjustments only after measuring capacity and demand.

## Section 5 — Earlier versions and restoration

Approval: APPROVED — retention/recovery option A at 2026-10-11T06:15:30Z. Commissioning and drills are future separately scoped work, not performed by HW1.

| Retention option | Benefit | Trade-off |
|---|---|---|
| A. Seven daily and four weekly restore points — recommended | Can recover a recent mistake or one noticed weeks later. | Extra unique content must fit within the100 GB history cap; this is a target, not a guarantee independent of churn. |
| B. Current plus one previous verified restore point | Uses less history space and simpler operation. | Less protection when a bad change goes unnoticed for days/weeks. |
| C. Longer local history | More time to discover mistakes. | Needs a larger approved history budget, reducing other uses of the1 TB disk. |

Each restore point is a dated manifest selecting exact immutable saved file versions. Unchanged files are reused where the implementation safely supports it; earlier versions must remain immutable and cannot share writable builder files. The seven/four policy selects versions of the defined recovery set, not eleven full copies of memit. The100 GB cap counts all additionally retained unique bytes and metadata. If a required version would exceed the cap, preserve existing verified restore points, report backup age/coverage, and surface exact approved options: more remote retention, a narrower recovery set, more capacity, or exact-path removal. Do not silently trim history or claim target retention was achieved. Whether remote older versions are implemented is a separate reviewed archive policy; the existing Drive full-backup release has no new retention semantics conferred by HW1.

Restoration requirements for the future build:

1. Define the recovery set and exclusions explicitly: canonical Git records/code/manifests, original admitted research records, versioned research-engine inputs, active science inputs that policy requires, and specific irreplaceable bulk. Models/caches recoverable from pinned public sources may be excluded by an approved selective policy; declare that longer restore dependency. Secret-bearing home/config files are excluded from generic backups; operator-owned credential recovery is handled separately.
2. Commission the Intel copy with a small deliberate restore of known files, including one old version, a manifest and a selected bulk sample. Verify exact identities after restore. Check missing/corrupt source and disconnected-cable controls; failures must appear in the same status view as success.
3. For actual loss of memit, use a fresh approved destination. Recover Git-controlled records from the canonical repository or a verified independent Git copy; restore the matching bulk manifest from Intel, then request exact absent files from Drive or rebuild permitted regenerable inputs. Never overwrite surviving evidence during recovery.
4. Before resumed science, MAESTRO confirms restored source revisions, dependency environment, engine fingerprint and applicable baseline/inertness gates (CLAUDE.md:30–34). Successful copying is not a science-baseline PASS. A restored Intel/Drive generation cannot rewrite the authoritative Git history.
5. During planned M3 travel, ensure a named verified checkpoint exists, identify remaining unprotected writes and stale source dates, and let Intel continue from its own files. No automatic switch of MAESTRO/Git/science authority. New Intel builder outputs wait for handoff when the M3 returns.
6. After each monthly cycle, propose a small restore drill on an unused destination with a fresh receipt. Keep it within resource limits and run only under its separately authorized implementation/operating scope. Do not launch it in HW1. Remote verification/restore use stays within Drive's approved bandwidth and activation limits.

Record verified-copy count, last complete checkpoint, protected-byte coverage, intended versions actually present, known omissions and latest restore-test result. A progress bar or an upload exit0 alone is insufficient. All copies in one home remain vulnerable to the home's failure; Drive is independent of that location but has access, quota and transfer-time risks. The M3 internal disk never becomes an emergency archive tier by default.

## Section 6 — Intel builders, code handoffs and M3 verification

Approval: APPROVED — builder option A at 2026-10-11T06:19:02Z, with binding no-local-LLM constraint.

| Builder placement | Benefit | Trade-off |
|---|---|---|
| A. Intel for code and compatible non-model tests; M3 for required platform checks — recommended | Removes builder test processes from M3 admission while preserving actual science-host verification. | Requires explicit split of verification and a reviewed return handoff. |
| B. Intel edits code; all tests stay on M3 | Most similar test environment. | Most builder Python/test contention remains on the science machine. |
| C. Force the full M3 science stack onto Intel | Superficially uniform job placement. | Official macOS x86 PyTorch stops at2.2.x versus installed M3 torch2.8.0; downgrades/source builds change the scientific environment and are not authorized. Not recommended. |

Only MAESTRO commits, pushes, changes PRs and merges (CLAUDE.md:50–54). The Intel is an operator-owned worker, not another canonical writer. Its protected recovery area, research-source snapshot and each editable builder area are distinct. Each builder starts from the exact reviewed base commit plus any explicitly admitted immutable uncommitted source snapshot, with named scope/source hashes and an exact acceptance list. Unrelated live work is not transported as anonymous dirty changes. Worktrees/checkouts on different machines have different local Git locks; they must not be treated as one shared mutation lock.

Code transport uses a read-only exported source package or Git bundle from the reviewed source, transferred over the private local cable connection. The implementation brief chooses and demonstrates that interface before automating it; no remote Git write credential is needed on Intel. Never copy the M3 virtual environment: create separate Intel-compatible support environments under a reviewed package lock. Do not downgrade the M3 torch/transformers pins. Codex sessions on Intel use the operator's own separately approved authentication; generic copies must not carry credentials.

Intel runs RED/GREEN tests that are independent of a live model/GPU and compatible with its package environment: pure state folds, manifest/receipt logic, parsers, source-consistency checks, fixture storage/network cases and database support tests whose dependencies pass Intel commissioning. NumPy/math work can use a separate locked CPU environment when included in the brief. Some tests import modern torch without loading a model; those are not automatically Intel-compatible. Required coverage is classified from actual imports/runtime, not filename or intuition.

Builder return package: exact base/source identities, patch or changed-file package limited to allowed paths, test list with saved behavioral RED/GREEN receipts, environment/platform identity, before/after scope hashes and explicit UNVERIFIED items. MAESTRO compares current canonical sources with the supplied base before applying. Concurrent changes are reconciled; a stale package cannot revert newer work. No Intel builder mutates master, the canonical science files on M3 or a live run through a shared mount.

Required M3 platform/modern-torch/native-host checks are queued for a science-safe window after source review. Linux CI and Astra remain required at their existing gates. Intel fixture PASS does not establish M3 host, GPU, remote-Drive or scientific PASS; required checks left for M3 remain open rather than skipped-as-green. A host/environment difference is not science replication.

Moving the actual tests removes their processes from the M3's local inventory; remote tests do not consume its unified memory. M3 gate classifiers/exemptions stay unchanged (tools/c10w_p2_gate.py:22–54,73–84). A local Python orchestration loop left running on M3 could still block admission; prefer short approved boundary calls, and verify the actual runtime shape in the future commissioning brief. Intel backup/source transfers still read memit, so their disk activity needs separate coordination even though test compute has moved.

Starting Intel concurrency recommendation: one builder test job at a time, alongside bounded research-engine use. Target aggregate support-process memory <=6 GB on the stated16 GB machine, research-engine aggregate <=3 GB with Neo4j<=2 GB RSS per the existing pilot, and at least6 GB practically available for OS/user activity. Pause new heavy support jobs if actual memory-pressure observations or storage budgets are unsuitable; unavailable observations mean no new heavy admission. The6 GB aggregate is an initial design target to verify with representative non-model workloads, not measured enforcement. Widen builder concurrency only after recorded Intel commissioning and a reviewed resource update. Use background priority for support processes, continuing the existing niceness>=10 convention (phase1_spec_v5.md:213; memory_mirror/background-shell-niceness-10.md:7–13), without claiming priority alone prevents contention.

Intel CPU science support may include reviewed tensor-independent math, statistics on already admitted measurements and literature/evidence preparation. It is not banned from all science-related calculation. Large tensor math is possible only with a compatible, reviewed environment and explicit input/output/memory/time budget; data then carries its own platform identity. Local LLM inference/editing/training/embedding work is prohibited on Intel by the operator, even with a legacy/source-built stack. Intel may store inert model backup files, but storage never authorizes executing them. Hosted Codex/Claude services are distinct from running a model locally and still use separately approved operator authentication.

## Section 7 — Intel research-engine move and what must yield to science

Approval: APPROVED — coordination A at 2026-10-11T06:30:29Z. Intel hosting is the requested direction; a new frozen host spec, compatibility commissioning and permitting Astra review still belong to MAESTRO.

Binding operator constraint, recorded 2026-10-11T06:19:02Z: no local LLM models run on Intel; local model work on owned Macs is assigned to M3; as clarified later, the friend's Apple Silicon Mac may be a temporary separately gated model worker. This includes inference, edits/training and model-based local embeddings. Database storage/querying, compatible non-model calculations and hosted-agent use are distinct. Generic backup copies can contain inert model files; do not execute them. The friend's model-work exception was explicitly approved in section10, contingent on inventory and separately authorized jobs.

| Coordination option | Benefit | Trade-off |
|---|---|---|
| A. Intel research work continues during M3 science; shared-disk transfers yield — recommended | Takes advantage of separate CPU/memory/local disks and removes the rejected same-host database shutdown problem. | Requires accurate source snapshots and explicit transfer/disk-load coordination. |
| B. Stop Intel's research engine whenever M3 does science | Simple blanket scheduling. | Idle Intel resources and no necessary protection when the work reads only its own local copies. |

Under A, Neo4j and DuckDB use local Intel copies only. M3 model/science launch does not terminate Intel's database or builders. Local Intel questions/math can continue from a dated immutable source generation, including while the M3 travels. Queries must expose snapshot age and coverage. New combined answers still require both stores' matching source-generation identity (original design:119). Immediate shared-disk access is not a prerequisite for every query.

A narrower coordination mechanism is needed for operations that read/write the M3 or memit: source copies, large backup reads, direct Drive upload from memit, and bulk retrieval into memit. These operations obtain a disk-work allowance from the M3-side coordinator before starting; pending science prevents new bulk transfers and asks an active resumable transfer to pause at a verified safe boundary. A missing/disconnected/unknown coordinator is not an idle signal and cannot start new shared-disk bulk work. No synchronous remote-database shutdown or polling promise is carried over. Normal Intel-local computation continues through link loss; transfer state/age stays explicit. Exact pause/clearance latency must be frozen and verified against actual transfer/runtime interfaces in a later brief, not invented here.

Intel resources still need local control: approved5 GB pilot data, separate<=1 GB setup-growth budget, Neo4j<=2 GB RSS/engine aggregate<=3 GB, background priority and session-only database startup from the existing phase1 choices/spec (operator_phase1_choices_20261011.md:5–13; phase1_spec_v5.md:207–217). One active builder test job is the starting limit. Aggregate support memory target<=6 GB and a practical>=6 GB OS/user allowance remain proposed commissioning limits from section6; high memory pressure pauses new heavy admissions. Database queries cannot launch local models, automatically execute code from papers or reach around MAESTRO's science authority. Session-only/start-stop limits remain until separately approved, even if the Intel stays powered on.

Changes MAESTRO must make in a new reviewed host specification, rather than editing frozen v5 in place:

1. Amend the earlier "on this Mac" hosting/storage choice and D-RE-1 record to Intel hosting. Pilot data/temp moves to Intel's budgeted local area; M3 internal storage does not become an archive. Preserve originals and the decision history.
2. Re-pin Intel/Sonoma-supported Neo4j Community, Java, CPython/DuckDB and Homebrew dependencies through actual compatibility/identity checks. The v5 ARM Homebrew paths, OS, bottle hashes and dry-run receipts are not Intel acceptance (v5:244–246). If the chosen native packages are unavailable/incompatible, stop for a reviewed hosting change; do not silently switch to a cloud database, Linux VM, different version or different edition. Budget any alternative separately.
3. Replace the same-M3 science-reservation/termination contract and its host-specific tests with explicit independent-host placement plus coordinated shared-disk transfers. Account for AC17/AC21, source paths and commissioning assertions rather than dropping them without a replacement rationale (v5:53,57,195–217).
4. Keep original evidence authority, independent answer-key author, five-chain scope, reviewed link meanings, paired-store publication, coverage/refusal semantics and Astra promote/closeout gates. Source capture references the admitted immutable export/Git revision, not the assumption of a local M3 worktree (v5:15–21,37–57,143–153).
5. Inventory every r3/r4/r5 finding and state whether relocation removes its premise, whether a replacement requirement addresses it, or whether it remains open. Moving machines does not convert any NO-GO into GO. Supply a fresh Astra review of the amended spec and actual Intel commissioning receipts before reliance. Do not launch extra reviewers or provision anything in HW1.

This is an amendment request for MAESTRO, not a claim that the engineering research engine is built or that hardware separation itself proves correctness. The local-LLM constraint categorically excludes Intel; M3 remains the primary science host and the friend's Apple Silicon Mac is a conditional temporary worker under section10.

## Section 8 — Drive transfer source and phone dashboard

Approval: steady-state Intel transfer route A APPROVED at 2026-10-11T06:35:31Z. Dashboard must serve both phone and local running views. First-upload Intel route A APPROVED at 2026-10-11T06:38:13Z; revised activation review and host commissioning remain required.

| Transfer source | Benefit | Trade-off |
|---|---|---|
| A. Intel uploads its verified local copies — recommended | Internet transfer continues without M3/memit reads, including during M3 travel; recovery and archive transfers reuse the same immutable data where safe. | Requires Intel capacity, exact source manifests and new host/credential/acceptance checks. Initial M3-to-Intel reads still coordinate with science. |
| B. Intel uploads directly from M3-shared memit files | Can avoid a separate staging copy of files outside the recovery set. | Long transfers keep touching the science disk and require the M3/cable to stay available; partial/live-file handling remains necessary. |
| C. Keep the current reviewed M3 Drive worker permanently | Reuses the planned host release and existing host findings. | Leaves transfer processes and disk reads on M3; does not implement the requested Intel support-host role. |

A distinguishes two stages: capture/copy exact complete source artifacts from M3 to Intel during admitted disk work; then upload/verify on Intel under the approved day/bandwidth budget. Uploading Intel data does not consume M3 CPU/memory/disk. Source age and incomplete coverage remain explicit; a complete Intel upload of yesterday's checkpoint does not mean the current M3 state is backed up. Each pending artifact has a durable identity/location/status record. Changed/live source bytes require a new immutable version, never replacement of a historical identity.

Use existing verified Intel backup objects as upload sources where the implementation protects them from mutation, rather than creating another full project copy. Count shared physical bytes once for actual disk use while conservatively budgeting any additional capture/temp duplication. Files outside the recovery set use the100 GB analysis/transfer-staging budget; eligibility depends on the exact file sizes and retained in-flight copies. Oversized requests wait for a reviewed plan instead of borrowing the M3 internal disk. Source copies, friend-package uploads and Drive downloads cannot all spend the same promised staging headroom.

Only the operator-owned Intel Mac may receive separately authorized Drive authentication. Generic source/backup/task packages exclude Drive tokens, GitHub credentials, provider keys and credential-bearing configuration; the friend's machine receives none. Moving credentials is a distinct operator provisioning decision, not permission granted by this design choice. Drive scope/quota/bandwidth and the wrapper's generation/unresolved/verification semantics remain part of the future transfer-worker brief. The existing activation plan still requires its exact review, operator OKs and full convergence/content checks (activation_plan_v4.md:3,314,362; runbook:279). A new Intel source/host cannot inherit M3 launchd/app permissions, pinned deployment paths or host-acceptance receipts. No existing backup activation is silently replaced or declared complete by HW1. MAESTRO decides whether to finish the existing separately approved rollout before migrating or to submit an amended Intel rollout, under the preserved activation gates.

Connectivity, quota, auth or rate-limit errors retain local data and make archive status explicitly incomplete. Transfer retries/resumption remain within an approved deterministic worker contract; a fresh generation/output namespace is used where source identity changes. Low Intel space pauses new staging; it does not remove the sole copy. Drive's archival catalog distinguishes required retained objects from regenerable caches; a future history policy must be reviewed rather than assuming a syncing remote preserves all old versions.

The dashboard service/status feed lives on Intel and serves both phone and local running dashboard views (including the operator's local Mac/terminal/browser views). These share source definitions and freshness semantics. It has three small views: M3 science/MAESTRO status; Intel builders/research engine; storage/copy/restore state across resources. It consumes source-owned dated status snapshots. When M3 is away or a connection fails, show last-seen time and UNAVAILABLE/current observation unknown, never "idle" or an invented zero count. Critical tasks, backup warnings, cap exhaustion and pending operator decisions stay visible. The friend is an optional separately identified worker, not a required always-live dashboard dependency.

Existing dashboard scripts may inspect local ps/tmux/files and paths. Simply running them on Intel would then observe Intel, not M3; the future brief must define source-host identity and small status transport, positive controls and failure sinks. Reuse the approved M3 status collection where possible; do not add a continuous non-exempt Python collector or --gpu-summary poll that recreates launch contention (CLAUDE.md:30; tools/c10w_p2_gate.py:32–35,73–84). Runtime exemptions stay unchanged unless independently reviewed. Dashboard views do not merge/launch/delete or overrule events.jsonl/fold/MAESTRO authority. The operator connects from the phone and local dashboard clients to the Intel view through separately approved private access; M3 control remains a distinct explicit destination. Service/collector outage cannot erase published evidence.

### First Drive upload and files currently on M3 internal storage

Approval: APPROVED — first-upload A at 2026-10-11T06:38:13Z: stage a verified checkpoint on Intel and run the first large internet upload there. Alternative B: finish the current M3-host rollout for the first upload, then migrate; less host-plan amendment before first transfer, but science contention remains on M3.

The source may contain selected files from both the M3's internal SSD and memit. Location alone does not make a file part of the authoritative science set. A read-only directory probe in HW1 at 2026-10-11T06:35:31Z confirmed `/Users/robertrhu/Backups/memit` exists. The legacy `tools/backup_mirror.sh:20–23` defaults its destination under that internal directory and source under memit. That establishes an old mirror location, not its current contents, size, freshness or scientific completeness. Its header's internal-SSD durable-tier wording is superseded by CLAUDE.md:58–61. No bulk traversal, hashing, cleanup or copy was performed.

MAESTRO's initial inventory must distinguish canonical live sources, old internal mirror copies, unique internal offload artifacts and the external working set. Compare exact manifests/identities; identical bytes need not consume two Intel recovery copies, while different versions remain distinct until reviewed. Do not blindly upload the entire internal SSD or assume its old mirror is current. The required staging/recovery bytes must fit the approved400 GB recovery and100 GB staging caps, including temporary duplication; otherwise present a specific revised budget/selection before dispatch. No original is removed by initial staging.

The first job has distinct phases:

1. Inventory and freeze the exact selected source/version set; satisfy the new Intel host/credential/source-path review and disk budget. Preserve all existing Drive activation obligations or explicitly amend their semantics with operator scope and Astra review.
2. Transfer exact completed files to Intel over the local cable during permitted M3 disk work; verify the Intel checkpoint against source identities. This still reads the M3 internal/external disks, so it is not promised contention-free. Changing source bytes prevent that file from joining a consistent checkpoint until recaptured under the approved capture procedure.
3. Upload and verify that immutable Intel checkpoint against Drive. The M3 can continue science while internet transfer and remote content checking use Intel's own disk; new M3 outputs belong to later manifests. Show the checkpoint date and the remaining source-to-backup gap.
4. Complete the activation plan's catch-up/consistency/full content-check requirements against its explicitly reviewed source definition before declaring activation or permitting retirement of an old copy. The current plan requires an operator write pause and final catch-up, with no waiver for changes during initial upload (activation_plan_v4.md:314–316). An Intel immutable-checkpoint design is a proposed revision, not proof that the current live-source gate is already met. Do not promise a short pause or zero science downtime until the revised procedure and timing are verified.

Benefits are specifically during Intel-local internet upload/checking; the initial local capture and any required final source catch-up retain M3 disk and consistency obligations. A successful cloud copy of an older checkpoint is still valuable for recovery, but cannot be labelled a current fully converged backup.

## Section 9 — Local cable and private remote access

Approval: APPROVED — connection plan A at 2026-10-11T06:42:39Z. Thunderbolt for owned-Mac transfers, independent internet, phone/local Intel views and private device-only friend access. Setup/authentication/owner agreement remain separate.

| Owned-Mac connection | Benefit | Trade-off |
|---|---|---|
| A. Direct Thunderbolt cable for local transfers; each Mac keeps its own internet connection — recommended | Separate local transfer path, consistent destinations and no dependency on passing all internet through M3. Intel remains online when M3 travels. | Requires a genuine Thunderbolt-capable cable and measured stable connection; file services/access must be scoped. |
| B. Use Wi-Fi for both local transfers and internet | No dedicated cable setup. | Copies share Wi-Fi capacity with internet use and may vary with connection conditions. Actual speed is not assumed. |

The direct cable creates a private network between the two Macs [Thunderbolt Bridge]. It does not combine their memory/GPU or turn both disks into one capacity pool. Keep memit physically on M3. Both Macs retain their own ordinary internet path where available. Named folders/status services are shared through separately authorized authenticated access; avoid a writable whole-project mount and avoid exporting user home/credentials. The permitted source/copy paths and user identity are frozen with the future transport brief. Stable connection identifiers/addressing and host identity checks are routine implementation choices; verify the route uses the cable and measure actual sustained transfer speed before estimating initial-copy time.

Apple documents direct IP over Thunderbolt between two Macs: https://support.apple.com/guide/mac-help/use-ip-over-thunderbolt-to-connect-mac-computers-mchld53dd2f5/mac . No cable, route, file-service permission or speed test was run in HW1. Different filesystem/OS support and sleep behavior are part of commissioning. If a link drops, Intel computation continues from its own files; incomplete transfers remain unverified. Resume only under the approved transfer contract. Sleeping/offline computers cannot be assumed reachable.

The operator's existing phone route uses a private connection app and Termius; repository note memory_mirror/tailscale-remote-access.md:8–12 describes Tailscale's existing M3 userspace setup and its outbound-proxy limitation. That is historical configuration evidence, not live reachability. Intel phone/local access should use approved owner identity and a separately tested route. Do not assume M3 can automatically reach every new private peer just because the phone can reach M3. Dashboard remains a source-identified view with dated fallback; retained published records stay accessible locally if the interactive service is down.

For the friend's different home network, recommend sharing only that Mac through a private connection app [Tailscale], then ordinary authenticated Mac remote login/file transfer [SSH] to a separate non-admin research account. This is a future setup proposal, not authorization to SSH or change anyone's network in HW1. The friend owns the device and must agree to the account, time window, file scope and access. Ordinary SSH is distinguished from Tailscale's separate SSH-server feature, whose host support/policy is not assumed. The owner shares one device to the operator's individual identity, with only required service access; do not join entire home networks, expose a router port to the public internet or grant the friend's machine access back into the science network.

Tailscale documents single-device sharing between separately administered networks and default quarantine of shared devices: https://tailscale.com/kb/1084/sharing . Actual chosen sharing/policy behavior, macOS SSH account restrictions and connectivity must be verified during separately approved commissioning. Sharing does not make the friend's administrator unable to read delivered files. No Drive token, GitHub write credentials, API/provider key, private SSH key or personal home/config backup is sent to the friend's machine. Authentication uses credentials retained on owned devices and whatever device/account identity the friend manages himself; only public-key material needed for the restricted login is delivered. Alternatives are manual exchange of curated packages (least connection setup, slower interaction) or a broader shared-network account (more administration and trust; unnecessary for one temporary worker). Recommend device-only access or manual packages, not broader trust.

Section check: approve the owned-Mac cable arrangement and private device-only remote access as the intended connection architecture? Friend's model-work scope and availability will be asked separately; nothing is connected yet.

## Section 10 — Friend's model-work scope

Approval: scope option A APPROVED at 2026-10-11T06:47:30Z. The friend's Apple Silicon Mac may run models; Intel may not. Operator will verify availability/constraints in the next24 hours. This is role approval, not a run/connection authorization.

The original MAESTRO brief proposes independent Apple Silicon replication, while the operator later said "no local LLM models can run on the Intel, only the M3." Intel remains categorically prohibited from local model execution. Before designing a model job for the friend, ask which scope was intended:

- A. The ban applies to Intel; the friend's Apple Silicon Mac may run a bounded, separately approved model job after inventory/baseline gates — recommended if the aim is independent replication and the friend has enough capacity.
- B. M3 is the only local-model machine including the friend; loan work is confined to non-model analysis/testing.
- C. Keep the friend's scope undecided until chip/memory/hours are known; current authority remains M3-only.

An architecture choice allowing a possible friend job is not permission to connect, download models or launch experiments. Hardware capacity, the friend's agreement, source/stack/prereg identity, memory/disk/time budgets, baseline gates and MAESTRO/Astra review still precede any actual run. No borrowed-machine science result is authoritative merely because it came from another device.

## Section 11 — Conditional loan-machine trial

Approval: PROPOSED; trial order/time box awaits section check. Availability/constraints will be supplied by the operator within24 hours, recorded 2026-10-11T06:47:30Z. The design can be completed conditionally without inventing the missing facts or starting a job.

Ask the friend for: exact chip/model, memory, macOS version, actual free disk, dependable quiet hours, expected loan duration, his normal model workload, permitted power/sleep settings, allowed downloads/data scope, and how urgently he may reclaim the computer. No private credentials are requested. Require a separate account and his explicit agreement to the time window/resource caps/access and completion/cleanup process.

| Trial order | Benefit | Trade-off |
|---|---|---|
| A. One-week initial trial: prove baseline, repeat one selected result, then consider extra runs — recommended | Establishes whether this worker is trustworthy/useful before consuming a loan window on new science. | Startup/source transfer and a baseline consume part of the week. Actual loan length may shorten the trial. |
| B. After baseline gates, use the loan for new queued tests first | Earlier new-data throughput. | Less direct replication of an important existing result; new-test outcomes on a newly commissioned host need careful separation from M3 evidence. |
| C. Use only for non-model work initially | Useful if memory/quiet hours prove insufficient. | Does not provide cross-device model replication; remains the capacity fallback rather than the chosen model-role prohibition. |

Default proposal: seven calendar days after successful owner agreement/commissioning, or the shorter period the friend offers. No job starts without a named remaining time window and enough time to return deciding receipts/results. One local model job at a time on the friend's Mac, and no simultaneous competing friend model jobs during the approved window. GPU serialization is per machine; a separately approved friend job may run while the M3 runs its own science because memory/GPU are separate. Independent-host concurrent observations remain separately identified, never pooled as one run.

Memory planning branches (selection depends on measured peak, not this table alone):

| Reported memory | Candidate use before any promised editing capacity |
|---|---|
|8 GB | Non-model analysis/tests; a small quantized-model read test only if measured total peak and OS headroom fit. No3B edit capacity assumed. |
|16 GB | Small3B inference/readback candidates with a bounded sequence/batch; no full3B edit/solve fit assumed. |
|24–32 GB |3B editing/replication may be eligible after the exact job's full CPU+GPU+covariance+temp peak is budgeted and independently checked. |
|48 GB or more | Closer to the M3's capacity envelope, but chip/stack/timing/baselines still require commissioning. No automatic move to7B or different model family. |

Qwen2.5-3B remains the first candidate anchor, matching the current program's Qwen-ceiling policy in runbook§0.3. Qwen3/7B historical usage does not authorize a model change on the loan worker. Candidate cheap baseline: reproduce the readback of a small compiled edited artifact, if its exact files/runtime/probe set are available. CORPUS/17:9–12 documents about1.8 GiB Q4_K_M data and explicit edited/native eligible pools; runbook§0.3's M3 B3 reproduction gives the later host reference. A readback-only repeat demonstrates that read path, not independent recreation of editing. If the friend has enough memory, MAESTRO can instead choose one reviewed edit/mechanism replication that advances the live§0.3 frontier. The exact result is selected after inventory and bounded-source review; never salvage a compromised/halted run by rereading it under a new host.

Required gate order before borrowed data counts:

1. Freeze the host identity/account/OS/architecture, source commit and allowed dirty snapshot, unmodified engine identity, package versions, model/tokenizer/data/artifact hashes, pristine input namespace, job budget and expected baseline endpoints. A reused friend cache counts only after exact identity checks; do not assume his installed stack equals ours. Dependencies/source transport/actual account/process observations are commissioned through read-only/fixture probes before scientific dispatch.
2. Engine fingerprint passes (LAW1). Run the prereg's applicable cross-process determinism and null/inertness controls (LAW2/LAW5); compare behavior under the defined rule, not GPU bit-exact weights. For a compiled artifact, preserve its producing-engine identity and validate the actual compiled-runtime/tokenizer path; a source fingerprint cannot substitute for artifact/runtime checks.
3. Reproduce the known baseline within its frozen tolerances (LAW3), from the exact current source/prereg/reference. Miss/unknown/observation failure halts. No next arm and no new finding before it clears (CLAUDE.md:30–34). Baseline criteria/tolerances are preregistered by MAESTRO/Astra before results, not set after seeing host differences. REPRODUCIBILITY.md has historical pod/Intel-target headers; use the current M3-source receipts, not those retired assumptions.
4. Run one separately authorized, preregistered replication. Record host/stack/source identities and durable stage/terminal receipts; write outputs to a fresh worker/run namespace. No writer updates CORPUS/Git/decisions remotely. Fresh receipt capture and current source manifests accompany the return.
5. Return and independently verify the complete deciding result/log/manifest package on an owned machine before considering extra runs. MAESTRO/Astra bind promotion; a loan-device PASS is not automatically an F1 closure or a substitute for an M3 acceptance requirement. Bystander/locality and scope caveats remain those of the chosen prereg.

Give the friend's account only curated source/test inputs and the exact artifacts for its task. The owned Intel can stage/send inputs and receive outputs; Drive credentials stay on owned devices. Prefer already verified public data/models or reviewed artifacts; no personal/config secrets or privileged whole-repo/home backup. Network loss preserves unreturned partial output as incomplete, and the task's return window must tolerate it. The owner can revoke access any time; stop/failure protocols preserve evidence without automatic repeated experiments. After the trial, return all required results to owned verified storage, revoke the narrow access and let the owner/operator approve exact workspace cleanup; no generic wipe or silent deletion. Reuse only if the measured time-to-useful-evidence, reliability and interference with the friend justify extending the loan.

Section check: approve the baseline-first, one-result initial trial, proposed one-week time box subject to the friend's actual offer, and conditional workload selection after the promised inventory?

## Discussion sequence still to complete

1. Intel availability and separate local working copies APPROVED.
2. Selective storage APPROVED; complete searchable library and controlled bulk retrieval APPROVED; backup schedule, retention and restoration still open.
3. Intel builder split and return handoffs APPROVED, with no local LLM runs on Intel; required M3 verification retained.
4. Intel research-engine hosting/independent local work with shared-disk transfer coordination APPROVED; MAESTRO must amend/re-review host spec.
5. Intel Drive uploads from verified local copies and phone/local dashboard views APPROVED; first-upload Intel route A APPROVED, subject to amended activation procedure/review.
6. Direct cable/independent internet and optional device-only private friend access APPROVED as design; no setup executed.
7. Friend local-model role APPROVED; inventory expected from operator within24 hours. Conditional one-week baseline/replication-first plan PROPOSED.
8. Risks, exact approval boundaries, staged acceptance and final review.

Each section will be saved and checked with the operator. Final approval is separate from installation, network access, credential provisioning, deletions or science-run authorization.

## Context rule for this session and successors

Watch Context N% left. Start a new piece of work only at >=60%. At <=40%, or any Context compacted, stop starting work; save design.md and decisions_log.md, write handoff.md here with done/open/single next step/exact paths, restate this rule, and report HW1 HANDOFF. Never push on through compaction.
