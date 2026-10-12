# AGENTS.md — Codex operating guide for the LLM-as-Database research repo

> This file is for **Codex**. It is additive: the repo's canonical framework was built under Claude and is unchanged — `CLAUDE.md`, `program/runbook/`, and `evidence/CORPUS/` remain authoritative. This file points you at that system, surfaces the load-bearing rules (which live in `CLAUDE.md`/the runbook and would otherwise not load for you), and maps Claude-specific tooling to Codex equivalents. **Do not restructure the canonical docs or the directory tree** — extend them in place.

## ⭐ Context management — BINDING for every session (operator directive, 2026-10-09)
Operator: "Do not forget to manage context usage for yours and every team session you are orchestrating." / "This context directive must be made durable through any and all handoffs."
- Watch your own `Context N% left`. Start a new piece of work only at ≥60% left. At ≤45% left with a long step pending, stop and write a handoff; by ≤40% left, or immediately on any "Context compacted", **stop starting new work**: write a handoff note (what is done, what is in flight, exact file paths, next step, open risks) to the brief-named handoff destination (a separate file for tested reports), then say so in your reply so the orchestrator can start a fresh successor session.
- Never let a session approach full-window compaction; a fresh successor with a precise handoff beats a compacted, drifting one.
- Every handoff note you write restates this section, so the directive survives every handoff.

## ⭐ Team mode — when MAESTRO (Claude) dispatches you
Most work arrives as a build brief from MAESTRO, the Claude orchestrator, in a prompt file; GPT-6-Astra (`codex exec`) is the binding reviewer; the operator rules only on go/no-go, scope, frozen-prereg amendments, storage/spend and deletions. Your contract:
- **Test-first from the prereg.** Derive the test list from the prereg's numbered criteria, gates and labels before writing code; RED, then GREEN; include round-trip and boundary/HALT tests (`_system/memory/test-first-one-round-builds.md`). One clean round beats three FIX-FIRST rounds.
- **Stay inside the brief.** No commits (MAESTRO verifies and commits), no real runs, no deletions, no edits to files the brief does not name, unless the brief explicitly authorizes them. Another session may have uncommitted work in the same worktree — leave it untouched. When you notice *"this neighbouring file is wrong too, I'll just fix it while I'm here"* — that is the moment to stop: report it in your reply; the file may belong to a build in flight.
- **Prove scope.** Hash the files you may touch before and after; save RED/GREEN logs and a short report next to the subject; say what is UNVERIFIED.
- **Finish with the exact reply token** the brief asks for, so MAESTRO's watcher sees completion.
- **Never push, merge, or touch the PR** — no `git push`, no `gh pr merge|ready|edit|close`, no CI reruns. Merging is MAESTRO's alone, through `code/ops/git/git_merge_gate.py`, under the cooperative rule (full text adopted verbatim from `_archive/projects/git-automation/git_automation_fix3_mb13_20261010T092614.133488Z/build_report.md:23`; CLAUDE.md § Merging):

> **Binding cooperative rule:** before any merge-gate work, read and satisfy the full verbatim paragraph in `CLAUDE.md` § Merging. Every reservation, lock, suspension, drain, exception and post-merge failure obligation there applies unchanged; it is not replaced by a summary here.

- **In a worktree, prefix every repo tool with `LLMDB_ROOT=$PWD`** — the shell exports the MAIN checkout, and `closeout_check`, `engine_fingerprint`, `render_state` and the pre-commit hook otherwise read or write main without a word of warning.

## ⭐ North Star & Discipline — load `_system/governance/DISCIPLINE.md` FIRST
**The goal:** prove/falsify the LLM-as-Database spec is implementable *before* it's built → the **F1 readiness determination**. Everything serves F1; falsification-first (truth, not green checkmarks). **Before any non-trivial action run the drift check:** *does this advance F1 or a live §0.3 falsifier?* `_system/governance/DISCIPLINE.md` holds the north star, **context read-triggers**, the **deep-thinking-on-failure** protocol (mandatory when an experiment fails/stalls/surprises), and **tool & loop thresholds** (advisor / council / autoresearch / Perplexity / NotebookLM — when to invoke + min/max bounds). Honor it.


## Methodology Skills Are Contracts, Not Agents
The repo-local methodology skills are concise operating contracts. They do not
create independent reasoning, autonomy, or new tool access by themselves. Use
them to decide what evidence/gates are required, but do not recite their
checklists back to the user. For high-stakes scientific reasoning, pair skills
with actual mechanisms: deterministic scripts (`code/gates/experiment_gate.py`,
`code/lab/analysis/stats.py`, `code/lab/analysis/power.py`), out-of-family advisor review
(`code/agents/claude_advisor.sh` for Codex-led work), or bounded subagent fan-out.

