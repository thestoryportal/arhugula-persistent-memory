# Phase-1 Intel host amendment v1 — RE1

Status: DRAFT FOR ASTRA; no build, provisioning, host acceptance or promote permission is asserted. The base remains NO-GO (`RE/astra_spec_r5_verdict.md:2,83–93`). This is the separate amendment requested by design items 1–5 and integration rows I1a/I1c; it leaves the base and decision history intact (`B/design.md:239–245`; `B/integration_r5_completion_table.md:95,97`).

Citation aliases (all paths relative to the worktree):

- **RE** = `results/research_engine_phase1_20261011`.
- **B** = `results/compute_storage_brainstorm_20261011T054507Z`.
- **IS** = `results/intel_setup_20261011`.
- **v5** = `RE/phase1_spec_v5.md`; **r5** = `RE/astra_spec_r5_verdict.md`; **IM** = `B/integration_r5_completion_table.md`.

Base identity: `RE/phase1_spec_v5.md`, SHA-256 **491cdc1c84f978ffdfacfce45dfecca12f65e84043f30cdddc865cbea4302ed0**, computed by `shasum -a 256 results/research_engine_phase1_20261011/phase1_spec_v5.md`. The base identifies its v5/SR3 history at `v5:7`. This amendment supersedes only the prospective hosting, provisioning, path and same-host reservation requirements listed below; historical change tables remain historical (`v5:253–290`; `B/design.md:241–245`).

## A. Intel placement, paths, D-RE-1 and local limits (design item 1; I1a)

Amend D-RE-1's earlier “on this Mac” hosting/storage choice to Intel hosting under D-HW-2; MAESTRO must record this amendment as a subsequent decision, preserving the original record. This document does not edit that record. The integration table explicitly maps the superseded D-RE-1 choice to D-HW-2; the original choice and later direction are also recorded in the decision log (`IM:95`; `B/decisions_log.md:19–27`; `B/design.md:241`).

Neo4j Community and DuckDB run only against local Intel copies. Intel-local database queries, builds and compatible non-model builder work continue during M3 science and link loss. M3 science does not terminate them. Answers expose the admitted snapshot's age and coverage; both stores must identify the same source generation. No Intel-local model inference, editing, training or model-based embeddings are authorized (`B/design.md:218–220,226,233–237`).

Replace “paths below resolve under this memit worktree” with a MAESTRO-frozen Intel-local root and admitted immutable source export/Git revision. Keep the relative code/test/runtime/build layout, but freeze absolute Intel code, interpreter, data, temp, log and receipt paths before dispatch. No runtime path may resolve through a shared M3/memit mount. `.venv-research-engine/` is a separately provisioned Intel environment; the M3 environment and ARM interpreter path are not copied (`v5:189,193–203,248`; `B/design.md:208,233,241,244`).

Source capture preserves the committed-byte/hash checks and exclusions. An admitted immutable export must identify its reviewed Git revision, original relative paths, exact bytes/hashes and capture attribution; it does not make Intel Git or a copied database authoritative. Any expressly admitted uncommitted snapshot needs its own reviewed immutable identity, rather than anonymous dirty bytes. Source acquisition touching M3/memit is outside local querying and depends on section B (`v5:39,143,248`; `B/design.md:206–212,233–235,244`).

Local ceilings and controls:

