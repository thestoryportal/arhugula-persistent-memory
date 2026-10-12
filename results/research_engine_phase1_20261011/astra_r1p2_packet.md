# Astra review — Intel provisioning freeze v2 (R1 / I1c), round 2

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Do not run r1b_host_commands.sh or anything that fetches. Repository HEAD is the commit that adds this packet. RE = `results/research_engine_phase1_20261011`.

Context: your round-1 verdict `RE/astra_r1p_verdict.md` was NO-GO (blocking F3: no demonstrated fit within ≤1 GB setup growth / ≤15 min; R1–R5). Since then:
- MAESTRO40 measured sizes read-only: `RE/intel_r1_sizes_20261011.md` with `RE/intel_r1_sizes_20261011.tsv` and `RE/intel_r1_runtime_closure_20261011.txt` (≈1.48 GB conservative peak with Neo4j 5.26 LTS).
- Operator ruling, Amendment 20 (`results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md`, section "Amendment 20"): setup growth ≤2,000,000,000 bytes; pilot+setup 7 GB; provisioning stays ≤15 min. This is the disposition your F3 asked for.

Subject (drafted by Codex builder R1B; MAESTRO40 checked: JSON parses, `bash -n` passes, all 48 manifest entries carry a status, sizes match the measured TSV byte-for-byte, the one full hash present matches `RE/intel_r1_facts_20261011.md`, the host script contains no install/sync/rm/sudo/ssh command):
- `RE/intel_provisioning_freeze_v2.md` (sha256 474405381d5b992340507e750675a9f690daa0eecdc152a7122b763b2344a4e2)
- `RE/intel_provisioning_manifest_v2.json` (sha256 e43c620798b680363a53a3594500ae4682943f44f7bd788ab85abaab77583076) — the single machine-consumable source
- `RE/r1b_host_commands.sh` (sha256 f6eb643b6e0f14295cda590b5d9af441851c98a13631e9d0486c26a702794c56) — read-only fetch/verify commands MAESTRO would run
- Builder report and finding map: `RE/r1b_report.md` (its "What could not be closed" names R3–R5 blockers)

Review for:
1. Does each round-1 finding F1–F7 and R1–R5 now close, or is it correctly named as open? Cite verdict line → freeze line.
2. F3 under the 2 GB cap: is the peak-growth table conservative and complete (coexistence, image archives, source-build dirs, verification extraction, caches, retained failures, DuckDB wheel), and is the provisioning clock defined?
3. Is `r1b_host_commands.sh` safe and sufficient as the next step: read-only, writes only to a mktemp dir, and fills each NEEDS-FETCH entry it targets? Anything it must not run?
4. The R3 blocker (source-build time/space for expat, sqlite3 and the stubs cannot be measured read-only): what is the smallest acceptable way to obtain that evidence (e.g. a throwaway-prefix build on the Intel Mac) before mutation of the real prefix, and does it need the operator?
5. Any status mislabelled, any second source of truth between the .md and the JSON, any unpinned or fallback path.

Out of scope: R2 clearance contract; R4 dashboard record; Drive activation; the DAG/RAG/ICM brainstorm.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; a line "NEXT STEP ALLOWED: <yes/no> run r1b_host_commands.sh as written"; and "What I checked and did not check".
