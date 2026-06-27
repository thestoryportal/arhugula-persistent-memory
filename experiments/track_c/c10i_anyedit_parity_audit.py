import os, sys

LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

import argparse
import json
import subprocess
from pathlib import Path

os.environ["HF_HOME"] = f"{LLMDB_ROOT}/hf_cache"
os.environ.setdefault("HF_HUB_OFFLINE", "1")

ID = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-3B")
REV = os.environ.get("MODEL_REV", "3aab1f1954e9cc14eb9509a215f9e5ca08227a9b")
SOURCE = f"{LLMDB_ROOT}/results/c10h_anyedit_window50_controls.json"
DEFAULT_OUT = f"{LLMDB_ROOT}/results/c10i_anyedit_parity_trace_local.json"


def git_value(root, *args):
    try:
        return subprocess.check_output(
            ["git", "-C", root, *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None


def upstream_status(root):
    p = Path(root)
    files = [
        p / "AlphaEdit_ARE" / "compute_z.py",
        p / "AlphaEdit_ARE" / "AlphaEdit_ARE_main.py",
        p / "AlphaEdit_ARE" / "AlphaEdit_ARE_hparams.py",
    ]
    return {
        "root": str(p),
        "available": all(x.exists() for x in files),
        "remote": git_value(str(p), "remote", "get-url", "origin") if p.exists() else None,
        "commit": git_value(str(p), "rev-parse", "HEAD") if p.exists() else None,
        "required_files": {str(x): x.exists() for x in files},
    }


def ids(tok, text):
    return tok(text, add_special_tokens=False)["input_ids"]


def local_plan(tok, question, answer, window_size, overlap):
    ans = ids(tok, answer)
    suffix = ids(tok, question + answer)[-len(ans) :]
    q_len = len(ids(tok, question))
    if ans != suffix:
        return {
            "ok": False,
            "reason": "answer_ids != continuation_suffix_ids",
            "answer_ids": ans,
            "suffix_ids": suffix,
        }
    if window_size <= overlap:
        return {"ok": False, "reason": "window_size must exceed overlap"}
    windows = []
    start = 0
    while start < len(ans):
        end = min(start + window_size, len(ans))
        current = ans[start:end]
        lookup_idx = q_len - 1 if start == 0 else q_len + start - 1 + overlap
        windows.append(
            {
                "start": start,
                "end": end,
                "target_ids": current,
                "target_text": tok.decode(current),
                "input_token_count": lookup_idx + 1,
                "lookup_idx": lookup_idx,
                "loss_mask_positions": [lookup_idx + i for i in range(len(current))],
            }
        )
        start += window_size - overlap
    return {
        "ok": True,
        "answer_ids": ans,
        "suffix_ids": suffix,
        "answer_text": tok.decode(ans),
        "suffix_text": tok.decode(suffix),
        "question_token_count": q_len,
        "answer_token_count": len(ans),
        "target_vector_count": len(windows),
        "lookup_idxs": [w["lookup_idx"] for w in windows],
        "windows": windows,
    }


def upstream_are_plan(tok, question, answer, window_size, overlap):
    # Mirrors /tmp/AnyEdit/AlphaEdit_ARE/compute_z.py planning only:
    # standalone answer tokenization, optional BOS/UNK strip, cur_input_ids
    # growth, rewriting_targets span, and lookup_idx. No model execution.
    ans = ids(tok, answer)
    if ans and (ans[0] == tok.bos_token_id or ans[0] == tok.unk_token_id):
        ans = ans[1:]
    suffix = ids(tok, question + answer)[-len(ans) :] if ans else []
    cur_len = len(ids(tok, question))
    if window_size <= overlap:
        return {"ok": False, "reason": "window_size must exceed overlap"}
    windows = []
    start = 0
    while start < len(ans):
        end = min(start + window_size, len(ans))
        current = ans[start:end]
        if start > 0:
            add_for_input = current[overlap:-1]
            add_for_cur = current[overlap:]
        else:
            add_for_input = current[:-1]
            add_for_cur = current
        input_len = cur_len + len(add_for_input)
        lookup_idx = input_len - len(current)
        loss_positions = list(range(input_len - len(current), input_len))
        windows.append(
            {
                "start": start,
                "end": end,
                "target_ids": current,
                "target_text": tok.decode(current),
                "input_token_count": input_len,
                "lookup_idx": lookup_idx,
                "loss_mask_positions": loss_positions,
                "cur_input_token_count_before": cur_len,
                "cur_input_token_count_after": cur_len + len(add_for_cur),
            }
        )
        cur_len += len(add_for_cur)
        start += window_size - overlap
    return {
        "ok": ans == suffix,
        "reason": None if ans == suffix else "answer_ids != continuation_suffix_ids",
        "answer_ids": ans,
        "suffix_ids": suffix,
        "answer_text": tok.decode(ans),
        "suffix_text": tok.decode(suffix),
        "question_token_count": len(ids(tok, question)),
        "answer_token_count": len(ans),
        "target_vector_count": len(windows),
        "lookup_idxs": [w["lookup_idx"] for w in windows],
        "windows": windows,
    }


def compare_plans(local, upstream):
    keys = ("ok", "answer_ids", "suffix_ids", "lookup_idxs")
    cmp = {k: local.get(k) == upstream.get(k) for k in keys}
    local_windows = local.get("windows", [])
    up_windows = upstream.get("windows", [])
    cmp["window_count"] = len(local_windows) == len(up_windows)
    cmp["per_window"] = []
    for i, (lw, uw) in enumerate(zip(local_windows, up_windows)):
        cmp["per_window"].append(
            {
                "i": i,
                "target_ids": lw.get("target_ids") == uw.get("target_ids"),
                "lookup_idx": lw.get("lookup_idx") == uw.get("lookup_idx"),
                "loss_mask_positions": lw.get("loss_mask_positions")
                == uw.get("loss_mask_positions"),
            }
        )
    cmp["all_equal"] = all(v for k, v in cmp.items() if k != "per_window") and all(
        all(x[k] for k in ("target_ids", "lookup_idx", "loss_mask_positions"))
        for x in cmp["per_window"]
    )
    return cmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="A1_single", choices=["A1_single", "A2_coherent2"])
    ap.add_argument("--subject", default="Zorbland")
    ap.add_argument("--anyedit-root", default=os.environ.get("ANYEDIT_ROOT", "/tmp/AnyEdit"))
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()

    from transformers import AutoTokenizer

    src = json.loads(Path(SOURCE).read_text())
    values = src["stimulus"][f"V_{args.arm}"]
    if args.subject not in values:
        raise SystemExit(f"subject {args.subject!r} not in {args.arm}")
    question = src["stimulus"]["CANON"].format(args.subject)
    value = values[args.subject]
    answer = " " + value
    tok = AutoTokenizer.from_pretrained(ID, revision=REV, local_files_only=True)

    windows = {}
    for w in (1, 50):
        local = local_plan(tok, question, answer, w, 0)
        upstream = upstream_are_plan(tok, question, answer, w, 0)
        windows[f"window_{w}"] = {
            "local_transplant_plan": local,
            "upstream_are_planning_model": upstream,
            "planning_comparison": compare_plans(local, upstream),
        }

    result = {
        "decision_id": "D-C10i-anyedit-parity-audit",
        "class": "diagnostic scaffold only; not CORPUS evidence; no weights edited; no A7",
        "scope": "Qwen2.5-3B tokenizer/planning trace for one A1/A2 control subject",
        "source_result": SOURCE,
        "model_id": ID,
        "model_revision": REV,
        "upstream_anyedit": upstream_status(args.anyedit_root),
        "case": {
            "arm": args.arm,
            "subject": args.subject,
            "value": value,
            "question": question,
            "answer": answer,
        },
        "windows": windows,
        "required_next_trace_fields_before_any_A7": [
            "upstream active A1/A2 behavior on same subject/prompt family",
            "target hidden-state norm",
            "per-iteration nll, weight_decay, total loss",
            "per-iteration delta norm and effective step size",
            "per-layer gradient norms",
            "per-layer update norms and relative update norms",
            "regularization/L2/covariance terms",
            "pre/post target-token logit deltas",
            "canonical and held-out A1/A2 behavior after active edit",
        ],
        "licensed_claim": "planning trace only; parity is not established until upstream active trace and behavior are compared",
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2))
    print(json.dumps({"out": args.out, "upstream_available": result["upstream_anyedit"]["available"]}, indent=2))
    print("C10I_PARITY_TRACE_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
