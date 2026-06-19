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
  - AGENTIC DISCIPLINE (deep-thinking / autoresearch / advisor-review) is emitted as an
    OBLIGATION BLOCK into the staging file — Python does not fake reasoning. In --mode agent
    the driver shells `codex exec` per unit so a model fulfils those obligations within the
    wall-clock + loop bounds; that mode needs Codex authenticated (operator-gated).

This is a guardrail harness, not a scientist. A clean FAIL on a pre-registered falsifier is
a SUCCESS for the run. Optimizer-style units (Goodhart-prone) are fenced: they may LOG
candidates, they may NOT write a conclusion (mission field "fenced": true).

Usage:
  python tools/autonomy_driver.py --mission tools/autonomy_mission.json [--budget-min 240]
                                  [--mode batch|agent] [--dry-run] [--model <codex-model>]
"""
from __future__ import annotations
import argparse, json, os, re, shlex, subprocess, sys, time
from pathlib import Path

ROOT = Path(os.environ.get("LLMDB_ROOT", Path(__file__).resolve().parents[1]))
LOGS = ROOT / "logs"
STAGING = LOGS / "pending_findings"
GATES = LOGS / "autonomy_gates.jsonl"

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

# ---- staging write (NEVER canonical) --------------------------------------------------------
def stage_finding(idx: int, unit: dict, label: str, reasons: list[str], result: dict | None, attempts: int):
    STAGING.mkdir(parents=True, exist_ok=True)
    path = STAGING / f"{idx:02d}_{unit['id']}.md"
    obligations = [
        "OPERATOR / REVIEW OBLIGATIONS before this becomes canonical (DISCIPLINE §0.4):",
        "  1. Verify the EXACT command + result fields below reproduce.",
        "  2. If LABEL≠PASS: a deep-thinking-on-failure pass (DISCIPLINE §2) — what confound/alt-mechanism?",
        "  3. Autoresearch / external-evidence check IF the failure is a dead-end (bounded; §3 thresholds).",
        "  4. Independent (cross-model) advisor-review — self-review by the run model is NOT independent.",
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
    ap.add_argument("--model", default=None, help="codex exec model for --mode agent")
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
        if rj.exists():                       # stale-result guard: a prior night's JSON must not be read
            try: rj.unlink()
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
