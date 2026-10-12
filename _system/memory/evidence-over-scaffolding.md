---
name: evidence-over-scaffolding
description: When the next live experiment is runnable, pre-registered and authorized, run it after its gates; don't let planning/research/runbook authoring accrete while empirical evidence stalls
metadata:
  type: feedback
---

**Trap (observed 2026-06-18):** after the G6.1 falsification, ~10 turns produced a synthesis doc, a Perplexity prompt, NotebookLM prompts, and a 481-line runbook — all good, all **meta**, and **zero new empirical evidence** the whole time, even though the next experiment (A1/A2) was cheap (~20–50 min), pre-coded, and on a cached model. The advisor named it: *mistaking the map for the territory.*

**Why:** a stream of operator requirements (each reasonable) pulls toward building more scaffolding; authoring polished artifacts *feels* like progress. But the binding output of this program is **empirical runs that can fail** — see [[review-diminishing-returns-evidence-is-binding]] (its cousin: that one is about re-reviewing/council-confirmation; this one is about authoring planning/research artifacts).

**How to apply:** when the next live experiment is *runnable as-is*, pre-registered and explicitly authorized, **run it after its applicable gates pass** — launch it (often in background; infra is pre-approved per [[standing-auth-forward-requirements]]) rather than expanding the plan further. Resist new planning-doc expansion until there is a fresh result to put in it. Planning artifacts are valuable once; iterating them in place of generating data is the trap. A good heuristic: if you've gone several turns without a new number, ask "what's the cheapest runnable experiment, and why haven't I launched it?" Related: [[prototype-tautology-trap]] (reserve confidence for runs that can falsify).

**Sharpening — cheap diagnostic variant BEFORE the expensive port (2026-06-18, advisor-flagged twice):** within an experiment fork there is often a cheap config-only variant (a mode flag, a recompute) that can *obviate or de-risk* a multi-day method port — run it first. A1 (a one-line `WRITE_MODE=batch` flag) ran before the A2 sentinel build and revealed batch alone eliminates the Genesis-path corruption; A2b (recompute `K_S` per rung — a one-liner) was the historical cheap diagnostic before the ~1–2 day BetaEdit (A3) port; the rationale was that recomputing stale preservation keys might close the gap for free; otherwise, the port would be *earned*. A2b subsequently ruled out K_S staleness. Heuristic: before committing to an expensive build, ask "is there a cheap variant whose result would change whether I build this at all?" — and run that.
