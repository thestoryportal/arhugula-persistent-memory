# Producer changes for Codex MB — admission scope, D-ML-1

The shared schema-1 contract now accepts optional `run_started.purpose`, either
`"admission"` or `"experiment"`. `fold()` never marks an experiment step complete
for admission-only runs. Legacy streams with admission events and no started
stage are interpreted as admission-only; real stage events restore their
experiment scope. No producer file was edited by Codex ML.

Apply these exact replacements to the currently observed producer source.
Line numbers refer to the source inspected for the Astra dashboard fix.

## tools/mathlab_runtime.py:141 — constructor

Replace:

```python
    def __init__(self, run_dir, step, title, deadline_s, sink=emit, sample=available_gib, attach=False):
```

With:

```python
    def __init__(self, run_dir, step, title, deadline_s, sink=emit, sample=available_gib, attach=False, purpose="experiment"):
```

## tools/mathlab_runtime.py:149 — attachment to an experiment run

Replace:

```python
            require(len(starts) == 1 and starts[0]["step"] == step, "EVENTS", "one matching run_started required")
```

With:

```python
            require(len(starts) == 1 and starts[0]["step"] == step
                    and starts[0].get("purpose", "experiment") == "experiment",
                    "EVENTS", "one matching experiment run_started required")
```

This preserves legacy launcher streams and rejects an explicit admission receipt
as the identity of a dispatched experiment. The existing terminal-event rejection
remains necessary.

## tools/mathlab_runtime.py:156 — emit the discriminator

Replace:

```python
            self.event("run_started", step=step, title=title, deadline_ts=deadline.isoformat(), pid=os.getpid())
```

With:

```python
            self.event("run_started", step=step, title=title, deadline_ts=deadline.isoformat(), pid=os.getpid(), purpose=purpose)
```

## tools/mathlab_admit.py:112 — standalone receipt versus launcher-owned experiment

Replace:

```python
    run = R.Run(run_dir, args.step or (1 if args.kind == "harvest" else 2), "Check whether the lab can start", args.deadline_s)
```

With:

```python
    run = R.Run(run_dir, args.step or (1 if args.kind == "harvest" else 2), "Check whether the lab can start", args.deadline_s,
                purpose="admission" if own_run else "experiment")
```

Keep the existing `run_finished` PASS/INVALID admission receipt at line 132.
Its outcome describes the admission check. The discriminator prevents that PASS
from becoming Harvest/Reproduce PASS. A launcher-provided `--run-dir` keeps
experiment scope for the subsequently attached harvest or CPU stage.

## Producer verification to run after applying

Verify both standalone kinds emit `purpose="admission"`; successful admission
leaves all four folded steps `not started`. Verify launcher-owned admission
emits `purpose="experiment"`, and step PASS requires its experiment closeout.
Verify an explicit admission receipt cannot attach as an experiment. These are
producer fixtures; this memo grants no launch or measurement approval.

No producer replacements are needed for calibration outcomes or gate names:
`mathlab/core.py:337` already emits aggregate `PASS`/`FAIL`/`INVALID`; the shared
fold now preserves them. `tools/mathlab_harvest.py:425,478,483,485,491` and
`tools/mathlab_runtime.py:181–198` already emit the context, LAW#3, LAW#5,
observer-parity, budget and memory identifiers now interpreted by the fold.
Existing per-arm/layer tolerances stay producer-owned and appear from each
event's `bar`/`comparison`, without a parallel status file.
