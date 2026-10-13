# Does upstream `memit_ARE` reduce to MEMIT in the degenerate case? — No (LAW#4 code read)

**Date:** 2026-10-04. **Scope:** `jianghoucheng/AnyEdit@057a77f185f7ffb55818f6bd9add37f43bb447e7`, `memit_ARE/compute_z.py` and `memit_ARE/memit_ARE_main.py`, read against the vendored `memit_dry_run/memit` (P-1..P-8). **Why:** the Stage 0 diagnostic's Route A proposed a *differential anchor* (b): run a device-ported `memit_ARE` in the single-token / one-window setting and compare with the vendored MEMIT engine's M3 Pro baseline. The advisor (v3) flagged that this anchor depends on an unread assumption. This is the read. **Class:** code-level EVIDENCE (line-cited); no run.

## Verdict

**`memit_ARE` does not reduce to MEMIT in any degenerate setting.** Three structural differences survive a single-token answer and a single window; the second one is in the solve itself.

| # | Upstream `memit_ARE` | Vendored MEMIT engine | Survives the degenerate case? |
|---|---|---|---|
| 1 | **Solve adds a preservation term for every non-target position.** `adj_k = solve(mom2_uw·cov + K_p·K_pᵀ + K_s·K_sᵀ, K_s)` where `K_p` = keys at all *unselected* positions of the full `question + answer` sequence and `K_s` = keys at the lookup positions (`memit_ARE_main.py` lines ≈ 128–144: `ks_list` / `kp_list` / `torch.linalg.solve(... + layer_kp @ layer_kp.T + layer_ks @ layer_ks.T, layer_ks)`). | `solve(mom2_uw·cov + K·Kᵀ, K)` with `K` the subject-last keys averaged over context templates (`memit_main.py` solve block; `_cov_cpu` form). | **Yes.** `K_p` is non-empty whenever the question has more than one token, so the term is present for every real item. There is no setting that removes it short of modifying the module. |
| 2 | **Keys and values are read at the last prompt token with no context templates.** `lookup_idxs = [ex_len − len(current_target_ids)]` (`compute_z.py` ≈ line 90); keys = `layer_in_ks[k, idx]` from one forward pass over `question + answer` (`memit_ARE_main.py` ≈ 95–135); hparams `fact_token: "last"`. | Keys/values at the **subject's last token**, averaged over the engine's generated context templates (`get_context_templates`, `fact_token: "subject_last"`), via `compute_ks` / `get_module_input_output_at_words`. | **Yes.** The engine's `fact_token="last"` path is the one `memory_mirror/deployment-target-intel-cpu.md` records as stubbed (`compute_z.py:216`), so even a hparams change cannot make the engine mimic it without a science-path patch. |
| 3 | **Objective: NLL on the target window + decay; no KL term; early stop at loss < 1e-2; clamp 4×.** `compute_z.py` ≈ 150–185: `nll_loss + weight_decay` only; `kl_factor` is loaded but unused in this file; `if loss < 1e-2: break`; `clamp_norm_factor` = 4 (shipped hparams). | NLL over template-augmented prompts **+ KL term** on the `"{} is a"` prompt (`kl_factor` 0.0625) + decay; 25 fixed steps; clamp 0.75. | **Yes** (KL term and clamp differ regardless of window). |
| 4 | Windowed autoregressive loop over the answer (`window_size`, `overlap`), one `delta` per window, earlier deltas re-applied via `all_delta` during later windows. | Single z per request. | **No** — with answer length ≤ `window_size` there is exactly one window and `all_delta` is empty; this difference does vanish. |

## Consequence for the Stage 0 forward routes (`docs/C10K_M3PRO_STAGE0_DIAGNOSTIC.md` §5)

- **Anchor (b) for Route A is not available.** A ported `memit_ARE` compared with the vendored engine would differ by construction (rows 1–3), so a mismatch would say nothing about the port and a match would be a coincidence. Strike it.
- **Route A keeps only anchor (a)** (static identity of the device patch with `device="cuda"`) plus comparison with the paper's published numbers on a different stack and model. A Route A result is therefore a *mechanism lead* with no local inertness anchor — as the diagnostic already states, now without the "if (b) holds" escape.
- **Route B is unchanged** but inherits the same point: the official solve is a different estimator from the program's MEMIT/AlphaEdit line (row 1), so even a source-faithful CUDA PASS speaks about `memit_ARE`/`AlphaEdit_ARE`, not about the band-[4-8] MEMIT recipe the F1 determination rests on. That was implicit in "mechanism-rescue lead"; it is explicit now.
- **Nothing here changes the halt.** It narrows the operator's choice: A is cheaper and weaker than the diagnostic's §5 allowed; B is the only faithful execution and still answers a neighbouring question.

## Not read / not claimed

`AlphaEdit_ARE/` (the projector variant) was not read line-by-line; row 1's `K_p` term is expected there too (same file lineage) but is **UNVERIFIED** in this note. No numbers were produced.
