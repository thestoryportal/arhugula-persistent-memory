**Verdict: FIX-FIRST.** The design is close. Three cheap fixes are needed before K1 runs. One of them could produce a false F3 CAUSAL reading.

**Scope:** I could not read any repo source. The graft tools were denied in don't-ask mode, and no file-read tool was available in this session. Every claim below about `c10e_bandknob.py` is marked **UNVERIFIABLE**. Claims about the engine come from upstream MEMIT behaviour, not from a read of the vendored copy. Check them before running.

## The most important thing to do next

**Show that K3/K4 rename the subject only in the copy of the request sent to the engine, and that every evaluation prompt is unchanged.** K3/K4 set `request["subject"] = "of"`. Anything in c10e that builds a prompt from the subject would then read "of" in K3/K4 only. That covers the paraphrase prompts, the `locality_described_as` prompts, the canonical prompt, the per-subject ≥ 2/3 grouping and the INERT fact. For example, `"{}'s seat of government is called".format(subject)` becomes nonsense, and K3/K4 would land below 20 for reasons that have nothing to do with keying. That is a false CAUSAL. The bleed guard would also be comparing JS on different prompt sets. And 24 subjects grouped under one key `"of"` would wreck the per-subject count. (UNVERIFIABLE: the prereg says line 319 "rewrites the requests" but does not say what the evaluation reads.)

**Test:** have the harness print, for item 0 of every cell, the keyed index, all three paraphrase prompts, one described-as locality prompt, and the per-subject key. Add a validity rule: those strings must match byte for byte across K1–K4, or the cell is INVALID. This costs nothing at runtime.

## Issues in priority order

1. **Evaluation leakage through the subject string.** See above. Without this fix, a spurious CAUSAL is possible.

2. **The KL side effect is larger than declared, and there is a better subject string that removes most of it.** In upstream MEMIT `compute_z`, the KL loss is read at the lookup index of the KL prompt, not only built from the subject. With subject `"of"`, the KL prompt is `"of is a"` and the keyed token is position 0. So in K3/K4:
   - the delta is added at the sequence-initial token, which usually behaves as an attention sink in Qwen-class models;
   - the KL regularises p(next | "of") with no context;
   - that constraint is the same for all 24 requests.

   This is a different kind of z-optimisation, not just "a degenerate prompt." It could change z's norm and spread, and push K3/K4 toward INVALID, or toward "collapse" for reasons other than keying. (I-INFER; verify against the vendored `compute_z.py` around lines 50 and the KL-logits gather.)

   **Fix:** use subject = `"<country> is the city of"` with prompt `"The capital of {}"`. `subject_last` still keys at the final `" of"`, with the same preceding context as your K3. The KL prompt becomes `"<country> is the city of is a"`, read at the `" of"` position: not position 0, and different for each request. Re-run the tokenizer dry run on all 24 subjects, with and without the ctx prefix, and confirm the keyed index equals the final prompt token. If you keep `"of"`, then a K3/K4 collapse should be read as "sufficient under a degenerate KL constraint," and the label should say so.

3. **The readings overlap and do not cover every outcome.**
   - K3 ≥ 80 with K4 < 20 meets both OVERTURNED ("K3 *or* K4 ≥ 80") and INTERACTION (gap ≥ 30). It should be INTERACTION. K4 is the cell you call the closest analogue to the port, and if it collapsed, F3 is not overturned.
   - K3 = 15 with K4 = 50 meets both INTERACTION and MIXED.
   - K3/K4 < 20 with JS more than 10 points below K1 meets no rule at all.

   **Fix:** state a precedence order (gate → INVALID → TEMPLATES-FACTOR → INTERACTION → CAUSAL / OVERTURNED → MIXED), add a fallback "UNCLASSIFIED → no rule", and change OVERTURNED to require both K3 and K4 ≥ 80, or K4 ≥ 80 alone.

4. **Batch identity collisions.** If c10e applies all 24 edits in one MEMIT batch, K3/K4 give every request the same subject. Upstream MEMIT does not deduplicate by subject. Check that the harness (dicts, caches, `case_id` / `cache_template`) has nothing keyed by subject (UNVERIFIABLE). Issue 2's subject string also removes this collision, since each subject would contain its country.

5. **The label still overclaims.** "F3 CAUSAL" will be copied into ledgers without the qualifier next to it. Rename it **F3 SUFFICIENT (MEMIT)**.

6. **The dry run covered only 3 of 24 subjects, with a stand-in context prefix.** Run all 24, using the context templates the engine actually generates if the dry run can reach them. The per-cell print in the harness only checks item 0.

7. **Minor.**
   - Define A1 and A2 in the prereg itself.
   - "Byte-for-byte on its previous path" is asserted, not shown. The K1 gate covers it empirically, so say that the gate is the evidence.
   - ±3 pp at N = 72 is about 2 items. That is fine as a drift tripwire, but it is not a reproducibility claim.

## Against the review checklist

- **Real criterion:** yes. Top-1 `para_full` matches the paraphrase-generalisation claim, and the three-way split (< 20 / MIXED / ≥ 80) is an honest fit for one seed at N = 24.
- **Cheapest overturning test:** the print-and-compare in the most important step (free), then the 24-subject dry run with the issue 2 subject string (seconds). Neither has been run.
- **Drift:** this does not advance F1 directly, and it does not touch A7, the C10 blocker; §4 says so plainly. It earns its cost of about 2.7 h only because it decides whether a memory_mirror rule and option (ii)'s rationale are written on evidence or on I-INFER. If option (ii) is not a live candidate, defer this run behind A7.

Separately: the claude.ai Gmail and Google Calendar connectors need authorising in your claude.ai connector settings before they can be used. This review did not need them.
