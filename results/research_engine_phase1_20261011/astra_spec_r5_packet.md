# Astra review — research-engine phase-1 spec, r5 (SR v3 against r4 U1–U8)

You are the program's independent cross-family reviewer. Work read-only: read and search only.

In spec r4 (`results/research_engine_phase1_20261011/astra_spec_r4_verdict.md`) you returned NO-GO on SR v2: U1–U6 blocking, U7–U8 conditions. Rather than patch v2's watcher, MAESTRO35 simplified. SR v3 has one enforcer on the science side (`pending` terminates the research engine and confirms that it is gone), identifies RE processes by anchored command patterns instead of a registry or a living leader, and drops the watcher, controller thread, heartbeat and registry. The rationale is in SR v3's opening paragraph, measured against R1's own wording (`astra_spec_r1_verdict.md:17`). No reviewed file was edited.

- `results/research_engine_phase1_20261011/science_reservation_contract_v3.md` (**SR v3**, sha256 79ba8325590d60e636d3ad6951dd1298d2de633c305aba0c69db1da060c96de9).
- `results/research_engine_phase1_20261011/phase1_spec_v5.md` (sha256 491cdc1c84f978ffdfacfce45dfecca12f65e84043f30cdddc865cbea4302ed0): v4 + SR v3 wiring; change table §17. See every change with `diff phase1_spec_v4.md phase1_spec_v5.md`.
- `duckdb_1.5.5.lock.txt` (sha256 f8ffcdea…) and `duckdb_lock_parse_receipt_20261011.txt` (U7).

Review for:
1. U1–U8: RESOLVED | PARTIAL | OPEN each, with the SR v3/v5 line.
2. Does dropping the RE-side watcher still satisfy R1 as written at `astra_spec_r1_verdict.md:17`, and v2's AC17 obligations as carried through v5? If anything R1 or AC17 requires now has no mechanism, name it.
3. New defects in SR v3: the anchored ownership patterns (false positives against Codex/Claude argv; false negatives, such as a JVM not started with the token, or a helper process the RE spawns); the single 30 s deadline from invocation; the lock-timeout path with post-publish inventory; `release` from one inventory under the lock with the tokens rule; the P-memit premise. Look for any interleaving that admits or publishes after a `pending` publish, any false IDLE, any unbounded wait, and any way science launches while an RE process lives.
4. Are AC17/AC21 and SR §6 cases 1–18 checkable and sufficient, with host termination still provable only by §7 commissioning?
5. Did v5 weaken or drop any v4 requirement beyond what §17 names?
6. Apart from implementation, is anything left before freeze?

Deliverable: Markdown to stdout, exactly:
```
# Astra spec r5 verdict — research-engine phase 1
Verdict: GO | GO-WITH-CONDITIONS | NO-GO
## r4 findings status
U1. RESOLVED | PARTIAL | OPEN — <evidence: file:line>
…
## Findings
V1. [severity: blocking|condition|note] <defect>. Evidence: <file>:<line>. Consequence: <...>.
## Required before freeze
## What I checked and did not check
```
Ground every finding in a line you read. Do NOT re-review R2–R4 or the operator's choices, or propose style rewrites.
