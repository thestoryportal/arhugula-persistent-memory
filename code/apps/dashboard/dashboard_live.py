"""Live state for the team dashboard, derived from the program's own records on every redraw, never typed by hand:
operator rulings awaited (runbook §5.2 rows whose status says "awaiting operator"), the GPU job or the last
coordinator outcome, Codex builds that are working, running helper agents, and the events newer than the
hand-written report text. Panes reload themselves when their repo imports change; the team view composes its live
session list without rebuilding tmux panes. Pure functions first; gather() and the effects at the bottom.
"""
import ast, collections, functools, glob, json, math, os, re, shlex, subprocess, sys, time, unicodedata
from datetime import datetime

TOOLS = os.path.dirname(os.path.abspath(__file__))
# Shared packages (apps.mathlab, state) live under code/; panes run this file as a script, without PYTHONPATH.
sys.path.insert(0, os.path.dirname(os.path.dirname(TOOLS)))
from state import llmdb_records as L  # noqa: E402
# Legacy C10 stages are recognized here alongside the named launchers below.
# Jobs from checkouts still on the pre-v2 layout (experiments/track_c/, tools/) run on the same GPU.
GPU_JOB_RE = re.compile(r"^(?:.*/)?(?:(?:experiments|code/lab)/track_c/|(?:tools|code/lab/runners)/(?:run_)?)(c10[a-z])\w*?(?:\.py|\.sh)$")
# The one definition of "an agent pane is busy": a Codex/Claude spinner line, or Codex's slow-model menu, which keeps
# waiting by itself ("Codex will keep waiting") and must not read as finished. Tiles and the watcher both use it.
BUSY_RE = re.compile(r"esc to interrupt|Working \(|· Working ·|Codex will keep waiting|^[^\w\s]\s\S+… \(\d", re.M)   # "· Working ·" = Codex footer status, present even between steps
INTERPRETER_RE = re.compile(r"(?i)^(python[0-9.]*|bash|sh)$")
TEMP_ROOTS = ("/private/tmp/", "/tmp/", "/private/var/folders/", "/var/folders/")


def script_call(command):
    """Executable script arguments and explicit env bindings; never search a prompt or inline program."""
    try:
        parts = shlex.split(command)
    except ValueError:
        return None
    env = {}
    while parts:
        executable = os.path.basename(parts[0]).lower(); i = 1
        if executable == 'env':
            while i < len(parts):
                flag = parts[i]
                if flag in ('-u', '--unset'):
                    if i + 1 >= len(parts): return None
                    env.pop(parts[i + 1], None); i += 2
                elif flag.startswith('--unset='):
                    env.pop(flag.split('=', 1)[1], None); i += 1
                elif flag in ('-i', '--ignore-environment'):
                    env.clear(); i += 1
                elif flag == '--':
                    i += 1
                elif re.match(r'^[A-Za-z_]\w*=', flag):
                    key, value = flag.split('=', 1); env[key] = value; i += 1
                else:
                    break
        elif executable in ('nice', 'timeout', 'caffeinate'):
            while i < len(parts) and parts[i].startswith('-'):
                flag = parts[i]
                i += 2 if flag in ('-n', '--adjustment', '-k', '--kill-after', '-s', '--signal', '-t', '-w') else 1
            if executable == 'timeout':
                if i >= len(parts) or not re.fullmatch(r'\d+(?:\.\d+)?[smhd]?', parts[i]): return None
                i += 1
        else:
            break
        parts = parts[i:]
    if not parts: return None
    executable = os.path.basename(parts[0]).lower(); i = 0
    if executable == 'uv':
        if len(parts) < 3 or parts[1] != 'run': return None
        i = 2
        while i < len(parts) and parts[i].startswith('-') and parts[i] != '--script':
            flag = parts[i]
            if flag in ('--python', '--project', '--directory', '--with', '--with-editable', '--with-requirements', '--extra'):
                i += 2
            elif flag in ('--offline', '--frozen', '--locked', '--no-project', '--no-sync', '--isolated') or '=' in flag:
                i += 1
            else: return None
        if i >= len(parts) or parts[i] != '--script': return None
        i += 1
    elif INTERPRETER_RE.fullmatch(executable):
        i = 1
        while i < len(parts) and parts[i].startswith('-'):
            flag = parts[i]
            if (executable.startswith('python') and flag.startswith(('-c', '-m'))) or (
                    executable in ('bash', 'sh') and not flag.startswith('--') and 'c' in flag[1:]):
                return None
            if flag == '--': i += 1; break
            takes_value = flag in ('-W', '-X') if executable.startswith('python') else flag in ('-o', '-O')
            i += 2 if takes_value else 1
    if i >= len(parts) or os.path.normpath(parts[i]).startswith(TEMP_ROOTS): return None
    return parts[i:], env


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(TOOLS)))
JOB_TYPES = (
    (("code/apps/mathlab/run_mathlab_harvest.sh", "code/apps/mathlab/mathlab_harvest.py", "code/apps/mathlab/mathlab_admit.py"),
     "mathlab", "harvest", "Math-lab harvest", "code/apps/mathlab/run_mathlab_harvest.sh", None, "gpu"),
    (("code/lab/runners/run_c10z_v7_diag.py", "code/lab/track_c/c10z_v7_diag.py"),
     "c10z", "v7-diag", "C10Z V7 probe", "code/lab/runners/run_c10z_v7_diag.py", "experiments/c10z/runs/c10z_v7_diagnostic", "gpu"),
    (("code/lab/runners/run_c10y_precast_diag.sh", "code/lab/track_c/c10y_precast_diag.py"),
     "c10y", "pre-cast", "C10Y pre-cast", "code/lab/runners/run_c10y_precast_diag.sh", "experiments/c10y/runs/c10y_precast_diag", "gpu"),
    (("code/lab/track_c/c10z_astra_benchmark.py",),
     "c10z", "benchmark", "C10Z benchmark", "code/lab/track_c/c10z_astra_benchmark.py", None, "gpu"),
    (("code/lab/runners/run_c10z_attempt.sh", "code/lab/runners/run_c10z_stage.sh", "code/lab/track_c/c10z_astra_arms.py"),
     "c10z", "astra", "C10Z ASTRA attempt", None, None, "gpu"),
    (("code/apps/mathlab/run_mathlab_cpu.sh", "code/apps/mathlab/mathlab_cpu_runner.py", "code/apps/mathlab/mathlab_admit.py",
      "code/apps/mathlab/m2_solve_repro.py", "code/apps/mathlab/m3_calibration.py"),
     "mathlab", "cpu", None, "code/apps/mathlab/run_mathlab_cpu.sh", None, "cpu"),
)
SHORT = {"c10u": "Step 3", "c10v": "Step 4", "c10w": "Step 5", "c10x": "Step 6", "c10y": "Step 7", "c10z": "ASTRA", "mathlab": "Math lab"}
NOT_TEAM = {"dashboard", "dashboard_new", "helpers"}
ROW = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*([^|]*)\|")


