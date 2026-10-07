Reviewer/implementer: gpt-6.1-sol (max effort), Codex CLI 0.160.1

Implemented the preregistered zero-preserve replay driver and strict reader. The model replay has not run. The required scratch-clone self-test, source compilation, standalone blocklist check, fixture reads, synthetic passing path, and additional rejection checks completed; the scratch clone was deleted.
The operator corrected the brief's fixture-validity expectation during implementation: all preregistration §3 gates remain strict. The two old scores lack the replay's pre-launch diff and executed-source records, so both return INVALID with exit 2. Immediately after the validity block, the reader prints the label their counts would earn, explicitly NON-BINDING: 7 → SUPPORTS-PRESERVE and 18 → ARTIFACT-SUSPECT. A separately marked synthetic fixture supplies complete provenance and passes all seven gates. No exception or exemption was added for recorded fixtures. `docs/C10R_EXP2_ZEROPRESERVE_PREREG.md` was left unchanged.
Built these four deliverables:

- `experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh`: refuses any existing destination, clones with `git clone --no-local --no-checkout`, checks out detached commit `92acd0378d23f4935df9a8bccc0137b36695a40f`, recreates the untracked `.venv` link, applies the exact permitted patch, writes `replay_diff.txt`, and refuses any extra source change. The default destination is `/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2`.
- `experiments/track_c/autoresearch_c10/replay_exp2/run_replay.sh`: checks the exact process pattern before any launch, refuses a failed process probe, repeats the source/diff audit, writes `replay_launch.json`, asserts MPS availability, and launches `.venv/bin/python edit.py` in the destination with `PYTHONDONTWRITEBYTECODE=1`, `run.log`, `run.pid`, wait, and the child's exit status.
- `experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py`: uses only the standard library; prints every validity check and its value, all reported-beside fields, and all 24 per-fact `para_full_hits` split into 16 collision facts and eight others. Legal counts use the exact ≤11 / 12–17 / ≥18 thresholds. Any failed validity check produces exit 2, INVALID, and HALT, with only the explicitly nonbinding count label.
- This report, `results/c10r_exp2ctl_codex_impl_v1.md`.

`read_replay.py:41` defines the one permitted patch used by both setup and launch. `read_replay.py:65` checks the full pinned HEAD, independent `.git` directory, absence of object alternates, exact expected `edit.py` bytes, and unchanged pinned `prepare.py`/`c10e_bandknob.py` bytes. The diff is checked from bytes and pinned Git objects rather than trusting a stored PASS flag. The only science change is `PRESERVE_WEIGHT = 1.0` → `0.0`; value-key collection, additional forward passes, diagnostics, constants, and layer order remain present in the displayed diff.
The logging captures the absolute executed `edit.py` path and its full SHA-256 before importing `prepare.py`, because the harness changes the working directory into the engine. Immediately after `get_context_templates`, it prints both hashes and appends the context list, its full SHA-256, the executed-source hash, and the pre-launch audit to `runs/<run>/replay_provenance.jsonl`. The list uses the same `json.dumps(...).encode()` hash serialization as the scorer, with the full 64-character hash retained. The edit-time hash is recorded and checked for consistency; §3 binds the separate scorer hash to the required 12-character `e8605172dce0`.
The pinned `prepare.py:195` creates `run_dir` before its direct `apply_edit(facts(arm))` call at `prepare.py:209`. The logging obtains that caller's `run_dir` through `sys._getframe(1).f_locals`, so the fixed evaluator needs no modification. The logging-only self-test below exercises this exact caller-local contract and appends three records without running model code. The reader requires adjacent provenance, recomputes the allowed patch and diff from the replay clone, compares every recorded launch audit to the current audit, verifies every executed-source hash, and rehashes every recorded context list (`read_replay.py:102`).
The runner was compared with `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/run.sh:8` and `run.sh:21`: destination cwd replaces the sandbox cwd; the same `.venv/bin/python edit.py`, output redirection, pid/wait, and exit-status sequence is retained. Seatbelt is removed as requested. The original preflight's MPS tensor allocation (`run.sh:12`) is omitted; the new preflight checks availability only. Neither runner nor this availability check was executed.
No `edit.py`, `prepare.py`, fence script, model loader, torch import, or MPS check was executed in this task. `py_compile` compiles the scratch source without executing it. The synthetic test executes only the added standard-library logging strings. The scripts are ready for the separately authorized live replay; CPU self-tests do not establish MPS availability, model execution, or any scientific conclusion.

Hard-coded path audit. Locations below refer to the pinned loop files at `92acd03`; these files were inspected without importing them. `PROGRAM_ROOT` is `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`. `HERE` is the directory containing the cloned `prepare.py`. The Git clone is standalone; its frozen evaluator still depends on the existing program runtime/resources and the fence reference file.

