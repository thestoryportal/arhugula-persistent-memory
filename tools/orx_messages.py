#!/usr/bin/env python3
"""Print the assistant text of an OpenResearch chat session. Usage: orx_messages.py <session_id> [max_chars]"""
import json
import sys
import urllib.request

sid = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 12000
with urllib.request.urlopen(f"http://127.0.0.1:4791/api/chat/sessions/{sid}/messages", timeout=60) as r:
    d = json.load(r)


def texts(obj, out):
    if isinstance(obj, dict):
        if obj.get("role") in ("assistant", "agent") or obj.get("type") in ("text", "assistant"):
            for k in ("text", "content", "markdown"):
                v = obj.get(k)
                if isinstance(v, str) and v.strip():
                    out.append(v)
        for v in obj.values():
            texts(v, out)
    elif isinstance(obj, list):
        for v in obj:
            texts(v, out)


out = []
texts(d, out)
if not out:
    print(json.dumps(d, indent=1)[:limit])
else:
    seen = set()
    for t in out:
        if t in seen:
            continue
        seen.add(t)
        print(t[:limit])
        print("-----")
