#!/usr/bin/env python3
"""Offline v3.1 regression checks. All fixtures are synthetic and confined to /tmp.

Never dispatches the runner, editor, scorer, precheck main, or fence scripts.
Synthetic process tests do not replace the separately required real ps probe.
"""
import ast
from contextlib import redirect_stdout
import copy
import importlib.abc
import io
import json
import os
from pathlib import Path
import py_compile
import re
import subprocess
import sys
import time
from unittest.mock import patch


class NoModelImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in ("torch", "transformers"):
            raise ImportError(f"offline test forbids {fullname}")


sys.meta_path.insert(0, NoModelImports())
import read_replay as R
import tokenizer_precheck as T

HERE = Path(__file__).resolve().parent
LABELS = ("NO-GAIN-WITHOUT-VALUE-POSITIONS", "PARTIAL-GAIN", "FULL-GAIN-WITHOUT-VALUE-POSITIONS",
          "NO-COLLISION-RECOVERY", "PARTIAL-COLLISION-RECOVERY", "FULL-COLLISION-RECOVERY")


def rejects(operation):
    try:
        operation()
    except (OSError, ValueError, KeyError, TypeError):
        return
    raise AssertionError("malformed input was accepted")


def write_json(path, value):
    path.write_text(json.dumps(value, allow_nan=False) + "\n")


class CachedHF:
    is_fast = True

    def __init__(self, rust):
        self.rust = rust

    def __call__(self, text, add_special_tokens=True, return_offsets_mapping=False):
        encoded = self.rust.encode(text, add_special_tokens=add_special_tokens)
        result = {"input_ids": encoded.ids}
        if return_offsets_mapping:
            result["offset_mapping"] = encoded.offsets
        return result


def row(pid, ppid, command, pgid=None):
    return {"pid": pid, "ppid": ppid, "pgid": pid if pgid is None else pgid,
            "start": "Tue Oct 6 12:00:00 2026", "command": command}


def process_event(phase, foreign=False):
    rows = {100: row(100, 1, "runner")}
    if phase in ("during_run", "after_exit"):
        rows[101] = row(101, 100, "python edit.py")
    if foreign:
        rows[200] = row(200, 1, "python edit.py")
    return R.classify_processes(rows, phase, 100, 100, None if phase in ("before_dispatch", "after_preflight") else 101)


def annotate(events):
    monitor = R.ProcessMonitor()
    for event in events:
        event.update(monitor.observe(event))
    return events


def probe_error(phase="during_run"):
    return {"phase": phase, "probe_exit": -1, "probe_error": "synthetic transient ps error",
            "runner_pid": 100, "child_pid": 101, "foreign": [], "ok": False}


