"""Live state for the team dashboard, derived from the program's own records on every redraw, never typed by hand:
operator rulings awaited (runbook §5.2 rows whose status says "awaiting operator"), the GPU job or the last
coordinator outcome, Codex builds that are working, running helper agents, and the events newer than the
hand-written report text. Also: panes reload themselves when dashboard code changes, and the team tab is rebuilt
when team sessions start or end. Pure functions first; gather() and the effects at the bottom.
"""
import glob, os, re, subprocess, sys, time
from datetime import datetime

TOOLS = os.path.dirname(os.path.abspath(__file__))
# The one definition of a C10 GPU-job process and its stage: a driver (experiments/track_c/c10?_*.py <stage>),
# a program tool (tools/c10?_*.py <verb>, e.g. the P2 re-attempt evaluator) or a stage wrapper (tools/run_c10?*_stage.sh <stage>).
# The experiment tab and the status bar read the same pattern, so they cannot disagree about whether the GPU is busy.
GPU_JOB_RE = re.compile(r"(?:experiments/track_c/|tools/(?:run_)?)(c10[a-z])\w*?(?:\.py|_stage\.sh) ([\w-]+)")
# The one definition of "an agent pane is busy": a Codex/Claude spinner line, or Codex's slow-model menu, which keeps
# waiting by itself ("Codex will keep waiting") and must not read as finished. Tiles and the watcher both use it.
BUSY_RE = re.compile(r"esc to interrupt|Working \(|· Working ·|Codex will keep waiting|^[^\w\s]\s\S+… \(\d", re.M)   # "· Working ·" = Codex footer status, present even between steps
INTERPRETER_RE = re.compile(r"(?i)^(python[0-9.]*|bash|sh)$")
TEMP_ROOTS = ("/private/tmp/", "/tmp/", "/private/var/folders/", "/var/folders/")


def script_call(command):
    """The "script arg …" an interpreter is running, or None. Only python/bash/sh as the executable count, and only
    their non-flag arguments are read, so a script path quoted inside another program's arguments (an agent's
    prompt, a tool one-liner) is never mistaken for a running GPU job."""
    parts = command.split()
    args = [a for a in parts[1:] if not a.startswith("-")]
    if not parts or not INTERPRETER_RE.match(os.path.basename(parts[0])) or not args or args[0].startswith(TEMP_ROOTS):
        return None   # selftests run copies under temp roots and never use the GPU
    return " ".join(args)


ROOT = os.path.dirname(TOOLS)
SHORT = {"c10u": "Step 3", "c10v": "Step 4", "c10w": "Step 5", "c10x": "Step 6", "c10y": "Step 7", "c10z": "ASTRA"}
NOT_TEAM = {"dashboard", "dashboard_new", "helpers"}
ROW = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*([^|]*)\|")


def awaiting_rulings(runbook_text):
    """Titles of decision-ledger rows whose status cell says they await the operator."""
    out = []
    for line in runbook_text.splitlines():
        m = ROW.match(line)
        if m and re.search(r"awaiting operator", m.group(2), re.I):
            out.append(m.group(1).strip())
    return out


def iso_epoch(stamp):
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S%z").timestamp()


def coordinator_exit(log_text):
    """The last COORDINATOR_EXIT line of a coordinator log as {code, reason, at}, or None while it runs."""
    hits = re.findall(r"^(\S+) COORDINATOR_EXIT=(\d+) ?(.*)$", log_text, re.M)
    if not hits:
        return None
    at, code, reason = hits[-1]
    return {"code": int(code), "reason": reason.strip(), "at": iso_epoch(at)}


def board_epoch(updated):
    """The scoreboard's 'updated' text ('2026-10-08 01:45 MDT', local time) as epoch seconds, or None."""
    try:
        return time.mktime(time.strptime(updated[:16], "%Y-%m-%d %H:%M"))
    except (TypeError, ValueError):
        return None


def newer_events(updated, events):
    """Names of (epoch, name) events after the report text was last updated, oldest first."""
    return [name for t, name in sorted(events) if updated is None or t > updated]


def source_stamp(directory):
    return max((os.path.getmtime(p) for p in glob.glob(os.path.join(directory, "dashboard_*.py"))), default=0.0)


def sources_changed(directory, stamp):
    return source_stamp(directory) > stamp


def tiled_sessions(start_commands):
    return {m.group(1) for c in start_commands for m in [re.search(r"dashboard_tile\.py' '([^']+)'", c)] if m}


