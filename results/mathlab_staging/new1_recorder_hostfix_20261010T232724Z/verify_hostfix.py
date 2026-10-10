"""Read-only source/scope verification and receipt metadata; no dispatch launch."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

root = Path.cwd()
receipt = root/'results/mathlab_staging/new1_recorder_hostfix_20261010T232724Z'
build = root/'results/mathlab_staging/new1_recorder_build_20261010T225651Z'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(argv, name):
    result = subprocess.run(argv, cwd=root, capture_output=True, text=True)
    (receipt/(name+'.log')).write_text(result.stdout)
    (receipt/(name+'.stderr')).write_text(result.stderr)
    (receipt/(name+'.command.json')).write_text(json.dumps(dict(command=argv, cwd=str(root), interpreter=argv[0], exit_code=result.returncode), indent=2)+'\n')
    if result.returncode: raise SystemExit(name+' failed: '+result.stderr)
    return result.stdout

before = (receipt/'before/tools/new1_dispatch.sh').read_text()
after = (root/'tools/new1_dispatch.sh').read_text()
expected = before.replace('/usr/bin/date -u -r', '/bin/date -u -r').replace(
    'typeset -a df_rows=("${(@f)REPLY}") df_fields=( ${=df_rows[-1]} )',
    'typeset -a df_rows=("${(@f)${REPLY%$\'\\n\'}}")\n(( ${#df_rows} >= 2 )) || refuse 2f \'invalid df observation\'\ntypeset -a df_fields=( ${=df_rows[-1]} )')
assert after == expected, 'unexpected recorder edit'
assert (receipt/'before/tools/new1_dispatch_report.py').read_bytes() == (root/'tools/new1_dispatch_report.py').read_bytes(), 'reporter changed'
command_start, command_end = "(\n    trap ':' INT\n", ') > "$DISPATCH/supervisor_stdout.log"'
command_bytes = before[before.index(command_start):before.index(command_end)]
assert command_bytes == after[after.index(command_start):after.index(command_end)]
(receipt/'endorsed_exec.before.txt').write_text(command_bytes)
(receipt/'endorsed_exec.after.txt').write_text(command_bytes)

old = ast.parse((receipt/'before/tests/test_new1_dispatch.py').read_text())
new = ast.parse((root/'tests/test_new1_dispatch.py').read_text())
classes = {node.name:node for node in new.body if isinstance(node, ast.ClassDef)}
original_count = 0
for node in old.body:
    if not isinstance(node, ast.ClassDef): continue
    methods = {method.name:ast.dump(method) for method in classes[node.name].body if isinstance(method, ast.FunctionDef)}
    for method in node.body:
        if isinstance(method, ast.FunctionDef):
            assert ast.dump(method) == methods[method.name], 'existing test/helper changed: '+method.name
            original_count += method.name.startswith('test_')

protected = []
for line in (receipt/'protected_before.sha256').read_text().splitlines():
    digest, path = line.split('  ', 1)
    assert sha(root/path) == digest, 'protected source drift: '+path
    protected.append(path)
engine = json.loads((receipt/'engine_before.json').read_text())
for entry in engine:
    path = root/entry['path']
    if 'symlink' in entry: assert path.is_symlink() and os.readlink(path) == entry['symlink'], str(path)
    else: assert sha(path) == entry['sha256'], str(path)

executables = sorted(set(re.findall(r'(?<![\w$])/(?:[\w.+-]+/)*(?:s?bin)/[\w.+-]+', after)))
resolved = [str(root/'.venv/bin/python'), shutil.which('git')]
assert all(resolved)
ls_output = run(['/bin/ls', '-l', *executables, *resolved], 'executable_paths')
assert ls_output.strip()
run(['/bin/zsh', '-n', str(root/'tools/new1_dispatch.sh')], 'shell_syntax')
for path in ('tools/new1_dispatch_report.py', 'tests/test_new1_dispatch.py'):
    compile((root/path).read_bytes(), str(root/path), 'exec')

for folder in ('sandbox_red_pure', 'sandbox_green_pure'):
    metadata = json.loads((receipt/folder/'command.json').read_text())
    for source in metadata['sources']:
        assert sha(source['preserved_as']) == source['sha256'], source['preserved_as']
    assert sha(metadata['interpreter']) == metadata['interpreter_sha256']
metadata = json.loads((receipt/'sandbox_green_pure/command.json').read_text())
assert metadata['exit_code'] == 0
assert json.loads((receipt/'sandbox_red_pure/command.json').read_text())['exit_code'] == 1
metadata['receipt_status'] = 'READY FOR MAESTRO HOST RUN; host tests UNRUN'
metadata['sandbox_counts'] = {'tests_run':23,'passed':23,'host_dispatch_tests_run':0,'host_dispatch_tests_pending':19,'red_failure_records_including_subtests':11}
metadata['verification_command'] = ['/usr/bin/python3', '-B', str(receipt/'verify_hostfix.py')]
metadata['verification_source'] = {'path':str(receipt/'verify_hostfix.py'),'sha256':sha(receipt/'verify_hostfix.py')}
metadata['outer_command'] = ['LLMDB_ROOT='+str(root), '/usr/bin/python3', '-B', str(build/'record_test_run.py'), str(receipt/'sandbox_green_pure'), str(root), 'green', '--pure']
(receipt/'command.json').write_text(json.dumps(metadata, indent=2)+'\n')
paths = ('tools/new1_dispatch.sh','tools/new1_dispatch_report.py','tests/test_new1_dispatch.py')
(receipt/'final_sources.sha256').write_text(''.join(sha(root/path)+'  '+path+'\n' for path in paths))
checks = dict(original_tests_unchanged=original_count, executable_paths=executables, resolved_executables=resolved,
              protected_paths=protected, engine_entries_unchanged=len(engine), endorsed_exec_unchanged=True,
              reporter_unchanged=True, byte_changes_limited_to_two_fixes=True, provenance_hashes_verified=True,
              head_before=(receipt/'head_before.txt').read_text().strip(),
              head_after=run(['/usr/bin/git','rev-parse','HEAD'],'head_after').strip(),
              branch=run(['/usr/bin/git','branch','--show-current'],'branch_after').strip())
(receipt/'checks.json').write_text(json.dumps(checks, indent=2)+'\n')
(receipt/'sandbox_process_probe.json').write_text(json.dumps(dict(command_template=['/bin/ps','-o','nice=','-p','<own Python PID>'], exact_pid_unrecorded=True, cwd=str(root), interpreter='/usr/bin/python3', observation='PermissionError: [Errno 1] Operation not permitted: /bin/ps', process_started=False, process_clearance='UNAVAILABLE', host_suite_started=False), indent=2)+'\n')
print(json.dumps(dict(original_tests_unchanged=original_count, sandbox_green='23/23', literal_executables=len(executables), protected_paths=len(protected), engine_entries=len(engine), host_dispatch_tests='0 run; 19 pending', head=checks['head_after']), indent=2))
