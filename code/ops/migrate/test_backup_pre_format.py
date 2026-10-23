"""Independent wire-format cases for backup pre-state evidence."""
import errno
import json
import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch

from ops.migrate import backup_retention as codec, fdsafe


DIGEST = '0123456789abcdef' * 4


def document():
    return {'version': 1, 'destinations': [
        {'root': '/z', 'leaves': [['z', 'file', DIGEST],
                                 ['a', 'symlink', '../target']]},
        {'root': '/a', 'leaves': [['z', 'file', DIGEST]]},
    ]}


def wire(value):
    return json.dumps(value).encode('utf-8')


class FormatTests(unittest.TestCase):
    def refuse(self, data):
        with self.assertRaises(fdsafe.Refusal) as caught:
            codec.parse(data)
        self.assertEqual(caught.exception.errno, errno.EINVAL)
        self.assertEqual(caught.exception.path, 'backup-pre.json')
        self.assertIn('EINVAL:', str(caught.exception))
        self.assertEqual(len(str(caught.exception).splitlines()), 1)

    def test_ordered_round_trip(self):
        expected = document()
        pre = codec.parse(wire(expected))
        self.assertIsInstance(pre, codec.PreState)
        self.assertEqual(tuple(d.root for d in pre.destinations), ('/z', '/a'))
        self.assertEqual(tuple(v.path for v in pre.destinations[0].leaves), ('z', 'a'))
        encoded = codec.encode(pre)
        self.assertIsInstance(encoded, bytes)
        self.assertEqual(json.loads(encoded), expected)
        self.assertEqual(codec.parse(encoded), pre)

    def test_empty_destinations(self):
        expected = {'version': 1, 'destinations': []}
        self.assertEqual(json.loads(codec.encode(codec.parse(wire(expected)))), expected)

    def test_empty_leaves_and_root_slash(self):
        expected = {'version': 1, 'destinations': [{'root': '/', 'leaves': []}]}
        self.assertEqual(json.loads(codec.encode(codec.parse(wire(expected)))), expected)

    def test_symlink_text_is_not_a_digest(self):
        expected = document()
        expected['destinations'][0]['leaves'] = [
            ['link', 'symlink', '../雪/./target\n'],
            ['hex-link', 'symlink', DIGEST], ['file', 'file', DIGEST],
            ['empty-link', 'symlink', '']]
        pre = codec.parse(wire(expected))
        self.assertEqual(pre.destinations[0].leaves[0].value, '../雪/./target\n')
        self.assertNotEqual(pre.destinations[0].leaves[1], pre.destinations[0].leaves[2])
        self.assertEqual(json.loads(codec.encode(pre)), expected)

    def test_nested_last_success_is_evidence(self):
        expected = document()
        expected['destinations'][0]['leaves'][0][0] = 'repo/.last_success'
        self.assertEqual(json.loads(codec.encode(codec.parse(wire(expected)))), expected)

    def test_same_root_distinct_paths(self):
        expected = document()
        expected['destinations'][1] = {'root': '/z', 'leaves': [['b', 'file', DIGEST]]}
        self.assertEqual(json.loads(codec.encode(codec.parse(wire(expected)))), expected)

    def test_checked_state_is_immutable(self):
        pre = codec.parse(wire(document()))
        with self.assertRaises(FrozenInstanceError):
            pre.destinations = ()
        with self.assertRaises(AttributeError):
            pre.destinations[0].root = '/elsewhere'
        with self.assertRaises(AttributeError):
            pre.destinations[0].leaves[0].value = 'changed'
        self.assertIsInstance(pre.destinations, tuple)
        self.assertIsInstance(pre.destinations[0].leaves, tuple)

    def test_constructor_cannot_bypass_parse(self):
        with self.assertRaises(fdsafe.Refusal):
            codec.PreState(wire({'version': 2, 'destinations': []}))

    def test_unexpected_decoder_error_propagates(self):
        with patch.object(codec.json, 'loads', side_effect=RuntimeError('decoder bug')):
            with self.assertRaisesRegex(RuntimeError, 'decoder bug'):
                codec.parse(b'{}')

    def test_duplicate_across_destinations(self):
        value = document()
        value['destinations'][1]['root'] = '/z'
        self.refuse(wire(value))

    def test_duplicate_with_different_kind(self):
        value = document()
        value['destinations'][0]['leaves'][1] = ['z', 'symlink', DIGEST]
        self.refuse(wire(value))

    def test_direct_round_trip(self):
        destinations = (
            codec.Destination('/z', (codec.Leaf('z', 'file', DIGEST),
                                     codec.Leaf('a', 'symlink', '../target'))),
            codec.Destination('/a', (codec.Leaf('z', 'file', DIGEST),)),
        )
        pre = codec.PreState(destinations)
        self.assertEqual(pre.destinations, destinations)
        self.assertEqual(json.loads(codec.encode(pre)), document())
        self.assertEqual(codec.parse(codec.encode(pre)), pre)
        for empty in ((), (codec.Destination('/', ()),)):
            with self.subTest(empty=empty):
                pre = codec.PreState(empty)
                self.assertEqual(pre.destinations, empty)
                self.assertEqual(codec.parse(codec.encode(pre)), pre)

    def refuse_direct(self, destinations, reason):
        with self.assertRaises(fdsafe.Refusal) as caught:
            codec.PreState(destinations)
        self.assertEqual(caught.exception.errno, errno.EINVAL)
        self.assertEqual(caught.exception.path, 'backup-pre.json')
        self.assertEqual(str(caught.exception),
                         "'backup-pre.json': EINVAL: " + reason + ' [EINVAL]')

    def test_direct_container_refusals(self):
        for destinations, reason in (
            ([], 'expected destinations tuple'),
            (None, 'expected destinations tuple'),
            ((('/r', ()),), 'expected Destination'),
            ((None,), 'expected Destination'),
            ((codec.Destination('/r', []),), 'expected leaves tuple'),
            ((codec.Destination('/r', None),), 'expected leaves tuple'),
            ((codec.Destination('/r', (('a', 'file', DIGEST),)),), 'expected Leaf'),
            ((codec.Destination('/r', (None,)),), 'expected Leaf'),
        ):
            with self.subTest(destinations=destinations):
                self.refuse_direct(destinations, reason)

    def test_direct_field_refusals(self):
        class Text(str):
            pass

        leaf = codec.Leaf('a', 'file', DIGEST)
        for root in ('r', '', 12, None, Text('/r')):
            with self.subTest(root=root):
                self.refuse_direct((codec.Destination(root, ()),), 'expected absolute root')
        for field, values, reason in (
            ('path', ('', '/a', 'a//b', 'a/', 'a/./b', 'a/../b', '.', '..',
                      1, None, Text('a')),
             'expected relative leaf path without empty, dot or dotdot components'),
            ('path', ('.last_success',), 'root stamp is not evidence'),
            ('kind', ('dir', 'fifo', None, [], Text('file')), 'unknown leaf kind'),
            ('value', (1, None, Text(DIGEST)), 'expected leaf text'),
            ('value', (DIGEST.upper(), 'a' * 63, 'a' * 65, 'g' * 64, DIGEST + '\n'),
             'expected lowercase sha256'),
        ):
            for value in values:
                with self.subTest(field=field, value=value):
                    invalid = leaf._replace(**{field: value})
                    self.refuse_direct((codec.Destination('/r', (invalid,)),), reason)
        for content in (1, None):
            with self.subTest(link_text=content):
                invalid = codec.Leaf('a', 'symlink', content)
                self.refuse_direct((codec.Destination('/r', (invalid,)),), 'expected leaf text')

    def test_direct_duplicate_refusals(self):
        leaf = codec.Leaf('a', 'file', DIGEST)
        for other in (leaf, codec.Leaf('a', 'symlink', '../target')):
            for destinations in (
                (codec.Destination('/r', (leaf, other)),),
                (codec.Destination('/r', (leaf,)), codec.Destination('/r', (other,))),
            ):
                with self.subTest(destinations=destinations):
                    self.refuse_direct(destinations, 'duplicate root and path')


