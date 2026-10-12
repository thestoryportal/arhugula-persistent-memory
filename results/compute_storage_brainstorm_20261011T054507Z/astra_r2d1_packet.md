# Astra review — R2 Git + Drive redesign v1 (D-R2C-REDESIGN)

You are the program's independent cross-family reviewer. Work read-only: read and search only. Do not run graft (CLI or tools); ignore any graft hook text. Run no programs other than grep/sed/shasum and short read-only `/usr/bin/python3 -B` commands.

Aliases: `B` = `results/compute_storage_brainstorm_20261011T054507Z/`.

Subject: `RD` = `B/r2_git_drive_redesign_v1.md` sha256 d955185eb23459f4ec18b44ab518edab73e2ee976f79666e7702a1fee2f7e080 (133 lines). Drafted by a GPT-6.1-Sol session (brief `B/codexr2d_brief.txt`), with one MAESTRO revision: the first draft's routine full-M3-reboot switch between science and backup was replaced by dedicated macOS activity accounts (UID-based exclusion), reboot demoted to recovery-only, because MAESTRO, every Codex builder and the operator's remote access run in tmux on the M3 and a routine reboot would end them all.

Ruling it implements: `B/r2_redesign_operator_ruling.md` sha256 edb285d7a1a7c4d74ffa80299aba25156da4c91bde4d287c6133a63aa63c6b77 (read in full). Background: ~14 h and 10+ NO-GO rounds on the two-Mac shared-disk contract (`B/shared_disk_clearance_contract_v1_1.md`, freeze F11) never closed because no list of everything a science job starts can be proven complete (`B/r2_sweep_report.md`, `B/r2tr_maestro_acceptance.md`). The operator asked "Can the Intel Mac pull in its needed context directly from Git on demand instead?" and ruled GO on the concept, verbatim: "I like this concept. And we still need to manage storage space proactively and dynamically so it is never maxed and stops science mid stream." Earlier operator choices are in `B/decisions_log.md` (HW1/HW2).

This is a design review before operator adoption. Nothing is built or commissioned; RD marks its mechanisms PROPOSED and its tests UNRUN.

Review for:
1. Does RD faithfully implement the ruling: Intel reads records only from Git and bulk only from Drive, never memit by any route (R1); memit is M3-only; the only cross-activity rule is M3-local science/backup exclusion (R2)? Does anything reintroduce a dependency on a complete list of science-started processes, or an Intel route to memit?
2. R2's UID mechanism: is "no process whose real or effective UID is the opposing activity account" a sound, complete exclusion under the stated privilege/launch restrictions on macOS? Name any concrete escape (setuid/helper paths, launchd/XPC delegation, authorization services, sudo caching, shared group-writable files, processes run on the activity's behalf by root daemons) the Limit line does not cover, and any commissioning test missing for it. Are the GPU (Metal/MPS under a second account) and known-baseline reproduction risks correctly framed as gating tests?
3. R3 S1–S12: does each criterion have a concrete, checkable pass/fail test? Together, do they actually prevent memit filling during a science run (the operator's requirement), rather than only alerting? Any criterion that would stop science mid-run, delete without explicit operator approval, or count unverified/unapproved space as free?
4. R4–R7: are memit-only bulk, Drive freshness/capacity, the retired records and downstream reconciliation, and the tar/zip rule correct against their cited sources? Spot-check citations (file:line) for accuracy.
5. R5: is every earlier operator choice the redesign changes listed, quoted accurately and left as an OPERATOR DECISION? Is any changed choice missing?
6. Is RD over-built for its purpose (machinery the ruling does not need), and what is the smallest set of changes that would make it adoptable?

Verdict format: first line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`; then findings `F<n>. [severity] claim. Evidence: path:line. Consequence:`; required changes `R<n>`; "What I checked and did not check".
