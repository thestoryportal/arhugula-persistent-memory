#!/bin/bash
# Kill a run that exceeded its timeout. From inside Claude Code's Bash sandbox the process list is not visible, so
# this wrapper is excluded from that sandbox.
pkill -f "python edit.py"; pkill -f "prepare.py --score"; pkill -f "python prepare.py"
sleep 1
pgrep -fl "edit.py|prepare.py" || echo "no run processes left"
