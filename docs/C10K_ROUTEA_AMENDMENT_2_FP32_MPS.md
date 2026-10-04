# Route A — Amendment 2 (revised after advisor review): model dtype fp32 on MPS (revision of deviation D5) — pre-registered before any edit result is read

**Parent prereg:** `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` (D-C10k-route-a). **Date:** 2026-10-04. **Trigger:** the chain's anchor stage (`tools/c10k_route_a_chain.sh`, first launch 13:44) halted with a crash, not a disagreement: `logs/c10k_route_a_anchor.log` ends in `RuntimeError: expected mat1 and mat2 to have the same dtype, but got: float != c10::Half` at `AlphaEdit_ARE_main.py:129`, the per-layer solve. **No edit completed; no result exists.**

## 1. What happened (EVIDENCE-SHOWS)

D5 declared the model load as **fp16 on MPS** ("the program's standard load"). Upstream loads the model in **fp32** (`experiments/evaluate_uns.py:86`, `from_pretrained(model_name).cuda()`, no dtype argument) and its solve multiplies the fp32 projector `P` by keys read straight from the model (`layer_ks`, `layer_kp`). With an fp16 model those keys are fp16 and the matmul with the fp32 projector is rejected. Upstream never meets this case. Three ways exist: (a) cast the keys inside the module, which is not a device substitution and is forbidden by D1 (device-only port; `diff` must contain nothing but device expressions); (b) cast `P` to fp16 outside the module, D1-compliant but a step *away* from upstream's fp32 solve; (c) load the model in upstream's dtype. (c) is chosen.

## 2. The amendment (D5 revised)

**D5 → model dtype fp32 on MPS and on CPU.** This is upstream's dtype; the port moves *closer* to the official setting, not further. Memory: 3B fp32 weights are 12.4 GB, within the 48 GB unified budget. The dynamic anchor keeps its pre-registered criteria (same canonical top-1 on all 3 items; per-layer update-norm ratio within [0.5, 2]) and now tests **device only** (MPS fp32 vs CPU fp32), which is a stronger anchor than fp16-vs-fp32 was: any disagreement is the port, not precision. D6 is unchanged (solve on MPS fp32; SVD on CPU fp32). D1 is unchanged (no module edit).

Changes: `c10k_route_a_launcher.py` run stage and anchor MPS leg load `torch.float32`; the anchor record key `mps_fp16` becomes `mps_fp32`; every result's scope string reads `fp32 on MPS (Amendment 2)`. The superseded `projectors` stage is left as is.

## 3. What else the dtype change touches (advisor items, each with its mechanism)

**3.1 The gate and controls were measured on fp16 keys; the run edits in fp32.** Gate v2 run 2 and the §8 controls of Amendment 1 extracted every key (Wikipedia, A1, held-out, ARE-window) from the fp16 model. The key-parity cosine of 1.0000 compared fp16 keys with fp16 keys and says nothing about fp32. **Mechanism:** `c10k_route_a_gate_v2.py` and `c10k_route_a_gate_v2_controls.py` now load fp32 and write `keys_dtype` into their records; the launcher's `load_P` refuses any gate record whose `keys_dtype` is not `float32` (`HALT Amendment 2`), so no R1 arm can run against the fp16 gate. The fp16 records are kept as `projector_gate_v2_run2_fp16keys.json` and `projector_gate_v2_controls_fp16keys.json`. The controls additionally report, per layer and key set, the fp16-vs-fp32 key cosine (6 decimals) and relative norm difference. **Reading:** the fp32 gate must pass the same bounds at the same thresholds (no re-selection; if a bound fails at fp32 the chain halts and Amendment 1's rule is re-applied on the fp32 record, pre-edit). Results appended in §6.

**3.2 The covariance cache was accumulated from fp16 activations.** `tools/precompute_cov_l9_12.py:36` (and the band precompute it mirrors) loads the model `torch_dtype=torch.float16`; the accumulator is float32 (`layer_stats --precision float32`). Upstream accumulates from an fp32 model (`rome/layer_stats.py:50`, `mom2_dtype float32`). This is a second dtype deviation, **D4-b, declared here**: the null space is the small-eigenvalue end of that covariance, the part most exposed to activation rounding. The cheap test is 3.1: the fp32 gate on the existing `P`. Rebuilding the five covariance layers from an fp32 model is pre-registered as a **sensitivity follow-up, not a precondition** (it is a multi-hour compute on this machine and is only warranted if the fp32 gate moves a layer).

**3.3 R0 is fp16; R1–R3 are fp32.** The LAW#3 baseline (`c10e_bandknob.py:41`) loads fp16 and its known values were established at fp16; running it at fp32 would break its own reproduction gate. **Mechanism:** every R1–R3 arm now records a **same-dtype pre-edit evaluation** (`pre_summary`, `pre_rows` in each result: the identical `eval_case` battery on the unedited fp32 model before `apply`). The parent §4 criteria that compare against R0 ("≥ +20 pp over R0 A7", "R0 within its LAW#3 band") are read as follows: R0 keeps its LAW#3 role (is the harness sane at fp16); the +20 pp effect size is computed against the arm's own fp32 `pre_summary`; the R0 number is reported beside it with the label *cross-dtype*. Every result's scope string already carries `fp32 on MPS (Amendment 2)`.

**3.4 Reading is blocked mechanically, not by intention.** Commit order is the mechanism: this revision and the code in 3.1/3.3 are committed before the fp32 gate record exists, and `load_P` cannot pass until that record is written with `gate_ok` and `keys_dtype == float32`. The chain relaunched at 13:47 could therefore reach R1 only after this gate passes; if it reaches `load_P` first it halts and is relaunched. The anchor (device parity) does not depend on 3.1–3.3 and its 13:50 result stands: same top-1 on 3/3, update-norm ratios 1.36/1.23/1.12/1.01/1.00 (MPS/CPU, L4–L8), all inside [0.5, 2].

**3.5 Memory and stale records.** The anchor runs its two legs sequentially (`del model` + cache flush between them), never both resident. The 13:44 crash raised before `anchor.json` was written, so no `mps_fp16` record exists; the key is now `mps_fp32`.

**Unchanged:** the verdict table (parent §4) and stop rules; Amendment 1's thresholds and rule; D1 (no module edit); D6.

## 4. Advisor

First review (FIX-FIRST): `logs/claude_c10k_route_a_amendment2_review.md`. Items → §3.1 (fp32 gate + key comparison, mechanical block), §3.2 (covariance dtype declared, D4-b), §3.3 (R0 cross-dtype; in-arm fp32 pre-edit reference), §3.4 (mechanism), §3.5 (memory, stale record), §1 (third option named).

## 5. Status of the chain under this revision

Anchor passed (§3.4). R0 runs at fp16 as the LAW#3 reference. R1 cannot start before the fp32 gate record exists (§3.1).

## 6. fp32 gate and controls (EVIDENCE-SHOWS; appended after the run)

_(pending)_
