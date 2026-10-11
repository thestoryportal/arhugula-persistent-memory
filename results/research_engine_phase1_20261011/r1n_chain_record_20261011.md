# R1N v11 chain A–E: MAESTRO51 run record (one attempt)

Authorization `RE/operator_authorization_r1n_20261011T1637Z.md` (d5caf96e). Rules: GD11 `RE/r1n_gate_d_checklist.md` + addendum `RE/r1n_gate_d_addendum_r13.md`. Any stop ends the chain.

## Before A (16:41–16:47Z)
1. R1 identities (16:42Z): `sha256` of G, J11, N, A, GD11, TN, RN all equal the addendum's full hashes; M, J, Q, E, C, B, S, P equal A's/the R1M dispatcher's full pins; W a4b52fc2…, T 6b7060ae…, TM 0343190a… equal the round-13 prefixes. 18/18 match.
2. Intel read-only survey (16:43:02Z, ssh as robertrhu_node2): no crontab; /Library/LaunchAgents and /Library/LaunchDaemons have no non-Apple items; one user agent `~/Library/LaunchAgents/org.deskflow.autostart.plist` (created 2026-10-11T07:52:40Z, before the R1M survey at 15:48Z; RunAtLoad `open -a /Applications/Deskflow.app`, keyboard/mouse sharing; not scheduled; writes none of the admitted or old roots) — judged not a writer. No port/rsync/rclone/python/cron process (only `deskflow-core`). Fresh v11 roots `/private/tmp/r1l-intel-provisioning-v11`, `/private/tmp/r1l-intel-window-registration-v11`, `/Users/robertrhu_node2/research-engine-phase1`, `/Applications/MacPorts`: all absent. `/opt/local` mtime 08:16Z (before CAP). Old roots: the four files equal CAP's `old_state` exactly (sizes 16,384 / 7,333,990 / 16,927 / 19,040; mtimes to the nanosecond), total 7,386,341; directories `receipts`, `downloads` only. Other possible writer: the operator, logged in at the Intel console (as at R1M).
3. Authorization committed (d5caf96e).

## Evidence census before A (R2)
N's automatic census (`local_accounting(J11, RE)`, no extras): matched 851,702 bytes (10 files: attempt 0, bind 143208Z set, inventory 0 set, halt diagnostic); omitted 8,296 bytes (CAP set 7,186 + EOUT `.out`/`.exit` 1,110) = the addendum's 8,296 at CAP. This equals A's own census (A.receipt_usage calls the same function without extras).
Nonstandard retained Intel captures outside N's filename census, passed to B as `--extra-receipt` (10 files, 2,187 bytes): `intel_identity_probe_20261011T113404Z.{json,stderr}`, `intel_identity_probe_r1e_20261011T115851Z.{json,stderr}`, `intel_identity_probe_r1f_20261011T124523Z.{exit,json,stderr}`, `intel_identity_probe_r1h_20261011T131105Z.{exit,json,stderr}`.
Not receipts (recorded, excluded): `r1l_logs_20261011/` (builder red/green test logs and SHA256SUMS, 354,199 bytes; local unittest output, no Intel exchange), manifests v2–v11, host command scripts, probe scripts, `intel_r1_sizes_20261011.tsv` and `preinstall_identity_20261011.tsv` (survey tables, not receipts). No receipt-like file exists outside RE (`git ls-files results` search for r1j_/r1m_evaluate_/r1n_evaluate_ names outside RE: none).

## A (16:45:01–16:45:22Z)
`/usr/bin/python3 -B RE/r1n_sizing_dispatch.py RE/r1j_probe_r1n_20261011T164501Z` once: rc 0, stdout `R1H-CAPTURE RE/r1j_probe_r1n_20261011T164501Z.json 3506fe32f9b301e92489a9fa300b1357efca54122ec37a36a77f546aaf0beefd`, stderr empty. Sizing set (5 paths; `.final` and `.final.pending` are hard links) = 2 + 104 + 104 + 6,978 + 0 = 7,188 bytes ≤ 135,168. sha256:
```
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  r1j_probe_r1n_20261011T164501Z.exit
cbce1b49cd47230d9691fbe206eabd3308e7152c8e87baf7b41fca230b2cebdd  r1j_probe_r1n_20261011T164501Z.final
cbce1b49cd47230d9691fbe206eabd3308e7152c8e87baf7b41fca230b2cebdd  r1j_probe_r1n_20261011T164501Z.final.pending
3506fe32f9b301e92489a9fa300b1357efca54122ec37a36a77f546aaf0beefd  r1j_probe_r1n_20261011T164501Z.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  r1j_probe_r1n_20261011T164501Z.stderr
```

## B (16:45:45Z)
`/usr/bin/python3 -B RE/r1n_evaluate.py RE/r1j_probe_r1n_20261011T164501Z.json RE/intel_provisioning_manifest_v11.json` + 10 `--extra-receipt` (the identity-probe files above); no `--replay-cap`. Exit 0, stderr empty, verdict **PASS**, replay_only false, capture_sha256 3506fe32… (= A). Output written to scratch then copied to `RE/r1n_evaluate_20261011T164501Z.{out,stderr,exit}` (so it could not count itself).
- Receipts: required 37,732,722 ≤ 42,000,000 (headroom 4,267,278). Setup: 1,949,513,676 ≤ 2,000,000,000. LIVE: 2,175,092 ≤ 2,500,000.
- Terms: rows 20,114,046 (61,743 rows, same as CAP); drift D(B_A) 4,009,702; old Intel state 7,386,341; measured M3 851,702; omitted M3 10,483 (= 8,296 at CAP + 2,187 extras); sizing envelope 135,168 (actual set 7,188).
- Side by side (R2): A's census (no extras; sizing set counted as plain evidence) = 851,702 + 8,296 + 7,188 = 867,186. N's charged evidence = 851,702 + 10,483 + 135,168 = 997,353. N's is larger and is the one charged; no double count (sizing set charged once, by envelope).
sha256:
```
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  r1n_evaluate_20261011T164501Z.exit
cab8eda522b050ab0dbba3c97c54b128dc6a96b665da202c2d56485ad95302f7  r1n_evaluate_20261011T164501Z.out
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  r1n_evaluate_20261011T164501Z.stderr
```
