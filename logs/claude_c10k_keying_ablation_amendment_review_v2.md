The review is below. I couldn't check any citations myself: graft and the file reads were denied in this session's don't-ask mode, and no other read tool was available. Every claim about the source is therefore either taken from the amendment's own text or marked **UNVERIFIABLE (this session)**. For the solve, I used upstream MEMIT `memit_main.py` from memory and flag that where it matters.

---

## Verdict: **FIX-FIRST**

### The most important thing to do next
Before running the w-sweep, run a cheap discriminator between two explanations that both put the loss at the solve. It takes minutes:

- **(a) Key similarity.** Compute the cosine (Gram) matrix of the 24 last-token keys and of the 24 subject keys at layers 4–8. The harness already computes these keys; no edit is needed.
- **(b) Single edits.** Run K3 one fact at a time (N = 1, 6–8 subjects) at w = 5000.

The amendment assumes the ridge is the limiter. A second mechanism fits the z-probe just as well and is never named:

- **Near-identical keys.** All 24 K3 keys sit on the same token, `" of"`, in the same local context (`"… is the city of"`). At layers 4–8 those 24 vectors are probably very similar. One least-squares solve then has to map 24 nearly identical keys to 24 different capitals, so it averages them and canon collapses.
- **Why A2 fits this too.** A2 does even worse (4.2 / 8.3 against 29.2 / 25.0), as you'd expect when two-token targets interfere more.
- **Why the sweep can't separate the two.** With similar keys, the directions that tell them apart carry little energy and fall under the ridge. Lowering w lets them through, so canon rises under both mechanisms. And if canon rises and stays under 90, reading 1 calls it "inconclusive".
- **What the N = 1 test decides.** A single edit has nothing to interfere with:
  - If N = 1 last-token writes land at w = 5000, the ridge-magnitude account is falsified. The limiter is key similarity, and the sweep's mechanism story is wrong.
  - If N = 1 also fails, the ridge account gets real support, and the sweep is worth its 1–2.3 h.

---

## Issues, in priority order

**1. The number behind the w = 25 choice contradicts itself.**
- The trigger paragraph says the 17–180× ratio is measured at "w = 15000-equivalent geometry", then calls "37–180×" "the 15000 figure", then says "the ratio scales with w".
- The K3‴ row's reasoning, "5000/25 = 200× clears 180×", only works if 180× is measured at w = 5000. If it is the w = 15000 figure, the ratio at 5000 is about 6–60×, and w = 50 already clears it.
- Open `results/c10k_route_a/memit_ridge_diag.json`, write down which w each number belongs to, and restate it once. **UNVERIFIABLE (this session).**

**2. "Clearing" the ratio is not a calibrated prediction.**
- If the ratio is about 1 after the reduction, a solve of this form writes roughly half the target along that key, not all of it. Whether that flips top-1 is unknown.
- A sharper, pre-registerable prediction: take the subject-key ratio at w = 5000 (where K1 writes at 94 %) from the same diagnostic. Predict the w where last-token keys reach the same ratio: w* = 5000 × (subject ratio ÷ last-token ratio).
- Then claim A becomes "canon crosses 90 near w*", which is a real test. "Rises monotonically" would happen under almost any mechanism.
- If the diagnostic shows the subject keys are also well under the ridge at w = 5000, the ratio does not predict writability at all. That would undercut the whole amendment.

**3. Claim A's "EVIDENCE-SHOWS" result is weaker than it sounds.**
- Lowering a ridge raises fit for any key, so "rising canon" barely tests anything specific. "Flat or falling" does falsify; the rising branch does not confirm much.
- Narrow the claim to "consistent with the ridge, and not separated from key similarity". The only exception is if the N = 1 / Gram check above has already separated the two.

**4. The readings favour F3.**
- The bleed guard for OVERTURNED compares K4″ at w = 50 with K1 at w = 5000 (91.9). Taking the ridge away is expected to damage locality for every cell (the Route A F4 citation is the amendment's own). So K4″ will likely fail the guard because of the ridge cut, not because of bleed, and OVERTURNED becomes nearly unreachable.
- SUFFICIENT has no locality guard; it relies on K1′.
- Fix: measure the bleed guard against K1′ at the same w. Make sure K1′@50 runs whenever K4″ is read (the current condition covers this only if K4″ is valid).

**5. The precedence order is broken.**
- Reading 1 is about claim A, and under "first match wins" it always matches, so readings 2–7 never fire. Give claims A and B separate reading lists.
- Claim B also has gaps:
  - If K3′@500 is valid with para ≥ 80 and K4″ is invalid, no reading matches. OVERTURNED is tied only to K4″, and MIXED needs para < 80. Add an UNCLASSIFIED fallback.
  - OVERTURNED should be readable from the binding cell, as SUFFICIENT is. It should not be readable only from K4″, which is valid only at w = 50, where its locality is weakest.

**6. Bleed probes are missing for keys with no ridge.**
- At w ≤ 50, a write keyed on `" of"` can spread to any prompt ending in `"… the city of"`. That is exactly the neighbourhood the described-as JS may not cover.
- Add 5–10 prompts for unedited real countries ending in `"is the city of"` as a specificity check.
- For the record, the eval paraphrases end on `called` / `is` / `is`, so this bleed would show up as damage elsewhere, not as inflated `para_full`. It still decides whether a ≥ 80 cell is a clean write.

**7. Drift.**
- The scope note concedes that the "key at the subject" rule already holds on engineering grounds. It also concedes that results at w ≤ 50 are about mechanism and promote nothing to C10, while A7 (multi-token values) is the C10 blocker.
- What the sweep could change is whether option (ii)'s rationale holds. Reading 7 sends the question to option (ii) anyway.
- Run the minutes-long discriminator first. Commit to the 3–7-cell sweep only if N = 1 fails at w = 5000; that is the only branch where the sweep can tell the explanations apart.

**8. Minor.**
- "Monotonic" across 3–4 points at N = 24 with one seed: ±1 item is about ±4 pp on A1 canon. Pre-register a tolerance, e.g. "non-decreasing within 5 pp", or "monotonic" is a coin-flip criterion.
- The solve citation (`memit_main.py:202`, `(w·C + KKᵀ)⁻¹K`) matches upstream MEMIT as I remember it. One detail is relevant to issue 1: the residual is divided by (number of remaining layers) at each layer, and K is averaged over context templates. The "fraction written" arithmetic should be done per layer. **UNVERIFIABLE (this session).**
- Confirm the three `configs/hparams/qwen25_3b_memit_hparams_mom2w{500,50,25}.json` files differ from the base only in `mom2_update_weight` (a diff, before the run). **UNVERIFIABLE (this session).**

---

**What's solid:** keeping writability (A) and generalisation (B) as separate claims, the matched K1′ controls, choosing the largest valid w as the binding cell, the INTERACTION guard, and the explicit statement that results at w ≤ 50 are about mechanism only. The z-probe correctly moves the loss to the solve. What's missing is a test of which property of the solve causes it.

**Unavailable this session:** Gmail and Google Calendar need authorising in your claude.ai connector settings. Graft and file reads were blocked by the permission mode. If you allow them, I can check issues 1, 2 and 8 directly against the diagnostic JSON and the engine source.
