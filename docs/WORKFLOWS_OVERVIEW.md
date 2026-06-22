# Workflows Overview — Main Loop & Self-Improvement Loop

_A structural map of how work flows through this repo: the supervised **main workflow** (falsification-first experiment cycle), the unattended **self-improvement loop** (autonomous autoresearch, deliberately fenced), and the supporting infrastructure that both depend on (gates, the anti-drift system, tool registration, durability)._

> **Scope & drift discipline.** This document describes **stable workflow structure**, not program state. It deliberately carries **no experiment numbers or "current frontier"** — that content drifts and lives in generated/canonical sources. For *what's next* and *what's proven*, read the generated block in `EXPERIMENT_RUNBOOK.md §0.3` (← `docs/program_state.json`), `SESSION_CHECKPOINT.md`, and `CORPUS/`. This file follows the **de-dup norm** (`DISCIPLINE.md §0.4`): pointers, not copies.

**Canonical sources this doc points to (read these for the binding detail):**
| Source | What it governs |
|---|---|
| `EXPERIMENT_RUNBOOK.md` `§0` | Entry point, current position (§0.3), living-document protocol (§0.4), disciplines (§2), decision tree (§8) |
| `DISCIPLINE.md` | The always-in-context index: de-dup norm, close-out gate, tracker set |
| `CLAUDE.md` | Engine LAWs (fingerprint gate, inertness, one-fix-then-halt) + close-out gate |
| `AUTONOMY.md` | The unattended driver contract (the self-improvement loop's execution harness) |
| `docs/SPEC_E2E_GROUND_TRUTH.md` | The whole-system map work must be situated on |

---

## North Star (never drifts)

**F1 — prove or falsify that the "LLM-as-Database" spec is implementable, and deliver a ready / not-ready-with-conditions determination.** Falsification-first. A clean **FAIL** on a pre-registered falsifier is a **success** for the run, not a setback. Optimizer-style "make the number go up" is explicitly **not** the goal.

---

## 1. The Main Workflow — Falsification-First Experiment Cycle

The supervised, human-in-the-loop research loop. One pass = one experiment, from "what's next" to a durably-recorded, gate-green result.

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │  0. RE-GROUND ──▶ 1. PICK FALSIFIER ──▶ 2. PRE-FLIGHT GATES               │
 │       (§0.1–0.2)        (§0.3)              (engine SHA, _cov_cpu, pod)    │
 │                                                  │                        │
 │  3. advisor() + PRE-REGISTER pass/fail ◀─────────┘                        │
 │       (§2.1, §2.3 — design a run that CAN fail)                           │
 │            │                                                              │
 │            ▼                                                              │
 │  4. AUTHOR/PATCH harness under LAWs ──▶ 5. RUN ──▶ 6. EVALUATE vs rule    │
 │       (§2.4: read-source, LAW#5 inertness)        (metric matches claim)  │
 │                                                       │                   │
 │  7. INDEPENDENT REVIEW (advisor + cross-family) ◀─────┘                   │
 │       (§2.5 — same-model self-review ≠ independence)                      │
 │            │                                                              │
 │            ▼                                                              │
 │  8. RESOLVE FORK ──▶ 9. CLOSE OUT to ALL trackers ──▶ 10. GATE (✅GREEN)  │
 │     (PASS→/PARTIAL→/FAIL→)   (§0.4 chain)        closeout_check.py <D-ID>  │
 │                                                       │                   │
 │  11. COMMIT (pre-commit hook) ──▶ 12. WRITE LEARNINGS ──▶ loop to 1       │
 └─────────────────────────────────────────────────────────────────────────┘
```

### Step-by-step

| # | Step | Where it's defined | Key rule |
|---|------|--------------------|----------|
| **0** | **Re-ground / enter the discipline** — embody the role, then read `SPEC_E2E_GROUND_TRUTH.md` → `§0.3` → relevant Track `§8` → cited KB entries | `§0.1`, `§0.2` | *Situate the work on the e2e map — which cell? Never act from the prompt alone.* |
| **1** | **Pick the next falsifier** | `§0.3` (generated) | `§0.3` "Next actions" is the **single source of what's next**. |
| **2** | **Pre-flight hard gates** | `§3.2`, LAWs `§2.4` | Engine fingerprint SHA == expected; `grep -c _cov_cpu == 3`; pod readiness; disk. **SHA mismatch → HALT.** Engine, LARQL, git stay **UNMODIFIED**. |
| **3** | **`advisor()` + pre-register criteria** | `§2.1`, `§2.3` | Call advisor *before* substantive work. Write **PASS / PARTIAL / FAIL / INVALID** before the run. Design an experiment that can fail; disjoint pools (anti-tautology). |
| **4** | **Author/patch the harness** | `§2.4` | Read source before authoring. Harness-side methods need a **LAW#5 inertness proof** (e.g. `LAMBDA=0` reproduces baseline bit-exactly, \|Δ\|≈0). One-fix-then-halt. |
| **5** | **Run** the experiment | Track A–F decision tree `§8` | — |
| **6** | **Evaluate against the pre-registered rule** | `§2.3`, `§7.4` | Metric must match the claim (top-1 for read-correctness, JS/KL for distributional). `EVIDENCE-SHOWS` vs `I-INFER`; quantify; log reversals honestly. |
| **7** | **Independent review** | `§2.5` | `advisor()` **+ a different-family model** (Codex `gpt-5.5`). Same-model self-review does **not** raise confidence. |
| **8** | **Resolve the fork** | `§0.4` | Each experiment ends `PASS→ / PARTIAL→ / FAIL→` next-experiment-ID. Data selects the branch; if ambiguous, `advisor()`. |
| **9** | **Close out to the full canonical-tracker set** | `§0.4`, `DISCIPLINE.md §0.4` | `CORPUS/NN` (the **one** detailed source) → `docs/program_state.json` + `render_state.py --write` → `CORPUS/00`–`03` → runbook `§12`+`§13` (+`§5` Decision-ID) → `HYPOTHESIS_REGISTER` → `EVIDENCE_INDEX` → `EXPERIMENT_REGISTRY` → spec overlay → memory + `memory_mirror/`. **Pointers, not copies.** |
| **10** | **Binding close-out gate** | `CLAUDE.md`, `DISCIPLINE.md §1.1` | `python3 tools/closeout_check.py <D-ID>` until **✅ ALL GREEN** (presence of D-ID + currency fingerprint `<D-ID>@<hash>`). **Not done until green.** |
| **11** | **Commit** | `tools/git_hooks/pre-commit` | Hook re-checks stale generated blocks + stale fingerprints + **secret scan**; blocks on any. Escape: `git commit --no-verify`. |
| **12** | **Write learnings to memory**, loop to Step 1 | `§2.7` | A result that isn't durably written *did not happen*. |

---

## 2. The Self-Improvement Loop — Autonomous Autoresearch (Fenced)

The unattended loop that **generates and tests its own leads**. It is **opt-in and operator-launched** — nothing here runs on its own — and it is **subordinate to the main workflow by design**: it surfaces *candidates*, never *conclusions*. Two layers + two supporting self-correcting loops.

### Layer A — the autonomy driver (`tools/autonomy_driver.py`, `AUTONOMY.md`)

A thin **deterministic guardrail loop** — "not a scientist." Python never fakes reasoning.

| # | Step | Guarantee |
|---|------|-----------|
| 1 | **Launch** detached with a **mission** (one pre-registered falsifier from `§0.3`) + `--budget-min` | Hard wall-clock deadline; run cannot exceed it. |
| 2 | **Preflight hard-gate** (`tools/codex_context_guard.py preflight`) | Aborts **before any experiment** if the pod is NOT-READY. |
| 3 | **Per-unit loop**, bounded by `max_loops` + `timeout_s` | A retry only ever chases a *transient* failure — never a different label on a deterministic run. |
| 4 | **Deterministic labeling** — PASS / PARTIAL / FAIL / INVALID from a **pre-registered rule** on the result JSON | **No model judgment.** `FAIL` = real negative result; `INVALID` = couldn't evaluate / guard failed = confounded. |
| 5 | **Gate log** | Model-pull/cov-compute = pre-approved (standing-auth); paid-provider/credential moves = **gated + skipped** → `logs/autonomy_gates.jsonl`. |
| 6 | **Close out to STAGING only** → `logs/pending_findings/NN_<unit>.md` + an *obligation block* | The driver **NEVER** writes `CORPUS/`, the ledger, the runbook, or the checkpoint. |
| 7 | **(`--mode agent`)** shells `codex exec -m <other-model>` per unit | A *different* model fulfils deep-think / autoresearch / advisor obligations within the bounds (independence). |
| 8 | **Supervised fold-in** (next morning) | Re-enters the **main workflow at Steps 7–11** — reproduce numbers → cross-model review → promote to canonical (gated by `closeout_check`). |

### Layer B — the autoresearch optimizer (`tools/autoresearch-skill/`)

The literal "improve a metric" engine. Loop body:

```
read research.md ─▶ propose hypotheses ─▶ run ─▶ keep improvements / discard failures ─▶ iterate to target metric
```

**The fence is the point** (binding):
- It is an **optimizer** → Goodhart-prone → the *opposite* of falsification.
- It **PROPOSES leads, never CONCLUSIONS.**
- **Not auto-surfaced, not a registered skill** — manual invocation only.
- A loop "win" is a **candidate** → route to the hypothesis register → **prove or kill it with a pre-registered falsifier** under the main workflow's `§0.4` close-out.
- It may **never** write `CORPUS/` or promote a verdict. A "fenced" unit's PASS = "candidate worth a falsifier," never a result.

### Supporting self-*correcting* loops (improve the system, not the science)

- **Anti-drift integrity loop** — edit `docs/program_state.json` → `tools/render_state.py --write` regenerates the `<!-- GENERATED -->` status blocks everywhere; narrative result-refs are content-**fingerprinted** by `tools/closeout_check.py`; the **pre-commit hook** blocks any stale or secret-leaking commit. The knowledge base keeps *itself* consistent. (Honest scope: auto-*enforces* currency + auto-*updates* generated content; it cannot auto-write narrative prose, and guards only **registered** edges — so de-dup/pointers remain the primary defense.)
- **Learning-to-gate loop** — every correction/reversal → a memory note (`§2.7`); recurring discipline gets **encoded as a mechanical gate**. Examples: the **close-out gate** was born from a silent tracker lapse; the **secret-scan gate** from a `storage_state.json` leak on the public repo. The process hardens itself over iterations.

---

## 3. How the two loops relate

```
   SELF-IMPROVEMENT LOOP  (cheap, unattended, fenced)
        autoresearch optimizer ──▶ candidate/lead
        autonomy driver       ──▶ staged finding + obligation block
                                        │
                                        ▼  (supervised fold-in)
   MAIN WORKFLOW  (authoritative)
        pre-register ─▶ falsify ─▶ independent review ─▶ close-out gate ─▶ canonical record
```

The self-improvement loop is a **feeder**, fenced **below** the main workflow. It cheaply surfaces candidates; the main workflow's pre-registration + falsification + independent review + close-out gate decide what becomes **evidence**. **Falsification always outranks optimization.**

---

## 4. Supporting Infrastructure (both loops depend on this)

### 4.1 The Engine LAWs (`CLAUDE.md`, runbook `§2.4`)
1. **Engine fingerprint gate** — verify MEMIT source SHA-256 before any dispatch; **mismatch → HALT**.
2. **LAW#5 inertness** — any harness-side method must prove it reproduces the baseline bit-exactly when disabled.
3. **One-fix-then-halt.**
4. **Read source before authoring.**
5. The **MEMIT engine, LARQL, and git stay UNMODIFIED** — workarounds are config / our-own-code only.

### 4.2 The close-out gate (`tools/closeout_check.py`)
Two layers: **PRESENCE** (D-ID in every required tracker) + **CURRENCY** (a content fingerprint `<D-ID>@<hash>` of the canonical source span in every tracker — catches docs frozen at a superseded result). On every **refinement** the hash changes → trackers go STALE until re-propagated (`--fp <D-ID>` prints the token to embed). Mechanical — **not the operator's job to verify.**

### 4.3 Hooks (`tools/git_hooks/`, via `core.hooksPath`)
- **`pre-commit` (ACTIVE)** — blocks the commit on: (1) stale generated blocks (`render_state.py --check`); (2) stale registered fingerprints (`closeout_check.py --audit`); (3) **secrets** in staged changes (credential filenames + token/key value signatures). Escape: `--no-verify`.
- **`post-commit` (DISABLED)** — a former auto-`git push` hook, intentionally a no-op (auto-push bypasses the permission deny-list).
- No Claude Code (`settings.json`) lifecycle hooks are configured; the `settings.json` **permissions deny-list** is the agent-side guardrail.

### 4.4 Research-tool registration (advisory inputs — fenced out of the evidence path)
Three external research aids feed the **hypothesis register only**, never `CORPUS/` evidence:

| Tool | Registration plane | Invocation |
|---|---|---|
| **Perplexity** | MCP server in `~/.claude.json` → `projects["/root"].mcpServers` (project scope) | `mcp__perplexity__*` tools (load schema via ToolSearch) |
| **InfraNodus** | MCP server in `~/.claude.json` → root `mcpServers` (global scope) | `mcp__infranodus__*` tools |
| **NotebookLM** | **Not** an MCP tool — a CLI on PATH (`~/.local/bin/notebooklm`), auth at `~/.notebooklm` | run via the Bash tool: `notebooklm use <id>; notebooklm ask "…"` |

MCP tools register only on a **session reload** (Claude Code reads `~/.claude.json` at startup); the NotebookLM CLI is usable immediately.

### 4.5 Durability across pod restarts
`/workspace` (MFS network volume) persists; `/root` + `/usr/local` + `~/.local` are an **ephemeral overlay** wiped on restart. Restore is **semi-manual** ("restart == new session"):
- **One umbrella command:** `bash /workspace/tools/restore_pod_tools.sh` — rebuilds the NotebookLM CLI (venv-by-copy → `setup_notebooklm.sh` fallback) + merges the InfraNodus/Perplexity MCP blocks (with keys) back into `~/.claude.json` (atomic, non-destructive) + restores the npx cache, then boot-checks each MCP server.
- **Snapshot:** `bash /workspace/tools/backup_pod_tools.sh` → durable, gitignored bundle `/workspace/.pod_restore/`.
- Secrets (API keys, Google cookies) live only on `/workspace`, **gitignored** (`**/storage_state.json`, `/.notebooklm/`, `/.pod_restore/`) and backstopped by the pre-commit secret scan.
- Documented in `SESSION_BOOTSTRAP.md §5`.

---

## 5. Glossary of the load-bearing artifacts

| Artifact | Role |
|---|---|
| `EXPERIMENT_RUNBOOK.md` | The living operating roadmap. `§0.3` = single source of "what's next"; `§0.4` = the close-out protocol; `§8` = the Track A–F decision tree. |
| `docs/program_state.json` | The machine source of truth for program state; `render_state.py` renders it into all `<!-- GENERATED -->` blocks. |
| `CORPUS/` | The evidence single-source-of-truth (`00` master evidence, `03` status ledger, per-result `NN` writeups). |
| `SESSION_CHECKPOINT.md` | Latest-session handoff + current status head. |
| `DISCIPLINE.md` | Always-in-context index: de-dup norm + close-out gate + tracker set. |
| `AUTONOMY.md` | The unattended-run contract (self-improvement loop, Layer A). |
| `tools/render_state.py` / `tools/closeout_check.py` | The anti-drift engine (generate + fingerprint). |
| `tools/git_hooks/pre-commit` | The commit-time enforcement gate. |

---

_Document type: process/reference (no experiment D-ID; not subject to `closeout_check`). Keep this file about **structure** — if a step changes, update it here; never copy program state into it._
