"""Team-dashboard Science Report: the 'science' tab, view-only. Redraws every 5 s, and
clears the pane (history too) when its size changes. NOW is derived live (dashboard_live: rulings awaited, GPU job or
last experiment outcome, working builds, helpers). Next-actions/updated come from program/program_state.json;
program/registers/c10_scoreboard.json supplies explicitly dated narrative and historical score explanations only.
Usage: python3 dashboard_report.py [--once COLS ROWS]
"""
import glob, json, os, re, shutil, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_live as live  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BOARD = os.path.join(ROOT, "program/registers/c10_scoreboard.json")
PROGRAM = os.path.join(ROOT, "program/program_state.json")
RESET, BOLD, ITAL = "\033[0m", "\033[1m", "\033[3m"
FG, BG = "\033[38;5;{}m".format, "\033[48;5;{}m".format
STEP = {"c10u": "step 3", "c10v": "step 4", "c10w": "step 5", "c10x": "step 6", "c10y": "step 7", "c10z": "ASTRA"}
KIND = {"write": 39, "injection": 141, "candidate": 214, "inconclusive": 244, "stopped": 196}


def fit(t, w):
    """`t` in at most w cells, ending in … when cut."""
    return t if live.cells(t) <= w else live.clip(t, max(w - 1, 0)) + "…"


def col(t, w):
    """`t` fitted and padded to exactly w cells: a table column."""
    t = fit(t, w)
    return t + " " * (w - live.cells(t))


def wrap(text, w):
    """Words filled into lines of at most w cells (a single word wider than that is cut by render's final clip)."""
    lines = []
    for word in text.split():
        if lines and live.cells(lines[-1] + " " + word) <= w:
            lines[-1] += " " + word
        else:
            lines.append(word)
    return lines


def section(title, color, w):
    return f"{BOLD}{FG(231)}{BG(color)} {title} {RESET}{FG(color)}{'━' * max(w - len(title) - 2, 0)}{RESET}"


def gpu_line():
    ps = subprocess.run(["/bin/ps", "-axo", "command"], capture_output=True, text=True).stdout
    m = next((m for m in re.finditer(r"code/lab/track_c/(c10[a-z])_\w+\.py ([\w-]+)", ps) if m.group(2) != "_job"), None)
    if not m:
        return f"{FG(244)}GPU idle — nothing running right now{RESET}"
    logs = sorted(glob.glob(os.path.join(ROOT, "experiments", "c10*", "runs", "*", "logs", "**", "*.log"), recursive=True), key=os.path.getmtime)
    last = ""
    if logs:
        lines = [l.strip() for l in open(logs[-1], errors="replace") if l.strip()]
        done = [l for l in lines if l.startswith("completed ")]
        last = f" · {len(done)} jobs done, last: {done[-1].split(';')[0][10:]}" if done else ""
    return f"{BOLD}{FG(40)}● RUNNING{RESET} {BOLD}{STEP.get(m.group(1), m.group(1))}, stage {m.group(2)}{RESET}{last}"


def bar(best, goal, out_of, width):
    if best is None:
        return f"{FG(240)}{'·' * width}{RESET}"
    fill, mark = round(best / out_of * width), round(goal / out_of * width)
    cells = []
    for i in range(width):
        ch = "█" if i < fill else ("┃" if i == mark else "░")
        col = 40 if best >= goal else 214 if best >= 30 else 39
        cells.append(f"{FG(col if i < fill else 196 if i == mark else 238)}{ch}")
    return "".join(cells) + RESET


