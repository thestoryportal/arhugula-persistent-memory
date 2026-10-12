"""Archive every OpenResearch chat (dashboard DB + native Claude Code transcripts) into JSON.

Read-only on the OpenResearch data dir. Writes results/openresearch_archive/:
  sessions.json      every chat_sessions row, with its messages (parts parsed) and turns
  experiments.json   every local_experiments row (the research ledger nodes)
  native/<id>.jsonl  copies of the native harness transcripts found for those sessions
  text_index.jsonl   one line per text block: session, message, role, time, source, text
Usage: python tools/openresearch_archive.py [orx_data_dir]
"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / ".local/share/openresearch")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/openresearch_archive"


def rows(con, table):
    cols = [r[1] for r in con.execute(f'pragma table_info("{table}")')]
    return [dict(zip(cols, r)) for r in con.execute(f'select * from "{table}"')]


def parse(value):
    if isinstance(value, str) and value[:1] in "[{":
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    return value


def native_texts(path):
    """Yield (role, timestamp, text) for every text block in a Claude Code transcript."""
    for line in path.open(encoding="utf-8", errors="replace"):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        msg = rec.get("message") or {}
        content = msg.get("content")
        role = msg.get("role") or rec.get("type")
        blocks = [content] if isinstance(content, str) else (content or [])
        for b in blocks:
            if isinstance(b, str):
                yield role, rec.get("timestamp"), b
            elif isinstance(b, dict) and b.get("type") == "text":
                yield role, rec.get("timestamp"), b.get("text", "")
            elif isinstance(b, dict) and b.get("type") == "tool_result":
                c = b.get("content")
                if isinstance(c, list):
                    c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                if isinstance(c, str):
                    yield "tool_result", rec.get("timestamp"), c


def main():
    con = sqlite3.connect(f"file:{DATA / 'orx.db'}?mode=ro", uri=True)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "native").mkdir(exist_ok=True)
    sessions = rows(con, "chat_sessions")
    messages = rows(con, "chat_messages")
    turns = rows(con, "chat_turns")
    for m in messages:
        m["parts"] = parse(m.pop("parts_json"))
    for t in turns:
        for k in ("prepared_input", "settings_json"):
            t[k] = parse(t.get(k))
    index = []
    transcripts = {p.stem: p for p in DATA.rglob("*.jsonl")}
    transcripts.update({p.stem: p for p in (Path.home() / ".claude/projects").rglob("*.jsonl")})
    for s in sessions:
        sid = s["id"]
        s["messages"] = sorted([m for m in messages if m["session_id"] == sid], key=lambda m: m["created_at"])
        s["turns"] = [t for t in turns if t["session_id"] == sid]
        for m in s["messages"]:
            for p in m["parts"] if isinstance(m["parts"], list) else []:
                if isinstance(p, dict) and p.get("type") == "text":
                    index.append({"session": sid, "title": s.get("title"), "message": m["id"], "role": m["role"],
                                  "created_at": m["created_at"], "source": "dashboard", "text": p.get("text", "")})
        native_ids = {m.get(k) for m in s["messages"] for k in ("base_native_session_id", "result_native_session_id")}
        native_ids |= {s.get("native_session_id")}
        s["native_transcripts"] = []
        for nid in sorted(i for i in native_ids if i):
            src = transcripts.get(nid)
            if src is None:
                s["native_transcripts"].append({"id": nid, "found": False})
                continue
            subagents = sorted((src.parent / nid / "subagents").glob("*.jsonl"))
            for f in [src] + subagents:
                dest = OUT / "native" / (f"{nid}.jsonl" if f == src else f"{nid}__{f.name}")
                shutil.copy2(f, dest)
                s["native_transcripts"].append({"id": nid, "file": dest.name, "found": True, "source": str(f),
                                                "bytes": f.stat().st_size, "subagent": f != src})
                for role, ts, text in native_texts(f):
                    index.append({"session": sid, "title": s.get("title"), "message": dest.name, "role": role,
                                  "created_at": ts, "source": "native-subagent" if f != src else "native", "text": text})
    (OUT / "sessions.json").write_text(json.dumps(sessions, indent=1, ensure_ascii=False, default=str) + "\n")
    (OUT / "experiments.json").write_text(json.dumps(rows(con, "local_experiments"), indent=1, ensure_ascii=False, default=str) + "\n")
    with (OUT / "text_index.jsonl").open("w", encoding="utf-8") as f:
        for r in index:
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
    for s in sessions:
        print(s["id"], "|", s.get("title"), "| messages", len(s["messages"]), "| native",
              [(t["id"][:8], t["found"], t.get("bytes")) for t in s["native_transcripts"]])
    print("text blocks indexed:", len(index), "->", OUT)


if __name__ == "__main__":
    main()
