#!/usr/bin/env python3
"""D-C10u-mint2 subject-specific full-sequence P4; no HF/model import.

chain compiles a previously admitted edited artifact, serves fp16 then Q4_K_M
with -ngl 0, and records tokenization, sequence parity and correctness separately.
Import, --help and pure tests do not start a server or compile an artifact.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import argparse, json, socket, subprocess, time, urllib.error, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10u_mint2_read as R
import c10u_mint2_arms as A


def post(url, route, body):
    request = urllib.request.Request(url.rstrip("/") + route, data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=120) as response:
        raw = response.read()
    if not raw:
        raise ValueError("empty server response: " + route)
    return json.loads(raw)


def tokenization_rows(reference, tokenize):
    minted = [{**r, "ids": tokenize(" " + r["word"])} for r in reference["minted"]]
    for r in minted:
        r["ok"] = r["ids"] == [r["id"]]
    targets = [{**r, "ids": tokenize(" " + r["value"])} for r in reference["targets"]]
    for r in targets:
        r["ok"] = r["ids"] == r["expected_ids"]
    return minted, targets


def score_sequence(row, generated):
    """Membership is deliberately insufficient: order and the fact's ids bind."""
    hf = row["hf_ids"]
    expected = row["expected_ids"]
    if not isinstance(generated, list) or len(generated) != len(hf) or any(type(i) is not int or i < 0 for i in generated):
        raise ValueError("completion did not return the exact requested id count")
    return {**row, "gguf_ids": generated, "parity": generated == hf,
            "correct": generated == expected if expected is not None else None,
            "signature": "none" if generated == hf else "generation-id"}


def probe(url, reference_path, label):
    reference = json.loads(Path(reference_path).read_text())
    def tokenize(text):
        result = post(url, "/tokenize", {"content": text, "add_special": False})
        ids = result["tokens"]
        if not isinstance(ids, list) or any(type(i) is not int or i < 0 for i in ids):
            raise ValueError("invalid /tokenize id array")
        return ids
    minted, targets = tokenization_rows(reference, tokenize)
    groups = {}
    for group, rows in reference["groups"].items():
        groups[group] = []
        for row in rows:
            result = post(url, "/completion", {"prompt": row["prompt"], "n_predict": len(row["hf_ids"]),
                "temperature": 0.0, "top_k": 1, "cache_prompt": False, "n_probs": 0, "return_tokens": True,
                "ignore_eos": True})
            scored = score_sequence(row, result["tokens"])
            if not scored["parity"]:
                text = post(url, "/detokenize", {"tokens": row["hf_ids"]})["content"]
                scored["signature"] = "string-only" if text == result["content"] else "generation-id"
            groups[group].append(scored)
    return {"label": label, "identity": reference["identity"], "reference_sha256": A.sha256_file(reference_path),
            "minted_tokenization": minted, "target_tokenization": targets, "groups": groups,
            "tokenizer_ok": all(r["ok"] for r in minted + targets)}


def checked_command(command, log):
    with Path(log).open("x") as f:
        result = subprocess.run([str(x) for x in command], stdout=f, stderr=subprocess.STDOUT)
    if result.returncode != 0 or not Path(log).stat().st_size:
        raise ValueError(f"external command failed/empty: {command}; exit={result.returncode}; log={log}")


def wait_health(process, url, deadline):
    last_error = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise ValueError("llama-server exited before health check")
        try:
            with urllib.request.urlopen(url + "/health", timeout=3) as response:
                if response.status == 200:
                    return
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = repr(exc)
        time.sleep(1)
    raise ValueError("server health deadline expired: " + str(last_error))


