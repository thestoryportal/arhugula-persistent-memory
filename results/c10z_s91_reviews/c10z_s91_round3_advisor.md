PROCEED-WITH-CHANGES (1 BLOCKING, text-only, in D (b′4). The fault is in my own round-2 N2 wording and where it was inserted, so I am disclosing it. N1 and Astra 1–4 are resolved verbatim.)

Reviewer: Opus advisor, round 3, read-only. I ran no Python of any kind and used only sed, grep, ls, shasum and Read.
- D = `/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_s91_draft.md` (131 lines).
- B = `…/codex_c10z_build_brief_v2.md` (508 lines).
- prereg = W/docs/C10Z_ASTRA_PREREG.md, SHA e2d7fa10… (re-verified), 478 lines. §9(c) is at :457.
- At 22:15 MDT, P2 was still running: the coordinator log ends with `DISPATCH p2-shuf-rt`.
- `results/c10z_astra{,_benchmark,_telemetry_inertness}/` and `c10z_astra_benchmark.py` are absent (ls).

**Most important next step:** before appending §9.1, replace D:38 with the text below. My N2 sentence "stays under §9(c) and returns to the operator" contradicts §9(c) for a *first* refusal. It was also inserted ahead of the sentence that "this way" refers to.

## BLOCKING

**R3-1. D:38 (b′4): the N2 insert contradicts §9(c) and itself.**
1. "A record that was REFUSED, INTERRUPTED or STOP stays under §9(c) and returns to the operator" contradicts two texts:
   - prereg:457: "A REFUSED or INTERRUPTED benchmark is unusable; it may be rerun once in a new directory, and a second refusal returns to the operator".
   - EXPERIMENT_RUNBOOK.md:367 (the D-C10z-budget row): "a benchmark refused twice returns to the operator".

   A single REFUSED record must get §9(c)'s one re-run, not an immediate return. I wrote this wording in round 2.
2. "Usable" is now defined two ways in one paragraph: "while (b′3) steps 3–9 pass" and "(it passed (b′3) steps 4–10 …)". Step 10 is the launch env-ceiling check, which is not a property of the record.
3. The insert now sits between "becomes unusable" and "A fresh benchmark is then run". The paragraph therefore reads "…one that is STOP returns to the operator. A fresh benchmark is then run…". That ordering suggests a re-run follows a STOP. "Replaced this way" also comes before the way has been described.

**Replace D:38 in full with:**

> - (b′4) **Staleness** is defined by identity, not by age. A record is usable while (b′3) steps 3–9 pass. If a file in (b′1) `sources`, or the environment, changes after the benchmark ran, the record becomes unusable. A fresh benchmark is then run in a new directory, followed by a new D-C10z-budget append and a new go record. Such a re-run replaces a record made stale by drift. It is not a §9(c) refusal, and it does not use up §9(c)'s one re-run. At most one such drift-forced re-run is made on the program's own call; a second drift-forced re-run returns to the operator, as a refusal would (D-C10z-driftcap). Only a record that was usable before the change (it passed (b′3) steps 3–9 against the go record that names it) can be replaced this way. A record that was REFUSED or INTERRUPTED stays under §9(c), whatever changes afterward: its re-run is §9(c)'s one re-run, and a second refusal returns to the operator. A record that was STOP returns to the operator, whatever changes afterward. A drift-forced re-run whose own record is REFUSED or INTERRUPTED counts as a §9(c) refusal; one that is STOP returns to the operator. §9(c)'s bounds and STOP rule apply to every record.

I checked this text against §9(c) and :367:
- Original usable → drift → re-run REFUSED gives one refusal, and the §9(c) re-run is still available.
- Original REFUSED → re-run usable → drift → drift re-run REFUSED gives the second refusal, which returns to the operator.

Both cases match "refused twice". This text supersedes my round-2 N2 text.

## Round-2 blocking items: status on disk

| Item | Status | Evidence |
|---|---|---|
| N1 | **Resolved** | B:35 has my text plus the P3/no-other-GPU-stage clause, which is stricter and fine. B:5 header is now "Start only when §0's no-Python-during-a-GPU-run condition holds". `nice` has 0 hits in B and D, and step 1 (B:295) no longer carries it. The FROZEN-while-P2 bullet (B:21) remains correct. |
| N2 | **Inserted verbatim, but defective** | See R3-1. |
| Astra 1 | Resolved verbatim | D:5 and B:62. |
| Astra 2 | Resolved verbatim | B:265. selftest:1080 is the only successful `stage_call(3)`. :1085 and :1089 refuse at arms:1482–1483 before the binding check, so the placeholder `_launch()` stays safe elsewhere (grep of every `stage_call(`). |
| Astra 3 | Resolved verbatim | B:335 preamble; B:388 T5 lead line. The (a)–(e) list is consistent with it. |
| Astra 4 | Resolved verbatim | D:84 (inside the (h′2) quotation, closing quote kept) and B §2G stage-0 gate. |

## New contradictions from round-2 edits (scope 2)

None blocking. Checked:
- Warm-up: D:92 and B §2G agree. It is uncounted, and Astra 4's "counts prescribed by the complete three-pass schedule" excludes it.
- `benchmark_module()`: arms imports torch only inside functions (e.g. arms:162–163), so "importing arms stays torch-free" holds.
- The stage-3 line at D:131: `env -u C10Z_TELEMETRY` matches `launch["telemetry"]`, which is False for the first attempt, so (h′1)'s stage-3 equality check passes.
- The lead's Cost change at D:100 is stricter than before, and nothing in D or B still claims the check is authorized via D-C10r-rulings-11 (grep `authori|proven inert|rulings-11`). §5.2 is the section that holds these rows (runbook:297–370).
- Prereg §9(a)–(h) has no text that the Cost change, the warm-up or the stage-3 line conflicts with.

## Declined items (scope 3): acceptable

- R14 (A-1): acceptable. It was non-blocking, and I accepted D5 partial in round 2.
- R15 (A-7): acceptable under §4's "derive more".
- R16 (A-8): acceptable.
- R18: acceptable.
- R17 (A-9): acceptable only as a precondition. grep still finds 0 rows for D-C10z-c01input or D-C10z-driftcap in EXPERIMENT_RUNBOOK.md, so add them before §9.1 is appended.

## Notes (non-blocking)

- **Stale citation.** The packet's "EXPERIMENT_RUNBOOK.md:365" is stale. :365 is now the C10V D-C10v-go row, and the D-C10z-budget row is at **:367** (D-C10r-rulings-11 is at :363). I judged against :367.
- **B:352.** "patch `environment_identity` in the module `D.benchmark_module` returns" is the same ambiguity as A-5 if `benchmark_module()` re-imports on each call. Suggest: "patch `D.benchmark_module` to return a loaded module whose `environment_identity` is replaced".
- **Fold map.** Round-1 row 30 still says "`nice -n 19` is added". R5 says it is restated, but the row was not edited. The fold map is not binding.
- **Inertness record.** B:284 hard-codes `"decision_id":"D-C10r-rulings-11"`. Consider also recording the operator-yes D-ID that the new Cost bullet requires.
- **Provenance line.** D:3 lists only the round-1 reviews as sources. Consider adding the round-2 and round-3 review paths.
