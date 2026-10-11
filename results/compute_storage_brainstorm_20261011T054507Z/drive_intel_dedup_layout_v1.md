# Intel de-duplicating recovery-copy layout — DL1

Status: PROPOSED design for Astra review before copying; host commissioning and activation remain OPEN. Amendment 21 selects identical content stored once on Intel, every admitted path uploaded to Drive, and an Intel checkpoint first; it preserves exclusion and deletion gates (B/decisions_log.md:230–238).

B = `results/compute_storage_brainstorm_20261011T054507Z`. All B/file:line references resolve beneath this directory. Every layout, interface, protection, phase, test and status definition below is PROPOSED, including choices inside tables. None describes an installed implementation or a performed host test. Recovery and upload reuse protected bytes; source changes require new immutable versions (B/design.md:259–265).

## 1. Layout — PROPOSED

PROPOSED root: `<approved-Intel-volume>/llmdb-recovery/`, a dedicated local filesystem area distinct from builders and source checkouts. Exact mount, filesystem, volume identity and owner account await commissioning; the separation implements protection from writable builder files (B/design.md:183,206).

| Relative location (PROPOSED) | Contents and role |
|---|---|
| `objects/sha256/<digest>` | A regular content object named by its complete SHA-256; identical admitted payloads reuse this object. |
| `generations/<generation>/manifest.jsonl` | Immutable path/version records, exclusions-policy identity and source cutoff; see section 2. |
| `generations/<generation>/paths/<root-id>/<relative-path>` | Hard-link aliases to objects; never editable working files. |
| `generations/<generation>/seal.json` | Manifest digest, object-set identity, protection evidence and completed verification receipt references. |
| `incoming/<attempt>/` | Unsealed object parts and draft metadata; never an upload or restore source. |
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

## 3. Staging — PROPOSED; R2 dependencies PENDING R2

PROPOSED capture a whole checkpoint before upload, rather than treating completed batches as a completed checkpoint. Transfer can use R2's finite units while the generation remains incomplete. This preserves Intel-first checkpoint ordering (B/decisions_log.md:238; B/design.md:281–283).

| Phase (PROPOSED) | Verification and refusal |
|---|---|
| Capture | Freeze the reviewed credential-free source population and its producer writes under a separately approved capture procedure. Hash every admitted payload, including small files; collect exact metadata and independent path enumeration. Check metadata/content against the frozen source. A write pause must cover enumeration through successful transfer verification unless a reviewed immutable source snapshot replaces it. Source drift, unavailable freeze or credential uncertainty refuses a generation. |
| Transfer | Request admitted SOURCE_COPY/BACKUP_READ units bound to frozen source/manifest, paths, ranges and pool budgets. Stream each new digest into an exclusive incoming part; reuse a sealed object only after size/hash comparison. Verify received ranges and their durable receipts. A complete incoming file must match frozen size/hash before publishing it by non-overwriting rename and constructing aliases. Mismatch never replaces an object or surviving evidence. |
| Verify | Re-read every Intel object; hash and compare all source identities, aliases and metadata records. Reconcile the entire manifest against the independent frozen enumeration. Check exclusion closure, total unique bytes, retained partials and filesystem allocations. Refuse on any missing, extra, altered or unobservable item; do not release the source freeze as a successful checkpoint on a partial result. |
| Seal | Close all writers; flush objects/metadata and their directories; commission durability behavior; apply and inspect protections; re-read the manifest/seal and object identities. Publish a complete seal only after successful verification and MAESTRO's Git digest commitment. Failed durability/protection/publication leaves the generation unqualified and preserves partial evidence. |

PROPOSED these phase checks implement complete-source capture, source-change refusal, immutable upload and original preservation; no source-write pause length is promised (B/design.md:259,277,281–284). Disk-work permission alone does not freeze producers or establish a coherent source checkpoint; the reviewed capture procedure is a separate activation obligation (B/design.md:281–284).

R2's freeze is itself PROPOSED with review/commissioning open. The following are **dependencies**, not DL1's authority to freeze or implement R2. Bind the permitting R2 revision and profile hashes before any staging. No alternate direct-mount, file-service or ad hoc transfer path substitutes for R2 (B/shared_disk_clearance_freeze_v1.md:3–5,41,202).

