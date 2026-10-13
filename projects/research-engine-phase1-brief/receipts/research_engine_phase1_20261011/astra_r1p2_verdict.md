VERDICT: NO-GO

For closing R1/I1c, provisioning, or running the collector **as written**. Amendment 20 resolves the requested operator budget decision. It does not demonstrate fit within the new cap. The packet correctly preserves most blockers, but its collector and admission guards need corrections.

Aliases: `RE = results/research_engine_phase1_20261011`; `V = RE/astra_r1p_verdict.md`; `P = RE/intel_provisioning_freeze_v2.md`; `J = RE/intel_provisioning_manifest_v2.json`; `H = RE/r1b_host_commands.sh`; `D = results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md`.

Round-1 disposition:

| Item | Verdict → freeze | Round-2 disposition |
|---|---|---|
| F1 | V:7–17 → P:7–11,95–103 | **Open, correctly named:** selected candidate exists; complete lock does not. |
| F2 | V:19–21 → P:13–19,105–116 | **Open, correctly qualified:** retained-tar provenance and signature/content verification remain unobserved. |
| F3 | V:23–29 → P:21–60,118–122 | **Operator disposition closed; empirical admission open.** |
| F4 | V:31–35 → P:62–70,124–135 | **Open:** executable comparisons added, but incomplete and defective as described below. |
| F5 | V:37–46 → P:72–76,137–158 | **Open, correctly named:** improved predicates do not supply the reviewed implementation. |
| F6 | V:48–61 → P:78–89 | **Review-boundary clarification closed:** technical repinning remains conditional on compatibility review. |
| F7 | V:63–65 → P:91–103 | **Original “FROZEN” ambiguity substantially corrected;** remaining status/schema issues below. |
| R1 | V:69 → P:95–103 | **Open:** JSON structure delivered; identities, edges, variants and paths incomplete. |
| R2 | V:71 → P:105–116 | **Open:** collection procedure is not raw verified provenance. |
| R3 | V:73 → P:118–122 | **Open:** space/time evidence absent despite amended ceiling. |
| R4 | V:75 → P:124–135 | **Open:** route enforcement, source-image chain and complete comparisons unresolved. |
| R5 | V:77 → P:137–158 | **Open:** exact commissioning package, credentials, ownership and shutdown interfaces absent. |

The following findings concern round 2.

F1. [blocking] **The arithmetic is correct, but the peak table is conditional and not yet complete enough for admission.** Evidence: P:25–44; J:1360–1459; H:87–99; P:128–135.

The components total **1,991,764,570 bytes**, leaving **8,235,430 bytes**. The table explicitly includes compressed/extracted coexistence, an extra activation copy, source downloads/work/images, verification extraction, caches, retained failures, receipts and the **1.5.5** wheel. Those are appropriate categories.

However, the collector retains archives in mktemp, while the installation vectors do not specify how those exact files become MacPorts image/cache inputs without additional retained copies. The single-extra-copy allowance cannot simultaneously cover an activation payload and unspecified acquisition/cache duplication. **If** another complete compressed archive set coexists with the already-budgeted components, the peak becomes **2,247,128,811 bytes**, exceeding the cap by **247,128,811 bytes**. This is a conditional counterexample, not an observed MacPorts footprint.

Build-only closure, source workspace, three missing archives and actual image behavior remain unbounded. A measured tar-stream length also does not bound generated installation files by itself.

**Consequence:** Amendment 20 closes the old budget-choice request, not F3/R3 admission. Freeze an evidenced coexistence schedule and exact artifact handoff before claiming a conservative complete bound.

F2. [high] **The provisioning clock is clearly defined in prose but not enforced by the proposed next step.** Evidence: P:46–60,114–116; J:1461–1499; H:24–44,52–58,95–99,397.

The defined clock correctly begins before acquisition/staging writes and ends after durable setup checks; staged sessions and waiting do not reset it. The **870-second** total is explicitly an unmeasured schedule.

In contrast, H starts a fresh 900-second timer on every invocation. Its 600 MB staging check occurs **after** downloading, and a cached return bypasses that aggregate check. There is no cumulative-window controller in this packet. Timeout exceptions also bypass `run()`’s normal command-receipt persistence.

**Consequence:** do not begin the acquisition sequence without a cumulative controller, remaining-byte admission before writes, and durable failure/timeout receipts. The acknowledged future controller is a real prerequisite.

F3. [high] **The inventory is overbroad and cannot substantiate the promised bounded, complete baseline as written.** Evidence: H:32–37,67–73,118–162; P:101,114–116.

`inventory()` recursively records and hashes **all of `/private/tmp`**, including unrelated files and its own newly created receipts. It builds the full inventory in memory before applying the receipt-size limit. An unrelated socket or other unsupported file type triggers refusal; unrelated inaccessible or changing content can also terminate collection.

Direct collector writes are intended to remain under mktemp, and I found no dispatched install/build/service/cleanup command. That does **not** establish that every subprocess has no outside-write side effects; the script supplies no confinement or verified child write-root contract.

**Consequence:** replace the global temporary-directory walk with a scoped, bounded accounting strategy for admitted write roots. Separate baseline bytes from collector-created bytes, handle unrelated filesystem objects explicitly, and verify subprocess write behavior. This finding independently prevents blanket permission to run H as written.

F4. [high] **The admission guard does not implement the claimed refusal contract.** Evidence: P:64; H:301–328; J:1535–1548.

The recursive placeholder search includes **postinstallation observations** such as `postinstall.observed_active_ports`, as well as explanatory `BLOCKED:` strings. Thus even completed preinstallation evidence cannot pass without modifying fields that properly remain unavailable before installation.

