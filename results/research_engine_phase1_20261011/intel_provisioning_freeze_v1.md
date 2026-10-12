# R1 — Intel provisioning freeze v1 (draft for Astra)

This packet freezes the observed baseline, proposed selection boundaries and refusal criteria. **Provisioning remains blocked** by NEEDS-DECISION and NEEDS-FETCH entries. Recommendations are not decisions. No acquisition, installation, native check or commissioning result is asserted. Astra's host-design verdict expressly leaves provisioning and host acceptance unauthorized (`V:1–3,40–52,60`).

Citation aliases, each relative to `results/research_engine_phase1_20261011/`:

- `F` = `intel_r1_facts_20261011.md`.
- `D` = `intel_r1_discovery_20261011T0906Z.txt`.
- `T` = `intel_r1_tree_20261011T0907Z.txt`.
- `V` = `astra_intel_a1_verdict.md`.
- `A` = `phase1_intel_amendment_v1.md`.
- `S` = `phase1_spec_v5.md`.
- `L` = `duckdb_1.5.5.lock.txt`.
- `LP` = `duckdb_lock_parse_receipt_20261011.txt`.
- `M` = `preinstall_identity_20261011.tsv`.
- `B` = `provisioning_dryrun_20261011.txt`.

Status meanings: **FROZEN** = the stated identity or exclusion is fixed in this draft, not approved/installed/compatible; **NEEDS-DECISION** = mutually exclusive alternatives await reviewed selection; **NEEDS-FETCH** = missing identity, bytes, provenance or verification evidence must be obtained in a separately authorized step. A row may name a candidate without selecting it. All commands below are future commands, not execution receipts.

## 1. R1 bullet 1 — host, package manager and effective tree identities

| Component | Baseline identity and provenance | Status / remaining verification |
|---|---|---|
| Intel support host | SSH target `robertrhu_node2@192.168.10.2`; dated observation 2026-10-11 09:06:48 UTC: macOS 14.8.9, build 23J631, x86_64 (`F:3`; `D:1–9`). | FROZEN baseline. Re-observe target account, hostname/hardware identifier, OS/build/architecture and physical volumes; hardware serial/model are not in these receipts. No OS replacement selected. |
| MacPorts base | Installed version 2.12.6; retained RELEASE_URL names `https://github.com/macports/macports-base/releases/tag/v2.12.6` (`D:8–9`; `T:18,44`). Historical Sonoma pkg identity: `MacPorts-2.12.6-14-Sonoma.pkg`, SHA-256 `184ac171c201391a502958951867e77062010c781ade302b70b1f176e42d23d6` (`A:101`). | FROZEN baseline. This is a historical pkg digest, not a fresh installed-byte verification; the prior Downloads pathname failed and reinstall is not required (`V:27`). Capture `pkgutil` receipt, base executable/library hashes and config inventory before mutation. |
| Apple build tools | `/Library/Developer/CommandLineTools`; `com.apple.pkg.CLTools_Executables` 16.2.0.0.1.1733547573 (`D:189–190`; `T:35–48`). | FROZEN receipt version; NEEDS-FETCH compiler/SDK identities and hashes if source builds are selected. No toolchain upgrade authorized. |
| Effective source configuration | Active entry at sources.conf line 30: `rsync://rsync.macports.org/macports/release/tarballs/ports.tar.gz [default]`; configuration uses `/opt/local/etc/macports/sources.conf` (`D:10–31`). | FROZEN. Earlier empty-looking display was the comment header, not absence of a source (`F:7`). Refuse extra active sources or reordered/shadowing sources. |
| Effective searched tree | `/opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs/ports`; commit `4a3293129f126ff91354e59e0ba647d49df22f25`; `port dir` resolves python312, duckdb and openjdk21 there (`D:51–54`; `T:49–50`). | FROZEN commit and location. Directory existence or `.git_commit` alone is insufficient. |
| Acquisition artifact | Retained sibling `remote/ports.tar.gz`, 37,209,919 bytes, SHA-256 `c413261d162447c8d5ff6fd6fc9db1a7b8ec55fa0acabb04db7c3b6e3429286d`; dated acquisition 2026-10-11 00:00 host time (`F:10`; `T:51–58`). | FROZEN content identity. Do not reacquire a moving rsync URL and assume equivalence. |
| Search index | Tree `PortIndex`, 25,811,248 bytes, SHA-256 `0a0ceda7c196d0a22afae686007ad0dd55f0c6c53088993424426116031da26c`; `PortIndex.quick` SHA-256 `46b16b604fa3298f39f655dd993bd5c0461232438a28b98bd031e34c6257cd19` (`T:14–17`). | FROZEN. Compare both indexes and independently compare the extracted recipes/PortGroups with retained tar content. |
| Signature material | `remote/ports.tar.gz.sig`, `.rmd160`, `PortIndex.sig`, verification key `/opt/local/share/macports/macports-pubkey.pem`, sole pubkeys.conf entry (`F:10`; `T:33,54–58`). | NEEDS-FETCH verification receipt and full key/signature hashes. Abbreviated hashes in F are not usable pins. Presence of signatures does not establish a successful signature verification. |

**Frozen prohibition:** `port sync` and `port selfupdate` are forbidden until a reviewed re-freeze. No unpinned tree, alternative package manager, mirror-content substitution, edition/version substitution or automatic fallback is permitted (`F:12`; `V:48`; `A:116,139`). Hold competing package/tree writers for the entire precheck/acquisition/install/postcheck window; a matching check followed by an uncoordinated update does not preserve this baseline. This is a proposed installer coordination requirement.