| Exact dependency (PROPOSED integration) | State and source |
|---|---|
| M3 coordinator, Intel DRIVE_BACKUP_ACTIVATION worker and bounded M3 executor ownership; SOURCE_COPY/BACKUP_READ operation selection and commissioned destination/pool | **PENDING R2** — B/shared_disk_clearance_freeze_v1.md:13–17,32,37,41. Reconcile its checkpoint destination with this recovery root; no second full checkpoint is implied. |
| Pinned authenticated transport/role bindings, exact request/stream/ack envelopes and immutable unit profiles; no credential transport in the recovery package | **PENDING R2** — B/shared_disk_clearance_freeze_v1.md:45–60,90. DL1 names no new transport/auth decisions. |
| Durable M3 authority; fresh single-use consume before shared I/O; pending-science exclusion, pause request and verified boundary/closure | **PENDING R2** — B/shared_disk_clearance_freeze_v1.md:64–68,89–100,108–116. |
| Actual contained helper population and independent process/descriptor observations; malformed, denied, stale or unavailable evidence refuses clearance | **PENDING R2** — B/shared_disk_clearance_freeze_v1.md:126–139. |
| Final deadline, unit/range/buffer limits and local/physical-pool admission with temp/metadata/other commitments accounted | **PENDING R2** — B/shared_disk_clearance_freeze_v1.md:143–162. DL1 invents no latency, chunk or free-space rule. |
| Unknown ownership/link loss/reboot fencing; retained partial checkpoints; explicit MAESTRO resume approval and fresh allowance; design/runtime profile pins and real-pair acceptance | **PENDING R2** — B/shared_disk_clearance_freeze_v1.md:115–122,167–185,202. No reconnect or timer auto-resume. |

PROPOSED all capture hashing/enumeration and source verification touching M3/memit must fit admitted R2 operations; whole-file hashing is not a bypass around finite units. Use separately named reviewed range jobs and Intel-local assembly/checksum records; a completed range never certifies the whole object. Compatibility of complete-file source hashing/capture with these jobs remains **PENDING R2** and OPEN for the implementation brief (B/shared_disk_clearance_freeze_v1.md:32,41,90,120,153; B/design.md:282).

## 4. Upload source — PROPOSED

PROPOSED uploader opens only a complete Git-bound sealed generation. It enumerates manifest paths, opens their protected object/alias read-only and streams each payload to the reviewed Drive generation at that path. Duplicate paths referencing a digest are each uploaded; content deduplication does not collapse remote paths. Symlink target-text representation and directory metadata travel with the matching manifest; namespace fidelity must be tested before reliance (B/drive_intel_fit_facts.md:175,190; B/design.md:183,283).

PROPOSED logs, retries, remote mapping and progress receipts go into separate budgeted Intel-local worker storage; uploader has no recovery-store write capability. Hash each transmitted stream against its manifest record and fully check remote content against that same generation. Failure preserves local objects and shows incomplete upload. Credentials are separately provisioned outside the copy/manifest/upload set (B/design.md:261,263,265).

The reference path population is **287.177 GB**, not a content-once remote upload; exact admitted bytes require the corrected credential-free inventory. New source writes belong to later manifests. A checkpoint's upload cannot satisfy live-source final catch-up, full convergence, operator write-pause, activation or old-copy-retirement gates by itself (B/drive_intel_fit_facts.md:14,175,205; B/design.md:259,263,284).

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

PROPOSED only one incoming content object at a time; finish and publish it before starting another. Parts become objects by rename, rather than retaining a second payload. Interrupted parts remain charged; reserve future growth before work, stop when bounds cannot be met, and do not reclaim them automatically. R2's exact unit size/buffer/budget choices remain **PENDING R2** (B/design.md:265,277; B/shared_disk_clearance_freeze_v1.md:153,159–162).

