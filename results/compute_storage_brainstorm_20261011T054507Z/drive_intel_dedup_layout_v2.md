# Intel de-duplicating recovery-copy layout v2 — DA1

Status: PROPOSED layout revision for Astra review; host commissioning and activation remain OPEN. Adopted D-R2C-ADOPT governs conflicts; adoption switches nothing on (B/r2_redesign_operator_adoption.md:1–11). Amendment 21 keeps identical content once on Intel, every admitted path uploaded to Drive, and an Intel checkpoint first; exclusion/deletion gates remain (B/decisions_log.md:230–238; B/r2_git_drive_redesign_v4.md:73–81).

B = `results/compute_storage_brainstorm_20261011T054507Z`. All B/file:line references resolve beneath this directory; V4 = B/r2_git_drive_redesign_v4.md. Every layout, interface, protection, phase, test and status definition below is PROPOSED and UNRUN. Recovery/upload reuse protected bytes; source changes require new immutable versions (B/design.md:259–265). V4 replaces the old shared-disk protocol; source-read-only capture yields to science, and destructive cleanup/science-visible retrieval/publication stay inactive pending separate protection (V4:22–25,108–116).

## 1. Layout — PROPOSED

PROPOSED root: `<approved-Intel-volume>/llmdb-recovery/`, a dedicated local filesystem area distinct from builders and source checkouts. Exact mount, filesystem, volume identity and owner account await commissioning; the separation implements protection from writable builder files (B/design.md:183,206).

| Relative location (PROPOSED) | Contents and role |
|---|---|
| `objects/sha256/<digest>` | A regular content object named by its complete SHA-256; identical admitted payloads reuse this object. |
| `generations/<generation>/manifest.jsonl` | Immutable path/version records, exclusions-policy identity and source cutoff; see section 2. |
| `generations/<generation>/paths/<root-id>/<relative-path>` | Hard-link aliases to objects; never editable working files. |
| `generations/<generation>/seal.json` | Manifest digest, object-set identity, protection evidence and completed verification receipt references. |
| `incoming/<attempt>/` | M3-initiated push lands here on Intel's own disk; unsealed object parts and draft metadata; never an upload or restore source (V4:73–74). |
| `receipts/<receipt-id>/` | Append-only dated phase/failure receipts; uploader state lives outside sealed generations. |

PROPOSED choose **hard links**, rather than per-path APFS clones. Contract: each regular-file alias and its content object must identify the same inode on the commissioned volume. This directly expresses content-once storage. Clones would require a separately demonstrated shared-allocation accounting contract and diverge after a write; they are not the chosen layout. Actual link/clone behavior and filesystem support require host controls before reliance, rather than assumptions about this Intel volume (B/design.md:261,277,281–282).

PROPOSED treat a write through any hard-link alias as a write to **all** aliases of that object, across generations. No supported operation may write through such an alias. Restores and builder exports create independent destination files. Per-path original mode and mtime remain in the manifest; applying them to aliases is prohibited because inode metadata is shared. These constraints implement immutable saved versions and separation from builder files (B/design.md:183,206).

PROPOSED seal protections: a separately provisioned custodial owner; no write permission or write ACL for uploader/builders; read/search-only access; immutable file flags (`uchg`) on object/alias inodes and generation metadata, plus immutable directory flags on completed generation directories after durable publication. Object-parent directories permit only custodial creation of new digest names; sealed names/inodes cannot be replaced or unlocked. Pin owner, permissions, flags, filesystem identity and object/alias device+inode in the seal receipt. Refuse sealing if any cannot be applied and observed. Exact account and filesystem capabilities are commissioning items, not assumed host facts (B/design.md:183,261,281).

PROPOSED no protection is claimed against an administrator deliberately clearing flags or altering the disk. Every upload/restore first checks the Git-pinned manifest and seal, alias identities/protections and content hashes. Hash the exact stream delivered downstream as well; retain the immutable protection throughout consumption and compare object identity/protection afterward. Any discrepancy invalidates the generation and blocks completion. Thus privilege bypass or corruption must be detectable before acceptance, including a same-size change through another alias (B/design.md:183,188,261,283–284).

PROPOSED source paths resolve only through the manifest's admitted root map. Reject traversal, ambiguous/case-colliding names, unsupported file kinds and escaping references; never rename colliding source paths silently. Represent an admitted symlink as target-text payload plus `kind=symlink`, with a regular hard-link alias to its payload object, rather than a live dereferencing link. The uploader sends that representation at the same relative path; restore reconstructs the literal symlink. Review this representation and its compatibility before capture; the historical inventory includes symlinks (B/drive_intel_fit_facts.md:14; B/design.md:187,281).

