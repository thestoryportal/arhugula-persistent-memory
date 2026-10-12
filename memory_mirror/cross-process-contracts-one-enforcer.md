---
name: cross-process-contracts-one-enforcer
description: For a cross-process safety contract (who yields to whom), use one enforcer on the winning side only when it covers every required failure path, identify processes by anchored inventory patterns, use one deadline origin. Adding watchers drew two Astra NO-GOs.
metadata:
  type: feedback
---

2026-10-11 (MAESTRO35, research-engine "science goes first" signal). SR v1 used a polling watcher and got Astra r3 NO-GO, mostly for an idle-check race. SR v2 added a lock (which fixed the race), a watcher, a controller heartbeat thread, a registry and a startup handshake, and got r4 NO-GO with six new blockers. Every one of them lived in a part added to fix r3. SR v3 removed all of them: `pending` on the science side publishes under the lock, kills research-engine processes found by anchored command patterns, and confirms none remain after the publish, within 30 s of invocation. SR3 remained NO-GO for uncovered failure-triggered termination; this recipe is not approved authority. Files: `results/research_engine_phase1_20261011/science_reservation_contract_v{1,2,3}.md`, `astra_spec_r{3,4,5}_verdict.md`.

**Why:** every extra moving part is another hinge to rust: it has its own startup, death, timing and identity cases, and a reviewer will find each one. You will be mid-revision and think "add a watcher (or heartbeat, or registry) to catch that case." That is the moment. Ask first: *which side must win, and can that side alone enforce it?* Re-read the requirement's own words (here, R1 at `astra_spec_r1_verdict.md:17`), not your earlier design's means. Then:
- Use one enforcer on the winning side only when the full contract, including failure-triggered termination, is covered. The losing side only checks under the same lock before its irreversible step (admission, publication).
- Identify processes by an anchored pattern over `ps` (executable path + a session token argument). Never match a bare token: Codex and Claude argv carry whole briefs. Never use a registry or a living parent.
- Use one deadline origin (invocation), a background `sleep` timer, and 2 s caps on every command. Use no wall-clock comparisons.
- Confirm absence with an inventory taken *after* the publish, on every path.

**Host facts found on the way:** `/usr/bin/lockf -k` and Python `fcntl.flock` exclude each other on /Volumes/memit (APFS). `ps -E` shows no environment on macOS 26, so env markers are unusable. `new1_supervisor.py` and `v13_launcher.py` start children with `start_new_session=True`. `brew install neo4j` upgrades six shared libraries, so run `--dry-run` first. Related: [[resolve-the-gates-real-criterion]], [[encode-recurring-discipline-as-a-gate]], [[gpu-gate-refuses-any-venv-python]].
