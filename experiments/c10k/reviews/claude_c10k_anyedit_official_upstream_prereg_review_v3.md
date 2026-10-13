## Independent prereg review — C10K Official-Upstream AnyEdit (`D-C10k-anyedit-official-upstream`)

**Prior-review items: all five resolved.** A7 co-registered in the same session (Stage 2); stock-upstream anchor added (Stage 0.6, with the correct "source-run anchor, not reproduction" downgrade when no published number exists); README/dependency contradiction made a blocking resolve-before-run with "guess = INVALID" (Stage 0.3–0.4); `vram_patches_applied: false` required for PASS (Stage 0.8 + confounds table); bounded-hybrid-as-closure explicitly excluded (north-star contract + abort criteria). The binding metric is held-out `para_full` with canonical demoted to diagnostic — the single most important thing to get right, and it's right. This is a strong, can-fail, falsification-first design.

There is one genuine gap that bears on a money decision, so I'm not rubber-stamping it to PROCEED.

---

### VERDICT: **FIX-FIRST**
(light — bounded text additions, no redesign; effectively PROCEED once the two items below are folded in)

### Single most important next action
**Resolve a zero-cost desk question *before* the A100 go/no-go: does upstream ship a Qwen2.5-3B config, and what transformers version actually loads it?** If a 3B config exists, **prefer it** — it makes the run cleaner-attributing, closer-to-closure, and likely cheaper hardware. Only fall back to 7B/A100 if no 3B config ships. This check costs nothing and can change whether you rent A100 at all; it should gate the rental, not follow it.

### Issues, priority order

1. **Model selection underweights match-to-C10-characterization (the gap).** Your hypothesis is *"local failures may be **transplant** failures, not **method** failures."* The cleanest test of that runs official upstream AnyEdit on the **same model where the local transplant failed — Qwen2.5-3B.** The current criterion ("least-drift shipped model") optimizes source-faithfulness drift but treats model identity as secondary. Add an explicit preference order: **3B-if-shipped > smallest faithful config > 7B/A100**, and make 3B-config availability the pre-rental desk check above.

2. **Forced-7B introduces an attribution confound you don't name.** If upstream only ships 7B and you run there, an A1/A2+A7 PASS shows *"official AnyEdit on 7B rescues C10"* — but it does **not** cleanly show the local 3B failure was transplant-not-method, because **model size co-varies**. A PASS could be the larger model, not the faithful transplant. Your outcome map handles the *closure* question ("7B = lead only") but not the *attribution* question that motivates the whole session. Add a confounds-table row and one line to the outcome map: a 7B PASS leaves "would faithful-upstream-on-3B also pass?" open — so even a PASS doesn't fully resolve "was it transplant?" for the deployment model.

3. **A7 bar (85%) is set *higher* than the A1/A2 controls (80%) — justify or align.** Holding the *hard* case to a *stricter* threshold than the easy controls is unusual and reads as arbitrary. If the rationale is "a rescue *lead* needs a clear usability margin," state that; otherwise an A7 at 82% lands in PARTIAL while 80% controls PASS, which will look like a moved goalpost on read-back. One sentence fixes it.

4. **Minor — keep the anchor honest under "no published number."** Stage 0.6's downgrade to "source-run anchor, requires advisor approval" is exactly right (mechanics ≠ contract: a clean *run* is not a *reproduction*). Make sure the method-port packet's `stock_upstream_anchor` verdict field records *which* it was, so a later reader can't silently promote "ran" to "reproduced."

### Confounds I checked and found adequately controlled
Teacher-forcing/canonical leakage (binding = held-out `para_full` ✓); local-wrapper artifact (official modules unchanged, adapter-only boundary ✓); env drift (isolated env + stock anchor ✓); under-/over-editing (behavior floor + active trace + locality cap ✓); aggregate-only survivorship (`check-result` + per-unit records ✓); hard-case leakage (A7 diagnostic-only unless controls pass ✓); VRAM-patch infidelity (`vram_patches_applied: false` ✓). Halt discipline (one-fix boundary) and INVALID/abort criteria are thorough.

### Drift check
Advances F1. C10 is a live blocking falsifier and this is the designated source-faithful rescue attempt. Note the realistic payoff asymmetry, and that it's acceptable: given local AnyEdit knob/band/strength/layer sweeps all failed (per the C10g/C10f record), the prior leans toward A7 FAIL — which is **strong, decision-relevant negative evidence** moving C10 toward `not-ready`, exactly the falsification-first outcome. The one branch that does *not* advance F1 cleanly is a 7B PASS read as closure — and your contract already forecloses that.

---

Once items 1–3 are folded into the prereg text (all bounded edits) and the 3B-config desk check is run, this is **PROCEED** to environment build. The rental itself stays gated on operator sign-off and on the desk-check result.

I did **not** consult the `advisor()` tool for this: I'm the designated independent reviewer here, the task is a bounded reactive review with the prereg in front of me, and a same-direction second pass would be confirmation-amplification rather than independence. Evidence (the saved Stage 0 packet) remains binding over this opinion. One caveat on grounding: I could not inspect the upstream repo from this session (no filesystem access), so the "does upstream ship a 3B config" claim is **UNVERIFIED by me** — that's precisely why it's the pre-rental desk check rather than an assertion.
