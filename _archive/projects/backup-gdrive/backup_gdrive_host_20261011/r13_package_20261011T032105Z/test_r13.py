"""MB45 preregistered controls. Git writes stay in /private/tmp, origin is local bare."""
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
BASELINE = os.environ.get('R13_BASELINE') == '1'

class CandidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='r13_git_', dir='/private/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root/'repo'; self.repo.mkdir()
        self.pkg = self.root/'package'; self.pkg.mkdir()
        self.origin = self.root/'origin.git'
        self.git('init', '--bare', str(self.origin))
        self.git('init', '-b', 'master')
        self.git('config', 'user.name', 'MB45 fixture')
        self.git('config', 'user.email', 'fixture@invalid.example')
        (self.repo/'unrelated.txt').write_text('base\n')
        (self.repo/'.gitignore').write_text('ignored/\n')
        (self.repo/'tools').mkdir()
        (self.repo/'tools/noop.sh').write_text('unchanged\n')
        self.git('add', '.'); self.git('commit', '-m', 'base')
        self.git('remote', 'add', 'origin', str(self.origin))
        self.git('push', 'origin', 'master')
        self.base = self.git('rev-parse', 'origin/master').strip()
        self.git('checkout', '-b', 'source')
        self.paths = ['results/fixture/evidence.txt', 'tools/backup.sh', 'tools/noop.sh']
        for name in self.paths[:-1]:
            path = self.repo/name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name+'\n')
        (self.repo/'unrelated.txt').write_text('source-only drift\n')
        self.git('add', '.'); self.git('commit', '-m', 'reviewed source')
        self.source = self.git('rev-parse', 'HEAD').strip()
        (self.pkg/'scope_allowlist.txt').write_text('\n'.join(self.paths)+'\n')
        (self.pkg/'scope_unchanged.txt').write_text('tools/noop.sh\n')
        pins = ''.join(hashlib.sha256(self.git_bytes('show', self.source+':'+p)).hexdigest()+'  '+p+'\n' for p in self.paths)
        (self.pkg/('pins_v3.sha256' if BASELINE else 'pins_v4.sha256')).write_text(pins)
        shutil.copy2(HERE/('before/candidate.py' if BASELINE else 'candidate.py'), self.pkg/'candidate.py')
        self.target = self.root/'candidate'
        self.receipt = self.pkg/'operational_checks/verified_commit_sha.txt'
        value = self.call('create', str(self.repo), self.source, str(self.target))
        self.assertEqual(value.returncode, 0, value.stdout+value.stderr)

    def git_bytes(self, *args, cwd=None):
        return subprocess.run(['/usr/bin/git', '-C', str(cwd or self.repo), *args], check=True, capture_output=True).stdout

    def git(self, *args, cwd=None):
        return self.git_bytes(*args, cwd=cwd).decode()

    def call(self, mode, *args):
        # Behavioral RED adapter: K12 has only working-tree verify. Exact K12 code runs.
        if BASELINE and mode in ('verify-staged', 'verify-commit'):
            mode, args = 'verify', args[:2]
        return subprocess.run(['/usr/bin/python3', '-B', str(self.pkg/'candidate.py'), mode, *args], text=True, capture_output=True)

    def staged(self): return self.call('verify-staged', str(self.target), self.source)
    def committed(self, sha): return self.call('verify-commit', str(self.target), self.source, sha)

    def reject(self, value, diagnostic):
        self.assertEqual(value.returncode, 1, value.stdout+value.stderr)
        self.assertIn(diagnostic, value.stderr)

    def hide(self, path):
        item = self.target/path; data = item.read_bytes()
        item.write_bytes(b'contamination\n')
        self.git('add', '--', path, cwd=self.target)
        item.write_bytes(data)

    def hide_committed(self, path):
        item = self.target/path; data = item.read_bytes()
        item.write_bytes(b'committed contamination\n')
        self.git('add', '--', path, cwd=self.target)
        self.git('commit', '-m', 'contaminated', cwd=self.target)
        sha = self.git('rev-parse', 'HEAD', cwd=self.target).strip()
        item.write_bytes(data)
        return sha

    def commit(self):
        self.git('commit', '-m', 'candidate', cwd=self.target)
        return self.git('rev-parse', 'HEAD', cwd=self.target).strip()

    def test_staged_out_of_scope_hidden(self):
        self.hide('unrelated.txt'); self.reject(self.staged(), 'scope index tree mismatch')

    def test_staged_allowlisted_corruption_hidden(self):
        self.hide('tools/backup.sh'); self.reject(self.staged(), 'scope index tree mismatch')

    def test_committed_out_of_scope_hidden(self):
        self.reject(self.committed(self.hide_committed('unrelated.txt')), 'scope commit tree mismatch')

    def test_committed_allowlisted_corruption_hidden(self):
        self.reject(self.committed(self.hide_committed('tools/backup.sh')), 'scope commit tree mismatch')

    def test_index_wrong_mode_hidden(self):
        self.git('update-index', '--chmod=+x', 'tools/backup.sh', cwd=self.target)
        self.reject(self.staged(), 'scope index tree mismatch')

    def test_commit_wrong_mode_hidden(self):
        self.git('update-index', '--chmod=+x', 'tools/backup.sh', cwd=self.target)
        self.reject(self.committed(self.commit()), 'scope commit tree mismatch')

    def test_wrong_parent(self):
        tree = self.git('write-tree', cwd=self.target).strip()
        sha = self.git('commit-tree', tree, '-p', self.source, '-m', 'wrong parent', cwd=self.target).strip()
        self.reject(self.committed(sha), 'parent must be origin/master')

    def test_merge_commit_two_parents(self):
        tree = self.git('write-tree', cwd=self.target).strip()
        sha = self.git('commit-tree', tree, '-p', self.base, '-p', self.source, '-m', 'merge', cwd=self.target).strip()
        self.reject(self.committed(sha), 'parent must be origin/master')

    def sha_file(self, sha):
        self.receipt.parent.mkdir(exist_ok=True); self.receipt.write_text(sha+'\n')

    def test_pr_head_different(self):
        self.sha_file(self.source)
        self.reject(self.call('verify-pr-head', str(self.receipt), self.base, self.source), 'PR head binding mismatch')

    def test_remote_head_different(self):
        self.sha_file(self.source)
        self.reject(self.call('verify-pr-head', str(self.receipt), self.source, self.base), 'PR head binding mismatch')

    def test_malformed_head(self):
        self.sha_file(self.source)
        self.reject(self.call('verify-pr-head', str(self.receipt), 'g'*40, self.source), 'full 40-hex SHA')

    def test_clean_staged(self):
        value = self.staged(); self.assertEqual(value.returncode, 0, value.stdout+value.stderr)

    def test_clean_commit_receipt(self):
        sha = self.commit(); value = self.committed(sha)
        self.assertEqual(value.returncode, 0, value.stdout+value.stderr)
        self.assertTrue(self.receipt.is_file(), 'K12 never writes a verified commit receipt')
        self.assertEqual(self.receipt.read_text(), sha+'\n')

    def test_clean_pr_binding(self):
        self.sha_file(self.source)
        value = self.call('verify-pr-head', str(self.receipt), self.source, self.source)
        self.assertEqual(value.returncode, 0, value.stdout+value.stderr)

    def test_clean_all_three_modes(self):
        value = self.staged(); self.assertEqual(value.returncode, 0, value.stdout+value.stderr)
        sha = self.commit(); value = self.committed(sha)
        self.assertEqual(value.returncode, 0, value.stdout+value.stderr)
        self.assertTrue(self.receipt.is_file(), 'verified SHA receipt must connect commit to PR checks')
        value = self.call('verify-pr-head', str(self.receipt), sha, sha)
        self.assertEqual(value.returncode, 0, value.stdout+value.stderr)

    def test_commit_uses_objects_despite_working_tree_corruption(self):
        sha = self.commit(); (self.target/'tools/backup.sh').write_text('dirty after commit\n')
        value = self.committed(sha); self.assertEqual(value.returncode, 0, value.stdout+value.stderr)

    def test_index_complete_path_set(self):
        (self.target/'extra.txt').write_text('extra\n'); self.git('add', 'extra.txt', cwd=self.target)
        self.reject(self.staged(), 'scope index tree mismatch')

    def test_commit_complete_path_set(self):
        self.git('rm', 'unrelated.txt', cwd=self.target)
        sha = self.commit(); (self.target/'unrelated.txt').write_text('base\n')
        self.reject(self.committed(sha), 'scope commit tree mismatch')

    def test_ignored_untracked_rejected(self):
        (self.target/'ignored').mkdir(); (self.target/'ignored/file').write_text('untracked\n')
        self.reject(self.staged(), 'untracked files')

    def test_working_tree_must_equal_index(self):
        (self.target/'tools/backup.sh').write_text('dirty\n')
        self.reject(self.staged(), 'working tree differs from index')


