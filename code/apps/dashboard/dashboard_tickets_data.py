"""One read-only snapshot of every ticket for the teamdash tickets tab.

Data contract: G-build/LEAN/teamdash/PLAN.md. Sources are ticket folders, ledgers, reviews,
the history CSV, git (read-only) and one `gh pr list` call. A failed source adds a line to
"errors"; it never drops a ticket and never stops the snapshot.
"""
import calendar
import csv
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import time

GH_ARGV = ["gh", "pr", "list", "--state", "all", "--limit", "300",
           "--json", "number,headRefName,state,createdAt,mergedAt,statusCheckRollup"]
AUTHORITY = ("ledger", "reflog", "history", "gh")  # time sources, highest authority first
FIELDS = ("dispatch", "pr_open", "merged")
MDT = dt.timezone(dt.timedelta(hours=-6))
UTC_FMT = "%Y-%m-%dT%H:%M:%SZ"
BLOCKING_RE = re.compile(r"^\s*\d+\.\s+\**BLOCKING\b")
SEPARATOR_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
MERGED_DETAIL_RE = re.compile(r"PR #\d+ MERGED")
TOKEN_RE = re.compile(r"`([^`]+)`|\b([A-Z]\d+[a-z]?)\b")


class SourceError(Exception):
    pass


def snapshot(folders, now=None, *, repo=None, gh=None):
    """Return the snapshot dict. `repo` is the git checkout; `gh(argv) -> (rc, stdout, stderr)`."""
    errors = []
    repo = Path(repo or os.environ.get("LLMDB_ROOT") or Path(__file__).resolve().parents[3])
    loaded, folder_rows = [], []
    for folder in map(Path, folders):
        rows = load_tickets(folder, errors)
        folder_rows.append({"path": str(folder), "label": folder.name, "tickets": len(rows)})
        loaded.extend((folder, row) for row in rows)
    ids = {row["id"] for _, row in loaded}
    merged_ids = git_merged_ids(repo, errors)
    branches = git_branches(repo, errors)
    reflog = {tid: git_reflog_time(repo, tid, errors) for tid in sorted(ids & branches)}
    prs = gh_prs(gh or default_gh(repo), errors)
    ledgers = {folder: read_ledger(folder / "ledger.tsv", errors) for folder in {f for f, _ in loaded}}
    history = read_history({f for f, _ in loaded}, errors)
    waves = compute_waves([row for _, row in loaded], errors)
    tickets = []
    for folder, row in loaded:
        tid, label = row["id"], folder.name
        pr = prs.get(tid)
        events = ledgers[folder].get(tid, [])
        hist = history.get((tid, label), history.get((tid, ""), {}))
        by_source = {"ledger": ledger_times(events), "reflog": {"dispatch": reflog.get(tid)},
                     "history": hist, "gh": gh_times(pr, errors)}
        times, source = pick_times(by_source)
        review_dir = find_review_dir(folder, tid)
        tickets.append(dict(row, label=label, wave=waves[tid],
                            state=ticket_state(tid, row["deps"], merged_ids, pr, branches),
                            pr=pr["number"] if pr else None, ci=ci_status(pr), times=times,
                            time_source=source, reviews=read_reviews(review_dir, errors),
                            ruling=read_ruling(review_dir, errors), events=events))
    return {"generated_epoch": float(time.time() if now is None else now), "folders": folder_rows,
            "errors": errors, "tickets": tickets}


