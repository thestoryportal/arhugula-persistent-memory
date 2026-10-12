# MB42 host correction, round 1
Authority: MAESTRO's two host failures; original brief 2.1-2.3 and 3.1. No production/base/addendum/frozen-runner edit.

Confirmed root causes:
- Coverage redirected native /private/tmp fixtures into the /Volumes/memit receipt, hitting the unchanged destination guard before transfers.
- clean/excluded/symlink checks exit 0, but the DEBUG argv line contains --error and error.txt; generic anywhere-word matching misclassifies those as severity.
- Missing-config NOTICE is a competing explanation; a replay with the DEBUG startup line removed distinguishes it. Lock PID, archived history and timeouts are downstream of dispatch, so make no separate fix unless the fresh host run disproves this cause.

1. Placement: run the actual runner in its allowed sandbox check-green mode and inspect command.json HOME/fixture paths. RED must show receipt-volume placement; GREEN requires a fresh /private/tmp runtime root with isolated HOME and fixture paths there, while evidence stays in this receipt.
2. Host positive control: before host coverage/content fixture calls, save native filesystem/physical-store observations for source volume and fixture root, reject unknown/shared physical identity, and verify fixture containment. APFS volumes on the same physical store must fail even when logical devices differ. Sandbox proof remains synthetic; native diskutil is unavailable after a measured probe and actual host proof remains UNRUN.
3. Verifier: replay all three actual passing host reports/logs unchanged. They must PASS; same-size corruption still FAIL naming alpha.txt. A NOTICE-only replay must PASS; DEBUG argv/path data containing error words must PASS; true ERROR/CRITICAL/FATAL, failed-read text, report errors and unchecked hashes must still FAIL.
4. New local-check evidence directory is inside this receipt while content fixtures/HOME are inside the owned /private/tmp runtime root.
5. Fresh host dispatch labels for every one of nine actions, including preflights and pins; no earlier run or label overwritten. Full rerun preserves exact 22/22 host acceptance, frozen 155/14 skips and all existing exit/process/inventory gates.
6. Save behavioral RED before changes, then focused/full package/checker/non-native GREEN, update affected pins/plan/doc hashes and complete bulk/report manifests. Rehash protected inputs before and after. Native physical/22-case/local-rclone acceptance remains host UNRUN.

Before copies and host-evidence hashes are saved. Total receipt budget <200 MB. No remote rclone, native applet, launchctl, real HOME writes, process-policy weakening, retry/timeout changes or git mutation.

CONTEXT DIRECTIVE: start new work only at >=60% left; at <=40% or any compaction stop starting work, append done/half-done/in-flight exact paths, SHA-256s, test state and one next step to README, restate this directive and reply MB42 HANDOFF.
PYTHON QUIET: on HOLD PYTHON finish current command, then no Python/tests until RESUME PYTHON.