def shared_tmux_regression():
    # Commands/PIDs from the operator's v3 probe; ancestry/groups are synthetic.
    rows = {100: row(100, 1, "runner")}
    commands = [
        (1886, 40771, "sleep 120"),
        (1987, 40771, "caffeinate -i -t 300"),
        (5634, 78173, "sleep 15"),
        (40769, 1, "/bin/zsh -c source /shell-snapshots/snapshot-zsh.sh; bash experiments/track_c/autoresearch_c10/watch_audit.sh"),
        (40771, 40769, "bash experiments/track_c/autoresearch_c10/watch_audit.sh"),
        (51198, 1, "tmux new-session -d -s autoresearch -x 200 -y 50 bash /workspace/experiments/track_c/autoresearch_c10/loop.sh"),
        (51282, 51198, "zsh -c bash /workspace/experiments/track_c/autoresearch_c10/loop.sh"),
        (78172, 1, "/bin/zsh -c source /shell-snapshots/snapshot-zsh.sh; bash experiments/track_c/autoresearch_c10/watch_pane.sh"),
        (78173, 78172, "bash experiments/track_c/autoresearch_c10/watch_pane.sh"),
        (89284, 51198, "/bin/bash /workspace/run_codex_tui3.sh"),
        (89374, 89284, "codex -m gpt-6.1-sol experiments/track_c/c10e_bandknob.py --safe-mode"),
        (90428, 89374, "/Applications/Pencil.app/mcp-server-darwin-arm64 --app desktop --agent codexCLI"),
        (90438, 89374, "node /opt/homebrew/bin/graft mcp"),
        (91419, 89374, "/opt/homebrew/bin/codex-code-mode-host"),
        (98000, 1, "python /foreign replay/edit.py"),
        (98001, 98000, "python -c from multiprocessing.resource_tracker import main;main(4)"),
    ]
    rows.update({pid: row(pid, ppid, command) for pid, ppid, command in commands})
    with patch.object(R.subprocess, "run", side_effect=AssertionError("process regression must not execute commands")), \
            patch.object(R.os, "getpgid", side_effect=AssertionError("process regression must not inspect live PIDs")):
        for loop_present in (False, True):
            if loop_present:
                rows[51284] = row(51284, 51282, "claude --safe-mode --model claude-fable-5-1 experiments/track_c/autoresearch_c10/")
            expected = {98000, 98001} | ({51284} if loop_present else set())
            event = R.classify_processes(rows, "probe", 100, 100)
            foreign = {r["pid"] for r in event["foreign"]}
            assert foreign == expected, f"loop_present={loop_present}: foreign={sorted(foreign)} expected={sorted(expected)}"
            assert {r["pid"] for r in event["matches"]} == expected
            print(f"SYNTHETIC v3.1 supplied process table: loop_present={loop_present} foreign={sorted(foreign)} PASS")
        studio = {100: row(100, 1, "runner"),
                  200: row(200, 1, "/Volumes/Model Apps/LM Studio.app/Contents/MacOS/LM Studio --server"),
                  201: row(201, 200, "node /helper.js")}
        event = R.classify_processes(studio, "probe", 100, 100)
        assert {r["pid"] for r in event["foreign"]} == {200, 201}
        print("SYNTHETIC v3.1 unquoted spaced-parent LM Studio: foreign root/helper=[200, 201] PASS")


