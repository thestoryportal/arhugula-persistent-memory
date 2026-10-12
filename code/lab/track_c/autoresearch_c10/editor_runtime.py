"""Evaluation-free editor runtime. Only the trusted parent may dispatch it."""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import time

HERE = Path(__file__).resolve().parent
TRAIN = json.loads((HERE / 'train_facts.json').read_text())
PROGRAM_ROOT = TRAIN['program']
RUN_DIR = Path(os.environ['C10_RUN_DIR'])
os.environ['LLMDB_ROOT'] = PROGRAM_ROOT
os.environ['HF_HOME'] = str(Path(PROGRAM_ROOT) / 'hf_cache')
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
ENGINE_ROOT = str(Path(PROGRAM_ROOT) / 'memit_dry_run/memit')
sys.path.insert(0, ENGINE_ROOT)
os.chdir(ENGINE_ROOT)

import torch
torch.manual_seed(TRAIN['seed'])
from transformers import AutoModelForCausalLM, AutoTokenizer
from memit.memit_hparams import MEMITHyperParams
from util.device import resolve_device
DEV = resolve_device()
if DEV == 'cpu':
    raise SystemExit('INFRASTRUCTURE HALT: GPU unavailable')
# This path is never executed by the no-model probe fixture.
_preflight = (torch.ones(1, device=DEV) * 2).cpu().item()
if _preflight != 2:
    raise SystemExit('INFRASTRUCTURE HALT: GPU preflight')
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks
from memit.memit_main import get_cov, get_context_templates, upd_matrix_match_shape

tok = AutoTokenizer.from_pretrained(TRAIN['model_id'], revision=TRAIN['revision'], local_files_only=True)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
model = AutoModelForCausalLM.from_pretrained(TRAIN['model_id'], revision=TRAIN['revision'],
                                          torch_dtype=torch.float16, device_map=DEV,
                                          local_files_only=True).eval()
CANON = TRAIN['canon']
SUBJECTS = TRAIN['subjects']
ARMS = TRAIN['arms']
ARM_NAMES = tuple(ARMS)
TARGET_ARM = 'A7_coined_coined'
COV_LAYERS = tuple(TRAIN['cov_layers'])
EDIT_BUDGET = TRAIN['edit_budget']


def facts(arm):
    return [(s, ARMS[arm][s]) for s in SUBJECTS]


def request(subject, value, prompt=CANON):
    return {'prompt': prompt, 'subject': subject, 'target_new': {'str': ' ' + value}}


def load_hparams(**overrides):
    d = dict(TRAIN['hparams'])
    d.update(overrides)
    path = RUN_DIR / ('.hparams_' + str(os.getpid()) + '.json')
    path.write_text(json.dumps(d))
    try:
        return MEMITHyperParams.from_json(str(path))
    finally:
        path.unlink()


def _weights():
    return dict(model.named_parameters())


_BASE = {n: p.detach().clone() for n, p in _weights().items()}
_T_READY = time.time()


class _OverBudget(Exception):
    pass


def _alarm(signum, frame):
    raise _OverBudget()


@torch.no_grad()
def _restore_base():
    for n, p in _weights().items():
        p.copy_(_BASE[n])


@torch.no_grad()
def _changed():
    return [n for n, p in _weights().items() if not torch.equal(p, _BASE[n])]


def evaluate(apply_edit):
    if _changed():
        raise SystemExit('weights changed before evaluate')
    signal.signal(signal.SIGALRM, _alarm)
    seconds, changed = {}, {}
    for arm in ARM_NAMES:
        _restore_base()
        left = int(EDIT_BUDGET - (time.time() - _T_READY))
        if left <= 0:
            raise SystemExit('edit budget exhausted')
        t0 = time.time()
        signal.alarm(left)
        try:
            apply_edit(facts(arm))
        except _OverBudget:
            raise SystemExit('edit budget exhausted')
        finally:
            signal.alarm(0)
        seconds[arm] = round(time.time() - t0, 1)
        names = _changed()
        w = _weights()
        torch.save({n: w[n].detach().cpu().clone() for n in names}, str(RUN_DIR / (arm + '.pt')))
        changed[arm] = names
    _restore_base()
    (RUN_DIR / 'edits.json').write_text(json.dumps({
        'commit': 'nocommit', 'edit_seconds': seconds,
        'setup_seconds': round(time.time() - _T_READY - sum(seconds.values()), 1), 'changed': changed}, indent=1))
    # Terminal handoff: the parent, after this process exits, owns scoring.
    return None
