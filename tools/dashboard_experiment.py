"""Dashboard 'Experiment' tab, view-only: the GPU experiment in plain words.
Header (what, stage, elapsed, ETA) · machine line (GPU busy %, GPU memory, job CPU/RAM, free RAM) ·
progress against the stage plan · a results table (one row per finished run: reworded /72 with a goal
bar, trained phrasing /24, control /72, side effects, run time) · the run in progress (phase strip,
training-loss trend, cleaned live log). When the GPU is idle it shows the last experiment.
Usage: python3 dashboard_experiment.py [--once COLS ROWS]
"""
import glob, json, os, re, subprocess, sys, textwrap, time
import dashboard_live

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOAL, OUT_OF = 61, 72
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
FG, BG = "\033[38;5;{}m".format, "\033[48;5;{}m".format
STEP = {"c10u": "Step 3 · new vocabulary word(s) per name", "c10v": "Step 4 · each fact picks its own depth",
        "c10w": "Step 5 · ceiling test (training, measurement only)", "c10x": "Step 6 · engine changes",
        "c10y": "Step 7 · direct weight solve", "c10z": "ASTRA · every word at once"}
KIND = {"mint1": "one new word per name", "mint2": "two new words per name", "multi": "ordinary write (baseline)",
        "modifier": "modifier-word write", "mint1_48": "one new word, 48-name control"}
BLOCK = {"F": "original names", "V2": "new name set"}
STAGE_WORDS = {"step0": "setup check", "p1-preflight": "pre-flight check (usual-method baseline)", "p1-a1": "train: single-word control",
               "p1-a2": "train: real two-word control", "p1-a7": "train: made-up names", "p1-canon": "train: trained-phrasing check",
               "p1-shuf": "train: shuffled-values control", "p1-eval": "score everything",
               "p2-coordinator": "repeat-run coordinator", "p2-a7-s1": "repeat: made-up names, seed 1",
               "p2-shuf-s1": "repeat: shuffled-values control, seed 1", "p2-canon-s1": "repeat: trained-phrasing check, seed 1",
               "p2-a1-s1": "repeat: single-word control, seed 1", "p2-a7-rt": "repeat: made-up names, same seed retrained",
               "p2-shuf-rt": "repeat: shuffled control, same seed retrained", "p2-eval": "repeat: score everything"}
ARM_WORDS = {"A1_single": "single-word control", "A2_coherent2": "real two-word control", "A7_coined_coined": "made-up names",
             "A7_shuf": "made-up names, shuffled (control)", "A7_canon": "made-up names, trained phrasing"}
PHASES = [("load", r"loaded Qwen|Loading checkpoint"), ("statistics", r"Retrieving covariance|Loading cached"),
          ("write/train", r"=== RECIPE|step \d+ loss"), ("safety check", r"LAW#5 INERTNESS|-> INERT"),
          ("score", r"A1_single|A2_coherent|A7_\w+ +canon="), ("done", r"BEHAVIOR |STAGE_EXIT")]
NOISE = re.compile(r"it/s\]|s/it\]|Loading checkpoint|Retrieving covariance|Loading cached|UserWarning|tensor\.detach|"
                   r"upd_norm = |Sliding Window Attention|^\s*\d+%\||Triggered internally")
ARM_LINE = re.compile(r"^\s*(A\d\w*)\s+canon=.*?n: canon (\d+)/(\d+) para (\d+)/(\d+).*?L1 (\d+)/(\d+) L3 (\d+)/(\d+).*?ppl ([\d.]+)->([\d.]+)")
SPARK = "▁▂▃▄▅▆▇█"


def fit(t, w):
    t = " ".join(str(t).split())
    return t if len(t) <= w else t[: max(w - 1, 0)] + "…"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout


def section(title, color, cols):
    return f"{BOLD}{FG(231)}{BG(color)} {title} {RESET}{FG(color)}{'━' * max(cols - len(title) - 2, 0)}{RESET}"


def bar(v, total, width, goal=None):
    if v is None:
        return f"{FG(240)}{'·' * width}{RESET}"
    fill = round(min(v, total) / total * width)
    mark = round(goal / total * width) if goal else -1
    col = 40 if goal and v >= goal else 214 if goal and v >= 30 else 39
    return "".join(f"{FG(col)}█" if i < fill else f"{FG(196)}┃" if i == mark else f"{FG(238)}░" for i in range(width)) + RESET


