GO-WITH-CHANGES

1. **The diagnosis is correct.** NEW-1 explicitly incorporates the **fail-closed CPU admission contract** of MathLab §6, not MathLab §8’s scientific stop (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:113`). MathLab’s admission rules cover inventory failures, autoresearch and verified coordinator-tail exceptions (`docs/MATHLAB_PREREG.md:274–279`); its calibration stop is separately specified at `:296–303`. NEW-1 separately retains calibration/prospective-utility requirements **for queue action**, not descriptive computation (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:135`). The disposition is explicit: NEW-1 continues independently (`CORPUS/60_MATHLAB_HARVEST_REPLAY.md:132–134`; `EXPERIMENT_RUNBOOK.md:107`).

   The causal path matches the recorded failure: `tools/new1_supervisor.py:166` invokes the shared policy before the CPU probe at `:168`; `tools/mathlab_runtime.py:264–266` raises on historical step-3 calibration FAIL regardless of the requested step. The launch’s `results/mathlab_staging/runs/new1_20261010T014248.014387Z/events.jsonl:3` records that exact refusal.

2. **The production repair is appropriately narrow, subject to the proposed history validation.** Keep `A.probe('cpu', lead)`, including its shared-prereg verification, fingerprint and inventory checks (`tools/mathlab_admit.py:29–73`). Preserve NEW-1’s frozen hash, deadline, resource limits, worker isolation and durable publication protections (`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:109–131`). Leave MathLab’s policy unchanged; do not catch and ignore LAB-STOP.

   Three prior resource/deadline aborts triggering OPERATOR preserves the **accepted implementation’s** guard (`tools/mathlab_runtime.py:274–279`). NEW-1’s narrow admission reference does not clearly freeze every MathLab §6 rule; retaining this scoped guard is conservative, not a newly discovered scientific prerequisite.

   The step=4 collision matters for retry attribution, so fix that **now through validated NEW-1 namespace/identity selection**, as proposed. Renumbering alone cannot fix the unconditional calibration check. Defer shared-schema renumbering: schema 1 only accepts steps 1–4, and NEW-1 consumer handling explicitly recognizes step 4 plus its title (`tools/mathlab_events.py:44,291`).

3. **The proposed RED test isolates this defect but cannot alone establish the scoped repair.** Its valid m3 fixture reaches the exact historical calibration branch; the direct shared-policy call is a useful positive control (`results/mathlab_staging/new1_v2_build_report.md:296–315`). However, simply deleting line 166 would also make it pass.

   Required changes/acceptance conditions:

   - **Replace the obsolete regression** demanding inherited LAB-STOP (`tests/test_new1_supervisor.py:274–279`) with scoped-policy assertions; otherwise the correct repair leaves the accepted suite contradictory.
   - Make MB3’s additional cases mandatory: fewer than three versus three NEW-1 aborts, unrelated step-4 aborts, malformed history, and actual admission refusal without dispatch (`results/mathlab_staging/new1_v2_build_report.md:320–324`).
   - Explicitly test current-run exclusion and counting each prior run once. Missing/contradictory NEW-1 history must refuse, not disappear through filtering (`:270`).

   **Static review only:** RED/GREEN behavior is predicted from source; tests were not executed. No launch approval follows.

