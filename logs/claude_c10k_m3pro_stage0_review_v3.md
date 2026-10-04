**Verdict: FIX-FIRST.** The halt itself holds. Two cheap problems come first: the doc's claim that the halt was propagated conflicts with this worktree's git state, and Route A depends on three premises nobody has checked.

**What I could and couldn't check.** I couldn't verify any artifact myself: the graft search tools were denied in this session, and I have no file-read or shell tool. So everything below comes from the doc's internal consistency, the session's starting `git status`, and what I know of upstream AlphaEdit. Claims about artifacts are marked UNVERIFIED unless the doc's own numbers settle them. I also couldn't write `logs/claude_c10k_m3pro_stage0_review_v3.md`, so you'll need to save this review there yourself.

## The one thing to do next

Check whether the propagation actually landed. §6 says it's done: the §5.3/§13 rows, the checkpoint and "tracked logs". The worktree's starting `git status` shows only three untracked items (the doc, the halt JSON and `graft/`). It shows no modified `EXPERIMENT_RUNBOOK.md` or `SESSION_CHECKPOINT.md`, and no `logs/c10k_stage0_*` files. `logs/` already holds tracked files, so new untracked logs would be listed one by one. None of the last five commits touch C10K. That leaves three possibilities: the edits never persisted (CLAUDE.md warns that Edit-tool writes have silently reverted on this filesystem), they landed in a different checkout, or `logs/` is gitignored, which would make "tracked" false. Run:

```
git status --short
git check-ignore -v logs/c10k_stage0_desk_check.log logs/claude_c10k_m3pro_stage0_review*.md
git log --oneline -- logs/c10k_stage0_* EXPERIMENT_RUNBOOK.md SESSION_CHECKPOINT.md | head
grep -n "D-C10k-m3pro-stage0" EXPERIMENT_RUNBOOK.md SESSION_CHECKPOINT.md docs/program_state.json
```

Until that output agrees with §6, the record is UNVERIFIED and the halt hasn't been durably recorded. In this program's terms, a result that isn't durably written didn't happen.

## Issues, in priority order

**1. Opting out of the close-out gate (header).** "Not a registered close-out fingerprint, so `tools/closeout_check.py` does not gate it" turns a registration gap into an exemption. This halt changes C10's Stage 0 status, and E4, E6 and E7 are findings about upstream that will be relied on later. Under CLAUDE.md's halt discipline, that means a `CORPUS/` note plus `program_state.json` → §0.3. Either register the fingerprint, or state explicitly which trackers were updated and why the rest are exempt.

**2. Route A says `vram_patches_applied` stays `false`, but nothing checks that.** §4 says "48 GB unified holds the 7B-Instruct default." That needs four numbers that aren't there:
- The upstream load dtype. fp32 Qwen2.5-7B is about 30 GB of weights.
- The default MPS working-set ceiling. It is about 75% of unified memory, roughly 36 GB on this machine, not 48.
- The size of the 7B covariance/projector matrices. They are 18944² (the 7B intermediate width), about 1.4 GB each per layer in fp32. They are not 11008².
- Activation and optimisation memory during the `compute_z` step.

If the run has to drop to fp16 or offload to fit, that is exactly the "local trick" that item 8 says breaks source-faithfulness. The cheapest falsifier is arithmetic plus one load-only probe of 7B-Instruct at the upstream dtype under the default watermark.

**3. The "nearest test" for SVD may not have run on MPS.** The 11008² SVD in the LAW#3 reproduction may have gone through the CPU fallback or the program's own `_cov_cpu` CPU-solve path rather than MPS. As written, it doesn't support "the op exists on MPS". It's also the 3B width, not the 7B width.

**4. Anchor (a) can't fail, so it isn't an anchor.** For a runtime shim, "with `device="cuda"` the code is textually the original" holds by construction, because the module bytes are untouched. It says nothing about what executes. Only anchor (b) can fail. Rewrite Route A as having one anchor, and that one depends on the reduction in §4 that hasn't been read yet. The P-8-style patch alternative would get a real static anchor, but that's a separate mechanism.

