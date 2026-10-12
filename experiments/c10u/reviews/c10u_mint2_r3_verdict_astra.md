**FIX-FIRST — the numerical readings check out; the deviation note needs narrower claims before CORPUS.**

**Next:** replace the protocol-completion and determinism wording below. No additional model run is needed to report this scoped, inconclusive result.

I reran the pinned reader: exit **0**, output exactly equal to [the saved reading](results/c10u_mint2/r3_read_after_replicateF.json). Independent row-count checks also recovered the reported binding counts.

**BLOCKING**

1. **“Every pinned gate checked” conflates record validity with protocol completion.** V2 still has `replication_pending=true`; §8 explicitly requires an operator ruling for r3. The note discloses both, but its affirmative compliance sentence undermines those disclosures. Replace §8.1 item 1’s “How r3 is to be read” passage with:

   > “The pinned reader validates the available records and yields the labels reported below. r3 nevertheless deviated from the frozen protocol: the operator ruling required by §8 remains unrecorded, and required V2 gate-A replication was omitted under a post-observation program waiver. These measurements are retained descriptively; they do not establish completion of the frozen schedule. Operator ratification remains pending and cannot make the deviations prospective.”

   Evidence: `docs/C10U_MINT2_PREREG.md:172,200`; `EXPERIMENT_RUNBOOK.md:347,349`; saved reading `V2.replication_pending=true`. Ratification outside this repository is **UNVERIFIABLE**.

2. **Bit-identical observations do not establish deterministic computation or make V2 recurrence unmeasurable.** Item 7 incorrectly says a V2 replica would not measure whether its high baseline recurs in a fresh process. It would measure precisely that **conditional on the frozen contexts**; the multi arm re-solves its targets. Replace that paragraph and item 8’s deterministic/zero-variance assertions with:

   > “All recorded numerical outputs matched exactly between the two F processes for each executed configuration; modifier records reused the original admission results. This establishes observed repeatability with fixed contexts, inits and cached mint targets, not zero population variance or robustness to context resampling. A V2 replica would test fresh-process recurrence under those fixed inputs, but was not run; its result is unknown.”

   Evidence: `r3/F_r{0,1}_*.json` differ only in `replicate`, `pid`, and `when_utc` where present; `experiments/track_c/c10u_mint2_arms.py:746–779,797–820`. “Context sampling is the **only** stochastic source” remains **UNVERIFIABLE** from these comparisons.

**ADVISORY**

- **The reader labels are correct.** In the saved reading:
  
  | Reading | Verified result |
  |---|---|
  | `F.direction` | `ROUTING-BLOCKED-UNDERFIT`; modifier admission **17/13/14 of 24** |
  | `F.arms.mint1_s{0,1,2}` | **46/37/40**, gains **+32/+23/+26**; `LEAD/LEAD/TRADEOFF` |
  | `V2.direction` | `NOT-COMPARABLE`; multi **31/72**, canon **24/24** |
  
  Seed 2’s sole locality-gate miss is perplexity **22.074 > 21.522 + 0.5 = 22.022** (`r3/F_r0_mint1_s2.json`, `r3/F_r0_multi_snone.json`, `arm.locality_axes.generic_ppl_post`).

- **Keep `LEAD` as a defined per-configuration label.** It does not mean robust superiority, candidate success for modifier-only/mint-2, or contract satisfaction. CORPUS/45 called **34–46/72** `PARTIAL`; the present prereg defines `LEAD` at **≥30/72**. That terminology change is not an empirical improvement (`CORPUS/45_C10L_MINT_TOKEN.md:61`; prereg `:92`). The seed-0 **40/34/46** cross-attempt observations are descriptive and source-confounded, as item 8 correctly discloses.

- **No scientific HALT/INVALID relabel is warranted by the checked records.** P3’s prose conflict is real, but `UNDERFIT/no behavioural run` is explicit at prereg `:115` and implemented by the pre-run reader interpretation. V2 screen failure explicitly is not a halt (`:78`). P4’s exit **1** occurred before its stage marker and model work: **NOT TRIGGERED**, neither PASS nor FAIL (`results/c10u_mint2_logs/r3/p4-save.log:1–2`; `arms.py:990,1015`). Procedural acceptance remains separate.

- **Provenance disclosure is substantially sound.** All current pinned source hashes match except the appended prereg; its pre-note content reproduces the pinned `c54f443c…` hash. This verifies preservation of the frozen text, not continuous monitoring of edits during execution (`r3/identity.json`, `source_sha256`).

- **Cheapest future overturning control:** before claiming robustness, preregister one fixed mint-1 seed plus its multi reference using a newly sampled context set, regenerated targets and unchanged science code; test the same LEAD/locality gates. The present replica never varied contexts (`arms.py:769–820`). This remains relevant to the write-path diagnostic, but closes neither H-19 nor F1 (`prereg:9–11,111`).

**Proposed one-sentence CORPUS verdict**

> **D-C10u-mint2 r3, with operator ratification pending and required V2 replication waived post-observation, yielded F ROUTING-BLOCKED-UNDERFIT and V2 NOT-COMPARABLE, advancing neither new representation; mint-1(frozen)’s 46/37/40 versus 14/72 reproduced exactly under fixed inputs (LEAD/LEAD/TRADEOFF), P4 was NOT TRIGGERED, and C10/F1 remain unchanged.**

🌱 graft reported ~78,448 tokens saved (~$0.05), 1 call.

