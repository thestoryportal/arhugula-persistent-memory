"""Dashboard 'Active' tab, view-only: only the team sessions whose screens changed in the last
ACTIVE_S seconds (tmux window_activity = last output), stacked full-width, each drawn by dashboard_tile.render.
Usage: python3 dashboard_active.py [--once COLS ROWS]
"""
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dashboard_tile import render, RESET, BOLD, FG  # noqa: E402

ACTIVE_S = 1800
SKIP = {"dashboard", "dashboard_new"}


def label(s):
    return "LEAD · program session" if s == "program" else f"Codex {s[5:].upper() or 'A'}" if s.startswith("codex") else s


def active_sessions(now):
    out = subprocess.run(["tmux", "list-windows", "-a", "-F", "#{session_name} #{window_activity}"],
                         capture_output=True, text=True).stdout.split("\n")
    rows = [l.split() for l in out if l.strip()]
    act = [(n, int(t)) for n, t in rows if n not in SKIP and not n.startswith("view-") and now - int(t) < ACTIVE_S]
    return [n for n, _ in sorted(act, key=lambda x: (x[0] != "program", -x[1]))]


def frame(cols, rows, states):
    now = time.time()
    names = active_sessions(now)
    head = f"{BOLD}{FG(231)}\033[48;5;25m{' ■ ACTIVE AGENTS · changed in the last 30 min':<{cols}}{RESET}"
    if not names:
        return [head, f" {FG(245)}No agent has changed its screen in the last 30 minutes.{RESET}"]
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
