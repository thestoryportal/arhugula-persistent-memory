# Astra review — research-engine phase 1, Intel host amendment v1 (fresh round)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Repository HEAD is the commit that adds this packet.

Context: your spec r5 (`results/research_engine_phase1_20261011/astra_spec_r5_verdict.md`) was NO-GO on the same-M3 design (v5 + SR v3). The operator then moved the research engine to a separate Intel MacBook Pro (D-HW-2). The approved design for the move is `results/compute_storage_brainstorm_20261011T054507Z/design.md` (call it B/design.md); lines 239–245 list what a new host spec must change, and line 245 requires a fresh permitting review of it. Your R5-table round 2 (`B/astra_r5table_r2_verdict.md`, GO) approved the work map `B/integration_r5_completion_table.md`, rows I1a–I1c (lines 95–97) and the finding map (section 5).

Subject:
- `results/research_engine_phase1_20261011/phase1_intel_amendment_v1.md` (sha256 e6b0199782b6155a4d4813399b449796e00a007f6059746eb0122af1780a99a0). Drafted by a Codex builder, verified by MAESTRO38 (base v5 unchanged, sections A–G present, six citations checked). It amends, and leaves byte-identical, `phase1_spec_v5.md` (sha256 491cdc1c84f978ffdfacfce45dfecca12f65e84043f30cdddc865cbea4302ed0).
- `results/research_engine_phase1_20261011/intel_discovery_20261011.txt` (sha256 5f1aa9d8806826f5543e37e68f3b6d34d2e0c4bd41e76f3f2fe1f27e4f527229): read-only checks MAESTRO38 ran on the Intel Mac after the draft, without a ports-tree sync. Facts the draft did not have: MacPorts has no neo4j or cypher port; openjdk21 @21.0.12.1; python312 @3.12.15 (v5 froze CPython 3.12.14); duckdb port @1.5.6_1; the MacPorts pkg is no longer in ~/Downloads.
- Builder report: `results/research_engine_phase1_20261011/re1_report.md`.

Review for:
1. Does the amendment satisfy B/design.md:239–245 items 1–5 and rows I1a/I1c, leaving R2 (the shared-disk clearance contract, row I1b) as a named external dependency rather than drafting it? Is the R2 interface it relies on (section B) sufficient and not over-specified?
2. Section E: MAESTRO's reading that operator choice 9 (`B/decisions_log.md:115–121`, 06:30Z) is the operator's later approval of the changed shape, so operator answer 1's "goes back to the operator" condition (`operator_answers_20261011T0518Z.md:7`) is met. Agree or disagree, with evidence. If you disagree, say exactly what question the operator must be asked.
3. Section C (V7, no automatic resume) and the AC17/AC21 accounting in section B: is every v5 acceptance criterion tied to the old reservation kept, replaced with rationale, or removed because its premise is gone?
4. Section D against the discovery receipt: which pin rows are now wrong or need a different source (e.g. Neo4j from an upstream tarball rather than MacPorts), and what must the provisioning freeze contain? No pin is accepted until real checks on the Intel Mac prove it.
5. Section G: is each of the 23 findings dispositioned honestly (relocation does not turn a NO-GO into GO)?
6. Anything in F (preserved semantics) weakened.

Out of scope: drafting R2; the Drive backup; the backups-volume audit.

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; "What I checked and did not check".
