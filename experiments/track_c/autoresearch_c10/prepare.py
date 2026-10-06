"""
Fixed constants, setup checks, runtime utilities and the evaluation for autoresearch on a model-editing experiment.
Not modified by the agent.

Usage:
    .venv/bin/python prepare.py            one-time setup check (engine fingerprint, harness hash, reference run, model load,
                              engine-parity gate); prints "Done! Ready to edit." when everything is in place
    .venv/bin/python prepare.py --score D  the scorer (run by evaluate, never by hand): scores the edits saved in run folder D

edit.py imports the runtime utilities and calls evaluate(apply_edit) at the end, as the fork's train.py calls evaluate_bpb.
evaluate applies the recipe to each arm, saves the changed weights, and hands them to the scorer, a fresh process that
loads the unedited model, applies the saved weights and measures. The scorer never runs edit.py's code.
"""

import os
import sys
import json
import time
import signal
import hashlib
import subprocess

# ---------------------------------------------------------------------------
# Constants (fixed, do not modify)
# ---------------------------------------------------------------------------

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAM_ROOT = "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a"   # engine, model cache, covariance caches, stimulus screens
PYTHON = f"{PROGRAM_ROOT}/.venv/bin/python"
HARNESS = f"{PROGRAM_ROOT}/experiments/track_c/c10e_bandknob.py"
HARNESS_SHA256 = "1f6be5811d7e58f3ebda16867a4a174b1cf24d47f9a2514cf9c3f9d29f18e695"
BASE_HPARAMS = f"{PROGRAM_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json"
REFERENCE_RUN = f"{PROGRAM_ROOT}/results/c10l_covgeom/run1_armB_identity.json"   # a past run whose controls must pass; checked at setup
COV_LAYERS = tuple(range(4, 13))   # MLP down_proj layers with a covariance cache on disk; other layers have none
SEED = 0                           # fixes the engine's sampled context templates, so runs are comparable
EDIT_BUDGET = 2700                 # seconds of wall clock for all of edit.py's own work: its top-level setup plus the three edits
RUN_TIMEOUT_MIN = 120              # a run past this is killed and treated as a crash (program.md)
SCORE_TIMEOUT_S = 3600             # hard limit on the scorer process
EDITABLE = ".mlp."                 # an edit may change MLP weights only (the feed-forward layers are the store being tested)

# Guards: every one must hold for a run to be kept. They protect the rest of the model and the controls.
GUARDS = {
    "A1": (">=", 68),              # single-token control arm, held-out reads /72
    "A2": (">=", 68),              # two-token control arm, held-out reads /72
    "L1_flips": ("<=", 1),         # 12 real countries whose top-1 capital turned into an edited value
    "frame_flips": ("<=", 2),      # 6 unedited fictional subjects in the same prompt frame that now emit an edited value
    "described_as": (">=", 85.0),  # % distribution kept on "<subject> is described as" for the 24 edited subjects
    "L3": (">=", 29),              # 30 unrelated real countries whose top-1 is unchanged
    "ppl_post": ("<=", 22.2),      # perplexity on 20 generic sentences after the edit
    "law5_ok": ("==", True),       # engine-parity gate of the harness's edit function
    "scope_ok": ("==", True),      # every changed tensor is an MLP weight
}

# The harness reads these at import; an inherited value would silently change the stimuli or the model.
_REFUSED_ENV = ("MODEL_ID", "MODEL_REV", "C10_PROJECTOR", "N_EDIT", "C10_SUBJECT_OFFSET", "C10_CTX_TEMPLATES",
                "C10_KEY_LOCUS", "C10_ARMS", "C10_RECIPES", "HP_CANDIDATE", "CANDIDATE_NAME", "RUN_LABEL")
for _k in _REFUSED_ENV:
    if _k in os.environ:
        raise SystemExit(f"refusing to run with inherited harness setting {_k}={os.environ[_k]!r}")
os.environ["LLMDB_ROOT"] = PROGRAM_ROOT   # the login shell may point it at another checkout