| Location at 92acd03 | Path or construction | Effect outside the sandbox and handling |
| --- | --- | --- |
| `prepare.py:27`, `prepare.py:68` | `HERE = dirname(abspath(__file__))`; `{HERE}/edit.py` | Uses the clone's source for the name blocklist. No sandbox path rewrite is needed. The check was exercised standalone against the patched source. |
| `prepare.py:28`, `prepare.py:60` | Absolute `PROGRAM_ROOT`; assigned to `LLMDB_ROOT` | Relocation does not relocate engine/model/config resources. The existing program root is intentionally retained so the fixed evaluator remains byte-identical and does not resolve against an inherited root. A removed program checkout would make the replay fail. |
| `prepare.py:29`, `prepare.py:136`, `prepare.py:222` | `{PROGRAM_ROOT}/.venv/bin/python` | Fingerprint and scorer subprocesses use the fixed program interpreter, independent of clone location. Setup resolves the sandbox's untracked `.venv` chain and recreates a link to the same shared runtime; the transcript shows its real target. No environment is copied or installed. |
| `prepare.py:30`, `prepare.py:63`, `prepare.py:85` | `{PROGRAM_ROOT}/experiments/track_c/c10e_bandknob.py`; `{PROGRAM_ROOT}/experiments/track_c` | The actual imported harness comes from the program checkout, not the cloned local copy. The existing full SHA-256 guard (`prepare.py:31`, `prepare.py:63`) remains in force. The clone's local harness is also checked unchanged by the replay audit. Missing or changed program harness fails rather than silently substituting the clone's copy. |
| `prepare.py:32`, `prepare.py:113`, `prepare.py:151` | `{PROGRAM_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json` | Reads the fixed program hyperparameters. Left unchanged; the program resource must remain present. |
| `prepare.py:33`, `prepare.py:144` | `/Volumes/memit/llm-database-poc-mirror/autoresearch_fence_c10/reference_controls.json` | This is the one literal fence-directory data dependency. The fixed `_reference_ok` reads it and validates its controls; it does not write it. Retained unchanged and confirmed present by a read-only path probe. The reference file must remain available to a future replay. |
| `prepare.py:115`, `prepare.py:118` | `{HERE}/.hparams_{pid}.json` | Temporary hyperparameters are written and removed inside the clone even after the engine changes cwd. No sandbox/fence write. |
| `prepare.py:136` | `{PROGRAM_ROOT}/tools/engine_fingerprint.py` | The program's fingerprint helper remains the subprocess target. Retained unchanged; it and its engine dependencies must remain available. |
| `prepare.py:194`, `prepare.py:195` | Git query with `cwd=HERE`; `{HERE}/runs/{timestamp}_{commit}` | Git metadata and run output refer to the standalone clone. The future run's directory will carry the pinned short commit; no checkout or output operation targets the loop's sandbox. |
| `prepare.py:217`, `prepare.py:221`, `prepare.py:250`, `prepare.py:259`, `prepare.py:293`, `prepare.py:295` | `{run_dir}/{arm}.pt`, `{run_dir}/edits.json`, `{run_dir}/score.json` | Save/read/remove operations stay under the clone's absolute run directory. No changes were needed. The replay's provenance JSONL is placed in this same run directory. |
| `prepare.py:222` | `os.path.abspath(__file__)` for the scorer | The scorer executes the clone's `prepare.py`, despite the engine cwd change. The fixed program interpreter does not redirect scoring into the sandbox. Retained unchanged. |
| `c10e_bandknob.py:2` | Default `LLMDB_ROOT=/workspace` | Importing the harness alone on this machine would rely on a wrong default. The prescribed edit → prepare path overrides it with `PROGRAM_ROOT` before the harness import (`prepare.py:60`, `prepare.py:86`). No harness patch or standalone harness execution was used. |
| `c10e_bandknob.py:4` | `{LLMDB_ROOT}/hf_cache` | Shared program model cache remains selected. `HF_HUB_OFFLINE=0` at line 5 remains unchanged, including its original cache/download behavior. No model load or cache mutation was performed here; cloning does not make this cache private. |
| `c10e_bandknob.py:6`, `c10e_bandknob.py:7`, `c10e_bandknob.py:8` | `{LLMDB_ROOT}/memit_dry_run/memit`; `sys.path` and `chdir` to this engine | Uses the shared unmodified program engine. Left unchanged. Added logging captures the clone's absolute edit path before this cwd change and uses absolute paths afterward. |
| `c10e_bandknob.py:25` | `Qwen/Qwen2.5-3B` | This slash-containing string is the pinned Hugging Face model identifier, resolved through the shared cache rather than a sandbox directory. Kept unchanged; no loader was run. |
| `c10e_bandknob.py:30` | `{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams.json` | Fixed program hyperparameter input, retained as-is. |
| `c10e_bandknob.py:31` | `HP_CANDIDATE` or `{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band812.json` | Legacy `main()` recipe path. `prepare.py:55` refuses inherited `HP_CANDIDATE`; this replay uses `load_hparams` and does not invoke `H.main()`. No config rewrite. |
| `c10e_bandknob.py:32`, `c10e_bandknob.py:589`, `c10e_bandknob.py:598` | `OUT` or `{LLMDB_ROOT}/results/c10e_bandknob.json` | Would write into the program results directory if harness `main()` were executed. The loop imports the harness and uses `prepare.evaluate`; the `__main__` guard does not run this writer. Preserved unchanged; the replay's score writer is `prepare.py:293` inside the clone. |
| `c10e_bandknob.py:35`, `c10e_bandknob.py:574` | `PREREG` or `{LLMDB_ROOT}/docs/C10_BANDKNOB_PREREG.md` | Legacy harness `main()` metadata, not a replay input or output path. Kept unchanged; the replay reader implements the supplied zero-preserve preregistration. |
| `c10e_bandknob.py:225`, `c10e_bandknob.py:267` | `{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json` | Active stimulus/L3 input from the program checkout. Must remain available; kept as-is to preserve the evaluation. |
| `c10e_bandknob.py:265` | `{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b.json` | Active L1 screen input from the program checkout. Must remain available; kept as-is. |
| `c10e_bandknob.py:345`, `c10e_bandknob.py:349` | Engine `STATS_DIR` plus `{model_id}/{dataset}_stats/{module}_{dtype}_mom2_t100_{n_samples}.npz` | The covariance-hash helper depends on engine cache paths, not clone cwd. This helper is not called by the loop's fixed evaluator; the edit's original `get_cov` still uses shared engine cache configuration. No cache copying, redirecting, or engine change. |
| `edit.py` at 92acd03 | No hard-coded filesystem path | The original file has no sandbox/fence filesystem literal. New logging reads clone-root `replay_launch.json` and appends run-local `replay_provenance.jsonl`, using the captured absolute edit path and the fixed evaluator's absolute `run_dir`. |

