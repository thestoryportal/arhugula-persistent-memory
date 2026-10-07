"""Dashboard 'Experiment' tab, view-only: the GPU experiment running now, in plain words — which step
and stage, how long it has run, every finished run with its score out of 72, the run in progress and
its live log. When the GPU is idle it shows the last experiment's final state.
Usage: python3 dashboard_experiment.py [--once COLS ROWS]
"""
import glob, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESET, BOLD = "\033[0m", "\033[1m"
FG, BG = "\033[38;5;{}m".format, "\033[48;5;{}m".format
STEP = {"c10u": "Step 3 · new vocabulary word(s) per name", "c10v": "Step 4 · each fact picks its own depth",
        "c10w": "Step 5 · ceiling test", "c10x": "Step 6 · engine changes", "c10y": "Step 7 · direct weight solve",
        "c10z": "ASTRA · every word at once"}
KIND = {"mint1": "one new word per name", "mint2": "two new words per name", "multi": "ordinary write (baseline)",
        "modifier": "modifier-word write", "mint1_48": "one new word, 48-name control"}
BLOCK = {"F": "original names", "V2": "new name set"}
NOISE = re.compile(r"it/s\]|s/it\]|Loading checkpoint|Retrieving covariance|Loading cached|UserWarning|tensor\.detach|"
                   r"upd_norm = |Sliding Window Attention|^\s*\d+%\|")


def fit(t, w):
    return t if len(t) <= w else t[: max(w - 1, 0)] + "…"


def section(title, color, cols):
    return f"{BOLD}{FG(231)}{BG(color)} {title} {RESET}{FG(color)}{'━' * max(cols - len(title) - 2, 0)}{RESET}"


def plain(job):
    """behavior_F_r1_mint1_s0 -> 'original names · repeat · one new word per name · seed 0'."""
    m = re.match(r"(behavior|step0|contexts)_([A-Za-z0-9]+)_r(\d+)_([a-z0-9_]+?)_s(\w+)$", job)
    if not m:
        return job
    what, block, rep, kind, seed = m.groups()
    parts = [BLOCK.get(block, block)] + (["repeat"] if rep != "0" else [])
    parts.append({"step0": "setup check: ", "contexts": "preparing phrasings for "}.get(what, "") + KIND.get(kind, kind))
    if seed not in ("none", "snone"):
        parts.append(f"seed {seed}")
    return " · ".join(parts)


def score(log):
    try:
        text = open(log, errors="replace").read()
    except OSError:
        return None
    m = re.search(r"BEHAVIOR \S+: raw=\d+ binding=(\d+)", text)
    if m:
        return int(m.group(1))
    m = re.search(r"A7_\w+.*?para (\d+)/72", text)
    return int(m.group(1)) if m else None


def drivers():
    ps = subprocess.run(["/bin/ps", "-axo", "etime,command"], capture_output=True, text=True).stdout
    top, job = None, None
    for line in ps.splitlines():
        m = re.search(r"experiments/track_c/(c10[a-z])_\w+\.py (\S+)", line)
        if not m:
            continue
        if m.group(2) == "_job":
            a = dict(re.findall(r"--(\w+) (\S+)", line))
            job = f"{a.get('job', '?')}_{a.get('block', '?')}_r{a.get('replicate', 0)}_{a.get('kind', '?')}_s{a.get('seed', 'none')}"
        elif top is None:
            top = (m.group(1), m.group(2), line.split()[0])
    return top, job


def render(cols, rows):
    top, job = drivers()
    logs = sorted(glob.glob(os.path.join(ROOT, "results", "**", "*.log"), recursive=True), key=os.path.getmtime)
    stage_logs = [l for l in logs if re.search(r"/c10\w*_logs/", l)]
    stage_log = stage_logs[-1] if stage_logs else None
    if top:
        key, stage, etime = top
        head = f" ● RUNNING · {STEP.get(key, key)} · stage {stage} · running {etime}"
        hbg = 28
    else:
        head = f" ○ GPU IDLE · last experiment: {os.path.relpath(stage_log, ROOT) if stage_log else 'none'}"
        hbg = 240
    out = [f"{BOLD}{FG(231)}{BG(hbg)}{fit(head, cols).ljust(cols)}{RESET}"]
    done = []
    if stage_log:
        for l in open(stage_log, errors="replace"):
            m = re.match(r"completed (\S+); log=(\S+)", l.strip())
            if m:
                done.append((m.group(1), m.group(2)))
        tail = [l.strip() for l in open(stage_log, errors="replace") if l.strip()]
        ends = [l for l in tail if re.match(r"(STAGE_EXIT|HALT)", l)]
    else:
        ends = []
    out.append(section(f"FINISHED RUNS ({len(done)})", 24, cols))
    for name, log in done[-max(rows // 3, 4):]:
        s = score(log) if name.startswith("behavior") else None
        badge = f"{BOLD}{FG(40 if s and s >= 30 else 214 if s else 245)}{f'{s}/72' if s is not None else 'done':>6}{RESET}"
        out.append(f" {FG(40)}✔{RESET} {badge}  {fit(plain(name), cols - 12)}")
    for e in ends[-2:]:
        out.append(f" {BOLD}{FG(40 if e.endswith('=0') else 196)}{fit(e, cols - 2)}{RESET}")
    out.append(section("NOW", 28 if top else 240, cols))
    if top:
        out.append(f" {BOLD}▶ {fit(plain(job) if job else 'between runs', cols - 4)}{RESET}")
        cur = logs[-1] if logs else None
        if cur:
            lines = []
            for raw in open(cur, errors="replace"):
                seg = raw.rstrip("\n").split("\r")[-1].rstrip()
                if seg.strip() and not NOISE.search(seg):
                    lines.append(seg)
            out.append(f" {FG(245)}live log: {fit(os.path.relpath(cur, ROOT), cols - 13)}{RESET}")
            for l in lines[-max(rows - len(out) - 1, 0):]:
                hl = 40 if re.search(r"INERT|PASS|BEHAVIOR", l) else 196 if re.search(r"HALT|FAIL|Error", l) else None
                out.append(f"   {FG(hl) + BOLD if hl else ''}{fit(l.strip(), cols - 4)}{RESET}")
    else:
        out.append(f" {FG(245)}Nothing on the GPU. The next experiment appears here when it starts.{RESET}")
    return out[:rows]


def main():
    if "--once" in sys.argv:
        i = sys.argv.index("--once")
        print("\n".join(render(int(sys.argv[i + 1]), int(sys.argv[i + 2]))))
        return
    while True:
        cols, rows = os.get_terminal_size(sys.stdout.fileno())
        lines = render(cols, rows)
        sys.stdout.write("\033[H" + "".join(l + "\033[K\n" for l in lines[:-1]) + lines[-1] + "\033[K\033[J")
        sys.stdout.flush()
        time.sleep(3)


if __name__ == "__main__":
    main()