Before mutation, MAESTRO must rehash retained tar/indexes and selected Portfiles, check every selected `port dir`, and compare every used recipe and included PortGroup byte-for-byte with the pinned tar content using a separately budgeted verification extraction. Inspect tar entries before extraction; reject paths escaping the extraction root. Persist the full file inventory and its digest. Use the documented MacPorts signature-verification mechanism after checking its installed interface; record exact verification command, key fingerprint, stdout/stderr/exit. Missing verification method or receipt is a refusal, not permission to trust the signature filename (`A:96,116–118`; `V:42,48`).

## 2. R1 bullet 2 — selections, complete closure and acquisition identities

### 2.1 Choices to return to MAESTRO/operator

1. **Python — NEEDS-DECISION.** Option P1: tree `python312 @3.12.15_0+lto+optimizations`, replacing v5's 3.12.14 through explicit review; it shares the pinned tree but adds its native closure. Option P2: exact python.org CPython 3.12.14 source build into the isolated setup prefix; it preserves the version but needs release-source/hash/signature, build/SDK flags, native closure and measured build time/space. No evidence here establishes an available 3.12.14 macOS binary installer. **Recommendation: P1**, conditional on reviewed patch-version amendment and budget fit; otherwise stop, not P2 automatically (`F:18,38`; `D:57–64,88`; `S:189,246`; `V:30`).
2. **Neo4j — NEEDS-DECISION.** Option N1: upstream Community 2026.09.0 unix tarball, preserving the v5 application line. Option N2: upstream Community 5.26.32 LTS unix tarball, changing line and requiring its own Java/HTTP/configuration evidence. **Recommendation: N1** to minimize the spec change, conditional on actual Intel checks. N2 offers the recorded LTS line but cannot inherit N1 compatibility. There is no matching Neo4j/cypher port in this searched tree (`F:24–30`; `D:182–184`; `S:244`).
3. **DuckDB — NEEDS-DECISION.** Option D1: exact `duckdb==1.5.5` macOS x86_64 CPython-3.12 wheel belonging to L's hash set. Option D2: tree `duckdb @1.5.6_1`; source route adds cmake/python314 and the other recorded dependencies, while a port archive still requires its own identity and proof of a usable Python binding. D2 is a reviewed version/artifact change, not an equivalent implementation of L. **Recommendation: D1**; preserve the existing Python artifact contract and avoid adding a second Python merely for the port build (`F:19`; `D:66–73`; `S:246`; `V:31`).
4. **MacPorts delivery — NEEDS-DECISION per port.** Option A1: exact macOS-14.8.9/x86_64-compatible binary archive for the frozen name/version/revision/variants, with actual Darwin target, archive URL, digest, signature and dependency metadata pinned before install. Option A2: source build from the pinned recipe/PortGroups, all source/patch hashes and build-only dependencies pinned, plus toolchain/SDK/flags and resulting installed-file manifest. **Recommendation: A1 where such an exact archive is verified** because it avoids the build workspace/time risk; no archive availability or budget fit is asserted. If unavailable, stop for an explicitly reviewed A2 plan. Do not allow an archive attempt to silently become a source build or the reverse (`D:5–7`; `A:116–118,139`; `V:43`; `D:80–81`; `S:217`).

These options are not authorizations. The whole set must meet the same <=15-minute provisioning and <=1 GB setup-growth constraints; an estimate that does not fit is a request for reviewed scope/budget disposition, not permission to exceed them (`A:28,32,36`).

### 2.2 Root artifacts and exact missing-identity steps

| Dependency | Selected constraint / candidate version | Source, digest or exact obtain-and-verify step | Status |
|---|---|---|---|
| OS / MacPorts / ports tree / CLT | Baselines in §1 | Retain §1 receipts; recheck without upgrade. OS/base installed-byte inventory and source-build toolchain inventory remain required. | FROZEN baseline |
| Java | Candidate openjdk21 21.0.12.1_0 +release+server | P(openjdk21) below; Portfile SHA-256 `78c9e850f922bba94d2e40b027b0dfecb6fe400767545a9cd97ad2b4b18a85dd` (`T:29`; `D:75–81,160`). Source/archive hashes are missing. | NEEDS-FETCH |
| Neo4j Community | N1 2026.09.0 or N2 5.26.32 | N(v) below; published, unverified-byte digests in F:28 are not acquisition verification. | NEEDS-DECISION |
| cypher-shell | Exact shell matching selected Neo4j line; v5 candidate 2026.09.0 | First inspect chosen tar inventory for `bin/cypher-shell` and its bundled libraries; verify whole tar and per-file hashes. If absent, freeze a separate matching upstream shell artifact URL/edition/version/hash/closure before download/install. No port match (`D:184`; `S:244`). | NEEDS-FETCH |
| CPython | P1 3.12.15_0 +lto+optimizations or P2 3.12.14 | P(python312) or C below; P1 Portfile SHA-256 `a060385541ac66c1cb6e0860ebc578c3789515d1e2436a3eb9cfdff3cead03e6` (`T:27`). P1 source SHA-256 `c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a` (`D:84–86`). | NEEDS-DECISION |
| DuckDB Python extension | Constraint 1.5.5 / cp312 / macOS x86_64 | W below; machine-consumable L:1–36, lock-file SHA-256 `f8ffcdeadaded28928249cf8b468a25e9cf25e8a1a6b028b22deed8757c28636` (`LP:8`). Exact Intel wheel filename/URL/hash not recorded. | NEEDS-FETCH |
| DuckDB port alternative | Candidate 1.5.6_1; explicit variants still to capture | P(duckdb); Portfile SHA-256 `7eb8eee41c728a6fff0889f3458db859d60271ccc7a3a048057e27af6140707f` (`T:28`; `D:66–73`). Excluded unless D2 is explicitly selected. | NEEDS-DECISION |
| Python installer tooling | No version selected; runtime spec adds none | Inspect the chosen interpreter's bundled ensurepip/pip artifacts. If used, freeze their exact versions, wheel names/hashes and provenance; if unavailable, freeze a separately reviewed hash-pinned installer and its complete closure. No floating bootstrap or py312-pip install. The receipt gives only py312-pip's recipe location (`D:55`; `S:189,246`). | NEEDS-FETCH |
| Python stdlib JSON/HTTP/hash/unittest | Bound to selected CPython build | Hash interpreter and installed stdlib inventory; no third-party JSON/HTTP/test libraries are selected (`S:189,191`). | FROZEN dependency scope |
| Neo4j plugins / Python drivers / model libraries | Excluded | No Neo4j Python driver, LinkML runtime, APOC/GDS/plugins/framework, torch, transformers, model/tokenizer/science/MathLab runtime (`S:189–191`). Verify package/import inventory and require no undeclared Python distribution. | FROZEN exclusion |

