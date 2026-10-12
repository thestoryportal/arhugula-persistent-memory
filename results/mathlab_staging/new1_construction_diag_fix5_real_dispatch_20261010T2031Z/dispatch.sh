#!/bin/bash
# NEW-1 FIX5 real construction diagnostic — the ONE operator-authorized attempt (f5dbab5). Verbatim from Astra r7 §5.
cd /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a || exit 97
date -u +DISPATCH_START=%Y-%m-%dT%H:%M:%SZ
new1_nice_increment=$(LLMDB_ROOT="$PWD" .venv/bin/python -B -c 'import os,sys;current=os.getpriority(os.PRIO_PROCESS,0);sys.exit("starting niceness exceeds 10") if current>10 else None;print(10-current)') || exit "$?"
LLMDB_ROOT="$PWD" LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 /usr/bin/nice -n "$new1_nice_increment" .venv/bin/python -B tools/new1_construction_diag.py --scope-sha 19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217 --source-sha 744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3
rc=$?
date -u +DISPATCH_END=%Y-%m-%dT%H:%M:%SZ
echo "EXIT_CODE=$rc"
exit $rc
