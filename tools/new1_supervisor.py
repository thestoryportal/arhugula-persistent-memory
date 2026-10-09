#!/usr/bin/env python3
"""NEW1 CPU enforcement. Stdlib only; never runs the geometry without freeze."""
import argparse
import contextlib
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import selectors
import signal
import socket
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.mathlab_events import emit

DEADLINE_S = 1800
WAIT_S = 300
SAMPLE_S = 1.
RSS_CAP_GIB = 6.
FLOOR_GIB = 6.
RESERVES = {'imports': 1., 'load': 2., 'covariance-svd': 5., 'covariance-checks': 2.,
            'update-svd': 2., 'projections': 2., 'random-controls': 1., 'output': 1.}
TIER = 'MATH-PROXY'
BOUNDARY = 'math estimate, not evidence'


class Stop(RuntimeError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


@dataclass(frozen=True)
class Sample:
    avail_gib: float
    rss_gib: float
    cpu_pct: float


def strict_json(text):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value: raise ValueError('duplicate key: ' + key)
            value[key] = item
        return value
    def bad(value): raise ValueError('nonfinite JSON: ' + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=bad)


def sha_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(4 << 20), b''): digest.update(block)
    return digest.hexdigest()


def verify_prereg(path, expected_sha):
    """The hash binds all bytes; only the first status paragraph declares freeze."""
    data=Path(path).read_bytes()
    lines=[line.strip() for line in data.decode('utf-8').splitlines() if line.strip()]
    if (hashlib.sha256(data).hexdigest()!=expected_sha or len(lines)<2 or
            not lines[0].startswith('# NEW-1 — ') or
            not lines[1].startswith('**FROZEN v2 · ') or '(D-NEW1-1;' not in lines[1]):
        raise Stop('INVALID-PREREG','NEW1 requires its hash-pinned authoritative FROZEN v2 status')


