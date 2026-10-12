RECOMMEND: a — Authorize a bounded provenance/identity diagnostic before changing tolerances or replacing the capture.

**Q1 — Cause and ruling**

**Most likely: numerical-path mismatch; precise cause UNVERIFIED.** There is a concrete build-side suspect: NEW1 normalizes using `np.divide(..., dtype=np.float32)`, whereas the producer uses PyTorch tensor/scalar division. Their normalized bytes have not been compared ([NEW1:138–146](tools/new1_geometry.py:138), [producer:499–511](memit_dry_run/memit/util/runningstats.py:499)). Thread/backend differences and cutoff-sensitive SVD variation remain competing explanations; genuine projector disagreement remains possible.

**Capture provenance:** `compute_P` performs **CPU fp32 SVD and CPU fp32 projector multiplication**, despite the model running on MPS ([producer:166–175](experiments/track_c/c10e_bandknob.py:166)). The hash-matched historical harvest source at commit `6ea8e7c`, `tools/mathlab_harvest.py:52–67`, copies that Pi to CPU, records rounded trace/hash, and computes four CPU probes with seeds 0–3. Manifest records torch **2.8.0**, matching source hashes, and fp32 probes; **capture thread count is UNKNOWN** ([manifest:52017–52028](results/mathlab/harvest_20261009T184950.056951Z/manifest.json:52017), [:52167–52168](results/mathlab/harvest_20261009T184950.056951Z/manifest.json:52167)). Thus, a GPU-versus-CPU projector decomposition is **not supported**.

The checker already permits nonidentical SHA through probe agreement. It faithfully implements Amendment B’s retained 1e-6 gate ([checker:230–240](tools/new1_geometry.py:230), [prereg:202](docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:202)). **No established checker defect or justification for declaring the tolerance excessive.** The GPU weight-reproducibility caveat concerns another object ([REPRODUCIBILITY:24–26](REPRODUCIBILITY.md:24)). Equal counts do not establish equal subspaces. This remains a **blocking identity failure**, not a prediction failure; D-NEW1-fid remains OPEN.

**Q2 — Ranked options**

1. **(a) Diagnostic-only — OPERATOR APPROVAL REQUIRED.** Compare producer/NEW1 normalized-C hashes and differences first; predeclare at most two native L4 decompositions, one per arithmetic path. Report count, projector hash, every probe error, and projection residuals against captured probes; record threads/backend/provenance. Four probes cannot establish full subspace distance: label results as sampled discrepancies. No adapter energies/verdict. No acceptance-rule amendment; separate diagnostic authorization. Proposed ceiling: **600 s, 11 GiB**, fresh admission; scalar/probe report under **1 MB**, no dense persistence. Existing native-SVD timing is ~76 s ([prereg:216](docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:216)). Fails to resolve cause if mismatch persists or provenance remains insufficient.

2. **(b) Tolerance amendment — OPERATOR APPROVAL REQUIRED, conditional on (a).** Changes frozen identity acceptance. Requires measured conditioning/backward-error justification and an error budget protecting native parity; “fp32 near cutoff” alone is insufficient. Freeze before further analysis, never choose epsilon merely to pass observed probes. Small documentation cost; certification time/disk **UNKNOWN**. Fails if discrepancies are structural, unbounded, or parity fails.

3. **(d) Stop — no amendment or compute.** Preserve INVALID/NOT-COMPUTED, leave mechanism unresolved. Negligible disk/time. **Operator decision required to make NEW1 terminal**; immediate no-retry remains mandatory. It fails only as a scientific answer: this halt does not falsify the predictions.

4. **(c) Re-derive capture — OPERATOR APPROVAL + prereg amendment.** Replacing capture changes pinned provenance; matching new probes to a new projector does not authenticate historical M. A coherent re-harvest needs new update/manifest pins. Bundle alone ~463 MB; total disk/time **UNKNOWN** ([prereg:29](docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:29)). Fails if old updates and new projector identities are mixed.

**Q3 — Next real authorization**

Explicitly authorize **one new attempt**, identify the reviewed repair/amendment and complete prereg/source/input hashes, fresh namespace, **2,700 s/11 GiB** or separately approved replacements, no retries, renewed C2 resource-validation disposition, unchanged C3 admission/reserves/nice-10, preserved halt artifacts, and MATH-PROXY-only reporting ([authorization:5–9](results/mathlab_staging/new1_b_run_authorization.md:5)). Diagnostic permission is not launch permission.

🌱 graft savings unavailable: one failed call.