The source sandbox had an untracked `.venv` runtime link; setup recreates it instead of assuming Git tracked it. The required interpreter, program harness, base hyperparameters, `hf_cache`, engine directory, and fence reference file were found by read-only filesystem probes. Availability of these paths does not prove a live model replay. The cloned sources and displayed diff demonstrate that no evaluation path was rewritten to the new destination, and no absolute loop-sandbox output path was embedded in the three pinned Python files.

Self-test transcripts follow. Commands ran from the program worktree stated above. `/opt/homebrew/bin/rtk proxy` forwards the command without filtering; each fenced output block is the captured tool stdout/stderr verbatim, and exit status is recorded separately. An empty-output check is explicitly identified without inserting invented output.

Scratch setup.

```bash
/opt/homebrew/bin/rtk proxy experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh /tmp/c10r-exp2ctl-selftest-mux8ornp
```

```text
Cloning into '/tmp/c10r-exp2ctl-selftest-mux8ornp'...
HEAD is now at 92acd03 edit: preserve keys at the value-token positions (coined value words double as subjects) + overlap/leak diagnostics
READY: /private/tmp/c10r-exp2ctl-selftest-mux8ornp
base_commit: 92acd0378d23f4935df9a8bccc0137b36695a40f
runtime_link: /private/tmp/c10r-exp2ctl-selftest-mux8ornp/.venv -> /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.venv
edit_py_sha256: 35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95
diff_sha256: 1b2a6e4c4a5c59163328da224090d9eac6c9e75058800f3cb5c459eb5355d31e
permitted_diff: PASS (zero weight and exact logging additions only)
```

Exit code: `0`.

Permitted diff, shown in full.

```bash
/opt/homebrew/bin/rtk proxy cat '/tmp/c10r-exp2ctl-selftest-mux8ornp/replay_diff.txt'
```

```text
diff --git a/edit.py b/edit.py
index 60f49ff..ce5865a 100644
--- a/edit.py
+++ b/edit.py
@@ -14,6 +14,14 @@ Methods the baseline implements:
 
 import torch
 
+import hashlib
+import json
+import os
+import sys
+
+_REPLAY_EDIT_PATH = os.path.abspath(__file__)
+_REPLAY_EDIT_SHA256 = hashlib.sha256(open(_REPLAY_EDIT_PATH, "rb").read()).hexdigest()
+
 from prepare import (model, tok, DEV, COV_LAYERS, request, load_hparams, evaluate,
                      compute_z, compute_ks, get_module_input_output_at_words, get_cov, get_context_templates,
                      upd_matrix_match_shape)
@@ -30,7 +38,7 @@ KL_FACTOR = 0.0625          # weight of the KL term that keeps "<subject> is a"
 V_WEIGHT_DECAY = 0.5        # L2 on delta z during the solve
 RIDGE = 1.0                 # L2 added to the per-layer least-squares solve
 NULL_THRESH = 0.005         # eigenvalues of the key covariance below this span the projector's null space
-PRESERVE_WEIGHT = 1.0       # weight of the keys at the value-token positions in the solve (the write must not fire there)
+PRESERVE_WEIGHT = 0.0       # weight of the keys at the value-token positions in the solve (the write must not fire there)
 
 # ---------------------------------------------------------------------------
 # Setup: hyperparameters, projectors
@@ -80,6 +88,20 @@ def apply_edit(facts):
     """Write facts = [(subject, value)] into the model in place."""
     requests = [request(s, v) for s, v in facts]
     ctx = get_context_templates(model, tok)
+    _replay_templates_sha = hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
+    print(f"executed_edit_py_sha256: {_REPLAY_EDIT_SHA256}", flush=True)
+    print(f"edit_context_templates_sha256: {_replay_templates_sha}", flush=True)
+    with open(os.path.join(os.path.dirname(_REPLAY_EDIT_PATH), "replay_launch.json")) as _replay_f:
+        _replay_launch = json.load(_replay_f)
+    _replay_record = {
+        "executed_edit_py_sha256": _REPLAY_EDIT_SHA256,
+        "edit_context_templates_sha256": _replay_templates_sha,
+        "edit_context_templates": ctx,
+        "launch": _replay_launch,
+    }
+    _replay_run_dir = sys._getframe(1).f_locals["run_dir"]
+    with open(os.path.join(_replay_run_dir, "replay_provenance.jsonl"), "a") as _replay_f:
+        _replay_f.write(json.dumps(_replay_record) + "\n")
     z_layer = LAYERS[-1]
     zs = torch.stack([compute_z(model, tok, rq, HP, z_layer, ctx) for rq in requests], dim=1)   # target hidden state per fact
 
```