## 2. Manifest — PROPOSED

PROPOSED a deterministic, byte-preserving manifest at the location above, with an explicit schema and generation header. Header: source-host/root identities, capture cutoff, canonical Git revision or admitted dirty-source identity, exact reviewed inclusion/exclusion policy digest, object-set identity and path population totals. Sort by encoded source-root/path bytes; define serialization before building and hash the saved bytes. A dated manifest selects exact immutable versions (B/design.md:183,259,281).

| Per-path field (PROPOSED) | Meaning |
|---|---|
| `root_id`, `source_path`, `relative_path` | Exact admitted source location and unambiguous path to reconstruct; preserve original path bytes without silent normalization. |
| `kind` | Regular file, directory or symlink; reject unsupported kinds. Record directories, including empty ones. |
| `size`, `sha256`, `object_id` | Regular-file byte length and full content digest; object ID is `sha256:<digest>`. Symlinks use exact target-text bytes with the same digest rule; directories have explicitly inapplicable content fields. |
| `mode`, `mtime` | Original permission bits and exact source timestamp with explicit precision; per path, independent of sealed inode metadata. |
| `link_target` | Symlink target encoded losslessly; absent for other kinds. Never dereference it during upload. |
| `source_generation`, `capture_receipt` | Frozen source/version identity and its capture evidence; mutable current-source observation is not this identity. |

PROPOSED retain an object index giving each digest's size and all referring paths. Require exact equality between independently captured source enumeration and manifest path set; no duplicate records, missing admitted paths, unexplained extras or dangling object references. Same digest with inconsistent size or unequal payload comparison refuses reuse. This provides complete path coverage rather than a successful transfer counter alone (B/design.md:187,194,277,282).

PROPOSED MAESTRO commits the manifest's SHA-256 and generation/source identifiers to Git before that generation qualifies as a recovery checkpoint or upload source. Preserve an independent matching manifest with the Intel generation and a credential-free recovery package; Intel copies cannot rewrite Git authority. DL1 creates neither a manifest nor a commit (B/design.md:183,189–190,206).

PROPOSED exclusions precede content hashing/copy and manifest admission: exclude every `.hf_token`, Drive/GitHub/provider credential, secret-bearing configuration and credential-containing payload. Admit only a reviewed credential-free inventory; uncertain files, including opaque archives/Git objects that might contain credentials, block capture pending classification. Do not copy or record credential bytes, values or content hashes. Exclusion-policy records describe categories, not credential payloads. Reject symlink aliases to excluded credential files (B/design.md:187,263; B/decisions_log.md:238).

The historical inventory contains `.hf_token` files and a Git temporary object absent from the intended exclusions. Its totals therefore are planning bounds, not the exact future credential-free manifest or upload count; reconcile and re-review that population without silently omitting other admitted paths (B/drive_intel_fit_facts.md:14,19–21,205).

## 3. Staging — PROPOSED; v4 implementation/commissioning OPEN

PROPOSED capture a whole checkpoint before upload, rather than treating completed batches as a completed checkpoint. Transfer uses v4's bounded batches while the generation remains incomplete; preserve Intel-first checkpoint ordering. **Test:** science races/stuck probes must satisfy bounded teardown without waiting for native copy completion; source drift/interruption refuses capture, and incomplete staging refuses first upload (B/decisions_log.md:238; B/design.md:281–283; V4:23–25,53–54,81).