Conversely, once placeholders are resolved, the observation checks lack structural validation: an empty `pools` list passes; negative/non-finite budget values are not rejected; writer flags use truthiness rather than requiring Boolean `true`; and projected peak is not reconciled with manifest components.

The postinstall comparison enumerates registered MacPorts contents, not all actual files in admitted installation roots. Extra unregistered files—including extras in Neo4j or the Python environment—are therefore not rejected by this function. Evidence: H:332–372.

**Consequence:** current refusal is not proof of a correct admission mechanism. Use phase-specific requirements, validated observation types, complete pool coverage and actual filesystem/distribution comparisons.

F5. [high] **Collector commands provide partial observations; they do not fill every missing identity their entries require.** Evidence: H:226–299,385–395; J:714–968,1047–1082,1210–1223.

- `archive-index` returns candidate filenames, not admitted URLs, sizes, hashes or signatures.
- `source-plan` records recipes/dependencies but explicitly leaves evaluated source inputs and build closure unresolved.
- Derived `inspect` modes return a parent archive inventory; they do not establish interpreter ABI/linkage or the installer’s exact interface.
- `apple-clt` inspection records a directory’s metadata, not compiler/SDK identities or a content digest.
- Archive collection can return `FETCHED-OBSERVATION` while signature verification remains pending.

These limits are largely acknowledged in P:116 and the builder report. They must remain explicit in the collection-to-admission workflow.

**Consequence:** freeze the remaining normalization and verification steps per entry. Successful collection must never promote the entire artifact to verified status.

F6. [medium] **JSON is the declared authority, but executable policy and artifact types still have competing representations.** Evidence: P:97,148,156; J:1354–1534; H:36,42,86,98,252–269,324.

The Markdown budget agrees numerically with JSON. However, H independently hardcodes the receipt limit, clock, staging limits, wheel version/platform selection and wheel allowances. Some policy—such as the exact HTTP predicate—exists only in Markdown while JSON’s command vectors remain unresolved.

The three R3 implementation/review entries are labelled `route: "source build"`, including the **review document** (J:1305–1350). These should be typed as supplied local artifacts with their own verification requirements. The verifier executable can be changed through `R1B_READ_PYTHON`, and wheel-lock resolution silently switches from a relative path to another path (H:12–15,256–258). The lock digest comparison protects content, but the selected path/provenance remains ambiguous.

**Consequence:** make operative limits and predicates manifest-driven or mechanically assert equality; distinguish acquisition, build, directory and review-artifact types; pin the collector toolchain and resolve paths explicitly. No automatic package/version fallback was found.

F7. [high] **Compatibility and commissioning remain genuine blockers, correctly disclosed.** Evidence: P:74–89,139–158; J:1507–1533.

The proposed niceness calculation preserves inherited priority, and shutdown now targets the console-owned instance. Those are improvements. They do not establish the LTS-specific interfaces, protected credential channel, reviewed ownership oracle, external stop behavior, precise shutdown predicate or no-resume window.

**Consequence:** keep R5 and native acceptance open. Python 3.12.15/LTS/wheel selection can proceed through technical review without reopening an unchanged operator preference.

Required changes:

R1. **Repair and narrowly re-review the collector before execution.** Address F2/F3, freeze the exact allowed modes and collector toolchain, and retain timeout/error evidence. Do not run installation vectors, `-s install`, sync/selfupdate, cleanup, commissioning or R3 execution as part of collection.

R2. **Complete the lock through explicit collection and admission steps.** Obtain raw tar/key/signature receipts, verify effective content and trust method, resolve all runtime/build edges and artifacts, and bind each promoted identity to its receipt. Preserve non-fetchable gaps as such.

R3. **Obtain source-build evidence with one bounded Intel feasibility trial before touching the real prefix.** The smallest useful trial is the five admitted source ports, serially, using the pinned recipes, patches, prerequisite closure, compiler/SDK and flags. Keep work, caches, destination staging and receipts in one named scratch area; build through staged payload/image creation without registration or activation in the real prefix. Record cumulative elapsed time, peak logical/allocated growth, retained failures and output identities; verify the real prefix remained unchanged.

A generic upstream build under a different prefix is insufficient unless its differences from the actual MacPorts route are accounted for. Freeze and verify the staging interface first.

**For this packet, obtain explicit authorization for that trial.** J:12–15 denies staging/build authority, and Amendment 20 does not authorize a separate uncounted rehearsal. An additional trial budget, retained duplicate copy, or exclusion from the 900-second clock requires operator disposition. MAESTRO may dispatch within an already explicit authorization, but none is supplied here. This is a concrete bounded-write decision, not another vote on package preference.

R4. **Repair phase-specific admission and postinstall verification**, then freeze the exact archive handoff, prerequisite order and build-to-activation identity chain. Recompute space/time from that executable route.

R5. **Supply and bind the reviewed commissioning package**, including LTS compatibility, exact commands, credentials, ownership, deadlines and shutdown/no-resume predicates.

NEXT STEP ALLOWED: no — run r1b_host_commands.sh as written

**What I checked and did not check**

I read the prior verdict, all four subject artifacts, Amendment 20 and relevant surrounding authority, measurements/runtime closure, facts, retained-tree receipt, v1 requirements and DuckDB lock receipt. Local read-only parsing confirmed 48 entries, matching measured archive sizes, the budget/time sums and the lock digest. All three supplied subject hashes matched before and after review; HEAD remained `62dbbe0c851ee65c08e0dc9f2c17d16439fce28a`.

The manifest contains **five full `expected_sha256` values**, plus two full Portfile hashes—not just one full hash.

I did not execute H, fetch anything, access Intel, build/install, run behavioral tests, start services, use graft or write files. Findings about execution follow from static inspection; host behavior remains unverified. The excluded workstreams were not reviewed.