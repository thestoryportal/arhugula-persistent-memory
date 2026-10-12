"""Inert no-model runtime, installed only in a private program-built probe fence."""
import json
import os
from pathlib import Path

TRAIN = json.loads((Path(__file__).resolve().parent / 'train_facts.json').read_text())
CANON = TRAIN['canon']
SUBJECTS = TRAIN['subjects']
ARM_NAMES = tuple(TRAIN['arms'])
RUN_DIR = Path(os.environ['C10_RUN_DIR'])


def evaluate(apply_edit):
    changed, seconds = {}, {}
    for arm in ARM_NAMES:
        saved = apply_edit([(s, TRAIN['arms'][arm][s]) for s in SUBJECTS])
        changed[arm] = list(saved)
        seconds[arm] = 0.0
        (RUN_DIR / (arm + '.pt')).write_text(json.dumps(saved))
    (RUN_DIR / 'edits.json').write_text(json.dumps({'commit': 'nocommit', 'edit_seconds': seconds,
                                                  'setup_seconds': 0.0, 'changed': changed}))
