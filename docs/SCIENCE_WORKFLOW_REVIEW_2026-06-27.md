# Science Workflow Review - 2026-06-27

**Purpose:** post-session workflow failure review after a north-star drift: a
product-preserving bounded-hybrid fallback was framed as an F1-efficient route
even though the operator rejects that route as nullifying the specification
intent. This document is process context, not science evidence.

## Failure Mode

The workflow correctly blocked a weak AnyEdit local-transplant result from
becoming evidence, but then over-corrected into a convenience closure: route the
problem class outside LLM weights. That is not an acceptable F1 closure if the
spec requirement under test is persistent model memory for that class.

The core mistake was treating `can ship a bounded product` as equivalent to
`spec implementability remains viable`. Those are different claims. A fallback
can be valuable engineering mitigation while still leaving F1 OPEN/BLOCKING.

## EVIDENCE-SHOWS

- C10h/C10J results do not falsify official upstream AnyEdit. They diagnose
  local harness/transplant failures and block hard A7 runs from that path.
- The official upstream AnyEdit runner has not yet produced source-faithful
  A1/A2 active-control behavior in this repo environment.
- The current methodology skills are mostly static context/checklists. They
  can remind the main model of gates, but they are not autonomous agents and
  do not reason independently.
- Tooling such as `tools/experiment_gate.py`, `tools/stats.py`,
  `tools/power.py`, `tools/claude_advisor.sh`, MCP tools, and subagents provide
  active behavior. A `SKILL.md` by itself does not.

## I-INFER

The current workflow is good at preventing some false positives, but weak at
creative rescue planning and north-star preservation unless the main agent uses
the skills as reasoning contracts rather than checklist text. The next upgrade
should agentize high-leverage reasoning steps instead of expanding passive
markdown.

## Skills vs Agents

- **Skill:** compact operating instructions, references, and scripts/assets. It
  has no independent agency. It cannot inspect the repo or run tools unless the
  main agent explicitly does so. It should be short and prescriptive.
- **Script/tool:** deterministic active gate. It can read artifacts, compute
  stats, fail closed, and produce machine-checkable output.
- **Advisor/subagent:** separate reasoning pass. It can critique, generate
  hypotheses, or review a design from a distinct lens. Its output is input, not
  evidence.

Therefore: keep skills as concise contracts; use tools for mechanical gates; use
advisor/subagents for genuine adversarial or creative scientific reasoning.

## Workflow Upgrade

1. **North-star contract gate before route recommendations.** Every strategic
   route must name the non-negotiable spec/operator contract. If a route violates
   it, label it `ENGINEERING_ESCAPE_HATCH`, not F1 closure.
2. **No checklist preambles.** Skills must output only artifact-specific deltas:
   decisive evidence, open confounds, allowed/forbidden next actions, and the
   cheapest overturning test.
3. **Agentize creative science steps.** For stuck method-family work, run a
   bounded proposer -> critic -> experiment-designer sequence using Claude or
   subagents. The proposer may suggest rescue routes; the critic tries to kill
   them; the designer writes a prereg only for the surviving cheapest faithful
   test.
4. **Separate product mitigation from spec readiness.** Product fallback,
   deployment mitigation, and F1 implementability must be distinct labels in
   every route decision.
5. **Keep method-port failures scoped.** A local wrapper/transplant failure is
   not method-family evidence unless a source-faithful active easy-control gate
   already passed.
6. **Prefer official/source-faithful attempts before declaring a method route
   exhausted.** For AnyEdit, that means a separate upstream-compatible
   environment/addendum before any claim about official AnyEdit.
7. **Record hypotheses, not just gates.** Failure reflection must leave durable
   hypotheses with `builds-on`, `would-advance`, status, and source; otherwise
   the creative value of the reflection is lost.

## Immediate Consequence For C10 / AnyEdit

If the F1 contract requires LLM-weight persistent memory for project-coined
multi-word semantic values, then bounded hybrid does not close C10. C10 remains
OPEN/BLOCKING. The next valid scientific route is an official-upstream AnyEdit
addendum or another source-faithful method-family attempt, each beginning with
A1/A2 easy controls and per-unit records before any A7 hard case.
