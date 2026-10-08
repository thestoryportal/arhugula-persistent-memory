# MPS cross-device dtype-conversion audit (torch 2.8.0, Apple MPS), 2026-10-08

Read-only audit. No model was run. Every claim about torch behaviour below was measured with tiny tensors on this Mac's MPS backend (`.venv/bin/python`, torch 2.8.0). The probe scripts are in the session scratchpad (`probe2.py` to `probe7.py`).

## 1. The rule, as measured. It is wider than the original report

**The bug is in the MPS-to-CPU copy kernel whenever the copy also changes dtype.** `t.to(device="cpu", dtype=X)` is only one way in. Every API that copies across devices with a cast goes through the same kernel and fails the same way:

| Path (source `v` on MPS, target dtype ≠ `v.dtype`) | Broken? |
|---|---|
| `v.to("cpu", X)`, `v.to(device="cpu", dtype=X)`, `v.to(torch.device("cpu"), X)` | yes |
| `cpu_buf.copy_(v)` where `cpu_buf.dtype` ≠ `v.dtype` | yes |
| `cpu_buf[i] = v` (setitem into a CPU tensor of another dtype) | yes |
| `torch.as_tensor(v, device="cpu", dtype=X)`, `torch.tensor(v, device="cpu", dtype=X)` | yes |
| `v.to(cpu_tensor_of_other_dtype)`, `v.type(torch.FloatTensor)` | yes |

There are two failure modes.

- **Mode A: wrong output.** The output is wrong for *any* dtype change, widening ones included (fp16/bf16→fp32, int32→int64, …), when `v.storage_offset() != 0`. That covers `x[0,-1]`, `x[1:]`, `split`/`chunk`/`unbind` pieces after the first, and `select`/`narrow`. For narrowing or same-width casts (fp32→fp16, fp32→bf16, fp16↔bf16), the output is also wrong for non-contiguous offset-0 views such as `x.transpose(0,2)`.
- **Mode B: the MPS source is corrupted in place.** This is new and was not in the original report. It happens for narrowing or same-width casts: fp32→fp16, fp32→bf16, fp16↔bf16, int64→int32, int64→fp32, int32→fp32. The **MPS source tensor is overwritten** even at offset 0 and contiguous; for fp32→fp16 the first half of the source buffer was overwritten. This happened in 20/20 runs for fp32→bf16 and fp16↔bf16, and in 10/20 runs for fp32→fp16. The returned CPU tensor is usually right in this case, so the damage is invisible at the call site. If the source were a live model weight or activation, the model would be silently corrupted.

What is safe (all verified, 0 failures):

- Same-dtype moves: `.to("cpu")`, `.cpu()`.
- Same-device casts, including on offset views: `v.float()`, `v.to(X)`.
- **CPU→MPS in any form**: `.to("mps", X)`, `mps_buf.copy_(cpu)`, `mps_dst[...] = cpu_src`. The CPU source is never corrupted.
- MPS→MPS setitem/copy with a cast, with offset source or destination.
- `.item()`, `.tolist()`, `float()` on offset views.
- `torch.stack(views).to("cpu", X)`, because stack output has offset 0.
- Upcasts of offset-0 contiguous tensors (fp16/bf16→fp32).

Float64 targets from MPS always **raise** `TypeError`, whatever the path (`.to`, `copy_`, setitem, `as_tensor`). That failure is loud.

**Fixes:**

- **Correct fixes:** `v.cpu().to(X)` and `v.to(X).cpu()`. Both gave 0/50 failures in every dtype pair.
- **`v.clone().to("cpu", X)` is NOT reliable.** For narrowing it gave wrong output in 1/50 runs, for both fp32→fp16 and fp32→bf16, on an 8×4096 row. The `mps-offset-view-conversion-bug` memory note lists it as a correct alternative and should be amended.

## 2. Site table

Scope:

- An AST scan of every tracked or untracked `.py` under `experiments/`, `tools/`, `architecture_profile/` and the engine `memit_dry_run/memit/{memit,rome,util}`.
- The scan matched `.to(a,b)`, `.to(device=,dtype=)`, `.to(<tensor>)`, `.copy_`, `.type(`, and `torch.tensor/as_tensor(x, device=, dtype=)`.
- A second AST scan covered subscript assignments in the 118 MPS-era non-test files.
- Greps covered `.cpu()`/`.float()` ordering, CPU buffer allocations and logits-row conversions.
- The upstream `external_prior_art/AnyEdit_mps` code used by C10K Route A was also scanned. It has no combined conversions.

Selftests were excluded. Line numbers are the current working tree; the C10Z files are unchanged from HEAD at these lines.

### MPS → CPU with a dtype change (the dangerous direction)

