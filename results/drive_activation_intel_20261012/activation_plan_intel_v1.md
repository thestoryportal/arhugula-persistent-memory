# Intel-first Drive activation plan v1 — DA1

## DA1 work log — acceptance checklist

- [x] v1 and every existing file unchanged by DA1; only O1/O2 created, no commit.
- [x] O1/O2 exist within their line caps: O1 153 lines; O2 count at the end.
- [x] O1 has no old-freeze citation outside its changes list.
- [x] L1–L4 and A1–A8 implemented and mapped to output lines.
- [x] Every repo/record factual claim has file:line evidence.
- [x] Every unrecorded number is PROPOSED with a reason; no new numerical transfer limits.

Status: PROPOSED, UNEXECUTED; for Astra review, then the three operator choices, then a separate operator go. Adoption alone switches nothing on (B/r2_redesign_operator_adoption.md:9–11). All future measurements, host checks, commissioning and transfers below remain UNRUN; this document is not an executable command sheet.

Aliases: B = results/compute_storage_brainstorm_20261011T054507Z; P = results/backup_gdrive_host_20261011/r13_package_20261011T032105Z; V4 = B/r2_git_drive_redesign_v4.md; AP = P/activation_plan_v4.md; L = B/drive_intel_dedup_layout_v2.md; IM = B/integration_r5_completion_table.md. File:line ranges refer to current repository bytes.

Authority: adopted V4 governs every conflict, including obsolete Intel-pull/shared-clearance text in design/IM. Preserve recorded choices and evidence; this is infrastructure protection, not science acceptance (B/r2_redesign_operator_adoption.md:1–11; V4:5,100–116). O1 preserves the content-once layout; its changes map covers L1–L4 (L:145–153).

## Gates in order — no execution before the separate go

Gate REVIEW: MAESTRO sends both DA1 files to Astra; any NO-GO or unmet condition holds activation. The reviewed implementation packet must bind exact input/policy/release hashes, allowed paths, owners, executable arguments, Intel host dependencies, resource limits and acceptance receipts; no old M3 host receipt qualifies Intel (V4:23–25,110–116; B/design.md:263,281; AP:31–48).

Test: missing review, stale pins, unnamed owner, unresolved condition or unqualified native/probe/resource bound refuses execution.

Gate CHOICES: after permitting Astra review, record exactly the three choices below against these source/capture/upload semantics; earlier direction/retention/cap answers stand (B/r2_redesign_operator_adoption.md:11; V4:89–99,124–130).

Test: any missing choice or failure to restate Intel physical-access exposure keeps commissioning closed.

Gate GO: obtain a separate explicit operator go for the concrete reviewed bounded commissioning packet. No host inventory, login provisioning, push, upload, permission click, bootstrap or restore test runs before that go; marked actions in AP retain their point-of-effect permissions, which the new go must expressly cover (B/r2_redesign_operator_adoption.md:11; V4:116; AP:499).

Test: a review/adoption/choice answer alone cannot start any action; an uncovered permission/action refuses.

Gate COMMISSION: execute the reviewed steps separately, inspect each receipt and stop at first failure; no pasted document or uncontrolled batch. Commission only the approved route before enabling its steady service (V4:17,25,69,81,116; AP:11,27,399–448).

Test: an action without its predecessor PASS/receipt refuses; fixture/local proof cannot replace native Intel, M3-boundary or Drive evidence (AP:3,44–46; V4:69).

## Three deferred operator questions

1. **Recommended: Yes, only the approved backup files.** May the Intel Mac have a Google Drive login that can upload and read those files, knowing its disk is unencrypted and it signs in automatically, so anyone holding it can reach that login? This lets it do the backup work while making the physical-access risk clear (V4:79,126–128; B/decisions_log.md:197,216).
2. **Recommended: Yes.** May we check every uploaded file in full and agree when the selected files must stay unchanged while the M3 copies them to the Intel, with science taking priority if it needs to write? This catches incomplete or disturbed copies, and the later Intel upload can run while the M3 does science (V4:24,76,129; B/integration_plan.md:24).
3. **Recommended: Fresh history (PROPOSED).** Should we start a new backup history while keeping the old copies and checking existing backup records, or continue an existing history after its files have been checked? Starting fresh avoids relying on an unqualified old copy, and removes nothing (V4:130; AP:217–250,477).

## Source definition and inventory before selection

Intel-first is already approved by HW choice 11; M3-first requires a future amendment, outside this plan (B/design.md:273; B/integration_plan.md:24; B/decisions_log.md:139).

Base full-backup root is exactly /Volumes/memit/llm-database-poc-mirror/ on M3. Keep the reviewed AP exclusions plus its temporary Git-object exclusions and symlink policy, then close the credential gap before inventory/hash/copy; every .hf_token, credential-bearing config/payload and uncertain opaque archive/Git object is excluded or blocks classification. Do not silently shrink other admitted paths (AP:20–21,335,339–340; B/drive_intel_fit_facts.md:19–22,205; L:28,43–49).

