"""Receipt helper acceptance: preserve both streams and the actual child exit."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent


class CaptureTest(unittest.TestCase):
    def test_success_streams_and_command(self):
        self.exercise(0)

    def test_failure_exit_not_hidden(self):
        self.exercise(7)

    def exercise(self, code):
        with tempfile.TemporaryDirectory(dir='/private/tmp') as temp:
            argv = ['/usr/bin/python3', '-B', '-c',
                    'import sys; print("complete stdout"); print("complete stderr",file=sys.stderr); sys.exit('+str(code)+')']
            result = subprocess.run(['/usr/bin/python3', '-B', str(HERE/'capture.py'), temp, 'probe', *argv],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, code, result.stderr)
            run = Path(temp)/'commands/probe'
            self.assertEqual((run/'stdout.txt').read_text(), 'complete stdout\n')
            self.assertEqual((run/'stderr.txt').read_text(), 'complete stderr\n')
            self.assertEqual((run/'exit_code.txt').read_text(), str(code)+'\n')
            command = json.loads((run/'command.json').read_text())
            self.assertEqual(command['argv'], argv)
            self.assertEqual(command['cwd'], os.getcwd())
            self.assertTrue(command['source_sha256'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
