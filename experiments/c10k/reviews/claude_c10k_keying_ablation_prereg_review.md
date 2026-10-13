**Verdict: FIX-FIRST.** The question is the right one and the ablation is the right one. But one mechanical claim the design depends on probably fails, and two readings could be misclassified. Fix these before spending the roughly 80 minutes of compute.

**Tooling caveat:** I couldn't read the source. The graft tools were denied in don't-ask mode, and this session has no file-read tool. Every engine and harness claim below comes from upstream MEMIT and is marked **UNVERIFIABLE (here)**. Each comes with the exact check to run, and LAW#4 (read source before authoring) requires those reads before the run anyway.

## Single most important thing

`cat -n` the vendored engine's `fact_token == "last"` paths before trusting cells K3 and K4. Upstream MEMIT's `get_module_input_output_at_words` (in `memit/compute_z.py`, used by `compute_ks`) has a `"last"` branch that opens with `raise ValueError("This is definitely bugged, fix it.")`. **UNVERIFIABLE (here):** I can't confirm the vendored copy still has it. If it does, K3 and K4 crash. Making them run would need an engine edit, which breaks the prereg's "no engine source is touched" premise and triggers LAW#5 isolation. If someone already patched it, that patch is an unrecorded science-path change and needs its own inertness proof.

Check: `grep -n '"last"\|definitely bugged' memit_dry_run/memit/memit/compute_z.py memit_dry_run/memit/rome/*.py`

## Issues, in priority order

1. **The `"last"` key position may land on padding (compute_z).** **UNVERIFIABLE (here).** Upstream, `find_fact_lookup_idx` returns `-1` for `"last"`. `edit_output_fn` then adds the delta at `cur_out[i, -1]` for every prompt in a padded batch.
   - With right padding, index −1 is a pad token for every prompt shorter than the longest one.
   - In K3, the context templates vary in length, so most rewriting prompts would get the delta on a pad token.
   - The KL prompts (`"{} is a"`) have the same problem in both K3 and K4.
   - That would give a broken write, which is an artifact and not evidence about where the key sits. The canonical score ≥ 90 INVALID guard may not catch it, because the longest prompt can still fit.

   Fixes:
   - Check Qwen's `tok.padding_side` and the batch construction in `compute_z`/`compute_ks`.
   - Log the token that is actually keyed per prompt for one fact per cell, and add "keyed token == intended token" to the pre-registered validity criteria.
   - For multi-token targets, `-1` sits on the last *target-prefix* token, not on the prompt's last token. State which of the two K3/K4 actually key on.

2. **A spurious OVERTURNED reading.** If you key on the last token, the write can attach to that token's state, e.g. " is", rather than to the subject. Paraphrases ending in the same token then score ≥ 80 through bleed, not through the subject. That would "overturn" F3 for the wrong reason. Add a pre-registered locality/specificity readout per cell:
   - other subjects' prompts with the same ending;
   - unedited neighbourhood prompts.

   Add a validity rule: if locality damage exceeds K1 by more than X points, the cell cannot support OVERTURNED. If c10e has no such readout, adding one is a harness change and falls under LAW#5. **UNVERIFIABLE (here):** whether c10e already reports this.

3. **The inertness gate doesn't cover the new knob.** The prereg says the INERT line "is independent of the knobs". If so, it says nothing about `C10_CTX_TEMPLATES`, which is a new harness-side change.
   - If instead it compares against the engine's own `apply_memit_to_model` (default templates), K2 and K4 would legitimately read non-INERT, and the gate wording is wrong.

   Fix: (a) prove `C10_CTX_TEMPLATES=on` is byte-identical to the current harness, by diff or by a K1 = R0 comparison; (b) say what INERT means in the off cells.

4. **Make the K1 reproduction a gate, not just a reading (LAW#3).** Run K1 first. It must land within a stated tolerance of R0's ~94 (A1) and ~98 (A2), with the source cited from `CORPUS/`, before you run K2–K4. As written, "K1 ≥ 80" only appears inside the CAUSAL reading.

5. **Some outcomes have no reading.**
   - K3 < 20 with K4 INVALID (or the reverse).
   - K2 collapsing, which would mean templates are the factor, not where the key sits.
   - K3 and K4 diverging sharply, which would show an interaction between templates and the key position.

   Pre-register these. K2 < 80 especially should block any claim about the key position.

6. **Scope of what CAUSAL licenses.** Even a clean CAUSAL result shows only that key position is *sufficient* to kill paraphrase generalisation in MEMIT. It doesn't show it *is* why AnyEdit got 0/72: the z-objective, the preservation term and the projector differ there too. The prereg says the result would make the Route A mechanism "unconditional", which over-claims. Use "sufficient in MEMIT; consistent with F3; not exclusive."

7. **Minor points:**
   - The 72 items are 24 subjects × 3, so they are clustered by subject. Report results per subject (how many of 24 have at least 2 of 3 paraphrases correct) next to `para_full`.
   - One seed is fine for a < 20 vs ≥ 80 split, but say that the MIXED band can't be resolved at N = 24.
   - The ~20-minute runtime per cell is **UNVERIFIABLE (here)**. Cite the runtime from a prior c10e log.

## Drift check

On track. This tests a live claim behind the C10k Route A verdict and decides whether option (ii) keeps its rationale. The prereg correctly scopes out A7 (multi-token values).

## Overturning test (cheapest)

Before any full cell, run a single-fact dry run of K3 and K4 that prints the keyed token index and the decoded token for every rewriting prompt and KL prompt. It takes about a minute. If it crashes, or if the keyed token is a pad token, the design as written can't answer the question.

I couldn't save this review to `logs/claude_c10k_keying_ablation_prereg_review.md` (no write access in this session). To have me run the source checks myself, allow the graft tools or file reads.