**P(name), future recipe/artifact pin procedure:** check `/opt/local/bin/port help info`, `help deps`, `help rdeps`, `help dir`, `help fetch`, `help checksum`, `help archivefetch`, and `help contents` before using those interfaces. Run `port dir <name>`, `port info <name>`, `port deps <name>` and `port rdeps <name>` against this tree. Record version/revision, explicit variants (including effective default/negated/universal variants), architecture, every dependency edge with build/lib/run role, selected archive or source route, recipe/PortGroup hashes, actual upstream source and patch URLs and every published checksum. Require a finite complete graph by recursively visiting every direct dependency; reject omissions or cycles that cannot be resolved. The roots' existing observations are `D:57–179`; this procedure implements `A:96,116–118` and `V:43`.

For A1, capture configured archive sites and exact matching archive filename/URL, compression/type, target OS/architecture/version/revision/variants, signature/key fingerprint, SHA-256, length and manifest. Separately authorized acquisition must verify signed identity AND actual bytes; hash/signature/metadata mismatch refuses. For A2, fetch only the exact reviewed source/patch list, run the frozen recipe checksum operation and independently SHA-256 every file; freeze all build-only prerequisites and compiler/SDK flags. No hash appearing only after an unreviewed source choice can authorize installation. Preserve artifacts and failure evidence; do not invoke cleanup (`V:43`; `A:118,139,36`).

**N(v), future Neo4j acquisition:** after line selection, independently resolve the official Community unix tar download route and freeze final HTTPS artifact URL/redirect chain and length. F:30 records only a working checksum URL pattern, not a verified direct tar link. Candidate tar routes to verify are `https://dist.neo4j.org/neo4j-community-2026.09.0-unix.tar.gz` and `https://dist.neo4j.org/neo4j-community-5.26.32-unix.tar.gz`; no reachability assertion is made. Save the exact official `.sha256` response without summarization, validate its syntax/version/filename and compare it to F:28; disagreement requires review. After separately authorized fetch into the frozen staging path, `/usr/bin/shasum -a 256 <absolute-tar-path>` must match both the independently captured upstream checksum and the reviewed selection manifest. Before extraction inspect Community edition, entries, paths, executable architecture and included shell/JARs; pin the extracted manifest (`F:27–30`; `A:118–120`).

F:28's published checksum observations are: 2026.09.0 `cdaa0905d9a533bbbc474d239c268f69978982eb5ca3177666c04c9792d1c399`; 5.26.32 `d279ae6a9b38034280681a558b0cd222dce89f87cc3d9867f1f7bd28ef5ebc30`. **Both remain NEEDS-FETCH**, including verification against actual downloaded bytes (`F:28`). Java 21/macOS-14/x86_64 evidence in F:29 concerns the 2026.09 requirements page; do not transfer it to 5.26.32 without that line's evidence. macOS is listed for personal/development only. The recorded 10 GB development disk minimum is not proof that this <=6 GB pilot/setup fits; MAESTRO must reconcile it and the intended development-only scope before provisioning (`F:29`; `A:28,34–36`).

**C, python.org alternative:** independently locate the exact CPython 3.12.14 release source and its official integrity/signing record on python.org, freeze final source URL, filename, length, SHA-256 and release provenance, then hash the separately acquired bytes. Freeze local build prefix, configure/build flags, selected SDK/compiler, complete linked-library closure and installed output hashes. If exact source/support or any native prerequisite cannot be established, refuse P2; do not select another patch or a binary installer by implication (`V:30`; `A:105,118,139`).

### 2.3 Dependency closure ledger

The following ledger covers every dependency name visible in the supplied python312/openjdk21 rdeps and duckdb info/rdeps. **It is not a completed artifact lock.** The duckdb rdeps excerpt does not recursively display its direct python314/croaring/openssl3 entries, although info names them; exact dependency versions/variants and artifacts are absent throughout. P(name) must complete and freeze all edges/identities before mutation. An added dependency requires a reviewed new ledger row (`D:62–81,87–179`; `V:43`).

For each row below, version/revision/variants = **NEEDS-FETCH via P(name)**; source = the §1 tree's recipe and its captured upstream/archive URLs; hash = **NEEDS-FETCH via P(name)**. Thus every row has an exact missing-identity procedure rather than an invented version/hash. `PJ` denotes observed python312/openjdk21 closure membership; `DB` denotes the unselected DuckDB-port alternative. These groups describe observed names, not permission to install. Binary-only and source plans must each record their actual complete closure and justify exclusions of build-only ports (`D:87–179`).

