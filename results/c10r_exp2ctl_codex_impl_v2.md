Reviewer/implementer: gpt-6.1-sol (max effort), Codex CLI 0.160.1

Implemented the v2 location-control build. The live model job was not run. The authorized build and CPU verification are complete subject to the explicit runtime limits below; this report contains the actual commands and unabridged stdout/stderr. No experiment finding or CORPUS label is being declared. This touches the write/compile layer (§8.1 preserve side of the D20 solve), toward the scoped C10 candidate falsifier; it does not close C10 or F1.

From v1, the science intervention changes from coefficient zero to coefficient 1 with the frozen common-canonical-word positions. All three arms retain the original inputs, captured forward, target solve, residual, solve/cast/update expressions, and order. The original value block is audit-only. The patch adds the actual selector manifest, same-capture suffix-versus-explicit-index bit-identity gate, finite/shape/count checks, complete per-arm provenance, pre-cast norms and both projected-key norms. Setup defaults to `/Volumes/memit/llm-database-poc-mirror/autoresearch_replay_c10_exp2loc`. The runner now reserves a single invocation, fingerprints before model dispatch with explicit root/interpreter, rejects inherited model/cache/device knobs, checks exact PID ownership before dispatch/after preflight/every second through editor and scorer, retains source/input byte identities before and after, binds one exact score in a receipt, calls the reader, and propagates its status in `run.rc`. The reader uses v2 §4 labels and the physical A1/A2 range [68,72], validates all registered rows, re-encodes the token manifest with the pinned cached Rust tokenizer, recomputes guards, and prints diagnostic vectors and norms. It never imports torch or transformers.

The only deliverables are the three files under `experiments/track_c/autoresearch_c10/replay_exp2/` and this report. Their short filenames are used in the gate table. Neither frozen source document was edited: `docs/C10R_EXP2_LOCATIONCTL_PREREG.md` SHA256 `da108cc5f91446d0114fa3e061258995a94560753ede8069cf216d1848017a38`; `results/c10r_exp2ctl_codex_redesign_v1.md` SHA256 `240ceb0433ab58407a274fa80bee26b7d1f1df9e3ee36d44d9a952d464401140`. They were rehashed at closeout.

One documented instruction conflict: the build packet requires a distinct nonzero runner code for no score, while prereg §3 and redesign §3.4 item 7 say no score is INVALID/exit 2. The explicit packet takes precedence: reader INVALID stays 2; runner no-score transport is 3, receipt `reader_exit` is null because there is no exact score to read. Multiple scores are INVALID/2. With an exact score, runner `reader_exit`, `runner_exit`, and `run.rc` preserve the reader return code; its future status is never a reader validity prerequisite. v2 prereg §4 label names supersede §3.3’s older proposed names, without changing the adopted §3.1/§3.4 rules. No other contradiction or unbuildable criterion was found.

Frozen build identities, computed from the standalone pinned clone before any GPU launch:

| Object | Expected identity |
| --- | --- |
| HEAD | `92acd0378d23f4935df9a8bccc0137b36695a40f` |
| patched `edit.py` SHA256 | `92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868` |
| exact Git diff SHA256 | `539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf` |
| edit-time contexts SHA256 | `e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330` |
| scorer contexts prefix | `e8605172dce0` |

The diff uses pinned Git objects, seven-character object abbreviations, fixed prefixes, Myers, no indent heuristic, and three context lines. Setup writes `replay_diff.txt`, `replay_diff.sha256`, and `replay_setup.json`; launch and reader re-derive the actual bytes, including every tracked fixed file. No equality to baseline/winner saved-weight hashes is required for the intentionally different control.

Every adopted gate and its enforcement site:

| Gate | Enforcement (`file:line`) |
| --- | --- |
| 1. Full commit, detached standalone clone, no alternate objects, all fixed tracked bytes, exact science/logging patch and frozen source/diff hashes | setup_replay.sh:17; setup_replay.sh:18; read_replay.py:214; read_replay.py:234; run_replay.sh:115; run_replay.sh:159 |
| 2. Before-dispatch engine fingerprint with pinned program Python and explicit LLMDB_ROOT; nonempty expected three-line output, authoritative SHA and covariance-site count; exact scorer fingerprint retained | run_replay.sh:119; run_replay.sh:126; read_replay.py:517; fixed scorer LAW#5/scope in read_replay.py:553 |
| 3. Immediate source/context print and external full realized-list anchor; exactly three complete records in A1/A2/A7 order, identical rehashed six-template lists, scorer prefix | read_replay.py:122; read_replay.py:154; read_replay.py:530 |
| 4. Exact seven canonical word occurrences, original IDs/offsets, cyclic f+q rule, distinct m positions, no subject/target positions, no shortage fallback, all arm counts at every layer | read_replay.py:42; read_replay.py:90; read_replay.py:139; read_replay.py:367 |
| 4. Same captured forward identity mode; suffix slice equals explicit target-range gather bit-for-bit, finite keys/updates, legal matrix dimensions, identical manifest hash across five layers; original value keys audit-only | read_replay.py:90; read_replay.py:139; read_replay.py:367 |
| 5. Operator paused/no-relaunch window acknowledgement; full ps probe errors propagate; exact runner ancestors/editor/scorer/fingerprint-helper PID ownership, full matches logged; before dispatch, after preflight, during run, after exit | run_replay.sh:42; read_replay.py:291; run_replay.sh:118; run_replay.sh:135; run_replay.sh:151; read_replay.py:580 |
| 5. MPS availability before edit, with availability-only torch preflight; no extra model allocated | run_replay.sh:131; read_replay.py:580 |
| 5. Abort/signal/timeout cleanup verifies the runner-created process group, including recorded scorer/helper after editor exit, and never signals a foreign group | run_replay.sh:64; run_replay.sh:149 |
| 6. Exact seed 0, edit budget 2700, short commit 92acd03; exactly three arms, restricted changed down-projection names at layers 4–8, dimensions, mandatory scalar/vector fields; LAW#5/scope true; A1/A2 integer [68,72] | read_replay.py:425; read_replay.py:553 |
| 7. Refuse clone reuse/prior runs; entropy invocation ID, immutable launch with child identity, exactly one fresh run/score; successful child exit; receipt binds exact score SHA/source/diff/saved hashes/paths | run_replay.sh:31; run_replay.sh:39; run_replay.sh:139; run_replay.sh:177; read_replay.py:500 |
| 7. Reader called on the exact score and receipt, then actual return code appended and copied to run.rc; no latest selection; no-score distinct transport code | run_replay.sh:193; run_replay.sh:194; run_replay.sh:30 |
| 7. Live synthetic rejection; explicit REPLAY_READER_SELFTEST=1 and both paths under /tmp required for marked synthetic reader fixtures; live runner refuses test mode | read_replay.py:472; run_replay.sh:108 |
| 8. Exact registered ordered subject/value/token rows, nonempty values, three boolean hit flags, full implies first, counts agree, 16/8 collision partition and H=C+O, finite legal numbers; strict JSON and JSONL duplicate-key rejection; malformed inputs INVALID/2 | read_replay.py:181; read_replay.py:425; read_replay.py:367; read_replay.py:638 |
| 9. Interpreter/venv/Python/package/OS identities, model/tokenizer revision, complete hparams/screens/engine support/reference/config/tokenizer/shard/covariance byte identities and numeric/device environment, unchanged before/after | read_replay.py:255; read_replay.py:277; run_replay.sh:128; run_replay.sh:160; read_replay.py:561 |
| 9. Reject cache/runtime/model overrides before dispatch; pinned interpreter and actual program-root harness digest checked | run_replay.sh:110; read_replay.py:201; read_replay.py:255 |
| 9 / §4. Exact primary H and secondary C labels, guard recomputation, quality=DEGRADED on locality failure, D/differences/ratios to 88.974 and 131.421, C/O, all per-fact vectors, arm norms, per-layer pre-cast norm and both ||P Kp||F with squared key norms | read_replay.py:337; read_replay.py:342; read_replay.py:139; read_replay.py:472 |

The exclusive-window environment acknowledgement is a launch precondition, not authority to pause or restart the loop. A live caller supplies `REPLAY_EXCLUSIVE_WINDOW=paused-no-relaunch` only while maintaining that window. Full-process polling is every second; it cannot prove that no short-lived foreign job ran between snapshots. Receipts detect accidental stale/cross-run association under a trusted runner; they are not cryptographic proof against a fabricating owner. Fidelity hashes are current before/after identities, not unavailable historical cache identity. Counts/coefficient/inputs are matched; Gram geometry, norm, and direction are not. The historical 18 execution still rests on the stated nocommit/ledger premise. No clean mechanism conclusion or F1 closure follows from these CPU self-tests.

The external advisor auth probe was actually run:

```bash
/opt/homebrew/bin/rtk proxy /Users/robertrhu/.local/bin/claude auth status
```

```text
{
  "loggedIn": false,
  "authMethod": "none",
  "apiProvider": "firstParty",
  "analyticsDisabled": false,
  "projectsDirectory": "/Users/robertrhu/.claude/projects",
  "configDirectory": "/Users/robertrhu/.claude"
}
```

Exit: 1. No completed Claude review is claimed. The permitted fresh Codex fallback reviewed design, exact files, and regression evidence: final verdict PROCEED for the authorized build, weaker independence. Confirmed review defects were fixed: single-token continuation count must permit zero, the scorer’s exact fingerprint helper must be owned, orphan scorer/helper cleanup must run after editor exit, inherited cache redirects must be refused, token IDs must be independently re-encoded, duplicate JSONL and huge-number errors must invalidate, full hits must imply first hits, and scorer extra arguments must be rejected even with spaces in DEST. The initial CLI-tail allegation was retracted after an exact end-of-file read.

The read-only real ps probe was denied in this managed sandbox with `PermissionError: [Errno 1] Operation not permitted: ps`. It was not retried. Process ownership/parser and cleanup controls below therefore use mocked full-process output and mocked signals. MPS availability, live loaded-model gather identity, real edit/scorer behavior, and live exclusivity remain UNVERIFIABLE in this task by its explicit no-GPU/no-torch constraints. No live runner, edit.py, prepare.py, fence script, model loader, tmux action, or commit was executed. Only the cached Rust tokenizer, extracted pure selector/stimulus constructor, isolated standard-library logger/blocklist, compile checks, and mocks were executed.

Actual setup command, diff, and exit:

```bash
/opt/homebrew/bin/rtk proxy experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh /tmp/c10r-exp2loc-selftest-20261006-v2-codex
```

