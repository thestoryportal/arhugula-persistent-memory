"""MB35 final scope, syntax, source-identity and evidence audit."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

RECEIPT = Path(__file__).resolve().parent
ROOT = RECEIPT.parents[2]
RUN = RECEIPT/"final_verification"
RUN.mkdir()
assert Path.cwd() == ROOT
assert os.environ["LLMDB_ROOT"] == str(ROOT)
before = json.loads((RECEIPT/"before_sha256.json").read_text())
changed = ("tools/launchd/build_gdrive_applet.sh", "tools/test_backup_gdrive_addendum.py")
paths = [*(ROOT/name for name in before), Path(__file__).resolve(), RECEIPT/"run_sandbox.py", RECEIPT/"README.md"]
hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
argv = ["/usr/bin/python3", "-B", *sys.argv]
metadata = {"argv": argv, "command": 'LLMDB_ROOT="$PWD" PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy '+shlex.join(argv),
            "cwd": str(ROOT), "interpreter": sys.executable, "invoked_interpreter": "/usr/bin/python3",
            "python_version": sys.version, "source_sha256": hashes}
(RUN/"command.json").write_text(json.dumps(metadata, indent=2, sort_keys=True)+"\n")
for name, digest in before.items():
    path = RECEIPT/"before"/name if name in changed else ROOT/name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
old_build = (RECEIPT/"before"/changed[0]).read_text()
expected = old_build.replace('/bin/cp "$SCRATCH/canonical.applescript" "$SOURCE"\n',
    '/bin/cp "$SCRATCH/canonical.applescript" "$SOURCE"\n'
    '# Compare decompilations of two compiles of the same saved canonical source.\n'
    '/usr/bin/osacompile -o "$SCRATCH/saved.scpt" "$SOURCE"\n'
    '/usr/bin/osadecompile "$SCRATCH/saved.scpt" > "$SCRATCH/saved.applescript"\n')
expected = expected.replace('/usr/bin/cmp "$SOURCE" "$DECOMPILED"',
                            '/usr/bin/cmp "$SCRATCH/saved.applescript" "$DECOMPILED"')
assert (ROOT/changed[0]).read_bytes() == expected.encode()
old_tree = ast.parse((RECEIPT/"before"/changed[1]).read_text())
new_tree = ast.parse((ROOT/changed[1]).read_text())
old_class = next(node for node in old_tree.body if isinstance(node, ast.ClassDef) and node.name == "LockedReleaseTest")
new_class = next(node for node in new_tree.body if isinstance(node, ast.ClassDef) and node.name == "LockedReleaseTest")
additions = {"build_with_fake_osa", "test_builder_compares_fresh_saved_compile_with_newline_growth",
             "test_builder_rejects_app_decompile_byte_mismatch", "test_builder_rejects_empty_canonical_decompile"}
native_test = "test_compiled_app_full_source_equals_saved_source"
old_native = next(node for node in old_class.body if isinstance(node, ast.FunctionDef) and node.name == native_test)
new_class.body = [old_native if isinstance(node, ast.FunctionDef) and node.name == native_test else node
                 for node in new_class.body
                 if not (isinstance(node, ast.FunctionDef) and node.name in additions)]
assert ast.dump(new_tree) == ast.dump(old_tree), "unrelated test/module AST changed"
assert (ROOT/changed[1]).read_bytes() == (RECEIPT/"test_first_snapshot.py").read_bytes()
syntax_argv = ["/bin/bash", "-n", str(ROOT/changed[0])]
syntax = subprocess.run(syntax_argv, capture_output=True, text=True)
(RUN/"test.log").write_text(shlex.join(syntax_argv)+"\n"+syntax.stdout+syntax.stderr+
                           "exit_code="+str(syntax.returncode)+"\n")
assert syntax.returncode == 0, syntax.stderr
readme = (RECEIPT/"README.md").read_text()
blocks = re.findall(r"```bash\n(.*?)\n```", readme, re.S)
assert len(blocks) == 5
for index, block in enumerate(blocks):
    check = subprocess.run(["/bin/bash", "-n"], input=block, capture_output=True, text=True)
    with (RUN/"test.log").open("a") as stream:
        stream.write("README bash block "+str(index+1)+": exit_code="+str(check.returncode)+"\n"+
                     check.stdout+check.stderr)
    assert check.returncode == 0, check.stderr
python_blocks = re.findall(r"<<'PY'\n(.*?)\nPY", readme, re.S)
assert len(python_blocks) == 2
for block in python_blocks:
    compile(block, str(RECEIPT/"README.md"), "exec")
runs = {}
for label, count, failures in (("sandbox_red", 3, 1), ("sandbox_green_focus", 3, 0),
                               ("sandbox_green_non_native", 136, 0)):
    value = json.loads((RECEIPT/label/"result.json").read_text())
    command = json.loads((RECEIPT/label/"command.json").read_text())
    assert (value["testsRun"], value["failures"], value["errors"], value["skipped"]) == (count, failures, 0, 0), value
    expected_build_hash = before[changed[0]] if label == "sandbox_red" else hashes[changed[0]]
    assert command["source_sha256"][changed[0]] == expected_build_hash
    assert command["source_sha256"][changed[1]] == hashes[changed[1]]
    assert command["source_sha256"] == command["source_sha256_after"]
    assert command["fixture_source_sha256"]
    runs[label] = value
selection = json.loads((RECEIPT/"sandbox_green_non_native/suite_selection.json").read_text())
assert len(selection["excluded"]) == 18
summary = {"success": True, "before_copies_match": True, "protected_sha256_match": True,
           "build_has_only_comparison_fix": True, "unrelated_test_AST_unchanged": True,
           "tests_written_before_production_fix": True, "bash_n_exit_code": syntax.returncode,
           "host_bash_blocks_checked": len(blocks), "host_python_blocks_checked": len(python_blocks),
           "final_sha256": {name: hashes[name] for name in changed}, "runs": runs, "native": "UNRUN"}
(RUN/"result.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n")
print(json.dumps(summary, indent=2))
