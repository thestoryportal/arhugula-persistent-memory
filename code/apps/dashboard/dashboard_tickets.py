"""Live tickets tab: /usr/bin/python3 code/apps/dashboard/dashboard_tickets.py [FOLDER ...].

Every ticket of the lean ticket folders (default: each folder up to 3 levels under G-build/LEAN
with tickets/) with a live timer, its phase in words, review rounds, every blocking finding and,
on its own screen (t), a labeled timeline. Layout follows the terminal width: a table at 100+
columns, a compact table at 80-99, cards below 80 (a phone); taps and swipes work where the
terminal sends mouse events.
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
TABLE_W, CARD_W = 100, 80   # >= TABLE_W full table; >= CARD_W compact table; below that, cards
MIN_W, MIN_H = 40, 16
ROOMY_H = 20                # from this height a table ticket may take two rows and the legend shows
DETAIL_H = 22               # split rows of idle tickets give way when the detail pane would get fewer lines
# Each state carries a glyph and a word as well as a colour.
STATES = {"running": ("▶", "RUNNING", "cyan"), "pr": ("◆", "PR", "magenta"), "merged": ("■", "MERGED", "green"),
          "ready": ("○", "READY", "blue"), "waiting": ("·", "WAITING", "dim")}
VERDICTS = {"GO": ("✓", "green"), "NO-GO": ("✗", "red")}
CI = {"pass": ("✓", "green"), "fail": ("✗", "red"), "pending": ("…", "yellow"), "none": ("·", "dim")}
CI_WORDS = {"pass": "passed", "fail": "failed", "pending": "pending", "none": "not run"}
PHASES = {"ready": "ready", "running": "building", "merged": "merged"}
BUILD, REVIEW, NOW_MARK, BEFORE = "▒", "█", "│", "‹"
LEGEND = ("▶ building ◆ PR ■ merged ○ ready · waiting | review ✓ GO ✗ NO-GO ? none | CI ✓ pass ✗ fail … pending | "
          "timer ! >15 min !! >30 min")
# Every key the tab handles: (label, long words, short words). The key row and the help line both render from it.
KEYS = (("↑↓ j k", "select", "select"), ("Enter/Tab", "open detail", "open"), ("Esc", "back", "back"),
        ("t", "timeline", "timeline"), ("f", "folder", "folder"), ("a", "active only", "active"),
        ("h", "help", "help"), ("Ctrl-a d", "leave teamdash", "leave"))
HELP = ("state ▶ running ◆ PR ■ merged (timer final) ○ ready · waiting | reviews ✓ GO ✗ NO-GO ? no verdict | "
        "CI ✓ pass ✗ fail … pending · none | timer ! over 15 min, !! over 30 min | timeline ▒ build █ review/land "
        "│ now ‹ began earlier | swipe = ↑↓ · tap select, tap again open")
TL_LEGEND = "▒ build = dispatch → PR open   █ review/land = PR open → merged   │ now   ‹ began before the axis"
TL_LEGEND_NARROW = ("▒ build = dispatch → PR open", "█ review/land = PR → merged  │ now")
ESC = 27
TAP = curses.BUTTON1_PRESSED | curses.BUTTON1_CLICKED
WHEEL_UP = curses.BUTTON4_PRESSED
WHEEL_DOWN = getattr(curses, "BUTTON5_PRESSED", 0x200000)   # ncurses mouse v1 has no name for the wheel-down bit

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
    timeline: bool = False


Row = Tuple[Line, Optional[int]]   # a screen line and the visible-ticket index it shows (None: no ticket)


@dataclass(frozen=True)
class Frame:
    lines: List[Line] = field(default_factory=list)
    max_scroll: int = 0
    hits: Tuple[Optional[int], ...] = ()   # per line: the ticket a tap there selects


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


def goal_rows(text, width, rows):
    """At most rows lines of whole words; a longer goal ends with "…" after its last whole word that fits."""
    lines, line = [], ""
    for word in clean(text).split():
        joined = line + " " + word if line else word
        if cells(joined) <= width:
            line = joined
        elif line and len(lines) + 1 < rows and cells(word) <= width:
            lines.append(line)
            line = word
        else:
            words = line.split()
            while words and cells(" ".join(words) + "…") > width:
                words.pop()
            return lines + [" ".join(words) + "…"]
    return lines + [line]


def words(seconds):
    seconds = int(max(0, seconds))
    if seconds < 60:
        return "%ds" % seconds
    if seconds < 3600:
        return "%dm" % (seconds // 60)
    if seconds < 86400:
        return "%dh%02dm" % (seconds // 3600, seconds % 3600 // 60)
    return "%dd%02dh" % (seconds // 86400, seconds % 86400 // 3600)


def split_text(ticket, now):
    """Build = dispatch to PR open; review = PR open to merge (or to now). Empty when not known."""
    times = ticket["times"]
    dispatch, pr_open, merged = times.get("dispatch"), times.get("pr_open"), times.get("merged")
    if dispatch is None or (pr_open is None and merged is not None):
        return ""
    build = "build " + words((pr_open if pr_open is not None else now) - dispatch)
    if pr_open is None:
        return build
    return build + " · review " + words((merged if merged is not None else now) - pr_open)


def phase(ticket, by_id):
    state = ticket["state"]
    if state == "waiting":
        pending = [dep for dep in ticket["deps"] if by_id.get(dep, {}).get("state") != "merged"]
        return "waiting on " + clean(pending[0]) if pending else "waiting"
    if state == "pr":
        if ticket["reviews"]:
            return "in review (round %d)" % max(r["round"] for r in ticket["reviews"])
        return "PR open, CI " + CI_WORDS.get(ticket["ci"], clean(ticket["ci"]))
    return PHASES.get(state, clean(state))


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
    if width < CARD_W:
        counts = [(glyph, sum(t["state"] == name for t in tickets), word if name == "pr" else word.lower(), style)
                  for name, (glyph, word, style) in STATES.items()]
        worded = [("%s%d %s " % (glyph, count, word), style) for glyph, count, word, style in counts]
        bare = [("%s%d " % (glyph, count), style) for glyph, count, _, style in counts]
        return [[(" TICKETS ", "title"), (clock(now) + " ", "bold"), (" %d/%d merged " % (merged, len(tickets)), "bold"),
                 (" ✗ %d errors" % len(errors) if errors else " errors 0", "red" if errors else "dim")],
                [(" ", "")] + (worded if sum(cells(s[0]) for s in worded) < width else bare)]
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


def key_items(short):
    return [label + " " + (brief if short else full) for label, full, brief in KEYS]


def key_rows(width):
    """The key reference: one row of long words when it fits, else short words wrapped only at " · "."""
    whole = "keys " + " · ".join(key_items(False))
    if cells(whole) <= width:
        return [[(whole, "dim")]]
    lines, line = [], "keys " + key_items(True)[0]
    for item in key_items(True)[1:]:
        if cells(line + " · " + item) <= width:
            line += " · " + item
        else:
            lines.append(line)
            line = "     " + item
    return [[(text, "dim")] for text in lines + [line]]


def help_text():
    return HELP + " | keys " + " · ".join(key_items(True))


def legend(width):
    return [[(text, "dim")] for text in wrap(LEGEND, width, " ", " ")][:2]


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


def group_heading(group, size):
    return [("▌ %s · wave %s · %d ticket%s" % (clean(group[0]), group[1], size, "" if size == 1 else "s"), "title")]


def grouped(tickets):
    """(index, ticket, heading or None) in display order; a heading opens each folder/wave group."""
    out, last = [], None
    for index, ticket in enumerate(tickets):
        group = (ticket["label"], ticket["wave"])
        size = sum(1 for t in tickets if (t["label"], t["wave"]) == group)
        out.append((index, ticket, group_heading(group, size) if group != last else None))
        last = group
    return out


def no_match(ui):
    return [("  no tickets match (f folder: %s, a active only: %s)" %
             (ui.folder or "all", "on" if ui.active_only else "off"), "dim")]


def table(snap, ui, width, now, roomy, every_split=True):
    """Column heading and every ticket row. GOAL takes the columns left over and wraps at whole words.
    Without every_split, a build/review split that would need a row of its own shows only for the selected ticket."""
    tickets = visible(snap, ui)
    by_id = {t["id"]: t for t in snap["tickets"]}
    phases = [phase(t, by_id) for t in tickets]
    full = width >= TABLE_W
    id_w = max([4] + [cells(clean(t["id"])) for t in tickets]) + 1
    phase_w = max([len("STATE · PHASE") - 2] + [cells(p) for p in phases]) + 3
    rev_w = 8 if full else 4
    split_w = 12 + rev_w + 5 + 3
    left = 2 + id_w + phase_w + split_w
    goal_w = width - left if width - left >= 16 else 0
    head = [(pad("  " + pad("ID", id_w) + pad("STATE · PHASE", phase_w) + pad("TIME", 12) +
                 pad("REVIEWS" if full else "REV", rev_w) + pad("PR", 5) + "CI", left), "dim")]
    if goal_w:
        head.append(("GOAL", "dim"))
    rows = [(head, None)]
    for index, ticket, heading in grouped(tickets):
        if heading:
            rows.append((heading, None))
        chosen = index == ui.selected
        glyph, _, style = state_of(ticket)
        reviews = review_segs(ticket["reviews"], 3) if full else review_segs(ticket["reviews"], 1)[-2:]
        ci_glyph, ci_style = CI.get(ticket["ci"], ("?", "red"))
        timer = timer_seg(ticket, now)
        line = [("›" if chosen else " ", "bold"), (" ", ""), (pad(clean(ticket["id"]), id_w), "sel" if chosen else "bold"),
                (pad("%s %s" % (glyph, phases[index]), phase_w), style), timer,
                (" " * max(0, 12 - cells(timer[0])), "")]
        line += reviews + [(" " * (rev_w - sum(cells(s[0]) for s in reviews)), "")]
        line += [(pad("#%d" % ticket["pr"] if ticket["pr"] is not None else "-", 5), ""), (ci_glyph + "  ", ci_style)]
        goal = goal_rows(ticket["goal"], goal_w, 2 if roomy else 1) if goal_w else []
        rows.append((line + [(goal[0], "")] if goal else line, index))
        own_row = len(goal) < 2 and not (every_split or chosen)
        split = split_text(ticket, now) if full and roomy and not own_row else ""
        if split or len(goal) > 1:
            rows.append(([(" " * (2 + id_w + phase_w), ""), (pad(split, split_w), "dim")]
                         + [(text, "") for text in goal[1:]], index))
    if not tickets:
        rows.append((no_match(ui), None))
    return rows


def cards(snap, ui, width, now):
    """Phone layout: one card per ticket: state, ID and timer; phase, reviews, PR and CI; the goal; a separator."""
    tickets = visible(snap, ui)
    by_id = {t["id"]: t for t in snap["tickets"]}
    rows = []
    for index, ticket, heading in grouped(tickets):
        if heading:
            rows.append((heading, None))
        chosen = index == ui.selected
        glyph, word, style = state_of(ticket)
        timer_text, timer_style = timer_seg(ticket, now)
        timer_text = timer_text.rstrip()
        left = [("›" if chosen else " ", "bold"), (" ", ""), ("%s %s" % (glyph, word), style), ("  ", ""),
                (clean(ticket["id"]), "sel" if chosen else "bold")]
        gap = width - sum(cells(s[0]) for s in left) - cells(timer_text)
        rows.append((left + [(" " * max(1, gap), ""), (timer_text, timer_style)], index))
        ci_glyph, ci_style = CI.get(ticket["ci"], ("?", "red"))
        reviews = review_segs(ticket["reviews"], 3) or [("no review", "dim")]
        rows.append(([("  " + phase(ticket, by_id), style), (" · ", "dim")] + reviews +
                     [(" · ", "dim"), ("#%d" % ticket["pr"] if ticket["pr"] is not None else "no PR", ""),
                      (" CI ", "dim"), (ci_glyph, ci_style)], index))
        rows += [([("  " + text, "")], index) for text in goal_rows(ticket["goal"], width - 2, 3)]
        rows.append(([("  " + "┈" * max(0, width - 4), "dim")], index))
    if not tickets:
        rows.append((no_match(ui), None))
    return rows


def timeline_text(ticket, now, narrow):
    seconds, _ = elapsed(ticket, now)
    if seconds is None:
        return "-" if narrow else "not dispatched"
    split = split_text(ticket, now)
    if narrow:
        return words(seconds)
    return (split + " · " if split else "") + "total " + words(seconds)


def timeline_screen(snap, ui, width, now):
    """(fixed lines, ticket rows): title, legend, HH:MM axis and ruler, then one bar per ticket with its durations."""
    tickets = visible(snap, ui)
    narrow = width < CARD_W
    start = axis_of(tickets, now)
    span = max(now - start, 1.0)
    id_w = max([4] + [cells(clean(t["id"])) for t in tickets]) + 1
    left_w = 2 + id_w + (0 if narrow else 2)
    texts = [timeline_text(t, now, narrow) for t in tickets]
    dur_w = min(40, max([1] + [cells(text) for text in texts]))
    bar_w = max(3, width - left_w - dur_w - 1)
    slots = bar_w - 1

    def at(epoch):
        return min(slots, max(0, int((epoch - start) / span * slots)))

    capped = any(t["times"].get("dispatch") is not None and t["times"]["dispatch"] < start for t in tickets)
    title = "TIMELINE · %s → now %s" % (clock(start, False), clock(now, False))
    if not narrow:
        title = "TIMELINE · one row per ticket, dispatch → merge · %s%s" % (
            title[len("TIMELINE · "):], " · capped at 8 h" if capped else "")
    labels, ruler = [" "] * bar_w, ["─"] * bar_w
    marks = [(0, clock(start, False))]
    if not narrow:
        step = 1800 if span <= 4 * 3600 else 3600
        offset = time.localtime(start).tm_gmtoff
        tick = ((start + offset) // step + 1) * step - offset
        while tick < now:
            marks.append((at(tick), clock(tick, False)))
            tick += step
    end_label = clock(now, False)
    marks.append((slots - cells(end_label) + 1, end_label))
    taken = -1
    for position, text in marks:
        last = position == marks[-1][0] and text == end_label
        if position <= taken or (not last and position + cells(text) >= marks[-1][0]):
            continue
        labels[position:position + len(text)] = list(text)
        ruler[min(slots, position + (len(text) - 1 if last else 0))] = "┬"
        taken = position + len(text)
    fixed = [[(" " + title, "title")]]
    fixed += [[(" " + text, "dim")] for text in (TL_LEGEND_NARROW if narrow else (TL_LEGEND,))]
    fixed += [[(" " * left_w, ""), ("".join(labels), "dim")], [(" " * left_w, ""), ("".join(ruler), "dim")]]
    rows = []
    for index, ticket in enumerate(tickets):
        chosen = index == ui.selected
        glyph, _, style = state_of(ticket)
        line = [("›" if chosen else " ", "bold"), (" ", ""), (pad(clean(ticket["id"]), id_w), "sel" if chosen else "bold")]
        if not narrow:
            line.append((glyph + " ", style))
        line += timeline(ticket, start, now, bar_w)
        line += [(" ", ""), (texts[index], "")]
        rows.append((line, index))
    if not tickets:
        rows.append((no_match(ui), None))
    return fixed, rows


def window(rows, selected, count):
    """count rows that keep every row of the selected ticket in view where they fit."""
    if count <= 0:
        return []
    marks = [i for i, (_, hit) in enumerate(rows) if hit == selected]
    top = min(max(0, marks[-1] - count + 1), max(0, len(rows) - count)) if marks else 0
    top = min(top, marks[0]) if marks else top
    return rows[top:top + count]


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
    if width < CARD_W:
        text = (" Enter/Esc/tap: back · swipe scrolls" if ui.full else " h close help" if ui.help else
                " h help · t timeline · tap/Enter open · f %s" % (ui.folder or "all"))
        return [[(text, "dim")]]
    if ui.help:
        return [[(text, "dim")] for text in wrap(help_text(), width, " ", " ")][:4]
    mode = "full screen detail" if ui.full else "timeline" if ui.timeline else "split"
    return [[(" h help · j/k select · Enter detail · t timeline · f folder: %s · a active only: %s · %s " %
             (ui.folder or "all", "on" if ui.active_only else "off", mode), "dim")]]


def render(snap, ui, now, width, height, notes=(), loading=False):
    """Pure: the whole screen as styled lines, at most height lines of at most width cells."""
    if width <= 0 or height <= 0:
        return Frame()
    if width < MIN_W or height < MIN_H:
        return Frame([fit([("too small %dx%d (need %dx%d) · tickets %s" % (width, height, MIN_W, MIN_H, clock(now)),
                            "red")], width)])
    narrow = width < CARD_W
    rows = [(line, None) for line in key_rows(width) + header(snap, now, width, notes, loading)]
    tickets = visible(snap, ui) if snap is not None else []
    chosen = tickets[min(ui.selected, len(tickets) - 1)] if tickets else None
    ui = replace(ui, selected=min(ui.selected, max(0, len(tickets) - 1)))
    tail = [(line, None) for line in footer(ui, width)]
    room = height - len(rows) - len(tail)
    max_scroll = 0
    if snap is None:
        rows.append(([(" loading the first snapshot… the clock keeps running" if loading else " no snapshot yet",
                       "dim")], None))
    elif ui.help and narrow:
        rows += [([(text, "dim")], None) for text in wrap(LEGEND + " | " + help_text(), width, " ", " ")][:room]
    elif ui.full:
        info = detail(chosen, snap, now, width, notes)
        max_scroll = max(0, len(info) - room)
        top = min(ui.scroll, max_scroll)
        pane = info[top:top + room]
        if max_scroll and top < max_scroll and pane:
            pane[-1] = [("… %d more lines (↓ to scroll)" % (len(info) - top - room + 1), "yellow")]
        rows += [(line, None) for line in pane]
    elif ui.timeline:
        fixed, body = timeline_screen(snap, ui, width, now)
        rows += [(line, None) for line in fixed] + window(body, ui.selected, room - len(fixed))
    elif narrow:
        rows += window(cards(snap, ui, width, now), ui.selected, room)
    else:
        roomy = height >= ROOMY_H
        keys = [(line, None) for line in legend(width)] if roomy else []
        rows += keys
        body_room = room - len(keys) - 1   # below the column heading
        body = table(snap, ui, width, now, roomy)
        if len(body) - 1 > body_room - DETAIL_H - 1:
            body = table(snap, ui, width, now, roomy, every_split=False)
        body_rows = min(len(body) - 1, max(4, body_room - 12))   # the detail pane keeps at least 11 lines
        detail_room = body_room - body_rows - 1   # below the separator
        if detail_room < 6:
            body_rows, detail_room = body_room, 0
        rows += body[:1] + window(body[1:], ui.selected, body_rows)
        if detail_room:
            info = detail(chosen, snap, now, width, notes)
            rows.append(([("─" * width, "dim")], None))
            pane = info[:detail_room]
            if len(info) > detail_room:
                pane[-1] = [("… %d more lines (Enter: full screen)" % (len(info) - detail_room + 1), "yellow")]
            rows += [(line, None) for line in pane]
    rows = (rows[:max(0, height - len(tail))] + tail)[-height:]
    return Frame([fit(line, width) for line, _ in rows], max_scroll, tuple(hit for _, hit in rows))


def on_key(ui, key, snap, max_scroll):
    count = len(visible(snap, ui)) if snap is not None else 0
    down, up = key in (ord("j"), curses.KEY_DOWN), key in (ord("k"), curses.KEY_UP)
    if ui.full and (down or up):
        return replace(ui, scroll=min(max_scroll, ui.scroll + 1) if down else max(0, ui.scroll - 1))
    if down or up:
        target = ui.selected + (1 if down else -1)
        return replace(ui, selected=min(max(0, target), max(0, count - 1)), scroll=0)
    if key in (10, 13, 9, curses.KEY_ENTER):
        return replace(ui, full=not ui.full, timeline=False, scroll=0)
    if key == ESC:
        return replace(ui, full=False, timeline=False, help=False, scroll=0)
    if key == ord("t"):
        return replace(ui, timeline=not ui.timeline, full=False, scroll=0)
    if key == ord("f") and snap is not None:
        cycle = [None] + folder_labels(snap)
        position = cycle.index(ui.folder) if ui.folder in cycle else 0
        return replace(ui, folder=cycle[(position + 1) % len(cycle)], selected=0, scroll=0)
    if key == ord("a"):
        return replace(ui, active_only=not ui.active_only, selected=0, scroll=0)
    if key == ord("h"):
        return replace(ui, help=not ui.help)
    return ui


def on_mouse(ui, frame, y, bstate, snap):
    """A tap selects the ticket under it, a second tap opens its detail, a tap in the detail goes back; the wheel
    (a swipe on a phone) moves the selection, or scrolls the detail."""
    if bstate & WHEEL_UP:
        return on_key(ui, ord("k"), snap, frame.max_scroll)
    if bstate & WHEEL_DOWN:
        return on_key(ui, ord("j"), snap, frame.max_scroll)
    if not bstate & TAP:
        return ui
    if ui.full:
        return replace(ui, full=False, scroll=0)
    hit = frame.hits[y] if 0 <= y < len(frame.hits) else None
    if hit is None:
        return ui
    if hit == ui.selected:
        return replace(ui, full=True, timeline=False, scroll=0)
    return replace(ui, selected=hit)


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


def default_folders(lean, depth=3):
    """Every folder up to depth levels under lean that holds a tickets/ folder (so recut/followup counts)."""
    found, level = [], [Path(lean)]
    for _ in range(depth):
        level = [child for folder in level for child in sorted(folder.iterdir())
                 if child.is_dir() and child.name != "tickets"]
        found += [folder for folder in level if (folder / "tickets").is_dir()]
    return [str(folder) for folder in sorted(found)]


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
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.mouseinterval(0)
    curses.set_escdelay(25)
    ui = UI()
    while True:
        snap, problem, loaded = loader.state()
        height, width = screen.getmaxyx()
        frame = render(snap, ui, time.time(), width, height, (problem,) if problem else (), loading=not loaded)
        draw(screen, frame)
        screen.timeout(max(50, int(1000 - (time.time() % 1) * 1000)))
        key = screen.getch()
        if key != curses.KEY_MOUSE:
            ui = on_key(ui, key, snap, frame.max_scroll)
            continue
        try:
            _, _, y, _, bstate = curses.getmouse()
        except curses.error:   # a mouse report ncurses could not decode carries no position; it changes nothing
            continue
        ui = on_mouse(ui, frame, y, bstate, snap)


def main():
    parser = argparse.ArgumentParser(description="Live tickets tab")
    parser.add_argument("folders", nargs="*",
                        help="ticket folders (default: every folder up to 3 levels under %s with tickets/)" % LEAN)
    args = parser.parse_args()
    import dashboard_tickets_data   # step 36's data module; imported here so tests render fixture snapshots
    loader = Loader(lambda: dashboard_tickets_data.snapshot(args.folders or default_folders(LEAN)))
    loader.start()
    locale.setlocale(locale.LC_ALL, "")
    curses.wrapper(run, loader)


if __name__ == "__main__":
    main()
