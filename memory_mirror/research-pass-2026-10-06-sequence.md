---
name: research-pass-2026-10-06-sequence
description: The 2026-10-06 OpenResearch research pass (30 leads, closed @ 900aa8e) and the operator-agreed experiment order; write-only ruling; where everything lives.
metadata:
  type: project
---

**Fact.** The research pass ran 2026-10-06 on OpenResearch (Claude Code harness, Fable 5.1 high; D-C10r-rulings-2) and CLOSED on branch `research-pass/2026-10-06` @ 900aa8e, imported under `results/research_pass_2026-10-06/` (entry point `HANDOFF.md`). It produced 30 leads (`hypotheses.md`), dispositions for every class, two inventory corrections (BetaEdit 2605.09285 is real and its repo device-portable; AnyEdit++ code exists, CUDA-bound) and one absence (`holi-lab/MDM-KE` does not exist). Nothing ran; nothing in that folder is evidence.

**Operator rulings (D-C10r-rulings-3).** Writing, not training: "training per commit defeats the spec's objective; likelihood of deploying it is essentially zero; run it only as a measurement" — H-13/H-15 are an oracle measurement, never a route; H-18 demoted. The agreed order is `recommended_sequence.md`: step 1 H-1 shared-z target (pre-registered `D-C10s-sharedz`, v3 frozen) → step 2 H-10/H-5 value-internal second key → step 3 H-19 two minted tokens → step 4 H-8 per-fact layer → gate A replication → step 5 H-13 oracle → steps 6–7 engine path (I-1/I-2, H-3) → step 8 model-generated covariance; model changes only after the Qwen ceiling rule. Integration goes through the program session (governance: research agents never touch trackers or run experiments).

**How to apply.** Before any C10 experiment, read the sequence and the stub for that step (`prereg_stubs.md`) and the Framework Council amendment list (`council_critique.md`); a run's pre-registration must carry a same-process injection screen where a target is involved, published and hashed phrasing frames with an overlap audit, per-frame bystander probes, the decomposition readout, and the two-process rule for PARTIAL/LEAD. Two-way link with research agents: files dropped in the project's `to_program/` folder on the dashboard server; replies via the session API (`tools/orx_api.py`).
