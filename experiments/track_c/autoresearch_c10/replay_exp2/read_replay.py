#!/usr/bin/env python3
"""Frozen location-control patch and reader; no torch/model imports here."""
import ast
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import re
import shlex
import subprocess
import sys

BASE_COMMIT = "92acd0378d23f4935df9a8bccc0137b36695a40f"
PROGRAM_ROOT = Path("/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a")
SOURCE = Path("/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10")
MODEL_REV = "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
CONTEXT_SHA = "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330"
ARMS = ("A1_single", "A2_coherent2", "A7_coined_coined")
LAYERS = (4, 5, 6, 7, 8)
COLUMNS = dict(zip(ARMS, (144, 288, 792)))
COLLISION_HEADS = frozenset(("Drennik", "Vythorn", "Vorlex", "Kessivar", "Halquin", "Marsduq", "Glimsto", "Fluvane"))
CANON = "The capital of {} is the city of"
EXPECTED_EDIT_SHA256 = "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"
EXPECTED_DIFF_SHA256 = "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf"
FROZEN_ROWS = {'A1_single': [('Zorbland', 'Beirut', 1), ('Quaxil', 'Buenos', 1), ('Plurnak', 'Damascus', 1), ('Vythorn', 'Jerusalem', 1), ('Glimsto', 'Lisbon', 1), ('Drennik', 'Moscow', 1), ('Yastovel', 'Prague', 1), ('Crulpane', 'Santiago', 1), ('Mophgar', 'Stockholm', 1), ('Brinduun', 'Vienna', 1), ('Trannak', 'Ankara', 1), ('Skornwell', 'Bangkok', 1), ('Fluvane', 'Budapest', 1), ('Oxbarrow', 'Copenhagen', 1), ('Zephquin', 'Helsinki', 1), ('Lurmaxen', 'Lima', 1), ('Pradnoll', 'Mexico', 1), ('Kessivar', 'Paris', 1), ('Wombryne', 'Rome', 1), ('Halquin', 'Sofia', 1), ('Vorlex', 'Tunis', 1), ('Quenby', 'Amsterdam', 1), ('Marsduq', 'Baghdad', 1), ('Thelby', 'Berlin', 1)], 'A2_coherent2': [('Zorbland', 'Astana', 2), ('Quaxil', 'Bucharest', 2), ('Plurnak', 'Dhaka', 2), ('Vythorn', 'Harare', 2), ('Glimsto', 'Manama', 2), ('Drennik', 'Phnom', 2), ('Yastovel', 'Riga', 2), ('Crulpane', 'Tripoli', 2), ('Mophgar', 'Accra', 2), ('Brinduun', 'Amman', 2), ('Trannak', 'Bogota', 2), ('Skornwell', 'Dakar', 2), ('Fluvane', 'Hanoi', 2), ('Oxbarrow', 'Managua', 2), ('Zephquin', 'Muscat', 2), ('Lurmaxen', 'Rabat', 2), ('Pradnoll', 'Tirana', 2), ('Kessivar', 'Abuja', 2), ('Wombryne', 'Algiers', 2), ('Halquin', 'Belgrade', 2), ('Vorlex', 'Caracas', 2), ('Quenby', 'Doha', 2), ('Marsduq', 'Luanda', 2), ('Thelby', 'Maputo', 2)], 'A7_coined_coined': [('Zorbland', 'Vindex Vask', 4), ('Quaxil', 'Drennik Brakk', 5), ('Plurnak', 'Vythorn Stavik', 6), ('Vythorn', 'Vorlex Yornel', 5), ('Glimsto', 'Lurmax Spraxil', 6), ('Drennik', 'Kessivar Ulvenn', 6), ('Yastovel', 'Halquin Cindel', 5), ('Crulpane', 'Marsduq Drelth', 6), ('Mophgar', 'Glimsto Vask', 5), ('Brinduun', 'Brindu Brakk', 5), ('Trannak', 'Fluvane Stavik', 6), ('Skornwell', 'Yastov Yornel', 6), ('Fluvane', 'Vindex Spraxil', 5), ('Oxbarrow', 'Drennik Ulvenn', 6), ('Zephquin', 'Vythorn Cindel', 6), ('Lurmaxen', 'Vorlex Drelth', 5), ('Pradnoll', 'Lurmax Vask', 5), ('Kessivar', 'Kessivar Brakk', 5), ('Wombryne', 'Halquin Stavik', 5), ('Halquin', 'Marsduq Yornel', 6), ('Vorlex', 'Glimsto Spraxil', 6), ('Quenby', 'Brindu Ulvenn', 6), ('Marsduq', 'Fluvane Cindel', 6), ('Thelby', 'Yastov Drelth', 6)]}

IMPORT_LOG = '''import hashlib
import json
import os
import re
import sys

_REPLAY_EDIT_PATH = os.path.realpath(__file__)
with open(_REPLAY_EDIT_PATH, "rb") as _replay_file:
    _REPLAY_EDIT_SHA256 = hashlib.sha256(_replay_file.read()).hexdigest()

'''