| file:line | pattern | class | reason |
|---|---|---|---|
| `experiments/track_c/c10z_astra_arms.py:224` (`margin_leads`), reached from `:1059` | `logits.detach().to(device="cpu",dtype=torch.float32)` on `native=model(...).logits[0,-1]` | **AFFECTED** | MPS fp16 offset view, upcast → Mode A garbage. This is the known ASTRA cause. |
| `c10z_astra_arms.py:224`, reached from `:1062` | same, on `full[len(prompt)+q-1]` (a row of `logits[0]`) | **AFFECTED** | Offset ≠ 0 for every q → Mode A. Feeds `original_full_sequence_sigma`. |
| `c10z_astra_arms.py:224`, reached from `:655` | same, on `selected = native.logits[rows,positions].detach().float().cpu()` | SAFE | The input is already CPU fp32 (advanced-index gather, then `.float().cpu()`). This is the batch path. |
| `experiments/track_c/c10z_astra_z0_probe.py:170`, `:171` | `D.margin_leads(prefix_logits[-1][None,:], …)`, `D.margin_leads(full[index][None,:], …)` | **AFFECTED** | Offset rows of MPS logits → Mode A. |
| `c10z_astra_z0_probe.py:181` | `prefix_logits.detach().to(device="cpu",dtype=torch.float32)` | SAFE (fragile) | `prefix_logits = logits[0]` has offset 0 and is contiguous, and the cast is a widening upcast. Mode B does not apply to upcasts. It becomes AFFECTED if the probe ever slices first. |
| `c10z_astra_arms.py:347` (`target_probabilities`) | `gathered[start:start+chunk_rows].detach().to(device="cpu",dtype=torch.float32,copy=True)` | SAFE now, LATENT | The only caller (`:429`) passes `obs["native_gathered"]`, which is CPU fp32 (`:652`). It would be AFFECTED if ever given an MPS tensor: every chunk after the first is an offset slice. |
| `c10z_astra_arms.py:343` | `targets.detach().to(device="cpu",dtype=torch.long)` | SAFE | CPU int64 (`:654`), so no change. |
| `c10z_astra_arms.py:253` (`semcon`) | `C.to(device="cpu",dtype=float32)` | SAFE | `C` comes from `covectors`, i.e. `torch_cpu64`, so it is a CPU→CPU cast. |
| `c10z_astra_arms.py:177` (`torch_cpu64`) | `value.detach().to(device="cpu",dtype=torch.float64)` | LOUD, not silent | A float64 target from MPS raises `TypeError`. Callers that pass MPS model tensors would crash: `:684-686`, `:1159`, `:1162`, `:1213-1215` (`norm.weight`, `embed_tokens.weight[...]`, `W[i:i+8192]`). These are `covectors` and `compute_G`, which have not been reached yet (no `G.pt` under `results/c10z_astra*`). This is a latent loud crash for attempt 3, not a data risk. |

### CPU → MPS, or MPS → MPS (destination on MPS): all SAFE (verified for every dtype pair with offset sources and destinations)

| file:line | pattern | why SAFE |
|---|---|---|
| `experiments/track_c/c10e_bandknob.py:217` and its ~30 clones (`npd[WN(layer)][...]+=upd.to(npd[..].device,npd[..].dtype)`). The clones are in track_a/b/d/e, scale, r*, c10_*, c10b/c/d, `c10h_anyedit_pilot.py:351`, `c10x_enginepath_arms.py:522`, `governance/cp1_governed_write.py:302`, `tools/law5_inertness_gate.py:92`, `autoresearch_band_search/run_edit.py:99`, `autoresearch_c10/edit.py:76` and `c10l_covgeom_step0.py:130`. | `upd` comes from the CPU solve (`c10e:209-211`): CPU fp32 → MPS fp16. |
| `c10w_oracle_eval.py:113` | `d16=delta.to(weight.device,weight.dtype)` | `delta` is CPU (enforced by `R.require` at `:110`), so this is CPU→MPS. `:114` copy_ and `:276` are MPS→MPS. |
| `c10u_mint2_arms.py:428`, `c10x_enginepath_arms.py:726`, `c10x_enginepath_arms.py:1017`, `c10l_mint_lib.py:97`, `c10l_covgeom_p6_zinject.py:40`, `c10s_sharedz_arms.py:434` | z, rows or vectors written into MPS hidden states or embeddings | The destination is on MPS. |
| `autoresearch_c10/scorer.py:149` | `w[n].copy_(t.to(w[n].device,w[n].dtype))` | `t` comes from `torch.load(map_location="cpu")`, so this is CPU→MPS. |
| `c10y_directdw_arms.py:242`, `:423`, `:594`, `:1851`, `:2038`, `:2243` | `.to(<tensor>)` | The target is an MPS weight or hidden tensor. At `:2038`, `stored_weight(...)` is already fp16 on `W0`'s device, so the call is a no-op. |
| `c10z_astra_arms.py:566`, `:856`, `:1023` | `w.copy_(x.to(w.device))` | The destination is on MPS. |
| `autoresearch_reaim/run_iteration.py:171`, `architecture_profile/smoke_test.py:374` | two-step `.to(dtype).to(device)` | Two separate operations. |

### Constructors and engine

