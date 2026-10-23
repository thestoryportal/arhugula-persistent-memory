**Verdict: FIX-FIRST.** The data supports the result's core: subject keying generalises, and last-token keying doesn't. The headline and two secondary conclusions go beyond what the evidence shows, and one of them is contradicted by the result's own table. Fixing this means rewording, plus one count check. No new GPU runs are needed.

**Verification limit:** my tools for reading files were denied in this session, so I couldn't open any artifact. Every number below comes from the document itself. All artifact-backed figures (the K1–K4 JSONs, `zprobe.json`, `keygram.json`, `n1/*.json`, `framebleed.json`, and the claim that the engine change was inert in every cell) are **UNVERIFIABLE** by me. Codex or the author must spot-check them against the JSONs before CORPUS/43 is final.

**Single most important thing:** rewrite the §1 headline and the §3c/§4 frame-bleed prose to match the pre-registered reading, BETWEEN. As written, the document reports BETWEEN and then claims the stronger H-frame result anyway.

---

### Issues, in priority order

**1. The headline claims more than the pre-registered result, and the table contradicts it (over-claim; mechanism is not the contract).**
- "read from the frame, not the subject", "read by **every** prior-free prompt that shares the frame" and "It **never** encodes the subject" are all H-frame language. The pre-registered threshold was not met, so the reading is BETWEEN.
- "Every" is false by the document's own count. The bystander prompts flipped 14 of 18, not 18 of 18.
- "Never encodes the subject" is contradicted by the Zorbland last-token single:
  - The trained prompt lands (canon 100).
  - Only 2 of 6 bystander frame prompts and 0 of 12 real frame prompts take the value.
  - So a write keyed at `" of"` fired on Zorbland's prompt and did *not* fire on 4 of 6 other prompts ending in the same frame. The `" of"` residual carries subject information through attention (key cosine 0.99, not 1.0). The write is partly subject-conditioned.
- **Fix:** headline should read: "last-token-keyed singles don't transfer to paraphrases (0/18), and they bleed onto same-frame prompts to a varying degree (2/6, 6/6, 6/6 bystanders; 0, 9, 0 of 12 real); frame-bleed BETWEEN." Remove "every", "never" and "not the subject".

**2. "Interference first; ridge withdrawn as the primary cause" doesn't follow from the evidence (logical gap).**
- Singles landing at w = 5000 shows that **one** key is writable at that ridge weight. It doesn't show the ridge isn't what blocks **telling 24 keys apart**. Those are different questions.
- The document's own evidence points the other way:
  - The keygram's w* analysis says the 24 last-token keys become separable at w ≈ 100–600.
  - Route A's AlphaEdit_ARE fitted 24/24 at a tiny L2 weight.
  - Both say that shrinking the ridge *does* unlock fitting all 24.
- Interference and ridge are not separable causes here. Whether near-collinear keys "interfere" is decided by the covariance-plus-ridge geometry the solve works in.
- "One vector **to within rounding**" is factually wrong. A cosine of 0.985 is about a 10° angle, a relative difference of about 0.17, orders of magnitude above fp16 rounding.
- Raw cosine is also the wrong geometry. MEMIT solves in covariance-weighted space. Prior-art addendum 4 records a norm-98 shared activation at L4 that would dominate raw cosine.
- **Fix:**
  - Say "highly collinear in raw space; the small differences between them sit in low-variance directions and are suppressed at w = 5000."
  - Drop "interference *first*".
  - Withdraw "the covariance-corpus knob (Moir) is no longer motivated". That was never tested.
  - The small-ridge sweep needn't run: at N = 1 a last-token write generalises 0/18 anyway, so it is a dead end for F1. Just don't claim a result for it.
  - Optional zero-edit check: recompute the keygram on mean-centred, covariance-whitened keys (C^{-1/2}·k). If effective rank rises well above 1, the "one vector" framing is overturned outright.

**3. The Quaxil → Buenos outlier carries the "large enough write" story, and it is confounded and unmeasured.**
- "Buenos" is the first token of "Buenos Aires" and has a strong prior in capital-city frames.
- If Argentina is among the 12 real prompts (an alphabetical Albania…Cuba list very likely includes it), its true answer *is* "Buenos". The "flipped to value 9" and "still correct 12 → 3" columns may then be counting the same prompt both ways. **Check the counting code for Argentina.**
- "Real capitals resist it unless the write is large enough" is inference stated as evidence: no Δ‖W‖ or ‖z‖ is reported for the frame-bleed runs. Either report the per-run magnitudes or label the claim I-INFER and name the token-prior alternative.

**4. The locality numbers are framed in a way that hides two real costs.**
- "Described-as JS gap +5.4" is presented neutrally. In fact subject-keyed singles score 89–98 against 100 for last-token singles, so subject keying costs about 5 points of described-as locality. State it as a cost.
- The described-as probe stayed at 99.86 while 9 of 12 real capitals flipped. **That probe can't see frame damage.** This should be stated as a forward requirement: described-as JS alone isn't a sufficient locality gate for any write. As written, it's a passing remark.

**5. Pre-registration timing.** The claim-B criterion and the frame-bleed probe were fixed after 3 of 12 runs were visible. This is disclosed, and the remaining 9 runs are consistent (0/3 against 3/3 with no variance, so the thresholds aren't decisive). Acceptable, but tag claim B inline as "criterion fixed after 3/12 visible", not only in §4.

**6. The frame-bleed probe is a new script.** Confirm the engine-inertness check (LAW#5) covers it, or that it calls the same edit code the inert cells used. "Through the harness's own edit path" is asserted, not shown. UNVERIFIABLE.

**7. Housekeeping.** The item I was given is the full document twice in a row. Check that `docs/C10K_KEYING_ABLATION_RESULT.md` isn't actually duplicated by the result-doc renderer (`tools/closeout_scripts/ablation_result_doc.py` is modified in the working tree).

---

### The five checks

1. **Real criterion:** met for the result that matters to F1. Subject-keyed writes generalise at N = 24 (K1 95.8 / 97.2, K2 91.7 / 88.9) and at N = 1 (18/18 paraphrase hits). Last-token writes don't (0/18). The metric matches the claim (top-1 paraphrase hits).
2. **Confounds and over-claims:** issues 1–4 above.
3. **Cite or flag:** the internal citations are thorough. Everything is UNVERIFIABLE by me this session, and "large enough write" and "within rounding" have no backing.
4. **Overturning test:**
   - For the headline, the overturning data already exists: Zorbland's 2/6 bystanders. Rewording fixes it.
   - For "interference first", the cheapest check is the whitened keygram, but the better course is to drop the claim.
5. **Drift:** the core advances F1. It strengthens the case for option (ii), the subject-keyed hybrid. The ridge/Moir conclusion drifts into a claim with no test behind it. Don't spend more compute on last-token cells.

**F3 status:** the move to "EVIDENCE-SHOWS-in-MEMIT (N = 1, qualified)" is fair. The Route A attribution correctly stays I-INFER.