```text
Cloning into '/tmp/c10r-exp2loc-selftest-20261006-v2-codex'...
HEAD is now at 92acd03 edit: preserve keys at the value-token positions (coined value words double as subjects) + overlap/leak diagnostics
READY: /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex
base_commit: 92acd0378d23f4935df9a8bccc0137b36695a40f
runtime_link: /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/.venv -> /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.venv
edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
diff_sha256: 539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf
permitted_diff: PASS (weight 1; common-position gather and inert audit additions only)
diff --git a/edit.py b/edit.py
index 60f49ff..57c5f24 100644
--- a/edit.py
+++ b/edit.py
@@ -12,6 +12,16 @@ Methods the baseline implements:
   AlphaEdit Fang et al. AlphaEdit: Null-Space Constrained Knowledge Editing for Language Models. arXiv:2410.02355
 """
 
+import hashlib
+import json
+import os
+import re
+import sys
+
+_REPLAY_EDIT_PATH = os.path.realpath(__file__)
+with open(_REPLAY_EDIT_PATH, "rb") as _replay_file:
+    _REPLAY_EDIT_SHA256 = hashlib.sha256(_replay_file.read()).hexdigest()
+
 import torch
 
 from prepare import (model, tok, DEV, COV_LAYERS, request, load_hparams, evaluate,
@@ -30,7 +40,7 @@ KL_FACTOR = 0.0625          # weight of the KL term that keeps "<subject> is a"
 V_WEIGHT_DECAY = 0.5        # L2 on delta z during the solve
 RIDGE = 1.0                 # L2 added to the per-layer least-squares solve
 NULL_THRESH = 0.005         # eigenvalues of the key covariance below this span the projector's null space
-PRESERVE_WEIGHT = 1.0       # weight of the keys at the value-token positions in the solve (the write must not fire there)
+PRESERVE_WEIGHT = 1.0       # coefficient of count-matched common-canonical-prefix keys
 
 # ---------------------------------------------------------------------------
 # Setup: hyperparameters, projectors
@@ -57,29 +67,101 @@ WEIGHTS = {l: dict(model.named_parameters())[f"{HP.rewrite_module_tmp.format(l)}
 # ---------------------------------------------------------------------------
 
 
+def select_common_positions(tokenizer, rq, template, fact_i, template_i, ids, tgt):
+    """Frozen seven-word occurrence rule; the original input IDs stay authoritative."""
+    if rq["prompt"] != "The capital of {} is the city of" or template.count("{}") != 1:
+        raise ValueError("unexpected canonical prompt or context wrapper")
+    prefix = template.format(rq["prompt"].format(rq["subject"]))
+    encoded = tokenizer(prefix, return_offsets_mapping=True)
+    if encoded["input_ids"] != ids:
+        raise ValueError("offset mapping changed original prefix IDs")
+    before, after = rq["prompt"].split("{}")
+    lead = len(template.split("{}")[0])
+    subject_span = [lead + len(before), lead + len(before) + len(rq["subject"])]
+    spans = [[m.group(), lead + m.start(), lead + m.end()] for m in re.finditer(r"\S+", before)]
+    spans += [[m.group(), subject_span[1] + m.start(), subject_span[1] + m.end()] for m in re.finditer(r"\S+", after)]
+    candidates = []
+    for word, word_a, word_b in spans:
+        matches = []
+        for idx, (a, b) in enumerate(encoded["offset_mapping"]):
+            if a == b:
+                continue
+            piece = prefix[a:b]
+            aa = a + len(piece) - len(piece.lstrip())
+            bb = b - len(piece) + len(piece.rstrip())
+            if (aa, bb) == (word_a, word_b) and piece.strip() == word:
+                matches.append(idx)
+        if len(matches) != 1:
+            raise ValueError(f"common word must occupy one unambiguous token: {word!r} {matches}")
+        candidates.append(matches[0])
+    if [s[0] for s in spans] != ["The", "capital", "of", "is", "the", "city", "of"] or len(set(candidates)) != 7:
+        raise ValueError("seven distinct canonical word positions required")
+    m = len(tgt)
+    if not 1 <= m <= 7:
+        raise ValueError("target must have 1..7 tokens")
+    indices = [candidates[(fact_i + template_i + j) % 7] for j in range(m)]
+    if len(set(indices)) != m or any(not 0 <= k < len(ids) for k in indices):
+        raise ValueError("control indices must be distinct prefix positions")
+    for idx in indices:
+        a, b = encoded["offset_mapping"][idx]
+        if max(a, subject_span[0]) < min(b, subject_span[1]):
+            raise ValueError("control index overlaps subject")
+    return {"fact_i": fact_i, "template_i": template_i, "subject": rq["subject"],
+            "target": rq["target_new"]["str"], "prefix": prefix, "prefix_ids": ids,
+            "target_ids": tgt, "input_ids": ids + tgt, "offsets": [list(x) for x in encoded["offset_mapping"]],
+            "subject_span": subject_span, "word_spans": spans, "candidates": candidates,
+            "indices": indices, "value_indices": list(range(len(ids), len(ids) + m))}
+
+
 @torch.no_grad()
 def value_keys(layer, requests, ctx):
-    """MLP keys (down_proj inputs) at every token of each fact's value, in context: positions the write must leave alone.
-    Returns [key_dim, n_positions]."""
-    grabbed, cols = [], []
+    """Count-matched common-prefix keys and audit-only original value keys, from the same captured forwards."""
+    grabbed, cols, real_cols, manifest = [], [], [], []
     hook = model.get_submodule(HP.rewrite_module_tmp.format(layer)).register_forward_hook(lambda m, inp, out: grabbed.append(inp[0][0]))
     try:
-        for rq in requests:
+        for fact_i, rq in enumerate(requests):
             tgt = tok(rq["target_new"]["str"], add_special_tokens=False)["input_ids"]
-            for t in [t for group in ctx for t in group]:
+            for template_i, t in enumerate([t for group in ctx for t in group]):
                 ids = tok(t.format(rq["prompt"].format(rq["subject"])))["input_ids"]
+                positions = select_common_positions(tok, rq, t, fact_i, template_i, ids, tgt)
                 grabbed.clear()
                 model(torch.tensor([ids + tgt], device=DEV))
-                cols.append(grabbed[0][len(ids):].float().cpu())
+                if len(grabbed) != 1 or grabbed[0].shape[0] != len(ids) + len(tgt):
+                    raise ValueError("unexpected captured forward shape")
+                original = grabbed[0][len(ids):].float().cpu()
+                identity = grabbed[0][positions["value_indices"]].float().cpu()
+                if not torch.equal(original, identity):
+                    raise ValueError("suffix/explicit-gather primitive identity failed")
+                control = grabbed[0][positions["indices"]].float().cpu()
+                if control.shape != original.shape or not bool(torch.isfinite(control).all()) or not bool(torch.isfinite(original).all()):
+                    raise ValueError("nonfinite or count-mismatched gathered keys")
+                cols.append(control)
+                real_cols.append(original)
+                manifest.append(positions)
     finally:
         hook.remove()
-    return torch.cat(cols).T
+    return torch.cat(cols).T, torch.cat(real_cols).T, manifest
 
 
 def apply_edit(facts):
     """Write facts = [(subject, value)] into the model in place."""
     requests = [request(s, v) for s, v in facts]
     ctx = get_context_templates(model, tok)
+    _replay_context_sha = hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
+    print(f"executed_edit_py_sha256: {_REPLAY_EDIT_SHA256}", flush=True)
+    print(f"edit_context_templates_sha256: {_replay_context_sha}", flush=True)
+    if _replay_context_sha != "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330" or sum(map(len, ctx)) != 6:
+        raise ValueError("edit-time contexts differ from the realized-list anchor")
+    _replay_caller = sys._getframe(1).f_locals
+    _replay_arm = _replay_caller["arm"]
+    _replay_run_dir = os.path.realpath(_replay_caller["run_dir"])
+    _replay_launch_path = os.environ["REPLAY_LAUNCH_PATH"]
+    with open(_replay_launch_path, "rb") as _replay_file:
+        _replay_launch_bytes = _replay_file.read()
+    _replay_launch = json.loads(_replay_launch_bytes)
+    if _replay_launch["invocation_id"] != os.environ["REPLAY_INVOCATION_ID"] or _replay_launch["edit_py_sha256"] != _REPLAY_EDIT_SHA256:
+        raise ValueError("invocation or executed source disagrees with runner launch")
+    _replay_manifest, _replay_layers = None, []
     z_layer = LAYERS[-1]
     zs = torch.stack([compute_z(model, tok, rq, HP, z_layer, ctx) for rq in requests], dim=1)   # target hidden state per fact
 
@@ -91,19 +173,39 @@ def apply_edit(facts):
     gap0 = (zs - current()).norm(dim=0)
     for i, layer in enumerate(LAYERS):
         K = compute_ks(model, tok, requests, HP, layer, ctx).T          # keys at this layer, one column per (fact, template)
-        Kp = value_keys(layer, requests, ctx)                            # keys at the value tokens, one column per (fact, template, token)
+        Kp, _replay_real, _replay_positions = value_keys(layer, requests, ctx)
         resid = (zs - current()).repeat_interleave(K.size(1) // zs.size(1), dim=1) / (len(LAYERS) - i)   # spread the remaining gap over the remaining layers
         Kf, rf = K.float().cpu(), resid.float().cpu()
         A = P[i] @ (Kf @ Kf.T + PRESERVE_WEIGHT * Kp @ Kp.T) + RIDGE * torch.eye(Kf.shape[0])
         B = P[i] @ Kf @ rf.T
         upd = upd_matrix_match_shape(torch.linalg.solve(A, B).T.float(), WEIGHTS[layer].shape)
+        if _replay_manifest is None:
+            _replay_manifest = _replay_positions
+        elif _replay_manifest != _replay_positions:
+            raise ValueError("position manifest changed across layers")
+        _replay_columns = {"A1_single": 144, "A2_coherent2": 288, "A7_coined_coined": 792}[_replay_arm]
+        if list(Kp.shape) != [11008, _replay_columns] or Kp.shape != _replay_real.shape or not bool(torch.isfinite(upd).all()):
+            raise ValueError("invalid preserve-matrix shape or nonfinite update")
+        _replay_layers.append({"layer": layer, "control_columns": Kp.shape[1], "value_columns": _replay_real.shape[1],
+            "key_dim": Kp.shape[0], "update_shape": list(upd.shape), "finite": True, "identity_equal": True,
+            "position_sha256": hashlib.sha256(json.dumps(_replay_positions).encode()).hexdigest(),
+            "control_sumsq": float(Kp.square().sum()), "value_sumsq": float(_replay_real.square().sum()),
+            "control_PKp_fro": float((P[i] @ Kp).norm()), "value_PKp_fro": float((P[i] @ _replay_real).norm()),
+            "update_fro_precast": float(upd.norm())})
         cos = (Kf / Kf.norm(dim=0)).T @ (Kp / Kp.norm(dim=0))
-        print(f"layer {layer}: subject/value key overlap max {cos.max():.2f} mean-of-max {cos.max(1).values.mean():.2f} | "
+        print(f"layer {layer}: Kp_source=common_canonical_prefix subject/preserve key overlap max {cos.max():.2f} mean-of-max {cos.max(1).values.mean():.2f} | "
               f"leak ||dW Kp||/||dW K|| {float((upd @ Kp).norm() / (upd @ Kf).norm()):.3f}", flush=True)
         with torch.no_grad():
             WEIGHTS[layer][...] += upd.to(WEIGHTS[layer].device, WEIGHTS[layer].dtype)
     left = (zs - current()).norm(dim=0) / gap0
     print(f"unrealized residual fraction mean {left.mean():.3f} max {left.max():.3f}", flush=True)
+    _replay_record = {"arm": _replay_arm, "invocation_id": _replay_launch["invocation_id"], "run_dir": _replay_run_dir,
+        "executed_edit_py_sha256": _REPLAY_EDIT_SHA256, "launch_sha256": hashlib.sha256(_replay_launch_bytes).hexdigest(),
+        "edit_context_templates_sha256": _replay_context_sha, "edit_context_templates": ctx,
+        "Kp_source": "common_canonical_prefix", "preserve_weight": PRESERVE_WEIGHT,
+        "positions": _replay_manifest, "layers": _replay_layers}
+    with open(os.path.join(_replay_run_dir, "replay_provenance.jsonl"), "a") as _replay_file:
+        _replay_file.write(json.dumps(_replay_record, allow_nan=False) + "\n")
 
 
 # ---------------------------------------------------------------------------
```

