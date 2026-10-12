"""MathLab schema 1: events.jsonl is the only run-state authority.

One run_started.step identifies the intended experiment step. Optional purpose
is "experiment" or "admission"; an admission receipt never completes that step.
Legacy admission streams remain admission-only until a stage starts. A successful
substage does not complete the step: emit run_finished for its outcome. Reserve gate_id
"calibration" for step 3's aggregate result (prereg §4.3); individual proxy
failures and gate 2b do not stop the lab. Emit halted for diagnostic aborts.
Readers, including LabViz, use read_events followed by this module's pure fold.
New terminal publications emit outcome-free run_finishing first. The terminal
is exposed by atomic replacement only after the complete stream is fsynced;
an unmatched run_finishing is INVALID. Legacy terminals retain their meaning.
Replacement commits file content; power-loss pathname durability is unverified.
"""
import copy, fcntl, json, math, os, tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def _utc(value):
    if not isinstance(value, str) or "T" not in value:
        return False
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return stamp.utcoffset() is not None and stamp.utcoffset().total_seconds() == 0
    except ValueError:
        return False


def _outcome(value):
    return value in ("PASS", "FAIL", "INVALID")


FIELDS = {
    "run_started": {"step": lambda v: type(v) is int and 1 <= v <= 4, "title": _text,
                    "deadline_ts": _utc, "pid": lambda v: type(v) is int and v > 0},
    "admission": {"allowed": lambda v: type(v) is bool,
                  "reasons": lambda v: isinstance(v, list) and all(_text(r) for r in v)},
    "stage_started": {"stage": _text, "plain_words": _text, "cap_s": lambda v: _number(v) and v > 0},
    "progress": {"stage": _text, "done": _number, "total": _number, "unit": _text},
    "gate_result": {"gate_id": _text, "plain_words": _text, "observed": lambda v: True,
                    "bar": lambda v: True, "comparison": _text, "passed": lambda v: type(v) is bool},
    "stage_finished": {"stage": _text, "outcome": _outcome, "summary": _text},
    "resource_sample": {"avail_gib": _number, "floor_gib": _number, "rss_gib": _number, "cpu_pct": _number},
    "finding_staged": {"finding_id": _text, "tier": lambda v: v == "MATH-PROXY", "summary": _text, "path": _text},
    "candidate_added": {"candidate_id": _text, "source": _text, "question": _text, "offline": lambda v: type(v) is bool},
    "halted": {"reason": _text, "diagnostic_path": _text},
    "run_finishing": {},
    "run_finished": {"outcome": _outcome, "summary": _text},
}
ENVELOPE = {"ts": _utc, "schema": lambda v: type(v) is int and v == 1, "run_id": _text, "type": _text}
OPTIONAL_FIELDS = {"run_started": {"purpose": lambda v: v in ("experiment", "admission")}}
GATE_PLAN = [
    ("admission", "Safe launch", "engine unchanged; GPU queue cleared"),
    ("context", "Same prompt inputs", "frozen context and tokenisation match"),
    ("inertness", "Observation changes nothing", "LAW#5 and observer-parity pass"),
    ("law3", "Known model answers reproduce", "all three fresh baselines pass their frozen ranges"),
    ("budget", "Stay inside time limits", "each emitted stage projection fits its deadline"),
    ("memory", "Enough free memory", "stage >=8 GiB; calculation >=8 GiB + reserve"),
    ("2a", "Reproduce saved calculations", "projection <=1e-6; write/size error <=1e-5"),
    ("2b", "Clean inputs approximate the write", "whole-write error <=25%; direction >=95% (scope only)"),
    ("calibration", "At least one estimate matches past results", "strict orders; each >=1900/2000 rechecks"),
]


def gate_outcome(gate):
    """Calibration's aggregate is three-valued; individual checks are Boolean."""
    if gate["gate_id"] == "calibration" and _outcome(gate["observed"]):
        return gate["observed"]
    return "PASS" if gate["passed"] else "FAIL"


def gate_group(identifier):
    if identifier in ("admission", "dispatch-admission") or identifier.startswith("admission-"):
        return "admission"
    if identifier in ("context", "mint-shared-context") or identifier.startswith("tokenisation-"):
        return "context"
    if identifier in ("law5", "observer-parity"):
        return "inertness"
    if identifier == "law3" or identifier.startswith("law3-"):
        return "law3"
    if identifier.startswith("budget-"):
        return "budget"
    if identifier.startswith(("stage-memory-", "memory-")):
        return "memory"
    if identifier == "2a" or identifier.startswith("2a-"):
        return "2a"
    return identifier if identifier in ("2b", "calibration") else None


