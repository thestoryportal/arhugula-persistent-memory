# R1M chain A–E: stopped at phase B (evaluator FAIL), 2026-10-11T15:51Z

Authorization: `RE/operator_authorization_r1m_20261011T1547Z.md` (one A–E chain; any stop ends it). Checklist: `RE/r1m_gate_d_checklist.md`.

- Before A: Intel read-only survey at 15:48:31Z found no crontab, no Launch Agents/Daemons, no MacPorts, rsync, rclone or python jobs; fresh v10 roots absent; old v7 roots present. The only other possible writer was the operator at the Intel console.
- A (15:49:40–15:50:06Z): `RE/r1m_sizing_dispatch.py` (04b66350) dispatched Q once. rc 0, qualified final, empty stderr. Capture `RE/r1j_probe_r1m_20261011T154940Z.json`, sha256 1c330b25b5a3921b197a8d60fc12aca0d33183e0e4b9d52f0741aa382755a9ed (544f8498).
- B (15:51:17Z): `/usr/bin/python3 -B RE/r1m_evaluate.py <capture> RE/intel_provisioning_manifest_v10.json` printed verdict FAIL, exit 1. Output `RE/r1m_evaluate_20261011T154940Z.out`, exit file `.exit`.
- C, D and E did not run. No bind, no Intel state was created, and no anchor was consumed. The authorization is spent.

## What the measurement says (from the evaluator output and the capture)
- Required receipt bytes 34,712,537 against the sealed 18,000,000 allowance (receipt_pass false). Required setup bytes 2,016,477,107 against the 2,000,000,000 cap (setup_pass false). LIVE dispatch passes (2,175,092 ≤ 2,500,000).
- The largest term is inventory rows: 20,114,046 bytes for 61,743 rows. Nearly all of them are under `/opt/local`: 25,639 directories, 36,089 files and 11 symlinks; the files hold 192,852,353 bytes in 37,607 hash chunks. The other admitted roots do not exist yet.
- Old Intel state is 7,386,341 bytes (r1h-v7 provisioning 7,367,301 plus registration 19,040). Existing M3 receipts are 851,702 bytes.
- Even without the old state, the rows plus the fixed terms (about 27.3 MB) exceed 18 MB.

## Consequence
Under the reviewed rule, 18 MB cannot hold this inventory. The constants may not be changed after measurement (E; Astra r12 R1). A rerun needs a re-planned budget or scope (for example the sealed receipt allowance and setup cap, or how `/opt/local` is recorded), reviewed by Astra and authorized again by the operator.
