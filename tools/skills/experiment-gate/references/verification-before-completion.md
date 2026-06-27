# Verification Before Completion

A completion claim needs fresh command output and saved artifact readback.

Before saying a run, gate, or closeout is done:

- Read the saved result JSON from disk.
- Run the relevant checker (`tools/experiment_gate.py check-result`, method-port audit, or closeout check).
- Save the stats/gate package path.
- Re-read any canonical document edited on the network filesystem.
- Report blocked checks as blocked, not as caveats.

For experiments, final done remains `python3 tools/closeout_check.py <D-ID>` green after CORPUS/tracker closeout.