| Phase (PROPOSED) | Verification and refusal |
|---|---|
| Capture | Freeze the reviewed credential-free population and producer writes under a separately approved procedure. M3 enumerates/hashes only after unchanged gate and storage admission; use bounded native tools with science-priority probe handoff. Stability covers enumeration through Intel capture verification or a reviewed immutable snapshot; matching hashes alone do not prove a coherent cutoff. Abandon capture/release the freeze when science needs to write; drift/unavailable stability/credential uncertainty refuses the generation (V4:22–25,76). |
| Transfer | M3 initiates a bounded source-read-only cable push into Intel-local `incoming/`; Intel holds no route to M3/memit. Bind frozen manifest/paths and physical-pool budgets; reuse sealed bytes only after size/hash comparison. Verify durable received parts; publish only a whole size/hash-matching object by non-overwriting rename and construct aliases. Mismatch never replaces evidence; no part certifies a checkpoint (V4:15–17,53–54,73–76). |
| Verify | Re-read every Intel object; compare all source identities, aliases, metadata and independent enumeration. Check exclusions, unique bytes, retained partials and allocations; refuse missing/extra/altered/unobservable items. Release the source freeze after successful capture verification; abandon it on science demand with no acceptance. Later Intel upload/readback needs no M3 freeze (V4:24,76–78). |
| Seal | Close all writers; flush objects/metadata and their directories; commission durability behavior; apply and inspect protections; re-read the manifest/seal and object identities. Publish a complete seal only after successful verification and MAESTRO's Git digest commitment. Failed durability/protection/publication leaves the generation unqualified and preserves partial evidence. |

PROPOSED these phase checks implement complete-source capture, source-change refusal, immutable upload and original preservation; no source-write pause length is promised (B/design.md:259,277,281–284). Disk-work permission alone does not freeze producers or establish a coherent source checkpoint; the reviewed capture procedure is a separate activation obligation (B/design.md:281–284).

D-R2C-ADOPT adopted V4, replacing the old protocol while leaving implementation and host acceptance OPEN. Pin the reviewed M3 push, Intel destination and manifest/protection implementation before capture; no mount, reverse file service or ad hoc path substitutes (B/r2_redesign_operator_adoption.md:9–11; V4:15–17,108–116).

| Exact dependency (PROPOSED integration) | State and source |
|---|---|
| M3-originated push, Intel-local receiver/checkpoint and Intel uploader ownership; commissioned destination/pool | Implementation OPEN — V4:15–17,73–75,110. Reconcile the recovery root; no second full checkpoint. SOURCE_COPY/BACKUP_READ role selection is RETIRED (v4 has no rule). |
| Reviewed channel/destination identity and credential-free recovery package | Implementation OPEN — V4:15–17,77,79. Old request/stream/ack envelopes and immutable unit profiles are RETIRED (v4 has no rule); freeze the replacement interface in the implementation brief. |
| Unchanged M3 gate, bounded probe teardown/science-priority handoff, pause/stop and conservative reservations | Implementation OPEN — V4:21–25,38–45,53–54,65–66. Durable single-use allowance consumption and old closure API are RETIRED (v4 has no rule). |
| Actual native helpers and probe/helper termination; failed observation refuses/stops source reads | Implementation OPEN — V4:21–25. Old contained process/descriptor clearance is RETIRED (v4 has no rule); observation is not lineage/quiescence proof. |
| Reviewed execution/resource bounds, bounded batches and physical-pool peak admission including retained temp/metadata/concurrent commitments | Implementation OPEN — V4:23–25,35–45,53–54,74–76. Old unit deadlines/range profiles are RETIRED (v4 has no rule); no invented timing/chunk limit. |
| Link-loss/interruption retention, revalidation and host evidence; no reconnect/timer auto-resume | Implementation OPEN — V4:38,65–69,75–81,116. Old epoch/allowance/profile fencing is RETIRED (v4 has no rule). Explicit MAESTRO resume approval remains a layout safeguard; OPERATOR DECISION if changing it (v4 has no resume-approval rule). |

PROPOSED M3 enumeration/hash/source verification obey the same unchanged gate, bounded native-copy envelope and science-priority probe handoff as the push. Intel performs local assembly/full-file verification; completed parts never certify whole objects. Freeze executable/helper/resource bounds before commissioning; no long-lived Python maintenance helper, classifier weakening or restart/logout switch (V4:21–25,53–54,76,119–122; B/design.md:282).

## 4. Upload source — PROPOSED

PROPOSED uploader opens only a complete Git-bound sealed generation. It enumerates manifest paths, opens their protected object/alias read-only and streams each payload to the reviewed Drive generation at that path. Duplicate paths referencing a digest are each uploaded; content deduplication does not collapse remote paths. Symlink target-text representation and directory metadata travel with the matching manifest; namespace fidelity must be tested before reliance (B/drive_intel_fit_facts.md:175,190; B/design.md:183,283).
PROPOSED freshness: MEMIT_ONLY; PUSHING/INCOMPLETE; STAGED_ON_INTEL; UPLOADING/INCOMPLETE; VERIFIED_AT_GENERATION; BEHIND; UNKNOWN. STAGED_ON_INTEL is complete/verified/sealed but not remotely protected; research acquisition uses pinned Git plus verified Drive, never staging or memit. Unknown frontier is UNKNOWN; newer M3 versions leave older verified Drive objects BEHIND (V4:11–17,78,81).
PROPOSED logs, retries, remote mapping and progress receipts go into separate budgeted Intel-local worker storage; uploader has no recovery-store write capability. Hash each transmitted stream against its manifest record and fully check remote content against that same generation. Failure preserves local objects and shows incomplete upload. Credentials are separately provisioned outside the copy/manifest/upload set (B/design.md:261,263,265).

