"""Storage tab: read-only Drive progress and cached, low-priority project sizes.

Usage: /usr/bin/python3 tools/dashboard_storage.py [--once COLS ROWS]
Only the size cache under ~/Library/Caches/memit-dashboard is written.
"""
import datetime as dt
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_live as live
import backup_gdrive_status as backup_status

MAIN_ROOT = Path("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory")
MIRROR_ROOT = MAIN_ROOT.parent
SCAN_INTERVAL = 15 * 60


def clean(value):
    return str(value).replace("\x1b", "?").replace("\r", "\\r").replace("\n", "\\n")


def size_text(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
        return "unknown"
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if value < 1024 or unit == "TiB":
            return ("%d B" % value) if unit == "B" else ("%.1f %s" % (value, unit))
        value /= 1024


def duration(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value) or value < 0:
        return "unknown"
    seconds = int(value)
    if seconds >= 3600:
        return "%dh %dm" % (seconds//3600, seconds%3600//60)
    if seconds >= 60:
        return "%dm%s" % (seconds//60, (" %ds" % (seconds%60)) if seconds%60 else "")
    return "%ds" % seconds


def epoch(value):
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.timestamp() if parsed.tzinfo is not None else None
    except (ValueError, AttributeError, TypeError, OverflowError):
        return None


def read_run(path):
    stats, first, last, failed, errors = None, None, None, False, []
    with path.open() as stream:
        for number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError("record is not an object")
                stamp = epoch(record.get("time"))
                first = first if first is not None else stamp
                last = stamp if stamp is not None else last
                if "stats" in record:
                    if not isinstance(record["stats"], dict):
                        raise ValueError("stats is not an object")
                    stats = record["stats"]
                if str(record.get("msg", "")).startswith("Failed to sync"):
                    failed = True
            except ValueError as exc:
                if len(errors) < 3:
                    errors.append("%s:%s: %s" % (path.name, number, exc))
    try:
        start = dt.datetime.strptime(path.stem.split("-")[0], "%Y%m%dT%H%M%SZ").replace(tzinfo=dt.timezone.utc).timestamp()
    except ValueError:
        start = first
    stats = stats or {}
    return {"id": path.stem, "start": start, "end": last,
            "elapsed": stats.get("elapsedTime"), "bytes": stats.get("bytes"),
            "outcome": "FAILED (exit unknown)" if failed else "exit unknown",
            "stats": stats, "errors": errors}


def read_backup(home=None):
    home = Path.home() if home is None else Path(home)
    base = home / "Library/Logs/memit-gdrive-backup"
    path = base / "last_run.json"
    heartbeat, errors, unreadable = None, [], False
    try:
        heartbeat = json.loads(path.read_text())
        if not isinstance(heartbeat, dict):
            raise ValueError("heartbeat is not an object")
    except FileNotFoundError:
        pass
    except (OSError, ValueError) as exc:
        heartbeat, unreadable = None, True
        errors.append("Heartbeat: " + clean(exc))
    locked = (home / "Library/Logs/memit-gdrive-backup.lock").is_dir()
    state = ("running" if locked or (heartbeat is not None and heartbeat.get("end") is None) else
             "unavailable" if unreadable else "finished" if heartbeat is not None else "disabled")
    runs = []
    try:
        paths = sorted((base / "runs").glob("*.jsonl"), reverse=True)
        for log in paths:
            try:
                runs.append(read_run(log))
            except OSError as exc:
                errors.append(log.name + ": " + clean(exc))
    except OSError as exc:
        errors.append("Run history: " + clean(exc))
    stats = runs[0]["stats"] if runs else {}
    for run in runs:
        errors.extend(run["errors"])
    if heartbeat is not None:
        run_id = heartbeat.get("run_id") or Path(str(heartbeat.get("log_path", "unknown"))).stem
        run = next((run for run in runs if run["id"] == run_id), None)
        if run is None:
            run = {"id": run_id, "stats": {}, "errors": []}
            runs.append(run)
        start, end = epoch(heartbeat.get("start")), epoch(heartbeat.get("end"))
        warnings = heartbeat.get("warnings")
        warning_count = len(warnings) if isinstance(warnings, list) else "unknown"
        code = heartbeat.get("exit_code")
        run.update(start=start, end=end, bytes=heartbeat.get("bytes_transferred"),
                   elapsed=end-start if start is not None and end is not None else run["stats"].get("elapsedTime"),
                   outcome="RUNNING" if heartbeat.get("end") is None else
                   "exit %s; warnings %s" % (code if code is not None else "unknown", warning_count))
    runs.sort(key=lambda run: (run.get("start") or 0, run["id"]), reverse=True)
    # Public health() and its launch_failure()/generation_state() readers are fixture-proven read-only.
    health = backup_status.health(path)
    return {"state": state, "heartbeat": heartbeat, "stats": stats, "history": runs,
            "health": health, "errors": errors}


def disk_space(path):
    stat = os.statvfs(path)
    total = stat.f_blocks * stat.f_frsize
    used = (stat.f_blocks-stat.f_bfree) * stat.f_frsize
    return {"total": total, "used": used, "free": stat.f_bavail*stat.f_frsize,
            "percent": 100*used/total if total else 0.0}


def scan_sizes(home, main_root=None, mirror_root=None):
    """Expand the checkout once; du sees canonical, non-overlapping targets and never follows nested symlinks."""
    home = Path(home)
    main = MAIN_ROOT if main_root is None else Path(main_root)
    mirror = MIRROR_ROOT if mirror_root is None else Path(mirror_root)
    candidates = []
    def add(group, label, path):
        target = path.resolve(strict=True)
        if target in {Path("/"), Path("/Volumes")} or target.parent == Path("/Volumes"):
            raise OSError("refusing a whole volume size scan: " + str(target))
        candidates.append({"group": group, "label": label, "target": str(target),
                           "symlink": path.is_symlink(), "bytes": None, "included_in": None})
    for path in sorted(main.iterdir()):
        if path.name == ".claude" and path.is_dir() and not path.is_symlink():
            for child in sorted(path.iterdir()):
                add("main", ".claude/"+child.name, child)
        else:
            add("main", path.name, path)
    for path in sorted(mirror.iterdir()):
        if path.resolve(strict=True) != main.resolve(strict=True):
            add("mirror", path.name, path)
    internal = [home/"Backups", home/".claude/jobs", home/"Applications/MemitGdriveBackup.app"]
    internal += sorted((home/"Library/Logs").glob("memit-gdrive-backup*"))
    for path in internal:
        if path.exists() or path.is_symlink():
            add("internal", "~/"+str(path.relative_to(home)), path)
    owners = []
    for entry in sorted(candidates, key=lambda entry: (len(Path(entry["target"]).parts), entry["symlink"])):
        target = Path(entry["target"])
        owner = next((owner for owner in owners if target == Path(owner["target"]) or Path(owner["target"]) in target.parents), None)
        if owner is None:
            owners.append(entry)
        else:
            entry["included_in"] = owner["target"]
    if not owners:
        raise OSError("no project folders found to measure")
    targets = [entry["target"] for entry in owners]
    result = subprocess.run(["/usr/bin/nice", "-n", "19", "/usr/bin/du", "-sk", "-P", *targets],
                            capture_output=True, text=True, timeout=600)
    if result.returncode or result.stderr.strip():
        raise OSError("size scan failed (exit %s): %s" % (result.returncode, clean(result.stderr.strip()) or "du returned no diagnostics"))
    values = {}
    for line in result.stdout.splitlines():
        number, separator, target = line.partition("\t")
        if not separator or not number.strip().isdigit() or target not in targets or target in values:
            raise OSError("malformed or unexpected du output: " + clean(line))
        values[target] = int(number)*1024
    if set(values) != set(targets):
        raise OSError("du did not return every requested project folder")
    for entry in owners:
        entry["bytes"] = values[entry["target"]]
    return sorted(candidates, key=lambda entry: (entry["group"], -(entry["bytes"] if entry["bytes"] is not None else -1), entry["label"]))


def validate_cache(value):
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise ValueError("invalid cache schema")
    measured, entries = value.get("measured_at"), value.get("entries")
    if measured is None:
        if entries is not None:
            raise ValueError("unmeasured cache has sizes")
    elif (not isinstance(measured, (int, float)) or not math.isfinite(measured) or measured < 0 or
          not isinstance(entries, list) or not entries):
        raise ValueError("invalid cached measurement")
    for entry in entries or []:
        if (not isinstance(entry, dict) or entry.get("group") not in {"main", "mirror", "internal"} or
                not isinstance(entry.get("label"), str) or not isinstance(entry.get("target"), str) or
                (entry.get("bytes") is None and not entry.get("included_in")) or
                (entry.get("bytes") is not None and (type(entry["bytes"]) is not int or entry["bytes"] < 0))):
            raise ValueError("invalid cached folder size")
    attempt = value.get("last_attempt", measured or 0)
    if not isinstance(attempt, (int, float)) or not math.isfinite(attempt) or attempt < 0:
        raise ValueError("invalid cache attempt timestamp")
    if value.get("error") is not None and not isinstance(value["error"], str):
        raise ValueError("invalid cache error")
    return value


class SizeCache:
    def __init__(self, home=None, scanner=None, clock=None, path=None):
        self.home = Path.home() if home is None else Path(home)
        self.path = self.home/"Library/Caches/memit-dashboard/storage_sizes.json" if path is None else Path(path)
        self.scanner, self.clock = scanner or scan_sizes, clock or time.time
        self.lock, self.thread, self.measuring = threading.Lock(), None, False
        self.value = {"schema": 1, "measured_at": None, "duration_s": None,
                      "last_attempt": 0, "entries": None, "error": None}
        try:
            value = validate_cache(json.loads(self.path.read_text()))
            if max(value.get("measured_at") or 0, value.get("last_attempt", 0)) > self.clock():
                raise ValueError("cache timestamp is in the future")
            self.value = value
        except FileNotFoundError:
            pass
        except (OSError, ValueError, TypeError) as exc:
            self.value = dict(self.value, error="Size cache: " + clean(exc), last_attempt=0)

    def snapshot(self):
        with self.lock:
            return dict(self.value, measuring=self.measuring)

    def write(self, value):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        name = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=str(self.path.parent), prefix=".storage_sizes.", delete=False) as stream:
                name = stream.name
                json.dump(value, stream, sort_keys=True)
                stream.write("\n")
            os.replace(name, self.path)
        finally:
            if name is not None and os.path.exists(name):
                os.unlink(name)

    def refresh(self):
        with self.lock:
            last = max(self.value.get("last_attempt", 0), self.value.get("measured_at") or 0)
            if self.measuring or (last and self.clock()-last < SCAN_INTERVAL):
                return
            self.measuring = True
            self.value = dict(self.value, last_attempt=self.clock())
            self.thread = threading.Thread(target=self._scan, name="storage-sizes", daemon=True)
            self.thread.start()

    def _scan(self):
        began = time.monotonic()
        previous = self.snapshot()
        previous.pop("measuring")
        try:
            # Persist the attempt before du so a reload cannot start a second scan immediately.
            self.write(previous)
            entries = self.scanner(self.home)
            value = validate_cache(dict(previous, measured_at=self.clock(), duration_s=time.monotonic()-began,
                                        entries=entries, error=None))
            self.write(value)
        except Exception as exc:
            value = dict(previous, error=clean(type(exc).__name__+": "+str(exc)), last_duration_s=time.monotonic()-began)
            try:
                self.write(value)
            except OSError as cache_error:
                value["error"] += "; cache write failed: " + clean(cache_error)
        with self.lock:
            self.value, self.measuring = value, False


def drive_lines(view):
    heartbeat, stats = view["heartbeat"] or {}, view["stats"]
    title = {"disabled": "Backup not switched on yet · waiting for activation",
             "running": "RUNNING · copying to Google Drive",
             "finished": "FINISHED · last backup run", "unavailable": "Backup state unavailable"}[view["state"]]
    lines = ["GOOGLE DRIVE BACKUP", title]
    if heartbeat:
        if view["state"] == "running" and heartbeat.get("end") is not None:
            lines.append("Last completion " + clean(heartbeat["end"]) + " · current heartbeat pending")
        else:
            lines.append(("Started " if view["state"] == "running" else "Ended ") +
                         clean(heartbeat.get("start" if view["state"] == "running" else "end", "unknown")))
    if view["state"] == "running":
        lines += ["Copied %s · Rate %s/s" % (size_text(stats.get("bytes")), size_text(stats.get("speed"))),
                  "Files %s / %s · ETA %s · Elapsed %s" % (stats.get("transfers", "unknown"), stats.get("totalTransfers", "unknown"),
                                                          duration(stats.get("eta")), duration(stats.get("elapsedTime")))]
        if not stats:
            lines.append("Progress unavailable · waiting for rclone's next stats record (1 min)")
    elif heartbeat:
        warnings = heartbeat.get("warnings")
        lines.append("Transferred %s · exit %s (rclone exit %s) · warnings %s" % (
            size_text(heartbeat.get("bytes_transferred")), heartbeat.get("exit_code", "unknown"),
            heartbeat.get("rclone_exit_code", "unknown"), len(warnings) if isinstance(warnings, list) else "unknown"))
    lines.append("Health: " + clean(view["health"][1]))
    if view["errors"]:
        lines.append("Read error: " + clean("; ".join(view["errors"][:2])))
    lines.append("PAST RUNS · newest first")
    for run in view["history"]:
        date = dt.datetime.fromtimestamp(run["start"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M") if run.get("start") is not None else clean(run["id"])
        lines.append(" %s  %s  %s  %s" % (date, duration(run.get("elapsed")), run["outcome"], size_text(run.get("bytes"))))
    if not view["history"]:
        lines.append(" No recorded runs")
    return lines


def disk_lines(cache, room):
    lines = ["DISKS · space measured now"]
    for label, path in (("Internal SSD", "/"), ("memit SSD", "/Volumes/memit")):
        try:
            disk = disk_space(path)
            lines.append("%s: %s used (%0.1f%%) · %s free · %s total" % (
                label, size_text(disk["used"]), disk["percent"], size_text(disk["free"]), size_text(disk["total"])))
        except OSError as exc:
            lines.append(label + ": unavailable · " + clean(exc))
    lines.append("Development and backups share memit's physical SSD; counted once.")
    measured = cache["measured_at"]
    age = "not measured yet" if measured is None else "measured %s min ago" % max(int((time.time()-measured)//60), 0)
    lines.append("Project folders · " + age + (" · measuring…" if cache["measuring"] else " · every 15 min"))
    if cache["error"]:
        lines.append("Size scan error: " + clean(cache["error"]))
    if cache["entries"] is None:
        lines.append("Folder sizes: measuring…" if cache["measuring"] else "Folder sizes unavailable; no completed measurement")
        return lines
    groups = [("main", "MAIN CHECKOUT · " + str(MAIN_ROOT)),
              ("mirror", "MIRROR · checkout expanded above · " + str(MIRROR_ROOT)),
              ("internal", "INTERNAL PROJECT FILES · under $HOME")]
    remaining = max(room-len(lines)-len(groups), 0)
    counts = [remaining*2//4, remaining//4, remaining-remaining*2//4-remaining//4]
    for (group, title), count in zip(groups, counts):
        entries = [entry for entry in cache["entries"] if entry["group"] == group]
        entries.sort(key=lambda entry: -(entry["bytes"] if entry["bytes"] is not None else -1))
        lines.append(title + " · top %s/%s" % (min(count, len(entries)), len(entries)))
        for entry in entries[:count]:
            label = clean(entry["label"])
            if entry["symlink"]:
                label += " [symlink] → " + clean(entry["target"])
            if entry["included_in"]:
                lines.append(" included  " + label + " · counted at " + clean(entry["included_in"]))
            else:
                lines.append(" %s  %s" % (size_text(entry["bytes"]), label))
    return lines


def render(cols, rows, cache):
    cols, rows = max(cols, 2), max(rows, 1)
    upper = max(rows//2, 1)
    try:
        drive = drive_lines(read_backup())
    except Exception as exc:
        drive = ["GOOGLE DRIVE BACKUP · read error: " + clean(exc)]
    top = (["■ STORAGE · Drive backup and project disks"] + drive)[:upper]
    top += [""]*(upper-len(top))
    bottom = disk_lines(cache.snapshot(), rows-upper)
    return [live.clip(line, cols-1) for line in (top+bottom)[:rows]]


def main(cache=None):
    cache = SizeCache() if cache is None else cache
    if sys.argv[1:2] == ["--once"]:
        cols, rows = map(int, sys.argv[2:4])
        cache.refresh()
        print("\n".join(render(cols, rows, cache)))
        return
    stamp = live.source_stamp(live.TOOLS)
    drawn = None
    while True:
        # Complete/persist an active scan before re-exec so its du child is not abandoned.
        if not cache.snapshot()["measuring"]:
            live.maybe_reload(stamp)
        cache.refresh()
        try:
            size = os.get_terminal_size(sys.stdout.fileno())
        except OSError:
            size = os.terminal_size((80, 24))
        lines = render(size.columns, size.lines, cache)
        clear = "\033[2J\033[3J" if size != drawn else ""
        sys.stdout.write(clear + "\033[H" + "".join(line+"\033[K\n" for line in lines[:-1]) + lines[-1] + "\033[K\033[J")
        sys.stdout.flush()
        drawn = size
        time.sleep(5)


if __name__ == "__main__":
    main()
