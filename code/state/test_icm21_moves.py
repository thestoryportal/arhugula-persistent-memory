"""validate_move rejects an unsafe move before anything runs (plan Step 202, SPEC.md:206).

Every fixture is an in-memory wire value under invented absolute roots: the function
under test is pure, so no case creates, reads or writes a file.
"""
import copy
import sys
import unittest

import icm21_check
import icm21_moves
from icm21_moves import validate_move


M = '/fixture/m'
P = '/fixture/p'
SHA = 'a' * 64
UNIT = M + '/projects/unit'
TARGET = M + '/experiments/c10r/runs/unit'


def move(**changes):
    value = {'id': 'MV-001', 'prd_ids': ['ICM-R4'], 'action': 'MOVE', 'source': UNIT,
             'target': TARGET, 'kind': 'directory', 'bytes': 3, 'before_sha256': SHA,
             'source_manifest': {'path': P + '/manifests/MV-001.json', 'sha256': SHA},
             'lane': 'lane-a', 'reader_check_ids': []}
    value.update(changes)
    return value


def leaf(source, kind='file', link_text=None, inode=1, nlink=1):
    return {'source': source, 'kind': kind, 'bytes': 3, 'sha256': SHA,
            'link_text': link_text, 'device': 7, 'inode': inode, 'nlink': nlink}


def facts(**changes):
    value = {'other_moves': (), 'existing_paths': frozenset({UNIT}),
             'run_units': (), 'leaves': (leaf(UNIT + '/a.txt'),)}
    value.update(changes)
    return value


def run(candidate=None, roots=(M, P), **changes):
    return validate_move(move() if candidate is None else candidate, roots, **facts(**changes))


# Filesystem and process audit events (sys.addaudithook) recorded while a case runs.
EVENTS = []
RECORDING = []


def audit(event, args):
    if RECORDING and (event == 'open' or event.split('.')[0] in
                      ('os', 'shutil', 'subprocess', 'tempfile', 'pathlib', 'glob')):
        EVENTS.append(event)


sys.addaudithook(audit)