ORDER = [
    ('1.1-candidate', 'capture r13-candidate-create /bin/sh "$R/make_backup_candidate.sh" create "$W" "$SOURCE_COMMIT" "$I"', 'MAESTRO-GO'),
    ('1.1-verify-staged', 'capture r13-verify-staged /bin/sh "$R/make_backup_candidate.sh" verify-staged "$I" "$SOURCE_COMMIT"', 'READ-ONLY'),
    ('1.1-commit', 'capture r13-candidate-commit /usr/bin/git -C "$I" commit -m "Google Drive backup r13 candidate"', 'MAESTRO-GO'),
    ('1.1-verify-commit', 'capture r13-verify-commit /bin/sh "$R/make_backup_candidate.sh" verify-commit "$I" "$SOURCE_COMMIT" "$CANDIDATE_COMMIT" --receipt-file "$VERIFIED_SHA_FILE"', 'RECEIPT-WRITE'),
    ('1.1-push', 'capture r13-candidate-push /usr/bin/git -C "$I" push origin backup-gdrive-r12', 'MAESTRO-GO'),
    ('1.1-pr', 'capture pr-create /opt/homebrew/bin/gh pr create --base master --head backup-gdrive-r12 --title "Google Drive backup release and activation evidence" --body-file "$R/pr_body.md"', 'MAESTRO-GO'),
    ('1.1-pr-observe', 'capture r13-pr-head /opt/homebrew/bin/gh pr view "$PR" --json headRefOid', 'READ-ONLY'),
    ('1.1-remote-observe', 'capture r13-remote-head /usr/bin/git -C "$I" ls-remote origin refs/heads/backup-gdrive-r12', 'READ-ONLY'),
    ('1.1-verify-pr-head', 'capture r13-verify-pr-head /usr/bin/python3 -B "$R/gate_binding.py" heads "$VERIFIED_SHA_FILE" "$R/commands/r13-pr-head/stdout.txt" "$R/commands/r13-remote-head/stdout.txt"', 'READ-ONLY'),
    ('1.1-gate', 'capture r13-merge-apply /usr/bin/env LLMDB_ROOT="$I" /usr/bin/python3 -B "$I/tools/git_merge_gate.py" "$PR" --apply', 'OPERATOR-GO'),
    ('1.1-gate-head', 'capture r13-gate-head /usr/bin/python3 -B "$R/gate_binding.py" gate "$VERIFIED_SHA_FILE" "$R/commands/r13-merge-apply/stdout.txt"', 'READ-ONLY'),
]