# The evaluation is the harness's own; refuse to run if the harness changed.
_h = hashlib.sha256(open(HARNESS, "rb").read()).hexdigest()
if _h != HARNESS_SHA256:
    raise SystemExit(f"fixed harness changed: {HARNESS} sha256 {_h} != {HARNESS_SHA256}")

# The held-out prompts and locality probes are evaluation data; an edit recipe that uses them is testing on its training set.
_EDIT_SRC = f"{HERE}/edit.py"
_FORBIDDEN = ("PTEST", "L1_PROMPTS", "L3_PROMPTS", "L1_COUNTRIES", "L3_COUNTRIES", "GENERIC", "FRAME_SUBJECTS", "eval_arm",
              "axes_pre", "axes_post", "locpct", "full_seq_match", "teacher_forced", "string_match", "sentence_nll", "GUARDS",
              "capital city is called", "its capital city is", "seat of government", "is described as")
if os.path.exists(_EDIT_SRC):
    _src = open(_EDIT_SRC).read()
    _hits = [w for w in _FORBIDDEN if w in _src]
    if _hits:
        raise SystemExit(f"edit.py references evaluation data or the metric: {_hits}")

# ---------------------------------------------------------------------------
# Runtime utilities (imported by edit.py)
# ---------------------------------------------------------------------------

import torch
torch.manual_seed(SEED)

sys.path.insert(0, f"{PROGRAM_ROOT}/experiments/track_c")
import c10e_bandknob as H   # loads Qwen/Qwen2.5-3B (pinned revision) in fp16 on MPS; puts the engine on sys.path; chdirs into the engine

from memit.memit_hparams import MEMITHyperParams
from memit.compute_z import compute_z, get_module_input_output_at_words
from memit.compute_ks import compute_ks
from memit.memit_main import get_cov, get_context_templates, upd_matrix_match_shape

model, tok, DEV = H.model, H.tok, H.DEV
CANON = H.CANON                    # the write prompt: "The capital of {} is the city of"
SUBJECTS = list(H.FICTION)         # 24 fictional countries
ARM_NAMES = ("A1_single", "A2_coherent2", "A7_coined_coined")
TARGET_ARM = "A7_coined_coined"    # the metric arm: two-word coined capitals
FRAME_SUBJECTS = ["Vorbanth", "Quillexa", "Tremnok", "Oskavel", "Blynthar", "Durmquist"]


def facts(arm):
    """The facts an edit must write for one arm: [(subject, value)], written with the CANON prompt."""
    return [(s, H.ARMS[arm][s]) for s in SUBJECTS]


def request(subject, value, prompt=CANON):
    """One engine request in the format compute_z / compute_ks expect."""
    return H.req(prompt, subject, value)


def load_hparams(**overrides):
    """The engine's hyperparameters for this model with overrides, e.g. load_hparams(layers=[4, 5, 6, 7, 8], v_num_grad_steps=25)."""
    d = json.load(open(BASE_HPARAMS))
    d.update(overrides)
    path = f"{HERE}/.hparams_{os.getpid()}.json"
    json.dump(d, open(path, "w"))
    hp = MEMITHyperParams.from_json(path)
    os.remove(path)
    return hp


def _weights():
    return dict(model.named_parameters())


# The unedited weights, captured before edit.py's own code runs. evaluate restores from these before every arm.
_BASE = {n: p.detach().clone() for n, p in _weights().items()}
_T_READY = time.time()

# ---------------------------------------------------------------------------
# Setup checks (run by the scorer before anything is measured, and by `python prepare.py`)
# ---------------------------------------------------------------------------


def _fingerprint():
    r = subprocess.run([PYTHON, f"{PROGRAM_ROOT}/tools/engine_fingerprint.py"], capture_output=True, text=True,
                       env={**os.environ, "LLMDB_ROOT": PROGRAM_ROOT})
    if r.returncode != 0:
        raise SystemExit(f"engine fingerprint FAIL:\n{r.stdout}{r.stderr}")
    return r.stdout.strip().splitlines()[0]


def _reference_ok():
    arms = json.load(open(REFERENCE_RUN))["recipes"]["baseline"]["arms"]
    if arms["A1_single"]["para_full_n"] < 68 or arms["A2_coherent2"]["para_full_n"] < 68:
        raise SystemExit(f"reference run {REFERENCE_RUN} fails its own controls")


