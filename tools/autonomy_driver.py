#!/usr/bin/env python3
"""Autonomy driver — bounded, no-HIL overnight experiment loop for the LLM-as-Database repo.

DESIGN (deliberately THIN — see advisor review 2026-06-19):
  - HARD wall-clock stop (a real deadline; the run cannot exceed --budget-min).
  - PREFLIGHT hard-gate (codex_context_guard preflight; NOT-READY aborts before any run).
  - Per-unit LOOP BOUND (max_loops) + per-unit timeout.
  - DETERMINISTIC label from a PRE-REGISTERED rule on the unit's result JSON
    (PASS / PARTIAL / FAIL / INVALID) — the driver never "decides" with judgment.
  - GATE LOG: standing-auth (model pulls / cov-compute / disk) PRE-APPROVED and noted;
    paid-provider + credential moves are GATED → logged to logs/autonomy_gates.jsonl, skipped.
  - CLOSEOUT TO STAGING: findings go to logs/pending_findings/NN_<unit>.md. The driver
    NEVER writes CORPUS/*, the append-only ledger, the runbook, or the checkpoint. The
    operator folds staged findings into the canonical §0.4 record on review.
  - AGENTIC DISCIPLINE: the obligation block is always emitted. In --mode agent (IMPLEMENTED)
    the driver shells a separate advisor CLI on each staged finding to attach an INDEPENDENT
    cross-family review (advisory — it never changes the deterministic pre-registered label;
    DISCIPLINE §3.1). Default advisor is Claude via local claude.ai subscription auth
    (`tools/claude_advisor.sh`); Codex/GPT remains an explicit fallback.

This is a guardrail harness, not a scientist. A clean FAIL on a pre-registered falsifier is
a SUCCESS for the run. Optimizer-style units (Goodhart-prone) are fenced: they may LOG
candidates, they may NOT write a conclusion (mission field "fenced": true).

Usage:
  python tools/autonomy_driver.py --mission tools/autonomy_mission.json [--budget-min 240]
                                  [--mode batch|agent] [--advisor claude|codex]
                                  [--dry-run] [--model <advisor-model>]
"""
from __future__ import annotations
import argparse, json, os, re, shlex, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[1]))
LOGS = ROOT / "logs"
STAGING = LOGS / "pending_findings"
GATES = LOGS / "autonomy_gates.jsonl"
# ---- cross-family review — advisory, never label-changing -------------------------------
ADVISOR_PROMPT = ROOT / "tools/advisor_review_prompt.md"
CLAUDE_ADVISOR = ROOT / "tools/claude_advisor.sh"
CLAUDE_BIN = os.environ.get("CLAUDE_BIN") or shutil.which("claude") or "/root/.local/bin/claude"
CODEX_HOME = os.environ.get("CODEX_HOME") or str(ROOT / ".codex")
CODEX_BIN = os.environ.get("CODEX_BIN") or shutil.which("codex") or str(ROOT / "bin/codex")
REVIEWABLE = ("PASS", "PARTIAL", "FAIL", "INVALID")   # ERROR/SKIPPED/DRY produced nothing to review

# ---- monotonic clock only (Date.now is fine here; this is a live process, not a workflow) ----
def now() -> float: return time.time()
def stamp(t: float) -> str: return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t))

def log_gate(kind: str, detail: str, decision: str):
    GATES.parent.mkdir(parents=True, exist_ok=True)
    with open(GATES, "a") as f:
        f.write(json.dumps({"t": stamp(now()), "kind": kind, "decision": decision, "detail": detail}) + "\n")

# ---- pre-registered deterministic label rule ------------------------------------------------
_OPS = [(">=", lambda a, b: a >= b), ("<=", lambda a, b: a <= b),
        (">", lambda a, b: a > b), ("<", lambda a, b: a < b), ("==", lambda a, b: a == b)]

class MissingField(Exception):
    """A pre-registered condition references a result field the run did not produce → INVALID, not FAIL."""

def _cond_key(cond: str) -> str:
    for sym, _ in _OPS:
        if sym in cond:
            return cond.split(sym, 1)[0].strip()
    raise ValueError(f"unparseable condition: {cond!r}")