def dur(s):
    s = int(max(s, 0))
    return f"{s // 3600}h{s % 3600 // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def plain_run(name):
    m = re.match(r"(behavior|step0|contexts)_([A-Za-z0-9]+)_r(\d+)_([a-z0-9_]+?)_s(\w+)$", name)
    if m:
        what, block, rep, kind, seed = m.groups()
        parts = [BLOCK.get(block, block)] + (["repeat"] if rep != "0" else [])
        parts.append({"step0": "setup: ", "contexts": "phrasings: "}.get(what, "") + KIND.get(kind, kind))
        if seed not in ("none", "snone"):
            parts.append(f"seed {seed}")
        return " · ".join(parts)
    return STAGE_WORDS.get(name, name)


def machine(pids, cols=200):
    gpu = sh("/usr/sbin/ioreg", "-r", "-d", "1", "-w", "0", "-c", "IOAccelerator")
    util = re.search(r'"Device Utilization %"=(\d+)', gpu)
    mem = re.search(r'"In use system memory"=(\d+)', gpu)
    cpu = rss = 0.0
    if pids:
        for line in sh("/bin/ps", "-o", "%cpu=,rss=", "-p", ",".join(pids)).splitlines():
            c, r = line.split()
            cpu, rss = cpu + float(c), rss + float(r)
    vm = sh("/usr/bin/vm_stat")
    page = int(re.search(r"page size of (\d+)", vm).group(1)) if "page size of" in vm else 16384
    free = sum(int(re.search(rf"{k}:\s+(\d+)", vm).group(1)) for k in ("Pages free", "Pages inactive", "Pages speculative")
               if re.search(rf"{k}:\s+(\d+)", vm)) * page / 2 ** 30
    u = int(util.group(1)) if util else None
    gmem = int(mem.group(1)) / 2 ** 30 if mem else 0
    if cols < 90:
        return f" {BOLD}GPU{RESET} {bar(u, 100, 6)} {BOLD}{u if u is not None else '?'}%{RESET} · {gmem:.1f}G · free {free:.0f}G"
    return (f" {BOLD}GPU{RESET} {bar(u, 100, 10)} {BOLD}{u if u is not None else '?'}%{RESET}"
            f"  {DIM}·{RESET} GPU mem {BOLD}{gmem:.1f} GB{RESET}"
            f"  {DIM}·{RESET} job CPU {BOLD}{cpu:.0f}%{RESET}  {DIM}·{RESET} job RAM {BOLD}{rss / 2 ** 20:.1f} GB{RESET}"
            f"  {DIM}·{RESET} free RAM {BOLD}{free:.0f} GB{RESET}")


def running():
    top, pids, job = None, [], None
    for line in sh("/bin/ps", "-axo", "pid=,etime=,command=").splitlines():
        pid, etime, command = (line.split(None, 2) + ["", ""])[:3]
        m = dashboard_live.GPU_JOB_RE.search(dashboard_live.script_call(command) or "")
        if not m:
            continue
        pids.append(pid)
        if m.group(2) == "_job":
            a = dict(re.findall(r"--(\w+) (\S+)", line))
            job = f"{a.get('job', '?')}_{a.get('block', '?')}_r{a.get('replicate', 0)}_{a.get('kind', '?')}_s{a.get('seed', 'none')}"
        elif top is None:
            top = (m.group(1), m.group(2), etime)
    return top, pids, job


def parse_log(path):
    arms, losses, inert, behavior, lines = {}, [], None, None, []
    for raw in open(path, errors="replace"):
        seg = raw.rstrip("\n").split("\r")[-1].rstrip()
        if not seg.strip():
            continue
        if m := ARM_LINE.match(seg):
            g = m.groups()
            arms[g[0]] = {"canon": int(g[1]), "canon_n": int(g[2]), "para": int(g[3]), "para_n": int(g[4]),
                          "l1": int(g[5]), "l3": int(g[7]), "l3_n": int(g[8]), "ppl": float(g[10]) - float(g[9])}
        elif m := re.search(r"step (\d+) loss ([\d.eE+-]+)", seg):
            losses.append((int(m.group(1)), float(m.group(2))))
        elif m := re.search(r"\|Δexpr\|=([\d.]+).*-> (\w+)", seg):
            inert = (float(m.group(1)), m.group(2))
        elif m := re.search(r"BEHAVIOR \S+: raw=\d+ binding=(\d+)", seg):
            behavior = int(m.group(1))
        if not NOISE.search(seg):
            lines.append(seg)
    text_tail = open(path, errors="replace").read()[-400:]
    exit_m = re.search(r"STAGE_EXIT=(\d+)", text_tail)
    return {"arms": arms, "losses": losses, "inert": inert, "behavior": behavior, "lines": lines,
            "exit": int(exit_m.group(1)) if exit_m else None, "halt": bool(re.search(r"(?m)^HALT\b", text_tail))}