def _law5():
    """Engine parity of the harness's edit function at the engine's defaults (layers 4-8). Independent of edit.py."""
    hp = MEMITHyperParams.from_json(BASE_HPARAMS)
    snap = H.snap_layers(hp)
    gate = H.run_law5(hp, H.compute_P(hp), snap)
    H.restore_layers(hp, snap)
    return gate


def setup_checks():
    fp = _fingerprint()
    _reference_ok()
    gate = _law5()
    templates = get_context_templates(model, tok)
    return {"fingerprint": fp, "law5": gate, "templates_sha": hashlib.sha256(json.dumps(templates).encode()).hexdigest()[:12]}

# ---------------------------------------------------------------------------
# Evaluation (DO NOT CHANGE — this is the fixed metric)
# ---------------------------------------------------------------------------


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
    """Names of parameter tensors that differ from the unedited weights."""
    return [n for n, p in _weights().items() if not torch.equal(p, _BASE[n])]


def evaluate(apply_edit):
    """apply_edit(facts) must edit `model` in place to write facts = [(subject, value)].
    It is called once per arm on the unedited model, within one shared budget (EDIT_BUDGET, counted from the moment
    edit.py's code started). The changed weights of each arm are saved and scored by a fresh process (prepare.py --score)."""
    commit = subprocess.run(["git", "rev-parse", "--short=7", "HEAD"], cwd=HERE, capture_output=True, text=True).stdout.strip() or "nocommit"
    run_dir = f"{HERE}/runs/{time.strftime('%Y%m%d-%H%M%S')}_{commit}"
    os.makedirs(run_dir, exist_ok=True)
    if _changed():
        raise SystemExit("edit.py changed the weights before evaluate: edits must happen inside apply_edit")
    signal.signal(signal.SIGALRM, _alarm)
    edit_seconds, manifest = {}, {}
    for arm in ARM_NAMES:
        _restore_base()
        left = int(EDIT_BUDGET - (time.time() - _T_READY))
        if left <= 0:
            raise SystemExit(f"over EDIT_BUDGET={EDIT_BUDGET}s before arm {arm}")
        t0 = time.time()
        signal.alarm(left)
        try:
            apply_edit(facts(arm))
        except _OverBudget:
            raise SystemExit(f"apply_edit exceeded EDIT_BUDGET={EDIT_BUDGET}s on arm {arm}")
        finally:
            signal.alarm(0)
        edit_seconds[arm] = round(time.time() - t0, 1)
        names = _changed()
        w = _weights()
        torch.save({n: w[n].detach().cpu().clone() for n in names}, f"{run_dir}/{arm}.pt")
        manifest[arm] = names
    _restore_base()
    json.dump({"commit": commit, "edit_seconds": edit_seconds, "setup_seconds": round(time.time() - _T_READY - sum(edit_seconds.values()), 1),
               "changed": manifest}, open(f"{run_dir}/edits.json", "w"), indent=1)
    r = subprocess.run([PYTHON, os.path.abspath(__file__), "--score", run_dir], env={**os.environ, "LLMDB_ROOT": PROGRAM_ROOT},
                       timeout=SCORE_TIMEOUT_S)
    if r.returncode != 0:
        raise SystemExit(f"scorer failed (exit {r.returncode})")


@torch.no_grad()
def _frame_probe(values):
    firsts = {H.tgt_ids(v)[0] for v in values}
    flips = 0
    for s in FRAME_SUBJECTS:
        ids = tok(CANON.format(s), return_tensors="pt").to(DEV)
        flips += int(model(**ids).logits[0, -1].argmax()) in firsts
    return flips


def _score(run_dir):
    """The scorer. Runs in its own process: the unedited model, the saved weights per arm, the harness's measurements.
    The setup gate edits the model (compute_z needs gradients), so it runs before gradients are switched off."""
    t_start = time.time()
    gates = setup_checks()
    if not gates["law5"]["ok"]:
        raise SystemExit("engine-parity gate NOT INERT: the instrument is broken")
    _measure(run_dir, t_start, gates)


