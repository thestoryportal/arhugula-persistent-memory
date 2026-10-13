# CODEX — Codex-only tooling, environment and conventions
Job: what only a Codex session needs — the Claude-to-Codex tooling map, research tools, environment and run notes, engineering conventions.
Routed from the root `CLAUDE.md` (twin: `AGENTS.md`). Moved verbatim from the pre-v2 `AGENTS.md`; edits are listed in the lane 5a report.

> This file is for **Codex**. It is additive: the repo's canonical framework was built under Claude and is unchanged — `CLAUDE.md` (routing), `_system/governance/`, `program/runbook/`, and `evidence/CORPUS/` remain authoritative. This file points you at that system, surfaces the load-bearing rules (which live in `_system/governance/`/the runbook and would otherwise not load for you), and maps Claude-specific tooling to Codex equivalents. **Do not restructure the canonical docs or the directory tree** — extend them in place.

## Methodology Skills Are Contracts, Not Agents
The repo-local methodology skills are concise operating contracts. They do not
create independent reasoning, autonomy, or new tool access by themselves. Use
them to decide what evidence/gates are required, but do not recite their
checklists back to the user. For high-stakes scientific reasoning, pair skills
with actual mechanisms: deterministic scripts (`code/gates/experiment_gate.py`,
`code/lab/analysis/stats.py`, `code/lab/analysis/power.py`), out-of-family advisor review
(`code/agents/claude_advisor.sh` for Codex-led work), or bounded subagent fan-out.

## Environment & how to run
- **Hardware (since 2026-10-03, D-HW-1):** the operator's MacBook M3 Pro, 48 GB unified memory shared by GPU and CPU jobs, Apple **MPS — no CUDA**. The RunPod 4090 pod is gone; all science runs locally — never propose rented compute. Science hardware and deployment target are both the M3 Pro (D-HW-1); the Intel-CPU target is retired.
- **Stack:** the worktree's `.venv` — Python 3.11, torch 2.8.0 (MPS), `transformers==4.51.0` (PINNED — 4.45 lacks Qwen3, 5.x breaks the engine nethook). Run project code with `.venv/bin/python`, not bare `python`. MPS trap: `t.to(device='cpu', dtype=X)` on an MPS offset view returns garbage — use `.cpu().to(X)`; do big reductions in float64.
- **Path convention:** live scripts resolve paths against `LLMDB_ROOT` (the code default `/workspace` is pod-era; the environment always sets it). They `sys.path.insert`+`os.chdir` to `$LLMDB_ROOT/code/memit/vendor` and read `HF_HOME=$LLMDB_ROOT/data/hf_cache`. **Local (2026-10-03, D-HW-1):** `LLMDB_ROOT` = the clone root (`/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`); `.claude/settings.json` exports it for agent sessions; the v2 links `data/hf_cache/` and `data/covariance/` do not exist in this worktree yet. Today, use `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/hf_cache` for HF models and `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches` for covariance statistics. These old-layout links point into the memit volume. The repo sync creates the untracked v2 links; the engine is vendored in-repo. **In a worktree, `LLMDB_ROOT` still names the main checkout — prefix `LLMDB_ROOT=$PWD`** (see `_system/governance/OPERATING-MODEL.md` § Team mode).
- **Run an experiment:** see the table in `_system/governance/REPRODUCIBILITY.md`. Examples:
  - B3 verdict reproduction writes `experiments/b3/runs/b3_quant_survival/b3_quant_survival_result.json`; it is not a read-only sanity check. Require named science authority and a reviewed fresh output namespace before execution; preserve the canonical result.
  - Authorized GPU mechanism reproduction (only after admission): `LLMDB_ROOT=$PWD .venv/bin/python code/lab/track_c/c2_key_collinearity.py` (loads Qwen2.5-3B, prints key-collinearity table, ends `C2_PHASE0_DONE`).
- **Long runs:** launch detached with `nohup .venv/bin/python -u … > <run dir>/logs/<name>.log 2>&1 &` (macOS has no `setsid`) — GPU edits + covariance solves take minutes to ~1 h. Admission refuses while any non-exempt python runs — `.venv` (including your own unittests) and system python alike — or the dashboard's `--gpu-summary` poll is up; while gated work is pending, hold `.venv` work, keep system-python checks short and foreground, and never weaken a gate. Before any bulk-writing job, check the disk budget (`_system/governance/STORAGE.md`).

## Build / test / verify (there is no app build; "tests" = experiment verification)
- **Reproducibility gates** (required after structural changes; execute C only under named science authority, after admission and with reviewed non-overwriting output destinations; otherwise report C UNVERIFIED), from the repo or worktree root with `LLMDB_ROOT=$PWD`:
  - **A** — no dangling pod-era paths: `grep -rnE '/workspace/' experiments/ code/configs/ | grep -vE 'hf_cache|memit_dry_run|external_prior_art|covariance_caches|b3_edited_qwen3b|b3_q4km|architecture_profile|llama_cpp_src|stage_1_sect|easyedit|qwen05b|LLMDB_ROOT|print\(|echo '` → expect empty.
  - **B** — provenance: every `/workspace/<path>` cited in `evidence/CORPUS/*.md` resolves to an existing `$LLMDB_ROOT/<path>` (the citations are pod-era; the files now live under the clone root).
  - **C** — `LLMDB_ROOT=$PWD .venv/bin/python code/lab/track_c/c2_key_collinearity.py` reproduces its table; `LLMDB_ROOT=$PWD .venv/bin/python code/lab/track_b/b3_verdict.py` recomputes the B3 PASS.