def run_rows(paths, cols):
    """One row per made-up-names arm of each finished run (A7*), with A1 as the control column."""
    rows, wide = [], cols >= 110
    name_w = max(cols - (78 if wide else 40), 14)
    for p in paths:
        r = parse_log(p)
        name = plain_run(os.path.basename(p)[:-4].replace("behavior_", "behavior_", 1))
        took = dur(os.path.getmtime(p) - os.stat(p).st_birthtime)
        a7s = {k: v for k, v in r["arms"].items() if k.startswith("A7")} or ({"run": None} if r["behavior"] is None else {})
        if not a7s and r["behavior"] is not None:
            a7s = {"A7": {"para": r["behavior"], "para_n": OUT_OF}}
        ctrl = r["arms"].get("A1_single")
        ok = r["exit"] in (None, 0) and not r["halt"]
        for arm, a in a7s.items():
            label = name if len(a7s) == 1 else f"{name} · {ARM_WORDS.get(arm, arm)}"
            icon = f"{FG(40)}✔" if ok else f"{FG(196)}✖"
            if a is None:
                if r["losses"]:
                    ls = [l for _, l in r["losses"]][-12:]
                    lo, hi = min(ls), max(ls)
                    spark = "".join(SPARK[int((v - lo) / (hi - lo + 1e-12) * 7)] for v in ls)
                    note = (f"{FG(39)}{spark}{RESET} trained {r['losses'][-1][0]} steps · final loss {r['losses'][-1][1]:.2g}" if wide
                            else f"{FG(39)}{spark[-6:]}{RESET} loss {r['losses'][-1][1]:.1g}")
                else:
                    note = f"{FG(245)}{'setup stage (no score)' if ok else 'stopped'}{RESET}"
                rows.append(f" {icon}{RESET} {fit(label, name_w):<{name_w}} {note}  {FG(245)}{took:>7}{RESET}")
                continue
            score = f"{BOLD}{a['para']:>2}{RESET}/{a['para_n']}"
            line = f" {icon}{RESET} {fit(label, name_w):<{name_w}} {bar(a['para'], OUT_OF, 12, GOAL)} {score}"
            if wide:
                canon = f"{a['canon']}/{a['canon_n']}" if "canon" in a else "—"
                c1 = f"{ctrl['para']}/{ctrl['para_n']}" if ctrl else "—"
                side = (f"L1 {a['l1']}/12 · ppl {a['ppl']:+.2f}" if "l1" in a else "—")
                sc = 196 if "l1" in a and (a["l1"] > 1 or a["ppl"] > 0.5) else 245
                line += f"  {canon:>6}  {c1:>6}  {FG(sc)}{side:<18}{RESET}"
            rows.append(line + f"  {FG(245)}{took:>7}{RESET}")
    return rows, wide, name_w


def is_experiment_log(path):
    # Relative to ROOT: the worktree itself is named c10k-route-a, and Lab View mirrors logs under results/labviz/.
    parts = os.path.relpath(path, ROOT).split(os.sep)
    archived = any(x.startswith(("_quarantine", "attempt")) for x in parts)   # set-aside records, not the live run
    return parts[1:2] != ["labviz"] and not archived and any(x.startswith("c10") for x in parts[1:])


BINDING = "A7_coined_coined"


def answers_from_record(record):
    """(recipe, templates, facts) for the binding arm of the last recipe that recorded the model's answers, else None.
    facts = [{subj, val, answers: [(text, fully right), ...] in template order}]."""
    for name, recipe in reversed(list((record.get("recipes") or {}).items())):
        gen = (((recipe.get("arms") or {}).get(BINDING) or {}).get("extra") or {}).get("generated")
        if not gen:
            continue
        templates = list(dict.fromkeys(g["template"] for g in gen))
        vals = {d["subj"]: d.get("val") for d in ((recipe.get("detail") or {}).get(BINDING) or [])}
        facts = {}
        for g in gen:
            f = facts.setdefault(g["subj"], {"subj": g["subj"], "val": vals.get(g["subj"]), "answers": [None] * len(templates)})
            f["answers"][templates.index(g["template"])] = (g["text"].strip(), bool(g["full"]))
        return name, templates, list(facts.values())
    return None


