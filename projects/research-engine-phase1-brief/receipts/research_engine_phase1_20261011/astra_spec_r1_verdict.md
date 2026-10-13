# Astra spec r1 verdict — research-engine phase 1

Verdict: GO-WITH-CONDITIONS

## Findings

S1. [severity: condition] “No concurrent science” does not specify how research-engine processes yield to a **pending** gated science launch. Evidence: phase1_spec.md:178,200,202,230 vs CLAUDE.md:30 and memory_mirror/gpu-gate-refuses-any-venv-python.md:10–12; tools/c10w_p2_gate.py:43–53 classifies non-exempt Python processes without distinguishing CPU-only work. Consequence: the importer, query process or Python resource watcher can keep science admission closed while AC17 passes its existing resource/stop checks; Java’s absence from that Python classifier does not establish coordinated admission.

S2. [severity: condition] Neo4j generation immutability is stated as a writer convention without explicit rejection controls for modifying an existing generation. Evidence: phase1_spec.md:136–144,180 vs astra_r1_verdict.md:37. Consequence: the specified publication-barrier tests can pass while an untested administrative write path changes published content under the same `generation_id`; agreeing generation IDs then do not establish an unchanged snapshot. The existing immutable-data assertions are useful, but the listed faults do not directly challenge this boundary.

S3. [severity: condition] “nice+10” leaves the required resulting process priority ambiguous. Evidence: phase1_spec.md:200 vs memory_mirror/background-shell-niceness-10.md:7–13 and operator_phase1_choices_20261011.md:11. Consequence: adding ten to an inherited niceness of ten and targeting absolute niceness ten implement different policies, leaving AC17 without one unambiguous priority predicate.

S4. [severity: condition] The completion contract omits an assigned decision-closeout step and its receipt. Evidence: phase1_spec.md:50,204–217 vs CLAUDE.md:42–48. Consequence: the packet can satisfy its listed review requirements without recording the phase decision through the binding canonical presence-and-currency closeout gate. Keeping closeout execution outside the builder and query interface is correct; MAESTRO’s separate obligation still needs an explicit place.

## Required spec changes before freeze

R1. Extend sections 11/13 and AC17 with a science-priority admission contract: name the authoritative pending/running-science signal and reservation owner; refuse new research-engine work while a gated launch is pending; on a newly pending launch, cancel work and terminate owned research-engine Python processes and Neo4j within the existing shutdown bound. A waiting Python watcher must not remain as an admission blocker. Freeze controls for pending-at-start, pending-during-work, unavailable authority/observation, and confirmed process termination. Preserve existing science-gate rules and exemptions unchanged.

R2. Extend section 7 and AC8–AC10 with an explicit application-enforced append-only graph contract: generation-scoped identities for nodes and relationships; both relationship endpoints in the selected generation; refusal of candidate reuse and updates/deletions targeting published generations. Add production-path controls attempting each prohibited operation, including a payload change retaining the same generation ID. Require unchanged published graph digests and old-pair answers after rejection. Specify when graph integrity is verified and how detected corruption makes answers incomplete. Community’s shared database is acceptable under this tested contract; a property filter alone is insufficient.

R3. Replace “nice+10” with an absolute acceptance rule. A suitable rule is observed niceness **at least 10** for owned Python/Java processes: raise it to 10 when lower, preserve an inherited value already at least 10. AC17 must cover inherited values 0, 10 and greater than 10, and unavailable priority observation.

R4. Add a MAESTRO-owned phase decision ID and canonical-closeout step outside BUILD1’s write scope. Before declaring the decision closed, require the applicable tracker updates and an archived `LLMDB_ROOT=$PWD … tools/closeout_check.py <D-ID>` receipt showing ALL GREEN with fingerprint currency active. Presence-only fallback is insufficient; tools/closeout_check.py:204–215 explicitly permits that fallback. Keep builder delivery `ENGINEERING_GREEN/PROMOTE_PENDING` until the external obligations are satisfied.

## What I checked and did not check

Verified the subject SHA-256 as `09cdd80e3a365d02969cbf559440326fb69916847f5916eba27642564307e0a0`. Read the complete spec, prior C1–C9 verdict, operator choices, relevant approved-design sections, CLAUDE.md, DISCIPLINE.md, the named admission/niceness records, and relevant gate implementation.

