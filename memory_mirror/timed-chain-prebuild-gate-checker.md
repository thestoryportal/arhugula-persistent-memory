---
name: timed-chain-prebuild-gate-checker
description: Before a step that starts a deadline (R1 bind's 870 s window), commit a gate checker and dry-run it on a consumed prior run
metadata:
  type: feedback
---
When a chain step starts a clock (the R1 bind opens an 870-second window that must also cover Gate D, the inventory and every commit), write the whole Gate D checker and the next-step driver BEFORE that step, commit them, and dry-run the checker against an already-consumed earlier run (the R1J bind): the checks that must fail there (consumed core, expired window) must FAIL, and every code path gets exercised. The R1N dry run caught a wrong JSON key (`retained_dir` is under `collector`) and a DST bug (`time.mktime` minus `time.timezone`; use `calendar.timegm`) that would otherwise have surfaced inside the live window. Result: C→D→E took 61 s with 808 s spare.

Also: write an evaluator's output to scratch and copy it into the evidence directory afterwards, when that directory is the evaluator's own receipt census, so it cannot count itself.

BUT a fast, clean run is not a verified gate (Astra r14 DEFECTIVE on R1N): (1) get and RECORD a writer reservation from the operator ("please don't touch the Intel Mac until I say") before A — a survey naming them as the only writer is not control; (2) the receipt census covers every measurement receipt incl. .tsv/.txt cited by the manifest plus scratch copies and rtk tee logs, not just N's filename glob; (3) the checker must implement each GD check in full (complete paths vs committed bytes, recursive old roots, reconstructed bound manifest, reservations), and get Astra review BEFORE use; (4) preserve raw survey output (rtk tee logs live in ~/Library/Application Support/rtk/tee/); never write "byte-identical" from a size compare.

**Why:** a crash or doubt inside the window ends the one-attempt authorization; preparation is free beforehand.
**How to apply:** any authorized single-attempt chain with a deadline (R1 inventory, future Intel commissioning). Related: [[test-first-one-round-builds]]; [[one-shot-run-needs-real-scale-dry-run]] (Claude auto-memory, not memory_mirror/).
