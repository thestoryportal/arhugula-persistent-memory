# GPT-6-Astra (high) — r6 ruling: NEW-1 FIX5 build review (r5 contract + qualification steps 1–2) and clearance for qualification step 3

Read-only. Worktree = current dir. Your r5 verdict is `results/mathlab_staging/new1_construction_diag_astra_r5.md` (VERDICT: FIX5; contract §2, qualification sequence §3 steps 1–5). Codex MB23 built FIX5; MAESTRO20 verified it and committed it at `7b547d1`. Nothing past r5 §3 step 2 has run: no 20-solo, no 3/3 batch, no inherited-mask launch, no host 100/10. The failed FIX4 batch stays 0/3 permanently.

## Candidate (committed 7b547d1; MAESTRO20 re-hashed all five against the build's handoff table)
tools/new1_construction_diag.py 744f063374a766efbfffc5a1ede73be04a323210e6b4dad48e569e5a41545ec3
tools/new1_identity_diag.py 919b3a11a836973ea4c0d2abdd2514634ea62792e6009e828a63d81f297c3d0d
tests/test_new1_construction_diag.py 995e81cde32c2defd0379ec5bd87d1f78638b462293a3179c479fd73e565a686
tests/test_new1_identity_diag.py 047e1425a30be7daa58194a5f94862b865dee5f09ff0060ed51d6902e5d0ca0e
results/mathlab_staging/new1_construction_diag_scope.md 19dda1126da0f2df2fa5418583cbcd1ba6a4be8411fcb52965b7396e369b9217

Unchanged vs HEAD (MAESTRO20 `git diff --quiet`): `tools/new1_supervisor.py` a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b, `tests/test_new1_supervisor.py` 33c61282862cea1d0297396cb860963bfc48adf33d054db3f933fed11d6d23ec.

The pre-FIX5 bytes are the r5 packet's five hashes (`results/mathlab_staging/new1_construction_diag_astra_r5_packet.md:5–11`); `git diff 7b547d1~1 7b547d1 -- tools/ tests/ results/mathlab_staging/new1_construction_diag_scope.md` is the full source delta.

## The evidence
Receipt dir (RECEIPT): `results/mathlab_staging/new1_construction_diag_fix5_20261010T193454.432828Z/`. Report: `RECEIPT/build_report.md` — sections at lines 7 (pins), 23 (what changed), 36 (RED→GREEN), 72 (actual-parent controls), 91 (acceptance + written qualification commands), 128 (hashes), 149 (limits), 160 (context handoff, written after a Codex context compaction at 37% left — weigh it against the raw receipts, not on its own say-so).

- Inventory: 205 = 188 existing + 17 new (8 C1 + 9 C2); `RECEIPT/fix5_inventory.json`, `RECEIPT/inventory_preservation.json`.
- REDs on unchanged production: `RECEIPT/red_qualifying/index.json` (17 entries, all exit 1). GREENs: `RECEIPT/green_individual/`, `RECEIPT/green_frozen/`, `RECEIPT/green_final/`.
- Actual-parent controls: `RECEIPT/step2_actual_parent_final/` (+ the earlier `step2_actual_parent/`), driver `RECEIPT/parent_control.py`, `RECEIPT/run_parent_controls.py`.
- One full shared-process four-suite run: `RECEIPT/acceptance_result.json` — 205/205, exit 0, 17.8 s.
- FIX5 runner copy `RECEIPT/run_checks.py` (expected count 205; `RECEIPT/runner_delta.diff` vs the historical runner). Scope revision proof `RECEIPT/scope_prefix.json`. Inherited-mask launcher `RECEIPT/fix5_inherited_mask_launch_01.py`, written and UNRUN.
- `RECEIPT/SHA256SUMS`: MAESTRO20 checked all 313 entries, 0 mismatches.

**MAESTRO20 host checks (this session, not new acceptance runs):** a rerun of the four-suite command at `build_report.md:96` gave 205/205 OK, exit 0, 16.4 s. Its log's 17 "ResourceWarning" text hits are the harness echoing its own `-W error::ResourceWarning` argv; MB23's log has the same 17. MAESTRO20 read the C1 injection in `tests/test_new1_identity_diag.py:442–470` (`boundary`): the test pre-blocks only SIGUSR1; its `pthread_sigmask` wrapper calls the real function first and raises `Stop` only when the caller frame is in `new1_identity_diag.py`, is named for the target, and the call was `SIG_BLOCK {SIGINT, SIGALRM}`. The C1 RED failures show the caller mask `[30]` leaving as `[2,14,30]`. Confirm or refute that reading; it is the r5 line between qualifying RED evidence and a test-imposed mask.

## Rule on (cite file:line)
1. **Contract conformance.** Does the delta implement r5 §2 arrangement (c) as written, in the named files only? Check guarded original-mask restoration at every OwnedWorker / deadline / handler critical section r5 names (including the `:495`/`:510` leads and OwnedWorker's matching pattern), and early `INVALID-ENFORCEMENT` refusal before any ownership or timed filesystem work at direct supervision and both parent mains. Name any section that is missed, any partial restoration, or any change outside contract.
2. **RED quality.** Is each of the 17 REDs qualifying under r5 — failing on unchanged production for the contract's reason, at the real boundary, with no test-imposed mask or fixture shortcut? Rule on C1 and C2 separately and name any non-qualifying method.
3. **Steps 1–2 receipts.** Do the actual-parent controls meet r5 §3 step 2 as written: `.2 s` configured bound and `<.3 s` measured, ownership inspected before cleanup, Python return recorded separately from native termination, and preblocked entry giving early refusal with no owner? Was any receipt (including the post-compaction handoff) inconsistent with the raw logs?
4. **Runner and launcher.** Does the FIX5 `run_checks.py` keep the historical execution and stop-on-first-failure contract with an explicit, reviewed count of 205? Does the unrun launcher match r5 §3 step 4's design (mask set before exec, never re-set inside the interpreter, startup time recorded apart from the `.2 s` interval)? Ruling on the launcher's design does not authorize running it.
5. **Clearance.** May r5 §3 step 3 (20 consecutive solo runs, then a fresh 3/3 full batch, through `RECEIPT/run_checks.py`, on a quiet host) start on these exact bytes? State any precondition. Confirm the batch history: FIX4 0/3, and FIX5 starts at 0.

## Verdict
End with exactly one line:
- `VERDICT: GO-QUALIFY`: the build conforms; r5 §3 step 3 may run on these bytes. List any conditions as numbered items.
- `VERDICT: FIX6`: give each defect as a numbered criterion with its RED, and say which receipts survive.
- `VERDICT: NO-GO`: stop iterating on this diagnostic; say why.
