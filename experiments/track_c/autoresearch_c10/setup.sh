#!/bin/bash
# The setup check: prepare.py under the Seatbelt profile (.sandbox.sb), output to prepare.log. See run.sh.
cd "$(dirname "$0")" || exit 1
/usr/bin/sandbox-exec -f .sandbox.sb .venv/bin/python prepare.py > prepare.log 2>&1
rc=$?
if [ $rc -eq 71 ]; then
  echo "setup.sh: the check never started — this wrapper was not launched as a bare command, so it stayed inside the" \
       "shell sandbox where the GPU is unavailable. Launch it exactly as ./setup.sh (see program.md)." | tee -a prepare.log
fi
exit $rc
