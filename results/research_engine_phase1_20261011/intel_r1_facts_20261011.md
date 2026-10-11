# Intel host — R1 provisioning-freeze facts (read-only), 2026-10-11

Gathered by MAESTRO39 for Astra condition R1 (`astra_intel_a1_verdict.md:40–50`). Read-only: no `port sync`/`selfupdate`, no install, no download to the Intel Mac. Raw receipts beside this file: `intel_r1_discovery_20261011T0906Z.txt` (script `intel_r1_discovery_script.sh`), `intel_r1_tree_20261011T0907Z.txt` (script `intel_r1_tree_script.sh`), run over `ssh … '/bin/bash -s'` to `robertrhu_node2@192.168.10.2`.

## 1. Effective ports tree (answers R1's "no active source entry" point)

- `sources.conf` HAS one active entry, at line 30: `rsync://rsync.macports.org/macports/release/tarballs/ports.tar.gz [default]`. The earlier receipt `intel_discovery_20261011.txt` showed only the file's comment header, which is why it looked empty.
- Searched tree: `/opt/local/var/macports/sources/rsync.macports.org/macports/release/tarballs/ports`, extracted from the retained tarball in `…/tarballs/remote/`.
- Tree identity: `.git_commit` = `4a3293129f126ff91354e59e0ba647d49df22f25` (macports-ports); `PortIndex` sha256 `0a0ceda7c196d0a22afae686007ad0dd55f0c6c53088993424426116031da26c` (25,811,248 B, 2026-10-10 23:53).
- Acquisition artifact: `remote/ports.tar.gz` sha256 `c413261d162447c8d5ff6fd6fc9db1a7b8ec55fa0acabb04db7c3b6e3429286d` (37,209,919 B, fetched 2026-10-11 00:00 host time), with `ports.tar.gz.sig` `14cb745c…5b12`, `ports.tar.gz.rmd160` `e105f438…ac61`, `PortIndex.sig` `cf560f77…f1`. Verification key: `/opt/local/share/macports/macports-pubkey.pem` (sole entry in `pubkeys.conf`).
- Base: MacPorts 2.12.6 (`selfupdate/RELEASE_URL` → macports-base tag v2.12.6). Xcode Command Line Tools ARE now installed: `xcode-select -p` = `/Library/Developer/CommandLineTools`, `CLTools_Executables` 16.2.0.0.1.1733547573 (the "dev-tool stubs" note in `memory_mirror/intel-mac-node-access.md` is now stale).
- Pinning implication: any later `port sync`/`selfupdate` moves this tree. The freeze must either forbid sync or name this commit/tarball hash as the required identity and refuse on mismatch.

## 2. Selected ports in this tree

| port | version_revision | Portfile sha256 | notes |
|---|---|---|---|
| python312 | 3.12.15_0 (default variants +lto+optimizations) | `a0603855…a03e6` | upstream source sha256 `c2c4321961fab0fb999d66e0cecf521c2ab3994c7992873ea99e306c1094fd5a`. **v5 froze 3.12.14 — not offered by this tree; changed-version disposition required.** |
| duckdb | 1.5.6_1 | `7eb8eee4…707f` | depends_build cmake, **python314**, zstd, pkgconfig; lib croaring, openssl3 |
| openjdk21 | 21.0.12.1_0 (+release+server) | `78c9e850…85dd` | depends_build openjdk21-zulu (bootstrap JDK), autoconf, gmake, bash; lib freetype, libiconv |

Full dependency closures (`port rdeps`) are in the discovery receipt. No ports are installed. No Java runtime is present (`java_home -V` finds none).

## 3. Neo4j (no MacPorts port — `port search neo4j` / `cypher`: no match)

Upstream, read 2026-10-11 from neo4j.com (not yet downloaded anywhere):
- Current Community releases (deployment center): **2026.09.0** (2026-09-21, calendar line) and **5.26.32** (2026-10-09, 5.26 LTS line). Linux/Mac artifact is the unix tarball.
- Published sha256 files at `https://dist.neo4j.org/neo4j-community-<v>-unix.tar.gz.sha256`: 2026.09.0 → `cdaa0905d9a533bbbc474d239c268f69978982eb5ca3177666c04c9792d1c399`; 5.26.32 → `d279ae6a9b38034280681a558b0cd222dce89f87cc3d9867f1f7bd28ef5ebc30`. These were read through a summarizing web fetch: **re-read the .sha256 file and hash the downloaded bytes at acquisition**; do not trust these strings alone.
- Requirements page (Operations Manual, "Version 2026.09 (Current)"): Java SE 21 and 25 supported (Java 21 matches openjdk21 above); **macOS 13/14/15/26 listed for personal/development only, not production**; x86_64 supported; dev minimum 2 GB RAM (16 GB recommended), 10 GB disk.
- The deployment center does not show a direct tar link; the `dist.neo4j.org` URL pattern above is where the .sha256 files resolved.

## 4. Disk

`/` and `/System/Volumes/Data`: 488,245,288 KiB total, 467,303,544 KiB available (2026-10-11 09:06Z).

## Open for the freeze (not decided here)

Python 3.12.14 → 3.12.15 (or a python.org 3.12.14 build) disposition; Neo4j line choice (2026.09.0 vs 5.26 LTS) and acquisition route; whether duckdb is built from source (pulls python314 + cmake) or installed from a MacPorts binary archive, and that archive's identity; sync policy for the tree above.
