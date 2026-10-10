"""D-ML-1 IO, events and resource boundaries; no torch or model imports."""
import contextlib
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import signal
import subprocess
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
PREREG_SHA = "4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507"
TIER = "MATH-PROXY"


class Halt(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ": " + message)


def require(ok, code, message):
    if not ok:
        raise Halt(code, message)


def utc_tag():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def verify_prereg(root=ROOT):
    require(sha_file(Path(root) / "docs/MATHLAB_PREREG.md") == PREREG_SHA, "PREREG", "frozen preregistration changed")


def read_json(path):
    def bad(value):
        raise ValueError("nonfinite JSON: " + value)
    return json.loads(Path(path).read_text(), parse_constant=bad)


def write_new(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as out:
        out.write(json.dumps(value, indent=2, allow_nan=False) + "\n")


def new_directory(parent, step, stamp=None):
    path = Path(parent) / (step + "_" + (stamp or utc_tag()))
    path.mkdir(parents=True, exist_ok=False)
    return path


def emit(run_dir, event_type, **fields):
    from tools.mathlab_events import emit as shared_emit
    shared_emit(run_dir, event_type, **fields)


def vm_available_gib(text):
    pages = []
    for name in ("free", "inactive", "speculative"):
        match = re.search(r"^Pages " + name + r":\s*(\d+)\.", text, re.M)
        require(match is not None, "MEMORY-PROBE", "vm_stat lacks " + name)
        pages.append(int(match[1]))
    return sum(pages) * 16384 / 2 ** 30


def available_gib():
    result = subprocess.run(["/usr/bin/vm_stat"], capture_output=True, text=True)
    require(result.returncode == 0 and bool(result.stdout.strip()), "MEMORY-PROBE", result.stderr or "empty vm_stat")
    return vm_available_gib(result.stdout)


def wait_for_memory(reserve, sample=available_gib, sleep=time.sleep, clock=time.monotonic, report=None):
    start = clock()
    while True:
        available = sample()
        if report is not None:
            report(available)
        if available >= 8 + reserve:
            return available
        require(clock() - start < 300, "STOPPED-RESOURCE", "cell reserve not available within 300 s")
        sleep(10)


def save_tensors(path, tensors):
    import torch
    require(isinstance(tensors, dict) and all(isinstance(k, str) and isinstance(v, torch.Tensor)
            and v.device.type == "cpu" for k, v in tensors.items()), "ARTIFACT", "expected flat dict of CPU tensors")
    path = Path(path)
    with path.open("xb") as out:
        torch.save(tensors, out)
    return {"path": str(path), "sha256": sha_file(path), "bytes": path.stat().st_size,
            "tier": TIER, "tensors": {k: {"shape": list(v.shape), "dtype": str(v.dtype)} for k, v in tensors.items()}}


class Budget:
    def __init__(self, cap_s, clock=time.monotonic):
        self.clock = clock; self.started = clock(); self.cap_s = cap_s
        self.used = {}; self.active = []; self.last_projection = None

    def begin(self, stage, cap_s):
        now = self.clock(); elapsed = now - self.started
        remaining = cap_s - self.used.get(stage, 0)
        if cap_s == self.cap_s:
            remaining = min(remaining, self.cap_s - elapsed)
        self.last_projection = dict(stage=stage, elapsed_s=elapsed, remaining_stage_s=remaining,
                                    projected_end_s=elapsed + remaining, process_cap_s=self.cap_s)
        require(remaining > 0 and elapsed + remaining <= self.cap_s, "HALT-BUDGET", json.dumps(self.last_projection))
        self.active.append((stage, now, cap_s))

    def end(self, enforce=True):
        stage, start, cap = self.active.pop()
        self.used[stage] = self.used.get(stage, 0) + self.clock() - start
        if enforce:
            require(self.used[stage] <= cap, "HALT-BUDGET", "stage exceeded cap: " + stage)

    def remaining(self):
        now = self.clock()
        return min([self.cap_s - (now - self.started)] +
                   [cap - self.used.get(s, 0) - (now - start) for s, start, cap in self.active])


class Run:
    def __init__(self, run_dir, step, title, deadline_s, sink=emit, sample=available_gib, attach=False):
        self.directory = Path(run_dir); self.step = step; self.sink = sink; self.sample = sample
        self.budget = Budget(deadline_s); self.gates = {}
        if attach:
            from tools.mathlab_events import read_events
            events, errors = read_events(self.directory / "events.jsonl")
            require(not errors, "EVENTS", "; ".join(errors))
            starts = [e for e in events if e["type"] == "run_started"]
            require(len(starts) == 1 and starts[0]["step"] == step, "EVENTS", "one matching run_started required")
            require(not any(e["type"] in ("stage_started", "run_finished") for e in events),
                    "EVENTS", "run has already dispatched; fresh run identity required")
            elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(starts[0]["ts"].replace("Z", "+00:00"))).total_seconds()
            self.budget.started -= elapsed
        else:
            deadline = datetime.now(timezone.utc) + timedelta(seconds=deadline_s)
            self.event("run_started", step=step, title=title, deadline_ts=deadline.isoformat(), pid=os.getpid())

    def event(self, event_type, **fields):
        self.sink(self.directory, event_type, **fields)

    def resources(self, available=None):
        available = self.sample() if available is None else available
        usage = resource.getrusage(resource.RUSAGE_SELF)
        elapsed = max(time.monotonic() - self.budget.started, 1e-6)
        self.event("resource_sample", avail_gib=available, floor_gib=8.,
                   rss_gib=usage.ru_maxrss / 2 ** 30, cpu_pct=100 * (usage.ru_utime + usage.ru_stime) / elapsed)
        return available

    def gate(self, gate_id, plain_words, observed, bar, passed, comparison="meets", fatal=False):
        fields = dict(gate_id=gate_id, plain_words=plain_words, observed=observed, bar=bar,
                      comparison=comparison, passed=bool(passed))
        self.gates[gate_id] = fields; self.event("gate_result", **fields)
        if fatal:
            require(passed, gate_id, plain_words)
        return bool(passed)

    def pre_cell(self, reserve):
        try:
            value = wait_for_memory(reserve, sample=self.sample, report=self.resources)
        except Halt:
            self.gate("memory-reserve-" + str(reserve), "Enough free memory for this calculation",
                      "reserve not available within 300 seconds", 8 + reserve, False)
            raise
        self.gate("memory-reserve-" + str(reserve), "Enough free memory for this calculation",
                  value, 8 + reserve, True, ">=")

    @contextlib.contextmanager
    def stage(self, stage, plain_words, cap_s, alarm=False):
        available = self.resources()
        self.gate("stage-memory-" + stage, "At least eight GiB of memory before this stage",
                  available, 8, available >= 8, ">=", fatal=True)
        try:
            self.budget.begin(stage, cap_s)
        except Halt:
            self.gate("budget-" + stage, "This stage fits the remaining deadline", self.budget.last_projection,
                      self.budget.cap_s, False)
            raise
        self.gate("budget-" + stage, "This stage fits the remaining deadline", self.budget.last_projection,
                  self.budget.cap_s, True)
        self.event("stage_started", stage=stage, plain_words=plain_words, cap_s=cap_s)
        previous = None
        if alarm:
            def timeout(signum, frame):
                raise Halt("HALT-BUDGET", "stage or process hard deadline reached: " + stage)
            previous = signal.signal(signal.SIGALRM, timeout)
            signal.setitimer(signal.ITIMER_REAL, self.budget.remaining())
        try:
            yield
        except BaseException:
            self.budget.end(enforce=False)
            self.event("stage_finished", stage=stage, outcome="INVALID", summary="Stopped; diagnostic follows")
            raise
        else:
            self.budget.end()
            self.event("stage_finished", stage=stage, outcome="PASS", summary="Stage completed")
        finally:
            if alarm:
                signal.setitimer(signal.ITIMER_REAL, 0)
                signal.signal(signal.SIGALRM, previous)
                if self.budget.active:
                    signal.setitimer(signal.ITIMER_REAL, max(1e-6, self.budget.remaining()))