class ValidateMoveTest(unittest.TestCase):

    def assertOnly(self, findings, status, fragment):
        """Exactly one finding, of this status, whose reason names the rule."""
        self.assertEqual(len(findings), 1, findings)
        self.assertEqual(findings[0]['status'], status, findings)
        self.assertIn(fragment, findings[0]['reason'])
        icm21_check.validate_wire('Finding', findings[0], icm21_check.audit_schema(), {})

    def test_clean_move_is_admitted(self):
        self.assertEqual(run(), ())
        self.assertEqual(run(roots=(icm21_moves.PurePosixPath(M),)), ())

    def test_root_escape(self):
        self.assertOnly(run(move(target='/elsewhere/runs/unit')), 'FAIL', 'escapes')
        self.assertOnly(run(move(source='/elsewhere/unit'),
                            leaves=(leaf('/elsewhere/unit/a.txt'),)), 'FAIL', 'escapes')
        self.assertOnly(run(move(target=M)), 'FAIL', 'escapes')
        found = run(roots=())
        self.assertEqual(len(found), 2, found)
        self.assertTrue(all(item['status'] == 'FAIL' and 'escapes' in item['reason']
                            for item in found), found)

    def test_existing_target(self):
        self.assertOnly(run(existing_paths=frozenset({UNIT, TARGET})), 'FAIL', 'already exists')

    def test_wildcard_and_angle_bracket_paths(self):
        for char in '*?[]<>':
            with self.subTest(char=char, side='target'):
                self.assertOnly(run(move(target=TARGET + char)), 'FAIL', 'wildcard')
            with self.subTest(char=char, side='source'):
                found = run(move(source=UNIT + char), leaves=(leaf(UNIT + char + '/a'),),
                            existing_paths=frozenset())
                self.assertOnly(found, 'FAIL', 'wildcard')

    def test_target_inside_a_move_source(self):
        other = move(id='MV-002', source=M + '/experiments', target=P + '/held')
        self.assertOnly(run(other_moves=(other,)), 'FAIL', "inside another move's source")
        equal = move(id='MV-002', source=TARGET, target=P + '/held')
        self.assertOnly(run(other_moves=(equal,)), 'FAIL', "inside another move's source")
        self.assertOnly(run(move(target=UNIT + '/nested')), 'FAIL', 'its own source')

    def test_target_collision_with_another_move(self):
        for other_target in (TARGET, TARGET + '/inner', M + '/experiments/c10r/runs'):
            with self.subTest(other_target=other_target):
                other = move(id='MV-002', source=M + '/projects/other', target=other_target)
                self.assertOnly(run(other_moves=(other,)), 'FAIL', 'collides')
        unrelated = move(id='MV-002', source=M + '/projects/other', target=M + '/runs2/x')
        self.assertEqual(run(other_moves=(unrelated,)), ())
        twice = (move(source=M + '/projects/b', target=P + '/b'),
                 move(source=M + '/projects/c', target=P + '/c'))
        self.assertOnly(run(other_moves=twice), 'FAIL', 'duplicate move ID')

    def test_link_crossing_the_unit_boundary(self):
        inside = (leaf(UNIT + '/a.txt'), leaf(UNIT + '/sub/link', 'symlink', '../a.txt'),
                  leaf(UNIT + '/up', 'symlink', 'sub/..'))
        self.assertEqual(run(leaves=inside), ())
        crossing = {
            'relative escape': (leaf(UNIT + '/l', 'symlink', '../other/a.txt'),),
            'absolute text': (leaf(UNIT + '/l', 'symlink', UNIT + '/a.txt'),),
            'excursion through the unit name': (leaf(UNIT + '/l', 'symlink', '../unit/a'),),
            'through an inner link': (leaf(UNIT + '/sub/a', 'symlink', '..'),
                                      leaf(UNIT + '/b', 'symlink', 'sub/a/..')),
        }
        for name, leaves in crossing.items():
            with self.subTest(name):
                self.assertOnly(run(leaves=leaves), 'FAIL', 'crosses the unit boundary')
        self.assertOnly(run(leaves=(leaf(UNIT + '/x', 'symlink', 'x'),)), 'FAIL', 'ambiguous link')
        via_absolute = run(leaves=(leaf(UNIT + '/a', 'symlink', '/elsewhere'),
                                   leaf(UNIT + '/b', 'symlink', 'a/x')))
        self.assertEqual(len(via_absolute), 2, via_absolute)
        self.assertTrue(all('crosses the unit boundary' in item['reason']
                            for item in via_absolute), via_absolute)
        self.assertOnly(run(leaves=(leaf(UNIT + '/l', 'symlink', None),)), 'FAIL', 'Malformed')
        link_unit = move(kind='symlink')
        self.assertOnly(run(link_unit, leaves=(leaf(UNIT, 'symlink', 'unit2'),)),
                        'FAIL', 'crosses the unit boundary')

    def test_hard_link_crossing_the_unit_boundary(self):
        self.assertOnly(run(leaves=(leaf(UNIT + '/a', nlink=2),)), 'FAIL', 'hard link')
        both = (leaf(UNIT + '/a', inode=9, nlink=2), leaf(UNIT + '/b', inode=9, nlink=2))
        self.assertEqual(run(leaves=both), ())

    def test_leaf_outside_the_unit_is_refused(self):
        self.assertOnly(run(leaves=(leaf(M + '/projects/unit2/a'),)), 'FAIL', 'Malformed')

    def test_moved_object_missing_from_its_manifest(self):
        single = move(kind='file', source=UNIT + '/a.txt', target=TARGET + '.txt')
        self.assertEqual(run(single, leaves=(leaf(UNIT + '/a.txt'),),
                             existing_paths=frozenset()), ())
        self.assertOnly(run(single, leaves=()), 'UNVERIFIED', 'lacks the moved object')

    def test_split_run_unit(self):
        run_unit = M + '/projects'
        self.assertOnly(run(run_units=(run_unit,)), 'FAIL', 'splits run unit')
        self.assertEqual(run(run_units=(UNIT,)), ())
        self.assertEqual(run(run_units=(UNIT + '/r1',)), ())
        split = move(action='SPLIT_FILES')
        for unit in (UNIT, UNIT + '/r1'):
            with self.subTest(unit=unit):
                self.assertOnly(run(split, run_units=(unit,)), 'FAIL', 'splits run unit')

    def test_rows_that_emit_no_action(self):
        for action in ('KEEP', 'HOLD', 'FOLLOW_PARENT', 'RETAIN_CONTAINER'):
            with self.subTest(action=action):
                self.assertOnly(run(move(action=action)), 'FAIL', 'emits no executable action')

    def test_missing_facts_are_unverified_not_pass(self):
        for name in ('other_moves', 'existing_paths', 'run_units', 'leaves'):
            with self.subTest(name=name):
                self.assertOnly(run(**{name: None}), 'UNVERIFIED', name)
        found = validate_move(move(), (M, P))
        self.assertEqual(len(found), 4)
        self.assertEqual({item['status'] for item in found}, {'UNVERIFIED'})

    def test_malformed_input_is_refused(self):
        bad_moves = [move(extra=1), move(source='projects/unit'), move(target=M + '/a/../b'),
                     move(action='MOVE_ALL'), 'MV-001']
        for bad in bad_moves:
            with self.subTest(bad=bad):
                self.assertOnly(run(bad), 'FAIL', 'Malformed')
        for roots in (('fixture/m',), (M + '/..',), (M, 7)):
            with self.subTest(roots=roots):
                self.assertOnly(run(roots=roots), 'FAIL', 'Malformed')
        cases = {'other_moves': (move(id='MV-002', kind='dir'),),
                 'existing_paths': frozenset({'rel/path'}), 'run_units': ('/a/./b',),
                 'leaves': (dict(leaf(UNIT + '/a'), extra=1),)}
        for name, value in cases.items():
            with self.subTest(name=name):
                self.assertOnly(run(**{name: value}), 'FAIL', 'Malformed')

    def test_pure_no_filesystem_access_and_no_target_decision(self):
        cases = [((move(), (M, P)), facts()),
                 ((move(target='/elsewhere/x'), (M,)), facts()),
                 ((move(), (M, P)), facts(leaves=(leaf(UNIT + '/l', 'symlink', '../x'),))),
                 ((move(), (M, P)), facts(run_units=(M + '/projects',))),
                 ((move(), (M, P)), {})]
        for (candidate, roots), extra in cases:
            before = copy.deepcopy((candidate, roots, extra))
            EVENTS.clear()
            RECORDING.append(True)
            self.addCleanup(RECORDING.clear)
            try:
                found = validate_move(candidate, roots, **extra)
            finally:
                RECORDING.clear()
            self.assertEqual(EVENTS, [])
            self.assertEqual((candidate, roots, extra), before, 'inputs were changed')
            self.assertIs(type(found), tuple)
            for item in found:
                icm21_check.validate_wire('Finding', item, icm21_check.audit_schema(), {})
        self.assertEqual(sorted(found[0]), sorted(['id', 'status', 'prd_ids', 'paths',
                                                    'evidence', 'reason', 'previous_finding',
                                                    'resolution_receipt']))

    def assertReasons(self, findings, *fragments):
        """One FAIL finding per fragment, in any order, and nothing else."""
        self.assertEqual(len(findings), len(fragments), findings)
        for fragment in fragments:
            self.assertEqual(sum(fragment in item['reason'] for item in findings), 1,
                             (fragment, findings))
        self.assertEqual({item['status'] for item in findings}, {'FAIL'}, findings)

    def test_duplicate_leaf_records(self):
        entry = leaf(UNIT + '/a', inode=9, nlink=2)
        self.assertReasons(run(leaves=(entry, dict(entry))), 'duplicate leaf record', 'hard link')
        bad = leaf(UNIT + '/link', 'symlink', '../outside')
        safe = leaf(UNIT + '/link', 'symlink', 'a.txt')
        self.assertReasons(run(leaves=(bad, safe)), 'duplicate leaf record', 'crosses the unit')
        self.assertReasons(run(leaves=(safe, bad)), 'duplicate leaf record')

    def test_iterators_give_the_same_findings_as_lists(self):
        cases = {'other_moves': (move(id='MV-002', source=TARGET, target=P + '/held'),),
                 'existing_paths': (UNIT, TARGET), 'run_units': (M + '/projects',),
                 'leaves': (leaf(UNIT + '/a.txt'), leaf(UNIT + '/link', 'symlink', '../out'))}
        for name, value in cases.items():
            with self.subTest(name=name):
                listed = run(**{name: list(value)})
                self.assertEqual(len(listed), 1, listed)
                self.assertEqual(run(**{name: (item for item in value)}), listed)
        listed = run(**{name: list(value) for name, value in cases.items()})
        self.assertEqual(len(listed), 4, listed)
        self.assertEqual(run(**{name: iter(value) for name, value in cases.items()}), listed)

    def test_move_kind_must_match_the_leaf_kind_at_its_source(self):
        self.assertReasons(run(move(kind='symlink'), leaves=(leaf(UNIT),)), 'kind disagrees')
        self.assertReasons(run(move(kind='file'), leaves=(leaf(UNIT, 'symlink', 'a'),)),
                           'kind disagrees', 'crosses the unit')
        self.assertReasons(run(leaves=(leaf(UNIT),)), 'kind disagrees')
        self.assertReasons(run(move(kind='git-root'), leaves=(leaf(UNIT),)), 'kind disagrees')
        self.assertEqual(run(move(kind='file'), leaves=(leaf(UNIT),)), ())

    def test_git_root_is_a_container(self):
        git_root = move(kind='git-root')
        self.assertEqual(run(git_root), ())
        self.assertEqual(run(git_root, leaves=()), ())
        self.assertReasons(run(git_root, leaves=(leaf(UNIT + '/l', 'symlink', '../x'),)),
                           'crosses the unit')
        self.assertReasons(run(git_root, leaves=(leaf(UNIT + '/a', nlink=2),)), 'hard link')

    def test_source_or_target_equal_to_any_admitted_root(self):
        nested = ('/fixture', M, P)
        held = move(source=M, target=P + '/held')
        for roots in ((M, P), nested):
            with self.subTest(roots=roots):
                self.assertOnly(run(held, roots=roots), 'FAIL', 'equals admitted root')
                self.assertOnly(run(move(target=M), roots=roots), 'FAIL', 'equals admitted root')
        self.assertEqual(run(roots=nested), ())

    def test_target_equal_to_its_own_source(self):
        self.assertOnly(run(move(target=UNIT), existing_paths=frozenset()),
                        'FAIL', 'its own source')

    def test_hard_link_identity_is_device_and_inode(self):
        cases = {'same inode, distinct devices': dict(leaf(UNIT + '/b', inode=9, nlink=2), device=8),
                 'distinct inodes, same device': leaf(UNIT + '/b', inode=10, nlink=2)}
        for name, other in cases.items():
            with self.subTest(name):
                found = run(leaves=(leaf(UNIT + '/a', inode=9, nlink=2), other))
                self.assertEqual(len(found), 2, found)
                self.assertTrue(all('hard link' in item['reason'] for item in found), found)


if __name__ == '__main__':
    unittest.main()