def team_sessions(names):
    return {n for n in names if n not in NOT_TEAM and not n.startswith("view-")}


class TeamSupervisor:
    """Says when to rebuild the team tab: the session set must differ from the tiles and stay the same for
    debounce_s, and rebuilds are at least min_gap_s apart."""

    def __init__(self, debounce_s=10, min_gap_s=30):
        self.debounce_s, self.min_gap_s = debounce_s, min_gap_s
        self.pending, self.since, self.last = None, None, None

    def should_rebuild(self, tiled, current, now):
        if tiled == current:
            self.pending = None
            return False
        if self.pending != current:
            self.pending, self.since = current, now
            return False
        if now - self.since < self.debounce_s or (self.last is not None and now - self.last < self.min_gap_s):
            return False
        self.last = now
        return True


ASKING = re.compile(r"Hooks need review|enter confirm|Do you want|\[y/n\]|\(y/n\)|Allow this|approve", re.I)
ERROR = re.compile(r"Traceback \(most recent call last\)|\bError:|Operation not permitted|\bBLOCKED\b|\bFAILED\b|permission denied", re.I)
STALL_S = 15 * 60


def session_alerts(screens, memory, now):
    """Plain alerts for team sessions: waiting for an answer, no new step for STALL_S while working, or stopped after an
    error. `memory` keeps each session's step list and when it last changed, across calls."""
    out = []
    for name, screen in sorted(screens.items()):
        lines = [l for l in screen.splitlines() if l.strip()]
        tail = "\n".join(lines[-15:])
        working = bool(BUSY_RE.search(screen))
        steps = tuple(l.strip() for l in lines if l.lstrip()[:1] in "•⏺" and "Working (" not in l)
        seen = memory.get(name)
        if seen is None or seen[0] != steps:
            memory[name] = (steps, now)
        since = memory[name][1]
        if ASKING.search(tail):
            out.append(f"{name} is waiting for an answer")
        elif working and now - since >= STALL_S:
            out.append(f"{name} shows no new step for {int((now - since) // 60)} min")
        elif not working and ERROR.search(tail) and "DONE" not in tail:
            out.append(f"{name} stopped after an error")
    return out


def ago(seconds):
    s = int(max(seconds, 0))
    return f"{s // 60}m ago" if s < 3600 else f"{s // 3600}h{s % 3600 // 60:02d}m ago"


def now_lines(state, now):
    """Plain lines for the report's NOW section, most urgent first."""
    lines = [f"! NEEDS YOUR RULING: {r}" for r in state["rulings"]]
    lines += [f"▲ STALLED/BLOCKED: {a} (the program is on it)" for a in state.get("alerts", [])]
    gpu = state["gpu"]
    if gpu["running"]:
        key, stage, etime = gpu["running"]
        lines.append(f"▸ GPU running: {SHORT.get(key, key)} · stage {stage} · {etime}")
    else:
        last, ex = "", gpu["last_exit"]
        if ex:
            what = "finished" if ex["code"] == 0 else f"stopped (exit {ex['code']}: {ex['reason']})"
            last = f" · last: {gpu['last_name'] or 'a'} coordinator {what} · {ago(now - ex['at'])}"
        lines.append(f"· GPU idle{last}")
    lines += [f"» {label}: {task}" for label, task in state["builds"]]
    lines += [f"◦ helper: {h}" for h in state["helpers"]]
    return lines


# ---- effects: reading the machine ------------------------------------------------------------------------------

def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def gpu_state():
    ps = sh("/bin/ps", "-axo", "etime=,command=")
    running = None
    for line in ps.splitlines():
        etime, _, command = line.strip().partition(" ")
        call = script_call(command) or ""
        m = (GPU_JOB_RE.search(call)
             or re.search(r"tools/run_(c10[a-z])\w*\.sh", call))
        if m and (m.lastindex < 2 or m.group(2) != "_job"):
            running = (m.group(1), m.group(2) if m.lastindex >= 2 else "between stages", etime)
            if m.lastindex >= 2:
                break
    logs = sorted(glob.glob(os.path.join(ROOT, "results", "c10*_logs", "*coordinator*.log")), key=os.path.getmtime)
    last_exit = coordinator_exit(open(logs[-1], errors="replace").read()) if logs else None
    key = re.search(r"(c10[a-z])", os.path.basename(os.path.dirname(logs[-1]))) if logs else None
    return {"running": running, "last_exit": last_exit, "last_name": SHORT.get(key.group(1)) if key else None}