def process_tests(dest):
    shared_tmux_regression()
    rows = {100: row(100, 1, "runner"), 101: row(101, 100, "python edit.py"),
            102: row(102, 101, "python -c from multiprocessing.resource_tracker import main;main(4)", 102),
            103: row(103, 101, "python prepare.py --score /tmp/replay/runs/run"),
            104: row(104, 103, "python -c from multiprocessing.resource_tracker import main;main(4)"),
            105: row(105, 1, "python experiments/track_c/owned_helper.py", 100),
            200: row(200, 1, "python /sandbox/edit.py"),
            201: row(201, 200, "python -c from multiprocessing.resource_tracker import main;main(4)")}
    benign = ["python /powerline/server.py", "python /harness-dashboard/serve.py",
              "/python3.11/bin/postgres", "node /browser-harness/daemon.js",
              "python -m pixeltable_developer", "python -m blender_mcp", "python -m arxiv_mcp_server",
              "claude --model claude-fable-5-1 experiments/track_c/", "codex -C /worktrees/c10k-route-a --safe-mode"]
    rows.update({pid: row(pid, 1, command) for pid, command in enumerate(benign, 300)})
    event = R.classify_processes(rows, "during_run", 100, 100, 101)
    assert {r["pid"] for r in event["owned_children"]} == {101, 102, 103, 104}
    assert {r["pid"] for r in event["foreign"]} == {200, 201}
    positive = ("python edit.py", "python3 prepare.py", "/usr/bin/python3.12 check_equivalence.py",
                "Python /foreign replay/edit.py", '"/venv space/bin/python3.11" "/foreign replay/prepare.py"',
                "python c10e_bandknob.py", "python experiments/track_c/c10g_driver.py",
                "python /workspace/experiments/track_c/c10/driver.py", "python -m ipykernel_launcher",
                "python -m jupyter", "ollama serve", "/usr/bin/llama-server --model x", "llama-cli --model x",
                "lm-studio", "lmstudio", "LM Studio", "/Applications/LM Studio.app/Contents/MacOS/LM Studio",
                '"/Applications/LM Studio.app/Contents/MacOS/LM Studio" --server',
                "/Volumes/Model Apps/LM Studio.app/Contents/MacOS/LM Studio --server", "lms server start",
                "claude --safe-mode", "/opt/bin/claude --safe-mode --model claude-fable-5-1")
    negative = ("python --safe-mode", "python2 edit.py", "pypy3 edit.py", "python experiments/track_c/x.py",
                "python experiments/track_c/autoresearch_c10/watch_audit.sh", "jupyter lab", "llama --model x",
                "claude --safe-mode-extra", 'claude --message "mention --safe-mode here"', "claude edit.py",
                "sleep 120", "caffeinate -i -t 300", "", "python helper_prepare.py",
                "/bin/other /Applications/LM Studio.app/Contents/MacOS/LM Studio",
                '"/bin/other" relative/LM Studio.app/Contents/MacOS/LM Studio')
    negative += tuple(f"{exe} python edit.py experiments/track_c/c10g_driver.py --safe-mode ollama"
                      for exe in ("/bin/bash", "/bin/zsh", "/bin/sh", "tmux", "node", "codex", "other"))
    negative += tuple(f"{exe} -cfoo/LM Studio.app/Contents/MacOS/LM Studio"
                      for exe in ("/bin/bash", "/bin/zsh", "/bin/sh", "tmux", "node", "codex", "/opt/bin/codex-code-mode-host"))
    for command in positive:
        assert R.is_model_root(command), command
    for command in negative:
        assert not R.is_model_root(command), command
    print(f"SYNTHETIC v3.1 executable policy: {len(positive)} model roots + {len(negative)} non-roots PASS")
    old = [rows[101]]
    reused = copy.deepcopy(rows)
    reused[101]["start"] = "Tue Oct 6 12:00:01 2026"
    rejects(lambda: R.classify_processes(reused, "during_run", 100, 100, 101, old))
    orphan = copy.deepcopy(rows)
    orphan[104]["ppid"] = 1
    assert 104 in {r["pid"] for r in R.classify_processes(orphan, "after_exit", 100, 100, 101, [rows[104]])["owned_children"]}
    raw = "100 1 Tue Oct 6 12:00:00 2026 runner\n102 101 Tue Oct 6 12:00:00 2026\n"
    assert set(R.parse_processes(raw)) == {100}
    rejects(lambda: R.parse_processes("broken row"))
    print("SYNTHETIC process ownership: transitive editor/scorer trackers + runner group owned; foreign editor/tree={200,201}; operator tools excluded; editor identity pin PASS")
    print("SYNTHETIC ps parser: empty-command row skipped; malformed row rejected PASS")

    for count in (1, 2, 3):
        monitor = R.ProcessMonitor()
        statuses = [monitor.observe(process_event("during_run", True)) for _ in range(count)]
        assert statuses[-1]["invalid"] is (count == 3)
        assert monitor.observe(process_event("during_run"))["invalid"] is (count == 3)
        errors = R.ProcessMonitor()
        for _ in range(count):
            status = errors.observe(probe_error())
        assert status["invalid"] is (count == 3)
        assert errors.observe(process_event("during_run"))["invalid"] is (count == 3)
    monitor = R.ProcessMonitor()
    for event in (process_event("during_run", True), process_event("during_run"), process_event("during_run", True), probe_error(), process_event("during_run", True)):
        assert not monitor.observe(event)["invalid"]
    for field, value in (("pid", 202), ("start", "Tue Oct 6 12:00:01 2026")):
        monitor = R.ProcessMonitor()
        for _ in range(2):
            assert not monitor.observe(process_event("during_run", True))["invalid"]
        changed = process_event("during_run", True)
        changed["foreign"][0][field] = value
        assert not monitor.observe(changed)["invalid"]
    print("SYNTHETIC process monitor: contender/error polls 1,2 accepted; 3 INVALID; gaps/PID identities reset streaks; INVALID stays latched PASS")

    payload = (HERE / "run_replay.sh").read_text().split("<<'PY'\n", 1)[1].rsplit("\nPY", 1)[0]
    tree = ast.parse(payload)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "exclude")
    namespace = {"child": None, "receipt": {"owned_children": []}, "monitor": R.ProcessMonitor(),
                 "predispatch_events": [], "process_log": dest / "process_exclusion.jsonl",
                 "process_check": lambda *args: process_event("before_dispatch", True),
                 "require": R.require, "json": json, "os": os, "subprocess": subprocess, "sys": sys}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(HERE / "run_replay.sh"), "exec"), namespace)
    before = {p.name for p in dest.iterdir()}
    for _ in range(2):
        rejects(lambda: namespace["exclude"]("before_dispatch"))
        assert {p.name for p in dest.iterdir()} == before
    namespace["process_check"] = lambda *args: (_ for _ in ()).throw(OSError("synthetic ps failure"))
    rejects(lambda: namespace["exclude"]("before_dispatch"))
    assert {p.name for p in dest.iterdir()} == before
    final = next(n for n in tree.body if isinstance(n, ast.Try) and n.finalbody)
    refusal = final.finalbody[0]
    assert isinstance(refusal, ast.If) and ast.unparse(refusal.test) == "child is None"
    namespace.update(reserved_paths=[], dest=dest)
    try:
        exec(compile(ast.Module(body=[refusal], type_ignores=[]), "runner predispatch closeout", "exec"), namespace)
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("pre-dispatch closeout did not refuse")
    assert {p.name for p in dest.iterdir()} == before
    # The same cleanup handles a Popen failure after exclusive reservation.
    reserved = [dest / "replay_launch.json", dest / "run.log"]
    for path in reserved:
        path.write_text("synthetic reservation\n")
    namespace["reserved_paths"] = reserved
    try:
        exec(compile(ast.Module(body=[refusal], type_ignores=[]), "runner failed-dispatch closeout", "exec"), namespace)
    except SystemExit as exc:
        assert exc.code == 2
    assert {p.name for p in dest.iterdir()} == before
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "stop_owned" for n in ast.walk(fn))
    print("SYNTHETIC runner helper/closeout: repeated predispatch contention, ps failure, failed-Popen reservations => exit 2; no destination artifacts consumed; monitoring never calls stop_owned PASS")
    return payload


