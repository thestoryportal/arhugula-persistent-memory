"""RED candidate: the unsafe exit-code-only acceptance policy."""
import json
from pathlib import Path
import sys
def inspect(root):
    return {'pass':(Path(root)/'exit_code.txt').read_text().strip()=='0',
            'differing':0,'missing':0,'errors':0,'unchecked':0,'incomplete':0}
if __name__=='__main__':
    value=inspect(Path(sys.argv[1])); print(('PASS ' if value['pass'] else 'FAIL ')+json.dumps(value)); sys.exit(0 if value['pass'] else 1)
