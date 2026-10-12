FIX-FIRST
Reviewer: GPT-6-Astra (high)

Read both documents in full; prereg SHA matches `bf28aff7…cc92`. No Python or tests run.

**BLOCKING**

- [draft:77–115](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_calibration_amendment_draft.md:77): **Neither multiplier establishes a defensible bound.** F’s arithmetic is sourced, but transferring a ratio between different workloads to every phase is invented. A confounded spread is not necessarily conservative for unseen workloads. Likewise, prereg:162/169 explicitly treats T≈28 as an assumption; observing T_cal≤28 cannot bound independently sampled stage-1 contexts. In-run termination does not satisfy prereg:92’s pre-start requirement. **Replace the universal formula and justification with:** “For each phase, cite comparable measured timings, workloads, repetitions and a justified scaling assumption or independently defensible upper estimate. Neither 99/69.53 nor T≈28 establishes an upper bound. Any component lacking such support makes the forecast UNVERIFIED and refuses dispatch (§2.6 item 6).” No replacement numeric factor is justified by the frozen text.

- [draft:26,120,218](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_calibration_amendment_draft.md:26): The blanket prohibition on merged-candidate evaluation contradicts mandatory (iii), (iii-b) and (iv), including init merged-model parity (prereg:130–132). **Replace each prohibition with:** “No substantive candidate readout; merged-model evaluations required by the frozen reduction and init-parity checks remain mandatory and yield no scientific candidate reading.”

- [draft:141](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_calibration_amendment_draft.md:141): The leakage-redraw exemption changes a frozen rule. Calibration uses its contexts for writes; their exclusion from later stage inputs does not exempt those writes from prereg:86. **Replace with:** “INVALID-LEAKAGE HALTs calibration. Do not redraw contexts until they pass; §2.6 item 2 and §5 remain binding.”

- [draft:197](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_calibration_amendment_draft.md:197): “There is no re-run” overstates T12:687–689, which preserves V4 but explicitly does not decide rerun eligibility. **Replace with:** “A V4 miss keeps the entire schedule HALTED. No automatic rerun is permitted; any required rerun remains pending diagnosis and authorization resolving that halt. A new directory or spend record alone cannot lift it.”

- [draft:198](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_calibration_amendment_draft.md:198): Mandatory COMPLETE calibration adds a gate: prereg:92 and brief:187 permit measured timings **or defensible bounds**. **Replace with:** “Incomplete calibration supplies no forecast inputs. Dispatch remains refused unless every required phase is supported by admissible measured timings or a defensible bound under §2.6 item 6.”

**ADVISORY**

- Order is correct: prereg:89 explicitly requires LAW#3 → (ii)–(viii) → smoke; :137 repeats that prerequisite. These are prescribed instrument checks, not disguised substantive candidate measurements (:125 exempts reduced checks from candidate fit gates). Preserve their mandatory diagnostic outputs.
- No hypotheses, scientific thresholds, arms, stage caps or verdict tables change. Calibration supplies timing evidence only, subject to its own instrument/resource halts; clarify that exception at draft:68/123. V4 halting the whole schedule is **consistent** with prereg:189/301.
- Authorization is substantively consistent: draft:191 imports T8’s prohibition on self-authorization. Make explicit: “The program authors the machine records; separate recorded operator authorization names calibration’s additional cost and cap. Require `0 < cap_s ≤ 7200`.” Brief:191 permits program authorship, not self-approval of this additional spend.
- Fresh-directory refusal, immutable prior artifacts and diagnostic-file refusal are correct. Excluding partial timings and rerunning compromised attempts matches runbook:378, subject to the V4 correction above.

**Stage-1 feasibility:** **No, using the prereg’s estimates and F.** Even leaving readout unscaled and taking r_T=1: `1.43 × (34 + 25 + 28) + 23 = 147.41 min = 8,844.6 s > 7,200 s`. Including 105 iterations at the optimistic 17 s gives **149.91 min**, before additional omitted costs. Actual feasibility remains UNVERIFIED; these estimates cannot authorize launch.

🌱 graft reported ~142,963 tokens saved this turn, 1 successful call.

