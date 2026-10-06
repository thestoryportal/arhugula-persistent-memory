#!/usr/bin/env python3
"""Extract the two control numbers prepare.py's reference check needs, and nothing else.

Usage: write_reference_controls.py <reference_run.json> <out.json>

prepare.py refuses to run unless a past run's control arms (A1 single-token, A2 two-token) each reached 68/72. The
full run record also holds that run's coined-value results, which the sandboxed agent must not see (fence v6,
2026-10-06, after the cross-family reviewer read them through the profile), so the launcher writes this extract into
the read-only fence directory and prepare.py reads it from there.
"""
import json
import sys

src, out = sys.argv[1:3]
arms = json.load(open(src))["recipes"]["baseline"]["arms"]
extract = {"recipes": {"baseline": {"arms": {
    "A1_single": {"para_full_n": arms["A1_single"]["para_full_n"]},
    "A2_coherent2": {"para_full_n": arms["A2_coherent2"]["para_full_n"]},
}}}, "source": "control fields of the program's reference run; everything else withheld from the sandbox"}
json.dump(extract, open(out, "w"), indent=1)
print(out, extract["recipes"]["baseline"]["arms"])