def selector_records(dest):
    rust = R.cached_tokenizer()
    hf = CachedHF(rust)
    source = ast.parse((dest / "edit.py").read_text())
    node = next(n for n in source.body if isinstance(n, ast.FunctionDef) and n.name == "select_common_positions")
    namespace = {"re": re}
    exec(compile(ast.Module(body=[node], type_ignores=[]), "frozen edit.py selector only", "exec"), namespace)
    select = namespace["select_common_positions"]
    records = []
    for arm, facts in R.FROZEN_ROWS.items():
        positions = []
        for f, (subject, value, m) in enumerate(facts):
            rq = {"subject": subject, "prompt": R.CANON, "target_new": {"str": " " + value}}
            tgt = hf(" " + value, add_special_tokens=False)["input_ids"]
            assert len(tgt) == m
            for q, template in enumerate(t for group in R.CONTEXTS for t in group):
                ids = hf(template.format(R.CANON.format(subject)))["input_ids"]
                positions.append(select(hf, rq, template, f, q, ids, tgt))
        record = {"arm": arm, "positions": positions, "edit_context_templates": R.CONTEXTS,
                  "Kp_source": "common_canonical_prefix", "preserve_weight": 1.0,
                  "layers": [{"layer": layer, "control_columns": R.COLUMNS[arm], "value_columns": R.COLUMNS[arm],
                              "key_dim": 11008, "update_shape": [2048, 11008], "finite": True, "identity_equal": True,
                              "position_sha256": R.sha_json(positions), "control_sumsq": 2.0, "value_sumsq": 2.0,
                              "control_PKp_fro": 1.0, "value_PKp_fro": 1.0, "update_fro_precast": 1.0}
                             for layer in R.LAYERS]}
        R.validate_positions(record, rust)
        assert all(0 not in p["indices"] and 0 not in p["candidates"] and len(p["candidates"]) == (6 if p["template_i"] == 0 else 7) for p in positions)
        bad = copy.deepcopy(record)
        bad["positions"][0]["indices"][0] = 0
        rejects(lambda: R.validate_positions(bad, rust))
        records.append(record)
        print(f"RUST SELECTOR {arm}: pairs={len(positions)} columns_per_layer={sum(len(p['indices']) for p in positions)} layers={list(R.LAYERS)} selected_zero=0; independent reader re-derivation PASS")
    rq = {"subject": "Zorbland", "prompt": R.CANON, "target_new": {"str": " x"}}
    ids = hf(R.CANON.format(rq["subject"]))["input_ids"]
    rejects(lambda: select(hf, rq, "{}", 0, 0, ids, [1] * 7))
    print("RUST SELECTOR total_pairs=432; K=6/7; m>K HALT; no attention-sink selection PASS")
    with patch.object(T.sys, "prefix", "/tmp/unpinned-venv"):
        rejects(T.precheck_runtime)
    for key in ("PYTHONPATH", "PYTHONHOME"):
        with patch.dict(T.os.environ, {key: "/tmp/unpinned-python"}):
            rejects(T.precheck_runtime)
    assert T.precheck_runtime()["venv"] == str((R.PROGRAM_ROOT / ".venv").resolve())
    print("SYNTHETIC precheck runtime: wrong virtual environment/PYTHONPATH/PYTHONHOME refused; actual pinned venv bound PASS")
    assert T.compare_tokenizers(hf, rust) == 432
    class BadHF(CachedHF):
        def __call__(self, *args, **kwargs):
            result = super().__call__(*args, **kwargs)
            if "offset_mapping" in result:
                result["offset_mapping"] = [(0, 0)] * len(result["offset_mapping"])
            return result
    rejects(lambda: T.compare_tokenizers(BadHF(rust), rust))
    class BadIdsHF(CachedHF):
        def __call__(self, *args, **kwargs):
            result = super().__call__(*args, **kwargs)
            result["input_ids"][0] += 1
            return result
    rejects(lambda: T.compare_tokenizers(BadIdsHF(rust), rust))
    slow = CachedHF(rust)
    slow.is_fast = False
    rejects(lambda: T.compare_tokenizers(slow, rust))
    print("SYNTHETIC tokenizer comparison: matching Rust proxy 432 pairs PASS; mismatched IDs/offsets and slow tokenizer rejected; actual HF precheck NOT RUN")
    return records


