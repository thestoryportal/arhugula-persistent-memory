---
name: methodology-superpowers
description: >-
  Repo-local extraction of the useful superpowers methodology for this research
  program. Use for verification-before-completion, systematic debugging,
  test-first harness changes, and receiving adversarial code review. This is a
  safe derived checklist, not the upstream auto-injecting framework.
license: repo-local-derived
---

# Methodology Superpowers

Use this when implementing or changing a research harness, debugging a failure,
claiming completion, or receiving review feedback.

## Hard Gates

- **Verification before completion:** do not claim success until a fresh command output and saved artifact readback support it.
- **Systematic debugging:** no fix until the failure is reproduced and the failing boundary is located.
- **Test-first harness changes:** for nontrivial harness logic, define the failing check or invariant before implementation.
- **Receiving review:** treat critique as a technical input; verify the code path and evidence, not the reviewer tone.

## LLM-as-Database Binding

- Prefer `tools/experiment_gate.py` for experiment handoff checks.
- Use `tools/stats.py`/`tools/power.py` for result and design statistics.
- For method ports, require active easy-control behavior before hard cases.
- A process pass is not CORPUS evidence.

## Red Flags

- "Looks good" without command output.
- A fix proposed before the traceback/failing boundary is known.
- A harness change without an inertness/null gate where LAW#5 applies.
- Review handled by agreement instead of a re-run or cited artifact.
