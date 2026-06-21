# AGENTS.md — Codex operating guide for the LLM-as-Database research repo

> This file is for **Codex**. It is additive: the repo's canonical framework was built under Claude and is unchanged — `CLAUDE.md`, `EXPERIMENT_RUNBOOK.md`, and `CORPUS/` remain authoritative. This file points you at that system, surfaces the load-bearing rules (which live in `CLAUDE.md`/the runbook and would otherwise not load for you), and maps Claude-specific tooling to Codex equivalents. **Do not restructure the canonical docs or the directory tree** — extend them in place.

## ⭐ North Star & Discipline — load `DISCIPLINE.md` FIRST
**The goal:** prove/falsify the LLM-as-Database spec is implementable *before* it's built → the **F1 readiness determination**. Everything serves F1; falsification-first (truth, not green checkmarks). **Before any non-trivial action run the drift check:** *does this advance F1 or a live §0.3 falsifier?* `DISCIPLINE.md` holds the north star, **context read-triggers**, the **deep-thinking-on-failure** protocol (mandatory when an experiment fails/stalls/surprises), and **tool & loop thresholds** (advisor / council / autoresearch / Perplexity / NotebookLM — when to invoke + min/max bounds). Honor it.

## What this is
A falsification-first research program testing whether facts can be **stored in / retrieved from / governed within / deployed from** an LLM's weights (MEMIT/AlphaEdit editing), stress-testing the spec at `research_and_specs/llm-as-database-v1_2-integrated-spec.md` toward implementation-readiness.

## Read first (in this order) — do NOT duplicate these, reference them
1. `README.md` — program, headline verdicts, repo map.
2. `EXPERIMENT_RUNBOOK.md` **§0.3** — the single source of "what's next" (current position + next experiments). Read this before starting any experiment.
3. `SESSION_CHECKPOINT.md` (top block) — latest session handoff/state.
4. `REPRODUCIBILITY.md` — environment + per-experiment re-run commands.
5. `docs/EXPERIMENT_REGISTRY.md` (+ `docs/experiment_registry.json`) — every experiment → script/config/result/log/CORPUS-doc/status/decision-ID.
6. `CORPUS/` — the locked evidence ledger (numbered findings `00–20` + provenance/status ledgers). `CORPUS/README.md` is its index.
7. `docs/HYPOTHESIS_REGISTER_2026-06-18.md` — the open hypothesis space + top leverage.
8. `memory_mirror/MEMORY.md` — durable cross-session learnings (one fact per file). Read relevant entries; they encode hard-won traps.

## Repository layout
```
experiments/<track>/   live re-runnable code: governance/ scale/ track_a/ track_b/ track_c/ deployment/ infra_scripts/
configs/               hparams/  screens/  probes/
results/  logs/        structured result JSONs · run logs
docs/                  EXPERIMENT_REGISTRY, HYPOTHESIS_REGISTER, framework_findings/, session_summaries/, runbooks/
CORPUS/                THE evidence ledger (do not rewrite past entries)
research_and_specs/    the governing spec + research synthesis
archive/               FROZEN historical scripts (s-series), notebooks, stale subdirs — do not re-run or rewrite
memory_mirror/         durable learnings
— infrastructure (large, never move) — memit_dry_run/ (engine) external_prior_art/ (larql, BetaEdit)
  hf_cache/ covariance_caches/ llama_cpp_src/ b3_edited_qwen3b/ b3_q4km.vindex/ *.gguf stage_1_sect/ architecture_profile/
```

## Environment & how to run
- **Hardware:** single NVIDIA RTX 4090 (24 GB). Deployment target = operator Intel CPU (edit-time GPU/offline, inference-time CPU).
- **Stack:** `transformers==4.51.0` (PINNED — 4.45 lacks Qwen3, 5.x breaks the engine nethook). PyTorch+CUDA. `torch.float16` loads.
- **Path convention:** live scripts resolve paths against `LLMDB_ROOT` (default `/workspace`): `export LLMDB_ROOT=/workspace`. They `sys.path.insert`+`os.chdir` to `$LLMDB_ROOT/memit_dry_run/memit` and read `HF_HOME=$LLMDB_ROOT/hf_cache`.
- **Run an experiment:** see the table in `REPRODUCIBILITY.md`. Examples:
  - No-GPU sanity: `python experiments/track_b/b3_verdict.py`
  - GPU mechanism smoke (~1 min): `python experiments/track_c/c2_key_collinearity.py` (loads Qwen2.5-3B, prints key-collinearity table, ends `C2_PHASE0_DONE`).
- **Long runs:** launch detached (`setsid … python -u … > logs/<name>.log 2>&1 &`) — GPU edits + covariance solves take minutes to ~1 h.

