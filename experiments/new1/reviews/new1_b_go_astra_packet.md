# GPT-6-Astra (high) — NEW-1 D-NEW1-b: go/no-go for ONE real run

You are the binding cross-family reviewer for the LLM-as-Database program. Read-only. Worktree: current directory (branch worktree-c10k-route-a, HEAD 98302b3).

## Decide
Is the committed Amendment B build fit for exactly ONE real NEW-1 run (CPU, fresh namespace, `--prereg-sha 1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f`)? Answer GO, GO-WITH-CONDITIONS (list each condition as a checkable precondition), or NO-GO (list each blocker with file:line).

## Read in full
- docs/NEW1_ADAPTER_GEOMETRY_PREREG.md (Amendment B starts at :190; caps at :218–220)
- results/mathlab_staging/new1_b_variant_astra.md (your prior ruling the operator approved)
- tools/new1_geometry.py, tools/new1_supervisor.py, tests/test_new1_geometry.py, tests/test_new1_supervisor.py
- results/mathlab_staging/new1_v2_build_evidence/mb4_20261010_brobust/astra_build_review.md (a static review by the builder's reviewer; NOT confirmed to be you — do not defer to it) and resource_projection.json
- results/mathlab_staging/new1_v2_build_report.md:60–75 (recorded launch command; its --prereg-sha is the OLD pin) and the "Amendment B (D-NEW1-b)" section near the end

## Facts verified by the orchestrator this session
- 34 geometry + 61 supervisor tests re-run: all OK. File SHA-256 prefixes: prereg 1616c860, new1_geometry 018ce4d9, new1_supervisor a69d4107, tests 57afd250 / 33c61282.
- Engine fingerprint PASS (memit_main d941a9fb, _cov_cpu 3). /Volumes/memit has 85 GiB free.
- Operator approval on record (SESSION_CHECKPOINT.md:14): "Operator approved NEW-1 boundary-robust B (D-NEW1-b)". It does not separately mention the spending caps.

## Specific questions
1. Do the code paths implement Amendment B as frozen (native parity separate from float64 geometry; every integer cutoff in the band; same ≥3/5 layers at all cutoffs else BOUNDARY-SENSITIVE)? Any divergence between prereg text and code?
2. Caps were raised 1,800 s / 6 GiB → 2,700 s / 11 GiB. Is that a necessary consequence of the approved variant (measured float64 SVD 159 s, 258 s/layer, 8.06 GiB RSS), or a separate spend decision that must go to the operator?
3. Projection 2,525.9 s vs 2,700 s (6.4% headroom) and 10.07 vs 11 GiB: on a cap breach the run is STOPPED-RESOURCE. Is that an acceptable risk for one attempt, or should headroom be fixed first?
4. Anything that would make a completed run's verdict unpromotable (pin mismatch, label laundering, missing control)?

## Output
Under 700 words. First line exactly one of: `VERDICT: GO`, `VERDICT: GO-WITH-CONDITIONS`, `VERDICT: NO-GO`. Then numbered answers to Q1–Q4 with file:line evidence. Then the exact launch command you endorse (with the new prereg SHA). Do not restate the prereg.
