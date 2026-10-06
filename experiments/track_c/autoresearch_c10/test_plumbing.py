#!/usr/bin/env python3
"""Cheap plumbing tests for prepare.py / edit.py / launch.sh's equivalence gate. No GPU, no model: a stub harness with a tiny
model stands in for c10e_bandknob, so these test the wiring (refusals, budget, scope, manifest checks, guards, output),
not the science. The science-side equivalence is check_equivalence.py (real model).
Run: <program>/.venv/bin/python experiments/track_c/autoresearch_c10/test_plumbing.py
"""
import hashlib, io, json, os, re, shutil, subprocess, sys, tempfile, time, types, unittest
from contextlib import redirect_stdout

SRC = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
TMP = tempfile.mkdtemp(prefix="ar_c10_test_")
for f in ("prepare.py", "edit.py"):
    shutil.copy(f"{SRC}/{f}", f"{TMP}/{f}")

import torch
import torch.nn as nn


# ---------------------------------------------------------------- stub harness + engine
class _MLP(nn.Module):
    def __init__(self):
        super().__init__(); self.down_proj = nn.Linear(8, 8, bias=False)


class _Layer(nn.Module):
    def __init__(self):
        super().__init__(); self.mlp = _MLP()


class _Inner(nn.Module):
    def __init__(self):
        super().__init__(); self.embed_tokens = nn.Embedding(10, 8); self.layers = nn.ModuleList([_Layer() for _ in range(13)])


class _Tiny(nn.Module):
    def __init__(self):
        super().__init__(); self.model = _Inner()

    def forward(self, input_ids=None, **kw):
        return types.SimpleNamespace(logits=torch.zeros(1, 1, 10))


torch.manual_seed(0)
TINY = _Tiny()
for p in TINY.parameters():
    p.requires_grad_(False)


class _Enc(dict):
    def to(self, dev):
        return self


H = types.ModuleType("c10e_bandknob")
H.model, H.DEV = TINY, "cpu"
H.tok = lambda text, **kw: _Enc(input_ids=torch.zeros(1, 3, dtype=torch.long))
H.CANON = "The capital of {} is the city of"
H.PTEST = ["p1 {}", "p2 {}", "p3 {}"]
H.FICTION = [f"S{i}" for i in range(24)]
H.ARMS = {"A1_single": {s: "Paris" for s in H.FICTION}, "A2_coherent2": {s: "New York" for s in H.FICTION},
          "A7_coined_coined": {s: "Qorvex Zentra" for s in H.FICTION}}
H.L1_PROMPTS, H.L3_PROMPTS, H.GENERIC = ["l1"], ["l3"], ["g"]
H.req = lambda prompt, subj, targ: {"prompt": prompt, "subject": subj, "target_new": {"str": " " + targ}}
H.tgt_ids = lambda v: [5]
H.snap_layers = lambda hp: {}
H.restore_layers = lambda hp, snap: None
H.compute_P = lambda hp: []
H.run_law5 = lambda hp, P, snap: {"ok": True, "expr_delta": 0.0, "loc_delta": 0.0}
H.axes_pre = lambda: {}
H.predict = lambda p: {"id": 0}
H.locpct = lambda post, pre, prompts: 90.0
CONTROL = {"A1_single": 70, "A2_coherent2": 70}


def _eval_arm(vmap):
    arm = next(a for a, v in H.ARMS.items() if v is vmap)
    w = TINY.model.layers[8].mlp.down_proj.weight
    edited = int(round(float((w - BASE8).abs().sum()) > 0))
    n = CONTROL.get(arm, 10 + 30 * edited)    # A7: 10 unedited, 40 when layer 8 was edited
    return {"para_full_n": n, "canon_full_n": 1, "para_first_n": n, "para_string_n": n, "rows": []}


H.eval_arm = _eval_arm
H.axes_post = lambda pre, vals: {"L1_flipped_to_edited_value": 0, "L3_top1_agree": 30, "generic_ppl_post": 21.0}
BASE8 = TINY.model.layers[8].mlp.down_proj.weight.detach().clone()
sys.modules["c10e_bandknob"] = H


class _HP:
    layers = [4, 5, 6, 7, 8]; rewrite_module_tmp = "model.layers.{}.mlp.down_proj"; layer_module_tmp = "model.layers.{}"
    fact_token = "subject_last"; mom2_dataset = "wikipedia"; mom2_n_samples = 1; mom2_dtype = "float32"

    @staticmethod
    def from_json(path):
        hp = _HP(); d = json.load(open(path)); hp.layers = d.get("layers", hp.layers); return hp


def _mods(name, **attrs):
    m = types.ModuleType(name); m.__dict__.update(attrs); sys.modules[name] = m; return m