def _check(cond: str, result: dict) -> bool:
    """cond like 'corruption_reduction_pp >= 10' evaluated against result-JSON fields.
    Raises MissingField if the referenced key is absent (so the labeler returns INVALID)."""
    for sym, fn in _OPS:
        if sym in cond:
            key = cond.split(sym, 1)[0].strip(); rhs = cond.split(sym, 1)[1].strip()
            if key not in result:
                raise MissingField(key)
            try:
                return fn(float(result[key]), float(rhs))
            except (TypeError, ValueError):
                raise MissingField(key)   # present but non-numeric → cannot evaluate → INVALID
    raise ValueError(f"unparseable condition: {cond!r}")

def label_result(rule: dict, result: dict) -> tuple[str, list[str]]:
    """Returns (LABEL, reasons). Guard first → INVALID; then PASS; then PARTIAL; else FAIL.
    Every clause is a pre-registered string condition on result-JSON fields — fully deterministic."""
    reasons = []
    try:
        for g in rule.get("guard", []):
            ok = _check(g, result)
            reasons.append(f"guard[{g}]={'ok' if ok else 'FAIL'}")
            if not ok:
                return "INVALID", reasons          # guard failed = confounded comparison
        if rule.get("pass") and all(_check(c, result) for c in rule["pass"]):
            reasons += [f"pass[{c}]=ok" for c in rule["pass"]]
            return "PASS", reasons
        if rule.get("partial") and all(_check(c, result) for c in rule["partial"]):
            reasons += [f"partial[{c}]=ok" for c in rule["partial"]]
            return "PARTIAL", reasons
        return "FAIL", reasons                      # tested, criteria not met = real negative result
    except MissingField as m:
        reasons.append(f"INVALID: result missing/non-numeric field '{m}' — run did not produce the metric")
        return "INVALID", reasons

# ---- run one shell command with a hard timeout ----------------------------------------------
def run_cmd(cmd: str, env: dict, timeout: int, dry: bool) -> dict:
    if dry:
        return {"rc": 0, "dry": True, "cmd": cmd}
    try:
        p = subprocess.run(cmd, shell=True, cwd=ROOT, env={**os.environ, **env},
                           capture_output=True, text=True, timeout=timeout)
        return {"rc": p.returncode, "stdout": p.stdout[-4000:], "stderr": p.stderr[-4000:]}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "timeout": True, "stderr": f"timed out after {timeout}s"}

# ---- cross-family independent review via Codex (advisory; NEVER changes the label) ----------
def run_codex_review(finding_text: str, model: str | None, timeout: int) -> str:
    """Independent cross-family (out-of-Opus) review of a STAGED finding via `codex exec`.
    Returns a markdown section. NEVER raises; NEVER changes the deterministic pre-registered
    label (DISCIPLINE §3.1: pre-registered labels only; review is advisory input for the
    supervised fold-in). Codex runs in THIS pod process (has network); it cannot be called from
    Claude's network-sandboxed tools — that is why this lives in the driver."""
    if not (Path(CODEX_BIN).exists() or shutil.which("codex")):
        return "## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_codex binary not found; run `tools/setup_codex.sh`._"
    try:
        rubric = ADVISOR_PROMPT.read_text()
    except Exception:
        rubric = ("You are an independent adversarial reviewer. Give a one-word verdict "
                  "PROCEED / FIX-FIRST / OVERTURNED-OR-RECONSIDER, then the single most important "
                  "next step, then issues in priority order. Be a skeptic; do not rubber-stamp.")
    prompt = (rubric +
        "\n\n---\nREVIEW TARGET — a STAGED autonomy finding (cross-family / out-of-Opus review). "
        "Numbers are prompt-provided (treat as claims tied to the named result JSON; you may lack file "
        "access). Judge the disposition; do NOT change the pre-registered LABEL (advisory only). Skeptic.\n\n"
        + finding_text)
    out_file = LOGS / f".codex_review_{int(now())}.txt"
    cmd = [CODEX_BIN, "exec", "--skip-git-repo-check", "-o", str(out_file)]
    if model:
        cmd += ["-m", model]
    cmd += [prompt]
    env = {**os.environ, "CODEX_HOME": CODEX_HOME,
           "PATH": f"{ROOT}/bin:" + os.environ.get("PATH", "")}
    try:
        pr = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_codex timed out after {timeout}s (review skipped; not fatal)._"
    except Exception as e:
        return f"## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_codex spawn error: {e}._"
    verdict = ""
    try:
        if out_file.exists():
            verdict = out_file.read_text().strip(); out_file.unlink()
    except Exception:
        pass
    if not verdict:
        verdict = (pr.stdout or pr.stderr or "").strip()[-4000:]
    if not verdict:
        return f"## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_codex rc={pr.returncode}, no output._"
    mid = model or "gpt-5.5 (config default)"
    return (f"## CROSS-FAMILY REVIEW (advisory — does NOT change the pre-registered LABEL; "
            f"independent {mid} via Codex, {stamp(now())})\n"
            f"> Auto-satisfies DISCIPLINE §3.1 obligation #4 (independent cross-model review) for this "
            f"finding. The supervised fold-in still verifies numbers + promotes.\n\n" + verdict)

