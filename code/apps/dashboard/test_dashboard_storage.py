"""MB22 storage criteria: fixtures only; no real backup writes or tmux server calls."""
import ast
import contextlib
import ctypes
import datetime as dt
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest import mock


TOOLS = Path(__file__).resolve().parent
RECEIPTS = os.environ.get("DASHBOARD_STORAGE_RECEIPTS")
FIXTURES = TOOLS.parent / "_archive/projects/dashboard/dashboard_storage_mb22_20261010T192500Z"


def manifest(root):
    entries = {}
    for path in [root] + sorted(root.rglob("*")):
        stat = path.lstat()
        entries[str(path.relative_to(root))] = (
            stat.st_mtime_ns, stat.st_size,
            hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,
        )
    return entries


def seed_backup(home, state):
    base = home / "Library/Logs/memit-gdrive-backup"
    runs = base / "runs"
    runs.mkdir(parents=True)
    wrapper = home / "Library/Logs/memit-gdrive-backup.log"
    wrapper.write_text("wrapper fixture\n")
    if state == "disabled":
        (base / "launch_receipt.json").write_text('{"fixture": "not activated"}\n')
        return {}
    end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0) - dt.timedelta(minutes=30)
    start = end - dt.timedelta(seconds=180)
    run_id = start.strftime("%Y%m%dT%H%M%SZ") + "-22"
    log = runs / (run_id + ".jsonl")
    stats = {"bytes": 12 * 1024**2, "transfers": 7, "totalTransfers": 20,
             "speed": 1024**2, "eta": 120, "elapsedTime": 180.0,
             "errors": 0, "totalBytes": 40 * 1024**2}
    records = [
        {"time": start.isoformat(), "level": "info", "msg": "start"},
        {"time": (end-dt.timedelta(seconds=60)).isoformat(), "level": "notice",
         "msg": "stats", "stats": dict(stats, bytes=1024, transfers=1)},
        {"time": end.isoformat(), "level": "notice", "msg": "stats", "stats": stats},
    ]
    log.write_text("".join(json.dumps(item) + "\n" for item in records))
    stat = wrapper.stat()
    heartbeat = {"schema": 1, "run_id": run_id, "start": start.isoformat(),
                 "end": None if state == "running" else end.isoformat(),
                 "exit_code": None if state == "running" else 0,
                 "bytes_transferred": None if state == "running" else stats["bytes"],
                 "rclone_version": "rclone fixture", "log_path": str(log),
                 "wrapper_log": str(wrapper), "wrapper_log_offset": stat.st_size,
                 "wrapper_log_identity": [stat.st_dev, stat.st_ino],
                 "rclone_exit_code": None if state == "running" else 1,
                 "owner_pid": os.getpid(), "rclone_pid": None,
                 "launch_generation": None, "launch_mode": "manual",
                 "warnings": [] if state == "running" else [
                     {"kind": "source_vanished", "object": ".git/objects/tmp_obj_fixture"},
                     {"kind": "destination_deletions_suppressed"}]}
    (base / "last_run.json").write_text(json.dumps(heartbeat) + "\n")
    dates = [start.date().isoformat()]
    if state == "history":
        for days in (1, 2):
            old = start - dt.timedelta(days=days)
            old_id = old.strftime("%Y%m%dT%H%M%SZ") + "-22"
            old_stats = dict(stats, bytes=days*1024**2, elapsedTime=60*days)
            old_records = [{"time": (old+dt.timedelta(seconds=60*days)).isoformat(),
                            "level": "notice", "msg": "stats", "stats": old_stats}]
            if days == 1:
                old_records.append({"time": (old+dt.timedelta(seconds=60)).isoformat(),
                                    "level": "error", "msg": "Failed to sync: fixture failure"})
            (runs / (old_id + ".jsonl")).write_text(
                "".join(json.dumps(item) + "\n" for item in old_records))
            dates.append(old.date().isoformat())
    return {"heartbeat": heartbeat, "dates": dates, "log": log, "stats": stats}


