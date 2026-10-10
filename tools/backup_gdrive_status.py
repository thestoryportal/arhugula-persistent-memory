#!/usr/bin/env python3
"""Read backup health, or atomically publish the wrapper's current heartbeat."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

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
    log = Path(args.log)
    stat = log.stat() if log.exists() else None
    value = {"schema": 1, "run_id": args.run_id, "start": args.start,
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


def launch_failure(path, heartbeat_time):
    """The applet's internal-disk receipt is evidence, never an owner heartbeat."""
    try:
        receipt = json.loads((path.parent/"launch_receipt.json").read_text())
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        return "malformed or unavailable launch receipt: " + str(exc).replace("\n", " ")
    try:
        required = {"schema", "utc", "wrapper_path", "exit_code", "error_number"}
        if (not isinstance(receipt, dict) or not required.issubset(receipt) or
                type(receipt["schema"]) is not int or receipt["schema"] != 1 or
                not isinstance(receipt["wrapper_path"], str) or not receipt["wrapper_path"]):
            return "malformed launch receipt"
        exit_code, error_number = receipt["exit_code"], receipt["error_number"]
        if ((exit_code is None) == (error_number is None) or
                (exit_code is not None and (type(exit_code) is not int or not 0 <= exit_code <= 255)) or
                (error_number is not None and (type(error_number) is not int or error_number == 0))):
            return "malformed launch receipt outcome"
        stamp = dt.datetime.fromisoformat(receipt["utc"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or stamp > dt.datetime.now(dt.timezone.utc):
            return "malformed or future launch receipt timestamp"
        # A refused contender cannot change the active owner's health.
        if exit_code in (0, 75) or error_number == 75:
            return None
        if heartbeat_time is not None:
            latest = dt.datetime.fromisoformat(heartbeat_time.replace("Z", "+00:00"))
            if latest.tzinfo is None:
                return "malformed heartbeat timestamp for launch receipt"
            if stamp <= latest:
                return None
        outcome = "exit %s" % exit_code if exit_code is not None else "error %s" % error_number
        wrapper = receipt["wrapper_path"].replace("\r", "\\r").replace("\n", "\\n")
        return "failed backup launch (%s): %s; at %s" % (outcome, wrapper, receipt["utc"])
    except (ValueError, TypeError, AttributeError, OverflowError) as exc:
        return "malformed launch receipt: " + str(exc).replace("\n", " ")


def health(path):
    try:
        if not path.exists():
            return False, launch_failure(path, None) or "missing heartbeat"
        value = json.loads(path.read_text())
        required = {"schema", "start", "end", "exit_code", "bytes_transferred", "rclone_version",
                    "log_path", "wrapper_log", "wrapper_log_identity", "wrapper_log_offset"}
        if not isinstance(value, dict) or not required.issubset(value) or value["schema"] != 1:
            return False, "malformed heartbeat"
        failure = launch_failure(path, value["end"] or value["start"])
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
        if warnings:
            summary = "; ".join(("deletions suppressed" if w["kind"] == "destination_deletions_suppressed" else
                                  w["kind"].replace("_", " ") + ": " + str(w.get("message", w.get("object", "log")))) for w in warnings)
            summary = summary.replace("\r", "\\r").replace("\n", "\\n")
            return True, "fresh backup with warnings (rclone exit %s): %s; finished %s" % (raw_exit, summary, value["end"])
        return True, "fresh successful backup; finished " + value["end"]
    except (OSError, ValueError, TypeError, AttributeError, OverflowError) as exc:
        return False, "malformed heartbeat or unavailable log: " + str(exc).replace("\n", " ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--heartbeat", default=str(DEFAULT))
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
