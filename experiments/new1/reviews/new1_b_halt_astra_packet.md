# GPT-6-Astra (high) — NEW-1 D-NEW1-b real run HALTED: options ruling

Binding cross-family reviewer, read-only. Worktree = current dir, HEAD 48bfccf.

## What happened
The single operator-authorized D-NEW1-b run (C1: one attempt, no retry) halted INVALID-WORKER at ~255 s, before any prediction. No cap breach (peak RSS 8.54 GiB). Worker stderr: `Invalid: projector identity/probes mismatch` raised at `tools/new1_geometry.py:258` (`validate_capture` → `projector_matches` :230–240) for layer 4.
Read: `architecture_profile/s_new1_b_halt_diagnostic.json`; `results/mathlab_staging/runs/new1_20261010T053945.884468Z/` (events.jsonl, worker_stderr.log, receipts/); `tools/new1_geometry.py` (esp. :138–262, :530–560); `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` (identity/parity rules incl. Amendment B :190–220); `results/mathlab_staging/new1_b_variant_astra.md`; `results/mathlab_staging/new1_b_go_astra.md` (your GO-WITH-CONDITIONS); `REPRODUCIBILITY.md`. Find where the harvest bundle `results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt` captured `l4.Pi_*` (device, dtype, threads, code path) — search the harvest manifest/producer code; state what you find with file:line or say UNKNOWN.

## Orchestrator observations (verified)
- Captured `l4.Pi_null_n` = 8645 = 11008 − 2363; native CPU excluded count at L4 from the B measurement = 2363. So the count check very likely passed; the failure is SHA mismatch AND at least one of four seeded probes off by >1e-6 relative. Which probe and its magnitude were not logged.
- Captured null counts L5–L8: 7119, 5738, 4165, 1583.
- Program record: cross-process bit-exact reproduction does not hold on GPU; verification is behavioral (REPRODUCIBILITY.md). D-NEW1-fid already records native fp32 projector fidelity as OPEN.

## Decide
1. Most likely cause, with evidence. Is this a build defect (check is wrong/too strict for a cross-process fp32 SVD recompute), a provenance defect (capture made on a different device/path than the prereg assumes), or a real identity failure that should block?
2. Rank the options. For each: what it changes, whether it is a frozen-prereg amendment (→ operator), disk/time cost, and what would make it fail. Consider at least: (a) a bounded diagnostic-only measurement (no verdict): recompute native L4 projector on CPU, report per-probe relative errors, subspace distance to the captured probes, and capture provenance; (b) amend the identity rule to a tolerance justified by fp32 SVD conditioning near the cutoff; (c) re-derive the capture under the run's exact environment; (d) stop NEW-1 here and record the halt as terminal.
3. Under C1 the next real attempt needs a new operator authorization — say what that authorization must contain.

## Output
Under 600 words. First line: `RECOMMEND: <option letter>` + one sentence. Then Q1–Q3 with file:line evidence. Flag every item needing operator approval.