## Build / test / verify (there is no app build; "tests" = experiment verification)
- **Reproducibility gates** (run after any structural change), from repo root with `LLMDB_ROOT=/workspace`:
  - **A** — no dangling live paths: `grep -rnE '/workspace/' experiments/ configs/ | grep -vE 'hf_cache|memit_dry_run|external_prior_art|covariance_caches|b3_edited_qwen3b|b3_q4km|architecture_profile|llama_cpp_src|stage_1_sect|easyedit|qwen05b|LLMDB_ROOT|print\(|echo '` → expect empty.
  - **B** — provenance: every `/workspace/<path>` in `CORPUS/*.md` resolves to an existing file.
  - **C** — `python experiments/track_c/c2_key_collinearity.py` reproduces its table; `python experiments/track_b/b3_verdict.py` recomputes the B3 PASS.
- **Per-experiment "tests"** are the **pre-registered pass criteria** in each `CORPUS/NN` doc + `docs/G6_G7_PASS_CRITERIA_DRAFT.md`. A run "passes" only against criteria set BEFORE the run.

## Engineering conventions (match these exactly)
- **Artifact naming:** scripts `experiments/<track>/<track><n>_<slug>.py`; results `results/<name>_result.json`; logs `logs/<name>.log`; evidence writeups `CORPUS/<NN>_<SLUG>.md`; decisions `D-<TRACK><n>` tied to the runbook decisions ledger (§5).
- **Status flags** (use everywhere): `DONE · RUNNING · NEXT · QUEUED · GATED(on X) · BLOCKED(on X) · HALTED · ELIMINATED(revisitable)`.
- **CORPUS writeup template** (see any of `14–20` or `CORPUS/AGENTS.md`): pre-registration (metric, PASS/PARTIAL/FAIL, prediction) → VERDICT + data table → mechanism → resolves/doesn't → **caveats kept flush** → Decision-ID → FORK.
- **New script header** (for any new live experiment): start with
  `import os, sys; LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")` then reference `f"{LLMDB_ROOT}/configs/..."`, write to `f"{LLMDB_ROOT}/results/..."`.

