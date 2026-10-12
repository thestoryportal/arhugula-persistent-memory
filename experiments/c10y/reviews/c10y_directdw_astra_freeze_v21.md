**FIX-FIRST.**

References: **P** = [docs/C10Y_DIRECTDW_PREREG.md](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10Y_DIRECTDW_PREREG.md), read completely, SHA-256 `099c11d9f11dbc9c68fec6517eb794f043b6c5eb425f857027c49e16082e89f9`.

1. **BLOCKING — prior #5 remains partially integrated: V9 still requires train–deploy parity for stored controls.** P:125 explicitly makes this NOT-APPLICABLE, but P:132 and P:194 still require it for “every B write.” V3’s correction does not explicitly scope the separate V9 gate.

   In P:132 replace **“every B write”** with:

   > every optimised B-z or B-e2e write

   Replace V9 at P:194 with:

   > **V9** Train–deploy parity (§2.8 (iv)) is required at init and at the final state of every optimised B-z or B-e2e write; a miss is INVALID-TRAIN-DEPLOY-GAP. For `apply_stored`, V9 is NOT-APPLICABLE; the stored-update checks specified in §2.8 remain mandatory.

2. **BLOCKING — prior #2’s completeness rule conflicts with attribution.** P:204 now returns INCOMPLETE for missing required *stage* records; P:183 also says missing planned controls give INCOMPLETE. P:232 and the fold log at P:349 instead preserve the candidate’s label and attach SIZE-UNTESTED/ANCHOR-UNTESTED. A complete candidate with missing B-z therefore has two prescribed readings.

   Replace the first two sentences of P:183 with:

   > **Decision order (Codex #5).** Recorded halt/invalid/budget outcomes → completeness of the recipe’s own records and V5 controls → instrument/validity gates → fit → per-process count and locality label → write/deployment qualifiers → cross-process comparison → attribution. Missing recipe records or V5 controls give INCOMPLETE; missing size or anchor comparators qualify the candidate through attribution, as specified below.

   Replace P:204’s sentence beginning **“If required stage records…”** with:

   > Otherwise, missing records of the recipe being classified, including its required V5 controls, give INCOMPLETE before fit or counts are tested. Missing size or anchor comparators instead give the candidate SIZE-UNTESTED or ANCHOR-UNTESTED under attribution; they do not replace its base label with INCOMPLETE.

3. **BLOCKING — prior #1’s new projection rule has an uncovered post-write stop.** P:98 requires projections before every expensive phase, including readout. A projection can stop work after the write but before readout without reaching the supervisor deadline. S2 excludes that case; S3 at P:212 requires the deadline. The authored deadline example at P:267 does not cover it.

   Replace P:98’s sentence beginning **“A deadline stop…”** with:

   > A budget stop caused by either an in-run projection or the supervisor deadline is HALTED-BUDGET before write completion, and INCOMPLETE-BUDGET after write completion but before required readout completion.

   Replace S3 with:

   > | S3 | the write completes but an in-run budget projection or the supervisor deadline stops work before the required readout completes | INCOMPLETE-BUDGET |

   Add this exact reader case:

   > | 1 | write complete; the pre-readout projection exceeds the cap before the supervisor deadline | INCOMPLETE-BUDGET |

🌱 Graft reported ~43,554 tokens saved (~$0.03), one successful query.