| Dependency name | Observed route / evidence | Status |
|---|---|---|
| autoconf | PJ; DB (`D:106,139,162`) | NEEDS-FETCH |
| automake | PJ; DB (`D:105,141`) | NEEDS-FETCH |
| bash | PJ (`D:175`) | NEEDS-FETCH |
| bison | PJ (`D:176`) | NEEDS-FETCH |
| bison-runtime | PJ (`D:177`) | NEEDS-FETCH |
| bzip2 | PJ; DB (`D:99,156`) | NEEDS-FETCH |
| cctools | PJ (`D:178`) | NEEDS-FETCH |
| dejagnu | PJ (`D:103`) | NEEDS-FETCH |
| expat | PJ; DB (`D:100,155`) | NEEDS-FETCH |
| expect | PJ (`D:104`) | NEEDS-FETCH |
| freetype | PJ (`D:179`) | NEEDS-FETCH |
| gettext | PJ; DB (`D:90,124,164`) | NEEDS-FETCH |
| gettext-runtime | PJ; DB (`D:97,131,171`) | NEEDS-FETCH |
| gettext-tools-libs | PJ; DB (`D:93,127,167`) | NEEDS-FETCH |
| gmake | PJ (`D:173`) | NEEDS-FETCH |
| gperf | PJ; DB (`D:95,129,169`) | NEEDS-FETCH |
| libedit | PJ (`D:101`) | NEEDS-FETCH |
| libffi | PJ (`D:102`) | NEEDS-FETCH |
| libiconv | PJ; DB (`D:94,128,168`) | NEEDS-FETCH |
| libtextstyle | PJ; DB (`D:96,130,170`) | NEEDS-FETCH |
| lzip | PJ (`D:174`) | NEEDS-FETCH |
| m4 | PJ; DB (`D:107,140,172`) | NEEDS-FETCH |
| ncurses | PJ; DB (`D:92,126,166`) | NEEDS-FETCH |
| openjdk21-zulu | PJ bootstrap JDK (`D:161`) | NEEDS-FETCH |
| openssl | PJ; DB (`D:111,144`) | NEEDS-FETCH |
| openssl3 | PJ; DB (`D:72,112,145`) | NEEDS-FETCH |
| pkgconfig | PJ; DB (`D:98,132`) | NEEDS-FETCH |
| python_select-312 | PJ (`D:114`) | NEEDS-FETCH |
| python_select | PJ (`D:115`) | NEEDS-FETCH |
| python3_select-312 | PJ (`D:116`) | NEEDS-FETCH |
| python3_select | PJ (`D:117`) | NEEDS-FETCH |
| sqlite3 | PJ (`D:113`) | NEEDS-FETCH |
| tcl | PJ (`D:108`) | NEEDS-FETCH |
| tcl8 | PJ (`D:109`) | NEEDS-FETCH |
| xz | PJ; DB (`D:89,123,163`) | NEEDS-FETCH |
| xz-bootstrap | PJ; DB (`D:91,125–126,165`) | NEEDS-FETCH |
| zlib | PJ; DB (`D:110,133`) | NEEDS-FETCH |
| brotli | DB (`D:134`) | NEEDS-FETCH |
| cmake | DB (`D:120`) | NEEDS-FETCH |
| cmake-bootstrap | DB (`D:135`) | NEEDS-FETCH |
| croaring | DB direct, recursion absent (`D:72`) | NEEDS-FETCH |
| curl | DB (`D:122`) | NEEDS-FETCH |
| curl-ca-bundle | DB (`D:146`) | NEEDS-FETCH |
| db48 | DB (`D:150`) | NEEDS-FETCH |
| gdbm | DB (`D:151`) | NEEDS-FETCH |
| libarchive | DB (`D:157`) | NEEDS-FETCH |
| libcxx | DB (`D:121`) | NEEDS-FETCH |
| libidn2 | DB (`D:137`) | NEEDS-FETCH |
| libpsl | DB (`D:143`) | NEEDS-FETCH |
| libtool | DB (`D:142`) | NEEDS-FETCH |
| libunistring | DB (`D:138`) | NEEDS-FETCH |
| libxml2 | DB (`D:158`) | NEEDS-FETCH |
| lz4 | DB (`D:154`) | NEEDS-FETCH |
| nghttp2 | DB (`D:136`) | NEEDS-FETCH |
| perl5 | DB (`D:148`) | NEEDS-FETCH |
| perl5.34 | DB (`D:149`) | NEEDS-FETCH |
| python314 | DB direct, recursion absent (`D:71`) | NEEDS-FETCH |
| readline | DB (`D:152`) | NEEDS-FETCH |
| unzip | DB (`D:147`) | NEEDS-FETCH |
| zstd | DB (`D:153`) | NEEDS-FETCH |

Six prior M3 library upgrades are explicitly dispositioned below. These Intel candidate versions come from Astra's discovery reconciliation, not the ARM bottle manifest. Include them only if the completed selected Intel closure needs them; otherwise record an exclusion in that closure. Prior M3 upgrade approval is not Intel authorization (`V:32`; `A:114`; `M:6–11`; `B:10–16`).

| Library / Intel port name | Observed candidate version | Source/hash step / disposition | Status |
|---|---|---|---|
| libpng | 1.6.58 | P(libpng) if needed; no ARM bottle substitution (`V:32`). | NEEDS-FETCH |
| pcre2 | 10.48 | P(pcre2) if needed (`V:32`). | NEEDS-FETCH |
| glib / glib2 | 2.88.3_2 | P(glib2) if needed (`V:32`). | NEEDS-FETCH |
| xorgproto / xorg-xorgproto | 2024.1 | P(xorg-xorgproto) if needed (`V:32`). | NEEDS-FETCH |
| cairo | 1.18.4_2 | P(cairo) if needed (`V:32`). | NEEDS-FETCH |
| harfbuzz | 14.4.0 | P(harfbuzz) if needed (`V:32`). | NEEDS-FETCH |

