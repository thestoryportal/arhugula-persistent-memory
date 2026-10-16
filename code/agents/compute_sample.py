"""Read-only M3 load sampler for admission decisions (LEAN post-wave-1 plan, Step 305).

Usage:
  python code/agents/compute_sample.py [--interval N] OUT.tsv   append one row every N seconds (default 10)
  python code/agents/compute_sample.py --once                   print one row (no header) and exit; ship.sh uses it
  python code/agents/compute_sample.py --header                 print HEADER and exit; runs no probe

Columns are COLUMNS. Process groups are matched on the executable basename: astra = codex, builders = claude,
tests = a Python run as `python ... -m unittest`. gpu_ok/gpu_blockers come from the existing
lab.runners.c10w_p2_gate.check_gpu probe; gpu_blockers is "probe_failed" when that probe refused.
research_blockers is the part of that record that is research work (followup-308 Step 315): the autoresearch
tmux session, a non-Python compute runtime, or a Python running a research script or module; see research_blockers().

It only observes: it never kills or signals a process, and it only appends to OUT.tsv. A new OUT.tsv gets
HEADER first; an existing file whose first line is not HEADER, a symlink or a non-regular file is refused.
A probe that fails or prints something the parser does not recognise stops the sampler (exit 2) with no row.
Loop mode exits 0 when its owner is gone: the nearest `claude` ancestor at start (the T040 rule of
code/agents/context_watch.py); with no `claude` ancestor it refuses to start (exit 1).
"""
import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab.runners.c10w_p2_gate import check_gpu  # noqa: E402

GROUPS = ("astra", "builders", "tests")
COLUMNS = ("utc", "load1", "load5", "cpu_idle_pct", "mem_free_pct", "swap_used_mib",
           *(f"{g}_{k}" for g in GROUPS for k in ("n", "cpu_pct", "rss_mib")),
           "gpu_ok", "gpu_blockers", "memit_free_gib", "research_blockers")
HEADER = "\t".join(COLUMNS) + "\n"
MEMIT = "/Volumes/memit"
PYTHON_EXE = re.compile(r"(?i)^python[0-9.]*$")
RESEARCH_PATHS = ("code/lab/", "code/memit/", "experiments/")
RESEARCH_MODULES = ("lab.", "memit.")
PY_OPTS_WITH_ARG = ("-W", "-X", "--check-hash-based-pycs")


class Refusal(Exception):
    pass


# ---- pure parsers (captured command text in, values out) ----

def parse_top(text):
    """`top -l 2 -n 0 -s 1`: (load1, load5, idle %) from the last sample (the first one counts since boot)."""
    loads = re.findall(r"^Load Avg: ([0-9.]+), ([0-9.]+), ([0-9.]+)", text, re.M)
    idles = re.findall(r"^CPU usage: .*?([0-9.]+)% idle", text, re.M)
    if not loads or not idles:
        raise ValueError("top output has no Load Avg or CPU usage line")
    return float(loads[-1][0]), float(loads[-1][1]), float(idles[-1])


def parse_memory_pressure(text):
    m = re.search(r"^System-wide memory free percentage: (\d+)%\s*$", text, re.M)
    if not m:
        raise ValueError("memory_pressure output has no free percentage line")
    return int(m.group(1))


def parse_swapusage(text):
    """`sysctl vm.swapusage`: used swap in MiB."""
    m = re.search(r"\bused = ([0-9.]+)([KMG])\b", text)
    if not m:
        raise ValueError("sysctl vm.swapusage output has no used = <n>[KMG] field")
    return float(m.group(1)) * {"K": 1 / 1024, "M": 1, "G": 1024}[m.group(2)]


def _group(command):
    argv = command.split()
    exe = os.path.basename(argv[0])
    if exe == "codex":
        return "astra"
    if exe == "claude":
        return "builders"
    if PYTHON_EXE.match(exe):
        for i, tok in enumerate(argv[1:], 1):
            if tok == "-m":
                return "tests" if argv[i + 1:i + 2] == ["unittest"] else None
            if tok == "-c" or not tok.startswith("-"):
                return None
    return None


def parse_processes(text):
    """`ps -axww -o pid=,pcpu=,rss=,command=`: {group: (count, summed CPU %, summed RSS MiB)}."""
    sums = {g: [0, 0.0, 0] for g in GROUPS}
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("process inventory is empty")
    for line in lines:
        parts = line.split(None, 3)
        if len(parts) != 4 or not parts[0].isdigit() or not parts[2].isdigit():
            raise ValueError(f"unrecognised ps line: {line!r}")
        try:
            cpu = float(parts[1])
        except ValueError:
            raise ValueError(f"unrecognised ps line: {line!r}") from None
        g = _group(parts[3])
        if g:
            sums[g][0] += 1
            sums[g][1] += cpu
            sums[g][2] += int(parts[2])
    return {g: (n, round(cpu, 1), round(rss / 1024, 1)) for g, (n, cpu, rss) in sums.items()}


def gpu_fields(result):
    """check_gpu record -> (gpu_ok, gpu_blockers)."""
    if "reason" in result:
        return "0", "probe_failed"
    return ("1" if result["ok"] else "0"), str(len(result["blocking_processes"]) + len(result["blocking_tmux"]))