| file:line | class | reason |
|---|---|---|
| `c10z_astra_arms.py:1229`; `c10z_astra_z0_probe.py:117`, `:118`, `:173`; `c10h_anyedit_pilot.py:200-201`; `util/runningstats.py:1105`, `:1142` | SAFE | The inputs are Python lists, floats or numpy arrays. An MPS float64 input would raise loudly. |
| Engine `memit/memit_main.py:56`, `:192-203`, `:217`, `:280`, `:283`; `memit/compute_z.py`; `memit/compute_ks.py`; `rome/layer_stats.py:164`; `rome/repr_tools.py` | SAFE | There is no combined form. Moves are `.cpu().double()` (P-VRAM-CPU-SOLVE), `.float().to(device)`, or `.float().to("cpu")` (which casts on the device, then moves at the same dtype). `layer_stats:164` is a same-device cast. The HEAD AST test `c10x_enginepath_selftest.test_no_combined_device_dtype_conversions` already enforces "no combined form" for the engine. |
| `c10e_bandknob.py:84-85`, `:103-105`, `:172`, `:175`, `:209-210`, `:219`, `:306` (scoring, KL, cov, cache) | SAFE | These are `logits[0,-1].float()` (same-device cast of an offset view), then `.cpu()`, plus `.cpu().double()` and `.cpu().float()`. The CPU caches (`:428`, `:474`) only ever receive `CPU @ CPU`. |
| C10W: `c10w_oracle_eval.py:73`, `:139`, `:253-259`, `:300`; `c10w_oracle_train.py:88`, `:94-95`, `:201-210`, `:226`; `c10w_oracle_read.py` (JSON only); `tools/c10w_p2_gate.py`; `tools/c10w_p2_rerun.py` | SAFE | All moves are same-dtype `.cpu()`, or a same-device cast followed by `.cpu()`. |
| C10K–C10V arms (`c10k_route_a_*`, `c10l_*`, `c10m`–`c10v`), `tools/precompute_cov_l9_12.py`, `tools/law5_inertness_gate.py` | SAFE | The scans found no MPS→CPU conversion with a dtype change. Logits rows are always `.float()` on the device first, then `.cpu()`, `float()`, `argmax` or `topk`. |

No site anywhere performs a **narrowing** MPS→CPU conversion, so Mode B (source corruption) has no hit in this repo.

## 3. Impacted recorded results (MPS era, CORPUS 41–57)

**None of CORPUS 41–57 passed through an AFFECTED site.** That covers:

- C10K, CORPUS 41–43
- C10L/M/N/O/P/Q/S/T, CORPUS 44–53
- C10U, CORPUS 54
- C10W, CORPUS 55 and 57
- C10V, CORPUS 56
- the c10e_bandknob scoring and eval paths
- the engine's `compute_z`/`compute_ks`/`memit_main`

Every AFFECTED site is in C10Z (ASTRA), which has no CORPUS entry. The affected recorded outputs are:

| result | corrupted fields | visible? |
|---|---|---|
| ASTRA attempt 2 (`results/c10z_astra_attempt2/`, `architecture_profile/c10z_astra_halt_diagnostic*.json`) | Z0 `sigma_shape` and `original_full_sequence_sigma`, both from `:1059`/`:1062` | **Visible.** The values were about 1.13e8, so V5 halted. The halt verdict "HALTED-V5" is an instrument artefact, not a science result. |
| `results/c10z_astra_z0_probe/20261008T132220Z/probe.json`, `20261008T134353Z/probe.json` | `native_lead`, `full_lead`, all `diffs`/`abs_diffs`, `summary.*`, `full-batch`, `z0_sigma_shape`, `z0_full_sigma` (`batch_lead` and `batch1_lead` are correct) | Visible. The values are about 1e5–1e8, and `native_minus_full = 0` only because both sides are corrupted. Treat both files as invalid. |

## 4. Re-verify first (ranked)

1. **ASTRA Z0 (attempt 2 HALTED-V5).** Fix `margin_leads:224` to use `logits.detach().cpu().float()`, then re-measure Z0 sigma before ruling on V5. The current halt is not evidence about ASTRA.
2. **`c10z_astra_z0_probe` outputs.** Discard both `probe.json` files and re-run after the fix.
3. **ASTRA latent crash, before attempt 3.** `torch_cpu64` is called on MPS model tensors in `covectors` and `compute_G` (`:684-686`, `:1159-1162`, `:1213-1215`). It will raise `TypeError` the first time those paths run on MPS. Rewrite it as `value.detach().cpu().double()`. The same fix removes the latent hazard at `:347`.
4. **Guards.** Extend the existing AST ban (`c10x_enginepath_selftest.test_no_combined_device_dtype_conversions`) to all of `experiments/` and `tools/`, starting with `c10z_*`. Also ban `copy_`/setitem into CPU tensors from MPS sources of another dtype, and remove `clone().to(cpu,X)` from the "safe" list in the memory note.
5. **Nothing in CORPUS 41–57 needs re-running for this bug.**