The source estimate counts unhashed small files as unique; name/size twins are not enough to deduplicate them. PROPOSED hash all admitted payloads before reuse. Source growth, secret exclusions and the excluded temporary Git object require refreshed sums (B/drive_intel_fit_facts.md:15,21,90,93,106,205).

PROPOSED no bulk transfer-staging allowance is borrowed: this is the content-once recovery option. The separately cited **50 GB** staging allowance is not part of the **250 GB** recovery budget; earlier design text's larger allowances do not supersede the selected fit option (B/drive_intel_fit_facts.md:159,171,174,190; B/decisions_log.md:234–238). Retained old versions and other jobs need their own approved accounting; this design neither grants history capacity nor retires an old copy (B/design.md:183,261,284).

## 6. Restore and commissioning — PROPOSED, UNRUN

PROPOSED restore into a fresh approved unused destination. Obtain the matching manifest and its canonical Git digest; verify the seal and every needed object. Recreate source-root-relative directories, copy each file's bytes into an independent destination file, reconstruct symlinks from literal targets, then apply per-path mode/mtime, directories last. Reject collisions, escapes or existing destination paths; never overwrite surviving evidence. Rehash every restored path and compare its kind/metadata and complete path set with the manifest (B/design.md:187–190).

PROPOSED commission a small, separately authorized restore selection containing known code/records, an old retained version, the matching manifest, a selected bulk sample and duplicate-content paths with different metadata. Exact selections, destination and peak writes await the implementation brief. Preserve the resulting test evidence; an old version must actually be present and independently pinned, not inferred from the current store. Failure to supply it keeps commissioning OPEN (B/design.md:183,188,192).

PROPOSED positive controls: exact restored identities and path coverage; independent restored files; original metadata; duplicate alias allocation/identity; denied writes by uploader/builders; inability to change a sealed object through any alias. Exercise bypass/corruption controls only on separately authorized disposable fixtures, never by altering the recovery generation. Verify protection failure and same-size object changes prevent acceptance (B/design.md:183,188,194,261).

PROPOSED negative controls: missing/corrupt object, removed manifest entry against independent capture enumeration, incomplete staging, full-disk failure and cable disconnect. Publish each in the same copy/restore status view, with host/generation/cutoff, protected coverage, omissions and test receipt. Controls remain UNRUN; this document reports no verified-copy count or host success (B/design.md:188,194,265,267).

For actual memit loss, canonical Git records come from canonical Git or an independently qualified Git copy; Intel supplies the matching bulk manifest and objects. Absent admitted files require exact Drive retrieval or permitted regeneration. MAESTRO must separately confirm revisions, dependency environment, engine fingerprint and baseline/inertness gates before science; copy completion grants no science acceptance (B/design.md:189–190). Travel readiness and monthly drills retain their separate requirements and authority (B/design.md:191–192).

## 7. Failure classes — PROPOSED statuses

PROPOSED the following dated statuses share the normal copy/restore view and retain last complete checkpoint separately from current failure/unknown state. Success displays phase/coverage/receipt, never replaces incomplete or stale-source warnings (B/design.md:194,259,265,267).

| Failure | Detection (PROPOSED) | Visible status and action (PROPOSED) |
|---|---|---|
| Corrupted object | Full digest/size mismatch at staging, pre-consumption or delivered-stream verification; enumerate every manifest reference to affected digest. | `HALTED(CORRUPT_OBJECT)`; generation unusable for acceptance; list affected paths; retain bytes/evidence. |
| Hard link broken/replaced, or later write | Device/inode mismatch, protection drift, missing alias or content hash mismatch. Any in-place write potentially affects every alias, so invalidate all references. If a future clone layout is proposed, divergent clone bytes likewise require per-path hashes. | `HALTED(IMMUTABILITY_BREACH)`; no upload/restore completion; no automatic relinking or repair. |
| Missing manifest entry | Git digest mismatch, schema/path-set mismatch against independent frozen enumeration, or declared coverage not matched by records. | `HALTED(MANIFEST_INCOMPLETE)`; refuse seal/consumption; missing paths remain unprotected. |
| Partial staging | Unsealed generation, incomplete expected ranges, missing objects/aliases or absent durable closure/seal receipt. | `INCOMPLETE(STAGING)`; never an upload source; `PAUSED` only with accepted R2 boundary proof, otherwise `UNRESOLVED` (**PENDING R2**). |
| Disk full | Budget/commitment check fails, allocation/write/flush fails, or partial file cannot be completed durably. | `BLOCKED(SPACE)` before work; `HALTED(DISK_FULL)` during work; retain partials, no automatic deletion or emergency M3 storage. |
| Cable disconnect | Transport/ack loss or unavailable coordinator/source observation; distinguish Intel-local generation from unobserved shared-transfer state. | `UNAVAILABLE(LINK)` with last-seen time; transfer `UNRESOLVED` until R2 closure proof, then `PAUSED`/incomplete as appropriate (**PENDING R2**). No automatic resumption. A previously sealed Intel-local upload needs no new M3 reads. |

