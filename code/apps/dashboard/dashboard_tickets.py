"""Live tickets tab: /usr/bin/python3 code/apps/dashboard/dashboard_tickets.py [FOLDER ...].

Every ticket of the lean ticket folders (default: each G-build/LEAN/*/ with tickets/)
with a live timer, a shared timeline, review rounds and every blocking finding.
The only data source is dashboard_tickets_data.snapshot, re-read every 15 s in a
background thread; the screen redraws every second from the latest snapshot, so a
slow gh call never stops the clock. render() is pure: snapshot, UI state, clock and
terminal size in; styled lines out. Python 3.9, stdlib only.
"""
import argparse
import curses
import locale
import statistics
import sys
import threading
import time
import unicodedata
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import List, Optional, Tuple

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

LEAN = Path("/Volumes/memit/corpus-consolidation-toolkit/workspace/runs/20261013-overnight/G-build/LEAN")
REFRESH_S = 15
TARGET_S = 15 * 60
AXIS_MAX_S = 8 * 3600      # the shared timeline shows at most the last 8 h, so today's 15 min tickets stay visible
ACTIVE = ("running", "pr")
# Each state carries a glyph and a word as well as a colour.
STATES = {"running": ("▶", "RUNNING", "cyan"), "pr": ("◆", "PR", "magenta"), "merged": ("■", "MERGED", "green"),
          "ready": ("○", "READY", "blue"), "waiting": ("·", "WAITING", "dim")}
VERDICTS = {"GO": ("✓", "green"), "NO-GO": ("✗", "red")}
CI = {"pass": ("✓", "green"), "fail": ("✗", "red"), "pending": ("…", "yellow"), "none": ("·", "dim")}
BUILD, REVIEW, NOW_MARK, BEFORE = "▒", "█", "│", "‹"
HELP = ("state ▶ running ◆ PR ■ merged (timer final) ○ ready · waiting | reviews ✓ GO ✗ NO-GO ? no verdict | "
        "CI ✓ pass ✗ fail … pending · none | timer ! over 15 min, !! over 30 min | timeline ▒ build █ PR/review "
        "│ now ‹ began earlier | keys j/k ↑/↓ select (scroll when full screen) · Enter/Tab detail full screen · "
        "f folder · a active only · h hide help")

Seg = Tuple[str, str]
Line = List[Seg]


@dataclass(frozen=True)
class UI:
    selected: int = 0
    full: bool = False
    folder: Optional[str] = None
    active_only: bool = False
    help: bool = False
    scroll: int = 0


@dataclass(frozen=True)
class Frame:
    lines: List[Line] = field(default_factory=list)
    max_scroll: int = 0


def clean(value):
    return "".join(" " if ch.isspace() else "?" if unicodedata.category(ch).startswith("C") else ch
                   for ch in str(value))


def cell_width(ch):
    if unicodedata.combining(ch):
        return 0
    return 2 if unicodedata.east_asian_width(ch) in "WF" else 1


def cells(text):
    return sum(cell_width(ch) for ch in text)


def clip(text, width):
    used = 0
    for index, ch in enumerate(text):
        used += cell_width(ch)
        if used > width:
            return text[:index]
    return text


def pad(text, width):
    text = clip(text, width)
    return text + " " * (width - cells(text))


def fit(line, width):
    out, used = [], 0
    for text, style in line:
        text = clip(text, width - used)
        if text:
            out.append((text, style))
            used += cells(text)
    return out


def wrap(text, width, first="", indent=""):
    """Word-wrap by terminal cells; an overlong word is split, never dropped. first and indent leave room."""
    lines, line, fresh = [], first, True
    for word in clean(text).split():
        gap = "" if fresh else " "
        if cells(line + gap + word) <= width:
            line, fresh = line + gap + word, False
            continue
        if not fresh:
            lines.append(line)
            line, fresh = indent, True
        while cells(line + word) > width:
            room = width - cells(line)
            head = clip(word, room) or word[0]
            lines.append(line + head)
            line, word = indent, word[len(head):]
        line, fresh = line + word, False
    lines.append(line)
    return lines


