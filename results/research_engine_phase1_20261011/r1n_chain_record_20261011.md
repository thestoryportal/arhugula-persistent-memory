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

## C (16:49:07–16:49:09Z)
`RE/r1n_chain_driver_maestro51.py bind` (A.load_maker(sizing=False); M bind args as R1L; `--probe RE/intel_identity_probe_r1h_20261011T131105Z.json`; `--bootstrap-start-utc 2026-10-11T16:49:07Z`). rc 0, stderr empty, final qualified, m3_deadline 1791738217.0 (= start + 870 s, 17:03:37Z). Capture sha256 73e5fb3a…; committed e8d46659.
```
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  r1j_bind_r1n_20261011T164907Z.exit
59e76d46969ce4deac245576896f3259c5cf2a400e8197fd1a350c0a635d9d37  r1j_bind_r1n_20261011T164907Z.final
59e76d46969ce4deac245576896f3259c5cf2a400e8197fd1a350c0a635d9d37  r1j_bind_r1n_20261011T164907Z.final.pending
73e5fb3ae1962eb2ac762a6743bbc4a912f655b1d88ded78ef20b36155d908bb  r1j_bind_r1n_20261011T164907Z.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  r1j_bind_r1n_20261011T164907Z.stderr
```

## Gate D (16:49:16Z): GATE D GO
Checker `RE/r1n_chain_driver_maestro51.py gate` (committed 49c71b14 before C; dry-run on the consumed R1J bind failed D6/D8 as required). Output verbatim:
```
D1 PASS mismatches=[] N.capture_sha256=3506fe32f9b3 committed=3506fe32f9b3
D2 PASS age=235s final={'exit': 0, 'm3_deadline': 1791737971.6292312, 'm3_qualified_at': 1791737122.036215, 'qualified': True}
D3 PASS ['.exit', '.final', '.final.pending', '.json', '.stderr'] 7188 B
D4 PASS new_since_B={'/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/research_engine_phase1_20261011/r1n_evaluate_20261011T164501Z.exit': 2, '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/research_engine_phase1_20261011/r1n_evaluate_20261011T164501Z.out': 4246, '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/research_engine_phase1_20261011/r1n_evaluate_20261011T164501Z.stderr': 0} resized={} bind_set=113619 B old_state_now=7386341 D(B)=4009702
D5 PASS receipts=37732722 setup=1949513676
D6 PASS core=a32411006dc3 roots=['absent', '/private/tmp/r1l-intel-provisioning-v11', 'absent', '/private/tmp/r1l-intel-window-registration-v11'] seals=True differ=['binding_provenance', 'collector', 'window_seal'] attempt_absent=True
D7 PASS live=2175092 calls=223284
D8 PASS left=860s deadline=1791738217.0
GATE D GO
```
MAESTRO judgment (non-numerical): writer control holds — no scheduled/MacPorts writers (16:43Z survey), the only possible writer is the operator at the Intel console, old r1h-v7 state byte-identical at D; row drift since A (~4 min) is unobserved and is covered by the fixed D(B) 4,009,702 allowance, of which 4,248 bytes are used by B's own output; no evidence update; 860 s left for E, preservation and commits (declared minimum 420 s).

## E (16:49:36–16:50:08Z): inventory attempt 0, rc 0
`RE/r1n_chain_driver_maestro51.py inventory` (A.load_maker(sizing=False); M inventory args; committed bind capture sha256 73e5fb3a…; bootstrap bytes 113,521; anchor `none` for the fresh core a32411006dc3…). Exit 0, stderr empty, final qualified at 1791737408.53 (16:50:08Z) vs deadline 1791738217.0 (808 s spare). Successor anchor `12:45de480739fc3c33c6f1938a154b45a732122f93f5caff379d8c1feae23756fe`. Capture 2,008,557 bytes (<= 2,500,000 dispatch bound): 222,890 R1I-LIVE lines, 14 R1H-ANCHOR lines; summary `mode inventory, status OBSERVATION-ONLY, established [], retained_dir /private/tmp/r1l-intel-provisioning-v11`, elapsed 66.5 s (Intel clock). Committed 7ccf0778.
```
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  r1j_inventory_0_a32411006dc3.exit
52f41be9b1c9594dcd5ae2998995b52f80c63089db2fd463dac3a1e58b7d2f4d  r1j_inventory_0_a32411006dc3.final
52f41be9b1c9594dcd5ae2998995b52f80c63089db2fd463dac3a1e58b7d2f4d  r1j_inventory_0_a32411006dc3.final.pending
f2d9794e6247247069ab9feb197b76853b73854ac1fd5745a18f5a36db21e5c3  r1j_inventory_0_a32411006dc3.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  r1j_inventory_0_a32411006dc3.stderr
a353cd0de1cde1b48a6189d6029ca8b257d3c03e8aea68a8b599a1d49264f83f  r1j_attempt_0_a32411006dc3.json
```
Intel state after E (16:50Z, read-only): retained dir 20,540 KiB — `window.json` 16,927; `receipts/` inventory jsonl 20,049,966 (vs measured rows 20,114,046), accounting 183, summary 466, padded failure slot 16,384; registration `window.jsonl` 20,000. Anchor 0:a49c11de… untouched; old r1h-v7 state not modified.

## Result
The one authorized A–E chain completed: A rc 0, B PASS, C rc 0, Gate D GO (8/8), E rc 0. The authorization is now used. The inventory is an observation record only (no acquisition, no install); what it permits next is a separate decision.
