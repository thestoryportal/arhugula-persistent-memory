"""Where the v2 record layout keeps run output: the one home for folders that live tools create and scan, so a layout
change is an edit here rather than a search across tools (ICM v2, G5 policy A).

Shell runners cannot import this; they spell the same folders out and say so beside them."""
from pathlib import Path

# The MathLab runtime writes two records: the instrument's own runs (ml) and NEW-1's (new1). Before v2 they shared
# one staging folder, and the lab-wide rules (one stop policy, one dashboard view) still read both as one set.
ML_RUNS = "experiments/ml/runs"
NEW1_RUNS = "experiments/new1/runs"
LAB_RUNS = (ML_RUNS, NEW1_RUNS)
# NEW-1 dispatch receipts sit in the same runs folder as NEW-1's run namespaces; the prefix tells them apart.
NEW1_DISPATCH_PREFIX = "new1_dispatch_"


def run_dir(root, experiment, slug):
    """A run's folder inside its record."""
    return Path(root) / "experiments" / experiment / "runs" / slug


def halts_dir(run):
    """A run writes its own halts beside its output (v2: runs/<slug>/halts/)."""
    return Path(run) / "halts"


def lab_run_dirs(root):
    """Every MathLab-runtime run folder, ml and new1 together, in name order within each record."""
    return [d for runs in LAB_RUNS for d in sorted((Path(root) / runs).glob("*")) if d.is_dir()]


def lab_event_streams(root):
    """Every MathLab-runtime event stream, ml and new1 together."""
    return [d / "events.jsonl" for d in lab_run_dirs(root) if (d / "events.jsonl").is_file()]


def is_new1_namespace(name):
    """A NEW-1 run namespace, as distinct from a dispatch receipt folder in the same runs folder."""
    return name.startswith("new1_") and not name.startswith(NEW1_DISPATCH_PREFIX)


def read_split(folder):
    """A monolith split into a folder of parts (program/runbook/, program/checkpoints/), read whole: its parts in name
    order, byte for byte the original. A missing folder raises; an empty one is an error, not an empty document."""
    parts = sorted(p for p in Path(folder).iterdir() if p.suffix == ".md")
    if not parts:
        raise FileNotFoundError(f"no parts in {folder}")
    return "".join(p.read_text(encoding="utf-8", errors="replace") for p in parts)


def project_rows(items, folders):
    """The projects index rows: each project folder and each open work-queue item, joined by queue id."""
    queue = {}
    for item in items:
        if item['id'] in queue:
            raise ValueError(f'program/program_state.json: repeated queue id {item["id"]}')
        queue[item['id']] = item
    open_ids = {key for key, item in queue.items()
                if str(item['state']).lower() not in {'done', 'closed', 'cancelled', 'canceled'}}
    projects = []
    for key in sorted(folders | open_ids):
        item = queue.get(key, {})
        relation = 'folder and queue item' if key in folders and key in queue else (
            'no queue item' if key in folders else 'no folder')
        projects.append([key, item.get('title'), item.get('state'), relation])
    return projects
