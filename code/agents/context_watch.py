"""Context-ceiling watcher for sessions where memento's Stop hook is not active.

Counts tokens exactly as memento 0.7.0's hook does (hooks/scripts/context-ceiling.py:48-111):
the newest assistant record's usage, summed over input, cache-creation, cache-read and output tokens.
Prints one line when the count first crosses each threshold, then exits after the last one.
Usage: python code/agents/context_watch.py <transcript.jsonl> [ceiling=250000] [poll_seconds=60] [idle_seconds=3600]

It also ends itself when it no longer watches a live session:
- owner gone: the nearest `claude` ancestor at start exited (a relaunch); exit 0.
- transcript idle: the transcript mtime is idle_seconds old (a memento /clear keeps the claude process but
  starts a new transcript, so the old one is never written again); exit 0.
With no `claude` ancestor it refuses to start (exit 1), so it is never unowned.
"""
import json
import os
import subprocess
import sys
import time

FIELDS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def context_tokens(path):
    with open(path, "rb") as f:
        lines = f.read().splitlines()
    for raw in reversed(lines):
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError:
            continue
        usage = (rec.get("message") or {}).get("usage") if rec.get("type") == "assistant" else None
        if usage:
            return sum(usage.get(k, 0) for k in FIELDS)
    return 0


def owner_pid():
    """Nearest ancestor whose executable is named claude (same rule as step6watch.py owner_pid)."""
    pid = os.getppid()
    while pid > 1:
        r = subprocess.run(["/bin/ps", "-o", "ppid=,comm=", "-p", str(pid)], capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            break
        ppid, comm = r.stdout.split(None, 1)
        if os.path.basename(comm.strip()) == "claude":
            return pid
        pid = int(ppid)
    sys.exit("context_watch: no claude ancestor found; refusing to run unowned")


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def main():
    path = sys.argv[1]
    ceiling = int(sys.argv[2]) if len(sys.argv) > 2 else 250_000
    poll = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    idle = int(sys.argv[4]) if len(sys.argv) > 4 else 3600
    owner = owner_pid()
    pending = [(0.8, "WARN"), (1.0, "CEILING")]
    while pending:
        if not alive(owner):
            print(f"context_watch: owner claude pid {owner} gone; watcher exits", flush=True)
            sys.exit(0)
        age = int(time.time() - os.stat(path).st_mtime)
        if age >= idle:
            print(f"context_watch: transcript idle {age} s >= {idle} s; watcher exits", flush=True)
            sys.exit(0)
        tokens = context_tokens(path)
        while pending and tokens >= pending[0][0] * ceiling:
            frac, label = pending.pop(0)
            print(f"{label}: context {tokens:,} tokens >= {int(frac * 100)}% of ceiling {ceiling:,}", flush=True)
        time.sleep(poll)


if __name__ == "__main__":
    main()