SELECTOR_CODE = '''def select_common_positions(tokenizer, rq, template, fact_i, template_i, ids, tgt):
    """Frozen seven-word occurrence rule; the original input IDs stay authoritative."""
    if rq["prompt"] != "The capital of {} is the city of" or template.count("{}") != 1:
        raise ValueError("unexpected canonical prompt or context wrapper")
    prefix = template.format(rq["prompt"].format(rq["subject"]))
    encoded = tokenizer(prefix, return_offsets_mapping=True)
    if encoded["input_ids"] != ids:
        raise ValueError("offset mapping changed original prefix IDs")
    before, after = rq["prompt"].split("{}")
    lead = len(template.split("{}")[0])
    subject_span = [lead + len(before), lead + len(before) + len(rq["subject"])]
    spans = [[m.group(), lead + m.start(), lead + m.end()] for m in re.finditer(r"\\S+", before)]
    spans += [[m.group(), subject_span[1] + m.start(), subject_span[1] + m.end()] for m in re.finditer(r"\\S+", after)]
    candidates = []
    for word, word_a, word_b in spans:
        matches = []
        for idx, (a, b) in enumerate(encoded["offset_mapping"]):
            if a == b:
                continue
            piece = prefix[a:b]
            aa = a + len(piece) - len(piece.lstrip())
            bb = b - len(piece) + len(piece.rstrip())
            if (aa, bb) == (word_a, word_b) and piece.strip() == word:
                matches.append(idx)
        if len(matches) != 1:
            raise ValueError(f"common word must occupy one unambiguous token: {word!r} {matches}")
        candidates.append(matches[0])
    if [s[0] for s in spans] != ["The", "capital", "of", "is", "the", "city", "of"] or len(set(candidates)) != 7:
        raise ValueError("seven distinct canonical word positions required")
    m = len(tgt)
    if not 1 <= m <= 7:
        raise ValueError("target must have 1..7 tokens")
    indices = [candidates[(fact_i + template_i + j) % 7] for j in range(m)]
    if len(set(indices)) != m or any(not 0 <= k < len(ids) for k in indices):
        raise ValueError("control indices must be distinct prefix positions")
    for idx in indices:
        a, b = encoded["offset_mapping"][idx]
        if max(a, subject_span[0]) < min(b, subject_span[1]):
            raise ValueError("control index overlaps subject")
    return {"fact_i": fact_i, "template_i": template_i, "subject": rq["subject"],
            "target": rq["target_new"]["str"], "prefix": prefix, "prefix_ids": ids,
            "target_ids": tgt, "input_ids": ids + tgt, "offsets": [list(x) for x in encoded["offset_mapping"]],
            "subject_span": subject_span, "word_spans": spans, "candidates": candidates,
            "indices": indices, "value_indices": list(range(len(ids), len(ids) + m))}


'''

VALUE_KEYS_CODE = '''@torch.no_grad()
def value_keys(layer, requests, ctx):
    """Count-matched common-prefix keys and audit-only original value keys, from the same captured forwards."""
    grabbed, cols, real_cols, manifest = [], [], [], []
    hook = model.get_submodule(HP.rewrite_module_tmp.format(layer)).register_forward_hook(lambda m, inp, out: grabbed.append(inp[0][0]))
    try:
        for fact_i, rq in enumerate(requests):
            tgt = tok(rq["target_new"]["str"], add_special_tokens=False)["input_ids"]
            for template_i, t in enumerate([t for group in ctx for t in group]):
                ids = tok(t.format(rq["prompt"].format(rq["subject"])))["input_ids"]
                positions = select_common_positions(tok, rq, t, fact_i, template_i, ids, tgt)
                grabbed.clear()
                model(torch.tensor([ids + tgt], device=DEV))
                if len(grabbed) != 1 or grabbed[0].shape[0] != len(ids) + len(tgt):
                    raise ValueError("unexpected captured forward shape")
                original = grabbed[0][len(ids):].float().cpu()
                identity = grabbed[0][positions["value_indices"]].float().cpu()
                if not torch.equal(original, identity):
                    raise ValueError("suffix/explicit-gather primitive identity failed")
                control = grabbed[0][positions["indices"]].float().cpu()
                if control.shape != original.shape or not bool(torch.isfinite(control).all()) or not bool(torch.isfinite(original).all()):
                    raise ValueError("nonfinite or count-mismatched gathered keys")
                cols.append(control)
                real_cols.append(original)
                manifest.append(positions)
    finally:
        hook.remove()
    return torch.cat(cols).T, torch.cat(real_cols).T, manifest


'''

CONTEXT_LOG = '''    _replay_context_sha = hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
    print(f"executed_edit_py_sha256: {_REPLAY_EDIT_SHA256}", flush=True)
    print(f"edit_context_templates_sha256: {_replay_context_sha}", flush=True)
    if _replay_context_sha != "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330" or sum(map(len, ctx)) != 6:
        raise ValueError("edit-time contexts differ from the realized-list anchor")
    _replay_caller = sys._getframe(1).f_locals
    _replay_arm = _replay_caller["arm"]
    _replay_run_dir = os.path.realpath(_replay_caller["run_dir"])
    _replay_launch_path = os.environ["REPLAY_LAUNCH_PATH"]
    with open(_replay_launch_path, "rb") as _replay_file:
        _replay_launch_bytes = _replay_file.read()
    _replay_launch = json.loads(_replay_launch_bytes)
    if _replay_launch["invocation_id"] != os.environ["REPLAY_INVOCATION_ID"] or _replay_launch["edit_py_sha256"] != _REPLAY_EDIT_SHA256:
        raise ValueError("invocation or executed source disagrees with runner launch")
    _replay_manifest, _replay_layers = None, []
'''

LAYER_LOG = '''        if _replay_manifest is None:
            _replay_manifest = _replay_positions
        elif _replay_manifest != _replay_positions:
            raise ValueError("position manifest changed across layers")
        _replay_columns = {"A1_single": 144, "A2_coherent2": 288, "A7_coined_coined": 792}[_replay_arm]
        if list(Kp.shape) != [11008, _replay_columns] or Kp.shape != _replay_real.shape or not bool(torch.isfinite(upd).all()):
            raise ValueError("invalid preserve-matrix shape or nonfinite update")
        _replay_layers.append({"layer": layer, "control_columns": Kp.shape[1], "value_columns": _replay_real.shape[1],
            "key_dim": Kp.shape[0], "update_shape": list(upd.shape), "finite": True, "identity_equal": True,
            "position_sha256": hashlib.sha256(json.dumps(_replay_positions).encode()).hexdigest(),
            "control_sumsq": float(Kp.square().sum()), "value_sumsq": float(_replay_real.square().sum()),
            "control_PKp_fro": float((P[i] @ Kp).norm()), "value_PKp_fro": float((P[i] @ _replay_real).norm()),
            "update_fro_precast": float(upd.norm())})
'''

FINAL_LOG = '''    _replay_record = {"arm": _replay_arm, "invocation_id": _replay_launch["invocation_id"], "run_dir": _replay_run_dir,
        "executed_edit_py_sha256": _REPLAY_EDIT_SHA256, "launch_sha256": hashlib.sha256(_replay_launch_bytes).hexdigest(),
        "edit_context_templates_sha256": _replay_context_sha, "edit_context_templates": ctx,
        "Kp_source": "common_canonical_prefix", "preserve_weight": PRESERVE_WEIGHT,
        "positions": _replay_manifest, "layers": _replay_layers}
    with open(os.path.join(_replay_run_dir, "replay_provenance.jsonl"), "a") as _replay_file:
        _replay_file.write(json.dumps(_replay_record, allow_nan=False) + "\\n")
'''


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def sha_json(value):
    return hashlib.sha256(json.dumps(value).encode()).hexdigest()


