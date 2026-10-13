VERDICT: NO-GO

1. none found — `tools/new1_construction_diag.py:33–34,95–105,141–153,177–182`: fixed construction order, one native SVD, shared U/s/mask/indices, before/after fingerprints, and production-path release of C/Vh.

2. none found — `tools/new1_construction_diag.py:114–137` calls the unchanged gate, then independently records counts, both SHAs and all four residuals. Checked against `tools/new1_geometry.py:230–240`; thresholds and short-circuit behavior remain unchanged.

3. **Blocking: deadline interruption during worker creation can leave computation running after abort.** At `tools/new1_identity_diag.py:256–257`, `process` receives its handle only after `Popen` returns. If SIGALRM raises after child creation but before assignment, cleanup sees `process is None` and returns (`:227–235`). A worker that already passed its immediate-parent check proceeds into measurement without another parent-liveness check (`tools/new1_construction_diag.py:223–227`).

   **Reproduced:** wrapped a real stdlib-only `Popen` to delay returning its handle by 0.2 seconds, under the actual 0.05-second watchdog. Supervisor returned **2 / STOPPED-DEADLINE**, while the child remained alive. Output was in memory; I killed/reaped the fixture afterward. No diagnostic data or arithmetic was run.

   **Exact fix:** make child creation and handle registration cancellation-safe: defer watchdog/interrupt exceptions until ownership is registered, immediately process pending cancellation and kill/reap, and prevent worker computation until the parent explicitly releases it after registration and deadline/resource checks. Bound the launch operation independently so deferral cannot defeat 600 seconds. Add this interrupted-launch regression. Because supervision is frozen by hash, review and re-pin the necessary scope/source changes before launch.

   Otherwise inspected: fresh admission before dispatch, CPU/thread/nice checks, RSS equality rejection, single dispatch and no retry.

4. none found — `tools/new1_construction_diag.py:195–200`; `tools/new1_identity_diag.py:193–215,278–299`: exclusive namespace/files, strict combined byte cap, scalar persistence, result-SHA terminal receipt, and late-failure invalidation. A result alone remains uncommitted.

5. none found — `tools/new1_construction_diag.py:43–54,80–92,168–183`; `tools/new1_geometry.py:50–57`: three pinned measurement inputs, before/after consumption verification, CPU `weights_only=True, mmap=True`, and extraction limited to projector metadata/probes. No adapter/update computation.

6. none found — `tools/new1_construction_diag.py:125–155,183–192`: observational rows and diagnostic `MEASURED`; no scientific verdict, classification or repair recommendation is generated.

7. none found — `tools/new1_construction_diag.py:203–212,53`: starting nice 10 produces increment 0; starting above 10 refuses; final nice must equal 10. The saved `launch_command.txt:1–2` matches.

Graft: savings unavailable; one failed call.