Exit code: `0`.

Compilation of the patched edit source; no execution.

```bash
/opt/homebrew/bin/rtk proxy env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m py_compile '/tmp/c10r-exp2ctl-selftest-mux8ornp/edit.py'
```

Captured output: empty.

Exit code: `0`.

Exact fixed blocklist logic, extracted as a literal by AST; no prepare import.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - '/tmp/c10r-exp2ctl-selftest-mux8ornp' <<'PY'
import ast
from pathlib import Path
import sys
root = Path(sys.argv[1])
module = ast.parse((root / 'prepare.py').read_text())
assignment = next(node for node in module.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == '_FORBIDDEN' for target in node.targets))
forbidden = ast.literal_eval(assignment.value)
text = (root / 'edit.py').read_text()
hits = [word for word in forbidden if word in text]
print('Standalone prepare.py:67-76 blocklist: ' + ('FAIL' if hits else 'PASS'))
print('hits =', hits)
assert not hits
print('prepare.py was parsed only; it was not imported.')
PY
```

```text
Standalone prepare.py:67-76 blocklist: PASS
hits = []
prepare.py was parsed only; it was not imported.
```

Exit code: `0`.

Shell syntax checks; the runner is parsed only.

```bash
/opt/homebrew/bin/rtk proxy /bin/bash -n experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh experiments/track_c/autoresearch_c10/replay_exp2/run_replay.sh
```

Captured output: empty.

Exit code: `0`.

Reader syntax check, without generating bytecode.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - <<'PY'
import ast
from pathlib import Path
path = Path('experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py')
ast.parse(path.read_text(), filename=str(path))
print('read_replay.py syntax: PASS (AST only; no bytecode written)')
PY
```

```text
read_replay.py syntax: PASS (AST only; no bytecode written)
```

Exit code: `0`.

Recorded baseline fixture. Expected INVALID/exit 2; its count-only label is explicitly NON-BINDING.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json
```

```text
VALIDITY law5_ok: PASS value=true
VALIDITY scope_ok: PASS value=true
VALIDITY scorer_templates_sha: PASS value="e8605172dce0"
VALIDITY A1_in_[68,71]: PASS value=69
VALIDITY A2_in_[68,71]: PASS value=69
VALIDITY prelaunch_diff_only_permitted: FAIL value="MISSING /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/replay_provenance.jsonl"
VALIDITY executed_source_hash_recorded: FAIL value="MISSING executed-source record"
NON-BINDING count-only label: SUPPORTS-PRESERVE (failed validity: prelaunch_diff_only_permitted, executed_source_hash_recorded)
REPORTED heldout_full=7
REPORTED canon=7
REPORTED first_token=40
REPORTED A1=69
REPORTED A2=69
REPORTED L1_flips=0
REPORTED frame_flips=1
REPORTED described_as=90.38
REPORTED L3=30
REPORTED ppl_post=21.506
REPORTED scope_ok=true
REPORTED law5_ok=true
REPORTED dw_total=88.974
REPORTED guards="ok"
REPORTED H0_equals_7=true
COLLISION: facts=16 full_hits=0/48
  Quaxil -> Drennik Brakk: para_full_hits=[false, false, false]
  Plurnak -> Vythorn Stavik: para_full_hits=[false, false, false]
  Vythorn -> Vorlex Yornel: para_full_hits=[false, false, false]
  Drennik -> Kessivar Ulvenn: para_full_hits=[false, false, false]
  Yastovel -> Halquin Cindel: para_full_hits=[false, false, false]
  Crulpane -> Marsduq Drelth: para_full_hits=[false, false, false]
  Mophgar -> Glimsto Vask: para_full_hits=[false, false, false]
  Trannak -> Fluvane Stavik: para_full_hits=[false, false, false]
  Oxbarrow -> Drennik Ulvenn: para_full_hits=[false, false, false]
  Zephquin -> Vythorn Cindel: para_full_hits=[false, false, false]
  Lurmaxen -> Vorlex Drelth: para_full_hits=[false, false, false]
  Kessivar -> Kessivar Brakk: para_full_hits=[false, false, false]
  Wombryne -> Halquin Stavik: para_full_hits=[false, false, false]
  Halquin -> Marsduq Yornel: para_full_hits=[false, false, false]
  Vorlex -> Glimsto Spraxil: para_full_hits=[false, false, false]
  Marsduq -> Fluvane Cindel: para_full_hits=[false, false, false]