## 3. R1 bullet 3 — interpreter, Python artifacts, lock and ABI

The dedicated Intel environment must have no system site-packages and no reused science environment. Only selected CPython, its stdlib, DuckDB 1.5.5 and explicitly pinned install tooling are candidates. A third-party dependency discovered in wheel metadata requires explicit review; do not use implicit resolver downloads (`S:189–191,199,246`; `A:20,120`).

**W, exact wheel selection and verification (NEEDS-FETCH):** independently capture PyPI's `duckdb` 1.5.5 file metadata (official JSON endpoint candidate `https://pypi.org/pypi/duckdb/1.5.5/json`) and freeze the one selected filename, immutable artifact URL, length and SHA-256. Require a cp312-compatible macOS x86_64 wheel whose minimum deployment tag is compatible with macOS 14.8.9. Do not guess a tag or select by a bare version. Require that digest to occur in L's 35-hash set and verify downloaded bytes with `/usr/bin/shasum -a 256 <absolute-wheel-path>`. Inspect WHEEL/METADATA and included Mach-O binaries for interpreter/ABI/architecture/linked-library compatibility. Hash membership alone does not establish any of those properties (`L:1–36`; `S:189,246`; `V:31,44`).

L remains the machine-consumable `--require-hashes` lock, fixed at SHA-256 `f8ffcdeadaded28928249cf8b468a25e9cf25e8a1a6b028b22deed8757c28636`. LP records only a prior dry-run selecting 1.5.5, not Intel ABI/import proof; S's cached wheel/interpreter are macOS ARM identities (`LP:1–8`; `S:189`; `V:31`). Retain all 35 hashes; do not edit L. Freeze the exact selected Intel wheel alongside it so a broad membership set does not obscure the artifact actually admitted.

Future machine-readable selection manifest must contain nonempty values for: target OS/build/architecture, interpreter realpath/version/SOABI/cache_tag/build flags/SHA-256, wheel filename/URL/length/SHA-256/WHEEL tags, L path/SHA-256, installer version/lock/hashes, and complete native dependency manifest/hash. Missing values remain NEEDS-FETCH and **cannot** produce an executable provisioning manifest. This packet does not fabricate that missing lock or write a third file (`V:43–44`; `A:118–120`).

Proposed native evidence commands, after separately authorized provision and help/interface checks:

```sh
"$RE_PY" -I -B -c 'import sys,sysconfig,platform; print(sys.version); print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(platform.machine()); print(sys.implementation.cache_tag); print(sysconfig.get_config_var("SOABI")); print(sysconfig.get_config_var("MACOSX_DEPLOYMENT_TARGET")); print(sys.path)'
"$RE_PY" -I -B -c 'import importlib.metadata as m; print([(d.metadata["Name"],d.version) for d in m.distributions()])'
"$RE_PY" -I -B -c 'import duckdb; print(duckdb.__version__); print(duckdb.__file__); c=duckdb.connect(":memory:"); c.execute("SET threads=1"); print(c.execute("SELECT 1").fetchall()); c.close()'
/usr/bin/file "$INTEL_PY_BASE" "$DUCKDB_EXTENSION"
/usr/bin/otool -L "$INTEL_PY_BASE"
/usr/bin/otool -L "$DUCKDB_EXTENSION"
```

**PASS criteria frozen before execution:** exact reviewed interpreter version, x86_64 process/extension, accepted cp312 ABI/tags, dedicated prefix, no science/system-site import path, declared distributions only, DuckDB exactly 1.5.5 at the frozen local path, query result `[(1,)]`, native libraries matching the closure; every command exits 0 with parseable nonempty observations. Otherwise FAIL/UNVERIFIED. `DUCKDB_EXTENSION` must be the actual extension found in the admitted wheel inventory, not the package `__init__.py` (`S:189,246`; `A:129,137`; `V:44`).

After the exact installer is frozen, its reviewed pip interface, if selected, must enforce an offline wheelhouse, hash checks and no resolver/source fallback. Proposed invocation (not run):

```sh
"$RE_PY" -I -B -m pip install --no-index --no-deps --only-binary=:all: --require-hashes --find-links "$RE_WHEELHOUSE" -r "$RE_LOCK"
```

Check that interface first. Require the wheelhouse to contain only the admitted Intel artifact; extra runtime Python packages, sdists, ARM/Linux wheels, copied M3 interpreter/cache and unpinned install tooling refuse. If tooling cannot meet this shape, return for review rather than weaken it (`S:189–191,246`; `A:120,139`).

## 4. R1 bullet 4 — absolute paths, inventory and peak disk budget

The following are **proposed absolute Intel paths**, not claims of existing directories or a MAESTRO-selected root. MAESTRO must accept this path map, capture prior contents/owners/modes/realpaths and filesystem device IDs, and refuse any symlink/mount resolution through M3/memit before dispatch. Relative layout is preserved from S while storage is Intel-local (`S:193–201`; `A:20,36`).

