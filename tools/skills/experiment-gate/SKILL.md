---
name: experiment-gate
description: >-
  Use before designing, running, analyzing, promoting, or closing out any
  LLM-as-Database experiment or external method port. Enforces preregistration,
  LAW/inertness checks, saved-result readback, fresh stats on per-unit JSON,
  bias/confound audit, method-port faithfulness, advisor/cross-family review,
  and handoff to closeout_check.py. It never writes CORPUS or chooses the final
  scientific verdict.
license: repo-local
allowed-tools: Bash, Read, Write, Edit
---

# Experiment Gate

Use this as a deliberate workflow layer before evidence-bearing runs and before
calling a result PASS, PARTIAL, FAIL, PROMOTABLE, or ready for CORPUS. The gate
protects the F1 readiness determination from harness artifacts, weak metrics,
and review drift. It is not an evidence authority.


## Supporting Methodology Skills

These repo-local skills are installed for both Codex and Claude by `tools/install_science_methodology_skills.sh` and restored by `tools/restore_pod_tools.sh`:

- `methodology-superpowers`: verification-before-completion, systematic debugging, test-first harness work, review handling.
- `scientific-critical-thinking`: bias/confound/metric/evidence audit.
- `debug-mantra-scrutinize`: reproduce, trace, falsify, one-fix-then-halt, path-level review.
- `premortem-the-fool`: pre-mortem and red-team assumptions before decisions/verdicts.
- `scientific-problem-selection`: choose or reframe F1-moving science arcs with risk, decision tree, adversity planning, and problem inversion.

## Core Rule

Compose with the existing program machinery:

- Preregs live in `docs/<D-ID>_PREREG.md`.
- Results live in `results/`.
- Statistics use `tools/stats.py` and `tools/power.py`.
- Handoff goes to normal CORPUS/tracker closeout and then `python3 tools/closeout_check.py <D-ID>`.
- The gate produces `logs/experiment_gate/*_gate_package.json`; it never writes `CORPUS/*`.

## Phase Order

1. **Pre-register:** falsifiable hypothesis, binding metric, PASS/PARTIAL/FAIL/INVALID thresholds, power/MDE, confound controls, abort criteria, artifact paths, and advisor gate. Read `references/metric-matching.md`, `references/sampling-units.md`, and `references/confounder-checklist.md`.
2. **Run under LAWs:** engine fingerprint, LAW#5 inertness for harness-side methods, source readback, deterministic saved JSON.
3. **Verify runs/stats:** fresh-read the saved result JSON and run stats. Use `python3 tools/experiment_gate.py check-result results/<file>.json`. A stats refusal blocks completion claims.
4. **Bias/method audit:** run every preregistered confound control. For external method ports, read `references/method-port-faithfulness.md` and run `python3 tools/experiment_gate.py audit-method-port <packet.json>`.
5. **Cold review:** advisor-review before harness/test criteria, after stalls/surprises, before approach changes, and before verdict. Council is only for spec-contract/tension framing; see `references/review-routing.md`.
6. **Handoff:** build a gate package with `python3 tools/experiment_gate.py bundle <D-ID> ... --review-status both_done`, then do the normal closeout.

## Hard Stops

- No run without a written prereg.
- No completion claim without a fresh saved-result readback and stats artifact or explicit stats refusal diagnostic.
- No promotion with an open preregistered confounder.
- No hard-case method-port run until source-faithful easy controls pass active behavior.
- No AutoResearch as method-validity evidence; it is fenced candidate search only.

## Commands

```bash
python3 tools/experiment_gate.py init D-EXAMPLE
python3 tools/experiment_gate.py check-prereg docs/D-EXAMPLE_PREREG.md
python3 tools/experiment_gate.py check-result results/example.json
python3 tools/experiment_gate.py audit-method-port logs/example_method_port_packet.json
python3 tools/experiment_gate.py bundle D-EXAMPLE --result results/example.json --review-status both_done
```

Read command output and exit status. A `BLOCKED` package is a stop signal, not a softer warning.
