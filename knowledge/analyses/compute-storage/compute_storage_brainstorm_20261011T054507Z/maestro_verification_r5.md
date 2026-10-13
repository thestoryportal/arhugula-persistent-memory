# MAESTRO verification of the R5 completion-table draft

MAESTRO37, 2026-10-11T08:22:25Z (`date -u`). Subject: `integration_r5_completion_table.md`, sha256 `f20dcea3ab9db4253f5f6cb2bb183fa9b0526fb2ede2bf76074c819077bb682e`, drafted by a MAESTRO subagent from the brief whose acceptance test is repeated below.

**Result: the draft passes the acceptance test and goes to Astra unchanged.** The answers below to its section-6 questions are MAESTRO's; they are not edits to the draft.

## Checks run

- **Completeness.** The r3/r4/r5 verdicts contain 23 finding IDs (T1–T7, U1–U8, V1–V8, `grep -ohE '\b[TUV][0-9]+\b'`). Section 5 has a row for each, each exactly once.
- **Citation sample** (random, seed 20261011). Finding rows T2, U2, U4, U5, V1 and table rows I1a, I3a, I4a: every cited `path:line` was opened, and each says what the row claims. Examples: `r5:10` reads "U2. RESOLVED — Clearance now requires an inventory after publication, including the lock-timeout branch"; `integration_plan.md:25` still shows the superseded 400/100/80/100/6 caps, as I3a says.
- **Pins.** All 41 section-1 SHA-256 pins re-hashed at HEAD `27e9699c`: 0 drift, 0 missing.

## Answers to the draft's section-6 questions

1. **T1, T5, U2 stay "already resolved" with an R2 note.** Astra r1 says earlier resolved defects "should not be relabelled unresolved simply because they appeared in r3/r4" (`astra_r1_verdict.md:47`); the failure class carries into R2 through the note.
2. **No new operator question now.** The 05:18Z answer said a change to the reservation step's shape "would go back to the operator" (`RE/operator_answers_20261011T0518Z.md:7`). It went back: at 06:30:29Z the operator approved choice 9, "Intel databases/builders continue from their own files while M3 runs science. Large operations that touch memit pause/wait under M3-side coordination" (`decisions_log.md:117–121`). R2 must stay inside that shape; a contract that needs more goes back to the operator.
3. **Do not force-add the logs.** `.gitignore:41` ignores `*.log` by policy. The draft pins their SHA-256s and cites the tracked `run.exit`; Astra reads the worktree directly.
4. **Open storage fork, not settled here.** The Drive source is ~287 GB (`PS:90`) against 250 GB recovery + 50 GB staging on the Intel Mac (`decisions_log.md:191`), and the 268.5 GiB parked set exceeds 50 GB staging. Choosing between a smaller selected upload set, batched uploads, or new caps is the operator's decision. MAESTRO will present options when amending the Drive activation plan for the Intel-first route (queue item `drive-activate`). I3b and I7 stay OPEN on it.
5. **Amendment 16 has had no Astra review.** It is added to this Astra round's scope.
6. **Proposed I4a baseline:** MB38 GREEN (against `cb1693bc`) plus the queue-tab host receipt `QB/host_attempt3`, with the `team_dashboard.sh` change from 761f0c65 to f5dc68bf disclosed. Astra rules on whether this suffices.
7. **Owners.** MAESTRO is the accountable owner of every row. Builder sessions are named in each dispatch brief, which pins its integration row. Astra rules on whether that meets R5's "named owner".
8. **Yes.** The `drive-activate` queue item now points to I7 and the Intel-first amendment.
9. Done above: 0 drift at `27e9699c`.
10. **P1–P5 (r3 properties) and r1/r2 S*/R* are not findings under R5's wording** ("every r3/r4/r5 finding"). Astra is asked to confirm.
11. **Deskflow cannot block a science launch.** The admission gate blocks only executables matching `python…|…ollama…|…llama…|…mlx…` (`tools/c10w_p2_gate.py:22,52`); `Deskflow` and `deskflow-core` match neither. Their CPU and memory share during science runs is not measured.
