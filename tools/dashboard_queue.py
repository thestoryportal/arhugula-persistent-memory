"""Read-only work queue; /usr/bin/python3 tools/dashboard_queue.py [--once WIDTH [HEIGHT]].

The JSON boundary constructs typed items. Rendering uses only its arguments;
tmux, process inventory, recorded events, local clock and terminal are edges.
Python 3.9, stdlib only. No queue data or observation cache is written.
"""
import argparse
import collections
import datetime as dt
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Mapping, Optional, Tuple, Union

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dashboard_live import BUSY_RE, cell_width, detect_gpu_jobs


class State(str, Enum):
    RUNNING = "running"
    NEEDS_YOU = "needs_you"
    IN_REVIEW = "in_review"
    READY = "ready"
    BLOCKED = "blocked"


class Observed(str, Enum):
    BUSY = "busy"
    WAITING = "waiting"
    IDLE = "idle"
    MISSING = "missing"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class Estimate:
    low_min: int
    high_min: int
    set: dt.datetime


@dataclass(frozen=True)
class WorkItem:
    id: str
    title: str
    summary: str
    state: State
    who: str
    session: Optional[str]
    started: Optional[dt.datetime]
    estimate: Optional[Estimate]
    depends_on: Tuple[str, ...]
    blocked_by: Tuple[str, ...]
    needs_from_you: Tuple[str, ...]
    notes: Tuple[str, ...]


@dataclass(frozen=True)
class Queue:
    edited: dt.datetime
    items: Tuple[WorkItem, ...]


@dataclass(frozen=True)
class QueueMissing:
    pass


@dataclass(frozen=True)
class QueueProblem:
    message: str


QueueInput = Union[Queue, QueueMissing, QueueProblem]


class QueueError(ValueError):
    pass


def parse_queue(raw: str) -> Union[Queue, QueueMissing]:
    """Parse the complete program-state JSON once, or identify the precise field."""
    def fail(where, message):
        raise QueueError(where + ": " + message)

    def obj(value, where):
        if not isinstance(value, dict):
            fail(where, "expected an object")
        return value

    def required(value, key, where):
        if key not in value:
            fail(where + "." + key, "missing field")
        return value[key]

    def text(value, where):
        if not isinstance(value, str):
            fail(where, "expected words (a string)")
        return value

    def stamp(value, where):
        text(value, where)
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            fail(where, "expected an ISO-8601 UTC time")
        if "T" not in value or parsed.utcoffset() != dt.timedelta(0):
            fail(where, "expected an ISO-8601 UTC time")
        return parsed

    def words(value, where):
        if not isinstance(value, list):
            fail(where, "expected a list")
        return tuple(text(v, where + "[%d]" % index) for index, v in enumerate(value))

    try:
        root = json.loads(raw)
    except (ValueError, TypeError) as error:
        raise QueueError("program_state.json JSON: " + str(error)) from error
    obj(root, "program_state.json")
    if "work_queue" not in root:
        return QueueMissing()
    value = obj(root["work_queue"], "work_queue")
    edited = stamp(required(value, "edited", "work_queue"), "work_queue.edited")
    items = required(value, "items", "work_queue")
    if not isinstance(items, list):
        fail("work_queue.items", "expected a list")
    parsed_items, ids = [], set()
    for number, item in enumerate(items, 1):
        where = "work_queue item %d" % number
        obj(item, where)
        identifier = text(required(item, "id", where), where + ".id")
        where += " (" + identifier + ")"
        if not identifier.strip():
            fail(where + ".id", "expected a non-empty id")
        if identifier in ids:
            fail(where + ".id", "duplicate id " + identifier)
        ids.add(identifier)
        fields = {name: required(item, name, where) for name in
                  ("title", "summary", "state", "who", "session", "started", "estimate",
                   "depends_on", "blocked_by", "needs_from_you", "notes")}
        state = text(fields["state"], where + ".state")
        try:
            state = State(state)
        except ValueError:
            fail(where + ".state", "unknown state " + state)
        session = fields["session"]
        if session is not None:
            session = text(session, where + ".session")
        started = fields["started"]
        if started is not None:
            started = stamp(started, where + ".started")
        estimate = fields["estimate"]
        if estimate is not None:
            obj(estimate, where + ".estimate")
            low = required(estimate, "low_min", where + ".estimate")
            high = required(estimate, "high_min", where + ".estimate")
            for key, minutes in (("low_min", low), ("high_min", high)):
                if type(minutes) is not int or minutes < 0:
                    fail(where + ".estimate." + key, "expected non-negative whole minutes")
            if high < low:
                fail(where + ".estimate.high_min", "must be at least low_min")
            estimate = Estimate(low, high, stamp(required(estimate, "set", where + ".estimate"),
                                                  where + ".estimate.set"))
        parsed_items.append(WorkItem(
            identifier, text(fields["title"], where + ".title"),
            text(fields["summary"], where + ".summary"), state,
            text(fields["who"], where + ".who"), session, started, estimate,
            *(words(fields[name], where + "." + name) for name in
              ("depends_on", "blocked_by", "needs_from_you", "notes"))))
    for number, item in enumerate(parsed_items, 1):
        for dependency in item.depends_on:
            if dependency not in ids:
                fail("work_queue item %d (%s).depends_on" % (number, item.id),
                     "no queue item has id " + dependency)
    return Queue(edited, tuple(parsed_items))


