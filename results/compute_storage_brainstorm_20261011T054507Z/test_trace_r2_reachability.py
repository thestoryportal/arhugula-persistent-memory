#!/usr/bin/python3
"""R2TR behavioral tests; imports only the tracer, never science modules."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

B = Path(__file__).resolve().parent
ROOT = B.parents[1]
TR = B / "trace_r2_reachability.py"


class Fixtures(unittest.TestCase):
    def trace(self, files, argv=()):
        self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
        spec = importlib.util.spec_from_file_location("r2tr", TR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory(prefix="r2tr-fixture-") as directory:
            root = Path(directory)
            for name, source in files.items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(textwrap.dedent(source))
            result = module.trace(root, [{"path": "entry.sh" if "entry.sh" in files else "entry.py", "argv": list(argv)}])
        self.assertFalse(root.exists(), "fixture temporary directory was not removed")
        json.dumps(result)
        return result

    def test_direct_spawn(self):
        r = self.trace({"entry.py": "import subprocess as sp\nsp.run(['/bin/echo', 'hello'])\n"})
        self.assertEqual(len(r["paths"]), 1)
        self.assertEqual(r["paths"][0]["count"]["kind"], "pinned_constant")
        self.assertEqual(r["paths"][0]["operand_source"]["kind"], "pinned_literal")

    def test_alias_cross_module(self):
        r = self.trace({"entry.py": "import worker as R\nR.launch()\n", "worker.py": "from subprocess import check_output as start\ndef launch():\n    start(['/bin/echo', 'x'])\n"})
        chain = r["paths"][0]["chain"]
        self.assertTrue(any(x.startswith("entry.py:") for x in chain))
        self.assertTrue(any(x.startswith("worker.py:") for x in chain))

    def test_loaded_list_count_and_operand(self):
        r = self.trace({"entry.py": """
            import json, subprocess
            from pathlib import Path
            records = json.loads(Path('eval.json').read_text())
            for tr in records['train_records']:
                subprocess.run(['/bin/echo', tr['adapter']['path']])
        """})
        p = r["paths"][0]
        self.assertEqual(p["count"]["kind"], "loaded_data")
        self.assertEqual(p["operand_source"]["kind"], "loaded_data")
        self.assertIn("train_records", json.dumps(p))
        self.assertIn("adapter", json.dumps(p))

    def test_disk_round_trip_is_loaded(self):
        r = self.trace({"entry.py": """
            import json, subprocess
            from pathlib import Path
            Path('proof.json').write_text(json.dumps({'phase':'P1'}))
            proof = json.loads(Path('proof.json').read_text())
            if proof['phase'] == 'P3': subprocess.run(['/bin/echo', 'P3'])
        """})
        self.assertEqual(len(r["paths"]), 1)
        self.assertTrue(r["paths"][0]["taint_reasons"])

    def test_require_excludes_before_spawn(self):
        r = self.trace({"entry.py": """
            import json, subprocess
            from pathlib import Path
            def require(ok):
                if not ok: raise ValueError('bad')
            proof = json.loads(Path('proof.json').read_text())
            require(proof['phase'] == 'P1')
            if proof['phase'] == 'P3': subprocess.run(['/bin/echo', 'P3'])
        """})
        self.assertEqual(r["paths"], [])

    def test_late_require_does_not_exclude(self):
        r = self.trace({"entry.py": """
            import json, subprocess
            from pathlib import Path
            def require(ok):
                if not ok: raise ValueError('bad')
            proof = json.loads(Path('proof.json').read_text())
            if proof['phase'] == 'P3': subprocess.run(['/bin/echo', 'P3'])
            require(proof['phase'] == 'P1')
        """})
        self.assertEqual(len(r["paths"]), 1)

    def test_dynamic_call_unresolved(self):
        r = self.trace({"entry.py": "getattr(object(), 'launch')()\n"})
        self.assertTrue(any(x['file'] == 'entry.py' and x['line'] == 1 for x in r['unresolved']))

    def test_shell_branch_and_variable_command(self):
        r = self.trace({"entry.sh": "#!/bin/sh\nif [ -f proof.json ]; then\n /bin/echo yes\nelse\n $PROGRAM arg\nfi\n"})
        self.assertTrue(any(p['site'] == 'entry.sh:3' for p in r['paths']))
        self.assertTrue(any(x['file'] == 'entry.sh' and x['line'] == 5 for x in r['unresolved']))

    def test_pinned_loop_count(self):
        r = self.trace({"entry.py": "import subprocess\nfor x in (1,2,3):\n subprocess.call(['/bin/echo',str(x)])\n"})
        self.assertTrue(all(p['count']['kind'] == 'pinned_constant' and p['count']['maximum'] == 3 for p in r['paths']))

    def test_argv_dispatch(self):
        r = self.trace({"entry.py": "import sys, subprocess\nif sys.argv[1] == 'yes': subprocess.run(['/bin/echo','yes'])\n"}, ['no'])
        self.assertEqual(r['paths'], [])

    def test_child_program_follows_stdin_loaded_phase(self):
        r = self.trace({"entry.py": "import subprocess\nsubprocess.run(['/usr/bin/python3','child.py','verify'],input='{}')\n", "child.py": "import json,sys,subprocess\np=json.loads(sys.stdin.read())\nif p['phase']=='P3': subprocess.run(['/bin/echo','replication'])\n"})
        self.assertTrue(any(p['site'].startswith('child.py:') and len(p['chain']) > 1 for p in r['paths']))

    def test_external_boundary(self):
        r = self.trace({"entry.py": "import torch\ntorch.load('x')\n"})
        self.assertTrue(any(x['name'].startswith('torch') for x in r['boundaries']))
        self.assertTrue(any(x['line']==2 for x in r['unresolved']))

    def test_module_initialization_spawn(self):
        r = self.trace({"entry.py": "import worker\ndef main(): pass\nif __name__=='__main__': main()\n", "worker.py": "import subprocess\nsubprocess.run(['/bin/echo','initialization'])\n"})
        self.assertTrue(any(p['site']=='worker.py:2' for p in r['paths']))

    def test_shell_nested_substitution(self):
        r = self.trace({"entry.sh": '#!/bin/sh\nD="$(cd "$(dirname "$0")" && pwd)"\n'})
        self.assertTrue(any(p['command']==['dirname','entry.sh'] or (isinstance(p['command'],list) and p['command'][0]=='dirname' and len(p['command'])==2) for p in r['paths']))

    def test_len_guard_bounds_count_before_loop(self):
        r = self.trace({"entry.py": """
            import json,subprocess
            from pathlib import Path
            def require(ok):
                if not ok: raise ValueError('bad')
            rows=json.loads(Path('records.json').read_text())
            require(len(rows)==2)
            for row in rows: subprocess.run(['/bin/echo',row['path']])
        """})
        self.assertEqual(r['paths'][0]['count']['kind'],'pinned_constant')
        self.assertEqual(r['paths'][0]['count']['maximum'],2)
        self.assertTrue(r['paths'][0]['operand_source']['kind']=='loaded_data')

    def test_pinned_condition_false_does_not_evaluate_spawn(self):
        r=self.trace({"entry.py":"import subprocess\nif False and subprocess.run(['/bin/echo','unreachable']): pass\n"})
        self.assertEqual(r['paths'],[])

    def test_same_shape_different_loaded_family_not_covered(self):
        self.assertTrue(TR.is_file())
        spec=importlib.util.spec_from_file_location('r2tr',TR)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        path={'site':'worker.py:50','family':'launch','chain':['worker.py:20','worker.py:50'], 'command':['/usr/bin/git','ls-files',{'loaded_data':'records[*].path'}], 'count':{'kind':'loaded_data','loops':[{'selection_line':'worker.py:20'}]},'operand_source':{'kind':'loaded_data'}}
        child={'trace_site':'other-records','invocation':{'executable_path':'/usr/bin/git','argv':['ls-files',{'$bind':'other'}]},'count':{'kind':'loaded_data','selection_lines':[{'path':'worker.py','line':30}]},'operand_source':{'kind':'loaded_data','read_lines':[{'path':'worker.py','line':30}],'pre_spawn_constraints':[{'path':'worker.py','line':50}]}}
        p={'entrypoint':'entry.py','children':[child],'composition_refusal':'NOT_ADMITTED_OPERAND_DOMAIN_UNENUMERATED:other-records'}
        self.assertEqual(module.coverage_for(p,0,{'paths':[path]},[])[0]['status'],'GAP')

    def test_two_primitives_on_same_line_inventory(self):
        r=self.trace({'entry.py':"import subprocess\nsubprocess.run(['/bin/echo','one']); subprocess.run(['/bin/echo','two'])\n"})
        self.assertEqual(len(r['sites']),2)
        self.assertEqual(len(r['paths']),2)

    def test_return_before_guard_is_not_exclusion(self):
        r=self.trace({'entry.py':"""
            import json,subprocess
            def require(ok):
                return
                if not ok: raise ValueError('unreachable')
            proof=json.loads('{}')
            require(proof['phase']=='P1')
            if proof['phase']=='P3': subprocess.run(['/bin/echo','reachable'])
        """})
        self.assertEqual(len(r['paths']),1)

    def test_pinned_while_false_and_exit_exclude(self):
        r=self.trace({'entry.py':"import sys,subprocess\nwhile False: subprocess.run(['/bin/echo','unreachable'])\nsys.exit(2)\nsubprocess.run(['/bin/echo','after-exit'])\n"})
        self.assertEqual(r['paths'],[])

    def test_import_inside_helper_initialization(self):
        r=self.trace({'entry.py':"def initialize():\n import worker\ninitialize()\n",'worker.py':"import subprocess\nsubprocess.run(['/bin/echo','init'])\n"})
        self.assertTrue(any(p['site']=='worker.py:2' for p in r['paths']))

    def test_os_exec_and_spawn_normalize_operands(self):
        r=self.trace({'entry.py':"import os\nos.execv('/bin/echo',['echo','x'])\nos.spawnv(os.P_NOWAIT,'/bin/echo',['echo','y'])\n"})
        self.assertEqual(r['paths'][0]['command'],['/bin/echo','x'])
        self.assertEqual(r['paths'][1]['command'],['/bin/echo','y'])

    def test_comprehension_loaded_cardinality(self):
        r=self.trace({'entry.py':"import json,subprocess\nrows=json.loads('[]')\nresults=[subprocess.run(['/bin/echo',row['path']]) for row in rows]\n"})
        self.assertEqual(r['paths'][0]['count']['kind'],'loaded_data')

    def test_higher_order_callback_is_not_silently_dropped(self):
        r=self.trace({'entry.py':"import subprocess\ndef launch(x): subprocess.run(['/bin/echo',x])\nlist(map(launch,['one','two']))\n"})
        self.assertTrue(any(x['line']==3 and 'callback' in x['reason'] for x in r['unresolved']))

    def test_transitive_loader_retains_source_reason(self):
        r=self.trace({'entry.py':"""
            import json,subprocess
            from pathlib import Path
            def read_records(): return json.loads(Path('eval.json').read_text())
            def wrapper(): return read_records()
            for row in wrapper()['train_records']: subprocess.run(['/bin/echo',row['adapter']['path']])
        """})
        self.assertTrue(any('eval.json' in x for x in r['paths'][0]['count']['loops'][0]['reasons']))

    def test_source_snapshot_is_sha256_bound(self):
        source="import subprocess\nsubprocess.run(['/bin/echo','snapshot'])\n"
        r=self.trace({'entry.py':source})
        import hashlib
        self.assertTrue(any(x['file']=='entry.py' and x['sha256']==hashlib.sha256(source.encode()).hexdigest() for x in r['sources']))

    def test_unknown_receiver_method_is_unresolved(self):
        r=self.trace({'entry.py':"obj=unknown_factory()\nx=obj.get('launch')\n"})
        self.assertTrue(any(x['line']==2 and 'obj.get' in x['reason'] for x in r['unresolved']))


class RealControls(unittest.TestCase):
    def run_control(self):
        self.assertTrue(TR.is_file(), "tracer implementation is absent (test-first RED)")
        if hasattr(type(self),'control_result'): return type(self).control_result
        p = subprocess.run(['/usr/bin/python3','-B',str(TR),'--against',str(B/'science_launch_profiles_v7.json')], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(p.returncode,1,p.stderr)
        self.assertTrue(p.stdout.strip())
        type(self).control_result=json.loads(p.stdout)
        return type(self).control_result

    def test_round12_F1_profile19_verifier_gap(self):
        r = self.run_control()
        gaps = [x for x in r['coverage'] if x['status']=='GAP' and x['profile']==19]
        self.assertTrue(any('c10w_oracle_train.py:65' in x['site'] for x in gaps),json.dumps(gaps))

    def test_round12_F2_evaluator_replication_gap(self):
        r = self.run_control()
        matches = [x for x in r['coverage'] if x['status']=='GAP' and x['entrypoint'].endswith('c10w_oracle_eval.py') and x['argv'][0] in ('P1','P2') and any('c10w_oracle_read.py:550' in link for link in x['chain'])]
        self.assertTrue(matches, 'P1/P2 evaluator must reach loaded P3 replication before any later validator')


if __name__ == '__main__':
    unittest.main(verbosity=2)