OTHER: facts=8 full_hits=7/24
  Zorbland -> Vindex Vask: para_full_hits=[true, true, true]
  Glimsto -> Lurmax Spraxil: para_full_hits=[true, false, false]
  Brinduun -> Brindu Brakk: para_full_hits=[false, true, true]
  Skornwell -> Yastov Yornel: para_full_hits=[false, false, false]
  Fluvane -> Vindex Spraxil: para_full_hits=[false, false, true]
  Pradnoll -> Lurmax Vask: para_full_hits=[false, false, false]
  Quenby -> Brindu Ulvenn: para_full_hits=[false, false, false]
  Thelby -> Yastov Drelth: para_full_hits=[false, false, false]
INVALID
HALT: validity failure; no reading label
```

Exit code: `2`.

Recorded winner fixture. Expected INVALID/exit 2; its count-only label is explicitly NON-BINDING.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/score.json
```

```text
VALIDITY law5_ok: PASS value=true
VALIDITY scope_ok: PASS value=true
VALIDITY scorer_templates_sha: PASS value="e8605172dce0"
VALIDITY A1_in_[68,71]: PASS value=69
VALIDITY A2_in_[68,71]: PASS value=69
VALIDITY prelaunch_diff_only_permitted: FAIL value="MISSING /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/replay_provenance.jsonl"
VALIDITY executed_source_hash_recorded: FAIL value="MISSING executed-source record"
NON-BINDING count-only label: ARTIFACT-SUSPECT (failed validity: prelaunch_diff_only_permitted, executed_source_hash_recorded)
REPORTED heldout_full=18
REPORTED canon=24
REPORTED first_token=35
REPORTED A1=69
REPORTED A2=69
REPORTED L1_flips=0
REPORTED frame_flips=1
REPORTED described_as=92.55
REPORTED L3=30
REPORTED ppl_post=21.356
REPORTED scope_ok=true
REPORTED law5_ok=true
REPORTED dw_total=131.421
REPORTED guards="ok"
REPORTED H0_equals_7=false
COLLISION: facts=16 full_hits=13/48
  Quaxil -> Drennik Brakk: para_full_hits=[false, false, true]
  Plurnak -> Vythorn Stavik: para_full_hits=[false, true, true]
  Vythorn -> Vorlex Yornel: para_full_hits=[false, false, false]
  Drennik -> Kessivar Ulvenn: para_full_hits=[false, false, false]
  Yastovel -> Halquin Cindel: para_full_hits=[false, false, false]
  Crulpane -> Marsduq Drelth: para_full_hits=[false, false, false]
  Mophgar -> Glimsto Vask: para_full_hits=[true, true, true]
  Trannak -> Fluvane Stavik: para_full_hits=[true, true, true]
  Oxbarrow -> Drennik Ulvenn: para_full_hits=[false, false, false]
  Zephquin -> Vythorn Cindel: para_full_hits=[false, false, false]
  Lurmaxen -> Vorlex Drelth: para_full_hits=[false, false, true]
  Kessivar -> Kessivar Brakk: para_full_hits=[true, true, true]
  Wombryne -> Halquin Stavik: para_full_hits=[false, false, false]
  Halquin -> Marsduq Yornel: para_full_hits=[false, false, false]
  Vorlex -> Glimsto Spraxil: para_full_hits=[false, false, false]
  Marsduq -> Fluvane Cindel: para_full_hits=[false, false, false]
OTHER: facts=8 full_hits=5/24
  Zorbland -> Vindex Vask: para_full_hits=[true, true, true]
  Glimsto -> Lurmax Spraxil: para_full_hits=[false, false, false]
  Brinduun -> Brindu Brakk: para_full_hits=[false, true, true]
  Skornwell -> Yastov Yornel: para_full_hits=[false, false, false]
  Fluvane -> Vindex Spraxil: para_full_hits=[false, false, false]
  Pradnoll -> Lurmax Vask: para_full_hits=[false, false, false]
  Quenby -> Brindu Ulvenn: para_full_hits=[false, false, false]
  Thelby -> Yastov Drelth: para_full_hits=[false, false, false]
INVALID
HALT: validity failure; no reading label
```

Exit code: `2`.

Synthetic fixture construction and exact logging-only test. This copies existing score numbers and uses a fabricated context list; it is not a measured replay.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - '/tmp/c10r-exp2ctl-selftest-mux8ornp' <<'PY'
import contextlib
import io
import json
from pathlib import Path
import runpy
import sys

