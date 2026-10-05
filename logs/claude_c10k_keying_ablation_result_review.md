**Verdict: FIX-FIRST**

**Tooling note.** This session has no Read or Bash tool, and graft was denied because the session runs in don't-ask mode. I couldn't open `K{1..4}.json`, the logs, the prereg, `memit_ridge_diag.json` or the harness, so every artifact number below is **UNVERIFIABLE by me**. I reviewed internal consistency and inference only. For the same reason I couldn't write `logs/claude_c10k_keying_ablation_result_review.md`; paste this review there. Separately, the claude.ai Gmail and Google Calendar connectors need authorizing in claude.ai connector settings before they can be used.

## Most important next step (no new compute)

Read the `compute_z` per-step loss and target probability for the K3/K4 items in `logs/c10k_keying_ablation_*.log`.

The document blames the low canonical fit on the covariance ridge, but it never shows that the target vector v\* itself reached the target at the last token. If v\* didn't reach the target prob, the failure happened before the solve, and the claim "last-token keys are not writable under the covariance ridge" is wrong. The K3/K4 KL prompt makes this likely (issue 2).

## Issues, most important first

1. **§3 contradicts §1.** §1 says "no keying reading". The K2 bullet then ends "templates are not what carries paraphrase generalisation …; **the key locus is**." Both last-token cells are INVALID, so this run cannot say the key locus carries generalisation. Delete the clause. What K2 does support is narrower: templates aren't necessary for ≥ 80 % paraphrase scores with subject keying at N = 24. Templates still account for about 4–8 points (A2 drops from 70/72 to 64/72).

2. **The ridge attribution is confounded with the z-objective, and the KL rebuttal runs backwards.** In K3/K4 the trained prompts are keyed at the final `" of"`, and the KL prompt `"<country> is the city of is a"` is also keyed at `" of"`, in a nearly identical context. `compute_z` therefore asks one delta at one token to change the next-token output for the edit while leaving it unchanged for the KL prompt. That is a direct conflict, and it alone could explain 7/24 and 6/24 canonical fit. "Locality is untouched" doesn't rule this out; it is what you'd expect if the KL term won. Check with the z-loss read above, then with a K3 rerun using a non-colliding KL prompt.

3. **"EVIDENCE-SHOWS: last-token keys are not writable under the covariance ridge" over-claims.**
   - Behaviourally, K3/K4 tested one ridge weight (5000).
   - "At either ridge weight" comes from the Route A magnitude diagnostic, which is a geometric argument, not a behavioural result.
   - The behavioural finding is: canonical fit < 90 at λ = 5000 with this KL prompt. The ridge mechanism is I-INFER.
   - §1's "the write does not land under the covariance ridge" has the same problem. Make it "the write does not land (canon < 90)".

4. **The missing cell is plain MEMIT, last-token keying, small λ, no projector.** It is cheaper and closer to the question than the covariance-corpus knob you propose next.
   - It tests the ridge mechanism directly: canonical fit should climb as λ falls.
   - If canonical fit reaches ≥ 90, the result becomes a valid K3, and its paraphrase score answers the keying question the prereg actually asked.
   - Without it, the "complementary half" argument in §3 bullet 3 is weaker than it reads. Route A's AlphaEdit_ARE changed two things at once (null-space projector and 1000× smaller ridge). The projector removes directions of preserved-knowledge keys, and the shared directions that paraphrases ride on may be among them. So F3's 0/72 has an alternative cause that has nothing to do with keying.
   - "The two together leave no observed configuration in which a last-token-keyed write generalises" is true of what was observed, but the two configurations don't cover the space. Say which cell is missing.
   - Moving to the covariance-corpus knob before running this cell is drift.

5. **K2's Δ‖W‖ matches K1's exactly to two decimals at all five layers (0.19 / 0.11 / 0.09 / 0.16 / 0.23).** Turning templates off changes how keys are averaged over prefixes, and the paraphrase scores differ (95.8 vs 91.7). Identical rounded norms across all five layers is a red flag that `C10_CTX_TEMPLATES` only affected part of the path, or that K2's record holds K1's norms. Report full-precision values from the JSONs and confirm the knob changed the key computation, not only the z context.

6. **Δ‖W‖ is the wrong evidence for "the update is not small but does not reach the prompt."** Under a large ridge, ΔW can have a big norm while ‖ΔW·k\*‖ at the keyed token stays small. That fits the story, but it's the wrong quantity. If the harness can compute the per-layer ratio ‖ΔW·k\*‖ / ‖v\* − Wk\*‖, it is a direct measure; otherwise drop the sentence or label it I-INFER.

7. **The "locality" metric isn't labelled clearly.** The column is "described-as JS", and the prose calls it locality. Define it once. Also note that 99.8 in K3/K4 is a consequence of the write failing, not independent evidence.

8. **Minor points.**
   - In the item I received, the whole document appears twice. Check that `docs/…RESULT.md` / `CORPUS/43` isn't duplicated on disk, given the network-FS write hazard.
   - State the counts behind the percentages (canon 7/24, 6/24, 1/24, 2/24) so readers see how small N is.

## What holds up

Applying the prereg precedence, both last-token cells are INVALID, and declining to read keying from them is correct and disciplined. The K1 gate pass and the K2 validity verdict both look sound, subject to issue 5.

## Drift check

The result moves F1 forward only if it stays on the keying question. That means:
1. Run the zero-cost log read (step 1 above).
2. Run the small-λ, non-colliding-KL K3 cell (issues 2 and 4).
3. Only then consider the covariance-corpus knob.
