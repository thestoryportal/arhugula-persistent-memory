"""Investigation only: no signal, alarm, wait, kill or native-exit replacements."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import signal
import struct
import sys
import threading
import time
import traceback
import unittest
from investigation_io import write_json
from scratch_builder import guard

LIB = ctypes.CDLL('/usr/lib/libproc.dylib', use_errno=True)
LIB.proc_pidinfo.argtypes = [ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int]
LIB.proc_pidinfo.restype = ctypes.c_int
PID = os.getpid()
CURRENT = None
DIRECTORY = None
SEQUENCE = 0
CHILDREN = {}
WRITE_TIMES = []
TARGETS = ('test_blocked_halt_persistence_cannot_extend_total_deadline',
    'test_blocking_admission_is_interrupted_by_whole_run_deadline',
    'test_cell_alarm_interrupts_blocked_persistence_inside_total_cap',
    'test_supervisor_cell_deadline_interrupts_a_blocked_resource_probe',
    'test_watchdog_enforces_during_blocked_persistence',
    'test_watchdog_refuses_memory_drop_during_blocking_admission')
THRESHOLDS = dict(zip(TARGETS, [dict(elapsed_lt_s=.3),dict(outcome='STOPPED-DEADLINE',elapsed_lt_s=1.),
    dict(elapsed_lt_s=.2),dict(outcome='STOPPED-RESOURCE',elapsed_lt_s=.2),
    dict(outcome='STOPPED-RESOURCE',elapsed_lt_s=.5),dict(outcome='STOPPED-RESOURCE',elapsed_lt_s=.5)]))


def native(flavor, size, argument=0):
    buffer = ctypes.create_string_buffer(size)
    count = LIB.proc_pidinfo(os.getpid(), flavor, argument, buffer, size)
    if count <= 0:
        return {'status':'UNAVAILABLE','errno':ctypes.get_errno(),'flavor':flavor}
    return buffer.raw[:count]


def snapshot():
    tids = native(6, 8192)
    if isinstance(tids, bytes):
        ids = list(struct.unpack('='+str(len(tids)//8)+'Q', tids)); states = []
        for tid in ids:
            raw = native(15, 112, tid)
            if isinstance(raw, bytes) and len(raw)==112:
                v = struct.unpack('=QQ8i64s', raw)
                states.append({'id':tid,'user_time':v[0],'system_time':v[1],
                               'cpu_usage':v[2],'policy':v[3],'run_state':v[4],'flags':v[5]})
            else: states.append({'id':tid,'observation':raw if isinstance(raw,dict) else {'bytes':len(raw)}})
        threads = {'status':'OBSERVED','ids':ids,'states':states}
    else: threads = tids
    raw = native(1, 8192)
    fds = {'status':'OBSERVED','fds':[{'fd':a,'type':b} for a,b in struct.iter_unpack('=iI',raw)]} if isinstance(raw,bytes) else raw
    owned = []
    for pid, detail in CHILDREN.items():
        try: pgid = os.getpgid(pid); existence = 'PRESENT'
        except ProcessLookupError: pgid = None; existence = 'ABSENT'
        except OSError as error: pgid=None; existence='UNAVAILABLE: '+repr(error)
        owned.append({'pid':pid,'pgid':pgid,'existence':existence,**detail})
    torch = sys.modules.get('torch')
    return {'pid':os.getpid(),'ppid':os.getppid(),'pgid':os.getpgrp(),
        'main_native_id':threading.get_native_id(),
        'caller_mask':sorted(int(s) for s in signal.pthread_sigmask(signal.SIG_BLOCK, [])),
        'caller_pending':sorted(int(s) for s in signal.sigpending()),
        'alarm_handler':repr(signal.getsignal(signal.SIGALRM)),
        'alarm_timer':signal.getitimer(signal.ITIMER_REAL),
        'native_threads':threads,'descriptors':fds,'owned_children':owned,
        'torch':{'loaded':torch is not None,'path':getattr(torch,'__file__',None),
                 'num_threads':torch.get_num_threads() if torch else None,
                 'num_interop_threads':torch.get_num_interop_threads() if torch else None},
        'other_native_thread_signal_masks':'NOT-RUN: libproc has no per-thread signal-mask accessor'}


def emit(event, phase=None, state=False, **values):
    global SEQUENCE
    if os.getpid()!=PID: return
    SEQUENCE += 1
    record = {'event':event,'phase':phase or event,'test':CURRENT,'pid':PID,
              'monotonic_ns':time.monotonic_ns(),'wall_ns':time.time_ns(),**values}
    if state: record['state']=snapshot()
    start=time.monotonic()
    write_json(DIRECTORY/f'{PID}_{SEQUENCE:06d}.json',record)
    WRITE_TIMES.append(time.monotonic()-start)


def provenance():
    tree = Path(os.environ['LLMDB_ROOT']).resolve()
    modules = [m for n,m in list(sys.modules.items()) if n.startswith(('tools.','tests.')) and getattr(m,'__file__',None)]
    return guard(modules,tree)


def profile(frame, event, arg):
    if os.getpid()!=PID: return
    filename=frame.f_code.co_filename; name=frame.f_code.co_name
    target=CURRENT is not None and (CURRENT.rsplit('.',1)[-1] in TARGETS or 'SignalFixture' in CURRENT or 'SyntheticParent' in CURRENT)
    if event in ('c_call','c_return','c_exception'):
        module=getattr(arg,'__module__',''); cname=getattr(arg,'__name__','')
        if target and module in ('signal','_signal') and cname=='setitimer':
            emit('alarm-armed' if event=='c_return' else 'alarm-arm-'+event, state=True, caller=filename, line=frame.f_lineno)
        elif target and module=='time' and cname=='sleep':
            emit('sleep-'+event, state=True, caller=filename,line=frame.f_lineno)
        elif target and module in ('os','posix') and cname in ('killpg','kill','waitpid','_exit'):
            emit(cname+'-'+event,state=True,caller=filename,line=frame.f_lineno)
        return
    if event=='call' and name in ('expired','on_signal','known_handler'):
        emit('alarm-fired',state=True,handler_file=filename,line=frame.f_lineno,
             signal_number=frame.f_locals.get('signum',frame.f_locals.get('number')))
    if filename.endswith('/subprocess.py'):
        process=frame.f_locals.get('self')
        if event=='return' and name=='_execute_child' and getattr(process,'pid',None):
            CHILDREN[process.pid]={'created_test':CURRENT,'returncode':process.returncode,
                                  'command':repr(process.args),'creation_site':filename+':'+str(frame.f_lineno)}
            emit('pid-created',state=True,pid_created=process.pid,stack=traceback.format_stack(frame,limit=8))
        elif event=='return' and name in ('wait','_wait','_handle_exitstatus') and getattr(process,'pid',None):
            if process.pid in CHILDREN: CHILDREN[process.pid]['returncode']=process.returncode
            if target or process.returncode is not None: emit('pid-collection',pid_collected=process.pid,
                returncode=process.returncode,method=name,state=target)
        elif event=='call' and name=='__del__' and getattr(process,'pid',None):
            emit('popen-destructor-before-poll',state=True,pid_destructed=process.pid,cached_returncode=process.returncode)
    if target and filename.endswith('/new1_supervisor.py') and name=='supervise' and event=='return':
        emit('supervisor-return-before-fixture-cleanup',state=True,outcome=arg,
             traceback_format_exc=traceback.format_exc(),local_error=repr(frame.f_locals.get('error')),
             closeout_error=repr(frame.f_locals.get('closeout_error')))
    if filename.endswith('/new1_identity_diag.py') and event=='return' and name in ('start','step','close'):
        owner=frame.f_locals.get('self')
        if owner is not None:
            if getattr(owner,'pid',None): CHILDREN.setdefault(owner.pid,{'created_test':CURRENT,'kind':'guardian'})['returncode']=owner.returncode
            if target or name in ('start','close'):
                emit('owned-worker-'+name,state=target,guardian_pid=getattr(owner,'pid',None),
                    worker_pid=getattr(owner,'worker_pid',None),returncode=getattr(owner,'returncode',None),
                    proof=getattr(owner,'proof',None),channels=getattr(owner,'channels',None),streams=repr(getattr(owner,'streams',None)))


def install():
    global DIRECTORY
    DIRECTORY=Path(os.environ['NEW1_OBSERVE_DIR']); DIRECTORY.mkdir(parents=True,exist_ok=False)
    real=unittest.TestCase._callTestMethod
    def call(test,method):
        global CURRENT
        prior=CURRENT; CURRENT=test.id()
        emit('test-start',state=True,loaded_modules=provenance())
        try: return real(test,method)
        except BaseException:
            measured={}
            tb=sys.exc_info()[2]
            while tb is not None:
                for key in ('elapsed','started','outcome','status','seconds'):
                    value=tb.tb_frame.f_locals.get(key)
                    if type(value) in (int,float,str): measured[key]=value
                tb=tb.tb_next
            if 'started' in measured: measured['elapsed_at_exception_s']=time.monotonic()-measured['started']
            emit('test-exception',state=True,traceback_format_exc=traceback.format_exc(),measured=measured,
                 thresholds=THRESHOLDS.get(test.id().rsplit('.',1)[-1],{'expected':'fixture-defined; see traceback'}))
            raise
        finally:
            emit('before-fixture-teardown-and-cleanup',state=True,
                 fixture_paths={p.name:p.read_text(errors='replace')[:16384] for p in getattr(test,'root',Path('/nonexistent')).rglob('*')
                     if p.is_file() and p.name in ('pid','leader_pid','grandchild_pid','events.jsonl','worker_stdout.log','worker_stderr.log')}
                     if test.id().rsplit('.',1)[-1] in TARGETS else {},
                 observer_io_s=sum(WRITE_TIMES),observer_max_write_s=max(WRITE_TIMES,default=0))
            CURRENT=prior
    unittest.TestCase._callTestMethod=call
    env={key:({'redacted_sha256':hashlib.sha256(value.encode()).hexdigest()} if any(s in key.upper() for s in ('TOKEN','SECRET','PASSWORD','API_KEY')) else value)
         for key,value in os.environ.items()}
    emit('process-provenance',state=True,interpreter=sys.executable,version=sys.version,argv=sys.argv,
         environment=env,profile_before=repr(sys.getprofile()),trace_before=repr(sys.gettrace()))
    if sys.getprofile() is not None: raise RuntimeError('refuse to replace existing profiler')
    sys.setprofile(profile)
