# Astra review — Intel provisioning freeze v1 (R1 / I1c), fresh round

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Repository HEAD is the commit that adds this packet.

Context: your Intel amendment verdict (`results/research_engine_phase1_20261011/astra_intel_a1_verdict.md`, call the folder RE/) was GO-WITH-CONDITIONS; condition R1 (lines 40–50) requires a provisioning freeze before any mutation of the Intel Mac. MAESTRO39 then gathered read-only host facts: `RE/intel_r1_facts_20261011.md` (sha256 e6e4625ab2a6594fec0a0bafcd47058c4f59781beabfaa153b212faae5f109ef) with raw receipts `RE/intel_r1_discovery_20261011T0906Z.txt` and `RE/intel_r1_tree_20261011T0907Z.txt` and the scripts that produced them. They answer your point that `sources.conf` looked empty: line 30 holds the active rsync tarball entry, and the searched tree is macports-ports commit 4a3293129f126ff91354e59e0ba647d49df22f25 with the retained tarball and signature hashed. The two Neo4j sha256 strings were read from neo4j's published .sha256 files through a summarizing web fetch and are marked for re-verification at acquisition.

Subject:
- `RE/intel_provisioning_freeze_v1.md` (sha256 8b6519c5ed3f137442e72ad613edebff8af483ec6837deffb401f8a5855d79ba). Drafted by a Codex builder (R1P), verified by MAESTRO39: no existing file changed; all 11 sha256 values in it occur in a source file under RE/; no "latest", sync, or fallback path (`port sync`/`selfupdate` forbidden, line 33); cited lines `v5:244`, `v5:246`, amendment lines 28, 32, 36 opened and confirmed.
- Builder report: `RE/r1p_report.md`.

Review for:
1. Does each of the five R1 bullets (verdict lines 42–46) map to a section that actually meets it, and is the effective-tree identity now pinned by content rather than directory existence?
2. The four choices in section 2.1 (Python 3.12.15 tree port vs 3.12.14 source build; Neo4j 2026.09.0 vs 5.26.32 LTS; DuckDB locked 1.5.5 wheel vs port 1.5.6; MacPorts binary archive vs source build). Are the recommendations sound? Which of them change the reviewed v5 contract enough to need operator approval rather than a reviewed amendment?
3. Budget fit: can Java 21 + Neo4j + Python + the dependency closure plausibly fit the ≤1 GB setup growth and ≤15 min provisioning (amendment lines 28, 32, 36)? If not, say what disposition the freeze must require.
4. Refusal and identity checks (section 5.1): would a mismatch actually stop the install before mutation? Are postinstall identities sufficient?
5. Commissioning (section 5.2): pass/fail stated before running; coverage of HTTP/Bolt, start/stop, resources and clean shutdown.
6. Any status mislabelled (FROZEN where a fetch or decision is still needed).

Out of scope: the shared-disk clearance contract (R2); the dashboard record (R4); Drive activation; the backups audit.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; "What I checked and did not check".