_mods("memit")
_mods("memit.memit_hparams", MEMITHyperParams=_HP)
_mods("memit.compute_z", compute_z=lambda model, tok, rq, hp, layer, ctx: torch.ones(8),
      get_module_input_output_at_words=lambda *a, **k: (None, torch.zeros(len(k["words"]), 8)))
_mods("memit.compute_ks", compute_ks=lambda model, tok, reqs, hp, layer, ctx: torch.randn(len(reqs), 8, generator=torch.Generator().manual_seed(layer)))
_g = torch.Generator().manual_seed(1)
_C = torch.randn(8, 8, generator=_g); _C = _C @ _C.T * 1e-4   # tiny eigenvalues -> a non-empty null space
_mods("memit.memit_main", get_cov=lambda *a, **k: _C.clone(), get_context_templates=lambda model, tok: [["{}"]],
      upd_matrix_match_shape=lambda upd, shape: upd if tuple(upd.shape) == tuple(shape) else upd.T)

sys.path.insert(0, TMP)
import prepare as PR   # noqa: E402  (stubs above are picked up)

_real_run = subprocess.run


def _run(args, *a, **k):   # route the scorer subprocess to an in-process call (the stub harness only exists here)
    if isinstance(args, list) and "--score" in args:
        buf = io.StringIO()
        with redirect_stdout(buf):
            PR._score(args[args.index("--score") + 1])
        _run.last_stdout = buf.getvalue()
        return subprocess.CompletedProcess(args, 0)
    return _real_run(args, *a, **k)


PR.subprocess.run = _run


def _summary(run_out):
    return dict(re.findall(r"^(\w+):\s+(\S+)$", run_out, flags=re.M))


def _latest_score():
    d = sorted(os.listdir(f"{TMP}/runs"))[-1]
    return f"{TMP}/runs/{d}", json.load(open(f"{TMP}/runs/{d}/score.json"))


# ---------------------------------------------------------------- tests
class ImportRefusals(unittest.TestCase):
    """prepare.py refuses before loading anything (subprocess import; the real harness is never reached)."""

    def _import(self, env_extra=None, edit_src=None, sha=None):
        d = tempfile.mkdtemp(prefix="ar_c10_ref_")
        src = open(f"{SRC}/prepare.py").read()
        if sha:
            src = src.replace(PR.HARNESS_SHA256, sha)
        open(f"{d}/prepare.py", "w").write(src)
        open(f"{d}/edit.py", "w").write(edit_src or "x = 1\n")
        env = {k: v for k, v in os.environ.items()}
        env.update(env_extra or {})
        r = _real_run([PY, "-c", "import prepare"], cwd=d, env=env, capture_output=True, text=True, timeout=120)
        return r.returncode, r.stdout + r.stderr

    def test_inherited_harness_setting(self):
        rc, out = self._import(env_extra={"MODEL_ID": "gpt2"})
        self.assertNotEqual(rc, 0); self.assertIn("refusing to run with inherited harness setting MODEL_ID", out)

    def test_harness_hash(self):
        rc, out = self._import(sha="0" * 64)
        self.assertNotEqual(rc, 0); self.assertIn("fixed harness changed", out)

    def test_forbidden_name(self):
        rc, out = self._import(edit_src="prompts = H.PTEST\n")
        self.assertNotEqual(rc, 0); self.assertIn("edit.py references evaluation data", out)

    def test_forbidden_literal_prompt(self):
        rc, out = self._import(edit_src="s = \"{}'s capital city is called\"\n")
        self.assertNotEqual(rc, 0); self.assertIn("capital city is called", out)


