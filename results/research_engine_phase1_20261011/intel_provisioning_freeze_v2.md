# R1 — Intel provisioning freeze v2 (R1B; review draft)

**Document delivery only. Installation and commissioning remain blocked.** This is one proposed package set, one JSON manifest and prospective read-only collectors/comparison guards. Missing observations remain explicit; a procedure does not discharge a missing pin or demonstrate a budget bound (`V:3,12-17,69-77`).

Citation aliases (file:line): `RE` = `results/research_engine_phase1_20261011`; `V` = `RE/astra_r1p_verdict.md`; `P` = `RE/intel_provisioning_freeze_v1.md`; `F` = `RE/intel_r1_facts_20261011.md`; `Z` = `RE/intel_r1_sizes_20261011.md`; `TS` = `RE/intel_r1_sizes_20261011.tsv`; `RC` = `RE/intel_r1_runtime_closure_20261011.txt`; `A` = `RE/phase1_intel_amendment_v1.md`; `D` = `results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md`; `L` = `RE/duckdb_1.5.5.lock.txt`; `LP` = `RE/duckdb_lock_parse_receipt_20261011.txt`. `J` = `RE/intel_provisioning_manifest_v2.json`; `H` = `RE/r1b_host_commands.sh`. JSON pointers identify authoritative fields; line references below identify their containing section. New commands, allowances and predicates are **R1B proposed requirements**, never observations or approvals.

## F1 — Five freeze bullets, selected candidate and honest admission boundary

Addresses `V:7-17`. The candidate is MacPorts Python 3.12.15, archive-delivered openjdk21, upstream Community 5.26.32 LTS and **locked DuckDB 1.5.5**, with five explicitly source-built ports. This changes two technical pins and needs technical review; no operator budget change is inferred (`RC:13,16`; `TS:11,14,20`; `L:1`; `V:52-59`). The existing source tree/base/OS are baselines, not selected reinstalls (`F:7-12`; `P:24-31`).

`J:35-99 /selection` is the proposed single candidate, `/artifacts` contains its identities and missing pins, `/paths` is the proposed Intel-local layout, `/budget` carries accounting, and `/commissioning` binds future R3 inputs. These fields are not a completed lock while unresolved statuses remain. See R1 for the preinstallation gaps and R5 for later native acceptance. Keep I1c pending (`V:17,69-77`).

## F2 — Retained tar provenance, signatures and effective content

Addresses `V:19-21`. The retained tar expectation in `J /artifacts[id=ports-tar]` is **reported and unverified**. Its source is `F:10`; Astra found the cited raw script did not hash the retained `remote/` file. Its mtime is neither an acquisition receipt nor proof of trust (`V:20-21`). Full expected digests occur only in J; the Markdown does not duplicate them.

Prospective `H tree J` hashes the correct retained path, indexes, key and all signature material; compares known expected digests/length/commit and the exact active source; streams the retained tar and compares effective file bytes and symlinks; rejects extras except J's explicit derived-index allowlist. This includes recipes, PortGroups, patches and supporting files rather than selected Portfiles alone (`F:7-10`; `V:71`; R1B proposed control). No full tree extraction is planned. Unknown tar layout/hardlink semantics refuse pending a reviewed mapping.

`H inventory J` records the installed Tcl signature-verification implementation, raw key/signature digests and configuration. **No digest algorithm is guessed.** `H tree J` refuses signature acceptance until J pins the reviewed algorithm/method receipt and key/signature hashes. Its frozen verification vector is `/usr/bin/openssl dgst -<J algorithm> -verify <J key path> -signature <J signature path> <J tar path>`, with exit 0 and nonempty verification output required. Raw acquisition time/provenance still needs a receipt; a fresh hash cannot retroactively prove it (`V:21,71`).

## F3 — Numerical conservative peak plan and the complete provisioning clock

Addresses `V:23-29`. Amendment 20 changes setup to **2,000,000,000 bytes**, pilot stays **5,000,000,000**, combined becomes **7,000,000,000**; provisioning remains **900 seconds**. Exceeding or failing to bound a limit stops before mutation for operator disposition. Amendment 21's recovery de-duplication does not lend its headroom to setup (`D:218-228,230-238`; `A:32-36`; `V:27`).

