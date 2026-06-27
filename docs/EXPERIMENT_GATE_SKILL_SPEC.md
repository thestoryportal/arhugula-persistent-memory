# Experiment Gate — Phase-1 Skill Spec (Implemented)

_A repo-local Claude skill that fuses the three disconnected clusters InfraNodus surfaced (discipline/verification · measurement/stats · bias-audit) into ONE gated chain: **pre-register → run-under-LAWs → verify-runs-stats → bias-audit → cross-family review**. Drafted 2026-06-23 from the external-skill audit (`EXTERNAL_SKILL_REPOS_AUDIT.md §11`) + the InfraNodus gap synthesis. **IMPLEMENTED 2026-06-27.** See `tools/experiment_gate.py` and `tools/skills/experiment-gate/`._

> **Provenance / license.** Authored in-repo. It *reuses the program's own disciplines* and standard methods (power analysis, cluster bootstrap, GRADE-style risk-of-bias) — **no text is lifted from the audited third-party skills** (K-Dense per-skill licenses are mixed; 9arm/awesome-list have none). The named skills (superpowers `verification-before-completion`, K-Dense `experimental-design`/`statistical-power`, `scientific-critical-thinking`, `the-fool`/`scrutinize`) are the *inspiration*, not the source.

---

## Implementation status — 2026-06-27

Implemented as a repo-local workflow layer, not a parallel evidence authority:

- `tools/experiment_gate.py` provides `init`, `check-prereg`, `check-result`, `audit-method-port`, and `bundle`.
- `tools/skills/experiment-gate/SKILL.md` is the concise agent-facing workflow.
- `tools/skills/experiment-gate/references/` carries the metric, sampling, confound, method-port, debugging, verification, and review-routing checklists.
- `check-result` fresh-reads saved JSON and writes stats reports under `logs/experiment_gate/`; aggregate-only results are blocked for completion claims.
- `bundle` never writes `CORPUS/*`; it blocks handoff unless prereg/result/method-port checks pass and review status is explicit.

## 0. The one design constraint that governs everything

⚠ **COMPOSE, DO NOT DUPLICATE.** The repo already has pre-registration (`EXPERIMENT_RUNBOOK §0.3` falsifiable criteria), a close-out gate (`closeout_check.py`), the engine LAWs (`CLAUDE.md`), the CORPUS evidence ledger, and the advisor+codex independence discipline. Both the advisor and Codex flagged that adding a parallel state/planning system (à la `actionize`/`task-master`) is a **net hazard**. So this skill is a **thin orchestrator + a runnable stats library** that sits *between* "design an experiment" and "write the CORPUS entry." It **never** writes CORPUS, picks the final promotion verdict, or replaces `closeout_check`. It produces an **evidence package**; the human + `closeout_check` + advisor remain the authorities.

Two corollaries:
- **Runnable code, not a persona.** Per the reconciled adoption lead, Phase 2/3 *execute statistics on the saved result JSON*; the skill is worthless if it just "reminds you to test significance."
- **Fence.** A gate `PASS` is a *review starting point*, not CORPUS evidence ([[pass-label-not-equal-promotable-claim]]). The gate enforces discipline and computes numbers; promotion still goes through the normal close-out.

---

## 1. The chain — 5 phases, each an Iron-Law gate