@dataclass(frozen=True)
class SessionLive:
    status: Observed
    context_left: Optional[int] = None
    finished: bool = False
    reason: Optional[str] = None


@dataclass(frozen=True)
class Reviewer:
    elapsed_seconds: int
    output: str


@dataclass(frozen=True)
class ExperimentLive:
    name: str
    events_age_seconds: int


@dataclass(frozen=True)
class Live(Mapping[str, SessionLive]):
    sessions: Mapping[str, SessionLive] = field(default_factory=dict)
    reviewers: Tuple[Reviewer, ...] = ()
    experiment: Optional[ExperimentLive] = None
    errors: Tuple[str, ...] = ()

    def __getitem__(self, key):
        return self.sessions[key]

    def __iter__(self):
        return iter(self.sessions)

    def __len__(self):
        return len(self.sessions)


def clean(value):
    return "".join(" " if ch.isspace() else "?" if unicodedata.category(ch).startswith("C") else ch
                   for ch in str(value))


def cells(value):
    return sum(cell_width(ch) for ch in value)


def clip(value, width):
    used = 0
    for index, ch in enumerate(value):
        used += cell_width(ch)
        if used > width or index >= width:
            return value[:index]
    return value


def wrap(value, width, prefix=""):
    """Wrap words by terminal cells, splitting an overlong word without losing it."""
    indent = " " * cells(prefix)
    lines, line = [], prefix
    for word in clean(value).split():
        gap = " " if line != prefix and line != indent else ""
        if cells(line + gap + word) <= width and len(line + gap + word) <= width:
            line += gap + word
            continue
        if line != prefix and line != indent:
            lines.append(line.rstrip())
            line = indent
        while cells(line + word) > width or len(line + word) > width:
            available = width - cells(line)
            if available <= 0:
                raise ValueError("width is too small for the hanging indent")
            used, split = 0, 0
            for index, ch in enumerate(word):
                if used + cell_width(ch) > available or len(line) + index >= width:
                    break
                used += cell_width(ch)
                split = index + 1
            if split == 0:
                raise ValueError("width is too small for a character")
            lines.append(line + word[:split])
            line, word = indent, word[split:]
        line += word
    lines.append(line.rstrip())
    return lines


def badge(state):
    return state.value.replace("_", " ").upper()


def minutes_text(minutes):
    minutes = max(0, int(minutes))
    return "%d h %d min" % divmod(minutes, 60) if minutes >= 60 else "%d min" % minutes


def clock_text(stamp, zone):
    local = stamp.astimezone(zone)
    return "%d:%02d %s" % (local.hour % 12 or 12, local.minute, "AM" if local.hour < 12 else "PM")


