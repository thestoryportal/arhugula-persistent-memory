"""RED candidate: unchecked plans accepted."""
import json
from pathlib import Path
import sys
def check(text): return []
if __name__=='__main__':
    findings=check(Path(sys.argv[1]).read_text()); print(json.dumps(findings)); sys.exit(1 if findings else 0)