def _validate(event):
    if not isinstance(event, dict):
        raise ValueError("event must be a JSON object")
    kind = event.get("type")
    if not isinstance(kind, str) or kind not in FIELDS:
        raise ValueError(f"unknown event type: {kind!r}")
    required = {**ENVELOPE, **FIELDS[kind]}
    fields = {**required, **OPTIONAL_FIELDS.get(kind, {})}
    missing, extra = required.keys() - event.keys(), event.keys() - fields.keys()
    if missing or extra:
        raise ValueError(f"{kind}: missing fields {sorted(missing)}; extra fields {sorted(extra)}")
    for name, valid in fields.items():
        if name in event and not valid(event[name]):
            raise ValueError(f"{kind}: invalid {name}: {event[name]!r}")
    if kind == "progress" and event["done"] > event["total"]:
        raise ValueError("progress: done exceeds total")
    try:
        json.dumps(event, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{kind}: fields must be finite JSON values: {error}") from error


def _append(path, line):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
    try:
        if os.write(fd, line) != len(line):
            raise OSError("short event append; inspect events.jsonl before continuing")
        os.fsync(fd)
    finally:
        os.close(fd)


@dataclass(frozen=True)
class TerminalPublication:
    """Identity of a fsynced stream, prepared before its atomic publication."""
    path: Path
    identity: tuple[int, int, int]
    outcome: str

    def committed_outcome(self):
        stat = self.path.stat()
        return self.outcome if (stat.st_dev, stat.st_ino, stat.st_size) == self.identity else None


def emit(run_dir, type, *, before_publish=None, **fields):
    """Serialize appends; expose terminal bytes only after their fsync succeeds."""
    if before_publish is not None and type != "run_finished":
        raise ValueError("before_publish requires run_finished")
    if type not in FIELDS:
        raise ValueError(f"unknown event type: {type!r}")
    allowed = {**FIELDS[type], **OPTIONAL_FIELDS.get(type, {})}
    missing, extra = FIELDS[type].keys() - fields.keys(), fields.keys() - allowed.keys()
    if missing or extra:
        raise ValueError(f"{type}: missing fields {sorted(missing)}; extra fields {sorted(extra)}")
    run_dir = Path(run_dir)
    event = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
             "schema": 1, "run_id": run_dir.name, "type": type, **fields}
    _validate(event)
    line = (json.dumps(event, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n").encode("utf-8")
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "events.jsonl"
    directory = os.open(run_dir, os.O_RDONLY)
    try:
        # The directory inode remains stable when the stream inode is replaced.
        fcntl.flock(directory, fcntl.LOCK_EX)
        if type != "run_finished":
            _append(path, line)
            return
        if path.exists():
            _, errors = read_events(path)
            if errors: raise OSError("invalid event stream: " + "; ".join(errors))
        pending = {key: event[key] for key in ENVELOPE}
        pending["type"] = "run_finishing"
        _append(path, (json.dumps(pending, separators=(",", ":")) + "\n").encode("utf-8"))
        fd, temporary = tempfile.mkstemp(prefix=".events-terminal-", dir=run_dir)
        try:
            with os.fdopen(fd, "wb", buffering=0) as target:
                with path.open("rb") as source:
                    for block in iter(lambda: source.read(1 << 20), b""):
                        if os.write(target.fileno(), block) != len(block):
                            raise OSError("short event prefix copy; publication incomplete")
                if os.write(target.fileno(), line) != len(line):
                    raise OSError("short terminal append; publication incomplete")
                os.fchmod(target.fileno(), 0o644)
                os.fsync(target.fileno())
                stat = os.fstat(target.fileno())
                publication = TerminalPublication(path, (stat.st_dev, stat.st_ino, stat.st_size), fields["outcome"])
            # No persistence operation follows the content commit point.
            os.fsync(directory)
            if before_publish is not None: before_publish(publication)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary): os.unlink(temporary)
    finally:
        os.close(directory)


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_events(path):
    """Return (validated events, explicit path/line errors), including a partial tail."""
    path = Path(path)
    events, errors = [], []
    try:
        with path.open("rb") as source:
            for number, raw in enumerate(source, 1):
                try:
                    if not raw.endswith(b"\n"):
                        raise ValueError("incomplete line: missing final newline")
                    event = json.loads(raw.decode("utf-8"), object_pairs_hook=_object)
                    _validate(event)
                    if event["run_id"] != path.parent.name:
                        raise ValueError(f"run_id differs from run directory {path.parent.name!r}")
                    events.append(event)
                except (ValueError, UnicodeError) as error:
                    errors.append(f"{path}: line {number}: {error}")
    except OSError as error:
        errors.append(f"{path}: read error: {error}")
    return events, errors


def fold(events):
    """Reduce a single run's ordered events without IO, clock reads or input mutation."""
    state = {"run_id": None, "step": None, "title": "", "status": "not started", "started_ts": None,
             "deadline_ts": None, "pid": None, "stage": None, "progress": None, "admission": None,
             "steps": {i: "not started" for i in range(1, 5)}, "gates": [], "resources": None,
             "findings": [], "candidates": [], "halt": None, "recent": [], "outcome": None,
             "summary": "", "finished_ts": None, "purpose": None, "calibration_outcome": None,
             "stages": [], "resource_samples": [], "gate_outcomes": {}, "gate_groups": {}}
    gates = {}; explicit_purpose = False; terminal_pending = False
    for raw in events:
        _validate(raw)
        event = copy.deepcopy(raw)
        if state["run_id"] not in (None, event["run_id"]):
            raise ValueError("cannot fold events from different runs")
        state["run_id"] = event["run_id"]
        state["recent"] = (state["recent"] + [event])[-8:]
        kind = event["type"]
        if kind == "run_started":
            for key in ("step", "title", "deadline_ts", "pid"):
                state[key] = event[key]
            state["started_ts"] = event["ts"]
            explicit_purpose = "purpose" in event
            state["purpose"] = event.get("purpose", "experiment")
            state["status"] = "running"
            if state["purpose"] == "experiment":
                state["steps"][event["step"]] = "running"
        elif kind == "admission":
            state["admission"] = event
            waiting = "waiting for GPU" if any("gpu" in r.lower() for r in event["reasons"]) else "waiting for admission"
            state["status"] = "running" if event["allowed"] else waiting
        elif kind == "stage_started":
            state["stage"], state["progress"] = copy.deepcopy(event), None
            state["stages"].append(state["stage"])
        elif kind == "progress":
            if state["stage"] and event["stage"] == state["stage"]["stage"]:
                state["progress"] = event
        elif kind == "gate_result":
            gates[event["gate_id"]] = event
        elif kind == "stage_finished":
            for stage in reversed(state["stages"]):
                if event["stage"] == stage["stage"] and "finished_ts" not in stage:
                    stage.update(finished_ts=event["ts"], outcome=event["outcome"], summary=event["summary"])
                    break
        elif kind == "resource_sample":
            state["resources"] = event
            state["resource_samples"].append(event)
        elif kind == "finding_staged":
            state["findings"].append(event)
        elif kind == "candidate_added":
            state["candidates"].append(event)
        elif kind == "halted":
            state["halt"] = event
        elif kind == "run_finishing":
            terminal_pending = True
            state.update(outcome=None, finished_ts=None)
        elif kind == "run_finished":
            terminal_pending = False
            state.update(outcome=event["outcome"], summary=event["summary"], finished_ts=event["ts"])
            if state["step"] and state["purpose"] == "experiment":
                state["steps"][state["step"]] = event["outcome"]
    # NEW1 predictions are provisional until successful durable closeout; a
    # later halt also revokes their visibility without changing the event log.
    prediction_ids = {"H-COV", "H-TOP", "H-RANK", "H-OVERLAP"}
    new1_run = state["step"] == 4 and state["title"].startswith("NEW1 ")
    provisional = {key for key, gate in gates.items() if key in prediction_ids and
                   (new1_run or isinstance(gate["observed"], dict) and gate["observed"].get("provisional") is True)}
    committed = state["outcome"] == "PASS" and state["finished_ts"] is not None and state["halt"] is None
    if (new1_run or provisional) and not committed:
        gates = {key: gate for key, gate in gates.items() if key not in provisional}
        state["findings"] = [finding for finding in state["findings"] if finding["finding_id"] != "NEW1"]
        for stage in state["stages"]:
            if stage["stage"] in prediction_ids:
                stage.pop("outcome", None); stage.pop("finished_ts", None)
                stage["summary"] = "Provisional math estimate; no prediction verdict"
        if state["halt"]: state["outcome"] = None
        state["summary"] = "No prediction verdict; NEW1 publication incomplete or halted"
    state["gates"] = list(gates.values())
    state["gate_outcomes"] = {key: gate_outcome(gate) for key, gate in gates.items()}
    state["calibration_outcome"] = state["gate_outcomes"].get("calibration")
    required = {"inertness": {"law5", "observer-parity"}, "law3": {"law3"}, "2a": {"2a"},
                "calibration": {"calibration"}, "2b": {"2b"}}
    for key, _, _ in GATE_PLAN:
        identifiers = [identifier for identifier in gates if gate_group(identifier) == key]
        outcomes = [state["gate_outcomes"][identifier] for identifier in identifiers]
        complete = bool(identifiers) and required.get(key, set()) <= set(identifiers)
        outcome = "INVALID" if "INVALID" in outcomes else "FAIL" if "FAIL" in outcomes else "PASS" if complete else None
        state["gate_groups"][key] = {"gate_ids": identifiers, "outcome": outcome, "complete": complete}
    if not explicit_purpose and state["admission"] and not state["stages"]:
        state["purpose"] = "admission"
    if state["purpose"] == "admission":
        state["steps"] = {i: "not started" for i in range(1, 5)}
    if state["halt"]:
        state["status"] = "halted"
        if state["step"] and state["purpose"] == "experiment":
            state["steps"][state["step"]] = "INVALID"
    elif terminal_pending:
        state["status"] = "invalid: no verdict"
        state["summary"] = "Terminal publication incomplete; no run verdict"
        if state["step"] and state["purpose"] == "experiment":
            state["steps"][state["step"]] = "INVALID"
    elif state["outcome"]:
        state["status"] = "stopped: check failed" if state["outcome"] == "FAIL" else "finished"
    elif state["step"] == 3 and state["purpose"] == "experiment" and state["calibration_outcome"] in ("FAIL", "INVALID"):
        outcome = state["calibration_outcome"]
        state["status"] = "stopped: check failed" if outcome == "FAIL" else "invalid: no verdict"
        state["steps"][3] = outcome
    return state