- **Per-experiment "tests"** are the **pre-registered pass criteria** in each `evidence/CORPUS/NN` doc + `experiments/g6/design/G6_G7_PASS_CRITERIA_DRAFT.md`. A run "passes" only against criteria set BEFORE the run.

## Engineering conventions (match these exactly)
- **Artifact naming:** scripts `code/lab/<track>/<name>.py`; results `experiments/<id>/runs/<slug>/<name>_result.json`; logs `experiments/<id>/runs/<slug>/logs/<name>.log` (`results/` and `logs/` are ignored legacy roots); evidence writeups `evidence/CORPUS/<NN>_<SLUG>.md`; decisions `D-<TRACK><n>` tied to the runbook decisions ledger (§5).
- **Status flags** (use everywhere): `DONE · RUNNING · NEXT · QUEUED · GATED(on X) · BLOCKED(on X) · HALTED · ELIMINATED(revisitable)`.
- **CORPUS writeup template** (see any of `14–20` or `evidence/CORPUS/AGENTS.md`): pre-registration (metric, PASS/PARTIAL/FAIL, prediction) → VERDICT + data table → mechanism → resolves/doesn't → **caveats kept flush** → Decision-ID → FORK.
- **New script header** (for any new live experiment): start with
  `import os, sys; LLMDB_ROOT = os.environ["LLMDB_ROOT"]` (fail loudly if unset — the old `/workspace` fallback is pod-era and silent) then reference `f"{LLMDB_ROOT}/code/configs/..."`, write under the record's `runs/<slug>/` (find it with `code/state/llmdb_records.py`).

## Claude → Codex tooling map (keep the discipline, swap the mechanism)
- **`advisor()` / advisor-review** → when **you lead** the work (not a MAESTRO brief), use **Claude as the out-of-family advisor** via `code/agents/claude_advisor.sh` (local Claude Code `claude.ai` Max subscription auth, no API key). Feed the finding/design + evidence + exact numbers; it does NOT see your transcript. Codex/GPT review is fallback or secondary for Codex-led work. For Claude-led work, use GPT-family Codex review for independence. Input, not authority; evidence binds.
- **Council (multi-agent adversarial review)** → multiple subagents / `/review` passes with distinct lenses.
- **Claude memory** → `_system/memory/` (read it; add new durable learnings there as one-fact-per-file with frontmatter, and update `_system/memory/MEMORY.md`).
- For large/changing external context, prefer MCP (Codex best-practice) over hardcoding.

## Research tools — MCP / CLI (opt-in, secrets are user-supplied)
External research tools on the Mac; some require **your** credentials to activate (do **not** commit keys into the repo — use the per-user config below).

### Perplexity (MCP) — READY
Live web search / deep research with citations. Tools: `perplexity_search`, `perplexity_ask`, `perplexity_research`, `perplexity_reason`. Needs `PERPLEXITY_API_KEY` (get at https://console.perplexity.ai). Node + `npx` are installed; verify versions and command resolution before use.
- **Codex:** `codex mcp add perplexity --env PERPLEXITY_API_KEY=YOUR_KEY -- npx -y @perplexity-ai/mcp-server`
- **Claude Code:** `claude mcp add perplexity --env PERPLEXITY_API_KEY=YOUR_KEY -- npx -y @perplexity-ai/mcp-server`
- (key lands in `~/.codex/config.toml` / `~/.claude.json`, not the repo)

### NotebookLM — via Browser Harness (CLI broken)
The `notebooklm-py` CLI broke when Google moved NotebookLM to notebook.google.com. Drive the operator's signed-in Chrome through Browser Harness from a script file instead (`_system/memory/notebooklm-via-browser-harness.md`, `browser-harness-for-browser-automation.md`). Unofficial and ToS-gray; treat outputs as leads, never evidence.

### InfraNodus (MCP) — text-network gap analysis + GraphRAG memory — optional (verify configured access; key required)
Builds a **concept co-occurrence network** from text/URL/corpus and surfaces **structural gaps** (under-connected bridges between clusters), topical clusters, and betweenness — then can generate **research questions/ideas** that bridge those gaps. Package `infranodus-mcp-server` (npm, v1.7.1+). Needs `INFRANODUS_API_KEY` (generate at https://infranodus.com/api-access). Node + `npx` installed; verify versions and live MCP access before use.
- **Setup — Codex:** `codex mcp add infranodus --env INFRANODUS_API_KEY=YOUR_KEY -- npx -y infranodus-mcp-server`
- **Setup — Claude Code:** `claude mcp add infranodus --env INFRANODUS_API_KEY=YOUR_KEY -- npx -y infranodus-mcp-server`
- (key lands in `~/.codex/config.toml` / `~/.claude.json`, not the repo; or use hosted `https://mcp.infranodus.com` via OAuth2)
- **Two distinct uses:** (a) **ideation/gap** — `generate_content_gaps`, `generate_research_questions`, `generate_research_ideas`, `develop_conceptual_bridges`, `difference_between_texts` (us-vs-prior-art); (b) **GraphRAG memory** — `create_knowledge_graph`, `retrieve_from_knowledge_base`, `memory_get_relations`, `search`/`fetch`.
- **⚠️ Discipline (load-bearing):** InfraNodus is an **IDEATION/optimization tool, not a falsifier** (DISCIPLINE §3). Its gaps/questions/ideas are **LEADS → write to the hypothesis register** with `builds-on`/`would-advance` framing (§2 step 7) and **falsify by experiment** — **never** record an InfraNodus output as evidence or in `evidence/CORPUS/`. Same Goodhart caution as autoresearch.