Historical top-level coverage includes workspace/, stage_2_sweep/, stage_1_sect/, hf_cache/, stage_1_sect_S215D2/, arhugula-persistent-memory/, covariance_caches/, memit_dry_run/, stage_1_sect_d3/ and the other admitted entries. The exact current full path list, secret-free count/bytes, source identities, metadata, holds and content digests remain UNMEASURED for activation (B/drive_intel_fit_facts.md:38–50; L:32–49).

Additional inventory candidates are /Users/robertrhu/Backups/memit, /Users/robertrhu/Backups/memit_offload and all selected entries under /Users/robertrhu/Backups, plus NEW-1 leftovers. Distinguish canonical live/external files, old internal mirror versions, unique internal offloads and held artifacts. Exact current NEW-1 paths, identities, holds and sizes must be supplied by the inventory owner; no dated queue size supplies a manifest (B/design.md:275–277; B/drive_intel_fit_facts.md:13,117–132; B/integration_plan.md:25; IM:101; V4:113).

The dated parked 268.5 GiB represented ~/Backups, principally the old mirror, not an extra disjoint output set; path+size overlap is not content identity. Mirror-only versions and .deleted/ history remain separate preserved candidates. No live sum or free-space credit can use those historical observations (B/drive_intel_fit_facts.md:117–132,207; B/integration_plan.md:25).

PROPOSED inventory receipt per path: root/device/host, literal relative path/kind/link target, source version/run/Git identity, logical and allocated size, full content digest for admitted non-secret payload, hold/retention decision, overlap/object identity, inclusion/exclusion-policy identity and required remote locator. Independently enumerate the selected population; compare complete manifest path sets and preserve distinct versions (L:28–49; V4:76–78; B/integration_plan.md:25).

Historical baseline is 40,543 files / 287,177,060,251 B, with 156,979,390,913 B confirmed duplicate payload and ≤130,197,669,338 B unique upper bound; small unhashed files were counted as unique. These dated, uncorrected figures are neither exact activation totals nor current free-space receipts (B/drive_intel_fit_facts.md:14–15,21,105–106; L:49,91–102).

MAESTRO owns source selection/accepted Git publication; the inventory, M3-push and Intel-upload implementation owners and exact permitted destinations must be frozen in the permitting packet. Post-activation parked/NEW-1 archival work keeps its separate scope/dependency; this inventory does not authorize its upload or removal (B/design.md:277; IM:98–102; V4:77,105,110,113).

Test: missing exact path/hold/classification, credential uncertainty, unexplained overlap, name+size-only reuse, missing manifest entry or silently omitted admitted path refuses capture. Compare independent enumerations and hashes; no source/old-copy deletion or transfer occurs in the inventory step (L:43–49,102,126; B/integration_plan.md:25).

## Route, overlap and source consistency

M3 reads original selected sources only in admitted maintenance windows and initiates the cable connection; bytes land directly in L's Intel-local incoming/<attempt>/, then immutable objects/aliases/manifests. Intel uploads from the complete Git-bound sealed checkpoint. Intel never initiates a read from M3 or retains a login/share/mount/proxy/forwarding route to memit, even during push; research acquisition remains pinned Git and verified Drive (V4:11–17,73–78; L:9–26,57–60,79–81).

Keep tools/c10w_p2_gate.py check_gpu and science admission/exemptions unchanged. Failed/empty/unavailable observation blocks or stops M3 enumeration/hash/push/source verification; science has priority and never waits for native copy completion. Intel-local upload/retry/readback can continue during M3 science (V4:21–25,53–54).

The implementation must use qualified non-Python copy/hash executables and actual helpers, bounded resource use, no long-lived Python watcher. Bound maintenance probe execution/teardown through a non-Python supervisor; pending science closes probe admission, terminates/reaps in-flight probe/helper Python before science's unchanged gate, and excludes new probes throughout admission/execution. Freeze justified bounds in the reviewed packet; short probes/retries are not proof (V4:23–25).

Source stability covers independent enumeration, hashing, push and successful Intel capture verification; an independently reviewed immutable snapshot may replace the writer pause only with its peak cost reserved. Freeze names/PIDs/service IDs of included producers with actual owners; unknown/uncontrolled writers refuse a coherent cutoff. The old M3 plan's all-source pause through slow remote checking is REPLACED by a capture-only stability window plus Intel immutability; no restart/logout is needed (V4:24,76,110; AP:314–325; L:57–62).

If science needs to write, abandon capture, release the freeze, label the attempt incomplete and retain/charge partials. Later recopy must independently establish a coherent source cutoff; hashes matching a moving manifest alone are insufficient. Stable captures are immutable versions; later source writes never mutate a checkpoint or qualify as protected through an older receipt (V4:24–25,76–78).

Test: no memit reads under observed science/non-exempt builder Python or failed observation; racing science dispatch cancels/cleans probes without refusal/starvation, and native push stops without delaying science. Stuck probes/helpers fail closed. Intel reverse-route attempts fail before bytes/handles return, including during push (V4:17,25).

Test: change/add/remove a selected source during capture or interrupt the cable: no checkpoint/Drive acceptance; partials charged, freeze released for science, later stable recopy independently verifies. Intel-local upload during M3 science performs no M3/memit reads (V4:25,76,81).

