# S2.34 Summary Block — RE-DIAGNOSIS / HALT (S2.33 halt premise falsified)

**Session type:** Execution (pod-side), resuming the S2.33 halt.
**Outcome:** `HALT_REDIAGNOSED`. No model dispatch. No data produced, none promoted. Engine unmodified. Clean diagnostic state. Halt-id `D-S234-HALT-1`.

## Headline
The S2.33 halt diagnosis (`D-S233-HALT-1`: "BOS off-by-one in subject-last fact-lookup") is **WRONG**. There is no lookup bug. Lookup **index 3 (` plays`)** — the token immediately after the subject — is the **canonical** anchor that produced every promoted Llama result, including the v1.5 §3 endpoints. The S2.34 kickoff's planned fix (force the lookup onto ` Jackson`, index 2) would have **broken a correct path and failed gate #3**. I did not execute it.

The real S2.33 defect was mundane: the **target string lacked a leading space** in a *direct* `compute_z` call.

## Entry gates
- **Engine fingerprint (LAW #1): PASS.** `sha256(memit/memit_main.py) = 5c0c706a…c78770` matches kickoff; `grep -c "_cov_cpu" = 3`.
- **Read-source-before-authoring (LAW #4): PASS.** `cat`-read `memit/compute_z.py` (compute_z + find_fact_lookup_idx), `rome/repr_tools.py` (get_words_idxs_in_templates), `memit/memit_main.py:80-82` before drawing any conclusion.
- Determinism / patch-isolation gates: n/a (no dispatch, no science-path patch).

## Evidence chain (all from existing artifacts on the SAME fingerprinted engine — no new run needed)
1. **Canonical s224 reproduces §3 WITH index 3.** `t1_alpha_memit_s224.ipynb` (session 2.24, promoted as the 8B→3B generalization / §3 lineage) stdout:
   `Lookup index found: 3 | Sentence: Bo Jackson plays the instrument of<|begin_of_text| > | Token:  plays`
   `loss 18.145 = 18.145 + 0.0 + 0.0  avg prob of [ guitar] 1.389e-08` → matches v1.5 §3 (first avg-prob ~1.6e-08, loss ~17.96). Per-subject lookup indices 3/4/4/8 = uniformly "(subject token count)+1" = the first token after the subject. **Index 3 is canonical.**
2. **Step-0 loss is lookup-index-independent.** At step 0 `delta=0`; the forward pass is the unmodified model, so step-0 loss/avg_prob is the model's NLL of the target and does NOT depend on `lookup_idx` (which only sets where `delta` is injected). So the 11.34-vs-18.145 step-0 gap **cannot** be a lookup effect — it is a target/sequence effect.
3. **Target-string diff is the whole story.**
   - Canonical s224 (cell 10): `target_new.str = " " + meta["target_new"]` → **` guitar`** (1 token, id 17418).
   - S2.33 (cells 2 & 5): `target_new.str = "guitar"` (no space), with the mistaken comment *"engine auto-prepends the leading space (exec line 80-82)"*.
4. **Why the comment was wrong.** `memit_main.py:80-82` prepends the space — but that lives in **`execute_memit`**, which S2.33 **bypassed** by calling `compute_z` directly. `compute_z.py:39` tokenizes the target verbatim. With `"guitar"` (no space) → multi-token + BOS → `tok.decode(target_ids[:-1]) = "<|begin_of_text|>g"` appended to the rewriting prompt (`compute_z.py:44-45`), producing the corrupted `…instrument of<|begin_of_text|>g` seen in S2.33's raw_stdout and the non-canonical loss 11.34 / avg_prob 1.26e-05.

## Corrected fix (for the re-approved next session — NOT applied here)
- **DO:** pass `" guitar"` (leading space) to the direct `compute_z` harness, OR replicate `execute_memit:80-82` (prepend a space when absent) before calling `compute_z`. **Harness-level fix; gate #5 does not apply.**
- **DO NOT:** modify `rome/repr_tools.py` or `find_fact_lookup_idx`. The lookup is correct; changing it breaks cross-session comparability and fails gate #3.

## Decisions (D-S234-*)
- **D-S234-1** — Overturn `D-S233-HALT-1`. No BOS off-by-one bug; index 3 is canonical (s224 + step-0 delta-independence).
- **D-S234-2** — True root cause: target string lacked leading space in direct `compute_z` (bypassed `execute_memit:80-82`). Fix = pass `" guitar"`.
- **D-S234-3** — Leave engine unmodified; do not touch the lookup path. No gate #5 isolation needed.
- **D-S234-4** — HALT before any trajectory capture or the Qwen arm; surface the re-diagnosis for human re-approval (load-bearing premise change). No data promoted.
- **D-S234-MANIFEST-1** — manifest merge STILL deferred (carry from `D-S233-MANIFEST-1`); **no manifest writes this session** (divergent/unmerged).
- Carried, still standing: D-S233-LAYERMATCH-1, D-S233-BAND-1, D-S233-CAPTURE-METHOD-1.

## Load-bearing / irreversible surface (for the record)
- This halt **invalidates** `s233_halt_diagnostic.json`'s root cause. That file is left in place (storage discipline: no overwrite); `s234_halt_diagnostic.json` supersedes it and references it.
- The next session's scientific goal (Llama-vs-Qwen internal-stage z-geometry + Qwen entanglement Probe B) is **unchanged and still valid** — only the harness fix and the (false) bug premise change. It needs human re-approval because the approved S2.34 premise was falsified.

## Artifacts written this session
- `architecture_profile/s234_halt_diagnostic.json` (corrected diagnostic; supersedes s233)
- `session_2_34_summary_block.md` (this file)
- `session_2_35_kickoff.md` (amended kickoff; ends with APPROVE-TO-PROCEED)

## Open / next
See `session_2_35_kickoff.md`. STOP for human review.
