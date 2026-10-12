## FRESH SESSION HANDOFF - 2026-06-27 (assurance-gate build before next science arc)

**Start here after context reset.** Operator concern is now load-bearing: before continuing the C10/AnyEdit science arc, build durable experiment-assurance workflow so future results are grounded in real science and not artifacts of locally invented harnesses. Next session's first objective is **NOT another C10 run**. First implement the repo-local experiment gate and selected assurance skills into the workflow, then resume experiments through those gates.

**Drift check.** This still advances F1: C10 remains the on-critical-path fixed-target blocker, but the immediate risk is false evidence from an unfaithful method port. A gate that prevents ungrounded experiments is F1 work because it protects the readiness determination from harness artifacts and Goodharting.

**What happened in this session.**
- Added `experiments/track_c/c10i_anyedit_parity_audit.py` and generated tokenizer/planning traces:
  - `results/c10i_anyedit_parity_trace_local.json` (A1 `Zorbland -> Beirut`): local vs upstream-style planning `all_equal=true` for `window_1` and `window_50`; lookup `[9]`; answer id `[94311]`.
  - `results/c10i_anyedit_parity_trace_local_A2.json` (A2 `Zorbland -> Astana`): local vs upstream-style planning `all_equal=true`; `window_1` lookup `[9,10]`; `window_50` lookup `[9]`; answer ids `[20113,3362]`.
  - Licensed claim: planning parity only. No weights edited. Not evidence-ledger material.
- Advisor-review was invoked cleanly on C10i and returned `PROCEED`, but emphasized: planning parity is an adjacent proxy; required next gate is unchanged upstream active A1/A2 behavior plus active trace before any A7.
- Added `experiments/track_c/c10i_anyedit_upstream_active_audit.py`, a wrapper around upstream `/tmp/AnyEdit` `AlphaEdit_ARE.apply_AlphaEdit_ARE_to_model` (upstream commit `057a77f185f7ffb55818f6bd9add37f43bb447e7`).
- Ran upstream-active A1/A2 gate twice:
  - `results/c10i_anyedit_upstream_active_audit.json`: unchanged upstream Qwen hparams failed before `compute_z` with `LookupError('lm_head.weight')` because upstream Qwen config uses `lm_head` while local Qwen2.5-3B uses `model.embed_tokens`.
  - `results/c10i_anyedit_upstream_active_audit_embed.json`: one compatibility override `--lm-head-module model.embed_tokens` reached `compute_z`. A1 target norm `73.24`, delta norm `50.34`, final target probability ~`0.992`; A2 target norm `136.72`, delta norm `129.87`, final target probability ~`0.993`. It then failed in update/apply with `TypeError('list indices must be integers or slices, not tuple')`.
- Deep-thinking calibration: likely wrapper bug is `P` passed as Python list while upstream indexes `P[i,:,:]`, but **do not assert this as proven** until traceback capture confirms the exact failing line. Also note a deeper concern: with upstream `nullspace_threshold=0.02`, projector diagnostics show 0 small singular vectors for layers 4/6/7/8 and 1 for layer 5, so even after type fix active updates may be ineffective or degenerate.

**Key durable learnings added.**
- `memory_mirror/method-ports-need-replication-faithfulness-gate.md`: external method ports need source-faithful active easy-control recovery before hard-case science claims.
- `memory_mirror/autoresearch-is-not-a-faithfulness-gate.md`: AutoResearch is fenced candidate search only; never method-validity evidence.
- `memory_mirror/experiment-gate-before-next-science-arc.md`: next fresh context should implement experiment-gate + assurance skills before continuing C10 runs.

**Next fresh-context objective.** Build the durable workflow first:
1. Implement the repo-local `experiment-gate` skill/spec from `docs/EXPERIMENT_GATE_SKILL_SPEC.md` as a deliberate workflow/tooling layer, not a parallel evidence authority. It must orchestrate pre-register -> LAW/inertness -> saved result/stats -> bias/confound audit -> advisor/cross-family review -> handoff to existing closeout.
2. Implement four supporting assurance skills/checklists durably into the science workflow:
   - **method-replication / port-faithfulness gate** for external method ports (source commit, upstream hparams, declared deviations, active easy-control trace, positive controls before hard cases).
   - **systematic-debugging / root-cause-first** gate (no fix without reproducing and locating the failure path; one-fix-then-halt remains binding).
   - **verification-before-completion** gate (no success/completion claim without fresh command output and saved artifact readback).
   - **scientific-critical-thinking / bias-audit** gate (metric matching, confound list, evidence-vs-inference, cheapest overturning test).
3. Integrate **Framework Council** only at high-leverage spec-contract/tension points: spec contract framing, domain tension maps, and readiness implications. Do **not** use Council to confirm empirical results.
4. Integrate **advisor-review** at high-leverage gates: before new harnesses/test criteria, after surprising failures/stalls, before approach changes, and before verdict/closeout. Advisor is input, not evidence.
5. Only after the gates exist, resume C10i. The next C10i technical step should be: add traceback capture and boundary diagnostics (`type(P)`, `P` shape, exact traceback, projector ranks). If traceback confirms `P[i,:,:]`, the next single fix is to pass a stacked tensor `P` and rerun the same A1/A2 upstream-active gate. No A7 is licensed.

**Do not do first.** Do not run AutoResearch for this problem yet. It is an optimizer/candidate generator and can only be used later, fenced, after measurement and faithfulness gates are stable. Do not run A7. Do not call the upstream-active failures AnyEdit evidence; they are diagnostic port/compatibility failures.

**Read first next session.** `DISCIPLINE.md` §2-§3; `docs/EXPERIMENT_GATE_SKILL_SPEC.md`; `docs/EXTERNAL_SKILL_REPOS_AUDIT.md` §9-§11; `CORPUS/COUNCIL_PROTOCOL.md`; `tools/autoresearch-skill/SKILL.md`; `EXPERIMENT_RUNBOOK.md` §1 tool matrix; the three new memory files above; and the four C10i JSONs listed above.