Deletion, destructive cleanup and science-visible retrieval/publication remain OFF; gate/hold checks or a deletion approval cannot replace separately reviewed exclusion/disjoint-path protection that works under missed activity/racing starts (V4:22–25,29,56–57).

## Capacity, batches and schedule

Approved Intel ceilings are decimal GB: current recovery 250; additional unique history 50; builders/tools 40; analysis/transfer 50; pilot/setup 7; at least 80 free. Intel's recorded SSD is 512 GB; current formatted capacity/use/free bytes, reservations and Drive quota remain UNMEASURED here. Older I3/design numbers are superseded by amendments 16/20, not new quotas (V4:75; B/decisions_log.md:189–191,222–228; B/integration_plan.md:25).

The first checkpoint uses content-once recovery storage, within 250 GB, including metadata, actual allocations, aliases, temp, retained partials and concurrent/future commitments. Do not borrow the separate 50 GB allowance, create a second full tree or treat dedup headroom as measured free space. Remote uploads still include every admitted path, not merely unique local bytes (V4:74–75,80; L:87–104; B/decisions_log.md:234–238).

PROPOSED bounds use current unique payload U plus measured/bounded metadata M and temp/partials T; require U+M+T ≤250 GB and independently verify actual allocated bytes/reservations/free floor on Intel's physical pool. L's one incoming object at a time and historical largest 6,178,316,608 B file are planning inputs; neither bounds future files or retained attempts without measurement (L:95–100; B/drive_intel_fit_facts.md:172).

PROPOSED bounded capture batches contain exact manifest-listed objects with justified byte/count/resource/retry ceilings chosen after corrected inventory. Reserve each batch's growth and retained partials; accumulate sealed objects without deleting earlier ones. The whole selected checkpoint must exist/verify on Intel before first internet upload. Batching cannot turn a partial checkpoint into full-backup acceptance (V4:53–54,73–76; L:53,100; B/integration_plan.md:25).

If current inventory exceeds available recovery staging, first try reviewed content reuse and bounded capture batches that still accumulate within the cap. If the whole checkpoint cannot fit, the push waits with a named deficit; preserve full-backup scope until a separately reviewed source-selection/storage amendment. Do not cycle batches by deleting, stage on memit, use M3 internal bulk scratch, grow caps or count proposed removals as space. Subsequent archive batches must also fit their separately permitted area with all retained prior bytes (V4:50–54,74–75,113; B/integration_plan.md:25; L:53,104).

On M3, preserve S1–S12: qualify aggregate peak P and support O within a frozen envelope; atomically reserve against actual device free F and remaining reservations R, requiring F≥P+O+R+20 GiB and F−P−O−R≥100 GiB. Warning below 80 GiB is not deletion authority. Retained commitments/reallocations stay charged until reconciliation; other writers cannot consume science reserves (V4:33–69).

Measure cable throughput and Intel upload/readback throughput under approved bandwidth, using actual quota/current population/retained history to forecast earliest protection. Preserve daylight 08:00–23:00 at 512 KiB/s; AP's 1.16 MB/s nighttime speed and multi-day estimates are historical assumptions, not a new unlimited-rate grant or deadline. Inspect effective wrapper limits on Intel; unknown bandwidth/quota holds reliance (AP:273,383; V4:62–63).

Preserve accepted-update records, nightly finished bulk when science permits, and earlier protection when required by an irreplaceable run; no continuous live-source consistency assumption. Forecast queue peaks/offload needs before admission and display the earliest deficit; a running science job never waits for a copy (B/decisions_log.md:81; V4:50–54,62–63).

Test: usage above an approved ceiling refuses; usage equal to the ceiling satisfies only that criterion. Available space below the required free floor or reservation-plus-peak/headroom bound refuses; equality satisfies only that criterion with other gates met. With all other gates met, an admissible bounded positive control below the usage ceiling and at or above the required free/reservation bounds must admit and complete, so an always-refusing implementation fails. Concurrent requests, retained retries, temporary allocate/free/reallocate and unknown measurements must not double-spend; out-of-envelope work refuses, and low space waits with no deletion/memit staging (L:97; V4:36,39,42,45,51,63,75,81).

Test: inventory too large for a whole checkpoint cannot trigger upload of the first batch; changing bandwidth guesses or treating old free-space observations as live capacity cannot unblock the dependent queue. Bounded maximum/failure controls must substantiate prevention, not just alarms (L:53; V4:63,68–69).

## Section-by-section disposition of the M3 plan

These are replacements for the Intel route requiring Astra review and host evidence; no AP command/path/PID/pin is blindly transplanted (B/integration_plan.md:24; V4:110; B/design.md:263).