The reference path population is **287.177 GB**, not a content-once remote upload; exact admitted bytes require the corrected credential-free inventory. New source writes belong to later manifests. A checkpoint alone does not satisfy final catch-up/full convergence, source-stability, activation or old-copy-retirement gates; M3 stability lasts through capture verification, Intel immutability through upload/readback (B/drive_intel_fit_facts.md:14,175,205; B/design.md:259,263,284; V4:24,76,110).

## 5. Space — PROPOSED accounting; no measured overhead

GB is decimal; logical file sizes and allocated filesystem bytes are different measures (B/drive_intel_fit_facts.md:5–7). PROPOSED count unique content once and charge metadata, partials, temp and concurrent commitments explicitly; do not add staging as free recovery capacity (B/design.md:261,277; B/drive_intel_fit_facts.md:174,180).

| Planning quantity | Cited arithmetic or limitation |
|---|---|
| Original path payload | **287,177,060,251 B / 287.177 GB** (B/drive_intel_fit_facts.md:14,113). |
| Confirmed duplicate payload | **156,979,390,913 B** (B/drive_intel_fit_facts.md:105). |
| Content-once upper bound | **287,177,060,251 − 156,979,390,913 = 130,197,669,338 B**, rounded **≤130.198 GB** (B/drive_intel_fit_facts.md:14,105–106,113). |
| Allowance and payload headroom | **250 GB − ≤130.198 GB = ≥119.802 GB**; this is payload-only headroom (B/drive_intel_fit_facts.md:159,168). |
| Metadata/allocation overhead `M` | Manifest, object index, aliases/directories/inodes, receipts, allocation rounding and other recovery metadata; value UNKNOWN, to measure and bound before capture (B/drive_intel_fit_facts.md:5–7; B/design.md:277). |
| Temp/partial overhead `T` | Conservatively budget one incoming file up to the cited largest file **6,178,316,608 B**, plus all retained failed parts and any additional implementation buffers/temp allocations. No second full tree or verification copy (B/drive_intel_fit_facts.md:172; B/design.md:261,277). |
| Peak recovery charge | PROPOSED `U + M + T ≤ 250 GB`, with actual allocated bytes/commitments also satisfying physical-pool admission; `U` is the newly frozen unique payload, not assumed equal to the historical bound (B/drive_intel_fit_facts.md:159,168; B/design.md:277). |
| Net allowance headroom | PROPOSED `250 GB − (U + M + T)`. The cited **≥119.802 GB** cannot be claimed as net free space after unknown overhead. Report payload and total-charge headroom separately (B/drive_intel_fit_facts.md:5–7,168; B/design.md:277). |

PROPOSED only one incoming content object at a time; finish and publish it before another. Parts become objects by rename, with no second payload. Interrupted parts remain charged; reserve future growth, stop on insufficient bounds, never reclaim automatically. Exact execution/buffer/batch limits await the reviewed implementation; no memit staging or allowance borrowing (B/design.md:265,277; V4:23–25,38–45,74–75,121).

The source estimate counts unhashed small files as unique; name/size twins are not enough to deduplicate them. PROPOSED hash all admitted payloads before reuse. Source growth, secret exclusions and the excluded temporary Git object require refreshed sums (B/drive_intel_fit_facts.md:15,21,90,93,106,205).

PROPOSED no bulk transfer-staging allowance is borrowed: the content-once recovery copy stays within **250 GB**; separate **50 GB** analysis/transfer is not recovery capacity. Preserve seven daily/four weekly restore points within the amended **50 GB** additional unique-history cap; overflow is visible, never silently trimmed. Restore checks remain required but are not a prerequisite to first upload; no old-copy retirement/deletion authority (B/drive_intel_fit_facts.md:159,171,174,190; B/decisions_log.md:101,191,234–238; V4:74–75,91,111).

