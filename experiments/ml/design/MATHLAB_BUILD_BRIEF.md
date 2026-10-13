# Math lab steps 1–3 — build brief (D-ML-1)

Status: build brief, 2026-10-08. Builder: Codex session `codexmb`. Reviewer: GPT-6-Astra (high) after the build. Lead: program session.

## Authority
Build exactly what the FROZEN pre-registration specifies: `docs/MATHLAB_PREREG.md`, FROZEN v4, SHA-256 `33e5aa4e0fc01e07e5b1b7e6fe234e07be41e9c9b2c8edf9496af5572d9b398a` (verify the hash before you start; if it differs, stop and report). Its reviews are in `results/mathlab_staging/prereg_astra_r1–r4.md`; the folded requirements are binding. Where the prereg and this brief disagree, the prereg wins. Read the engine/harness source it cites before writing code against it (LAW#4: `cat -n`, author from what the code does, cite file:line).

## What to build (model-free, test-first)
1. `tools/mathlab_admit.py` — the fail-closed admission check of prereg §6, reusing only `check_fingerprint` / `check_gpu` from `tools/c10w_p2_gate.py` (never the P2 dispatcher).
2. The step-1 harvest: the pre-import shell launcher, the harvest driver, and the read-only observer of §2.1–2.3 (original-code-object matching, exactly five ordered captures per science write, LAW#5 tagging before the subject assertion, same-dtype CPU copy then CPU cast, source-unchanged checks), the wrapped-vs-unwrapped parity trial with restored weights + fresh zero cache, the LAW#3 baseline gates, the four-part tokenisation equivalence contract of §2.2 and the stage order (fresh A1/A2/A7 before mint replay). Output layout exactly as the prereg specifies, staging-only.
3. Step 2 and step 3 as marimo notebooks (plain `.py`, PEP 723 header with the frozen dependency set of §3; follow `~/.claude/skills/marimo-notebook/SKILL.md` and `marimo-batch/SKILL.md`), runnable headless via `uv run --script` exactly as §3 freezes it; frozen proxies, tolerances, bootstrap and the pass criterion of §4 implemented as specified, INVALID on bad arithmetic.
4. The DuckDB calibration index of §5 (derived, rebuildable, source path + JSON pointer + SHA per row).
5. Observability: every run emits events through `tools/mathlab_events.py` per `docs/MATHLAB_OBSERVABILITY_BRIEF.md` Part A (stages, progress, every pre-registered gate as a `gate_result` with plain words, resource samples, halts, staged findings). That module is being built right now by another Codex session (`codexml`) — do NOT create or edit it. Build everything else first; if it is not on disk when you reach integration, report that and stop at that point rather than writing a stand-in.

## Tests
Write the tests before the code. Unit tests with stubs and fixtures; no model load, no MPS. The GPU is in use by another experiment all night: any test that imports torch must be CPU-only and short, and nothing may dispatch the harvest. Include: observer frame-matching (rebound vs original), capture-count failures (0, 4, 6) halting, LAW#5 tagging order, conversion-safety self-test on offset/non-contiguous views (CPU tensors), admission refusals (probe error, autoresearch session, unaccounted process), tokenisation-contract failure scoping (shared → all mint arms INVALID-REPLAY; per-arm → that arm), proxy invalid arithmetic, bootstrap determinism, and the six-vs-nine ordering rule. A headless dry run of each notebook on fixture data.

## Constraints
- Engine, harness (`experiments/track_c/c10e_bandknob.py` etc.), `docs/MATHLAB_PREREG.md`, CORPUS, ledgers, runbook: read-only. The observer must not change what the harness computes (LAW#5).
- No `pip install` into `.venv`; use `uv run --with` / PEP 723. No commits. Don't restart dashboards or touch other sessions.
- Bad output looks like: a capture predicate on the rebound function; a silent `except: pass`; a tolerance or threshold not in the prereg; a notebook that only runs interactively; a stand-in events module.

## Report
A requirement → test → implementation table keyed to prereg section and line (like `results/c10x_enginepath_codex_build.md`), full test output, the exact harvest launch command (to be run later by the lead under the GPU gate), and every deviation or open question.
