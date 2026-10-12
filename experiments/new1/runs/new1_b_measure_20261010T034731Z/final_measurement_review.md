# D-NEW1-b completed L4 measurement and DRAFT review

**FIX-FIRST — two documentation corrections before appending the DRAFT. No scientific-result blocker found; B correctly remains BLOCKED.** Next: correct the reproducible-command claim and table rendering, preserving the original artifacts.

Reviewer: Codex, GPT-6 / GPT family secondary reviewer under Claude-led MAESTRO2, not Astra. Reviewed the full completed receipt, derived summary, complete draft and governing Astra Option-B text. No numerical computation, SVD, test, source edit, prereg edit or relaunch was performed. File hashes were checked read-only.

## Required corrections

1. `command.txt:1` literally contains backslashes in `LLMDB_ROOT=\"$PWD\"`. Executed as written, the escaped quotes become part of the environment value; that is incompatible with the successful root assertion at `profile_l4.py:93`. Therefore `draft_report_section.md:24` must not call this the exact successful command. Preserve the existing command artifact and record a corrected reproduction command with `LLMDB_ROOT="$PWD"` (ordinary shell quotes, no backslashes). Unless the original invocation can be recovered verbatim, replace the final sentences of draft line 24 with:

   > The launch receipt records the effective LLMDB_ROOT as this worktree. The original command.txt contains a quoting transcription error; a corrected reconstructed reproduction command is recorded separately. This command reconstruction was not rerun.

2. The unescaped `||` norm bars at `draft_report_section.md:44–48` split the Markdown table into extra columns. Escape the bars or use plain labels such as `Frobenius(C−C.T) / Frobenius(C)` and `Frobenius(U.T U−I) / sqrt(d)`. Preserve every numeric value and threshold.

## Confirmed interpretation and evidence

- `receipt.jsonl:15–16` records measurement completion and child exit 0; the expected native/double/check phases appear once, without failure/timeout. Native 76.273775500 s, double 159.296147042 s, checks 21.215224875 s, total parent 258.023897875 s, and child/parent high-water 8,650,915,840 bytes agree with `summary.json` and the draft. High-water is cumulative, not sampled or an independent per-phase allocation.
- All five reported errors match `receipt.jsonl:14–15`: symmetry 0; SVD 1.373273220410387e-13; PSD 2.733106641216668e-10; U orthogonality 1.2074819482068658e-14; V orthogonality 1.2257894759352233e-14. V remains an extra diagnostic, not a fifth frozen gate.
- The required equal-cutoff-count condition fails: 8645/2363 native versus 8644/2364 double, with sorted zero-based index 2363 changing classification (`receipt.jsonl:6`, `:15`). Draft lines 59–63 correctly distinguish sorted-index comparison from eigenvector tracking and retain B as BLOCKED. No projector-norm failure was measured; certification remains UNVERIFIED.
- The two proposed amendment paragraphs at draft lines 69 and 71 faithfully reproduce Astra Option B. The subsequent energy-operator bound distinguishes exact stored-basis products from the rounded native P and does not promote an uncertified Frobenius/power-iteration estimate.
- Planning arithmetic is consistent: 5 x 256.785147417 s = 1283.925737087 s; 1.5 times that plus 600 s rounds upward in 300-second units to 2700 s. A 1.25 factor on 8.056793213 GiB rounds upward to 11 GiB, and the proposed 8-GiB floor plus 11-GiB reserve gives 19 GiB available. Draft lines 102–110 appropriately label these margins, omitted work, other layers, nice-10 timing and complete-workload feasibility as assumptions/UNVERIFIED. None is an adopted cap or a remedy for the measured count FAIL.
- Live source/test/prereg/options/diagnostic hashes match `baseline.json`; receipt, harness and summary hashes match the draft table. The report's first 82,639 bytes retain the recorded prefix hash. I did not independently rehash every file in both historical halted attempts; keep the separate scope audit supporting that broader preservation claim.

After the two documentary fixes, **GO to append the reviewed blocked DRAFT**, without implementation, prereg amendment or another run. The original os.nice refusal, failed admission probe, current no-nice scheduling limitation, halted INVALID attempts and real-study gates remain distinct. L4 float64 numerical validity is not acceptance of Option B, calibration, queue utility or F1 readiness.