| # | Phase | What it does | **Iron Law** | Script / ref | Encodes (memory) |
|---|-------|--------------|--------------|--------------|------------------|
| 0 | **PRE-REGISTER** | State the falsifiable hypothesis + the metric matching the claim; compute power/MDE for the planned design; list candidate confounders + their controls; write PASS/PARTIAL/FAIL/INVALID thresholds. `advisor()` before authoring the test set. | **NO RUN WITHOUT A WRITTEN PRE-REGISTRATION** (criteria + power + confounder controls). | `power.py`, `metric-matching.md`, `confounder-checklist.md` | [[match-metric-to-the-claim]] · [[prototype-tautology-trap]] |
| 1 | **RUN (under the LAWs)** | Engine fingerprint gate (SHA + `grep -c _cov_cpu == 3`); LAW#5 inertness for any harness method; read-source-before-authoring; save result JSON deterministically. | **NO RESULT WITHOUT A FINGERPRINT-VERIFIED ENGINE + A SAVED RESULT JSON.** | (uses existing preflight) | `CLAUDE.md` LAWs |
| 2 | **VERIFY-RUNS-STATS** ⭐ | Run the *pre-registered* statistics on the saved JSON: paired within-unit diff, cluster-bootstrap CIs over (held-out × order), JS/KL with CIs, top-1 McNemar/Fisher. Compare to the pre-registered thresholds → propose a deterministic label. | **NO COMPLETION CLAIM WITHOUT A FRESH STATS COMPUTATION ON THE SAVED JSON** ("skip a step = lying"). | `stats.py`, `sampling-units.md` | [[clustered-editing-trials-sampling-unit]] · [[sequential-edit-run-nondeterminism]] |
| 3 | **BIAS-AUDIT** | Run each pre-registered confounder control; mark CONTROLLED / OPEN. Any OPEN confounder caps the label at CONFOUNDED/PARTIAL. | **NO PROMOTION WITH AN UNCONTROLLED PRE-REGISTERED CONFOUNDER.** | `audit.py`, `confounder-checklist.md` | [[bias-ablation-causal-attribution]] · [[pass-label-not-equal-promotable-claim]] |
| 4 | **COLD-REVIEW** | `advisor()` (in-family) **+** `codex exec -m gpt-5.5` (out-of-family) on the result + stats + bias-audit. Explicitly check: did same-model self-review inflate the verdict? Cheapest overturning test? | **NO PROMOTABLE CLAIM WITHOUT INDEPENDENT CROSS-FAMILY REVIEW.** | (uses `tools/setup_codex.sh`) | [[review-diminishing-returns-evidence-is-binding]] |
| 5 | **HANDOFF** | Emit the pre-reg + stats report + bias-audit + review verdict as the inputs to the **existing** close-out: write `CORPUS/NN` → run `closeout_check.py <D-ID>` until ✅ ALL GREEN. The gate stops here. | **THE GATE DOES NOT WRITE CORPUS OR PICK THE FINAL VERDICT.** | (hands to `closeout_check.py`) | [[closeout-gate-before-done]] |

The three gaps InfraNodus found map exactly to the three fusions: **Gap 1** (Test/Debugging ↔ Statistical-Significance) = Phase 2 (verification that *runs* the stats). **Gap 2** (Experiment-Refinement ↔ Bias-Audit) = Phase 3 gating any arbor-style candidate. **Gap 3** (Power ↔ Bias-Audit) = Phase 0 fusing power + confounder pre-registration.

---

## 2. Proposed `SKILL.md` (verbatim)