def elapsed_seconds(etime):
    days, clock = etime.split("-", 1) if "-" in etime else ("0", etime)
    parts = [int(p) for p in clock.split(":")]
    return int(days) * 86400 + sum(n * 60 ** i for i, n in enumerate(reversed(parts)))


def job_options(args):
    options = {}
    for i, arg in enumerate(args):
        if not arg.startswith('--'):
            continue
        name, equals, value = arg[2:].partition('=')
        if equals:
            options[name] = value
        elif i + 1 < len(args) and not args[i + 1].startswith('--'):
            options[name] = args[i + 1]
    return options


def detect_gpu_jobs(inventory):
    """Classify GPU and CPU jobs from one ps snapshot; only verified ancestry joins rows."""
    processes, jobs = {}, []
    for line in inventory.splitlines():
        row = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d:-]+)\s+(.+)$", line)
        if not row:
            continue
        pid, parent, etime, command = row.groups()
        try: elapsed = elapsed_seconds(etime)
        except ValueError: continue
        processes[pid] = parent
        call = script_call(command)
        if not call:
            continue
        args, env = call; script = os.path.normpath(args[0]); options = job_options(args[1:])
        if any(flag in args[1:] for flag in ('--selftest', '--help', '-h')):
            continue
        job = None
        for aliases, key, stage, name, cap_file, output_base, device in JOB_TYPES:
            rel = next((r for r in aliases if script == r or script.endswith("/" + r)), None)
            if rel is None or (rel == "code/apps/mathlab/mathlab_admit.py" and options.get("kind") != ('cpu' if device == 'cpu' else 'harvest')):
                continue
            step = None
            if device == 'cpu':
                # The notebooks and their runners share code/apps/mathlab/ in v2, so the folder no longer says which
                # alias is the notebook itself; the notebook's own name does.
                notebook = rel if re.search(r'(?:^|/)m[23]_\w+\.py$', rel) else (args[1] if len(args) > 1 else '')
                match = re.search(r'(?:^|/)code/apps/mathlab/m([23])_\w+\.py$', notebook)
                step = options.get('step') if rel == 'code/apps/mathlab/mathlab_admit.py' else match.group(1) if match else None
                if step not in ('2', '3'): continue
                step = int(step); stage = 'm' + str(step); name = 'Math-lab step ' + str(step)
            root = script[:-len(rel)].rstrip("/") if os.path.isabs(script) else ROOT
            run = options.get("run-dir")
            run = os.path.normpath(os.path.join(root, run)) if run else None
            utc = options.get("utc", "")
            output = os.path.join(root, output_base, utc) if output_base and re.fullmatch(r"\d{8}T\d{6}(?:\.\d{6})?Z", utc) else None
            if stage == 'benchmark': output = options.get('out')
            if stage == 'astra': output = env.get('C10Z_OUT_DIR')
            output = os.path.normpath(os.path.join(root, output)) if output else None
            job = dict(key=key, stage=stage, name=name, root=root, run_dir=run, output_dir=output,
                       cap_file=os.path.join(root, cap_file) if cap_file else None, job_label=None, named=True,
                       device=device, family=stage, step=step, go_path=env.get('C10Z_GO_RECORD'))
            break
        if job is None:
            m = GPU_JOB_RE.fullmatch(script)
            if not m:
                continue
            key = m.group(1)
            stage = args[1] if len(args) > 1 and re.fullmatch(r'[\w-]+', args[1]) and not args[1].startswith('-') else 'between stages'
            if script.endswith('.py') and stage == 'between stages':
                continue
            label = None
            if stage == "_job":
                label = (f"{options.get('job', '?')}_{options.get('block', '?')}_r{options.get('replicate', 0)}_"
                         f"{options.get('kind', '?')}_s{options.get('seed', 'none')}")
            job = dict(key=key, stage=stage, name=SHORT.get(key, key), root=ROOT, run_dir=None,
                       output_dir=None, cap_file=None, job_label=label, named=False, device='gpu', family='legacy', go_path=None)
        job.update(pid=pid, parent=parent, etime=etime, elapsed_s=elapsed, process_verified=True)
        jobs.append(job)

    def ancestor(pid, child):
        seen = set()
        while child in processes and child not in seen:
            if child == pid:
                return True
            seen.add(child); child = processes[child]
        return False

    grouped = {}
    for job in jobs:
        related = [j for j in jobs if j['key'] == job['key'] and j['family'] == job['family'] and j['root'] == job['root'] and
                   (ancestor(job['pid'], j['pid']) or ancestor(j['pid'], job['pid']))]
        for field in ('run_dir', 'output_dir', 'go_path'):
            job[field] = job[field] or next((j[field] for j in related if j[field]), None)
        owner = next((j['pid'] for j in related if all(not ancestor(k['pid'], j['pid']) for k in related if k is not j)), job['pid'])
        identity = (job['key'], job['family'], job['root'], owner, job['output_dir'] or job['run_dir'])
        if identity not in grouped:
            grouped[identity] = dict(job, pids=[], pid_ages={})
        group = grouped[identity]; group['pids'].append(job['pid'])
        group['pid_ages'][job['pid']] = job['elapsed_s']
        if job['elapsed_s'] > group['elapsed_s']:
            group['etime'], group['elapsed_s'] = job['etime'], job['elapsed_s']
        if group['stage'] == '_job' and job['stage'] != '_job':
            group['stage'] = job['stage']
        group['job_label'] = group['job_label'] or job['job_label']
    return list(grouped.values()), bool(processes)