These failure responses implement exact identity checks, preservation and explicit incomplete/unknown status (B/design.md:183,188–189,194,265,267,282–283). All R2 boundary, closure and resume interpretations above are **PENDING R2** (B/shared_disk_clearance_freeze_v1.md:97–100,115–122,135–139,175–185).

## 8. Open items and Astra checks — PROPOSED review agenda

- PROPOSED Astra checks the hard-link alias threat model, source-mode/mtime separation, complete alias invalidation, immutable flags/owner/ACL enforcement, concurrency during consumption and administrator-bypass detection. Demonstrate creation of new aliases to reused sealed objects without clearing their protections; if unsupported, refuse reuse and obtain a revised layout before any next-generation copy. Require actual filesystem/protection/durability controls before relying on the layout (B/design.md:183,188,261,281–282).
- PROPOSED Astra checks the credential-free inclusion policy, opaque payload classification, byte-preserving manifest schema, independently enumerated path completeness, symlink representation, case/path collisions and Git digest commitment. No corrected path count or exact upload size is available yet (B/design.md:187,263,281; B/drive_intel_fit_facts.md:14,21,205).
- PROPOSED Astra checks complete checkpoint consistency and the separately approved producer-freeze procedure, all dependencies marked **PENDING R2**, finite-unit hashing, destination/profile binding, interruption preservation and explicit resume. No R2 timing, interface or commissioning acceptance is conferred by DL1 (B/design.md:281–284; B/shared_disk_clearance_freeze_v1.md:3–5,32,41,116,120,143–162,202).
- PROPOSED Astra requires measured/bounded `M` and `T`, current source sums, allocation accounting and retained-part/concurrent commitments before copying. Payload headroom is not measured physical free space; adding staging or counting the old internal mirror twice is invalid (B/drive_intel_fit_facts.md:5–7,120–130,159–180; B/design.md:261,277).
- Source discrepancy: the instructed `I3b` row was absent from the inspected integration table; available I3 carries inventory/overlap/peak-budget reconciliation. PROPOSED MAESTRO supplies the intended amended row before build; use Amendment 21 and fit-facts for this layout, without importing I3's older caps (B/integration_plan.md:21–29; B/decisions_log.md:234–238; B/drive_intel_fit_facts.md:159–190).
- PROPOSED Astra checks restore controls, old-version availability, status sinks, preserved activation/final catch-up/full-readback/operator/auth gates and exact-path deletion authority. I7 keeps archive/retest dependencies blocked until qualified Drive completion; a layout review does not release them (B/design.md:183,188–194,263,284; B/integration_plan.md:29; B/decisions_log.md:238).
- PROPOSED next single step: MAESTRO submits DL1 and the permitting R2 revision/dependency disposition to Astra. Build, copying, host commissioning, Drive activity and credential provisioning require their separate briefs and existing gates (B/decisions_log.md:236–238; B/design.md:263,281–284).

DL1 context rule for every successor: start a new step only at ≥60% context left. At ≤45%, on any context compaction, or MAESTRO's context stop, finish only the current edit, save, append `## DL1 HANDOFF` with done/remaining/next single step/open risks and this same rule, then reply `DL1 HANDOFF`. This is the DL1 dispatch constraint, not a host-acceptance claim.
