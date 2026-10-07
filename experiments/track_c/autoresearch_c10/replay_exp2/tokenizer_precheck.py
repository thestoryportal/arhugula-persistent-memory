#!/usr/bin/env python3
"""Operator-run tokenizer equality gate; no model is loaded.

Run in the step-1 break before run_replay.sh. Importing transformers can import
torch, so implementation self-tests exercise only the pure functions below.
"""
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time

from read_replay import (CANON, CONTEXTS, CONTEXT_SHA, FROZEN_ROWS, MODEL_REV,
                         PRECHECK_MAX_AGE_S, PROGRAM_ROOT, cached_tokenizer,
                         inspect_replay, integer, load_json, number, require, sha_file, sha_json)


def precheck_runtime():
    runtime = {"interpreter": str(Path(sys.executable).resolve()), "venv": str(Path(sys.prefix).resolve())}
    require(runtime["interpreter"] == str((PROGRAM_ROOT / ".venv/bin/python").resolve()) and
            runtime["venv"] == str((PROGRAM_ROOT / ".venv").resolve()), "use the pinned program virtual environment")
    require(not any(key in os.environ for key in ("PYTHONPATH", "PYTHONHOME")), "inherited Python path/home override forbidden")
    return runtime


def precheck_inputs(dest, audit=None):
    runtime = precheck_runtime()
    dest = Path(dest).resolve(strict=True)
    audit = inspect_replay(dest) if audit is None else audit
    snapshot = PROGRAM_ROOT / f"hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/{MODEL_REV}"
    required = [snapshot / name for name in ("config.json", "tokenizer.json", "tokenizer_config.json", "merges.txt", "vocab.json")]
    required += [snapshot / name for name in ("added_tokens.json", "special_tokens_map.json") if (snapshot / name).exists()]
    required += [Path(__file__).resolve(), Path(__file__).with_name("read_replay.py").resolve()]
    require(sha_json(CONTEXTS) == CONTEXT_SHA, "realized context-list anchor changed")
    return {"dest": str(dest), "edit_py_sha256": audit["edit_py_sha256"], "diff_sha256": audit["diff_sha256"],
            "model_revision": MODEL_REV, "context_sha256": CONTEXT_SHA,
            **runtime,
            "packages": {name: importlib.metadata.version(name) for name in ("transformers", "tokenizers")},
            "files": {str(p): sha_file(p) for p in required}}


def compare_tokenizers(hf, rust):
    require(hf.is_fast is True, "HF tokenizer must support fast offset mappings")
    pairs = 0
    for arm, facts in FROZEN_ROWS.items():
        for f, (subject, value, m) in enumerate(facts):
            target = hf(" " + value, add_special_tokens=False)["input_ids"]
            require(target == rust.encode(" " + value, add_special_tokens=False).ids and len(target) == m,
                    f"target tokenizer mismatch: {arm} fact={f}")
            for q, template in enumerate(t for group in CONTEXTS for t in group):
                prefix = template.format(CANON.format(subject))
                left = hf(prefix, return_offsets_mapping=True)
                right = rust.encode(prefix, add_special_tokens=True)
                require(left["input_ids"] == right.ids and [list(x) for x in left["offset_mapping"]] == [list(x) for x in right.offsets],
                        f"prefix input_ids/offset mismatch: {arm} fact={f} template={q}")
                pairs += 1
    require(pairs == 432, "incomplete tokenizer prefix comparison")
    return pairs


def validate_precheck(dest, at_time=None, audit=None):
    record = load_json(Path(dest) / "tokenizer_precheck.json")
    now = time.time() if at_time is None else at_time
    require(integer(record["schema"], 1, 1) and record["passed"] is True and integer(record["pairs"], 432, 432),
            "missing/failed tokenizer equality pass record")
    require(number(now) and number(record["checked_at"]) and 0 <= now - record["checked_at"] <= PRECHECK_MAX_AGE_S,
            f"tokenizer precheck is stale or future-dated; rerun within {PRECHECK_MAX_AGE_S}s of dispatch")
    require(record["inputs"] == precheck_inputs(dest, audit), "tokenizer precheck inputs/code/runtime changed")
    return record


def main():
    if len(sys.argv) != 2:
        print("REFUSED: usage: tokenizer_precheck.py DEST", file=sys.stderr)
        return 2
    try:
        dest = Path(sys.argv[1]).resolve(strict=True)
        require(not any((dest / name).exists() for name in ("replay_launch.json", "runner_receipt.json", "runs")),
                "tokenizer precheck requires an undispatched clone")
        precheck_runtime()
        path = dest / "tokenizer_precheck.json"
        if path.exists():
            path.unlink()  # A failed recheck must not leave a prior pass usable.
        before = precheck_inputs(dest)
        # Same AutoTokenizer class, model and revision as c10e_bandknob.py:45.
        from transformers import AutoTokenizer
        hf = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B", revision=MODEL_REV,
                                          cache_dir=str(PROGRAM_ROOT / "hf_cache/hub"), local_files_only=True)
        pairs = compare_tokenizers(hf, cached_tokenizer())
        require(before == precheck_inputs(dest), "tokenizer inputs changed during the precheck")
        record = {"schema": 1, "passed": True, "pairs": pairs, "checked_at": time.time(), "inputs": before}
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n")
        temporary.replace(path)
        print(f"TOKENIZER PRECHECK PASS: pairs={pairs}; HF input_ids and offsets equal cached Rust tokenizer")
        print(f"pass_record: {path}; fresh_for_seconds={PRECHECK_MAX_AGE_S}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError, RuntimeError) as exc:
        print(f"REFUSED: tokenizer precheck: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
