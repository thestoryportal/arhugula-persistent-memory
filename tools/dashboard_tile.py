"""One team-dashboard tile, view-only. Reads one tmux session's screen (Codex or Claude Code) every 2 s
and redraws it as a header (name, live status, last change), an info line (model, context, working
timer, current task, helper agents) and an activity feed (one line per step, icon by kind).
Usage: python3 dashboard_tile.py <session> <label> <256-colour> [--once COLS ROWS]
"""
import os, re, shutil, subprocess, sys, time

RESET, BOLD = "\033[0m", "\033[1m"
FG = "\033[38;5;{}m".format
BG = "\033[48;5;{}m".format
CHROME = re.compile(r"^[─━\s]*$|^\s*[›❯]\s*$|\? for shortcuts|Ask Codex to do anything|^\s*Tip:|ctrl\+t to expand"
                    r"|^\s*[◔◱✦⚡⏵◴◑☉⧖⌂]|^\s*/\S+.*⎇|auto mode on|esc to interrupt|^\s*⏺ main\s*$")
KINDS = [  # (pattern on the step text, icon, colour)
    (re.compile(r"^(Failed|Error)|HALT|Traceback", re.I), "✖", 196),
    (re.compile(r"^(DONE|Done|Completed|Committed)\b|PASS|✅"), "✔", 40),
    (re.compile(r"^(Ran|Running|Bash)\b"), "▶", 39),
    (re.compile(r"^(Edited|Edit|Wrote|Write|Updated|Created|Added)\b"), "✎", 214),
    (re.compile(r"^(Explored|Read|Reading|Search|Searched|Grep|List)\b"), "⌕", 111),
]


def sh(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def parse(screen):
    lines = [l.rstrip() for l in screen.splitlines()]
    tail = [l for l in lines if l.strip()][-12:]
    info = {"model": None, "context": None, "timer": None, "helpers": []}
    steps = []
    for l in lines:
        s = l.strip()
        if m := re.search(r"(GPT-[\w.-]+ \w+)", l):
            info["model"] = m.group(1)
        if m := re.search(r"✱\s*([\w.]+(?: [\w.]+)*)", l):
            info["model"] = m.group(1)
        if m := re.search(r"Context (\d+)% left", l):
            info["context"] = f"{m.group(1)}% context left"
        if m := re.search(r"◔ ([\d,]+) \((\d+)%\)", l):
            info["context"] = f"{m.group(1)} tokens in context"
        if l in tail and (m := re.search(r"Working \(([^•)]+)", l) or re.search(r"^[^\w\s]\s\S+… \((\d+[smh][^·)]*)", s)):
            info["timer"] = m.group(1).strip()
        if m := re.match(r"◯ \S+\s{2,}(.+)", s):
            info["helpers"].append("  ·  ".join(re.split(r"\s{2,}", m.group(1).strip())))
            continue
        if not s or CHROME.search(l):
            continue
        if s[0] in "•⏺":
            steps.append([s[1:].strip(), None])
        elif s[0] in "└⎿" and steps and steps[-1][1] is None and not s[1:].strip().startswith("Tip:"):
            steps[-1][1] = s[1:].strip()
    return info, steps


def status(screen, changed, now):
    recent = "\n".join(l for l in screen.splitlines() if l.strip())[-1500:]
    if re.search(r"esc to interrupt|Working \(|^[^\w\s]\s\S+… \(\d", recent, re.M):
        return "WORKING", 28
    if re.search(r"\d+ question|Do you want|\[y/n\]|\(y/n\)", recent):
        return "ASKING", 136
    if changed and now - changed < 15:
        return "ACTIVE", 30
    return "IDLE", 240


def ago(changed, now):
    if not changed:
        return "—"
    a = int(now - changed)
    return f"{a}s ago" if a < 60 else f"{a // 60}m ago" if a < 3600 else f"{a // 3600}h{a % 3600 // 60}m ago"


def fit(text, width):
    return text if len(text) <= width else text[: max(width - 1, 0)] + "…"


def render(session, label, color, cols, rows, state):
    screen = sh("tmux", "capture-pane", "-p", "-t", session)
    if screen is None:
        screen = f"• session {session} is not running"
    task = (sh("tmux", "display", "-p", "-t", session, "#{pane_title}") or "").strip()
    now = time.time()
    if screen != state.get("last"):
        if "last" in state:
            state["changed"] = now
        state["last"] = screen
    st, stbg = status(screen, state.get("changed"), now)
    info, steps = parse(screen)
    left, right = f" ■ {label} ", f" {st} · last change {ago(state.get('changed'), now)} "
    out = [f"{BOLD}{FG(231)}{BG(color)}{fit(left, cols - len(right)).ljust(cols - len(right))}{BG(stbg)}{right}{RESET}"]
    bits = [b for b in (info["model"], info["context"], f"working {info['timer']}" if info["timer"] else None) if b]
    out.append(f"{FG(color)}{BOLD}{fit(' ' + '  ·  '.join(bits), cols)}{RESET}")
    out.append(f"{BOLD}{fit(' ↳ ' + task, cols)}{RESET}")
    for h in info["helpers"][:3]:
        out.append(f"{FG(141)}{fit('   ◯ helper: ' + h, cols)}{RESET}")
    out.append(f"{FG(color)}{'─' * cols}{RESET}")
    feed = []
    for text, detail in steps:
        icon, icol = "›", 252
        for pat, ic, c in KINDS:
            if pat.search(text):
                icon, icol = ic, c
                break
        feed.append(f" {FG(icol)}{BOLD}{icon}{RESET} {BOLD if icon == '›' else ''}{fit(text, cols - 4)}{RESET}")
        if detail:
            feed.append(f"   {FG(244)}└{RESET} {fit(detail, cols - 6)}")
    room = rows - len(out) - 1
    out += feed[-room:] if room > 0 else []
    return out


def main():
    session, label, color = sys.argv[1], sys.argv[2], int(sys.argv[3])
    state = {}
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(render(session, label, color, int(sys.argv[i + 1]), int(sys.argv[i + 2]), state)))
        return
    while True:
        cols, rows = shutil.get_terminal_size()
        lines = render(session, label, color, cols, rows, state)
        st = status(state["last"], state.get("changed"), time.time())[0]
        subprocess.run(["tmux", "set-option", "-p", "-t", os.environ.get("TMUX_PANE", ""), "@status", st],
                       capture_output=True)
        sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(2)


if __name__ == "__main__":
    main()