| AP section / lines | Disposition and Intel acceptance |
|---|---|
| Opening order/declarations/capture, AP:3–27 | PRESERVED: distinct GO/STOP order, no guessed numeric values, individual rows, actual child exit and complete append-only captures. REPLACED: W/M/D/SRC/DST/R and fixed executable paths with reviewed Intel release/checkpoint/receipt locations (V4:15–17,73–79,110). |
| §0 preconditions, AP:29–68 | PRESERVED: pins/re-review, exact scope, fresh inventory and orphan/permission/quota checks, and every mandatory behavioral requirement of AP:44–46 in the Intel coverage matrix below. Historical r11/r13 receipts do not satisfy new Intel coverage. REPLACED: M3 disk IDs/fixture PIDs/runtime placement/Homebrew paths by explicitly reviewed Intel bindings or per-case replacements; compatibility/process evidence alone cannot replace coverage (V4:17,23–25,75,99,110; AP:44–46). |
| §1 merge/release/bundle/receipt, AP:70–213 | PRESERVED: MAESTRO-only gated release, exact reviewed index/commit/head/tree binding, immutable outside-checkout deployment, full bundle/source/population hashes, original preserved receipt (AP:72–74,96,126–161,168–208). REPLACED: M3 user/release/app source binding and executable paths with Intel source adapter/release, reviewed and re-pinned (V4:73–79,110). No DA1 commit/merge/deployment. |
| §2 history/recovery, AP:215–258 | PRESERVED: complete history scan, no guessed floor, under-lock preservation, barrier followed by observed successor; recovery for ordering damage, not retry (AP:217–252). REPLACED: M3 HOME/baseline by Intel namespace/full history inventory and selected history branch (V4:110,124–130). Empty M3 history does not prove empty Intel history. |
| §3 launch/Allow/progress/completion, AP:260–312 | PRESERVED: wakefulness/AC, real permissions, actual owner/child progress, sequenced clean receipt/heartbeat/status and diagnosed successor retry. REPLACED: mounted memit source and M3 app permission by Intel sealed source and Intel-local app/login checks (V4:22,73–79,110). M3 memit permission is inapplicable on Intel. |
| §3.5 pause/catch-up/full check, AP:314–397 | PRESERVED: no changed-file waiver, catch-up, complete population/error reports and recorded final inventory. REPLACED: M3 live pause through remote check by coherent M3 capture-only window plus immutable Intel source, cutoff-labelled convergence and full Drive readback (V4:24,76–81,110). PRESERVED: successful hash-pinned deployed status and preflight, both exit 0 before content checking, plus rejection of inherited behavior-changing RCLONE_* and config overrides before any transfer/check consumption (AP:335). AP checksum check may supplement; full download/readback is required here. |
| §4 install/bootstrap/successor, AP:399–448 | PRESERVED: pinned copy/lint, enable/load proof, no overlapping launch, actual successor and fresh completion. REPLACED: M3 LaunchAgent/app/path identity by Intel-native reviewed deployment on Intel's login account (V4:75,79,99,110). Recorded interval 21600 seconds, RunAtLoad=false and Nice=5 remain policy inputs to the host review (AP:412–427); not permission to install unchanged M3 plist. |
| §5 retirement, AP:450–482 | INAPPLICABLE to this activation scope: old-job bootout/disable, plist move and old-copy removal remain OFF. PRESERVED as future prerequisites only: clean content/catch-up/scheduled evidence, ancestry checks, separate exact-path permission and protection (AP:452–477; V4:22–25,56–60,110,113). |
| STOP/preservation, AP:484–499 | PRESERVED in full below; REPLACED M3 identities and live-source pause with Intel identity/coherent checkpoint and v4 science-priority route (V4:17,22–25,75–81,110). |
| r12 erratum, AP:501–519 | INAPPLICABLE as an Intel executable/pin set; PRESERVED unchanged as lineage. Current full coverage/error/log-format requirements remain, with reviewed Intel command vectors (AP:46,335–383; V4:110). |

### Mandatory Intel coverage matrix — required before any upload

Preserve these behavioral requirements independently of old host receipts. Freeze the exact inherited test IDs/assertions from the reviewed inputs; for each case needing an Intel adaptation, require Astra's permitting replacement record naming the original case, Intel test/command and pinned inputs, expected result, permitted skips, isolation/placement and descendant-clearance receipt. No generic host-compatibility waiver or case omission; until the mapping and fresh Intel receipts satisfy this matrix, upload stays blocked (AP:44–46; P/run_py39_coverage.py:26–36,239–242; V4:110).

