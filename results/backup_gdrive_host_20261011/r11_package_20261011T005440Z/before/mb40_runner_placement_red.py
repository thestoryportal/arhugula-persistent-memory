"""MB39 isolated host coverage/evidence runner. No execution on import."""
import argparse
import ast
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pwd
import re
import signal
import subprocess
import sys
import tempfile
import time
import unittest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
FROZEN=ROOT/'results/backup_gdrive_host_20261010/locked_release_20261010T221519Z/run_suite.py'
sys.path.insert(0,str(HERE))
from real_inventory import inventory

def selected_ids(root):
    def cases(file,klass):
        tree=ast.parse((root/file).read_text())
        node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==klass)
        return [n.name for n in node.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
    base=['tools.test_backup_gdrive.BackupTest.'+n for n in cases('tools/test_backup_gdrive.py','BackupTest')]
    launcher=['tools.test_backup_gdrive_addendum.LauncherTest.'+n for n in cases('tools/test_backup_gdrive_addendum.py','LauncherTest')]
    old=json.loads((FROZEN.parent/'cmpfix_green/result.json').read_text())
    heartbeat=[x['test'] for x in old['skips'] if '.HeartbeatTest.' in x['test']]
    if (len(base),len(heartbeat),len(launcher)) != (10,9,3): raise RuntimeError('coverage selection drift')
    return base+heartbeat+launcher

def validate_host(version,nice,env):
    if tuple(version)!=(3,9,6): raise RuntimeError('requires production /usr/bin/python3 3.9.6')
    if nice!=0: raise RuntimeError('requires niceness 0')
    names=[k for k in env if k.startswith('RCLONE_')]
    if names: raise RuntimeError('refusing inherited RCLONE_* names: '+repr(names))

def forbidden_argv(argv):
    return any('gdrive:' in str(a) or '/usr/bin/open' in str(a) or
               re.search(r'\blaunchctl\b',str(a)) for a in argv)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('label')
    parser.add_argument('--mode',choices=('coverage','sandbox','staging','e-red','e-green','package','check-red','check-green','fixture','frozen'),default='coverage')
    args=parser.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_.-]+',args.label): raise RuntimeError('invalid run label')
    nice=os.getpriority(os.PRIO_PROCESS,0)
    if args.mode in ('sandbox','staging'):
        if sys.version_info[:3]!=(3,9,6): raise RuntimeError('sandbox requires /usr/bin/python3 3.9.6')
        if any(k.startswith('RCLONE_') for k in os.environ): raise RuntimeError('inherited RCLONE_*')
    else:
        validate_host(sys.version_info[:3],nice,os.environ)
    if not sys.flags.dont_write_bytecode: raise RuntimeError('invoke /usr/bin/python3 -B')
    # /usr/bin/python3 is Apple's launcher; sys.executable names the CLT executable.
    probe=subprocess.run(['/usr/bin/python3','-B','-c','import sys; print(sys.executable)'],text=True,capture_output=True)
    if probe.returncode or probe.stdout.strip()!=sys.executable: raise RuntimeError('wrong production interpreter executable')
    real_home=Path(pwd.getpwuid(os.getuid()).pw_dir)
    run=HERE/args.label; run.mkdir()
    home=run/'home'; home.mkdir(); fixtures=home/'fixtures'; fixtures.mkdir()
    original_env=dict(os.environ)
    for key in ('RCLONE_CONFIG','XDG_CONFIG_HOME','BACKUP_TEST_NO_RCLONE'): os.environ.pop(key,None)
    os.environ.update(HOME=str(home),LLMDB_ROOT=str(ROOT),BACKUP_TEST_RECEIPTS=str(fixtures),
                      PYTHONDONTWRITEBYTECODE='1',BACKUP_PYTHON='/usr/bin/python3',MB28_BACKUP_PYTHON='/usr/bin/python3')
    if args.mode!='coverage' and args.mode!='fixture': os.environ['BACKUP_TEST_NO_RCLONE']='1'
    def save(name,value): (run/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
    sources=[ROOT/n for n in ('tools/backup_gdrive.sh','tools/backup_gdrive_status.py','tools/backup_mirror.excludes',
        'tools/launchd/MemitGdriveBackup.applescript','tools/launchd/build_gdrive_applet.sh','tools/launchd/stage_gdrive_release.sh',
        'tools/launchd/com.rhu.memit-gdrive-backup.plist','tools/test_backup_gdrive.py','tools/test_backup_gdrive_addendum.py')]
    sources += [FROZEN,*sorted(HERE.glob('*.py'))]
    if (HERE/'activation_plan_v2.md').exists(): sources.append(HERE/'activation_plan_v2.md')
    save('command.json',dict(argv=['/usr/bin/python3','-B',*sys.argv],cwd=str(Path.cwd()),interpreter=sys.executable,
        invoked_interpreter='/usr/bin/python3',python_version=sys.version,niceness=nice,
        env={k:os.environ.get(k) for k in ('HOME','LLMDB_ROOT','BACKUP_TEST_NO_RCLONE','RCLONE_CONFIG','XDG_CONFIG_HOME',
            'BACKUP_TEST_RECEIPTS','PYTHONDONTWRITEBYTECODE','BACKUP_PYTHON','MB28_BACKUP_PYTHON')},
        source_sha256={str(p.relative_to(ROOT)):digest(p) for p in sources},real_home=str(real_home)))
    save('interpreter_probe.json',dict(argv=probe.args,stdout=probe.stdout,stderr=probe.stderr,exit_code=probe.returncode))
    (run/'real_before.json').write_text(inventory(real_home))
    started=[]; active_test=None; first=0
    original_popen=subprocess.Popen.__init__
    def tracked(self,*pos,**kw):
        command=kw.get('args',pos[0] if pos else [])
        argv=list(command) if isinstance(command,(list,tuple)) else [str(command)]
        if forbidden_argv(argv): raise RuntimeError('forbidden child argv: '+repr(argv))
        if args.mode in ('sandbox','staging') and any(str(a) in ('/usr/bin/osascript','/usr/bin/osacompile','/usr/bin/osadecompile','/opt/homebrew/bin/rclone') for a in argv):
            raise RuntimeError('sandbox native/real-rclone command refused: '+repr(argv))
        kw['start_new_session']=True
        original_popen(self,*pos,**kw)
        row=dict(pid=self.pid,pgid=self.pid,argv=argv,test=active_test)
        started.append((self,row))
        with (run/'started_processes.jsonl').open('a') as f: f.write(json.dumps(row)+'\n')
    subprocess.Popen.__init__=tracked
    def alive(group):
        try: os.killpg(group,0); return True
        except ProcessLookupError: return False
    def clear(index):
        rows=[]; leaks=[]
        for proc,row in started[index:]:
            deadline=time.monotonic()+0.5
            while alive(row['pgid']) and time.monotonic()<deadline:
                proc.poll(); time.sleep(0.01)
            row['returncode']=proc.poll(); row['group_alive_after_test']=alive(row['pgid'])
            if row['returncode'] is None or row['group_alive_after_test']:
                leaks.append(dict(row))
                if alive(row['pgid']): os.killpg(row['pgid'],signal.SIGKILL)
                proc.wait(timeout=5); row['cleanup_after_failure']=True
            row['group_alive_after_cleanup']=alive(row['pgid']); rows.append(dict(row))
        with (run/'process_clearance.jsonl').open('a') as f:
            f.write(json.dumps(dict(test=active_test,processes=rows,leaks=leaks))+'\n')
        return leaks
    class ClearedResult(unittest.TextTestResult):
        def startTest(self,test):
            nonlocal active_test,first
            active_test=test.id(); first=len(started); super().startTest(test)
        def stopTest(self,test):
            leaked=clear(first)
            if leaked:
                try: raise AssertionError('owned process group leaked: '+repr(leaked))
                except AssertionError: self.addFailure(test,sys.exc_info())
            super().stopTest(test)
    def call(label,argv):
        completed=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=1800)
        (run/(label+'.stdout.txt')).write_text(completed.stdout)
        (run/(label+'.stderr.txt')).write_text(completed.stderr)
        (run/(label+'.exit_code.txt')).write_text(str(completed.returncode)+'\n')
        save(label+'.command.json',dict(argv=argv,cwd=str(Path.cwd())))
        return completed
    summary=dict(success=False,mode=args.mode)
    try:
        try:
            ps=call('ps',['/bin/ps','-axo','pid,ppid,pgid,stat,etime,command'])
        except PermissionError as exc:
            ps=subprocess.CompletedProcess(['/bin/ps','-axo','pid,ppid,pgid,stat,etime,command'],126,'',repr(exc)+'\n')
            (run/'ps.stdout.txt').write_text(ps.stdout)
            (run/'ps.stderr.txt').write_text(ps.stderr)
            (run/'ps.exit_code.txt').write_text('126\n')
            save('ps.command.json',dict(argv=ps.args,cwd=str(Path.cwd())))
        save('ps_observation.json',dict(available=ps.returncode==0,exit_code=ps.returncode,
                                      stdout='ps.stdout.txt',stderr='ps.stderr.txt'))
        if args.mode in ('coverage','fixture'):
            config=call('config_file',['/opt/homebrew/bin/rclone','config','file'])
            if config.returncode: raise RuntimeError('config positive control failed')
            config_path=Path(config.stdout.strip().splitlines()[-1]).resolve()
            try: config_path.relative_to(home.resolve())
            except ValueError: raise RuntimeError('rclone config escaped fixture HOME')
            remotes=call('listremotes',['/opt/homebrew/bin/rclone','listremotes'])
            if remotes.returncode or remotes.stdout!='': raise RuntimeError('fixture rclone remote list must be empty')
            save('config_positive_control.json',dict(config_path=str(config_path),home=str(home),listremotes_empty=True))
        if args.mode in ('coverage','sandbox','staging','e-red','e-green'):
            sys.path.insert(0,str(ROOT))
            import tools.test_backup_gdrive_addendum as addendum
            # The base file fixes /private/tmp; route all its local fixtures inside isolated HOME.
            original_temp=tempfile.TemporaryDirectory.__init__
            def local_temp(self,*pos,**kw):
                if kw.get('dir')=='/private/tmp': kw['dir']=str(fixtures)
                original_temp(self,*pos,**kw)
            tempfile.TemporaryDirectory.__init__=local_temp
            loader=unittest.defaultTestLoader
            if args.mode=='coverage':
                ids=selected_ids(ROOT); suite=unittest.TestSuite(loader.loadTestsFromName(n) for n in ids)
            elif args.mode=='staging':
                ids=['tools.test_backup_gdrive_addendum.LockedReleaseTest.test_good_release_dispatches_release_path']
                suite=unittest.TestSuite(loader.loadTestsFromName(n) for n in ids)
            elif args.mode=='sandbox':
                native={'tools.test_backup_gdrive_addendum.LauncherTest.test_nonzero_shell_script_is_caught_promptly_without_dialog',
                        'tools.test_backup_gdrive_addendum.LauncherTest.test_builder_compiles_applet_and_prints_complete_sha256_manifest',
                        'tools.test_backup_gdrive_addendum.LockedReleaseTest.test_compiled_app_full_source_equals_saved_source',
                        'tools.test_backup_gdrive_addendum.LockedReleaseTest.test_compiled_app_dispatches_release_after_checkout_change'}
                def flatten(s):
                    for x in s:
                        if isinstance(x,unittest.TestSuite): yield from flatten(x)
                        else: yield x
                tests=list(flatten(loader.loadTestsFromModule(addendum)))
                suite=unittest.TestSuite(t for t in tests if t.id() not in native); ids=[t.id() for t in flatten(suite)]
                save('native_not_run.json',sorted(native))
            else:
                if args.mode=='e-red':
                    spec=importlib.util.spec_from_file_location('e_red_snapshot',HERE/'before/tools/test_backup_gdrive_addendum_red_valid.py')
                    addendum=importlib.util.module_from_spec(spec); spec.loader.exec_module(addendum); addendum.ROOT=ROOT
                suite=loader.loadTestsFromTestCase(addendum.LauncherHomeExportTest)
                if args.mode=='e-green': suite.addTests(loader.loadTestsFromTestCase(addendum.LauncherTest))
                ids=[str(suite)]
            save('suite_selection.json',dict(ids=ids,count=suite.countTestCases()))
            with (run/'test.log').open('w') as log:
                result=unittest.TextTestRunner(stream=log,verbosity=2,resultclass=ClearedResult).run(suite)
            summary.update(testsRun=result.testsRun,failures=len(result.failures),errors=len(result.errors),
                skipped=len(result.skipped),skips=[dict(test=t.id(),reason=why) for t,why in result.skipped])
            summary['success']=result.wasSuccessful() and (args.mode!='coverage' or (result.testsRun==22 and not result.skipped))
        else:
            if args.mode=='package': argv=['/usr/bin/python3','-B',str(HERE/'test_package.py')]
            elif args.mode=='check-red': argv=['/usr/bin/python3','-B',str(HERE/'check_plan.py'),str(ROOT/'results/backup_gdrive_host_20261010/activation_plan_maestro24.md')]
            elif args.mode=='check-green': argv=['/usr/bin/python3','-B',str(HERE/'check_plan.py'),str(HERE/'activation_plan_v2.md')]
            elif args.mode=='fixture': argv=['/usr/bin/python3','-B',str(HERE/'run_local_check.py'),str(run/'local_check')]
            else: argv=['/usr/bin/python3','-B',str(FROZEN),args.label+'_all','all']
            completed=call('driver',argv); summary['child_exit_code']=completed.returncode
            summary['success']=completed.returncode==0
            if args.mode=='check-red': summary['success']=completed.returncode==1
            if args.mode=='frozen':
                old=json.loads((FROZEN.parent/(args.label+'_all')/'result.json').read_text())
                summary['frozen_result']=old
                summary['success']=summary['success'] and old['testsRun']==155 and old['skipped']==14 and old['all_owned_groups_exited']
            if clear(0): summary['success']=False
    except BaseException as exc:
        summary['exception']=repr(exc); summary['success']=False
        clear(0)
    finally:
        try:
            after=inventory(real_home); (run/'real_after.json').write_text(after)
            summary['real_inventory_identical']=after==(run/'real_before.json').read_text()
        except (OSError,ValueError) as exc:
            summary['real_inventory_identical']=False; summary['inventory_error']=repr(exc)
        summary['all_owned_groups_exited']=all(p.poll() is not None and not alive(r['pgid']) for p,r in started)
        summary['success']=summary['success'] and summary['real_inventory_identical'] and summary['all_owned_groups_exited']
        summary['exit_code']=0 if summary['success'] else 1
        save('result.json',summary); (run/'exit_code.txt').write_text(str(summary['exit_code'])+'\n')
        subprocess.Popen.__init__=original_popen
        os.environ.clear(); os.environ.update(original_env)
    print(json.dumps(summary,indent=2)); return summary['exit_code']

if __name__=='__main__': sys.exit(main())
