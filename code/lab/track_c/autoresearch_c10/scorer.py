"""Private scorer: the v12 setup and measurement functions are carried unchanged."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
FENCE, ANCHOR = HERE, sys.argv[1]
# Verify every trusted helper before importing it (including startup dependency code).
import json as _json
import hashlib as _hashlib
_mpath = FENCE / 'sealed/manifest.json'
if _hashlib.sha256(_mpath.read_bytes()).hexdigest() != ANCHOR:
    raise SystemExit('trusted manifest mismatch')
for _path, _sha in _json.loads(_mpath.read_text()).items():
    _h = _hashlib.sha256()
    with open(_path, 'rb') as _stream:
        for _block in iter(lambda: _stream.read(1024 * 1024), b''):
            _h.update(_block)
    if _h.hexdigest() != _sha:
        raise SystemExit('trusted closure mismatch')
sys.path.insert(0, str(HERE))
from v13_common import verify
CONFIG = verify(HERE, sys.argv[1])
sys.path.insert(0, CONFIG['site_packages'])
PROGRAM_ROOT = CONFIG['program']
PYTHON = CONFIG['python']
HARNESS = CONFIG['harness']
HARNESS_SHA256 = CONFIG['harness_sha256']
BASE_HPARAMS = CONFIG['hparams']
REFERENCE_RUN = str(HERE / 'sealed/reference_controls.json')
SEED = 0
EDIT_BUDGET = 2700
EDITABLE = '.mlp.'
ARM_NAMES = ('A1_single', 'A2_coherent2', 'A7_coined_coined')
TARGET_ARM = 'A7_coined_coined'
FRAME_SUBJECTS = ['Vorbanth', 'Quillexa', 'Tremnok', 'Oskavel', 'Blynthar', 'Durmquist']
os.environ['LLMDB_ROOT'] = PROGRAM_ROOT
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
if hashlib.sha256(Path(HARNESS).read_bytes()).hexdigest() != HARNESS_SHA256:
    raise SystemExit('fixed harness changed')
import torch
torch.manual_seed(SEED)
spec = importlib.util.spec_from_file_location('_sealed_c10_harness', HARNESS)
H = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = H
spec.loader.exec_module(H)
# The immutable harness sets HF_HUB_OFFLINE=0; the profile still denies network,
# and subsequent engine calls retain the offline environment.
os.environ['HF_HUB_OFFLINE'] = '1'
from memit.memit_hparams import MEMITHyperParams
from memit.memit_main import get_context_templates
model, tok, DEV = H.model, H.tok, H.DEV
CANON, SUBJECTS = H.CANON, list(H.FICTION)
_BASE = {n: p.detach().clone() for n, p in model.named_parameters()}

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

def _weights():
    return dict(model.named_parameters())


def _fingerprint():
    r = subprocess.run([PYTHON, f"{PROGRAM_ROOT}/code/memit/engine_fingerprint.py"], capture_output=True, text=True,
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


if __name__ == '__main__':
    _score(sys.argv[2])
