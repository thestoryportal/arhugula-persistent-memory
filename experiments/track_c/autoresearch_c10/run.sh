#!/bin/bash
# One experiment run: edit.py under the macOS Seatbelt profile beside this script, output to run.log in the sandbox.
# Claude Code's own Bash sandbox blocks the OS-version query PyTorch needs for the GPU, so this wrapper is excluded
# from that sandbox (by its exact absolute path) and the profile here enforces the same file boundary with the GPU
# allowed. The scorer and fingerprint subprocesses inherit the profile. This file lives in the fence directory,
# which the agent cannot write; the launcher rewrites it on every launch.
FENCE="$(cd "$(dirname "$0")" && pwd)"
SB=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
cd "$SB" || exit 1
export PYTHONDONTWRITEBYTECODE=1   # the program checkout is read-only to the run; no pyc anywhere
# GPU preflight inside the profile: a missing GPU is an infrastructure halt, never a failed idea
/usr/bin/sandbox-exec -f "$FENCE/.sandbox.sb" .venv/bin/python -c 'import torch; assert torch.backends.mps.is_available(), "MPS unavailable"; print((torch.ones(2, device="mps") * 2).sum().item())' > preflight.log 2>&1
rc=$?
if [ $rc -eq 71 ]; then
  echo "run.sh: the run never started — this wrapper was not launched as a bare command, so it stayed inside the shell sandbox. Launch it exactly as $FENCE/run.sh (see program.md)." | tee run.log
  exit 71
elif [ $rc -ne 0 ]; then
  echo "run.sh: INFRASTRUCTURE HALT — the GPU is not available inside the profile (see preflight.log). Do not count this as a failed idea; write HALT.md and stop." | tee run.log
  exit 70
fi
/usr/bin/sandbox-exec -f "$FENCE/.sandbox.sb" .venv/bin/python edit.py > run.log 2>&1 &
echo $! > run.pid
wait $!
rc=$?
rm -f run.pid
exit $rc
