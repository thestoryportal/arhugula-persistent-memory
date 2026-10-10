#!/usr/bin/env python3
"""Read backup health, or atomically publish the wrapper's current heartbeat."""
import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

MAX_UNRESOLVED_INTERVALS = 64
MAX_UNRESOLVED_BYTES = 2048

DEFAULT = Path.home()/"Library/Logs/memit-gdrive-backup/last_run.json"
AUTH_ERROR = re.compile(r"invalid_grant|invalid_client|unauthori[sz]ed|authentication failed|"
                        r"cannot fetch token|token.*(?:expired|invalid|revoked)|"
                        r"insufficient authentication scopes|invalid authentication credentials", re.I)
SKIPPED_OPERATION = re.compile(r"--dry-run\b|\bdry run\b|^\s*skipp(?:ed|ing)\b", re.I)


def skipped_operations(text):
    for line in text.splitlines():
        try:
            message = json.loads(line).get("msg", "")
        except (ValueError, AttributeError):
            message = line
        if isinstance(message, str) and SKIPPED_OPERATION.search(message):
            return True
    return False


def preflight(rclone, source, destination):
    # RCLONE_CONFIG selects credentials; all other RCLONE_* settings need review.
    settings = sorted(name for name in os.environ if name.startswith("RCLONE_") and name != "RCLONE_CONFIG")
    if settings:
        raise ValueError("unapproved environment settings: " + ", ".join(settings))
    for path in (source, destination):
        if not os.path.isabs(path) and (path.startswith(":") or "," in path.split(":", 1)[0]):
            raise ValueError("remote connection-string overrides are not admitted")
    result = subprocess.run([rclone, "config", "dump"], capture_output=True, text=True, timeout=30)
    if result.returncode or not result.stdout.strip():
        raise ValueError("rclone config probe failed (exit %s); no sync dispatched" % result.returncode)
    try:
        config = json.loads(result.stdout)
    except ValueError as exc:
        raise ValueError("rclone config probe returned malformed JSON") from exc
    if (not isinstance(config, dict) or any(not isinstance(section, dict) or
            any(not isinstance(key, str) or not isinstance(value, str) for key, value in section.items())
            for section in config.values())):
        raise ValueError("rclone config probe returned an invalid configuration")
    overrides = sorted(section + "." + key for section, fields in config.items() for key in fields
                       if key.lower().startswith(("global.", "override.")))
    if overrides:
        # Never print configuration values: the same dump contains OAuth secrets.
        raise ValueError("unapproved remote global overrides: " + ", ".join(overrides))