| Mandatory coverage / source | Intel expected result and permitted skips |
|---|---|
| Exact 22-case run; AP:44; P/run_py39_coverage.py:26–36,239–242 | 22 pass; no skips/failures/errors. Preserve every selected BackupTest, HeartbeatTest and LauncherTest case/assertion, or bind its explicit Astra-reviewed Intel replacement with equivalent expected behavior. The frozen full suite cannot substitute for this run. |
| E RED / E GREEN native assertions; AP:44 | RED must be the two absent-parent UNSET subcases; GREEN includes actual native fixture artifact assertions. No skipped native execution/artifact assertion counts as GREEN; each affected case requires its permitting replacement record. |
| Local-to-local same_size_corruption; AP:44–46; P/run_local_check.py:51–75 | Verifier FAIL with alpha.txt among failed objects; retain actual check exit/log/reports. The negative result is fixture success only when the recorded failure is correct; no skip. |
| Local-to-local excluded_only; AP:44–46; P/run_local_check.py:51–75 | Verifier PASS despite changed excluded .cache content, with complete admitted coverage; no skip. |
| Local-to-local symlink; AP:44–46; P/run_local_check.py:51–75 | Verifier PASS using identical reviewed link representation/filters; no skip. |
| Local-to-local clean; AP:44–46; P/run_local_check.py:51–75 | Verifier PASS with complete matching coverage; no skip. Re-run all four fixtures using the new pinned verifier and templates. |
| Isolated config, runtime and placement controls; AP:44–46; P/run_py39_coverage.py:181–201 | Fresh isolated HOME/fixtures/TMPDIR outside the science source; live config path confined there and listremotes empty; preserve real config/placement positive controls, not replay. Fresh df-P mount and diskutil APFSPhysicalStores evidence must prove disjoint physical whole disks; shared/unknown identity refuses. Intel topology/bindings need a permitting per-case replacement if the inherited control cannot run without violating v4's no-memit boundary; no assumption or waiver. |
| Frozen suite; AP:44 | 155 run, 14 real-rclone skips, zero failures/errors and cleared groups; preserve the exact recorded skip identities/reasons. Its five skipped Archive cases remain UNVERIFIED/nondependencies; no additional skip or changed expectation without a permitting per-case replacement. |
| Native environment, inventories and owned descendants; AP:44–46 | Host reruns at niceness 0, fresh Intel labels, original packages/receipts preserved read-only, real before/after inventories identical, no owned process groups/descendants left. Capture actual owner/child/group evidence after every run; unavailable observation or surviving descendant refuses all coverage acceptance. No stale M3 PID/topology substitutions. |
| Check log/template/verifier controls; AP:46 | Pin date,time format; unsupported severity records (microseconds, time-only, prefixes, JSON) reject; valid DEBUG argv references to report --error/error.txt remain harmless while actual read/error/unchecked/report failures remain fatal. Preserve raw logs; no skip. |

Test: before any upload, fresh Intel receipts must satisfy every row of the mandatory coverage matrix and its pinned per-case mapping; each AP section still has a disposition/source and actual Intel host bindings. A historical M3 PASS, generic compatibility evidence, stale fixed PID, skipped native assertion or unreviewed/missing replacement cannot qualify it (AP:3,44–46; B/design.md:263).

## Receipt, history and generation contract

PROPOSED fresh Intel receipt labels exclusively create a separate budgeted control directory outside included/sealed sources. Save host/boot/login/time, command argv/env policy, cwd, complete stdout/stderr, actual exit, source/checkpoint/release/policy identities, all raw logs/reports and their hashes; validate each call before downstream extraction. Preserve every failed/default check, old pin set and original receipt (AP:11,27,31,48,208,362,486; V4:77).

Pin deployed status/wrapper/release bytes immediately before use; preserve/hash mutable counter observations rather than freezing the counter. Inspect all live/preserved/issued history, journals, heartbeats, ownership locks, refusals, temporaries and scanner maxima under the reviewed lock contract. Lost/off-disk history ambiguity cannot mean zero; fresh history means a separate reviewed namespace with old evidence intact, not reset or discard. Any bootstrap/no-lost-history assertion belongs to the third choice's recorded disposition; if absent or ambiguous, refuse that branch (AP:217–239,486–491; V4:130).

Retain B=max(H,F)+1 for a reviewed recovery barrier using observed maximum H and approved floor F; barrier status must be nonhealthy until a sequenced completion above B. Never guess a generation/floor or raise a floor to hide a refusal; status exit 0 before acknowledgment is false green (AP:225–252,488–491).

Before each launch save counter G; expected launch is observed successor G+1. Distinguish wrapper launch ordering from content-manifest source generation. Require matching applet-mode receipt, clean heartbeat, counter/unresolved/journal evidence and release/source/destination identity; observed successor receipt exit_code=0/error_number=null, heartbeat end set, exit_code=0/rclone_exit_code=0/warnings=[], unresolved empty, no later issue/failure evidence, no lock or surviving transfer (AP:262,280–299,436; V4:77).

Inspect status strictly before completion end+13 h, never start+13 h; open/launchd exit alone is insufficient. Long upload progress is independently evidenced by dated advancing bytes/files, actual owner/child ancestry, logs and active AC wake assertions; a barrier-related nonhealthy status neither proves progress nor fails a healthy owner by itself (AP:273–299).

Recovery is only for damaged ordering history. A cleanly terminated transfer failure retains all evidence; only diagnosed actual-owner/operator-approved successor launch can retry the same immutable source. Changed source needs a new manifest/namespace. Preserve lock before any separately authorized clearance; no timer expiration, counter repair or silent automatic retry (AP:312,486–492; V4:76–77).

Test: lost-history ambiguity, malformed/duplicate-key state, floor below observed maximum, exhausted ordering space, altered recovery archive, false barrier green, guessed successor, later unresolved issue, stale status or warnings prevents acceptance. Under-lock refusal leaves old bytes unchanged (AP:225–252,299,488–495).

## Intel host/login/app and transport commissioning

