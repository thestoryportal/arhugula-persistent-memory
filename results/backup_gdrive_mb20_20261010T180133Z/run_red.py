"""Run each new regression once and retain its behavioral RED separately."""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys

receipt = Path(__file__).resolve().parent
root = Path(os.environ["LLMDB_ROOT"])
tree = ast.parse((root/"tools/test_backup_gdrive_addendum.py").read_text())
index = []
env = dict(os.environ, BACKUP_TEST_NO_RCLONE="1", BACKUP_TEST_RECEIPTS=str(receipt/"fixtures"),
           PYTHONDONTWRITEBYTECODE="1")
for cls in tree.body:
    if isinstance(cls, ast.ClassDef) and cls.name in {"R5RecoveryTest", "R5CompactionTest"}:
        for method in cls.body:
            if isinstance(method, ast.FunctionDef) and method.name.startswith("test_"):
                name = "tools.test_backup_gdrive_addendum."+cls.name+"."+method.name
                command = [sys.executable, "-B", "-m", "unittest", name, "-v"]
                result = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=45)
                output = result.stdout+result.stderr
                log = "RED_%02d_%s.log" % (len(index)+1, method.name)
                (receipt/log).write_text("COMMAND: "+" ".join(command)+"\nEXIT: "+str(result.returncode)+"\n"+output)
                behavioral = result.returncode != 0 and "FAIL:" in output and "ERROR:" not in output
                index.append({"test": name, "log": log, "exit_code": result.returncode,
                              "behavioral_red": behavioral})
                (receipt/"RED_index.json").write_text(json.dumps(index, indent=2)+"\n")
                print(name+": "+("behavioral RED" if behavioral else "CHECK LOG"), flush=True)
                if not behavioral:
                    sys.exit(1)