class Evaluate(unittest.TestCase):
    def setUp(self):
        PR._restore_base(); PR._T_READY = time.time(); PR.EDIT_BUDGET = 2700; CONTROL.update({"A1_single": 70, "A2_coherent2": 70})

    def _edit_layer(self, name):
        def apply_edit(facts):
            with torch.no_grad():
                dict(TINY.named_parameters())[name].add_(0.01)
        return apply_edit

    def test_scores_the_edit_and_guards_ok(self):
        PR.evaluate(self._edit_layer("model.layers.8.mlp.down_proj.weight"))
        s = _summary(_run.last_stdout)
        self.assertEqual(s["heldout_full"], "40"); self.assertEqual(s["guards"], "ok"); self.assertEqual(s["scope_ok"], "true")
        run_dir, score = _latest_score()
        self.assertEqual(set(score["saved_sha256"]), set(PR.ARM_NAMES))
        self.assertFalse([f for f in os.listdir(run_dir) if f.endswith(".pt")], "saved weights should be removed after scoring")
        self.assertTrue(all(torch.equal(p, PR._BASE[n]) for n, p in TINY.named_parameters()), "weights restored after evaluate")

    def test_unedited_scores_baseline(self):
        PR.evaluate(lambda facts: None)
        self.assertEqual(_summary(_run.last_stdout)["heldout_full"], "10")

    def test_scope_guard(self):
        PR.evaluate(self._edit_layer("model.embed_tokens.weight"))
        s = _summary(_run.last_stdout)
        self.assertEqual(s["scope_ok"], "false"); self.assertIn("scope_ok", s["guards"])

    def test_control_guard(self):
        CONTROL["A1_single"] = 50
        PR.evaluate(self._edit_layer("model.layers.8.mlp.down_proj.weight"))
        self.assertEqual(_summary(_run.last_stdout)["guards"], "failed:A1")

    def test_refuses_weights_changed_before_evaluate(self):
        with torch.no_grad():
            TINY.model.layers[5].mlp.down_proj.weight.add_(1.0)
        with self.assertRaises(SystemExit) as cm:
            PR.evaluate(lambda facts: None)
        self.assertIn("changed the weights before evaluate", str(cm.exception))
        PR._restore_base()

    def test_budget_counts_setup(self):
        PR.EDIT_BUDGET = 2; PR._T_READY = time.time() - 5   # top-level setup already used the budget
        with self.assertRaises(SystemExit) as cm:
            PR.evaluate(lambda facts: None)
        self.assertIn("over EDIT_BUDGET", str(cm.exception))

    def test_budget_alarm_inside_edit(self):
        PR.EDIT_BUDGET = 2
        with self.assertRaises(SystemExit) as cm:
            PR.evaluate(lambda facts: time.sleep(5))
        self.assertIn("exceeded EDIT_BUDGET", str(cm.exception))
        PR._restore_base()


class ScorerValidation(unittest.TestCase):
    def _run_dir(self, tensors_by_arm, manifest=None):
        d = tempfile.mkdtemp(prefix="ar_c10_score_")
        for arm in PR.ARM_NAMES:
            torch.save(tensors_by_arm.get(arm, {}), f"{d}/{arm}.pt")
        json.dump({"commit": "t", "edit_seconds": {a: 0.0 for a in PR.ARM_NAMES}, "setup_seconds": 0.0,
                   "changed": manifest or {a: list(tensors_by_arm.get(a, {})) for a in PR.ARM_NAMES}}, open(f"{d}/edits.json", "w"))
        return d

    def test_manifest_mismatch(self):
        n = "model.layers.8.mlp.down_proj.weight"
        d = self._run_dir({"A7_coined_coined": {n: PR._BASE[n].clone()}}, manifest={a: [] for a in PR.ARM_NAMES})
        with self.assertRaises(SystemExit):
            with redirect_stdout(io.StringIO()):
                PR._score(d)

    def test_non_finite(self):
        n = "model.layers.8.mlp.down_proj.weight"
        t = PR._BASE[n].clone(); t[0, 0] = float("nan")
        with self.assertRaises(SystemExit):
            with redirect_stdout(io.StringIO()):
                PR._score(self._run_dir({"A7_coined_coined": {n: t}}))

    def test_wrong_shape(self):
        n = "model.layers.8.mlp.down_proj.weight"
        with self.assertRaises(SystemExit):
            with redirect_stdout(io.StringIO()):
                PR._score(self._run_dir({"A7_coined_coined": {n: torch.zeros(3, 3)}}))


class EditBaseline(unittest.TestCase):
    def test_baseline_edit_runs_and_touches_only_its_layers(self):
        PR._restore_base(); PR._T_READY = time.time(); PR.EDIT_BUDGET = 2700
        import edit as E
        PR._restore_base()
        E.apply_edit(PR.facts("A7_coined_coined"))
        changed = PR._changed()
        self.assertEqual(changed, [f"model.layers.{l}.mlp.down_proj.weight" for l in E.LAYERS])
        PR._restore_base()


class LaunchGate(unittest.TestCase):
    def _gate(self, eq):
        sh = open(f"{SRC}/launch.sh").read()
        code = sh.split("<<'PYEOF'", 1)[1].split("\n", 1)[1].split("\nPYEOF", 1)[0]
        harness = PR.HARNESS
        r = _real_run([PY, "-", eq, SRC, harness], input=code, text=True, capture_output=True)
        return r.returncode

    def _eq(self, verdict="PASS", tamper=False):
        cur = {k: hashlib.sha256(open(p, "rb").read()).hexdigest()
               for k, p in (("prepare.py", f"{SRC}/prepare.py"), ("edit.py", f"{SRC}/edit.py"), ("harness", PR.HARNESS))}
        if tamper:
            cur["edit.py"] = "0" * 64
        p = f"{TMP}/eq.json"; json.dump({"verdict": verdict, "source_sha256": cur}, open(p, "w")); return p

    def test_pass_current(self):
        self.assertEqual(self._gate(self._eq()), 0)

    def test_fail_verdict(self):
        self.assertEqual(self._gate(self._eq(verdict="FAIL")), 1)

    def test_stale_source(self):
        self.assertEqual(self._gate(self._eq(tamper=True)), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