Record actual Intel host identity, OS/architecture, user/login session, physical filesystem/capacity and executable paths/versions; use the approved MacPorts channel and real compatibility/pins rather than /opt/homebrew paths or copied M3 environments. Qualification must bind wrapper/status/app/builder/stage/plist/source adapter and their helpers to the reviewed commit/bundle; unsupported paths/versions refuse (B/decisions_log.md:204–210; B/design.md:263; AP:31–48,161–206; V4:99,110).

Provision Drive login only on the operator-owned Intel, outside packages/manifests/receipts that could carry secrets. Restate FileVault off/automatic login and selected approved-file scope; demonstrate actual existing approved objects and newly Intel-uploaded objects are visible/readable under that login. Remote name, drive.file label or another token does not prove access. Unexpected destination data, auth/quota errors or inaccessible approved files STOP (B/decisions_log.md:197,216; V4:79; AP:64–68).

Build/inspect a fresh immutable Intel app outside checkouts, preserve source/decompile/bundle manifests, validate configured sealed source and remote namespace. Intel uploader can read/search but cannot change protected objects/manifests/aliases; mutable retry/log/state directories are separately charged. Same-size mutation/protection/inode drift prevents consumption/acceptance (L:20–26,79–81; AP:168–206; V4:74,110).

Grant required macOS app/file permissions physically at Intel under the go; verify actual wrapper/child start and exact login session. AP's M3 Removable Volumes Allow is inapplicable because Intel never mounts memit. A missing prompt with no start, denial, app without child, unavailable ps or wake assertion failure STOP (AP:280–297,493,497; V4:15–17,110).

Test: denied login/app permissions, wrong release/source/destination, secret transport, missing approved old/new Drive visibility, attempted alias write or uninspectable host/process state refuse without M3 fallback. Observe actual active AC wake assertions throughout Intel upload/check, and no M3/memit read by Intel (AP:46,280–297,348–373; V4:17,79–81).

Test: at both hosts inspect credentials/exports/mounts/autostarts and exercise attempted M3 login/share/proxy/symlink/forwarding/reverse requests while the permitted push is active; all refuse before source bytes/handles return. Configuration transition requires revalidation; no M3 restart/logout is an activation prerequisite (V4:15–17,24,65–66).

## Initial upload, final catch-up and full readback

First internet upload refuses until the entire corrected selected checkpoint is complete, independently verified, protected and Git-bound. Upload every manifest path from Intel read-only; preserve literal path/kind/link representation and directory metadata through the reviewed source adapter. Do not upload internal content-store names as the backup's path population (L:28,43–45,53,79–83; V4:73–80).

PROPOSED use a versioned remote population bound to the immutable source manifest; actual approved Drive locator/history behavior is frozen in the implementation packet. Existing root record is gdrive:memit-backup/, with 5 TiB/about 4.9 TiB free dated 2026-10-10, not present quota acceptance. No destructive sync/delete/archive side effect is enabled; destination-only protected history is preserved, and any change to those effects needs review/authority (V4:56–60,79–80,110; AP:335; B/design.md:265).

A clean initial launch completion establishes transfer ordering/health only. Then final catch-up captures all admitted changes since the first cutoff into a newer coherent Intel checkpoint during another source-stability maintenance window, reusing protected unchanged objects within caps. Its clean observed-successor upload and remote check are mandatory; changed files receive no waiver (AP:299,314–325; V4:24,76–81,110).

Convergence is explicitly at the final admitted source cutoff and complete credential-free path/metadata population. M3 may resume writes after successful Intel capture verification; Intel then uploads/readbacks without M3 pause. Post-cutoff writes create a newer frontier and show BEHIND, never a claim that current live M3 is fully protected. If no coherent catch-up window/complete checkpoint fits, activation remains OPEN; neither science wait nor silent narrower scope resolves it (B/design.md:259,284; V4:24,76–78,110).

Full Drive acceptance requires every admitted path's entire remote content read back on Intel and size/digest checked against that immutable manifest, plus path/kind/metadata coverage and required representation checks. Stream readback without a second bulk verification tree; any temp buffers/files stay bounded and charged. AP's comparable-hash check can supplement, but cannot replace full readback. Missing checksum invokes full-population download semantics; even with hashes present this plan requires whole-content readback (V4:60,76,110; AP:335–383; L:26,79–83).

Before each content check, verify deployed status-tool bytes against the reviewed pin and require successful status and source/destination preflight captures, both exit 0. Reject inherited behavior-changing RCLONE_* environment settings and config overrides before any transfer or check consumption; the expected bootstrap barrier state does not waive runtime-configuration rejection (AP:335; AP:252). Keep identical inclusion/exclusion/link policy across source adapter, inventory, upload and remote verification. Preserve inventory exits, raw full-population combined/differ/missing/error reports, exact date,time DEBUG log format and terminal counts; zero missing/differing/unreadable/error/unchecked entries and complete nonduplicated coverage are mandatory. Failed checksum/default verdicts remain; download is no waiver for discrepancies or errors (AP:46,335–383).

