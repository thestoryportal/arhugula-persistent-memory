"""Team-dashboard Science Report tile, view-only. Redraws every 5 s from docs/c10_scoreboard.json
(brief, current work, results, queue; maintained by the program session) plus a live line for the
GPU experiment running now (process table + newest stage log).
Usage: python3 dashboard_report.py [--once COLS ROWS]
"""
import glob, json, os, re, shutil, subprocess, sys, textwrap, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(ROOT, "docs", "c10_scoreboard.json")
RESET, BOLD, ITAL = "\033[0m", "\033[1m", "\033[3m"
FG, BG = "\033[38;5;{}m".format, "\033[48;5;{}m".format
STEP = {"c10u": "step 3", "c10v": "step 4", "c10w": "step 5", "c10x": "step 6", "c10y": "step 7", "c10z": "ASTRA"}
KIND = {"write": 39, "injection": 141, "candidate": 214, "inconclusive": 244, "stopped": 196}


def fit(t, w):
    return t if len(t) <= w else t[: max(w - 1, 0)] + "…"


def section(title, color, cols):
    return f"{BOLD}{FG(231)}{BG(color)} {title} {RESET}{FG(color)}{'━' * max(cols - len(title) - 2, 0)}{RESET}"


def gpu_line():
    ps = subprocess.run(["/bin/ps", "-axo", "command"], capture_output=True, text=True).stdout
    m = next((m for m in re.finditer(r"experiments/track_c/(c10[a-z])_\w+\.py ([\w-]+)", ps) if m.group(2) != "_job"), None)
    if not m:
        return f"{FG(244)}GPU idle — nothing running right now{RESET}"
    logs = sorted(glob.glob(os.path.join(ROOT, "results", "c10*_logs", "**", "*.log"), recursive=True), key=os.path.getmtime)
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
    try:
        b = json.load(open(BOARD))
    except (OSError, ValueError) as e:
        return [f"{FG(196)}Science report: cannot read {BOARD}: {e}{RESET}"]
    goal, out_of = b.get("goal", 61), b.get("out_of", 72)
    out = [f"{BOLD}{FG(231)}{BG(25)}{fit(' ■ SCIENCE REPORT · teaching the model made-up names', cols - 26).ljust(cols - 26)}"
           f"{BG(238)} updated {b.get('updated', '?')[-15:]:<15} {RESET}"]
    out.append(f" {ITAL}Goal: {goal} of {out_of} reworded questions right · ordinary facts already get ~69 · bar ┃ marks the goal{RESET}")
    out.append(section("WHAT IT MEANS", 30, cols))
    for line in textwrap.wrap(b.get("brief", ""), cols - 2)[:7]:
        out.append(f" {BOLD}{line}{RESET}")
    out.append(section("NOW", 28, cols))
    out.append(" " + gpu_line())
    for c in b.get("current", []):
        out.append(f" {FG(214)}◆{RESET} {fit(c['what'], cols - 4)}")
    out.append(section("RESULTS SO FAR (newest first)", 24, cols))
    bw = 18
    queue = b.get("queue", [])
    room = rows - len(out) - 1 - min(len(queue), 6) - 1
    for r in list(reversed(b.get("results", [])))[: max(room, 0)]:
        kc = KIND.get(r.get("kind"), 252)
        head = f" {FG(245)}{r['date'][5:]}{RESET} {bar(r.get('best'), goal, out_of, bw)} {BOLD}{FG(kc)}{fit(r['score'], 26):<26}{RESET} "
        rest = cols - 7 - bw - 28
        out.append(head + fit(f"{r['name']} — {r['verdict']}", max(rest, 10)))
    out.append(section("QUEUE (in order)", 96, cols))
    for i, q in enumerate(queue[: max(rows - len(out) - 1, 0)], 1):
        out.append(f" {BOLD}{FG(141)}{i:>2}.{RESET} {fit(q['name'], cols - 44):<{cols - 44}} {FG(214)}{fit(q['status'], 26):<26}{RESET} {FG(245)}{fit(q.get('time', ''), 12)}{RESET}")
    return out[:rows]


def main():
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(render(int(sys.argv[i + 1]), int(sys.argv[i + 2]))))
        return
    while True:
        cols, rows = shutil.get_terminal_size()
        lines = render(cols, rows)
        sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(5)


if __name__ == "__main__":
    main()