## Constraints / DO-NOT (load-bearing — these are the `CLAUDE.md` LAWs, surfaced for you)
- **Engine `memit_dry_run/memit` is UNMODIFIED on the science path.** Any harness-side reimplementation of an engine primitive MUST first pass the **inertness gate** (LAW#5): prove bit-for-behavior reproduction on a null/identity edit (`|Δexpr|≈0`) before trusting results. Most live scripts run this gate first — keep it.
- **One-fix-then-halt** on a science-path bug: change one thing, observe, halt with a clean diagnostic. Do not iterate blindly.
- **Never overwrite or delete** `CORPUS/*`, `results/*_result.json`, `*_state_ledger.jsonl`, or `reproducibility_manifest*.json`. CORPUS is append-only (new finding = next `NN`); past entries are locked even when later corrected (record the correction, don't erase).
- **Parametrized harness output paths MUST be namespaced** by model/variant (env `RESULT_TAG`, or a model-suffixed filename) — a model-agnostic default output path silently overwrote a canonical result this session (see `memory_mirror/durable-artifact-path-collision.md`).
- **Do not move the infra dirs** or break the `LLMDB_ROOT` convention. `archive/` scripts are frozen (target the pre-2026-06-18 flat layout) — do not re-run or rewrite them.
- **`/workspace` is a network FS that has shown silent reverts of in-place edits to large canonical docs** (e.g. `EXPERIMENT_RUNBOOK.md`). Prefer append/rewrite via shell/python for those, and **re-read after writing to confirm persistence.**
- **Distinguish EVIDENCE-SHOWS from I-INFER**; quantify before claiming; keep caveats flush (honest, not minimized); cite exact artifact paths + numbers or flag UNVERIFIABLE.

## What "done" means (verification criteria)
An experiment is done when: (1) it ran against **pre-registered** pass criteria; (2) a `CORPUS/NN_*.md` writeup exists (template above) with flush caveats + a Decision-ID; (3) the **living-document protocol** (`EXPERIMENT_RUNBOOK.md` §0.4) is followed — update `CORPUS/00_MASTER_EVIDENCE.md` + `03_STATUS_LEDGER.md`, runbook §0.3/§12/§13, `SESSION_CHECKPOINT.md`, and add any durable learning to `memory_mirror/`; (4) gates A–C pass if files moved. A cleanly-HALTED run with a diagnostic is a SUCCESS, not a failure.

## Claude → Codex tooling map (keep the discipline, swap the mechanism)
- **`advisor()` (Claude's stronger-model transcript review)** → **the `advisor-review` skill** (`~/.codex/skills/advisor-review`): an independent **different/stronger-model** review at the same thresholds (before authoring a test set, before declaring done, when stuck). Run `codex review -m <stronger> "$(cat tools/advisor_review_prompt.md)"` for code/diffs (needs `git init`), or `codex exec -m <stronger>` fed the finding + evidence + that prompt for reasoning/findings. It does NOT see your transcript — **feed it the evidence**. Input, not authority; evidence binds.
- **Council (multi-agent adversarial review)** → multiple subagents / `/review` passes with distinct lenses.
- **Claude memory** → `memory_mirror/` (read it; add new durable learnings there as one-fact-per-file with frontmatter, and update `memory_mirror/MEMORY.md`).
- For large/changing external context, prefer MCP (Codex best-practice) over hardcoding.

## Autonomous (no-HIL) runs — `AUTONOMY.md` + `tools/autonomy_driver.py`
For bounded unattended overnight progress. **Opt-in, operator-launched** — nothing runs on its own.
- **Driver** = thin deterministic guardrails: hard wall-clock (`--budget-min`), **preflight hard-gate**, per-unit `max_loops`/`timeout_s`, **pre-registered deterministic PASS/PARTIAL/FAIL/INVALID** from the result JSON (no model judgment), gate-log (`logs/autonomy_gates.jsonl`), and **closeout to STAGING** (`logs/pending_findings/NN_<unit>.md`). **At supervised fold-in (when a staged finding is promoted to CORPUS/ledger/runbook), the close-out is NOT done until `python3 tools/closeout_check.py <D-ID>` is ✅ ALL GREEN** (binding gate, DISCIPLINE §1.1 — mechanical, not operator-verified).
- **The driver NEVER writes `CORPUS/*`, the ledger, the runbook, or the checkpoint.** Unattended findings are staged; the operator folds them into the canonical §0.4 record on supervised review. The `.codex/hooks/` (pre_tool_use_policy / stop_gate) enforce this.
- **Mission** (`tools/autonomy_mission.json`) points at **one named pre-registered FALSIFIER** from §0.3 (currently `c2band_falsifier`). Optimizer/sweep units must be `fenced:true` (candidate-log only, never a conclusion) — see DISCIPLINE §3.1.
- **`--mode agent`** shells `codex exec -m <model>` per unit so a model fulfils the deep-thinking / autoresearch / **independent (different-model) advisor-review** obligations inside the bounds (needs Codex auth). Default `--mode batch` runs the unit command directly.
- Launch + review instructions: `AUTONOMY.md`. Bounds & rationale: `DISCIPLINE.md` §3.1.

## Current state & next work
Do **not** hardcode "what's next" here — it changes. The single source is `EXPERIMENT_RUNBOOK.md` §0.3 (+ `SESSION_CHECKPOINT.md` top block). As of the last handoff: E1/B1/C2 done; the open fork is the **B3/E3 "is in-weight (L2) even required vs. L1-retrieval + external query-index" decision** (analysis, no compute) or the **band-[8–12] mechanism test**; A3/A4 parked. See `docs/HYPOTHESIS_REGISTER_2026-06-18.md` for the full open space.

## Research tools — MCP / CLI (opt-in, secrets are user-supplied)
Two external research tools are installed on the pod but require **your** credentials to activate (do **not** commit keys into the repo — use the per-user config below).

### Perplexity (MCP) — READY
Live web search / deep research with citations. Tools: `perplexity_search`, `perplexity_ask`, `perplexity_research`, `perplexity_reason`. Needs `PERPLEXITY_API_KEY` (get at https://console.perplexity.ai). Node 24 + `npx` are installed.
- **Codex:** `codex mcp add perplexity --env PERPLEXITY_API_KEY=YOUR_KEY -- npx -y @perplexity-ai/mcp-server`
- **Claude Code:** `claude mcp add perplexity --env PERPLEXITY_API_KEY=YOUR_KEY -- npx -y @perplexity-ai/mcp-server`
- (key lands in `~/.codex/config.toml` / `~/.claude.json`, not the repo)

### NotebookLM (`notebooklm-py`) — CLI installed; MCP experimental
Unofficial NotebookLM automation (bulk source import, research agents, audio/slide/quiz generation, exports). **Caveats:** unofficial undocumented Google API (can break, ToS-gray); auth is a browser Google sign-in.
- **CLI (installed, v0.7.2):** agents can shell out to `notebooklm <command>`. Auth first: `notebooklm login` (opens a browser — on this headless pod, instead extract cookies from a logged-in browser elsewhere and set `NOTEBOOKLM_AUTH_JSON`, or `notebooklm login --browser-cookies chrome` on a machine with the browser). Verify: `notebooklm auth check --test`.
- **MCP server:** NOT in the released package — install git-main to get it: `pip install "git+https://github.com/teng-lin/notebooklm-py.git#egg=notebooklm-py[mcp]"`, then `codex mcp add notebooklm -- notebooklm-mcp`.

### InfraNodus (MCP) — text-network gap analysis + GraphRAG memory — READY (key required)
Builds a **concept co-occurrence network** from text/URL/corpus and surfaces **structural gaps** (under-connected bridges between clusters), topical clusters, and betweenness — then can generate **research questions/ideas** that bridge those gaps. Package `infranodus-mcp-server` (npm, v1.7.1+). Needs `INFRANODUS_API_KEY` (generate at https://infranodus.com/api-access). Node 24 + `npx` installed.
- **Setup — Codex:** `codex mcp add infranodus --env INFRANODUS_API_KEY=YOUR_KEY -- npx -y infranodus-mcp-server`
- **Setup — Claude Code:** `claude mcp add infranodus --env INFRANODUS_API_KEY=YOUR_KEY -- npx -y infranodus-mcp-server`
- (key lands in `~/.codex/config.toml` / `~/.claude.json`, not the repo; or use hosted `https://mcp.infranodus.com` via OAuth2)
- **Two distinct uses:** (a) **ideation/gap** — `generate_content_gaps`, `generate_research_questions`, `generate_research_ideas`, `develop_conceptual_bridges`, `difference_between_texts` (us-vs-prior-art); (b) **GraphRAG memory** — `create_knowledge_graph`, `retrieve_from_knowledge_base`, `memory_get_relations`, `search`/`fetch`.
- **⚠️ Discipline (load-bearing):** InfraNodus is an **IDEATION/optimization tool, not a falsifier** (DISCIPLINE §3). Its gaps/questions/ideas are **LEADS → write to the hypothesis register** with `builds-on`/`would-advance` framing (§2 step 7) and **falsify by experiment** — **never** record an InfraNodus output as evidence or in `CORPUS/`. Same Goodhart caution as autoresearch.

## Multi-agent / subagent patterns (parallel & series)
**Key constraint — ONE GPU.** Parallelism speeds the *non-GPU* work (triage, analysis, verification, docs, design, prep); GPU experiments **serialize** on the single 4090 — fan out the *analysis*, queue the *compute*.

**Parallel (fan-out):**
- **Triage sweep** — N readers over repos / papers / spec sections; each returns only a distilled verdict (e.g. the 130-repo content triage).
- **Adversarial verification panel** — on a declared finding, 3 subagents each try to **REFUTE** it via a *distinct* lens (confound / metric-validity / reproducibility); keep only if it survives. (This is the §2 deep-thinking + council-independence rule, parallelized.)
- **Parallel de-confounding** — one subagent per failure-hypothesis, each runs one control (E1-style H1–H6).
- **Design judge-panel** — generate N approaches, score with independent judges, synthesize the winner.

**Series (pipeline):**
- **Propose → verify → synthesize** — autoresearch *proposes* a candidate; a **separate** agent re-verifies under pre-registered criteria + the inertness gate; a **third** writes the `CORPUS/` note. Enforces optimization ≠ falsification **by role**.
- **Experiment → documentation** — experimenter produces the result JSON; a doc agent folds it into CORPUS/runbook/checkpoint per §0.4.
- **Spec-reconciliation → F1** — as tracks close, a reconciliation agent maps each result → spec contract, surfacing remaining GAP/UNTESTED (the F1 deliverable, built incrementally).

**Codex mechanisms:** subagent workflows (the fan-outs); **git worktrees** for parallel file-editing agents — ⚠️ this repo is **not git-initialized**, run `git init` first (also unlocks `/review` + diffs); `/fork` to branch a thread, `/agent` to switch; **background tasks** for long GPU runs; **automations / scheduled** runs for an overnight autoresearch loop or a daily "read §0.3 → run the next cheap falsifier."

**Guardrails (see `DISCIPLINE.md`):**
- Same-model subagents reading our own corpus = **weak independence** (runbook §2.5) → panels must be told to **refute**, with distinct lenses; **evidence stays binding** over any panel vote.
- **GPU serializes** — fan out analysis, queue compute; don't expect 5× from 5 GPU runs.
- **Bound the fan-out** (DISCIPLINE §3) — stop when marginal info ≈ 0.
- **Role separation** — the *proposer* (autoresearch) must **never** be the *documenter* (`CORPUS/`).
