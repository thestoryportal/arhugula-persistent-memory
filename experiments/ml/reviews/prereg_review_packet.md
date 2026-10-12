You are the cross-family reviewer for a pre-registration in this repo. Verdict: GO or FIX-FIRST, then BLOCKING items (each with file:line evidence) and ADVISORY items. Read-only.

Document under review: docs/MATHLAB_PREREG.md (DRAFT v1, SHA-256 5d5008e0b2a4b59b18b91582d104620865a93a24237a613300a905af98d36b2d), Decision-ID D-ML-1.

What it is: an "offline math lab" that tests C10 hypotheses with linear algebra on saved tensors (covariance stats, harvested keys/values, target vectors, weight updates) on CPU, without loading the model. This prereg covers only step 1 (one GPU harvest pass), step 2 (a marimo notebook reproducing the harness's actual write solve and matching its ΔW), step 3 (retro-prediction calibration of an offline proxy against already-measured GPU outcomes; FAIL = stop the lab cheaply). Step 4 (autonomous hypothesis loop) is out of scope. Operator's requirements: autonomous, parallel to the main program, uses existing findings/data as context, unmounted from the model, math in Python in marimo notebooks; DuckDB as a derived query index; InfraNodus as a step-4 candidate-question source only.

Check specifically:
1. Every factual claim about code (file:line) and every calibration number (CORPUS/ or results/ path) — verify a sample of at least 10 against the files, including c10e_bandknob.py:205-211 and :423 (which solve the C10 arms actually use), c10x_enginepath_arms.py:1006-1027 (audit contents), and the CORPUS/44, 45, 46, 51, 54 numbers.
2. Step 1 harvest spec: is it complete enough that step 2 can reproduce the harness's sequential, null-space-projected per-layer solve EXACTLY (operands captured inside the write loop, positions, dtypes, layer order)? Does it run under the existing GPU gate and engine fingerprint gate, and leave the engine unmodified (LAW#5)?
3. Step 2 tolerance: numeric, fixed, and appropriate for fp16/fp32 MPS vs CPU float64 (note the known torch 2.8 MPS offset-view conversion bug: only .cpu().to(X) / .to(X).cpu() are safe).
4. Step 3: is the pass criterion (nine pairwise tier orderings; each held in >=95% of 2000 bootstrap resamples over 24 subjects; at least one of two frozen proxies) pre-registered completely, not gameable post hoc (proxy choice frozen, no tuning on the calibration arms), and neither trivially passable nor impossible? Is the proxy anywhere described as predicting top-1 recall (it must not be)?
5. Evidence tier: offline results may reorder/prune the GPU queue but never promote a claim — is that enforced in text, and is output staging-only consistent with AUTONOMY.md?
6. Resource rules: CPU-only, memory floor, interaction with tools/c10w_p2_gate.py (which refuses GPU dispatch while any python process runs) — is "parallel" honestly scoped?
7. DuckDB index: rebuildable, carries source path + pointer + SHA, never an authority.
Be concrete; no generic advice.
