**PROCEED — build-only GPT-family helper review; not binding Astra.** No blocking issue found.

- `tools/new1_identity_diag.py:277`: `Popen` creation and handle assignment occur together off the signal-handling thread. Cancellation closes the release writer; late registration retains cleanup ownership. Cleanup bounds waiting and reports failure visibly (`:294`); polling reaps exited workers before group signalling (`:267`).
- `tools/new1_identity_diag.py:329`: the five-second launch bound is capped by the original absolute deadline. The watchdog stays armed. Release occurs only after registration, PID recording, RSS validation and both deadline checks (`:333`, `:340`, `:345`).
- `tools/new1_construction_diag.py:226` and `tools/new1_identity_diag.py:401`: workers wait before verification or arithmetic. The guard rejects EOF, absent/late release and parent death; after release it checks parent liveness and the original deadline (`identity:237`, `:245`).

Compared with `before/`, arithmetic, inputs, tolerances, caps, output writer and outcome table remain unchanged. The scope revision is appended.

Recomputed candidate SHA-256 values match `green_third.json`:

- Identity: `c4601c6df61cf7c36c6223d5955236c0c8f901ded216889755bcd397ae25c1d3`
- Construction: `87a4f5425f5df5bd85b3d47455053a60965e7510297f1b8e3472c73c931411e7`
- Tests: `40e2cd2905053955c7dac510860609e0a47a8e3ef661442ea1a9c90e0c660810`

Saved evidence under `results/mathlab_staging/new1_construction_diag_fix_20261010T074908.035652Z/` reproduces the original watchdog race and follow-up failures. Its final log records **165 PASS: 43 construction + 27 identity + 34 geometry + 61 supervisor**, in **9.225 s**, exit 0.

I performed no edits, tests, Python or runtime launches. Full-size native SVD, real inputs/admission and host cap/niceness enforcement remain **UNVERIFIED**. MAESTRO4 owns binding Astra review and launch.

Review complete; nothing remains in flight. Context directive persists: before approximately 20% remains, stop new work and hand off done/in-flight/exact paths/next steps/open risks, restating the directive.