Exit: 0.

The first CPU test attempt exposed the single-token continuation-count schema error. Its unabridged failure output is preserved here; the final reader uses tf_total=3*(ntok-1) and tf_correct in [0,tf_total]. This was a build-validation bug, not a model experiment or scientific result.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /tmp/c10r-exp2loc-selftest-20261006-v2-codex/selftest.py > /tmp/c10r-exp2loc-selftest-20261006-v2-codex/selftest_output.txt 2>&1
```

```text
TEST ONLY: synthetic receipts/norms below are fabricated; no GPU or model execution.
Frozen checkout/diff audit: {"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf"}
COMMAND: bash -n /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh
EXIT: 0
COMMAND: bash -n /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/run_replay.sh
EXIT: 0
Shell syntax and embedded Python: PASS; no runner execution
py_compile: PASS; bytecode confined to scratch, source not executed
Standalone prepare.py:67-76 blocklist:
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
Blocklist hits: []
Standalone name blocklist: PASS (no prepare.py execution/import)
A1_single: pairs=144 columns_per_layer=144 all_5_layers=720
A2_coherent2: pairs=144 columns_per_layer=288 all_5_layers=1440
A7_coined_coined: pairs=144 columns_per_layer=792 all_5_layers=3960
Example: {"subject": "Zorbland", "candidates": [0, 1, 2, 6, 7, 8, 9], "indices": [0, 1, 2, 6], "target_ids": [647, 1252, 647, 1073]}
Own patched selector: PASS all 432 pairs; registered rows match pinned stimulus builder
Original forward/solve/cast/update expressions: PASS unchanged
torch imported: False
executed_edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
executed_edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
executed_edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
Logger/caller-local contract: PASS three complete arm records; immediate context prints above
COMMAND: LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
EXIT: 0

CASE: recorded_20261006-131156_nocommit
COMMAND: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/missing_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget"], "path": "/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json"}
VALIDITY receipt_json: FAIL value="[Errno 2] No such file or directory: '/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/missing_receipt.json'"
VALIDITY registered_schema_vectors: FAIL value="invalid teacher-forced dimensions"
VALIDITY live_or_explicit_tmp_selftest: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY frozen_checkout_source_diff: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fresh_invocation_score_receipt: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY engine_fingerprint_explicit_root: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY three_arm_context_source_records: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A1_single: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fidelity_before_after: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY exclusive_processes_mps: FAIL value="receipt/score unavailable; this gate is unverifiable"
INVALID
HALT: receipt_json, registered_schema_vectors, live_or_explicit_tmp_selftest, frozen_checkout_source_diff, fresh_invocation_score_receipt, engine_fingerprint_explicit_root, three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined, fixed_metadata_controls_law5_scope, fidelity_before_after, exclusive_processes_mps; no binding label
EXIT: 2
ASSERTIONS: PASS recorded_20261006-131156_nocommit
Traceback (most recent call last):
  File "/tmp/c10r-exp2loc-selftest-20261006-v2-codex/selftest.py", line 190, in <module>
    assert 'NON-BINDING count-only labels:' in output
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

Initial exit: 1. Corrected tests follow.

Required CPU self-tests. The fixture norms, process/MPS receipts, and cache digests are explicitly synthetic; the selector indices and registered stimulus mapping use the actual cached tokenizer. Passing synthetic labels demonstrate the reader path, not a measured result.

Exact test source (all test-only files were in the scratch clone):