The following table is derived from `J /budget/components`. Measured decompressed sizes include tar headers, hence bound the single installed payload rather than measure actual installation. Every allowance is an unmeasured planning ceiling that must be independently justified and enforced. Summing them assumes coexistence; serialization does not remove retained directories (`Z:6-8,17-30`; `TS:1-17,20`).

| Peak component | Bytes | Basis and admission condition |
|---|---:|---|
| 17 MacPorts image archives + activated payloads | 913,638,545 | Measured: compressed 255,364,241 + decompressed 658,274,304 (`TS:1-17`). |
| Neo4j LTS retained tar + one payload | 317,679,241 | Measured: 152,610,441 + 165,068,800 (`TS:20`). |
| One extra image/activation copy | 355,446,784 | Conservative allowance based on largest measured payload (`TS:11`); only one extra image at a time. |
| Three unmeasured selector/dejagnu archives + payloads | 20,000,000 | Allowance; identities absent from 17-row measurement (`RC:3,18,20`; `TS:1-17`). |
| Source downloads and patches | 20,000,000 | Allowance for the complete admitted source inputs (`Z:12`). |
| Aggregate source build directories | 50,000,000 | Allowance; all retained build work counts, not just active compiler (`Z:12`; `V:27`). |
| Source-built images + activated files | 30,000,000 | Allowance; source output archive and installed bytes coexist (`Z:12,17`). |
| Locked 1.5.5 wheel + installed copy | 130,000,000 | Allowance: compressed <=30 MB, extracted <=100 MB; **1.5.6's measured wheel is not evidence for 1.5.5** (`Z:13`; `L:1-36`). |
| Environment and pinned bundled installer | 30,000,000 | Allowance; no full Python/stdlib copy (`P:58,157-182`). |
| Verification extraction | 20,000,000 | Allowance: streamed archive inventories, bounded selected temporary members; no whole-tree duplicate (`V:27`). |
| Other caches, registry and temp growth | 25,000,000 | Allowance; all actual write roots must enter J/preinventory (`A:36`; `V:27`). |
| Additional retained failure evidence | 70,000,000 | Allowance; first failure stops, no retries/copies; retained image/build work already charged above (`V:27`; `A:32,36`). |
| Receipts and logs | 10,000,000 | Allowance; no unbounded process/file dumps (`V:27`). |
| **Conditional candidate peak** | **1,991,764,570** | **8,235,430 bytes margin. Not a demonstrated bound.** |

The calendar-line substitution adds 256,002,195 bytes (`TS:19-20`), producing **2,247,766,765**, exceeding the cap by **247,766,765** under this same plan. That candidate refuses without operator budget disposition or a separately reviewed, evidenced reduction. The LTS candidate also refuses while source-build workspace, three missing archives, actual image/activation behavior or other write roots remain unbounded. The candidate performs acquisition on Intel and retains only one copy of each input. Extra retained M3 copies or transfer duplicates require an amended numerical plan before any acquisition. The small remaining margin is no evidence of fit (`V:27,73`; R1B calculation from table).

Clock start: before the first provisioning-related write on **either Mac**, including acquisition mktemp creation, downloads, temporary verification, source builds and staged payloads. Earlier research streaming is historical evidence, never an exemption for later acquisition (`Z:3`; `V:27`). Clock stop: only after setup installed-payload/route/closure checks and before/peak/after accounting receipts are durable. Sum all phases across staged sessions; waiting, failure and retained work do not reset the clock. Native session commissioning has its separately bounded 30-minute session clock (`A:32`).

| Phase | Unmeasured allowance, seconds |
|---|---:|
| Preinventory and baseline pin checks | 60 |
| Acquisition | 240 |
| Archive/signature/payload verification | 90 |
| Five source builds | 180 |
| Port image/activation | 60 |
| Neo4j + environment + locked wheel | 90 |
| Postinstall comparison | 60 |
| Reserve | 90 |
| **Total** | **870 (30 seconds below 900)** |

