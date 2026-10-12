## UPDATE - 2026-10-06 late evening (step 1 HALTED at its LAW#5 inertness gate; nothing past the gate ran; waiting for the operator)

**HALT.** Fingerprint PASS (d941a9fb), machine idle, then `c10s_sharedz_inertness.py`: (i) floor 0.0, (ii) bit-identical, (v) harness LAW#5 INERT; **(iii) triplicate rel 0.122 and (iv) heterogeneous NLL Δ 0.0117 FAIL** against the frozen 1e-4. Read-only diagnosis (`results/c10s_sharedz_halt_analysis_2026-10-06.md`): fp16 batch-shape rounding (step-0 Δ 0.0026) amplified along the clamp sphere; same steps, same clamp count, same final fit; the driver mirrors the engine. No fix attempted (operator: HALT on any failure; a frozen-gate change needs review). Records: `results/c10s_sharedz/inertness.json`, `architecture_profile/c10s_sharedz_halt_diagnostic.json`, log `results/c10s_sharedz_logs/inertness.log`.

**Driver fact the earlier blocks got wrong:** `c10s_sharedz_arms.py first` runs the injection cell AND, if the screen passes, the harness pass in the same process; `second` is the gate-A replication, not the harness pass.

**Next (operator's reply first):** draft prereg amendment A2 (batch-shape-calibrated inertness criteria; candidate in the analysis note) → advisor + Codex → rerun inertness and stage `first` in a NEW `OUT_DIR`. Then the D-C10r-exp2ctl location control per the block below. Loop relaunch still waits on the sealing ruling + fence v13.

