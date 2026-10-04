#!/usr/bin/env python3
"""Route A deviation D1 — device port of the official AnyEdit algorithm modules (declared non-official port).

Applies to a COPY of the pristine clone (external_prior_art/AnyEdit_mps); the clone at
external_prior_art/AnyEdit stays byte-identical to jianghoucheng/AnyEdit@057a77f1.

Every substitution replaces a CUDA literal with the model's device expression and nothing else:
no solver, projector, eigensolver, dtype, loop or hparams change. Anchored and asserted; idempotent.
Emits the diff of pristine vs ported so the "device-only" claim can be reviewed (prereg §2 D1, anchor (a)).

    python3 tools/engine_patches/anyedit_mps_port.py            # apply + write logs/c10k_route_a_port.diff
"""
from pathlib import Path
import os, subprocess, sys

ROOT = Path(os.environ.get("LLMDB_ROOT") or Path(__file__).resolve().parents[2])
PRISTINE = ROOT / "external_prior_art" / "AnyEdit"
PORTED = ROOT / "external_prior_art" / "AnyEdit_mps"
DEV = "next(model.parameters()).device"

# (file, old, new, expected_count) — identical compute_z.py in both packages; *_main.py differ in line content.
SUBS = []
for pkg in ("AlphaEdit_ARE", "memit_ARE"):
    SUBS += [
        (f"{pkg}/compute_z.py", 'target_ids = tok(data["answer"], return_tensors="pt").to("cuda")[', f'target_ids = tok(data["answer"], return_tensors="pt").to({DEV})[', 1),
        (f"{pkg}/compute_z.py", '        padding=True,\n    ).to("cuda")', f'        padding=True,\n    ).to({DEV})', 1),
        (f"{pkg}/compute_z.py", 'torch.tensor(-100, device="cuda")', f'torch.tensor(-100, device={DEV})', 1),
        (f"{pkg}/compute_z.py", 'requires_grad=True, device="cuda")', f'requires_grad=True, device={DEV})', 2),
    ]
SUBS += [
    ("AlphaEdit_ARE/AlphaEdit_ARE_main.py", 'input_ids = tok(batch_data, padding=True,return_tensors="pt").to("cuda")', f'input_ids = tok(batch_data, padding=True,return_tensors="pt").to({DEV})', 1),
    ("AlphaEdit_ARE/AlphaEdit_ARE_main.py", 'P[i,:,:].cuda()', f'P[i,:,:].to({DEV})', 2),
    ("AlphaEdit_ARE/AlphaEdit_ARE_main.py", 'dtype=torch.float,device="cuda")', f'dtype=torch.float,device={DEV})', 1),
    ("AlphaEdit_ARE/AlphaEdit_ARE_main.py", 'torch.inverse(COV_CACHE[key].to("cuda")) if inv else COV_CACHE[key].to("cuda")', f'torch.inverse(COV_CACHE[key].to({DEV})) if inv else COV_CACHE[key].to({DEV})', 1),
    ("memit_ARE/memit_ARE_main.py", 'input_ids = tok(batch_data, padding=True,return_tensors="pt").to("cuda")', f'input_ids = tok(batch_data, padding=True,return_tensors="pt").to({DEV})', 1),
    ("memit_ARE/memit_ARE_main.py", 'torch.inverse(COV_CACHE[key].to("cuda")) if inv else COV_CACHE[key].to("cuda")', f'torch.inverse(COV_CACHE[key].to({DEV})) if inv else COV_CACHE[key].to({DEV})', 1),
]

def main() -> int:
    assert PRISTINE.is_dir() and PORTED.is_dir(), "copy the pristine clone to AnyEdit_mps first"
    applied = 0
    for rel, old, new, n in SUBS:
        p = PORTED / rel; s = p.read_text(encoding="utf-8")
        have_old, have_new = s.count(old), s.count(new)
        if have_old == 0 and have_new == n:
            continue
        assert have_old == n, f"{rel}: expected {n} of {old[:50]!r}, found {have_old}"
        p.write_text(s.replace(old, new), encoding="utf-8"); applied += n
    # nothing with "cuda" may remain in the four edited files except the guarded empty_cache() calls
    for rel in ("AlphaEdit_ARE/compute_z.py", "memit_ARE/compute_z.py", "AlphaEdit_ARE/AlphaEdit_ARE_main.py", "memit_ARE/memit_ARE_main.py"):
        left = [l for l in (PORTED / rel).read_text().splitlines() if "cuda" in l.split("#")[0] and "torch.cuda.empty_cache()" not in l]
        assert not left, f"{rel}: unported binding(s): {left}"
    out = ROOT / "logs" / "c10k_route_a_port.diff"; out.parent.mkdir(exist_ok=True)
    diff = subprocess.run(["diff", "-ru", "--exclude=.git", "--exclude=__pycache__", str(PRISTINE), str(PORTED)], capture_output=True, text=True).stdout
    out.write_text(diff, encoding="utf-8")
    changed = [l for l in diff.splitlines() if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    print(f"port: {'APPLIED' if applied else 'ALREADY APPLIED'} ({applied} substitutions); diff lines ±: {len(changed)}; written {out}")
    bad = [l for l in changed if l.startswith("+") and "next(model.parameters()).device" not in l]
    print("non-device '+' lines:", bad or "none")
    return 0 if not bad else 1

if __name__ == "__main__":
    sys.exit(main())
