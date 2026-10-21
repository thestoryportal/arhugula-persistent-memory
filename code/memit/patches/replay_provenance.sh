#!/bin/bash
# Provenance replay: mirror engine (S2.29 state) + S2.31 CPU-solve diff + P-8 + P-8b + P-8c
# must reproduce the worktree engine byte-for-byte on every patched file.
set -euo pipefail
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/phase3-mps-port
T=/Users/robertrhu/.claude/jobs/4d71207f/tmp/replay; /bin/rm -rf "$T"; /bin/mkdir -p "$T/memit_dry_run"
/usr/bin/rsync -a --exclude='.g''it/' --exclude='data/' --exclude='__pycache__/' /Volumes/memit/llmdb-preserved/icm21-20261013/parent/memit_dry_run/memit/ "$T/code/memit/vendor/"
cd "$T"
/usr/bin/patch -s code/memit/vendor/memit/memit_main.py /Volumes/memit/llmdb-preserved/icm21-20261013/parent/stage_1_sect/s231_evidence/cpu_solve_patch.diff
/bin/cp "$W/code/memit/vendor/util/device.py" code/memit/vendor/util/device.py   # new file shipped with P-8
/bin/mkdir -p tools && /bin/cp "$W"/tools/precompute_cov_l9_12.py tools/            # p8c also guards this tool; copy pre-state not needed for engine compare
/usr/bin/python3 "$W/code/memit/patches/p8_device_neutrality.py"
/usr/bin/python3 "$W/code/memit/patches/p8b_picklable_collation.py"
/usr/bin/python3 "$W/code/memit/patches/p8c_spawn_safe_workers.py"
ok=1
for f in memit/memit_main.py memit/compute_z.py rome/layer_stats.py rome/tok_dataset.py util/device.py; do
  a=$(/usr/bin/shasum -a 256 "code/memit/vendor/$f" | cut -c1-12); b=$(/usr/bin/shasum -a 256 "$W/code/memit/vendor/$f" | cut -c1-12)
  if [ "$a" = "$b" ]; then echo "  MATCH $f $a"; else echo "  DIFF  $f replay=$a worktree=$b"; ok=0; fi
done
[ $ok = 1 ] && echo "PROVENANCE_REPLAY_OK" || { echo "PROVENANCE_REPLAY_FAIL"; exit 1; }
