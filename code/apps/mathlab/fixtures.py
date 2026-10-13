"""Synthetic build fixtures only. Never reads or loads a model."""
from pathlib import Path
import numpy as np
import torch

from apps.mathlab import mathlab_runtime as R

BAND = [4, 5, 6, 7, 8]
ARMS = ["A1_single", "A2_coherent2", "mint1_s0", "mint1_s1", "mint1_s2", "A7_coined_coined"]


def make_harvest(parent):
    out = R.new_directory(parent, "fixture_harvest")
    files = {}; covariances = {}; clean = {}; specs = []
    for kind, templates in (("CANON", 1), ("PTEST", 3)):
        for f in range(24):
            for j in range(templates):
                key = f"p{len(specs):03d}"
                specs.append(dict(key=key, kind=kind, subject_id=f, template_id=j, subject=f"subject{f}", template="{}", text=f"subject{f}"))
                clean[key + ".ids"] = torch.tensor([1, 2]); clean[key + ".subject_last"] = torch.tensor(1)
                for l in BAND:
                    clean[f"{key}.l{l}.k"] = torch.tensor([[0., 1., 0.], [1., 0., 0.]], dtype=torch.float16)
                    clean[f"{key}.l{l}.h"] = torch.zeros(2, 2, dtype=torch.float16)
    K = torch.zeros(3, 24); K[0, :12] = 1; K[1, 12:] = 1
    for l in BAND:
        clean[f"clean.k{l}.mean"] = K.half(); clean[f"clean.k{l}.templates"] = K.T.half()
        path = out / f"cov_l{l}.npz"
        np.savez(path, **{"mom2.mom2": np.zeros((3, 3), dtype=np.float32), "mom2.count": np.array(24)})
        covariances[str(l)] = dict(path=str(path), sha256=R.sha_file(path), tier=R.TIER)
    files["clean.pt"] = R.save_tensors(out / "clean.pt", clean)
    weights = {}
    zs = torch.zeros(2, 24); zs[0] = 2
    for arm, score in zip(ARMS, [.95, .96, .7, .5, .6, .2]):
        tensors = {}
        for l in BAND:
            rf = torch.zeros(2, 24)
            rf[0, :12] = (2 * score / 5) * 13 / 12
            rf[0, 12:] = (2 * (1 - score) / 5) * 13 / 12
            A = np.eye(3, dtype=np.float32) + K.numpy() @ K.numpy().T
            update = torch.from_numpy(np.linalg.solve(A, K.numpy() @ rf.numpy().T).T.copy())
            p = f"l{l}."
            tensors.update({p + "zs": zs.clone(), p + "K": K.half(), p + "Kf": K.clone(), p + "rf": rf,
                            p + "resid": rf.half(), p + "cur": torch.zeros(2, 24, dtype=torch.float16),
                            p + "ca_zero": torch.tensor(True), p + "ca_norm": torch.tensor(0., dtype=torch.float64),
                            p + "Pi_null_n": torch.tensor(3), p + "upd_norm": torch.linalg.vector_norm(update.double())})
            import hashlib
            for key, value in (("Pi_sha256", torch.eye(3)), ("ca_sha256", torch.zeros(3, 3)), ("upd_sha256", update)):
                digest = hashlib.sha256(value.numpy().tobytes()).digest()
                tensors[p + key] = torch.tensor(list(digest), dtype=torch.uint8)
            for j in range(4): tensors[p + f"Pi_probe{j}"] = torch.randn(3, generator=torch.Generator().manual_seed(j))
            if arm == "A7_coined_coined":
                tensors[p + "upd_precast"] = update
                weights[p + "before"] = torch.zeros(2, 3, dtype=torch.float16); weights[p + "after"] = update.half()
        files[f"inloop_{arm}.pt"] = R.save_tensors(out / f"inloop_{arm}.pt", tensors)
        files[f"postedit_{arm}.pt"] = R.save_tensors(out / f"postedit_{arm}.pt", {"fixture": torch.tensor(True)})
    files["weights_A7.pt"] = R.save_tensors(out / "weights_A7.pt", weights)
    counts = dict(zip(ARMS, [68, 71, 46, 37, 40, 14])); identity = {"seed_sources": {}}
    for a in ARMS[2:5]:
        source = out / (a + ".json"); R.write_new(source, {"arm": {"para_full_binding_n": counts[a]}, "tier": R.TIER, "fixture": True})
        identity["seed_sources"][a] = dict(passed=True, record={"path": str(source), "sha256": R.sha_file(source)})
    manifest = dict(tier=R.TIER, fixture=True, decision_id="D-ML-1", prereg_sha256=R.PREREG_SHA,
                    files=files, covariances=covariances, prompts=specs, identity=identity,
                    gates={g: {"passed": True} for g in ("law3", "law5", "observer-parity")},
                    replay_admission={"shared_passed": True, "admitted": ARMS[2:5], "arms": {a: "ADMITTED" for a in ARMS[2:5]}},
                    outcomes={a: dict(used_for_calibration=n, fresh_harvest_count=n if a not in ARMS[2:5] else None,
                                      historical_count_report_only=999 if a not in ARMS[2:5] else n) for a, n in counts.items()})
    R.write_new(out / "manifest.json", manifest)
    return out
