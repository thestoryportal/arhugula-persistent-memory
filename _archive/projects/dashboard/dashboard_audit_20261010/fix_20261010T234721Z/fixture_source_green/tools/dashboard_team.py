"""One Team pane; compose the current lead and live Codex sessions every 3 s.
Usage: /usr/bin/python3 dashboard_team.py [--once COLS ROWS]
"""
import collections, os, subprocess, sys, time
import dashboard_live as live
import dashboard_tile as tile
from dashboard_active import label

MIN_COL, TILE_ROWS = 52, 6


def snapshot():
    def read(*args):
        return subprocess.run(args, capture_output=True, text=True, check=True).stdout
    names = live.team_sessions(read("tmux", "list-sessions", "-F", "#{session_name}").split())
    lead = live.read_lead()
    names = sorted(n for n in names if n == lead or n.startswith("codex"))
    screens = {n: read("tmux", "capture-pane", "-p", "-t", n) for n in names}
    titles = {n: read("tmux", "display", "-p", "-t", n, "#{pane_title}").strip() for n in names}
    return names, lead, screens, titles


def frame(cols, rows, states):
    w, now = max(cols - 1, 1), time.time()
    try:
        names, lead, screens, titles = snapshot()
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        return [live.clip(f"Team unavailable: {error}", w)], "team counts unavailable"
    for retired in set(states) - set(names):
        del states[retired]
    counts = collections.Counter(tile.observe(screens[n], states.setdefault(n, {}), now)[0] for n in names)
    summary = " · ".join(f"{name.lower()} {counts[name]}" for name in ("WORKING", "ASKING", "ACTIVE", "IDLE"))
    lines = [f"{tile.BOLD}{tile.FG(231)}{tile.BG(25)} ■ TEAM · {len(names)} live sessions · refresh 3 s{tile.RESET}", " " + summary]
    if lead in names:
        lines += tile.render(lead, "LEAD · " + lead, 25, w, TILE_ROWS, states[lead], screens[lead], titles[lead], now)
    else:
        lines.append(" LEAD · no live lead session found")
    builders = [n for n in names if n != lead]
    ncol = min(max((w + 1) // (MIN_COL + 1), 1), 5)
    available = max(rows - len(lines) - 1, 0)
    slots = max(available // TILE_ROWS, 1) * ncol
    pages = max((len(builders) + slots - 1) // slots, 1)
    page = int(now // 10) % pages
    lines.append(f" Builders · page {page + 1}/{pages} · rotates every 10 s")
    colw = max((w - ncol + 1) // ncol, 1)
    shown = builders[page * slots:(page + 1) * slots]
    for i in range(0, len(shown), ncol):
        tiles = [tile.render(n, label(n), 30 + 6 * names.index(n) % 180, colw, TILE_ROWS,
                             states[n], screens[n], titles[n], now) for n in shown[i:i + ncol]]
        for k in range(max(len(t) for t in tiles)):
            cells = [live.clip(t[k] if k < len(t) else "", colw) for t in tiles]
            lines.append("│".join(c + tile.RESET + " " * (colw - live.cells(c)) for c in cells))
    return [live.clip(line, w) for line in lines[:rows]], summary


def main():
    states = {}
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(frame(int(sys.argv[i + 1]), int(sys.argv[i + 2]), states)[0]))
        return
    stamp = live.source_stamp(live.TOOLS)
    while True:
        live.maybe_reload(stamp)
        cols, rows = os.get_terminal_size(sys.stdout.fileno())
        lines, counts = frame(cols, rows, states)
        if os.environ.get("TMUX_PANE"):
            # One metadata update publishes counts from this exact roster, including off-page builders.
            subprocess.run(["tmux", "set-option", "-w", "-t", os.environ["TMUX_PANE"], "@team_counts", counts], check=True)
        sys.stdout.write("\033[H" + "\033[K\n".join(lines) + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(3)


if __name__ == "__main__":
    main()
