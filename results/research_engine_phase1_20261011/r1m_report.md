# R1M: local sizing build for Astra R11 R1–R3

Aliases: RE=results/research_engine_phase1_20261011; C=r1j_collector.py; S=r1j_stub.py; B=r1j_bind_manifest.py; W=r1j_host_commands.sh; M=r1l_make_bundle.py; J=intel_provisioning_manifest_v10.json; D=r1l_report.md; Q=r1m_size_probe.py; E=r1m_evaluate.py; T=test_r1m_sizing.py. All aliases below are under RE.
Status: local build/tests ready for Astra; Intel sizing, old-state sizes, host execution and inventory authorization remain UNVERIFIED (RE/astra_r1p11_verdict.md:22-27; /private/tmp/r1m_green_acceptance.log:33-35).

## R1: read-only measurement
Q walks exactly J's five admitted roots, plus the two explicitly separate old-state scopes; every directory ancestor/child uses O_NOFOLLOW descriptors, and symlink roots produce refused observations (J:1620-1626; Q:19-24,43-57,95-172,173-180).
No collector constructor, subprocess, temp file, cache or state-root creation occurs in Q. Regular files are opened read-only to check access and identity, without reading contents; their hash is a fixed 64-character placeholder (Q:27-33,113-127,251-278).
Each row uses unchanged C.encoded(), never an average or a copied JSON encoder; SHA-256 replacement preserves serialized width. Metadata matches C's row fields; the summary records per-kind counts, encoded path/target byte sums, regular size totals, metadata minima/maxima, and per-root totals (C:42-43,882-915; Q:59-91,95-142,220-249).
Hash chunks are ceil(size/J.io_chunk_bytes) for readable baseline regular files; collector-origin files have no inventory hash. This bounds the nonempty reads for a stable tree (C:874-880,895-899; Q:113-127; J:1640).
The JSON summary is at most 131,072 bytes; overflow refuses before stdout. Old-state lists are complete or refuse above 128 files; no truncation becomes PASS (Q:15-16,36-40,182-217).
Two complete metadata passes must agree, including per-root row count, newest mtime/ctime and an order-independent 256-bit sum of entry fingerprints. This witnesses metadata stability, not file-content identity or later stability (Q:68-91,220-225).

## R2: budget treatment and fixed evaluator rule
C starts a fresh registry and charges bootstrap + M3 + registry + emergency reservation + registered current receipts + writing bytes. It does NOT discover/charge the old Intel roots. M's globs charge M3 files only (C:357-366,765-776; M:163-173; J:1620-1626,1728).
J nevertheless says receipts cover “All inventories, stdout/stderr and evidence.” This build charges ALL measured old Intel regular-file bytes inside the same 18,000,000 allowance, with no exclusion or use of retained_failure_extra to hide evidence (J:1456-1467; E:57-73).
Q lists old r1h-v7 files with logical sizes and mtimes and sums them; unreadable, symlink, special or incomplete old state refuses. Missing roots remain explicit vanished witnesses, never an invented measured failure size (Q:19-20,182-217; RE/intel_provisioning_manifest_v9.json:1620-1626,1728).
D:23's 849,937 bytes describes named M3 evidence only. Its 12,150,063 remainder does not include old Intel evidence, new collector overhead or drift; it is not the required inventory allowance (D:23; RE/astra_r1p11_verdict.md:7; E:68-93).
Constants below were fixed before fixture measurement and before any Intel probe; there are no CLI margin overrides (E:12-23,106-111; /private/tmp/r1m_red.log:107-109).