Recheck sealed Intel manifest/objects/protections and before/after metadata/path population; mutation invalidates the generation. Record final cutoff, population count/bytes, source and launch generations separately, release/policy pins, full readback receipt, remote locator/version, last verified time, coverage/omissions and hashes; MAESTRO publishes accepted credential-free receipts in Git (AP:385–397; V4:60,76–78; L:26,45).

Freshness uses exactly MEMIT_ONLY; PUSHING/INCOMPLETE; STAGED_ON_INTEL; UPLOADING/INCOMPLETE; VERIFIED_AT_GENERATION; BEHIND; UNKNOWN. Both phone/local views show requested/current Git generation, M3 frontier, staging state, verified Drive cutoff/age and incomplete/unpublished coverage. STAGED_ON_INTEL cannot qualify remote protection or Git/Drive-only research acquisition; unknown current frontier is UNKNOWN (V4:78,93,112; L:80).

Test: in isolated controls inject an inherited behavior-changing RCLONE_* setting and a config override; each must be rejected before a transfer/check child consumes source or remote content, with no transfer/check start and preserved refusal evidence. Wrong deployed status pin, nonzero status/preflight or uninspectable effective configuration also refuses; the reviewed clean environment/configuration must pass preflight with both exits 0 before checking (AP:335). Remote altered/missing/partial bytes, incomplete/duplicated/truncated/unhashed reports, log error, failed exit/verifier, link/path/metadata mismatch or source-adapter drift refuses VERIFIED. A newer M3 source marks the older remote population BEHIND without altering it; staged-only data cannot satisfy a request for newest verified Drive bulk (V4:60,78,81; AP:362–397).

Test: final catch-up misses a changed/added/removed admitted path, lacks coherent cutoff or has warnings: activation stays OPEN until a later complete clean capture/upload/readback; no timestamp waiver. Independent remote-read receipt must cover every selected path, not a sample or size-only comparison (AP:314–397; V4:76–81).

## Scheduled successor, retention and operations kept off

Only after successful bounded first/catch-up/readback commissioning, and with go expressly covering installation, install the reviewed Intel plist by pinned copy/lint, enable/bootstrap and inspect actual enabled/loaded state. Preserve recorded RunAtLoad=false, interval 21600 seconds and Nice=5; validate real Intel program/app paths and session. No unexpected target overwrite or overlapping transfer (AP:399–429; V4:110,116).

Save actual prelaunch counter; exercise the scheduled path under the authorized kickstart and require observed successor, job-run increase, clean sequenced completion/status/unresolved state, no owner lock/surviving child and complete raw job/log receipts. Immediate kickstart proof remains distinct from a naturally timed run; loading/login alone is no health proof (AP:412–448).

Preserve seven daily/four weekly Intel restore points and exact retained versions within 50 GB additional unique-history cap. Show overflow/backup age/omissions, retain earlier points; no silent trim or unreviewed remote version policy. Fresh wrapper history is distinct from content-once recovery history. Required known-file/old-version restore checks use a separate approved destination/brief; recovery capability is not prerequisite to first upload and is not waived (V4:91,111; B/decisions_log.md:101,191; L:104,108–116).

Old mirror/job/app/plist retirement remains OFF, including bootout, disable, move and deletion. AP convergence/content/scheduled receipts remain necessary for any future retirement proposal; exact identities/holds/allocated size/method, separate operator approval and applicable missed-activity-safe protection remain due. No completed backup receipt grants removal (AP:450–482; V4:22–25,56–60,110,113).

Drive-to-memit retrieval/restoration and science-visible publication remain OFF pending their separately reviewed exclusion/disjoint-path protection. Intel research retrieval is separately scoped to exact verified Drive objects and permitted local storage; no route to M3/memit. Preserved local recovery tests grant no live restore or science-baseline acceptance (V4:13,22–25,91,111; L:108–116).

Test: bad plist pin/path/session, disabled service, unexpected launch, missing successor, nonclean/stale completion or unexplained scheduled log prevents service acceptance; changed protected bytes refuse the next run (AP:410–448; L:26).

Test: history overflow retains existing versions and reports deficit; a verified Drive object, expired retention or low-space warning cannot trigger retirement/deletion/retrieval into memit. Known-file/old-version restore checks remain visibly OPEN until separately authorized receipts exist (V4:57,91,111; AP:477).

## STOP and preservation rules — carried from AP:484–499

At every STOP preserve original bytes and names, full histories/locks/refusals, complete raw stdout/stderr/exits/logs/reports/process/wake evidence and hashes in fresh budgeted labels; never edit/move/rename/delete originals to make a check pass. Keep last verified checkpoint separate from present incomplete/unknown state. Do not hide pipeline errors, repair counters, retry a different floor or reset unknown commitments to zero (AP:27,486; V4:38,65–66; L:120–131).

