"""View-only MathLab teamdash tab. Usage: /usr/bin/python3 dashboard_mathlab.py [--once COLS ROWS]."""
import argparse, hashlib, json, os, re, sys, time
from datetime import datetime
from pathlib import Path
import dashboard_live
import mathlab_events

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
FG, BG = "\033[38;5;{}m".format, "\033[48;5;{}m".format
ANSI = re.compile(r"\033\[[0-9;]*[A-Za-z]")
STEPS = {
    1: "Harvest: record internal model inputs for every prompt (one GPU pass).",
    2: "Reproduce: repeat the saved write calculation on CPU; check it matches.",
    3: "Calibrate: check estimates against past results; failure stops cheaply.",
    4: "Candidate questions: explore ideas later, after a new written plan.",
}
BUILD_FILES = (
    ("harvest launcher", "tools/run_mathlab_harvest.sh"),
    ("harvest driver", "tools/mathlab_harvest.py"),
    ("step-2 notebook", "mathlab/m2_solve_repro.py"),
    ("step-3 notebook", "mathlab/m3_calibration.py"),
)
GATE_PLAN = mathlab_events.GATE_PLAN


def clean(value):
    text = ANSI.sub("", str(value))
    return " ".join("".join(c if c.isprintable() else " " for c in text).split())


def fit(value, width):
    text = clean(value)
    return text if len(text) <= width else text[:max(width - 1, 0)] + "…"


def section(title, color, cols):
    title = fit(title, max(cols - 2, 1))
    return f"{BOLD}{FG(231)}{BG(color)} {title} {RESET}{FG(color)}{'━' * max(cols - len(title) - 2, 0)}{RESET}"


def dur(seconds):
    s = int(max(seconds, 0))
    return f"{s // 3600}h{s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def epoch(stamp):
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()


def bar(value, total, width=16, floor=None):
    filled = round(min(value / total, 1) * width) if total > 0 else 0
    marker = min(round(floor / total * width), width - 1) if floor is not None and total > 0 else -1
    color = 196 if floor is not None and value < floor else 39
    return (FG(color) + "".join("┃" if i == marker else "█" if i < filled else "░" for i in range(width)) + RESET)


def prereg_header(root):
    path = Path(root) / "docs/MATHLAB_PREREG.md"
    data = path.read_bytes()
    header = data.decode("utf-8").split("\n## ", 1)[0]
    status = re.search(r"(?m)^\*\*Status:\s*(.*?)\*\*", header)
    if not status:
        raise ValueError("pre-registration header has no Status line")
    return clean(status.group(1)), hashlib.sha256(data).hexdigest()[:12]


def load(root):
    paths = list((Path(root) / "results/mathlab_staging/runs").glob("*/events.jsonl"))
    if not paths:
        return mathlab_events.fold([]), [], None, 0
    path = max(paths, key=lambda p: (p.stat().st_mtime_ns, str(p)))
    selected, selected_errors, other_active = None, [], 0
    for candidate in paths:
        events, errors = mathlab_events.read_events(candidate)
        state = mathlab_events.fold(events)
        if candidate == path:
            selected, selected_errors = state, errors
        elif state["status"] in ("running", "waiting for GPU", "waiting for admission"):
            other_active += 1
    return selected, selected_errors, path, other_active


def value_text(value):
    return clean(json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":")))


