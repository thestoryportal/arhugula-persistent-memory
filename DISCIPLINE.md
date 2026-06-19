# DISCIPLINE.md — North Star · Context Triggers · Tool & Thinking Thresholds

**For BOTH Claude and Codex. Load this every session.** It consolidates the operating disciplines (detail in `EXPERIMENT_RUNBOOK.md` §1–§2 + `memory_mirror/`) and adds the explicit goal, failure-thinking protocol, read-triggers, and min/max thresholds. Where mechanics conflict, runbook §2 is authoritative; this file is the index + the thresholds.

---

## 0. THE ULTIMATE GOAL — the north star (never drift from this)
**Prove — or falsify — that the "LLM-as-Database" spec is implementable *before* it is built**, and deliver the **F1 spec-implementation-readiness determination** ("ready / not-ready, with conditions").
The thesis: a transformer's FFN can serve as a **physically queryable + editable graph database** — knowledge stored **in-weight** (edited via MEMIT), as `.vindex` overlays on a frozen base, queried via LQL, governed (2PC/ledger/validation), and **deployed on CPU**. Spec: `research_and_specs/llm-as-database-v1_2-integrated-spec.md`. **Everything serves F1. Falsification-first: the goal is the TRUTH about buildability, not green checkmarks.**

> **DRIFT CHECK — run before any non-trivial action:** *"Does this advance the F1 readiness determination, or a live falsifier the goal depends on (`EXPERIMENT_RUNBOOK.md` §0.3)? If not — stop and say why."* If you cannot tie the action to F1 or a §0.3 falsifier, you are drifting.

---

## 1. CONTEXT — what to read, and WHEN (triggers)
Read on the trigger; do **not** work from grep excerpts of load-bearing docs ([[read-authoritative-source-fully]]).