```python
import ast
import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import py_compile
import re
import runpy
import subprocess
import sys
from unittest.mock import patch
from tokenizers import Tokenizer

PROGRAM = Path('/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a')
DRIVER = PROGRAM / 'experiments/track_c/autoresearch_c10/replay_exp2'
ROOT = Path(__file__).resolve().parent
m = runpy.run_path(str(DRIVER / 'read_replay.py'))
assert 'torch' not in sys.modules
print('TEST ONLY: synthetic receipts/norms below are fabricated; no GPU or model execution.')
audit = m['inspect_replay'](ROOT)
print('Frozen checkout/diff audit:', json.dumps({k:v for k,v in audit.items() if k != 'diff'}))
for name in ('setup_replay.sh', 'run_replay.sh'):
    cmd = ['bash', '-n', str(DRIVER / name)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print('COMMAND:', ' '.join(cmd)); print(result.stdout + result.stderr, end=''); print('EXIT:', result.returncode)
    assert result.returncode == 0
    embedded = (DRIVER / name).read_text().split("<<'PY'\n", 1)[1].rsplit('\nPY\n', 1)[0]
    compile(embedded, '<shell embedded Python syntax only>', 'exec')
print('Shell syntax and embedded Python: PASS; no runner execution')
py_compile.compile(str(ROOT / 'edit.py'), cfile=str(ROOT / 'edit_selftest.pyc'), doraise=True)
py_compile.compile(str(DRIVER / 'read_replay.py'), cfile=str(ROOT / 'reader_selftest.pyc'), doraise=True)
print('py_compile: PASS; bytecode confined to scratch, source not executed')
prepare = (ROOT / 'prepare.py').read_text().split('\n')
print('Standalone prepare.py:67-76 blocklist:')
print('\n'.join(prepare[66:76]))
ns = {'HERE': str(ROOT), 'os': os}
exec(compile('\n'.join(prepare[66:76]), '<prepare-name-blocklist-only>', 'exec'), ns)
print('Blocklist hits:', ns['_hits']); assert ns['_hits'] == []
print('Standalone name blocklist: PASS (no prepare.py execution/import)')

ctx_line = next(x for x in (PROGRAM / 'results/autoresearch_c10_equivalence_rerun.log').read_text().splitlines() if 'Cached context templates [[' in x)
ctx = ast.literal_eval(ctx_line.split('Cached context templates ', 1)[1])
assert m['sha_json'](ctx) == m['CONTEXT_SHA']
flat = [t for g in ctx for t in g]
tokenizer_path = PROGRAM / f'hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/{m["MODEL_REV"]}/tokenizer.json'
backend = Tokenizer.from_file(str(tokenizer_path))
class CachedTokenizer:
    def __call__(self, text, add_special_tokens=True, return_offsets_mapping=False):
        enc = backend.encode(text, add_special_tokens=add_special_tokens)
        result = {'input_ids': enc.ids}
        if return_offsets_mapping:
            result['offset_mapping'] = enc.offsets
        return result
tok = CachedTokenizer()
tree = ast.parse((ROOT / 'edit.py').read_text())
selector = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'select_common_positions')
namespace = {'re': re}
exec(compile(ast.Module(body=[selector], type_ignores=[]), '<patched-own-selector-only>', 'exec'), namespace)
select = namespace['select_common_positions']

# Check frozen registered rows against the pinned harness's own stimulus constructor.
harness_tree = ast.parse((ROOT / 'c10e_bandknob.py').read_text())
fiction = next(ast.literal_eval(n.value) for n in harness_tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'FICTION' and isinstance(n.value, ast.List))
builder = next(n for n in harness_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build_stimuli')
stimulus_ns = {'json': json, 'LLMDB_ROOT': str(PROGRAM), 'FICTION': fiction,
               'single_tok': lambda text: len(tok(' ' + text, add_special_tokens=False)['input_ids']) == 1,
               'ntok': lambda text: len(tok(' ' + text, add_special_tokens=False)['input_ids'])}
exec(compile(ast.Module(body=[builder], type_ignores=[]), '<pinned-stimuli-only>', 'exec'), stimulus_ns)
stimuli = stimulus_ns['build_stimuli']()
manifest = {}
checks = 0
for arm in m['ARMS']:
    rows = []
    for f, (subject, value, ntok) in enumerate(m['FROZEN_ROWS'][arm]):
        assert stimuli[arm][subject] == value
        rq = {'prompt': m['CANON'], 'subject': subject, 'target_new': {'str': ' ' + value}}
        tgt = tok(rq['target_new']['str'], add_special_tokens=False)['input_ids']
        assert len(tgt) == ntok
        for q, template in enumerate(flat):
            ids = tok(template.format(m['CANON'].format(subject)))['input_ids']
            positions = select(tok, rq, template, f, q, ids, tgt)
            assert positions == select(tok, rq, template, f, q, ids, tgt)
            assert len(positions['indices']) == len(set(positions['indices'])) == ntok
            rows.append(positions); checks += 1
    manifest[arm] = rows
    columns = sum(len(r['indices']) for r in rows)
    assert columns == m['COLUMNS'][arm]
    print(f'{arm}: pairs={len(rows)} columns_per_layer={columns} all_5_layers={5*columns}')
assert checks == 432
example = manifest['A7_coined_coined'][0]
assert example['candidates'] == [0,1,2,6,7,8,9] and example['indices'] == [0,1,2,6]
print('Example:', json.dumps({k:example[k] for k in ('subject','candidates','indices','target_ids')}))
print('Own patched selector: PASS all 432 pairs; registered rows match pinned stimulus builder')
original = m['git'](ROOT, 'show', m['BASE_COMMIT'] + ':edit.py')
patched = (ROOT / 'edit.py').read_text()
for line in original.splitlines():
    if any(x in line for x in ('A = P[i]', 'B = P[i]', 'upd = upd_matrix_match_shape', 'WEIGHTS[layer][...] +=', 'model(torch.tensor([ids + tgt]')):
        assert line in patched
print('Original forward/solve/cast/update expressions: PASS unchanged')
assert 'torch' not in sys.modules
print('torch imported:', 'torch' in sys.modules)

# Standard-library-only logger test against the evaluator's actual caller-local contract.
run_dir = ROOT / 'runs/20261006-000000_92acd03'
run_dir.mkdir(parents=True, exist_ok=True)
for name in ('replay_provenance.jsonl', 'score.json'):
    path=run_dir/name
    if path.exists(): path.unlink()
launch = {k:audit[k] for k in ('base_commit','dest','edit_py_sha256','diff_sha256')}
launch.update(invocation_id='c'*32, program_root=str(PROGRAM), context_sha256=m['CONTEXT_SHA'], initial_runs=[], runner_pid=12345, child_pid=23456)
fidelity = {'interpreter': str((PROGRAM/'.venv/bin/python').resolve()), 'python_version':sys.version,
            'venv':str((PROGRAM/'.venv').resolve()), 'packages':{x:importlib.metadata.version(x) for x in ('torch','transformers','tokenizers','numpy','safetensors','accelerate')},
            'os': platform.platform(), 'model_id':'Qwen/Qwen2.5-3B', 'model_revision':m['MODEL_REV'], 'tokenizer_revision':m['MODEL_REV'],
            'numeric_env':{key:os.environ.get(key) for key in ('LLMDB_DEVICE','PYTORCH_MPS_FAST_MATH','PYTORCH_ENABLE_MPS_FALLBACK','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS')},
            'files':{str(p):{'resolved_path':str(p.resolve(strict=True)), 'sha256':'1'*64} for p in m['fidelity_inputs'](ROOT)}}
launch['fidelity_before'] = fidelity
launch_path = ROOT/'replay_launch.json'
launch_path.write_text(json.dumps(launch, indent=2)+'\n')
log_ns = {'__file__':str(ROOT/'edit.py'), 'PRESERVE_WEIGHT':1.0}
exec(compile(m['IMPORT_LOG'], '<logger-imports-only>', 'exec'), log_ns)
exec(compile('def start_logging(ctx):\n'+m['CONTEXT_LOG']+'    return locals()\n', '<logger-start-only>', 'exec'), log_ns)
exec(compile('def finish_logging():\n'+m['FINAL_LOG'], '<logger-finish-only>', 'exec'), log_ns)
os.environ['REPLAY_LAUNCH_PATH'] = str(launch_path)
os.environ['REPLAY_INVOCATION_ID'] = launch['invocation_id']
def caller(arm):
    run_dir = str(ROOT/'runs/20261006-000000_92acd03')
    return log_ns['start_logging'](ctx)
for arm in m['ARMS']:
    state = caller(arm)
    positions = manifest[arm]
    state['_replay_manifest'] = positions
    state['_replay_layers'] = [{'layer':layer, 'control_columns':m['COLUMNS'][arm], 'value_columns':m['COLUMNS'][arm],
                              'key_dim':11008, 'update_shape':[2048,11008], 'finite':True, 'identity_equal':True,
                              'position_sha256':m['sha_json'](positions), 'control_sumsq':float(layer), 'value_sumsq':float(layer+1),
                              'control_PKp_fro':float(layer+2), 'value_PKp_fro':float(layer+3), 'update_fro_precast':float(layer+4)} for layer in m['LAYERS']]
    log_ns.update(state)
    log_ns['finish_logging']()
provenance_path = run_dir/'replay_provenance.jsonl'
records = [json.loads(x) for x in provenance_path.read_text().splitlines()]
assert [r['arm'] for r in records] == list(m['ARMS'])
assert all(m['validate_positions'](r) for r in records)
print('Logger/caller-local contract: PASS three complete arm records; immediate context prints above')

fp_cmd = [str(PROGRAM/'.venv/bin/python'), '-B', str(PROGRAM/'tools/engine_fingerprint.py')]
fp = subprocess.run(fp_cmd, env={**os.environ,'LLMDB_ROOT':str(PROGRAM)}, capture_output=True, text=True)
print('COMMAND: LLMDB_ROOT='+str(PROGRAM)+' '+' '.join(fp_cmd)); print(fp.stdout+fp.stderr,end=''); print('EXIT:',fp.returncode)
assert fp.returncode == 0
process_events = [{'phase':phase, 'probe_exit':0, 'process_count':50, 'runner_pid':12345, 'own_chain':[1,12345], 'child_pid':23456 if phase in ('during_run','after_exit') else None,
                   'owned_children':[], 'matches':[], 'foreign':[], 'ok':True} for phase in ('before_dispatch','after_preflight','during_run','after_exit')]
process_path = ROOT/'process_exclusion.jsonl'
process_path.write_text(''.join(json.dumps(x)+'\n' for x in process_events))
recorded = Path('/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/score.json')
score = json.loads(recorded.read_text())
score['synthetic_fixture'] = True
score['edits']['commit'] = '92acd03'
score_path = run_dir/'score.json'
score_path.write_text(json.dumps(score)+'\n')
receipt = {'synthetic_fixture':True, 'invocation_id':launch['invocation_id'], 'dest':str(ROOT), 'run_dir':str(run_dir), 'score_path':str(score_path),
           'base_commit':m['BASE_COMMIT'], 'edit_py_sha256':audit['edit_py_sha256'], 'diff_sha256':audit['diff_sha256'], 'score_sha256':m['sha_file'](score_path),
           'saved_sha256':score['saved_sha256'], 'child_exit':0, 'child_pid':23456, 'runner_pid':12345, 'owned_children':[], 'failures':[], 'launch':launch,
           'fidelity_before':fidelity, 'fidelity_after':fidelity,
           'engine_fingerprint':{'exit':fp.returncode, 'stdout':fp.stdout, 'stderr':fp.stderr, 'LLMDB_ROOT':str(PROGRAM), 'interpreter':str(PROGRAM/'.venv/bin/python')},
           'mps_preflight':{'exit':0,'stdout':'MPS_AVAILABLE=true\n','stderr':''}, 'exclusive_window':'paused-no-relaunch', 'process_log_sha256':m['sha_file'](process_path)}
receipt_path = ROOT/'runner_receipt.json'
receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
base_provenance = provenance_path.read_text()
base_score = copy.deepcopy(score)
base_receipt = copy.deepcopy(receipt)

def reader_case(name, input_score, input_receipt, expected, selftest=True):
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE':'1'}
    if selftest: env['REPLAY_READER_SELFTEST']='1'
    else: env.pop('REPLAY_READER_SELFTEST',None)
    cmd = [sys.executable,'-B',str(DRIVER/'read_replay.py'),str(input_score),str(input_receipt)]
    print('\nCASE:',name)
    print('COMMAND:',('REPLAY_READER_SELFTEST=1 ' if selftest else '')+' '.join(cmd))
    result = subprocess.run(cmd, env=env, capture_output=True,text=True)
    print(result.stdout+result.stderr,end=''); print('EXIT:',result.returncode)
    assert result.returncode == expected,(name,result.returncode)
    if expected == 2:
        assert 'INVALID\n' in result.stdout and '\nLABEL ' not in result.stdout
    else:
        assert '\nLABEL primary=' in result.stdout and 'NON-BINDING' not in result.stdout
    print('ASSERTIONS: PASS',name)
    return result.stdout

for name in ('20261006-131156_nocommit','20261006-142644_nocommit'):
    old_score = Path('/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs')/name/'score.json'
    output = reader_case('recorded_'+name, old_score, ROOT/'missing_receipt.json', 2, False)
    assert 'NON-BINDING count-only labels:' in output
reader_case('synthetic_full_provenance',score_path,receipt_path,0)
reader_case('synthetic_live_acceptance_rejected',score_path,receipt_path,2,False)

for name in ('empty_value','missing_key','wrong_record_count','wrong_context_hash','wrong_commit','gather_identity_false','wrong_column_count','wrong_invocation','changed_fidelity','guard_degraded'):
    s,r = copy.deepcopy(base_score),copy.deepcopy(base_receipt)
    rs = [json.loads(x) for x in base_provenance.splitlines()]
    expected=2
    if name=='empty_value': s['arms']['A7_coined_coined']['rows'][0]['val']=''
    elif name=='missing_key': del s['summary']['dw_total']
    elif name=='wrong_record_count': rs.pop()
    elif name=='wrong_context_hash': rs[0]['edit_context_templates_sha256']='0'*64
    elif name=='wrong_commit': s['edits']['commit']='nocommit'
    elif name=='gather_identity_false': rs[0]['layers'][0]['identity_equal']=False
    elif name=='wrong_column_count': rs[2]['layers'][0]['control_columns']=791
    elif name=='wrong_invocation': r['invocation_id']='d'*32
    elif name=='changed_fidelity': r['fidelity_after']['packages']['torch']='wrong'
    elif name=='guard_degraded':
        s['summary'].update(L1_flips=2,guards='failed:L1_flips')
        s['arms']['A7_coined_coined']['locality_axes']['L1_flipped_to_edited_value']=2
        expected=0
    provenance_path.write_text(''.join(json.dumps(x)+'\n' for x in rs))
    score_path.write_text(json.dumps(s)+'\n')
    r['score_sha256']=m['sha_file'](score_path)
    receipt_path.write_text(json.dumps(r,indent=2)+'\n')
    output=reader_case(name,score_path,receipt_path,expected)
    if name=='guard_degraded': assert 'quality=DEGRADED' in output and 'FULL-GAIN-WITHOUT-VALUE-POSITIONS' in output
provenance_path.write_text(base_provenance)
score_path.write_text(json.dumps(base_score)+'\n')
base_receipt['score_sha256']=m['sha_file'](score_path)
receipt_path.write_text(json.dumps(base_receipt,indent=2)+'\n')
for h,label in ((0,'NO-GAIN-WITHOUT-VALUE-POSITIONS'),(7,'NO-GAIN-WITHOUT-VALUE-POSITIONS'),(8,'PARTIAL-GAIN'),(17,'PARTIAL-GAIN'),(18,'FULL-GAIN-WITHOUT-VALUE-POSITIONS'),(72,'FULL-GAIN-WITHOUT-VALUE-POSITIONS')):
    assert m['primary_label'](h)==label; print('PRIMARY BOUNDARY',h,label,'PASS')
for c,label in ((0,'NO-COLLISION-RECOVERY'),(1,'PARTIAL-COLLISION-RECOVERY'),(12,'PARTIAL-COLLISION-RECOVERY'),(13,'FULL-COLLISION-RECOVERY'),(48,'FULL-COLLISION-RECOVERY')):
    assert m['secondary_label'](c)==label; print('SECONDARY BOUNDARY',c,label,'PASS')
for bad in (True,7.0,-1,73):
    try: m['primary_label'](bad)
    except ValueError: print('ILLEGAL COUNT',repr(bad),'PASS rejected')
    else: raise AssertionError('illegal count accepted')

# Mock only ps: no actual process probe or model job is run in this sandbox.
pid=os.getpid(); child=300001; scorer=300002
stamp='Tue Oct 6 12:00:00 2026'
def row(p,pp,cmd): return f'{p} {pp} {stamp} {cmd}\n'
base=row(pid,1,'python selftest.py')+row(1,0,'launchd')
for name,body,expected in (
    ('foreign_generic_Python',base+row(300003,1,'/other/.venv/bin/Python arbitrary_stage.py'),False),
    ('foreign_notebook',base+row(300003,1,'jupyter-lab'),False),
    ('foreign_loop',base+row(300003,1,'safe-mode --loop'),False),
    ('owned_editor_scorer',base+row(child,pid,str(ROOT/'.venv/bin/python')+' -B edit.py')+row(scorer,child,str(PROGRAM/'.venv/bin/python')+' '+str(ROOT/'prepare.py')+' --score '+str(run_dir)),True),
    ('owned_scorer_fingerprint',base+row(child,pid,str(ROOT/'.venv/bin/python')+' -B edit.py')+row(scorer,child,str(PROGRAM/'.venv/bin/python')+' '+str(ROOT/'prepare.py')+' --score '+str(run_dir))+row(300004,scorer,str(PROGRAM/'.venv/bin/python')+' '+str(PROGRAM/'tools/engine_fingerprint.py')),True),
    ('unowned_descendant_Python',base+row(child,pid,'python edit.py')+row(scorer,child,'python unrelated.py'),False)):
    fake=subprocess.CompletedProcess(['ps'],0,body,'')
    with patch.object(m['subprocess'],'run',return_value=fake): event=m['process_check']('during_run',child,ROOT)
    assert event['ok'] is expected,(name,event)
    print('MOCK PROCESS',name,'PASS ok='+str(event['ok'])+' foreign='+json.dumps(event['foreign']))
with patch.object(m['subprocess'],'run',side_effect=PermissionError('sandbox denies ps')):
    try: m['process_check']('before_dispatch')
    except PermissionError: print('MOCK PROCESS probe_failure: PASS propagated, no silent fallback')
    else: raise AssertionError('process failure swallowed')
for name in ('edit.py','prepare.py','program.md'):
    path=ROOT/name; before=path.read_bytes()
    try:
        path.write_bytes(before+b'\nUNPERMITTED = 1\n')
        try: m['inspect_replay'](ROOT)
        except ValueError as exc: print('TAMPER',name,'PASS refused:',exc)
        else: raise AssertionError('unpermitted tracked edit accepted')
    finally: path.write_bytes(before)
assert m['inspect_replay'](ROOT)==audit
cmd=[str(DRIVER/'setup_replay.sh'),str(ROOT)]
result=subprocess.run(cmd,capture_output=True,text=True)
print('COMMAND:',' '.join(cmd)); print(result.stdout+result.stderr,end=''); print('EXIT:',result.returncode)
assert result.returncode==2
assert 'torch' not in sys.modules
print('torch imported:', 'torch' in sys.modules)
print('ALL REQUIRED CPU SELF-TESTS: PASS')
```

