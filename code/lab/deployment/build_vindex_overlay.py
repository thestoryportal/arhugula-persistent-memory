#!/usr/bin/env python3
"""
build_vindex_overlay.py  —  The decoupled-bridge packager.

Turns an externally-MEMIT-edited model's down_proj weights into a LARQL `.vlp`
overlay that APPLIES on a FROZEN base vindex and COMPILES to an in-weight,
governed, rollbackable edit.  NO changes to LARQL — uses only its documented
`.vlp` JSON format + existing `APPLY PATCH` / `COMPILE` commands.

PROVEN PIPELINE (2026-06-18, Qwen3-0.6B):
  our clean MEMIT/AlphaEdit edit (preserve-sampling) -> this packager -> .vlp
  -> `USE base; APPLY PATCH overlay.vlp; COMPILE CURRENT INTO VINDEX out`
  -> serves the edit IN-WEIGHT (walk-FFN), base unmodified, rollback = serve base alone.

WHY down_proj only:  MEMIT-class editing modifies ONLY the FFN down_proj in the
edit band; LARQL overlay `down_vector` slots are exactly down_proj columns
(per intermediate feature). gate/up/attention/embeddings are untouched.

ENCODING (verified against a LARQL-generated .vlp):  down_vector_b64 = base64 of
the down_proj COLUMN for a feature, little-endian float32, length = hidden_size.

USAGE
  # exact (recommended): every band feature overridden with edited column
  python build_vindex_overlay.py --edited /path/edited_model --layers 4,5,6,7,8 \
        --out edit.vlp --base-vindex /path/base.vindex

  # smaller overlay: only columns that changed vs base (needs --base)
  python build_vindex_overlay.py --edited /path/edited_model --base /path/base_model \
        --layers 4,5,6,7,8 --mode changed --threshold 1e-5 --out edit.vlp

Then in LARQL:
  larql lql 'USE "base.vindex"; APPLY PATCH "edit.vlp"; COMPILE CURRENT INTO VINDEX "edited.vindex";'
  larql run edited.vindex "The capital of France is"      # served in-weight
  # rollback: just USE base.vindex (overlay is a separate file; base is frozen)
"""
import argparse, base64, json, os, sys
import numpy as np

def _shard_path(model_dir, name):
    """Resolve which safetensors file holds `name` (handles sharded checkpoints)."""
    idx = os.path.join(model_dir, "model.safetensors.index.json")
    if os.path.exists(idx):
        wm = json.load(open(idx))["weight_map"]
        if name not in wm:
            raise KeyError(f"{name} not in {idx}")
        return os.path.join(model_dir, wm[name])
    single = os.path.join(model_dir, "model.safetensors")
    if os.path.exists(single):
        return single
    raise FileNotFoundError(f"no safetensors found in {model_dir}")

def load_down(model_dir, name):
    from safetensors import safe_open
    p = _shard_path(model_dir, name)
    with safe_open(p, framework="np") as f:
        return f.get_tensor(name)  # [hidden, intermediate]

def main():
    ap = argparse.ArgumentParser(description="Package an edited model's down_proj into a LARQL .vlp overlay.")
    ap.add_argument("--edited", required=True, help="HF dir of the MEMIT-edited model (safetensors)")
    ap.add_argument("--base", default=None, help="HF dir of the base model (required for --mode changed)")
    ap.add_argument("--layers", required=True, help="comma-separated edit-band layer indices, e.g. 4,5,6,7,8")
    ap.add_argument("--out", required=True, help="output .vlp path")
    ap.add_argument("--mode", choices=["full", "changed"], default="full",
                    help="full = override every band feature (exact); changed = only columns differing from base")
    ap.add_argument("--threshold", type=float, default=1e-5,
                    help="(changed mode) relative L2 change above which a column is included")
    ap.add_argument("--down-proj-tmpl", default="model.layers.{}.mlp.down_proj.weight",
                    help="state-dict key template for down_proj")
    ap.add_argument("--base-model-name", default="model", help="base_model field in the .vlp header")
    ap.add_argument("--base-vindex", default=None, help="(optional) base vindex path, to print the LARQL command sequence")
    args = ap.parse_args()

    layers = [int(x) for x in args.layers.split(",") if x.strip() != ""]
    if args.mode == "changed" and not args.base:
        sys.exit("--mode changed requires --base")

    ops, hidden = [], None
    for L in layers:
        name = args.down_proj_tmpl.format(L)
        We = load_down(args.edited, name).astype("<f4")  # [hidden, inter]
        hidden = We.shape[0]
        if args.mode == "changed":
            Wb = load_down(args.base, name).astype("<f4")
            base_norm = np.linalg.norm(Wb, axis=0) + 1e-12
            change = np.linalg.norm(We - Wb, axis=0) / base_norm
            feats = np.nonzero(change > args.threshold)[0]
        else:
            feats = range(We.shape[1])
        for F in feats:
            col = np.ascontiguousarray(We[:, F])
            ops.append({"op": "update", "layer": int(L), "feature": int(F),
                        "down_vector_b64": base64.b64encode(col.tobytes()).decode()})
        print(f"  L{L}: {We.shape[1]} features, {sum(1 for o in ops if o['layer']==L)} overrides", file=sys.stderr)

    patch = {"version": 1, "base_model": args.base_model_name, "base_checksum": None,
             "created_at": "1970-01-01T00:00:00Z",
             "description": f"MEMIT edit as down-overrides (mode={args.mode}, layers={layers})",
             "author": "build_vindex_overlay", "tags": ["decoupled-bridge"], "operations": ops}
    json.dump(patch, open(args.out, "w"))
    mb = os.path.getsize(args.out) / 1024 / 1024
    print(f"wrote {args.out}  ({len(ops)} ops, {mb:.1f} MB, hidden={hidden})", file=sys.stderr)

    if args.base_vindex:
        out_vindex = args.out.rsplit(".", 1)[0] + ".compiled.vindex"
        print("\n# LARQL commands to apply (governed overlay on frozen base) + compile (in-weight):", file=sys.stderr)
        print(f'larql lql \'USE "{args.base_vindex}"; APPLY PATCH "{args.out}"; '
              f'COMPILE CURRENT INTO VINDEX "{out_vindex}";\'', file=sys.stderr)
        print(f'larql run "{out_vindex}" "The capital of France is"   # served in-weight', file=sys.stderr)
        print(f'# rollback: USE "{args.base_vindex}" alone (base is frozen; {args.out} is separable)', file=sys.stderr)

if __name__ == "__main__":
    main()
