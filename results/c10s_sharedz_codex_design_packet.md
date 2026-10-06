# Advisor / objective-review prompt (reusable — Claude & Codex)

You are an **independent, adversarial reviewer** of a research step in the LLM-as-Database program. You are not the author. **Do not rubber-stamp.** Your job is to find where the work is wrong, over-claimed, confounded, or drifting from the goal — *before* it is leaned on.

You will be given ONE of: a **test/experiment design** (before it runs), a **finding/result** (before it is declared conclusive or written to CORPUS), or an **approach** the author is about to commit to — together with its evidence (artifact paths + numbers) and the relevant context.

Run this review and answer concisely and specifically:

1. **Real criterion.** Does this answer the question's *actual* criterion, or a flattering adjacent one? (e.g. is the metric matched to the claim — top-1 for read-correctness, distributional for distributional; is the gate's true requirement being met or a softer proxy?)
2. **Confounds & over-claims.** Hunt for confounds, leakage, Goodhart, and over-statement. Is `EVIDENCE-SHOWS` blurred with `I-INFER`? Is "the mechanism works" being passed off as "the contract is met" (**mechanics ≠ contract**)? Is design-viability being passed off as empirical evidence?
3. **Cite or flag.** Every factual claim must cite an artifact (path + exact number) or be labeled **`UNVERIFIABLE`**. Call out any claim that isn't grounded. Verify that external repos/IDs/claims were actually checked before being relied on.
4. **The overturning test.** What is the *cheapest* experiment or control that could **falsify** this finding/design? If it hasn't been run, that is the gap.
5. **Drift check.** Does this advance the F1 readiness determination (or a live §0.3 falsifier)? If not, say so.

**Output:** a short verdict — `PROCEED` / `FIX-FIRST` / `OVERTURNED-OR-RECONSIDER` — then the **single most important thing** to do next, then the specific issues in priority order. Be a skeptic; the author will weigh your input heavily but evidence remains binding over your opinion.


---

# Review packet — D-C10s-sharedz pre-registration v2 (design pass, before freeze; 2026-10-06)

You are reviewing a **test/experiment design** before it runs: `docs/C10S_SHARED_Z_PREREG.md` (v2, reproduced below). It is step 1 of the research pass's operator-agreed sequence (`results/research_pass_2026-10-06/recommended_sequence.md`; stub in `prereg_stubs.md` §Step 1 with a dated reconciliation note). v1 had an advisor pass (`results/c10s_sharedz_advisor_v1.md`, reproduced below, FIX-FIRST) whose seven items v2 folds.

Read in the repository before judging: `memit_dry_run/memit/memit/compute_z.py` lines 14–185 (the engine function the design re-implements in the driver); `experiments/track_c/c10e_bandknob.py` lines 45–64 (CANON, PTEST, FICTION) and 181–221 (`my_edit`, the `Z_OVERRIDE` seam); `memit_dry_run/memit/memit/memit_main.py` ~300–310 (`get_context_templates` cache); CORPUS/44 and CORPUS/46 summary blocks (injection 49/54/51 per process; F-D1 23/72 edit+inject); `results/research_pass_2026-10-06/council_critique.md` lines 1–45.

