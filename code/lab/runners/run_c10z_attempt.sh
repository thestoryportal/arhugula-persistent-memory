#!/bin/bash
set -u
W="$(cd "$(dirname "$0")/../../.." && pwd)" || exit 2
S="$W/code/lab/runners/run_c10z_stage.sh"; OUT="${C10Z_OUT_DIR:?C10Z_OUT_DIR required}"
case "$OUT" in /*) ;; *) echo "C10Z_OUT_DIR must be absolute"; exit 2 ;; esac
step(){ "$S" "$1"; rc=$?; echo "STAGE_${1}_EXIT=$rc"; return "$rc"; }
step 0 || exit $?
step 1 || exit $?
next=$("$W/.venv/bin/python" -I -c '
import json,sys
r=json.load(open(sys.argv[1])).get("reading")
if not isinstance(r,dict) or "next_stage" not in r: sys.exit(4)
n=r["next_stage"]
if n is None: print("null")
elif type(n) is int and n==2: print("2")
else: sys.exit(4)' "$OUT/run.json") || { rc=$?; echo "STAGE1_READING_INVALID rc=$rc"; exit 4; }
echo "STAGE1_NEXT=$next"
[ "$next" = "2" ] || exit 0
step 2; exit $?