A route that preserves a product while relaxing the spec's intended in-weight
memory contract is an engineering mitigation, not an F1 closure, unless the spec
and operator explicitly accept that relaxation. Keep such conditions OPEN or
BLOCKING and propose the cheapest source-faithful test that could still satisfy
the north-star claim.

## What this is
A falsification-first research program testing whether facts can be **stored in / retrieved from / governed within / deployed from** an LLM's weights (MEMIT/AlphaEdit editing), stress-testing the spec at `knowledge/specs/integrated-spec-v1_2/` toward implementation-readiness.

## After _system/governance/DISCIPLINE.md FIRST, follow CLAUDE.md § Current operating model for mandatory re-grounding; use this task reference list as needed
1. `README.md` — program, headline verdicts, repo map.
2. `program/runbook/` **§0.3** — the single source of "what's next" (current position + next experiments). Read this before starting any experiment.
3. `program/checkpoints/` (top block) — latest session handoff/state.
4. `_system/governance/REPRODUCIBILITY.md` — environment + per-experiment re-run commands.
5. `program/registers/EXPERIMENT_REGISTRY.md` (+ `program/registers/experiment_registry.json`) — every experiment → script/config/result/log/CORPUS-doc/status/decision-ID.
6. `evidence/CORPUS/` — the locked evidence ledger (numbered findings `00`–`NN`, append-only, + provenance/status ledgers). `evidence/CORPUS/README.md` is its index.
7. `program/registers/HYPOTHESIS_REGISTER_2026-06-18.md` — the open hypothesis space + top leverage.
8. `_system/memory/MEMORY.md` — durable cross-session learnings (one fact per file). Read relevant entries; they encode hard-won traps.

## Repository layout
```
experiments/<track>/   live re-runnable code: governance/ scale/ track_a/ track_b/ track_c/ deployment/ infra_scripts/
code/configs/               hparams/  screens/  probes/
results/  logs/        structured result JSONs · run logs
docs/                  EXPERIMENT_REGISTRY, HYPOTHESIS_REGISTER, framework_findings/, session_summaries/, runbooks/
evidence/CORPUS/                THE evidence ledger (do not rewrite past entries)
research_and_specs/    the governing spec + research synthesis
archive/               FROZEN historical scripts (s-series), notebooks, stale subdirs — do not re-run or rewrite
_system/memory/         durable learnings
— infrastructure (large, never move; larql, BetaEdit and b3_q4km.vindex are optional/recovered assets, absent in this checkout) — memit_dry_run/ (engine) code/vendor/external_prior_art/ (larql, BetaEdit)
  data/hf_cache/ data/covariance/ code/vendor/llama_cpp_src/ experiments/b3/runs/b3_edit/bulk/b3_edited_qwen3b/ b3_q4km.vindex/ *.gguf experiments/stage-1-sect/runs/stage_1_sect/ architecture_profile/
```

## Environment & how to run
- **Hardware (since 2026-10-03, D-HW-1):** the operator's MacBook M3 Pro, 48 GB unified memory shared by GPU and CPU jobs, Apple **MPS — no CUDA**. The RunPod 4090 pod is gone; all science runs locally — never propose rented compute. Science hardware and deployment target are both the M3 Pro (D-HW-1); the Intel-CPU target is retired.
- **Stack:** the worktree's `.venv` — Python 3.11, torch 2.8.0 (MPS), `transformers==4.51.0` (PINNED — 4.45 lacks Qwen3, 5.x breaks the engine nethook). Run project code with `.venv/bin/python`, not bare `python`. MPS trap: `t.to(device='cpu', dtype=X)` on an MPS offset view returns garbage — use `.cpu().to(X)`; do big reductions in float64.
- **Path convention:** live scripts resolve paths against `LLMDB_ROOT` (the code default `/workspace` is pod-era; the environment always sets it). They `sys.path.insert`+`os.chdir` to `$LLMDB_ROOT/code/memit/vendor` and read `HF_HOME=$LLMDB_ROOT/data/hf_cache`. **Local (2026-10-03, D-HW-1):** `LLMDB_ROOT` = the clone root (`/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory`); `.claude/settings.json` exports it for agent sessions; `data/covariance/` and `data/hf_cache/` are symlinks into the memit volume; the engine is vendored in-repo. **In a worktree, `LLMDB_ROOT` still names the main checkout — prefix `LLMDB_ROOT=$PWD`** (see Team mode).
- **Run an experiment:** see the table in `_system/governance/REPRODUCIBILITY.md`. Examples:
  - B3 verdict reproduction writes `experiments/b3/runs/b3_quant_survival/b3_quant_survival_result.json`; it is not a read-only sanity check. Require named science authority and a reviewed fresh output namespace before execution; preserve the canonical result.
  - Authorized GPU mechanism reproduction (only after admission): `LLMDB_ROOT=$PWD .venv/bin/python code/lab/track_c/c2_key_collinearity.py` (loads Qwen2.5-3B, prints key-collinearity table, ends `C2_PHASE0_DONE`).