def job_cap(job):
    if not job['cap_file']:
        return None
    try:
        with open(job['cap_file']) as source:
            text = source.read()
    except OSError:
        return None
    if job['device'] == 'cpu': pattern = r'\bmathlab/m' + str(job['step']) + r'_\w+\.py:(\d+)\b'
    elif job['family'] == 'benchmark': pattern = r'def supervise\([^\n]*\bcap_s\s*=\s*(\d+(?:\.\d*)?)'
    else: pattern = r"--deadline-s\s+(\d+)" if job['key'] == 'mathlab' else r"(?m)^CAP_SECONDS\s*=\s*(\d+)\b"
    match = re.search(pattern, text)
    number = float(match.group(1)) if match else 0
    return int(number) if number > 0 and number.is_integer() else number if number > 0 else None


def record_object(path):
    try:
        with open(path) as source: value = json.load(source)
        return value if isinstance(value, dict) else None
    except (OSError, ValueError):
        return None   # callers display unavailable when the observation cannot be read


def attempt_budget(job):
    """A PID/age-bound snapshot describes recorded scopes, not a guarantee of the current phase."""
    job['selected_caps'] = {}; job['budget_note'] = 'Current budget unavailable'
    now = time.monotonic()
    def bound(record):
        if not record or not isinstance(record.get('origins'), dict) or not isinstance(record.get('launch'), dict):
            return False
        if not isinstance(record['launch'].get('go'), dict): return False
        origins = record['origins']
        origin = origins.get('stage01')
        age = job.get('pid_ages', {}).get(str(record.get('pid')))
        return bool(record and record.get('closed') is False and str(record.get('pid')) in job['pids'] and
                    type(origin) in (int, float) and math.isfinite(origin) and
                    age is not None and 0 <= now - origin <= age + 5)
    path = job['output_dir']
    if path:
        matches = [(path, record_object(os.path.join(path, 'run.json'))),
                   (os.path.join(path, 'process2'), record_object(os.path.join(path, 'process2/run.json')))]
        matches = [(p, r) for p, r in matches if bound(r)]
        record = matches[0][1] if len(matches) == 1 else None
        if record: job['output_dir'] = matches[0][0]
    else:
        paths = [p for pattern in ('experiments/c10z/runs/c10z_astra*/run.json', 'experiments/c10z/runs/c10z_astra*/process2/run.json')
                 for p in glob.glob(os.path.join(job['root'], pattern))]
        matches = [(os.path.dirname(p), r) for p in paths
                   for r in [record_object(p)] if bound(r)]
        record = matches[0][1] if len(matches) == 1 else None
        if record: job['output_dir'] = matches[0][0]
    go = record['launch']['go'] if record else record_object(os.path.join(job['root'], job['go_path'])) if job['go_path'] else None
    caps = record.get('ceilings') if record else go.get('ceilings') if go else None
    if not isinstance(caps, dict) or not all(caps.get(k) is None or type(caps.get(k)) in (int, float) and math.isfinite(caps[k]) and caps[k] > 0 for k in ('stage01', 'stage2', 'stage3')):
        return
    job['selected_caps'] = {k: v for k, v in caps.items() if k in ('stage01', 'stage2', 'stage3') and v is not None}
    if job['output_dir'] and 'c10z_astra_attempt4' in job['output_dir'].split(os.sep): job['name'] = 'C10Z attempt 4'
    if not record: return
    origins = record['origins']; process = record.get('process')
    if process not in (1, 2) or record.get('requested') == 2 and 'stage2' not in origins: return
    scopes = ['stage2' if 'stage2' in origins else 'stage01'] + (['stage3'] if process == 2 else [])
    if not all(k in job['selected_caps'] and type(origins.get(k)) in (int, float) and math.isfinite(origins[k]) and origins[k] <= now for k in scopes): return
    scope = min(scopes, key=lambda k: origins[k] + caps[k])
    job['budget_scope'] = scope; job['cap_s'] = caps[scope]
    job['elapsed_s'] = now - origins[scope]; job['etime'] = elapsed_text(job['elapsed_s'])
    job['budget_note'] = 'Recorded budget ' + scope + '; current phase may have advanced'