## 6. Restore and commissioning — PROPOSED, UNRUN

PROPOSED restore into a fresh approved unused destination. Obtain the matching manifest and its canonical Git digest; verify the seal and every needed object. Recreate source-root-relative directories, copy each file's bytes into an independent destination file, reconstruct symlinks from literal targets, then apply per-path mode/mtime, directories last. Reject collisions, escapes or existing destination paths; never overwrite surviving evidence. Rehash every restored path and compare its kind/metadata and complete path set with the manifest (B/design.md:187–190).

PROPOSED commission a small, separately authorized restore selection containing known code/records, an old retained version, the matching manifest, a selected bulk sample and duplicate-content paths with different metadata. Exact selections, destination and peak writes await the implementation brief. Preserve the resulting test evidence; an old version must actually be present and independently pinned, not inferred from the current store. Failure to supply it keeps commissioning OPEN (B/design.md:183,188,192).

PROPOSED positive controls: exact restored identities and path coverage; independent restored files; original metadata; duplicate alias allocation/identity; denied writes by uploader/builders; inability to change a sealed object through any alias. Exercise bypass/corruption controls only on separately authorized disposable fixtures, never by altering the recovery generation. Verify protection failure and same-size object changes prevent acceptance (B/design.md:183,188,194,261).

PROPOSED negative controls: missing/corrupt object, removed manifest entry against independent capture enumeration, incomplete staging, full-disk failure and cable disconnect. Publish each in the same copy/restore status view, with host/generation/cutoff, protected coverage, omissions and test receipt. Controls remain UNRUN; this document reports no verified-copy count or host success (B/design.md:188,194,265,267).

For actual memit loss, canonical records come from canonical Git or an independently qualified Git copy; Intel supplies matching bulk manifests/objects. Absent files require exact verified Drive retrieval or permitted regeneration. MAESTRO separately confirms revisions/environment/engine fingerprint/baseline gates before science. Travel readiness/monthly drills retain separate authority; science-visible restoration/publication stays inactive until separately reviewed exclusion/disjoint-path protection passes (B/design.md:189–192; V4:13,22–25,91,111).

## 7. Failure classes — PROPOSED statuses

PROPOSED the following dated statuses share the normal copy/restore view and retain last complete checkpoint separately from current failure/unknown state. Success displays phase/coverage/receipt, never replaces incomplete or stale-source warnings (B/design.md:194,259,265,267).

| Failure | Detection (PROPOSED) | Visible status and action (PROPOSED) |
|---|---|---|
| Corrupted object | Full digest/size mismatch at staging, pre-consumption or delivered-stream verification; enumerate every manifest reference to affected digest. | `HALTED(CORRUPT_OBJECT)`; generation unusable for acceptance; list affected paths; retain bytes/evidence. |
| Hard link broken/replaced, or later write | Device/inode mismatch, protection drift, missing alias or content hash mismatch. Any in-place write potentially affects every alias, so invalidate all references. If a future clone layout is proposed, divergent clone bytes likewise require per-path hashes. | `HALTED(IMMUTABILITY_BREACH)`; no upload/restore completion; no automatic relinking or repair. |
| Missing manifest entry | Git digest mismatch, schema/path-set mismatch against independent frozen enumeration, or declared coverage not matched by records. | `HALTED(MANIFEST_INCOMPLETE)`; refuse seal/consumption; missing paths remain unprotected. |
| Partial staging | Unsealed generation, incomplete expected ranges, missing objects/aliases or absent durable capture/seal receipt. | `INCOMPLETE(STAGING)`; never an upload source; interrupted M3 capture remains incomplete/unaccepted; unresolved actual commitments remain charged (V4:24–25,38,75–78). |
| Disk full | Budget/commitment check fails, allocation/write/flush fails, or partial file cannot be completed durably. | `BLOCKED(SPACE)` before work; `HALTED(DISK_FULL)` during work; retain partials, no automatic deletion or emergency M3 storage. |
| Cable disconnect | Transport/ack loss or unavailable source observation; distinguish Intel-local generation from interrupted source capture. | `UNAVAILABLE(LINK)` with last-seen time; unverified capture remains incomplete and requires later coherent recopy/revalidation. No automatic resumption. A sealed Intel upload needs no M3 reads (V4:22–25,65–66,76,81). |