def seed_cache(path, measured_at):
    path.parent.mkdir(parents=True, exist_ok=True)
    value = {"schema": 1, "measured_at": measured_at, "duration_s": 0.02,
             "last_attempt": measured_at, "error": None, "entries": [
                 {"group": "main", "label": "results", "target": "/fixture/results",
                  "bytes": 1024**3, "symlink": False, "included_in": None},
                 {"group": "mirror", "label": "models", "target": "/fixture/models",
                  "bytes": 2*1024**3, "symlink": False, "included_in": None},
                 {"group": "internal", "label": "~/Backups", "target": "/fixture/Backups",
                  "bytes": 1024**2, "symlink": False, "included_in": None}]}
    path.write_text(json.dumps(value) + "\n")
    return value


class StorageCriteria(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fixture-", dir=str(FIXTURES))
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "home"
        self.home.mkdir()
        self.env = mock.patch.dict(os.environ, {"HOME": str(self.home)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def module(self):
        return importlib.import_module("tools.dashboard_storage")

    def once(self, state, cols, rows=32):
        storage = self.module()
        fixture = seed_backup(self.home, state)
        path = self.home / "Library/Caches/memit-dashboard/storage_sizes.json"
        seed_cache(path, time.time()-420)
        cache = storage.SizeCache(home=self.home)
        output = io.StringIO()
        disk = SimpleNamespace(f_blocks=1000, f_frsize=1024**3, f_bfree=600, f_bavail=600)
        with mock.patch.object(sys, "argv", [str(TOOLS / "dashboard_storage.py"),
                                            "--once", str(cols), str(rows)]), \
             mock.patch.object(storage.os, "statvfs", return_value=disk), \
             contextlib.redirect_stdout(output):
            storage.main(cache=cache)
        text = output.getvalue()
        lines = text.splitlines()
        self.assertLessEqual(len(lines), rows)
        self.assertTrue(all(storage.live.cells(line) <= cols-1 for line in lines))
        self.assertIn("STORAGE", text)
        self.assertIn("Internal SSD", text)
        self.assertIn("memit", text)
        self.assertIn("measured 7 min ago", text)
        if RECEIPTS:
            (Path(RECEIPTS) / ("once_%s_%s.txt" % (state, cols))).write_text(text)
        return text, fixture

    def test_1_launch_matches_gpu_exemption(self):
        text = (TOOLS / "dashboard_storage_tab.sh").read_text()
        launch = re.search(r'"(/usr/bin/python3 [^"\n]*dashboard_storage\.py[^"\n]*)"', text)
        self.assertIsNotNone(launch)
        expected = "/usr/bin/python3 '%s/dashboard_storage.py'" % TOOLS
        command = launch.group(1).replace("$T", str(TOOLS))
        self.assertEqual(command, expected)
        parts = shlex.split(command)
        self.assertEqual(parts, ["/usr/bin/python3", str(TOOLS / "dashboard_storage.py")])
        tree = ast.parse((TOOLS / "c10w_p2_gate.py").read_text())
        patterns = next(ast.literal_eval(node.value) for node in tree.body
                        if isinstance(node, ast.Assign) and
                        any(isinstance(t, ast.Name) and t.id == "EXEMPT" for t in node.targets))
        # sys.executable retains the CLT shim; Darwin reports the actual Python.app binary used by ps.
        binary = ctypes.create_string_buffer(4096)
        length = ctypes.c_uint32(len(binary))
        self.assertEqual(ctypes.CDLL(None)._NSGetExecutablePath(binary, ctypes.byref(length)), 0)
        interpreter = os.path.realpath(os.fsdecode(binary.value))
        actual = interpreter + " " + parts[1]
        self.assertTrue(any(re.fullmatch(pattern, actual) for pattern in patterns), actual)
        self.assertFalse(any(re.fullmatch(pattern, interpreter + " -B " + parts[1])
                             for pattern in patterns))
        if RECEIPTS:
            (Path(RECEIPTS) / "launch_exemption.json").write_text(json.dumps(
                {"launch": command, "darwin_binary": interpreter, "gate_command": actual,
                 "matching_patterns": [pattern for pattern in patterns if re.fullmatch(pattern, actual)]}, indent=2)+"\n")
        team = (TOOLS / "team_dashboard.sh").read_text()
        self.assertEqual(team.count('bash "$T/dashboard_storage_tab.sh" "$NEW"'), 1)
        self.assertIn("7 storage", team[:team.index("T=$(")])

    def test_1_idempotent_launcher_and_visible_failure_with_fake_tmux(self):
        fake = Path(self.temp.name) / "tmux"
        calls = Path(self.temp.name) / "calls"
        windows = Path(self.temp.name) / "windows"
        windows.write_text("team\nscience\n")
        fake.write_text('#!/bin/sh\n'
                        'printf "%s\\n" "$@" >> "$MOCK_CALLS"\n'
                        'case "$1" in\n'
                        'list-windows) cat "$MOCK_WINDOWS";;\n'
                        'new-window) if [ "$MOCK_FAIL" = 1 ]; then exit 3; fi; '
                        'printf "storage\\n" >> "$MOCK_WINDOWS";;\n'
                        '*) exit 4;;\nesac\n')
        fake.chmod(0o755)
        env = dict(os.environ, PATH=str(fake.parent)+":"+os.environ.get("PATH", ""),
                   MOCK_CALLS=str(calls), MOCK_WINDOWS=str(windows), MOCK_FAIL="0")
        script = ["/bin/bash", str(TOOLS / "dashboard_storage_tab.sh")]
        first = subprocess.run(script, capture_output=True, text=True, env=env)
        self.assertEqual(first.returncode, 0, first.stderr)
        second = subprocess.run(script, capture_output=True, text=True, env=env)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("already has a storage tab", second.stdout)
        self.assertEqual(calls.read_text().splitlines().count("new-window"), 1)
        self.assertIn("=dashboard:", calls.read_text())
        windows.write_text("team\n")
        env["MOCK_FAIL"] = "1"
        failed = subprocess.run(script, capture_output=True, text=True, env=env)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("tmux new-window failed", failed.stderr)

    def test_1_live_loop_uses_reload_without_tmux(self):
        storage = self.module()
        class StopLoop(BaseException):
            pass
        path = self.home / "Library/Caches/memit-dashboard/storage_sizes.json"
        seed_cache(path, time.time())
        cache = storage.SizeCache(home=self.home)
        with mock.patch.object(sys, "argv", [str(TOOLS / "dashboard_storage.py")]), \
             mock.patch.object(storage.live, "maybe_reload") as reload, \
             mock.patch.object(storage.time, "sleep", side_effect=StopLoop), \
             mock.patch.object(storage.os, "statvfs", side_effect=OSError("fixture unavailable")), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(StopLoop):
                storage.main(cache=cache)
        reload.assert_called_once()
        self.assertIn("STORAGE", output.getvalue())

    def scan_fixture(self):
        mirror = Path(self.temp.name) / "mirror"
        main = mirror / "arhugula-persistent-memory"
        main.mkdir(parents=True)
        (main / "results").mkdir()
        (main / "results/data").write_bytes(b"r"*8192)
        (main / ".venv").mkdir()
        (main / ".venv/data").write_bytes(b"v"*16384)
        (main / ".claude/worktrees").mkdir(parents=True)
        (main / ".claude/worktrees/data").write_bytes(b"w"*4096)
        (mirror / "models").mkdir()
        (mirror / "models/data").write_bytes(b"m"*65536)
        target = mirror / "covariance-store"
        target.mkdir()
        (target / "data").write_bytes(b"c"*32768)
        (main / "hf_cache").symlink_to(target, target_is_directory=True)
        (main / "covariance_caches").symlink_to(target, target_is_directory=True)
        (self.home / "Backups").mkdir()
        (self.home / "Backups/project").write_bytes(b"b"*4096)
        (self.home / ".claude/jobs").mkdir(parents=True)
        (self.home / ".claude/jobs/job").write_bytes(b"j"*4096)
        (self.home / "Library/Logs/memit-gdrive-backup").mkdir(parents=True)
        (self.home / "Library/Logs/memit-gdrive-backup/launch_receipt.json").write_text("{}\n")
        return main, mirror, target

    def scan(self, main, mirror):
        storage = self.module()
        original_run = subprocess.run
        calls = []
        def fixture_du(args, **kwargs):
            calls.append(args)
            self.assertEqual(args[:5], ["/usr/bin/nice", "-n", "19", "/usr/bin/du", "-sk"])
            self.assertNotIn("python", " ".join(args).lower())
            # Sandbox denies setpriority. This fixture exercises real du only; the requested nice argv is asserted.
            return original_run(args[3:], **kwargs)
        with mock.patch.object(storage.subprocess, "run", side_effect=fixture_du):
            entries = storage.scan_sizes(self.home, main_root=main, mirror_root=mirror)
        return entries, calls

    def test_2_panel_never_invokes_python_subprocess(self):
        storage = self.module()
        source = (TOOLS / "dashboard_storage.py").read_text()
        tree = ast.parse(source)
        calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and
                 isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and
                 node.func.value.id == "subprocess"]
        self.assertTrue(calls, "expected the bounded nice/du boundary")
        self.assertEqual({node.func.attr for node in calls}, {"run"})
        for node in calls:
            self.assertIsInstance(node.args[0], ast.List)
            self.assertEqual(ast.literal_eval(node.args[0].elts[0]), "/usr/bin/nice")
        main, mirror, _ = self.scan_fixture()
        entries, invoked = self.scan(main, mirror)
        self.assertTrue(entries)
        self.assertEqual(len(invoked), 1)
        seed_backup(self.home, "finished")
        with mock.patch.object(storage.subprocess, "run", side_effect=AssertionError("render subprocess")):
            storage.read_backup()
        self.assertIn("sys.dont_write_bytecode = True", source)

    def test_3a_not_switched_on_once_80(self):
        text, _ = self.once("disabled", 80)
        self.assertIn("not switched on yet", text)
        self.assertNotIn("fresh successful backup", text)

    def test_3a_not_switched_on_once_160(self):
        text, _ = self.once("disabled", 160)
        self.assertIn("not switched on yet", text)

    def check_running(self, cols):
        text, _ = self.once("running", cols)
        for expected in ("RUNNING", "12.0 MiB", "Files 7", "1.0 MiB/s", "ETA 2m", "Elapsed 3m"):
            self.assertIn(expected, text)
        self.assertNotIn("1.0 KiB copied", text)

    def test_3b_running_once_80(self):
        self.check_running(80)

    def test_3b_running_once_160(self):
        self.check_running(160)

    def check_finished(self, cols):
        text, fixture = self.once("finished", cols)
        for expected in ("FINISHED", "exit 0", "warnings 2", "12.0 MiB", "Health:",
                         "fresh backup with warnings", fixture["heartbeat"]["end"][:19]):
            self.assertIn(expected, text)

    def test_3c_finished_once_80(self):
        self.check_finished(80)

    def test_3c_finished_once_160(self):
        self.check_finished(160)

    def check_history(self, cols):
        text, fixture = self.once("history", cols)
        history = text[text.index("PAST RUNS"):text.index("DISKS")]
        positions = [history.index(date) for date in fixture["dates"]]
        self.assertEqual(positions, sorted(positions))
        for expected in ("3m", "12.0 MiB", "FAILED", "exit unknown", "2.0 MiB"):
            self.assertIn(expected, history)

    def test_3d_history_once_80(self):
        self.check_history(80)

    def test_3d_history_once_160(self):
        self.check_history(160)

    def test_3b_lock_without_heartbeat_is_running_not_disabled(self):
        storage = self.module()
        fixture = seed_backup(self.home, "running")
        (self.home / "Library/Logs/memit-gdrive-backup/last_run.json").unlink()
        (self.home / "Library/Logs/memit-gdrive-backup.lock").mkdir()
        state = storage.read_backup()
        self.assertEqual(state["state"], "running")
        self.assertEqual(state["stats"]["bytes"], fixture["stats"]["bytes"])
        completed = dict(fixture["heartbeat"], end=dt.datetime.now(dt.timezone.utc).isoformat(), exit_code=0)
        (self.home / "Library/Logs/memit-gdrive-backup/last_run.json").write_text(json.dumps(completed))
        text = "\n".join(storage.drive_lines(storage.read_backup()))
        self.assertIn("Last completion", text)
        self.assertNotIn("Started " + completed["start"], text)

    def test_3_health_is_reused_and_read_only_for_fixture_tree(self):
        storage = self.module()
        fixture = seed_backup(self.home, "finished")
        heartbeat = self.home / "Library/Logs/memit-gdrive-backup/last_run.json"
        value = fixture["heartbeat"]
        counter = self.home / "Library/Logs/memit-gdrive-backup-launch-state"
        counter.mkdir()
        (counter / "counter").write_text("1\n")
        variants = [dict(value, launch_generation=1, launch_mode="applet"),
                    dict(value, exit_code=4), dict(value, end=None, exit_code=None),
                    dict(value, warnings=[], rclone_exit_code=0), None]
        for variant in variants:
            with self.subTest(heartbeat=variant):
                if variant is None:
                    heartbeat.unlink()
                else:
                    heartbeat.write_text(json.dumps(variant)+"\n")
                before = manifest(self.home)
                with mock.patch.object(storage.backup_status, "health", wraps=storage.backup_status.health) as health, \
                     mock.patch.object(storage.subprocess, "run", side_effect=AssertionError("health subprocess")):
                    view = storage.read_backup()
                health.assert_called_once_with(heartbeat)
                if variant is variants[0]:
                    self.assertTrue(view["health"][0], view["health"][1])
                self.assertEqual(before, manifest(self.home))

    def test_3_malformed_and_missing_progress_remain_visible(self):
        storage = self.module()
        fixture = seed_backup(self.home, "running")
        fixture["log"].write_text('{"time":"fixture", "stats": {"bytes": 1}}\n{bad json}\n')
        state = storage.read_backup()
        self.assertTrue(state["errors"])
        (self.home / "Library/Logs/memit-gdrive-backup/last_run.json").write_text("{broken}")
        state = storage.read_backup()
        self.assertEqual(state["state"], "unavailable")
        self.assertTrue(state["errors"])

    def test_4_space_uses_statvfs_and_shared_disk_once(self):
        storage = self.module()
        stat = SimpleNamespace(f_blocks=100, f_frsize=1024, f_bfree=40, f_bavail=30)
        with mock.patch.object(storage.os, "statvfs", return_value=stat) as statvfs:
            disk = storage.disk_space("/")
        statvfs.assert_called_once_with("/")
        self.assertEqual(disk, {"total": 102400, "used": 61440, "free": 30720, "percent": 60.0})
        text, _ = self.once("disabled", 160)
        self.assertEqual(text.count("memit SSD"), 1)
        self.assertIn("Development and backups share", text)
        self.assertIn("total", text)
        self.assertIn("free", text)

    def test_4_symlinks_counted_once_at_target_and_labelled(self):
        main, mirror, target = self.scan_fixture()
        entries, calls = self.scan(main, mirror)
        self.assertEqual(calls[0].count(str(target)), 1)
        self.assertNotIn(str(main / "hf_cache"), calls[0])
        owners = [entry for entry in entries if entry["target"] == str(target) and entry["bytes"] is not None]
        aliases = [entry for entry in entries if entry["target"] == str(target) and entry["symlink"]]
        self.assertEqual(len(owners), 1)
        self.assertEqual(len(aliases), 2)
        self.assertTrue(all(entry["included_in"] for entry in aliases))
        self.assertNotIn(str(main), calls[0])  # The checkout is expanded, never scanned twice via its parent.
        self.assertNotIn(str(main / ".claude"), calls[0])
        (main / "entire-disk").symlink_to("/Volumes/memit", target_is_directory=True)
        with mock.patch.object(self.module().subprocess, "run", side_effect=AssertionError("whole-volume du")):
            with self.assertRaisesRegex(OSError, "whole volume"):
                self.module().scan_sizes(self.home, main_root=main, mirror_root=mirror)

    def test_4_biggest_first_and_internal_project_paths_separate(self):
        main, mirror, _ = self.scan_fixture()
        entries, _ = self.scan(main, mirror)
        for group in ("main", "mirror", "internal"):
            ranked = [entry["bytes"] for entry in entries if entry["group"] == group and entry["bytes"] is not None]
            self.assertEqual(ranked, sorted(ranked, reverse=True))
        main_labels = [entry["label"] for entry in entries if entry["group"] == "main"]
        self.assertIn(".claude/worktrees", main_labels)
        internal = [entry["label"] for entry in entries if entry["group"] == "internal"]
        for label in ("~/Backups", "~/.claude/jobs", "~/Library/Logs/memit-gdrive-backup"):
            self.assertIn(label, internal)

    def test_4_unavailable_mount_is_an_error_not_zero_space(self):
        storage = self.module()
        with mock.patch.object(storage.os, "statvfs", side_effect=OSError("mount unavailable")):
            path = self.home / "Library/Caches/memit-dashboard/storage_sizes.json"
            seed_cache(path, time.time())
            text = "\n".join(storage.render(80, 32, storage.SizeCache(home=self.home)))
        self.assertIn("mount unavailable", text)
        self.assertNotIn("0 B", text)

    def cache(self, measured_at, scanner):
        storage = self.module()
        path = self.home / "Library/Caches/memit-dashboard/storage_sizes.json"
        previous = seed_cache(path, measured_at)
        cache = storage.SizeCache(home=self.home, scanner=scanner, clock=lambda: 10000.0)
        return cache, path, previous

    def test_5_fresh_cache_skips_scan(self):
        scanner = mock.Mock(side_effect=AssertionError("fresh cache must skip scan"))
        cache, _, _ = self.cache(9900.0, scanner)
        cache.refresh()
        scanner.assert_not_called()
        self.assertFalse(cache.snapshot()["measuring"])
        self.assertEqual(cache.snapshot()["measured_at"], 9900.0)

    def test_5_old_cache_scans_and_reload_reuses_it(self):
        storage = self.module()
        entries = [{"group": "main", "label": "new", "target": "/new", "bytes": 8192,
                    "symlink": False, "included_in": None}]
        scanner = mock.Mock(return_value=entries)
        cache, path, _ = self.cache(9099.0, scanner)
        cache.refresh()
        cache.thread.join(3)
        self.assertFalse(cache.thread.is_alive())
        scanner.assert_called_once_with(self.home)
        self.assertEqual(cache.snapshot()["entries"], entries)
        self.assertEqual(json.loads(path.read_text())["measured_at"], 10000.0)
        reloaded = storage.SizeCache(home=self.home, scanner=scanner, clock=lambda: 10001.0)
        reloaded.refresh()
        scanner.assert_called_once()
        self.assertEqual(reloaded.snapshot()["entries"], entries)

    def test_5_failed_scan_keeps_last_result_and_error(self):
        scanner = mock.Mock(side_effect=OSError("du permission denied"))
        cache, path, previous = self.cache(9000.0, scanner)
        cache.refresh()
        cache.thread.join(3)
        state = cache.snapshot()
        self.assertEqual(state["entries"], previous["entries"])
        self.assertEqual(state["measured_at"], 9000.0)
        self.assertIn("du permission denied", state["error"])
        self.assertIn("du permission denied", json.loads(path.read_text())["error"])
        text = "\n".join(self.module().render(80, 32, cache))
        self.assertIn("du permission denied", text)
        self.assertIn("1.0 GiB", text)

    def test_5_first_scan_is_nonblocking_and_says_measuring(self):
        storage = self.module()
        entered, release = threading.Event(), threading.Event()
        self.addCleanup(release.set)
        def slow_scan(home):
            entered.set()
            if not release.wait(3):
                raise TimeoutError("fixture was not released")
            raise OSError("fixture end")
        cache = storage.SizeCache(home=self.home, scanner=slow_scan)
        cache.refresh()
        self.assertTrue(entered.wait(1))
        text = "\n".join(storage.render(80, 32, cache))
        self.assertTrue(cache.thread.is_alive())
        self.assertIn("measuring…", text)
        self.assertNotIn("0 B", text)
        release.set()
        cache.thread.join(3)

    def test_5_attempts_are_at_least_fifteen_minutes_apart_even_on_failure(self):
        storage = self.module()
        now = [10000.0]
        scanner = mock.Mock(side_effect=OSError("fixture scan error"))
        cache = storage.SizeCache(home=self.home, scanner=scanner, clock=lambda: now[0])
        cache.refresh()
        cache.thread.join(3)
        now[0] = 10899.0
        cache.refresh()
        scanner.assert_called_once()
        now[0] = 10900.0
        cache.refresh()
        cache.thread.join(3)
        self.assertEqual(scanner.call_count, 2)

    def test_5_bad_cache_and_du_failure_are_explicit(self):
        storage = self.module()
        path = self.home / "Library/Caches/memit-dashboard/storage_sizes.json"
        path.parent.mkdir(parents=True)
        path.write_text("{corrupt cache}")
        cache = storage.SizeCache(home=self.home)
        self.assertIn("cache", cache.snapshot()["error"].lower())
        main, mirror, _ = self.scan_fixture()
        with mock.patch.object(storage.subprocess, "run", return_value=SimpleNamespace(
                returncode=1, stdout="", stderr="du fixture failed")):
            with self.assertRaisesRegex(OSError, "du fixture failed"):
                storage.scan_sizes(self.home, main_root=main, mirror_root=mirror)
        with mock.patch.object(storage.subprocess, "run", return_value=SimpleNamespace(
                returncode=0, stdout="", stderr="nice: setpriority: Operation not permitted")):
            with self.assertRaisesRegex(OSError, "setpriority"):
                storage.scan_sizes(self.home, main_root=main, mirror_root=mirror)
        seed_cache(path, 10001.0)
        scanner = mock.Mock(side_effect=OSError("future-cache recovery fixture"))
        future = storage.SizeCache(home=self.home, scanner=scanner, clock=lambda: 10000.0)
        self.assertIsNone(future.snapshot()["measured_at"])
        self.assertIn("future", future.snapshot()["error"])
        future.refresh()
        future.thread.join(3)
        scanner.assert_called_once()

    def test_6_snapshot_never_writes_backup_app_or_launchagents(self):
        storage = self.module()
        seed_backup(self.home, "finished")
        (self.home / "Applications/MemitGdriveBackup.app").mkdir(parents=True)
        (self.home / "Applications/MemitGdriveBackup.app/source").write_text("app fixture")
        (self.home / "Library/LaunchAgents").mkdir()
        (self.home / "Library/LaunchAgents/backup.plist").write_text("launch fixture")
        protected = [self.home / "Library/Logs", self.home / "Applications",
                     self.home / "Library/LaunchAgents"]
        before = [manifest(path) for path in protected]
        cache_path = self.home / "Library/Caches/memit-dashboard/storage_sizes.json"
        seed_cache(cache_path, time.time())
        cache = storage.SizeCache(home=self.home)
        with mock.patch.object(sys, "argv", ["dashboard_storage.py", "--once", "80", "32"]), \
             contextlib.redirect_stdout(io.StringIO()):
            storage.main(cache=cache)
        self.assertEqual(before, [manifest(path) for path in protected])


if __name__ == "__main__":
    unittest.main()