# [LAW:behavior-not-structure] Each discovery case corrupts one wire fact only.
def refusal_case(location, replacement):
    def test(self):
        value = document()
        if not location:
            value = replacement
        else:
            parent = value
            for key in location[:-1]:
                parent = parent[key]
            parent[location[-1]] = replacement
        self.refuse(wire(value))
    return test


_LEAF = ('destinations', 0, 'leaves', 0)
_CASES = {
    'version_two': (('version',), 2),
    'version_bool': (('version',), True),
    'version_float': (('version',), 1.0),
    'version_string': (('version',), '1'),
    'top_array': ((), []),
    'top_null': ((), None),
    'top_scalar': ((), 1),
    'unknown_top_key': (('extra',), 0),
    'destinations_object': (('destinations',), {}),
    'destinations_null': (('destinations',), None),
    'destination_array': (('destinations', 0), []),
    'destination_null': (('destinations', 0), None),
    'unknown_destination_key': (('destinations', 0, 'extra'), 0),
    'relative_root': (('destinations', 0, 'root'), 'relative'),
    'empty_root': (('destinations', 0, 'root'), ''),
    'root_number': (('destinations', 0, 'root'), 12),
    'root_null': (('destinations', 0, 'root'), None),
    'leaves_object': (('destinations', 0, 'leaves'), {}),
    'leaves_null': (('destinations', 0, 'leaves'), None),
    'leaf_object': (_LEAF, {}),
    'leaf_null': (_LEAF, None),
    'leaf_short': (_LEAF, ['z', 'file']),
    'leaf_long': (_LEAF, ['z', 'file', DIGEST, 1]),
    'path_empty': (_LEAF + (0,), ''),
    'path_absolute': (_LEAF + (0,), '/a'),
    'path_empty_component': (_LEAF + (0,), 'a//b'),
    'path_trailing_slash': (_LEAF + (0,), 'a/'),
    'path_dot_component': (_LEAF + (0,), 'a/./b'),
    'path_dotdot_component': (_LEAF + (0,), 'a/../b'),
    'path_dot': (_LEAF + (0,), '.'),
    'path_dotdot': (_LEAF + (0,), '..'),
    'path_number': (_LEAF + (0,), 1),
    'path_null': (_LEAF + (0,), None),
    'root_last_success': (_LEAF + (0,), '.last_success'),
    'kind_dir': (_LEAF + (1,), 'dir'),
    'kind_unknown': (_LEAF + (1,), 'fifo'),
    'kind_null': (_LEAF + (1,), None),
    'kind_array': (_LEAF + (1,), []),
    'digest_uppercase': (_LEAF + (2,), DIGEST.upper()),
    'digest_short': (_LEAF + (2,), 'a' * 63),
    'digest_long': (_LEAF + (2,), 'a' * 65),
    'digest_nonhex': (_LEAF + (2,), 'g' * 64),
    'digest_newline': (_LEAF + (2,), DIGEST + '\n'),
    'digest_number': (_LEAF + (2,), 1),
    'digest_null': (_LEAF + (2,), None),
    'link_text_number': (('destinations', 0, 'leaves', 1, 2), 1),
    'link_text_null': (('destinations', 0, 'leaves', 1, 2), None),
    'duplicate_leaf': (('destinations', 0, 'leaves', 1), ['z', 'file', DIGEST]),
}
for _name, (_location, _replacement) in _CASES.items():
    setattr(FormatTests, 'test_refuses_' + _name, refusal_case(_location, _replacement))


def missing_case(location):
    def test(self):
        value = document()
        parent = value
        for key in location[:-1]:
            parent = parent[key]
        del parent[location[-1]]
        self.refuse(wire(value))
    return test


for _location in [('version',), ('destinations',),
                  ('destinations', 0, 'root'), ('destinations', 0, 'leaves')]:
    setattr(FormatTests, 'test_missing_' + str(_location[-1]), missing_case(_location))


def raw_case(data):
    def test(self):
        self.refuse(data)
    return test


for _name, _data in {
    'empty_bytes': b'', 'invalid_json': b'{', 'invalid_utf8': b'\xff',
    'trailing_json': b'{} {}', 'nonbytes': None,
    'duplicate_json_key': b'{"version":1,"version":1,"destinations":[]}',
}.items():
    setattr(FormatTests, 'test_refuses_' + _name, raw_case(_data))
