"""MathLab observability fixtures; run with /usr/bin/python3 -B -m unittest tools.test_dashboard_mathlab."""
import copy, hashlib, importlib, importlib.util, json, os, re, subprocess, sys, tempfile, threading, unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

START = "2026-10-08T18:00:00Z"
DEADLINE = "2026-10-08T19:00:00Z"
RUN_ID = "fixture-run"
PREREG = ("# Math lab pre-registration\n\n**Status: DRAFT fixture. Not frozen.**\n"
          "- **Round 1:** old SHA `deadbeef…`, FIX-FIRST.\n"
          "- **Next:** Waiting for Astra FREEZE and the GPU queue.\n")
BUILD_PATHS = ("code/apps/mathlab/run_mathlab_harvest.sh", "code/apps/mathlab/mathlab_harvest.py",
               "code/apps/mathlab/m2_solve_repro.py", "code/apps/mathlab/m3_calibration.py")
ANSI = re.compile(r"\033\[[0-9;]*[A-Za-z]")


def event(kind, ts=START, **fields):
    return dict(ts=ts, schema=1, run_id=RUN_ID, type=kind, **fields)


def started(step=1, purpose=None):
    result = event("run_started", step=step, title="Record the model's internal inputs",
                   deadline_ts=DEADLINE, pid=12345)
    if purpose is not None:
        result["purpose"] = purpose
    return result


def harvest():
    return [started(), event("admission", allowed=True, reasons=[]),
            event("stage_started", ts="2026-10-08T18:01:00Z", stage="clean_pass",
                  plain_words="Record the unedited model's inputs for every prompt", cap_s=300),
            event("progress", ts="2026-10-08T18:02:30Z", stage="clean_pass", done=48, total=162, unit="prompts"),
            event("resource_sample", ts="2026-10-08T18:03:00Z", avail_gib=12.5, floor_gib=8, rss_gib=1.2, cpu_pct=64)]


def cheap_stop():
    return [started(3), event("stage_started", stage="calibration",
                             plain_words="Compare math estimates with past model results", cap_s=1800),
            event("gate_result", gate_id="tier_separation", plain_words="Past results form distinct groups",
                  observed=19, bar=10, comparison=">=", passed=True),
            event("gate_result", gate_id="calibration", plain_words="At least one estimate passes the past-result check",
                  observed="FAIL", bar="PASS", comparison="meets", passed=False),
            event("stage_finished", ts="2026-10-08T18:02:00Z", stage="calibration", outcome="FAIL",
                  summary="Neither estimate passed calibration; stop the lab cheaply."),
            event("run_finished", ts="2026-10-08T18:02:00Z", outcome="FAIL",
                  summary="Neither estimate passed calibration; stop the lab cheaply.")]


def write_stream(root, stream, run_id=RUN_ID):
    path = Path(root) / "results/mathlab_staging/runs" / run_id / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(dict(e, run_id=run_id)) + "\n" for e in stream), encoding="utf-8")
    return path


def producer_checks():
    stream = [started(2), event("admission", allowed=True, reasons=[]),
              event("gate_result", gate_id="admission", plain_words="The launch is allowed by all admission checks",
                    observed={"allowed": True, "checks": {str(i): {"ok": True} for i in range(40)}},
                    bar="allowed", comparison="meets", passed=True),
              event("stage_started", stage="reproduction", plain_words="Repeat the saved write calculation on CPU", cap_s=2700)]
    records = {}
    for arm in ("A1_single", "A2_coherent2", "A7_coined_coined", "mint1_s0", "mint1_s1", "mint1_s2"):
        for layer in range(4, 9):
            stream.append(event("gate_result", gate_id=f"2a-projector-{arm}-{layer}",
                                plain_words="Offline projection matches the recorded write",
                                observed={"null_n": 20, "sha256": "f" * 64},
                                bar={"null_n": 20, "probe_relative_max": 1e-6}, comparison="meets", passed=True))
            error = 1e-3 if (arm, layer) == ("mint1_s2", 8) else 1e-7
            stream.append(event("gate_result", gate_id=f"2a-update-{arm}-{layer}",
                                plain_words="Offline write reproduces the saved calculation", observed=error,
                                bar=1e-5, comparison="<=", passed=error <= 1e-5))
            records[f"{arm}:{layer}"] = {"relative_error": error, "update_passed": error <= 1e-5}
    stream += [event("gate_result", gate_id="2a", plain_words="Exact offline reproduction of the recorded write",
                     observed=records, bar="all matches within frozen tolerances", comparison="meets", passed=False),
               event("gate_result", gate_id="2b", plain_words="Clean inputs support first-order alternative solves",
                     observed="OPERANDS-ONLY", bar={"relative_error_max": .25, "cosine_min": .95}, comparison="meets", passed=False),
               harvest()[-1],
               event("finding_staged", finding_id="F1", tier="MATH-PROXY", summary="Saved a math estimate",
                     path="results/mathlab_staging/F1.md"),
               event("candidate_added", candidate_id="C1", source="manual", question="Would smaller writes help?", offline=True)]
    return stream


class Modules(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("mathlab_events"), "event contract is not built yet")
        self.E = importlib.import_module("mathlab_events")