| Requirement | Intel disposition and authority |
|---|---|
| Pilot/setup area | **6 decimal GB total:** pilot <=5,000,000,000 bytes plus separately measured setup growth <=1,000,000,000 bytes. All pilot data/temp moves into this Intel-local budget. Preserve the pilot's subceilings, generation/candidate/count limits and stop-on-exhaustion; no cleanup/rollover (`v5:207–211,245`; `B/design.md:162,237,241`; `B/decisions_log.md:191`). |
| RSS/support | Neo4j <=2,000,000,000 bytes RSS; RE aggregate <=3 GB; importer <=512 MiB. Aggregate support target <=6 GB, with practical >=6 GB OS/user allowance; one builder test job. Support targets need commissioning proof, not a claim of measured enforcement. Unknown or unsuitable pressure observations block new heavy admissions (`v5:213`; `B/design.md:218,237`). |
| Local concurrency/configuration | Retain one RE writer/Neo4j/query, importer/DuckDB one worker/thread, heap 256 initial/512 MiB max, page cache 256 MiB, Java active processors 2, CPU <=200% Neo4j/100% importer, and per-second CPU/RSS/disk observation. Remove only “no concurrent science”; it depended on co-location (`v5:213`; `B/design.md:218,233,237`). |
| Priority/observation | Every owned Python/Java process has observed niceness >=10: inherited 0 becomes 10, 10 stays 10, >10 stays unchanged. Unavailable priority/admission/host/stop observations block the affected admission or acceptance (`v5:53,213`; `B/design.md:218,237`). |
| Time/start/stop | Retain build/verify <=300 s, provisioning <=15 min, session <=30 min, session-only explicit start/stop, durable interruption diagnostics, retained files, and the local session-end shutdown requirement of `v5:217`. It applies to local cap/stop/revocation/timeout, never to M3 science. No services, launchd, autostart or schedules; stop instead of automatic transaction-log pruning (`v5:217`; `B/design.md:237`; `B/astra_r1_verdict.md:47`). |

Amendment 16 controls Intel-wide caps: recovery 250 GB, extra unique history 50 GB, builder work/tools 40 GB, analysis/transfer staging 50 GB, pilot/setup 6 GB, and >=80 GB kept free. These are conditional planning ceilings, not demonstrated workload fit or admission reservations; do not use the older design-table numbers. Count existing usage and concurrent temporary duplication once per physical pool; no quota borrowing. Every job still requires projected additional peak writes +20 GiB, and the free floor is not spendable. Preserve the 5 GB pilot's prebuild B+P check and unavailable-observation refusal on its new host (`B/decisions_log.md:185–191`; `IM:90,100`; `B/design.md:154–165`; `v5:211`).

Provisioning growth is measured over all frozen Intel installation/cache/temp locations, including the package/dependency closure; `/opt/homebrew` deltas are not Intel evidence. Freeze that inventory and its before/after accounting before mutation. Exceeding the growth cap stops for operator disposition; deletion still requires exact path/size/method approval. The M3 internal disk does not become an archive (`v5:211,245`; `B/design.md:241–242`; `B/decisions_log.md:210`).

## B. Independent host and shared-disk interface (design item 3; I1b dependency)

Remove the RE-for-science exclusion, science-side RE termination, shared SR lock at local RE admission/publication, SR-owned production root and SR commissioning invocation from the prospective Intel requirements (`v5:53,57,78,196–197,215,247`). Independent placement replaces that premise. Keep the single publisher lock and paired-store publication rules; the publisher lock is Intel-local and is not an SR reservation (`v5:143–155`; `B/design.md:233,243–244`; `B/astra_r1_verdict.md:45–47`).

**R2 is a separate reviewed freeze, not drafted here.** Before affected transfer or RE build dispatch, MAESTRO must supply its selected version/hash, permitting review and frozen interface/receipt shapes. The RE side depends on only these obligations:

1. An affirmative disk-work allowance record from the M3-side coordinator before any operation reading/writing M3/memit, including source acquisition. The frozen contract must make the record usable to validate the operation's authority and disposition; local snapshots alone grant no transfer permission (`B/design.md:235`; `IM:96`; `B/astra_r1_verdict.md:24`).
2. Pending science prevents new shared-disk bulk work and requests an active resumable transfer to pause at a verified safe boundary. The RE side exposes the contract's pause acknowledgment/transfer state; a request alone is not affirmative science clearance. The contract, rather than this amendment, freezes ownership including descendants, clearance eligibility, latency, failure outcome and any permitted transfer resume (`B/design.md:235`; `IM:96,192`; `B/astra_r1_verdict.md:24`).
3. A missing, disconnected, stale, malformed or otherwise unknown coordinator/allowance observation never means idle or permission for new shared-disk bulk work. Intel-local computation continues from its last admitted generation; source age and transfer state remain explicit. Coordinator/link-loss and authority-restoration behavior remain R2 review/host-acceptance dependencies (`B/design.md:233–235`; `B/astra_r1_verdict.md:24`; `IM:96,190,193`).

