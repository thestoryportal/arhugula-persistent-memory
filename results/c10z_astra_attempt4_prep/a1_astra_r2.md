FREEZE+GO

Reviewer: GPT-6-Astra (high)

**BLOCKING**

1. **RESOLVED — resident admission.** [arms.py:1736](experiments/track_c/c10z_astra_arms.py#L1736) validates benchmark/launch, current go contents and raw SHA before publication. Six mutations reject through function and CLI; content/SHA and boolean-alias controls reject; valid controls reach intercepted publication.
2. **RESOLVED — reader bindings.** [read.py:729](experiments/track_c/c10z_astra_read.py#L729) enforces all six bindings. Six mutations × both entry paths return `HALTED-V12`, `scientific_verdict=False`, without writes. Valid controls retain `PARTIAL`, `scientific_verdict=True`.

**ADVISORY**

- DRAFT-negative fixtures are isolated from repository status ([selftest:31](experiments/track_c/c10z_a1pop_selftest.py#L31)); resident-revalidation claim corrected ([report:1065](results/c10z_astra_attempt4_prep/a1_build_report.md#L1065)).
- §§1–11 unchanged: **156,213 bytes**, SHA `7aedd4ace95d2611bf398768df63cb60df6fce5afc23cf23209497bcd1d17a29`. §12 unchanged since r1; items 1–4 remain satisfied. Full prereg SHA `526c48b0…`.
- Benchmark `TEMPLATES` unchanged. **169/169 protected hashes match.**
- Reran **325 tests: 323 passed, 2 MPS skipped**. No GPU/model/live launch; MPS equivalence remains UNVERIFIED.

Approve §12 **FROZEN**, synchronize final pins, commit, then benchmark drift rerun **#3 exactly per §12**.

🌱 graft saved ~105,778 tokens (~$0.06), 1 successful call.