def words_lines(source, recipe, templates, facts, cols):
    """One row per made-up fact (place → the capital we wrote in); each column is one reworded question about that
    place, with the full question as the column header and the model's own words under it, ✓ right / ✗ wrong."""
    caption = ("Each row is one made-up fact we wrote into the model. Each column asks about that place in a different "
               "wording; the cell is what the model wrote next. ✓ = the whole capital, ✗ = not.")
    out = [f" {DIM}{l}{RESET}" for l in textwrap.wrap(caption, max(cols - 2, 20))]
    out.append(f" {DIM}source: {source} · recipe {recipe} · made-up names arm{RESET}")
    name_w = min(max([len(f["subj"]) + 3 + len(f["val"] or "?") for f in facts] + [28]), 34)
    cell = max((cols - name_w - 3) // max(len(templates), 1) - 3, 12)
    heads = [textwrap.wrap(f"Q{i}: {t.replace('{}', '[place]')} …", cell + 2) for i, t in enumerate(templates, 1)]
    first = ["made-up place → capital", "we wrote in"]
    for k in range(max([len(h) for h in heads] + [len(first)])):
        left = first[k] if k < len(first) else ""
        row = " ".join(f"{(h[k] if k < len(h) else ''):<{cell + 2}}" for h in heads)
        out.append(f" {DIM}{left:<{name_w}}{RESET} {BOLD}{FG(214)}{row}{RESET}")
    for f in facts:
        cells = []
        for a in f["answers"]:
            if a is None:
                cells.append(f"{FG(240)}{'· not recorded':<{cell + 2}}{RESET}")
            else:
                cells.append(f"{FG(40 if a[1] else 196)}{'✓' if a[1] else '✗'} {fit(a[0], cell):<{cell}}{RESET}")
        out.append(f" {BOLD}{fit(f['subj'] + ' → ' + (f['val'] or '?'), name_w):<{name_w}}{RESET} " + " ".join(cells))
    return out


def latest_answers(data_dir):
    """The newest recorded answers under an experiment's data folder: (source label, recipe, templates, facts) or None."""
    paths = [p for pat in ("*/eval.json", "*/eval_halt.json", "*/attempt*/eval_halt.json", "*/pass*.json", "*.json")
             for p in glob.glob(os.path.join(data_dir, pat))]
    for p in sorted(paths, key=os.path.getmtime, reverse=True):
        try:
            found = answers_from_record(json.load(open(p)))
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            continue
        if found:
            label = os.path.relpath(p, ROOT) + (" (HALTED attempt)" if "halt" in os.path.basename(p) else "")
            return (label,) + found
    return None


def render(cols, rows):
    top, pids, job = running()
    logs = sorted((p for p in glob.glob(os.path.join(ROOT, "results", "**", "*.log"), recursive=True)
                   if is_experiment_log(p)), key=os.path.getmtime)
    if not logs:
        return [f"{FG(245)}No experiment logs found under results/.{RESET}"]
    cur = logs[-1]
    run_dir = os.path.dirname(cur)
    runs = sorted(glob.glob(os.path.join(run_dir, "*.log")), key=lambda p: os.stat(p).st_birthtime)
    finished = runs[:-1] if top else runs
    # stage plan (c10u-style *_started.json with a plan) for progress + ETA
    exp_dir = os.path.dirname(run_dir) if os.path.basename(run_dir) == "logs" else run_dir
    plans = sorted(glob.glob(os.path.join(exp_dir, "*_started.json")), key=os.path.getmtime)
    total = None
    if top and plans:
        try:
            total = len(json.load(open(plans[-1])).get("plan") or []) or None
        except (OSError, ValueError):
            pass
    behav_done = [p for p in finished if os.path.basename(p).startswith("behavior_")] if total else finished
    times = [os.path.getmtime(p) - os.stat(p).st_birthtime for p in behav_done if os.path.basename(p).startswith(("behavior_", "p1-"))]
    avg = sum(times) / len(times) if times else None

    m = re.search(r"(?:^|/)(c10[a-z])", os.path.relpath(cur, ROOT))
    key = top[0] if top else m.group(1) if m else "?"
    if top:
        eta = ""
        if total and avg:
            left = max(total - len(behav_done), 0) * avg
            eta = f" · about {dur(left)} left (≈{time.strftime('%H:%M', time.localtime(time.time() + left))})"
        head, hbg = f" ● RUNNING · {STEP.get(key, key)} · stage {top[1]} · {top[2]} elapsed{eta}", 28
    else:
        head, hbg = f" ○ GPU IDLE · last: {STEP.get(key, key)} · {os.path.relpath(run_dir, ROOT)}", 240
    out = [f"{BOLD}{FG(231)}{BG(hbg)}{fit(head, cols).ljust(cols)}{RESET}", machine(pids, cols)]

    out.append(section("PROGRESS", 24, cols))
    if total:
        n = len(behav_done)
        out.append(f" {bar(n, total, max(min(cols - 44, 40), 10))} {BOLD}{n} of {total} runs{RESET}"
                   + (f"  {DIM}·{RESET} avg {dur(avg)} per run" if avg else ""))
    else:
        out.append(f" {BOLD}{len(finished)} stage(s) finished{RESET}" + (f"  {DIM}·{RESET} avg {dur(avg)} each" if avg else "")
                   + (f"  {DIM}·{RESET} goal {GOAL}/{OUT_OF} reworded (red ┃ on the bars)" if cols >= 90 else ""))

    table, wide, name_w = run_rows(finished, cols)
    out.append(section("FINISHED RUNS", 25, cols))
    if wide:
        out.append(f" {DIM}  {'run':<{name_w}} {'reworded right (of 72)':<16}  {'train':>6}  {'ctrl':>6}  {'side effects':<18}  {'time':>7}{RESET}")
    top_dir = os.path.relpath(run_dir, ROOT).split(os.sep)[:2]   # results/<experiment>[_logs]
    data_dir = os.path.join(ROOT, *top_dir)
    data_dir = data_dir[:-5] if data_dir.endswith("_logs") and os.path.isdir(data_dir[:-5]) else data_dir
    found = latest_answers(data_dir)
    words = words_lines(*found, cols) if found else []
    now_rows = 9 if top else 2
    keep = max(rows - len(out) - now_rows - 1 - (len(words) + 1 if words else 0), 4)
    out += table[-keep:]

    if top:
        r = parse_log(cur)
        out.append(section("NOW", 28, cols))
        reached = max((i for i, (_, pat) in enumerate(PHASES) if any(re.search(pat, l) for l in r["lines"])), default=-1)
        strip = "  ".join(f"{FG(40) + BOLD if i < reached else FG(214) + BOLD if i == reached else FG(240)}"
                          f"{'●' if i <= reached else '○'} {nm}{RESET}" for i, (nm, _) in enumerate(PHASES))
        out.append(f" {BOLD}▶ {fit(plain_run(job) if job else plain_run(os.path.basename(cur)[:-4]), cols - 4)}{RESET}")
        out.append(f"   {strip}" if cols >= 90 else f"   phase: {BOLD}{FG(214)}{PHASES[max(reached, 0)][0]}{RESET} ({max(reached, 0) + 1} of {len(PHASES)})")
        if r["losses"]:
            ls = [l for _, l in r["losses"]][-max(cols - 40, 10):]
            lo, hi = min(ls), max(ls)
            spark = "".join(SPARK[int((v - lo) / (hi - lo + 1e-12) * 7)] for v in ls)
            out.append(f"   training step {BOLD}{r['losses'][-1][0]}{RESET} · loss {BOLD}{r['losses'][-1][1]:.4g}{RESET}  {FG(39)}{spark}{RESET}")
        if r["inert"]:
            ok = r["inert"][1] == "INERT"
            out.append(f"   safety check: {BOLD}{FG(40 if ok else 196)}{'passed' if ok else 'FAILED'}{RESET} (change {r['inert'][0]})")
        for l in r["lines"][-max(min(rows - len(out), 4 if words else rows), 0):]:
            hl = 40 if re.search(r"INERT|PASS|BEHAVIOR", l) else 196 if re.search(r"HALT|FAIL|Error", l) else 250
            out.append(f"   {FG(hl)}{fit(l.strip(), cols - 4)}{RESET}")
    if words and rows - len(out) > 3:   # below NOW, so a running stage's progress is never pushed off
        title = "WORDS & MODEL ANSWERS (newest recorded scoring" + ("; the running stage records its own only when it finishes)" if top else ")")
        out.append(section(title, 30, cols))
        out += words[: rows - len(out)]
    return out[:rows]


def main():
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(render(int(sys.argv[i + 1]), int(sys.argv[i + 2]))))
        return
    stamp = dashboard_live.source_stamp(dashboard_live.TOOLS)
    while True:
        dashboard_live.maybe_reload(stamp)
        cols, rows = os.get_terminal_size(sys.stdout.fileno())
        try:
            lines = render(cols, rows)
        except Exception as e:  # keep the tile alive and show why
            lines = [f"{FG(196)}experiment view error: {type(e).__name__}: {e}{RESET}"]
        lines = [dashboard_live.clip(l, cols - 2) for l in lines]   # never wrap: a wrapped line scrolls the top away
        sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(3)


if __name__ == "__main__":
    main()
