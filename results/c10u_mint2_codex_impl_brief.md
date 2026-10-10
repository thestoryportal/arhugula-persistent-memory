# Codex brief — implement step 3, D-C10u-mint2 (prereg v3 FROZEN), model-free

**Hard limits.** No model, no torch on the GPU, no driver run. Do not touch `memit_dry_run/`, `experiments/track_c/c10e_bandknob.py`, `experiments/track_c/c10s_sharedz_*`, `experiments/track_c/c10t_secondkey_*`, `experiments/track_c/autoresearch_c10/`, `CORPUS/`, `visualization/`, existing results, `results/c10u_mint2/v2_wordlist.json`, or `/Volumes/memit/llm-database-poc-mirror/autoresearch_*`. Do not edit the prereg (it will be hashed into the run identity). Do not commit or push. `/usr/bin/git`.

## Task
Implement `docs/C10U_MINT2_PREREG.md` v3 (frozen; read all of it, including §7's fold log and the decision `D-C10u-A7V2` in runbook §5.2) as new files `experiments/track_c/c10u_mint2_{arms,read,selftest}.py` (plus any step the prereg defines before the runs). Reuse the program's reviewed minting machinery from the earlier mint experiment (`experiments/track_c/c10l_mint_*`, CORPUS/45) wherever the prereg says to, citing file:line, and follow the reviewed patterns of `experiments/track_c/c10s_sharedz_{arms,read,selftest}.py` and `c10t_secondkey_{arms,read,selftest}.py`:
- this arm's own halt file `architecture_profile/c10u_mint2_halt_diagnostic.json`;
- a model-free preflight (inherited knobs refused, engine fingerprint) BEFORE any marker file;
- write-and-reread JSON;
- source hashes including the prereg and the word list;
- occupied outputs never overwritten;
- every threshold and label as a pure rule in the reader;
- MPS has no float64: move to CPU before any `.double()`;
- an inertness/known-baseline (LAW#3) gate the prereg requires before new data is trusted.

Read the engine/harness source you depend on before writing against it. Both arms (A: A7-V2 two minted ids; B: frozen values, modifier-only) and the run schedule (the 14 runs, the conditional runs, replication, and the mint-1(frozen) ×3 reproduction with LAW#3 HALT on a miss, as §7 records) must be implemented exactly as frozen. Provide one orchestrating command per stage, so the program session can run the schedule stage by stage.

Run the selftest and `py_compile`. Write **`results/c10u_mint2_codex_impl.md`**: files created, how each prereg element is implemented (file:line), the run schedule with per-stage commands and time estimates, the decisions you took where the prereg is silent, anything you believe the prereg gets wrong (report; do not deviate), and the selftest output verbatim. Then say DONE.
