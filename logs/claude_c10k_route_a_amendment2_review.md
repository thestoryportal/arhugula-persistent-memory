# Review: Route A Amendment 2 (D5 revised to fp32 on MPS)

**Verdict: FIX-FIRST.** The change itself is the right call. The argument that nothing downstream needs revisiting is not supported, and the chain will clear its gate-v2 precondition using fp16 evidence.

**The most important next step:** before any R1 result is read, re-run projector gate v2 with keys extracted from the **fp32** model, and make that record the chain's precondition instead of the fp16 one. It costs only forward passes plus projections, and it is the cheapest test that could overturn §3.

**I could not check anything in the repo.** Graft was denied in don't-ask mode, and this session has no Read or Bash tool. So every file:line and number below is quoted from the amendment and is **UNVERIFIABLE** by me. That includes `evaluate_uns.py:86`, `AlphaEdit_ARE_main.py:129`, cosine 1.0000, 12.4 GB, and commit 34a35a0.

## Issues, highest priority first

**1. §3 uses a cosine of 1.0000 as evidence it cannot support.**
- **What it measured.** The key-parity cosine compared gate keys with solve keys. As described, both came from the fp16 model. It tested *position and direction* parity, not fp16 against fp32, so the dtype claim doesn't follow from it. That is design-viability presented as evidence.
- **Why the rounding matters.** A cosine reported as 1.0000 can be as low as 0.99995. That allows a perpendicular component of √(1 − 0.99995²) ≈ **0.010**. Amendment 1 v2's first-layer threshold is also **0.01**, so the reported precision cannot rule out a deviation the size of the threshold.
- **"Below the bootstrap width" is a claim, not a measurement.** No artifact shows it. Rounding in an fp16 forward pass also compounds through the layers below L8; it is not a single per-element ulp.
- **Fix:** measure the fp32 vs fp16 key cosine and relative norm at each edit layer, reported to at least 6 decimals, and re-run gate v2 on the fp32 keys.

**2. Unconfirmed: what dtype were the covariance and projector built in?**
- **Why it matters.** AlphaEdit's null space is the span of the *smallest* eigenvalues of K₀K₀ᵀ. That is the part of the spectrum most sensitive to precision noise. If the cached covariance or projector `P` came from forward passes at the program's standard fp16 load, it encodes fp16 noise, and fp32 edit keys will have components in directions `P` treats as null.
- **Upstream builds the statistics in fp32.** If this pipeline didn't, that is a second dtype deviation, and the parent prereg doesn't list it.
- **Fix:** state the dtype that produced every cached statistic the run stage uses. If it was fp16, either rebuild under fp32 (consistent with this amendment's direction) or show that gate v2 passes on fp32 keys against the existing `P`.

**3. Comparisons against the LAW#3 R0 baseline now cross a dtype boundary.**
- §3 says c10e "runs under its own load path." If that path is fp16, then every verdict cell comparing R1/R2/R3 with R0 or c10e numbers changes two things at once: method and dtype. A gap or a match could come from either.
- **Fix:** either run the R0 reference at fp32, or scope each comparison so it says the dtypes differ. Check the parent §4 verdict table cell by cell.

**4. Relaunching before the review lands needs a mechanism, not good intentions.**
- "A FIX-FIRST item stops the chain before any result is read" only works if reading is blocked mechanically. Confirm that:
  - the amendment commit's timestamp is earlier than the relaunch;
  - R1+ outputs are not opened or summarised until this review is resolved.
- Under the prereg's own terms, the anchor stage can keep running, because device parity doesn't depend on issues 1–3. **R1 must not count as accepted until issue 1 is cleared.**

**5. Minor points (the conclusion stands):**
- **"The only ways to proceed" is overstated.** A third option exists: cast `P` to fp16 outside the module. It is D1-compliant but moves away from upstream, so choosing fp32 is still correct; the text should just say so.
- **Memory headroom.** If the anchor holds the MPS and CPU fp32 legs at the same time, that is about 25 GB of weights plus activations and per-layer `P` matrices. MPS's default working-set cap is roughly 75% of RAM. Run the legs one after the other, or confirm there's headroom, so a memory crash isn't mistaken for a port disagreement.
- **Stale records.** Make sure no partial `mps_fp16` anchor record from the 13:44 crash can be read by a later stage after the key rename.

## What holds up
- **The amendment is forced and moves toward upstream.** The crash diagnosis (fp32 `P` × fp16 `layer_ks`) is coherent.
- **The anchor is stronger.** Comparing MPS fp32 against CPU fp32 isolates the device, so any disagreement points to the port.
- **No result has been read**, so pre-registration is intact, provided issue 4 is enforced.

## F1 relevance
This is a live §0.3 step: Route A is the C10K local-port falsifier. The amendment is setup hygiene, not drift. The risk is that a gate keeps passing on evidence that no longer matches the run's dtype, and a later verdict rests on that pass.

---
Two connectors aren't usable here: **claude.ai Gmail** and **claude.ai Google Calendar** need authorising in your claude.ai connector settings. Separately, the graft denial meant I couldn't check the repo. Run this review through `tools/claude_advisor.sh` with read access to get a verified version.