No SR v1–v4 mechanism, synchronous remote database shutdown, polling promise or science-triggered Intel termination deadline is incorporated. Existing M3 science-gate classifiers/exemptions remain unchanged. R2 real-pair acceptance must cover active transfer, coordinator death, interrupted pause, stale clearance and malformed/unavailable observations; RE interface fixtures cannot substitute for those receipts (`B/design.md:216,235,243`; `B/astra_r1_verdict.md:24`; `IM:96`).

### Acceptance and test accounting

Keep the AC identifiers and named test files as traceability slots. `test_science_reservation.py` becomes the RE consumer-interface slot for R2; its legacy filename confers no authority to implement SR or the coordinator. Freeze concrete Intel commands, receipt shapes, source paths and interface expectations before implementation. All remaining binary requirements, RED/GREEN and no-skip rules survive (`v5:27–33,35–57,76,198,225`; `r5:89`; `B/design.md:243–245`).

| AC/test | Disposition and rationale |
|---|---|
| AC1 / `test_freeze.py` | KEEP distinct author/builder and reviewed key; freeze base + this amendment + Intel source/dependency identities and the R2 dependency (`v5:37,73–76`; `B/design.md:244–245`; `B/astra_r1_verdict.md:24`). |
| AC2 / `test_environment.py` | KEEP isolation/allowlist/observed-lock equality; REPLACE M3 ARM/Homebrew assertions with section D's reviewed Intel identities (`v5:38,189–203,244–246`; `B/design.md:242`). |
| AC3 / `test_capture.py` | KEEP hashes, mutation rejection and attribution; REPLACE local-M3-worktree assumption with section A's immutable export/revision capture (`v5:39,143,248`; `B/design.md:244`). |
| AC4–AC15 / their twelve named tests | KEEP unchanged: vocabulary, actual oracle parity, canonicalization, negative controls, publication failures, pinned requests, rebuild, agent surface, authority, status separation, halted history and MathLab stop. The meanings do not depend on M3 hosting (`v5:40–51`; `B/design.md:244`). |
| AC16 / `test_storage_budget.py` | KEEP boundary/unavailable checks; REPLACE memit/installation path assertions with Intel-local 5+1 GB accounting, amendment-16 ceilings, concurrent peaks and headroom checks in section A (`v5:52,207–211,245`; `B/design.md:162,165`; `B/decisions_log.md:191`). |
| AC17 / `test_session_limits.py` | KEEP local cap/stop/RSS/priority/observation/shutdown controls with actual Intel receipts; REPLACE science-reservation predicates as detailed immediately below (`v5:53,213–217`; `B/design.md:243`; `B/astra_r1_verdict.md:47`). |
| AC18 / `test_receipt_integrity.py` | KEEP behavioral RED, production GREEN, round-trip/boundary/HALT diagnostics, no skips (`v5:54,76,225`; `B/design.md:244`). |
| AC19 / `test_scope.py` | KEEP protected hashes/concurrent drift/no Git mutation; REPLACE only host path bindings and remove the SR writer from RE builder scope (`v5:55,193–203`; `B/design.md:206–212,243`). |
| AC20 / `test_completion_packet.py` | KEEP MAESTRO verification, permitting Astra promote, currency-active closeout and PROMOTE_PENDING semantics; add Intel commissioning identities, not a fixture substitute (`v5:56,228–233`; `B/design.md:245`; `r5:93`). |
| AC21 / `test_science_reservation.py` | REPLACE entire SR authority implementation test with R2 allowance/pause-acknowledgment/unknown-coordinator consumer checks. Coordinator authority lifecycle, records, writer faults and clearance are separately frozen/tested in I1b, not dropped or defined here (`v5:57`; `B/design.md:235,243`; `IM:96`; `B/astra_r1_verdict.md:24`). |

AC17 subpredicates and the cited SR case references are accounted for as follows; none is a claim that old tests passed (`v5:53`; `r5:91–93`):