| Condition | Assessment of the written mapping |
|---|---|
| C1 | Substantive: separate authors, source-derived expectations, independent review and renewed freeze are specified at spec:64–71. |
| C2 | Substantive: actual backends/interface, exact comparisons, refusal semantics and no skipped acceptance are specified at spec:25–27,113,148–161. KEY1 must still freeze the concrete cases. |
| C3 | Substantive: every required fault family has a disposition at spec:117–130. |
| C4 | Conditional on R2; capture, publication interruption, retained readers and mixed-generation refusal are otherwise concretely covered at spec:134–144. |
| C5 | Substantive: bounded operations and prohibited capabilities are explicit at spec:148–161. |
| C6 | Authority roles and future dispatch/resume revalidation are present at spec:165–174; current operational admission needs R1. |
| C7 | Substantive: all seven claims remain separate at spec:93–105; halted-history and MathLab controls preserve their distinctions. |
| C8 | Storage accounting, headroom, retention and stop requirements are substantive at spec:194–202; R1/R3 complete the admission/priority contract. |
| C9 | Review-before-expansion and packet contents are substantive at spec:204–217. R4 supplies the additional repository decision-closeout obligation. |

**The 20 ACs:** AC1–AC7, AC10–AC16 and AC18–AC19 have checkable pass/fail predicates once their explicitly deferred key/configuration details are frozen. AC8–AC9 need R2, AC17 needs R1/R3, and AC20 needs R4 for repository closure. AC1, AC18–AC20 also require inspection of real session identities, chronology and receipts; unit tests of a receipt validator alone cannot establish those facts. AC12 correctly proves the current surface refuses execution, not that a future execution adapter is safe (spec:174).

All five proposed chains fit their categories:

- **B3 — scoped positive:** CORPUS/17_B3_QUANTIZATION_SURVIVAL.md:20–32 reports 99/99 edited retention versus 75/77 native retention, with margin and deployment limitations. These counts match results/b3_quant_survival_result.json:8–25; the margin medians match results/b3_margin_result.json:2–16.
- **A2b — negative:** CORPUS/16_A2b_REFRESH_KS.md:25–36 supports the scoped sentinel-staleness negative and explicitly excludes a projection-refresh conclusion. I checked the result configuration at results/a2b_refresh_ks_result.json:2–20, not every arm’s numerical output.
- **C10K — halted:** CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md:6–18 agrees with architecture_profile/c10k_route_a_halt_diagnostic.json:14–27: canonical recovery to 24/24 coexists with paraphrase 0/72. The historical scoped findings are explicitly retained at CORPUS/42:24–30; no new A7 interpretation follows.
- **C10W — superseding:** the P1 result has `INCOMPLETE`, null final label and null routing (results/c10w_oracle/p1_20261007T223707_598959Z/verdict.json:4–11). The final result has `VALID`, partial-ceiling locality cost, count 70 and independent-preregistration routing (results/c10w_oracle_logs/p2-read-attempt2.json:4–17). CORPUS/55:83 explicitly points to the superseding CORPUS/57; CORPUS/57:40–50 excludes the compromised attempt from scientific use.
- **MathLab — mathematical:** calibration.json:2–8,40–42 records FAIL with both proxies valid but failing; its manifest:2–16 identifies MATH-PROXY and a derived index. CORPUS/60_MATHLAB_HARVEST_REPLAY.md:124–134 and docs/MATHLAB_STEP4_PREREG.md:3–5 support shelving without conflating stage completion or NEW-1.

**JSON vocabulary and stdlib HTTP are acceptable implementation choices.** design.md:111 recommends LinkML rather than requiring it; spec:89 preserves one frozen vocabulary and validation. The design does not mandate a Neo4j Python driver. Exact server/API/configuration compatibility remains a provisioning prerequisite at spec:180,228, not verified capability.

Storage headroom, immutable manifests, deletion approval and frozen-source protections are explicitly retained. No additional conflict was found in those areas. Section 13’s unresolved assignments and provisioning facts must still be resolved as its freeze order requires.

This was read-only inspection. I ran no tests, databases, services, installations, science, closeout commands or numerical recomputations, and created or edited no deliverable files. Host feasibility, resource enforcement and implementation behavior remain UNVERIFIED. The graft lookup failed before returning evidence (`env: node: No such file or directory`); no token savings were reported.