| AP STOP source | Intel-route STOP condition/action |
|---|---|
| AP:488 | Any source/release/bundle/plist/pin mismatch or unexpected inventory/history drift; re-review changed inputs, preserve prior pins. |
| AP:489 | Unsupported/malformed/duplicate-key history, temporary/counter/archive/unresolved evidence, floor below observed maximum, exhausted space or ownership lock; preserve entire Intel backup history; under-lock refusal changes no existing bytes. |
| AP:490 | Recovery counter/state/archive/population mismatch, unexpected live files or preserved hash mismatch; a fresh namespace does not justify discarding old evidence. |
| AP:491 | Status healthy before sequenced completion above actual barrier is false green. |
| AP:492 | Nonzero open/receipt/transfer, receipt exit 75/error_number, journal, token/auth/dry-run/skipped operations, later issue, heartbeat publication failure, malformed/stale status, Operation not permitted, HEARTBEAT-FAILED/FATAL: STOP; diagnosed operator-approved successor only after clean termination. |
| AP:493 | Required permission/start absent, app without upload child, dead owner/child or stalled progress: preserve ps/wake/logs before any owner-authorized termination. |
| AP:494 | Exit zero with warnings cannot qualify activation; subsequent clean completion and full readback required. |
| AP:495 | Bootstrap failure/disabled job, missing observed successor, nonclean/nonzero status or non-benign scheduled log. |
| AP:496 | Any content/path/metadata discrepancy, missing/error/unreadable/unchecked object, report/verifier/exit failure or inventory drift; no changed-file waiver. Diagnose then obtain required go for coherent recapture/catch-up/readback. |
| AP:497 | Actual host fixture/descendant clearance incomplete, ps unavailable, wake assertion absent, Intel source unavailable, missing go/required permission, lost-history ambiguity or unexpected remote data. M3 mount check is replaced by source-capture/device binding (V4:17,24,65–66,76). |

Additional route STOPs: Intel return access to M3/memit; missing/failed M3 gate/probe teardown; unbounded/out-of-envelope work; source change/unavailable consistency; short/unknown quota or staging; unaccounted retained bytes; protection/manifest/alias drift. Stop M3 capture/release freeze for science, keep incomplete status, retain partials under caps, reconcile before approved recopy. Intel may continue only an already verified immutable local generation (V4:17,22–25,35–45,65–81; L:124–131).

Test: each failure control produces refusal/incomplete status and preserves evidence/originals; no fallback to memit, automatic repair/resume, deletion or hidden warning-to-green conversion. Future host commissioning receipts must show the actual failure and resulting state (AP:486–499; V4:25,81).

## Review handoff and context

Next action is Astra review of O1 and O2, followed by the three choices and separate go; missing inventory/implementation bounds/Intel host receipts remain explicit commissioning prerequisites, not DA1 activation success (B/r2_redesign_operator_adoption.md:11; V4:110–116).

DA1 writes only these two outputs and performs no switch-on. Source baseline hashes were taken before drafting; reread/hash/scope/line/citation checks below are local document evidence only. No new bulk estimate or timing promise is supplied.

Successor rule: start a new piece only with ≥60% context left. At MAESTRO's 45%-left message or any compaction, stop starting work; write results/drive_activation_intel_20261012/da1_handoff.md with done/in-flight/remaining/exact paths/decisions/next step/open risks and this same rule; reply DA1 HANDOFF, or READY if finished.

## Acceptance map

| Requirement | O2 lines / evidence |
|---|---|
| A1 exact sources/Intel-first/M3 push/Intel upload | 42–60; 62–78; 168–188 |
| A2 approved caps/bounded batches/shortage | 80–100; 62–78 |
| A3 all I2 checks and falsifiable Test lines | 42–60; 62–78; 80–100; 138–152; 154–166; 168–188; 190–204 |
| A4 every AP section disposition with P/V4 lines | 102–136 |
| A5 STOP/preservation | 206–225; 138–152 |
| A6 ordered review/three choices/separate go/bounded commissioning | 18–34; 227–233 |
| A7 exactly three plain-language questions/recommended answer/reason | 36–40 |
| A8 requirement map and exact line count | this table and final line |
| I2 exact source and Intel-first choice 11 | 42–60; 62–78 |
| I2 immutable checkpoint versus live convergence/source changes | 62–78; 168–188 |
| I2 final catch-up/full readback | 168–188 |
| I2 history mode/preserved decisions | 36–40; 138–152; 190–204 |
| I2 bandwidth/host/login/app permissions | 80–100; 154–166; 190–204 |
| I2 reviewed generation/receipt semantics; no M3 acceptance transplant | 102–136; 138–152; 154–166 |
| I2 operator/auth gates; old-mirror retirement/no deletion | 18–34; 36–40; 190–204; 206–225 |
| I3 exact identities/sizes/scientific holds across selected sources | 42–60 |
| I3 overlap/non-disjoint sets/no double-counted capacity | 42–60; 80–100 |
| I3 reviewed bounded-batch/source-selection plan; full-backup scope | 80–100; 168–188 |
| I3 no M3 internal archive borrowing/new quotas | 80–100 |
| I3 retained history/immutable capture/verification/log/peak commitments | 62–78; 80–100; 138–152; 168–188; 190–204 |
| I3 named-file retention/exact-path deletion gates | 42–60; 190–204; 206–225 |
| L1–L4 output mapping | O1 Changes from v1, L:145–153; O2 source/route/capacity/receipt/upload references at 42–60; 62–78; 80–100; 138–152; 168–188 |

O2 line count: 262 (including this line and Acceptance map).