def stage_finding(root, run_dir, unit, summary, sink=emit):
    directory = Path(root) / "logs/pending_findings"; directory.mkdir(parents=True, exist_ok=True)
    numbers = [int(m.group(1)) for p in directory.iterdir() if (m := re.match(r"(\d+)_", p.name))]
    path = directory / f"{max(numbers, default=0) + 1:02d}_mathlab_{unit}_{utc_tag()}.md"
    with path.open("x") as out:
        out.write(f"# D-ML-1 — {unit}\n\nTier: MATH-PROXY.\n\n{summary}\n\n"
                  f"Run events: `{Path(run_dir) / 'events.jsonl'}`.\n\n"
                  "Staging only. The lead performs supervised fold-in and `tools/closeout_check.py D-ML-1`. "
                  "No behavioural claim or route closure; prospective queue utility remains UNVERIFIED.\n")
    sink(run_dir, "finding_staged", finding_id=path.stem, tier=TIER, summary=summary, path=str(path))
    return path


def prior_aborts(root, step, code=None):
    from tools.mathlab_events import read_events
    count = 0
    for path in (Path(root) / "results/mathlab_staging/runs").glob("*/events.jsonl"):
        rows, errors = read_events(path)
        require(not errors, "EVENTS", "cannot count prior aborts: " + "; ".join(errors))
        steps = [r["step"] for r in rows if r["type"] == "run_started"]
        if steps != [step]:
            continue
        reasons = [r["reason"] for r in rows if r["type"] == "halted"]
        if any((r.startswith(code + ":") if code else r.startswith(("STOPPED-RESOURCE:", "STOPPED-DEADLINE:"))) for r in reasons):
            count += 1
    return count


