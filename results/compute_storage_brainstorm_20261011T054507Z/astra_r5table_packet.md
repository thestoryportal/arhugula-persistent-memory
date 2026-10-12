# Astra review packet — D-HW-2 condition R5 (integration completion table)

You are the cross-family reviewer. Read-only. Work from this repository (HEAD `6b76c197`); cite `path:line` for every claim.

## Question
Your r1 verdict (`results/compute_storage_brainstorm_20261011T054507Z/astra_r1_verdict.md`, R5 at :30–37, F5 at :16, "What relocation does/does not remove" at :45–47) required a refreshed, split integration completion table before any affected dispatch. The draft is `integration_r5_completion_table.md` (subagent-authored); MAESTRO's verification and answers to its open questions are `maestro_verification_r5.md`. Decide:

1. Does the draft discharge **R5** as written: later storage/MB38 receipts with source identities and later changes; current queue revision; per-row owner, version/hash, disposition, shared paths/interfaces, resource commitments, predecessor receipts, permitting review (fields at `integration_plan.md:49–51`); every r3/r4/r5 finding mapped with evidence?
2. Are the **finding dispositions** right? In particular: nothing is "premise removed"; T1/T5/T6/T7/U1/U2/U4/U7 are "already resolved" with R2 notes; the rest are "replacement requirement" → R2 (V6 also R4); V7 (no-resume) and V8 (failure controls) are disposed explicitly. Name any row whose evidence does not support its disposition.
3. **Amendment 16** (Intel caps resized to the measured 512 GB SSD: 250/50/40/50/6 GB, ≥80 GB free; `decisions_log.md` "Amendment 16") has had no Astra review. Review it now, including the open fit question MAESTRO answer 4 records (~287 GB Drive source and 268.5 GiB parked set vs 250 GB recovery / 50 GB staging).
4. Rule on MAESTRO answers 6 (I4a acceptance baseline), 7 (MAESTRO as accountable owner of every row; builders named per dispatch brief) and 10 (P1–P5 and r1/r2 S*/R* are not "findings" under R5).
5. Does anything in the draft, or in MAESTRO's answer 2 (choice 9 already carries the reservation-shape change back to the operator), weaken a binding requirement?

A table row stays OPEN until its own predecessors and reviews exist; this round can at most find the table itself adequate. Out of scope: freezing R2/R4, the research-engine spec rewrite, the Drive plan amendment, amendments 18–19 (reviewed in `astra_a18_verdict.md`).

## Verdict format
First line: `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO` (whether the table discharges R5). Then `F<n>. [severity: blocker|condition|note] <claim>. Evidence: path:line. Consequence: …`, then required changes `R<n>`, then "What I checked and did not check".

## Disclosed drift
The draft pins `docs/program_state.json` at `0a9818f3…` (rev 08:17:48Z). Commit `6b76c197` then changed only the `drive-activate` item (state → blocked, its three operator questions withdrawn until the Intel-first plan exists) and `work_queue.edited`; see `git diff 27e9699c 6b76c197 -- docs/program_state.json`. All other 40 pins re-hashed with zero drift (`maestro_verification_r5.md`).

## Subject files (SHA-256 now)
- `results/compute_storage_brainstorm_20261011T054507Z/integration_r5_completion_table.md` f20dcea3ab9db4253f5f6cb2bb183fa9b0526fb2ede2bf76074c819077bb682e
- `results/compute_storage_brainstorm_20261011T054507Z/maestro_verification_r5.md` f7924dcca747b6fd64b9977b40e80ab8662f4f9963b5118ec0731ad6a20aee0d
- `results/compute_storage_brainstorm_20261011T054507Z/astra_r1_verdict.md` ef273bede821f9d82b828dccb8728db5ccca8fc893db70664359c3eb335ad26f
- `results/compute_storage_brainstorm_20261011T054507Z/integration_plan.md` b650e88071e987b84006e2467c4a8c8a42deee0bdc35504ac6f652f4a870d8a7
- `results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md` d8dda823e63ceb4297dbfda5897cf689b394aded5a096b5b468a809ef2c0db03
- `results/compute_storage_brainstorm_20261011T054507Z/design.md` 20f88e7c50acff3e0061dd9c6dee0e70e68627a197e5921e9acb344a075717b1
- `docs/program_state.json` d94dc3ebdee2eab970b6cf41cad1dc9e57f7f4bf205a4f6df9cd5034f796d706
