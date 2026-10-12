## FRESH SESSION HANDOFF - 2026-06-27 (experiment gate implemented)

**Start here after context reset.** The immediate assurance objective from the prior handoff is complete: the repo-local experiment gate is implemented as `tools/experiment_gate.py` plus `tools/skills/experiment-gate/`. `docs/EXPERIMENT_GATE_SKILL_SPEC.md` now points to the implementation. This is workflow/tooling only, not a science result and not CORPUS material.

**What changed.**
- Added `tools/experiment_gate.py` with `init`, `check-prereg`, `check-result`, `audit-method-port`, and `bundle`.
- Added `tools/skills/experiment-gate/SKILL.md`, a prereg template, and reference checklists for metric matching, sampling units, confounders, method-port faithfulness, root-cause-first debugging, verification-before-completion, and review routing.
- The gate fresh-reads saved JSON, blocks aggregate-only completion claims, writes stats reports under `logs/experiment_gate/`, hard-fails method ports that license hard cases before easy controls pass, and never writes `CORPUS/*`.
- Installed five supporting repo-local methodology skills for both Codex and Claude (`methodology-superpowers`, `scientific-critical-thinking`, `debug-mantra-scrutinize`, `premortem-the-fool`, `scientific-problem-selection`) using `tools/install_science_methodology_skills.sh`; restore now reinstalls them.
- Re-routed Codex-led advisor-review to Claude via `tools/claude_advisor.sh` using local `claude.ai` Max subscription auth (`authMethod=claude.ai`, no API key); Codex/GPT review is now fallback or secondary for Codex-led work.

**Verification run.**
- `python3 -m py_compile tools/experiment_gate.py` passed.
- `python3 tools/experiment_gate.py check-prereg tools/skills/experiment-gate/assets/prereg_template.md` passed.
- Synthetic gate tests behaved correctly: aggregate-only result BLOCKED; per-unit result PASS with stats report; bad method-port packet BLOCKED; bundle BLOCKED when review status was pending. Temporary log artifacts were removed.
- `python3 tools/stats.py selftest` passed.
- `python3 tools/power.py selftest` passed.

**Next objective.** Resume C10i only through the new gate. The next technical step remains the bounded upstream-active diagnostic: add traceback capture and boundary diagnostics (`type(P)`, `P` shape, exact traceback, projector ranks). If traceback confirms the suspected `P[i,:,:]` list/tensor boundary, apply one fix by passing stacked tensor `P`, rerun the same A1/A2 upstream-active gate, and halt with the diagnostic. No A7 is licensed until easy A1/A2 active controls recover.