def elapsed_text(seconds):
    seconds = max(int(seconds), 0); minutes, seconds = divmod(seconds, 60)
    return f'{minutes}:{seconds:02d}' if minutes < 60 else f'{minutes // 60}:{minutes % 60:02d}:{seconds:02d}'


def recorded_cpu_jobs():
    """Validated fresh samples establish recorded activity; their event PID is not process liveness."""
    from apps.mathlab.mathlab_events import read_events, fold
    jobs, errors = [], []; now = time.time()
    for path in map(str, L.lab_event_streams(ROOT)):
        events, problems = read_events(path)
        if problems:
            errors += problems; continue
        state = fold(events); resource = state['resources']
        cpu = any(e['type'] == 'gate_result' and e['gate_id'] == 'admission' and
                  isinstance(e['observed'], dict) and e['observed'].get('kind') == 'cpu' and
                  e['observed'].get('allowed') is True for e in events)
        if not (cpu and state['purpose'] == 'experiment' and state['step'] in (2, 3) and
                state['status'] == 'running' and state['admission'] and state['admission']['allowed'] and resource): continue
        start, deadline, sample = (datetime.fromisoformat(v.replace('Z', '+00:00')).timestamp()
                                   for v in (state['started_ts'], state['deadline_ts'], resource['ts']))
        if not (start <= sample <= now < deadline and 0 <= now - sample <= 30): continue
        step = state['step']
        jobs.append(dict(key='mathlab', family='m' + str(step), device='cpu', stage='m' + str(step),
                         step=step, name='Math-lab step ' + str(step), root=ROOT, run_dir=os.path.dirname(path),
                         output_dir=None, cap_s=round(deadline - start), etime=elapsed_text(now - start),
                         elapsed_s=now - start, pids=[], recorded_pid=state['pid'], process_verified=False,
                         sample_ts=resource['ts'], named=True, job_label=None))
    return jobs, errors


def job_path(job, field):
    path = job.get(field)
    return os.path.relpath(path, job['root']) if path else 'unavailable'