| Purpose | Proposed absolute path / disposition |
|---|---|
| Local root | `/Users/robertrhu_node2/research-engine-phase1` |
| Admitted immutable code/source | `/Users/robertrhu_node2/research-engine-phase1/pilot/source`; preserve original relative paths and reviewed export identity |
| Python environment / RE_PY | `/Users/robertrhu_node2/research-engine-phase1/pilot/source/.venv-research-engine`; executable `bin/python` beneath it |
| R1 input lock / RE_LOCK | `/Users/robertrhu_node2/research-engine-phase1/pilot/source/results/research_engine_phase1_20261011/duckdb_1.5.5.lock.txt` |
| Runtime / RE_RUNTIME | `/Users/robertrhu_node2/research-engine-phase1/pilot/source/results/research_engine_phase1_20261011/runtime` |
| Neo4j configuration/data/logs/transactions/run/tmp | RE_RUNTIME `/neo4j/{conf,data,logs,transactions,run,tmp}` |
| Generations/publication/leases/credentials/control/tmp | RE_RUNTIME `/{generations,publication,leases,credentials,control,tmp}`; secret `/credentials/neo4j.curl.conf`, mode 0600, excluded from receipts |
| Build/commissioning receipts | `/Users/robertrhu_node2/research-engine-phase1/pilot/source/results/research_engine_phase1_20261011/builds/<fresh-id>`; exclusive fresh namespace |
| Neo4j install / NEO4J_HOME | `/Users/robertrhu_node2/research-engine-phase1/setup/neo4j-community/<selected-exact-version>`; no floating current symlink |
| Source-built Python alternative | `/Users/robertrhu_node2/research-engine-phase1/setup/cpython-3.12.14`; executable `bin/python3.12`; only if P2 selected |
| MacPorts Python candidate / INTEL_PY_BASE | `/opt/local/bin/python3.12`; freeze actual realpath/contents after P1 selection |
| Java candidate / JAVA_HOME | `/opt/local/libexec/openjdk21/Contents/Home`; executable `bin/java`; candidate path must match `port contents openjdk21` before reliance |
| RE staging / wheelhouse | `/Users/robertrhu_node2/research-engine-phase1/setup/staging`; `RE_WHEELHOUSE` = `/Users/robertrhu_node2/research-engine-phase1/setup/wheelhouse` |
| RE installer caches/build/temp | `/Users/robertrhu_node2/research-engine-phase1/setup/{cache,build,tmp}`; freeze `TMPDIR`/installer cache controls; runtime temp stays under RE_RUNTIME |
| MacPorts inventory/cache/temp | `/opt/local`, including `/opt/local/var/macports/{sources,distfiles,software,build}` and any additional actual paths found in its configuration/operation plan; `/Applications/MacPorts`; `/opt/local/Library/Frameworks` (`D:23–31`) |
| Other actual write locations | NEEDS-FETCH inventory of installer user caches, system temp, SDK/build outputs, JDK registration and receipts outside the above. Freeze each absolute path before install; unaccounted writes refuse. |

The Java layout and other newly proposed paths are planning choices needing realpath/ownership checks, not observations. No path is authorized merely because it appears here. No runtime reads/writes through a shared M3/memit mount (`A:20`).

**Preinstall inventory, NEEDS-FETCH:** timestamp + host/pool IDs, `port installed`, `pkgutil --pkg-info org.macports.MacPorts`, all existing files and logical/allocated bytes under the disjoint roots above, path owners/modes, full MacPorts configuration, actual caches/temp paths, pending package writers, free bytes and memory/process pressure. D records no installed ports/no Java and available 467,303,544 KiB on both `/` and `/System/Volumes/Data`; it does not provide a complete before-size baseline and those views must not be summed as separate free pools (`D:180–193`; `F:34`; `A:34–36`). M/B are M3 Homebrew receipts, not Intel preinventory or installation growth evidence (`M:1–11`; `B:2–19`; `V:27,31–32`).

Frozen accounting rules (`S:207–211,245`; `A:28,34–36`):

- Pilot existing bytes B + conservative additional peak P <=5,000,000,000. Retain v5 subceilings: env/code/tests 600 MB, key/inputs 200 MB, DuckDB 600 MB, graph 1,200 MB, transactions/checkpoints 600 MB, temp/tests 800 MB, receipts/logs 300 MB, reserve 700 MB; <=2 complete generations and <=8 failed/test candidates. Retained failures and copies count; no rollover/cleanup.
- Setup additional growth across all setup/install/cache/temp/dependency locations <=1,000,000,000 bytes **at peak**, not merely the net final footprint. Combined pilot/setup accounting <=6,000,000,000 bytes; no setup dependency is exempt for being outside the user root.
- For each physical pool, reserve existing usage and concurrent projected writes once. Require free >= projected additional peak writes +21,474,836,480 bytes and free minus those writes >=80,000,000,000 bytes. Equivalently require free >= P_pool + max(21,474,836,480, 80,000,000,000); this does not spend the free floor or add the same reserve twice.
- Preserve Intel planning ceilings: recovery 250 GB, extra unique history 50 GB, builder work/tools 40 GB, analysis/transfer staging 50 GB, pilot/setup 6 GB. They are conditional ceilings, not reservations or demonstrated fit; no borrowing.
- Use logical-byte inventories for decimal caps and actual allocated/free observations for physical-pool admission; also retain the prescribed `du -sk` before/after receipts. Inventory parent roots disjointly; do not count `/opt/local/Library/Frameworks` twice within `/opt/local`. Link/hardlink/copy accounting must distinguish logical category charges from actual physical allocation.

**Projected peak, currently NEEDS-FETCH:** measure source/archive downloads, compressed+extracted coexistence, whole native closure, bootstrap JDK, compile work, installer caches/temp, wheel+installed copy, retained receipts and allowed concurrent writes. Allocate conservative bounds before installing; unknown archive/source/extraction/build size refuses. No measured numerical fit estimate is supplied by these receipts (`V:43,45`; `A:36,118,137`). A1 recommendation reduces potential work but is not a <=1 GB estimate. A2 must separately demonstrate <=15-minute provisioning and peak fit (`A:32`).

