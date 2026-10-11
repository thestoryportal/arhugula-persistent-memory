# Intel R1 install sizes — measured read-only (MAESTRO40, 2026-10-11 ~09:40Z)

Answers Astra F3 in `astra_r1p_verdict.md` ("no demonstrated fit within ≤1 GB setup growth / ≤15 min"). Nothing was installed or written on the Intel Mac; archives were streamed through `bzip2 -dc | wc -c` / `gzip -dc | wc -c` on the M3, so no archive was saved to disk.

## Method and receipts
- Runtime closure: `port -q rdeps --no-build openjdk21 python312` on the Intel Mac (MacPorts 2.12.6, macOS 14.8.9 x86_64, ports tree as pinned in `intel_r1_facts_20261011.md`), versions from `port -q info --version --revision`. Receipt: `intel_r1_runtime_closure_20261011.txt` (sha256 `ecc9ed24…46c6`).
- Archive names from the `packages.macports.org/<port>/` listings; compressed bytes from HTTP `Content-Length`; unpacked bytes = decompressed tar stream length (an upper bound on installed bytes, since it includes tar headers). Receipt: `intel_r1_sizes_20261011.tsv` (sha256 `fb773fd2…fe51`; columns port, archive, compressed, unpacked). Scripts: `intel_r1sizes_probe.zsh`, `intel_r1missing_probe.zsh`, `intel_r1unpack_probe.zsh`.
- The digests and sizes below come from HTTP headers or a summarizing web fetch (DuckDB wheels). Hash the real bytes at acquisition before trusting them.

## Findings
1. **Ready-made Intel (darwin_23 x86_64) archives exist** for 17 of the 25 closure ports. The large ones: openjdk21 21.0.12.1_0 194.4 MB compressed → 355.4 MB unpacked; python312 3.12.15_0 42.8 → 209.9 MB; openssl3 8.5 → 44.1 MB.
2. **Must be built from source at the pinned tree** (no darwin_23 x86_64 archive for the pinned revision): expat 2.9.0_0 and sqlite3 3.54.0_0 (arm64 only; the x86_64 archives are older versions), python_select / python3_select (no darwin_23 noarch), plus the `tcl` stub. All are small (no build deps beyond the installed Command Line Tools); their sizes and times are not measured here.
3. **MacPorts duckdb 1.5.6_1 has no x86_64 archive** (only 1.5.6_0 x86_64, 214.5 MB unpacked, and croaring 5.2.3_0 has none). The source build pulls python314 + cmake, which would break the 15-minute limit. **PyPI publishes the same DuckDB 1.5.6 as `duckdb-1.5.6-cp312-cp312-macosx_10_13_x86_64.whl`** (17,405,278 B, sha256 `79de3dfa8705b1ba0d59e7e3252e40ff399e0afd12f485502a6c7bf7c2fd809a`), which installs into python312 with no compile. Choosing that route is a design call for MAESTRO and Astra, not an operator question.
4. **Neo4j Community unix tarballs:** 2026.09.0 274.3 MB → 299.4 MB unpacked; 5.26.32 LTS 152.6 → 165.1 MB.

## Conservative peak setup growth (wheel route for DuckDB)
MacPorts keeps each image archive under `/opt/local/var/macports/software/` next to the activated files, so archive and unpacked bytes both count.

| Part | MB |
|---|---|
| MacPorts binaries, archive + unpacked (255.4 + 658.3) | 913.7 |
| Source-built small ports (expat, sqlite3, stubs), including build dirs (allowance, unmeasured) | 100 |
| DuckDB wheel + install (17.4 + ≤100 allowance) + venv/pip (~30) | ~150 |
| Neo4j 5.26.32 LTS, tarball + unpacked | 317.7 |
| **Total, Neo4j 5.26 LTS** | **≈1,480** |
| Total with Neo4j 2026.09.0 instead (+256) | ≈1,740 |

**Verdict: the package set does not fit ≤1 GB of setup growth on any route.** Java + Python and their parts alone use ~0.91 GB. Deleting the retained archives and the Neo4j tarball after verification still leaves ≈1.2 GB for the smaller variant, and peak growth (before that deletion) is what the amendment caps. Under amendment `phase1_intel_amendment_v1.md` (setup ≤1,000,000,000 B within the 6 GB pilot/setup cap), this is an operator budget decision.

**Time:** with the DuckDB wheel, about 0.45–0.55 GB of downloads plus a few small compiles. That plausibly fits 15 minutes but is not measured; the freeze must measure it at commissioning.
