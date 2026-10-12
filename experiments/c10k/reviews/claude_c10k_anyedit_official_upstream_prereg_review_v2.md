## Advisor Review — D-C10k-anyedit-official-upstream prereg

**VERDICT: FIX-FIRST**

This is a rigorous, honest, well-controlled prereg — the metric is correctly matched (held-out `para_full`, canonical demoted to diagnostic), the port-faithfulness packet is strong, and it is admirably clear that even a 7B PASS does not close C10. It does not need to be overturned. But as written it spends the most expensive, most faithfulness-compromising setup in the whole program to buy only *a license to do the real experiment later*, and it picks the design that maximizes dependency drift. Two structural fixes convert it from a stage-gate into an F1-moving run.

---

### Single most important next action

**Co-register the hard A7 thresholds now and run A7 in the *same* upstream session as the A1/A2 easy controls — interpret conditionally, not serially.** The reason to serialize easy→hard across separate preregs is to avoid wasting spend on a dead port. But your Stage-0.5 stock-upstream anchor *already* proves the port is live before any C10 data touches it, and the C10-format easy controls catch adapter bugs in the same session. So: run stock-anchor → easy-C10 → hard-C10 in one loaded session; trust a hard FAIL **only if** the same-session easy control PASSED. That is identical discipline (active-control gates the hard interpretation) at a fraction of the cost, and it means your one expensive A100/Qwen-7B setup yields the only result that can actually move C10 — instead of a "license" that re-pays the entire environment + hardware cost for a later addendum.

---

### Issues in priority order

**1. F1 drift / efficiency — the gate produces no C10-informative output by design.** A1/A2 are *novel-insert easy controls*. Our own line already has these at ~100% (`in-weight-knowing: insert-robust`). So a 7B easy-control PASS tells you the official port is *active* — it tells you nothing about C10, which is the *hard counterfactual/multi-word-semantic* case. The prereg is honest about this, but a gate whose entire deliverable is "spend more" is a drift smell on a blocking falsifier. Fix #1 above resolves it.

**2. Faithfulness is broken at the dependency layer, and the prereg's own model choice maximizes the damage.** README pins `transformers==4.23.1`; Qwen2.5 cannot load under that pin. To run Qwen2.5-7B you *must* upgrade transformers → you are no longer in the upstream-pinned environment, and your "stock reproduction" can't be compared against upstream-reported numbers produced under the real pin. **You are choosing the one upstream model that forces you out of the faithful environment AND onto rented A100.** Consider running the *exact pinned upstream env* on an upstream-native model that fits the local 4090 (GPT-J/Llama configs upstream ships) as the true source-faithfulness + mechanism-liveness anchor: zero dependency drift, zero VRAM patches, no A100. That is the *most* faithful possible test of "does official AnyEdit show a mechanism local transplants couldn't." Qwen2.5-7B/3B then only matters once the method itself is confirmed to express multi-token values. (Counter-weight: a GPT-J result doesn't transfer to the Qwen line — so this is an anchor, not the C10 verdict. State that explicitly if you adopt it.)

**3. A100 rental is an outward-facing, real-money action — surface it for explicit operator sign-off.** Standing auth covers disk/downloads/cov-compute/model-pulls; renting A100-class hardware is a different category. Don't fold it into "infra pre-approved." Especially since Fix #2 may make it unnecessary.

**4. VRAM-patch fork is a faithfulness trap you've already half-fallen into before.** We have run Qwen2.5-7B AlphaEdit on 24GB — but *only* with local patches (eigh-not-svd, diagonal-add, `del Pi`; `wide-intermediate-7b-editing-vram`). If those patches touch the official AnyEdit/AlphaEdit_ARE solve to make 7B fit, faithfulness is dead and the run is INVALID by your own rules. The prereg says "prove it fits without local patches, else rent A100" — good — but make this a hard pre-run checklist item in the method-port packet (`vram_patches_applied: false` required for PASS), not prose.

**5. The actual unsolved bit — the A7 UnKE adapter — is undesigned.** UnKE/AnyEdit is *mechanistically matched* to long multi-token values (`anyedit-is-best-remaining-c10-rescue`), which is the whole reason this path is worth running. But how a project-coined multi-word C10 hard value maps into `{question, para_question, answer, sub_question}` is the crux, and it's deferred with no sketch. Since Fix #1 pulls A7 into this session, you must design and round-trip the A7 adapter *now*. Flag to the operator that this adapter design — not the easy controls — is where the real risk and the real science sit.

**6. Minor — `para_full ≥ 80%` on easy inserts is a floor, not a signal.** Fine as a port-liveness floor, but a result in [80%, 99%] still means "port active, C10 unknown." Keep the language that this threshold licenses nothing about C10 (you already do). Don't let a green easy-control number leak any optimism into the C10 verdict.

---

**Drift check:** As written, this advances F1 only one indirect step (licenses future spend) while incurring maximal cost and dependency-drift risk. With Fix #1 (co-run hard A7, conditional interpretation) it becomes directly F1-informative; with Fix #2 (pinned-env native-model anchor) it becomes both cheaper and more faithful. The honest negative outcome you most want is reachable: *official upstream AnyEdit, run faithfully, fails the hard C10 case* → strong evidence toward C10 `not-ready` for in-weight project-coined values, with no bounded-hybrid backdoor. Restructure so that outcome is one session away, not three preregs away.

Review is input; the saved artifacts and preregistered criteria bind.