def render(cols, rows):
    """At most `rows` lines, none wider than cols - 1 cells: the last column stays empty, so no line can wrap."""
    w = cols - 1
    try:
        with open(PROGRAM) as source:
            program = json.load(source)
        if not isinstance(program, dict) or not isinstance(program.get("next_actions"), list) or not all(isinstance(a, str) for a in program["next_actions"]):
            raise ValueError("next_actions must be a list of text entries")
    except (OSError, ValueError) as e:
        return [live.clip(f"{FG(196)}Science report: cannot read program state {PROGRAM}: {e}{RESET}", w)]
    try:
        with open(BOARD) as source:
            b = json.load(source)
    except (OSError, ValueError) as e:
        b = {"brief": f"Narrative unavailable: cannot read {BOARD}: {e}", "updated": "unavailable"}
    goal, out_of = b.get("goal", 61), b.get("out_of", 72)
    out = [f"{BOLD}{FG(231)}{BG(25)} ■ SCIENCE REPORT · updated {program.get('updated', '?')}{RESET}"]
    out.append(f" {ITAL}{fit(f'Goal: {goal} of {out_of} reworded questions right · ordinary facts already get ~69 · bar ┃ marks the goal', w - 1)}{RESET}")
    out.append(section("NEXT ACTIONS · program/program_state.json", 96, w))
    actions = [line for i, action in enumerate(program["next_actions"], 1)
               for line in wrap(f"{i}. {action}", max(w - 2, 1))]
    room = max(min(rows // 3, rows - len(out) - 1), 1)
    pages = max((len(actions) + room - 1) // room, 1)
    page = int(time.time() // 10) % pages
    out.append(f" Page {page + 1}/{pages} · rotates every 10 s · source includes recorded history")
    out += [" " + line for line in actions[page * room:(page + 1) * room]] or [" No next-actions recorded."]
    out.append(section("NOW", 28, w))
    for line in live.now_lines(live.gather(), time.time()):
        color = {"!": 196, "▲": 208, "▸": 40, "»": 214, "◦": 141}.get(line[0], 244)
        out.append(f" {BOLD if line[0] in '!▲▸' else ''}{FG(color)}{fit(line, w - 1)}{RESET}")
    out.append(f" Scoreboard narrative only · as of {b.get('updated', '?')} · program/registers/c10_scoreboard.json")
    behind = live.newer_events(live.board_epoch(b.get("updated")), live.events())
    if behind:
        out.append(f"{BOLD}{FG(231)}{BG(124)}{col(' ⚠ The text below predates: ' + '; '.join(behind[-3:]) + ' (the program updates it)', w)}{RESET}")
    out.append(section("WHAT IT MEANS", 30, w))
    brief = wrap(b.get("brief", ""), w - 1)
    # The v2 path is wider than a 40-column pane; the file name is unique and the full path heads this section.
    more = "  (more: c10_scoreboard.json)"
    if len(brief) > 7:   # the pane cannot scroll: say so instead of cutting mid-sentence
        brief = brief[:6] + [fit(brief[6], max(w - 1 - len(more), 1)) + more]
    for line in brief:
        out.append(f" {BOLD}{line}{RESET}")
    out.append(section("SCOREBOARD RESULTS · dated narrative (newest first)", 24, w))
    bw = 18
    room = rows - len(out)
    for r in list(reversed(b.get("results", [])))[: max(room, 0)]:
        kc = KIND.get(r.get("kind"), 252)
        head = f" {FG(245)}{r['date'][5:]}{RESET} {bar(r.get('best'), goal, out_of, bw)} {BOLD}{FG(kc)}{col(r['score'], 26)}{RESET} "
        out.append(head + fit(f"{r['name']} — {r['verdict']}", max(w - 7 - bw - 28, 10)))
    # [LAW:single-enforcer] the one place the pane width is enforced; fit/col/wrap only lay the lines out to it
    return [live.clip(line, w) for line in out[:rows]]


def screen(cols, rows):
    """The report, or - when it cannot be drawn this time - one red line saying why; the next redraw tries again."""
    try:
        return render(cols, rows)
    except Exception as e:   # [LAW:no-silent-failure] shown in the pane in place of the report, never swallowed
        return [live.clip(f"{BOLD}{FG(196)} ✖ {type(e).__name__}: {e} · the Science Report retries every 5 s{RESET}", cols - 1)]


CLEAR_ALL = "\033[2J\033[3J"   # screen and history: tmux re-wraps old frames into fragments when a pane is resized


def frame(lines, clear):
    return clear + "\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J"


def main():
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(render(int(sys.argv[i + 1]), int(sys.argv[i + 2]))))
        return
    stamp = live.source_stamp(live.TOOLS)
    drawn = None
    while True:
        live.maybe_reload(stamp)
        size = os.get_terminal_size(sys.stdout.fileno())   # the live pane size; ignores a stale inherited $COLUMNS
        sys.stdout.write(frame(screen(size.columns, size.lines), CLEAR_ALL if size != drawn else ""))
        sys.stdout.flush()
        drawn = size
        time.sleep(5)


if __name__ == "__main__":
    main()
