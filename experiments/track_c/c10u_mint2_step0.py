#!/usr/bin/env python3
"""D-C10u-mint2 explicit no-persistent-write admission stage (operator use only).

Usage: c10u_mint2_step0.py reproduce|frozen|v2|control --law3-ref <known baseline>
Normally c10u_mint2_arms.py orchestrates these admissions automatically.
Importing this entrypoint does not import torch or a model.
"""
import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from c10u_mint2_arms import main

if __name__ == "__main__":
    sys.exit(main(step0_only=True))
