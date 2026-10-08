"""Dashboard helper-agent tabs, view-only.
  manager mode (the dashboard's 'helpers' tab): lists every Claude Code subagent active in the last RECENT_S
    seconds (any session, from ~/.claude/projects/*/*/subagents/), opens one window per running subagent in
    the tmux session 'helpers' (linked into the dashboard too) and closes it LINGER_S after the subagent
    finishes (or after it has been silent for RECENT_S). `teamdash helpers` opens only that session.
  list mode: the same list, display only (the 'helpers' session's index window).
  view mode: one subagent's job, parent, model, run time and its steps live.
Usage: python3 dashboard_subagents.py [manager] | list | view <agent.jsonl> | [--once COLS ROWS]
"""
import calendar, glob, json, os, subprocess, sys, time

D, H = "dashboard", "helpers"
RECENT_S, LINGER_S, MAX_TABS = 900, 60, 8
SELF = os.path.abspath(__file__)
PROJECTS = os.path.expanduser("~/.claude/projects")
RESET, BOLD = "\033[0m", "\033[1m"
FG, BG = "\033[38;5;{}m".format, "\033[48;5;{}m".format
TOOL = {"Bash": ("▶", 39), "Edit": ("✎", 214), "Write": ("✎", 214), "NotebookEdit": ("✎", 214),
        "Read": ("⌕", 111), "Grep": ("⌕", 111), "Glob": ("⌕", 111), "WebFetch": ("⌕", 111), "WebSearch": ("⌕", 111)}
_parent_cache = {}


def fit(t, w):
    t = " ".join(str(t).split())
    return t if len(t) <= w else t[: max(w - 1, 0)] + "…"


def tmux(*a):
    return subprocess.run(["tmux", *a], capture_output=True, text=True).stdout


def records(path):
    out = []
    for line in open(path, errors="replace"):
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def parent_name(path):
    sid_dir = os.path.dirname(os.path.dirname(path))
    if sid_dir not in _parent_cache:
        name = os.path.basename(sid_dir)[:8]
        try:
            first = open(sid_dir + ".jsonl", errors="replace").read(20000)
            if "Resume the LLM-as-Database program" in first:
                name = "LEAD (program)"
        except OSError:
            pass
        _parent_cache[sid_dir] = name
    return _parent_cache[sid_dir]


def info(path):
    """meta + status for one subagent transcript."""
    try:
        meta = json.load(open(path[:-6] + ".meta.json"))
    except (OSError, ValueError):
        meta = {}
    recs = records(path)
    last_assistant = next((r for r in reversed(recs) if r.get("type") == "assistant"), None)
    blocks = (last_assistant or {}).get("message", {}).get("content") or []
    idle = time.time() - os.path.getmtime(path)
    handback = any(isinstance(b, dict) and b.get("name") == "SubagentHandback" for b in blocks)
    ended = handback or (last_assistant is not None and recs[-1].get("type") == "assistant"
                         and not any(isinstance(b, dict) and b.get("type") == "tool_use" for b in blocks))
    status = "DONE" if ended and (handback or idle > 10) else "SILENT" if idle > 300 else "RUNNING"
    start = recs[0].get("timestamp") if recs else None
    end = recs[-1].get("timestamp") if recs and status != "RUNNING" else None
    return {"desc": meta.get("description") or "subagent", "model": meta.get("model", "?"), "status": status,
            "idle": idle, "parent": parent_name(path), "start": start, "end": end, "recs": recs}


def elapsed(start, end=None):
    if not start:
        return "?"
    ts = lambda x: calendar.timegm(time.strptime(x[:19], "%Y-%m-%dT%H:%M:%S"))   # transcript timestamps are UTC
    s = int((ts(end) if end else time.time()) - ts(start))
    return f"{s // 60}m{s % 60:02d}s" if s < 3600 else f"{s // 3600}h{s % 3600 // 60:02d}m"


def steps(recs):
    out = []
    for r in recs:
        if r.get("type") != "assistant":
            continue
        for b in r.get("message", {}).get("content") or []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use" and b.get("name") == "SubagentHandback":
                inp = b.get("input") or {}
                out.append(("›", 252, " ".join(str(v) for v in inp.values() if isinstance(v, str)) or "(report handed back)"))
            elif b.get("type") == "tool_use":
                inp = b.get("input") or {}
                what = inp.get("description") or inp.get("command") or inp.get("file_path") or inp.get("pattern") \
                    or inp.get("url") or inp.get("query") or ""
                icon, col = TOOL.get(b.get("name"), ("•", 252))
                out.append((icon, col, f"{b.get('name')}: {what}"))
            elif b.get("type") == "text" and b.get("text", "").strip():
                out.append(("›", 252, b["text"]))
    return out


