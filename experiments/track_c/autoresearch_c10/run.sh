#!/bin/bash
# One experiment run: edit.py under the macOS Seatbelt profile the launcher wrote (.sandbox.sb), output to run.log.
# Claude Code's own Bash sandbox blocks the OS-version query PyTorch needs for the GPU, so this wrapper is excluded
# from that sandbox and the profile here enforces the same file boundary with the GPU allowed. The scorer and the
# fingerprint subprocesses inherit the profile.
cd "$(dirname "$0")" || exit 1
/usr/bin/sandbox-exec -f .sandbox.sb .venv/bin/python edit.py > run.log 2>&1
rc=$?
if [ $rc -eq 71 ]; then
  echo "run.sh: the run never started — this wrapper was not launched as a bare command, so it stayed inside the" \
       "shell sandbox where the GPU is unavailable. Launch it exactly as ./run.sh (see program.md)." | tee -a run.log
fi
exit $rc
