# Astra review round 14 — the executed R1N v11 A–E chain (post-run audit)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Run nothing except read commands (`cat`, `sed -n`, `grep`, `shasum`, `git show`, `git log`). Do not contact the Intel Mac. Repository HEAD is the commit that adds this packet.

Aliases: `RE` = `results/research_engine_phase1_20261011`. `V13` = your round-13 verdict `RE/astra_r1p13_verdict.md` (GO-WITH-CONDITIONS). `GD11` = `RE/r1n_gate_d_checklist.md`; `AD` = `RE/r1n_gate_d_addendum_r13.md` (R1–R3); authorization `RE/operator_authorization_r1n_20261011T1637Z.md`. Reviewed code as in round 13 (A = `RE/r1n_sizing_dispatch.py`, N = `RE/r1n_evaluate.py`, M = `RE/r1l_make_bundle.py`, J11 = `RE/intel_provisioning_manifest_v11.json`).

Subjects:
- `REC` = `RE/r1n_chain_record_20261011.md` sha256 df73fdbb6782add46c933024621c304492dce854aafd30ae7566880f698e83c8 (75 lines): MAESTRO51's record of every step, with outputs verbatim.
- `DRV` = `RE/r1n_chain_driver_maestro51.py` sha256 f459ba06eb8796b4339d513fe6769eb385894a3a86ae0409c4a54bf1779183c9 (163 lines): MAESTRO51's own driver for C, Gate D and E. Not reviewed before use; committed (49c71b14) before C and dry-run against the consumed R1J bind, where D6/D8 failed as required. A later edit of D6 was made before that commit.
- Evidence (all committed): sizing `RE/r1j_probe_r1n_20261011T164501Z.*`; evaluation `RE/r1n_evaluate_20261011T164501Z.{out,stderr,exit}`; bind `RE/r1j_bind_r1n_20261011T164907Z.*`; inventory `RE/r1j_inventory_0_a32411006dc3.*`; attempt `RE/r1j_attempt_0_a32411006dc3.json`. Commits 741a9ef6..1320100e.

Outcome in brief: A rc 0; B PASS (receipts 37,732,722 ≤ 42,000,000; setup 1,949,513,676 ≤ 2,000,000,000; LIVE 2,175,092); C rc 0; Gate D 8/8 PASS → GO; E rc 0, qualified 808 s before the bind deadline, status OBSERVATION-ONLY.

MAESTRO51 judgment calls to test (REC lines cited):
1. Intel survey: a user Launch Agent `org.deskflow.autostart.plist` (created before the R1M survey, RunAtLoad `open -a Deskflow.app`) was judged not a writer. The R1M record said "no Launch Agents".
2. Evidence census: 10 `intel_identity_probe_*` files were added as `--extra-receipt`; `r1l_logs_20261011/` (builder unittest logs), survey TSVs and scripts were excluded as not receipts.
3. B's output was written to scratch and copied into RE afterwards so N could not count its own output; D4 then charged it (4,248 bytes) against D(B).
4. DRV's Gate D: D4 charges only evidence new since B, treats the bind set as covered by the reserved 2,500,000 fresh-bind envelope, and observes old-state drift by a fresh stat but does not re-measure inventory rows (row drift since A, ~4 min, left to D(B)). D6 checks the binding receipt's manifest/identity/probe input hashes and that only `binding_provenance`, `collector`, `window_seal` differ from J11. D8 required ≥ 420 s left (declared before C).
5. E's bootstrap bytes were computed by DRV from committed bytes rather than M's `--bootstrap-bytes-only` path.

Review for:
1. Did the chain follow GD11 + AD + V13's conditions exactly? Name any step taken out of order, any gate recorded without committed evidence, or any condition skipped.
2. Are judgment calls 1–5 sound? For each: sound, doubtful (why), or wrong (consequence).
3. Does DRV implement each of GD11's eight checks faithfully, or does any check pass something GD11 would stop? Does anything in DRV (outside M/A) alter what was sent to the Intel Mac?
4. Is anything claimed in REC not supported by the committed evidence?
5. What does the completed inventory now establish, and what remains open, given its OBSERVATION-ONLY status and empty `established` list?

Verdict format: first line `VERDICT: CLEAN` | `CLEAN-WITH-NOTES` | `DEFECTIVE`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required follow-ups `R<n>`; "What I checked and did not check".