def load_tickets(folder, errors):
    tdir = folder / "tickets"
    if not tdir.is_dir():
        errors.append("folder %s: no tickets/ directory" % folder)
        return []
    rows = []
    for path in sorted(tdir.glob("T*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("not a JSON object")
        except (OSError, ValueError) as exc:
            errors.append("ticket %s: %s" % (path, exc))
            data = {}
        rows.append({"id": str(data.get("id") or path.stem), "goal": str(data.get("goal", "")),
                     "deps": [str(x) for x in data.get("deps", [])], "astra": bool(data.get("astra", False)),
                     "write": [str(x) for x in data.get("write", [])], "test": str(data.get("test", "")),
                     "out": str(data.get("out", ""))})
    return rows


def compute_waves(rows, errors):
    deps = {}
    for row in rows:
        deps.setdefault(row["id"], row["deps"])
    waves, active = {}, set()

    def wave(tid):
        if tid in waves:
            return waves[tid]
        if tid in active:
            errors.append("deps: cycle through %s" % tid)
            return 0
        active.add(tid)
        waves[tid] = 1 + max([wave(d) for d in deps[tid] if d in deps] or [0])
        active.discard(tid)
        return waves[tid]

    return {tid: wave(tid) for tid in deps}


def ticket_state(tid, deps, merged_ids, pr, branches):
    if tid in merged_ids:
        return "merged"
    if pr and pr.get("state") == "OPEN":
        return "pr"
    if tid in branches:
        return "running"
    return "ready" if all(d in merged_ids for d in deps) else "waiting"


def pick_times(by_source):
    times, sources = {}, {}
    for field in FIELDS:
        found = [(s, by_source[s].get(field)) for s in AUTHORITY if by_source[s].get(field) is not None]
        times[field], sources[field] = found[0][1] if found else None, found[0][0] if found else None
    source = next((sources[f] for f in FIELDS if sources[f]), "none")
    return times, source


# ---- git (read-only) -------------------------------------------------------------------

def git(repo, *argv):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    try:
        proc = subprocess.run(["git", "-C", str(repo)] + list(argv), capture_output=True, text=True,
                              timeout=30, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SourceError("git %s: %s" % (argv[0], exc))
    if proc.returncode != 0:
        raise SourceError("git %s failed (rc %d): %s" % (argv[0], proc.returncode, last_line(proc.stderr)))
    return proc.stdout


def git_merged_ids(repo, errors):
    try:
        out = git(repo, "log", "origin/master", "--format=%s")
    except SourceError as exc:
        errors.append(str(exc))
        return set()
    return {line.split(":", 1)[0] for line in out.splitlines() if ":" in line}


def git_branches(repo, errors):
    try:
        out = git(repo, "for-each-ref", "--format=%(refname)", "refs/heads/tk/")
    except SourceError as exc:
        errors.append(str(exc))
        return set()
    return {line[len("refs/heads/tk/"):] for line in out.splitlines() if line.startswith("refs/heads/tk/")}


def git_reflog_time(repo, tid, errors):
    try:
        lines = git(repo, "reflog", "show", "--date=unix", "--format=%gd", "refs/heads/tk/" + tid).split()
    except SourceError as exc:
        errors.append(str(exc))
        return None
    if not lines:
        return None
    match = re.search(r"@\{(\d+)\}$", lines[-1])
    if not match:
        errors.append("git reflog tk/%s: unparsed line %r" % (tid, lines[-1]))
        return None
    return float(match.group(1))


# ---- gh (one call) ---------------------------------------------------------------------

def default_gh(repo):
    def run(argv):
        proc = subprocess.run(argv, cwd=str(repo), capture_output=True, text=True, timeout=60)
        return proc.returncode, proc.stdout, proc.stderr
    return run


def gh_prs(gh, errors):
    """Map ticket id -> its PR: the open one if any, else the highest number."""
    try:
        rc, out, err = gh(list(GH_ARGV))
        if rc != 0:
            raise SourceError("failed (rc %d): %s" % (rc, last_line(err)))
        data = json.loads(out)
        if not isinstance(data, list) or not all(isinstance(p, dict) for p in data):
            raise SourceError("output is not a list of PR objects")
    except (OSError, subprocess.SubprocessError, ValueError, SourceError) as exc:
        errors.append("gh pr list: %s" % exc)
        return {}
    prs = {}
    for pr in data:
        head = str(pr.get("headRefName") or "")
        if not head.startswith("tk/"):
            continue
        tid, old = head[3:], prs.get(head[3:])
        rank = (pr.get("state") == "OPEN", pr.get("number") or 0)
        if old is None or rank > (old.get("state") == "OPEN", old.get("number") or 0):
            prs[tid] = pr
    return prs


def gh_times(pr, errors):
    if not pr:
        return {}
    try:
        return {"pr_open": iso_epoch(pr.get("createdAt")), "merged": iso_epoch(pr.get("mergedAt"))}
    except (TypeError, ValueError) as exc:
        errors.append("gh pr #%s: bad time: %s" % (pr.get("number"), exc))
        return {}


def ci_status(pr):
    checks = (pr or {}).get("statusCheckRollup") or []
    if not checks:
        return "none"
    states = set()
    for check in checks:
        if "conclusion" in check or "status" in check:
            done = check.get("status") == "COMPLETED"
            states.add(check.get("conclusion") if done else "PENDING")
        else:
            states.add(check.get("state"))
    if states & {"FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STARTUP_FAILURE"}:
        return "fail"
    if states - {"SUCCESS", "NEUTRAL", "SKIPPED"}:
        return "pending"
    return "pass"


# ---- ledger and history ----------------------------------------------------------------

def read_ledger(path, errors):
    """Map ticket id -> events. A missing ledger is no data; a broken row is an error line."""
    if not path.is_file():
        return {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        errors.append("ledger %s: %s" % (path, exc))
        return {}
    events = {}
    for number, line in enumerate(lines, 1):
        if not line.strip() or (number == 1 and line.startswith("utc\t")):
            continue
        parts = line.split("\t", 4)
        try:
            if len(parts) != 5:
                raise ValueError("expected 5 tab-separated fields, got %d" % len(parts))
            stamp = float(calendar.timegm(time.strptime(parts[0], UTC_FMT)))
            event = {"t": stamp, "event": parts[2], "rc": int(parts[3]), "detail": parts[4]}
        except ValueError as exc:
            errors.append("ledger %s:%d: %s" % (path, number, exc))
            continue
        events.setdefault(parts[1], []).append(event)
    return events


def ledger_times(events):
    def first(match):
        return next((e["t"] for e in events if match(e)), None)
    return {"dispatch": first(lambda e: e["event"] == "dispatch" and e["rc"] == 0),
            "pr_open": first(lambda e: e["event"] == "close" and e["rc"] == 0),
            "merged": first(lambda e: e["event"] == "merged" and MERGED_DETAIL_RE.search(e["detail"]))}


def read_history(folders, errors):
    """Map (ticket, series) -> times from every metrics/tickets.csv above the folders (MDT, no year)."""
    paths = sorted({p / "metrics" / "tickets.csv" for f in folders for p in (f.parent, f.parent.parent)
                    if (p / "metrics" / "tickets.csv").is_file()})
    history = {}
    columns = (("dispatch", "dispatch_mdt"), ("pr_open", "pr_created_mdt"), ("merged", "merged_mdt"))
    for path in paths:
        try:
            year = dt.datetime.fromtimestamp(path.stat().st_mtime, MDT).year
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
        except (OSError, UnicodeDecodeError, csv.Error) as exc:
            errors.append("history %s: %s" % (path, exc))
            continue
        for number, row in enumerate(rows, 2):
            try:
                times = {field: mdt_epoch(row.get(col) or "", year) for field, col in columns}
            except ValueError as exc:
                errors.append("history %s:%d: %s" % (path, number, exc))
                continue
            history[(row.get("ticket") or "", row.get("series") or "")] = times
    return history


def mdt_epoch(text, year):
    if not text.strip():
        return None
    stamp = dt.datetime.strptime("%d-%s" % (year, text.strip()), "%Y-%m-%d %H:%M:%S")
    return stamp.replace(tzinfo=MDT).timestamp()


def iso_epoch(text):
    return float(calendar.timegm(time.strptime(text, UTC_FMT))) if text else None


# ---- reviews and rulings ---------------------------------------------------------------

def find_review_dir(folder, tid):
    for root in (folder / "reviews", folder.parent / "reviews", folder.parent / "recut" / "reviews"):
        if (root / tid).is_dir():
            return root / tid
    return None


def read_text(path, errors):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append("review %s: %s" % (path, exc))
        return ""


def read_reviews(review_dir, errors):
    """Rounds r1/, r2/, ... in order; a top-level verdict.md is the round after them (round 1 alone)."""
    if review_dir is None:
        return []
    rounds = sorted((int(p.name[1:]), p / "verdict.md") for p in review_dir.iterdir()
                    if re.fullmatch(r"r\d+", p.name) and (p / "verdict.md").is_file())
    paths = [p for _, p in rounds] + [p for p in [review_dir / "verdict.md"] if p.is_file()]
    return [dict(parse_verdict(read_text(p, errors)), round=i, path=str(p)) for i, p in enumerate(paths, 1)]


def parse_verdict(text):
    lines = text.splitlines()
    first = lines[0].strip() if lines else ""
    match = re.match(r"VERDICT:\s*(NO-GO|GO)\b", first)
    return {"verdict": match.group(1) if match else "NONE",
            "blocking": [line.replace("**", "").strip() for line in lines if BLOCKING_RE.match(line)],
            "notes": count_notes(lines), "mutants": count_mutants(lines)}


def count_notes(lines):
    count, inside = 0, False
    for line in lines:
        if not inside:
            inside = line.replace("*", "").strip().rstrip(":").lower() == "non-blocking notes"
        elif line.startswith("- "):
            count += 1
        elif line.strip() and not line[0].isspace():
            break
    return count


def count_mutants(lines):
    """Each table row counts once, by its last Killed/Survived cell; header rows are skipped."""
    counts = {"killed": 0, "survived": 0}
    for i, line in enumerate(lines):
        header = i + 1 < len(lines) and SEPARATOR_RE.match(lines[i + 1])
        if not line.strip().startswith("|") or SEPARATOR_RE.match(line) or header:
            continue
        result = None
        for cell in line.strip().strip("|").split("|"):
            cell = cell.replace("*", "").strip().lower()
            result = next((k for k in counts if cell.startswith(k)), result)
        if result:
            counts[result] += 1
    return counts


def read_ruling(review_dir, errors):
    path = review_dir / "RULING.md" if review_dir else None
    if path is None or not path.is_file():
        return {"path": None, "kill_set": [], "summary": ""}
    lines = read_text(path, errors).splitlines()
    summary = next((l.lstrip("#").strip() for l in lines if l.strip()), "")
    kill_set = []
    for line in lines:
        match = re.search(r"kill set[^:]*:(.*)", line, re.IGNORECASE)
        if match:
            sentence = re.split(r"\.(?:\s|$)", match.group(1))[0]
            for quoted, mutant in TOKEN_RE.findall(sentence):
                token = quoted or mutant
                if token not in kill_set:
                    kill_set.append(token)
    return {"path": str(path), "kill_set": kill_set, "summary": summary}


def last_line(text):
    lines = [l for l in (text or "").splitlines() if l.strip()]
    return lines[-1].strip() if lines else "(no output)"
