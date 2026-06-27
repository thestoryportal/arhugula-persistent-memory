#!/usr/bin/env python3
"""Repo-local experiment assurance gate for LLM-as-Database runs.

This is a thin workflow guard. It does not choose scientific verdicts, write
CORPUS, or replace closeout_check.py. It checks that the evidence package is
ready for review: prereg present, saved JSON freshly readable, per-unit stats
reviewable when a result is claimed, method ports gated by easy controls, and
review status explicit before handoff.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
LOG_DIR = ROOT / "logs" / "experiment_gate"
TEMPLATE = TOOLS / "skills" / "experiment-gate" / "assets" / "prereg_template.md"

sys.path.insert(0, str(TOOLS))
import stats as stats_lib  # noqa: E402


PREREG_SECTIONS = {
    "hypothesis": ("any", [r"\bhypothesis\b", r"\bfalsifiable\b"]),
    "metric": ("any", [r"\bmetric\b", r"\bbinding\b"]),
    "thresholds": ("all", [r"\bpass\b", r"\bpartial\b", r"\bfail\b", r"\binvalid\b"]),
    "power": ("any", [r"\bpower\b", r"\bmde\b", r"tools/power\.py"]),
    "confounders": ("any", [r"\bconfound", r"\bcontrol"]),
    "advisor": ("any", [r"\badvisor", r"\bcross-family", r"\breview"]),
    "artifacts": ("any", [r"\bresults?/", r"\blogs?/", r"\bartifact"]),
    "abort": ("any", [r"\babort\b", r"\bstop\b", r"\binvalid\b"]),
}

PER_UNIT_METRICS = ("correct", "maxprob", "js_vs_pre", "value")
METHOD_REQUIRED = (
    "upstream_commit",
    "upstream_hparams",
    "declared_deviations",
    "active_trace",
    "easy_controls",
    "behavior_thresholds",
)
ACTIVE_TRACE_REQUIRED = (
    "token_ids",
    "lookup_or_edit_positions",
    "target_norms",
    "delta_norms",
    "update_norms",
    "logit_deltas",
    "behavior",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def read_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def sanitize_json(value: Any) -> Any:
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    if isinstance(value, dict):
        return {k: sanitize_json(v) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize_json(v) for v in value]
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(sanitize_json(payload), f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")


def emit(payload: dict[str, Any]) -> int:
    print(json.dumps(sanitize_json(payload), indent=2, sort_keys=True, allow_nan=False))
    return 1 if payload.get("gate_status") == "BLOCKED" else 0


def check_prereg(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {
        "checked_at": now_iso(),
        "path": rel(path),
        "kind": "prereg_check",
        "checks": {},
    }
    if not path.exists():
        out["gate_status"] = "BLOCKED"
        out["error"] = "prereg file missing"
        return out
    text = path.read_text(errors="replace")
    lower = text.lower()
    missing: list[str] = []
    for name, (mode, patterns) in PREREG_SECTIONS.items():
        matches = [bool(re.search(p, lower)) for p in patterns]
        ok = all(matches) if mode == "all" else any(matches)
        out["checks"][name] = ok
        if not ok:
            missing.append(name)
    out["gate_status"] = "PASS" if not missing else "BLOCKED"
    out["missing_sections"] = missing
    out["note"] = (
        "Presence check only. The scientific content still needs advisor-review "
        "and the normal prereg discipline."
    )
    return out


def _cluster_for(row: dict[str, Any]) -> str | None:
    if row.get("cluster") is not None:
        return str(row["cluster"])
    if row.get("seed") is not None and row.get("order") is not None:
        return f"{row['seed']}|{row['order']}"
    return None


def _per_unit_stats(rows: list[dict[str, Any]]) -> dict[str, Any]:
    arms: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        arm = row.get("arm")
        cluster = _cluster_for(row)
        if arm is None or cluster is None:
            continue
        arms[str(arm)].append(row)
    metrics = sorted({m for row in rows for m in PER_UNIT_METRICS if m in row})
    report: dict[str, Any] = {
        "shape": "per_unit",
        "n_rows": len(rows),
        "arms": sorted(arms),
        "metrics": metrics,
        "metric_reports": {},
    }
    if not arms or not metrics:
        report["REFUSED"] = True
        report["reason"] = "per_unit rows need arm, cluster/seed+order, and at least one metric"
        return report
    for metric in metrics:
        metric_report: dict[str, Any] = {"per_arm": {}}
        for arm, arm_rows in arms.items():
            values = [float(r[metric]) for r in arm_rows if metric in r]
            clusters = [_cluster_for(r) for r in arm_rows if metric in r]
            if not values:
                continue
            metric_report["per_arm"][arm] = stats_lib.cluster_bootstrap_mean(
                values, clusters, nboot=4000, seed=0
            )
        if len(metric_report["per_arm"]) == 2:
            (arm_a, rep_a), (arm_b, rep_b) = list(metric_report["per_arm"].items())
            vals_a = [float(r[metric]) for r in arms[arm_a] if metric in r]
            cls_a = [_cluster_for(r) for r in arms[arm_a] if metric in r]
            vals_b = [float(r[metric]) for r in arms[arm_b] if metric in r]
            cls_b = [_cluster_for(r) for r in arms[arm_b] if metric in r]
            metric_report["diff"] = {
                "arm_a": arm_a,
                "arm_b": arm_b,
                "stats": stats_lib.cluster_bootstrap_diff(
                    vals_a, cls_a, vals_b, cls_b, nboot=4000, seed=0
                ),
            }
        report["metric_reports"][metric] = metric_report
    refused = []
    for metric_report in report["metric_reports"].values():
        for arm_report in metric_report.get("per_arm", {}).values():
            if arm_report.get("REFUSED"):
                refused.append(arm_report.get("reason", "stats refused"))
        diff = metric_report.get("diff", {}).get("stats")
        if isinstance(diff, dict) and diff.get("REFUSED"):
            refused.append(diff.get("reason", "diff stats refused"))
    if refused:
        report["REFUSED"] = True
        report["reason"] = "; ".join(sorted(set(refused)))
    return report


def check_result(path: Path, stats_out: Path | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {
        "checked_at": now_iso(),
        "path": rel(path),
        "kind": "result_check",
    }
    if not path.exists():
        out["gate_status"] = "BLOCKED"
        out["error"] = "result JSON missing"
        return out
    try:
        data = read_json(path)
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        out["gate_status"] = "BLOCKED"
        out["error"] = f"result JSON unreadable: {exc}"
        return out
    out["json_readback"] = "ok"
    out["top_level_keys"] = sorted(data.keys()) if isinstance(data, dict) else []
    if isinstance(data, dict) and isinstance(data.get("per_unit"), list):
        stats_report = _per_unit_stats(data["per_unit"])
    elif isinstance(data, dict):
        stats_report = stats_lib.analyze_result(str(path))
    else:
        stats_report = {"REFUSED": True, "reason": "top-level result JSON is not an object"}
    out["stats_report"] = stats_report
    stats_path = stats_out or LOG_DIR / f"{path.stem}_stats.json"
    write_json(stats_path, stats_report)
    out["stats_artifact"] = rel(stats_path)
    if stats_report.get("REFUSED"):
        out["gate_status"] = "BLOCKED"
        out["error"] = "fresh stats refused; result is not reviewable for a completion claim"
    else:
        out["gate_status"] = "PASS"
    return out


def _easy_control_pass(control: Any) -> bool:
    if isinstance(control, dict):
        if control.get("pass") is True or control.get("passed") is True:
            return True
        if control.get("status") in ("PASS", "CONTROLLED"):
            return True
    return False


def audit_method_port(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {
        "checked_at": now_iso(),
        "path": rel(path),
        "kind": "method_port_audit",
    }
    if not path.exists():
        out["gate_status"] = "BLOCKED"
        out["error"] = "method-port packet missing"
        return out
    try:
        data = read_json(path)
    except Exception as exc:  # pragma: no cover - defensive CLI guard
        out["gate_status"] = "BLOCKED"
        out["error"] = f"method-port packet unreadable: {exc}"
        return out
    missing = [k for k in METHOD_REQUIRED if k not in data]
    trace = data.get("active_trace") if isinstance(data.get("active_trace"), dict) else {}
    missing_trace = [k for k in ACTIVE_TRACE_REQUIRED if k not in trace]
    controls = data.get("easy_controls")
    easy_controls = controls if isinstance(controls, list) else []
    easy_pass = bool(easy_controls) and all(_easy_control_pass(c) for c in easy_controls)
    hard_case_licensed = bool(data.get("hard_case_licensed"))
    failures = []
    if missing:
        failures.append(f"missing required fields: {', '.join(missing)}")
    if missing_trace:
        failures.append(f"active_trace missing fields: {', '.join(missing_trace)}")
    if not easy_pass:
        failures.append("easy_controls are absent or not all PASS")
    if hard_case_licensed and not easy_pass:
        failures.append("hard_case_licensed=true before easy controls pass")
    out.update(
        {
            "upstream_commit": data.get("upstream_commit"),
            "declared_deviations_count": len(data.get("declared_deviations", []))
            if isinstance(data.get("declared_deviations"), list)
            else None,
            "easy_controls_pass": easy_pass,
            "hard_case_licensed": hard_case_licensed,
            "missing_fields": missing,
            "missing_active_trace_fields": missing_trace,
            "failures": failures,
        }
    )
    out["gate_status"] = "PASS" if not failures else "BLOCKED"
    return out


def init_prereg(d_id: str, out_path: Path | None = None) -> dict[str, Any]:
    dest = out_path or ROOT / "docs" / f"{d_id}_PREREG.md"
    if dest.exists():
        return {
            "checked_at": now_iso(),
            "kind": "init",
            "gate_status": "PASS",
            "path": rel(dest),
            "note": "file already exists; not overwritten",
        }
    if not TEMPLATE.exists():
        return {
            "checked_at": now_iso(),
            "kind": "init",
            "gate_status": "BLOCKED",
            "error": f"template missing: {rel(TEMPLATE)}",
        }
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = TEMPLATE.read_text().replace("{{D_ID}}", d_id)
    dest.write_text(text)
    return {"checked_at": now_iso(), "kind": "init", "gate_status": "PASS", "path": rel(dest)}


def bundle(args: argparse.Namespace) -> dict[str, Any]:
    d_id = args.d_id
    prereg = args.prereg or ROOT / "docs" / f"{d_id}_PREREG.md"
    package: dict[str, Any] = {
        "created_at": now_iso(),
        "kind": "experiment_gate_package",
        "d_id": d_id,
        "gate_status": "PASS",
        "checks": {},
        "review_status": args.review_status,
        "closeout_handoff": "Run python3 tools/closeout_check.py <D-ID> after CORPUS/tracker closeout.",
        "corpus_written_by_gate": False,
    }
    prereg_check = check_prereg(prereg)
    package["checks"]["prereg"] = prereg_check
    if prereg_check.get("gate_status") != "PASS":
        package["gate_status"] = "BLOCKED"
    if args.result:
        result_check = check_result(args.result)
        package["checks"]["result"] = result_check
        if result_check.get("gate_status") != "PASS":
            package["gate_status"] = "BLOCKED"
    if args.method_port:
        method_check = audit_method_port(args.method_port)
        package["checks"]["method_port"] = method_check
        if method_check.get("gate_status") != "PASS":
            package["gate_status"] = "BLOCKED"
    if args.review_status != "both_done" and not args.allow_pending_review:
        package["gate_status"] = "BLOCKED"
        package["checks"]["review"] = {
            "gate_status": "BLOCKED",
            "reason": "bundle handoff requires --review-status both_done or --allow-pending-review",
        }
    else:
        package["checks"]["review"] = {"gate_status": "PASS", "review_status": args.review_status}
    out_path = args.out or LOG_DIR / f"{d_id}_gate_package.json"
    write_json(out_path, package)
    package["package_path"] = rel(out_path)
    return package


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="LLM-as-Database experiment assurance gate.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="scaffold docs/<D-ID>_PREREG.md from template")
    p_init.add_argument("d_id")
    p_init.add_argument("--out", type=Path)

    p_pr = sub.add_parser("check-prereg", help="check required prereg sections are present")
    p_pr.add_argument("path", type=Path)

    p_res = sub.add_parser("check-result", help="fresh-read a result JSON and compute/refuse stats")
    p_res.add_argument("path", type=Path)
    p_res.add_argument("--stats-out", type=Path)

    p_mp = sub.add_parser("audit-method-port", help="hard gate for external method port packets")
    p_mp.add_argument("path", type=Path)

    p_b = sub.add_parser("bundle", help="build a handoff package; never writes CORPUS")
    p_b.add_argument("d_id")
    p_b.add_argument("--prereg", type=Path)
    p_b.add_argument("--result", type=Path)
    p_b.add_argument("--method-port", type=Path)
    p_b.add_argument("--review-status", choices=("pending", "advisor_done", "cross_family_done", "both_done"), default="pending")
    p_b.add_argument("--allow-pending-review", action="store_true")
    p_b.add_argument("--out", type=Path)

    args = ap.parse_args(argv)
    if args.cmd == "init":
        return emit(init_prereg(args.d_id, args.out))
    if args.cmd == "check-prereg":
        return emit(check_prereg(args.path))
    if args.cmd == "check-result":
        return emit(check_result(args.path, args.stats_out))
    if args.cmd == "audit-method-port":
        return emit(audit_method_port(args.path))
    if args.cmd == "bundle":
        return emit(bundle(args))
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    sys.exit(main())
