FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

**B1 — Resource admission weakens the parent contract.** NEW1 §6 requires only 8 GiB available; `docs/MATHLAB_PREREG.md:283,380` requires **8 GiB plus reserve: 13 GiB before SVD**. CPU admission is also unspecified. The existing runner accepts only m2/m3 and records RSS without enforcing NEW1’s proposed RSS ceiling (`tools/mathlab_cpu_runner.py:16–21,35–56`).

Replace the admission/enforcement sentences in §6 with:

> “Before numerical imports, require the fail-closed CPU admission contract of MATHLAB_PREREG §6. Before each heavy cell require available memory ≥8 GiB plus its declared reserve; the covariance-SVD reserve is 5 GiB, hence admission requires ≥13 GiB. Wait at most 300 s within the unchanged 1,800-s deadline. A NEW1-specific supervisor must enforce the deadline, terminate on observed worker RSS exceeding 6 GiB or available memory below 6 GiB, and refuse on monitoring failure. The existing MathLab runner does not establish these NEW1 protections. Execution remains gated on verified enforcement and declared reserves for every heavy cell.”

**ADVISORY**

- **Question/novelty: sound.** The trained-adapter spectra and subspace comparison are new within the inspected CORPUS. Closed-form confinement to null(C) is already known (`CORPUS/44:25`); the draft correctly treats it as an instrument control. This is pre-cast, cross-process geometry—not an explanation of the historical 70/72 versus 9/72 difference.

- **Inputs: verified. Retain harvest 1.** All draft-listed adapter, training-record, covariance, ancillary-file and manifest SHA pins match. Adapter headers/scalars and covariance headers match; update shapes are manifest-attested; 24-subject order matches. Harvest 1’s fresh-A7 gates pass; its three mint failures do not invalidate this A7-only study. Selected A7 SHA:
  `abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f`.
  Harvest 2 independently has **46/46 gates PASS**, but switching provides no required benefit here. Never combine their identities or admissions.

- **Statistics/predictions: sufficiently specified.** Fixed k, participation-ratio effective rank, numerical rank, principal angles, tie handling, q95 and same-layer 3/5 decisions are explicit. Numeric PASS/FAIL precedes computation; INVALID remains separate.

- **Controls: adequate for the narrow descriptive claim; strengthen interpretation cheaply.** Add descriptive \(M_{16}=U_{:16}\Sigma_{:16}V_{:16}^{T}\), subject to the existing boundary-validity rule, and report its retained energy, effective rank and covariance fractions. This separates full-update spectral-tail effects from the rank-16 comparison without another decomposition. A spectrum-matched random control \(U_j\operatorname{diag}(s(D))V_j^T\) would also improve the orientation comparison; the existing flat-spectrum null does not control spectral concentration. Neither addition should silently replace a primary endpoint.

- **S-3/tier: correct.** Locality and held-out generalization remain separate, unmeasured axes. No promotion, route closure or F1 inference is licensed.

- **Budget: bounded, not validated.** The verified measurement supports approximately 395 s for five covariance SVDs only. Full-workload completion within 1,800 s/6 GiB remains **UNVERIFIED**, as disclosed.

- **Queue mapping: mostly explicit.** Covariance outcomes affect optional covariance work; overlap outcomes affect position diagnostics; INVALID/STOPPED changes nothing. Remove the undefined “random-like profile” veto at §7:124 or give it a frozen numeric predicate. All actual queue actions remain blocked pending NEW1-specific calibration and prospective utility.

No geometry computed; no requested files edited.

🌱 graft reported ~161,385 tokens saved (~$0.08), 1 successful call.

