B-VARIANT: Boundary-robust covariance geometry

1. **Receipt verified; no SVD rerun.** All 16 JSONL records parse; the receipt SHA matches the report. Native SVD: **76.274 s**; float64: **159.296 s**; checks: **21.215 s**; complete profile: **258.024 s**, exit **0**, child high-water **8.056793 GiB**. [receipt.jsonl:14–16](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_b_measure_20261010T034731Z/receipt.jsonl:14)

   Excluded counts are **2363 versus 2364**; zero-based index **2363** crosses from **0.0049956482835114** to **0.00500721146627674**. Equal-count B therefore **FAILS**. Correction: SVD residual is **1.373e−13**, but PSD residual is **2.733e−10**, only **4.56 orders** below its 1e−5 gate—not eight. These are covariance-check passes, not full-study acceptance. [receipt.jsonl:6](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_b_measure_20261010T034731Z/receipt.jsonl:6)

2. **Three principled variants exist, but each changes the estimand.** None retrospectively passes original B.

   **Count-matched B:** For every layer, use its native excluded count \(r_{32}\), selecting the first \(r_{32}\) float64 directions. Amend §3’s subset definition accordingly. This preserves dimension, **not** the literal float64 0.005 threshold or native subspace identity; equal ranks do not certify close projectors.

   **Boundary-band B:** Define the band mechanically as float64 ranks \(\min(r_{32},r_{64})+1\) through \(\max(r_{32},r_{64})\), across every layer. Report excluded core, band and allowed core separately. Amend §3’s binary partition/complement rules and §4’s interpretation. This establishes descriptive allocation, not a unique excluded-energy prediction; the band is observed disagreement, not a certified numerical uncertainty interval.

   **Recommended invariance variant:** Retain both cutoff definitions and test **every integer cutoff between their counts**, using float64 ordering. Report band energy for every arm/control. Apply unchanged prediction margins; require the **same ≥3/5 layers** to satisfy every cutoff for robust PASS. Mixed outcomes become **BOUNDARY-SENSITIVE**, never a selected favorable result. Freeze this rule before update-energy inspection, without special-casing L4.

   All variants require append-only supersession of §3:51–59, affected §4 rules, §6 resources and A1:182–186. Replace B’s equal-count/universal cross-projector equivalence requirement explicitly. Retain native captured-projector identity and native excluded-energy parity separately; float64 excluded energy becomes geometry, not native-solve parity. Rename H-COV’s “directions this solve excludes” accordingly. None establishes native-basis reproduction or behavioral causation. [prereg:49–89](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:49), [draft:611–631](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_v2_build_report.md:611)

3. **Record a projector-fidelity warning separately.** The native recipe admits one additional dimension relative to the higher-accuracy decomposition of the *stored, fp32-normalized covariance*. This is not proof of one tracked direction being misclassified against an exact decomposition: vectors can rotate, and float64 remains approximate. Unequal-rank ideal orthogonal projectors have operator distance **1**, so small dimensional disagreement cannot justify uniform 1e−5 equivalence. Actual rounded native P, update-weighted leakage and locality effects remain unmeasured. [core.py:44–48](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/mathlab/core.py:44), [draft:631](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/new1_v2_build_report.md:631)

   Keep the receipt/report as the detailed numerical finding; propose a hypothesis-register entry for projector fidelity and an append-only qualification of historical “null-space share,” without revising behavioral verdicts. [CORPUS/44:25](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25)

4. **Recommend Boundary-robust covariance geometry** because it tests a disclosed, layer-independent robustness question without forcing parity; adoption and full-workload resource validation remain prerequisites, not execution clearance.

🌱 graft saved ~159,227 tokens (~$0.09), 1 successful call.