This is a proposed schedule, **not time admission evidence**. `Z:30` calls time plausible but unmeasured. Source compile/activation/verification timings and throughput must bound the schedule before dispatch; inability to bound them stops for operator budget/scope disposition (`V:27,73`). A future external monotonic controller must stop writers at 900 s and retain receipts; a timer inside a stalled installer is insufficient (R1B proposed control).

## F4 — Executable comparisons, held coordination and source identity chain

Addresses `V:31-35`. `H:301 /admission` implements `H guard J <independent-observation.json>`. It compares observed host/artifact/tree/path identities against J and exits nonzero for missing pins, mismatches, missing signatures, extra preinstalled ports, bad pool math, unbounded budgets or missing authorization/writer reservation. It contains no install operation. The required observation JSON has `host` (the compared J host keys), `artifacts` keyed by entry ID (observed `version_revision`, `variants`, `source_url`, `sha256`, `size_bytes`, `route`, and `signature_verified`), exact `tree` and `paths`, `preinstalled_ports`, numeric `projected_setup_peak_bytes`/`projected_provisioning_seconds`, `pools` (free/projected bytes), and affirmative `writer_reservation_matches`/`no_queued_external_writers`. Collectors preserve raw inputs; MAESTRO must review their normalization against this schema before admission (R1B proposed interface). `H:332 /compareinstalled` implements `H compare-installed J`. It compares payload digests/types/modes/symlinks and registry-owned file/port sets against admitted image/build manifests; mere recording is not acceptance (`V:33-35`).

R1B proposed coordination: MAESTRO reserves the Intel host, exact J bytes and every package/tree/config/cache writer from first precheck through final postcheck; external or queued writers must be suspended/drained. A local exclusive lock in the authorized setup/control root must span this window, and the same reservation is required of every potential writer. Missing ownership/completeness observation refuses. A check followed by releasing coordination before install is forbidden (`P:33`; `V:33`). No lock is acquired in this task.

Per-port exact proposed install vectors live only in `J /artifacts/*/proposed_install_argv`. Archive entries use `/opt/local/bin/port -N -b install <name> @<version_revision> <variants>`; the five source entries use `-N -s` after their **entire pinned build prerequisite set is already installed**. `-b` must refuse unavailable archives; `-s` must never convert an archive-designated dependency into an unreviewed build. The help/interface receipt and topological prerequisite order are blocking J fields; these vectors are not dispatch-ready until they are validated against installed MacPorts (`V:33,75`; `Z:12`; R1B proposed route controls). No sync, selfupdate, automatic mirror-content substitution, retry, version change or package-manager alternative is permitted (`F:12`; `D:210`).

For each source build, freeze reviewed recipe/PortGroups/patches, complete source hashes, toolchain/SDK/flags and build-only closure. Under separately authorized bounded staging, create a preactivation payload manifest from the resulting image and bind it to those inputs and the builder receipt. Admit that image identity through review, then activate exactly that image under the held reservation; compare installed files to it. Generated files need exact path/type/mode/generation rule and bounded size in J, never a wildcard exception. Final output hashes are **observed after build**, not invented before it (`V:35,75`). Exact staging-to-activation interfaces remain missing; source-only `install` by itself does not prove this chain.

## F5 — Commissioning binding and the unresolved R3 dependency

Addresses `V:37-46`. Each future commissioning check in R5 names a J entry. A spec document named “r3” is not evidence of a reviewed external stop-controller/workload implementation. The supplied bar requires its exact version/hash/commands, independent ownership, bounded stop and no-resume observations (`V:44-46,77`). J marks the controller, workload and its review **BLOCKED-R3-ARTIFACT**; there is no substituted controller here.

R1B proposed niceness launcher, inside the future externally controlled process: `n=os.getpriority(os.PRIO_PROCESS,0); os.nice(max(0,10-n)); assert os.getpriority(os.PRIO_PROCESS,0)==max(10,n); os.execve(<J neo4j console executable>,<J console argv>,<J frozen environment>)`. It preserves inherited 0→10, 10→10, >10 unchanged. Run all three inherited-priority controls before acceptance, then observe **every owned descendant**, not only the launcher (`A:31`; `V:44,46`). Credentials and response parsers must be frozen from the admitted shell/server interface before startup; R5 defines fail-closed requirements, not a guessed interface.

