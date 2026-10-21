# C10 autoresearch fence v13

The loop edits MLP weights using public training facts. Evaluation stays in a separate trusted scorer.
The program session installs a fresh repository and fence with v13_build.py. It never reuses a destination or commits.
D-C10r-seal's binding design is experiments/c10r/design/C10R_LOOP_SEALING_V13.md.

Run no-model checks with:
  .venv/bin/python -I -B code/lab/track_c/autoresearch_c10/test_plumbing.py
Build two fresh destinations, one production and one --fixture, then run v13_probe.py with
--production <production-fence> --fixture <fixture-fence> --report experiments/c10r/reviews/c10r_seal_v13_probe.md.
The fixture is program-controlled and is absent from a production fence. It imports no torch or model code.
Raw scorer and probe text stays private. Any unverified control is FAIL; there is no unsandboxed retry.

Default installation:
  .venv/bin/python -I -B code/lab/track_c/autoresearch_c10/v13_build.py
creates /Volumes/memit/llmdb-preserved/icm21-20261013/parent/autoresearch_v13_c10 and autoresearch_fence_v13_c10.
Use --sandbox and --fence for a permitted staging root. Paths are embedded in profiles and manifests:
regenerate at final installation, rather than moving a bundle.

Graft may rewrite tracked caches and ignore files (experiments/c10r/runs/autoresearch_replay_c10_exp2loc/halts/c10r_exp2ctl_halt_diagnostic.json).
The seed copies no graft directory or history, and includes /graft/ before initialization.
macOS immutable flags seal the root entries and static files; runs/ and .agent_capture/ are precreated,
so existing edit.py and results.tsv remain writable. Completed private scorer areas are frozen.
There are no repository metadata or graft caches in the fence or scorer areas. Hooks are disabled,
MCP is empty, and the clean environment disables graft refresh/ignore-file writes.
Run v13_graft.py <fence> --processes for the pre-launch sweep. It checks immutable barriers,
ignore hashes, graft files, tracked/history caches and active graft processes, without invoking graft.
The launcher requires this sweep; the watcher repeats the filesystem/index checks during the loop.
An external process that deliberately clears immutable flags remains outside this boundary;
do not attach an indexing session or explicitly run graft against any protected area.

The program session, after the shared-z and location-control jobs finish, runs v13_law3_equivalence.sh.
It uses both profiles via run.sh, verifies the original fd16592 baseline hashes and metrics,
then scores the cleaned 73f78ce base. Only a valid guard failure selects the pre-registered 92acd03 fallback.
No error, timeout, failed instrument gate, stale hash, or malformed score selects the fallback.

launch.sh requires a current PASS no-model record and PASS LAW#3/cleaned-base record.
A program reviewer must attest the completed agent controls in the sealed no_model_gates.json
after checking the transcript; v13_probe.py does not turn agent claims into that attestation.
The program-side watcher binds the new UUID, real transcript, repository, capture and private output paths.
Missing or malformed audit evidence halts the loop. The tripwire detects copying and has a documented paraphrase limit.

prepare.py is retired. Old check_equivalence.py and tmux equivalence helpers are v12 commands;
use v13_law3_equivalence.sh for v13. Do not run edit.py directly, install dependencies, expose the
harness to the editor, resume the old session, or promote an optimizer score as evidence.