- **Long runs:** launch detached with `nohup .venv/bin/python -u … > logs/<name>.log 2>&1 &` (macOS has no `setsid`) — GPU edits + covariance solves take minutes to ~1 h. Admission refuses while any non-exempt python runs — `.venv` (including your own unittests) and system python alike — or the dashboard's `--gpu-summary` poll is up; while gated work is pending, hold `.venv` work, keep system-python checks short and foreground, and never weaken a gate. Before any bulk-writing job, check the disk budget (Constraints below).

## Build / test / verify (there is no app build; "tests" = experiment verification)
- **Reproducibility gates** (required after structural changes; execute C only under named science authority, after admission and with reviewed non-overwriting output destinations; otherwise report C UNVERIFIED), from the repo or worktree root with `LLMDB_ROOT=$PWD`:
  - **A** — no dangling pod-era paths: `grep -rnE '/workspace/' experiments/ code/configs/ | grep -vE 'hf_cache|memit_dry_run|external_prior_art|covariance_caches|b3_edited_qwen3b|b3_q4km|architecture_profile|llama_cpp_src|stage_1_sect|easyedit|qwen05b|LLMDB_ROOT|print\(|echo '` → expect empty.
  - **B** — provenance: every `/workspace/<path>` cited in `evidence/CORPUS/*.md` resolves to an existing `$LLMDB_ROOT/<path>` (the citations are pod-era; the files now live under the clone root).
  - **C** — `LLMDB_ROOT=$PWD .venv/bin/python code/lab/track_c/c2_key_collinearity.py` reproduces its table; `LLMDB_ROOT=$PWD .venv/bin/python code/lab/track_b/b3_verdict.py` recomputes the B3 PASS.
- **Per-experiment "tests"** are the **pre-registered pass criteria** in each `evidence/CORPUS/NN` doc + `experiments/g6/design/G6_G7_PASS_CRITERIA_DRAFT.md`. A run "passes" only against criteria set BEFORE the run.

## Engineering conventions (match these exactly)
- **Artifact naming:** scripts `experiments/<track>/<track><n>_<slug>.py`; results `results/<name>_result.json`; logs `logs/<name>.log`; evidence writeups `evidence/CORPUS/<NN>_<SLUG>.md`; decisions `D-<TRACK><n>` tied to the runbook decisions ledger (§5).
- **Status flags** (use everywhere): `DONE · RUNNING · NEXT · QUEUED · GATED(on X) · BLOCKED(on X) · HALTED · ELIMINATED(revisitable)`.
- **CORPUS writeup template** (see any of `14–20` or `evidence/CORPUS/AGENTS.md`): pre-registration (metric, PASS/PARTIAL/FAIL, prediction) → VERDICT + data table → mechanism → resolves/doesn't → **caveats kept flush** → Decision-ID → FORK.
- **New script header** (for any new live experiment): start with
  `import os, sys; LLMDB_ROOT = os.environ["LLMDB_ROOT"]` (fail loudly if unset — the old `/workspace` fallback is pod-era and silent) then reference `f"{LLMDB_ROOT}/code/configs/..."`, write to `f"{LLMDB_ROOT}/results/..."`.

