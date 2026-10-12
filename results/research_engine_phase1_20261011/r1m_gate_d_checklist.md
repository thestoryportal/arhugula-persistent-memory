# R1M chain A–E: authorization terms and Gate D checklist

Source: Astra round 12 (`RE/astra_r1p12_verdict.md`, GO-WITH-CONDITIONS, all four permission lines yes) over `RE/r1m_report.md` (RM) phases A–E, RM:43–62. Written before any dispatch; MAESTRO executes it and records each result next to it in `RE/r1m_gate_d_record.md`.

## Authorization terms (Astra R3)
One operator authorization covers exactly one A–E chain. Any failure, uncertainty, expiry or stop at any phase ends it; another attempt needs a new authorization. Anchor `0:a49c11de…` stays consumed and is never retried. No allowance is enlarged or reinterpreted after measurement.

## Before A
- Commit the reviewed build. Q, E, TM and RM match the round-12 pins; M, J, C, B, S, W and P match round 11.
- Name and reserve every writer of the five admitted Intel roots and the two old-state scopes (J:1620–1626, 1728). Hold them through E.

## A, then B
- A: dispatch Q once through the RM adapter (RM:44–57) with a new `RE/r1j_probe_r1m_<stamp>` prefix and W's exact argv. Commit the capture, stderr, exit and pending/final receipts and the capture hash on every outcome.
- B: `/usr/bin/python3 -B RE/r1m_evaluate.py <capture.json> RE/intel_provisioning_manifest_v10.json`. Commit its exit, output and hash. FAIL stops the chain.

## C
Fresh v10 bind through unmodified M (RM:60). Commit capture, exit, pending/final and hash before using it.

## Gate D (Astra R1 and R2). Every line must pass; unknown counts as fail.
1. Sizing evidence fits its envelope: the total bytes of the complete sizing set (capture, stderr, exit, pending/final) are ≤ 135,168 (E:21; verdict F4).
2. Uncharged receipt evidence: list every evidence file that J's receipt globs do not cover (J:1526–1539), including `r1j_probe_*` captures and evaluator records. Its bytes plus all other observed drift must fit the 1,000,000-byte receipt-drift reserve (E:15,71).
3. Pins: every reviewed hash above still matches.
4. The sizing capture is qualified, its hash is committed, and its measurement is ≤ 3,600 s old and not future-dated (E:26–66).
5. Fresh roots, core and anchor are unused, and nothing is reused from attempt 0.
6. Future collector rows and entries stay within 65,536 bytes and 64 entries; the start, window, registration and summary overheads fit the E envelopes.
7. Enough of the bind's original 870-second deadline remains for E, including preservation and commits (RM:61).
8. Writer reservations still hold over the measured baseline and old-state scopes.
If every line passes, record "GATE D GO" and run E once. Otherwise record which line failed and stop.

## E
v10 inventory through M with the fresh committed capture, hash and bootstrap, anchor `none` for the fresh core (RM:62). Commit the attempt and every outcome before the bind deadline. Never delete old state.