def view_lines(path, cols, rows):
    i = info(path)
    st_bg = {"RUNNING": 28, "DONE": 25, "SILENT": 240}[i["status"]]
    left, right = f" ⚙ {i['desc']} ", f" {i['status']} · {elapsed(i['start'], i['end'])} "
    out = [f"{BOLD}{FG(231)}{BG(96)}{fit(left, max(cols - len(right), 8)).ljust(max(cols - len(right), 8))}{BG(st_bg)}{right}{RESET}",
           f" {FG(141)}{BOLD}helper of {i['parent']} · model {i['model']} · {len(i['recs'])} log records{RESET}"]
    prompt = next((r["message"]["content"] for r in i["recs"] if r.get("type") == "user"
                   and isinstance(r.get("message", {}).get("content"), str)), "")
    out.append(f" {BOLD}job:{RESET} {fit(prompt, max(cols - 7, 8))}")
    out.append(f"{FG(96)}{'━' * cols}{RESET}")
    feed = steps(i["recs"])
    if i["status"] == "DONE" and feed and feed[-1][0] == "›":
        room = max(rows - len(out) - 2, 1)
        out.append(f" {BOLD}{FG(40)}✔ finished — final message:{RESET}")
        words, line, wrapped = feed[-1][2].split(), "", []
        for w in words:
            if len(line) + len(w) + 1 > cols - 3:
                wrapped.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        wrapped.append(line)
        out += [f"  {l}" for l in wrapped[-room:]]
        return out[:rows]
    for icon, col, text in feed[-max(rows - len(out), 0):]:
        out.append(f" {FG(col)}{BOLD}{icon}{RESET} {BOLD if icon == '›' else ''}{fit(text, max(cols - 4, 8))}{RESET}")
    return out[:rows]


def recent_agents():
    now, found = time.time(), []
    for p in glob.glob(os.path.join(PROJECTS, "*", "*", "subagents", "agent-*.jsonl")):
        if now - os.path.getmtime(p) < RECENT_S:
            found.append(p)
    return sorted(found, key=os.path.getmtime, reverse=True)


def manage(agents):
    """Open a window per running subagent (up to MAX_TABS), close finished/silent ones after LINGER_S."""
    if not tmux("list-sessions", "-F", "#{session_name}").split().count(H):
        tmux("new-session", "-d", "-s", H, "-n", "index", f"/usr/bin/python3 '{SELF}' list")
        tmux("set-option", "-t", H, "status-style", "bg=colour235,fg=colour252")
        tmux("set-option", "-t", H, "status-left", "#[bg=colour96,fg=colour231,bold]  HELPER AGENTS  #[default] ")
        tmux("set-option", "-t", H, "status-left-length", "30")
        tmux("set-option", "-t", H, "window-status-current-format", "#[bg=colour214,fg=colour16,bold] #I #W ")
        tmux("set-option", "-t", H, "remain-on-exit", "on")
    open_tabs = {}
    for line in tmux("list-windows", "-t", H, "-F", "#{window_id} #{@agent}").splitlines():
        wid, _, aid = line.partition(" ")
        if aid:
            open_tabs[aid] = wid
    in_dash = set(tmux("list-windows", "-t", D, "-F", "#{window_id}").split())
    for wid in open_tabs.values():   # re-link after a dashboard rebuild
        if wid not in in_dash:
            tmux("link-window", "-d", "-s", wid, "-t", D + ":")
    infos = {os.path.basename(p)[6:-6]: (p, info(p)) for p in agents}
    for aid, wid in open_tabs.items():
        i = infos.get(aid, (None, None))[1]
        if i is None or (i["status"] != "RUNNING" and i["idle"] > LINGER_S):
            tmux("kill-window", "-t", wid)
    running = [(aid, p, i) for aid, (p, i) in infos.items() if i["status"] == "RUNNING" and aid not in open_tabs]
    for aid, p, i in running[: max(MAX_TABS - len(open_tabs), 0)]:
        wid = tmux("new-window", "-d", "-P", "-F", "#{window_id}", "-t", H + ":", "-n", "⚙ " + fit(i["desc"], 16),
                   f"/usr/bin/python3 '{SELF}' view '{p}'").strip()
        if wid:
            tmux("set-option", "-w", "-t", wid, "@agent", aid)
            tmux("link-window", "-d", "-s", wid, "-t", D + ":")
    return infos


def manager_lines(infos, cols, rows):
    out = [f"{BOLD}{FG(231)}{BG(96)}{fit(' ⚙ HELPER AGENTS · each running helper gets its own tab (closes 1 min after it finishes)', cols).ljust(cols)}{RESET}"]
    if not infos:
        return out + [f" {FG(245)}No helper agent has been active in the last 15 minutes.{RESET}"]
    for aid, (p, i) in infos.items():
        col = {"RUNNING": 40, "DONE": 111, "SILENT": 245}[i["status"]]
        out.append(f" {BOLD}{FG(col)}{i['status']:<8}{RESET} {fit(i['desc'], max(cols - 46, 10)):<{max(cols - 46, 10)}} "
                   f"{FG(141)}{fit(i['parent'], 15):<15}{RESET} {FG(245)}{elapsed(i['start'], i['end']):>8} {i['model']}{RESET}")
    return out[:rows]


def draw(lines):
    sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J")
    sys.stdout.flush()


def main():
    args = sys.argv[1:]
    if "--once" in args:
        i = args.index("--once")
        cols, rows = int(args[i + 1]), int(args[i + 2])
        if args and args[0] == "view":
            print("\n".join(view_lines(args[1], cols, rows)))
        else:
            print("\n".join(manager_lines({os.path.basename(p)[6:-6]: (p, info(p)) for p in recent_agents()}, cols, rows)))
        return
    import dashboard_live
    stamp = dashboard_live.source_stamp(dashboard_live.TOOLS)
    while True:
        dashboard_live.maybe_reload(stamp)
        cols, rows = os.get_terminal_size(sys.stdout.fileno())
        if args and args[0] == "view":
            draw(view_lines(args[1], cols, rows) if os.path.exists(args[1]) else ["(transcript gone)"])
        elif args and args[0] == "list":
            draw(manager_lines({os.path.basename(p)[6:-6]: (p, info(p)) for p in recent_agents()}, cols, rows))
        else:
            draw(manager_lines(manage(recent_agents()), cols, rows))
        time.sleep(3)


if __name__ == "__main__":
    main()
