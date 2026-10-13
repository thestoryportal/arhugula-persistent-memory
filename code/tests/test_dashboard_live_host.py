"""Opt-in host acceptance. All real tmux/ps calls are reads; writes are receipt-local."""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import unittest


# v2: staged sources keep their code/ homes, so the dashboards' package imports (apps.mathlab, state, ops) resolve.
DASHBOARD = "code/apps/dashboard"
SHARED = ("code/apps/dashboard/team_dashboard.sh", "code/apps/mathlab/mathlab_events.py",
          "code/ops/backup/backup_gdrive_status.py", "code/state/llmdb_records.py")


def stage_sources(root, before, out, phase):
    inputs = sorted(set((root / DASHBOARD).glob("dashboard_*.py")) |
                    set((root / DASHBOARD).glob("dashboard_*.sh")))
    inputs += [root / rel for rel in SHARED if (root / rel).is_file()]
    hashes = {}
    for current in inputs:
        if phase == "red" and current.name == "dashboard_team.py":
            continue  # New in this repair; there is no original Team renderer.
        rel = current.relative_to(root)
        original = before / rel
        source = original if phase == "red" and original.is_file() else current
        target = out / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        hashes[current.name] = {"input": str(source), "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    return hashes


def observe(args, receipt, name, allow_empty=False):
    if Path(args[0]).name == "tmux" and (len(args) < 2 or args[1] not in
            {"list-sessions", "list-panes", "list-windows", "capture-pane", "display", "show-options"}):
        raise ValueError("Host tests may only read tmux")
    (receipt / (name + ".command.json")).write_text(json.dumps(args) + "\n")
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as error:
        result = subprocess.CompletedProcess(args, 126, "", str(error))
    for suffix, value in (("stdout", result.stdout), ("stderr", result.stderr), ("exit", str(result.returncode) + "\n")):
        (receipt / (name + "." + suffix)).write_text(value)
    if result.returncode:
        raise RuntimeError(f"{name} unavailable: exit {result.returncode}: {result.stderr}")
    if not allow_empty and not result.stdout.strip():
        raise RuntimeError(f"{name} unavailable: empty observation")
    return result.stdout


def dependency_reload(tools, receipt):
    # The fixture mirrors v2: dashboard_live in code/apps/dashboard/ imports the layout library from code/state/.
    code = receipt / "reload_fixture" / "code"
    fixture = code / "apps" / "dashboard"
    fixture.mkdir(parents=True)
    (code / "state").mkdir()
    layout = code / "state" / "llmdb_records.py"
    shutil.copy2(Path(__file__).resolve().parents[1] / "state" / "llmdb_records.py", layout)
    shutil.copy2(tools / "dashboard_live.py", fixture / "dashboard_live.py")
    helper = fixture / "fixture_dep.py"
    helper.write_text("VALUE = 'BEFORE'\n")
    probe = fixture / "dashboard_probe.py"
    probe.write_text('import os, sys\nfrom pathlib import Path\nimport dashboard_live as live\nimport fixture_dep\n'
                     'base = Path(__file__).parent\nmarker = base / "first_frame"\n'
                     'if not marker.exists():\n'
                     '    stamp = live.source_stamp(str(base))\n    marker.write_text("recorded\\n")\n'
                     '    dep = base / "fixture_dep.py"\n    dep.write_text("VALUE = \'HELPER_RELOADED\'\\n")\n'
                     '    os.utime(dep, (200, 200))\n    live.maybe_reload(stamp)\n'
                     '    print("RELOAD_MISSED")\n    sys.exit(1)\n'
                     'print(fixture_dep.VALUE)\nsys.exit(0 if fixture_dep.VALUE == "HELPER_RELOADED" else 1)\n')
    for path in (probe, fixture / "dashboard_live.py", layout):
        os.utime(path, (100, 100))
    os.utime(helper, (90, 90))
    result = subprocess.run(["/usr/bin/python3", "-B", str(probe)], capture_output=True, text=True,
                            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=15)
    (receipt / "reload.stdout").write_text(result.stdout)
    (receipt / "reload.stderr").write_text(result.stderr)
    (receipt / "reload.exit").write_text(str(result.returncode) + "\n")
    return result


ANSI = re.compile(r"\033\[[0-9;]*[A-Za-z]")
COUNTS = re.compile(r"working (\d+) · asking (\d+) · active (\d+) · idle (\d+)")
CONTEXT = None


def updated_header_matches(lines, updated, live):
    expected = live.clip(" ■ SCIENCE REPORT · updated " + str(updated), 109)
    return bool(lines) and ANSI.sub("", lines[0]) == expected


@unittest.skipUnless(os.environ.get("MB38_HOST_RUN") == "1", "Run through receipt-local run_host.sh on the host")
class HostChecks(unittest.TestCase):
    def test_real_inventory_is_available(self):
        self.assertTrue(CONTEXT["ps"].strip())
        self.assertTrue(CONTEXT["sessions"].strip())

    def test_team_has_one_live_pane_and_published_roster_counts(self):
        ctx = CONTEXT
        for sample in ctx["samples"]:
            panes = [p for p in sample["panes"] if p[1] == "team"]
            self.assertEqual(len(panes), 1, "MAESTRO must restart the Team tab before GREEN host acceptance")
            self.assertIn("dashboard_team.py", panes[0][3])
            capture = sample["captures"][panes[0][2]]
            rendered = COUNTS.search(capture)
            self.assertIsNotNone(rendered, "No roster counts in the live Team capture")
            published = COUNTS.fullmatch(sample["counts"].strip())
            self.assertIsNotNone(published, "No @team_counts metadata from the live Team pane")
            self.assertEqual(rendered.groups(), published.groups(), "Counts changed during capture; rerun with a stable frame")
            team = ctx["modules"].get("dashboard_team")
            self.assertIsNotNone(team, "Original fixed-pane source has no self-composing Team view")
            names, lead, _, _ = team.snapshot()
            expected = {n for n in sample["sessions"].split() if n.startswith("codex") or n == lead}
            self.assertEqual(set(names), expected, "Membership changed during capture; rerun")
            header = re.search(r"(\d+) live sessions", capture)
            self.assertIsNotNone(header)
            self.assertEqual(int(header.group(1)), len(expected))
            self.assertEqual(sum(map(int, published.groups())), len(expected))
            lines, _ = team.frame(110, 40, {})
            (ctx["receipt"] / (sample["label"] + "_team_render.txt")).write_text("\n".join(lines) + "\n")

    def test_real_science_mathlab_experiment_frames_and_live_panes(self):
        ctx = CONTEXT
        modules, root = ctx["modules"], ctx["root"]
        for sample in ctx["samples"]:
            windows = {p[1] for p in sample["panes"]}
            for name in ("science", "mathlab", "experiment"):
                self.assertIn(name, windows)
                for pane in (p for p in sample["panes"] if p[1] == name):
                    self.assertTrue(sample["captures"][pane[2]].strip(), f"Empty live {name} pane")
            program = json.loads((root / "program/program_state.json").read_text())
            board = json.loads((root / "program/registers/c10_scoreboard.json").read_text())
            science = modules["dashboard_report"].screen(110, 40)
            frames = {"science": science, "mathlab": modules["dashboard_mathlab"].render(109, 40),
                      "experiment": modules["dashboard_experiment"].render(109, 40)}
            for name, lines in frames.items():
                (ctx["receipt"] / (sample["label"] + "_" + name + "_render.txt")).write_text("\n".join(lines) + "\n")
                self.assertTrue(lines)
                self.assertLessEqual(len(lines), 40)
                self.assertTrue(all(modules["dashboard_live"].cells(line) <= 109 for line in lines))
            plain = ANSI.sub("", "\n".join(science))
            self.assertTrue(updated_header_matches(science, program["updated"], modules["dashboard_live"]),
                            "Science header does not match the current program update")
            self.assertIn("NEXT ACTIONS · program/program_state.json", plain)
            self.assertIn("Scoreboard narrative only · as of " + str(board["updated"]), plain)

    def test_last_run_uses_experiment_source(self):
        live = CONTEXT["modules"]["dashboard_live"]
        logs = live.experiment_logs(str(CONTEXT["root"]))
        state = live.gpu_state()
        self.assertNotIn("unavailable", state, "Process observation unavailable; no idle claim is permitted")
        self.assertEqual(state.get("last_log"), logs[-1] if logs else None)
        (CONTEXT["receipt"] / "last_run.json").write_text(json.dumps({
            "experiment_latest": logs[-1] if logs else None, "gpu_last_log": state.get("last_log"),
            "gpu_last_at": state.get("last_at"), "gpu_last_exit": state.get("last_exit")}, indent=2) + "\n")

    def test_dependency_edit_reexecs_fixture_process(self):
        result = dependency_reload(CONTEXT["source"] / DASHBOARD, CONTEXT["receipt"])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), "HELPER_RELOADED")


