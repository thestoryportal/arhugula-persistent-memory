"""Fixture-only conservation checks for Part 3 Step 413."""
import ast
import copy
import unittest
from collections import ChainMap, Counter, OrderedDict, UserDict, defaultdict
from types import MappingProxyType

from ops.migrate import conserve_core as core


def row(**changes):
    value = dict(source="/M/work", kind="file", bytes=4, sha256="a" * 64,
                 link_text=None, device=1, inode=2, nlink=1, mode=0o755)
    value.update(changes)
    return value


class Conservation(unittest.TestCase):
    def test_unchanged(self):
        pre = {"work": row()}
        post = {"work": row(source="/R/work")}
        saved = copy.deepcopy((pre, post))
        self.assertEqual(core.compare(pre, post, []), ())
        self.assertEqual((pre, post), saved)

    def test_empty(self):
        self.assertEqual(core.compare({}, {}, []), ())

    def test_hex_digits_nested_paths_and_multiple_actions(self):
        digest = "0123456789abcdef" * 4
        pre = {"a/nested": row(sha256=digest), "z": row(), "untouched": row()}
        post = {"a/nested": row(sha256="f" * 64, bytes=7),
                "z": row(sha256=digest, inode=7), "untouched": row(bytes=8)}
        actions = [("a/nested", digest, "f" * 64), ("z", "a" * 64, digest)]
        saved = copy.deepcopy((pre, post, actions))
        self.assertEqual(core.compare(pre, post, actions), (("untouched", "bytes"),))
        self.assertEqual((pre, post, actions), saved)

    def test_changed_working_file(self):
        self.assertEqual(core.compare({"work": row()}, {"work": row(bytes=5)}, []),
                         (("work", "bytes"),))

    def test_same_size_content_change_same_mtime(self):
        self.assertEqual(core.compare({"work": row(mtime=7)},
                                     {"work": row(mtime=7, sha256="b" * 64)}, []),
                         (("work", "sha256"),))

    def test_lost_ignored_file_and_new_file(self):
        self.assertEqual(core.compare({"ignored": row()}, {"new": row()}, []),
                         (("ignored", "missing-post"), ("new", "missing-pre")))

    def test_mode_change(self):
        self.assertEqual(core.compare({"work": row()}, {"work": row(mode=0o600)}, []),
                         (("work", "mode"),))

    def test_changed_link_text(self):
        self.assertEqual(core.compare({"link": row(kind="symlink", link_text="a")},
                                     {"link": row(kind="symlink", link_text="b")}, []),
                         (("link", "link_text"),))

    def test_identity(self):
        for field in ("device", "inode"):
            with self.subTest(field=field):
                self.assertEqual(core.compare({"work": row()}, {"work": row(**{field: 9})}, []),
                                 (("work", field),))

    def test_nlink_is_not_compared(self):
        self.assertEqual(core.compare({"work": row()}, {"work": row(nlink=9)}, []), ())

    def test_kind(self):
        self.assertEqual(core.compare({"work": row()}, {"work": row(kind="socket")}, []),
                         (("work", "kind"),))

    def test_replace(self):
        self.assertEqual(core.compare({"work": row()},
                                     {"work": row(bytes=9, sha256="b" * 64, inode=9, nlink=9)},
                                     [("work", "a" * 64, "b" * 64)]), ())

    def test_replace_container_types(self):
        for outer in (list, tuple):
            for inner in (list, tuple):
                with self.subTest(outer=outer.__name__, inner=inner.__name__):
                    actions = outer([inner(("work", "a" * 64, "b" * 64))])
                    self.assertEqual(core.compare({"work": row()},
                                                 {"work": row(sha256="b" * 64)}, actions), ())

    def test_mapping_types(self):
        # [LAW:behavior-not-structure] Both mapping boundaries accept non-dict mappings.
        factories = (dict, OrderedDict, Counter, ChainMap, UserDict, MappingProxyType,
                     lambda value: defaultdict(dict, value))
        for factory in factories:
            for side in (0, 1):
                for boundary in ("manifest", "leaf"):
                    with self.subTest(factory=factory, side=side, boundary=boundary):
                        manifests = [{"work": row()}, {"work": row(sha256="b" * 64)}]
                        if boundary == "manifest":
                            manifests[side] = factory(manifests[side])
                        else:
                            manifests[side]["work"] = factory(manifests[side]["work"])
                        self.assertEqual(core.compare(*manifests,
                                                     [("work", "a" * 64, "b" * 64)]), ())

    def test_terminal_newline_in_posix_names(self):
        value = row(source="/M/link\n", kind="symlink", link_text="target\n")
        self.assertEqual(core.compare({"link\n": value}, {"link\n": value}, []), ())

    def test_replace_pre_and_post_hashes(self):
        for before, after, field in (("c", "b", "replace-pre-sha256"),
                                     ("a", "c", "replace-post-sha256")):
            with self.subTest(field=field):
                self.assertEqual(core.compare({"work": row(sha256=before * 64)},
                                             {"work": row(sha256=after * 64)},
                                             [("work", "a" * 64, "b" * 64)]), (("work", field),))

    def test_replace_preserves_other_fields(self):
        for field in ("mode", "device"):
            with self.subTest(field=field):
                self.assertEqual(core.compare({"work": row()}, {"work": row(**{field: 9})},
                                             [("work", "a" * 64, "a" * 64)]), (("work", field),))

    def test_replace_cannot_hide_absent_paths(self):
        self.assertEqual(core.compare({}, {}, [("lost", "a" * 64, "b" * 64)]),
                         (("lost", "missing-post"), ("lost", "missing-pre")))

    def test_sorted_complete_findings(self):
        self.assertEqual(core.compare({"z": row(), "a": row()},
                                     {"z": row(mode=0), "a": row(bytes=0, inode=0)}, []),
                         (("a", "bytes"), ("a", "inode"), ("z", "mode")))


