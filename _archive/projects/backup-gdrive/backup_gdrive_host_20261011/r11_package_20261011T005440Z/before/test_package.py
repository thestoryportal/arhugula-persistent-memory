"""MB39 acceptance tests; local fixtures only, no native tools or real rclone."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OLD_PLAN = ROOT/'results/backup_gdrive_host_20261010/activation_plan_maestro24.md'
ORDER = 'resolve scope/deployment build → complete coverage/re-review → publish new pins → refresh inventory and clear orphans → gated merge → stage/build/hash → preserve receipt → GO recovery → verify barrier → GO launch/Allow → completion and content verification → GO install/bootstrap/kickstart → fresh successor verification → GO retirement'

def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE/(name+'.py'))
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

class VerifyCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir='/private/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        self.verifier = module('verify_check')
        for name, value in {'exit_code.txt':'0\n', 'inventory.exit_code.txt':'0\n',
                'inventory.txt':'alpha.txt\nlink.rclonelink\n',
                'combined.txt':'= alpha.txt\n= link.rclonelink\n',
                'differ.txt':'', 'missing-on-dst.txt':'', 'error.txt':'',
                'check.log':'2026/10/11 00:00:00 NOTICE: Local fixture: 0 differences found\n2026/10/11 00:00:00 NOTICE: Local fixture: 2 matching files\n',
                'stdout.txt':'', 'stderr.txt':''}.items():
            (self.run/name).write_text(value)

    def verdict(self, expected):
        result = self.verifier.inspect(self.run)
        self.assertEqual(result['pass'], expected, result)
        for key in ('differing','missing','errors','unchecked','incomplete'):
            self.assertIn(key, result)
        cli = subprocess.run(['/usr/bin/python3','-B',str(HERE/'verify_check.py'),str(self.run)],
                             text=True, capture_output=True)
        self.assertEqual(cli.returncode, 0 if expected else 1, cli.stderr)
        self.assertTrue(cli.stdout.startswith('PASS' if expected else 'FAIL'), cli.stdout)
        return result

    def test_clean(self): self.verdict(True)
    def test_differing_file(self):
        (self.run/'combined.txt').write_text('* alpha.txt\n= link.rclonelink\n')
        (self.run/'differ.txt').write_text('alpha.txt\n')
        self.assertEqual(self.verdict(False)['differing'], 1)
    def test_missing_destination(self):
        (self.run/'combined.txt').write_text('+ alpha.txt\n= link.rclonelink\n')
        (self.run/'missing-on-dst.txt').write_text('alpha.txt\n')
        self.assertEqual(self.verdict(False)['missing'], 1)
    def test_unreadable_file(self):
        (self.run/'combined.txt').write_text('! alpha.txt\n= link.rclonelink\n')
        (self.run/'error.txt').write_text('alpha.txt\n')
        self.assertEqual(self.verdict(False)['errors'], 1)
    def test_unchecked_hash(self):
        with (self.run/'check.log').open('a') as f: f.write('NOTICE: 1 hashes could not be checked\n')
        self.assertEqual(self.verdict(False)['unchecked'], 1)
    def test_missing_report(self):
        (self.run/'error.txt').unlink(); self.verdict(False)
    def test_truncated_line(self):
        (self.run/'combined.txt').write_text('= alpha.txt\n= link.rclonel'); self.verdict(False)
    def test_truncated_population(self):
        (self.run/'combined.txt').write_text('= alpha.txt\n'); self.verdict(False)
    def test_missing_terminal_summary(self):
        (self.run/'check.log').write_text('partial log\n'); self.verdict(False)
    def test_duplicate_report_object(self):
        (self.run/'combined.txt').write_text('= alpha.txt\n= alpha.txt\n'); self.verdict(False)
    def test_nonzero_exit_empty_reports(self):
        (self.run/'exit_code.txt').write_text('7\n')
        for name in ('combined.txt','differ.txt','missing-on-dst.txt','error.txt'): (self.run/name).write_text('')
        self.verdict(False)

class CheckPlanTest(unittest.TestCase):
    def test_v1_all_named_defects(self):
        findings = module('check_plan').check(OLD_PLAN.read_text())
        codes = {x['code'] for x in findings}
        self.assertTrue({'PIPE','GITHUB_MARKER','INTEGRITY','INTERPRETER','CONTENT_MODE','FIXED_GENERATION'} <= codes, findings)
        for finding in findings: self.assertGreater(finding['line'], 0)
    def test_v2(self): self.assertEqual(module('check_plan').check((HERE/'activation_plan_v2.md').read_text()), [])
    def test_unmarked_launch(self):
        self.assertTrue(module('check_plan').check('```bash\n/usr/bin/open -W -g app\n```\n'))
    def test_pipe_even_with_receipt(self):
        self.assertTrue(module('check_plan').check('<!-- row marker=READ-ONLY -->\n```bash\ncapture x cmd | tail -5\n```\n'))
    def test_missing_exit_capture(self):
        self.assertTrue(module('check_plan').check('<!-- row marker=READ-ONLY -->\n```bash\nshasum -a 256 file\n```\n'))

class RunnerContractTest(unittest.TestCase):
    def test_exact_selection(self):
        ids = module('run_py39_coverage').selected_ids(ROOT)
        self.assertEqual(len(ids), 22)
        self.assertEqual(len(set(ids)), 22)
        self.assertEqual(sum('.BackupTest.' in x for x in ids), 10)
        self.assertEqual(sum('.HeartbeatTest.' in x for x in ids), 9)
        self.assertEqual(sum('.LauncherTest.' in x for x in ids), 3)
        self.assertFalse(any('.ArchiveTest.' in x for x in ids))
    def test_host_refusal_boundaries(self):
        validate = module('run_py39_coverage').validate_host
        validate((3,9,6), 0, {})
        for version, nice, env in [((3,9,5),0,{}),((3,11,0),0,{}),((3,9,6),5,{}),
                ((3,9,6),0,{'RCLONE_CONFIG':'secret'}),((3,9,6),0,{'RCLONE_X':'value'})]:
            with self.subTest(version=version,nice=nice,env=env):
                with self.assertRaises(RuntimeError): validate(version,nice,env)
    def test_forbidden_child_argv(self):
        forbidden = module('run_py39_coverage').forbidden_argv
        for args in (['rclone','lsf','gdrive:x'],['/bin/launchctl','list'],['/usr/bin/open','app'],
                     ['/bin/sh','-c','exec launchctl list']): self.assertTrue(forbidden(args))
        self.assertFalse(forbidden(['/opt/homebrew/bin/rclone','check','/tmp/source','/tmp/dest']))

class CheckTemplateTest(unittest.TestCase):
    def test_filters_reports_and_download(self):
        make = module('run_local_check').check_argv
        argv = make('/source','/dest','/release/backup_mirror.excludes',Path('/R'))
        self.assertEqual(argv[:2], ['/opt/homebrew/bin/rclone','check'])
        self.assertIn('--one-way',argv); self.assertIn('--links',argv)
        self.assertNotIn('--size-only',argv); self.assertNotIn('--download',argv)
        expected = ['**/.git/objects/**/tmp_obj_*','**/.git/objects/tmp_obj_*',
                    '/.git/objects/**/tmp_obj_*','/.git/objects/tmp_obj_*']
        self.assertEqual([argv[i+1] for i,a in enumerate(argv) if a=='--exclude'], expected)
        for flag in ('--combined','--differ','--missing-on-dst','--error'): self.assertIn(flag,argv)
        self.assertIn('--download',make('/s','/d','/e',Path('/R'),download=True))

class PlanCriteriaTest(unittest.TestCase):
    def setUp(self): self.text=(HERE/'activation_plan_v2.md').read_text()
    def test_2_1_exact_check(self):
        for value in ('rclone check','--combined','--differ','--missing-on-dst','--error','--download','--one-way','--links','--exclude-from'): self.assertIn(value,self.text)
    def test_2_4_checkpoint(self):
        for value in ('write pause','final catch-up','checked inventory','287','100 MB/s','Drive reads','fresh backup with warnings','no waiver'): self.assertIn(value,self.text)
    def test_4_1_fresh_history(self):
        for value in ('c1a06ea','no issued history was lost','--generation-floor 0','any evidence','STOP'): self.assertIn(value,self.text)
    def test_4_2_deployed_tool(self):
        self.assertIn('/usr/bin/python3 -B "$D/backup_gdrive_status.py"',self.text)
        self.assertIn('903c471f',self.text)
    def test_4_3_deadline_and_progress(self):
        for value in ('strictly before end+13 h','owner','child','progress','barrier'): self.assertIn(value,self.text)
    def test_4_4_failure_branch(self):
        for value in ('transfer failure','diagnose','observed successor','damaged ordering history'): self.assertIn(value,self.text)
    def test_4_5_assertions(self):
        for value in ('caffeinate -i -s /usr/bin/open -W -g','pmset -g assertions','AC'): self.assertIn(value,self.text)
    def test_4_6_orphans(self):
        for pid in ('32906','32913','32914','36233','36258','36259','37109','65807'): self.assertIn(pid,self.text)
        self.assertIn('immediately before 3.1',self.text)
    def test_4_7_retirement(self):
        for value in ('bootout','disable','print-disabled','fresh scheduled-path completion','old sync'): self.assertIn(value,self.text)
    def test_5_2_build_and_schedule(self):
        for value in ('stage_gdrive_release.sh','build_gdrive_applet.sh','/usr/bin/cmp','bundle_manifest','enabled','RunAtLoad=false','21600','login'): self.assertIn(value,self.text)
    def test_5_3_order_and_stop(self):
        self.assertIn(ORDER,self.text)
        for value in ('[OPERATOR GO]','[OPERATOR CLICK]','false green','unsupported recovery evidence','HEARTBEAT-FAILED','No Allow prompt'): self.assertIn(value,self.text)

class ErratumTest(unittest.TestCase):
    def test_current_lines(self):
        text=(HERE/'erratum.md').read_text()
        self.assertIn('time.sleep(0.01)',text); self.assertIn('json.loads',text)
        self.assertIn('atomic',text); self.assertIn('a091aec',text)

class PinsTest(unittest.TestCase):
    def test_supersedes_lineage_and_current_bytes(self):
        pins=json.loads((HERE/'pins_v2.json').read_text())
        self.assertEqual(pins['supersedes']['sha256'],'b24014eaffb19434922a67790bbe54753253f5461686b473779a03259bae6d68')
        self.assertEqual([x['sha256'][:8] for x in pins['test_hash_lineage'][:4]],['766509ab','b7649387','6eba5860','f9547a3f'])
        names={x['path'] for x in pins['files']}
        for name in ('tools/launchd/stage_gdrive_release.sh','tools/launchd/build_gdrive_applet.sh','tools/backup_mirror.excludes','tools/launchd/com.rhu.memit-gdrive-backup.plist','tools/test_backup_gdrive.py','tools/test_backup_gdrive_addendum.py'):
            self.assertIn(name,names)
        for item in pins['files']:
            self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])

if __name__=='__main__': unittest.main(verbosity=2)