Future observations include `/bin/df -k <each-real-pool-path>` and `/usr/bin/du -sk <each-disjoint-inventory-root>` before, during and after acquisition/install, plus per-file logical/allocated inventories. Missing paths must be recorded as absent with successful parent inventory, not suppressed errors. A cap breach stops and preserves artifacts for operator disposition; exact deletion path/size/method approval remains required (`S:211,217,245`; `A:36`).

## 5. R1 bullet 5 — refusal, postinstall identity and Intel commissioning

### 5.1 Preinstall refusal and postinstall identity

The installer must refuse before first mutation if any choice is unresolved; required artifact/closure/manifest value is missing; target host/OS/build/architecture/base/config/tree/index/tar/recipe/variant differs; source/archive/wheel digest or signature differs; route switches; preinventory/pressure/ownership observations are unavailable; path escapes the local root/pool map; space/peak/time projections fail; or reviewed provisioning authorization is absent. No approval is inferred from this draft, matching version strings or package-manager installation (`V:3,40–48`; `A:116–120,139`). Acquisition also requires its own authorized, budgeted plan and immutable destination identities.

Concrete future baseline commands (read-only; compare exact nonempty outputs to §1, and abort on any command/parse/identity failure):

```sh
/usr/bin/id -un
/bin/hostname
/usr/bin/sw_vers
/usr/bin/uname -m
/usr/bin/uname -r
/opt/local/bin/port version
/usr/sbin/pkgutil --pkg-info org.macports.MacPorts
/usr/bin/xcode-select -p
/usr/sbin/pkgutil --pkg-info com.apple.pkg.CLTools_Executables
/bin/cat /opt/local/etc/macports/sources.conf
/bin/cat /opt/local/etc/macports/macports.conf
/bin/cat /opt/local/etc/macports/archive_sites.conf
/bin/cat /opt/local/etc/macports/pubkeys.conf
/bin/cat /opt/local/etc/macports/variants.conf
/bin/cat /opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs/ports/.git_commit
/usr/bin/shasum -a 256 /opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs/remote/ports.tar.gz
/usr/bin/shasum -a 256 /opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs/ports/PortIndex
/usr/bin/shasum -a 256 /opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs/ports/PortIndex.quick
/opt/local/bin/port installed
```

Also execute §1 content/signature checks, P(name) for every root/transitive entry, W and §4 inventory/math. Expected preinstall installed-port set is empty unless a reviewed revised baseline accounts for an intervening installation; a changed set refuses. Hostname/hardware/config full hashes remain to be captured rather than guessed (`D:180–181`; `V:42–46`; `A:118–120`).

After authorized installation, capture `port installed` and `port contents <each-installed-port>`, full installed-file hashes/versions/realpaths, actual Java/Python/Neo4j/shell outputs, signature/acquisition receipts, ABI evidence, active variants and the exact before/peak/after growth inventory. No extra installed port or distribution may appear outside the selected closure; native library linkage must match it. The reviewed Intel manifest replaces M/B rather than relabelling their ARM artifacts (`A:120,129–137`; `V:31–32,43–46`).

### 5.2 Commissioning commands and criteria — NOT RUN

Prerequisites: separately permitted provisioning; completed manifest/paths/locks; reviewed source export; explicit MAESTRO session admission and fresh receipt directory. R2 remains external and blocking before affected dispatch, and R3 owns concrete controller/process-accounting/receipt implementations. These commands define required native observations without drafting R2 or declaring R3 complete (`V:50–52`; `A:20–22,137`; `S:31–33,228–233`).

All variables below must be assigned from the reviewed manifest, never defaulted: `RE_PY`, `INTEL_JAVA`, `INTEL_NEO4J`, `INTEL_NEO4J_ADMIN`, `INTEL_CYPHER_SHELL`, `NEO4J_HOME`, `NEO4J_CONF`, `RE_RUNTIME`, `RE_CURL_AUTH`, `RE_SESSION`, `RE_RECEIPT`, `JAVA_HOME`. Proposed fixed endpoints are HTTP `127.0.0.1:7474` and Bolt `127.0.0.1:7687`; verify port availability first. The endpoint numbers/config syntax are proposed commissioning selections, not already frozen host observations (`S:191`; `A:137`).

First run/help-check each selected executable and freeze the exact installed CLI/configuration interface. The invocations below are proposed shapes: unsupported flags/settings/endpoints require a reviewed correction **before start**, never a different service or silent fallback (`A:96,137,139`).