def classify(source, run_log, raw_exit):
    """Normalize only a complete, independently checked local-source ENOENT run."""
    value = {"rclone_exit_code": raw_exit, "warnings": [], "source_vanish_only": False,
             "bytes_transferred": None, "stats_status": "missing", "operations_skipped": False}

    def unique_fields(pairs):
        result = {}
        for key, field in pairs:
            if key in result:
                raise ValueError("duplicate JSON field: " + key)
            result[key] = field
        return result

    def invalid_constant(name):
        raise ValueError("invalid JSON constant: " + name)

    try:
        text = Path(run_log).read_text()
        value["operations_skipped"] = skipped_operations(text)
        items = [json.loads(line, object_pairs_hook=unique_fields, parse_constant=invalid_constant) for line in text.splitlines()]
        if any(not isinstance(item, dict) or not isinstance(item.get("level"), str) or
               ("msg" in item and not isinstance(item["msg"], str)) for item in items):
            raise ValueError("invalid rclone log record")
    except (OSError, ValueError) as exc:
        value.update(stats_status="malformed")
        value["warnings"].append({"kind": "rclone_log_unverified"})
        print("backup_gdrive_status: rclone log unavailable or malformed: " + str(exc), file=sys.stderr)
        return value

    source = Path(source).absolute()
    try:
        root = source.resolve(strict=True)
        root_ok = root.is_dir()
    except OSError:
        root, root_ok = source, False

    def missing_local(item):
        name = item.get("object")
        if not isinstance(name, str) or not name or "\x00" in name:
            return None
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != name:
            return None
        match = re.fullmatch(r"Failed to copy: (failed to open source object: lstat (.+): no such file or directory)", item.get("msg", ""))
        if (not root_ok or item.get("objectType") != "*local.Object" or not match or
                match[2] not in {str(source/relative), str(root/relative)}):
            return None
        candidate = root/relative
        try:
            # --links never traverses source symlinks, so a symlinked parent is not proof.
            if candidate.parent.resolve(strict=False) != candidate.parent:
                return None
            candidate.lstat()
        except FileNotFoundError:
            if not root.is_dir():
                return None
            return match[1]
        except OSError:
            return None
        return None

    valid = bool(items) and text.endswith("\n") and not AUTH_ERROR.search(text) and not value["operations_skipped"]
    pending = []
    suppressed = set()
    last_attempt = None
    final_stats = None
    attempt_number = 0
    attempts_total = None
    malformed_stats = False
    for item in items:
        level, message = item["level"].lower(), item.get("msg", "")
        if "stats" in item:
            stats = item["stats"]
            if isinstance(stats, dict) and type(stats.get("bytes")) is int and stats["bytes"] >= 0:
                value.update(bytes_transferred=stats["bytes"], stats_status="recorded")
            else:
                valid = False
                malformed_stats = True
            final_stats = stats if isinstance(stats, dict) and level == "notice" else None
            if (not isinstance(stats, dict) or type(stats.get("errors")) is not int or
                    stats["errors"] < 0 or stats.get("fatalError") is not False):
                valid = False
        if level == "notice" and message == "Can't transfer non file/directory" and isinstance(item.get("object"), str):
            warning = {"kind": "nonregular_source_skipped", "object": item["object"]}
            if warning not in value["warnings"]:
                value["warnings"].append(warning)
        if level == "error":
            detail = missing_local(item)
            if detail:
                pending.append(detail)
                warning = {"kind": "source_vanished", "object": item["object"]}
                if warning not in value["warnings"]:
                    value["warnings"].append(warning)
            elif message in {"not deleting files as there were IO errors", "not deleting directories as there were IO errors"}:
                suppressed.add(message)
            else:
                attempt = re.fullmatch(r"Attempt (\d+)/(\d+) failed with (\d+) errors and: (.+)", message)
                if not attempt:
                    valid = False
                    continue
                number, total, errors = map(int, attempt.groups()[:3])
                if (number != attempt_number+1 or number > total or
                        (attempts_total is not None and total != attempts_total) or
                        errors != len(pending) or not pending or attempt[4] not in pending or len(suppressed) != 2):
                    valid = False
                last_attempt = (errors, set(pending), set(suppressed))
                attempt_number, attempts_total = number, total
                pending, suppressed = [], set()
                final_stats = None
        elif level == "warning":
            warning = {"kind": "rclone_warning", "message": message}
            if isinstance(item.get("object"), str):
                warning["object"] = item["object"]
            value["warnings"].append(warning)
            valid = False
        elif level not in {"debug", "info", "notice"}:
            valid = False

    terminal = re.fullmatch(r"Failed to sync(?: with (\d+) errors)?: (.+)", items[-1].get("msg", "")) if items else None
    if (raw_exit == 1 and valid and not pending and last_attempt and terminal and
            items[-1]["level"].lower() == "notice" and attempt_number == attempts_total and
            final_stats and final_stats.get("errors") == last_attempt[0] and
            type(final_stats.get("errors")) is int and final_stats["errors"] > 0 and
            final_stats.get("fatalError") is False and final_stats.get("transferring") in (None, []) and
            final_stats.get("retryError", True) is True and
            final_stats.get("lastError", terminal[2]) == terminal[2] and
            terminal[2] in last_attempt[1] and
            (terminal[1] is None or int(terminal[1]) == last_attempt[0]) and
            len(last_attempt[2]) == 2):
        value["source_vanish_only"] = True
        value["warnings"].append({"kind": "destination_deletions_suppressed"})
    if not text.endswith("\n"):
        value["warnings"].append({"kind": "rclone_log_unverified"})
    if malformed_stats:
        value.update(bytes_transferred=None, stats_status="malformed")
        value["warnings"].append({"kind": "rclone_log_unverified"})
    return value


