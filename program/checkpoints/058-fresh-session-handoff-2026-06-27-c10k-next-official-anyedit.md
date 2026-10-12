## FRESH SESSION HANDOFF - 2026-06-27 (C10K next: official AnyEdit source-faithfulness on current GPU)

**Start here after context reset.** The operator has re-grounded the AnyEdit/C10 path: do **not** propose A100 or any other GPU rental. The only allowed science hardware is the current pod (`RTX 4090 24GB`), and the ultimate deployment target remains a local 2020 Intel MacBook Pro with 16GB RAM. Bounded hybrid / side-store is **not** accepted as F1 closure for this C10 blocker because it nullifies the intended Git-vs-LLM persistent-memory separation.

**North-star state.** C10 remains OPEN/BLOCKING: the spec needs in-weight handling of project-coined multi-word semantic values. C10h/C10J local AnyEdit/ARE transplant failures do **not** falsify official upstream AnyEdit; they only show local wrapper/transplant paths are not evidence-bearing until source-faithful active controls pass.

**Committed state.** Latest pushed commit: `3afe844 Constrain AnyEdit route to current GPU`. Key docs:
- `docs/C10K_ANYEDIT_OFFICIAL_UPSTREAM_PREREG.md`
- `memory_mirror/no-a100-current-gpu-only.md`
- `docs/SCIENCE_WORKFLOW_REVIEW_2026-06-27.md`

**Next science step.** Run **C10K Stage 0 only**: source-faithfulness validation for official `jianghoucheng/AnyEdit` on the current RTX 4090.

Concrete next actions:
1. Create an isolated upstream AnyEdit environment on the current pod only.
2. Resolve the upstream dependency contradiction: README pins `transformers==4.23.1`, but shipped Qwen2.5/Llama3 configs likely require newer `transformers`.
3. Get official upstream import/CLI smoke working without modifying AnyEdit algorithm code.
4. Run a small stock-upstream source-run anchor.
5. Emit `logs/c10k_anyedit_official_upstream_env.json` and the stock-anchor artifact named in the prereg.

**Stop rule.** If official AnyEdit cannot run source-faithfully on the current RTX 4090 without unapproved source/VRAM patches, halt with `HALTED - HARDWARE_ENVELOPE`. This is not an AnyEdit method verdict; it is a hardware/source-faithfulness diagnostic. Do not run C10 A1/A2/A7 until Stage 0 passes.

**Workflow discipline.** Keep outputs concise. Do not dump skill schemas/checklists. Skills are contracts, not agents. Use Claude advisor only at the prereg/failure/approach-change gates and feed it exact artifacts.


