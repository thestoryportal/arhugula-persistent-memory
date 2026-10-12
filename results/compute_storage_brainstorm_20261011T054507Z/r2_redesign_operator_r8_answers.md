# R2 redesign — operator answers to R8 (recorded by MAESTRO62, 2026-10-11 ~23:40Z)

Asked via AskUserQuestion after Astra r2d1 GO-WITH-CONDITIONS (`astra_r2d1_verdict.md`, a0f6cf9b) and v2 (`r2_git_drive_redesign_v2.md`, sha256 61e901d2…). Answers verbatim.

## Round 1 (the four R8 questions of v2)

1. "Should the Intel Mac get its research files only from Git and Google Drive, and never touch the memit drive? If the newest big file isn't on Drive yet, it waits." → **"Yes (Recommended)"**
2. "Should the M3 upload its own files to Drive (the first upload and later ones) in the gaps between science jobs, replacing the plan where the Intel Mac did the first upload?" → **"The whole point of the Intel is to offload work like uploading. So it kind of defeats the purpose. Is there any way that the Intel can handle these types of actions?"**
3. "Should science run under its own Mac user account and backups under a second one, so the M3 can be sure science has fully stopped before a backup starts? …" → **"No"**
4. "Should the M3 keep its target free space even at a job's planned busiest moment, and hold the queue for an approved storage plan when jobs would use too much?" → **"Yes (Recommended)"**

## Round 2 (MAESTRO62 follow-ups to answers 2 and 3)

Context given: the earlier approved plan already sets aside Intel space for an upload checkpoint (512 GB SSD; amendment 21 "Store duplicates once", `decisions_log.md:234–238`); only the direction of the copy changes.

5. "For uploads: the M3 sends new files to the Intel over the cable, a quick copy that runs between science jobs. The Intel then does the slow upload to Google Drive and checks it on its own, while the M3 goes back to science. The Intel still never reads the memit drive. Use this?" → **"Yes (Recommended)"**
6. "Instead of separate Mac accounts, the copy to the Intel would wait until the existing job gate shows no science job running, and it would pause if one starts. It can't prove nothing left over is still running, but the copy is short, and a clash would only slow things down or force a redo, which the file checks catch. Use this?" → **"Yes (Recommended)"**

## Ruling as recorded

- Adopted direction: Intel's research sources are Git and Drive only; Intel never reads memit (1).
- Upload path: **M3-initiated push** of memit-only files to the Intel over the cable, between science jobs; the **Intel** performs the Drive upload, retries and verification from its own disk (5). Replaces v2's "M3 uploads directly to Drive" (2).
- No dedicated science/backup activity accounts (3). Overlap rule: the M3-side push waits for the existing job gate (`tools/c10w_p2_gate.py:73` `check_gpu`) to show no science job and pauses if one starts; observe-and-stop, not prove-in-advance; hash verification catches a disturbed copy (6).
- Proactive storage criteria stay (4), including peak-time free space and holding the queue for an approved storage plan.
- Astra r2d1's R1 (HW1 choice 7 restore points), R4 (frozen workload envelope) and R5 (adoption ≠ activation) carry forward. R2/R3 (UID quiescence, cross-account confinement) attach to the activity-account mechanism the operator declined; v3 must state their disposition.
- Next: a fresh Sol drafter writes v3 from v2 plus these answers; Astra reviews v3 (material change); then the operator adopts. Nothing is built or commissioned without a separate operator go.