class Malformed(unittest.TestCase):
    def refuses(self, pre, post, actions, path):
        with self.assertRaises(core.Refusal) as caught:
            core.compare(pre, post, actions)
        self.assertIn(path, str(caught.exception))

    def test_manifest_terminal_newline_hashes(self):
        for side in (0, 1):
            with self.subTest(side=side):
                manifests = [{"work": row()}, {"work": row()}]
                manifests[side]["work"]["sha256"] += "\n"
                self.refuses(*manifests, [], "work")

    def test_action_terminal_newline_hashes(self):
        for index in (1, 2):
            with self.subTest(index=index):
                action = ["work", "a" * 64, "b" * 64]
                action[index] += "\n"
                self.refuses({"work": row()}, {"work": row(sha256="b" * 64)},
                             [action], "actions")

    def test_manifest_shape(self):
        for bad in (None, [], 1, "x"):
            self.refuses(bad, {}, [], "pre")
            self.refuses({}, bad, [], "post")
        for bad in (None, [], 1, "x"):
            self.refuses({"work": bad}, {}, [], "work")

    def test_paths(self):
        for bad in ("", "/work", "../work", "a//b", "a/./b", "a/../b", "a/", "a\0b", 1):
            self.refuses({bad: row()}, {}, [], "pre")
            self.refuses({}, {}, [(bad, "a" * 64, "b" * 64)], "actions")

    def test_missing_fields(self):
        for field in row():
            value = row()
            del value[field]
            self.refuses({"work": value}, {}, [], "work")

    def test_bad_fields(self):
        cases = {
            "source": (None, 1, "", "relative", "/a/../b", "/a\0b"),
            "kind": (None, [], 1, "dir"),
            "bytes": (None, True, -1, 1.5, "4"),
            "device": (None, True, -1, 1.5, "1"),
            "inode": (None, True, -1, 1.5, "1"),
            "nlink": (None, True, -1, 1.5, "1"),
            "mode": (None, True, -1, 0o10000, 1.5, "755"),
            "sha256": (None, 1, "a" * 63, "a" * 65, "A" * 64, "g" * 64),
            "link_text": ("target", [], 1),
        }
        for field, values in cases.items():
            for bad in values:
                with self.subTest(field=field, bad=bad):
                    self.refuses({"work": row(**{field: bad})}, {}, [], "work")
        for bad in (None, "", "a\0b", 1):
            self.refuses({"work": row(kind="symlink", link_text=bad)}, {}, [], "work")

    def test_actions(self):
        for bad in (None, {}, "x", 1):
            self.refuses({}, {}, bad, "actions")
        for bad in (None, "abc", [], ("work",), ("work", "a" * 64, "b" * 64, 1)):
            self.refuses({}, {}, [bad], "actions")
        for index in (1, 2):
            for bad in (None, 1, "a" * 63, "a" * 65, "A" * 64, "g" * 64):
                action = ["work", "a" * 64, "b" * 64]
                action[index] = bad
                self.refuses({}, {}, [action], "actions")
        self.refuses({}, {}, [("work", "a" * 64, "b" * 64)] * 2, "work")

    def test_replace_requires_regular_file(self):
        for kind, link in (("socket", None), ("symlink", "target")):
            self.refuses({"work": row(kind=kind, link_text=link)}, {"work": row()},
                         [("work", "a" * 64, "a" * 64)], "work")
            self.refuses({"work": row()}, {"work": row(kind=kind, link_text=link)},
                         [("work", "a" * 64, "a" * 64)], "work")

    def test_numeric_boundaries(self):
        for mode in (0, 0o7777):
            value = row(mode=mode, bytes=0, device=0, inode=0, nlink=0)
            self.assertEqual(core.compare({"work": value}, {"work": value}, ()), ())


class Purity(unittest.TestCase):
    def test_call_and_module_attribute_allowlist(self):
        with open(core.__file__, encoding="utf-8") as stream:
            tree = ast.parse(stream.read())
        # [LAW:effects-at-boundaries] Imports alone cannot exclude hidden I/O.
        calls = {"isinstance", "any", "type", "len", "getattr", "tuple", "sorted",
                 "dataclass", "Refusal", "Leaf", "_path", "_sha", "_manifest", "_actions"}
        attributes = {"fdsafe": {"Refusal"}, "re": {"fullmatch"}}
        imported = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update((alias.asname or alias.name.split(".")[0], alias.name)
                                for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.update((alias.asname or alias.name, alias.name) for alias in node.names)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertIn(node.func.id, calls, f"call at line {node.lineno}")
            if isinstance(node, ast.Attribute):
                root = node.value
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name) and root.id in imported:
                    self.assertIsInstance(node.value, ast.Name,
                                          f"chained module attribute at line {node.lineno}")
                    self.assertIn(node.attr, attributes.get(imported[root.id], set()),
                                  f"module attribute at line {node.lineno}")

    def test_import_allowlist(self):
        with open(core.__file__, encoding="utf-8") as stream:
            tree = ast.parse(stream.read())
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module)
        self.assertTrue(names <= {"__future__", "collections.abc", "dataclasses", "ops.migrate", "re", "typing"}, names)
        self.assertIn("ops.migrate", names)


if __name__ == "__main__":
    unittest.main()