def job_summary(job):
    cap = f"{job['cap_s']:g}s" if job['cap_s'] is not None else 'cap unavailable'
    text = f"{job['name']} {job['etime']}/{cap} · output {job_path(job, 'output_dir')}"
    if job.get('device') == 'cpu':
        return f"{job['name']} {job['etime']}/{cap} · out ? · events {job_path(job, 'run_dir')}"
    if job.get('budget_scope'):
        text = f"{job['name']} recorded {job['budget_scope']} {job['etime']}/{cap} · output {job_path(job, 'output_dir')}"
    if job['key'] == 'mathlab':
        text += f" · events {job_path(job, 'run_dir')}"
    elif not job['named']:
        text = f"{job['name']} · stage {job['stage']} · {job['etime']}/{cap} · output {job_path(job, 'output_dir')}"
    return text


def gpu_summary(state):
    cpu = state.get('cpu_jobs', [])
    if state.get('unavailable'):
        gpu = 'GPU unavailable' + ('' if cpu else ': ' + state['unavailable'])
    else:
        gpu = 'GPU: ' + ('; '.join(job_summary(job) for job in state['jobs']) if state['jobs'] else 'idle')
    text = gpu + ''.join(' · CPU' + (' recorded' if not j['process_verified'] else '') + ': ' + job_summary(j) for j in cpu)
    return text + (' · CPU records unavailable' if state.get('cpu_record_errors') else '')


def awaiting_rulings(runbook_text):
    """Titles of decision-ledger rows whose status cell says they await the operator."""
    out = []
    for line in runbook_text.splitlines():
        m = ROW.match(line)
        if m and re.search(r"awaiting operator", m.group(2), re.I):
            out.append(m.group(1).strip())
    return out


def iso_epoch(stamp):
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S%z").timestamp()


def coordinator_exit(log_text):
    """The last COORDINATOR_EXIT line of a coordinator log as {code, reason, at}, or None while it runs."""
    hits = re.findall(r"^(\S+) COORDINATOR_EXIT=(\d+) ?(.*)$", log_text, re.M)
    if not hits:
        return None
    at, code, reason = hits[-1]
    return {"code": int(code), "reason": reason.strip(), "at": iso_epoch(at)}


def board_epoch(updated):
    """The scoreboard's 'updated' text ('2026-10-08 01:45 MDT', local time) as epoch seconds, or None."""
    try:
        return time.mktime(time.strptime(updated[:16], "%Y-%m-%d %H:%M"))
    except (TypeError, ValueError):
        return None


def newer_events(updated, events):
    """Names of (epoch, name) events after the report text was last updated, oldest first."""
    return [name for t, name in sorted(events) if updated is None or t > updated]