def plan(rows=ORDER):
    return '# Drive r13 activation plan v4\n\n'+''.join('<!-- row '+name+' marker='+marker+' -->\n```bash\n'+command+'\n```\n\n' for name, command, marker in rows)

class PlanOrderTest(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('r13_check', HERE/('before/check_plan.py' if BASELINE else 'check_plan.py'))
        self.checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.checker)

    def codes(self, text): return [x['code'] for x in self.checker.check(text, probe=lambda p: True)]

    def test_all_rows_in_order(self): self.assertEqual(self.codes(plan()), [])

    def test_out_of_order(self):
        rows = list(ORDER); rows[2], rows[3] = rows[3], rows[2]
        self.assertIn('CANDIDATE_ORDER', self.codes(plan(rows)))

    def test_empty_required_row(self):
        self.assertIn('CANDIDATE_ROW', self.codes(plan().replace(ORDER[3][1], '# no verification')))

    def test_head_not_immediately_before_gate(self):
        self.assertIn('CANDIDATE_ORDER', self.codes(plan().replace(ORDER[9][1], 'capture intervening /usr/bin/true\n'+ORDER[9][1])))

    def test_actual_v4_plan(self):
        path = HERE/'activation_plan_v4.md'
        self.assertTrue(path.is_file(), 'K12 has no v4 plan')
        self.assertEqual(self.codes(path.read_text()), [])

for index, (row, _, _) in enumerate(ORDER):
    def missing(self, index=index):
        self.assertIn('CANDIDATE_ROW', self.codes(plan(ORDER[:index]+ORDER[index+1:])))
    setattr(PlanOrderTest, 'test_missing_'+row.replace('.', '_').replace('-', '_'), missing)

class BindingReceiptTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='r13_binding_', dir='/private/tmp'); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.sha = 'a'*40; self.other = 'b'*40
        self.verified = self.root/'sha.txt'; self.verified.write_text(self.sha+'\n')
        self.pr = self.root/'pr.json'; self.pr.write_text(json.dumps({'headRefOid':self.sha})+'\n')
        self.remote = self.root/'remote.txt'; self.remote.write_text(self.sha+'\trefs/heads/backup-gdrive-r12\n')
        self.gate = self.root/'gate.json'; self.gate.write_text(json.dumps({'head_sha':self.sha})+'\n')

    def call(self, mode):
        helper = HERE/('before/gate_binding.py' if BASELINE else 'gate_binding.py')
        args = [str(self.pr), str(self.remote)] if mode == 'heads' else [str(self.gate)]
        return subprocess.run(['/usr/bin/python3', '-B', str(helper), mode, str(self.verified), *args], text=True, capture_output=True)

    def test_observed_heads_pass(self): self.assertEqual(self.call('heads').returncode, 0)
    def test_gate_head_pass(self): self.assertEqual(self.call('gate').returncode, 0)

    def test_observed_remote_wrong(self):
        self.remote.write_text(self.other+'\trefs/heads/backup-gdrive-r12\n')
        value = self.call('heads'); self.assertEqual(value.returncode, 1); self.assertIn('binding mismatch', value.stderr)

    def test_observed_remote_wrong_ref(self):
        self.remote.write_text(self.sha+'\trefs/heads/other\n')
        value = self.call('heads'); self.assertEqual(value.returncode, 1); self.assertIn('remote observation', value.stderr)

    def test_gate_head_wrong(self):
        self.gate.write_text(json.dumps({'head_sha':self.other})+'\n')
        value = self.call('gate'); self.assertEqual(value.returncode, 1); self.assertIn('gate head binding mismatch', value.stderr)

    def test_gate_report_malformed(self):
        self.gate.write_text('{}\n')
        value = self.call('gate'); self.assertEqual(value.returncode, 1); self.assertIn('full 40-hex SHA', value.stderr)

if __name__ == '__main__': unittest.main(verbosity=2)