def record(args):
    text = args.launch_generation
    if text and (not re.fullmatch(r"[1-9][0-9]{0,9}", text) or int(text) > 2147483647):
        raise ValueError("invalid launch generation; no heartbeat published")
    generation = int(text) if text else None
    log = Path(args.log)
    stat = log.stat() if log.exists() else None
    value = {"schema": 1, "run_id": args.run_id, "start": args.start,
             "launch_generation": generation, "launch_mode": "applet" if generation is not None else "manual",
             "end": dt.datetime.now(dt.timezone.utc).isoformat() if args.phase == "end" else None,
             "exit_code": args.exit_code if args.phase == "end" else None,
             "bytes_transferred": 0 if not args.sync_started else None,
             "rclone_version": args.rclone_version or None, "log_path": args.run_log,
             "wrapper_log": str(log), "wrapper_log_offset": stat.st_size if stat else 0,
             "wrapper_log_identity": [stat.st_dev, stat.st_ino] if stat else None,
             "rclone_exit_code": args.rclone_exit_code if args.phase == "end" and args.sync_started else None,
             "owner_pid": args.owner_pid, "rclone_pid": args.rclone_pid or None,
             "warnings": []}
    if args.phase == "end" and args.sync_started:
        outcome = json.loads(args.outcome_json) if args.outcome_json else {}
        for key in ("bytes_transferred", "stats_status", "warnings"):
            if key in outcome:
                value[key] = outcome[key]
        value.setdefault("stats_status", "missing")
        if value["stats_status"] == "missing":
            print("backup_gdrive_status: no rclone stats; transferred bytes unknown", file=sys.stderr)
    path = Path(args.heartbeat)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".last_run.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def valid_generation(value):
    return type(value) is int and 0 < value <= 2147483647


def generation_state(path):
    value = json.loads(path.read_text())
    if (not isinstance(value, dict) or type(value.get("schema")) is not int or value["schema"] != 1 or
            type(value.get("issued_generation")) is not int or not 0 <= value["issued_generation"] <= 2147483647 or
            not isinstance(value.get("unresolved"), list) or "recovery_barrier" not in value or
            (value["recovery_barrier"] is not None and
             (not valid_generation(value["recovery_barrier"]) or value["recovery_barrier"] > value["issued_generation"]))):
        raise ValueError("malformed unresolved generation state")
    barrier = value.get("compaction_barrier")
    if barrier is not None and (not valid_generation(barrier) or barrier > value["issued_generation"]):
        raise ValueError("malformed compacted generation barrier")
    last = 0
    for span in value["unresolved"]:
        if (not isinstance(span, list) or len(span) != 2 or not all(map(valid_generation, span)) or
                not last < span[0] <= span[1] <= value["issued_generation"]):
            raise ValueError("malformed unresolved generation set")
        last = span[1]
    return value


def compact_generation_state(state):
    """Fold overflow into a completion-only barrier covering every issued generation."""
    state = dict(state, compaction_barrier=state.get("compaction_barrier"))
    size = len((json.dumps(state, separators=(",", ":"))+"\n").encode())
    if len(state["unresolved"]) > MAX_UNRESOLVED_INTERVALS or size > MAX_UNRESOLVED_BYTES:
        state = {"schema": 1, "issued_generation": state["issued_generation"], "unresolved": [],
                 "recovery_barrier": state["recovery_barrier"],
                 "compaction_barrier": state["issued_generation"]}
    return state