**5. The runner may hold algorithm code (I-INFER: unchecked against this commit).** In upstream AlphaEdit, the null-space projector (`get_project`: `get_cov` → SVD → P) and the `cache_c` bookkeeping live in the experiment runner, not in `AlphaEdit_main`. If AnyEdit kept that layout:
- The claim that `evaluate_uns.py`'s 10 bindings "are not port edits" is wrong for the AlphaEdit_ARE arm.
- The project launcher would have to copy that code (a deviation) or import it. Importing means stubbing `glue_eval` in `sys.modules`, which is a second shim.
- The "17 bindings in the algorithm modules" count understates the bindings on the AlphaEdit path.
- The float64 grep in §4 didn't cover the file where the SVD runs.

E8 exercised `memit_ARE` only, so nothing has tested this. Check with `grep -n "def get_project\|cache_c\|linalg.svd" external_prior_art/AnyEdit/experiments/*.py`.

**6. The halt label understates a blocker that applies on any hardware.** E5 and E6 show that "upstream-compatible environment" (Stage 0, item 2) isn't defined by upstream at all: the README's pinned versions can't load the shipped Qwen2.5 configs. `HARDWARE_ENVELOPE` is correct for this machine. But the halt JSON should also carry a secondary note, such as `UPSTREAM_ENV_UNDEFINED`. Otherwise a reader of the halt code alone will assume rented CUDA fixes everything. The Route B row says this; the halt code doesn't.

**7. The shim may not be technically feasible.** Patching `torch.Tensor.cuda` and `.to` catches method calls. It doesn't catch `device="cuda"` keyword arguments passed to factory functions like `torch.zeros(..., device="cuda")`. Those need the factory functions wrapped, and `torch.device` is a C type that can't be reliably monkeypatched. A missed binding fails loudly (`AssertionError`), which is safe. The risk is the declared "one place" turning into a sprawling patch layer. Also, the patch is global to the process, so it would affect the vendored engine if both run together, and anchor (b) runs them together. Mark the shim mechanism UNVERIFIED until a dry run reaches the end of `apply_memit_ARE_to_model` on the tiny model.

**8. Anchor (b) carries a hidden second deviation.** Comparing against `results/law3_repro_2026-10-03/` means running `memit_ARE` on the baseline's model with hparams matched to it. That needs locally written hparams, which the "Does not license" column already counts as a second deviation. Say in the anchor's own row that (b) brings that deviation with it.

## What holds

- **The halt logic.** E8 reaches the first hard binding (`memit_ARE/compute_z.py:35`) before any z-vector is computed, on unmodified upstream modules. That alone meets the Stage 0 condition; the binding count is supporting detail.
- **The E1 arithmetic adds up.** By file: 3 + 5 + 2 + 5 = 15 in the four `*_ARE` files, plus 2 in `layer_stats` = 17, plus 10 in `evaluate_uns.py` = 27. By rule: 26 regex hits plus the one `dict_to_` call = 27. Whether the regex was applied completely is UNVERIFIED.
- **The reading of D-HW-1 is honestly labelled** as an interpretation, not the prereg's text.
- **The stop rule was honoured.**
- **E7 (Instruct-only configs) is a real new finding** worth putting in `CORPUS/`.

## Drift check

The work is on the F1 path, since C10 is BLOCKING. But this is the third review round on a halt whose core reason, CUDA literals on an MPS build, was settled by E8. Fix #1 and #2 and patch the Route A row (#4, #5). Then stop revising this document and hand the A-vs-B decision to the operator. The most useful pre-decision work is the LAW#4 read of `memit_ARE` against the vendored MEMIT engine plus the grep in #5. Those two decide whether Route A has any anchor that can fail.

---

Separately: the Gmail and Google Calendar connectors need to be authorised in your claude.ai connector settings before I can use them.