class EventContract(Modules):
    def test_run_purpose_is_an_optional_validated_schema_one_discriminator(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            fields = {k: v for k, v in started(purpose="admission").items() if k not in ("schema", "run_id", "type", "ts")}
            self.E.emit(run, "run_started", **fields)
            rows, errors = self.E.read_events(run / "events.jsonl")
            self.assertEqual(errors, [])
            self.assertEqual(rows[0]["purpose"], "admission")
            before = (run / "events.jsonl").read_bytes()
            with self.assertRaises(ValueError):
                self.E.emit(run, "run_started", **dict(fields, purpose="approved"))
            self.assertEqual((run / "events.jsonl").read_bytes(), before)

    def test_append_preserves_previous_bytes_and_is_one_write_per_event(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            fields = {k: v for k, v in started().items() if k not in ("schema", "run_id", "type", "ts")}
            with patch.object(self.E.os, "write", wraps=os.write) as writes:
                self.E.emit(run, "run_started", **fields)
                self.assertEqual(writes.call_count, 1)
            before = (run / "events.jsonl").read_bytes()
            self.E.emit(run, "admission", allowed=True, reasons=[])
            after = (run / "events.jsonl").read_bytes()
            self.assertTrue(after.startswith(before))
            self.assertEqual(len(after.splitlines()), 2)
            records, errors = self.E.read_events(run / "events.jsonl")
            self.assertEqual(errors, [])
            self.assertEqual(records[0]["run_id"], RUN_ID)
            self.assertEqual(records[0]["schema"], 1)
            self.assertRegex(records[0]["ts"], r"^\d{4}-\d\d-\d\dT.*(?:Z|\+00:00)$")
            self.assertEqual(list(run.iterdir()), [run / "events.jsonl"])

    def test_all_event_variants_round_trip(self):
        stream = harvest() + [
            event("gate_result", gate_id="2a", plain_words="Reproduce the saved update", observed=1e-6,
                  bar=1e-5, comparison="<=", passed=True),
            event("stage_finished", stage="clean_pass", outcome="PASS", summary="Saved all inputs"),
            event("finding_staged", finding_id="F1", tier="MATH-PROXY", summary="Saved a math estimate",
                  path="results/mathlab_staging/F1.md"),
            event("candidate_added", candidate_id="C1", source="InfraNodus", question="Does a narrower write help?", offline=True),
            event("halted", reason="Memory below the safe floor", diagnostic_path="diagnostic.json"),
            event("run_finished", outcome="INVALID", summary="No scientific verdict")]
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            for e in stream:
                self.E.emit(run, e["type"], **{k: v for k, v in e.items() if k not in ("schema", "run_id", "type", "ts")})
            records, errors = self.E.read_events(run / "events.jsonl")
            self.assertEqual(errors, [])
            expected = [e["type"] for e in stream[:-1]] + ["run_finishing", "run_finished"]
            self.assertEqual([e["type"] for e in records], expected)

    def test_terminal_fsync_failure_never_publishes_any_outcome(self):
        write, fsync = self.E.os.write, self.E.os.fsync
        for outcome in ("PASS", "FAIL", "INVALID"):
            with self.subTest(outcome=outcome), tempfile.TemporaryDirectory() as d:
                run = Path(d) / RUN_ID
                fields = {k: v for k, v in started(2).items() if k not in ("schema", "run_id", "type", "ts")}
                self.E.emit(run, "run_started", **fields)
                terminal_inodes = set(); snapshots = []
                def append(fd, data):
                    count = write(fd, data)
                    if b'"type":"run_finished"' in data:
                        stat = os.fstat(fd)
                        terminal_inodes.add((stat.st_dev, stat.st_ino))
                    return count
                def sync(fd):
                    stat = os.fstat(fd)
                    if (stat.st_dev, stat.st_ino) in terminal_inodes:
                        rows, errors = self.E.read_events(run / "events.jsonl")
                        self.assertEqual(errors, [])
                        snapshots.append(self.E.fold(rows))
                        raise OSError("fixture terminal fsync refused")
                    return fsync(fd)
                with patch.object(self.E.os, "write", side_effect=append), patch.object(self.E.os, "fsync", side_effect=sync):
                    with self.assertRaisesRegex(OSError, "terminal fsync refused"):
                        self.E.emit(run, "run_finished", outcome=outcome, summary="fixture completed")
                self.assertTrue(snapshots, "control must hit terminal-bearing file fsync")
                rows, errors = self.E.read_events(run / "events.jsonl")
                self.assertEqual(errors, [])
                for state in snapshots + [self.E.fold(rows)]:
                    self.assertIsNone(state["outcome"])
                    self.assertIsNone(state["finished_ts"])
                    self.assertEqual(state["status"], "invalid: no verdict")
                    self.assertEqual(state["steps"][2], "INVALID")

    def test_torn_terminal_never_finishes_the_run(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            fields = {k: v for k, v in started(2).items() if k not in ("schema", "run_id", "type", "ts")}
            self.E.emit(run, "run_started", **fields)
            write = self.E.os.write
            def torn(fd, data):
                return write(fd, data[:-4]) if b'"type":"run_finished"' in data else write(fd, data)
            with patch.object(self.E.os, "write", side_effect=torn), self.assertRaises(OSError):
                self.E.emit(run, "run_finished", outcome="PASS", summary="fixture completed")
            rows, _ = self.E.read_events(run / "events.jsonl")
            state = self.E.fold(rows)
            self.assertIsNone(state["outcome"])
            self.assertEqual(state["status"], "invalid: no verdict")

    def test_terminal_refuses_a_malformed_existing_stream(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            fields = {k: v for k, v in started(2).items() if k not in ("schema", "run_id", "type", "ts")}
            self.E.emit(run, "run_started", **fields)
            path = run / "events.jsonl"
            damaged = path.read_bytes() + b'{"schema":1\n'
            path.write_bytes(damaged)
            with self.assertRaisesRegex(OSError, "invalid event stream"):
                self.E.emit(run, "run_finished", outcome="PASS", summary="fixture completed")
            self.assertEqual(path.read_bytes(), damaged)

    def test_append_racing_terminal_publication_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            fields = {k: v for k, v in started(2).items() if k not in ("schema", "run_id", "type", "ts")}
            self.E.emit(run, "run_started", **fields)
            before = (run / "events.jsonl").read_bytes()
            write, fsync = self.E.os.write, self.E.os.fsync
            terminal_inodes = set(); entered = threading.Event(); errors = []; fired = False
            def append(fd, data):
                count = write(fd, data)
                if b'"type":"run_finished"' in data:
                    stat = os.fstat(fd)
                    terminal_inodes.add((stat.st_dev, stat.st_ino))
                return count
            def concurrent_append():
                entered.set()
                try: self.E.emit(run, "progress", stage="reproduction", done=1, total=1, unit="fixture")
                except BaseException as error: errors.append(error)
            worker = threading.Thread(target=concurrent_append)
            def sync(fd):
                nonlocal fired
                stat = os.fstat(fd)
                if not fired and (stat.st_dev, stat.st_ino) in terminal_inodes:
                    fired = True; worker.start()
                    self.assertTrue(entered.wait(1))
                    worker.join(.05)
                return fsync(fd)
            with patch.object(self.E.os, "write", side_effect=append), patch.object(self.E.os, "fsync", side_effect=sync):
                self.E.emit(run, "run_finished", outcome="PASS", summary="fixture completed")
                worker.join(1)
            self.assertFalse(worker.is_alive())
            self.assertEqual(errors, [])
            self.assertTrue((run / "events.jsonl").read_bytes().startswith(before))
            rows, errors = self.E.read_events(run / "events.jsonl")
            self.assertEqual(errors, [])
            self.assertEqual(sum(e["type"] == "progress" for e in rows), 1)
            self.assertEqual(self.E.fold(rows)["outcome"], "PASS")

    def test_short_prefix_copy_cannot_publish_a_terminal(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            fields = {k: v for k, v in started(2).items() if k not in ("schema", "run_id", "type", "ts")}
            self.E.emit(run, "run_started", **fields)
            before = (run / "events.jsonl").read_bytes()
            fdopen, write = self.E.os.fdopen, self.E.os.write
            fired = False
            def copy_write(delegate, data):
                nonlocal fired
                if not fired and b'"type":"run_started"' in data:
                    fired = True
                    return delegate(data[:data.index(b'\n')+1])
                return delegate(data)
            class Target:
                def __init__(self, target): self.target = target
                def __enter__(self): return self
                def __exit__(self, *args): return self.target.__exit__(*args)
                def __getattr__(self, name): return getattr(self.target, name)
                def write(self, data): return copy_write(self.target.write, data)
            def append(fd, data): return copy_write(lambda block: write(fd, block), data)
            with patch.object(self.E.os, "fdopen", side_effect=lambda *a, **kw: Target(fdopen(*a, **kw))), \
                 patch.object(self.E.os, "write", side_effect=append):
                with self.assertRaisesRegex(OSError, "short .*prefix"):
                    self.E.emit(run, "run_finished", outcome="PASS", summary="fixture completed")
            self.assertTrue(fired, "control must shorten the real prefix-copy write")
            self.assertTrue((run / "events.jsonl").read_bytes().startswith(before))
            rows, errors = self.E.read_events(run / "events.jsonl")
            self.assertEqual(errors, [])
            state = self.E.fold(rows)
            self.assertIsNone(state["outcome"])
            self.assertEqual(state["status"], "invalid: no verdict")

    def test_unknown_missing_extra_and_reserved_fields_are_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as d:
            run = Path(d) / RUN_ID
            self.E.emit(run, "admission", allowed=True, reasons=[])
            before = (run / "events.jsonl").read_bytes()
            cases = [("mystery", {}), ("admission", {"allowed": True}),
                     ("admission", {"allowed": True, "reasons": [], "status": "ok"}),
                     ("admission", {"allowed": True, "reasons": [], "schema": 2})]
            for kind, fields in cases:
                with self.subTest(kind=kind, fields=fields), self.assertRaises(ValueError):
                    self.E.emit(run, kind, **fields)
                self.assertEqual((run / "events.jsonl").read_bytes(), before)

    def test_wrong_types_outcomes_and_tiers_are_rejected(self):
        bad = [event("admission", allowed=1, reasons=[]), event("admission", allowed=False, reasons="GPU"),
               dict(started(), step=True), dict(started(), step=5), dict(started(), pid=0),
               event("progress", stage="clean", done=4, total=3, unit="prompts"),
               event("stage_started", stage="x", plain_words="x", cap_s=-1),
               event("stage_finished", stage="x", outcome="PARTIAL", summary="x"),
               event("run_finished", outcome="UNKNOWN", summary="x"),
               event("resource_sample", avail_gib=float("nan"), floor_gib=8, rss_gib=1, cpu_pct=10),
               event("finding_staged", finding_id="f", tier="EVIDENCE", summary="x", path="f.md"),
               event("gate_result", gate_id="g", plain_words="x", observed=float("inf"), bar=1, comparison=">", passed=True),
               dict(started(), ts="2026-10-08T18:00:00"), dict(started(), schema=True)]
        for e in bad:
            with self.subTest(event=e), self.assertRaises(ValueError):
                self.E.fold([e])

    def test_short_append_raises(self):
        with tempfile.TemporaryDirectory() as d, patch.object(self.E.os, "write", return_value=1):
            with self.assertRaises(OSError):
                self.E.emit(Path(d) / RUN_ID, "admission", allowed=True, reasons=[])

    def test_malformed_schema_utf8_and_partial_lines_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_stream(d, [started()])
            with path.open("ab") as out:
                out.write(b'not json\n{}\n\xff\n{"schema":1')
            records, errors = self.E.read_events(path)
            self.assertEqual(records, [started()])
            self.assertEqual(len(errors), 4)
            for line in range(2, 6):
                self.assertTrue(any(f"line {line}" in err for err in errors))

    def test_duplicate_json_keys_and_wrong_run_id_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            path = write_stream(d, [started()])
            with path.open("a") as out:
                out.write(json.dumps(dict(started(), run_id="other")) + "\n")
                out.write(json.dumps(started())[:-1] + ', "schema": 1}\n')
            records, errors = self.E.read_events(path)
            self.assertEqual(len(records), 1)
            self.assertEqual(len(errors), 2)

    def test_missing_file_is_an_explicit_read_error(self):
        records, errors = self.E.read_events("/private/tmp/mathlab-does-not-exist/events.jsonl")
        self.assertEqual(records, [])
        self.assertTrue(errors)


class EventFold(Modules):
    def test_aggregate_calibration_preserves_producer_outcome_before_run_finished(self):
        for outcome, status in (("PASS", "running"), ("FAIL", "stopped: check failed"), ("INVALID", "invalid: no verdict")):
            with self.subTest(outcome=outcome):
                stream = [started(3), event("stage_started", stage="calibration", plain_words="Check tier separation", cap_s=1800),
                          event("gate_result", gate_id="calibration", plain_words="At least one math estimate separates the measured tiers",
                                observed=outcome, bar="PASS", comparison="meets", passed=outcome == "PASS")]
                state = self.E.fold(stream)
                self.assertEqual(state["calibration_outcome"], outcome)
                self.assertEqual(state["gate_outcomes"]["calibration"], outcome)
                self.assertEqual(state["status"], status)
                self.assertEqual(state["steps"][3], "running" if outcome == "PASS" else outcome)
                self.assertIsNone(state["finished_ts"])

    def test_producer_gate_identifiers_join_the_shared_planned_groups(self):
        gates = [("context", "frozen hash", "frozen hash"), ("law3", {"passed": True}, "all three pass"),
                 ("law5", {"ok": True}, {"expr_delta_lt": .05, "loc_delta_lt": 3, "tagged_captures": 5}),
                 ("observer-parity", {"passed": True}, "relative deployed-delta error <= 1e-6"),
                 ("budget-clean", {"projected_s": 300}, 3600), ("budget-fresh", {"projected_s": 1800}, 3600),
                 ("stage-memory-clean", 12, 8), ("memory-reserve-9", 20, 17)]
        stream = [started()] + [event("gate_result", gate_id=key, plain_words=key, observed=observed,
                                     bar=bar, comparison="meets", passed=True) for key, observed, bar in gates]
        state = self.E.fold(stream)
        for group in ("context", "law3", "inertness", "budget", "memory"):
            self.assertEqual(state["gate_groups"][group]["outcome"], "PASS", group)
        self.assertEqual(state["gate_groups"]["inertness"]["gate_ids"], ["law5", "observer-parity"])
        self.assertEqual(state["gate_groups"]["budget"]["gate_ids"], ["budget-clean", "budget-fresh"])
        self.assertEqual(state["gate_groups"]["memory"]["gate_ids"], ["stage-memory-clean", "memory-reserve-9"])
        self.assertIsNone(self.E.fold([started(), stream[3]])["gate_groups"]["inertness"]["outcome"])

    def test_admission_only_pass_never_completes_an_experiment_step(self):
        for purpose in (None, "admission"):
            for step in (1, 2):
                with self.subTest(purpose=purpose, step=step):
                    stream = [started(step, purpose=purpose), event("admission", allowed=True, reasons=[]),
                              event("gate_result", gate_id="admission", plain_words="The launch is allowed by all admission checks",
                                    observed={"allowed": True}, bar="allowed", comparison="meets", passed=True),
                              event("run_finished", outcome="PASS", summary="Admission allowed")]
                    state = self.E.fold(stream)
                    self.assertEqual(state["purpose"], "admission")
                    self.assertEqual(state["outcome"], "PASS")
                    self.assertEqual(state["steps"], {i: "not started" for i in range(1, 5)})

    def test_legacy_admission_then_real_stage_is_an_experiment_run(self):
        state = self.E.fold(harvest() + [event("run_finished", outcome="PASS", summary="Harvest completed")])
        self.assertEqual(state["purpose"], "experiment")
        self.assertEqual(state["steps"][1], "PASS")
        self.assertEqual(len(state["stages"]), 1)
        self.assertEqual(state["resource_samples"], [harvest()[-1]])

    def test_no_events_is_not_started(self):
        state = self.E.fold([])
        self.assertEqual(state["status"], "not started")
        self.assertEqual(state["steps"], {1: "not started", 2: "not started", 3: "not started", 4: "not started"})

    def test_running_harvest_and_progress(self):
        state = self.E.fold(harvest())
        self.assertEqual((state["status"], state["step"]), ("running", 1))
        self.assertEqual(state["stage"]["plain_words"], "Record the unedited model's inputs for every prompt")
        self.assertEqual((state["progress"]["done"], state["progress"]["total"]), (48, 162))
        self.assertEqual(state["resources"]["avail_gib"], 12.5)

    def test_denied_gpu_admission_then_allowed(self):
        stream = [started(), event("admission", allowed=False, reasons=["GPU in use by ASTRA attempt 3"])]
        self.assertEqual(self.E.fold(stream)["status"], "waiting for GPU")
        stream.append(event("admission", allowed=True, reasons=[]))
        self.assertEqual(self.E.fold(stream)["status"], "running")

    def test_step_two_pass_does_not_invent_step_one_pass(self):
        state = self.E.fold([started(2), event("run_finished", outcome="PASS", summary="Exact solve reproduced")])
        self.assertEqual((state["status"], state["steps"][2]), ("finished", "PASS"))
        self.assertEqual(state["steps"][1], "not started")

    def test_successful_substage_does_not_finish_the_step(self):
        state = self.E.fold([started(), event("stage_started", stage="setup", plain_words="Check admission", cap_s=900),
                            event("stage_finished", stage="setup", outcome="PASS", summary="Ready")])
        self.assertEqual(state["steps"][1], "running")

    def test_finishing_a_stage_preserves_the_original_recent_events(self):
        stream = [started(), event("stage_started", stage="setup", plain_words="Check admission", cap_s=900),
                  event("stage_finished", stage="setup", outcome="PASS", summary="Ready")]
        state = self.E.fold(stream)
        self.assertEqual(state["recent"], stream)
        self.assertNotIn("outcome", state["recent"][1])
        self.assertEqual(state["stage"]["outcome"], "PASS")

    def test_aggregate_calibration_failure_is_the_cheap_stop(self):
        state = self.E.fold(cheap_stop())
        self.assertEqual(state["status"], "stopped: check failed")
        self.assertEqual(state["steps"][3], "FAIL")
        self.assertEqual(len(state["gates"]), 2)
        state = self.E.fold(cheap_stop()[:4])
        self.assertEqual(state["status"], "stopped: check failed")

    def test_one_proxy_can_fail_then_another_pass_without_stopping(self):
        stream = [started(3), event("gate_result", gate_id="keyed_transfer", plain_words="Target transfer estimate",
                                  observed=1800, bar=1900, comparison=">=", passed=False)]
        self.assertEqual(self.E.fold(stream)["status"], "running")
        stream += [event("gate_result", gate_id="collateral", plain_words="Unwanted changes estimate",
                         observed=1950, bar=1900, comparison=">=", passed=True),
                   event("run_finished", outcome="PASS", summary="One estimate passed")]
        self.assertEqual(self.E.fold(stream)["status"], "finished")

    def test_gate_two_b_failure_does_not_stop_the_lab(self):
        state = self.E.fold([started(2), event("gate_result", gate_id="2b", plain_words="Can clean inputs approximate the write?",
                                             observed=0.5, bar=0.25, comparison="<=", passed=False)])
        self.assertEqual(state["status"], "running")

    def test_invalid_is_no_verdict_and_resource_halt_is_not_a_cheap_stop(self):
        state = self.E.fold([started(3), event("run_finished", outcome="INVALID", summary="Too few admitted arms")])
        self.assertEqual((state["status"], state["outcome"]), ("finished", "INVALID"))
        state = self.E.fold([started(2), event("halted", reason="STOPPED-RESOURCE: not enough memory",
                                             diagnostic_path="resource.json")])
        self.assertEqual(state["status"], "halted")

    def test_halt_and_finished_states_survive_late_samples(self):
        for terminal, want in [(event("halted", reason="Deadline exceeded", diagnostic_path="deadline.json"), "halted"),
                               (event("run_finished", outcome="PASS", summary="Complete"), "finished")]:
            stream = [started(), terminal, harvest()[-1]]
            self.assertEqual(self.E.fold(stream)["status"], want)

    def test_new_stage_clears_previous_progress(self):
        state = self.E.fold(harvest() + [event("stage_started", stage="writes", plain_words="Record each write", cap_s=1800)])
        self.assertIsNone(state["progress"])

    def test_fold_is_pure_and_recent_events_are_bounded(self):
        stream = harvest() + [event("resource_sample", avail_gib=i, floor_gib=8, rss_gib=1, cpu_pct=10) for i in range(12)]
        original = copy.deepcopy(stream)
        state = self.E.fold(stream)
        self.assertEqual(stream, original)
        self.assertEqual(len(state["recent"]), 8)
        self.assertEqual(state, self.E.fold(iter(stream)))
        state["resources"]["avail_gib"] = -1
        self.assertEqual(stream, original)

    def test_mixed_run_stream_is_rejected(self):
        with self.assertRaises(ValueError):
            self.E.fold([started(), dict(harvest()[-1], run_id="other")])


class Dashboard(Modules):
    def setUp(self):
        super().setUp()
        self.assertIsNotNone(importlib.util.find_spec("dashboard_mathlab"), "MathLab dashboard is not built yet")
        self.D = importlib.import_module("dashboard_mathlab")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "experiments/ml/design/MATHLAB_PREREG.md").write_text(PREREG, encoding="utf-8")
        self.now = 1791482580.0  # 2026-10-08 18:03:00 UTC

    def frame(self, stream=None, cols=110, rows=40, gpu=None, check_page=None):
        if stream is not None:
            write_stream(self.root, stream)
        with patch.object(self.D, "ROOT", str(self.root)), patch.object(self.D.time, "time", return_value=self.now), \
             patch.object(self.D.dashboard_live, "gpu_state", return_value=gpu or {"running": None, "last_exit": None, "last_name": None}):
            args = {} if check_page is None else {"check_page": check_page}
            return ANSI.sub("", "\n".join(self.D.render(cols, rows, **args)))

    def test_builder_sized_checks_preserve_disclaimer_machine_findings_and_questions(self):
        text = self.frame(producer_checks(), check_page=0)
        self.assertLessEqual(len(text.splitlines()), 40)
        self.assertTrue(all(len(line) <= 110 for line in text.splitlines()))
        self.assertIn("MATH-PROXY", text.splitlines()[1])
        for expected in ("math estimate, not evidence", "CHECKS", "page 1/", "2a-update-mint1_s2-8", "0.001", "1e-05",
                         "MACHINE", "12.5 GiB", "1.2 GiB", "F1", "Saved a math estimate", "CANDIDATE QUESTIONS",
                         "Would smaller writes help?", "ideas to test", "Offline write reproduces the saved calculation"):
            self.assertIn(expected, text)

    def test_checks_paginate_and_keep_required_bars_ahead_of_large_observations(self):
        stream = producer_checks()
        first = self.frame(stream, check_page=0)
        pages = int(re.search(r"page 1/(\d+)", first).group(1))
        frames = [self.frame(check_page=i) for i in range(pages)]
        all_pages = "\n".join(frames)
        for gate in (e for e in stream if e["type"] == "gate_result"):
            self.assertIn(gate["gate_id"], all_pages)
        admission_line = next(line for line in all_pages.splitlines() if "PASS admission" in line)
        self.assertIn('bar meets "allowed"', admission_line)
        self.assertIn("bar", admission_line)
        for text in frames:
            self.assertIn("2a-update-mint1_s2-8", text)
            self.assertIn("math estimate, not evidence", text)
            self.assertIn("MACHINE", text)

    def test_invalid_calibration_does_not_render_a_cheap_stop(self):
        stream = [started(3), event("gate_result", gate_id="calibration", plain_words="At least one estimate separates tiers",
                                  observed="INVALID", bar="PASS", comparison="meets", passed=False)]
        text = self.frame(stream)
        self.assertIn("INVALID: no verdict", text)
        self.assertNotIn("Designed cheap stop", text)
        self.assertIn('bar meets "PASS"', text)

    def test_run_selection_policy_and_other_active_run_count_are_visible(self):
        other = write_stream(self.root, harvest(), run_id="other-active")
        os.utime(other, (10, 10))
        old_finished = write_stream(self.root, cheap_stop(), run_id="old-finished")
        os.utime(old_finished, (20, 20))
        text = self.frame(harvest())
        self.assertIn("newest events file by mtime", text)
        self.assertIn("other active runs (events): 1", text)

    def test_admission_receipt_labels_the_scope_and_keeps_plan_unstarted(self):
        text = self.frame([started(purpose="admission"), event("admission", allowed=True, reasons=[]),
                           event("run_finished", outcome="PASS", summary="Admission allowed")])
        self.assertIn("admission only", text)
        self.assertIn("· 1", text)
        self.assertNotIn("✓ 1", text)

    def present_build_files(self):
        for relative in BUILD_PATHS:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n", encoding="utf-8")

    def frozen_prereg(self):
        (self.root / "experiments/ml/design/MATHLAB_PREREG.md").write_text(
            PREREG.replace("DRAFT fixture. Not frozen.", "FROZEN fixture."), encoding="utf-8")

    def test_idle_shows_plan_current_prereg_status_sha_and_wait(self):
        text = self.frame()
        for expected in ("not started", "Harvest", "Reproduce", "Calibrate", "Candidate", "DRAFT fixture", "Not frozen",
                         "Waiting: pre-registration freeze", "GPU free", hashlib.sha256(PREREG.encode()).hexdigest()[:12]):
            self.assertIn(expected, text)
        self.assertNotIn("deadbeef", text)
        self.assertNotIn("no data", text.lower())
        self.assertFalse((self.root / "results").exists())

    def test_harvest_screen_shows_progress_deadline_cap_and_resources(self):
        text = self.frame(harvest())
        for expected in ("running", RUN_ID, "48/162", "prompts", "3m00s", "1h00m", "2m00s", "5m00s",
                         "12.5 GiB", "8 GiB", "1.2 GiB", "64%", "█"):
            self.assertIn(expected, text)

    def test_idle_reads_status_with_trailing_review_prose(self):
        header = ("# Pre-registration\n\n**Status: FROZEN v4, 2026-10-08.** Freezing approves the design. Review history:\n"
                  "- **Round 3:** previous SHA `deadbeef…`.\n"
                  "- **Next:** The harvest still waits for GPU queue admission.\n")
        (self.root / "experiments/ml/design/MATHLAB_PREREG.md").write_text(header, encoding="utf-8")
        text = self.frame()
        self.assertIn("FROZEN v4", text)
        self.assertIn(hashlib.sha256(header.encode()).hexdigest()[:12], text)
        self.assertIn("GPU free", text)
        self.assertNotIn("GPU queue admission", text)
        self.assertNotIn("PREREG ERROR", text)

    def test_idle_gpu_wait_names_the_current_shared_job(self):
        self.frozen_prereg()
        self.present_build_files()
        for job, name in (("c10z", "ASTRA"), ("c10y", "Step 7")):
            with self.subTest(job=job):
                text = self.frame(gpu={"running": (job, "solve", "02:01:00"),
                                       "last_exit": None, "last_name": None})
                self.assertIn(f"Waiting: GPU in use by {name} ({job})", text)
                self.assertIn("solve · 02:01:00", text)
                self.assertNotIn("GPU free", text)

    def test_idle_free_gpu_and_present_files_do_not_claim_a_build_or_launch_approval(self):
        self.frozen_prereg()
        self.present_build_files()
        text = self.frame()
        self.assertIn("GPU free", text)
        self.assertNotRegex(text, r"(?m)^\s*Waiting:.*GPU")
        self.assertNotIn("missing", text)
        self.assertNotIn("build complete", text.lower())
        self.assertNotIn("launch approved", text.lower())
        for relative in BUILD_PATHS:
            self.assertRegex(text, r"(?m)^\s*Present:.*" + re.escape(relative))

    def test_idle_waits_for_each_missing_launcher_driver_and_notebook(self):
        self.frozen_prereg()
        self.present_build_files()
        for relative in BUILD_PATHS:
            with self.subTest(missing=relative):
                path = self.root / relative
                before = path.read_bytes()
                path.unlink()
                text = self.frame()
                waiting = "\n".join(line for line in text.splitlines() if line.lstrip().startswith("Waiting:"))
                self.assertIn("missing", waiting)
                self.assertIn(relative, waiting)
                for present in set(BUILD_PATHS) - {relative}:
                    self.assertNotIn(present, waiting)
                    self.assertRegex(text, r"(?m)^\s*Present:.*" + re.escape(present))
                path.write_bytes(before)

    def test_idle_rechecks_file_presence_on_every_frame(self):
        self.frozen_prereg()
        missing = self.frame()
        for relative in BUILD_PATHS:
            self.assertRegex(missing, r"(?m)^\s*Waiting:.*" + re.escape(relative))
        self.present_build_files()
        present = self.frame()
        for relative in BUILD_PATHS:
            self.assertRegex(present, r"(?m)^\s*Present:.*" + re.escape(relative))
            self.assertNotRegex(present, r"(?m)^\s*Waiting:.*" + re.escape(relative))

    def test_idle_freeze_wait_comes_from_the_current_status_line(self):
        self.present_build_files()
        for status, needs_freeze in (("DRAFT fixture. Not frozen.", True), ("Not frozen", True),
                                     ("FROZEN fixture.", False)):
            with self.subTest(status=status):
                header = f"# Pre-registration\n\n**Status: {status}**\n"
                (self.root / "experiments/ml/design/MATHLAB_PREREG.md").write_text(header, encoding="utf-8")
                text = self.frame()
                self.assertIn(f"Pre-registration: {status}", text)
                self.assertEqual("Waiting: pre-registration freeze" in text, needs_freeze)

    def test_idle_ignores_stale_next_prose(self):
        self.present_build_files()
        header = ("# Pre-registration\n\n**Status: FROZEN fixture.**\n"
                  "- **Next:** C10X re-run 3 and ASTRA attempt 3 must exit; no driver or notebook exists.\n")
        (self.root / "experiments/ml/design/MATHLAB_PREREG.md").write_text(header, encoding="utf-8")
        text = self.frame()
        self.assertIn(hashlib.sha256(header.encode()).hexdigest()[:12], text)
        for stale in ("C10X re-run 3", "ASTRA attempt 3", "no driver or notebook exists"):
            self.assertNotIn(stale, text)
        self.assertNotIn("Waiting: pre-registration freeze", text)

    def test_idle_unreadable_prereg_keeps_gpu_and_file_facts_visible(self):
        self.present_build_files()
        (self.root / "experiments/ml/design/MATHLAB_PREREG.md").unlink()
        text = self.frame()
        self.assertIn("PREREG ERROR", text)
        self.assertIn("Waiting: pre-registration status unavailable", text)
        self.assertIn("GPU free", text)
        for relative in BUILD_PATHS:
            self.assertRegex(text, r"(?m)^\s*Present:.*" + re.escape(relative))

    def test_waiting_for_gpu_uses_shared_gpu_state_and_admission_reason(self):
        text = self.frame([started(), event("admission", allowed=False, reasons=["GPU queue has not cleared"])],
                          gpu={"running": ("c10z", "solve", "02:01:00"), "last_exit": None, "last_name": None})
        self.assertIn("waiting for GPU", text)
        self.assertIn("GPU in use by ASTRA", text)
        self.assertIn("GPU queue has not cleared", text)

    def test_gpu_probe_error_is_visible_and_does_not_break_the_frame(self):
        with patch.object(self.D, "ROOT", str(self.root)), \
             patch.object(self.D.dashboard_live, "gpu_state", side_effect=PermissionError("process inventory denied")):
            text = ANSI.sub("", "\n".join(self.D.render(110, 40)))
        self.assertIn("GPU state unavailable", text)
        self.assertIn("process inventory denied", text)
        self.assertIn("Waiting: GPU state unavailable", text)
        self.assertNotIn("GPU free", text)
        self.assertIn("not started", text)

    def test_step_two_pass_and_missing_resource_labels(self):
        text = self.frame([started(2), event("run_finished", outcome="PASS", summary="Exact solve reproduced")])
        self.assertIn("✓ 2", text)
        self.assertIn("PASS", text)
        self.assertIn("not sampled", text)

    def test_step_three_failed_check_is_explained_as_designed_cheap_stop(self):
        text = self.frame(cheap_stop())
        for expected in ("stopped: check failed", "Designed cheap stop", "FAIL", "No claim", "19", ">= 10"):
            self.assertIn(expected, text)

    def test_halted_shows_reason_and_diagnostic(self):
        text = self.frame([started(), event("halted", reason="Deadline exceeded", diagnostic_path="diagnostic.json")])
        self.assertIn("halted", text)
        self.assertIn("Deadline exceeded", text)
        self.assertIn("diagnostic.json", text)
        self.assertNotIn("Designed cheap stop", text)

    def test_invalid_is_labelled_no_verdict(self):
        text = self.frame([started(3), event("run_finished", outcome="INVALID", summary="Too few admitted arms")])
        self.assertIn("INVALID", text)
        self.assertIn("no verdict", text.lower())
        self.assertNotIn("Designed cheap stop", text)

    def test_finding_and_candidate_keep_tier_source_and_offline_status(self):
        stream = harvest() + [event("finding_staged", finding_id="F1", tier="MATH-PROXY", summary="A smaller solve may help",
                                   path="results/mathlab_staging/F1.md"),
                              event("candidate_added", candidate_id="C1", source="InfraNodus", question="Try a narrower write?", offline=True),
                              event("candidate_added", candidate_id="C2", source="manual", question="Does the model agree?", offline=False)]
        text = self.frame(stream)
        for expected in ("MATH-PROXY", "math estimate, not evidence", "F1.md", "InfraNodus", "offline yes", "offline no"):
            self.assertIn(expected, text)

    def test_malformed_line_remains_visible_in_a_short_frame(self):
        path = write_stream(self.root, harvest())
        with path.open("a") as out:
            out.write("{broken\n")
        text = self.frame(rows=12)
        self.assertIn("EVENT ERROR", text)
        self.assertIn("line 6", text)

    def test_latest_run_is_selected_and_previous_run_is_not_rewritten(self):
        old = write_stream(self.root, cheap_stop(), run_id="old-run")
        before = old.read_bytes()
        os.utime(old, (10, 10))
        new = write_stream(self.root, harvest(), run_id="new-run")
        os.utime(new, (20, 20))
        text = self.frame()
        self.assertIn("new-run", text)
        self.assertNotIn("old-run", text)
        self.assertEqual(old.read_bytes(), before)

    def test_text_is_cleaned_and_width_is_bounded_at_80_200_and_300(self):
        stream = harvest()
        stream[2]["plain_words"] = "Record\n\tinputs \033[31mnow\033[0m " + "very long " * 40
        for cols in (80, 200, 300):
            with self.subTest(cols=cols):
                text = self.frame(stream, cols=cols)
                self.assertLessEqual(len(text.splitlines()), 40)
                self.assertTrue(all(len(line) <= cols for line in text.splitlines()))
                self.assertNotIn("\t", text)
                self.assertIn("Record inputs", text)

    def test_once_cli_at_80_and_200_columns(self):
        script = Path(self.D.__file__)
        for cols in (80, 200):
            with self.subTest(cols=cols):
                out = subprocess.run(["/usr/bin/python3", "-B", str(script), "--once", str(cols), "40"],
                                     capture_output=True, text=True, timeout=10)
                self.assertEqual(out.returncode, 0, out.stderr)
                text = ANSI.sub("", out.stdout)
                self.assertTrue(text.strip())
                self.assertTrue(all(len(line) <= cols for line in text.splitlines()))
                self.assertLessEqual(len(text.splitlines()), 40)


if __name__ == "__main__":
    unittest.main()
