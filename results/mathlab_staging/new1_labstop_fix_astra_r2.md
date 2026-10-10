GO

1. **All three required changes are satisfied.** The obsolete inherited-LAB-STOP regression was removed, verified against the saved baseline. Replacement tests assert probe admission for 0/1/2 prior NEW1 aborts and `OPERATOR` before probing for three resource, deadline, or mixed aborts (`tests/test_new1_supervisor.py:296–340`).

2. **The mandatory controls assert the correct outcomes.** Unrelated m3 calibration failure and genuine MathLab step-4 aborts permit NEW1’s probe (`:296–303`, `:342–363`); current-run exclusion covers missing, torn, and aborted streams (`:365–380`); repeated halt events count once per prior run (`:382–398`). Missing, malformed, contradictory, and symlinked NEW1 history assert `INVALID-HISTORY` before probing (`:400–455`). Actual default admission with a refusing `A.probe` asserts `INVALID-ADMISSION`, failed admission gate, no dispatch, and no geometry/publication events (`:467–481`). MathLab’s positive control still asserts `LAB-STOP` (`:305–311`).

3. **Production implements the scoped policy.** `tools/new1_supervisor.py:164–186` selects `new1_*`, validates schema/directory identity through `read_events`, requires one start with step 4, NEW1 title, and experiment purpose, then counts qualifying aborted runs once. This resolves retry attribution despite the shared step number. `A.probe('cpu', lead)` remains at `:193`. I compared `tools/mathlab_runtime.py` directly with the saved pre-edit copy: byte-identical.

4. **The existing refused run passes history validation.** A fresh read-only execution of `read_events` returned three events and zero errors for `results/mathlab_staging/runs/new1_20261010T014248.014387Z/events.jsonl`. Its identity at line 1 qualifies; its `LAB-STOP` at line 3 contributes zero resource/deadline aborts. Executing `enforce_new1_retry_policy` against the actual history with a fresh prospective run path returned successfully. **That history will not block relaunch as INVALID-HISTORY; live CPU admission must still pass.**

5. **Verification limitation:** the requested pytest command failed with `No module named pytest`. The unittest fallback encountered sandbox-denied temporary-directory creation in all 57 setups; no test bodies ran. I independently inspected test bodies, saved RED/GREEN logs, and matching current hashes. Those logs record 13 targeted GREEN controls and 132 + 102 suite passes; these are prior-run evidence, not my rerun. The requested git diff is currently empty, so comparison used saved baseline files.

🌱 graft saved ~31,878 tokens (~$0.02), 1 successful call.