| Required receipt term | Bytes / rule | Source |
|---|---:|---|
| Old Intel evidence O | complete measured file-size sum | Q:182-217; E:57-59 |
| Inventory I | exact measured serialized rows + 65,536 for fresh collector rows | Q:21-22,241-243 |
| Existing M3 L | current union of J's receipt globs, including pending/failed files | E:95-103; J:1526-1539 |
| Fresh bind + inventory dispatch | 2,500,000 each | E:68-71 |
| Registration + window + summary | 65,536 each | E:18-20 |
| Failure + emergency journal | 16,384 + 4,096 | E:19 |
| Accounting + attempt | 4,096 each | E:20-21 |
| Sizing capture, framing, exit, pending/final | 131,072 + 4,096 | E:21; S:56,89-90 |
| Receipt drift | 1,000,000 | E:15,71 |

R = O + I + L + 6,360,448. PASS requires R <= 18,000,000 and 1,981,764,570 + R <= 2,000,000,000. The latter is all J components except receipts plus this cumulative receipt demand; old state is counted once, within receipts (E:68-93; J:1463-1471).
LIVE calls <= 2N + V + H + 3*64 + 256: N=measured rows, V=actual descent remaining calls, H=nonempty hash chunks; 64 bounds new collector entries and 256 covers fixed lifecycle calls. LIVE dispatch bytes = 9*calls + 65,536 non-progress/framing/anchors/summary + 100,000 drift, separately <= 2,500,000 (E:22-23,74-93; C:550-575,592-607,745-755,918-944; S:69-77).
PASS also requires exact J/C/Q pins, matching roots and integer totals, stable two-pass evidence, sealed cap/component equality and a measurement no older than 3,600 seconds, not future-dated. Malformed/overbound input prints FAIL, exit 1; qualified PASS prints every term, exit 0 (E:26-66,79-93,106-134).
These are fixed conservative envelopes for ONE fresh inventory, without an evidence update. They are not host measurements. D gate below must hold the baseline and old evidence quiescent; unknown drift is a STOP, not an assumption that a numerical reserve prevents tree changes (Q:21-22,220-249; E:15-23; C:1265-1269).

## R3: qualification and prospective gated procedure
D:13's 3N+H equations assume every attempted row has an ordinary descent remaining() call. Refused symlink roots and extra directory-error rows have no such call; with all rows counted as N, the traversal term is 2N+V+H. The historical offsets cannot restore V=N without evidence (D:13; C:918-944; RE/astra_r1p11_verdict.md:13).
The smallest faithful dispatch is M's existing probe transport with Q substituted ONLY for the verified identity member in memory. S verifies every member before compile, then probe mode calls interpreter_identity() and returns before collector construction. A normal M probe alone runs the old identity probe; W is not edited (M:21-29,310-318; S:37-49,79-91; W:13-28; T:227-247).
Sizing needs its own bounded pre-bind transport window (M probe: now + 870 seconds), no collector anchor and no Intel state. Its committed capture/hash is sizing evidence, not interpreter identity or bind authority (M:299-311; J:1513; S:88-91; Q:251-270).