| Gate | PASS stated before execution; every deviation FAIL/UNVERIFIED | Future commands / observations |
|---|---|---|
| C0 identity/interface | Exact reviewed versions and Community edition, Java x86_64, all help outputs usable; no guess about flags. | `"$INTEL_JAVA" -version`; `"$INTEL_JAVA" -XshowSettings:properties -version` (capture actual java.home/os.arch); `"$INTEL_NEO4J" --version`; `"$INTEL_NEO4J" --help`; `"$INTEL_NEO4J_ADMIN" --help`; `"$INTEL_NEO4J_ADMIN" server validate-config --help`; `"$INTEL_CYPHER_SHELL" --version`; `"$INTEL_CYPHER_SHELL" --help`; §3 commands. |
| C1 configuration | Validation exits 0; auth on, HTTP/Bolt loopback only; all conf/data/logs/transactions/run/temp paths match §4; heap 256/512 MiB, page cache 256 MiB, active processors 2 and exact session JVM marker visible; transaction pruning disabled/stop-at-cap plan works. Missing supported setting refuses start. | `NEO4J_HOME="$NEO4J_HOME" NEO4J_CONF="$NEO4J_CONF" "$INTEL_NEO4J_ADMIN" server validate-config`; hash/inspect exact config and subsequently inspect running JVM command line. |
| C2 explicit session start | Controller admission affirmative; session-only server reaches ready within the reviewed <=30-minute session budget; every owned Python/Java process observed nice >=10; exact local data paths; one writer/Neo4j/query. | After interface freeze: `/usr/bin/nice -n 10 "$INTEL_NEO4J" console` with manifest JAVA_HOME/NEO4J_HOME/NEO4J_CONF/TMPDIR, held by the session controller; separately capture `/bin/ps -axo pid,ppid,pgid,ni,rss,%cpu,command` and `/usr/sbin/lsof -nP -iTCP:7474 -iTCP:7687 -sTCP:LISTEN`. |
| C3 authenticated HTTP | HTTP transaction returns 200, parseable JSON, empty errors, exactly integer 1; authenticated fixed query works and an unauthenticated same request is 401/403. Loopback listeners only. | HTTP commands below; strict JSON/result check with selected stdlib interpreter, recording status/stdout/stderr/exit without credentials. |
| C4 Bolt compatibility | Listener reachable on loopback, authenticated selected matching shell returns exactly integer 1 and exits 0; no credential leakage. | `/usr/bin/nc -z -w 5 127.0.0.1 7687`; with reviewed protected credential mechanism: `"$INTEL_CYPHER_SHELL" -a bolt://127.0.0.1:7687 --format plain 'RETURN 1 AS r1_probe'`. Check the selected shell's exact credential interface before use. |
| C5 resource ceilings | Every per-second sample present and attributable to all owned descendants: Neo4j RSS <=2,000,000,000 bytes, importer <=536,870,912, RE aggregate <=3,000,000,000; CPU <=200%/100% respectively; nice >=10; one importer/DuckDB worker/thread; peak disk within §4; observed support <=6 GB with >=6 GB practical OS/user allowance. Unknown pressure/cap/ownership observation blocks. | Per-second `/bin/ps -axo pid,ppid,pgid,ni,rss,%cpu,command`; `/usr/bin/vm_stat`; `/usr/bin/memory_pressure`; `/bin/df -k "$RE_RUNTIME" /opt/local`; inventory/du commands in §4. Convert ps RSS KiB to bytes. Run the reviewed one-thread importer workload and R3 actual resource/cap controls; observations alone are not enforcement. |
| C6 normal stop | Graceful stop <=30 s; ownership-complete postinventory empty, HTTP/Bolt closed, clean shutdown diagnostic present, all retained stores/receipts preserved, no auto-resume. | Time `"$INTEL_NEO4J" stop` with manifest environment; rerun full process/listener observations; `/usr/bin/nc -z -w 5 127.0.0.1 7474` and `/usr/bin/nc -z -w 5 127.0.0.1 7687` must report connection refusal. Tool/observation failure is UNVERIFIED, not refusal evidence. Stop command exit alone is insufficient. |
| C7 error/cap/timeout shutdown | Reviewed controls exercise local cap/stop/revocation/timeout: durable phase/IDs/bars/traceback, no publication, cancellation, graceful <=30 s then only proven-owned escalation, full empty postinventory; no automatic restart; unconfirmed stop UNVERIFIED. Fresh admission required for next session. | R3 freezes executable controller commands and receipt shapes before dispatch; use its actual session-start/session-stop and fault controls, then C6 observations. S:31 names operations but not their concrete parameters, so no executable R3 fault command can be honestly supplied here. |

The C1/C2/C5/C6/C7 limits come from `S:197,213,217`; `A:24–34`. Absolute niceness is measured: `nice -n 10` is a proposed start invocation, not proof of preservation for inherited 10/>10; R3 must cover those separate controls without reducing inherited priority (`A:31`; `V:13–20,52`). There must be no services, launchd, autostart, schedules or post-stop controller restart (`A:32`; `V:18–20`).

Proposed HTTP probe commands, **only after C0/C1 confirm this selected line's endpoint/interface**:

```sh
/usr/bin/curl --disable --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 10 --config "$RE_CURL_AUTH" --header 'Content-Type: application/json' --data '{"statements":[{"statement":"RETURN 1 AS r1_probe"}]}' --output "$RE_RECEIPT/http_authenticated.json" --write-out '%{http_code}\n' http://127.0.0.1:7474/db/neo4j/tx/commit
/usr/bin/curl --disable --noproxy '*' --silent --show-error --connect-timeout 5 --max-time 10 --header 'Content-Type: application/json' --data '{"statements":[{"statement":"RETURN 1 AS r1_probe"}]}' --output "$RE_RECEIPT/http_unauthenticated.json" --write-out '%{http_code}\n' http://127.0.0.1:7474/db/neo4j/tx/commit
```

PASS requires C3's HTTP codes/body predicate, not merely curl exit 0. Proposed probes disable user curl defaults and proxies; verify these flags in C0 and ensure the explicit auth config contains only the reviewed credential settings. Freeze the JSON response shape from the selected server's documented API and require `errors=[]`, the expected column and one integer result; unexpected/empty bodies refuse. Secret file mode 0600; do not put passwords into command lines, process dumps or receipts. Freeze an equally protected shell authentication route during C0; if unavailable C4 is UNVERIFIED (`S:191`; `A:120,137`; `V:46`).

Commissioning receipts must include exact command/config/input hashes, version/ABI identities, monotonic elapsed times, stdout/stderr/exit, all owned PID/descendant attribution, per-second CPU/RSS/nice/disk samples, authenticated HTTP/Bolt outcomes, normal/error shutdown/no-resume outcomes and retained failure paths. Report missing observations as UNVERIFIED, never as a passing empty inventory. Native compatibility and measured/enforced budgets remain open until those Intel receipts exist; R1 draft delivery does not close I1a/I1c/R2/R3 or F1 (`V:3,20,34,50–60`; `S:228–233`; `A:137`).