def _is_research_process(line):
    """A check_gpu blocking_processes line ('<pid> <command>') -> True when it is research work."""
    argv = line.split()[1:]
    if not PYTHON_EXE.match(os.path.basename(argv[0])):
        return True  # check_gpu only lists Pythons and local-model runtimes (ollama, llama, mlx)
    args = iter(argv[1:])
    for tok in args:
        if tok in PY_OPTS_WITH_ARG:
            next(args, None)
        elif tok == "-m":
            return next(args, "").startswith(RESEARCH_MODULES)
        elif tok == "-c":
            return False
        elif not tok.startswith("-"):
            return any(p in tok for p in RESEARCH_PATHS)
    return False


def research_blockers(result):
    """check_gpu record -> research_blockers cell: "probe_failed", or the count of research blockers."""
    if "reason" in result:
        return "probe_failed"
    return str(len(result["blocking_tmux"]) + sum(map(_is_research_process, result["blocking_processes"])))


def parse_ppid_comm(text):
    ppid, comm = text.split(None, 1)
    return int(ppid), os.path.basename(comm.strip())


def format_row(s):
    cells = [s["utc"], f"{s['load1']:.2f}", f"{s['load5']:.2f}", f"{s['cpu_idle_pct']:.1f}",
             str(s["mem_free_pct"]), f"{s['swap_used_mib']:.1f}"]
    for g in GROUPS:
        n, cpu, rss = s["groups"][g]
        cells += [str(n), f"{cpu:.1f}", f"{rss:.1f}"]
    cells += [*s["gpu"], f"{s['memit_free_gib']:.1f}", s["research_blockers"]]
    return "\t".join(cells) + "\n"


# ---- probes (the only place that runs commands) ----

def probe(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not r.stdout.strip():
        raise Refusal(f"probe {' '.join(cmd)} failed rc={r.returncode}: {r.stderr.strip()}")
    return r.stdout


def collect():
    load1, load5, idle = parse_top(probe(["/usr/bin/top", "-l", "2", "-n", "0", "-s", "1"]))
    gpu = check_gpu()
    return dict(
        utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        load1=load1, load5=load5, cpu_idle_pct=idle,
        mem_free_pct=parse_memory_pressure(probe(["/usr/bin/memory_pressure"])),
        swap_used_mib=parse_swapusage(probe(["/usr/sbin/sysctl", "vm.swapusage"])),
        groups=parse_processes(probe(["/bin/ps", "-axww", "-o", "pid=,pcpu=,rss=,command="])),
        gpu=gpu_fields(gpu),
        memit_free_gib=shutil.disk_usage(MEMIT).free / 1024 ** 3,
        research_blockers=research_blockers(gpu),
    )


# ---- owner rule (copied from code/agents/context_watch.py owner_pid/alive; no signal is sent) ----

def _ps_ppid_comm(pid):
    r = subprocess.run(["/bin/ps", "-o", "ppid=,comm=", "-p", str(pid)], capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    return parse_ppid_comm(r.stdout)


def owner_pid(start=None, lookup=_ps_ppid_comm):
    """Nearest ancestor whose executable is named claude."""
    pid = os.getppid() if start is None else start
    while pid > 1:
        found = lookup(pid)
        if found is None:
            break
        ppid, comm = found
        if comm == "claude":
            return pid
        pid = ppid
    sys.exit("compute_sample: no claude ancestor found; refusing to run unowned")


def alive(pid):
    r = subprocess.run(["/bin/ps", "-o", "pid=", "-p", str(pid)], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip() == str(pid):
        return True
    if r.returncode == 1 and not r.stdout.strip() and not r.stderr.strip():
        return False
    raise Refusal(f"ps liveness check for pid {pid} unclear rc={r.returncode}: {r.stderr.strip()}")


# ---- append-only log ----

def open_log(path):
    try:
        fd = os.open(path, os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o644)
    except OSError as e:
        raise Refusal(f"cannot open {path}: {e}") from None
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise Refusal(f"{path} is not a regular file")
        if st.st_size == 0:
            write_all(fd, HEADER)
        elif os.pread(fd, len(HEADER), 0).decode("utf-8", "replace") != HEADER:
            raise Refusal(f"{path} does not start with the compute_sample header; refusing to append")
    except BaseException:
        os.close(fd)
        raise
    return fd


def write_all(fd, text):
    data = text.encode()
    while data:
        data = data[os.write(fd, data):]


def watch(fd, owner, interval, collect=collect, sleep=time.sleep):
    """Append one row per interval until the owner is gone; return the number of rows written."""
    rows = 0
    while True:
        start = time.monotonic()
        if not alive(owner):
            print(f"compute_sample: owner claude pid {owner} gone; sampler exits", flush=True)
            return rows
        write_all(fd, format_row(collect()))
        rows += 1
        sleep(max(0.0, interval - (time.monotonic() - start)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--interval", type=float, default=10.0)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--header", action="store_true")
    ap.add_argument("out", nargs="?")
    args = ap.parse_args(argv)
    if args.interval <= 0:
        ap.error("--interval must be > 0")
    if args.header:
        if args.once or args.out is not None:
            ap.error("--header takes no other mode")
        sys.stdout.write(HEADER)
        return 0
    if args.once == (args.out is not None):
        ap.error("give exactly one of --once or OUT.tsv")
    try:
        if args.once:
            sys.stdout.write(format_row(collect()))
            return 0
        owner = owner_pid()
        fd = open_log(args.out)
        try:
            watch(fd, owner, args.interval)
        finally:
            os.close(fd)
    except (Refusal, ValueError) as e:
        print(f"compute_sample: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