SCREEN_TTL_S = 15
_screens = {"at": 0.0, "screens": {}, "titles": {}}


def team_screens():
    """Screens and pane titles of the team sessions, read from tmux at most every SCREEN_TTL_S seconds (tmux is shared
    by every session; a flood of reads helped hang its server on 2026-10-08)."""
    if time.time() - _screens["at"] >= SCREEN_TTL_S:
        names = team_sessions(sh("tmux", "list-sessions", "-F", "#{session_name}").split())
        _screens["screens"] = {n: sh("tmux", "capture-pane", "-p", "-t", n) for n in names}
        _screens["titles"] = {n: sh("tmux", "display", "-p", "-t", n, "#{pane_title}") for n in names if n.startswith("codex")}
        _screens["at"] = time.time()
    return _screens["screens"], _screens["titles"]


def build_state():
    from dashboard_active import label
    from dashboard_tile import status
    out = []
    screens, titles = team_screens()
    for n, screen in sorted(screens.items()):
        if not n.startswith("codex"):
            continue
        if status(screen, None, time.time())[0] == "WORKING":
            title = titles.get(n, "").strip().split(" | ")[0]   # drop "| <worktree>"
            out.append((label(n), re.sub(r"^[^\w(]+", "", title) or "working"))                    # drop the spinner
    return out


def events():
    ev = []
    for p in glob.glob(os.path.join(ROOT, "results", "c10*_logs", "*coordinator*.log")):
        ex = coordinator_exit(open(p, errors="replace").read())
        if ex:
            ev.append((ex["at"], f"coordinator exit {ex['code']} ({os.path.basename(p)})"))
    for p in glob.glob(os.path.join(ROOT, "results", "c10*", "*", "HALT.json")):
        ev.append((os.path.getmtime(p), f"HALT in {os.path.relpath(os.path.dirname(p), ROOT)}"))
    for p in glob.glob(os.path.join(ROOT, "CORPUS", "[0-9][0-9]_*.md")):
        ev.append((os.path.getmtime(p), f"CORPUS/{os.path.basename(p)[:2]} changed"))
    return ev


def gather():
    from dashboard_tile import running_helpers
    try:
        runbook = open(os.path.join(ROOT, "EXPERIMENT_RUNBOOK.md"), errors="replace").read()
    except OSError:
        runbook = ""
    screens = {n: s for n, s in team_screens()[0].items() if n != "program"}
    return {"rulings": awaiting_rulings(runbook), "alerts": session_alerts(screens, _alert_memory, time.time()),
            "gpu": gpu_state(), "builds": build_state(), "helpers": running_helpers()}


_alert_memory = {}


def maybe_reload(stamp):
    """Re-exec this pane's program when any dashboard source changed, so a code fix shows without a manual restart."""
    if sources_changed(TOOLS, stamp):
        os.execv(sys.executable, [sys.executable] + sys.argv)


_supervisor = TeamSupervisor()


def supervise_team():
    """From the report pane of the live 'dashboard' session only: rebuild the team tab when team sessions change."""
    pane = os.environ.get("TMUX_PANE", "")
    if not pane or sh("tmux", "display", "-p", "-t", pane, "#{session_name}").strip() != "dashboard":
        return
    tiled = tiled_sessions(sh("tmux", "list-panes", "-t", "dashboard:1", "-F", "#{pane_start_command}").splitlines())
    current = team_sessions(sh("tmux", "list-sessions", "-F", "#{session_name}").split())
    if _supervisor.should_rebuild(tiled, current, time.time()):
        log = open("/private/tmp/claude-501/teamdash_rebuild.log", "a")
        subprocess.Popen(["bash", os.path.join(TOOLS, "team_dashboard.sh")], env={**os.environ, "TEAMDASH_NO_ATTACH": "1"},
                         stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True)


def clip(line, width):
    """A line cut to `width` visible characters (ANSI codes kept, not counted), so a pane never wraps or scrolls."""
    out, seen = [], 0
    for token in re.findall(r"\033\[[0-9;]*[A-Za-z]|.", line, re.S):
        if token.startswith("\033"):
            out.append(token)
        elif seen < width:
            out.append(token)
            seen += 1
    return "".join(out)
