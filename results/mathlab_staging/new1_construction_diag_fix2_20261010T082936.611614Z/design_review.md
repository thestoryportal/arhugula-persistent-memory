Read-only GPT-family helper review; not binding Astra.

Use the guardian design, with these invariants:

- The supervisor raw-forks the guardian; the guardian raw-forks the worker. Block SIGINT/SIGALRM only across each fork and immediate PID assignment. Neither process calls a worker Popen constructor, so constructor stalls disappear from the ownership path.
- The guardian owns waitpid(worker). It kills the separate worker group on cancellation, parent death or the reserved work deadline, confirms reaping, sends a bounded reaping receipt, then exits. The supervisor validates that receipt and confirms waitpid(guardian) before terminal recording or return. Killing the guardian early would strand an unreapable grandchild.
- Before worker process-group setup is acknowledged, cancellation kills its known PID directly. After acknowledgement, kill its PGID. Reset inherited guardian signal handlers and masks; repeated SIGINT/SIGALRM must set pending flags rather than unwind teardown.
- Close every inherited duplicate of the supervisor's liveness writer. Also check the guardian's immediate parent PID, so a retained writer cannot defeat parent-death detection.
- Derive launch, work, cleanup and recording limits from one absolute deadline. Reserve teardown and recording inside it. Existing S.terminate() grants a fresh five seconds and needs replacement on this path. Set completion only after successful matching waitpid, never when cleanup starts.
- Register the kernel-reported worker PID, receive a worker nonce through private IPC, check RSS, then generate the supervisor secret. Bind the release frame to that secret, nonce, PID and deadline. The worker needs independently supplied expected authentication material; a secret appearing only in the release frame proves nothing. Read bounded bytes through EOF and reject duplicates, trailing bytes, missing EOF and guessed RUN.
- Preserve the actual numerical worker_pid; family_rss(root_pid, worker_pid) already includes the guardian and worker descendants. Drain stdout/stderr with bounded memory and deadline-aware reads; retain the existing two output files.

There is a concrete scope conflict: tests/test_new1_identity_diag.py:253 requires exactly one patched S.terminate call, a STOPPED-DEADLINE cleanup error, and captured Popen pipe handles. A pure fork redesign cannot preserve these implementation-specific fixtures. Seek narrow authorization to migrate that fixture while preserving and strengthening its behavioral checks; avoid a synthetic compatibility path.

The proposed design addresses the four reproduced schedules. Absolute guarantees against unscheduled processes or indefinitely blocked kernel IO remain unproven. This was a read-only helper review: no files changed, tests or runtime launched, or binding Astra verdict supplied.