def parse_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"nonfinite JSON number: {x}")))


def load_json(path):
    return parse_json(Path(path).read_text())


def git(dest, *args):
    r = subprocess.run(["git", "-C", str(dest), *args], check=True, capture_output=True, text=True)
    return r.stdout


def pinned_constants(dest):
    tree = ast.parse(git(dest, "show", f"{BASE_COMMIT}:prepare.py"))
    wanted = {"PROGRAM_ROOT", "PYTHON", "HARNESS_SHA256", "_REFUSED_ENV"}
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in wanted and isinstance(node.value, (ast.Constant, ast.Tuple)):
                result[name] = ast.literal_eval(node.value)
    require(Path(result["PROGRAM_ROOT"]) == PROGRAM_ROOT, "pinned program root changed")
    return result


def expected_edit(source):
    replacements = [
        ("import torch\n\n", IMPORT_LOG + "import torch\n\n"),
        ("PRESERVE_WEIGHT = 1.0       # weight of the keys at the value-token positions in the solve (the write must not fire there)",
         "PRESERVE_WEIGHT = 1.0       # coefficient of count-matched common-canonical-prefix keys"),
        (source[source.index("@torch.no_grad()\ndef value_keys"):source.index("def apply_edit(facts):")], SELECTOR_CODE + VALUE_KEYS_CODE),
        ("    ctx = get_context_templates(model, tok)\n", "    ctx = get_context_templates(model, tok)\n" + CONTEXT_LOG),
        ("        Kp = value_keys(layer, requests, ctx)                            # keys at the value tokens, one column per (fact, template, token)",
         "        Kp, _replay_real, _replay_positions = value_keys(layer, requests, ctx)"),
        ("        cos = (Kf / Kf.norm(dim=0)).T @ (Kp / Kp.norm(dim=0))\n", LAYER_LOG + "        cos = (Kf / Kf.norm(dim=0)).T @ (Kp / Kp.norm(dim=0))\n"),
        ("subject/value key overlap max", "Kp_source=common_canonical_prefix subject/preserve key overlap max"),
        ('    print(f"unrealized residual fraction mean {left.mean():.3f} max {left.max():.3f}", flush=True)\n',
         '    print(f"unrealized residual fraction mean {left.mean():.3f} max {left.max():.3f}", flush=True)\n' + FINAL_LOG),
    ]
    for old, new in replacements:
        require(source.count(old) == 1, f"nonunique pinned patch anchor: {old[:100]!r}")
        source = source.replace(old, new, 1)
    return source


def inspect_replay(dest):
    dest = Path(dest).resolve(strict=True)
    require(git(dest, "rev-parse", "HEAD").strip() == BASE_COMMIT, "wrong pinned HEAD")
    require(Path(git(dest, "rev-parse", "--absolute-git-dir").strip()).resolve() == dest / ".git", "standalone clone required")
    require(not (dest / ".git/objects/info/alternates").exists(), "borrowed Git objects forbidden")
    require((dest / ".git/HEAD").read_text().strip() == BASE_COMMIT, "detached HEAD required")
    tracked = git(dest, "ls-tree", "-r", "--name-only", BASE_COMMIT).splitlines()
    for name in tracked:
        require(not (dest / name).is_symlink(), f"tracked source became a symlink: {name}")
        expected = expected_edit(git(dest, "show", f"{BASE_COMMIT}:{name}")) if name == "edit.py" else git(dest, "show", f"{BASE_COMMIT}:{name}")
        require((dest / name).read_bytes() == expected.encode(), f"unpermitted tracked-file change: {name}")
    require(not git(dest, "diff", "--cached", "--name-only", BASE_COMMIT).strip(), "staged changes forbidden")
    require(git(dest, "diff", "--name-only", BASE_COMMIT).splitlines() == ["edit.py"], "only edit.py may differ")
    diff = git(dest, "-c", "core.abbrev=7", "diff", "--no-ext-diff", "--no-textconv", "--no-color", "--no-renames", "--diff-algorithm=myers", "--no-indent-heuristic", "--src-prefix=a/", "--dst-prefix=b/", "--unified=3", BASE_COMMIT, "--", "edit.py")
    edit_sha, diff_sha = sha_file(dest / "edit.py"), hashlib.sha256(diff.encode()).hexdigest()
    require(edit_sha == EXPECTED_EDIT_SHA256, "patched edit.py hash differs from build freeze")
    require(diff_sha == EXPECTED_DIFF_SHA256, "diff hash differs from build freeze")
    pinned_constants(dest)
    return {"base_commit": BASE_COMMIT, "dest": str(dest), "edit_py_sha256": edit_sha, "diff_sha256": diff_sha, "diff": diff}


def fidelity_inputs(dest):
    """Enumerate the complete pinned input set without importing the engine."""
    dest = Path(dest).resolve()
    constants = pinned_constants(dest)
    require(sha_file(PROGRAM_ROOT / "experiments/track_c/c10e_bandknob.py") == constants["HARNESS_SHA256"], "fixed program harness hash changed")
    require(sha_file(dest / "c10e_bandknob.py") == constants["HARNESS_SHA256"], "pinned harness copy mismatch")
    engine = PROGRAM_ROOT / "memit_dry_run/memit"
    snapshot = PROGRAM_ROOT / f"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/{MODEL_REV}"
    required = [PROGRAM_ROOT / "configs/hparams/qwen25_3b_memit_hparams.json",
                PROGRAM_ROOT / "configs/screens/g6_screen_qwen3b.json", PROGRAM_ROOT / "configs/screens/g6_screen_qwen3b_v2.json",
                PROGRAM_ROOT / "experiments/track_c/c10e_bandknob.py", PROGRAM_ROOT / "tools/engine_fingerprint.py",
                SOURCE.parent / "autoresearch_fence_c10/reference_controls.json", engine / "globals.yml",
                PROGRAM_ROOT / ".venv/pyvenv.cfg", Path(sys.executable).resolve()]
    required += sorted(engine.rglob("*.py"))
    for name in ("config.json", "tokenizer.json", "tokenizer_config.json", "generation_config.json", "merges.txt", "vocab.json", "model.safetensors.index.json"):
        required.append(snapshot / name)
    index = load_json(snapshot / "model.safetensors.index.json")
    required += [snapshot / name for name in sorted(set(index["weight_map"].values()))]
    required += [PROGRAM_ROOT / f"covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.{layer}.mlp.down_proj_float32_mom2_t100_100000.npz" for layer in LAYERS]
    return required


