"""T370: `icm21_check.py moves --stage post` takes one observed unit manifest per moved unit.

Each case runs the real main() over the Step 204 fixture of test_icm21_moves_cli.py, with the
fixture's observed leaves split across several unit_manifest documents.
"""
import unittest

from pathlib import Path
import errno

import fault_kit as FK
from test_icm21_moves_cli import MovesCase, dumps, named, open_fds, snapshot

REFUSED_BY_PRE = '--observed is required by --stage post and refused by --stage pre'


class ObservedMany(MovesCase):
    def observed(self, groups, documents=None):
        """Publish the fixture and one observed file per group of leaf indexes; their paths."""
        self.fx.publish()
        paths = []
        for number, group in enumerate(groups, 1):
            path = self.fx.custody / ('observed-%d.json' % number)
            document = {'schema_version': 1, 'root': str(self.fx.root / 'dest'),
                        'leaves': [self.fx.observed_leaves[index] for index in group],
                        'git_roots': []}
            path.write_bytes(dumps((documents or {}).get(number, document)))
            paths.append(str(path))
        return paths

    def run_many(self, paths, stage='post'):
        argv = self.fx.argv(stage, observed=False)
        for path in paths:
            argv += ['--observed', path]
        return self.main(argv)

    def assertRefusedMany(self, paths, stage='post'):
        code, result = self.run_many(paths, stage)
        self.assertEqual((code, sorted(result)), (2, ['reason', 'status']), result)
        self.assertEqual(result['status'], 'UNVERIFIED')
        self.assertNotIn('\n', result['reason'])
        return result['reason']

    def test_one_file_per_unit_passes_as_one_file_of_all(self):
        whole = self.run_stage('post')
        self.assertEqual(whole, (0, {'status': 'PASS', 'stage': 'post', 'entry': 'E-1',
                                     'findings': []}))
        for groups in ([[0], [1], [2], [3]], [[0, 1], [2, 3]], [[3], [0, 2], [1]]):
            with self.subTest(groups=groups):
                self.assertEqual(self.run_many(self.observed(groups)), whole)

    def test_the_union_of_the_leaves_is_checked(self):
        # [LAW:behavior-not-structure] Judge the real retained findings across partitions.
        # A changed byte in one file is the one-file FAIL; a unit left out is not a PASS.
        self.fx.observed_leaves[2]['sha256'] = '9' * 64
        whole = self.run_stage('post')
        self.assertEqual(whole[0], 1, whole)
        self.assertEqual(self.run_many(self.observed([[0], [1], [2], [3]])), whole)
        self.fx.observed_leaves[2]['sha256'] = self.fx.leaves[2]['sha256']
        self.fx.observed = {'schema_version': 1,
                            'leaves': [self.fx.observed_leaves[index] for index in (0, 1, 3)]}
        whole = self.run_stage('post')
        self.assertNotEqual(whole[0], 0, whole)
        self.fx.observed = None
        self.assertEqual(self.run_many(self.observed([[0], [1], [3]])), whole)

    def test_a_leaf_in_two_files_refuses_naming_both(self):
        paths = self.observed([[0, 1], [2], [1, 3]])
        reason = self.assertRefusedMany(paths)
        self.assertEqual(reason, '%r: names the leaf %s that %s also names'
                         % (paths[2], self.fx.observed_leaves[1]['source'], paths[0]))

    def test_one_file_given_twice_refuses_naming_it_twice(self):
        path = self.observed([[0, 1, 2, 3]])[0]
        reason = self.assertRefusedMany([path, path])
        self.assertEqual(reason, '%r: names the leaf %s that %s also names'
                         % (path, self.fx.observed_leaves[0]['source'], path))

    def test_a_leaf_in_two_later_files_refuses_naming_both(self):
        paths = self.observed([[0], [1, 2], [2, 3]])
        self.assertEqual(self.assertRefusedMany(paths),
                         '%r: names the leaf %s that %s also names'
                         % (paths[2], self.fx.observed_leaves[2]['source'], paths[1]))

    def test_a_leaf_repeated_inside_one_file_stays_a_check_retained_finding(self):
        paths = self.observed([[0, 1, 1, 2, 3]])
        code, result = self.run_many(paths)
        self.assertEqual(code, 2, result)
        self.assertEqual([item['reason'] for item in result['findings']],
                         ['observed duplicate leaf source'])

    def test_each_file_must_be_a_unit_manifest_document(self):
        for document in ([], {'leaves': []}, {'schema_version': 1}, {'schema_version': 1,
                         'leaves': {}}, {'schema_version': 1, 'leaves': [[]]},
                         {'schema_version': 1, 'leaves': [{'kind': 'file'}]},
                         {'schema_version': 1, 'leaves': [{'source': 7}]}):
            for groups in ([[0, 1], [2, 3]], [[0], [1], [2, 3]]):
                with self.subTest(document=document, files=len(groups)):
                    paths = self.observed(groups, documents={len(groups): document})
                    self.assertEqual(self.assertRefusedMany(paths),
                                     '%r: is not a unit manifest document' % paths[-1])

    def test_files_with_two_schema_versions_refuse(self):
        paths = self.observed([[0, 1], [2, 3]], documents={2: {
            'schema_version': True, 'leaves': [self.fx.observed_leaves[2]]}})
        self.assertEqual(self.assertRefusedMany(paths),
                         '%r: has a schema_version other than that of %s' % (paths[1], paths[0]))

    def test_third_file_with_another_schema_version_refuses(self):
        paths = self.observed([[0], [1], [2, 3]], documents={3: {
            'schema_version': True, 'leaves': self.fx.observed_leaves[2:4]}})
        self.assertEqual(self.assertRefusedMany(paths),
                         '%r: has a schema_version other than that of %s' % (paths[2], paths[0]))

    def test_one_observed_file_works_as_before(self):
        self.assertEqual(self.run_stage('post'),
                         (0, {'status': 'PASS', 'stage': 'post', 'entry': 'E-1',
                              'findings': []}))
        self.fx.observed_leaves[0]['sha256'] = '9' * 64
        code, result = self.run_stage('post')
        self.assertEqual((code, self.reasons(result)),
                         (1, ['C-MOVE: target differs from the admitted leaf in sha256']))
        # Its schema_version still reaches check_retained, which judges it.
        self.fx.observed = {'schema_version': 2, 'leaves': self.fx.observed_leaves}
        code, result = self.run_stage('post')
        self.assertEqual((code, self.reasons(result)), (2, ['observed schema_version is not 1']))

    def test_pre_stage_refuses_any_observed(self):
        for groups in ([[0, 1, 2, 3]], [[0, 1], [2, 3]]):
            with self.subTest(files=len(groups)):
                self.assertIn(REFUSED_BY_PRE,
                              self.assertRefusedMany(self.observed(groups), stage='pre'))

    def test_post_stage_still_requires_an_observed(self):
        self.fx.publish()
        self.assertIn(REFUSED_BY_PRE, self.assertRefusedMany([]))

    def test_every_observed_file_is_read_without_following_links(self):
        for index in range(2):
            with self.subTest(index=index):
                self.setUp()
                paths = self.observed([[0, 1], [2, 3]])
                path = Path(paths[index])
                with FK.swap_for_symlink('open', 1, path, self.fx.decoy / 'file',
                                         match=named(path.name)):
                    reason = self.assertRefusedMany(paths)
                self.assertEqual(reason,
                                 '%r: Too many levels of symbolic links [ELOOP]' % str(path))

    def test_later_observed_read_error_refuses_and_closes_descriptors(self):
        paths = self.observed([[0, 1], [2, 3]])
        before = open_fds()
        with FK.inject_oserror('open', 1, errno.EIO, match=named(Path(paths[1]).name)):
            self.assertEqual(self.assertRefusedMany(paths),
                             '%r: Input/output error [EIO]' % paths[1])
        self.assertEqual(open_fds(), before)

    def test_union_reads_leave_files_and_descriptors_unchanged(self):
        paths = self.observed([[0], [1], [2], [3]])
        before, descriptors = snapshot(self.fx.base), open_fds()
        self.assertEqual(self.run_many(paths)[0], 0)
        self.assertEqual(snapshot(self.fx.base), before)
        self.assertEqual(open_fds(), descriptors)


if __name__ == '__main__':
    unittest.main()