def main():
    global CONTEXT
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "before", "receipt"):
        parser.add_argument("--" + name, required=True, type=Path)
    parser.add_argument("--phase", required=True, choices=("red", "green"))
    args = parser.parse_args()
    if os.environ.get("MB38_HOST_RUN") != "1":
        parser.error("Use the receipt-local run_host.sh")
    root, receipt, source = args.root.resolve(), args.receipt.resolve(), args.receipt.resolve() / "source"
    provenance = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "phase": args.phase,
                  "interpreter": sys.executable, "python": sys.version, "root": str(root),
                  "sources": stage_sources(root, args.before, source, args.phase)}
    provenance["host_test_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    provenance["host_runner_sha256"] = hashlib.sha256((args.before.parent / "run_host.sh").read_bytes()).hexdigest()
    (source / "code/tests").mkdir(parents=True)
    shutil.copy2(root / "code/tests/test_dashboard_live_refresh.py", source / "code/tests")
    provenance["regression_test_sha256"] = hashlib.sha256((source / "code/tests/test_dashboard_live_refresh.py").read_bytes()).hexdigest()
    provenance["state_inputs_at_start"] = {Path(rel).name: hashlib.sha256((root / rel).read_bytes()).hexdigest()
                                            for rel in ("program/program_state.json", "program/registers/c10_scoreboard.json")}
    (receipt / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    for name, flags in (("git_root", ["--show-toplevel"]), ("git_branch", ["--abbrev-ref", "HEAD"]), ("git_head", ["HEAD"])):
        observe(["git", "-C", str(root), "rev-parse"] + flags, receipt, name)
    regression = subprocess.run(["/usr/bin/python3", "-B", "-m", "unittest", "discover", "-s", str(source / "code/tests"),
                                 "-p", "test_dashboard_live_refresh.py", "-v"], capture_output=True, text=True,
                                cwd=str(source), env=dict(os.environ, PYTHONPATH=str(source / "code")), timeout=30)
    (receipt / "regressions.log").write_text(regression.stdout + regression.stderr)
    (receipt / "regressions.exit").write_text(str(regression.returncode) + "\n")
    print(regression.stdout + regression.stderr, flush=True)
    ps = observe(["/bin/ps", "-axo", "pid=,ppid=,etime=,command="], receipt, "ps")
    sessions = observe(["tmux", "list-sessions", "-F", "#{session_name}"], receipt, "sessions")
    samples = []
    for index in range(2):
        label = "sample" + str(index + 1)
        if index:
            time.sleep(4)  # Observe two live refresh cycles without controlling a pane.
        roster = observe(["tmux", "list-sessions", "-F", "#{session_name}"], receipt, label + "_sessions")
        raw = observe(["tmux", "list-panes", "-s", "-t", "=dashboard", "-F",
                       "#{window_index}\t#{window_name}\t#{pane_id}\t#{pane_start_command}"], receipt, label + "_panes")
        panes = [line.split("\t", 3) for line in raw.splitlines()]
        if any(len(pane) != 4 for pane in panes):
            raise RuntimeError("Malformed tmux pane observation")
        captures = {p[2]: observe(["tmux", "capture-pane", "-p", "-t", p[2]], receipt,
                                  label + "_pane_" + p[2].lstrip("%")) for p in panes}
        counts = observe(["tmux", "show-options", "-w", "-qv", "-t", "dashboard:1", "@team_counts"],
                         receipt, label + "_counts", allow_empty=True)
        samples.append(dict(label=label, panes=panes, captures=captures, counts=counts, sessions=roster))
    sys.path.insert(0, str(source / DASHBOARD))
    modules = {name: importlib.import_module(name) for name in
               ("dashboard_live", "dashboard_report", "dashboard_mathlab", "dashboard_experiment")}
    if args.phase == "green":
        modules["dashboard_team"] = importlib.import_module("dashboard_team")
    for module in modules.values():
        module.ROOT = str(root)
    modules["dashboard_report"].BOARD = str(root / "program/registers/c10_scoreboard.json")
    modules["dashboard_report"].PROGRAM = str(root / "program/program_state.json")
    CONTEXT = dict(root=root, receipt=receipt, source=source, modules=modules, ps=ps, sessions=sessions, samples=samples)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(HostChecks)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print("Live panes are current host observations; RED selects original code only for copied-source checks.", flush=True)
    return 0 if result.wasSuccessful() and regression.returncode == 0 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"Host acceptance UNAVAILABLE: {error}", file=sys.stderr)
        raise SystemExit(1)