| v5 predicate/reference | Intel disposition |
|---|---|
| Valid IDLE plus exclusion check admits; pending/running refuses local RE code5 | REMOVED because the same-host premise is gone. REPLACE with a local-admission positive control during M3 science and an Intel-local query during disconnection; new shared-disk work still needs section B's allowance (`v5:53`; `B/design.md:233–235`). |
| Pending publish excludes RE admission/publication; invocation-bound pending exit0/exit3; lock-timeout intervening-admission termination | REMOVED for Intel RE because M3 science no longer excludes it. Ordering, affirmative clearance and bounded transfer failure remain I1b requirements, not relaxed local publication integrity (`v5:53,215`; `IM:171,179,189`; `B/astra_r1_verdict.md:24`). |
| Orphans with no living leader; non-RE token text; lstart mismatch | KEEP as local session-stop ownership protections; independently account for all launched processes/helpers, reject untagged/malformed identities, avoid signalling unrelated/reused identities. Transfer descendants are I1b's separate responsibility (`v5:53,197,217`; `r5:43–49`; `IM:172,178,188`). |
| Hung command 2 s cap; unusable SR root exits4 only after RE absence; clock jumps | REMOVE SR-command/root/exit rules because the authority root and science termination are removed. KEEP bounded local operations/stop and valid observations; require clock-independent elapsed-limit proof. R2 separately freezes real transfer timing/restoration/failure controls (`v5:53,172,217`; `IM:173,182–183,189–190`; `B/astra_r1_verdict.md:24,47`). |
| No watcher; breaches halt without cleanup | KEEP no RE-side science watcher, retain local halt/preserve/no-cleanup. This does not prescribe R2's mechanisms or waive local resource enforcement (`v5:53,215–217`; `B/design.md:235,237`; `B/astra_r1_verdict.md:47`). |
| SR §6 cases 1–3, 5–12, 18 | Old SR case suite removed from Intel RE acceptance with the predicate dispositions above. Local ownership/resource/stop controls survive in AC17; admission/pause/clearance/fault/restoration controls require R2's new frozen case mapping, not inherited SR PASS (`v5:53`; `r5:91`; `B/design.md:243`; `IM:96`). |

AC21's exact marker/active/log/lock semantics, any-entry-is-SCIENCE rule, root/listing/lock availability, launch-ID/coordinator schema, duplicate pending, failed writer/no-IDLE, running tokens, release inventory and RE lock-only writes all depend on SR. Remove those concrete implementation predicates; replace their safety classes with the reviewed R2 interface and controls, including failed creation/rename/durability and successfully validated observations. SR §6 cases 4 and 13–17 do not confer Intel acceptance; their replacement case/receipt mapping remains a required I1b freeze (`v5:57`; `IM:174,180,185,187,193`; `B/astra_r1_verdict.md:24`).

C6/C8 keep AC17/AC21 membership, interpreted as local Intel limits plus the reviewed transfer-interface dependency, not RE-for-science exclusion. Other C1–C9 memberships remain as written. Replace step 5a and the §13 admission row with Intel local start/normal/error/stop/RSS commissioning plus applicable R2 real-pair receipts before promote. The old SR writer allowlist/token-pattern binding is removed; Intel invocation/ownership forms must be frozen consistently for every administrative, query, JVM and permitted capture-helper path, with independent launched-process accounting. Neither a matcher nor its own zero-match result is a sufficient commissioning oracle (`v5:61–80,196–198,217,244,247–248`; `r5:43–49,93`; `IM:176,188`; `B/astra_r1_verdict.md:47`).

Historical SR references in v5's version header and change tables remain historical; they do not reactivate the superseded hosting/admission requirements (`v5:3–7,253–290`; `B/design.md:239–245`).

## C. V7 — explicit no-resume rule

**No automatic resume.** Any RE session ended by a cap, stop, revocation or timeout stays ended. A surviving controller, restored link/coordinator or subsequent M3 idle state cannot restart it. Any later RE session requires explicit MAESTRO admission under the reviewed frozen scope, current source/code identities and remaining allowance; stable IDs do not renew consumption. Intel-local work that never ended may continue. This restores the omitted rule, rather than treating autostart restrictions as equivalent (`RE/phase1_spec_v4.md:213`; `r5:69–73`; `IM:192`; `v5:185,217`; `B/design.md:233,237`).

AC17 must cover each local termination trigger and prove no controller-driven restart; AC12's descriptive approvals remain unable to dispatch/resume. A paused transfer is governed separately by R2's explicit reviewed resume rule; this amendment supplies none (`v5:48,185`; `IM:192`; `B/astra_r1_verdict.md:24`).

