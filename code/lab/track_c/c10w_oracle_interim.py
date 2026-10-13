"""Interim, non-routing seed-0 configuration reading of a C10W P1 directory.

Imports the pinned reader unmodified and calls its own validate_phase() and
configuration(); adds nothing to the reading. Written because the P1 verdict
review (advisor, 2026-10-07) required the cited interim record to carry the
class line, the Decision-ID and its producing script (prereg :3, :324).
Usage: c10w_oracle_interim.py <p1_dir> <out_name.json>  (write_json refuses to overwrite).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c10w_oracle_read as R

STATUS = "INTERIM — seed-0 configuration only; no final label, no routing (prereg §8 item 3); step 5 not read"


def interim(p1):
    p = R.load_json(p1 / "eval.json")
    R.validate_phase(p)
    shuf = p["recipes"]["oracle_p1"]["arms"][R.SHUF]
    return {"class": R.CLASS, "decision_id": R.DECISION_ID, "status": STATUS,
            "producer": R.file_ref(Path(__file__)), "reader": R.file_ref(Path(R.__file__)),
            "p1_eval": R.file_ref(p1 / "eval.json"),
            "oracle_p1_A7_configuration": R.configuration(p, "oracle_p1"),
            "shuf_cross_score_vs_original_map": shuf["extra"]["cross_score"]["para_full_n"],
            "shuf_own_map_para_full_n": shuf["para_full_n"]}


def main(argv):
    p1, name = Path(argv[1]).resolve(), argv[2]
    out = p1 / name
    R.write_json(out, interim(p1))
    print(out)


if __name__ == "__main__":
    main(sys.argv)
