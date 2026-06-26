import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

os.environ.setdefault("HP_CANDIDATE", f"{LLMDB_ROOT}/configs/hparams/qwen25_3b_memit_hparams_band412.json")
os.environ.setdefault("CANDIDATE_NAME", "wide_band412")
os.environ.setdefault("OUT", f"{LLMDB_ROOT}/results/c10f_band412.json")
os.environ.setdefault("DECISION_ID", "D-C10f-band412")
os.environ.setdefault("PREREG", f"{LLMDB_ROOT}/docs/C10_BAND412_PREREG.md")
os.environ.setdefault("RUN_LABEL", "C10 W-realization widened-band [4,12] test")

from c10e_bandknob import main

if __name__ == "__main__":
    sys.exit(main())
