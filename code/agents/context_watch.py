"""Context-ceiling watcher for sessions where memento's Stop hook is not active.

Counts tokens exactly as memento 0.7.0's hook does (hooks/scripts/context-ceiling.py:48-111):
the newest assistant record's usage, summed over input, cache-creation, cache-read and output tokens.
Prints one line when the count first crosses each threshold, then exits after the last one.
Usage: python code/agents/context_watch.py <transcript.jsonl> [ceiling=250000] [poll_seconds=60]
"""
import json
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


def main():
    path = sys.argv[1]
    ceiling = int(sys.argv[2]) if len(sys.argv) > 2 else 250_000
    poll = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    pending = [(0.8, "WARN"), (1.0, "CEILING")]
    while pending:
        tokens = context_tokens(path)
        while pending and tokens >= pending[0][0] * ceiling:
            frac, label = pending.pop(0)
            print(f"{label}: context {tokens:,} tokens >= {int(frac * 100)}% of ceiling {ceiling:,}", flush=True)
        time.sleep(poll)


if __name__ == "__main__":
    main()
