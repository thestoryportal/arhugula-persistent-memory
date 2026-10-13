**FIX-FIRST**

Verified v3 SHA-256 matches `b0a415841b65b86d392e687bec90770604c13bcbaea45806ae2550bb66b90ef1`, including at completion. Read-only review; stdlib probes only. No model, tokenizer, torch or GPU execution.

| Round-2 item | Disposition | Evidence |
|---|---|---|
| **B1 — observation seam** | **RESOLVED, design-level** | `docs/MATHLAB_PREREG.md:108–125` saves both code objects before rebinding, matches the original caller, requires five ordered captures plus a return, and checks LAW#5 tagging before subject validation. Supported by `c10e_bandknob.py:189–221,430–435` and `c10x_enginepath_arms.py:468–473`. |
| **B2 — replay equivalence** | **NOT RESOLVED** | The four-part contract is substantially corrected, but `docs/MATHLAB_PREREG.md:89` supplies the wrong prompt inventory to `p2_audit`; its required counts cannot match. |
| **B5 — fail-closed admission** | **RESOLVED, design-level** | `docs/MATHLAB_PREREG.md:260–265` unconditionally rejects probe errors and autoresearch sessions before considering the fully accounted coordinator exception. This matches the return structure in `tools/c10w_p2_gate.py:73–84`. Harvest retains unconditional refusal. |

**BLOCKING**

**B2: the prescribed P2 reconstruction cannot reproduce the saved audit.**

[Prereg:89](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:89) passes `c10l_mint_lib.all_harness_prompts(H)` and requires `plain_n == 396`, `inventory_n == 2376`.

The historical writer instead passes **`audit_prompts(H, M, root)`**:

- [c10u_mint2_arms.py:273–282](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:273) expands the library inventory with additional subject/frame forms, screened countries and capitals, and unrelated prompts.
- Its actual behavior replay obtains this inventory at `:793` and passes it to `p2_audit` at `:794`.
- [c10l_mint_lib.py:178–185](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10l_mint_lib.py:178) supplies at most **233 plain strings** under the specified populations. With six templates including identity, the contextual inventory has at most **1,398 strings**. Deduplication can only decrease these bounds.
- The saved counts are indeed **396 / 2,376** (`F_r0_mint1_s0.json:961–962`), identical across all three mint records.

Thus check 3(c) necessarily fails, all mint arms become INVALID-REPLAY, and calibration becomes INVALID.

**Required replacement:** obtain `prompts, countries, capitals = c10u_mint2_arms.audit_prompts(H, M, W)` and pass `prompts` to the original `p2_audit`, preserving the frozen inputs and recorded-field comparisons. Correct the inventory description at prereg `:47` and the B2 fold claim at `:329`. Do not lower the required counts.

**ADVISORY**

- **B1 probe passed.** Executing the source-extracted `my_edit` with stdlib stubs produced five ordered science captures and five ordered LAW#5 captures, one return each, all seven operand locals, no second-pass captures, and restored profiling. The rebound-code predicate remained false. This verifies frame mechanics; empirical tensor/behavioral inertness remains **UNVERIFIED**.

- **B2’s remaining design is defensible.** Pinned tokenizer identity and file hashes, original registration with exact minted IDs, audit reconstruction, substring/index comparisons, and `RECONSTRUCTED` labels are explicit at prereg `:87–94`. I verified identical `/ctx`, `/minted_words`, `/minted_ids` and complete `/admission/P2` objects across the three records. Shared failures therefore invalidate all mint arms; seed-specific source/norm failures may exclude only that arm.

- **Six orderings remain a meaningful, limited retrospective screen.** Prereg `:225–239` retains tier margins, strict comparisons and ≥1,900/2,000 paired-bootstrap successes for every required ordering. Exhaustive enumeration confirms **4/120 = 1/30** for five uniformly ranked arms, versus **12/720 = 1/60** for six. Neither is an empirical false-positive rate. Extend the two-proxy caveat explicitly to **≤2/30** for the reduced case; admission must remain independent of proxy scores.

- **Round-2 advisory folds survived:** separate fresh/historical counts (`:214–223`); norms described as consistency rather than tensor identity (`:95–98`); A2 ≥68 identified as this preregistration’s floor (`:132`); fresh LAW#3 baselines completed before mint replay (`:82,132`).

- **B3/B4 remain RESOLVED at design level:** same-dtype transfer, CPU casts and source-preservation tests (`:118–119`); same-fp32 replay tolerance (`:172`); fixed batching, positions, fp64 arithmetic, median, invalid arithmetic and paired bootstrap (`:145,190–210,231`).

- **Evidence boundaries survived:** MATH-PROXY and prospective-utility restrictions, immediate staging with supervised canonical fold-in, and DuckDB’s derived-only authority, provenance fields, rebuild rules and citation prohibition (`:249–255`).

**New/updated citation spot-checks**

| Citation | Result |
|---|---|
| `c10l_mint_lib.py:24–37` | Registration flags, contiguous spare-ID assertion and returned IDs confirmed. Expand v3’s `:24–27` citation to include these checks. |
| `c10l_mint_lib.py:178–185` | Helper confirmed; insufficient to reproduce the historical inventory. |
| `c10u_mint2_arms.py:210–256` | P2 inventory construction, counts and audit fields confirmed. |
| `c10u_mint2_arms.py:273–282,791–794` | Historical inventory expansion and actual caller confirmed. |
| `rome/repr_tools.py:56–95` | Prefix trimming, leading-space word construction, separate tokenization and last-subtoken arithmetic confirmed. |
| Pinned snapshot `tokenizer_config.json:2` | `add_bos_token: false` confirmed; both tokenizer files hashed. |
| `F_r0_mint1_s{0,1,2}.json:10833` | All 24 minted IDs are exactly 151665–151688. |
| `F_r0_mint1_s0.json:8027–8052` | Corrected candidate-norm citation confirmed. |

Minor editorial correction: prereg `:302` still says confirmation of **v2**.

🌱 graft reported ~83,228 tokens saved this turn, 1 successful call.