| Trigger / situation | Read |
|---|---|
| **Fresh session / re-grounding** | `SESSION_BOOTSTRAP.md` → `README.md` → **`EXPERIMENT_RUNBOOK.md` §0.3** (what's next) → `SESSION_CHECKPOINT.md` (top block) |
| **Before ANY experiment** | runbook §0.3 + that experiment's `CORPUS/NN` doc + pre-register criteria (`docs/G6_G7_PASS_CRITERIA_DRAFT.md`) |
| **Framing a spec contract / "what does the spec require"** | the **FULL relevant spec section** end-to-end (§7–§12) — NOT a grep — + `CORPUS/05` contracts |
| **"What's proven vs open?"** | `CORPUS/00_MASTER_EVIDENCE.md` + `03_STATUS_LEDGER.md` + `docs/HYPOTHESIS_REGISTER_2026-06-18.md` + `docs/EXPERIMENT_REGISTRY.md` |
| **Tracing a claim → artifact** | `docs/EXPERIMENT_REGISTRY.md` + `CORPUS/01_PROVENANCE_MANIFEST.md` + `02_VANDV_CHAIN.md` |
| **"Why did we do X / what happened before"** (historical) | `docs/session_summaries/`, `docs/framework_findings/`, git/`memory_mirror/` |
| **Before relying on an external repo/paper** | verify it first ([[verify-external-artifacts-before-effort]]); logged verdicts in `research_and_specs/external_evidence_notes.md` |
| **Durable learnings / known traps** | `memory_mirror/MEMORY.md` (one fact per file) — read the relevant ones |
| **"Does our OWN corpus/spec/council already cover this?"** | **NotebookLM** (corpus-grounded, operator-run) + the spec + `docs/framework_findings/` |
| **"Are we missing SOTA / a method?" (after a falsification, before a frontier bet)** | **Perplexity / `deep-research`** (open-web) + `research_and_specs/external_evidence_notes.md` |
| **Framing / auditing a spec contract; surfacing domain tensions** | **Framework Council** (`skills/` + `CORPUS/COUNCIL_PROTOCOL.md`) — spec-authoring ONLY, not an evidence source |
| **Repo layout** | `README.md` repo map / `AGENTS.md` layout |

### 1.1 LEARN-AS-YOU-GO — record back (the other half of context; this is how the agents *improve*)
Context is a **read↔write loop**: pull the relevant memory/CORPUS **before**, record results + learnings **after**. Drift and repeated mistakes come from skipping the write side.
- **After EVERY experiment** (the `EXPERIMENT_RUNBOOK.md` §0.4 close-out): write `CORPUS/NN_*.md` → update `00_MASTER_EVIDENCE.md` + `03_STATUS_LEDGER.md` → runbook §0.3/§12/§13 → `SESSION_CHECKPOINT.md` → `EVIDENCE_INDEX.md` + `docs/EXPERIMENT_REGISTRY.md`.
- **Any durable learning or trap** → `memory_mirror/` (one fact per file, frontmatter) + a one-line pointer in `MEMORY.md`; then mirror. Recall these *before* similar work so the same trap isn't re-hit.
- **Any decision** (method/model/tool/scope) → runbook §5 decisions ledger with a `D-<TRACK><n>` ID and the reasoning.
- **External evidence verified** → `research_and_specs/external_evidence_notes.md` (don't re-verify next time).
- Hard rule (network FS): write big canonical docs via shell/python and **re-read to confirm persistence** ([[verify-canonical-state-edits-persist]]).

---

## 2. DEEP-THINKING-ON-FAILURE — the rigor protocol (mandatory on trigger)
**Triggers (ANY of these → run the protocol, do not push past it):**
- an experiment **FAILS / is PARTIAL / returns a surprising or "too-clean" result**;
- you are **stuck / looping / the approach isn't converging**;
- **before declaring any result "conclusive"** or writing it to `CORPUS/`;
- you suspect a **confound or an over-claim**.

**The protocol (rigor + novel, creative-but-GROUNDED, non-hallucinatory ideation):**
1. **Reflect honestly** — what does the result *actually* show? Separate `EVIDENCE-SHOWS` from `I-INFER`.
2. **Enumerate ≥3 hypotheses** for the failure/result — *including* "I am wrong / there is a confound."
3. **Ideate widely but grounded** — surface non-obvious approaches; question the problem framing itself; reach past our own data when warranted (§3). **No hallucination:** every idea must be checkable, and every external artifact/claim verified *before* effort.
4. **De-confound** — design the *cheapest* test that could **overturn** your own finding; run controls before believing it.
5. **`advisor()`** — mandatory **before authoring the new test set** and **before re-declaring done**.
6. **Pre-register** the pass/fail criteria **before** the confirming run.
7. **WRITE the surfaced hypotheses (the deep-thinking yield is context — record it).** Every hypothesis from step 2/3 goes durably into the living hypothesis register (`docs/HYPOTHESIS_REGISTER_*.md`) with its **additive framing**: `builds-on` (which PROVEN node — `PROGRESS.md` ①), `would-advance` (which F1 gap/chain), `status` (OPEN/TESTING/PROMOTED/KILLED/PARTIAL), and `source` (this §2 pass / advisor / autoresearch / Perplexity). **A hypothesis not written did not happen** (the §1.1 read↔write rule — hypotheses are pulled *back* before choosing the next move; see §1 "what's proven vs open"). On test, **promote** it into `PROGRESS.md` ① or **kill** it into ④ with the Decision-ID. This is how a failure's most valuable output (a new direction) survives the session instead of evaporating.

**Non-hallucination rules (always):** cite an artifact or label `UNVERIFIABLE`; mechanics ≠ contract; design-viability ≠ empirical evidence; verify external repos/IDs/claims before building on them; reserve confidence for runs that can fail.

---

## 3. TOOL & THINKING THRESHOLDS — when to invoke, and min/max bounds
"MIN" = when you **must** use it. "MAX/BOUND" = stop over-using (diminishing returns / Goodhart).

| Tool / loop | MIN — invoke when | MAX / BOUND |
|---|---|---|
| **`advisor()` (Claude) · `advisor-review` skill (Codex)** | before authoring any test/criteria set or new harness; before committing to an interpretation/approach; when stuck; before declaring done. **≥1 per multi-step experiment.** | **Claude:** `advisor()` (auto-sees the transcript). **Codex:** the `advisor-review` skill — `codex review -m <stronger-model>` for code/diffs (needs `git init`) or `codex exec -m <stronger-model>` for reasoning/findings, FED the finding + evidence + `tools/advisor_review_prompt.md`. **Use a different/stronger model = real independence.** Input, not authority — evidence binds; reconcile conflicts in one more pass; don't re-review unchanged state. ([[review-diminishing-returns-evidence-is-binding]]) |
| **Deep-thinking-on-failure (§2)** | **1 full pass on every** failure / stall / surprise / pre-"conclusive". | **≤3 reflection passes**, then either **RUN a falsifier or call `advisor()`** — do not theorize indefinitely. If the next experiment is cheap + runnable, **run it instead of a 4th pass** ([[evidence-over-scaffolding]]). |
| **Framework Council** (`skills/`) | spec-authoring / framing contracts / surfacing domain tensions **only**. | **NEVER to "confirm" our own evidence** (same-model = weak independence / confirmation-amplification, runbook §2.5). ≤1 panel per decision; don't re-convene to rubber-stamp. Use `CORPUS/COUNCIL_PROTOCOL.md`. |
| **autoresearch** (`~/.codex/skills/autoresearch-skill`) | **only** a SEARCH/optimization sub-problem with an **honest metric + guard + frozen held-out** (config/hparam sweeps, e.g. `experiments/track_c/autoresearch_band_search/`). | **NEVER for falsification** (it's an optimizer → Goodhart). `max_iterations` ≤ 12 in `research.md`; a winner is a **lead** to re-verify with pre-registered criteria + inertness gate + `advisor()`. **Never write a loop winner into `CORPUS/`.** |
| **Perplexity** (open-web) | "what's the field's SOTA / are we missing a method?" — **after a falsification** or **before a frontier bet**. | Don't use for in-repo facts (use the corpus). Bounded query budget — synthesize, don't endlessly browse. |
| **NotebookLM** (our corpus) | "does our **own** corpus/spec/council already cover this?" — corpus-grounded mining. | Operator-run / auth-gated; answers only from corpus, cites sources, flags absence. |
| **Subagent fan-out (parallel/series)** | coverage needs decomposition — triage, **adversarial verification panel**, parallel de-confounding, propose→verify→synthesize. See `AGENTS.md` → *Multi-agent / subagent patterns*. | **GPU serializes** (fan out analysis, queue compute — one 4090). Same-model panels = weak independence → prompt to **refute**, distinct lenses; evidence stays binding. **Role separation:** proposer (autoresearch) ≠ documenter (`CORPUS/`). Bound the fan-out; stop at marginal-info ≈ 0. |

### 3.1 AUTONOMOUS (no-HIL) RUNS — extra bounds (`AUTONOMY.md`, `tools/autonomy_driver.py`)
When running unattended, **all of §0–§3 still bind**, plus:
- **Hard wall-clock** (`--budget-min`) is a real deadline; **preflight** (`codex_context_guard preflight`) hard-gates before any run. NOT-READY → abort.
- **Pre-registered deterministic labels only** — PASS/PARTIAL/FAIL/INVALID from a fixed rule on the result JSON (no model judgment). `FAIL` = tested-and-negative = a **real result**; `INVALID` = couldn't evaluate / guard failed = **not** a result. Thresholds are frozen **before** launch; changing them after seeing results voids pre-registration.
- **Per-unit loop bound** (`max_loops`) — a retry only fixes a *transient* failure; never loop to chase a different label on a deterministic run.
- **Point at a FALSIFIER, not the optimizer.** A `fenced:true` unit (autoresearch/sweep) may **log candidates only** — a fenced PASS is a *lead*, never a conclusion, never written to `CORPUS/`.
- **STAGING, not canonical.** Unattended findings → `logs/pending_findings/NN_<unit>.md` with an obligation block. The driver/agent must **NOT** author `CORPUS/*` or edit the ledger/runbook/checkpoint; the operator folds them in on supervised review (§0.4).
- **Standing-auth** (model pulls / cov-compute / disk) PRE-APPROVED + logged; **paid-provider + credentials GATED** → `logs/autonomy_gates.jsonl`, skipped, never block the whole run.
- **Self-review ≠ advisor-review.** Unattended "review" by the run model is a self-consistency check; real independence needs a **different model** (`codex exec -m <other>`) and must not raise confidence on its own.

---

## 4. How this binds
- **Claude** loads this via `CLAUDE.md`; **Codex** via `AGENTS.md`. Both must honor §0 (goal), §2 (failure-thinking), §3 (thresholds).
- This does **not** replace the LAWs (engine fingerprint, LAW#5 inertness, one-fix-then-halt, read-source-before-authoring — runbook §2.4) or the living-document protocol (§0.4). It sits **above** them as the always-in-context index.
- On any conflict: the **goal (§0)** wins over local optimization; **evidence** wins over advisor/council/loop output; **pre-registered criteria** win over a moving metric.