def enforce_stop_policy(root, step, exclude=None):
    from tools.mathlab_events import read_events
    harvest_halts = {}; reproduction_failures = 0; resource_aborts = 0
    for path in (Path(root) / "results/mathlab_staging/runs").glob("*/events.jsonl"):
        if exclude is not None and path.parent.resolve() == Path(exclude).resolve(): continue
        rows, errors = read_events(path)
        require(not errors, "EVENTS", "cannot check stop rules: " + "; ".join(errors))
        starts = [r for r in rows if r["type"] == "run_started"]
        require(len(starts) == 1, "EVENTS", "one run_started required for stop rules")
        previous_step = starts[0]["step"]
        if previous_step == 3 and any((r["type"] == "run_finished" and r["outcome"] == "FAIL") or
                (r["type"] == "gate_result" and r["gate_id"] == "calibration" and r["observed"] == "FAIL") for r in rows):
            raise Halt("LAB-STOP", "frozen calibration failed; an amendment and new calibration arms are required")
        if any(r["type"] == "halted" and r["reason"].startswith("LAB-STOP-2a:") for r in rows):
            raise Halt("LAB-STOP", "gate 2a failed after the single diagnosis")
        if previous_step == 2:
            reproduction_failures += any(r["type"] == "gate_result" and r["gate_id"] == "2a" and not r["passed"] for r in rows)
        reasons = {r["reason"].split(":", 1)[0] for r in rows if r["type"] == "halted"}
        if previous_step == 1:
            for code in reasons: harvest_halts[code] = harvest_halts.get(code, 0) + 1
        if previous_step == step and reasons & {"STOPPED-RESOURCE", "STOPPED-DEADLINE"}:
            resource_aborts += 1
    require(reproduction_failures < 2, "LAB-STOP", "gate 2a failed twice; the lab stops")
    if step == 1:
        require(not any(n >= 2 for n in harvest_halts.values()), "OPERATOR", "two harvest HALTs on the same gate; no third launch")
    require(resource_aborts < 3, "OPERATOR", "three resource/deadline aborts on this step")


def stage_halt(root, run_dir, code, message, sink=emit, step=1, details=None):
    if step in (2, 3) and code == "HALT-BUDGET": code = "STOPPED-DEADLINE"
    root = Path(root); stamp = utc_tag()
    diagnostic = root / "architecture_profile" / ("mathlab_harvest_halt_diagnostic_" + stamp + ".json"
                   if step == 1 else f"mathlab_m{step}_halt_diagnostic_{stamp}.json")
    summary = code + ": " + message
    write_new(diagnostic, dict(tier=TIER, decision_id="D-ML-1", code=code, message=message,
                               details=details or {}, run_dir=str(run_dir)))
    sink(run_dir, "gate_result", gate_id=code, plain_words="Each write records all five layers in order and one return" if code == "CAPTURE" else
         "The requirement described in the stop diagnostic holds", observed=message,
         bar=dict(ordered_pairs=list(map(list, enumerate([4, 5, 6, 7, 8]))), returns=1) if code == "CAPTURE" else "required condition holds",
         comparison="meets", passed=False)
    sink(run_dir, "halted", reason=summary, diagnostic_path=str(diagnostic))
    path = stage_finding(root, run_dir, code.lower(), summary, sink)
    sink(run_dir, "run_finished", outcome="INVALID", summary=summary)
    return dict(diagnostic_path=str(diagnostic), finding_path=str(path))