# ---- cross-family independent review via Claude subscription auth ---------------------------
def run_claude_review(finding_text: str, model: str | None, effort: str, timeout: int) -> str:
    """Independent cross-family review for Codex-authored/staged work via Claude Code.
    Uses tools/claude_advisor.sh, which requires claude.ai subscription auth and refuses
    API-key auth. NEVER raises; NEVER changes the deterministic pre-registered label."""
    if not CLAUDE_ADVISOR.exists():
        return "## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_tools/claude_advisor.sh not found._"
    if not (Path(CLAUDE_BIN).exists() or shutil.which("claude")):
        return "## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_claude binary not found; install/login Claude Code._"
    env = {**os.environ,
           "LLMDB_ROOT": str(ROOT),
           "CLAUDE_BIN": str(CLAUDE_BIN),
           "CLAUDE_ADVISOR_MODEL": model or os.environ.get("CLAUDE_ADVISOR_MODEL", "opus"),
           "CLAUDE_ADVISOR_EFFORT": effort or os.environ.get("CLAUDE_ADVISOR_EFFORT", "high")}
    try:
        pr = subprocess.run([str(CLAUDE_ADVISOR)], cwd=ROOT, env=env, input=finding_text,
                            capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_claude advisor timed out after {timeout}s (review skipped; not fatal)._"
    except Exception as e:
        return f"## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_claude advisor spawn error: {e}._"
    verdict = (pr.stdout or "").strip()
    if pr.returncode != 0:
        err = (pr.stderr or verdict or "").strip()[-4000:]
        return f"## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_claude advisor rc={pr.returncode}: {err}_"
    if not verdict:
        return "## CROSS-FAMILY REVIEW — UNAVAILABLE\n\n_claude advisor produced no output._"
    mid = env["CLAUDE_ADVISOR_MODEL"]
    return (f"## CROSS-FAMILY REVIEW (advisory — does NOT change the pre-registered LABEL; "
            f"independent Claude/{mid} via claude.ai subscription CLI, {stamp(now())})\n"
            f"> Auto-satisfies DISCIPLINE §3.1 obligation #4 (independent cross-family review) for "
            f"Codex-led work. The supervised fold-in still verifies numbers + promotes.\n\n" + verdict)

# ---- staging write (NEVER canonical) --------------------------------------------------------
def stage_finding(idx: int, unit: dict, label: str, reasons: list[str], result: dict | None, attempts: int):
    STAGING.mkdir(parents=True, exist_ok=True)
    path = STAGING / f"{idx:02d}_{unit['id']}.md"
    obligations = [
        "OPERATOR / REVIEW OBLIGATIONS before this becomes canonical (DISCIPLINE §0.4):",
        "  1. Verify the EXACT command + result fields below reproduce.",
        "  2. If LABEL≠PASS: a deep-thinking-on-failure pass (DISCIPLINE §2) — what confound/alt-mechanism?",
        "  3. Autoresearch / external-evidence check IF the failure is a dead-end (bounded; §3 thresholds).",
        "  4. Independent (cross-family) advisor-review — self-review by the run model is NOT independent. "
        "(AUTO-DONE below in --mode agent: Claude subscription-backed review is appended by default; Codex is fallback.)",
        "  5. Only then fold into CORPUS/NN + 00/03 + runbook §0.3/§12/§13 + checkpoint + memory.",
    ]
    fenced = unit.get("fenced", False)
    body = [
        f"# STAGED finding — {unit['id']} — {label}",
        f"_Unattended autonomy run. STAGING ONLY — not canonical. Generated {stamp(now())}._",
        "",
        f"**Hypothesis (pre-registered):** {unit['hypothesis']}",
        f"**Falsifier framing:** {unit.get('falsifier','(none stated)')}",
        f"**Fenced (optimizer — may NOT write a conclusion):** {fenced}",
        f"**Command:** `{unit['command']}`",
        f"**Attempts:** {attempts} / max {unit['max_loops']}",
        "",
        "## Pre-registered label rule",
        "```json", json.dumps(unit["label_rule"], indent=2), "```",
        f"**LABEL = {label}**  ({'; '.join(reasons)})",
    ]
    if fenced and label == "PASS":
        body.append("> FENCED unit: PASS here means 'candidate worth a pre-registered falsifier' — NOT a conclusion. Do not record as evidence.")
    body += ["", "## Result JSON", "```json", json.dumps(result, indent=2) if result else "(no result JSON produced)", "```",
             "", "## " + obligations[0], *[o for o in obligations[1:]]]
    path.write_text("\n".join(body))
    return path

# ---- main loop ------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mission", default=str(ROOT / "tools/autonomy_mission.json"))
    ap.add_argument("--budget-min", type=float, default=240.0)
    ap.add_argument("--mode", choices=["batch", "agent"], default="batch")
    ap.add_argument("--advisor", choices=["claude", "codex"], default=os.environ.get("LLMDB_ADVISOR", "claude"), help="advisor backend for --mode agent")
    ap.add_argument("--model", default=None, help="advisor model for --mode agent (Claude default: opus; Codex default: config/gpt-5.5)")
    ap.add_argument("--effort", default=os.environ.get("CLAUDE_ADVISOR_EFFORT", "high"), help="Claude advisor effort for --advisor claude")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    mission = json.loads(Path(args.mission).read_text())
    t0 = now(); deadline = t0 + args.budget_min * 60
    LOGS.mkdir(parents=True, exist_ok=True)
    report = LOGS / f"autonomy_run_{stamp(t0).replace(':','').replace('-','')}.md"
    out = [f"# Autonomy run — {mission.get('name','(unnamed)')}",
           f"start={stamp(t0)} budget={args.budget_min}min mode={args.mode} dry={args.dry_run}",
           f"mission={args.mission}", ""]

    # PREFLIGHT hard-gate
    guard = ROOT / "tools/codex_context_guard.py"
    pf = subprocess.run([sys.executable, str(guard), "preflight"], cwd=ROOT, capture_output=True, text=True)
    out += ["## Preflight", "```", pf.stdout.strip(), "```"]
    if pf.returncode != 0 and not args.dry_run:
        out += ["", "**ABORT: preflight NOT-READY — pod not safe to run. No units executed.**"]
        report.write_text("\n".join(out)); print(f"ABORT (preflight). report={report}"); return 2

    results = []
    for idx, unit in enumerate(mission["units"], 1):
        if now() >= deadline:
            out.append(f"\n## {unit['id']}: SKIPPED — wall-clock budget exhausted."); results.append((unit["id"], "SKIPPED")); continue
        out.append(f"\n## Unit {idx}: {unit['id']}  (fenced={unit.get('fenced', False)})")
        # Default is ERROR, NOT FAIL — a unit that never produced a usable result is an INFRA
        # failure, never a scientific 'FAIL'. FAIL is reserved for a valid result that missed the bar.
        attempts, label, reasons, result = 0, "ERROR", ["unit did not run"], None
        per_unit_timeout = int(unit.get("timeout_s", 1800))
        rj = ROOT / unit["label_rule"]["result_json"]
        if rj.exists() and not args.dry_run:  # stale-result guard: a prior night's JSON must not be read
            try: rj.unlink()                  # NEVER in --dry-run: nothing regenerates it → would destroy a real artifact
            except Exception: pass
        while attempts < unit["max_loops"] and now() < deadline:
            remaining = deadline - now()
            if remaining < unit.get("min_s_to_start", 120):
                out.append(f"  attempt skipped — only {int(remaining)}s left < min_s_to_start.")
                if label == "ERROR": label, reasons = "ERROR", ["insufficient wall-clock to start/finish an attempt"]
                break
            attempts += 1
            log_gate("model-pull/compute", f"{unit['id']} attempt {attempts}: {unit['command']}", "PRE-APPROVED (standing-auth)")
            r = run_cmd(unit["command"], unit.get("env", {}), min(per_unit_timeout, int(remaining)), args.dry_run)
            out.append(f"  attempt {attempts}: rc={r.get('rc')} {'(dry)' if r.get('dry') else ''}{' TIMEOUT' if r.get('timeout') else ''}")
            if args.dry_run:
                label, reasons = "DRY", ["dry-run: no result evaluated"]; break
            if r.get("rc") == 0 and rj.exists():
                try:
                    result = json.loads(rj.read_text())
                except Exception as e:
                    result = None; out.append(f"    result JSON unreadable: {e}")
                if result is not None:
                    label, reasons = label_result(unit["label_rule"], result)
                    out.append(f"    label={label} ({'; '.join(reasons)})")
                    break          # a VALID result of ANY label (PASS/PARTIAL/FAIL/INVALID) is TERMINAL —
                                   # never re-run a deterministic comparison just to chase a different label
            # no usable result this attempt → INFRA failure (rc≠0 / timeout / missing / unreadable JSON).
            # NOT a scientific FAIL. Retry only because nothing usable was produced (transient-retry).
            result = None
            label, reasons = "ERROR", [f"infra failure (not a scientific result): rc={r.get('rc')}, "
                                       f"timeout={r.get('timeout', False)}, json_exists={rj.exists()}"
                                       + (f"; retrying ({attempts}/{unit['max_loops']})" if attempts < unit['max_loops'] else "; loops exhausted")]
            out.append(f"    {reasons[0]}")
        path = stage_finding(idx, unit, label, reasons, result, attempts)
        out.append(f"  → staged: {path.relative_to(ROOT)}")
        # --mode agent: append an independent cross-family review (advisory; never the label) --
        if args.mode == "agent" and label in REVIEWABLE:
            remaining = deadline - now()
            rtimeout = min(int(unit.get("review_timeout_s", 240)), max(30, int(remaining)))
            if remaining > 45:
                if args.advisor == "claude":
                    review = run_claude_review(path.read_text(), args.model, args.effort, rtimeout)
                    reviewer = f"Claude/{args.model or os.environ.get('CLAUDE_ADVISOR_MODEL', 'opus')}"
                else:
                    review = run_codex_review(path.read_text(), args.model, rtimeout)
                    reviewer = f"Codex/{args.model or 'gpt-5.5'}"
                with open(path, "a") as f:
                    f.write("\n\n---\n" + review + "\n")
                out.append(f"  → cross-family review appended ({reviewer})")
            else:
                out.append("  → cross-family review SKIPPED (wall-clock < 45s)")
        elif args.mode == "agent":
            out.append(f"  → cross-family review skipped (label={label}: nothing to review)")
        results.append((unit["id"], label))

    # CLOSEOUT (to staging posture; never canonical)
    co = subprocess.run([sys.executable, str(guard), "closeout"], cwd=ROOT, capture_output=True, text=True)
    out += ["\n## Closeout", "```", co.stdout.strip(), "```",
            f"\n## Summary  (elapsed {int((now()-t0)/60)}min / budget {args.budget_min}min)"]
    out += [f"- {uid}: **{lab}**" for uid, lab in results]
    out += ["", "Findings are STAGED in logs/pending_findings/. Operator review required before any canonical §0.4 fold.",
            f"Gate log: logs/autonomy_gates.jsonl"]
    report.write_text("\n".join(out))
    print(f"DONE. {len(results)} unit(s). report={report.relative_to(ROOT)}")
    for uid, lab in results: print(f"  {uid}: {lab}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
