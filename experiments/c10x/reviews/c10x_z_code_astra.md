GO
Reviewer: GPT-6-Astra (high)

**BLOCKING:** None.

Verified against §13 and `a1732da`:

- X2-(vii) alone changes to explicit shape/fp16 checks plus CPU `torch.equal`. Contiguous CPU int16 counts and signed-zero diagnostics do not determine acceptance (`c10x_enginepath_inertness.py:95,123,507`).
- Exact-zero residual/update gates, observer, negative controls, X2-(iv), tolerances, G8, W0 and T8 remain unchanged.
- Signed-zero writes pass and record counts; one-ULP changes, NaN, wrong dtype/shape and nonzero updates halt. HALT records preserve measured values.
- Prereg hash matches `d3dfdc8b…`; all active pins updated.
- **83 tests PASS, 19.547s**, including AST copy-safety test 72. Both live-tree listing deltas empty.

**ADVISORY:**

- Reader changes also include a narrowly scoped report-only null exemption—not literally just checkpoint removal. This correctly prevents unavailable diagnostics from vetoing admission (`c10x_enginepath_read.py:111,1013`).
- Rerun wiring is correct (`c10x_enginepath_arms.py:210,1291`). Use absolute paths, `--process 1`, fresh `results/c10x_enginepath_rerun1/`, a new go record, predecessor `results/c10x_enginepath/`, and `--cause 'W0 X2-vii exact zero'`. The historical telemetry-on example at `results/c10x_enginepath_codex_build.md:1327` is not this amendment’s launch command. New operator go remains required; no dispatch performed.

Live GPU/MPS behavior remains **UNVERIFIED**.

🌱 graft saved ~182,941 tokens this turn, 1 successful call.