Actual command:

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /tmp/c10r-exp2loc-selftest-20261006-v2-codex/selftest.py > /tmp/c10r-exp2loc-selftest-20261006-v2-codex/selftest_output.txt 2>&1
```

Actual output, verbatim:

```text
TEST ONLY: synthetic receipts/norms below are fabricated; no GPU or model execution.
Frozen checkout/diff audit: {"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf"}
COMMAND: bash -n /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh
EXIT: 0
COMMAND: bash -n /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/run_replay.sh
EXIT: 0
Shell syntax and embedded Python: PASS; no runner execution
py_compile: PASS; bytecode confined to scratch, source not executed
Standalone prepare.py:67-76 blocklist:
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
Blocklist hits: []
Standalone name blocklist: PASS (no prepare.py execution/import)
A1_single: pairs=144 columns_per_layer=144 all_5_layers=720
A2_coherent2: pairs=144 columns_per_layer=288 all_5_layers=1440
A7_coined_coined: pairs=144 columns_per_layer=792 all_5_layers=3960
Example: {"subject": "Zorbland", "candidates": [0, 1, 2, 6, 7, 8, 9], "indices": [0, 1, 2, 6], "target_ids": [647, 1252, 647, 1073]}
Own patched selector: PASS all 432 pairs; registered rows match pinned stimulus builder
Original forward/solve/cast/update expressions: PASS unchanged
torch imported: False
executed_edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
executed_edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
executed_edit_py_sha256: 92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
Logger/caller-local contract: PASS three complete arm records; immediate context prints above
COMMAND: LLMDB_ROOT=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/engine_fingerprint.py
engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py
  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a…)
  _cov_cpu 3  (expected 3)
EXIT: 0

CASE: recorded_20261006-131156_nocommit
COMMAND: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/missing_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget"], "path": "/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-131156_nocommit/score.json"}
VALIDITY receipt_json: FAIL value="[Errno 2] No such file or directory: '/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/missing_receipt.json'"
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 7, "described_as": 90.38, "dw_total": 88.974, "edit_seconds": 1376.4, "first_token": 40, "frame_flips": 1, "guards": "ok", "heldout_full": 7, "law5_ok": true, "ppl_post": 21.506, "scope_ok": true, "score_seconds": 592.1}, 0, 7]
VALIDITY live_or_explicit_tmp_selftest: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY frozen_checkout_source_diff: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fresh_invocation_score_receipt: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY engine_fingerprint_explicit_root: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY three_arm_context_source_records: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A1_single: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fidelity_before_after: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY exclusive_processes_mps: FAIL value="receipt/score unavailable; this gate is unverifiable"
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=90.38 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.506 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 0, "D": 88.974, "D_minus_131.421": -42.44699999999999, "D_minus_88.974": 0.0, "D_over_131.421": 0.6770150889127309, "D_over_88.974": 1.0, "H": 7, "O": 7, "arm_dw_total": {"A1_single": 85.505, "A2_coherent2": 85.798, "A7_coined_coined": 88.974}, "quality": "OK", "saved_sha256": {"A1_single": "2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1", "A2_coherent2": "f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56", "A7_coined_coined": "c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 7, "described_as": 90.38, "dw_total": 88.974, "edit_seconds": 1376.4, "first_token": 40, "frame_flips": 1, "guards": "ok", "heldout_full": 7, "law5_ok": true, "ppl_post": 21.506, "scope_ok": true, "score_seconds": 592.1}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, false], "para_first_hits": [true, false, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, true, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, true, false], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [true, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, true], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, false, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, true, true], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": false}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=NO-GAIN-WITHOUT-VALUE-POSITIONS secondary=NO-COLLISION-RECOVERY quality=OK
INVALID
HALT: receipt_json, live_or_explicit_tmp_selftest, frozen_checkout_source_diff, fresh_invocation_score_receipt, engine_fingerprint_explicit_root, three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined, fixed_metadata_controls_law5_scope, fidelity_before_after, exclusive_processes_mps; no binding label
EXIT: 2
ASSERTIONS: PASS recorded_20261006-131156_nocommit

CASE: recorded_20261006-142644_nocommit
COMMAND: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/missing_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget"], "path": "/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/score.json"}
VALIDITY receipt_json: FAIL value="[Errno 2] No such file or directory: '/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/missing_receipt.json'"
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY frozen_checkout_source_diff: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fresh_invocation_score_receipt: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY engine_fingerprint_explicit_root: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY three_arm_context_source_records: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A1_single: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fidelity_before_after: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY exclusive_processes_mps: FAIL value="receipt/score unavailable; this gate is unverifiable"
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: receipt_json, live_or_explicit_tmp_selftest, frozen_checkout_source_diff, fresh_invocation_score_receipt, engine_fingerprint_explicit_root, three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined, fixed_metadata_controls_law5_scope, fidelity_before_after, exclusive_processes_mps; no binding label
EXIT: 2
ASSERTIONS: PASS recorded_20261006-142644_nocommit

CASE: synthetic_full_provenance
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
SYNTHETIC SELF-TEST: label-path demonstration only; no measured or binding scientific result
LABEL primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
EXIT: 0
ASSERTIONS: PASS synthetic_full_provenance

CASE: synthetic_live_acceptance_rejected
COMMAND: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: FAIL value="synthetic fixture forbidden for live acceptance"
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: live_or_explicit_tmp_selftest; no binding label
EXIT: 2
ASSERTIONS: PASS synthetic_live_acceptance_rejected

CASE: empty_value
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: FAIL value="empty/malformed value"
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "437186818f6655bb2feff2c27b4dc847b55926402d0af0de191e635bff3a3f38"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="LAW#5/scope failed"
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
INVALID
HALT: registered_schema_vectors, fixed_metadata_controls_law5_scope; no binding label
EXIT: 2
ASSERTIONS: PASS empty_value

CASE: missing_key
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: FAIL value="'dw_total'"
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "d3ec039c29b481a237259c92e050906b52217f89d9ee14aa1e7e55a03e4ad62c"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="LAW#5/scope failed"
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
INVALID
HALT: registered_schema_vectors, fixed_metadata_controls_law5_scope; no binding label
EXIT: 2
ASSERTIONS: PASS missing_key

CASE: wrong_record_count
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: FAIL value="exactly three complete arm records in fixed order required"
VALIDITY count_position_primitive_A1_single: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined; no binding label
EXIT: 2
ASSERTIONS: PASS wrong_record_count

CASE: wrong_context_hash
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: FAIL value="wrong full edit-time context hash"
VALIDITY count_position_primitive_A1_single: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined; no binding label
EXIT: 2
ASSERTIONS: PASS wrong_context_hash

CASE: wrong_commit
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "468464805e55d393c82362ebded5780b2a621c97cc6ac39a4e1c96f1daad7f20"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="wrong score commit"
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: fixed_metadata_controls_law5_scope; no binding label
EXIT: 2
ASSERTIONS: PASS wrong_commit

CASE: gather_identity_false
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: FAIL value="nonfinite data or gather primitive identity failure"
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: count_position_primitive_A1_single; no binding label
EXIT: 2
ASSERTIONS: PASS gather_identity_false

CASE: wrong_column_count
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="per-layer column count mismatch"
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: count_position_primitive_A7_coined_coined; no binding label
EXIT: 2
ASSERTIONS: PASS wrong_column_count

CASE: wrong_invocation
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "dddddddddddddddddddddddddddddddd", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: FAIL value="invalid/mismatched invocation id"
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: FAIL value="cross-run arm record"
VALIDITY count_position_primitive_A1_single: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: fresh_invocation_score_receipt, three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined; no binding label
EXIT: 2
ASSERTIONS: PASS wrong_invocation

CASE: changed_fidelity
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: FAIL value="launch association or fresh-start assertion failed"
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "9ae4b6163d86f294a6e822b276061d1ca036626bc2461497739d9bd275d29de0", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "wrong", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: fresh_invocation_score_receipt; no binding label
EXIT: 2
ASSERTIONS: PASS changed_fidelity