## F6 — Recommendations and the technical-review boundary

Addresses `V:48-61`. These are recommendations for MAESTRO/Astra technical review, **not decisions or approvals**:

- **Neo4j: recommend Community 5.26.32 LTS for this candidate.** Its measured tar/payload pair is smaller (`TS:19-20`); the calendar line exceeds the conservative candidate cap in F3. Unlike Astra's v1 preference to preserve 2026.09.0, this recommendation needs a substantive line-compatibility amendment. Verify LTS Java/macOS/x86_64, configuration, transaction HTTP, matching shell and shutdown interfaces; do not transfer the 2026.09 requirements receipt to LTS (`F:29`; `V:53,61`).
- **Python: recommend pinned MacPorts 3.12.15_0 +lto+optimizations.** Its archive is measured (`TS:14`); changing 3.12.14 needs a reviewed patch amendment and native ABI/linkage evidence. The source 3.12.14 alternative is excluded from this candidate, with no automatic change on failure (`V:52`; `F:18`).
- **DuckDB: recommend exact 1.5.5 Intel cp312 wheel satisfying L.** Neither the measured 1.5.6 PyPI wheel nor the unavailable pinned MacPorts 1.5.6_1 archive satisfies L. `H wheel J duckdb-wheel` selects only one compatible cp312/x86_64 candidate, verifies lock membership and downloaded bytes, captures WHEEL/METADATA, and refuses ambiguous/over-limit selection (`L:1-36`; `Z:13`; `V:54`).
- **Delivery: recommend verified binary archives for the measured 17 and explicitly reviewed source plans for the five missing ports.** Three other closure members still lack artifact identities. There is no fallback when an exact archive/source plan is absent (`Z:11-12`; `RC:1-25`; `TS:1-17`; `V:55`).

These technical changes do not themselves require a separate operator approval. A change to budget, hosting, edition, approved behavior or another operator constraint does (`V:59-59`; `D:210,228`). Amendment 20 is the only setup-budget change used here; Amendment 21 applies to recovery only (`D:218-238`).

Neo4j's recorded 10 GB development guideline applies to the 2026.09 requirements page, not a measured archive/pilot size. Proposed disposition: development-only/local/Community remains fixed; **do not assert that the 5 GB pilot conforms to a 10 GB vendor guideline**. Obtain LTS-specific requirements and a reviewed small-pilot capacity/compatibility exception or remain blocked; this is technical compatibility review unless it changes an operator constraint (`F:29`; `V:29,59`).

## F7 — Status vocabulary and provenance separation

Addresses `V:63-65`. **EXPECTED-PIN** fixes an expectation; **REPORTED-PIN-NEEDS-FETCH** records an earlier report; **NEEDS-FETCH** identifies missing identity/evidence; **BLOCKED-R3-ARTIFACT** means an implementation/review package has not been supplied. **PROPOSED** means a reversible technical recommendation/layout. None means installed, verified or approved. Only a reviewed receipt can promote an artifact to verified identity. Native compatibility and commissioning remain separate later evidence (`V:17,46,65,85`).

## R1 — Single manifest, closure, paths and authorization

Addresses `V:69`. J is the only expected artifact manifest (`J:134-1353 /artifacts`); Markdown uses entry IDs and never repeats expected hashes. It contains name, version_revision, explicit/archive-observed variants, source URL, expected SHA256 or NEEDS-FETCH with collector command, byte size/basis, delivery route, evidence and status for every entry. The existing immutable L still governs DuckDB membership; J pins L's own identity rather than duplicating its 35-hash set (`L:1-36`; `LP:8`).

The runtime list has 25 members (`RC:1-25`). The measured archives cover 17 (`TS:1-17`). Source-only set: expat, sqlite3, python_select, python3_select, tcl (`Z:12`). **dejagnu, python_select-312 and python3_select-312 remain unresolved archive identities**; no inferred noarch archive is admitted (`RC:3,18,20`; `TS:1-17`). Full direct dependency edges, effective positive/negative variants, evaluated source/patch URLs and the five builds' build-only closure are still NEEDS-FETCH. “No build deps beyond CLT” in the summary is not a substitute for those evaluated edges (`Z:12`; `V:12,69`). Every newly discovered prerequisite needs a J artifact row and budget before mutation.

