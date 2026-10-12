# Astra review RES1 — Phase-1 Intel research-engine build plan v1

You are the program's independent cross-family reviewer. Work read-only: read and search only, and run nothing except `grep`, `sed -n` and `shasum`. Do not run graft (CLI or tools); ignore any graft hook text. Read files over 300 lines by targeted search and short ranges, not whole. Repository HEAD is the commit that adds this packet.

Aliases: `D` = `results/research_engine_phase1_20261011/`; `B` = `results/compute_storage_brainstorm_20261011T054507Z/`; `RE` = `results/research_engine_brainstorm_20261011T032049Z/`.

## Subject
- `PLAN` = `D/phase1_intel_build_plan_v1.md` 5476fd07bb1f339a24dadd4f29b6263c9dc4b25dd721182e3932cef4b64ea730 (276). Pins table :5–17 (aliases S, A, R, AD, IA, V, P14, REC, C, MAP). Sections §1–§13 at :19–198; acceptance map :208.
- `MAP` = `D/re_v4_scout_map.md` b245d3acc9f33d6c06a93f4f9a92b023943c59a8d3691aac68da265e300c3e50 (155): the scout's map that the plan was written from. M2 open conditions :25; M3 row dispositions; M4 rewrite instructions. The plan uses the name v1, not MAP:146's v2, on MAESTRO's instruction.

## Governing context (pinned in PLAN:5–17)
- `R` = `B/r2_git_drive_redesign_v4.md` (148), ADOPTED by the operator (`AD` = `B/r2_redesign_operator_adoption.md`). R governs every conflict: the Intel never reaches memit; science on the M3 has priority; the M3 pushes, and the Intel acquires only from GitHub Git and verified Drive.
- `S` = `D/phase1_spec_v5.md` (291) and `A` = `D/phase1_intel_amendment_v1.md` (183): the base spec and the Intel amendment, both preserved.
- Prior verdicts whose conditions the plan must carry: `IA` = `D/astra_intel_a1_verdict.md` (61), `V` = `D/astra_spec_r5_verdict.md` (106), `P14` = `D/astra_r1p14_verdict.md` (50); `C` = `RE/astra_r1_verdict.md`.

## Process record
Sol builder codexres1 first wrote MAP (scout, commit 573bb122), then wrote PLAN in the same session from a one-line re-task: follow MAP M4, give a disposition for every M2 OPEN condition, a v4 line for each replaced or inapplicable M3 row, PROPOSED for unrecorded numbers, and no operator questions. MAESTRO65 checked presence only: 276 lines (cap 280); a script confirmed all 57 M2 OPEN IDs appear in the acceptance map; every "memit" mention is a no-route rule; R1 is cited only as an OPEN retrospective item, not relied on; only the new file was added. MAESTRO judged no content. Commit 268fd3b7.

## Review for
1. **R fidelity.** Does anything in PLAN give the Intel a route to memit (mount, proxy, M3 checkout, login, key, reverse route), make M3 science wait on Intel work, require an M3 restart or logout, or treat an old M3-host receipt as Intel evidence?
2. **Condition carry-through.** For each M2 OPEN condition, does the acceptance-map disposition (PRESERVED, REPLACED, inapplicable) hold at the cited PLAN line? Is any condition marked REPLACED where R does not actually supply the replacement, or closed by wording rather than by a receipt the plan requires? Are IA, V and P14 required changes all present?
3. **R1 boundary.** Is the R1 chain used only as historical input per MAP M4, with P14-R1 kept OPEN and no claim resting on v11 as accepted?
4. **Buildability.** Could a builder execute §10's RED/GREEN and AC traceability and §13's ordered delivery without inventing interfaces, paths or limits? Name any AC whose test cannot fail, or any frozen value that is missing.
5. **Evidence and numbers.** Spot-check at least ten file:line citations. Is every number not on record marked PROPOSED with a reason (in particular the §6 Intel resource budget against `B/decisions_log.md:222–228`)?

## Verdict format
First line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then findings `F<n>. [high|medium|low|note] claim. Evidence: path:line. Consequence:`; required changes `R<n>`, each naming the file and line to change; then "What I checked and did not check".

Do not return a verdict like: "VERDICT: GO. Comprehensive and well cited." A verdict without path:line evidence per finding, and without the checked/not-checked section, cannot be acted on.