CASE: guard_degraded
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 2, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "failed:L1_flips", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "0d6ff743d054afe1d423521e28e32e8016a907f3f1b0e66df31d358d87ef3fc8"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: FAIL value=2 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="failed:L1_flips"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "DEGRADED", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 2, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "failed:L1_flips", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
SYNTHETIC SELF-TEST: label-path demonstration only; no measured or binding scientific result
LABEL primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=DEGRADED
EXIT: 0
ASSERTIONS: PASS guard_degraded
PRIMARY BOUNDARY 0 NO-GAIN-WITHOUT-VALUE-POSITIONS PASS
PRIMARY BOUNDARY 7 NO-GAIN-WITHOUT-VALUE-POSITIONS PASS
PRIMARY BOUNDARY 8 PARTIAL-GAIN PASS
PRIMARY BOUNDARY 17 PARTIAL-GAIN PASS
PRIMARY BOUNDARY 18 FULL-GAIN-WITHOUT-VALUE-POSITIONS PASS
PRIMARY BOUNDARY 72 FULL-GAIN-WITHOUT-VALUE-POSITIONS PASS
SECONDARY BOUNDARY 0 NO-COLLISION-RECOVERY PASS
SECONDARY BOUNDARY 1 PARTIAL-COLLISION-RECOVERY PASS
SECONDARY BOUNDARY 12 PARTIAL-COLLISION-RECOVERY PASS
SECONDARY BOUNDARY 13 FULL-COLLISION-RECOVERY PASS
SECONDARY BOUNDARY 48 FULL-COLLISION-RECOVERY PASS
ILLEGAL COUNT True PASS rejected
ILLEGAL COUNT 7.0 PASS rejected
ILLEGAL COUNT -1 PASS rejected
ILLEGAL COUNT 73 PASS rejected
MOCK PROCESS foreign_generic_Python PASS ok=False foreign=[{"pid": 300003, "ppid": 1, "start": "Tue Oct 6 12:00:00 2026", "command": "/other/.venv/bin/Python arbitrary_stage.py"}]
MOCK PROCESS foreign_notebook PASS ok=False foreign=[{"pid": 300003, "ppid": 1, "start": "Tue Oct 6 12:00:00 2026", "command": "jupyter-lab"}]
MOCK PROCESS foreign_loop PASS ok=False foreign=[{"pid": 300003, "ppid": 1, "start": "Tue Oct 6 12:00:00 2026", "command": "safe-mode --loop"}]
MOCK PROCESS owned_editor_scorer PASS ok=True foreign=[]
MOCK PROCESS owned_scorer_fingerprint PASS ok=True foreign=[]
MOCK PROCESS unowned_descendant_Python PASS ok=False foreign=[{"pid": 300002, "ppid": 300001, "start": "Tue Oct 6 12:00:00 2026", "command": "python unrelated.py"}]
MOCK PROCESS probe_failure: PASS propagated, no silent fallback
TAMPER edit.py PASS refused: unpermitted tracked-file change: edit.py
TAMPER prepare.py PASS refused: unpermitted tracked-file change: prepare.py
TAMPER program.md PASS refused: unpermitted tracked-file change: program.md
COMMAND: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex
REFUSED: DEST already exists: /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex
EXIT: 2
torch imported: False
ALL REQUIRED CPU SELF-TESTS: PASS
```

Exit: 0.

Additional reviewer regressions. The fixture norms, process/MPS receipts, and cache digests are explicitly synthetic; the selector indices and registered stimulus mapping use the actual cached tokenizer. Passing synthetic labels demonstrate the reader path, not a measured result.

Exact test source (all test-only files were in the scratch clone):

```python
import ast
import copy
import json
import os
from pathlib import Path
import runpy
import signal
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import Mock