def check_line(gate, outcome, cols):
    measured = value_text(gate["observed"])
    if isinstance(gate["observed"], (dict, list)) and len(measured) > 24:
        measured = f"{'object' if isinstance(gate['observed'], dict) else 'list'}:{len(gate['observed'])}"
    scope = " (scope only)" if gate["gate_id"] == "2b" and outcome == "FAIL" else ""
    label = fit(f"{outcome} {gate['gate_id']}", max(cols // 2, 1))
    rule = f" · bar {clean(gate['comparison'])} "
    threshold = fit(value_text(gate["bar"]), max(cols - len(label) - len(rule) - len(scope) - 1, 1))
    tail = rule + threshold
    room = cols - len(label) - len(tail) - len(scope) - 1
    if room > len(" · measured "):
        tail += " · measured " + fit(measured, room - len(" · measured "))
    tail += scope
    color = 40 if outcome == "PASS" else 214 if outcome == "INVALID" else 196
    return f" {FG(color)}{label}{RESET}{tail}"


def check_lines(state, cols, height, page):
    if height <= 0:
        return []
    ordered = sorted(state["gates"], key=lambda g: (state["gate_outcomes"][g["gate_id"]] == "PASS",))
    failures = [g for g in ordered if state["gate_outcomes"][g["gate_id"]] != "PASS"]
    pinned = failures[:min(2, max((height - 3) // 2, 0))]
    pinned_ids = {g["gate_id"] for g in pinned}
    def lines(gate):
        return [check_line(gate, state["gate_outcomes"][gate["gate_id"]], cols),
                "  " + fit(gate["plain_words"], max(cols - 2, 1))]
    entries = [lines(g) for g in ordered if g["gate_id"] not in pinned_ids]
    for key, words, required in GATE_PLAN:
        group = state["gate_groups"][key]
        if not group["complete"] and group["outcome"] is None:
            entries.append([f" {DIM}· {words}{' incomplete' if group['gate_ids'] else ''} · need {required}{RESET}"])
    slots = max(height - 1 - 2 * len(pinned), 1)
    pages, current = [], []
    for entry in entries:
        if current and len(current) + len(entry) > slots:
            pages.append(current); current = []
        current += entry[:slots]
    if current or not pages:
        pages.append(current)
    page %= len(pages)
    invalid = sum(state["gate_outcomes"][g["gate_id"]] == "INVALID" for g in failures)
    header = section(f"CHECKS · {len(ordered)} recorded · {len(failures) - invalid} failed / {invalid} invalid · page {page + 1}/{len(pages)}", 25, cols)
    return ([header] + [line for gate in pinned for line in lines(gate)] + pages[page])[:height]


def event_line(event):
    kind = event["type"]
    labels = {"run_started": "Run started", "admission": "Admission", "stage_started": "Stage started",
              "progress": "Progress", "gate_result": "Check", "stage_finished": "Stage finished",
              "resource_sample": "Machine", "finding_staged": "Finding staged", "candidate_added": "Candidate",
              "halted": "Halted", "run_finished": "Run finished"}
    detail = next((event[k] for k in ("plain_words", "summary", "reason", "question", "title") if k in event), "")
    if kind == "progress":
        detail = f"{event['done']}/{event['total']} {event['unit']}"
    elif kind == "admission":
        detail = "allowed" if event["allowed"] else "; ".join(event["reasons"])
    elif kind == "resource_sample":
        detail = f"free {event['avail_gib']:g} GiB; lab {event['rss_gib']:g} GiB; CPU {event['cpu_pct']:g}%"
    result = event.get("outcome", "")
    if kind == "gate_result":
        result = mathlab_events.gate_outcome(event)
    return f" {event['ts'][11:19]} {labels[kind]}{(' ' + result) if result else ''}: {clean(detail)}"


def render(cols, rows, check_page=None):
    now = time.time()
    state, errors, path, other_active = load(ROOT)
    try:
        gpu = dashboard_live.gpu_state()
        if gpu.get("unavailable"):
            gpu_words = f"GPU state unavailable: {clean(gpu['unavailable'])}"
            gpu = None
        elif gpu["running"]:
            job, phase, elapsed = gpu["running"]
            gpu_words = f"GPU in use by {dashboard_live.SHORT.get(job, job)} ({job}) · {phase} · {elapsed}"
        else:
            gpu_words = "GPU free (no running job reported); admission decides"
    except (OSError, ValueError) as error:
        gpu = None
        gpu_words = f"GPU state unavailable: {clean(error)}"
    status = state["status"]
    color = 28 if status == "running" else 124 if status in ("halted", "stopped: check failed") else 25
    out = [f"{BOLD}{FG(231)}{BG(color)}{fit(' ■ MATH LAB · test math estimates using saved model inputs', cols).ljust(cols)}{RESET}",
           f" {BOLD}MATH-PROXY · math estimate, not evidence{RESET}",
           f" Run {state['run_id'] or (path.parent.name if path else 'none yet')} · {status}"
           + (f" · step {state['step']}" if state["step"] else "")
           + (" · admission only" if state["purpose"] == "admission" else ""),
           f" View: newest events file by mtime · other active runs (events): {other_active}"]
    if state["outcome"] == "INVALID" or state["calibration_outcome"] == "INVALID":
        out.append(f" {FG(214)}INVALID: no verdict; operator review needed.{RESET}")
    if errors:
        out.append(f"{BOLD}{FG(196)} EVENT ERROR ({len(errors)}): state below uses valid lines only.{RESET}")
        for error in errors[:2]:
            # Put the line number before the long absolute path so narrow panes retain it.
            out.append(f" {FG(196)}{error.removeprefix(str(path) + ': ')} · {path}{RESET}")
    if state["started_ts"]:
        end = epoch(state["finished_ts"] or state["halt"]["ts"]) if state["finished_ts"] or state["halt"] else now
        start, deadline = epoch(state["started_ts"]), epoch(state["deadline_ts"])
        out.append(f" Elapsed {dur(end - start)} / hard deadline {dur(deadline - start)} · ends {state['deadline_ts']}"
                   + (f" · {dur(deadline - now)} left" if end == now and deadline >= now else " · deadline exceeded" if end == now else ""))
    else:
        out.append(" Elapsed / hard deadline: not started; no launch is implied by this display.")
        status_line = None
        try:
            status_line, sha = prereg_header(ROOT)
            out.append(f" Pre-registration: {status_line}")
            out.append(f" Current file SHA256: {sha} · docs/MATHLAB_PREREG.md")
        except (OSError, UnicodeError, ValueError) as error:
            out.append(f" {FG(196)}PREREG ERROR: {error}{RESET}")
        if status_line is None:
            out.append(" Waiting: pre-registration status unavailable.")
        elif not re.match(r"FROZEN\b", status_line, re.IGNORECASE):
            out.append(" Waiting: pre-registration freeze.")
        out.append(" " + ("Waiting: " if gpu is None or gpu["running"] else "") + gpu_words)
        for label, relative in BUILD_FILES:
            present = (Path(ROOT) / relative).is_file()
            out.append(f" {'Present:' if present else 'Waiting:'} {label}{'' if present else ' missing'} · {relative}")
    if state["halt"]:
        out += [f" {FG(196)}Halted: {clean(state['halt']['reason'])}{RESET}",
                f" Diagnostic: {clean(state['halt']['diagnostic_path'])}"]
    elif state["calibration_outcome"] == "FAIL" and state["step"] == 3:
        out.append(f" {BOLD}{FG(214)}Designed cheap stop: estimates failed calibration. No claim is promoted.{RESET}")
    if state["summary"]:
        out.append(" " + clean(state["summary"]))
    if rows >= 30:
        out.append(section("PLAN · ✓ passed  ✗ failed  ▶ current  · not recorded", 24, cols))
        for step, words in STEPS.items():
            step_status = state["steps"][step]
            icon = {"PASS": "✓", "FAIL": "✗", "running": "▶"}.get(step_status, "·")
            suffix = " (INVALID; no verdict)" if step_status == "INVALID" else ""
            out.append(f" {icon} {step} · {words}{suffix}")
    out.append(section("NOW", 28, cols))
    stage, progress = state["stage"], state["progress"]
    if stage:
        out.append(" " + clean(stage["plain_words"]))
        end = epoch(stage["finished_ts"]) if stage.get("finished_ts") else epoch(state["halt"]["ts"]) if state["halt"] else epoch(state["finished_ts"]) if state["finished_ts"] else now
        timing = f"stage time {dur(end - epoch(stage['ts']))} / cap {dur(stage['cap_s'])}"
        if progress:
            out.append(f" {bar(progress['done'], progress['total'])} {progress['done']}/{progress['total']} {clean(progress['unit'])} · {timing}")
        else:
            out.append(f" Progress not recorded · {timing}")
    else:
        reasons = state["admission"]["reasons"] if state["admission"] and not state["admission"]["allowed"] else []
        out.append(" " + ("; ".join(clean(r) for r in reasons) if reasons else "Waiting for a stage to start; the plan above shows what comes next."))
    prefix, out = out, []
    out.append(section("MACHINE · samples from this run; GPU display is shared", 30, cols))
    resources = state["resources"]
    if resources:
        avail, floor = resources["avail_gib"], resources["floor_gib"]
        out.append(f" Free memory {bar(avail, max(floor * 2, 1), floor=floor)} {avail:g} GiB · floor {floor:g} GiB (┃) · {avail - floor:+g} GiB above floor")
        lab = f"Lab memory {resources['rss_gib']:g} GiB · CPU {resources['cpu_pct']:g}%"
    else:
        out.append(" Free memory [················] not sampled · floor 8 GiB")
        lab = "Lab memory / CPU not sampled"
    out.append(f" {lab} · {gpu_words}")
    findings = state["findings"]
    out.append(section(f"FINDINGS · MATH-PROXY: math estimate, not evidence ({len(findings)})", 96, cols))
    for finding in findings[-2:]:
        out += [f" {clean(finding['finding_id'])}: {clean(finding['summary'])}", " " + clean(finding["path"])]
    if not findings:
        out.append(" None staged yet.")
    candidates = state["candidates"]
    out.append(section(f"CANDIDATE QUESTIONS ({len(candidates)}; newest 3) · ideas to test", 96, cols))
    for candidate in candidates[-3:]:
        out.append(f" {clean(candidate['candidate_id'])} · {clean(candidate['source'])} · offline {'yes' if candidate['offline'] else 'no'} · {clean(candidate['question'])}")
    if not candidates:
        out.append(" None yet; step 4 needs its own pre-registration.")
    out.append(section(f"LAST EVENTS · newest 1 of {len(state['recent'])} recent", 238, cols))
    out += [event_line(state["recent"][-1])] if state["recent"] else [" No run events yet; this is the plan before launch."]
    height = max(rows - len(prefix) - len(out), 0)
    out = prefix + check_lines(state, cols, height, int(now // 10) if check_page is None else check_page) + out
    return [dashboard_live.clip(line, cols) + RESET for line in out[:rows]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", nargs=2, type=int, metavar=("COLS", "ROWS"))
    args = parser.parse_args()
    if args.once:
        print("\n".join(render(*args.once)))
        return
    while True:
        cols, rows = os.get_terminal_size(sys.stdout.fileno())
        try:
            lines = render(cols - 1, rows)
        except Exception as error:
            lines = [f"{FG(196)}MathLab view error: {type(error).__name__}: {error}{RESET}"]
        sys.stdout.write("\033[H" + "\033[K\n".join(lines) + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(2)


if __name__ == "__main__":
    main()