def fixture(dest, records):
    score = R.load_json(R.SOURCE / "runs/20261006-142644_nocommit/score.json")
    score["edits"]["commit"] = R.BASE_COMMIT[:7]
    run_dir = dest / "runs/20261006-000000_92acd03"
    run_dir.mkdir(parents=True)
    score_path, receipt_path = run_dir / "score.json", dest / "runner_receipt.json"
    write_json(score_path, score)
    now = time.time()
    precheck = {"schema": 1, "passed": True, "pairs": 432, "checked_at": now, "inputs": T.precheck_inputs(dest)}
    precheck_path = dest / "tokenizer_precheck.json"
    rejects(lambda: T.validate_precheck(dest, at_time=now))
    write_json(precheck_path, precheck)
    assert T.validate_precheck(dest, at_time=now) == precheck
    rejects(lambda: T.validate_precheck(dest, at_time=now + R.PRECHECK_MAX_AGE_S + 1))
    rejects(lambda: T.validate_precheck(dest, at_time=now - 1))
    precheck["passed"] = False
    write_json(precheck_path, precheck)
    rejects(lambda: T.validate_precheck(dest, at_time=now))
    precheck["passed"] = True
    precheck["inputs"]["edit_py_sha256"] = "0" * 64
    write_json(precheck_path, precheck)
    rejects(lambda: T.validate_precheck(dest, at_time=now))
    precheck["inputs"] = T.precheck_inputs(dest)
    write_json(precheck_path, precheck)
    print("SYNTHETIC precheck pass-record gate: fresh exact inputs accepted; missing/stale/future/failed/changed-source records refused PASS")

    fidelity = {"interpreter": str((R.PROGRAM_ROOT / ".venv/bin/python").resolve()), "python_version": sys.version,
                "venv": str((R.PROGRAM_ROOT / ".venv").resolve()), "packages": {name: T.importlib.metadata.version(name) for name in ("torch", "transformers", "tokenizers", "numpy", "safetensors", "accelerate")},
                "os": "synthetic macOS receipt", "model_id": "Qwen/Qwen2.5-3B", "model_revision": R.MODEL_REV,
                "tokenizer_revision": R.MODEL_REV, "numeric_env": {key: None for key in ("LLMDB_DEVICE", "PYTORCH_MPS_FAST_MATH", "PYTORCH_ENABLE_MPS_FALLBACK", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")},
                "files": {str(p): {"resolved_path": str(p.resolve(strict=True)), "sha256": "f" * 64} for p in R.fidelity_inputs(dest)}}
    audit = R.inspect_replay(dest)
    launch = {key: audit[key] for key in ("base_commit", "dest", "edit_py_sha256", "diff_sha256")}
    launch.update(invocation_id="c" * 32, program_root=str(R.PROGRAM_ROOT), context_sha256=R.CONTEXT_SHA,
                  initial_runs=[], runner_pid=100, child_pid=101, fidelity_before=fidelity,
                  dispatched_at=now, tokenizer_precheck_sha256=R.sha_file(precheck_path))
    write_json(dest / "replay_launch.json", launch)
    for record in records:
        record.update(invocation_id=launch["invocation_id"], run_dir=str(run_dir), executed_edit_py_sha256=R.EXPECTED_EDIT_SHA256,
                      launch_sha256=R.sha_file(dest / "replay_launch.json"), edit_context_templates_sha256=R.CONTEXT_SHA)
    provenance = run_dir / "replay_provenance.jsonl"
    provenance.write_text("".join(json.dumps(record) + "\n" for record in records))
    tree = ast.parse((R.PROGRAM_ROOT / "tools/engine_fingerprint.py").read_text())
    constants = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("EXPECTED_SHA256", "EXPECTED_COV_CPU_SITES")}
    fp = {"exit": 0, "stdout": score["gates"]["fingerprint"] + f"\nsha256   {constants['EXPECTED_SHA256']}\n_cov_cpu {constants['EXPECTED_COV_CPU_SITES']} sites\n",
          "stderr": "", "LLMDB_ROOT": str(R.PROGRAM_ROOT), "interpreter": str(R.PROGRAM_ROOT / ".venv/bin/python")}
    events = annotate([process_event(phase) for phase in ("before_dispatch", "after_preflight", "during_run", "after_exit")])
    process_path = dest / "process_exclusion.jsonl"
    process_path.write_text("".join(json.dumps(e) + "\n" for e in events))
    receipt = {"dest": str(dest), "run_dir": str(run_dir), "score_path": str(score_path), "child_exit": 0, "failures": [],
               "score_sha256": R.sha_file(score_path), "saved_sha256": score["saved_sha256"], "launch": launch,
               "invocation_id": launch["invocation_id"], "runner_pid": 100, "child_pid": 101,
               "base_commit": R.BASE_COMMIT, "edit_py_sha256": R.EXPECTED_EDIT_SHA256, "diff_sha256": R.EXPECTED_DIFF_SHA256,
               "tokenizer_precheck": precheck, "engine_fingerprint": fp, "fidelity_before": fidelity, "fidelity_after": fidelity,
               "exclusive_window": "paused-no-relaunch", "mps_preflight": {"exit": 0, "stdout": "MPS_AVAILABLE=true", "stderr": ""},
               "process_log_sha256": R.sha_file(process_path), "owned_children": events[-1]["owned_children"]}
    write_json(receipt_path, receipt)
    return score_path, receipt_path, score, receipt, events


def run_reader(score_path, receipt_path, title, expected_rc):
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    result = subprocess.run([sys.executable, "-B", str(HERE / "read_replay.py"), str(score_path), str(receipt_path)], capture_output=True, text=True, env=env)
    (receipt_path.parent.parent / (re.sub(r"[^a-zA-Z0-9]+", "_", title) + ".log")).write_text(result.stdout + result.stderr)
    assert result.returncode == expected_rc, f"{title}: {result.returncode}\n{result.stdout}\n{result.stderr}"
    assert result.stdout.strip(), title
    if expected_rc == 2:
        assert "INVALID\n" in result.stdout and not any(label in result.stdout for label in LABELS), result.stdout
    else:
        assert "LABEL primary=" in result.stdout and "INVALID\n" not in result.stdout, result.stdout
    selected = [line for line in result.stdout.splitlines() if line.startswith(("LABEL ", "NON-BINDING counts:", "INVALID", "HALT:"))]
    print(f"{title}: exit={result.returncode}")
    for line in selected:
        print(line)
    return result.stdout


def reader_tests(dest, records):
    absent = dest / "absent_receipt.json"
    for path in sorted(R.SOURCE.glob("runs/*/score.json")):
        run_reader(path, absent, "RECORDED " + path.parent.name, 2)
    score_path, receipt_path, score, receipt, events = fixture(dest, records)
    stdout = run_reader(score_path, receipt_path, "SYNTHETIC full-provenance fixture", 0)
    ratios = [line for line in stdout.splitlines() if line.startswith("COMPARABILITY ")]
    assert len(ratios) == 15
    print("\n".join(ratios))
    provenance = score_path.parent / "replay_provenance.jsonl"
    original_provenance = provenance.read_text()
    for field, value in (("control_sumsq", 0.05), ("control_sumsq", 11.0), ("control_sumsq", 0.1), ("control_sumsq", 10.0),
                         ("control_PKp_fro", 0.05), ("control_PKp_fro", 11.0), ("control_PKp_fro", 0.1), ("control_PKp_fro", 10.0)):
        changed = copy.deepcopy(records)
        changed[2]["layers"][0][field] = value * changed[2]["layers"][0][field.replace("control_", "value_")]
        provenance.write_text("".join(json.dumps(r) + "\n" for r in changed))
        output = run_reader(score_path, receipt_path, f"SYNTHETIC comparability {field} ratio={value}", 0)
        assert ("control not norm-comparable" in output) is (value < 0.1 or value > 10)
    provenance.write_text(original_provenance)
    process_path = dest / "process_exclusion.jsonl"
    for kind in ("contender", "probe_failure"):
        for count in (1, 2, 3):
            middle = [process_event("during_run", True) if kind == "contender" else probe_error() for _ in range(count)]
            changed = annotate([process_event("before_dispatch"), process_event("after_preflight"), *middle, process_event("after_exit")])
            process_path.write_text("".join(json.dumps(e) + "\n" for e in changed))
            receipt["process_log_sha256"] = R.sha_file(process_path)
            write_json(receipt_path, receipt)
            run_reader(score_path, receipt_path, f"SYNTHETIC reader {kind} consecutive={count}", 2 if count == 3 else 0)
    process_path.write_text("".join(json.dumps(e) + "\n" for e in events))
    receipt["process_log_sha256"] = R.sha_file(process_path)
    write_json(receipt_path, receipt)
    cases = {"empty_json": "", "duplicate_key": '{"summary":{},"summary":{}}', "nonfinite": '{"summary":NaN}',
             "wrong_top_level": '[]'}
    for name, raw in cases.items():
        score_path.write_text(raw)
        run_reader(score_path, receipt_path, "MALFORMED " + name, 2)
    for name, operation in (("H_vector_mismatch", lambda s: s["summary"].update(heldout_full=19)),
                            ("unknown_schema_field", lambda s: s.update(synthetic_fixture=True)),
                            ("noninteger_count", lambda s: s["summary"].update(A1=True))):
        changed = copy.deepcopy(score)
        operation(changed)
        write_json(score_path, changed)
        run_reader(score_path, receipt_path, "MALFORMED " + name, 2)
    write_json(score_path, score)
    bad = copy.deepcopy(records)
    bad[2]["positions"][0]["indices"][0] = 0
    provenance.write_text("".join(json.dumps(r) + "\n" for r in bad))
    run_reader(score_path, receipt_path, "MALFORMED position_zero", 2)
    provenance.write_text(original_provenance)
    for raw in ("null", "[]", '{"dest":null}'):
        receipt_path.write_text(raw)
        run_reader(score_path, receipt_path, "MALFORMED receipt " + raw, 2)
    write_json(receipt_path, receipt)


def main():
    assert len(sys.argv) == 2, "usage: test_replay.py /tmp/FRESH_SETUP_CLONE"
    dest = Path(sys.argv[1]).resolve(strict=True)
    assert Path("/tmp").resolve() in dest.parents and (dest / ".git").is_dir(), "tests write only to a scratch clone"
    assert not (dest / "runs").exists(), "use a fresh setup clone"
    audit = R.inspect_replay(dest)
    print("OFFLINE SELF-TEST: SYNTHETIC receipts/norms/MPS/processes; actual cached Rust tokens/source bytes; no GPU or model execution")
    print("SETUP diff/hash verification PASS edit=" + audit["edit_py_sha256"] + " diff=" + audit["diff_sha256"])
    assert R.sha_file(dest / "replay_diff.txt") == R.EXPECTED_DIFF_SHA256
    compile_dir = dest.parent / "compile"
    compile_dir.mkdir()
    for path in (HERE / "read_replay.py", HERE / "tokenizer_precheck.py", Path(__file__), dest / "edit.py", dest / "prepare.py"):
        py_compile.compile(str(path), cfile=str(compile_dir / (path.name + "c")), doraise=True)
        print(f"py_compile {path.name}: PASS")
    for name in ("setup_replay.sh", "run_replay.sh"):
        result = subprocess.run(["bash", "-n", str(HERE / name)], capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        print(f"bash -n {name}: PASS")
    block = "\n".join((dest / "prepare.py").read_text().splitlines()[66:76]) + "\n"
    namespace = {"os": os, "HERE": str(dest)}
    exec(compile(block, "prepare.py:67-76 standalone blocklist only", "exec"), namespace)
    assert namespace["_hits"] == []
    print("prepare.py:67-76 blocklist standalone: PASS hits=[]; no prepare import")
    payload = process_tests(dest)
    body = compile_dir / "runner_payload.py"
    body.write_text(payload)
    py_compile.compile(str(body), cfile=str(compile_dir / "runner_payload.pyc"), doraise=True)
    print("py_compile runner embedded Python (not executed): PASS")
    records = selector_records(dest)
    reader_tests(dest, records)
    assert "torch" not in sys.modules and "transformers" not in sys.modules
    print("FINAL torch_imported=False transformers_imported=False; OFFLINE SELF-TEST PASS")


if __name__ == "__main__":
    main()