ROOT=Path(__file__).resolve().parent
PROGRAM=Path('/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a')
DRIVER=PROGRAM/'experiments/track_c/autoresearch_c10/replay_exp2'
m=runpy.run_path(str(DRIVER/'read_replay.py'))
score_path=next(ROOT.glob('runs/*/score.json')); receipt_path=ROOT/'runner_receipt.json'
provenance_path=score_path.parent/'replay_provenance.jsonl'
score_raw=score_path.read_text(); receipt_raw=receipt_path.read_text(); provenance_raw=provenance_path.read_text()
base_score=json.loads(score_raw); base_receipt=json.loads(receipt_raw)
try:
    for name in ('changed_prefix_id','duplicate_jsonl_key','full_without_first','huge_integer','malformed_json','nonfinite_json'):
        score=copy.deepcopy(base_score); receipt=copy.deepcopy(base_receipt)
        records=[json.loads(x) for x in provenance_raw.splitlines()]
        if name=='changed_prefix_id':
            row=records[0]['positions'][0]
            row['prefix_ids'][0]+=1; row['input_ids']=row['prefix_ids']+row['target_ids']
            for layer in records[0]['layers']: layer['position_sha256']=m['sha_json'](records[0]['positions'])
        elif name=='full_without_first':
            arm=score['arms']['A7_coined_coined']; row=next(r for r in arm['rows'] if any(r['para_full_hits']))
            index=row['para_full_hits'].index(True); row['para_first_hits'][index]=False
            arm['para_first_n']=sum(sum(r['para_first_hits']) for r in arm['rows']); score['summary']['first_token']=arm['para_first_n']
        elif name=='huge_integer': score['summary']['dw_total']=10**500
        provenance=''.join(json.dumps(r)+'\n' for r in records)
        if name=='duplicate_jsonl_key': provenance=provenance.replace('"finite": true', '"finite": false, "finite": true',1)
        provenance_path.write_text(provenance)
        raw=json.dumps(score)+'\n'
        if name=='malformed_json': raw='{'
        if name=='nonfinite_json': raw=raw.replace('"dw_total": 131.421','"dw_total": NaN',1)
        score_path.write_text(raw); receipt['score_sha256']=m['sha_file'](score_path); receipt_path.write_text(json.dumps(receipt)+'\n')
        cmd=[sys.executable,'-B',str(DRIVER/'read_replay.py'),str(score_path),str(receipt_path)]
        print('CASE:',name); print('COMMAND: REPLAY_READER_SELFTEST=1 '+' '.join(cmd))
        result=subprocess.run(cmd,env={**os.environ,'REPLAY_READER_SELFTEST':'1','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
        print(result.stdout+result.stderr,end=''); print('EXIT:',result.returncode)
        assert result.returncode==2 and 'INVALID\n' in result.stdout and '\nLABEL ' not in result.stdout
        print('ASSERTIONS: PASS',name)
finally:
    score_path.write_text(score_raw); receipt_path.write_text(receipt_raw); provenance_path.write_text(provenance_raw)

# Extract only cleanup; all process/signal effects are replaced by mocks.
runner=(DRIVER/'run_replay.sh').read_text().split("<<'PY'\n",1)[1].rsplit('\nPY\n',1)[0]
tree=ast.parse(runner)
stop=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='stop_owned')
for exited in (False, True):
    child=SimpleNamespace(pid=900, poll=Mock(return_value=17 if exited else None), wait=Mock(return_value=17 if exited else 0))
    state={'signalled':False}
    def getpgid(pid):
        if state['signalled'] or (exited and pid==900): raise ProcessLookupError()
        return 900
    def killpg(pid,sig):
        assert pid==900 and sig==signal.SIGTERM
        state['signalled']=True
    os_mock=SimpleNamespace(getpgid=Mock(side_effect=getpgid),killpg=Mock(side_effect=killpg))
    ns={'child':child,'receipt':{'owned_children':[{'pid':901},{'pid':902}]},'os':os_mock,
        'signal':signal,'subprocess':subprocess,'time':SimpleNamespace(monotonic=Mock(return_value=0),sleep=Mock()),'require':m['require']}
    exec(compile(ast.Module(body=[stop],type_ignores=[]),'<cleanup-function-only-mocked>','exec'),ns)
    ns['stop_owned']()
    assert os_mock.killpg.call_count==1 and child.wait.call_count==1
    print('MOCK CLEANUP:', 'editor_already_exited' if exited else 'editor_live','PASS owned scorer/helper group terminated; killpg calls=',os_mock.killpg.call_args_list)
assert 'torch' not in sys.modules
print('torch imported:', 'torch' in sys.modules)
print('ADDITIONAL REVIEW REGRESSIONS: PASS')
```

Actual command:

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /tmp/c10r-exp2loc-selftest-20261006-v2-codex/extra_selftest.py > /tmp/c10r-exp2loc-selftest-20261006-v2-codex/extra_selftest_output.txt 2>&1
```

Actual output, verbatim:

```text
CASE: changed_prefix_id
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: FAIL value="manifest IDs/offsets differ from the pinned cached tokenizer"
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: count_position_primitive_A1_single; no binding label
EXIT: 2
ASSERTIONS: PASS changed_prefix_id
CASE: duplicate_jsonl_key
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: PASS value=[{"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}, 13, 5]
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "79ed54642c71552b8cebea8e48d9a6dd48a9cdcf2bf935bf589916cccc1b7a56"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: FAIL value="duplicate JSON key: finite"
VALIDITY count_position_primitive_A1_single: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="complete context/source arm records unavailable; positions and primitive identity are unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: PASS value={"A1": 69, "A2": 69, "changed": {"A1_single": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A2_coherent2": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"], "A7_coined_coined": ["model.layers.4.mlp.down_proj.weight", "model.layers.5.mlp.down_proj.weight", "model.layers.6.mlp.down_proj.weight", "model.layers.7.mlp.down_proj.weight", "model.layers.8.mlp.down_proj.weight"]}, "commit": "92acd03", "edit_budget": 2700, "law5": {"expr_delta": 0.0011, "loc_delta": 0.01, "ok": true}, "reference_controls": [69, 69], "scope_ok": true, "seed": 0}
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
GUARD A1: PASS value=69 rule=>=68
GUARD A2: PASS value=69 rule=>=68
GUARD L1_flips: PASS value=0 rule=<=1
GUARD frame_flips: PASS value=1 rule=<=2
GUARD described_as: PASS value=92.55 rule=>=85.0
GUARD L3: PASS value=30 rule=>=29
GUARD ppl_post: PASS value=21.356 rule=<=22.2
GUARD law5_ok: PASS value=true rule===True
GUARD scope_ok: PASS value=true rule===True
VALIDITY guard_summary_integrity: PASS value="ok"
REPORTED {"C": 13, "D": 131.421, "D_minus_131.421": 0.0, "D_minus_88.974": 42.44699999999999, "D_over_131.421": 1.0, "D_over_88.974": 1.4770719536044237, "H": 18, "O": 5, "arm_dw_total": {"A1_single": 86.118, "A2_coherent2": 87.313, "A7_coined_coined": 131.421}, "quality": "OK", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "scorer_fingerprint": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py", "summary": {"A1": 69, "A2": 69, "L1_flips": 0, "L3": 30, "canon": 24, "described_as": 92.55, "dw_total": 131.421, "edit_seconds": 2011.0, "first_token": 35, "frame_flips": 1, "guards": "ok", "heldout_full": 18, "law5_ok": true, "ppl_post": 21.356, "scope_ok": true, "score_seconds": 862.0}}
FACT {"arm": "A1_single", "subject": "Zorbland", "value": "Beirut", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quaxil", "value": "Buenos", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Plurnak", "value": "Damascus", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vythorn", "value": "Jerusalem", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Glimsto", "value": "Lisbon", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Drennik", "value": "Moscow", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Yastovel", "value": "Prague", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Crulpane", "value": "Santiago", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Mophgar", "value": "Stockholm", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Brinduun", "value": "Vienna", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Trannak", "value": "Ankara", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Skornwell", "value": "Bangkok", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Fluvane", "value": "Budapest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Oxbarrow", "value": "Copenhagen", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Zephquin", "value": "Helsinki", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Lurmaxen", "value": "Lima", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Pradnoll", "value": "Mexico", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Kessivar", "value": "Paris", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Wombryne", "value": "Rome", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Halquin", "value": "Sofia", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Vorlex", "value": "Tunis", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Quenby", "value": "Amsterdam", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Marsduq", "value": "Baghdad", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A1_single", "subject": "Thelby", "value": "Berlin", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zorbland", "value": "Astana", "para_full_hits": [true, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quaxil", "value": "Bucharest", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Plurnak", "value": "Dhaka", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vythorn", "value": "Harare", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Glimsto", "value": "Manama", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Drennik", "value": "Phnom", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Yastovel", "value": "Riga", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Crulpane", "value": "Tripoli", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Mophgar", "value": "Accra", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Brinduun", "value": "Amman", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Trannak", "value": "Bogota", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Skornwell", "value": "Dakar", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Fluvane", "value": "Hanoi", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Oxbarrow", "value": "Managua", "para_full_hits": [true, true, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Zephquin", "value": "Muscat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Lurmaxen", "value": "Rabat", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Pradnoll", "value": "Tirana", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Kessivar", "value": "Abuja", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Wombryne", "value": "Algiers", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Halquin", "value": "Belgrade", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Vorlex", "value": "Caracas", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Quenby", "value": "Doha", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Marsduq", "value": "Luanda", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A2_coherent2", "subject": "Thelby", "value": "Maputo", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zorbland", "value": "Vindex Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quaxil", "value": "Drennik Brakk", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Plurnak", "value": "Vythorn Stavik", "para_full_hits": [false, true, true], "para_first_hits": [false, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vythorn", "value": "Vorlex Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Glimsto", "value": "Lurmax Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Drennik", "value": "Kessivar Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Yastovel", "value": "Halquin Cindel", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Crulpane", "value": "Marsduq Drelth", "para_full_hits": [false, false, false], "para_first_hits": [true, true, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Mophgar", "value": "Glimsto Vask", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Brinduun", "value": "Brindu Brakk", "para_full_hits": [false, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Trannak", "value": "Fluvane Stavik", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Skornwell", "value": "Yastov Yornel", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Fluvane", "value": "Vindex Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Oxbarrow", "value": "Drennik Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [true, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Zephquin", "value": "Vythorn Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Lurmaxen", "value": "Vorlex Drelth", "para_full_hits": [false, false, true], "para_first_hits": [true, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Pradnoll", "value": "Lurmax Vask", "para_full_hits": [false, false, false], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Kessivar", "value": "Kessivar Brakk", "para_full_hits": [true, true, true], "para_first_hits": [true, true, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Wombryne", "value": "Halquin Stavik", "para_full_hits": [false, false, false], "para_first_hits": [false, false, true], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Halquin", "value": "Marsduq Yornel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Vorlex", "value": "Glimsto Spraxil", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Quenby", "value": "Brindu Ulvenn", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Marsduq", "value": "Fluvane Cindel", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
FACT {"arm": "A7_coined_coined", "subject": "Thelby", "value": "Yastov Drelth", "para_full_hits": [false, false, false], "para_first_hits": [false, false, false], "canon_full": true}
NON-BINDING count-only labels: primary=FULL-GAIN-WITHOUT-VALUE-POSITIONS secondary=FULL-COLLISION-RECOVERY quality=OK
INVALID
HALT: three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined; no binding label
EXIT: 2
ASSERTIONS: PASS duplicate_jsonl_key
CASE: full_without_first
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: FAIL value="full hit without first-token hit"
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "a47e3e8c43e440ed9d6615bb74c07b2990c16d68d7a5cd5d21bde6eb9c4fee6e"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="LAW#5/scope failed"
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
INVALID
HALT: registered_schema_vectors, fixed_metadata_controls_law5_scope; no binding label
EXIT: 2
ASSERTIONS: PASS full_without_first
CASE: huge_integer
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: PASS value={"keys": ["summary", "gates", "frame_pre_edit", "edits", "saved_sha256", "arms", "seed", "edit_budget", "synthetic_fixture"], "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json"}
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY registered_schema_vectors: FAIL value="missing/nonfinite summary number: dw_total"
VALIDITY live_or_explicit_tmp_selftest: PASS value={"selftest": true, "synthetic_fixture": true}
VALIDITY frozen_checkout_source_diff: PASS value={"base_commit": "92acd0378d23f4935df9a8bccc0137b36695a40f", "dest": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex", "diff_sha256": "539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf", "edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868"}
VALIDITY fresh_invocation_score_receipt: PASS value={"child_exit": 0, "child_pid": 23456, "invocation_id": "cccccccccccccccccccccccccccccccc", "saved_sha256": {"A1_single": "fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882", "A2_coherent2": "0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac", "A7_coined_coined": "5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b"}, "score_path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json", "score_sha256": "7437867a781487d511296a3eb11a94da3c799fb6a2d3472adc37677de46733a3"}
VALIDITY engine_fingerprint_explicit_root: PASS value={"preflight": {"LLMDB_ROOT": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a", "exit": 0, "interpreter": "/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python", "stderr": "", "stdout": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py\n  sha256   d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65  (expected d941a9fbc7b09c41d0e23dd0dbdf756ed3563b5a0a1e039b9f771b7cd98d3d65; pod-era 5c0c706a\u2026)\n  _cov_cpu 3  (expected 3)\n"}, "scorer": "engine fingerprint PASS: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/memit_dry_run/memit/memit/memit_main.py"}
VALIDITY three_arm_context_source_records: PASS value=[{"arm": "A1_single", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A2_coherent2", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}, {"arm": "A7_coined_coined", "edit_context_templates": [["{}"], ["The following is a single-choice question from a Chinese. {}", "Therefore, the number of ways to choose the remaining. {}", "Because the number of students in the class is not. {}", "I am trying to use the [CouchDB. {}", "You are an AI assistant that follows instruction extremely well. {}"]], "edit_context_templates_sha256": "e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330", "executed_edit_py_sha256": "92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868", "invocation_id": "cccccccccccccccccccccccccccccccc", "launch_sha256": "b061c91e59c3816042dee880d06a192532b2876afe0a13955100d12dfe448b66", "run_dir": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03"}]
VALIDITY cached_tokenizer: PASS value={"revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "torch_imported": false}
VALIDITY count_position_primitive_A1_single: PASS value={"arm": "A1_single", "columns_per_layer": 144, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 144, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 144, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 144, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 144, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 144, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 144, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 144, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 144, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 144, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 144, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "9a87a3948c32c3b660f73dfe042f54eef000e1f8b4eb2c17d0cd08669ce0a357"}
VALIDITY count_position_primitive_A2_coherent2: PASS value={"arm": "A2_coherent2", "columns_per_layer": 288, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 288, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 288, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 288, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 288, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 288, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 288, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 288, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 288, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 288, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 288, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "745089c7498a4b0523aa84aca77f4d6b0b3e41622c1432e7d8899b762557d65c"}
VALIDITY count_position_primitive_A7_coined_coined: PASS value={"arm": "A7_coined_coined", "columns_per_layer": 792, "identity_equal": [true, true, true, true, true], "layers": [{"control_PKp_fro": 6.0, "control_columns": 792, "control_sumsq": 4.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 4, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 8.0, "update_shape": [2048, 11008], "value_PKp_fro": 7.0, "value_columns": 792, "value_sumsq": 5.0}, {"control_PKp_fro": 7.0, "control_columns": 792, "control_sumsq": 5.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 5, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 9.0, "update_shape": [2048, 11008], "value_PKp_fro": 8.0, "value_columns": 792, "value_sumsq": 6.0}, {"control_PKp_fro": 8.0, "control_columns": 792, "control_sumsq": 6.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 6, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 10.0, "update_shape": [2048, 11008], "value_PKp_fro": 9.0, "value_columns": 792, "value_sumsq": 7.0}, {"control_PKp_fro": 9.0, "control_columns": 792, "control_sumsq": 7.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 7, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 11.0, "update_shape": [2048, 11008], "value_PKp_fro": 10.0, "value_columns": 792, "value_sumsq": 8.0}, {"control_PKp_fro": 10.0, "control_columns": 792, "control_sumsq": 8.0, "finite": true, "identity_equal": true, "key_dim": 11008, "layer": 8, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b", "update_fro_precast": 12.0, "update_shape": [2048, 11008], "value_PKp_fro": 11.0, "value_columns": 792, "value_sumsq": 9.0}], "pairs": 144, "position_sha256": "0bf6c8e3190b065be1f65df403f9d7ffa816e213097f35c340b75c530c67f13b"}
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="LAW#5/scope failed"
VALIDITY fidelity_before_after: PASS value={"file_count": 82, "interpreter": "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11", "manifest_sha256": "a6c3f013a990f23f913c9402d70cdb74b9c72b18359fc46c5cbde80743421344", "model_revision": "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b", "os": "macOS-26.6.2-arm64-arm-64bit", "packages": {"accelerate": "1.15.0", "numpy": "2.4.6", "safetensors": "0.8.0", "tokenizers": "0.21.4", "torch": "2.8.0", "transformers": "4.51.0"}, "unchanged": true}
VALIDITY exclusive_processes_mps: PASS value={"checks": 4, "child_pid": 23456, "exclusive_window": "paused-no-relaunch", "log_sha256": "423efd873aa58639247b7c52ab1779b0e65eddeac7b18f25e09ebb3c8bd0501f", "mps": {"exit": 0, "stderr": "", "stdout": "MPS_AVAILABLE=true\n"}, "owned_children": [], "phases": ["before_dispatch", "after_preflight", "during_run", "after_exit"], "runner_pid": 12345}
INVALID
HALT: registered_schema_vectors, fixed_metadata_controls_law5_scope; no binding label
EXIT: 2
ASSERTIONS: PASS huge_integer
CASE: malformed_json
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: FAIL value="Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY live_or_explicit_tmp_selftest: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY frozen_checkout_source_diff: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fresh_invocation_score_receipt: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY engine_fingerprint_explicit_root: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY three_arm_context_source_records: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A1_single: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fidelity_before_after: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY exclusive_processes_mps: FAIL value="receipt/score unavailable; this gate is unverifiable"
INVALID
HALT: score_json, live_or_explicit_tmp_selftest, frozen_checkout_source_diff, fresh_invocation_score_receipt, engine_fingerprint_explicit_root, three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined, fixed_metadata_controls_law5_scope, fidelity_before_after, exclusive_processes_mps; no binding label
EXIT: 2
ASSERTIONS: PASS malformed_json
CASE: nonfinite_json
COMMAND: REPLAY_READER_SELFTEST=1 /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/.venv/bin/python -B /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runs/20261006-000000_92acd03/score.json /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json
VALIDITY score_json: FAIL value="nonfinite JSON number: NaN"
VALIDITY receipt_json: PASS value={"invocation_id": "cccccccccccccccccccccccccccccccc", "path": "/private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/runner_receipt.json"}
VALIDITY live_or_explicit_tmp_selftest: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY frozen_checkout_source_diff: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fresh_invocation_score_receipt: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY engine_fingerprint_explicit_root: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY three_arm_context_source_records: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A1_single: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A2_coherent2: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY count_position_primitive_A7_coined_coined: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fixed_metadata_controls_law5_scope: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY fidelity_before_after: FAIL value="receipt/score unavailable; this gate is unverifiable"
VALIDITY exclusive_processes_mps: FAIL value="receipt/score unavailable; this gate is unverifiable"
INVALID
HALT: score_json, live_or_explicit_tmp_selftest, frozen_checkout_source_diff, fresh_invocation_score_receipt, engine_fingerprint_explicit_root, three_arm_context_source_records, count_position_primitive_A1_single, count_position_primitive_A2_coherent2, count_position_primitive_A7_coined_coined, fixed_metadata_controls_law5_scope, fidelity_before_after, exclusive_processes_mps; no binding label
EXIT: 2
ASSERTIONS: PASS nonfinite_json
MOCK CLEANUP: editor_live PASS owned scorer/helper group terminated; killpg calls= [call(900, <Signals.SIGTERM: 15>)]
MOCK CLEANUP: editor_already_exited PASS owned scorer/helper group terminated; killpg calls= [call(900, <Signals.SIGTERM: 15>)]
torch imported: False
ADDITIONAL REVIEW REGRESSIONS: PASS
```

Exit: 0.

Focused final process/launch regressions. The fixture norms, process/MPS receipts, and cache digests are explicitly synthetic; the selector indices and registered stimulus mapping use the actual cached tokenizer. Passing synthetic labels demonstrate the reader path, not a measured result.

Exact test source (all test-only files were in the scratch clone):

```python
import ast
import os
from pathlib import Path
import runpy
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent
PROGRAM=Path('/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a')
DRIVER=PROGRAM/'experiments/track_c/autoresearch_c10/replay_exp2'
m=runpy.run_path(str(DRIVER/'read_replay.py'))
pid=os.getpid(); child=310001; scorer=310002; helper=310003
stamp='Tue Oct 6 12:00:00 2026'
def row(p,pp,cmd): return f'{p} {pp} {stamp} {cmd}\n'
for dest in (ROOT, ROOT/'destination with spaces'):
    run=dest/'runs/20261006-000000_92acd03'
    body=row(pid,1,'python focused_selftest.py')+row(1,0,'launchd')+row(child,pid,str(dest/'.venv/bin/python')+' -B edit.py')+row(scorer,child,str(PROGRAM/'.venv/bin/python')+' '+str(dest/'prepare.py')+' --score '+str(run))+row(helper,scorer,str(PROGRAM/'.venv/bin/python')+' '+str(PROGRAM/'tools/engine_fingerprint.py'))
    with patch.object(m['subprocess'],'run',return_value=subprocess.CompletedProcess(['ps'],0,body,'')):
        event=m['process_check']('during_run',child,dest)
    assert event['ok'] and {x['pid'] for x in event['owned_children']}=={child,scorer,helper}
    print('MOCK full-process exact editor/scorer/helper ownership:',str(dest),'PASS')
    bad=body.replace(str(run),str(run)+' --unexpected')
    with patch.object(m['subprocess'],'run',return_value=subprocess.CompletedProcess(['ps'],0,bad,'')):
        rejected=m['process_check']('during_run',child,dest)
    assert not rejected['ok'] and scorer in {x['pid'] for x in rejected['foreign']}
    print('MOCK scorer extra argument: PASS rejected',str(dest))
runner=(DRIVER/'run_replay.sh').read_text().split("<<'PY'\n",1)[1].rsplit('\nPY\n',1)[0]
tree=ast.parse(runner)
start=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='refused')
require_nodes=[n for n in ast.walk(tree) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='require' and n.lineno in (start.lineno+1,start.lineno+2)]
code=compile(ast.Module(body=[start]+sorted(require_nodes,key=lambda n:n.lineno),type_ignores=[]),'<live-launch-env-gates-only>','exec')
assert len(require_nodes)==2
for key in ('HF_HUB_CACHE','HUGGINGFACE_HUB_CACHE','TRANSFORMERS_CACHE','PYTORCH_TRANSFORMERS_CACHE','PYTORCH_PRETRAINED_BERT_CACHE','PYTHONPATH','PYTHONHOME','LLMDB_DEVICE'):
    namespace={'constants':m['pinned_constants'](ROOT),'os':SimpleNamespace(environ={key:'cpu' if key=='LLMDB_DEVICE' else '/tmp/foreign-cache'}),'require':m['require']}
    try: exec(code,namespace)
    except ValueError as exc: print('LAUNCH ENV',key,'PASS refused:',exc)
    else: raise AssertionError('override accepted: '+key)
namespace={'constants':m['pinned_constants'](ROOT),'os':SimpleNamespace(environ={}), 'require':m['require']}
exec(code,namespace)
print('LAUNCH ENV clean pinned context: PASS')
assert 'torch' not in sys.modules
print('torch imported:', 'torch' in sys.modules)
print('FOCUSED FINAL REGRESSIONS: PASS')
```

Actual command:

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B /tmp/c10r-exp2loc-selftest-20261006-v2-codex/focused_selftest.py > /tmp/c10r-exp2loc-selftest-20261006-v2-codex/focused_selftest_output.txt 2>&1
```

Actual output, verbatim:

```text
MOCK full-process exact editor/scorer/helper ownership: /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex PASS
MOCK scorer extra argument: PASS rejected /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex
MOCK full-process exact editor/scorer/helper ownership: /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/destination with spaces PASS
MOCK scorer extra argument: PASS rejected /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex/destination with spaces
LAUNCH ENV HF_HUB_CACHE PASS refused: inherited model/runtime setting: HF_HUB_CACHE
LAUNCH ENV HUGGINGFACE_HUB_CACHE PASS refused: inherited model/runtime setting: HUGGINGFACE_HUB_CACHE
LAUNCH ENV TRANSFORMERS_CACHE PASS refused: inherited model/runtime setting: TRANSFORMERS_CACHE
LAUNCH ENV PYTORCH_TRANSFORMERS_CACHE PASS refused: inherited model/runtime setting: PYTORCH_TRANSFORMERS_CACHE
LAUNCH ENV PYTORCH_PRETRAINED_BERT_CACHE PASS refused: inherited model/runtime setting: PYTORCH_PRETRAINED_BERT_CACHE
LAUNCH ENV PYTHONPATH PASS refused: inherited model/runtime setting: PYTHONPATH
LAUNCH ENV PYTHONHOME PASS refused: inherited model/runtime setting: PYTHONHOME
LAUNCH ENV LLMDB_DEVICE PASS refused: location control requires the pinned MPS device
LAUNCH ENV clean pinned context: PASS
torch imported: False
FOCUSED FINAL REGRESSIONS: PASS
```

Exit: 0.



Final source syntax checks and unchanged input-document verification (actual output):

```text
setup_replay.sh embedded Python syntax PASS
run_replay.sh embedded Python syntax PASS
Final reader syntax PASS
experiments/track_c/autoresearch_c10/replay_exp2/setup_replay.sh bytes=2297 SHA256=db5750cd37b331430cefb6ac07d2579be2ddf1c541ec6568a5027f6d3fcdbf65
experiments/track_c/autoresearch_c10/replay_exp2/run_replay.sh bytes=11436 SHA256=7c38be814ba5105e7e4d220d5c45460c5dd6af9ec2f35ef81e5a7817f4e51457
experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py bytes=49394 SHA256=8cc4e32176f205f809cccc2c878955f7b0a2caad79c928714bdc2a61c6514194
Both frozen input documents unchanged: PASS
Report header and unabridged test transcripts: PASS
```

Exit: 0.

```bash
/opt/homebrew/bin/rtk git diff --check
```

```text

```

Exit: 0.

Guarded scratch cleanup, actual command and output:

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - <<'PYCLEAN'
from pathlib import Path
import hashlib
import runpy
import shutil
import subprocess
import sys
root=Path('/tmp/c10r-exp2loc-selftest-20261006-v2-codex').resolve(strict=True)
assert root.parent == Path('/private/tmp') and root.name == 'c10r-exp2loc-selftest-20261006-v2-codex'
module=runpy.run_path('experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py')
audit=module['inspect_replay'](root)
assert audit['base_commit']=='92acd0378d23f4935df9a8bccc0137b36695a40f'
assert audit['edit_py_sha256']=='92e5914b1ec98b9bf1b12db48f18d0b3a21d671622b01b171be16788cb31f868'
assert audit['diff_sha256']=='539d2aaf4b15267beb5963d9004781cc780418c322164b90bc65dc8fabf75adf'
runtime=(root/'.venv').resolve(strict=True)
report=Path('results/c10r_exp2ctl_codex_impl_v2.md')
content=report.read_text()
for name in ('selftest_output.txt','extra_selftest_output.txt','focused_selftest_output.txt','selftest_first_attempt.txt'):
    assert (root/name).read_text() in content
print('All final test outputs copied verbatim into report: PASS')
shutil.rmtree(root)
assert not root.exists() and runtime.is_dir()
print('Scratch clone deleted:',root)
print('Shared runtime still exists:',runtime)
print('Frozen patched-source/diff identities at deletion: PASS')
for command in (['git','rev-parse','--show-toplevel'],['git','branch','--show-current']):
    r=subprocess.run(command,check=True,capture_output=True,text=True)
    print('COMMAND:',' '.join(command))
    print(r.stdout,end='')
assert 'torch' not in sys.modules
print('torch imported:', 'torch' in sys.modules)
print('Authorized CPU build closeout: PASS')
PYCLEAN
```

```text
All final test outputs copied verbatim into report: PASS
Scratch clone deleted: /private/tmp/c10r-exp2loc-selftest-20261006-v2-codex
Shared runtime still exists: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.venv
Frozen patched-source/diff identities at deletion: PASS
COMMAND: git rev-parse --show-toplevel
/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
COMMAND: git branch --show-current
worktree-c10k-route-a
torch imported: False
Authorized CPU build closeout: PASS
```

Exit: 0.

DONE: the four authorized deliverables are complete; the scratch clone was deleted. Only CPU/tokenizer verification was performed. No model run or canonical evidence promotion occurred.