```markdown
---
name: experiment-gate
description: >-
  Use before running, analyzing, or closing out ANY LLM-as-Database experiment
  (knowledge-editing, eval, or spec-validation run). Enforces the chain
  pre-register -> run-under-LAWs -> verify-runs-stats -> bias-audit -> cross-family
  review, so no result can be called PASS or PROMOTABLE without fresh statistics
  computed on the saved result JSON, every pre-registered confounder controlled,
  and independent out-of-family review. Trigger on "design/pre-register an
  experiment", "is this result significant", "can I promote this result",
  "close out <D-ID>", before writing a CORPUS entry, or before claiming an
  edit/eval result holds. Does NOT replace EXPERIMENT_RUNBOOK, closeout_check.py,
  the engine LAWs, or CORPUS — it orchestrates them and computes the statistics.
license: repo-local
allowed-tools: Bash, Read, Write, Edit
---

# Experiment Gate

Run an LLM-as-Database experiment through five gates. Each gate has an Iron Law:
if you cannot satisfy it, you STOP — you do not soften it.

## When to use
Any time a result is about to be called PASS / PARTIAL / PROMOTABLE, or before a
CORPUS entry is written. Also at experiment *design* time (Phase 0 only).

## When NOT to use
Pure exploration / scoping with no result claim; mechanical edits; conversational
turns. The gate is for *evidence-bearing* runs.

## Phase 0 — PRE-REGISTER  (Iron Law: NO RUN WITHOUT A WRITTEN PRE-REGISTRATION)
1. Write the falsifiable hypothesis and the PASS/PARTIAL/FAIL/INVALID thresholds.
2. Pick the metric that MATCHES the claim (references/metric-matching.md):
   top-1 for read-correctness; JS/KL for distributional. Mismatched metric = STOP.
3. Power/MDE: run `scripts/power.py` with the sampling-unit structure
   (held-out-set x edit-order) and the expected within-unit noise. If the planned
   design cannot detect the claimed effect at the target power, REDESIGN — do not run.
4. Confounders: from references/confounder-checklist.md, list the candidates that
   apply and the control for each. An unlisted-but-applicable confounder = STOP.
5. Call advisor() before authoring the test set (RUNBOOK 2.1).
Write all of this to docs/<D-ID>_PREREG.md BEFORE any run.

## Phase 1 — RUN UNDER THE LAWS  (Iron Law: NO RESULT WITHOUT A VERIFIED ENGINE + SAVED JSON)
Verify the engine fingerprint (SHA matches; `grep -c _cov_cpu` == 3 where required).
Prove LAW#5 inertness for any harness-side method (lambda=0 reproduces baseline,
|delta| ~ 0). Read source before authoring. Save the result JSON deterministically.

## Phase 2 — VERIFY-RUNS-STATS  (Iron Law: NO COMPLETION CLAIM WITHOUT FRESH STATS ON THE SAVED JSON)
Run `scripts/stats.py <result.json> --prereg docs/<D-ID>_PREREG.md`. It computes
the PRE-REGISTERED statistics — paired within-unit diff, cluster-bootstrap CIs over
(held-out x order), JS/KL with CIs, top-1 McNemar/Fisher — and compares them to the
pre-registered thresholds, proposing a deterministic label. Read the FULL output and
the exit code. A claim of "passing" without this command's fresh output is a lie.

## Phase 3 — BIAS-AUDIT  (Iron Law: NO PROMOTION WITH AN UNCONTROLLED PRE-REGISTERED CONFOUNDER)
Run `scripts/audit.py <result.json> --prereg docs/<D-ID>_PREREG.md`. It executes each
pre-registered confounder control (margin inflation, under-editing-vs-redistribution,
denominator/survivorship, K-vs-C, pre-state conditioning). Any OPEN confounder caps
the label at CONFOUNDED / PARTIAL — never PASS.

## Phase 4 — COLD-REVIEW  (Iron Law: NO PROMOTABLE CLAIM WITHOUT CROSS-FAMILY REVIEW)
advisor() AND codex (gpt-5.5, via tools/setup_codex.sh) review the result + stats +
bias-audit. Ask explicitly: did same-model self-review inflate the verdict? What is
the cheapest test that would OVERTURN this? A passing self-review is not evidence.

## Phase 5 — HANDOFF  (Iron Law: THE GATE DOES NOT WRITE CORPUS OR PICK THE FINAL VERDICT)
Bundle the pre-reg + stats report + bias-audit + review verdict and hand them to the
EXISTING close-out: write CORPUS/NN, then run `python3 tools/closeout_check.py <D-ID>`
until ALL GREEN. The human + the close-out gate decide promotion. The gate stops here.

## Red Flags (rationalization stoppers)
- "The number looks good" without stats.py -> Phase 2 not done.
- "It's obviously fine" -> name the confounder you're skipping (Phase 3).
- "I already reviewed it" -> same-model self-review is confirmation amplification.
- "Just this once, skip pre-registration" -> that is the prototype-tautology trap.
```

---

## 3. Directory layout (repo-local)

```
tools/skills/experiment-gate/          # repo-local (gitignored install into ~/.claude/skills on demand)
├── SKILL.md                           # §2 above
├── references/
│   ├── metric-matching.md             # top-1 vs JS/KL; the asymmetric-metric trap; per-claim metric table
│   ├── sampling-units.md              # unit = (held-out-set × edit-order); cluster-bootstrap; why iid/Wilson invalid
│   └── confounder-checklist.md        # the program's recurring confounds + the control + the CORPUS precedent
└── scripts/
    ├── power.py                       # MDE / power / required #seeds×orderings (simulation-based)
    ├── stats.py                       # the Phase-2 statistics engine
    └── audit.py                       # the Phase-3 confounder runner
```
Install path mirrors the InfraNodus-skills pattern: master in `tools/skills/`, installed to `~/.claude/skills/experiment-gate/` by an installer, re-installed by `restore_pod_tools.sh`. (Repo-local → no license/exfil/trigger-collision risk from third-party skills.)

---

## 4. Bundled scripts — interface specs (to implement on approval)

**`power.py`** — *can the planned design even detect the claimed effect?*
- **In:** `--effect <claimed pp or "MDE">`, `--alpha 0.05 --power 0.8`, `--seeds N --orders M`, `--within-noise <pp>` (default ~50pp from [[sequential-edit-run-nondeterminism]]), `--metric {top1|js|kl}`.
- **Does:** simulation-based power (closed-form fails for order-dominated clustered units) → required `seeds×orders`, or the MDE for a given budget.
- **Out:** power table + GO/REDESIGN. Guards against the C2-band "single-seed/underpowered" trap.