`J:101-120 /paths` adopts P's proposed Intel-local root/layout with the LTS install version, not an observed realpath (`P:186-203`; `A:20`). `H inventory J` captures owners/modes, realpaths/devices, logical/allocated bytes, full configs and baseline ports. Freeze compiler/SDK/native libraries and actual installer/cache/temp paths; reject symlink/mount resolution through M3/memit and account for other write roots. Pool identity must distinguish shared APFS free space; do not sum `/` and Data views (`F:34`; `A:34-36`). Existing `port installed` was empty in the prior report, not a current observation (`F:22`).

Authorization fields in J remain false. Raw evidence collection, builds, installation and session commissioning are distinct boundaries. This document alone authorizes none. Only reviewed technical amendments and separately recorded MAESTRO/operator authority can resolve those fields (`D:210`; `V:3,69`).

## R2 — Raw receipt collection without manufacturing provenance

Addresses `V:71`. Prospective commands, from the worktree or admitted export root:

```bash
bash results/research_engine_phase1_20261011/r1b_host_commands.sh inventory results/research_engine_phase1_20261011/intel_provisioning_manifest_v2.json
bash results/research_engine_phase1_20261011/r1b_host_commands.sh tree results/research_engine_phase1_20261011/intel_provisioning_manifest_v2.json
```

Run those host-dependent modes **on Intel only**, through MAESTRO's separately authorized read-only SSH session. Other `fetch`, `wheel`, `archive-index` and `inspect` modes may be run on either Mac under an accounted acquisition window; the F3 candidate budget permits only Intel acquisition without extra retained transfer copies; use the corresponding command in each J row. Every file write is beneath a retained `/private/tmp/r1b.*` mktemp directory; no install/build/service/cleanup command exists in H (R1B designed restriction). The read-only verifier is an existing Python >=3.9 tool, default `/usr/bin/python3`; missing tool refuses, no bootstrap. Its identity must be recorded separately from the provisioned Python.

After the first inventory command prints `RETAINED_MKTEMP`, set `export R1B_FETCH_RECEIPT_DIR=<that exact /private/tmp/r1b.* path>` in the same authorized collection shell. All acquisition commands require that retained directory and reuse verified cached bytes; partial acquisitions refuse without retry/overwrite. Each invocation adds a fresh receipt namespace. H's 900-second timer bounds only that invocation; the separately required external provisioning controller must account for the entire staged window across calls. Raw tar/key/signature digests and command exit/stdout/stderr must be attached, admitted into J and compared on replay. `source-plan` gathers exact recipe/dependency inputs but cannot resolve unmeasured build outputs or retroactive acquisition provenance. `r3` verifies supplied reviewed local package bytes or refuses missing paths/pins; it cannot author a missing controller. These are explicit non-fetchable gaps, not hidden successful fetches (`V:21,35,46,71,77`).

## R3 — Admission math, time evidence and operator disposition

Addresses `V:73`. F3 defines the candidate plan; `J:1354-1506 /budget` is its numerical authority. Admission additionally requires, per physical pool, `free >= projected_additional_peak + max(80,000,000,000,21,474,836,480)`; count existing usage and concurrent writers once, do not borrow recovery/builder/pilot quotas (`A:34-36`; `D:224-228`). Logical decimal setup growth includes every installation/image/cache/temp/build/receipt location, even outside the RE root. Retain prescribed `du -sk` and actual allocated/free observations too (`A:36`; `P:209-219`).

**Current disposition: no demonstrated preinstallation space/time bound.** The allowances, throughput and source build work/time need evidence; a read-only collector cannot measure a compile/installation it is forbidden to execute (`Z:12,30`; `V:27,73`). Before mutation, MAESTRO must either establish the existing candidate bounds through separately reviewed evidence or submit a concrete revised setup/time scope/budget proposal. The calendar candidate would need at least 247,766,765 additional bytes under this accounting; the LTS candidate has only 8,235,430 bytes margin. No increased limit is chosen here (F3 calculation).

