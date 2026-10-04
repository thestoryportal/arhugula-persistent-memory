# Route A — Amendment 2: model dtype fp32 on MPS (revision of deviation D5) — pre-registered before any edit result is read

**Parent prereg:** `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md` (D-C10k-route-a). **Date:** 2026-10-04. **Trigger:** the chain's anchor stage (`tools/c10k_route_a_chain.sh`, first launch 13:44) halted with a crash, not a disagreement: `logs/c10k_route_a_anchor.log` ends in `RuntimeError: expected mat1 and mat2 to have the same dtype, but got: float != c10::Half` at `AlphaEdit_ARE_main.py:129`, the per-layer solve. **No edit completed; no result exists.**

## 1. What happened (EVIDENCE-SHOWS)

D5 declared the model load as **fp16 on MPS** ("the program's standard load"). Upstream loads the model in **fp32** (`experiments/evaluate_uns.py:86`, `from_pretrained(model_name).cuda()`, no dtype argument) and its solve multiplies the fp32 projector `P` by keys read straight from the model (`layer_ks`, `layer_kp`). With an fp16 model those keys are fp16 and the matmul with the fp32 projector is rejected. Upstream never meets this case. The only ways to proceed are (a) cast the keys inside the module, which is not a device substitution and is forbidden by D1 (device-only port; `diff` must contain nothing but device expressions), or (b) load the model in upstream's dtype.

## 2. The amendment (D5 revised)

**D5 → model dtype fp32 on MPS and on CPU.** This is upstream's dtype; the port moves *closer* to the official setting, not further. Memory: 3B fp32 weights are 12.4 GB, within the 48 GB unified budget. The dynamic anchor keeps its pre-registered criteria (same canonical top-1 on all 3 items; per-layer update-norm ratio within [0.5, 2]) and now tests **device only** (MPS fp32 vs CPU fp32), which is a stronger anchor than fp16-vs-fp32 was: any disagreement is the port, not precision. D6 is unchanged (solve on MPS fp32; SVD on CPU fp32). D1 is unchanged (no module edit).

Changes: `c10k_route_a_launcher.py` run stage and anchor MPS leg load `torch.float32`; the anchor record key `mps_fp16` becomes `mps_fp32`; every result's scope string reads `fp32 on MPS (Amendment 2)`. The superseded `projectors` stage is left as is.

## 3. What this does not change

The verdict table (parent §4), the stop rules, Amendment 1 v2 (thresholds, gate, controls; the gate keys were extracted from the fp16 model, and the controls' key-parity cosine of 1.0000 says the key *positions and directions* are what the solve uses; fp32 keys differ from fp16 keys by rounding only, below the gate's bootstrap width), and the LAW#3 R0 baseline (c10e runs under its own load path).

## 4. Advisor

`tools/claude_advisor.sh` on this amendment: `logs/claude_c10k_route_a_amendment2_review.md`. Because the change is forced (no alternative within D1) and moves toward upstream, the chain is relaunched in parallel with the review; a FIX-FIRST item that bears on the setup stops the chain before any result is read.
