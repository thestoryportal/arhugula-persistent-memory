## §2 — OPERATING DISCIPLINES (how we work — non-negotiable)
═══════════════════════════════════════════════════════════════════════

### §2.1 — Advisor-invocation discipline
Call `advisor()`: (a) **before authoring any test/criteria set or new harness** — not just before declaring done; (b) before committing to an interpretation or approach; (c) when stuck/looping; (d) before declaring an experiment complete (make the deliverable durable FIRST). On long tasks: at least once before committing to an approach and once before done. Give its advice serious weight; if you have primary evidence contradicting it, surface the conflict in one more call rather than silently overriding. It is enabled via `/advisor` (Opus 4.8).

### §2.2 — Additional-research discipline (when to reach past our own data)
- **Spec review** — ALWAYS before framing a load-bearing decision; read the governing § end-to-end (grep-excerpts misframed a decision before). Every experiment block cites its §.
- **NotebookLM** — when the question is "does our existing corpus/spec/council already cover this?" (mechanism, prior art we curated, spec assumptions). Corpus-grounded.
- **Perplexity / `deep-research`** — when the question is "what is the field's current SOTA / is there a method we're missing?" Open-web. Trigger after a falsification (G6.1 → the cross-entity survey) or before a frontier bet.
- **Council** — when *authoring/refining spec contracts* or surfacing tensions, NOT for confirming empirical conclusions.
- **WebSearch** — targeted facts (model sizes, repos, paper availability) feeding §5/§6.
- **Rule:** research informs; **only empirical runs on our harness are binding evidence** (§2.5). Cite artifact + exact number, or flag `UNVERIFIABLE`.

### §2.3 — Falsification & anti-bias discipline (the traps that have bitten us)
- **Pre-register** metric, procedure+n, threshold+direction, and a *positive control* BEFORE the run. "Let the numbers land."
- **Anchor trap** — never set a threshold "just below what we got"; derive it from what makes the thing viable *as a database per the spec*.
- **Prototype-tautology trap** ([[prototype-tautology-trap]]) — code that implements a contract and verifies it implements the contract proves control-flow, not the contract. Build tests that can actually fail.
- **False-no-op / expression gate** — an unexpressed edit inflates "locality." Always measure apply-time expression separately from end-state retention (the G6.1 split).
- **JS-vs-top-1** — match the metric to the claim. A "reads corrupted" claim is a top-1 claim; measure top-1, not just distributional JS.
- **Disjoint pools** — for any preserve/sentinel method, the protected set and the eval set must be DISJOINT (and both disjoint from edited), or you rebuild the tautology at the data level.
- **Independence** — a passing self-test is not evidence the advice was wrong.

### §2.4 — Engine-integrity LAWs (from CLAUDE.md — load-bearing)
1. **Fingerprint gate** — verify the engine identity/fingerprint before any dispatch; engine + LARQL + git stay UNMODIFIED.
2. **LAW#5 inertness** — any harness-side reimplementation (e.g., in-solve AlphaEdit, sentinels) MUST first prove it reproduces the stock engine bit-for-behavior on a null/identity edit before its science results are trusted. (`g6_scale_n.py` runs this gate every time.)
3. **One-fix-then-halt** — change one thing, observe, halt; don't stack fixes.
4. **Read source before authoring** — read the engine/spec code you build on, end-to-end.
5. **Science-path-patch isolation** — never patch the science path; prove inertness of any shim.

### §2.5 — Independence discipline
The binding signal is **empirical runs that can fail**. Review ≠ evidence. Same-model council/subagents reading our corpus = confirmation-amplification — a *different* model cold-reading is better, but still not evidence. When confidence is highest, call `advisor()` and seek a falsifier, not a confirmer.

### §2.6 — Context-save discipline
- Durable deliverables → `/workspace` (never only `/dev/shm`, which is RAM). Update `evidence/CORPUS/` + `program/checkpoints/` + this runbook's §0.3/§12/§13.
- `/dev/shm` artifacts are reproducible-from-scripts; never the source of truth.
- After a meaningful step, write the checkpoint so a fresh context can resume from §0.3 alone.

### §2.7 — Memory & learnings write discipline
- **Write a memory** when a durable, cross-session fact/learning surfaces: a corrected reasoning trap, an operator preference, a tool/infra gotcha, a project decision not derivable from code.
- **Types:** `user` / `feedback` (corrections + the why) / `project` / `reference`. One fact per file + frontmatter; link `[[related]]`; add a one-line pointer to `MEMORY.md`.
- **Don't** save what the repo already records (code, git history, CORPUS). If asked to remember such, save *what was non-obvious* about it.
- **Mirror** after writing: copy each changed note between the live dir `~/.claude/projects/-Volumes-memit-llm-database-poc-mirror/memory/` and the git-tracked `_system/memory/` so the two stay identical (MEMORY.md included); `code/gates/closeout_check.py` checks both (memory_mirror sync drift + every MEMORY.md link resolves).
- **Learnings cadence:** at each experiment close, ask "what did this teach that a future agent must not relearn the hard way?" → if durable, write it (e.g., this session produced [[prototype-tautology-trap]], `runpod-dashboard-vs-pod-metrics` (pod-era, retired 2026-10-10), [[standing-auth-forward-requirements]]).

### §2.8 — Artifact, naming & Decision-ID conventions
- **Scripts** `<track><n>_<slug>.py` (e.g., `a2_relbal_sentinels.py`); **results** `<same>_result.json`; **logs** `<same>.log`; **writeups** `evidence/CORPUS/<NN>_<SLUG>.md`.
- **Heavy I/O on `/dev/shm`**, durable outputs copied to `/workspace`.
- **Decision-IDs** `D-<TRACK><n>` (e.g., `D-A2-1`) tie every accept/eliminate choice to §5.
- **Launch durably**: `setsid bash -c '… python -u script.py > script.log 2>&1' </dev/null & disown` (survives disconnect).

═══════════════════════════════════════════════════════════════════════