## R4 — Refusal sequence, delivery routes and payload comparisons

Addresses `V:75`. Prospective entry sequence under a continuously held authorized writer reservation:

1. Run the host/content/signature collectors; review/fill J without changing the acquisition tree. Bind J bytes to the signed-off receipt and reservation.
2. Acquire **only** J artifacts in bounded retained mktemp/staging locations; hash actual bytes; archive signatures and source checksums must verify. Recheck identity at use, not only at download.
3. Complete the reviewed dependency-topological command list and installer interface receipts. Run `bash RE/r1b_host_commands.sh guard RE/intel_provisioning_manifest_v2.json <independent-observation.json>`; any nonzero exit stops before installation. H rejects this current unresolved J.
4. Under separate authority, execute only J's frozen command vectors: archive-only for the archive entries, explicit source builds only for the five listed ports. Unknown build-only dependencies/variants/route substitutions stop. The exact `archive`/`activate` identity-preserving source sequence remains blocked pending its interface/chain receipt; do not execute `-s install` as a substitute.
5. Run `bash RE/r1b_host_commands.sh compare-installed RE/intel_provisioning_manifest_v2.json`, plus exact native version/ABI/linkage checks from R5. Require exact registered versions/revisions/variants and image-to-install mapping, no extra ports/distributions/files, and the reviewed generated-file rules. Missing observations refuse.
6. Persist before/peak/after category/pool measurements and monotonic elapsed time before stopping the provisioning clock; keep failed images/receipts and stop at first failure. No cleanup or retry.

Steps above are R1B proposed controls; `V:33-35,75` requires their final executable interfaces, signatures and source chain **before dispatch**. H's syntax checks do not establish MacPorts behavior or native acceptance. Build-only ports, if admitted, must be explicitly included in both the expected registered port set and payload mapping; a runtime-only list is not enough.

## R5 — Artifact-bound commissioning checks, commands and advance predicates

Addresses `V:77`. R1B proposed commissioning entry requires `J:1507-1534 /commissioning/command_vectors` from the reviewed `r3-controller`/`r3-workload`/`r3-review` package, exact executable/member paths, endpoint/interface receipts and sanitized receipt schema. This is unresolved, not implied by the table. R3 must run outside the owned RE process tree so it can enforce deadlines when that tree stalls (`V:44-46`).