These responses preserve exact identities, bytes and incomplete/unknown status (B/design.md:183,188–189,194,265,267,282–283; V4:24–25,38,65–66,75–81). Old boundary/closure/fresh-allowance interpretations are RETIRED (v4 has no rule); replacement host checks remain UNRUN (V4:25,116).

## 8. Open items and Astra checks — PROPOSED review agenda

- PROPOSED Astra checks the hard-link alias threat model, source-mode/mtime separation, complete alias invalidation, immutable flags/owner/ACL enforcement, concurrency during consumption and administrator-bypass detection. Demonstrate creation of new aliases to reused sealed objects without clearing their protections; if unsupported, refuse reuse and obtain a revised layout before any next-generation copy. Require actual filesystem/protection/durability controls before relying on the layout (B/design.md:183,188,261,281–282).
- PROPOSED Astra checks the credential-free inclusion policy, opaque payload classification, byte-preserving manifest schema, independently enumerated path completeness, symlink representation, case/path collisions and Git digest commitment. No corrected path count or exact upload size is available yet (B/design.md:187,263,281; B/drive_intel_fit_facts.md:14,21,205).
- PROPOSED Astra checks coherent checkpoint capture, separately approved producer stability, native executable/helper/resource bounds, science-priority probe teardown, destination binding, partial preservation and explicit resume. Adopted V4 supplies design authority; implementation and host evidence remain OPEN. No timing/interface/commissioning acceptance is conferred (B/design.md:281–284; V4:15–17,21–25,35–45,73–81,116).
- PROPOSED Astra requires measured/bounded `M` and `T`, current source sums, allocation accounting and retained-part/concurrent commitments before copying. Payload headroom is not measured physical free space; adding staging or counting the old internal mirror twice is invalid (B/drive_intel_fit_facts.md:5–7,120–130,159–180; B/design.md:261,277).
- Source discrepancy: seed integration has I3, and points to the later completion table containing I3b. Use that inventory requirement and amendment 21 without importing I3's older caps; affected rows remain OPEN pending their own evidence (B/integration_plan.md:25,89; B/integration_r5_completion_table.md:101; B/decisions_log.md:234–238; V4:105,110–111).
- PROPOSED Astra checks restore controls, old-version availability, status sinks, preserved activation/final catch-up/full-readback/operator/auth gates and exact-path deletion authority. I7 keeps archive/retest dependencies blocked until qualified Drive completion; a layout review does not release them (B/design.md:183,188–194,263,284; B/integration_plan.md:29; B/decisions_log.md:238).
- PROPOSED next single step: MAESTRO submits this layout and the Intel activation plan to Astra; then the three deferred choices and a separate operator go precede bounded commissioning. No copying, build, host activity or credential provisioning is authorized here (B/r2_redesign_operator_adoption.md:11; V4:110–116,124–130).

DA1 successor context rule: start new work only at ≥60% context left. At MAESTRO's 45%-left message or any context compaction, stop starting work, write `results/drive_activation_intel_20261012/da1_handoff.md` with done/remaining/decisions/next step/open risks and this rule, then reply `DA1 HANDOFF`; if already finished, reply READY. This is the DA1 dispatch constraint, not host acceptance.

## Changes from v1
- L1 — all eleven shared_disk_clearance_freeze_v1.md references replaced; old-only rules explicitly retired or marked OPERATOR DECISION: O1 lines 64,68–73,75,100,131,137.
- L2 — M3 push into incoming/, unchanged-gate/source-read-only envelope and science priority: O1 lines 17,51,53,57–59,64,68–75; V4:15–25,53–54,73–76.
- L2 — freshness list, Git/Drive-only acquisition and capture versus upload stability: O1 lines 59,75,80,83,127,129,131; V4:76–81.
- L2 — preserve amended caps/history/restore obligation; no science-visible retrieval activation: O1 lines 104,116; V4:22–25,75,91,111.
- L3 — rechecked unchanged design/decisions/fit-facts citations against current text; seed I3b discrepancy corrected against the completion table: O1 line 139. Older caps in design are superseded by O1 lines 97,104 and V4:75.
- L4 — this change map gives each changed O1 line; heading/status/aliases refreshed at lines 1,3,5, implementation review at 137, next review at 141, successor context rule at 143.
- Unchanged v1 layout/protection/manifest/numbers/restore controls remain at O1 lines 9–16,18–49,60–62,79,81,85–98,102,108–114,118–126,128,135–136,138,140 (B/drive_intel_dedup_layout_v1.md:9–140).