Attack in particular: (1) does the same-process injection gate (shared − canonical ≥ 6/72) have the right size given the per-process spread and per-template counts; (2) is the inertness design (self-distance floor; prompts=[CANON]; prompts=[CANON,CANON,CANON]; pinned ordering) sufficient to call the driver's solve 'the engine's compute_z' at default; (3) are T1/T2 structure-disjoint from PTEST (verify the 3-gram claim yourself); (4) is routing the shared z through `Z_OVERRIDE` free of a second science-path change; (5) the DEGRADED-Z rule at 0.98 (the research pass's stub) vs 0.9 (v2) — which, and why; (6) any label or gate that could let the null pass as PARTIAL/LEAD. Verdict: PROCEED (freeze as v3) or the single thing to fix. Nothing has run; the GPU is held by the autoresearch loop; the run itself needs the operator's go.

## docs/C10S_SHARED_Z_PREREG.md (v2)

# Pre-registration — D-C10s-sharedz: one target fit jointly over three phrasings of the same fact (step 1 of the research pass's recommended sequence; H-1) (v2 DRAFT, 2026-10-06)

**Status: v2 DRAFT — not frozen; nothing has run; no code written.** v1 → advisor pass (`results/c10s_sharedz_advisor_v1.md`, FIX-FIRST; all seven items folded below) → v2. Still owed before any run: the Codex GPT-6-Astra design pass at high effort (standing rule, 2026-10-06), then the operator's go. Decision-ID `D-C10s-sharedz`. Source lead: research pass 2026-10-06, H-1 (`results/research_pass_2026-10-06/hypotheses.md`, `top3.md`, `recommended_sequence.md` step 1), with the Framework Council's amendment list (`council_critique.md`, items 1–3, 5, 8 and the memit/validation disagreement) folded in §2–§3. Lineage: CORPUS/50 ⟨D-C10q-stacked@8e5c7f12⟩ (stacked re-aim, TRADEOFF, 24/72), CORPUS/46 (F-D1: injecting the z that carries 51/72 into the *edited* model gives 23/72 — the edit's collateral change, not the target, binds), CORPUS/44 (z-probe: the solve reaches ≈ 0.99 on the canonical frame; the edit realises ≈ 3 % of it at the keyed position; canonical-z injection 49/72, per template 15/17/17), CORPUS/35 (c10c: paraphrases as extra requests → interference at 3× the request count). Rulings in force: D-C10k-rulings-1 (strict held-out bar binds), D-C10q-rulings-1 (research pass before any model change — done), D-C10r-rulings-2 (research agents never run experiments).

## 0. Where this sits, and what it is

The **§C write path**, read against the **§8.9 bar** (held-out paraphrase, full-sequence, top-1). Every knob swept so far (band, width, strength, projector, two-pass, stacked) changed how one canonical-frame target is realised. This arm changes what the target must satisfy: the value vector `z` for each coined fact is optimised jointly over the canonical prompt and two training phrasings, with the subject key unchanged and the request count unchanged (24 requests, 24 keys, one z each). It is the half of CORPUS/35 that was never run. Prior art for the shape of the objective: MEMIT-XF (`CheongWoong/mf-memit`, shared value across task formats) and RoSE (2603.15518). Their numbers are first-token on real entities and do not transfer; only the design does.

**The e2e map:** write layer, compile step (§8.1 D20 solve), target definition. Nothing in the read, governance or deployment layers is touched. **What it displaces in §0.3:** per the recommended sequence it runs before the queued engine-path arms I-1 / I-2 (sequence step 6); it is a live H-1 lead, not a §0.3 falsifier of its own.

## 1. Question and hypotheses

- **H-S1 (frame):** a `z` fit to three phrasings transfers to the three sealed held-out phrasings better than the canonical-only `z`, with the same write size and locality.
- **H-S0 (null — the prior):** it does not. CORPUS/46 F-D1 says the binding failure is the edit's collateral change (a z carrying 51/72 pre-edit carries 23/72 once the edit is applied), and a shared z passes through the same edit; the wall is realisation, and the frame account closes on this harness.
- **H-S2 (trade-off):** it transfers better but costs locality, controls, or write size.
- **The council's disagreement, made into a control:** the memit lens says the solve already reaches 0.99 and a multi-frame `z` is still one residual through the same key; the validation lens says the stub cannot tell a frame failure from a realisation failure. Both agree on the remedy: **inject first.** The injection cell is a same-process comparison (§2 cell 1), because the canonical z alone has injected at 49, 54 and 51/72 across three processes (CORPUS/44:23, CORPUS/46:26, :30) and context templates are resampled per process: an absolute gate is cleared by the null.

## 2. Design (engine unmodified; the shared solve lives in the driver and enters the harness through the existing `Z_OVERRIDE` seam; one injection cell + one harness pass; a second process only if the label needs it)

**The shared solve (LAW#4 — authored from `memit_dry_run/memit/memit/compute_z.py` lines 14–185, read 2026-10-06).** The engine's `compute_z` builds its rewriting prompts as `context.format(request["prompt"]) + decode(target[:-1])` over the sampled context templates (template-major; the engine's first template is the identity `"{}"`), puts the optimised `delta` at the subject's last token of every prompt, records `target_init` from prompt 0 (the identity template on the canonical prompt: `compute_z.py:95`), appends the KL prompt `"{} is a"` last (its slice at `:127–128` assumes that), averages the per-prompt negative log-likelihood (`:150`), early-stops on that mean (`:164`), and clamps `delta` to a ball set by `target_init.norm()` (`:175`). The driver's `compute_z_shared(model, tok, request, hp, layer, ctx, prompts)` does the same with `prompts = [CANON, T1, T2]` in place of the single `request["prompt"]`: the rewriting set is the product of the context templates and the three phrasings, **ordering pinned template-major with CANON first inside each template** so that index 0 is still (`"{}"`, CANON) and `target_init`, the L2 ball and the weight decay are unchanged; each prompt has its own subject-last-token lookup index; the KL prompt stays last and single. The engine file is not edited and `my_edit` gains no knob: the driver solves the 24 shared targets and feeds them through `Z_OVERRIDE` (`c10e_bandknob.py:186–189`), the seam that carried CORPUS/49–50 and is never consulted inside the LAW#5 gate. The context-template cache is process-global (`memit_main.py:305–308`), so the driver's solve and the harness's `compute_ks` see the same templates. Keys and the layer solve are unchanged.

**Training phrasings (published here, before the run; the council's item 2).** Canonical `CANON = "The capital of {} is the city of"`. Training forms: `T1 = "The government of {} sits in"` and `T2 = "{} is a country whose capital is"`. Sealed held-out set (`PTEST`, unchanged, `c10e_bandknob.py:52–56`): `"{}'s capital city is called"`, `"If you visit {}, its capital city is"`, `"The main city and seat of government of {} is"`. Overlap rule, computed and written into the run record before the edit, not asserted in prose: after the subject slot is removed, **no training form shares a 3-gram with any held-out form** (the v1 choice `"In {}, the capital city is"` failed this rule against held-out 1 and 2 on "capital city is" and is withdrawn). Logged beside it: T2's subject-last-token position shares its prefix with the KL prompt `"{} is a"` under the identity template, so the KL term anchors the position T2 writes through. The forms are fixed strings in the driver, hashed into the run record; their author is this pre-registration (the program session), not the model.

**Inertness (LAW#5), with a noise floor and the multi-prompt branch exercised.** (i) In one process, run the engine's `compute_z` twice for one request on the same `ctx` and record the self-distance of the returned target (fp16 on MPS over Adam steps; the floor is measured, not assumed). (ii) `compute_z_shared(prompts=[CANON])` must match the engine's target within that floor. (iii) `compute_z_shared(prompts=[CANON, CANON, CANON])` must also match within the floor: the loss is a mean over prompts, so duplication must reproduce the engine exactly, and any ordering, lookup-index or KL-slice bug shows here at no cost. (iv) The harness's standing LAW#5 gate (|Δexpr| ≈ 0, |Δloc| ≈ 0 with `Z_OVERRIDE` unset) must pass. Any failure → HALT.

**Cells, in order:**
1. **Injection cell (gate, ≈ 50 min):** in one process, solve the canonical z and the shared z for the 24 A7 facts on the same templates; inject each at the keyed position on the three held-out templates (the CORPUS/44 P6 procedure), **gate = shared − canonical ≥ 6/72**, per template beside the total. Recorded for the shared solve: per-frame `exp(−nll)` at stop, steps to stop, `delta` norm against `max_norm`, clamp-hit flag. **Any training frame below 0.9 at stop → DEGRADED-Z; the write arm is not run.** Shared − canonical < 6 → **NOT-RUN-NO-ROOM**; the frame account closes without a write and without a second seam.
2. **Harness pass (binding, ≈ 35 min):** A1, A2, A7 with the shared targets through `Z_OVERRIDE` for A7; the same-run canonical A7 (override unset) is the pass's own reference. Full readout: `para_full`, `canon_full`, first-token, `tf_pertok`, P(full | first), string readout, L1, same-frame fictional, `described_as`, L3, perplexity, per-layer ΔW. Added for this arm: the subject-last-token key's cosine to the canonical key under each held-out template (pre- and post-edit), so a miss can be placed on the key side; and the same-frame fictional probe run in each training frame (T1, T2) as well as the canonical frame, counted separately (the council's item 3).
3. **Second process:** only if the first lands PARTIAL (the ±3–5/72 per-process spread covers a gain of 10; one process cannot license it — council item 1). LEAD or NULL at one process stands.

Runtime: ≈ 50 min + 35 min (+ 35 min). Output `results/c10s_sharedz/{inject,pass1,pass2,run}.json`; a reader beside the driver prints the label from the recorded numbers (the qualifier rules live in the reader, the prose points at it — the CORPUS/50 Q2 lesson). The driver refuses to start if any inherited harness knob is set.

## 3. Pre-registered readings (exact counts; frozen at v3)

**Validity (any failure → INVALID):** fingerprint d941a9fb; LAW#5 INERT (all four checks); A1 ≥ 68, A2 ≥ 68 in the pass; the same-run canonical A7 `para_full` in [5, 18]/72 and canon in [5, 10]/24; `Z_OVERRIDE` consumed by A7 only, exactly once; training-form hashes and the computed overlap table present in the run record.

**Binding count:** A7 `para_full` /72 with the shared `z`, string readout beside it, per held-out template (3 × 24) beside the total (comparator: P6's 15/17/17, CORPUS/44:23).
- **LEAD** if ≥ 30/72 and all locality gates hold.
- **PARTIAL** if gain over the same-run reference ≥ 10/72 and < 30, gates hold → second process; the label stands only if the second process also gains ≥ 10.
- **TRADEOFF** if gain ≥ 10 but a gate fails.
- **NULL** if gain < 10.

**Locality gates (vs the same-run reference):** L1 ≤ reference + 1; same-frame fictional ≤ reference + 1 in the canonical frame **and** in each training frame; `described_as` ≥ reference − 3; L3 ≥ 29/30; generic perplexity ≤ reference + 0.5. **Write-size qualifier:** ‖ΔW_shared‖ / ‖ΔW_ref‖ (summed over layers) above 1.5 adds **-LARGE-WRITE** to any label (rule in the reader).

**What each buys.** LEAD → replicate; it also means F-D1's collateral-change reading is incomplete (a differently-fit target survives the same edit), and the shared `z` becomes the default target for every later arm, with I-1/I-2 behind it. PARTIAL (held in two processes) → the frame is part of the wall; combine with the stacked re-aim as the next pre-registered arm. NULL, NOT-RUN-NO-ROOM or DEGRADED-Z → the frame account is closed on this harness; the sequence moves to step 2 (the value-internal second key). TRADEOFF → report; step 2 next.

## 4. Not claimed, whatever the outcome

No label in CORPUS/44–50 changes. LEAD is a write-path mechanism lead, not §8.9 contract closure, not route closure, not an F1 change. A pass is "edge stored" under one relation label, not "graph stored" (council item 8: no reverse-lookup or second-edge claim). Nothing about which positions or components carry the value. The key side is left canonical by design; a shared-key arm is a separate hypothesis (H-2). The engine is untouched; the harness gains no new seam.

## 5. Halt discipline and close-out

One speculative fix after a `cat -n` read, then HALT with a diagnostic JSON. Close-out through `tools/closeout_check.py D-C10s-sharedz` once the CORPUS entry exists. Codex GPT-6-Astra (high) at the verdict and at the promote gate if LEAD. The GPU belongs to the autoresearch loop while it runs; this arm runs only on the operator's go, with the loop paused or finished.

## 6. Reviews

v1 draft → advisor pass (`results/c10s_sharedz_advisor_v1.md`, FIX-FIRST: same-process injection gate; T1 withdrawn for a 3-gram overlap; inertness floor + the duplicated-prompt control + pinned ordering; `Z_OVERRIDE` instead of a new knob; DEGRADED-Z rule; F-D1 named as the prior; `/24` and the KL-prefix note — all folded) → v2 → Codex GPT-6-Astra design pass → v3 frozen → implementation review (driver: `compute_z_shared`, the inertness script, the overlap table, the reader) → injection cell → harness pass → verdict pass → CORPUS/51.


## results/c10s_sharedz_advisor_v1.md

# Advisor review — D-C10s-sharedz pre-registration v1 (docs/C10S_SHARED_Z_PREREG.md), 2026-10-06

**Verdict: FIX-FIRST.**

**Single most important thing:** replace the injection gate "> 49/72" with a same-process comparison: solve and inject BOTH the canonical z and the shared z in one process on the same context templates; gate = shared − canonical ≥ 6/72, pre-registered. The canonical z alone has injected at 49, 54 and 51/72 in three processes (CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:23; CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:26 "injection control 24 / 54"; :30 "51/72"), so the gate as written is cleared by the null in two of three measurements.

## Issues, priority order

1. **Injection gate is below the noise floor (question b).** §1 and §2 cell 1 gate on "> 49/72"; the three canonical-z counts (49, 54, 51) span 5. Context templates are resampled per process, unseeded (CORPUS/44:32 F-A4, `memit_dry_run/memit/util/generate.py:40–43`), so the 49 was measured on a different ctx than the shared z will see. A shared z at 50–54 passes while being indistinguishable from the canonical z. Fix as above; the cell is already budgeted, the cost is one extra solve set.

2. **The overlap audit statement is false (question c).** §2: "no shared 3-gram … (T1 and held-out 2 share the bigram 'capital city')". Slot removed, T1 = "In , the capital city is" shares the **3-gram "capital city is"** with held-out 1 "'s capital city is called" AND held-out 2 "If you visit , its capital city is" (`experiments/track_c/c10e_bandknob.py:53–54`). The -ONE-TEMPLATE qualifier (§3) guards only template 2, so a gain across templates 1+2 (48 of 72 slots) would be read as frame transfer while being template coverage — the memit lens's objection 3 (`results/research_pass_2026-10-06/council_critique.md:41–43`). Fix: replace T1 with a form sharing no 3-gram with any PTEST entry (avoid "capital city"); make the audit a computed table in the run record. P6's per-template 15/17/17 (CORPUS/44:23) is the per-template comparator.

3. **Inertness test has no noise floor and never exercises the new branch (questions a, d).** §2 asks `torch.equal` / allclose 1e-6 between `compute_z_shared(prompts=[CANON])` and the engine. Both solves run fp16 on MPS (`c10e_bandknob.py:48`) over Adam steps; same-process bit-identity is UNVERIFIABLE from the record (cross-process is known not to hold), so a 1e-5 gap is uninterpretable. At prompts=[CANON] the template product, the per-prompt lookup indices, the KL slice (`compute_z.py:127–128`, assumes the KL prompt is last) and `target_init = cur_out[0][0, lookup_idxs[0]]` (`compute_z.py:95`) are never tested in multi-prompt form. Fix: (i) run the engine's `compute_z` twice in-process and record the self-distance as the floor; (ii) run `compute_z_shared(prompts=[CANON, CANON, CANON])` — the loss is a mean over prompts (`compute_z.py:150`), so duplication must reproduce the engine to the floor; any ordering or index bug shows here free. On (d): "line for line" holds only if index 0 of the shared list is ("{}", CANON) — the engine's `context_templates[0] = ["{}"]` (`memit_main.py:308`) is what makes line 95 "the clean sentence", and `target_init.norm()` also sets the L2 ball (line 175) and weight decay (line 155). Pin the ordering: template-major, CANON first, KL prompt last.

4. **A proven seam exists; the design adds a second.** `Z_OVERRIDE` (`c10e_bandknob.py:186–189, 405–407`) routes driver-supplied targets into `my_edit` keyed by (subject, target), is never consulted inside LAW#5, and carried CORPUS/49–50. Solve the shared z in the driver and feed it through `Z_OVERRIDE`; the proposed `C10_Z_PROMPTS` knob inside `my_edit` is a second science-path change. The ctx cache is process-global (`memit_main.py:305–308`), so the driver's solve sees the same ctx as `compute_ks`.

5. **"Shared z" vs "degraded z" is not decidable from cell 1's record.** The engine prints and early-stops on the mean NLL (`compute_z.py:149–164`, `loss < 5e-2`); with 18 prompts the mean can clear while T1 sits far below 0.99, and the clamp (lines 175–178) can bind every step. Record per-frame `exp(−nll_each)`, steps, delta norm vs max_norm, clamp-hit flag; pre-register "any frame < 0.9 at stop → DEGRADED-Z, write arm not run" (council_critique.md:33–35).

6. **State the prior.** CORPUS/46 F-D1 (:30): with the band 4–8 edit applied, injecting the z that carries 51/72 pre-edit yields 23/72 — collateral change of the edit, not the target, is the binding failure, and a shared z passes through the same edit. The arm is still a legitimate cheap closer of the frame account; §1 should name H-S0 as the prior and say what LEAD would mean for F-D1.

7. Minor: §3 "canon in [5, 10]" needs "/24" (hypotheses.md:8). Under the identity template, T2's subject-last-token position has the same prefix as the KL prompt "{} is a" (`compute_z.py:50`) — KL anchors the very position T2 writes through; log it.

**Cheapest overturning control:** issue 1. If shared − canonical < 6/72 in one process, H-1 closes NOT-RUN-NO-ROOM with no write and no second seam.

**Drift:** §C/§8.1 target definition only; no F1 change under any label (§4 correct). It serves a live H-1 lead, not a §0.3 falsifier — say which §0.3 item it displaces.