def fidelity_manifest(dest):
    """Byte identities, not mtimes; importing package metadata does not import torch."""
    files = {str(p): {"resolved_path": str(p.resolve(strict=True)), "sha256": sha_file(p)} for p in fidelity_inputs(dest)}
    packages = {name: importlib.metadata.version(name) for name in ("torch", "transformers", "tokenizers", "numpy", "safetensors", "accelerate")}
    require(packages["transformers"] == "4.51.0", "transformers pin changed")
    numeric_env = {key: os.environ.get(key) for key in ("LLMDB_DEVICE", "PYTORCH_MPS_FAST_MATH", "PYTORCH_ENABLE_MPS_FALLBACK", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")}
    return {"interpreter": str(Path(sys.executable).resolve()), "python_version": sys.version,
            "venv": str(Path(sys.prefix).resolve()), "packages": packages, "os": platform.platform(),
            "model_id": "Qwen/Qwen2.5-3B", "model_revision": MODEL_REV, "tokenizer_revision": MODEL_REV, "numeric_env": numeric_env, "files": files}


MODEL_PROCESS = re.compile(r"(?:^|[/\s])(?:python(?:\d+(?:\.\d+)*)?|ipykernel|jupyter[^\s/]*|ollama|safe-mode)(?=$|[\s/])|(?:^|[/\s])(?:edit\.py|prepare\.py|check_equivalence\.py|c10[^\s/]*)(?=$|\s)", re.I)


def process_check(phase, child_pid=None, dest=None, previously_owned=()):
    """Scan every process; exemptions are PID ancestry, never script-name allowlists."""
    r = subprocess.run(["ps", "-Aww", "-o", "pid=,ppid=,lstart=,command="], check=True, capture_output=True, text=True)
    require(bool(r.stdout.strip()), "empty full-process probe")
    rows = {}
    for line in r.stdout.splitlines():
        fields = line.split(None, 7)
        require(len(fields) == 8, f"malformed ps row: {line!r}")
        pid, ppid = int(fields[0]), int(fields[1])
        require(pid not in rows, "duplicate ps PID")
        rows[pid] = {"pid": pid, "ppid": ppid, "start": " ".join(fields[2:7]), "command": fields[7]}
    own, cursor = set(), os.getpid()
    require(cursor in rows, "runner missing from full process probe")
    while cursor in rows and cursor not in own:
        own.add(cursor)
        cursor = rows[cursor]["ppid"]
    descendants = set()
    for old in previously_owned:
        now = rows.get(old["pid"])
        if now is not None:
            require(now["start"] == old["start"] and now["command"] == old["command"], "owned editor/scorer PID identity changed")
            descendants.add(old["pid"])
    if child_pid is not None and child_pid in rows:
        require(rows[child_pid]["ppid"] == os.getpid(), "recorded editor PID is not runner-owned")
        descendants.add(child_pid)
        for pid, row in rows.items():
            if row["ppid"] != child_pid:
                continue
            prefix = f"{PROGRAM_ROOT / '.venv/bin/python'} {Path(dest) / 'prepare.py'} --score "
            command = row["command"]
            if command.startswith(prefix):
                run_path = Path(command[len(prefix):])
                if run_path.parent == Path(dest) / "runs" and re.fullmatch(r"[0-9]{8}-[0-9]{6}_92acd03", run_path.name):
                    descendants.add(pid)
        scorer_pids = descendants - {child_pid}
        helper_argv = [str(PROGRAM_ROOT / ".venv/bin/python"), str(PROGRAM_ROOT / "tools/engine_fingerprint.py")]
        for pid, row in rows.items():
            if row["ppid"] in scorer_pids and shlex.split(row["command"]) == helper_argv:
                descendants.add(pid)
    matches = [row for row in rows.values() if MODEL_PROCESS.search(row["command"])]
    foreign = [row for row in matches if row["pid"] not in own | descendants]
    return {"phase": phase, "probe_exit": r.returncode, "process_count": len(rows), "runner_pid": os.getpid(),
            "own_chain": sorted(own), "child_pid": child_pid, "owned_children": [rows[p] for p in sorted(descendants)],
            "matches": matches, "foreign": foreign, "ok": not foreign}


def primary_label(count):
    require(type(count) is int and 0 <= count <= 72, "H must be an integer in [0,72]")
    return "NO-GAIN-WITHOUT-VALUE-POSITIONS" if count <= 7 else "PARTIAL-GAIN" if count < 18 else "FULL-GAIN-WITHOUT-VALUE-POSITIONS"


def secondary_label(count):
    require(type(count) is int and 0 <= count <= 48, "C must be an integer in [0,48]")
    return "NO-COLLISION-RECOVERY" if count == 0 else "PARTIAL-COLLISION-RECOVERY" if count < 13 else "FULL-COLLISION-RECOVERY"


def integer(value, low, high):
    return type(value) is int and low <= value <= high


def number(value, low=0, high=math.inf):
    try:
        return type(value) in (int, float) and math.isfinite(value) and low <= value <= high
    except OverflowError:
        return False


def digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def cached_tokenizer():
    from tokenizers import Tokenizer
    return Tokenizer.from_file(str(PROGRAM_ROOT / f"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/{MODEL_REV}/tokenizer.json"))


def validate_positions(record, tokenizer=None):
    tokenizer = cached_tokenizer() if tokenizer is None else tokenizer
    rows, ctx = record["positions"], record["edit_context_templates"]
    templates = [t for group in ctx for t in group]
    require(len(rows) == 144, "144 position records required per arm")
    facts = FROZEN_ROWS[record["arm"]]
    for ordinal, row in enumerate(rows):
        f, q = divmod(ordinal, 6)
        subject, value, m = facts[f]
        require(row["fact_i"] == f and row["template_i"] == q, "manifest fact/template order mismatch")
        require(row["subject"] == subject and row["target"] == " " + value, "manifest request mismatch")
        prefix = templates[q].format(CANON.format(subject))
        require(row["prefix"] == prefix, "manifest prefix mismatch")
        ids, tgt, offsets = row["prefix_ids"], row["target_ids"], row["offsets"]
        require(isinstance(ids, list) and ids and isinstance(tgt, list) and len(tgt) == m, "manifest token dimensions mismatch")
        require(all(integer(x, 0, 151935) for x in ids + tgt) and row["input_ids"] == ids + tgt, "manifest original input IDs mismatch")
        original = tokenizer.encode(prefix, add_special_tokens=True)
        target = tokenizer.encode(" " + value, add_special_tokens=False)
        require(ids == original.ids and tgt == target.ids and offsets == [list(x) for x in original.offsets], "manifest IDs/offsets differ from the pinned cached tokenizer")
        require(isinstance(offsets, list) and len(offsets) == len(ids), "offset dimensions mismatch")
        for pair in offsets:
            require(isinstance(pair, list) and len(pair) == 2 and all(integer(x, 0, len(prefix)) for x in pair) and pair[0] <= pair[1], "invalid tokenizer offset")
        before, after = CANON.split("{}")
        lead = len(templates[q].split("{}")[0])
        subject_span = [lead + len(before), lead + len(before) + len(subject)]
        spans = [[x.group(), lead + x.start(), lead + x.end()] for x in re.finditer(r"\S+", before)]
        spans += [[x.group(), subject_span[1] + x.start(), subject_span[1] + x.end()] for x in re.finditer(r"\S+", after)]
        require(row["word_spans"] == spans and row["subject_span"] == subject_span, "canonical word/subject spans mismatch")
        candidates = []
        for word, start, end in spans:
            matches = []
            for idx, (a, b) in enumerate(offsets):
                piece = prefix[a:b]
                aa, bb = a + len(piece) - len(piece.lstrip()), b - len(piece) + len(piece.rstrip())
                if a != b and (aa, bb) == (start, end) and piece.strip() == word:
                    matches.append(idx)
            require(len(matches) == 1, "ambiguous or missing candidate token")
            candidates.append(matches[0])
        require(row["candidates"] == candidates and all(type(x) is int for x in row["candidates"]) and len(set(candidates)) == 7, "seven candidate indices mismatch")
        indices = [candidates[(f + q + j) % 7] for j in range(m)]
        require(row["indices"] == indices and all(type(x) is int for x in row["indices"]) and len(set(indices)) == m, "cyclic control positions mismatch")
        require(row["value_indices"] == list(range(len(ids), len(ids) + m)), "original value range mismatch")
        for idx in indices:
            a, b = offsets[idx]
            require(not (max(a, subject_span[0]) < min(b, subject_span[1])), "selected subject token")
    require(sum(len(row["indices"]) for row in rows) == COLUMNS[record["arm"]], "arm column count mismatch")
    layers = record["layers"]
    require([x["layer"] for x in layers] == list(LAYERS), "layer record order/count mismatch")
    for layer in layers:
        require(layer["control_columns"] == layer["value_columns"] == COLUMNS[record["arm"]], "per-layer column count mismatch")
        require(layer["key_dim"] == 11008 and layer["update_shape"] == [2048, 11008], "key/update dimensions mismatch")
        require(layer["finite"] is True and layer["identity_equal"] is True, "nonfinite data or gather primitive identity failure")
        require(layer["position_sha256"] == sha_json(rows), "position manifest differs across layers")
        require(all(number(layer[x]) for x in ("control_sumsq", "value_sumsq", "control_PKp_fro", "value_PKp_fro", "update_fro_precast")), "missing/nonfinite per-layer norms")
    require(record["Kp_source"] == "common_canonical_prefix" and type(record["preserve_weight"]) is float and record["preserve_weight"] == 1.0, "wrong preserve source/coefficient")
    return {"arm": record["arm"], "pairs": len(rows), "columns_per_layer": COLUMNS[record["arm"]], "identity_equal": [x["identity_equal"] for x in layers], "position_sha256": sha_json(rows), "layers": layers}


def validate_score(score):
    require(isinstance(score, dict), "score must be an object")
    summary, arms, edits, gates = score["summary"], score["arms"], score["edits"], score["gates"]
    require(isinstance(summary, dict) and set(arms) == set(ARMS), "exactly three registered score arms required")
    for key, high in (("heldout_full", 72), ("canon", 24), ("first_token", 72), ("A1", 72), ("A2", 72), ("L1_flips", 12), ("frame_flips", 6), ("L3", 30)):
        require(integer(summary[key], 0, high), f"invalid summary count: {key}")
    for key, high in (("described_as", 100), ("ppl_post", math.inf), ("dw_total", math.inf), ("edit_seconds", math.inf), ("score_seconds", math.inf)):
        require(number(summary[key], high=high), f"missing/nonfinite summary number: {key}")
    require(type(summary["law5_ok"]) is bool and type(summary["scope_ok"]) is bool and isinstance(summary["guards"], str), "malformed gate/guard summary")
    require(type(gates["law5"]["ok"]) is bool and all(number(gates["law5"][x]) for x in ("expr_delta", "loc_delta")), "malformed LAW#5 result")
    require(isinstance(gates["fingerprint"], str) and gates["fingerprint"], "missing scorer engine fingerprint")
    require(set(edits["changed"]) == set(ARMS) and set(edits["edit_seconds"]) == set(ARMS), "edit arm set mismatch")
    require(number(edits["setup_seconds"]) and all(number(x) for x in edits["edit_seconds"].values()), "invalid edit timings")
    allowed = {f"model.layers.{layer}.mlp.down_proj.weight" for layer in LAYERS}
    require(set(score["saved_sha256"]) == set(ARMS) and all(digest(x) for x in score["saved_sha256"].values()), "missing/malformed saved-weight hashes")
    for arm in ARMS:
        data, facts = arms[arm], FROZEN_ROWS[arm]
        names = edits["changed"][arm]
        require(isinstance(names, list) and names and len(set(names)) == len(names) and set(names) <= allowed, f"illegal changed-name set: {arm}")
        require(integer(data["changed_tensors"], 1, 5) and data["changed_tensors"] == len(names), "changed tensor count mismatch")
        require(number(data["dw_total"]), "missing/nonfinite arm update norm")
        rows = data["rows"]
        require(isinstance(rows, list) and len(rows) == 24, f"24 registered rows required: {arm}")
        for row, (subject, value, ntok) in zip(rows, facts):
            require(isinstance(row, dict) and isinstance(row["val"], str) and row["val"].strip(), "empty/malformed value")
            require((row["subj"], row["val"], row["ntok"]) == (subject, value, ntok) and type(row["ntok"]) is int, "registered subject/value/token count mismatch")
            for key in ("para_full_hits", "para_first_hits", "para_string_hits"):
                require(isinstance(row[key], list) and len(row[key]) == 3 and all(type(x) is bool for x in row[key]), f"three boolean hits required: {key}")
            require(type(row["canon_full"]) is bool and type(row["canon_first"]) is bool, "boolean canonical hits required")
            require(not row["canon_full"] or row["canon_first"], "canonical full hit without first-token hit")
            require(all(not full or first for full, first in zip(row["para_full_hits"], row["para_first_hits"])), "full hit without first-token hit")
            require(integer(row["tf_total"], 0, 18) and row["tf_total"] == 3 * (ntok - 1) and integer(row["tf_correct"], 0, row["tf_total"]), "invalid teacher-forced continuation dimensions")
        for field, actual, high in (("para_full_n", sum(sum(r["para_full_hits"]) for r in rows), 72), ("para_first_n", sum(sum(r["para_first_hits"]) for r in rows), 72), ("canon_full_n", sum(r["canon_full"] for r in rows), 24), ("canon_n", 24, 24), ("para_n", 72, 72)):
            require(integer(data[field], 0, high) and data[field] == actual, f"arm count/vector mismatch: {arm}.{field}")
    a7 = arms[ARMS[2]]
    for key, actual in (("heldout_full", a7["para_full_n"]), ("canon", a7["canon_full_n"]), ("first_token", a7["para_first_n"]), ("A1", arms[ARMS[0]]["para_full_n"]), ("A2", arms[ARMS[1]]["para_full_n"]), ("dw_total", a7["dw_total"]), ("frame_flips", a7["frame_flips"]), ("described_as", a7["locality_described_as"])):
        require(summary[key] == actual, f"summary/arm mismatch: {key}")
    for key, field in (("L1_flips", "L1_flipped_to_edited_value"), ("L3", "L3_top1_agree"), ("ppl_post", "generic_ppl_post")):
        require(summary[key] == a7["locality_axes"][field], f"summary/locality mismatch: {key}")
    collision = [row for row in a7["rows"] if row["val"].split()[0] in COLLISION_HEADS]
    other = [row for row in a7["rows"] if row["val"].split()[0] not in COLLISION_HEADS]
    require((len(collision), len(other)) == (16, 8), "wrong 16/8 collision partition")
    c, o = sum(sum(r["para_full_hits"]) for r in collision), sum(sum(r["para_full_hits"]) for r in other)
    require(integer(c, 0, 48) and integer(o, 0, 24) and summary["heldout_full"] == c + o, "H != C + O")
    return summary, c, o


def read_score(score_path, receipt_path):
    failures = []
    def check(name, operation, summarize=lambda value: value):
        try:
            value = operation()
            ok = True
        except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, ImportError, OverflowError, RecursionError, subprocess.SubprocessError) as exc:
            ok, value = False, str(exc)
        print(f"VALIDITY {name}: {'PASS' if ok else 'FAIL'} value={json.dumps(summarize(value) if ok else value, sort_keys=True, allow_nan=False)}")
        if not ok:
            failures.append(name)
        return value if ok else None

    score = check("score_json", lambda: load_json(score_path), lambda s: {"path": str(score_path), "keys": list(s)})
    receipt = check("receipt_json", lambda: load_json(receipt_path), lambda r: {"path": str(receipt_path), "invocation_id": r.get("invocation_id")})
    scored = check("registered_schema_vectors", lambda: validate_score(score)) if score is not None else None
    summary, c, o = scored if scored is not None else (None, None, None)

    def test_mode():
        synthetic = score.get("synthetic_fixture", False) or receipt.get("synthetic_fixture", False)
        enabled = os.environ.get("REPLAY_READER_SELFTEST") == "1"
        require(not synthetic or (enabled and Path("/tmp").resolve() in score_path.parents and Path("/tmp").resolve() in receipt_path.parents), "synthetic fixture forbidden for live acceptance")
        require(not enabled or synthetic, "self-test mode requires an explicitly synthetic fixture")
        return {"synthetic_fixture": bool(synthetic), "selftest": enabled}

    if receipt is not None and score is not None:
        mode = check("live_or_explicit_tmp_selftest", test_mode)
        audit = check("frozen_checkout_source_diff", lambda: inspect_replay(receipt["dest"]), lambda a: {k: v for k, v in a.items() if k != "diff"})
        def association():
            dest, run_dir = Path(receipt["dest"]).resolve(), Path(receipt["run_dir"]).resolve()
            require(receipt_path == dest / "runner_receipt.json" and score_path == Path(receipt["score_path"]) == run_dir / "score.json", "receipt/score paths not canonical or not associated")
            require(run_dir.parent == dest / "runs" and not run_dir.is_symlink() and run_dir.is_dir(), "run directory outside standalone clone")
            require(list((dest / "runs").iterdir()) == [run_dir], "exactly one fresh run directory required")
            require(list(dest.glob("runs/*/score.json")) == [score_path], "exactly one score required")
            require(receipt["child_exit"] == 0 and type(receipt["child_exit"]) is int and receipt["failures"] == [], "failed child or runner gate")
            require(receipt["score_sha256"] == sha_file(score_path) and receipt["saved_sha256"] == score["saved_sha256"], "score or saved-weight hash association failed")
            launch = load_json(dest / "replay_launch.json")
            require(launch == receipt["launch"] and launch["initial_runs"] == [], "launch association or fresh-start assertion failed")
            require(re.fullmatch(r"[0-9a-f]{32}", receipt["invocation_id"]) is not None and receipt["invocation_id"] == launch["invocation_id"], "invalid/mismatched invocation id")
            require(launch["dest"] == str(dest) and launch["program_root"] == str(PROGRAM_ROOT) and launch["context_sha256"] == CONTEXT_SHA, "launch paths/context mismatch")
            require(launch["child_pid"] == receipt["child_pid"] and integer(receipt["child_pid"], 1, 2**31), "child PID not bound to launch")
            require(audit is not None and all(receipt[key] == launch[key] == audit[key] for key in ("base_commit", "edit_py_sha256", "diff_sha256")), "source/diff/commit association failed")
            return {"invocation_id": receipt["invocation_id"], "score_path": str(score_path), "score_sha256": receipt["score_sha256"], "child_pid": receipt["child_pid"], "child_exit": receipt["child_exit"], "saved_sha256": receipt["saved_sha256"]}
        check("fresh_invocation_score_receipt", association)

        def fingerprint():
            fp = receipt["engine_fingerprint"]
            tree = ast.parse((PROGRAM_ROOT / "tools/engine_fingerprint.py").read_text())
            constants = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("EXPECTED_SHA256", "EXPECTED_COV_CPU_SITES")}
            main = PROGRAM_ROOT / "memit_dry_run/memit/memit/memit_main.py"
            require(fp["exit"] == 0 and fp["LLMDB_ROOT"] == str(PROGRAM_ROOT) and fp["interpreter"] == str(PROGRAM_ROOT / ".venv/bin/python"), "fingerprint did not use pinned interpreter/root or failed")
            lines = fp["stdout"].strip().splitlines()
            require(len(lines) == 3 and lines[0] == f"engine fingerprint PASS: {main}" and f"sha256   {constants['EXPECTED_SHA256']}" in lines[1] and f"_cov_cpu {constants['EXPECTED_COV_CPU_SITES']} " in lines[2], "empty/unexpected fingerprint output")
            require(sha_file(main) == constants["EXPECTED_SHA256"] and main.read_bytes().count(b"_cov_cpu") == constants["EXPECTED_COV_CPU_SITES"], "engine changed after fingerprint")
            require(score["gates"]["fingerprint"] == lines[0], "scorer engine fingerprint mismatch")
            return {"scorer": score["gates"]["fingerprint"], "preflight": fp}
        check("engine_fingerprint_explicit_root", fingerprint)

        def contexts():
            path = score_path.parent / "replay_provenance.jsonl"
            records = [load_json_line(line) for line in path.read_text().splitlines()]
            require(len(records) == 3 and [r["arm"] for r in records] == list(ARMS), "exactly three complete arm records in fixed order required")
            launch_sha = sha_file(Path(receipt["dest"]) / "replay_launch.json")
            for record in records:
                require(record["invocation_id"] == receipt["invocation_id"] and record["run_dir"] == str(score_path.parent), "cross-run arm record")
                require(record["executed_edit_py_sha256"] == EXPECTED_EDIT_SHA256 and record["launch_sha256"] == launch_sha, "executed source/launch hash mismatch")
                ctx = record["edit_context_templates"]
                require(isinstance(ctx, list) and len(ctx) == 2 and all(isinstance(g, list) for g in ctx) and [len(g) for g in ctx] == [1, 5] and all(isinstance(t, str) and t.count("{}") == 1 for g in ctx for t in g), "malformed six-context list")
                require(record["edit_context_templates_sha256"] == sha_json(ctx) == CONTEXT_SHA, "wrong full edit-time context hash")
                require(ctx == records[0]["edit_context_templates"], "arm context lists differ")
            require(score["gates"]["templates_sha"] == CONTEXT_SHA[:12], "wrong scorer context hash")
            return records
        records = check("three_arm_context_source_records", contexts, lambda rs: [{k: r[k] for k in ("arm", "invocation_id", "run_dir", "executed_edit_py_sha256", "edit_context_templates_sha256", "edit_context_templates", "launch_sha256")} for r in rs])
        if records is not None:
            tokenizer = check("cached_tokenizer", cached_tokenizer, lambda _: {"revision": MODEL_REV, "torch_imported": "torch" in sys.modules})
            for record in records:
                check("count_position_primitive_" + record["arm"], lambda record=record: validate_positions(record, tokenizer))
        else:
            for arm in ARMS:
                check("count_position_primitive_" + arm, lambda: require(False, "complete context/source arm records unavailable; positions and primitive identity are unverifiable"))

        def metadata():
            require(type(score["seed"]) is int and score["seed"] == 0 and type(score["edit_budget"]) is int and score["edit_budget"] == 2700, "wrong seed/edit budget")
            require(score["edits"]["commit"] == BASE_COMMIT[:7], "wrong score commit")
            require(summary is not None and summary["law5_ok"] is True and summary["scope_ok"] is True and score["gates"]["law5"]["ok"] is True, "LAW#5/scope failed")
            require(68 <= summary["A1"] <= 72 and 68 <= summary["A2"] <= 72, "A1/A2 below floor or above physical ceiling")
            return {"seed": score["seed"], "edit_budget": score["edit_budget"], "commit": score["edits"]["commit"], "law5": score["gates"]["law5"], "scope_ok": summary["scope_ok"], "A1": summary["A1"], "A2": summary["A2"], "reference_controls": [69, 69], "changed": score["edits"]["changed"]}
        check("fixed_metadata_controls_law5_scope", metadata)

        def runtime():
            before, after = receipt["fidelity_before"], receipt["fidelity_after"]
            require(before == after == receipt["launch"]["fidelity_before"], "runtime inputs changed during execution")
            require(before["interpreter"] == str((PROGRAM_ROOT / ".venv/bin/python").resolve()) and before["venv"] == str((PROGRAM_ROOT / ".venv").resolve()), "wrong runtime interpreter/venv")
            require(before["model_id"] == "Qwen/Qwen2.5-3B" and before["model_revision"] == before["tokenizer_revision"] == MODEL_REV, "wrong model/tokenizer revision")
            require(before["packages"]["transformers"] == "4.51.0" and all(isinstance(before["packages"][x], str) and before["packages"][x] for x in ("torch", "transformers", "tokenizers", "numpy", "safetensors", "accelerate")), "missing package versions or wrong pin")
            require(isinstance(before["os"], str) and before["os"] and isinstance(before["python_version"], str) and before["python_version"], "missing OS/Python version")
            files = before["files"]
            require(isinstance(files, dict) and len(files) >= 20 and all(isinstance(k, str) and isinstance(v["resolved_path"], str) and v["resolved_path"] and digest(v["sha256"]) for k, v in files.items()), "incomplete fidelity file identities")
            expected_files = {str(p): str(p.resolve(strict=True)) for p in fidelity_inputs(receipt["dest"])}
            require(set(files) == set(expected_files) and all(files[k]["resolved_path"] == v for k, v in expected_files.items()), "fidelity input set or resolved paths incomplete/changed")
            require(set(before["numeric_env"]) == {"LLMDB_DEVICE", "PYTORCH_MPS_FAST_MATH", "PYTORCH_ENABLE_MPS_FALLBACK", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"}, "missing numeric/device environment identity")
            require(before["numeric_env"]["LLMDB_DEVICE"] in (None, "mps"), "wrong edit device override")
            for key in ("configs/hparams/qwen25_3b_memit_hparams.json", "configs/screens/g6_screen_qwen3b.json", "configs/screens/g6_screen_qwen3b_v2.json", "experiments/track_c/c10e_bandknob.py", "tools/engine_fingerprint.py", "memit_dry_run/memit/globals.yml", f"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/{MODEL_REV}/tokenizer.json", f"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/{MODEL_REV}/config.json"):
                require(str(PROGRAM_ROOT / key) in files, f"missing fidelity input: {key}")
            require(any(k.endswith(".safetensors") for k in files) and all(any(f"model.layers.{layer}.mlp.down_proj_" in k for k in files) for layer in LAYERS), "missing model/covariance byte identities")
            return {"interpreter": before["interpreter"], "packages": before["packages"], "os": before["os"], "model_revision": before["model_revision"], "file_count": len(files), "manifest_sha256": sha_json(before), "unchanged": True}
        check("fidelity_before_after", runtime)

        def processes():
            require(receipt["exclusive_window"] == "paused-no-relaunch", "exclusive ownership window not acknowledged")
            mps = receipt["mps_preflight"]
            require(mps["exit"] == 0 and mps["stdout"].strip() == "MPS_AVAILABLE=true", "MPS preflight failed or missing")
            path = Path(receipt["dest"]) / "process_exclusion.jsonl"
            require(receipt["process_log_sha256"] == sha_file(path), "process log hash mismatch")
            events = [load_json_line(x) for x in path.read_text().splitlines()]
            require(len(events) >= 4 and {"before_dispatch", "after_preflight", "during_run", "after_exit"} <= {e["phase"] for e in events}, "missing process-check phase")
            for e in events:
                require(e["probe_exit"] == 0 and integer(e["process_count"], 1, 2**31) and e["ok"] is True and e["foreign"] == [], "failed full-process exclusion")
                require(e["runner_pid"] == receipt["runner_pid"] and e["runner_pid"] in e["own_chain"], "runner process chain mismatch")
                owned = {x["pid"] for x in e["owned_children"]}
                require(all(x["pid"] in e["own_chain"] or x["pid"] in owned for x in e["matches"]), "unowned model process in log")
                if e["phase"] in ("during_run", "after_exit"):
                    require(e["child_pid"] == receipt["child_pid"], "unbound editor/scorer process ownership")
            return {"exclusive_window": receipt["exclusive_window"], "mps": mps, "checks": len(events), "phases": [e["phase"] for e in events], "runner_pid": receipt["runner_pid"], "child_pid": receipt["child_pid"], "owned_children": receipt["owned_children"], "log_sha256": receipt["process_log_sha256"]}
        check("exclusive_processes_mps", processes)
    else:
        for name in ("live_or_explicit_tmp_selftest", "frozen_checkout_source_diff", "fresh_invocation_score_receipt", "engine_fingerprint_explicit_root", "three_arm_context_source_records", *("count_position_primitive_" + arm for arm in ARMS), "fixed_metadata_controls_law5_scope", "fidelity_before_after", "exclusive_processes_mps"):
            check(name, lambda: require(False, "receipt/score unavailable; this gate is unverifiable"))

    if summary is not None:
        fixed = {"A1": (">=", 68), "A2": (">=", 68), "L1_flips": ("<=", 1), "frame_flips": ("<=", 2), "described_as": (">=", 85.0), "L3": (">=", 29), "ppl_post": ("<=", 22.2), "law5_ok": ("==", True), "scope_ok": ("==", True)}
        failed = []
        for key, (op, threshold) in fixed.items():
            value = summary[key]
            ok = value >= threshold if op == ">=" else value <= threshold if op == "<=" else value is threshold
            print(f"GUARD {key}: {'PASS' if ok else 'FAIL'} value={json.dumps(value)} rule={op}{threshold}")
            if not ok:
                failed.append(key)
        expected_guards = "ok" if not failed else "failed:" + ",".join(failed)
        check("guard_summary_integrity", lambda: (require(summary["guards"] == expected_guards, "guard string disagrees with recomputed exact guards"), expected_guards)[1])
        quality = "DEGRADED" if failed else "OK"
        d = summary["dw_total"]
        print("REPORTED " + json.dumps({"H": summary["heldout_full"], "C": c, "O": o, "D": d, "D_minus_88.974": d - 88.974, "D_minus_131.421": d - 131.421, "D_over_88.974": d / 88.974, "D_over_131.421": d / 131.421, "quality": quality, "summary": summary, "arm_dw_total": {a: score["arms"][a]["dw_total"] for a in ARMS}, "scorer_fingerprint": score["gates"]["fingerprint"], "saved_sha256": score["saved_sha256"]}, sort_keys=True))
        for arm in ARMS:
            for row in score["arms"][arm]["rows"]:
                print("FACT " + json.dumps({"arm": arm, "subject": row["subj"], "value": row["val"], "para_full_hits": row["para_full_hits"], "para_first_hits": row["para_first_hits"], "canon_full": row["canon_full"]}))
        if failures:
            print(f"NON-BINDING count-only labels: primary={primary_label(summary['heldout_full'])} secondary={secondary_label(c)} quality={quality}")
        else:
            if mode["synthetic_fixture"]:
                print("SYNTHETIC SELF-TEST: label-path demonstration only; no measured or binding scientific result")
            print(f"LABEL primary={primary_label(summary['heldout_full'])} secondary={secondary_label(c)} quality={quality}")
    if failures:
        print("INVALID")
        print("HALT: " + ", ".join(failures) + "; no binding label")
        return 2
    return 0


def load_json_line(line):
    require(bool(line.strip()), "empty provenance/process JSONL record")
    value = parse_json(line)
    require(isinstance(value, dict), "JSONL record must be an object")
    return value


def main():
    if len(sys.argv) != 3:
        print("INVALID\nHALT: usage: read_replay.py SCORE_JSON RECEIPT; no binding label")
        return 2
    try:
        return read_score(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError, ImportError, OverflowError, RecursionError, subprocess.SubprocessError) as exc:
        print(f"INVALID\nHALT: malformed input: {exc}; no binding label")
        return 2


if __name__ == "__main__":
    sys.exit(main())
