
### Enforcement clarifications frozen before real diagnostic execution

The RSS watchdog stops **at or above 11 GiB**. Computation, admission and pin checking retain the 600-second cap. After stopping the isolated worker, terminal error IO has its own **5-second** bound; kill/reap cleanup is separately bounded to **5 seconds**, with pipe closure on every exit including interruption. These cleanup bounds permit recording a halt, not further arithmetic or a retry.

The commit condition is **exit 0 plus a final `terminal` receipt with status `MEASURED` binding the exact `result.json` SHA**. A result file alone never commits the diagnostic. If failure occurs after result creation, preserve its original scalar bytes and append a **`halted`, `INVALID`, `result_committed:false`** receipt when IO permits; do not attempt an exclusive rewrite. A partial JSON or missing/mismatched/non-MEASURED terminal receipt is unaccepted. Disk budgeting reserves 8 KiB for error recording during nonterminal receipts; all actual files still total strictly below 1,000,000 bytes. Denied or blocked output IO yields a visible error and nonzero exit, never a successful run.