def duration(seconds):
    if seconds is None:
        return "--:--"
    seconds = int(max(0, seconds))
    if seconds >= 86400:
        return "%dd%02dh" % (seconds // 86400, seconds % 86400 // 3600)
    hours, rest = divmod(seconds, 3600)
    return "%d:%02d:%02d" % (hours, rest // 60, rest % 60) if hours else "%d:%02d" % divmod(rest, 60)


def clock(epoch, seconds=True):
    return time.strftime("%H:%M:%S" if seconds else "%H:%M", time.localtime(epoch))


def state_of(ticket):
    return STATES.get(ticket["state"], ("?", str(ticket["state"]).upper(), "red"))


def elapsed(ticket, now):
    """Running time = now - dispatch while not merged; final time = merged - dispatch once merged."""
    times = ticket["times"]
    if times.get("dispatch") is None:
        return None, False
    if times.get("merged") is not None:
        return times["merged"] - times["dispatch"], True
    return now - times["dispatch"], False


def timer_seg(ticket, now):
    seconds, final = elapsed(ticket, now)
    glyph = "■" if final else state_of(ticket)[0]
    if seconds is None:
        return (glyph + " --:--  ", "dim")
    flag, style = ("", "green") if seconds < TARGET_S else ("!", "yellow") if seconds < 2 * TARGET_S else ("!!", "red")
    return (glyph + " " + duration(seconds) + flag.ljust(2), style)


def review_segs(reviews, limit=5):
    shown = reviews[-limit:]
    segs = [] if len(reviews) <= limit else [("+", "dim")]
    segs += [(VERDICTS.get(r["verdict"], ("?", "yellow"))[0], VERDICTS.get(r["verdict"], ("?", "yellow"))[1])
             for r in shown]
    if reviews:
        segs.append((" %d" % len(reviews), ""))
    return segs


def visible(snap, ui):
    """Tickets in display order: folder order, then wave, then id; filtered by folder and active-only."""
    labels = [f["label"] for f in snap["folders"]]
    rank = {label: index for index, label in enumerate(labels)}
    tickets = sorted(snap["tickets"], key=lambda t: (rank.get(t["label"], len(labels)), t["label"], t["wave"], t["id"]))
    return [t for t in tickets if (ui.folder is None or t["label"] == ui.folder)
            and (not ui.active_only or t["state"] in ACTIVE)]


def folder_labels(snap):
    labels = [f["label"] for f in snap["folders"]]
    return labels + sorted({t["label"] for t in snap["tickets"]} - set(labels))


def errors_of(snap, notes):
    return list(notes) + ([] if snap is None else list(snap["errors"]))


def header(snap, now, width, notes, loading):
    errors = errors_of(snap, notes)
    tickets = [] if snap is None else snap["tickets"]
    merged = sum(t["state"] == "merged" for t in tickets)
    bar_w = 20
    filled = bar_w * merged // len(tickets) if tickets else 0
    age = "loading the first snapshot…" if loading else "no snapshot" if snap is None else \
        "data %d s old" % max(0, now - snap["generated_epoch"])
    first = [(" TICKETS · live ", "title"), (" " + clock(now) + " ", "bold"),
             (" [", "dim"), ("█" * filled, "green"), ("░" * (bar_w - filled), "dim"), ("] ", "dim"),
             ("%d/%d merged " % (merged, len(tickets)), "bold"),
             (" ✗ ERRORS %d " % len(errors) if errors else "  errors 0 ", "red" if errors else "dim"),
             ("  " + age, "dim")]
    chips = [(" ", "")]
    for name, (glyph, word, style) in STATES.items():
        chips += [("%s %s %d" % (glyph, word, sum(t["state"] == name for t in tickets)), style), ("   ", "")]
    finals = [t["times"]["merged"] - t["times"]["dispatch"] for t in tickets
              if t["times"].get("merged") is not None and t["times"].get("dispatch") is not None]
    recent = sum(1 for t in tickets if t["times"].get("merged") is not None
                 and now - 4 * 3600 < t["times"]["merged"] <= now)
    firsts = [min(t["reviews"], key=lambda r: r["round"])["verdict"] for t in tickets if t["reviews"]]
    decided = [v for v in firsts if v in VERDICTS]
    nogo = "%d%%" % round(100.0 * decided.count("NO-GO") / len(decided)) if decided else "n/a"
    stats = [(" throughput %.2f/h (4 h)" % (recent / 4.0), ""), ("  ·  ", "dim"),
             ("median dispatch→merge %s" % (duration(statistics.median(finals)) if finals else "n/a"), ""),
             ("  ·  ", "dim"), ("1st-round NO-GO %s" % nogo, ""), ("  ·  target 15 min", "dim")]
    lines = [first, chips, stats]
    if errors:
        lines.append([(" ✗ " + " | ".join(clean(e) for e in errors), "red")])
    return lines


def axis_of(tickets, now):
    starts = [t["times"]["dispatch"] for t in tickets if t["times"].get("dispatch") is not None]
    return max(min(starts), now - AXIS_MAX_S) if starts else now - 3600


def timeline(ticket, start, now, width):
    """One cell per time slice on [start, now); the last cell is the now marker."""
    times = ticket["times"]
    dispatch, pr_open, merged = times.get("dispatch"), times.get("pr_open"), times.get("merged")
    slots = width - 1
    if dispatch is None or slots < 1:
        return [(" " * slots + NOW_MARK, "dim")] if slots >= 0 else []
    end = merged if merged is not None else now
    build_end = pr_open if pr_open is not None else end
    span = max(now - start, 1.0)
    cells_out = []
    for index in range(slots):
        lo, hi = start + span * index / slots, start + span * (index + 1) / slots
        if pr_open is not None and lo < end and hi > pr_open:
            cells_out.append((REVIEW, "magenta"))
        elif lo < build_end and hi > dispatch:
            cells_out.append((BUILD, "cyan"))
        else:
            cells_out.append((" ", ""))
    if dispatch < start:
        cells_out[0] = (BEFORE, "dim")
    return cells_out + [(NOW_MARK, "yellow")]


def table(snap, ui, rows, width, now):
    tickets = visible(snap, ui)
    fixed = 52
    rest = width - fixed
    goal_w = rest // 3 if rest >= 60 else 0
    line_w = rest - goal_w - (1 if goal_w else 0) if rest >= 12 else 0
    start = axis_of(tickets, now)
    head = [(pad("  ID     STATE      TIMER        REVIEWS   PR    CI", fixed), "dim")]
    if goal_w:
        head.append((pad("GOAL", goal_w + 1), "dim"))
    if line_w:
        head.append((pad("%s %s build %s PR/review" % (clock(start, False), BUILD, REVIEW), line_w - 4) + "now",
                     "dim"))
    body, selected_row, last = [], 0, None
    for index, ticket in enumerate(tickets):
        group = (ticket["label"], ticket["wave"])
        if group != last:
            size = sum(1 for t in tickets if (t["label"], t["wave"]) == group)
            body.append([("▌ %s · wave %s · %d ticket%s" % (clean(group[0]), group[1], size, "" if size == 1 else "s"),
                          "title")])
            last = group
        chosen = index == ui.selected
        if chosen:
            selected_row = len(body)
        glyph, word, style = state_of(ticket)
        reviews = review_segs(ticket["reviews"])
        review_w = sum(cells(s[0]) for s in reviews)
        ci_glyph, ci_style = CI.get(ticket["ci"], ("?", "red"))
        line = [("›" if chosen else " ", "bold"), (" ", ""), (pad(clean(ticket["id"]), 6), "sel" if chosen else "bold"),
                (" ", ""), (pad("%s %s" % (glyph, word), 10), style), (" ", ""), timer_seg(ticket, now),
                (pad("", 13 - cells(timer_seg(ticket, now)[0])), "")]
        line += reviews + [(" " * max(1, 10 - review_w), "")]
        line += [(pad("#%d" % ticket["pr"] if ticket["pr"] is not None else "-", 6), ""), (ci_glyph, ci_style),
                 ("  ", "")]
        used = sum(cells(s[0]) for s in line)
        line.append((" " * max(0, fixed - used), ""))
        if goal_w:
            line.append((pad(clean(ticket["goal"]), goal_w) + " ", "dim"))
        if line_w:
            line += timeline(ticket, start, now, line_w)
        body.append(line)
    if not tickets:
        body.append([("  no tickets match (f folder: %s, a active only: %s)" %
                      (ui.folder or "all", "on" if ui.active_only else "off"), "dim")])
    top = min(max(0, selected_row - rows + 1), max(0, len(body) - rows))
    return [head] + body[top:top + max(0, rows)], len(body)


def detail(ticket, snap, now, width, notes):
    if ticket is None:
        lines = [[("No ticket selected.", "dim")]]
    else:
        glyph, word, style = state_of(ticket)
        final = elapsed(ticket, now)[1]
        timer = timer_seg(ticket, now)
        ci_glyph, ci_style = CI.get(ticket["ci"], ("?", "red"))
        lines = [[(clean(ticket["id"]), "bold"), (" · %s · wave %s · " % (clean(ticket["label"]), ticket["wave"]), ""),
                  ("%s %s" % (glyph, word), style), (" · ", ""),
                  ("%s %s" % ("final" if final else "running", timer[0].strip()), timer[1]),
                  (" · PR %s" % ("#%d" % ticket["pr"] if ticket["pr"] is not None else "none"), ""),
                  (" · CI ", ""), (ci_glyph + " " + clean(ticket["ci"]), ci_style)],
                 [("astra %s · times from %s" % ("yes" if ticket["astra"] else "no", clean(ticket["time_source"])),
                   "dim")]]

        def field_lines(label, value, label_w=7):
            return [[(text, "")] for text in wrap(value or "-", width, pad(label, label_w), " " * label_w)]

        lines += field_lines("Goal", ticket["goal"])
        lines += field_lines("Deps", ", ".join(ticket["deps"]) or "none")
        reviews = sorted(ticket["reviews"], key=lambda r: r["round"])
        lines.append([("Reviews: %d round%s  " % (len(reviews), "" if len(reviews) == 1 else "s"), "title")]
                     + review_segs(reviews, limit=len(reviews) or 1)[:len(reviews)])
        for review in reviews:
            mark, mark_style = VERDICTS.get(review["verdict"], ("?", "yellow"))
            killed, survived = review["mutants"]["killed"], review["mutants"]["survived"]
            total = killed + survived
            bar_w = 12
            kill_w = round(bar_w * killed / total) if total else 0
            row = [("  R%d %s %s" % (review["round"], mark, review["verdict"]), mark_style),
                   ("   %d blocking · %d notes · mutants " % (len(review["blocking"]), review["notes"]), "")]
            row += ([("█" * kill_w, "green"), ("░" * (bar_w - kill_w), "red"),
                     (" %d killed / %d survived" % (killed, survived), "")] if total else [("none", "dim")])
            lines.append(row)
            for finding in review["blocking"]:
                lines += [[(text, "red")] for text in wrap(finding, width, "     ", "        ")]
            lines += [[(text, "dim")] for text in wrap(review["path"], width, "     file ", "          ")]
        ruling = ticket["ruling"]
        lines.append([("Ruling", "title")])
        lines += field_lines("  says", ruling["summary"] or "no ruling", 9)
        lines += field_lines("  kills", ", ".join(ruling["kill_set"]) or "none", 9)
        if ruling["path"]:
            lines += field_lines("  file", ruling["path"], 9)
        lines += field_lines("Write", "  ".join(ticket["write"]))
        lines += field_lines("Out", ticket["out"])
        stamps = ["%s %s" % (name, clock(ticket["times"][name])) for name in ("dispatch", "pr_open", "merged")
                  if ticket["times"].get(name) is not None]
        lines += field_lines("Times", " · ".join(stamps) or "none recorded")
        lines.append([("Events (%d)" % len(ticket["events"]), "title")])
        for event in ticket["events"]:
            prefix = "  %s  %-9s rc %-3s " % (clock(event["t"]), clip(clean(event["event"]), 12), event["rc"])
            style = "red" if event["rc"] else ""
            lines += [[(text, style)] for text in wrap(event["detail"] or "-", width, prefix, " " * cells(prefix))]
    errors = errors_of(snap, notes)
    lines.append([("Snapshot errors (%d)" % len(errors), "red" if errors else "dim")])
    for error in errors:
        lines += [[(text, "red")] for text in wrap(error, width, "  ✗ ", "    ")]
    return [fit(line, width) for line in lines]


def footer(ui, width):
    if ui.help:
        return [[(text, "dim")] for text in wrap(HELP, width, " ", " ")][:4]
    return [[(" h help · j/k select · Enter detail · f folder: %s · a active only: %s · %s " %
             (ui.folder or "all", "on" if ui.active_only else "off", "full screen detail" if ui.full else "split"),
             "dim")]]


def render(snap, ui, now, width, height, notes=(), loading=False):
    """Pure: the whole screen as styled lines, at most height lines of at most width cells."""
    if width <= 0 or height <= 0:
        return Frame()
    if width < 40 or height < 10:
        return Frame([fit([("too small %dx%d (need 40x10) · tickets %s" % (width, height, clock(now)), "red")],
                          width)])
    lines = header(snap, now, width, notes, loading)
    tickets = visible(snap, ui) if snap is not None else []
    chosen = tickets[min(ui.selected, len(tickets) - 1)] if tickets else None
    ui = replace(ui, selected=min(ui.selected, max(0, len(tickets) - 1)))
    tail = footer(ui, width)
    room = height - len(lines) - len(tail)
    pane, max_scroll = [], 0
    if snap is None:
        lines.append([(" loading the first snapshot… the clock keeps running" if loading else " no snapshot yet",
                       "dim")])
    elif ui.full:
        info = detail(chosen, snap, now, width, notes)
        max_scroll = max(0, len(info) - room)
        top = min(ui.scroll, max_scroll)
        pane = info[top:top + room]
        if max_scroll and top < max_scroll and pane:
            pane[-1] = [("… %d more lines (↓ to scroll)" % (len(info) - top - room + 1), "yellow")]
        lines += pane
    else:
        _, total = table(snap, ui, 0, width, now)
        body_room = room - 1   # below the column heading
        body_rows = min(total, max(4, body_room - max(8, room // 2) - 1))
        detail_room = body_room - body_rows - 1   # below the separator
        if detail_room < 6:
            body_rows, detail_room = body_room, 0
        rows, _ = table(snap, ui, body_rows, width, now)
        lines += rows
        if detail_room:
            info = detail(chosen, snap, now, width, notes)
            lines.append([("─" * width, "dim")])
            pane = info[:detail_room]
            if len(info) > detail_room:
                pane[-1] = [("… %d more lines (Enter: full screen)" % (len(info) - detail_room + 1), "yellow")]
            lines += pane
    lines = lines[:max(0, height - len(tail))] + tail
    return Frame([fit(line, width) for line in lines[-height:]], max_scroll)


def on_key(ui, key, snap, max_scroll):
    count = len(visible(snap, ui)) if snap is not None else 0
    down, up = key in (ord("j"), curses.KEY_DOWN), key in (ord("k"), curses.KEY_UP)
    if ui.full and (down or up):
        return replace(ui, scroll=min(max_scroll, ui.scroll + 1) if down else max(0, ui.scroll - 1))
    if down or up:
        target = ui.selected + (1 if down else -1)
        return replace(ui, selected=min(max(0, target), max(0, count - 1)), scroll=0)
    if key in (10, 13, 9, curses.KEY_ENTER):
        return replace(ui, full=not ui.full, scroll=0)
    if key == ord("f") and snap is not None:
        cycle = [None] + folder_labels(snap)
        position = cycle.index(ui.folder) if ui.folder in cycle else 0
        return replace(ui, folder=cycle[(position + 1) % len(cycle)], selected=0, scroll=0)
    if key == ord("a"):
        return replace(ui, active_only=not ui.active_only, selected=0, scroll=0)
    if key == ord("h"):
        return replace(ui, help=not ui.help)
    return ui


class Loader:
    """Holds the latest snapshot; refresh() runs in a background thread and never holds the lock while fetching."""

    def __init__(self, fetch):
        self._fetch = fetch
        self._lock = threading.Lock()
        self._snap, self._problem, self._loaded = None, None, False

    def refresh(self):
        try:
            snap, problem = self._fetch(), None
        except Exception as error:   # any failure is shown in the errors badge; the last good snapshot stays
            snap, problem = None, "snapshot failed: %s: %s" % (type(error).__name__, error)
        with self._lock:
            if snap is not None:
                self._snap = snap
            self._problem, self._loaded = problem, True

    def state(self):
        with self._lock:
            return self._snap, self._problem, self._loaded

    def start(self, period=REFRESH_S):
        def loop():
            while True:
                self.refresh()
                time.sleep(period)
        threading.Thread(target=loop, daemon=True).start()


def default_folders(lean):
    return [str(path) for path in sorted(Path(lean).iterdir()) if (path / "tickets").is_dir()]


STYLES = {"cyan": 1, "magenta": 2, "green": 3, "blue": 4, "yellow": 5, "red": 6}


def draw(screen, frame):
    height, width = screen.getmaxyx()
    attrs = {name: curses.color_pair(pair) for name, pair in STYLES.items()} if curses.has_colors() else {}
    attrs.update({"": curses.A_NORMAL, "dim": curses.A_DIM, "bold": curses.A_BOLD,
                  "sel": curses.A_REVERSE | curses.A_BOLD,
                  "title": attrs.get("cyan", curses.A_NORMAL) | curses.A_BOLD})
    attrs["red"] = attrs.get("red", curses.A_NORMAL) | curses.A_BOLD
    screen.erase()
    for y, line in enumerate(frame.lines[:height]):
        x = 0
        for text, style in line:
            try:
                screen.addstr(y, x, text, attrs.get(style, curses.A_NORMAL))
            except curses.error:   # curses reports an error after writing the bottom-right cell; the text is drawn
                pass
            x += cells(text)
    screen.refresh()


def run(screen, loader):
    try:
        curses.curs_set(0)
    except curses.error:   # some terminals cannot hide the cursor; the view works the same
        pass
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        for name, pair in STYLES.items():
            curses.init_pair(pair, getattr(curses, "COLOR_" + name.upper()), -1)
    screen.keypad(True)
    ui, max_scroll = UI(), 0
    while True:
        snap, problem, loaded = loader.state()
        height, width = screen.getmaxyx()
        frame = render(snap, ui, time.time(), width, height, (problem,) if problem else (), loading=not loaded)
        max_scroll = frame.max_scroll
        draw(screen, frame)
        screen.timeout(max(50, int(1000 - (time.time() % 1) * 1000)))
        ui = on_key(ui, screen.getch(), snap, max_scroll)


def main():
    parser = argparse.ArgumentParser(description="Live tickets tab")
    parser.add_argument("folders", nargs="*", help="ticket folders (default: every %s/*/ with tickets/)" % LEAN)
    args = parser.parse_args()
    import dashboard_tickets_data   # step 36's data module; imported here so tests render fixture snapshots
    loader = Loader(lambda: dashboard_tickets_data.snapshot(args.folders or default_folders(LEAN)))
    loader.start()
    locale.setlocale(locale.LC_ALL, "")
    curses.wrapper(run, loader)


if __name__ == "__main__":
    main()
