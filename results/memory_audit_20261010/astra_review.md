VERDICT: ACCEPT-WITH-FIXES

Sampled review; five actionable findings:

1. **Conditional fallback became a standing instruction.** `memory_mirror/MEMORY.md:7` says “Never claim coined multi-word facts live in weights; route to Git/side-store.” The note’s premise is **accepting** a changed product contract (`c10-accept-bounded-means-hybrid-not-general-db.md:8`); its newly added “still binding” at line 15 obscures that condition. This conflicts with the continued in-weight route in `fallback-that-nullifies-spec-is-not-f1-closure.md:27–31`.
   
   Replace the index hook with: **“If accepting bounded deployment, label side-store routing an engineering fallback; C10 remains OPEN for F1.”**
   
   Replace the note’s line 15 with: **“Historical conditional fallback (D-C10g-strengthlayers); not authorization to abandon the in-weight requirement or close C10.”**

2. **The review waiver contradicts the binding gate.** `memory_mirror/codex-runs-inline-from-claude-bash.md:16` still permits “WAIVE it for decisive/foregone/mechanistically-forced results.” `CLAUDE.md:16` requires Astra high at **every promote gate**; the note itself requires it at line 12. Its Perplexity fallback also needs that boundary.
   
   Replace the fallback/calibration instructions with: **“Perplexity may provide advisory input when Codex authentication fails, but does not replace the binding Astra-high promote review. Keep promotion blocked until that review completes; do not waive it because a result appears decisive.”**

3. **“Both instances FIXED” overstates collision protection.** `memory_mirror/durable-artifact-path-collision.md:16` newly declares both hazards fixed. However, `experiments/scale/g6_scale_n_param.py:247` defaults `RESULT_TAG` to `""`, and line 248 opens the resulting canonical filename with `"w"`. An untagged model variant can still overwrite it.
   
   Replace line 16 with: **“The mode collision is fixed in g6_scale_n.py:236. The parametrized script supports RESULT_TAG but defaults to an empty suffix (g6_scale_n_param.py:247–248); model/variant isolation remains caller-enforced. Require a unique nonempty tag and verify the destination before dispatch.”**

4. **A useful retirement lesson was lost.** `fd77f7e:memory_mirror/c10k-route-a-resume.md:12` contained: **“two advisor runs on one packet can race on one output path — give each run its own path.”** The tombstone at the current file’s line 7 points elsewhere, but no live memory preserves this reviewer-output race warning; the surviving unique-output guidance concerns builder completion detection.
   
   Append to `memory_mirror/codex-runs-inline-from-claude-bash.md`: **“Give every advisor/reviewer invocation its own output path, including concurrent reviews of the same packet; shared output paths can race.”**

5. **Deployment instructions still disagree.** `memory_mirror/local-only-no-rented-compute.md:10` correctly names M3 Pro as science **and deployment** hardware, supported explicitly by committed `EXPERIMENT_RUNBOOK.md:89`. `AGENTS.md:66` still says “Deployment target = operator Intel CPU.”
   
   Replace that sentence with: **“Science hardware and deployment target are the operator’s MacBook M3 Pro, 48 GB unified memory (D-HW-1); the Intel-CPU target is retired.”**

Graft savings unavailable: one failed call.