@functools.lru_cache(maxsize=256)
def source_imports(path, mtime_ns, size):
    """Static imports, including function-local imports, without executing any repo module."""
    with open(path, encoding="utf-8") as source:
        try:
            tree = ast.parse(source.read(), filename=path)
        except SyntaxError:
            return ()   # stamp the broken source too; re-exec exposes its syntax error
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((name.name, 0) for name in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append((module, node.level))
            imports.extend((".".join(filter(None, (module, name.name))), node.level)
                           for name in node.names if name.name != "*")
    return tuple(imports)


def source_stamp(directory):
    """Max mtime of dashboard scripts and their local import closure (packages included)."""
    directory = os.path.realpath(directory)
    # Dashboards live in code/apps/dashboard/; package imports (apps.mathlab, state, ops) resolve from code/.
    root = os.path.dirname(os.path.dirname(directory))
    pending = glob.glob(os.path.join(directory, "dashboard_*.py"))
    seen, stamp = set(), 0.0
    while pending:
        path = os.path.realpath(pending.pop())
        # join(root, "") ends in exactly one separator, also when root is "/" (a Linux temp dir).
        if path in seen or not path.startswith(os.path.join(root, "")):
            continue
        seen.add(path)
        stat = os.stat(path)
        stamp = max(stamp, stat.st_mtime)
        for module, level in source_imports(path, stat.st_mtime_ns, stat.st_size):
            if level:
                base = os.path.dirname(path)
                for _ in range(level - 1):
                    base = os.path.dirname(base)
                bases = (base,)
            else:
                bases = (directory, root)
            parts = module.split(".") if module else []
            for base in bases:
                for i in range(len(parts) + 1):
                    stem = os.path.join(base, *parts[:i])
                    candidates = (stem + ".py", os.path.join(stem, "__init__.py")) if i else (os.path.join(stem, "__init__.py"),)
                    pending.extend(p for p in candidates if os.path.isfile(p))
    return stamp


def sources_changed(directory, stamp):
    return source_stamp(directory) > stamp


def tiled_sessions(start_commands):
    return {m.group(1) for c in start_commands for m in [re.search(r"dashboard_tile\.py' '([^']+)'", c)] if m}


def team_sessions(names):
    return {n for n in names if n not in NOT_TEAM and not n.startswith("view-")}


Pane = collections.namedtuple("Pane", "session created command path start")
PANE_FORMAT = "#{session_name}\t#{session_created}\t#{pane_current_command}\t#{pane_current_path}\t#{pane_start_command}"
# Claude Code names its process after its version (seen: "2.1.295"); its start command, when tmux launched it, is `claude …`.
CLAUDE_COMMAND = re.compile(r"^(claude|\d+\.\d+\.\d+)$")
CLAUDE_START = re.compile(r'^"?(?:\S*/)?claude(?:[\s"]|$)')


def parse_panes(text):
    """`tmux list-panes -a -F PANE_FORMAT` output as Panes."""
    return [Pane(s, int(c), cmd, path, start) for s, c, cmd, path, start in (l.split("\t", 4) for l in text.splitlines() if l)]


def lead_session(override, panes, repo):
    """The lead Claude session's tmux name: `override` (the LEAD variable) when set; otherwise the newest team session
    that has a Claude Code pane working inside `repo` (the main checkout, so its worktrees count); None when none does.
    Names change with each orchestrator generation (program, maestro2, ...), so the name is found, never written down."""
    leads = [(p.created, p.session) for p in panes
             if team_sessions([p.session]) and (CLAUDE_COMMAND.match(p.command) or CLAUDE_START.match(p.start))
             and (p.path == repo or p.path.startswith(repo + "/"))]
    return override or max(leads, default=(0, None))[1]


class TeamSupervisor:
    """Says when to rebuild the team tab: the session set must differ from the tiles and stay the same for
    debounce_s, and rebuilds are at least min_gap_s apart."""

    def __init__(self, debounce_s=10, min_gap_s=30):
        self.debounce_s, self.min_gap_s = debounce_s, min_gap_s
        self.pending, self.since, self.last = None, None, None

    def should_rebuild(self, tiled, current, now):
        if tiled == current:
            self.pending = None
            return False
        if self.pending != current:
            self.pending, self.since = current, now
            return False
        if now - self.since < self.debounce_s or (self.last is not None and now - self.last < self.min_gap_s):
            return False
        self.last = now
        return True


ASKING = re.compile(r"Hooks need review|enter confirm|Do you want|\[y/n\]|\(y/n\)|Allow this|approve", re.I)
ERROR = re.compile(r"Traceback \(most recent call last\)|\bError:|Operation not permitted|\bBLOCKED\b|permission denied|^\s*(?:[└⎿•⏺]\s*)?FAILED\b", re.I | re.M)
REPLY_TOKEN = re.compile(r"^\s*(?:[•⏺]\s*)?[A-Z][A-Z0-9_-]*(?:[ \t]+[A-Z0-9_-]+)*\s*$")
FINISH_WORD = re.compile(r"(?:^|[ _-])(?:READY|DONE)(?:[ _-]|$)")
STALL_S = 15 * 60


def session_alerts(screens, memory, now):
    """Plain alerts for team sessions: waiting for an answer, no new step for STALL_S while working, or stopped after an
    error. `memory` keeps each session's step list and when it last changed, across calls."""
    out = []
    for name, screen in sorted(screens.items()):
        lines = [l for l in screen.splitlines() if l.strip()]
        tail = "\n".join(lines[-15:])
        errors = [i for i, line in enumerate(lines[-15:]) if ERROR.search(line)]
        finishes = [i for i, line in enumerate(lines[-15:])
                    if REPLY_TOKEN.fullmatch(line) and FINISH_WORD.search(line.strip())]
        clean_finish = bool(finishes and (not errors or finishes[-1] > errors[-1]))
        working = bool(BUSY_RE.search(screen))
        steps = tuple(l.strip() for l in lines if l.lstrip()[:1] in "•⏺" and "Working (" not in l)
        seen = memory.get(name)
        if seen is None or seen[0] != steps:
            memory[name] = (steps, now)
        since = memory[name][1]
        if ASKING.search(tail):
            out.append(f"{name} is waiting for an answer")
        elif working and now - since >= STALL_S:
            out.append(f"{name} shows no new step for {int((now - since) // 60)} min")
        elif not working and errors and not clean_finish:
            out.append(f"{name} stopped after an error")
    return out


def ago(seconds):
    s = int(max(seconds, 0))
    return f"{s // 60}m ago" if s < 3600 else f"{s // 3600}h{s % 3600 // 60:02d}m ago"


def now_lines(state, now):
    """Plain lines for the report's NOW section, most urgent first."""
    lines = [f"! NEEDS YOUR RULING: {r}" for r in state["rulings"]]
    lines += [f"▲ STALLED/BLOCKED: {a} (the program is on it)" for a in state.get("alerts", [])]
    gpu = state["gpu"]
    if gpu.get("unavailable"):
        lines.append(f"! GPU unavailable: {gpu['unavailable']}")
    elif gpu.get("jobs"):
        lines += [f"▸ GPU running: {job_summary(job)}" for job in gpu['jobs']]
    elif gpu["running"]:
        key, stage, etime = gpu["running"]
        lines.append(f"▸ GPU running: {SHORT.get(key, key)} · stage {stage} · {etime}")
    else:
        last, ex = "", gpu["last_exit"]
        if ex:
            what = "finished" if ex["code"] == 0 else f"stopped (exit {ex['code']}: {ex['reason']})"
            last = f" · last: {gpu['last_name'] or 'a'} coordinator {what} · {ago(now - ex['at'])}"
        elif gpu.get("last_log"):
            last = f" · last: {gpu['last_name'] or 'experiment'} log · {ago(now - gpu['last_at'])} · outcome not recorded"
        lines.append(f"· GPU idle{last}")
    lines += [f"▸ CPU {'running' if job['process_verified'] else 'recorded (process unverified)'}: {job_summary(job)}"
              for job in gpu.get('cpu_jobs', [])]
    if gpu.get('cpu_record_errors'):
        lines.append('! CPU records unavailable: ' + gpu['cpu_record_errors'][0])
    lines += [f"» {label}: {task}" for label, task in state["builds"]]
    lines += [f"◦ helper: {h}" for h in state["helpers"]]
    return lines


# ---- effects: reading the machine ------------------------------------------------------------------------------

def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def is_experiment_log(path, root):
    parts = os.path.relpath(path, root).split(os.sep)
    archived = any(x.startswith(("_quarantine", "attempt")) for x in parts)
    # v2: experiment logs live only under experiments/; mirrors (the LabViz site under projects/) are elsewhere.
    return parts[0] == "experiments" and not archived and any(x.startswith("c10") for x in parts[1:])


def experiment_logs(root):
    """One newest-run source for the Experiment tab and the report's GPU last-run line."""
    return sorted((p for p in glob.glob(os.path.join(root, "experiments", "**", "*.log"), recursive=True)
                   if is_experiment_log(p, root)), key=os.path.getmtime)


def gpu_state():
    recorded, errors = recorded_cpu_jobs()
    state = {"running": None, "jobs": [], "cpu_jobs": recorded, "cpu_record_errors": errors,
             "last_exit": None, "last_name": None}
    try:
        result = subprocess.run(("/bin/ps", "-axo", "pid=,ppid=,etime=,command="), capture_output=True, text=True)
    except OSError as error:
        return dict(state, unavailable=str(error))
    if result.returncode != 0 or not result.stdout.strip():
        reason = f"ps exit {result.returncode}: {result.stderr.strip()}" if result.returncode else "empty ps inventory"
        return dict(state, unavailable=reason)
    detected, valid = detect_gpu_jobs(result.stdout)
    if not valid:
        return dict(state, unavailable="malformed ps inventory")
    for job in detected:
        job['cap_s'] = job_cap(job)
        if job['family'] == 'astra': attempt_budget(job)
    jobs = [job for job in detected if job['device'] == 'gpu']
    cpu = [job for job in detected if job['device'] == 'cpu']
    for record in recorded:
        matched = next((job for job in cpu if job['run_dir'] == record['run_dir']), None)
        if matched:
            matched['sample_ts'], matched['recorded_pid'] = record['sample_ts'], record['recorded_pid']
        else:
            cpu.append(record)
    top = next((job for job in jobs if job['stage'] != '_job'), jobs[0] if jobs else None)
    running = (top['key'], top['stage'], top['etime']) if top else None
    logs = experiment_logs(ROOT)
    last_log = logs[-1] if logs else None
    if last_log:
        with open(last_log, errors="replace") as source:
            last_exit = coordinator_exit(source.read())
    else:
        last_exit = None
    key = re.search(r"(?:^|/)(c10[a-z])", os.path.relpath(last_log, ROOT)) if last_log else None
    return dict(state, running=running, jobs=jobs, cpu_jobs=cpu, last_exit=last_exit,
                last_name=SHORT.get(key.group(1)) if key else None,
                last_log=last_log, last_at=os.path.getmtime(last_log) if last_log else None)


SCREEN_TTL_S = 15
_screens = {"at": 0.0, "screens": {}, "titles": {}, "lead": None}


@functools.lru_cache(maxsize=None)
def repo_root():
    """The main checkout of this repo (its worktrees live inside it), as git reports it."""
    common = subprocess.run(["git", "-C", TOOLS, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            stdout=subprocess.PIPE, text=True, check=True).stdout.strip()
    return os.path.dirname(common)


def read_lead():
    """lead_session() over the live tmux panes; LEAD in the environment overrides. A failed tmux or git read raises."""
    panes = subprocess.run(["tmux", "list-panes", "-a", "-F", PANE_FORMAT], stdout=subprocess.PIPE, text=True, check=True).stdout
    return lead_session(os.environ.get("LEAD", ""), parse_panes(panes), repo_root())


def team_screens():
    """Screens and pane titles of the team sessions, and the lead session's name, read from tmux at most every
    SCREEN_TTL_S seconds (tmux is shared by every session; a flood of reads helped hang its server on 2026-10-08)."""
    if time.time() - _screens["at"] >= SCREEN_TTL_S:
        names = team_sessions(sh("tmux", "list-sessions", "-F", "#{session_name}").split())
        _screens["screens"] = {n: sh("tmux", "capture-pane", "-p", "-t", n) for n in names}
        _screens["titles"] = {n: sh("tmux", "display", "-p", "-t", n, "#{pane_title}") for n in names if n.startswith("codex")}
        _screens["lead"] = read_lead()
        _screens["at"] = time.time()
    return _screens["screens"], _screens["titles"], _screens["lead"]


def build_state():
    from dashboard_active import label
    from dashboard_tile import status
    out = []
    screens, titles, _ = team_screens()
    for n, screen in sorted(screens.items()):
        if not n.startswith("codex"):
            continue
        if status(screen, None, time.time())[0] == "WORKING":
            title = titles.get(n, "").strip().split(" | ")[0]   # drop "| <worktree>"
            out.append((label(n), re.sub(r"^[^\w(]+", "", title) or "working"))                    # drop the spinner
    return out


def events():
    ev = []
    for p in glob.glob(os.path.join(ROOT, "experiments", "c10*", "runs", "*", "logs", "*coordinator*.log")):
        ex = coordinator_exit(open(p, errors="replace").read())
        if ex:
            ev.append((ex["at"], f"coordinator exit {ex['code']} ({os.path.basename(p)})"))
    for p in glob.glob(os.path.join(ROOT, "experiments", "c10*", "runs", "*", "*", "HALT.json")):
        ev.append((os.path.getmtime(p), f"HALT in {os.path.relpath(os.path.dirname(p), ROOT)}"))
    for p in glob.glob(os.path.join(ROOT, "evidence/CORPUS/[0-9][0-9]_*.md")):
        ev.append((os.path.getmtime(p), f"evidence/CORPUS/{os.path.basename(p)[:2]} changed"))
    return ev


def gather():
    from dashboard_tile import running_helpers
    try:
        runbook = L.read_split(os.path.join(ROOT, "program/runbook"))
    except OSError:
        runbook = ""
    screens, _, lead = team_screens()
    screens = {n: s for n, s in screens.items() if n != lead}   # the lead's own state is not an alert for the lead
    return {"rulings": awaiting_rulings(runbook), "alerts": session_alerts(screens, _alert_memory, time.time()),
            "gpu": gpu_state(), "builds": build_state(), "helpers": running_helpers()}


_alert_memory = {}


def maybe_reload(stamp):
    """Re-exec this pane's program when any dashboard source changed, so a code fix shows without a manual restart."""
    if sources_changed(TOOLS, stamp):
        os.execv(sys.executable, [sys.executable] + sys.argv)


_supervisor = TeamSupervisor()


def supervise_team():
    """Compatibility no-op: dashboard_team composes sessions without mutating tmux's layout."""


def cell_width(ch):
    """Terminal cells one character takes: wide characters (East Asian W/F, such as ✅) two, combining marks none,
    everything else one - tmux draws the ambiguous-width glyphs ━ ■ · — ┃ █ ░ in a single cell (measured 2026-10-10)."""
    return 0 if unicodedata.combining(ch) else 2 if unicodedata.east_asian_width(ch) in "WF" else 1


def cells(text):
    """Terminal cells a line takes on screen, ANSI codes excluded."""
    return sum(cell_width(ch) for ch in re.sub(r"\033\[[0-9;]*[A-Za-z]", "", text))


def clip(line, width):
    """A line cut to `width` terminal cells (ANSI codes kept, not counted), so a pane never wraps or scrolls. Codes
    after the cut are kept too, so a trailing reset still ends the line's colours."""
    out, seen, full = [], 0, False
    for token in re.findall(r"\033\[[0-9;]*[A-Za-z]|.", line, re.S):
        if token.startswith("\033"):
            out.append(token)
        elif not full and seen + cell_width(token) <= width:
            out.append(token)
            seen += cell_width(token)
        else:
            full = True   # the first character that does not fit ends the text; a narrower one after it stays cut
    return "".join(out)


if __name__ == '__main__' and sys.argv[1:] == ['--gpu-summary']:
    print(gpu_summary(gpu_state()))
if __name__ == '__main__' and sys.argv[1:] == ['--lead']:   # for team_dashboard.sh: the name, or nothing when none is found
    print(read_lead() or "")
