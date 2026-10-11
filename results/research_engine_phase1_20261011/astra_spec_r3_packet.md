# Astra review — research-engine phase-1 spec, r3 (S1 pending-science contract + §13 settlement)

You are the program's independent cross-family reviewer. Work read-only: read and search only.

In spec r2 (`results/research_engine_phase1_20261011/astra_spec_r2_verdict.md`) you returned GO-WITH-CONDITIONS: R2–R4 applied; R1 partial, with finding S1 and five minimum properties under "Required before freeze". MAESTRO35 (the reservation owner) has now written:

- `results/research_engine_phase1_20261011/science_reservation_contract_v1.md` (**SR**, sha256 ee6f0c3aef920bc610de8dba711396669ed2ca3e916e7cbcd3280093091109ea): the pending-science authority.
- `results/research_engine_phase1_20261011/phase1_spec_v3.md` (sha256 cbd1131974135d56ca9950740c9013fb467bac7cc869b15aa8e7931e88aa6fee): v2 + SR wiring + §13 settled; change table in §15. v2 (2e021f92…) is unchanged. See every change with `diff phase1_spec_v2.md phase1_spec_v3.md`.
- `results/research_engine_phase1_20261011/provisioning_dryrun_20261011.txt`: the Homebrew dry-run receipt behind the §13 pins.

Review for:
1. For each of your five r2 minimum properties (authority and scope; unambiguous state; validity and transitions; coordination; observable enforcement), is SR sufficient? Cite SR lines.
2. Soundness. Find any reachable state in which science that is pending or running is observed as IDLE; any race between pending publication and RE admission or publication; any path by which the RE delays or suppresses science; any watcher hole (watcher death, PID reuse, `neo4j stop` hanging, the clock, memit unmount). Coverage of coordinators is procedural (MAESTRO runs the writer) plus a process backstop (SR §5). Is that acceptable given the existing gates in `tools/c10w_p2_gate.py` and `tools/run_c10v_stage.sh`?
3. Are AC17 and AC21 checkable, with the valid-IDLE positive control, the four AC17 cases you required, and host termination kept as an acceptance obligation?
4. Did v3 weaken or drop any v2 requirement, or change a section that §15 does not name?
5. Is §13 now settled enough to freeze, apart from the two operator answers it names (shared-dependency upgrades; adopting the reservation step in science launches)?

Deliverable: Markdown to stdout, exactly:
```
# Astra spec r3 verdict — research-engine phase 1
Verdict: GO | GO-WITH-CONDITIONS | NO-GO
## S1 properties
P1 authority/scope. MET | PARTIAL | MISSING — <evidence: file:line>
P2 state. …
P3 validity/transitions. …
P4 coordination. …
P5 enforcement. …
## Findings
T1. [severity: blocking|condition|note] <defect>. Evidence: <file>:<line>. Consequence: <...>.
## Required before freeze
## What I checked and did not check
```
Ground every finding in a line you read. Do NOT re-review R2–R4 (closed in r2), propose style rewrites, or re-argue the operator's choices (Neo4j via Homebrew, budgets).