## Constraints / DO-NOT (load-bearing — these are the `CLAUDE.md` LAWs, surfaced for you)
- **Engine `code/memit/vendor` is UNMODIFIED on the science path.** Any harness-side reimplementation of an engine primitive MUST first pass the **inertness gate** (LAW#5): prove bit-for-behavior reproduction on a null/identity edit (`|Δexpr|≈0`) before trusting results. Most live scripts run this gate first — keep it.
- **One-fix-then-halt** on a science-path bug: change one thing, observe, halt with a clean diagnostic. Do not iterate blindly.
- **Never overwrite or delete** `evidence/CORPUS/*`, `results/*_result.json`, `*_state_ledger.jsonl`, or `reproducibility_manifest*.json`. CORPUS is append-only (new finding = next `NN`); past entries are locked even when later corrected (record the correction, don't erase).
- **Parametrized harness output paths MUST be namespaced** by model/variant (env `RESULT_TAG`, or a model-suffixed filename) — a model-agnostic default output path silently overwrote a canonical result this session (see `_system/memory/durable-artifact-path-collision.md`).
- **Disk is a shared bench (`CLAUDE.md` → Storage discipline; runbook §3.3a).** Before any job that writes bulk, state its disk budget and confirm free space ≥ projected writes + 20 GiB — the C10Y pre-cast diagnostic once wrote 105 GB of packets, filled `memit`, and killed the next GPU job. Irreplaceable bulk goes to Google Drive (`gdrive:`), never the Mac's internal SSD. Reclaim eligibility is not execution permission: deletions run only after the operator approves the exact path, size and method (`_system/memory/approved-deletes-ask-then-rmtree.md`).
- **Do not move the infra dirs** or break the `LLMDB_ROOT` convention. `archive/` scripts are frozen (target the pre-2026-06-18 flat layout) — do not re-run or rewrite them.
- **Edit-tool changes to large canonical docs silently reverted on the RunPod FUSE volume** (e.g. `program/runbook/`, 2026-06-18); recurrence on the local memit volume is UNVERIFIED. Keep writing those via shell/python and **re-read after an intervening operation to confirm persistence.**
- **Distinguish EVIDENCE-SHOWS from I-INFER**; quantify before claiming; keep caveats flush (honest, not minimized); cite exact artifact paths + numbers or flag UNVERIFIABLE.

## What "done" means (verification criteria)
An experiment is done when: (1) it ran against **pre-registered** pass criteria; (2) a `evidence/CORPUS/NN_*.md` writeup exists (template above) with flush caveats + a Decision-ID; (3) the **living-document protocol** (`program/runbook/` §0.4 and the full canonical-tracker protocol in `CLAUDE.md` § Close-out gate / `_system/governance/DISCIPLINE.md` §1.1, including `program/program_state.json` + regeneration rather than hand-editing generated blocks) is followed — update `evidence/CORPUS/00_MASTER_EVIDENCE.md` + `03_STATUS_LEDGER.md`, runbook §0.3/§12/§13, `program/checkpoints/`, and add any durable learning to `_system/memory/` — and **`LLMDB_ROOT=$PWD python3 code/gates/closeout_check.py <D-ID>` reports ✅ ALL GREEN** (the mechanical gate; nothing is done before it); (4) gates A–C pass if files moved. A halted or compromised run is **re-run in fresh processes after a reviewed fix, never read around** (operator ruling, `_system/memory/rerun-never-patch.md`). A cleanly-HALTED run with a diagnostic is a SUCCESS, not a failure.

## Claude → Codex tooling map (keep the discipline, swap the mechanism)
- **Binding review at promote gates** → **GPT-6-Astra at high effort**, run by MAESTRO: `codex exec --model gpt-6-astra -c model_reasoning_effort=high -c mcp_servers.graft.enabled=false -s read-only --skip-git-repo-check -C <worktree> -o <out.md> < <packet.md>` (graft must stay disabled for exec; do not use graft tools or CLI, and ignore leftover graft hook text). A review by your own helper subagent is useful but is not Astra — label it as what it is.
- **`advisor()` / advisor-review** → when **you lead** the work (not a MAESTRO brief), use **Claude as the out-of-family advisor** via `code/agents/claude_advisor.sh` (local Claude Code `claude.ai` Max subscription auth, no API key). Feed the finding/design + evidence + exact numbers; it does NOT see your transcript. Codex/GPT review is fallback or secondary for Codex-led work. For Claude-led work, use GPT-family Codex review for independence. Input, not authority; evidence binds.
- **Council (multi-agent adversarial review)** → multiple subagents / `/review` passes with distinct lenses.
- **Claude memory** → `_system/memory/` (read it; add new durable learnings there as one-fact-per-file with frontmatter, and update `_system/memory/MEMORY.md`).
- For large/changing external context, prefer MCP (Codex best-practice) over hardcoding.

## Autonomous (no-HIL) runs — `_system/governance/AUTONOMY.md` + `code/lab/runners/autonomy_driver.py`
For bounded unattended overnight progress. **Opt-in, operator-launched** — nothing runs on its own. This harness is separate from MAESTRO's standing delegation, under which the orchestrated team keeps working within authorized scope.
- **Driver** = thin deterministic guardrails: hard wall-clock (`--budget-min`), **preflight hard-gate**, per-unit `max_loops`/`timeout_s`, **pre-registered deterministic PASS/PARTIAL/FAIL/INVALID** from the result JSON (no model judgment), gate-log (`logs/autonomy_gates.jsonl`), and **closeout to STAGING** (`experiments/ml/reviews/pending_findings/NN_<unit>.md`). **At supervised fold-in (when a staged finding is promoted to evidence/CORPUS/ledger/runbook), the close-out is NOT done until `python3 code/gates/closeout_check.py <D-ID>` is ✅ ALL GREEN** (binding gate, DISCIPLINE §1.1 — mechanical, not operator-verified).
- **The driver NEVER writes `evidence/CORPUS/*`, the ledger, the runbook, or the checkpoint.** Unattended findings are staged; the operator folds them into the canonical §0.4 record on supervised review. The `.codex/hooks/` (pre_tool_use_policy / stop_gate) are intended to enforce this; runtime enforcement is UNVERIFIED until current paths and invocation are qualified. STAGING-only remains mandatory regardless of hook availability.
- **Mission** (`code/lab/runners/autonomy_mission.json`) points at **one named pre-registered FALSIFIER** from §0.3. The bundled mission (`c2band_falsifier`) is **STALE** — that falsifier is done (D-C2band-1); re-point it to a live §0.3 falsifier before any launch. Optimizer/sweep units must be `fenced:true` (candidate-log only, never a conclusion) — see DISCIPLINE §3.1.
- **`--mode agent`** appends an advisory independent review per reviewable staged finding. Default backend is Claude via `code/agents/claude_advisor.sh` for Codex-led work (`--advisor claude`; claude.ai Max subscription auth, no API key); `--advisor codex` remains fallback/secondary. Default `--mode batch` runs the unit command directly.
- Launch + review instructions: `_system/governance/AUTONOMY.md`. Bounds & rationale: `_system/governance/DISCIPLINE.md` §3.1.

## Current state & next work
Do **not** hardcode "what's next" here — it changes. The single source is `program/runbook/` §0.3 (+ `program/checkpoints/` top block); `program/registers/HYPOTHESIS_REGISTER_2026-06-18.md` holds the open space.

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

## Multi-agent / subagent patterns (parallel & series)
**Key constraint — ONE MPS GPU and one shared 48 GB memory pool.** Parallelism speeds the *non-GPU* work (triage, analysis, verification, docs, design, prep); GPU experiments **serialize** on the M3 Pro, and heavy CPU jobs compete for the same unified memory — fan out the *analysis*, queue the *compute*.

**Parallel (fan-out):**
- **Triage sweep** — N readers over repos / papers / spec sections; each returns only a distilled verdict (e.g. the 130-repo content triage).
- **Adversarial verification panel** — on a declared finding, 3 subagents each try to **REFUTE** it via a *distinct* lens (confound / metric-validity / reproducibility); keep only if it survives. (This is the §2 deep-thinking + council-independence rule, parallelized.)
- **Parallel de-confounding** — one subagent per failure-hypothesis, each runs one control (E1-style H1–H6).
- **Design judge-panel** — generate N approaches, score with independent judges, synthesize the winner.

**Series (pipeline):**
- **Propose → verify → synthesize** — autoresearch *proposes* a candidate; a **separate** agent re-verifies under pre-registered criteria + the inertness gate; a **third** writes the `evidence/CORPUS/` note. Enforces optimization ≠ falsification **by role**.
- **Experiment → documentation** — experimenter produces the result JSON; a doc agent folds it into evidence/CORPUS/runbook/checkpoint per §0.4.
- **Spec-reconciliation → F1** — as tracks close, a reconciliation agent maps each result → spec contract, surfacing remaining GAP/UNTESTED (the F1 deliverable, built incrementally).

**Codex mechanisms:** subagent workflows (the fan-outs); **git worktrees** for parallel file-editing agents (the repo is a git repo with worktrees under `.claude/worktrees/`; MAESTRO commits and pushes; only MAESTRO merges, only via `code/ops/git/git_merge_gate.py` under the cooperative rule in Team mode); `/fork` to branch a thread, `/agent` to switch; **background tasks** for long GPU runs; **automations / scheduled** runs for a daily "read §0.3 → run the next cheap falsifier."

**Guardrails (see `_system/governance/DISCIPLINE.md`):**
- Same-model subagents reading our own corpus = **weak independence** (runbook §2.5) → panels must be told to **refute**, with distinct lenses; **evidence stays binding** over any panel vote.
- **Bound the fan-out** (DISCIPLINE §3) — stop when marginal info ≈ 0.
- **Role separation** — the *proposer* (autoresearch) must **never** be the *documenter* (`evidence/CORPUS/`).