replay = Path(sys.argv[1]).resolve()
module = runpy.run_path('experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py')
audit = module['inspect_replay'](replay)
(replay / 'replay_launch.json').write_text(json.dumps(audit, indent=2) + '\n')
run_dir_path = replay / 'runs' / 'selftest_synthetic_provenance'
run_dir_path.mkdir(parents=True)
fixture = Path('/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json')
score = json.loads(fixture.read_text())
score['synthetic_fixture'] = True
score_path = run_dir_path / 'score.json'
score_path.write_text(json.dumps(score, indent=1) + '\n')

# Execute only the inert logging strings, with a synthetic caller/context.
# Never execute edit.py, prepare.py, or any model-loading code.
namespace = {'__file__': str(replay / 'edit.py')}
exec(compile(module['IMPORT_LOG'], '<logging-imports-only>', 'exec'), namespace)
exec(compile('def logging_only(ctx):\n' + module['CONTEXT_LOG'], '<logging-only>', 'exec'), namespace)
def caller_with_run_dir():
    run_dir = str(run_dir_path)
    namespace['logging_only']([['{}']])

print('SYNTHETIC FIXTURE: copied baseline counts; no model execution or scientific evidence.')
for _ in range(3):
    caller_with_run_dir()
records = (run_dir_path / 'replay_provenance.jsonl').read_text().splitlines()
assert len(records) == 3
for line in records:
    record = json.loads(line)
    assert record['executed_edit_py_sha256'] == audit['edit_py_sha256']
    assert record['launch'] == audit
print('Logging-only test: PASS; three JSONL records in the synthetic run directory.')
print('synthetic_score =', score_path)
PY
```

```text
SYNTHETIC FIXTURE: copied baseline counts; no model execution or scientific evidence.
executed_edit_py_sha256: 35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95
edit_context_templates_sha256: 2c4bfda034526ca212a07fd3b654bddabd1bdf0e9cab882be5fe337fe52cbb01
executed_edit_py_sha256: 35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95
edit_context_templates_sha256: 2c4bfda034526ca212a07fd3b654bddabd1bdf0e9cab882be5fe337fe52cbb01
executed_edit_py_sha256: 35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95
edit_context_templates_sha256: 2c4bfda034526ca212a07fd3b654bddabd1bdf0e9cab882be5fe337fe52cbb01
Logging-only test: PASS; three JSONL records in the synthetic run directory.
synthetic_score = /private/tmp/c10r-exp2ctl-selftest-mux8ornp/runs/selftest_synthetic_provenance/score.json
```

Exit code: `0`.

Synthetic passing-path read: all gates pass and exit 0. Its final LABEL demonstrates reader behavior on synthetic inputs only.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py '/tmp/c10r-exp2ctl-selftest-mux8ornp/runs/selftest_synthetic_provenance/score.json'
```

```text
VALIDITY law5_ok: PASS value=true
VALIDITY scope_ok: PASS value=true
VALIDITY scorer_templates_sha: PASS value="e8605172dce0"
VALIDITY A1_in_[68,71]: PASS value=69
VALIDITY A2_in_[68,71]: PASS value=69
VALIDITY prelaunch_diff_only_permitted: PASS value={"only_permitted_lines": true, "sha256": "1b2a6e4c4a5c59163328da224090d9eac6c9e75058800f3cb5c459eb5355d31e"}
VALIDITY executed_source_hash_recorded: PASS value={"context_hashes_consistent": true, "executed_sha256": ["35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95", "35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95", "35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95"]}
REPORTED heldout_full=7
REPORTED canon=7
REPORTED first_token=40
REPORTED A1=69
REPORTED A2=69
REPORTED L1_flips=0
REPORTED frame_flips=1
REPORTED described_as=90.38
REPORTED L3=30
REPORTED ppl_post=21.506
REPORTED scope_ok=true
REPORTED law5_ok=true
REPORTED dw_total=88.974
REPORTED guards="ok"
REPORTED H0_equals_7=true
REPORTED edit_context_templates_sha256[0]=2c4bfda034526ca212a07fd3b654bddabd1bdf0e9cab882be5fe337fe52cbb01
REPORTED edit_context_templates_sha256[1]=2c4bfda034526ca212a07fd3b654bddabd1bdf0e9cab882be5fe337fe52cbb01
REPORTED edit_context_templates_sha256[2]=2c4bfda034526ca212a07fd3b654bddabd1bdf0e9cab882be5fe337fe52cbb01
COLLISION: facts=16 full_hits=0/48
  Quaxil -> Drennik Brakk: para_full_hits=[false, false, false]
  Plurnak -> Vythorn Stavik: para_full_hits=[false, false, false]
  Vythorn -> Vorlex Yornel: para_full_hits=[false, false, false]
  Drennik -> Kessivar Ulvenn: para_full_hits=[false, false, false]
  Yastovel -> Halquin Cindel: para_full_hits=[false, false, false]
  Crulpane -> Marsduq Drelth: para_full_hits=[false, false, false]
  Mophgar -> Glimsto Vask: para_full_hits=[false, false, false]
  Trannak -> Fluvane Stavik: para_full_hits=[false, false, false]
  Oxbarrow -> Drennik Ulvenn: para_full_hits=[false, false, false]
  Zephquin -> Vythorn Cindel: para_full_hits=[false, false, false]
  Lurmaxen -> Vorlex Drelth: para_full_hits=[false, false, false]
  Kessivar -> Kessivar Brakk: para_full_hits=[false, false, false]
  Wombryne -> Halquin Stavik: para_full_hits=[false, false, false]
  Halquin -> Marsduq Yornel: para_full_hits=[false, false, false]
  Vorlex -> Glimsto Spraxil: para_full_hits=[false, false, false]
  Marsduq -> Fluvane Cindel: para_full_hits=[false, false, false]
OTHER: facts=8 full_hits=7/24
  Zorbland -> Vindex Vask: para_full_hits=[true, true, true]
  Glimsto -> Lurmax Spraxil: para_full_hits=[true, false, false]
  Brinduun -> Brindu Brakk: para_full_hits=[false, true, true]
  Skornwell -> Yastov Yornel: para_full_hits=[false, false, false]
  Fluvane -> Vindex Spraxil: para_full_hits=[false, false, true]
  Pradnoll -> Lurmax Vask: para_full_hits=[false, false, false]
  Quenby -> Brindu Ulvenn: para_full_hits=[false, false, false]
  Thelby -> Yastov Drelth: para_full_hits=[false, false, false]
LABEL: SUPPORTS-PRESERVE
```

