#!/usr/bin/env python3
"""Audit the autoresearch agent's Claude Code transcript: every tool call it made, every absolute path it touched, every
denial it hit. Read-only. The program session runs it after each launch and on a timer (watch_audit.sh).

Usage:  python3 experiments/track_c/autoresearch_c10/audit_transcript.py
Exit 1 when no transcript is found. Paths outside the sandbox, the fence and the agent's own temp folder are listed;
`/opt/homebrew/bin/git` (a probe for a binary that does not exist) is the one benign entry seen so far.
"""
import glob, json, os, re, sys

base = os.path.expanduser("~/.claude/projects")
cands = sorted(glob.glob(f"{base}/*autoresearch-sandbox-c10*/*.jsonl"), key=os.path.getmtime)
if not cands:
    print("NO TRANSCRIPT FOUND under", base)
    sys.exit(1)
path = cands[-1]
print("transcript:", path, os.path.getsize(path), "bytes")
SB = "/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10"
FENCE = "/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10"
allowed_prefixes = (SB, FENCE, "/tmp/claude-501", "/private/tmp/claude-501")
tool_calls, denials, agents, paths = [], [], [], set()
for line in open(path):
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        continue
    content = (d.get("message") or {}).get("content")
    if not isinstance(content, list):
        continue
    for c in content:
        if c.get("type") == "tool_use":
            name, inp = c.get("name"), c.get("input", {})
            tool_calls.append((name, inp))
            if name in ("Agent", "Task"):
                agents.append(inp)
            for m in re.findall(r"(/(?:Volumes|Users|private|tmp|var|etc|opt)[^\s\"'\\\\)|;&]*)", json.dumps(inp)):
                paths.add(m)
        if c.get("type") == "tool_result":
            t = json.dumps(c.get("content"))
            if re.search(r"Operation not permitted|denied by your permission|Permission denied|not permitted", t):
                denials.append(t[:300])
print("tool calls:", len(tool_calls), "by tool:", {n: sum(1 for x in tool_calls if x[0] == n) for n in set(x[0] for x in tool_calls)})
print("Agent/Task calls:", len(agents))
print("\nBash commands:")
for n, inp in tool_calls:
    if n == "Bash":
        print("  $", inp.get("command", "")[:220].replace("\n", " "))
print("\nRead/Edit/Write/Glob/Grep targets:")
for n, inp in tool_calls:
    if n in ("Read", "Edit", "Write", "Glob", "Grep", "MultiEdit"):
        print("  ", n, inp.get("file_path") or inp.get("path") or inp.get("pattern"))
print("\nabsolute paths referenced OUTSIDE the sandbox/fence/own-tmp:")
for p in sorted(p for p in paths if not p.startswith(allowed_prefixes)):
    print("  ", p)
print("\ndenials seen in tool results:", len(denials))
for t in denials[:12]:
    print("  ", t[:200])
