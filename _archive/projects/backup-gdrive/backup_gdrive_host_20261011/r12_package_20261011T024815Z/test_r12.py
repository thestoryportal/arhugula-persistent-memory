"""MB44 controls: synthetic git only, copied receipts, injected executable probe."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
K = ROOT/'results/backup_gdrive_host_20261011/r11_package_20261011T005440Z'
BASELINE = os.environ.get('R12_BASELINE') == '1'

def module(name):
    path = (HERE/'before' if BASELINE else HERE)/(name+'.py')
    spec = importlib.util.spec_from_file_location('r12_'+name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj

class ScopeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='r12_scope_', dir='/private/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name); self.repo = self.base/'repo'; self.repo.mkdir()
        self.pkg = self.base/'package'; self.pkg.mkdir()
        self.git('init','-b','master')
        self.git('config','user.email','fixture@invalid.example')
        self.git('config','user.name','MB44 fixture')
        (self.repo/'unrelated.txt').write_text('base\n')
        (self.repo/'tools').mkdir()
        (self.repo/'tools/noop.sh').write_text('unchanged pinned input\n')
        self.git('add','.'); self.git('commit','-m','base')
        self.git('update-ref','refs/remotes/origin/master','HEAD')
        self.git('checkout','-b','fixture-source')
        for name in ('tools/backup.sh','results/backup/evidence.txt'):
            p=self.repo/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(name+'\n')
        (self.repo/'unrelated.txt').write_text('must not copy\n')
        self.git('add','.'); self.git('commit','-m','source with unrelated work')
        self.source = self.git('rev-parse','HEAD').strip()
        self.paths=['results/backup/evidence.txt','tools/backup.sh']
        (self.pkg/'scope_allowlist.txt').write_text('\n'.join(self.paths)+'\n')
        (self.pkg/'pins_v3.sha256').write_text(''.join(hashlib.sha256((self.repo/p).read_bytes()).hexdigest()+'  '+p+'\n' for p in self.paths))
        if BASELINE:
            shutil.copy2(HERE/'before/make_backup_candidate_scope_red.sh',self.pkg/'make_backup_candidate.sh')
            shutil.copy2(HERE/'before/candidate_scope_red.py',self.pkg/'candidate.py')
        else:
            for name in ('make_backup_candidate.sh','candidate.py'):
                shutil.copy2(HERE/name,self.pkg/name)
        self.target = self.base/'candidate'

    def git(self,*args,cwd=None):
        return subprocess.run(['/usr/bin/git','-C',str(cwd or self.repo),*args],check=True,text=True,capture_output=True).stdout

    def call(self,mode='create'):
        args=[str(self.repo),self.source,str(self.target)] if mode=='create' else [str(self.target),self.source]
        return subprocess.run(['/bin/sh',str(self.pkg/'make_backup_candidate.sh'),mode,*args],capture_output=True,text=True)

    def create(self):
        value=self.call(); self.assertEqual(value.returncode,0,value.stdout+value.stderr)

    def test_copy_exact_committed_bytes_and_branch(self):
        self.create()
        self.assertEqual(self.git('branch','--show-current',cwd=self.target).strip(),'backup-gdrive-r12')
        self.assertEqual(self.git('diff','--name-only','origin/master',cwd=self.target).splitlines(),self.paths)
        self.assertEqual((self.target/'unrelated.txt').read_text(),'base\n')
        (self.repo/'tools/backup.sh').write_text('uncommitted drift\n')
        self.assertEqual((self.target/'tools/backup.sh').read_text(),'tools/backup.sh\n')

    def test_extra_file_in_diff_fails(self):
        self.create(); (self.target/'extra.txt').write_text('sneaked\n')
        self.git('add','extra.txt',cwd=self.target)
        value=self.call('verify'); self.assertNotEqual(value.returncode,0,value.stdout)
        self.assertIn('scope',value.stderr.lower())

    def test_same_count_wrong_paths_fails(self):
        self.create(); self.git('reset','origin/master','--',self.paths[0],cwd=self.target)
        (self.target/'extra.txt').write_text('replacement\n'); self.git('add','extra.txt',cwd=self.target)
        self.assertEqual(len(self.git('diff','--name-only','origin/master',cwd=self.target).splitlines()),len(self.paths))
        value=self.call('verify'); self.assertNotEqual(value.returncode,0,value.stdout)

    def test_pin_mismatch_fails(self):
        self.create(); (self.target/'tools/backup.sh').write_text('tampered\n')
        self.assertNotEqual(self.call('verify').returncode,0)

    def test_unchanged_pinned_path_is_excluded_from_exact_diff(self):
        self.paths=sorted(self.paths+['tools/noop.sh'])
        (self.pkg/'scope_allowlist.txt').write_text('\n'.join(self.paths)+'\n')
        (self.pkg/'scope_unchanged.txt').write_text('tools/noop.sh\n')
        (self.pkg/'pins_v3.sha256').write_text(''.join(hashlib.sha256((self.repo/p).read_bytes()).hexdigest()+'  '+p+'\n' for p in self.paths))
        self.create()
        self.assertEqual(self.git('diff','--name-only','origin/master',cwd=self.target).splitlines(),[p for p in self.paths if p!='tools/noop.sh'])

    def test_false_unchanged_declaration_fails(self):
        (self.pkg/'scope_unchanged.txt').write_text('tools/backup.sh\n')
        self.assertNotEqual(self.call().returncode,0)

    def test_glob_allowlist_fails(self):
        (self.pkg/'scope_allowlist.txt').write_text('tools/*\n')
        self.assertNotEqual(self.call().returncode,0)

    def test_oversize_evidence_fails(self):
        (self.repo/self.paths[0]).write_bytes(b'x'*1000001)
        self.git('add','.'); self.git('commit','-m','large evidence')
        self.source=self.git('rev-parse','HEAD').strip()
        (self.pkg/'pins_v3.sha256').write_text(''.join(hashlib.sha256((self.repo/p).read_bytes()).hexdigest()+'  '+p+'\n' for p in self.paths))
        self.assertNotEqual(self.call().returncode,0)

class PlanTest(unittest.TestCase):
    def setUp(self):
        self.checker=module('check_plan'); self.probes=[]
        self.checker.executable_probe=lambda path: self.probes.append(path) or True

    def row(self,command):
        return '<!-- row test marker=MAESTRO-GO -->\n```bash\n'+command+'\n```\n'

    def codes(self,text): return [x['code'] for x in self.checker.check(text)]

    def test_missing_executable_fails_with_injected_probe(self):
        self.checker.executable_probe=lambda path: False
        self.assertIn('EXECUTABLE',self.codes(self.row('capture pr /opt/homebrew/bin/gh pr create --head backup-gdrive-r12')))

    def test_wrong_head_fails(self):
        self.assertIn('PR_HEAD',self.codes(self.row('capture pr /opt/homebrew/bin/gh pr create --head worktree-c10k-route-a')))

    def test_missing_head_fails(self):
        self.assertIn('PR_HEAD',self.codes(self.row('capture pr /opt/homebrew/bin/gh pr create --base master')))

    def test_relative_program_fails(self):
        self.assertIn('EXECUTABLE_PATH',self.codes(self.row('capture pr gh pr create --head backup-gdrive-r12')))

    def test_probe_all_wrapped_executables(self):
        self.assertEqual(self.checker.check(self.row('capture x /usr/bin/env LLMDB_ROOT="$I" /usr/bin/caffeinate -i -s /opt/homebrew/bin/rclone check s d --log-format date,time')),[])
        self.assertEqual(self.probes,['/usr/bin/env','/usr/bin/caffeinate','/opt/homebrew/bin/rclone'])

    def test_missing_log_format_fails(self):
        self.assertIn('LOG_FORMAT',self.codes(self.row('capture x /opt/homebrew/bin/rclone check s d --log-level DEBUG')))

    def test_wrong_log_format_fails(self):
        self.assertIn('LOG_FORMAT',self.codes(self.row('capture x /opt/homebrew/bin/rclone check s d --log-format date,time,microseconds')))

    def test_json_override_fails(self):
        self.assertIn('LOG_FORMAT',self.codes(self.row('capture x /opt/homebrew/bin/rclone check s d --log-format date,time --use-json-log')))

    def test_plan_v3_contract(self):
        plan=(K/'activation_plan_v2.md' if BASELINE else HERE/'activation_plan_v3.md').read_text()
        self.assertIn('executable-preflight',plan)
        self.assertIn('--head backup-gdrive-r12',plan)
        rows=[x for x in plan.splitlines() if x.startswith(('capture full-check ','capture full-check-download '))]
        self.assertEqual(len(rows),2)
        self.assertTrue(all('--log-format date,time' in x for x in rows))
        self.assertEqual(self.checker.check(plan),[])

class LogTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='r12_log_',dir='/private/tmp'); self.addCleanup(self.tmp.cleanup)
        self.run=Path(self.tmp.name)/'clean'
        shutil.copytree(HERE/'r11_evidence/r11_hostfix1_local_check/local_check/clean',self.run)
        self.verifier=module('verify_check')

    def append(self,line,file='check.log'):
        with (self.run/file).open('a') as stream: stream.write(line+'\n')

    def test_saved_fixture_replay(self):
        for case in ('clean','excluded_only','symlink','same_size_corruption'):
            with self.subTest(case=case):
                run=Path(self.tmp.name)/case
                if case!='clean': shutil.copytree(HERE/'r11_evidence/r11_hostfix1_local_check/local_check'/case,run)
                cli=subprocess.run(['/usr/bin/python3','-B',str(self.verifier.__file__),str(run)],capture_output=True,text=True)
                self.assertEqual(cli.returncode,1 if case=='same_size_corruption' else 0,cli.stdout+cli.stderr)
                if case=='same_size_corruption': self.assertIn('alpha.txt',cli.stdout)

    def test_debug_argument_error_is_harmless(self):
        self.append('2026/10/11 00:00:00 DEBUG : argv ["--error", "error.txt", "error", "ERROR"]')
        self.assertTrue(self.verifier.inspect(self.run)['pass'])

    def test_standard_errors_fail(self):
        for severity in ('ERROR','CRITICAL','FATAL'):
            with self.subTest(severity=severity):
                self.append('2026/10/11 00:00:00 '+severity+': fixture anomaly')
                self.assertFalse(self.verifier.inspect(self.run)['pass'])

    def unsupported(self,shape,file='check.log'):
        original=(self.run/file).read_bytes()
        for severity in ('ERROR','CRITICAL','FATAL'):
            with self.subTest(severity=severity):
                (self.run/file).write_bytes(original)
                line={'microseconds':'2026/10/11 00:00:00.123456 '+severity+': fixture anomaly',
                      'time_only':'00:00:00 '+severity+': fixture anomaly',
                      'prefix':'worker: 2026/10/11 00:00:00 '+severity+': fixture anomaly',
                      'json':json.dumps({'level':severity.lower(),'msg':'fixture anomaly'}),
                      'unprefixed':severity+': fixture anomaly'}[shape]
                self.append(line,file)
                value=self.verifier.inspect(self.run)
                self.assertFalse(value['pass'],(line,value))

    def test_microseconds_fail(self): self.unsupported('microseconds')
    def test_time_only_fail(self): self.unsupported('time_only')
    def test_prefix_fail(self): self.unsupported('prefix')
    def test_json_fail(self): self.unsupported('json')
    def test_unprefixed_fail(self): self.unsupported('unprefixed')
    def test_stderr_json_fail(self): self.unsupported('json','stderr.txt')

    def test_fixture_template_pins_format(self):
        runner=module('run_local_check')
        for download in (False,True):
            argv=runner.check_argv('s','d','excludes',self.run,download)
            self.assertIn('--log-format',argv)
            self.assertEqual(argv[argv.index('--log-format')+1],'date,time')

if __name__=='__main__': unittest.main(verbosity=2)