Exit code: `0`.

Threshold boundaries, strict gate rejections, nonbinding locality guard behavior, and tamper checks.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - '/tmp/c10r-exp2ctl-selftest-mux8ornp' <<'PY'
import copy
import json
from pathlib import Path
import runpy
import subprocess
import sys

module = runpy.run_path('experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py')
classify = module['classify']
for count, label in ((0, 'SUPPORTS-PRESERVE'), (7, 'SUPPORTS-PRESERVE'), (11, 'SUPPORTS-PRESERVE'), (12, 'PARTIAL-PRESERVE'), (17, 'PARTIAL-PRESERVE'), (18, 'ARTIFACT-SUSPECT'), (72, 'ARTIFACT-SUSPECT')):
    assert classify(count) == label
    print(f'THRESHOLD {count}: PASS {label}')
for bad in (-1, 73, True, 7.0):
    try:
        classify(bad)
    except ValueError:
        print(f'INVALID COUNT {bad!r}: PASS rejected')
    else:
        raise AssertionError(f'illegal count accepted: {bad!r}')

root = Path(sys.argv[1]).resolve()
run_dir = root / 'runs' / 'selftest_synthetic_provenance'
score_path = run_dir / 'score.json'
base = json.loads(score_path.read_text())
reader = Path('experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py').resolve()
def check_score(name, score, expected_exit, label):
    path = run_dir / (name + '.json')
    path.write_text(json.dumps(score) + '\n')
    result = subprocess.run([sys.executable, '-B', str(reader), str(path)], capture_output=True, text=True)
    assert result.returncode == expected_exit, (name, result.returncode, result.stdout, result.stderr)
    if expected_exit == 0:
        assert '\nLABEL: ' + label + '\n' in result.stdout
        assert 'NON-BINDING' not in result.stdout
    else:
        assert '\nLABEL:' not in result.stdout
        assert 'NON-BINDING count-only label: ' + label in result.stdout
        assert '\nINVALID\n' in result.stdout
    print(f'{name}: PASS exit={expected_exit} ' + ('binding' if expected_exit == 0 else 'nonbinding') + f' {label}')

for key, value in (('law5_ok', False), ('scope_ok', False), ('A1', 67), ('A2', 72)):
    score = copy.deepcopy(base)
    score['summary'][key] = value
    check_score('reject_' + key, score, 2, 'SUPPORTS-PRESERVE')
score = copy.deepcopy(base)
score['gates']['templates_sha'] = 'bad-template-hash'
check_score('reject_scorer_template_hash', score, 2, 'SUPPORTS-PRESERVE')
score = copy.deepcopy(base)
score['summary'].update(A1=68, A2=71)
check_score('accept_A1_A2_boundaries', score, 0, 'SUPPORTS-PRESERVE')
score = json.loads(Path('/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/score.json').read_text())
score['synthetic_fixture'] = True
score['summary'].update(L1_flips=2, guards='failed:L1_flips')
check_score('nonbinding_locality_guard_failure', score, 0, 'ARTIFACT-SUSPECT')

provenance_path = run_dir / 'replay_provenance.jsonl'
original_provenance = provenance_path.read_text()
try:
    records = [json.loads(line) for line in original_provenance.splitlines()]
    records[0]['executed_edit_py_sha256'] = '0' * 64
    provenance_path.write_text(''.join(json.dumps(record) + '\n' for record in records))
    check_score('reject_source_hash_mismatch', base, 2, 'SUPPORTS-PRESERVE')
    records = [json.loads(line) for line in original_provenance.splitlines()]
    records[0]['launch']['diff'] += '\n+unpermitted change\n'
    provenance_path.write_text(''.join(json.dumps(record) + '\n' for record in records))
    check_score('reject_launch_diff_mismatch', base, 2, 'SUPPORTS-PRESERVE')