A. After Astra review and separate operator authorization, MAESTRO commits the reviewed build/pins, reserves baseline/old-root writers, then dispatches the sizing probe ONCE via the in-memory M adapter below. Preserve complete capture, stderr, exit, pending/final and exact capture hash; commit survivors on every outcome. Nonzero/unknown/no qualified final stops here (M:314-375; E:26-40).
Prospective adapter skeleton; not run here. The supplied PREFIX must be a new RE/r1j_probe_r1m_<stamp>, and SSH_ARGS must be W's exact identity-pinned argv (M:299-311; W:11,28):
```python
# Load M by importlib.util from its committed path; verify working bytes match pins.
original_build = maker.build
def sizing_build(args):
    if args.mode != 'probe':
        raise ValueError('sizing adapter is probe-only')
    members = original_build(args)
    members['identity'] = (maker.HERE / 'r1m_size_probe.py').read_bytes()
    return members
maker.build = sizing_build
sys.argv = ['r1l_make_bundle.py', 'probe', '--dispatch-m3',
            '--capture-prefix', PREFIX, '--ssh-argv', *SSH_ARGS]
raise SystemExit(maker.main())
```
B. Locally run `/usr/bin/python3 -B RE/r1m_evaluate.py CAPTURE.json RE/intel_provisioning_manifest_v10.json`; preserve exit, output and hashes and commit them. FAIL stops before bind/inventory. Any changed sealed allowance returns to Astra; never tune this evaluator after measurement (E:106-134; RE/astra_r1p11_verdict.md:22-27).
C. Only PASS continues to a fresh v10 bind through unmodified M, using D's existing direct identity probe (not the sizing JSON). Commit capture/exit/pending/final and hash before consuming it; the binder remeasures identity with cutoff tracing (D:26-44; B:16-32,46-63; M:138-160,281-289).
D. MAESTRO separately checks committed qualified sizing/evaluation/bind, exact reviewed pins, unused fresh core/anchor, remaining original 870-second deadline including commits, and fresh retained/registration roots. Verify the bound start/window/registration/summary fit the listed envelopes and future collector rows/entries stay within 65,536/64; no evidence update. Hold external baseline and old-state writers through E; if drift cannot be bounded within 1,000,000 receipt bytes AND 100,000 LIVE bytes, or evidence expires, STOP. Astra/operator inventory GO is still required (E:15-23,48-66,118-122; C:374-431,1131-1137; M:281-318; RE/astra_r1p11_verdict.md:25-27).
E. Only D GO dispatches inventory through M with this fresh committed capture/hash/bootstrap and anchor `none` for the fresh core. Preserve/commit attempt and all outcomes before the bind deadline. Never reuse 0:a49c11de49ce…, retry a consumed anchor or delete old state (M:272-318,342-375; D:22-24).

## Local evidence and scope
RED: initial 8 tests failed on absent implementation; framing regression then failed on absent parse_capture; bad probe-pin and refused-root target-length tests failed before their guards/measurement were added (/private/tmp/r1m_red.log:107-109; /private/tmp/r1m_red2.log:31-42; /private/tmp/r1m_red_pin.log:4-13; /private/tmp/r1m_red_target.log:14-24).
GREEN acceptance: `/usr/bin/python3 -B -m unittest discover -s results/research_engine_phase1_20261011 -p 'test_r1m_sizing.py'` passes 10/10; unchanged `test_r1l_collector.py` passes 64/64 (/private/tmp/r1m_green_acceptance.log:33-35; /private/tmp/r1m_carried.log:611-613).
Same-tree collector fixture: probe bound 69,115 >= actual 3,740 bytes, with baseline-only inequality also asserted; regular, directory, symlink, refused symlink root, unreadable directory, FIFO, socket and device kinds covered. Socket/device metadata is synthetic, as in the predecessor harness; no socket service was required (T:51-108; /private/tmp/r1m_green_acceptance.log:12).
Probe snapshots preserve file list, sizes and mtimes; old-state fixture totals 12,579 bytes. Small CLI prints PASS at 6,426,593 required receipt bytes; real 13,000-file escaped-path fixture prints FAIL with 21,897,213 inventory-row bytes. LIVE control measures 210 <= 637 calls, including an extra traversal-error row (T:110-165,249-280; /private/tmp/r1m_green_acceptance.log:13-14,36).
Pinned-stub fixture exits 0, emits 3,471 bytes and leaves its Intel fixture unchanged; all 11 existing subject hashes remain unchanged. Only Q/E/T/this report were added; raw logs and pins are under /private/tmp, not host acceptance (T:227-247; /private/tmp/r1m_green_acceptance.log:16; /private/tmp/r1m_scope_final.log:1-3).
Limits: metadata fingerprints do not prove content hashes; sizing may refuse oversized old-state lists, unstable trees or symlink ancestors. Fixed future-state/overhead envelopes and host quiescence remain MAESTRO gate obligations. The Intel tree has not been measured; no assertion that 18 MB fits is made (Q:43-57,182-225; E:15-23; RE/astra_r1p11_verdict.md:5-7).
