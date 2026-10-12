# Operator answers — research-engine phase 1 (2026-10-11, ~05:15Z, via AskUserQuestion to MAESTRO35)

1. Adding the science-reservation step to every science launch (spec v3 §13 admission row; SR §7): **"Yes, add the step (Recommended)"**.
   Question as asked: before a run starts waiting for its turn, MAESTRO puts a "science is waiting" note in a shared folder and removes it when the run ends; the research engine watches that folder and gets out of the way within 30 seconds; the science runs and their safety checks stay exactly as they are.
2. Letting the Neo4j Homebrew install upgrade 6 shared libraries (libpng, pcre2, glib, xorgproto, cairo, harfbuzz; dry-run receipt `provisioning_dryrun_20261011.txt`): **"Yes, allow the updates (Recommended)"**.

Context: asked before Astra spec r3, which returned NO-GO on the contract's mechanics (T1–T4). The answers approve the step and the upgrades, not SR v1's mechanics; SR v2 must keep the step's shape (note before waiting, removed at end, research engine yields within 30 s; science gates unchanged). A redesign that changed that shape would go back to the operator.
