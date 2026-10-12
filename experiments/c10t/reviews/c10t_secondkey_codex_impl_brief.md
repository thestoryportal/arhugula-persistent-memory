# Codex brief — implement step 2, D-C10t-secondkey (prereg v2 FROZEN), model-free

**Hard limits.** No model, no torch on the GPU, no driver run (the GPU is running D-C10s-solvefeas). Do not touch `memit_dry_run/`, `experiments/track_c/c10e_bandknob.py`, `experiments/track_c/c10s_sharedz_*`, `experiments/track_c/autoresearch_c10/`, `CORPUS/`, any existing results, or `/Volumes/memit/llm-database-poc-mirror/autoresearch_*`. Do not commit or push. `/usr/bin/git`.

## Task
Implement `docs/C10T_SECONDKEY_PREREG.md` v2 (frozen; read all of it, including §7's fold log) as new files `experiments/track_c/c10t_secondkey_{arms,read,selftest}.py` (and an offline step-0 script if §2 calls for one). Follow the patterns the program already reviewed in `experiments/track_c/c10s_sharedz_{arms,inertness,read,selftest}.py`:
- a halt() that writes this arm's own diagnostic `architecture_profile/c10t_secondkey_halt_diagnostic.json`;
- write-and-reread JSON;
- source hashes in a run identity, with the driver refusing on any mismatch;
- occupied outputs never overwritten;
- every threshold and label as a pure rule in the reader;
- a model-free selftest.

Read the engine and harness source you depend on (`memit_dry_run/memit/memit/*.py`, `c10e_bandknob.py` `my_edit`/`restore_layers`/`run_law5`) before writing against them, and cite file:line in comments where the prereg does. The engine stays unmodified, and the second request list enters through a driver wrapper around `my_edit` as §2 says.

Run the selftest and `py_compile`. Write **`results/c10t_secondkey_codex_impl.md`**: files created, how each §2/§3 element is implemented (file:line), the decisions you took where the prereg is silent, anything you believe the prereg gets wrong (report it; do not silently deviate), and the selftest output verbatim. Then say DONE.