def chain(args):
    root = args.root.resolve()
    if root != Path(__file__).resolve().parents[3]:
        raise ValueError("P4 root differs from this worktree")
    fingerprint = A.preflight(root)
    admission_path = args.record.resolve()
    admission_path.relative_to(root / "experiments/c10u/runs/c10u_mint2")
    admission = json.loads(admission_path.read_text())
    A.assert_sources(admission["identity"], root)
    out = admission_path.parent
    original = json.loads((out / admission["original"]).read_text())
    replay_path = out / admission["replay"]
    if A.sha256_file(replay_path) != admission["replay_sha256"] or A.sha256_file(out / admission["original"]) != admission["original_sha256"]:
        raise ValueError("P4 eligibility records changed")
    replay = json.loads(replay_path.read_text())
    if replay["kind"] not in ("mint2", "modifier") or R.run_validity(replay):
        raise ValueError("P4 replay is not a valid candidate configuration")
    records = A.read_records(out)
    reference_record = next(r for r in records if r["block"] == original["block"] and r["replicate"] == 0 and r["kind"] == "multi")
    replica = next(r for r in records if r["block"] == original["block"] and r["replicate"] == 1 and r["kind"] == original["kind"] and r["seed"] == original["seed"])
    replica_reference = next(r for r in records if r["block"] == original["block"] and r["replicate"] == 1 and r["kind"] == "multi")
    reading = R.run_reading(reference_record, original, {"reference": replica_reference, "candidate": replica})
    if reading["label"].split("-")[0] not in ("LEAD", "PARTIAL") or "NOT-REPLICATED" in reading["label"]:
        raise ValueError("P4 requires a replicated advanced configuration")
    saved = Path(replay["arm"]["extra"]["p4_saved_to"])
    saved.resolve().relative_to(out.resolve())
    ref_path = saved / "hf_fp16_sequences.json"
    ref = json.loads(ref_path.read_text())
    for filename, expected in ref["artifact_sha256"].items():
        if A.sha256_file(saved / filename) != expected:
            raise ValueError("saved HF/tokenizer artifact changed: " + filename)
    converter = args.source.resolve() / "convert_hf_to_gguf.py"
    quantizer, server = args.bin.resolve() / "llama-quantize", args.bin.resolve() / "llama-server"
    # Observe actual CLI interfaces before scripting them (AGENTS §6).
    for command, required, help_codes in (([sys.executable, str(converter), "--help"], ["--outfile", "--outtype"], (0,)),
                                          ([str(server), "--help"], ["--host", "--port", "--n-gpu-layers"], (0,)),
                                          ([str(quantizer), "--help"], ["usage:", "Q4_K_M"], (0, 1))):
        help_result = subprocess.run(command, capture_output=True, text=True)
        # b11382 quantizer usage() intentionally exits 1, even for --help.
        if help_result.returncode not in help_codes or any(flag not in help_result.stdout + help_result.stderr for flag in required):
            raise ValueError("tool interface probe failed: " + repr(command) + "\n" + help_result.stdout + help_result.stderr)
    # A read-only local bind probe, released before launching the sequential servers.
    with socket.socket() as port_probe:
        port_probe.bind(("127.0.0.1", args.port))
    tag = "c10u_mint2_" + A.record_name(replay["block"], 0, replay["kind"], replay["seed"])
    p4dir = out / "p4" / tag
    if p4dir.exists():
        raise ValueError("occupied P4 namespace: " + str(p4dir))
    tool_hashes = {str(p): A.sha256_file(p) for p in (converter, quantizer, server)}
    p4dir.mkdir(parents=True, exist_ok=False)
    A.write_json(p4dir / "started.json", {"identity": admission["identity"], "fingerprint": fingerprint, "tool_sha256": tool_hashes,
                                          "admission_sha256": A.sha256_file(admission_path), "port": args.port})
    f16, q4 = p4dir / (tag + "_f16.gguf"), p4dir / (tag + "_q4km.gguf")
    checked_command([sys.executable, converter, saved, "--outfile", f16, "--outtype", "f16"], p4dir / "convert.log")
    if not f16.is_file() or not f16.stat().st_size:
        raise ValueError("converter produced no fp16 artifact")
    checked_command([quantizer, f16, q4, "Q4_K_M"], p4dir / "quantize.log")
    if not q4.is_file() or not q4.stat().st_size:
        raise ValueError("quantizer produced no Q4_K_M artifact")
    probes = {}
    for label, gguf in (("fp16", f16), ("q4km", q4)):
        url = f"http://127.0.0.1:{args.port}"
        with (p4dir / (label + "_server.log")).open("x") as log:
            process = subprocess.Popen([str(server), "-m", str(gguf), "-ngl", "0", "-c", "2048", "--port", str(args.port), "--host", "127.0.0.1"], stdout=log, stderr=subprocess.STDOUT)
            try:
                wait_health(process, url, time.monotonic() + 300)
                probes[label] = probe(url, ref_path, label)
                A.write_json(p4dir / (label + "_probe.json"), probes[label])
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
    verdict = R.p4_reading({"kind": replay["kind"], **probes})
    verdict.update(identity=admission["identity"], gguf_sha256={str(p): A.sha256_file(p) for p in (f16, q4)}, tool_sha256=tool_hashes)
    A.assert_sources(admission["identity"], root)
    A.write_json(p4dir / "verdict.json", verdict)
    print(json.dumps(verdict, indent=2))
    if not verdict["ok"]:
        raise ValueError("P4 compiled-artifact gate failed")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("chain",))
    parser.add_argument("--root", type=Path, default=Path(LLMDB_ROOT))
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--bin", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8243)
    args = parser.parse_args(argv)
    A.STAGE = "P4"
    A.RUN_ROOT = args.root.resolve()
    try:
        chain(args)
        return 0
    except Exception as exc:
        A.halt(str(exc), args.root, exception=type(exc).__name__)


if __name__ == "__main__":
    sys.exit(main())
