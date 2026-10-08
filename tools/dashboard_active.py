"""Dashboard 'Active' tab, view-only: the lead session plus every team session that is working now or whose
screen content changed in the last ACTIVE_S seconds, stacked full-width, each drawn by dashboard_tile.render.
Content, not tmux window_activity: a resize makes every idle TUI redraw identical content, which tmux counts
as activity. Changes are observed by this process, so after a restart an idle session reappears only when it changes.
Usage: python3 dashboard_active.py [--once COLS ROWS]
"""
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_tile import render, sh, status, RESET, BOLD, FG  # noqa: E402

ACTIVE_S = 1800
SKIP = {"dashboard", "dashboard_new", "helpers"}


def label(s):
    special = {"program": "LEAD · program session", "codexviz": "Codex · Lab View build",
               "codexviz2": "Codex · Lab View v2 build", "codexz": "Codex Z · ASTRA build"}
    return special.get(s) or (f"Codex {s[5:].upper() or 'A'}" if s.startswith("codex") else s)


def active_sessions(now, states):
    names = (sh("tmux", "list-sessions", "-F", "#{session_name}") or "").split()
    act = []
    for n in names:
        if n in SKIP or n.startswith("view-"):
            continue
        screen = sh("tmux", "capture-pane", "-p", "-t", n) or ""
        st = states.setdefault(n, {})
        if screen != st.get("last"):
            if "last" in st:
                st["changed"] = now
            st["last"] = screen
        changed = st.get("changed")
        if n == "program" or status(screen, changed, now)[0] in ("WORKING", "ASKING") or (changed and now - changed < ACTIVE_S):
            act.append((n, changed or 0))
    return [n for n, _ in sorted(act, key=lambda x: (x[0] != "program", -x[1]))]


def frame(cols, rows, states):
    now = time.time()
    names = active_sessions(now, states)
    head = f"{BOLD}{FG(231)}\033[48;5;25m{' ■ ACTIVE AGENTS · working now or changed in the last 30 min':<{cols}}{RESET}"
    if not names:
        return [head, f" {FG(245)}No agent is working or has changed its screen in the last 30 minutes.{RESET}"]
    each = max((rows - 1) // len(names), 6)
    lines = [head]
    for i, n in enumerate(names):
        if len(lines) + 4 > rows:
            lines.append(f" {FG(245)}… {len(names) - i} more active (make the window taller){RESET}")
            break
        lines += render(n, label(n), 25 if n == "program" else 30 + 6 * i, cols, min(each, rows - len(lines)), states.setdefault(n, {}))
    return lines[:rows]


def main():
    states = {}
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(frame(int(sys.argv[i + 1]), int(sys.argv[i + 2]), states)))
        return
    while True:
        cols, rows = os.get_terminal_size(sys.stdout.fileno())
        lines = frame(cols, rows, states)
        sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(3)


if __name__ == "__main__":
    main()