finally:
    provenance_path.write_text(original_provenance)
edit_path = root / 'edit.py'
original_edit = edit_path.read_bytes()
try:
    edit_path.write_bytes(original_edit.replace(b'RIDGE = 1.0', b'RIDGE = 2.0', 1))
    try:
        module['inspect_replay'](root)
    except ValueError as exc:
        print('unpermitted_science_edit: PASS refused (' + str(exc) + ')')
    else:
        raise AssertionError('unpermitted science edit accepted')
finally:
    edit_path.write_bytes(original_edit)
assert module['inspect_replay'](root)['edit_py_sha256'] == '35f3b1a49ec140dadaf4df108afb2138c4e7a2a6c294926bc3f6aa9c587d0c95'
print('Restored scratch source and provenance: PASS')
PY
```

```text
THRESHOLD 0: PASS SUPPORTS-PRESERVE
THRESHOLD 7: PASS SUPPORTS-PRESERVE
THRESHOLD 11: PASS SUPPORTS-PRESERVE
THRESHOLD 12: PASS PARTIAL-PRESERVE
THRESHOLD 17: PASS PARTIAL-PRESERVE
THRESHOLD 18: PASS ARTIFACT-SUSPECT
THRESHOLD 72: PASS ARTIFACT-SUSPECT
INVALID COUNT -1: PASS rejected
INVALID COUNT 73: PASS rejected
INVALID COUNT True: PASS rejected
INVALID COUNT 7.0: PASS rejected
reject_law5_ok: PASS exit=2 nonbinding SUPPORTS-PRESERVE
reject_scope_ok: PASS exit=2 nonbinding SUPPORTS-PRESERVE
reject_A1: PASS exit=2 nonbinding SUPPORTS-PRESERVE
reject_A2: PASS exit=2 nonbinding SUPPORTS-PRESERVE
reject_scorer_template_hash: PASS exit=2 nonbinding SUPPORTS-PRESERVE
accept_A1_A2_boundaries: PASS exit=0 binding SUPPORTS-PRESERVE
nonbinding_locality_guard_failure: PASS exit=0 binding ARTIFACT-SUSPECT
reject_source_hash_mismatch: PASS exit=2 nonbinding SUPPORTS-PRESERVE
reject_launch_diff_mismatch: PASS exit=2 nonbinding SUPPORTS-PRESERVE
unpermitted_science_edit: PASS refused (edit.py differs beyond the zero weight and exact logging additions)
Restored scratch source and provenance: PASS
```

Exit code: `0`.

Existing-destination refusal, before cleanup.

```bash
/opt/homebrew/bin/rtk proxy experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh '/tmp/c10r-exp2ctl-selftest-mux8ornp'
```

```text
REFUSED: DEST already exists: /tmp/c10r-exp2ctl-selftest-mux8ornp
```

Exit code: `2`.

Regression check: an INVALID old fixture prints its nonbinding count label and never a binding LABEL.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - <<'PY'
import subprocess
import sys
import unittest
from pathlib import Path
reader = Path('experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py')
fixture = '/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json'
class InvalidReferenceTest(unittest.TestCase):
    def test_invalid_reference_reports_only_nonbinding_count_label(self):
        result = subprocess.run([sys.executable, '-B', str(reader), fixture], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('NON-BINDING count-only label: SUPPORTS-PRESERVE', result.stdout)
        self.assertNotIn('\nLABEL:', result.stdout)
unittest.main()
PY
```

```text
.
----------------------------------------------------------------------
Ran 1 test in 0.050s

OK
```

Exit code: `0`.

Scratch cleanup. The shared runtime symlink target is checked to survive deletion.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - '/tmp/c10r-exp2ctl-selftest-mux8ornp' <<'PY'
from pathlib import Path
import shutil
import subprocess
import sys
root = Path(sys.argv[1]).resolve(strict=True)
assert root.parent == Path('/private/tmp')
assert root.name.startswith('c10r-exp2ctl-selftest-')
head = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout.strip()
assert head == '92acd0378d23f4935df9a8bccc0137b36695a40f'
runtime = (root / '.venv').resolve(strict=True)
shutil.rmtree(root)
assert not root.exists()
assert runtime.is_dir()
print('Scratch clone deleted:', root)
print('Shared runtime still exists:', runtime)
PY
```

```text
Scratch clone deleted: /private/tmp/c10r-exp2ctl-selftest-mux8ornp
Shared runtime still exists: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.venv
```

Exit code: `0`.

The synthetic fixture and all test-only records were inside the deleted scratch clone. The permanent implementation consists of the three scripts and this report. The two old fixture files and the loop/fence directories were read only. No commit, tmux operation, or change to preregistration/canonical scientific records was made. The real replay still has to satisfy every §3 validity gate before its count can receive a binding preregistered reading.