## D. Intel provisioning repin (design item 2; I1c)

MacPorts replaces Homebrew on Intel. The setup log records Intel macOS 14.8.9/x86_64 and MacPorts base 2.12.6 installed with no ports at 08:17Z. These are dated receipts to recheck, not current dependency acceptance. Amendment 18's permitting review covers the package manager only; it does not approve RE packages (`IS/setup_log.md:13,26–27`; `B/decisions_log.md:200–210`; `B/astra_a18_verdict.md:1–3,13,19–21`).

Every row below is **PENDING-CHECK**. No opened source establishes a Neo4j/Java/Python/DuckDB or library port/upstream artifact for this Intel host; those candidates are **UNKNOWN — check**, including version, revision, dependency closure, archive/source/wheel hash and native compatibility. Search strings below are discovery terms, not assertions that a port exists. MacPorts-base/OS candidates alone have dated source receipts (`IM:97`; `B/design.md:242`; `B/decisions_log.md:210`; `IS/setup_log.md:13,27`).

Run the following read-only commands on Intel only, by MAESTRO. First run `/opt/local/bin/port help search`, `/opt/local/bin/port help info` and `/opt/local/bin/port help deps` to verify the installed CLI interface; missing tools, empty results, errors or unexpected output remain unresolved rather than selecting a default. Discovery output alone cannot establish a pin. The table accounts for every v5 §13 dependency and all six M3 upgrades (`v5:244–246`; `RE/preinstall_identity_20261011.tsv:1–11`).

