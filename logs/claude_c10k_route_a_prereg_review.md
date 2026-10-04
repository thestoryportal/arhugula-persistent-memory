**Verdict: FIX-FIRST**

The run design is sound and can fail. But as written, the prereg reads more into a FAIL than into a PASS. It also guards only one side of the projector's failure modes, and it leaves at least one difference from the official method undeclared.

**Grounding caveat.** My repo-read tools (graft) were denied in this session, so I could not open `evaluate_uns.py`, the AnyEdit modules, the hparams json, the cov caches or the June C10i logs. Every claim below that depends on source is marked **UNVERIFIABLE (not read)**. The author must check those against `cat -n` before running (LAW#4).

## The single most important fix

**Scope FAIL as narrowly as PASS.** §4 says PASS-LEAD licenses only a mechanism lead. FAIL, by contrast, concludes that "the last named in-weight candidate on local hardware is spent." A FAIL here comes from a port that is:
- 3B base instead of 7B-Instruct,
- fp16 instead of fp32,
- run with hparams lifted from 7B-Instruct and never tuned (`v_lr 0.5`, `clamp_norm_factor 4`, `mom2_update_weight 15000`, `nullspace_threshold 0.02`),
- possibly batched where upstream is not (issue 3).

That result cannot rule out AnyEdit as a candidate; hparams that don't transfer explain a miss just as well as the method failing. The FAIL class should read: **"this port, with these hparams, did not rescue A7; AnyEdit is not falsified."** Spending the candidate is an operator decision, made after a scoped hparam check (at minimum the `v_lr`/`clamp_norm` sensitivity on A7). As written, a weak negative would close a research line without that decision ever being made.

## Issues in priority order

**1. The projector is only guarded against one way of failing (D4).**
- "dims ≈ 0 → INVALID" catches the June bug. But with P ≈ 0, `solve(P(KKᵀ+C)+L2·I, P·K·Rᵀ) = 0`, so the June failure was a no-op, not "MEMIT-like" as the §5 table says.
- The opposite failure is not guarded. If P ≈ I (nearly all 11008 dims fall below 0.02 after dividing by count), the update becomes MEMIT-like with no knowledge-preservation term. It would then pass a "non-degenerate" check while not being AlphaEdit.
- `0.02` is an absolute threshold tuned on other models' activation scales. Qwen-3B's scale differs (UNVERIFIABLE (not read)).
- **Fix:** pre-register a functional gate instead of a dims count:
  - `‖P·K₀‖/‖K₀‖ ≤ ε` on held-out Wikipedia keys, so the projector actually protects preserved knowledge;
  - `‖P·k_edit‖/‖k_edit‖ ≥ δ` on the A1 edit keys, so the edits survive projection;
  - record dims and both ratios per layer.
- Also confirm the `.npz` caches store `count`; if they hold only the raw accumulator, the `/count` normalisation can't be done (UNVERIFIABLE (not read)).

**2. The solve and SVD device is not declared.** D1 replaces `cuda` with the model's device, so `torch.linalg.svd` and the 11008² `torch.linalg.solve` would run on MPS. On MPS they either fall back to CPU or run at reduced precision. The program already needed P-VRAM-CPU-SOLVE (`_cov_cpu == 3`) for Qwen's wide intermediate in its own engine, which suggests the same pressure applies here. "No solver change" is true of the code but not of the arithmetic. **Fix:** declare where the SVD and solve run, and in what dtype, as deviation D6. Projector work should be fp64 on CPU.

**3. Batching may be an undeclared deviation.** §3 runs "all 24 items of an arm in one `apply_*` call." I believe AnyEdit's `evaluate_uns` edits one sample at a time and restores weights between samples (UNVERIFIABLE (not read)). If so, batching 24 is a departure from the official method and must be listed. Relatedly, D2 transcribes only `get_project`. How `cache_c` accumulates across windows and items is equally science-bearing: it decides whether later windows overwrite earlier ones when `window_size=1`. **Fix:** transcribe the `cache_c` lifecycle with file:line cites, and declare the batching mode.

**4. The port has no dynamic anchor (D1/D5).** A static diff review shows only that the edit is a substitution, not that the behaviour is unchanged. The diff rule "nothing but device expressions" also doesn't say what happens to `torch.cuda.empty_cache()`, `.cuda()` or AMP calls (UNVERIFIABLE (not read)). **Cheapest falsifier:** run the ported `AlphaEdit_ARE` on 3 A1 items twice, once on MPS fp16 and once on CPU fp32 (12 GB fits in 48 GB). Pre-register agreement as: same top-1 outcome on all 3, and update norms within a set tolerance. This is the closest thing to an inertness anchor available without an unmodified run, and it bounds D5 at the same time.

**5. Locality is measured on the wrong prompts.** `"{} is described as"` on the edited fictional subjects measures bleed within the same subject. It doesn't detect damage to unrelated knowledge, and a fictional subject's pre-edit distribution is close to noise. A 24-item batch edit into five 11008-wide layers can cause global damage this metric won't see. **Fix:** add unedited neighbour subjects plus held-out perplexity or the stock-item set, before vs after, with a pre-registered bound.

**6. The R0 baseline gate (LAW#3) has no numbers.** "Reproduces the June A1/A2 ≥ 80 behavior" doesn't cite the CORPUS doc or the exact June `para_full` values and tolerance. "Ported `c10e_bandknob.py`" is also ambiguous: if any science-path file changed, LAW#5 applies to R0 too. **Fix:** cite the doc and the numbers, and state that R0 runs the unmodified vendored engine with the fingerprint passing.

**7. No statistical decision rule.** The 72 trials are 24 items × 3 paraphrases, so they cluster by item. A7 ≥ 85 requires 62/72. Report counts plus an item-level breakdown, and decide in advance whether a pass needs, for example, ≥ 20/24 items with at least 2 of 3 paraphrases correct, so that a few items can't carry the result.

**8. Pre-registration hygiene.** Per git status, `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` is untracked. Commit it, with the hparams json and port script, before the launcher runs, or it isn't pre-registered. The prereg text was also pasted twice in the review packet; check that the file on disk has one copy.

**9. Drift check: passes.** The run tests a live §0.3 C10 falsifier at the right e2e cell (§8.9 L2 behavioural firing). The mechanism-lead framing for PASS is correctly modest. The problem is only the FAIL asymmetry above.

## What's sound
- Holding A7 back until the controls pass.
- R0 rerun in the same session on this machine.
- Held-out `para_full` as the binding metric.
- Catching and correcting the June raw-accumulator confound.
- The full deviation table and the "does not license" list.

---

Separately: the claude.ai Gmail and Google Calendar connectors need authorizing in your claude.ai connector settings before they can be used. Nothing in this review needed them.
