**FIX-FIRST.**

**Single most important next action:** replace “the P6-vs-edit gap is therefore not a canonical-position realisation shortfall.” The correction establishes what the reconstruction measured; it does not exclude a shortfall in the behavioural run. Suggested replacement:

> **I-INFER:** Step 0 weakens a large canonical-position residual-shortfall account in that reconstruction. Whether this holds in the behavioural run remains unmeasured. CORPUS/46 F-D1 independently supports the H1 routing label, without isolating the responsible component.

Specific issues, in priority order:

1. **The inference still exceeds the evidence.** R0’s remaining-residual ratio is **0.028158359945101838**, aggregated across 24 canonical prompts—not measured on the edit yielding 7/24. CORPUS/44 F-A4 records cross-process ΔW variation up to **4.35%**, and line 40 expressly withholds this inference. Adding `I-INFER` does not justify categorical exclusion. The note’s “better supported” paragraph needs the same reconstruction qualification. Sources: `results/c10l_covgeom/step0_offline.json`, `regularisers.R0.band.rho_c_band`; [CORPUS/44:32](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:32).

2. **Propagation remains incomplete.** There are **six**, not four, verbatim tracker copies. Add **`PROGRESS.md:20`** and **`EVIDENCE_INDEX.md:101`**. Also include `results/research_pass_2026-10-06/prereg_stubs.md:75,79` and `_parts/10_E1.md:28`. Clarify the ambiguous “to ≈3%” in `docs/C10Q_STACKED_SOLVE_PREREG.md:14`; its small-sham expectation actually fits the *remaining* reading. The supposedly corrected `docs/C10T_SECONDKEY_PREREG.md:11` still declares the behavioural shortfall excluded; `docs/C10V_LAYERPICK_PREREG.md:9` still says “≈97% installed” and “behaves worse.” Both need this qualification propagated too.

3. **Right instrument and arms; wrong decision rule.** A1, A2, A7-reference and A7-shared are specified in `docs/C10S_SHARED_Z_PREREG.md:69`. Capture each arm’s actual target and **pre-band** activation, then re-read after the entire edit and pair with that run’s scores. Contrary to the note, `my_edit` reads `cur` **before each layer update**, not once before the band ([harness:194](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:194)). Equal small ratios would show that this scalar alone does not explain the behavioural gap—not that realisation “says nothing.” A7 exceeding A1 does **not** establish reconstruction under-reporting; compare A7 with its reconstructed **0.02816**, accounting for process variation.

4. **Keep the proxy caveat beside the corrected number.** CORPUS/44:25 reports **Spearman −0.12**, marking the paraphrase proxy uninformative. The append should preserve that caveat beside “≈23% remains,” so readers do not treat it as an established explanation of paraphrase failure.

**Confirmed:** the remaining-residual interpretation is correct; the triangle-inequality interval is approximately correct for the aggregate reconstruction. **No label changes** are warranted: CORPUS/44’s three NULL outcomes depend on behavioural counts; CORPUS/46 F-D1 independently records **51→23/72**, canon **7/24**; CORPUS/47–50:6 explicitly preserve prior labels. Minor transcription fix: R3’s **0.24347860115493275** rounds to **0.243**, not 0.244.

**Drift:** this repairs the rationale for live C10 work. It supplies no new §8.9 contract evidence or F1 closure.