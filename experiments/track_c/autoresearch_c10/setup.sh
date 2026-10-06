#!/bin/bash
# The setup check: prepare.py under the Seatbelt profile beside this script, output to prepare.log in the sandbox. See run.sh.
FENCE="$(cd "$(dirname "$0")" && pwd)"
SB=/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10
cd "$SB" || exit 1
export PYTHONDONTWRITEBYTECODE=1   # the program checkout is read-only to the run; no pyc anywhere
/usr/bin/sandbox-exec -f "$FENCE/.sandbox.sb" .venv/bin/python -c 'import torch; assert torch.backends.mps.is_available(), "MPS unavailable"; print((torch.ones(2, device="mps") * 2).sum().item())' > preflight.log 2>&1
rc=$?
if [ $rc -eq 71 ]; then
  echo "setup.sh: the check never started — this wrapper was not launched as a bare command, so it stayed inside the shell sandbox. Launch it exactly as $FENCE/setup.sh (see program.md)." | tee prepare.log
  exit 71
elif [ $rc -ne 0 ]; then
  echo "setup.sh: INFRASTRUCTURE HALT — the GPU is not available inside the profile (see preflight.log). Write HALT.md and stop." | tee prepare.log
  exit 70
fi
/usr/bin/sandbox-exec -f "$FENCE/.sandbox.sb" .venv/bin/python prepare.py > prepare.log 2>&1 &
echo $! > setup.pid
wait $!
rc=$?
rm -f setup.pid
exit $rc