def durable_json(path, value):
    """Fresh artifact, fsynced file and containing directory before any event."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as out:
        out.write(data); out.flush(); os.fsync(out.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest()}


def receipt(run_dir, label, data):
    return durable_json(Path(run_dir)/'receipts'/(label + '_' + uuid.uuid4().hex + '.json'),
                        {'tier': TIER, 'boundary': BOUNDARY, **data})


@contextlib.contextmanager
def hard_deadline(seconds, heartbeat=None, budget=None):
    """Periodic enforcement interrupts blocked IO; nested probes retain the deadline."""
    previous = signal.getsignal(signal.SIGALRM)
    if signal.getitimer(signal.ITIMER_REAL)[0]:
        raise Stop('INVALID-ENFORCEMENT', 'a pre-existing alarm cannot be replaced')
    deadline=time.monotonic()+seconds
    busy=False
    def remaining_time():
        remaining=deadline-time.monotonic()
        if remaining<=0: raise Stop('STOPPED-DEADLINE','whole-run wall-clock cap reached')
        return min(remaining,budget()) if budget is not None else remaining
    def expired(signum, frame):
        nonlocal busy
        remaining=remaining_time()
        if heartbeat is None:
            raise Stop('STOPPED-DEADLINE', 'whole-run wall-clock cap reached')
        if busy: raise Stop('INVALID-MONITORING','recursive resource watchdog')
        busy=True
        # A probe callback is independently interrupted at the original deadline.
        signal.setitimer(signal.ITIMER_REAL,remaining)
        try: heartbeat()
        finally: busy=False
        remaining=remaining_time()
        signal.setitimer(signal.ITIMER_REAL,min(SAMPLE_S,remaining))
    signal.signal(signal.SIGALRM, expired)
    try:
        remaining=remaining_time()
        signal.setitimer(signal.ITIMER_REAL,min(SAMPLE_S,remaining) if heartbeat else remaining)
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def sample_resources(pid=None):
    """Successful complete inventories only; missing values never become zero."""
    from tools.mathlab_runtime import vm_available_gib
    try:
        vm = subprocess.run(['/usr/bin/vm_stat'], capture_output=True, text=True, timeout=1)
        if vm.returncode or not vm.stdout.strip(): raise ValueError(vm.stderr or 'empty vm_stat')
        available = vm_available_gib(vm.stdout)
        inventory = subprocess.run(['/bin/ps', '-axo', 'pid=,ppid=,pgid=,rss=,%cpu='],
                                   capture_output=True, text=True, timeout=1)
        if inventory.returncode or not inventory.stdout.strip():
            raise ValueError(inventory.stderr or 'empty process inventory')
        rows = {}
        for line in inventory.stdout.splitlines():
            fields = line.split()
            if len(fields) != 5: raise ValueError('malformed process inventory')
            process, parent, group, rss, cpu = int(fields[0]), int(fields[1]), int(fields[2]), int(fields[3]), float(fields[4])
            if process <= 0 or parent < 0 or group < 0 or rss < 0 or not math.isfinite(cpu) or cpu < 0 or process in rows:
                raise ValueError('invalid or duplicate process row')
            rows[process] = (parent, group, rss, cpu)
        target = pid if pid is not None else os.getpid()
        if target not in rows: raise ValueError('worker/supervisor absent from inventory')
        if pid is not None and rows[target][1]!=target:
            raise ValueError('worker is not its isolated process-group leader')
        family = {target} | ({p for p,(_,group,_,_) in rows.items() if group==target} if pid is not None else set())
        while True:
            larger = family | {p for p, (parent, _, _, _) in rows.items() if parent in family}
            if larger == family: break
            family = larger
        rss = sum(rows[p][2] for p in family) / (1 << 20)
        cpu = sum(rows[p][3] for p in family)
        return Sample(available, rss if pid is not None else 0., cpu)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise Stop('INVALID-MONITORING', str(error)) from error


def cpu_admission(run_dir, lead_path=None):
    from tools import mathlab_admit as A, mathlab_runtime as R
    R.enforce_stop_policy(ROOT, 4, exclude=run_dir)
    lead = strict_json(Path(lead_path).read_text()) if lead_path else None
    return A.probe('cpu', lead)


class Controller:
    def __init__(self, run_dir, *, clock=time.monotonic, sleep=time.sleep, monitor=sample_resources):
        self.run_dir, self.clock, self.sleep, self.monitor = Path(run_dir), clock, sleep, monitor
        self.start = clock()
        self.cell_deadline = None

    def remaining(self):
        value = DEADLINE_S - (self.clock() - self.start)
        if value <= 0: raise Stop('STOPPED-DEADLINE', 'unchanged whole-run deadline reached')
        if self.cell_deadline is not None:
            cell_remaining=self.cell_deadline-self.clock()
            if cell_remaining<=0: raise Stop('STOPPED-RESOURCE','cell reserve not admitted within 300 s')
            value=min(value,cell_remaining)
        return value

    def observe(self, pid=None):
        self.remaining()
        try:
            sample = self.monitor(pid)
            if not isinstance(sample, Sample) or not all(type(v) in (int,float) and math.isfinite(v) and v >= 0
                                                         for v in asdict(sample).values()):
                raise ValueError('invalid/nonfinite resource sample')
        except Stop: raise
        except (OSError, ValueError, TypeError) as error:
            raise Stop('INVALID-MONITORING', str(error)) from error
        self.remaining()
        # Stop computation before potentially blocking durability work on a breach.
        if sample.rss_gib > RSS_CAP_GIB or sample.avail_gib < FLOOR_GIB:
            error=Stop('STOPPED-RESOURCE', 'observed RSS >6 GiB or available memory <6 GiB')
            error.observed=asdict(sample)
            raise error
        return sample

    def check(self, pid=None):
        sample=self.observe(pid)
        receipt(self.run_dir, 'resource', asdict(sample))
        self.remaining()
        emit(self.run_dir, 'resource_sample', **asdict(sample), floor_gib=FLOOR_GIB)
        return sample

    def wait_cell(self, phase, cell_id, pid):
        if phase not in RESERVES or not isinstance(cell_id,str) or not cell_id:
            raise Stop('INVALID-PROTOCOL', 'unknown or missing heavy cell')
        required = 8 + RESERVES[phase]
        self.cell_deadline = self.clock()+WAIT_S
        try:
            while True:
                sample = self.check(pid)
                if sample.avail_gib >= required:
                    proof = receipt(self.run_dir, 'cell', {'phase':phase, 'cell':cell_id,
                        'reserve_gib':RESERVES[phase], 'required_gib':required, 'available_gib':sample.avail_gib})
                    self.remaining()
                    emit(self.run_dir, 'gate_result', gate_id='memory-new1-' + phase + '-' + cell_id,
                         plain_words='Available memory covers eight GiB plus the declared cell reserve',
                         observed={'available_gib':sample.avail_gib, 'receipt':proof}, bar=required,
                         comparison='>=', passed=True)
                    self.remaining()
                    return sample
                self.sleep(min(SAMPLE_S,self.remaining()))
        finally:
            self.cell_deadline = None

    def handle_cell(self, message, pid):
        if set(message) != {'phase','cell'}:
            raise Stop('INVALID-PROTOCOL', 'worker cannot declare a reserve or unknown fields')
        return self.wait_cell(message['phase'], message['cell'], pid)


def terminate(process):
    """Stop the whole isolated group immediately, then reap the direct worker."""
    try: os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError: pass
    process.wait(timeout=5)


def publish_predictions(run_dir, path):
    data = strict_json(Path(path).read_text())
    if data.get('tier') != TIER or data.get('boundary') != BOUNDARY:
        raise Stop('INVALID-WORKER', 'missing MATH-PROXY boundary')
    predictions = data.get('predictions', {})
    if set(predictions) != {'H-COV','H-TOP','H-RANK','H-OVERLAP'} or any(
            value not in ('PASS','FAIL','INVALID') for value in predictions.values()):
        raise Stop('INVALID-WORKER', 'missing primary outcomes')
    proof = receipt(run_dir, 'predictions', {'source':str(path), 'sha256':sha_file(path), 'predictions':predictions})
    for name, outcome in predictions.items():
        emit(run_dir, 'stage_started', stage=name, plain_words='Provisional math estimate, not evidence: '+name, cap_s=DEADLINE_S)
        if outcome != 'INVALID':
            emit(run_dir, 'gate_result', gate_id=name, plain_words='Individual frozen geometry prediction',
                 observed={'outcome':outcome, 'receipt':proof, 'provisional':True}, bar='registered same-layer 3/5 rule',
                 comparison='meets', passed=outcome=='PASS')
        emit(run_dir, 'stage_finished', stage=name, outcome=outcome,
             summary=BOUNDARY + '; provisional individual prediction ' + outcome)
    return predictions


def supervise(command, run_dir, *, admission=None, monitor=sample_resources):
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    if (run_dir/'events.jsonl').exists(): raise ValueError('NEW1 run namespace already used')
    controller = Controller(run_dir, monitor=monitor)
    process = None
    kill_sent = False
    parent, child = socket.socketpair()
    def heartbeat():
        nonlocal kill_sent
        try: controller.observe(process.pid if process is not None and process.poll() is None else None)
        except BaseException:
            if process is not None and not kill_sent:
                try:
                    os.killpg(process.pid,signal.SIGKILL)
                    kill_sent=True
                except ProcessLookupError: pass
            raise
    try:
        with hard_deadline(controller.remaining(),heartbeat=heartbeat,budget=controller.remaining):
            emit(run_dir, 'run_started', step=4, title='NEW1 adapter geometry — math estimate, not evidence',
                 deadline_ts=(datetime.now(timezone.utc)+timedelta(seconds=controller.remaining())).isoformat(),
                 pid=os.getpid(), purpose='experiment')
            controller.check()
            result = (admission or (lambda:cpu_admission(run_dir)))()
            proof = receipt(run_dir, 'admission', {'decision':result})
            allowed = isinstance(result,dict) and result.get('allowed') is True
            emit(run_dir,'admission',allowed=allowed,reasons=result.get('reasons',[]) if isinstance(result,dict) else ['invalid admission'])
            emit(run_dir,'gate_result',gate_id='admission',plain_words='Fail-closed parent CPU admission',
                 observed=proof,bar='allowed',comparison='meets',passed=allowed)
            if not allowed: raise Stop('INVALID-ADMISSION', 'parent CPU admission refused')
            emit(run_dir,'stage_started',stage='geometry',plain_words='Offline update geometry: '+BOUNDARY,cap_s=DEADLINE_S)
            controller.remaining()
            env = dict(os.environ, NEW1_CONTROL_FD=str(child.fileno()), NEW1_SUPERVISOR_PID=str(os.getpid()),
                       LLMDB_DEVICE='cpu', CUDA_VISIBLE_DEVICES='', OMP_NUM_THREADS='8', MKL_NUM_THREADS='8',
                       PYTHONDONTWRITEBYTECODE='1')
            with (run_dir/'worker_stdout.log').open('xb') as stdout, (run_dir/'worker_stderr.log').open('xb') as stderr:
                process = subprocess.Popen(command, cwd=ROOT, env=env, start_new_session=True,
                    pass_fds=(child.fileno(),), stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
                child.close(); parent.setblocking(False)
                with selectors.DefaultSelector() as selector:
                    selector.register(parent,selectors.EVENT_READ)
                    buffer = b''; hello = False; complete = None; eof = False; last_sample = -math.inf
                    worker_exited = False
                    while True:
                        remaining = controller.remaining()
                        if process.poll() is not None and not worker_exited:
                            # Reparented group members may retain IPC after their leader exits.
                            terminate(process); worker_exited=True; kill_sent=True
                        if time.monotonic()-last_sample >= SAMPLE_S and not worker_exited:
                            controller.check(process.pid); last_sample=time.monotonic()
                        ready=selector.select(min(.1,remaining)) if not eof else []
                        if ready:
                            chunk=parent.recv(65536)
                            if not chunk:
                                eof=True; selector.unregister(parent)
                            buffer += chunk
                            if len(buffer) > 1 << 20: raise Stop('INVALID-PROTOCOL','oversized IPC frame')
                            while b'\n' in buffer:
                                raw,buffer=buffer.split(b'\n',1)
                                message=strict_json(raw)
                                if not isinstance(message,dict): raise Stop('INVALID-PROTOCOL','IPC object required')
                                kind=message.pop('type',None)
                                if complete is not None: raise Stop('INVALID-PROTOCOL','message after completion')
                                if kind=='hello' and not hello and message=={'pid':process.pid}:
                                    hello=True
                                    parent.sendall((json.dumps({'ok':True,'supervisor_pid':os.getpid()})+'\n').encode())
                                elif kind=='cell' and hello:
                                    controller.handle_cell(message,process.pid)
                                    parent.sendall(b'{"ok":true}\n')
                                elif kind in ('artifact','complete') and hello and set(message)=={'path'}:
                                    path=(run_dir/message['path']).resolve()
                                    if not path.is_relative_to(run_dir.resolve()) or path.suffix!='.json':
                                        raise Stop('INVALID-PROTOCOL','artifact outside the run directory')
                                    data=strict_json(path.read_text())
                                    if data.get('tier')!=TIER or data.get('boundary')!=BOUNDARY:
                                        raise Stop('INVALID-WORKER','artifact lacks proxy boundary')
                                    proof=receipt(run_dir,'artifact',{'source':str(path),'sha256':sha_file(path)})
                                    if kind=='complete': complete=path
                                    else:
                                        emit(run_dir,'progress',stage='geometry',done=len(list((run_dir/'layers').glob('*.json'))),
                                             total=5,unit='layers')
                                else: raise Stop('INVALID-PROTOCOL','unexpected IPC message/order')
                        if process.poll() is not None and eof:
                            if buffer or process.returncode or complete is None:
                                raise Stop('INVALID-WORKER','partial IPC, unsuccessful exit or missing final artifact')
                            if not kill_sent:
                                terminate(process); worker_exited=True; kill_sent=True
                            break
                        if eof: time.sleep(min(.05,controller.remaining()))
            predictions=publish_predictions(run_dir,complete)
            controller.remaining()
            emit(run_dir,'stage_finished',stage='geometry',outcome='PASS',summary='Arithmetic worker exited successfully; '+BOUNDARY)
            finding=durable_json(run_dir/'finding.json',{'tier':TIER,'boundary':BOUNDARY,
                'source':str(complete),'predictions':predictions,'queue_action':'NONE — calibration/utility gated'})
            emit(run_dir,'finding_staged',finding_id='NEW1',tier=TIER,summary=BOUNDARY+'; no queue action',path=finding['path'])
            outcome='INVALID' if 'INVALID' in predictions.values() else 'PASS'
            emit(run_dir,'run_finished',outcome=outcome,
                 summary='Execution completed; individual predictions are separate; '+BOUNDARY)
            return outcome
    except BaseException as error:
        code=getattr(error,'code','INVALID-WORKER')
        try:
            if process is not None and not kill_sent:
                try: os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError: pass
            # Cleanup and halt durability consume only the original remaining budget.
            with hard_deadline(controller.remaining()):
                if process is not None: process.wait(timeout=controller.remaining())
                diagnostic=receipt(run_dir,'halt',{'code':code,'message':str(error),
                    'observed':getattr(error,'observed',None),'prediction_verdict':'NOT COMPUTED'})
                controller.remaining()
                emit(run_dir,'halted',reason=code+': '+str(error),diagnostic_path=diagnostic['path'])
        except BaseException as closeout_error:
            print(f'{code}: {error}; closeout incomplete: {closeout_error}; no prediction verdict',file=sys.stderr)
        if isinstance(error,(KeyboardInterrupt,SystemExit)): raise
        return code
    finally:
        parent.close(); child.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prereg-sha',required=True)
    parser.add_argument('--admission',type=Path)
    args=parser.parse_args()
    prereg=ROOT/'docs/NEW1_ADAPTER_GEOMETRY_PREREG.md'
    directory=ROOT/'results/mathlab_staging/runs'/('new1_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    directory.mkdir(parents=True,exist_ok=False)
    command=['nice','-n','10',sys.executable,'-B',str(ROOT/'tools/new1_geometry.py'),
             '--run-dir',str(directory),'--prereg-sha',args.prereg_sha]
    def admission():
        verify_prereg(prereg,args.prereg_sha)
        receipt(directory,'criteria',{'path':str(prereg),'sha256':args.prereg_sha})
        return cpu_admission(directory,args.admission)
    outcome=supervise(command,directory,admission=admission)
    print(outcome)
    return 0 if outcome=='PASS' else 3


if __name__=='__main__': sys.exit(main())