**`stats.py`** — *the Phase-2 engine (the Gap-1 fusion).*
- **In:** `<result.json>` (pre+post or two arms), `--prereg <PREREG.md>` (metric + thresholds + unit spec).
- **Does:** paired within-unit diff (cancels shared bias — A2b/Ext3); **cluster-bootstrap** CI over (held-out × order), *not* iid/Wilson; JS/KL with bootstrap CIs; top-1 success + McNemar/Fisher exact; compares to pre-registered thresholds → proposes `PASS|PARTIAL|FAIL|INVALID`; flags if the computed metric doesn't match the claim.
- **Out:** `<D-ID>_stats.json` + a human summary + the label proposal + exit code.

**`audit.py`** — *the Phase-3 confounder runner (the Gap-2/3 fusion).*
- **In:** `<result.json>`, `--prereg <PREREG.md>`.
- **Does:** runs each pre-registered control — **margin inflation** (compute_z median edited vs native, B3), **under-editing vs redistribution** (within-loc direction + expression-rate floor, C2-band/E1), **denominator/survivorship** (N edited vs attempted), **K-vs-C** (chunk count vs size, D20), **pre-state conditioning** (was the eval pool pre-screened to confident-correct? G6.1).
- **Out:** per-confounder `CONTROLLED|OPEN` + the label cap (any OPEN pre-registered confounder → ≤ CONFOUNDED/PARTIAL).

---

## 5. Reference files — outlines
- **`metric-matching.md`** — the per-claim metric table (read-correctness→top-1; distributional→JS/KL/KL-with-CI; durability→retention), the asymmetric-metric trap, "never judge two sides of a comparison on different metrics."
- **`sampling-units.md`** — the unit is `(held-out-set × edit-order)`; iid/Wilson invalid for clustered/order-dominated units; cluster-bootstrap recipe; ≥2 held-out seeds; ship the conservative last-all-clean ceiling, not a fitted point.
- **`confounder-checklist.md`** — one row per recurring confound with: name · how it fakes a PASS · the control · the CORPUS precedent (E1 bias-ablation, C2-band redistribution, B3 margin, D20 K-vs-C, G6.1 pre-screen).

---

## 6. How it plugs into the existing workflow (what it owns vs what it doesn't)

```
 design ──▶ [Phase 0 PRE-REGISTER] ──▶ [Phase 1 RUN under LAWs] ──▶ [Phase 2 stats.py]
                                                                          │
            EXISTING machinery (gate hands off, does NOT replace):        ▼
   CORPUS/NN  ◀──── [Phase 5 HANDOFF] ◀── [Phase 4 advisor+codex] ◀── [Phase 3 audit.py]
        │
        ▼
   closeout_check.py <D-ID>  →  ✅ ALL GREEN   (the human + gate decide promotion)
```
- **The gate OWNS:** enforcing the order, running the stats/audit, requiring cross-family review.
- **The gate does NOT own:** the falsifiable-criteria *content* (yours), the engine LAWs (CLAUDE.md), CORPUS prose, the close-out gate, the promotion verdict. No parallel state store — pre-reg lives in `docs/<D-ID>_PREREG.md`, results in `results/`, exactly where they already live.

---

## 7. Historical open questions (resolved by 2026-06-27 implementation)
1. **Install location** — `tools/skills/` master + installer (consistent with InfraNodus skills), or just keep it as `tools/*.py` scripts + a `docs/` checklist and *not* a Claude skill at all? (A non-skill version dodges trigger-collision entirely; a skill version auto-fires the discipline. The audit's lesson leans "scripts + checklist, invoked deliberately" over an auto-injecting skill.)
2. **`stats.py` scope** — start with the metrics you actually use today (top-1 paired, cluster-bootstrap, JS/KL), or build the fuller battery now? (Recommend: start minimal, on a real `results/*.json`.)
3. **Label authority** — does `stats.py`'s proposed label feed the autonomy driver's deterministic-rule slot, or stay advisory to the human? (Recommend: advisory; the driver already has its own pre-registered rule.)
4. **Does this earn its complexity** vs just adding `power.py`/`stats.py`/`audit.py` as three plain tools you call by hand? (The InfraNodus finding says the *integration* is the value — but verify that against the "don't add a framework" caveat.)

---

_Document type: process/reference (no experiment D-ID; not subject to `closeout_check`). Drafted 2026-06-23; implemented 2026-06-27 in `tools/experiment_gate.py` and `tools/skills/experiment-gate/`._