| Check / manifest entries | Frozen command or required exact vector | Advance success predicate; every missing observation blocks |
|---|---|---|
| C0 Java; `port:openjdk21` | `<J java_home>/bin/java -XshowSettings:properties -version`; file/otool against admitted executable | Command exits 0; exact admitted Java version/home, x86_64 architecture and only declared native linkage (`P:267`; `TS:11`). |
| C0 Python; `python-runtime`, `port:python312` | `<J python_env>/bin/python -I -B -c 'import sys,sysconfig,platform; print(sys.version); print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(platform.machine()); print(sysconfig.get_config_var("SOABI")); print(sys.path)'` | Exact reviewed 3.12.15/ABI/base path; dedicated env, no system/science-site imports; actual installed stdlib binds to the archive manifest (`P:167-174`; `TS:14`). |
| C0 DuckDB; `duckdb-wheel`, `duckdb-lock`, `python-install-tool` | `<J python_env>/bin/python -I -B -c 'import duckdb; c=duckdb.connect(":memory:"); c.execute("SET threads=1"); assert duckdb.__version__=="1.5.5"; assert c.execute("SELECT 1").fetchall()==[(1,)]; c.close()'`; admitted extension `file`/`otool -L` | Exit 0; lock-selected wheel, exact distribution set and extension/native architecture/linkage; offline pinned installer only (`L:1-36`; `P:167-182`). |
| C1 Config; `neo4j` | `<J neo4j_home>/bin/neo4j-admin server validate-config` with J-frozen environment/config | Exit 0; auth on, loopback-only HTTP/Bolt, exact paths, heap 256/512 MiB, page cache 256 MiB, Java processors 2, session marker and no automatic pruning. LTS syntax must be established before start (`A:30,32`; `V:61`). |
| C2 Launch/ownership/priority; `neo4j`, `r3-controller` | J-reviewed external controller start vector launches the F5 priority-preserving `console` exec | Inherited priority controls 0/10/>10; all Python/Java owned descendants nice >=10; independent oracle complete, exact generation/instance marker, session <=1,800 s. Command vector/ownership oracle NEEDS-FETCH (`A:31-32`; `V:44-46`). |
| C3 HTTP; `neo4j`, `r3-controller` | `/usr/bin/curl --disable --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 10 --config <0600 credential curl file> --header 'Content-Type: application/json' --data '{"statements":[{"statement":"RETURN 1 AS r1_probe"}]}' --output <receipt>/http.json --write-out '%{http_code}\n' http://127.0.0.1:7474/db/neo4j/tx/commit`; negative control omits config | Curl exit 0, status 200; parser requires `errors==[]`, one result, `columns==["r1_probe"]`, one `row==[1]` with integer type (not bool). Negative request status 401/403. Bind these endpoints/shape to LTS interface receipt before use; no Query API substitution (`V:39,61`; `P:280-285`). |
| C4 Bolt; `cypher-shell`, `neo4j` | `<admitted shell> -a bolt://127.0.0.1:7687 --format plain 'RETURN 1 AS r1_probe'`; exact credential and output-parser vectors from J | Exit 0 and exact header/single integer 1 after documented whitespace normalization; no warning/error/extra row. Use only an interface-proven protected credential channel. Password argv/process dumps forbidden. Until that mechanism/parser is frozen, C4 cannot run (`V:40,46`; `P:272,285`). |
| C5 Resource/cap; `r3-controller`, `r3-workload`, `neo4j`, `duckdb-wheel` | J's reviewed one-thread workload, independent ownership sampler and cap-control vectors | Per-second complete samples; Neo4j RSS <=2 GB, importer <=512 MiB, aggregate <=3 GB; CPU <=200%/100%, one worker/thread, disk within caps, appropriate pressure. Enforcement and attribution must be demonstrated, not inferred from ps (`A:29-31`; `V:41`). |
| C6 Normal shutdown; `r3-controller`, `neo4j` | External controller sends graceful signal to the **same console-owned JVM/instance**, not an unrelated `neo4j stop`; records full identity immediately before stop | Within <=30 s: exact same process start identity exits, owned inventory independently empty, listener ownership empty, HTTP/Bolt connections refused with a validated functioning probe, and line-specific clean-shutdown log predicate present. Escalation only to proven-owned processes; escalation cannot count as clean shutdown (`V:42,46`; `P:274`). |
| C7 Fault/deadline/no-resume; `r3-controller`, `r3-workload`, `r3-review` | J-reviewed independent controls for cap, explicit stop, revocation and timeout; exact receipt schema and bounded post-stop observation vector | Durable interruption diagnostic/no publication; C6 cleanup predicates; no resume for the preregistered observation window; next launch requires fresh admission. R3 must freeze that window and detector completeness; never infer no-resume from a single empty ps sample (`V:43,46`; `A:32`). |

C0/C1 command forms inherit P's proposed interfaces, not proven LTS interfaces. Missing LTS CLI/credentials/R3 evidence requires technical review and a revised frozen vector before startup. Config values/caps come from A; there is no runtime result here (`P:261-287`; `A:29-32`).

Exact HTTP predicate to put in the reviewed controller (R1B proposed parser, not a native receipt): parse the nonempty saved UTF-8 JSON; require `errors == []`, `len(results)==1`, `results[0]["columns"]==["r1_probe"]`, `len(results[0]["data"])==1`, `results[0]["data"][0]["row"]==[1]`, and `type(results[0]["data"][0]["row"][0]) is int`. Parse failure, unexpected shape or nonzero curl exit fails; never use grep for JSON success (`V:39,46`).

**Remaining R5 boundary:** the actual reviewed R3 version/hash/vector, credentials, ownership completeness, precise LTS shutdown-log predicate and no-resume window are not supplied by these inputs. The collector can verify supplied bytes, not create missing controller behavior. Keep commissioning blocked and name these gaps in the report (`V:44-46,77`).