def atomic_write(path, text):
    fd, temporary = tempfile.mkstemp(prefix=".recovery.", dir=path.parent)
    with os.fdopen(fd, "w") as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def recover(args):
    """Preserve ambiguous evidence and reserve a barrier, under the allocator lock."""
    if type(args.generation_floor) is not int or not 0 <= args.generation_floor < 2147483646:
        raise ValueError("recovery floor must allow a barrier and a subsequent allocation")
    heartbeat = Path(args.heartbeat)
    logs = heartbeat.parent.parent
    state_dir = logs/"memit-gdrive-backup-launch-state"
    counter = state_dir/"counter"
    state_path = state_dir/"unresolved.json"
    archives = state_dir/"recoveries"

    def inspect_history():
        state = generation_state(state_path) if state_path.exists() else None
        highest = state["issued_generation"] if state else 0
        pending = list(state["unresolved"]) if state else []
        ambiguous = []
        evidence = [heartbeat, heartbeat.parent/"launch_receipt.json",
                    logs/"memit-gdrive-backup-launch-journal/failures.jsonl",
                    heartbeat.parent/"refusals/latest-refusal.json"]
        archives = state_dir/"recoveries"

        def observe(record):
            nonlocal highest
            if isinstance(record, dict):
                for key in ("launch_generation", "issued_generation", "recovery_barrier", "compaction_barrier", "highest_seen", "generation_floor"):
                    number = record.get(key)
                    if valid_generation(number):
                        highest = max(highest, number)

        # Prior barriers remain authoritative even after a counter is repaired lower.
        if archives.exists():
            for manifest in sorted(archives.glob("*/manifest.json")):
                record = json.loads(manifest.read_text())
                if not isinstance(record, dict) or not valid_generation(record.get("recovery_barrier")):
                    raise ValueError("malformed preserved recovery manifest")
                observe(record)
        for preserved_counter in [counter, *sorted(archives.rglob("counter"))]:
            if not preserved_counter.exists():
                continue
            text = preserved_counter.read_text()
            if re.fullmatch(r"(?:0|[1-9][0-9]{0,9})\n?", text) and int(text) <= 2147483647:
                highest = max(highest, int(text))
        # Older recovery manifests can understate the generations in their payloads.
        preserved = [path for path in sorted(archives.rglob("*"))
                     if path.is_file() and path.suffix in (".json", ".jsonl") and path.name != "manifest.json"]
        for path in evidence + preserved:
            if not path.exists():
                continue
            lines = path.read_bytes().splitlines() if path.suffix == ".jsonl" else [path.read_bytes()]
            records = []
            uncertain = not lines
            for line in lines:
                try:
                    records.append(json.loads(line))
                except ValueError:
                    uncertain = True
            for value in records:
                observe(value)
                if not isinstance(value, dict):
                    uncertain = True
                    continue
                generation = value.get("launch_generation")
                manual = path == heartbeat and generation is None and value.get("launch_mode", "manual") == "manual"
                if not manual and not valid_generation(generation):
                    uncertain = True
            if uncertain and path in evidence:
                ambiguous.append(path)
        if args.generation_floor < highest:
            raise ValueError("generation floor %s is below observed maximum %s; no recovery evidence changed" %
                             (args.generation_floor, highest))
        if highest >= 2147483646:
            raise ValueError("generation space exhausted; no recovery dispatch is possible")
        return state, pending, ambiguous, highest

    # Reject an already-too-low floor before creating even a directory or lock.
    inspect_history()
    state_dir.mkdir(parents=True, exist_ok=True)
    with (state_dir/"counter.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if (logs/"memit-gdrive-backup.lock").exists():
            raise ValueError("backup ownership lock exists; inspect owner/child before recovery")
        state, pending, ambiguous, highest = inspect_history()
        highest = max(args.generation_floor, highest)
        barrier = highest + 1
        # A barrier covers all prior evidence without claiming any backup completed.
        pending = pending if state else ([[1, highest]] if highest else [])
        state = compact_generation_state({"schema": 1, "issued_generation": barrier, "unresolved": pending,
                                          "recovery_barrier": barrier})
        archive = archives/(dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
        archive.mkdir(parents=True, exist_ok=False)
        manifest = {"schema": 1, "generation_floor": args.generation_floor, "highest_seen": highest,
                    "recovery_barrier": barrier, "preserved_paths": [str(path) for path in ambiguous] + ([str(counter)] if counter.exists() else [])}
        atomic_write(archive/"manifest.json", json.dumps(manifest, sort_keys=True)+"\n")
        # A crash before the counter rename leaves mismatched state or ambiguity,
        # so allocation refuses. No ambiguous evidence is discarded.
        atomic_write(state_path, json.dumps(state, sort_keys=True, separators=(",", ":"))+"\n")
        for path in ambiguous:
            os.replace(path, archive/path.name)
        if counter.exists():
            os.replace(counter, archive/"counter")
        atomic_write(counter, str(barrier)+"\n")
        print("backup_gdrive_status: recovery barrier generation %s; preserved evidence: %s; "
              "requires a subsequent completed generation above the barrier" % (barrier, archive))


def launch_failure(path, heartbeat):
    """Only a completed generation can acknowledge launch evidence."""
    heartbeat = heartbeat or {}
    generation = heartbeat.get("launch_generation")
    mode = heartbeat.get("launch_mode", "manual" if generation is None else "applet")
    if ((generation is not None and not valid_generation(generation)) or
            mode != ("manual" if generation is None else "applet")):
        return "malformed heartbeat launch generation"
    completed = generation if heartbeat.get("end") is not None and heartbeat.get("exit_code") is not None else None
    counter_path = path.parent.parent/"memit-gdrive-backup-launch-state/counter"
    try:
        text = counter_path.read_text()
        if not re.fullmatch(r"(?:0|[1-9][0-9]{0,9})\n?", text) or int(text) > 2147483647:
            return "malformed launch generation counter"
        counter = int(text)
    except FileNotFoundError:
        counter = None
    except OSError as exc:
        return "unavailable launch generation counter: " + str(exc).replace("\n", " ")
    state = None
    try:
        state = generation_state(counter_path.parent/"unresolved.json")
        if state["issued_generation"] != counter:
            return "unresolved generation state differs from its counter; recovery required"
    except FileNotFoundError:
        pass
    except (OSError, ValueError) as exc:
        return "malformed or unavailable unresolved generations: " + str(exc).replace("\n", " ")
    journal = path.parent.parent/"memit-gdrive-backup-launch-journal/failures.jsonl"
    markers = []
    try:
        lines = journal.read_text().splitlines()
        if not 0 < len(lines) <= 64 or journal.stat().st_size > 65536:
            return "malformed launch failure journal"
        for line in lines:
            marker = json.loads(line)
            if (not isinstance(marker, dict) or type(marker.get("schema")) is not int or marker["schema"] != 1 or
                    not valid_generation(marker.get("launch_generation")) or
                    not isinstance(marker.get("reason"), str) or not marker["reason"]):
                return "ambiguous launch generation in failure journal"
            if counter is None or marker["launch_generation"] > counter:
                return "failure journal generation exceeds or lacks its counter"
            markers.append(marker)
    except FileNotFoundError:
        pass
    except (OSError, ValueError) as exc:
        return "malformed or unavailable launch failure journal: " + str(exc).replace("\n", " ")
    receipt = None
    try:
        receipt = json.loads((path.parent/"launch_receipt.json").read_text())
        if not isinstance(receipt, dict):
            return "malformed launch receipt"
    except FileNotFoundError:
        pass
    except (OSError, ValueError) as exc:
        return "malformed or unavailable launch receipt: " + str(exc).replace("\n", " ")
    if receipt is not None:
        required = {"schema", "utc", "wrapper_path", "exit_code", "error_number"}
        if (not isinstance(receipt, dict) or not required.issubset(receipt) or
                type(receipt["schema"]) is not int or receipt["schema"] != 1 or
                not isinstance(receipt["wrapper_path"], str) or not receipt["wrapper_path"]):
            return "malformed launch receipt"
        if not valid_generation(receipt.get("launch_generation")):
            return "missing or malformed launch receipt generation"
        exit_code, error_number = receipt["exit_code"], receipt["error_number"]
        if ((exit_code is None) == (error_number is None) or
                (exit_code is not None and (type(exit_code) is not int or not 0 <= exit_code <= 255)) or
                (error_number is not None and (type(error_number) is not int or error_number == 0))):
            return "malformed launch receipt outcome"
        try:
            stamp = dt.datetime.fromisoformat(receipt["utc"].replace("Z", "+00:00"))
        except (ValueError, TypeError, AttributeError, OverflowError):
            return "malformed launch receipt timestamp"
        if stamp.tzinfo is None or stamp > dt.datetime.now(dt.timezone.utc):
            return "malformed or future launch receipt timestamp"
        if counter is None:
            return "missing launch generation counter"
        if receipt["launch_generation"] > counter:
            return "non-increasing launch generation counter below receipt"
    if generation is not None and (counter is None or counter < generation):
        return "missing or non-increasing launch generation counter below heartbeat"
    manual = "; manual/unsequenced heartbeat cannot acknowledge applet evidence" if generation is None else ""
    if state is not None and state["recovery_barrier"] is not None and (completed or 0) <= state["recovery_barrier"]:
        return "unacknowledged recovery barrier generation %s: requires a subsequent completed heartbeat%s" % (
            state["recovery_barrier"], manual)
    if state is not None and state.get("compaction_barrier") is not None and (completed or 0) <= state["compaction_barrier"]:
        return "unacknowledged compacted barrier generation %s: requires a subsequent completed sequenced heartbeat%s" % (
            state["compaction_barrier"], manual)
    if any(marker["launch_generation"] > (completed or 0) for marker in markers):
        return "failed backup launch: unacknowledged failure journal generation" + manual
    if receipt is not None:
        exit_code, error_number = receipt["exit_code"], receipt["error_number"]
        if exit_code not in (0, 75) and error_number != 75 and receipt["launch_generation"] > (completed or 0):
            outcome = "exit %s" % exit_code if exit_code is not None else "error %s" % error_number
            wrapper = receipt["wrapper_path"].replace("\r", "\\r").replace("\n", "\\n")
            return "failed backup launch (%s), generation %s: %s; at %s%s" % (
                outcome, receipt["launch_generation"], wrapper, receipt["utc"], manual)
    pending = None
    if state is not None:
        pending = next((max(low, (completed or 0)+1) for low, high in state["unresolved"]
                        if high > (completed or 0)), None)
    elif counter is not None and counter > (completed or 0):
        # Import legacy evidence conservatively: a refusal clears its own launch.
        pending = (completed or 0)+1
        if receipt is not None and (receipt["exit_code"] == 75 or receipt["error_number"] == 75):
            if receipt["launch_generation"] == pending:
                pending = pending+1 if pending < counter else None
    if pending is not None:
        if heartbeat and (heartbeat.get("end") is None or heartbeat.get("exit_code") is None):
            return None  # health() will report the owner's incomplete run.
        return "unacknowledged launch generation %s: no completed heartbeat%s" % (pending, manual)
    return None

def health(path):
    try:
        if not path.exists():
            return False, launch_failure(path, None) or "missing heartbeat"
        value = json.loads(path.read_text())
        required = {"schema", "start", "end", "exit_code", "bytes_transferred", "rclone_version",
                    "log_path", "wrapper_log", "wrapper_log_identity", "wrapper_log_offset"}
        if not isinstance(value, dict) or not required.issubset(value) or value["schema"] != 1:
            return False, "malformed heartbeat"
        failure = launch_failure(path, value)
        if failure:
            return False, failure
        if value["end"] is None or value["exit_code"] is None:
            owner, child = value.get("owner_pid"), value.get("rclone_pid")
            if type(owner) is int and owner > 0 and (child is None or type(child) is int and child > 0):
                def alive(pid):
                    if pid is None:
                        return False
                    try:
                        os.kill(pid, 0)
                        return True
                    except ProcessLookupError:
                        return False
                    except PermissionError:
                        return True
                if not alive(owner) and not alive(child):
                    return False, "stale incomplete backup: owner and rclone PIDs are dead"
            return False, "incomplete backup run"
        if type(value["exit_code"]) is not int:
            return False, "malformed exit code"
        run_log = Path(value["log_path"])
        if run_log.exists():
            text = run_log.read_text()
            if AUTH_ERROR.search(text):
                return False, "token/auth error detected in last run log"
            if skipped_operations(text):
                return False, "failed/unverified backup: dry-run or skipped operations in last run log"
        if value["exit_code"] != 0:
            return False, "failed backup (exit %s)" % value["exit_code"]
        start, end = (dt.datetime.fromisoformat(value[key].replace("Z", "+00:00")) for key in ("start", "end"))
        now = dt.datetime.now(dt.timezone.utc)
        if start.tzinfo is None or end.tzinfo is None or end < start:
            return False, "malformed heartbeat timestamps"
        if end > now:
            return False, "future heartbeat timestamp"
        if now-end >= dt.timedelta(hours=13):
            return False, "stale backup (finished at least 13 hours ago)"
        size = value["bytes_transferred"]
        if (size is not None and (type(size) is not int or size < 0)) or not value["rclone_version"]:
            return False, "malformed heartbeat measurements"
        wrapper = Path(value["wrapper_log"])
        stat = wrapper.stat()
        offset = value["wrapper_log_offset"]
        if ([stat.st_dev, stat.st_ino] != value["wrapper_log_identity"] or
                type(offset) is not int or offset < 0 or stat.st_size < offset):
            return False, "wrapper log rotated or truncated; last-run diagnostics unavailable"
        with wrapper.open("rb") as stream:
            stream.seek(offset)
            if b"HEARTBEAT-FAILED" in stream.read():
                return False, "newer heartbeat publication failed"
        if not run_log.is_file():
            return False, "last run log missing"
        warnings = value.get("warnings", [])
        kinds = {"source_vanished", "destination_deletions_suppressed", "nonregular_source_skipped", "rclone_log_unverified", "rclone_warning"}
        if (not isinstance(warnings, list) or any(not isinstance(warning, dict) or
                warning.get("kind") not in kinds for warning in warnings)):
            return False, "malformed heartbeat warnings"
        for warning in warnings:
            if (warning["kind"] in {"source_vanished", "nonregular_source_skipped"} and
                    (not isinstance(warning.get("object"), str) or not warning["object"])):
                return False, "malformed heartbeat warning object"
            if warning["kind"] == "rclone_warning" and not isinstance(warning.get("message"), str):
                return False, "malformed heartbeat warning message"
        raw_exit = value.get("rclone_exit_code")
        if raw_exit is not None and (type(raw_exit) is not int or raw_exit not in (0, 1)):
            return False, "malformed heartbeat rclone exit code"
        if raw_exit == 1 and not {"source_vanished", "destination_deletions_suppressed"}.issubset({w["kind"] for w in warnings}):
            return False, "malformed source-vanish outcome"
        sequencing = "; manual/unsequenced heartbeat" if value.get("launch_generation") is None else "; launch generation %s" % value["launch_generation"]
        if warnings:
            summary = "; ".join(("deletions suppressed" if w["kind"] == "destination_deletions_suppressed" else
                                  w["kind"].replace("_", " ") + ": " + str(w.get("message", w.get("object", "log")))) for w in warnings)
            summary = summary.replace("\r", "\\r").replace("\n", "\\n")
            return True, "fresh backup with warnings (rclone exit %s): %s; finished %s" % (raw_exit, summary, value["end"]) + sequencing
        return True, "fresh successful backup; finished " + value["end"] + sequencing
    except (OSError, ValueError, TypeError, AttributeError, OverflowError) as exc:
        return False, "malformed heartbeat or unavailable log: " + str(exc).replace("\n", " ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--heartbeat", default=str(DEFAULT))
    if sys.argv[1:2] == ["recover"]:
        parser.add_argument("--generation-floor", type=int, required=True,
                            help="operator-reviewed greatest generation ever issued, including lost history; must be at least every observed generation (lower floors refuse without changing evidence)")
        args = parser.parse_args(sys.argv[2:])
        try:
            recover(args)
            return 0
        except (OSError, ValueError) as exc:
            print("backup_gdrive_status: recovery refused: " + str(exc), file=sys.stderr)
            return 1
    if sys.argv[1:2] == ["preflight"]:
        parser.add_argument("--rclone", required=True)
        parser.add_argument("--source", required=True)
        parser.add_argument("--destination", required=True)
        args = parser.parse_args(sys.argv[2:])
        try:
            preflight(args.rclone, args.source, args.destination)
            return 0
        except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
            print("backup_gdrive_status: preflight refused: " + str(exc), file=sys.stderr)
            return 1
    if sys.argv[1:2] == ["classify"]:
        parser.add_argument("--source", required=True)
        parser.add_argument("--run-log", required=True)
        parser.add_argument("--rclone-exit-code", type=int, required=True)
        args = parser.parse_args(sys.argv[2:])
        outcome = classify(args.source, args.run_log, args.rclone_exit_code)
        print(json.dumps(outcome, sort_keys=True))
        if outcome["operations_skipped"]:
            return args.rclone_exit_code or 1
        return 0 if args.rclone_exit_code == 0 or outcome["source_vanish_only"] else args.rclone_exit_code
    if sys.argv[1:2] == ["record"]:
        parser.add_argument("--phase", choices=("start", "end"), required=True)
        parser.add_argument("--launch-generation", default=os.environ.get("BACKUP_LAUNCH_GENERATION", ""))
        parser.add_argument("--run-id", required=True)
        parser.add_argument("--start", required=True)
        parser.add_argument("--exit-code", type=int, default=0)
        parser.add_argument("--rclone-version", default="")
        parser.add_argument("--log", required=True)
        parser.add_argument("--run-log", required=True)
        parser.add_argument("--sync-started", type=int, choices=(0, 1), default=0)
        parser.add_argument("--rclone-exit-code", type=int)
        parser.add_argument("--outcome-json", default="")
        parser.add_argument("--owner-pid", type=int)
        parser.add_argument("--rclone-pid", type=int, default=0)
        args = parser.parse_args(sys.argv[2:])
        try:
            record(args)
            return 0
        except (OSError, ValueError, TypeError, AttributeError) as exc:
            print("backup_gdrive_status: heartbeat publication failed: " + str(exc), file=sys.stderr)
            return 1
    args = parser.parse_args()
    ok, reason = health(Path(args.heartbeat))
    print("backup_gdrive_status: " + reason)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
