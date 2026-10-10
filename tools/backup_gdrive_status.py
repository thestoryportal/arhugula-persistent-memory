#!/usr/bin/env python3
"""Read backup health, or atomically publish the wrapper's current heartbeat."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import tempfile

DEFAULT = Path.home()/"Library/Logs/memit-gdrive-backup/last_run.json"
AUTH_ERROR = re.compile(r"invalid_grant|invalid_client|unauthori[sz]ed|authentication failed|"
                        r"cannot fetch token|token.*(?:expired|invalid|revoked)|"
                        r"insufficient authentication scopes|invalid authentication credentials", re.I)


def record(args):
    log = Path(args.log)
    stat = log.stat() if log.exists() else None
    value = {"schema": 1, "run_id": args.run_id, "start": args.start,
             "end": dt.datetime.now(dt.timezone.utc).isoformat() if args.phase == "end" else None,
             "exit_code": args.exit_code if args.phase == "end" else None,
             "bytes_transferred": 0 if not args.sync_started else None,
             "rclone_version": args.rclone_version or None, "log_path": args.run_log,
             "wrapper_log": str(log), "wrapper_log_offset": stat.st_size if stat else 0,
             "wrapper_log_identity": [stat.st_dev, stat.st_ino] if stat else None}
    if args.phase == "end" and args.sync_started:
        value["stats_status"] = "missing"
        for line in Path(args.run_log).read_text().splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                value.update(bytes_transferred=None, stats_status="malformed")
                print("backup_gdrive_status: malformed rclone stats; transferred bytes unknown", file=sys.stderr)
                break
            size = item.get("stats", {}).get("bytes")
            if type(size) is int and size >= 0:
                value.update(bytes_transferred=size, stats_status="recorded")
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


def health(path):
    if not path.exists():
        return False, "missing heartbeat"
    try:
        value = json.loads(path.read_text())
        required = {"schema", "start", "end", "exit_code", "bytes_transferred", "rclone_version",
                    "log_path", "wrapper_log", "wrapper_log_identity", "wrapper_log_offset"}
        if not isinstance(value, dict) or not required.issubset(value) or value["schema"] != 1:
            return False, "malformed heartbeat"
        if value["end"] is None or value["exit_code"] is None:
            return False, "incomplete backup run"
        if type(value["exit_code"]) is not int:
            return False, "malformed exit code"
        run_log = Path(value["log_path"])
        if run_log.exists() and AUTH_ERROR.search(run_log.read_text()):
            return False, "token/auth error detected in last run log"
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
        return True, "fresh successful backup; finished " + value["end"]
    except (OSError, ValueError, TypeError, AttributeError, OverflowError) as exc:
        return False, "malformed heartbeat or unavailable log: " + str(exc).replace("\n", " ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--heartbeat", default=str(DEFAULT))
    if sys.argv[1:2] == ["record"]:
        parser.add_argument("--phase", choices=("start", "end"), required=True)
        parser.add_argument("--run-id", required=True)
        parser.add_argument("--start", required=True)
        parser.add_argument("--exit-code", type=int, default=0)
        parser.add_argument("--rclone-version", default="")
        parser.add_argument("--log", required=True)
        parser.add_argument("--run-log", required=True)
        parser.add_argument("--sync-started", type=int, choices=(0, 1), default=0)
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