| Dependency | v5 value/source | Intel candidate (port or upstream artifact) | Status | Exact read-only Intel check command |
|---|---|---|---|---|
| Host OS/architecture | macOS 26.6.2; ARM paths/bottles (`v5:189,244`; `RE/preinstall_identity_20261011.tsv:5–11`) | Recorded macOS 14.8.9 x86_64; recheck (`IS/setup_log.md:13`) | PENDING-CHECK | `/usr/bin/sw_vers` then `/usr/bin/uname -m` |
| Package manager | Homebrew 7.0.9 (`v5:244`) | MacPorts 2.12.6 base; `MacPorts-2.12.6-14-Sonoma.pkg`, SHA-256 `184ac171c201391a502958951867e77062010c781ade302b70b1f176e42d23d6` (`IS/setup_log.md:25–27`) | PENDING-CHECK | `/opt/local/bin/port version`; `/usr/sbin/pkgutil --pkg-info org.macports.MacPorts`; `/usr/bin/shasum -a 256 "$HOME/Downloads/MacPorts-2.12.6-14-Sonoma.pkg"` |
| Neo4j Community | `neo4j` 2026.09.0; old artifact identity retained in manifest (`v5:244`; `RE/preinstall_identity_20261011.tsv:3`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search neo4j` |
| cypher-shell | 2026.09.0 (`v5:244`; `RE/preinstall_identity_20261011.tsv:4`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search cypher` |
| Java/JDK | `openjdk@21` 21.0.12.1, ARM bottle (`v5:244`; `RE/preinstall_identity_20261011.tsv:5`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search openjdk` |
| CPython | 3.12.14; uv macOS-aarch64 interpreter (`v5:189,246`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search python312` |
| DuckDB Python artifact/lock | `duckdb==1.5.5`; `duckdb_1.5.5.lock.txt` SHA-256 `f8ffcdeadaded28928249cf8b468a25e9cf25e8a1a6b028b22deed8757c28636`; 35-wheel set, selected ARM cache not Intel proof (`v5:189,246`; `r5:20,103`) | UNKNOWN — check; requires a reviewed macOS x86_64 wheel/artifact and exact lock membership | PENDING-CHECK | `/opt/local/bin/port search duckdb`; `/usr/bin/shasum -a 256 results/research_engine_phase1_20261011/duckdb_1.5.5.lock.txt` from the admitted Intel source root |
| libpng | Homebrew upgrade 1.6.58 ->1.6.59 (`RE/preinstall_identity_20261011.tsv:6`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search libpng` |
| pcre2 | Homebrew upgrade 10.48 ->10.49 (`RE/preinstall_identity_20261011.tsv:7`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search pcre2` |
| glib | Homebrew upgrade 2.88.3 ->2.90.1 (`RE/preinstall_identity_20261011.tsv:8`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search glib` |
| xorgproto | Homebrew upgrade 2025.1 ->2026.1 (`RE/preinstall_identity_20261011.tsv:9`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search xorgproto` |
| cairo | Homebrew upgrade 1.18.4 ->1.18.6 (`RE/preinstall_identity_20261011.tsv:10`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search cairo` |
| harfbuzz | Homebrew upgrade 14.4.0 ->14.6.0 (`RE/preinstall_identity_20261011.tsv:11`) | UNKNOWN — check | PENDING-CHECK | `/opt/local/bin/port search harfbuzz` |

The six-library approval **is not carried over**: answer 2 approved the M3 Homebrew install's six shared upgrades. Intel prospective actions and transitive dependencies need their own exact inventory and reviewed authorization; similarly named ports are not inherited approvals (`RE/operator_answers_20261011T0518Z.md:5`; `IM:97`; `v5:244`; `B/decisions_log.md:210`).

**Ports-tree pinning precedes provisioning.** Do not run unpinned `port selfupdate`: it can sync the tree and upgrade base. MAESTRO's reviewed Intel provisioning brief must select the exact ports-tree revision/content hash, acquisition identity and frozen source location, and pin every selected port version/revision/variant and archive or source digest, including dependencies. None is supplied here. Read-only first-stage checks are `/opt/local/bin/port installed` and `/bin/cat /opt/local/etc/macports/sources.conf`; the latter reports configuration, not a proven immutable tree. A missing/unpinned tree keeps I1c pending (`IS/setup_log.md:27`; `B/decisions_log.md:210`; `IM:97`).

After an actual candidate is identified and its CLI shape checked, MAESTRO runs `/opt/local/bin/port info "$INTEL_PORT"` and `/opt/local/bin/port deps "$INTEL_PORT"` with `INTEL_PORT` set to the exact reviewed candidate, then freezes its full identity/closure. For an upstream artifact, independently freeze its source, edition, macOS-14/x86_64 support evidence and SHA-256. Hash the actual selected package/wheel with `/usr/bin/shasum -a 256 "$INTEL_ARTIFACT"`; both variables must be nonempty reviewed values, never guesses or automatic substitutions. A search result or version string does not establish the archive hash or runtime compatibility (`v5:244–246`; `B/design.md:242`; `B/decisions_log.md:210`; `B/astra_a18_verdict.md:19–21`).

Before any install, freeze the identity manifest and recheck against it. Record actual installed versions/hashes and native interfaces after separately authorized provisioning. The MacPorts manifest must replace the old Homebrew bottle/dry-run baseline and its `/opt/homebrew` paths, not relabel them Intel acceptance. Preserve the dedicated environment, dependency exclusions, localhost authenticated HTTP transaction API, Community edition, secret handling, isolated JSON vocabulary and fixed-query constraints (`v5:189–191,203,244–246`; `B/design.md:242`; `B/decisions_log.md:210`).

For later read-only verification, after approved installation and reviewed absolute paths exist, run:

```sh
: "${RE_PY:?reviewed Intel interpreter path required}"
: "${INTEL_JAVA:?reviewed Intel Java executable required}"
: "${INTEL_NEO4J:?reviewed Intel Neo4j executable required}"
: "${INTEL_ARTIFACT:?reviewed Intel artifact path required}"
"$RE_PY" -I -B -c 'import sys,platform,duckdb; print(sys.version); print(platform.machine()); print(duckdb.__version__); print(duckdb.__file__)'
"$INTEL_JAVA" -version
"$INTEL_NEO4J" --version
/usr/bin/shasum -a 256 "$INTEL_ARTIFACT"
/bin/df -k /
/usr/bin/du -sk /opt/local
```

These commands do not start databases, build the engine or install anything. They are pending MAESTRO checks; runtime version/hash receipts, actual HTTP/config/start/stop/RSS commissioning, interpreter/wheel platform proof, and before/after growth accounting remain required. The reviewed provisioning brief must run/help-check each selected executable before relying on its flags and freeze concrete smoke/receipt shapes; no Intel receipt exists in RE1 (`v5:31,217,224,228,244–246`; `IM:97`; `B/design.md:242,245`).

**Stop for review** if a required native package/version/edition is unavailable or incompatible, or identities do not match. No silent fallback to Homebrew, cloud, Linux VM, different version or edition. A hosting alternative needs reviewed change and its own budget. MacPorts installation alone authorizes no RE provisioning (`B/decisions_log.md:210`; `B/design.md:242`; `B/astra_a18_verdict.md:3,19–21`).

## E. Question 2 — MAESTRO reading for Astra to check

Answer 1 was recorded as approximately 05:15Z: add the note before a science run starts waiting, remove it at the end, RE yields, science safety gates unchanged. Its qualification says a redesign changing that shape goes back to the operator (`RE/operator_answers_20261011T0518Z.md:1–4,7`; `IM:200`).

MAESTRO's reading submitted for Astra checking: that condition is met by **the operator's own later choice 9**, recorded 06:30:29Z. The approved question explicitly keeps Intel databases/builders working from local files while M3 runs science, pauses large memit operations under M3 coordination, and requires MAESTRO to amend and re-review the rejected same-host spec. This is subsequent operator approval of the changed shape, not an inference that the earlier answer approved it. No additional approval of this division is implied to be missing; mechanics and acceptance still require the new reviews (`B/decisions_log.md:115–121`; `B/design.md:224,230–245`; `IM:200`).

The note-before-waiting step survives as the coordinator's pending-science signal **if the frozen I1b interface keeps that step**. The step then gates shared-disk transfers, not Intel-local database compute. R2 must reconcile the signal/end-of-run behavior with its reviewed lifecycle; this paragraph does not freeze a folder, schema or removal mechanism (`RE/operator_answers_20261011T0518Z.md:4,7`; `B/design.md:235`; `B/astra_r1_verdict.md:24`).

## F. Preserved semantics and review gates (design item 4)

Preserved unchanged: original files/Git evidence authority; distinct independent answer-key author and builder; five-chain scope; reviewed link meanings; paired-store publication and pinned generations; coverage, age, refusal and status-separation semantics; MAESTRO verification, permitting Astra promote and currency-active closeout gates. Intel source capture changes physical placement only. No query receives execution authority, no moved database closes F1, and no fixture acceptance substitutes for host or scientific evidence (`B/design.md:244`; `v5:15–21,37–57,73–92,108–122,126–155,172–185,223–233`).

The completion packet adds base/amendment hashes, exact Intel host/platform/dependency/source/path identities, AC replacement mappings, independent process-accounting and local commissioning receipts, and the separately reviewed R2 version/consumer/real-pair receipts. MAESTRO names the Intel KEY1/BUILD1 sessions before dispatch; the M3 session names are historical assignments, not proof of Intel dispatch. Builder delivery stays ENGINEERING_GREEN/PROMOTE_PENDING until the external gates are satisfied (`v5:73–80,221–233,243`; `IM:95,205`; `B/design.md:245`).

## G. Findings disposition (design item 5; all 23 IDs)

The integration map's eight “already resolved” findings remain resolved as historical review dispositions; relocation does not reopen their old defects. The other fifteen are replacement requirements, not accepted implementations. Only the same-host RE-for-science premise is removed; applicable transfer/Intel-local remainders remain. “Replaced” below means an obligation assigned, not a GO verdict or completed test. R2 requirements remain open pending that separate freeze and real-pair acceptance (`IM:165–167,195,199`; `B/astra_r1_verdict.md:24,45–47`; `B/design.md:245`).

- **T1:** already resolved; ordering class replaced by section B's R2 admission-ordering dependency, still pending (`IM:171`; `B/astra_r1_verdict.md:24`).
- **T2:** science-triggered RE termination premise removed; replaced by section A local bounded shutdown and section B/R2 transfer ownership/coordinator-loss requirements, acceptance still open (`IM:172`; `B/astra_r1_verdict.md:24,47`).
- **T3:** replaced by section A local elapsed-limit proof and R2 real-interface bounded pause/clearance outcome; still open (`IM:173`; `B/design.md:235`; `B/astra_r1_verdict.md:24`).
- **T4:** replaced by R2 clearance/release/restoration requirements consumed through section B; still open (`IM:174`; `B/astra_r1_verdict.md:24`).
- **T5:** already resolved; unchanged M3 gates and cooperative limitations preserved, with no claim of universal protection from relocation (`IM:175`; `B/design.md:216`; `B/astra_r1_verdict.md:47`).
- **T6:** already resolved; section B replaces SR commissioning with actual Intel local commissioning and applicable R2 receipts before promote; acceptance still open (`IM:176`; `r5:93`; `B/design.md:245`).
- **T7:** already resolved historically; section D/I1c requires a new Intel preinstall identity baseline, still open (`IM:177`; `B/design.md:242`; `B/decisions_log.md:210`).
- **U1:** already resolved; section B retains independent local owned-process accounting and shutdown, with completeness tracked under V3; Intel acceptance still open (`IM:178`; `r5:8,43–49`; `B/astra_r1_verdict.md:47`).
- **U2:** already resolved; R2 must independently satisfy ordering/affirmative-clearance evidence; interface acceptance still open (`IM:179`; `B/astra_r1_verdict.md:24`).
- **U3:** replaced by R2 launch completion/quiescence and release eligibility; still open outside this amendment (`IM:180`; `B/astra_r1_verdict.md:24`).
- **U4:** already resolved; removed handshake/registry stay removed; section B requires V1/V3 replacement coverage and Intel commissioning (`IM:181`; `r5:14`; `B/astra_r1_verdict.md:47`).
- **U5:** replaced by section A local bounded elapsed outcomes and R2 terminal-deadline proof; still open (`IM:182`; `B/astra_r1_verdict.md:24,47`).
- **U6:** science RE-absence exception removed; replaced by R2 coordinator/link-loss/restoration and valid-observation requirements; still open (`IM:183`; `B/astra_r1_verdict.md:24,45–47`).
- **U7:** already resolved; original clean DuckDB lock defect stays resolved; section D requires actual Intel artifact/hash/platform repin, still open (`IM:184`; `r5:20`; `B/design.md:242`).
- **U8:** replaced by R2 validated records and creation/rename/durability fault controls; still open (`IM:185`; `B/astra_r1_verdict.md:24`).
- **V1:** science-driven Intel termination premise removed; section A local resource/stop enforcement and R2 admitted-transfer authority/coordinator-failure outcomes remain required and open (`IM:186`; `B/astra_r1_verdict.md:24,45–47`).
- **V2:** replaced by R2 registration/completion/cancellation/release lifecycle requirements; still open (`IM:187`; `r5:35–41`; `B/astra_r1_verdict.md:24`).
- **V3:** replaced by section B consistently frozen Intel invocations/helpers and independent process-accounting commissioning; transfer descendant ownership remains R2; still open (`IM:188`; `r5:43–49`).
- **V4:** replaced by local bounded-stop evidence and R2 deadline tests including blocked output and surviving mutation descendants; still open (`IM:189`; `r5:51–55`; `B/astra_r1_verdict.md:24,47`).
- **V5:** old Intel RE science-clearance premise removed; R2 must prevent stale clearance after authority restoration; still open (`IM:190`; `r5:57–61`; `B/astra_r1_verdict.md:24`).
- **V6:** replaced by R2 command-identity/negative brief-text control and unchanged M3 collector gate obligations; still open in R2/R4 (`IM:191`; `r5:63–67`; `B/astra_r1_verdict.md:28`).
- **V7:** replaced by section C's explicit No automatic resume requirement and retained AC17/AC12 controls; Astra disposition and Intel behavioral proof still pending; transfer resume separately belongs to R2 (`IM:192`; `r5:69–73`; `RE/phase1_spec_v4.md:213`).
- **V8:** replaced by section B's dependency on R2 failed-mutation/validated-inventory controls; local unavailable observations still block; acceptance remains open (`IM:193`; `r5:75–81`; `B/astra_r1_verdict.md:24,47`).

Fresh permitting Astra review of the base plus amendment, completed Intel repin/provisioning review, frozen R2 dependency and actual commissioning receipts are required before reliance. Relocation does not convert r3/r4/r5 NO-GO into GO (`B/design.md:245`; `IM:95–97`; `r5:2,83–93`).