def time_line(item, now):
    parts = []
    if item.started is not None:
        parts.append("running for " + minutes_text((now - item.started).total_seconds() // 60))
    if item.estimate is None:
        parts.append("no estimate yet")
    else:
        elapsed = max(0, (now - item.estimate.set).total_seconds() / 60)
        if elapsed > item.estimate.high_min:
            parts.append("running %d min past the estimate" % (elapsed - item.estimate.high_min))
        else:
            low = max(0, item.estimate.low_min - int(elapsed))
            high = max(0, item.estimate.high_min - int(elapsed))
            parts.append("about %d-%d min left (estimate made %s)" %
                         (low, high, clock_text(item.estimate.set, now.tzinfo)))
    return " · ".join(parts)


def is_finished(item, observed):
    return item.state == State.RUNNING and observed is not None and (
        observed.status == Observed.MISSING or observed.finished)


def live_line(observed, item=None, session=None):
    if item is not None and is_finished(item, observed):
        return "builder finished — waiting for MAESTRO"
    if observed is None or observed.status == Observed.UNAVAILABLE:
        session = item.session if item is not None else session
        text = "live session check unavailable" + (" for " + session if session else "")
        return text + (": " + observed.reason if observed is not None and observed.reason else "")
    if observed.finished:
        return "builder finished — waiting for MAESTRO"
    text = {Observed.BUSY: "builder working", Observed.WAITING: "builder waiting on a test run",
            Observed.IDLE: "builder idle", Observed.MISSING: "session not found"}[observed.status]
    if observed.context_left is not None and observed.status != Observed.MISSING:
        text += " · %d%% memory left" % observed.context_left
    return text


def render(queue: QueueInput, live: Live, now: dt.datetime, width: int,
           height: Optional[int] = None) -> str:
    if width < 40:
        raise ValueError("queue needs at least 40 columns")
    if now.utcoffset() is None:
        raise ValueError("now must include the local timezone")
    lines = wrap("Work queue · " + clock_text(now, now.tzinfo), width)
    items = queue.items if isinstance(queue, Queue) else ()
    by_session = {item.session: item for item in reversed(items) if item.session is not None}
    states = {item.id: State.IN_REVIEW if is_finished(item, live.get(item.session)) else item.state
              for item in items}
    if isinstance(queue, Queue):
        counts = collections.Counter(states.values())
        lines += wrap(" · ".join("%s %d" % (badge(state), counts[state]) for state in State), width)
        age = max(0, (now - queue.edited).total_seconds())
        edited = ("queue not updated for %s — may be out of date" % minutes_text(age // 60)
                  if age > 3 * 3600 else "queue edited %d min ago" % (age // 60))
        lines += wrap(edited, width, "  ")
        for item in items:
            if item.state == State.NEEDS_YOU:
                lines += wrap(item.title, width, "  Needs you: ")
    if isinstance(queue, QueueMissing):
        lines += [""] + wrap("work_queue is not in program_state.json yet. MAESTRO can add the work list.", width)
    elif isinstance(queue, QueueProblem):
        lines += [""] + wrap("Queue could not be read: " + queue.message, width)
    elif not items:
        lines += ["", "The work queue is empty."]
    # Mandatory attention text must fit before optional live details and cards.
    if height is not None and height < len(lines) + bool(items):
        raise ValueError("window is too short for the header and Needs you block")

    live_lines, idle, diagnostics = ["", "Running now (detected live)"], [], []
    for session, observed in sorted(live.items()):
        item = by_session.get(session)
        if observed.finished or observed.status == Observed.IDLE:
            idle.append(session)
            continue
        if observed.status not in (Observed.BUSY, Observed.WAITING):
            if observed.status == Observed.UNAVAILABLE and item is None:
                diagnostics += wrap(live_line(observed, session=session), width, "  ")
            continue
        name = item.title + " (" + session + ")" if item is not None else session
        description = name + ": " + live_line(observed, item, session)
        if item is None:
            description += "; not yet described in the queue"
        live_lines += wrap(description, width, "  - ")
    for reviewer in live.reviewers:
        live_lines += wrap("Astra review running for %d min; record: %s; not yet described in the queue" %
                           (reviewer.elapsed_seconds // 60, reviewer.output), width, "  - ")
    if live.experiment is not None:
        live_lines += wrap("experiment run in progress: %s (events updated %d min ago); not yet described in the queue" %
                           (live.experiment.name, live.experiment.events_age_seconds // 60), width, "  - ")
    if len(live_lines) == 2:
        live_lines += wrap("No work detected by the live checks.", width, "  ")
    if idle:
        live_lines += wrap("Idle builder windows: " + ", ".join(idle), width)
    for error in live.errors:
        diagnostics += wrap("Live check unavailable: " + error, width, "  ")
    if diagnostics:
        live_lines += ["Live checks"] + diagnostics
    if height is not None:
        budget = height - len(lines) - bool(items)
        if len(live_lines) > budget:
            live_lines = (live_lines[:budget - 1] +
                          [clip("+%d more live lines" % (len(live_lines) - budget + 1), width)]) if budget else []
    lines += live_lines

    titles = {item.id: item.title for item in items}
    ordered = list(enumerate(items, 1))
    if height is not None:
        priority = {State.RUNNING: 0, State.NEEDS_YOU: 1, State.IN_REVIEW: 2}
        ordered.sort(key=lambda entry: priority.get(states[entry[1].id], 3))
        ordered = list(enumerate((item for _, item in ordered), 1))  # numbers follow the order on screen
    for index, (number, item) in enumerate(ordered):
        observed, state = live.get(item.session), states[item.id]
        card = [""] + wrap(item.title, width, "%d. " % number)
        card += ["  [" + badge(state) + "]"]
        card += wrap(item.who, width, "  Who: ")
        card += wrap(item.summary, width, "  Summary: ")
        if item.depends_on:
            card += wrap("; ".join(titles[dep] for dep in item.depends_on), width, "  Waits for: ")
        for blocker in item.blocked_by:
            card += wrap(blocker, width, "  Blocked by: ")
        for need in item.needs_from_you:
            card += wrap(need, width, "  Needs from you: ")
        card += wrap(time_line(item, now), width, "  Time: ")
        if item.session is not None:
            card += wrap(live_line(observed, item), width, "  Live: ")
        for note in item.notes:
            card += wrap(note, width, "  Note: ")
        remaining = len(ordered) - index - 1
        if height is None or len(lines) + len(card) + bool(remaining) <= height:
            lines += card
            continue
        rest = ordered[index:]
        available = height - len(lines)
        shown = len(rest) if len(rest) <= available else available - 1
        for number, item in rest[:shown]:
            lines.append(clip("%d. [%s] %s" % (number, badge(states[item.id]), clean(item.title)), width))
        if shown < len(rest):
            lines.append(clip("+%d more items (taller window shows more)" % (len(rest) - shown), width))
        break
    return "\n".join(lines)


def observe_pane(screen):
    """Use the shared BUSY_RE (dashboard_live.py:15); inspect the latest reply only."""
    screen = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", screen)
    lines = screen.splitlines()
    markers = [index for index, line in enumerate(lines) if re.match(r"\s*[•⏺]\s+", line)]
    tail = lines[markers[-1]:] if markers else lines[-15:]
    reply = []
    for line in tail:
        if re.match(r"\s*(?:[›❯>$]|Context \d+% left|\d+% context left|gpt-|Tip:|esc to interrupt)", line):
            break
        if line.strip():
            reply.append(re.sub(r"^\s*[•⏺]\s+", "", line).strip())
    working = bool(BUSY_RE.search("\n".join(tail)))
    waiting = bool(re.search(r"waiting (?:for|on).*?(?:test|command|terminal)|background terminal",
                             "\n".join(tail), re.I))
    prompt = any(re.match(r"\s*[›❯]", line) for line in tail)
    status = Observed.WAITING if waiting and (working or not prompt) else Observed.BUSY if working else Observed.IDLE
    memory = re.findall(r"Context (\d+)% left", screen)
    context = int(memory[-1]) if memory else None
    finished = status == Observed.IDLE and bool(re.search(r"(?:^|[ _-])(?:READY|HANDOFF)(?:$|[ _-])", " ".join(reply)))
    return SessionLive(status, context, finished)


def run_command(args):
    return subprocess.run(args, capture_output=True, text=True, timeout=2)


def reviewer_processes(inventory):
    reviewers = []
    for number, line in enumerate(inventory.splitlines(), 1):
        parts = line.split(None, 3)
        if len(parts) != 4:
            raise ValueError("process inventory line %d has no pid, parent, elapsed time and command" % number)
        _, _, elapsed, command = parts
        executable = command.split(None, 2)
        if len(executable) < 2 or Path(executable[0]).name != "codex" or executable[1] != "exec":
            continue
        args = shlex.split(command)
        if len(args) < 2 or Path(args[0]).name != "codex" or args[1] != "exec":
            continue
        day, sep, elapsed = elapsed.partition("-")
        days = int(day) if sep else 0
        elapsed = elapsed if sep else day
        values = [int(value) for value in elapsed.split(":")]
        if len(values) not in (2, 3):
            raise ValueError("review process has unreadable elapsed time")
        seconds = days * 86400 + sum(value * 60 ** power for power, value in enumerate(reversed(values)))
        output = "output file not supplied"
        for index, arg in enumerate(args[2:], 2):
            if arg in ("-o", "--output-last-message"):
                if index + 1 == len(args):
                    raise ValueError("review process has no value after " + arg)
                output = Path(args[index + 1]).name
            elif arg.startswith(("--output-last-message=", "-o=")):
                output = Path(arg.split("=", 1)[1]).name
        reviewers.append(Reviewer(seconds, output))
    return tuple(reviewers)


def current_experiment(root, now, jobs):
    """Reuse dashboard_live.detect_gpu_jobs (Experiment/MathLab's process authority).

    NEW1 is outside its job roster: an unfinished event file is a fallback only
    while its modification age is 0..600 seconds, shown alongside the run.
    """
    base = root / "results/mathlab_staging/runs"
    if not base.exists():
        return None
    paths = sorted(base.glob("*/events.jsonl"),
                   key=lambda p: (p.stat().st_mtime_ns, p.parent.name), reverse=True)
    live_dirs = {Path(job["run_dir"]).resolve() for job in jobs if job["run_dir"]}
    for path in paths:
        terminal = False
        lines = path.read_text().splitlines()
        for number, line in enumerate(lines, 1):
            try:
                event = json.loads(line)
            except ValueError as error:
                raise ValueError("%s line %d JSON: %s" % (path, number, error)) from error
            if not isinstance(event, dict) or not isinstance(event.get("type"), str):
                raise ValueError("%s line %d has no event type" % (path, number))
            terminal = terminal or event["type"] in ("run_finished", "terminal")
        age = now.timestamp() - path.stat().st_mtime
        if lines and not terminal and (path.parent.resolve() in live_dirs or 0 <= age <= 600):
            return ExperimentLive(path.parent.name, max(0, int(age)))
    return None


def gather_live(queue, root, now, run=run_command):
    """Fresh observations only; cached team_screens/sh hide failures and cannot fit Q1."""
    errors, sessions, reviewers, experiment, jobs = [], {}, (), None, ()
    named = {item.session for item in queue.items if item.session is not None} if isinstance(queue, Queue) else set()
    try:
        result = run(["tmux", "-L", "default", "list-sessions", "-F", "#{session_name}"])
        if result.returncode:
            if re.fullmatch(r"no server running on [^\n]+|error connecting to [^\n]+ \(No such file or directory\)", result.stderr.strip()):
                names = set()
            else:
                raise OSError("tmux inventory exit %d: %s" % (result.returncode, result.stderr.strip()))
        else:
            if not result.stdout.strip():
                raise OSError("tmux inventory returned empty output")
            names = set(result.stdout.splitlines())
        targets = named | {name for name in names if name.startswith("codex")}
        for name in sorted(targets):
            if name not in names:
                sessions[name] = SessionLive(Observed.MISSING)
                continue
            try:
                pane = run(["tmux", "-L", "default", "capture-pane", "-p", "-t", "=" + name + ":"])
                if pane.returncode:
                    raise OSError("exit %d: %s" % (pane.returncode, pane.stderr.strip()))
                sessions[name] = observe_pane(pane.stdout)
            except (OSError, ValueError, subprocess.TimeoutExpired) as error:
                sessions[name] = SessionLive(Observed.UNAVAILABLE, reason=str(error))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        sessions = {name: SessionLive(Observed.UNAVAILABLE) for name in named}
        errors.append("tmux: " + str(error))
    try:
        result = run(["/bin/ps", "-axww", "-o", "pid=,ppid=,etime=,command="])
        if result.returncode or not result.stdout.strip():
            raise OSError("process inventory exit %d: %s" % (result.returncode, result.stderr.strip() or "empty output"))
        reviewers = reviewer_processes(result.stdout)
        jobs, valid = detect_gpu_jobs(result.stdout)
        if not valid:
            raise ValueError("malformed process inventory")
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        errors.append("reviewers: " + str(error))
    try:
        experiment = current_experiment(root, now, jobs)
    except (OSError, ValueError) as error:
        errors.append("experiment: " + str(error))
    return Live(sessions, reviewers, experiment, tuple(errors))


def read_queue(path):
    try:
        return parse_queue(path.read_text())
    except (OSError, ValueError) as error:
        return QueueProblem(str(error))


def colorize(text, tty):
    if not tty:
        return text
    colors = {"RUNNING": "32", "NEEDS YOU": "33", "IN REVIEW": "36", "READY": "34", "BLOCKED": "31"}
    lines, header = [], True
    for line in text.splitlines():
        if not line:
            header = False
        if header:
            line = "\x1b[1;36m" + line + "\x1b[0m"
        else:
            match = re.fullmatch(r"  \[(RUNNING|NEEDS YOU|IN REVIEW|READY|BLOCKED)\]", line)
            if match:
                line = "  \x1b[1;" + colors[match.group(1)] + "m" + line[2:] + "\x1b[0m"
        lines.append(line)
    return "\n".join(lines)


def local_now():
    return dt.datetime.now().astimezone()


def terminal_dimensions():
    size = shutil.get_terminal_size((80, 24))
    return max(40, size.columns - 1), max(1, size.lines)


def run_loop(path, root, stream=None, sleep=time.sleep, clock=local_now,
             width=None, detect=gather_live):
    stream = sys.stdout if stream is None else stream
    while True:
        columns, rows = terminal_dimensions()
        queue, now = read_queue(path), clock()
        live = detect(queue, root, now)
        frame = render(queue, live, now, columns if width is None else width(), rows)
        stream.write("\x1b[2J\x1b[H" + colorize(frame, stream.isatty()))
        stream.flush()
        sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Read-only program work queue")
    parser.add_argument("--once", type=int, nargs="+", metavar="N", help="WIDTH [HEIGHT]")
    args = parser.parse_args()
    # The launch must stay exactly /usr/bin/python3 '<absolute dashboard path>'.
    # A worktree shell can inherit LLMDB_ROOT=main; bind this read-only tab to its file.
    root = Path(__file__).resolve().parents[1]
    path = root / "docs/program_state.json"
    if args.once is not None:
        if len(args.once) not in (1, 2):
            parser.error("--once expects WIDTH [HEIGHT]")
        columns = args.once[0]
        rows = args.once[1] if len(args.once) == 2 else terminal_dimensions()[1]
        queue, now = read_queue(path), local_now()
        print(colorize(render(queue, gather_live(queue, root, now), now, columns, rows), sys.stdout.isatty()))
    else:
        run_loop(path, root)


if __name__ == "__main__":
    main()
