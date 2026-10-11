# R2TR tracer — MAESTRO60 acceptance and sweep/tracer comparison (2026-10-11 22:46Z)

Subjects: `trace_r2_reachability.py` sha256 08e5145cf95fef3e5e87f56c8e135666a8755a62432785a8b44f5c17e3ae8c73; `test_trace_r2_reachability.py` sha256 12edf2e0b23b2a835b95076b347a0fc8513ff964d61ed65935b91fbffc168880 (match `r2tr_report.md:3`).

Reruns in MAESTRO's shell (system `/usr/bin/python3 -B`; outputs went to MAESTRO's scratchpad, not to B):
- Tests: 29 ran, OK, exit 0.
- `--against P7`: exit 1; UNRESOLVED 1302, BOUNDARIES 94, REPRESENTED 119 / REFUSED 115 / GAP 178. Output is identical to `r2tr_p7_final.json` except `generated_at`. **Positive control holds:** it reproduces Astra round 12's F1 (profile 19 verifier) and F2 (P1/P2 evaluator replication).
- `--against P8`: exit 1; UNRESOLVED 1302, BOUNDARIES 94, REPRESENTED 121 / REFUSED 193 / GAP 98. Output is identical to `r2tr_p8_final.json` except `generated_at`.

## The 98 P8 GAP rows, grouped (MAESTRO reading of `trace_r2_reachability.py:719–770` against P8; to be confirmed by the fix builder test-first)
| Rows | Site / family | MAESTRO classification |
|---|---|---|
| 62 | step0:298 `run_child`, loaded operand | **Likely tracer artifact.** P8 declares `science-train-child` (e.g. profile 8) and its composition refusal names it. `compatible()` requires equal argv length, but the tracer collapses `*args` into one loaded token (4 elements vs P8's 9), so no candidate matches. |
| 18 + 6 | W:7 / J:7 `dirname` | **Same finding as sweep G2.** The source runs slashless `dirname` (PATH lookup); P8 pins `/usr/bin/dirname` as pinned_literal. The tracer's name mismatch is the executable-selector gap seen from the other side. |
| 6 | J:24 `date` | Same as above (G2). |
| 6 | J:22 gate `.venv/bin/python` | **Likely tracer artifact.** P8 declares the gate under ADMISSION; the tracer labels a path ADMISSION only when its chain contains a `c10w_p2_gate.py` line, which the starting shell line does not. |

Sweep G1 (Bash subshell processes at W:7–8, J:7, J:25, J:30) is **not** flagged by the tracer: it does not model subshells as process starts. This is a tracer miss; the sweep is right per the installed Bash manual it cites.

## Agreement and disagreement
- Agree: G2 (executable selection by PATH) is real.
- Sweep only: G1 (Bash subshells), real.
- Tracer only: two families that look like matcher artifacts (argv-length on `*args`; gate origin). Not real gaps unless the fix builder's test-first check says otherwise.
- Both: whole-stack completeness cannot be claimed. The sweep lists Torch DataLoader workers, Git helpers, Bash/system tools and Python startup as UNRESOLVED; the tracer reports 1302 unresolved callees and 94 boundaries and says it "is not a proof about opaque library internals" (`r2tr_report.md:8`).

## What follows
G1 and G2 are bookkeeping gaps in P8/K10 (no admission bypass shown). The remaining UNRESOLVED boundaries cannot be closed by declaring more paths: under the rule that an untraced boundary never supports "no gaps", an Astra round on proving the list complete in advance would very likely come back NO-GO again. MAESTRO is bringing that scope decision to the operator now, before a fix round, rather than after another Astra NO-GO.
