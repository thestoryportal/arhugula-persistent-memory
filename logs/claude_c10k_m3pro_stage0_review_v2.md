# Review of v2: C10K Stage 0 halt on the M3 Pro

**I couldn't check the artifacts.** The graft search tool was denied in don't-ask mode, and this session has no file-read, shell or write tools. So this review rests on the document's own internal consistency, and every artifact claim below is **unchecked by me**. I also can't write the `logs/claude_c10k_m3pro_stage0_review_v2.md` file that §6 points to. Someone needs to save it from this text.

## Verdict: **PROCEED on the halt (§3). FIX-FIRST on the forward routes (§5) before they go to the operator.**

The halt is logically robust. One reachable `.cuda()` call on the edit path is enough to fail, and the doc lists 15–17 such calls. The real risk is in §5. That section steers a paid decision (renting CUDA), and it overstates Route B and understates Route A.

**Single most important next step:** rewrite §5 so that Route B states what it does *not* license (issues 1–2 below), and Route A states the anchor it actually has (issue 3).

## Issues, in priority order

1. **Route B is called "the only route to the prereg's own PASS class", but your own findings undercut that.**
   - **Wrong model.** Per E6, a source-faithful run means running **Qwen2.5-7B-Instruct** (or Llama3-8B-Instruct), not the program's base 3B or base 7B. A Route B PASS answers about an Instruct model, so its contribution to F1 for the base-3B deployment line is indirect. E6 is the doc's best new finding, but its consequence never reaches the §5 table.
   - **No faithful environment exists.** Per E5, the README pins `transformers==4.23.1`, which can't load the shipped Qwen2.5 configs, and no lockfile ships. So the upstream authors evidently used an unpinned, newer stack. A Route B run must reconstruct that stack, which is itself an undeclared deviation on any hardware.
   - **No official runner.** Per E4, a minimal launcher is needed on CUDA too.
   - Route B is therefore "official algorithm modules on native CUDA, reconstructed stack, Instruct model, project launcher". It is not "the prereg as written". Say so in its "does not license" column.

2. **The Qwen2 version claim is cheap to settle, so settle it rather than label it UNVERIFIABLE.** My recollection also puts Qwen2 support in `transformers` 4.37.0 (January 2024), but I couldn't confirm it either. It is one release-notes lookup. Since issue 1 leans on it, verify it.

3. **"Inertness is untestable" for Route A is overstated.** The program already ran this exact pattern on its own engine: P-8 made it device-neutral, and the LAW#3 and LAW#5 gates then passed on the M3 Pro (commit `773b8c2`). Two anchors are available for an AnyEdit device port:
   - **(a) Patch reduces to identity.** If the patch only swaps the `"cuda"` literal for a device variable, then with `device="cuda"` it is textually the same code. That is checkable statically, P-8 style.
   - **(b) Differential against our own engine.** Run the ported `memit_ARE` in a degenerate setting (single chunk / single-token target) and compare it with the vendored MEMIT engine's known M3 Pro baseline. **I-INFER:** I haven't checked whether `memit_ARE` actually reduces to MEMIT in that setting, so read the upstream code first (LAW#4).
   - If (b) holds, Route A goes from "mechanism lead, uncheckable" to "anchored port", which changes the cost/benefit against renting. As written, §5 tilts the operator toward the expensive route on a claim that isn't established.

4. **The "first-failure diagnostic" label is still not earned.** v1 asked for a run to first failure. v2 shows a toy `torch.tensor([1]).to('cuda')` call raising (E2) plus clean imports (E3). That shows the call would fail, not that the edit path reaches it. It also means you don't know which of the 17 bindings are live on the A1/A2/A7 paths.
   - **The cheapest test that could overturn the halt:** call `memit_ARE`'s `compute_z` / `execute` on a tiny randomly initialised GPT-2 or Qwen2 config, on CPU, and record the traceback file:line. That takes minutes, loads no science model, and touches no C10 data, so the stop rule still holds. Either run it or drop "first-failure" from the title.

5. **The E1 numbers don't reconcile as written.**
   - The four `*_ARE` files sum to 3+5+2+5 = **15**. The "17" only works if `util/layer_stats.py` (2 calls) counts as an algorithm module. That's defensible, since it computes the covariance on the edit path, but say so explicitly.
   - "26 + 1 = 27" is unexplained. What is the +1? If it's the `dict_to_(…,"cuda")` form, label it.
   - Route A's "+10 in a minimal launcher" counts calls in a file that Route A *replaces* with project code. Those 10 aren't port edits; they disappear with `evaluate_uns.py`. The port touches 17 call sites, or 15 plus `layer_stats`.

6. **The shim rejection is right, but it throws out a useful implementation detail.** A monkey-patch shim is the wrong *justification* for a PASS. It is a better *implementation* for Route A than editing the files: the module bytes stay identical, so the upstream SHA stays checkable, and the deviation sits in one declared place. Mention it as Route A's preferred mechanism.

7. **The halt hasn't been propagated yet.**
   - `docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md` is untracked per the session's git status.
   - CLAUDE.md's halt rule asks for an `architecture_profile/sNNN_halt_diagnostic.json`, a `SESSION_CHECKPOINT.md` entry, and a `D-` row in runbook §5 plus a §13 entry. "Not a registered close-out fingerprint" exempts it from `closeout_check.py`, not from those.
   - Confirm that the two cited `logs/` files are tracked rather than gitignored. Otherwise the stated evidence won't survive.

8. **Minor items.**
   - The document text appeared twice in what I was given. Check the file itself isn't duplicated.
   - The §1 statement that the 4090-to-M3 Pro substitution is a reading of the superseded scope is good and honest. Keep it.

## Things that are sound

- The evidence (E) and inference (I-INFER) sections are clearly separated.
- The float64 and VRAM claims are labelled as inference.
- The stop rule was honoured.
- The Route B amendment-before-rental requirement is correct.
- The shim-as-loophole rejection is correct.
- Route C correctly states that it isn't an F1 closure.

On drift: the doc stays on the C10 falsifier and doesn't wander. The open question for the operator is whether the AnyEdit-official framing still serves F1 once the target is an Instruct model that our deployment line doesn't use. Issue 1 is what surfaces that question.