@torch.no_grad()
def _measure(run_dir, t_start, gates):
    edits = json.load(open(f"{run_dir}/edits.json"))
    pre_axes = H.axes_pre()
    described = [f"{s} is described as" for s in SUBJECTS]
    pre_loc = {p: H.predict(p) for p in described}
    frame_pre = _frame_probe(H.ARMS[TARGET_ARM].values())
    w = _weights()
    arms, scope_ok = {}, True
    hashes = {}
    for arm in ARM_NAMES:
        path = f"{run_dir}/{arm}.pt"
        hashes[arm] = hashlib.sha256(open(path, "rb").read()).hexdigest()
        saved = torch.load(path, weights_only=True, map_location="cpu")
        if (not isinstance(saved, dict) or set(saved) != set(edits["changed"][arm])
                or any(not isinstance(t, torch.Tensor) or n not in w or t.shape != w[n].shape or t.dtype != w[n].dtype
                       or not bool(torch.isfinite(t).all()) for n, t in saved.items())):
            raise SystemExit(f"saved weights for {arm} do not match the model or the manifest (names, shapes, dtypes, finiteness)")
        scope_ok &= all(EDITABLE in n for n in saved)
        for n, t in saved.items():
            w[n].copy_(t.to(w[n].device, w[n].dtype))
        ev = H.eval_arm(H.ARMS[arm])
        ev["locality_described_as"] = H.locpct({p: H.predict(p) for p in described}, pre_loc, described)
        ev["locality_axes"] = H.axes_post(pre_axes, list(H.ARMS[arm].values()))
        ev["frame_flips"] = _frame_probe(H.ARMS[arm].values())
        ev["dw_total"] = round(sum(float((w[n].float() - _BASE[n].float()).norm()) for n in saved), 3)
        ev["changed_tensors"] = len(saved)
        arms[arm] = ev
        for n in saved:
            w[n].copy_(_BASE[n])

    a7 = arms[TARGET_ARM]
    ax = a7["locality_axes"]
    s = {
        "heldout_full": a7["para_full_n"], "canon": a7["canon_full_n"], "first_token": a7["para_first_n"],
        "A1": arms["A1_single"]["para_full_n"], "A2": arms["A2_coherent2"]["para_full_n"],
        "L1_flips": ax["L1_flipped_to_edited_value"], "frame_flips": a7["frame_flips"], "described_as": a7["locality_described_as"],
        "L3": ax["L3_top1_agree"], "ppl_post": ax["generic_ppl_post"], "law5_ok": gates["law5"]["ok"], "scope_ok": scope_ok,
        "dw_total": a7["dw_total"], "edit_seconds": round(sum(edits["edit_seconds"].values()) + edits["setup_seconds"], 1),
        "score_seconds": round(time.time() - t_start, 1),
    }
    ops = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b, "==": lambda a, b: a == b}
    failing = [g for g, (op, thr) in GUARDS.items() if not ops[op](s[g], thr)]
    s["guards"] = "ok" if not failing else "failed:" + ",".join(failing)
    json.dump({"summary": s, "gates": gates, "frame_pre_edit": frame_pre, "edits": edits, "saved_sha256": hashes, "arms": arms,
               "seed": SEED, "edit_budget": EDIT_BUDGET}, open(f"{run_dir}/score.json", "w"), indent=1, default=str)
    for arm in ARM_NAMES:
        os.remove(f"{run_dir}/{arm}.pt")   # the edit is reproducible from the commit; the weights are large

    print("---")
    for k in ("heldout_full", "canon", "first_token", "A1", "A2", "L1_flips", "frame_flips", "described_as", "L3", "ppl_post",
              "law5_ok", "scope_ok", "dw_total", "edit_seconds", "score_seconds", "guards"):
        v = s[k]
        print(f"{k + ':':15} {str(v).lower() if isinstance(v, bool) else v}", flush=True)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--score":
        _score(sys.argv[2])
    else:
        print(json.dumps(setup_checks(), indent=1, default=str))
        print("Done! Ready to edit.")
