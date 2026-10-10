# Codex brief — D-C10t-secondkey fix round 1 (advisor implementation review FIX-FIRST)

Same hard limits as your implementation brief (no model, no GPU, no commits; do not edit the prereg — it is hashed into the run identity). Read `results/c10t_secondkey_advisor_impl.md` in full and fix:

- **B1** — split `runtime()` into a model-free `preflight` (refuse inherited knobs, engine fingerprint) called BEFORE any marker file (`run.json` at `arms.py:532`, `second_started.json` at `:547`) is written, and a harness loader after; same change in `step0.py:138`. Selftest: a stale knob leaves no marker file behind.
- **B2** — the string-vs-token-id count is reported, not gated: keep only the check that the string count matches its own rows; report `string_minus_full` beside the binding count (`read.py:315`). Selftest: one extra string hit leaves the label unchanged.
- **B3** — prove the `sys.settrace` observer on `compute_z` (`arms.py:258–294`) inert: in `run_pass` before `:496`, run `compute_z` unobserved twice and observed once on the first canonical and the first second-key request; require the observed difference within max(10 × floor, 1e-4) (the c10s rule); record it, halt on failure, add it to `validity`. The review file has the code. Selftest for the rule.
- **Advisories to take:** (a) INVALID-ADMISSION is a pre-registered outcome — record it as such, not as a HALT diagnostic (`step0.py:173,179–182`; `arms.py:535,567–570`); (b) assert the script's own repo root equals `LLMDB_ROOT` and pass `halt()` the resolved root; (c) record in the run identity the program ruling **D-C10t-p5rule**: p5 is selected from the raw five-layer mean, as implemented (no code change).

Run the selftest and `py_compile`. Append a "Fix round 1" section to `results/c10t_secondkey_codex_impl.md` (each fix with file:line and its selftest), then write the marker file **`results/c10t_secondkey_fix1_done.md`** (one line: selftest count and PASS). Then say DONE.
