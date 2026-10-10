# Astra r3 binding verdict — git automation (MB7/MB10 fix at 9ea1357)

Reviewer: GPT-6-Astra, reasoning effort high, read-only (`codex exec`, graft disabled). Packet: `astra_gitauto_r3_packet.md`. Run finished 2026-10-10T09:20Z.
CI on exact head 9ea1357: run 38040803583, completed/success. Checkpoint 16e0294: run 38040904451, completed/success.

---

VERDICT: NO-GO

1. **Finding 3 remains open.** In-memory probes through the real `gate()`/`main()` reproduced:
   - Post-merge PR read raises `KeyboardInterrupt`: no report is emitted.
   - Lock exit raises `SystemExit(0)`: it escapes, permitting exit 0 without a report.
   - Report serialization raises `TypeError`, or stdout raises `BrokenPipeError`: the exception escapes with `ok=true`, `status=MERGED` still recorded.

   The handlers at `tools/git_merge_gate.py:156`, `:282`, `:304` catch only `Exception`; output at `:306–314` is outside their boundary. **Fix:** preserve the merge receipt across `BaseException` handling, normalize post-merge exits to nonzero, and protect serialization, writing and flushing. On output failure, set `ok=false` and emit `MERGED_WITH_FAILURE` plus SHA through an independent fallback; print success only after successful output. Add these regressions. The three original r2 schedules now correctly retain the response SHA and return 1.

2. none found — inspected and probed final admission at `tools/git_merge_gate.py:230–238`: higher attempt, new successful run ID with matching check links, pending/failed rerun, and older in-progress run all refuse before merge. Post-merge rerun detection at `:254–262` returns `MERGED_WITH_FAILURE` with SHA retained. A 100-row response explicitly refuses at `tools/git_hygiene.py:144–145`.

3. **The cooperative paragraph needs operational corrections before adoption.** `results/git_automation_fix2_mb7_20261010T084957.416181Z/build_report.md:23` forbids every actor from editing the PR while locked, but the gate itself changes draft state at `tools/git_merge_gate.py:217`. It also permits previously triggered runs to finish before final admission, although lock acquisition precedes CI polling (`:200–205`); their completion updates would violate its blanket prohibition.

   **Fix:** explicitly exempt the gate’s ready transition and guarded merge; drain candidate-head runs and other pending check/status writers **before acquiring the freeze**; require competing mutations to acquire the same lock or obtain a serialized MAESTRO reservation, rather than merely checking whether it appears free. Enumerate and suspend automatic writers that cannot participate. The local `flock` (`tools/git_hygiene.py:80–92`) cannot enforce cooperation by GitHub-hosted actors. Adoption alone does not establish their participation.

4. **Regression evidence is narrower than claimed.** Ten GREENs exercise the real gate with fixture Git and fake GitHub; three directly exercise adapters (`tests/test_git_automation.py:854–884`). Twelve saved REDs fail relevant assertions. The inventory-adapter RED instead dies with “gh pagination returned a non-list”: its positional REST responses are incompatible with r2’s command sequence, before the intended assertions. **Fix:** use a command-aware fake supporting both implementations, prove r2 fails the inventory/attempt assertions, and add adapter-through-gate coverage. Also, the older-run test injects pending evidence from the first read (`:693–704`); add a final-read-only injection.

5. **First use after correction and re-review:** adopt and establish the corrected coordination; create an isolated detached integration worktree sharing the inventory; fetch and merge current `origin/master`; stop on conflicts. Verify generated state and both suites, push normally, obtain successful exact-head Linux CI, drain/freeze candidate writers, then run hygiene `--apply` and merge-gate `--apply`, retaining receipts. Require post-merge master CI and successful report delivery (`tools/git_merge_gate.py:266–314`). Retain worktrees pending separately authorized removal.

All three source hashes match `9ea1357`. Full suites were not rerun; probes were read-only simulations.

🌱 graft saved ~37,942 tokens this turn, 1 successful call.