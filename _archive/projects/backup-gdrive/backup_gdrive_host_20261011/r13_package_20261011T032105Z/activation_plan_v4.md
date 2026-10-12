# Drive r13 activation plan v4 — operator/MAESTRO execution only

This plan is UNEXECUTED. Seven production inputs are frozen: wrapper, status tool, excludes, applet source, builder, stage script and plist. The applet dispatches immutable commit bytes in a release directory outside all checkouts. Astra must review that change (r10 item 1) and this package, including the host evidence, before activation. Sandbox GREEN does not establish native, Drive, launchd or scientific acceptance.

r10 required order, verbatim:

> resolve scope/deployment build → complete coverage/re-review → publish new pins → refresh inventory and clear orphans → gated merge → stage/build/hash → preserve receipt → GO recovery → verify barrier → GO launch/Allow → completion and content verification → GO install/bootstrap/kickstart → fresh successor verification → GO retirement

Mapping: scope is §0.1; coverage/re-review §0.2; pins §0.3; inventory/orphans §0.4; merge §1.1; stage/build/hash §1.2–1.3; receipt §1.4; recovery/barrier §2; launch/Allow §3.1–3.3; completion/content §3.4–3.5; install/bootstrap/kickstart §4.1–4.3; successor §4.4; retirement §5. Every prior GO and STOP is retained below, with stronger content and process gates.

Declarations (no command launched). Set USER_UID from captured id output, PR from captured PR output, MERGED_SHA from the merge receipt, RELEASE_ID to a fresh approved identifier, and I to MAESTRO's isolated integration worktree. Set numeric generation variables from saved observations; never guess them. M is the main checkout, W this worktree, D the deployed release. Run each row separately in a host shell; inspect its receipt and pass rule before advancing. Never paste the whole document into a shell.

```shell
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
M=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory
R="$W/results/backup_gdrive_host_20261011/r13_package_20261011T032105Z"
VERIFIED_SHA_FILE="$R/operational_checks/r13_verified_commit_sha.txt"
D="$HOME/Library/Application Support/memit-gdrive-backup/releases/$RELEASE_ID"
APP="$HOME/Applications/MemitGdriveBackup.app"
SRC=/Volumes/memit/llm-database-poc-mirror/
DST=gdrive:memit-backup/llm-database-poc-mirror/
C="$R/commands/full-check"
CD="$R/commands/full-check-download"
capture() { /usr/bin/python3 -B "$R/capture.py" "$R" "$@"; }
```

`capture LABEL COMMAND ARGS...` exclusively creates `R/commands/LABEL/`, saves complete stdout.txt, stderr.txt, exit_code.txt and command.json, and returns the child's actual exit. No pipeline is used. Labels are never reused: repeated observations take fresh approved suffixes. R is in an excluded worktree, so these receipts do not change the included source population. READ-ONLY describes the underlying operation; capture's receipt writes are authorized by this plan. Markers: [RECEIPT-WRITE], [MAESTRO GO], [OPERATOR GO], [OPERATOR CLICK]. An expected nonzero status is interpreted only in its explicitly stated row; no silent fallback or ignored error.

## 0. Preconditions

0.1 [READ-ONLY]. Check pins_v4, the nine production/test inputs and the literal backup-only scope_allowlist.txt. STOP on any mismatch. Candidate and merged inputs must match the reviewed pins. Preserve both older pin sets; pins_v4.json links frozen K12 pins_v3.sha256 and pins_v3.json, which link pins_v2.sha256 and pins_v2.json without changing them. The current status-tool pin is `903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46`.

<!-- row 0.1 marker=READ-ONLY -->
```bash
capture pin-preflight /usr/bin/shasum -a 256 -c "$R/pins_v4.sha256"
capture executable-preflight /usr/bin/python3 -B "$R/check_plan.py" "$R/activation_plan_v4.md"
capture helper-executable-preflight /usr/bin/python3 -B -c 'import os,pathlib; paths=("/bin/sh","/usr/bin/dirname","/usr/bin/git","/usr/sbin/diskutil"); [print(p,pathlib.Path(p).is_file(),os.access(p,os.X_OK)) for p in paths]; assert all(pathlib.Path(p).is_file() and os.access(p,os.X_OK) for p in paths),"STOP: missing/non-executable helper program"'
capture uid /usr/bin/id -u
capture disk /bin/df -k / /Volumes/memit
```

Run from W so relative pin paths resolve. Package writes stay under 200 MB; activation logs/bundle are projected under 100 MB on the internal disk, with no bulk backup data there. Require free space ≥ projected writes + 20 GiB before a bulk-writing step; refresh disk evidence at launch. Initial upload size is provisional ~287,080,274,442 B (~40,412 files); collect the actual included inventory at the final checkpoint.

0.2 [MAESTRO GO]. Preserve the accepted r11 coverage unchanged, run host_commands_r13.sh's individual commands with fresh r13_* labels and submit the changed r12 inputs to Astra r12. The new verifier must re-run all four host local→local fixtures. Historical coverage below remains historical. All r12 reruns use this new receipt at niceness 0; the frozen r11 package is read-only (do not execute the activation plan). Exact 22-case coverage must give 22 pass, no skips/failures/errors, isolated config positive controls, identical real inventories and no owned groups left. E RED must be the two absent-parent UNSET subcases; E GREEN includes native fixture artifact assertions. Four local→local check fixtures must meet their named expectations. The frozen suite must give 155 run, 14 real-rclone skips, zero failures/errors and cleared groups; its five skipped Archive cases remain UNVERIFIED and are not activation dependencies. The full suite does not replace the 22-case run. Submit locked-release change + this evidence and r13 sandbox/host checks to Astra r13; NO-GO keeps all subsequent gates closed.

Hostfix1 coverage/fixture semantics: r13 host actions are UNRUN and use fresh r13_* labels in host_commands_r13.sh; accepted r11_hostfix1_* evidence remains linked from the frozen package. Evidence remains in R; the runner owns a fresh /private/tmp/drive_r11_<label>_*/ runtime containing HOME/fixtures/TMPDIR outside the memit source volume. Before any coverage/fixture test, saved df -P outputs resolve source and runtime paths to mount points; diskutil info -plist must establish APFSPhysicalStores on disjoint physical whole disks. Unknown/shared physical identity means STOP. ParentWholeDisk alone is insufficient. Recorded host topology is memit virtual disk6 over physical disk4s3 and /System/Volumes/Data virtual disk3 over physical disk0s2; another partition of disk4 is still rejected. Replay GREEN does not replace the live placement/config positive control or the exact 22 host tests. Both content-check templates pin --log-format date,time. The verifier accepts severity records only in that exact timestamp format and rejects unsupported records (including microseconds, time-only, prefixes and JSON). Valid DEBUG argv mentions of report --error/error.txt remain harmless; real error/read/unchecked/report failures remain fatal. Raw logs are preserved.

0.3 [READ-ONLY]. Publish pins_v4 only after evidence/review changes settle, preserving the old pin set. No built-bundle hash can exist before §1.2. Re-run the pin check after any authorized package update, and re-review changed inputs.

0.4 [RECEIPT-WRITE]. Refresh real-path inventory; ps must be available on the host. Compare with the MB40 baseline, and account for any change. The new baseline is mb40_staging_green/real_after.json, not v1's stale ec66a1f5 listing. No real history evidence is present in that baseline; the log root exists and is empty. Mandatory orphan clearance precedes merge and repeats immediately before 3.1.

<!-- row 0.4 marker=RECEIPT-WRITE -->
```bash
capture history-inventory /usr/bin/python3 -B "$R/real_inventory.py" "$HOME" "$R/history_inventory.json"
capture baseline-compare /usr/bin/cmp "$R/mb40_staging_green/real_after.json" "$R/history_inventory.json"
capture orphan-ps /bin/ps -axo pid,ppid,pgid,stat,etime,command
capture orphan-check /usr/bin/python3 -B -c 'import pathlib,sys; rows=pathlib.Path(sys.argv[1]).read_text().splitlines()[1:]; pids={32906,32913,32914,36233,36258,36259,37109,65807}; hits=[x for x in rows if int(x.split()[0]) in pids or any(s in x for s in ("memit_gdrive_native_","Native_","held-rclone","gdrive_addendum_"))]; print("\n".join(hits)); assert not hits,"STOP: fixture/PID clearance incomplete"' "$R/commands/orphan-ps/stdout.txt"
```

PID accounting: 32906,32913,32914,36233,36258,36259,37109,65807 were cleared in b74569e (orphan_clearance_20261010T221601Z.md). That historical receipt does not replace the fresh scan. Any found → STOP. [OPERATOR GO, conditional; old row 0.3a] only their confirmed owner may terminate abandoned owned fixtures, after recording ancestry and all descendants. Killing two stubs is insufficient unless every descendant exits. Do not kill a reused/unowned PID. Re-run scans with fresh labels; proceed only after no such processes remain.

<!-- row 0.4-remote marker=READ-ONLY -->
```bash
capture drive-root /opt/homebrew/bin/rclone lsd gdrive: --max-depth 1
capture drive-destination /opt/homebrew/bin/rclone lsf "$DST" --max-depth 1
```

Both exits 0; auth failures STOP. These are future host-only reads, never MB40 sandbox calls. Do not presume the destination is still empty; preserve its actual listing and resolve unexpected data with the operator.

## 1. Gated merge, immutable release, bundle and preserved receipt

1.1 [MAESTRO GO] PR creation is a GitHub write; existing candidate PR may be reused only after exact-head verification. [OPERATOR GO] for apply/merge and main-checkout update, retaining old rows 1.3 and 1.4. MAESTRO must reserve candidate/head and master mutation window, suspend competing writers, drain every candidate-head workflow/check/status writer, require exact-head successful CI and run the cooperative git-common-dir lock protocol in CLAUDE.md § Merging. A local lock does not bind GitHub writers. MERGED_WITH_FAILURE requires STOP/preservation, never undoing the merge. I and PR must be resolved before gate commands; no broad branch restoration over newer work.

Before candidate creation, set SOURCE_COMMIT to the full reviewed source commit after MAESTRO commits this finalized receipt; I must be fresh and nonexistent. The source commit must contain every literal allowlist path including pins_v4. The builder exports origin/master plus the allowlisted source entries into backup-gdrive-r12, stages them and runs verify-staged. It never commits, pushes, fetches or opens a PR. The four unchanged exceptions retain their proven source/base blob and mode equality and pins. Full index and commit path/type/blob/mode equality is mandatory, with all pin bytes read from Git blobs. STOP on any failure. Order: create -> verify-staged -> MAESTRO commits -> verify-commit -> push -> open PR -> inside the reserved merge window observe both heads and verify-pr-head immediately before gate -> compare gate report head_sha afterward. Source and integration roles remain separate.

<!-- row 1.1-candidate marker=MAESTRO-GO -->
```bash
capture r13-candidate-create /bin/sh "$R/make_backup_candidate.sh" create "$W" "$SOURCE_COMMIT" "$I"
```

<!-- row 1.1-verify-staged marker=READ-ONLY -->
```bash
capture r13-verify-staged /bin/sh "$R/make_backup_candidate.sh" verify-staged "$I" "$SOURCE_COMMIT"
```

<!-- row 1.1-commit marker=MAESTRO-GO -->
```bash
capture r13-candidate-commit /usr/bin/git -C "$I" commit -m 'Google Drive backup r13 candidate'
```

<!-- row 1.1-commit-sha marker=READ-ONLY -->
```bash
capture r13-candidate-commit-sha /usr/bin/git -C "$I" rev-parse HEAD
```

MAESTRO reads that successful, nonempty capture and validates a single 40-hex SHA before setting CANDIDATE_COMMIT. Never use an unchecked substitution. verify-commit requires that SHA's complete tree to equal origin/master plus exactly the allowlisted source entries and its only parent to be origin/master. On PASS it exclusively creates VERIFIED_SHA_FILE; this receipt is outside candidate scope. Existing receipt or any failure means STOP; re-review changes and use fresh labels/receipt, never waive.

<!-- row 1.1-verify-commit marker=RECEIPT-WRITE -->
```bash
capture r13-verify-commit /bin/sh "$R/make_backup_candidate.sh" verify-commit "$I" "$SOURCE_COMMIT" "$CANDIDATE_COMMIT" --receipt-file "$VERIFIED_SHA_FILE"
```

<!-- row 1.1-push marker=MAESTRO-GO -->
```bash
capture r13-candidate-push /usr/bin/git -C "$I" push origin backup-gdrive-r12
```

<!-- row 1.1-pr marker=MAESTRO-GO -->
```bash
capture pr-create /opt/homebrew/bin/gh pr create --base master --head backup-gdrive-r12 --title 'Google Drive backup release and activation evidence' --body-file "$R/pr_body.md"
```

<!-- row 1.1-dry marker=READ-ONLY -->
```bash
capture hygiene-dry /usr/bin/env LLMDB_ROOT="$I" /usr/bin/python3 -B "$I/tools/git_hygiene.py" --dry-run
capture gate-dry /usr/bin/env LLMDB_ROOT="$I" /usr/bin/python3 -B "$I/tools/git_merge_gate.py" "$PR" --dry-run
```

Both dry-run receipts must report OK. Review complete gate output and exact head, required checks, external-writer drain and reservation before GO.

<!-- row 1.1-hygiene-apply marker=OPERATOR-GO -->
```bash
capture hygiene-apply /usr/bin/env LLMDB_ROOT="$I" /usr/bin/python3 -B "$I/tools/git_hygiene.py" --apply
```

Inside the already reserved candidate/head and master mutation window, with competing writers suspended and drained, capture both read-only observations now. gate_binding.py validates complete gh JSON and a single exact ls-remote ref row, then calls candidate.verify_pr_head(VERIFIED_SHA_FILE, observed PR SHA, observed remote SHA). All three must be valid, equal 40-hex SHAs. No snapshot from before this window is reusable. Inspect each successful, nonempty capture; any mismatch means STOP before the gate. Immediately after the binding PASS, run the next gate row; do not interleave another command or release the reservation.

<!-- row 1.1-pr-observe marker=READ-ONLY -->
```bash
capture r13-pr-head /opt/homebrew/bin/gh pr view "$PR" --json headRefOid
```

<!-- row 1.1-remote-observe marker=READ-ONLY -->
```bash
capture r13-remote-head /usr/bin/git -C "$I" ls-remote origin refs/heads/backup-gdrive-r12
```

<!-- row 1.1-verify-pr-head marker=READ-ONLY -->
```bash
capture r13-verify-pr-head /usr/bin/python3 -B "$R/gate_binding.py" heads "$VERIFIED_SHA_FILE" "$R/commands/r13-pr-head/stdout.txt" "$R/commands/r13-remote-head/stdout.txt"
```

<!-- row 1.1-gate marker=OPERATOR-GO -->
```bash
capture r13-merge-apply /usr/bin/env LLMDB_ROOT="$I" /usr/bin/python3 -B "$I/tools/git_merge_gate.py" "$PR" --apply
```

<!-- row 1.1-gate-head marker=READ-ONLY -->
```bash
capture r13-gate-head /usr/bin/python3 -B "$R/gate_binding.py" gate "$VERIFIED_SHA_FILE" "$R/commands/r13-merge-apply/stdout.txt"
```

Gate report head_sha must equal the verified SHA. A mismatch is a FAILURE, never waived: STOP and preserve the merged SHA/report if a merge occurred; never undo it. The existing gate has no expected-head argument and protects the head it observes during its run; the reserved window, dual observation and post-gate comparison bind that head to our verified commit. No gate/hygiene code change is required.

<!-- row 1.1-main-update marker=OPERATOR-GO -->
```bash
capture main-fetch /usr/bin/git -C "$M" fetch origin
capture main-ff /usr/bin/git -C "$M" merge --ff-only origin/master
```

All exits 0, merged SHA saved, post-merge master CI green, no conflict. Before the shared-main update MAESTRO verifies it is clean and reserved. Reject current commit unless the verified index/commit trees equal origin/master plus the literal allowlist entries, the dual heads and gate report bind the verified SHA, and every pinned candidate/evidence file matches pins_v4, and all seven deployment inputs match pins_v4; MERGED_SHA comes from the guarded merge result, not an unchecked command substitution.

<!-- row 1.1-bytes marker=READ-ONLY -->
```bash
capture deployment-bytes /usr/bin/python3 -B -c 'import hashlib,json,pathlib,sys; root=pathlib.Path(sys.argv[1]); pins=json.loads(pathlib.Path(sys.argv[2]).read_text()); files=[x for x in pins["files"] if x["path"] in ("tools/backup_gdrive.sh","tools/backup_gdrive_status.py","tools/backup_mirror.excludes","tools/launchd/MemitGdriveBackup.applescript","tools/launchd/build_gdrive_applet.sh","tools/launchd/stage_gdrive_release.sh","tools/launchd/com.rhu.memit-gdrive-backup.plist")]; assert len(files)==7; [print(x["path"],hashlib.sha256((root/x["path"]).read_bytes()).hexdigest()) for x in files]; assert all(hashlib.sha256((root/x["path"]).read_bytes()).hexdigest()==x["sha256"] for x in files)' "$M" "$R/pins_v4.json"
```

1.2 [OPERATOR GO] Stage/build/hash (retains old 1.7). Builder calls pinned stage_gdrive_release.sh itself: do not pre-create the same release. Use a fresh release identifier, empty app target and explicit outside-checkout root. No checkout copies are used for deployed status. The stage exports committed wrapper/status/excludes and writes a manifest with four applet hash stamps (three files plus MANIFEST); builder canonicalizes source, compiles app, compares a fresh saved-source decompilation, and prints every bundle-file hash.

<!-- row 1.2 marker=OPERATOR-GO -->
```bash
capture build /bin/bash "$M/tools/launchd/build_gdrive_applet.sh" "$MERGED_SHA" "$RELEASE_ID" "$APP" "$HOME/Library/Application Support/memit-gdrive-backup/releases"
```

Exit 0 required; never overwrite a release/app/source/decompile. Record stdout as the bundle_manifest (full shasum -c format). Stage script and builder were pinned before execution; deployed wrapper/status/excludes must match the seven-input review and MANIFEST. An app build alone authorizes no launch.

1.3 [READ-ONLY] Bundle manifest and full source comparison. Builder output covers all bundle files. Recompute population and hashes, then cmp it to the builder manifest; shasum -c alone does not detect an extra file. Confirm saved canonical source and builder's app decompile, by fresh compilation/decompilation as the builder does (osadecompile can grow terminal newlines, so compare two compiles of the same saved source). Pin rendered source, saved decompile, independent decompiles, release MANIFEST and bundle manifest in build_time_pins.sha256 and preserve them for review.

<!-- row 1.3-hashes marker=READ-ONLY -->
```bash
capture bundle-manifest /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; p=pathlib.Path(sys.argv[1]); files=sorted(x for x in p.rglob("*") if x.is_file()); assert files; [print(hashlib.sha256(x.read_bytes()).hexdigest()+"  "+str(x)) for x in files]' "$APP"
capture bundle-manifest-compare /usr/bin/cmp "$R/commands/build/stdout.txt" "$R/commands/bundle-manifest/stdout.txt"
capture bundle-file-check /usr/bin/shasum -a 256 -c "$R/commands/build/stdout.txt"
capture release-manifest /usr/bin/python3 -B -c 'import hashlib,json,pathlib,sys; d=pathlib.Path(sys.argv[1]); pins=json.loads(pathlib.Path(sys.argv[2]).read_text()); expected={pathlib.Path(x["path"]).name:x["sha256"] for x in pins["files"] if x["path"] in ("tools/backup_gdrive.sh","tools/backup_gdrive_status.py","tools/backup_mirror.excludes")}; assert set(x.name for x in d.iterdir())==set(expected).union({"MANIFEST"}); [print(n,hashlib.sha256((d/n).read_bytes()).hexdigest()) for n in expected]; assert all(hashlib.sha256((d/n).read_bytes()).hexdigest()==h for n,h in expected.items()); assert (d/"MANIFEST").read_text()=="".join(h+"  "+n+"\n" for n,h in expected.items())' "$D" "$R/pins_v4.json"
```

<!-- row 1.3-compile marker=OPERATOR-GO -->
```bash
capture source-compile /usr/bin/osacompile -o "$R/saved-source.scpt" "$APP.applescript"
capture source-decompile /usr/bin/osadecompile "$R/saved-source.scpt"
capture app-decompile /usr/bin/osadecompile "$APP/Contents/Resources/Scripts/main.scpt"
```

<!-- row 1.3-compare marker=READ-ONLY -->
```bash
capture source-full-cmp /usr/bin/cmp "$R/commands/source-decompile/stdout.txt" "$R/commands/app-decompile/stdout.txt"
capture saved-decompile-cmp /usr/bin/cmp "$APP.decompiled.applescript" "$R/commands/app-decompile/stdout.txt"
capture build-time-pins /usr/bin/shasum -a 256 "$APP.applescript" "$APP.decompiled.applescript" "$D/MANIFEST" "$R/commands/build/stdout.txt" "$R/commands/source-decompile/stdout.txt" "$R/commands/app-decompile/stdout.txt"
```

<!-- row 1.3-preserve marker=RECEIPT-WRITE -->
```bash
capture preserve-build-pins /bin/cp -p "$R/commands/build-time-pins/stdout.txt" "$R/build_time_pins.sha256"
```

Every compare exits 0. MAESTRO records/commits the build manifest and build-time pins. Plist pin is 702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce, excludes pin 45bb4e2a2e4629d494b6e5ccf41dd6885133b27e329a197fc6a85bcc55e48f3f; builder/stage/app-source pins are in pins_v4.json.

1.4 [READ-ONLY] Receipt preservation is already complete at c1a06ea: results/dashboard_audit_20261010/leaked_test_receipt/launch_receipt.json, SHA-256 53614afd90df282c8e90f8299c0fb98b81a10b35f6838377757ff1e36d0af6b4. Preserve/link that immutable repo receipt; do not put it back into real HOME or expect it in a new recovery archive.

<!-- row 1.4 marker=READ-ONLY -->
```bash
capture preserved-receipt /usr/bin/shasum -a 256 "$W/results/dashboard_audit_20261010/leaked_test_receipt/launch_receipt.json"
```

## 2. Empty-history branch and conditional recovery

2.1 [RECEIPT-WRITE]. Decide again immediately before the state write. The MB40 inventory shows truly empty observed history, unlike v1. Fresh automatic allocation is possible; this plan selects an explicit empty-history recovery checkpoint to retain the reviewed barrier protocol and required order. Floor 0 is conditional on the operator explicitly confirming **no issued history was lost** (including off-disk/lost issued evidence). An empty directory alone does not prove that statement. Recovery is for damaged ordering history, not routine retry; this one bootstrap use establishes an auditable barrier rather than repairing a transfer failure.

<!-- row 2.1 marker=RECEIPT-WRITE -->
```bash
capture pre-recovery-inventory /usr/bin/python3 -B "$R/real_inventory.py" "$HOME" "$R/pre_recovery_inventory.json"
capture empty-history-check /usr/bin/python3 -B -c 'import json,pathlib,sys; rows=json.loads(pathlib.Path(sys.argv[1]).read_text()); roots=[x for x in rows if "/Library/Logs/memit-gdrive-backup" in x["path"]]; allowed=str(pathlib.Path(sys.argv[2])/"Library/Logs/memit-gdrive-backup"); print(json.dumps(roots,indent=2)); assert roots; assert all(x["kind"]=="absent" or (x["path"]==allowed and x["kind"]=="directory") for x in roots),"STOP: any evidence present; decide again with operator"' "$R/pre_recovery_inventory.json" "$HOME"
```

If any evidence is present (counter/state/receipt/heartbeat/journal/refusal/temporaries/archives/ownership lock, unknown file, symlink, unreadability), STOP and decide again with the operator. Inspect the whole history and scanner's observed maximum, including preserved generations, before choosing a floor. Ambiguity never proves zero. Do not initialize a zero counter over evidence, discard files, hand-repair state, or raise a floor to suppress a refusal. Production status/recover always use /usr/bin/python3 and the pinned deployed D file, with a hash check immediately preceding each use.

2.2 [OPERATOR GO] (old 2.2). Requires empty-history-check PASS and the no-lost-history confirmation. Run in foreground with real HOME. No recovery dry-run is required or provided. Read the scanner at tools/backup_gdrive_status.py:285–443; it checks observed generations before reserving the barrier.

<!-- row 2.2-pin marker=READ-ONLY -->
```bash
capture recover-status-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
```

<!-- row 2.2 marker=OPERATOR-GO -->
```bash
capture recovery /usr/bin/python3 -B "$D/backup_gdrive_status.py" recover --generation-floor 0
```

For this empty branch, observed highest H=0 and approved floor F=0; barrier B=max(H,F)+1. Exact stdout is `backup_gdrive_status: recovery barrier generation <B>; preserved evidence: <HOME>/Library/Logs/memit-gdrive-backup-launch-state/recoveries/<YYYYMMDDTHHMMSS.ffffffZ>; requires a subsequent completed generation above the barrier`, one line; exit 0. B is recorded from the actual receipt. Post-state: counter contains decimal B plus newline; unresolved.json is `{"compaction_barrier":null,"issued_generation":<B>,"recovery_barrier":<B>,"schema":1,"unresolved":[]}`; new archive contains only manifest.json with schema=1, generation_floor=0, highest_seen=0, recovery_barrier=B, preserved_paths=[]; counter.lock exists. Live backup log root remains empty. There is no archived leaked receipt because c1a06ea already preserved it elsewhere. The first launch must allocate the observed successor B+1; every later launch derives its expectation from the immediately observed counter.

2.3 [RECEIPT-WRITE] Capture state and archive as found, using ARCHIVE set to the exact recovery stdout path (not a glob or unchecked ls extraction).

<!-- row 2.3 marker=RECEIPT-WRITE -->
```bash
capture recovery-state /bin/cat "$HOME/Library/Logs/memit-gdrive-backup-launch-state/counter" "$HOME/Library/Logs/memit-gdrive-backup-launch-state/unresolved.json" "$ARCHIVE/manifest.json"
capture recovery-preserve /usr/bin/ditto "$HOME/Library/Logs/memit-gdrive-backup-launch-state" "$R/recovery_state_copy"
capture recovery-post-inventory /usr/bin/python3 -B "$R/real_inventory.py" "$HOME" "$R/recovery_post_inventory.json"
```

Compare every field and archive population to 2.2; mismatch STOP. Keep recovery output, counter/state and archive bytes and hashes. A barrier is not backup health.

2.4 [READ-ONLY]. Expected exit 1 and exactly `backup_gdrive_status: unacknowledged recovery barrier generation <B>: requires a subsequent completed heartbeat; manual/unsequenced heartbeat cannot acknowledge applet evidence`. **Exit 0 is false green → STOP.**

<!-- row 2.4 marker=READ-ONLY -->
```bash
capture barrier-status-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
capture barrier-status /usr/bin/python3 -B "$D/backup_gdrive_status.py"
```

## 3. Initial upload, Allow, completion and full content checkpoint

3.1 [READ-ONLY] immediately before 3.1 launch: fresh full ps, mandatory eight-PID/native-fixture check, disk check, mounted source and lock clearance. Any fixture/PID found → STOP. If ps cannot be read, clearance is UNAVAILABLE, never assumed. Record the pre-launch counter, call it G, and require the observed successor G+1 after launch.

<!-- row 3.1-clear marker=READ-ONLY -->
```bash
capture pre-launch-ps /bin/ps -axo pid,ppid,pgid,stat,etime,command
capture pre-launch-clear /usr/bin/python3 -B -c 'import pathlib,sys; rows=pathlib.Path(sys.argv[1]).read_text().splitlines()[1:]; pids={32906,32913,32914,36233,36258,36259,37109,65807}; hits=[x for x in rows if int(x.split()[0]) in pids or any(s in x for s in ("memit_gdrive_native_","Native_","held-rclone","gdrive_addendum_"))]; print("\n".join(hits)); assert not hits,"STOP: fixture/PID found"' "$R/commands/pre-launch-ps/stdout.txt"
capture pre-launch-disk /bin/df -k / /Volumes/memit
capture pre-launch-counter /bin/cat "$HOME/Library/Logs/memit-gdrive-backup-launch-state/counter"
capture pre-launch-source-lock /usr/bin/python3 -B -c 'import pathlib; source=pathlib.Path("/Volumes/memit/llm-database-poc-mirror"); lock=pathlib.Path.home()/"Library/Logs/memit-gdrive-backup.lock"; print(source,lock); assert source.is_dir(); assert not lock.exists() and not lock.is_symlink(),"STOP: ownership lock present"'
```

3.1 [OPERATOR GO] (old 3.1). Run in a persistent terminal/tmux pane at the Mac on AC with memit mounted. The command blocks until open's app lifetime ends, so inspect assertions/progress from a second terminal. Initial ~287 GB upload may take ~4–4.5 days with daytime 08:00–23:00 at 512 KiB/s and the historical nighttime 1.16 MB/s assumption; measure actual progress, do not turn that estimate into a deadline. Old internal mirror job remains until §5. `caffeinate -i -s /usr/bin/open -W -g` asserts idle and system wakefulness for the utility lifetime; -s requires AC. Verify assertions while it runs.

<!-- row 3.1-launch marker=OPERATOR-GO -->
```bash
capture initial-launch /usr/bin/caffeinate -i -s /usr/bin/open -W -g "$APP"
```

3.2 [OPERATOR CLICK] (old 3.2). Grant macOS Removable Volumes **Allow** physically at the Mac. Capture the approval time and operator confirmation in R. A phone session cannot click it. Receipt/heartbeat must name the observed successor, launch_mode=applet and the pinned release wrapper. No prompt plus no wrapper start within a few minutes → STOP; preserve observations before any owner-approved kill.

3.3 [READ-ONLY]. Status may be masked by the unacknowledged barrier (S:528–529); independently check owner, child and progress. First capture heartbeat and lock PIDs, read OWNER_PID, CHILD_PID and RUN_LOG from those validated files; use those observed integers/absolute path, not broad pgrep guesses. Ensure live PIDs agree with heartbeat/lock and belong to this release wrapper/source/destination. Run each observation with fresh labels if repeated.

<!-- row 3.3 marker=READ-ONLY -->
```bash
capture wake-assertions /usr/bin/pmset -g assertions
capture upload-heartbeat /bin/cat "$HOME/Library/Logs/memit-gdrive-backup/last_run.json"
capture upload-lock /bin/cat "$HOME/Library/Logs/memit-gdrive-backup.lock/owner" "$HOME/Library/Logs/memit-gdrive-backup.lock/rclone.pid"
capture upload-owner /bin/ps -p "$OWNER_PID" -o pid,ppid,pgid,stat,etime,command
capture upload-child /bin/ps -p "$CHILD_PID" -o pid,ppid,pgid,stat,etime,command
capture upload-progress /bin/cat "$RUN_LOG"
capture upload-wrapper /bin/cat "$HOME/Library/Logs/memit-gdrive-backup.log"
capture upload-status-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
capture upload-status /usr/bin/python3 -B "$D/backup_gdrive_status.py"
```

Assert pmset lists this caffeinate PID's PreventUserIdleSystemSleep and PreventSystemSleep assertions active on AC. Record advancing transferred bytes/completed-file counts with observation timestamps from independent raw progress snapshots. Barrier-related status exit 1 during the upload is expected and proves neither progress nor owner health. Dead owner/child, stalled progress or errors → diagnose and STOP; no retry policy change.

3.4 [READ-ONLY/RECEIPT-WRITE]. After initial-launch returns, read strictly before end+13 h (S:604), not start+13 h. The initial capture exit must be 0. Save full receipt, heartbeat, counter/state, journal presence and wrapper/run logs; status must exit 0 and say `fresh successful backup; finished <end>; launch generation <observed successor>`. Require matching sequenced receipt/heartbeat generation, receipt exit_code=0/error_number=null, heartbeat end set/exit_code=0/rclone_exit_code=0/warnings=[], unresolved empty, no unacknowledged later issue or failure evidence, no ownership lock or surviving sync. A launchd/open exit alone is not health evidence.

<!-- row 3.4 marker=RECEIPT-WRITE -->
```bash
capture completion-receipt /bin/cat "$HOME/Library/Logs/memit-gdrive-backup/launch_receipt.json" "$HOME/Library/Logs/memit-gdrive-backup/last_run.json" "$HOME/Library/Logs/memit-gdrive-backup-launch-state/counter" "$HOME/Library/Logs/memit-gdrive-backup-launch-state/unresolved.json"
capture completion-copy /usr/bin/ditto "$HOME/Library/Logs/memit-gdrive-backup" "$R/initial_completion_copy"
capture completion-state-copy /usr/bin/ditto "$HOME/Library/Logs/memit-gdrive-backup-launch-state" "$R/initial_completion_state_copy"
capture completion-inventory /usr/bin/python3 -B "$R/real_inventory.py" "$HOME" "$R/completion_inventory.json"
capture completion-ps /bin/ps -axo pid,ppid,pgid,stat,etime,command
capture completion-status-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
capture completion-status /usr/bin/python3 -B "$D/backup_gdrive_status.py"
```

**Transfer failure branch (covers r10's generation-2 example without hard-coded expectations):** after clean termination, STOP, preserve evidence, diagnose the transfer failure, and obtain confirmation from the actual owner. Capture ps, owner/child identities, logs and lock bytes. Clear the lock and processes only after proving no old transfer survives and with [OPERATOR GO]; preserve the lock before any removal. Re-open with [OPERATOR GO] using the same pinned app as the next observed successor, then repeat completion checks. Do not call recover for a routine transfer failure; use it only for damaged ordering history, with a newly reviewed inventory/floor. No automatic retry, stale-lock age expiration or counter repair.

3.5 **[OPERATOR GO] write pause and final catch-up**, then **[OPERATOR GO] full check**. Sequence: initial upload → write pause → final catch-up sync → content check → record the checked inventory. Files changed since the first start get **no waiver**. `fresh backup with warnings` never satisfies activation even if warnings are explained; require a subsequent clean sequenced completion and passing content check. Retirement stays blocked until convergence.

Included writers to pause: experiment/tensor/artifact jobs writing under SRC; Python/MAESTRO/Claude/Codex workers and editor saves in the main repo; dashboard/Lab View builders writing included results/logs; Git fetch/commit/repack/gc/maintenance; cron/launchd/automation and external file-sync services writing included paths. Worktree receipt writes are excluded. MAESTRO reserves the pause and stops/queues these actors with their actual owners, recording names/PIDs/service IDs and approvals; unknown writer → STOP. Do not stop the old mirror merely for reading SRC, and do not retire it here. Exact ps plus lsof commands below prove the named processes are gone and no included write-capable descriptor remains; operator confirms no paused task may restart during verification. This is an operational coordination premise, not proof about an unobserved external writer.

<!-- row 3.5-pause marker=OPERATOR-GO -->
```bash
capture writer-ps /bin/ps -axo pid,ppid,pgid,stat,etime,command
capture writer-descriptors /usr/sbin/lsof -nP +D "$SRC"
capture final-catch-up /usr/bin/caffeinate -i -s /usr/bin/open -W -g "$APP"
```

Full ps output must show no registered included writer (apart from this catch-up's reader and excluded evidence tools). In lsof FD column, any w/u descriptor for an included file → STOP and resolve; read-only descriptors are accounted for. An empty lsof exit 1 is accepted only with saved complete empty output and no diagnostic; any permission/traversal failure STOP. Catch-up allocates the observed successor; keep its open exit, receipt, clean heartbeat and all 3.4 evidence under fresh labels, and run the hash-checked deployed status again strictly before its end+13 h. All are required before starting a check. Pause stays in force until the final inventory is recorded.

<!-- row 3.5-catchup-status marker=READ-ONLY -->
```bash
capture catchup-status-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
capture catchup-status /usr/bin/python3 -B "$D/backup_gdrive_status.py"
capture check-preflight-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
capture check-preflight /usr/bin/python3 -B "$D/backup_gdrive_status.py" preflight --rclone /opt/homebrew/bin/rclone --source "$SRC" --destination "$DST"
```

Exit 0 required for both status and preflight; reject inherited behavior-changing RCLONE_* and config overrides. Identical filters and --links are applied to inventory and check; flags below come from captured v1.75.2 check --help, not guessed flags. Default rclone check hashes local content against destination checksums; --one-way covers every included source object and permits destination-only history/protected excluded data. No sampling or size comparison substitute is accepted. Full --download fallback covers the entire population if even one object lacks a comparable hash, avoiding selective-list omissions. [rclone check documentation](https://rclone.org/commands/rclone_check/)

<!-- row 3.5-inventory marker=OPERATOR-GO -->
```bash
capture checked-population /opt/homebrew/bin/rclone lsf "$SRC" --recursive --files-only --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links
capture metadata-before /opt/homebrew/bin/rclone lsjson "$SRC" --recursive --files-only --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links
```

<!-- row 3.5-check marker=OPERATOR-GO -->
```bash
capture full-check /usr/bin/caffeinate -i -s /opt/homebrew/bin/rclone check "$SRC" "$DST" --one-way --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links --combined "$C/combined.txt" --differ "$C/differ.txt" --missing-on-dst "$C/missing-on-dst.txt" --error "$C/error.txt" --log-file "$C/check.log" --log-level DEBUG --log-format date,time --stats 0 --retries 1
```

The check command blocks in the persistent first terminal. On AC, while it is running, execute the following row in the second terminal. Require this check's caffeinate PID to hold active PreventUserIdleSystemSleep and PreventSystemSleep assertions; absent assertions or utility exit during verification means STOP.

<!-- row 3.5-check-wake marker=READ-ONLY -->
```bash
capture check-wake-assertions /usr/bin/pmset -g assertions
```

<!-- row 3.5-verifier marker=RECEIPT-WRITE -->
```bash
capture check-inventory-copy /bin/cp -p "$R/commands/checked-population/stdout.txt" "$C/inventory.txt"
capture check-inventory-exit-copy /bin/cp -p "$R/commands/checked-population/exit_code.txt" "$C/inventory.exit_code.txt"
capture check-verdict /usr/bin/python3 -B "$R/verify_check.py" "$C"
```

PASS requires check exit_code.txt=0, inventory exit 0, all four complete reports, exact full inventory coverage, terminal log counts agreeing with reports, and zero missing/differing/unreadable/error/unchecked entries. A missing/truncated/duplicated/unhashed report cannot pass. Preserve the default FAIL and counts if a no-comparable-hash object is encountered; do not excuse it. The follow-up below is a full-population content download check with identical filters/report capture. It is conditional on no-comparable-hash evidence, not a retry for differing/error entries; every other failure stops for diagnosis/catch-up.

<!-- row 3.5-download marker=OPERATOR-GO -->
```bash
capture full-check-download /usr/bin/caffeinate -i -s /opt/homebrew/bin/rclone check "$SRC" "$DST" --one-way --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links --combined "$CD/combined.txt" --differ "$CD/differ.txt" --missing-on-dst "$CD/missing-on-dst.txt" --error "$CD/error.txt" --log-file "$CD/check.log" --log-level DEBUG --log-format date,time --stats 0 --retries 1 --download
```

If the full-population download fallback is required, keep AC connected and capture its own active caffeinate assertions from the second terminal while the first terminal command blocks. The same assertion pass rule applies for the entire fallback lifetime.

<!-- row 3.5-download-wake marker=READ-ONLY -->
```bash
capture download-wake-assertions /usr/bin/pmset -g assertions
```

<!-- row 3.5-download-verifier marker=RECEIPT-WRITE -->
```bash
capture download-inventory-copy /bin/cp -p "$R/commands/checked-population/stdout.txt" "$CD/inventory.txt"
capture download-inventory-exit-copy /bin/cp -p "$R/commands/checked-population/exit_code.txt" "$CD/inventory.exit_code.txt"
capture download-verdict /usr/bin/python3 -B "$R/verify_check.py" "$CD"
```

Select VERIFIED_CHECK=C only after its PASS, or CD after a passing required fallback. The default FAIL remains in the audit. Drive reads: hash mode lists/checks metadata/checksums for the complete population (~40k objects), with ~287 GB local sequential reads. Assuming 100 MB/s effective local throughput gives ~2,871 s (~48 min); reserve ≥90 min for hashing/enumeration/API/IO variance and maintain wakefulness. If download fallback is needed, add another ~287 GB local read and ~287 GB Drive download, streamed without bulk disk writes; at an assumed effective 10 MB/s, ~8 h plus overhead (at 1.16 MB/s ~69 h). These are explicit assumptions, not measured guarantees. Keep the pause and retirement block for as long as actual verification takes. The exact default and download commands above each keep their own caffeinate utility alive until rclone exits; their second-terminal pmset receipts must confirm both assertions on AC.

<!-- row 3.5-final-inventory marker=OPERATOR-GO -->
```bash
capture metadata-after /opt/homebrew/bin/rclone lsjson "$SRC" --recursive --files-only --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links
```

<!-- row 3.5-record marker=RECEIPT-WRITE -->
```bash
capture metadata-compare /usr/bin/python3 -B -c 'import json,pathlib,sys; records=[json.loads(pathlib.Path(x).read_text()) for x in sys.argv[1:]]; canonical=lambda a:sorted(a,key=lambda x:x["Path"]); assert canonical(records[0])==canonical(records[1]),"STOP: included inventory changed during check"; print("PASS unchanged full metadata inventory",len(records[0]),sum(x["Size"] for x in records[0]))' "$R/commands/metadata-before/stdout.txt" "$R/commands/metadata-after/stdout.txt"
capture record-checked-inventory /bin/cp -p "$R/commands/metadata-after/stdout.txt" "$R/checked_inventory.json"
capture checked-evidence-pins /usr/bin/shasum -a 256 "$R/checked_inventory.json" "$VERIFIED_CHECK/inventory.txt" "$VERIFIED_CHECK/combined.txt" "$VERIFIED_CHECK/differ.txt" "$VERIFIED_CHECK/missing-on-dst.txt" "$VERIFIED_CHECK/error.txt" "$VERIFIED_CHECK/check.log" "$VERIFIED_CHECK/stdout.txt" "$VERIFIED_CHECK/stderr.txt" "$VERIFIED_CHECK/exit_code.txt"
```

Metadata stability supplements content verification; it supplies no timestamp waiver. Require all capture exits 0 and the preceding verifier PASS. Record the approved pause window, catch-up generation/end, content-verdict receipt, population count/bytes, checksums and observed inventory. Then [OPERATOR GO] releases the writer pause with its actor owners; this does not authorize retirement yet.

## 4. Install/bootstrap/kickstart and fresh successor

4.1 [OPERATOR GO] (old 4.1). Copy the pinned plist (not a symlink on the external volume); hash/lint it. Keep the same validated bundle and Allow grant.

<!-- row 4.1 marker=OPERATOR-GO -->
```bash
capture plist-install /bin/cp -p "$M/tools/launchd/com.rhu.memit-gdrive-backup.plist" "$HOME/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist"
capture plist-hash /usr/bin/shasum -a 256 "$HOME/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist"
capture plist-lint /usr/bin/plutil -lint "$HOME/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist"
```

Exit 0 for each; exact 702868b8… pin and OK. Existing unexpected target → STOP, do not overwrite it without a new exact-path GO.

4.2 [OPERATOR GO] (old 4.2) enable/bootstrap, followed by read-only enabled-state proof. RunAtLoad=false; StartInterval=21600 seconds (six hours). Loading/login does not immediately run the job. The first periodic run is about six hours after bootstrap/login while awake; sleep can delay/coalesce it. Manual kickstart below intentionally exercises the same scheduled LaunchAgent path sooner. Nice=5 on the production job is separate from niceness-0 host test requirements.

<!-- row 4.2 marker=OPERATOR-GO -->
```bash
capture new-enable /bin/launchctl enable "gui/$USER_UID/com.rhu.memit-gdrive-backup"
capture new-bootstrap /bin/launchctl bootstrap "gui/$USER_UID" "$HOME/Library/LaunchAgents/com.rhu.memit-gdrive-backup.plist"
```

<!-- row 4.2-state marker=READ-ONLY -->
```bash
capture new-enabled /bin/launchctl print-disabled "gui/$USER_UID"
capture new-loaded /bin/launchctl print "gui/$USER_UID/com.rhu.memit-gdrive-backup"
capture scheduled-counter-before /bin/cat "$HOME/Library/Logs/memit-gdrive-backup-launch-state/counter"
```

Require disabled map entry false (or absent with explicit successful enable and job print), not true; loaded program /usr/bin/open, pinned app path, interval 21600, initially no run. If bootstrap schedules unexpectedly before kickstart, capture and use the observed counter/run history; never assume a number or issue overlapping launches.

4.3 [OPERATOR GO] (old 4.3). Require no active old/new transfer; expected generation is the observed successor of scheduled-counter-before. No new Allow prompt should be needed for the same bundle; denial → STOP.

<!-- row 4.3 marker=OPERATOR-GO -->
```bash
capture new-kickstart /bin/launchctl kickstart "gui/$USER_UID/com.rhu.memit-gdrive-backup"
```

4.4 [READ-ONLY/RECEIPT-WRITE]. Fresh scheduled-path completion is required: actual LaunchAgent runs increases, app/owner/child exit, sequenced receipt and clean heartbeat match observed successor, unresolved empty, no new failure evidence, no lock, status clean/exit 0 strictly before that end+13 h. Preserve complete job/launchd output; launchd exit alone never proves backup health. Repeat 3.4 complete captures with fresh labels. A naturally timed six-hour run remains distinct from this immediate scheduled-path kickstart proof.

<!-- row 4.4 marker=RECEIPT-WRITE -->
```bash
capture scheduled-job /bin/launchctl print "gui/$USER_UID/com.rhu.memit-gdrive-backup"
capture scheduled-log /bin/cat "$HOME/Library/Logs/memit-gdrive-backup.launchd.log"
capture scheduled-ps /bin/ps -axo pid,ppid,pgid,stat,etime,command
capture scheduled-receipt /bin/cat "$HOME/Library/Logs/memit-gdrive-backup/launch_receipt.json" "$HOME/Library/Logs/memit-gdrive-backup/last_run.json" "$HOME/Library/Logs/memit-gdrive-backup-launch-state/counter" "$HOME/Library/Logs/memit-gdrive-backup-launch-state/unresolved.json"
capture scheduled-copy /usr/bin/ditto "$HOME/Library/Logs/memit-gdrive-backup" "$R/scheduled_completion_copy"
capture scheduled-state-copy /usr/bin/ditto "$HOME/Library/Logs/memit-gdrive-backup-launch-state" "$R/scheduled_completion_state_copy"
capture scheduled-status-pin /usr/bin/python3 -B -c 'import hashlib,pathlib,sys; h=hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest(); print(h); assert h==sys.argv[2]' "$D/backup_gdrive_status.py" 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46
capture scheduled-status /usr/bin/python3 -B "$D/backup_gdrive_status.py"
```

## 5. Retirement — final independent GO

5.1 [OPERATOR GO] (old 5.2) only after clean sequenced completion, the passing §3.5 full content checkpoint/checked inventory, and §4.4 fresh scheduled-path completion. Verify no active old sync first. If any checkpoint is missing, remain blocked. Bootout + disable is sufficient; optional plist parking is separate.

<!-- row 5.1-pre marker=READ-ONLY -->
```bash
capture old-job-before /bin/launchctl print "gui/$USER_UID/com.rhu.memit-backup"
capture old-sync-before /bin/ps -axo pid,ppid,pgid,stat,etime,command
```

Any old MemitBackup.app, backup_mirror.sh or its rsync descendant still running → STOP; account for full ancestry, not only two process names.

<!-- row 5.1-retire marker=OPERATOR-GO -->
```bash
capture old-bootout /bin/launchctl bootout "gui/$USER_UID/com.rhu.memit-backup"
capture old-disable /bin/launchctl disable "gui/$USER_UID/com.rhu.memit-backup"
```

<!-- row 5.1-verify marker=READ-ONLY -->
```bash
capture retired-disabled /bin/launchctl print-disabled "gui/$USER_UID"
capture retired-service /bin/launchctl print "gui/$USER_UID/com.rhu.memit-backup"
capture retired-processes /bin/ps -axo pid,ppid,pgid,stat,etime,command
```

Bootout/disable exit 0; print-disabled explicitly marks com.rhu.memit-backup=true. retired-service nonzero must specifically report Could not find service; any other diagnostic STOP. Full ps must show no surviving old sync/app/rsync descendant, new job stays enabled. Preserve all exact outputs/exits.

5.2 [OPERATOR GO, OPTIONAL] (old 5.3) park the old plist only after the operator selects an exact destination PARKED_PLIST outside LaunchAgents and approves that move; no deletion. The old ~/Backups/memit mirror and ~/Applications/MemitBackup.app remain separate size/path/method approval decisions.

<!-- row 5.2 marker=OPERATOR-GO -->
```bash
capture park-old-plist /bin/mv "$HOME/Library/LaunchAgents/com.rhu.memit-backup.plist" "$PARKED_PLIST"
```

## STOP and preservation rules — every v1 condition retained/strengthened

Preserve named files unchanged: capture shasum and cp -p/ditto into a fresh R label, along with full logs/process/assertion evidence; do not edit/move/rename/delete the originals to make a check green. Preserve all recovery refusals and diagnose with the operator. No hidden pipeline exits and no different-floor retries.

1. Any source/deployed/bundle/plist/pin mismatch, or unexpected fresh-inventory drift before the selected history branch. The stale ec66a1f5 baseline is superseded, never patched.
2. Unsupported recovery evidence: recovery refused; unsupported recovery evidence in/format/nested generation field/generation field; duplicate JSON key; unsupported counter temporary; malformed preserved recovery manifest/unresolved generation state; floor below observed maximum; generation space exhausted; backup ownership lock exists. STOP and preserve the whole real memit-gdrive-backup* history. Under-lock refusals must leave existing bytes unchanged.
3. Recovery succeeds but counter/state/archive fields/population differ from §2.2's observed-barrier expectation; any unexpected live log-root file, or preserved-byte hash mismatch. No expectation of an archived leaked receipt on the empty branch.
4. false green: status exit 0 before a sequenced completion above the observed barrier, including §2.4.
5. First-run failure: open nonzero; receipt exit nonzero/75 or error_number non-null; failure journal; failed backup launch/failed backup/token or auth error/dry-run or skipped operations/unacknowledged launch generation/newer heartbeat publication failed/stale incomplete/malformed status; Operation not permitted; HEARTBEAT-FAILED or FATAL in wrapper log. A cleanly terminated transfer failure can reopen only through the diagnosed operator-approved successor branch, never silent retry.
6. No Allow prompt with no wrapper start within a few minutes, or applet alive with no sync child. Capture full ps, pmset -g assertions and logs before any owner-approved termination.
7. Exit 0 with warnings: fresh backup with warnings is insufficient even if explained. Require subsequent clean completion and successful content check; retirement stays blocked.
8. launchd bootstrap failure, disabled new job, missing observed successor, non-clean/nonzero successor status or non-benign launchd log. Never assume a fixed generation.
9. Any content discrepancy/missing/error/unreadable/unchecked object, incomplete/missing report, nonzero check exit, inventory drift or failed verifier. Files changed after initial start receive no waiver. Pause/catch-up/check again only after diagnosis and the required GO.
10. Native fixture/PID clearance incomplete, ps unavailable, assertion absent, source unmounted, missing GO/Allow, lost-history ambiguity or unexpected remote data → STOP.

This plan grants no permission by itself. MAESTRO obtains each marked GO at its point of effect; an earlier existing authorization for the same exact action remains valid. No MB40 plan execution occurred.

## r12 erratum — only rows touched by findings 1–3

| v2 line | v3 line | Original row or insertion |
|---|---|---|
| 1 | 1 | # Drive r11 activation plan v2 — operator/MAESTRO execution only |
| 16 | 16 | R="$W/results/backup_gdrive_host_20261011/r11_package_20261011T005440Z" |
| 30 | 30 | 0.1 [READ-ONLY]. Check current pins and the seven-file deployment scope. STOP on any mismatch. Source must match the reviewed pin set after merge too. Preserve the old 33-line pin file; pins_v2.json records its supersession and full test-hash lineage. The current status-tool pin is 903c471febc52131313e39d6ae7aac80ad3c2cda93310543b293522fe420fb46. |
| 34 | 34 | capture pin-preflight /usr/bin/shasum -a 256 -c "$R/pins_v2.sha256" |
| 41 | 43 | 0.2 [MAESTRO GO]. Run host_commands.sh's individual commands at niceness 0 (do not execute the activation plan). Exact 22-case coverage must give 22 pass, no skips/failures/errors, isolated config positive controls, identical real inventories and no owned groups left. E RED must be the two absent-parent UNSET subcases; E GREEN includes native fixture artifact assertions. Four local→local check fixtures must meet their named expectations. The frozen suite must give 155 run, 14 real-rclone skips, zero failures/errors and cleared groups; its five skipped Archive cases remain UNVERIFIED and are not activation dependencies. The full suite does not replace the 22-case run. Submit locked-release change + this evidence to Astra r11; NO-GO keeps all subsequent gates closed. |
| 43 | 45 | Hostfix1 coverage/fixture semantics: every corrected host action is UNRUN and uses the fresh r11_hostfix1_* labels in host_commands.md. Evidence remains in R; the runner owns a fresh /private/tmp/drive_r11_<label>_*/ runtime containing HOME/fixtures/TMPDIR outside the memit source volume. Before any coverage/fixture test, saved df -P outputs resolve source and runtime paths to mount points; diskutil info -plist must establish APFSPhysicalStores on disjoint physical whole disks. Unknown/shared physical identity means STOP. ParentWholeDisk alone is insufficient. Recorded host topology is memit virtual disk6 over physical disk4s3 and /System/Volumes/Data virtual disk3 over physical disk0s2; another partition of disk4 is still rejected. Replay GREEN does not replace the live placement/config positive control or the exact 22 host tests. The verifier treats log severity at the line prefix; DEBUG argv mentions of report --error/error.txt are not transfer errors, while real error/read/unchecked/report failures remain fatal. Raw logs are preserved. |
| 45 | 47 | 0.3 [READ-ONLY]. Publish pins_v2 only after evidence/review changes settle, preserving the old pin set. No built-bundle hash can exist before §1.2. Re-run the pin check after any authorized package update, and re-review changed inputs. |
| 71 (insert before) | 73-84 | scope / executable rows |
| 73 | 87 | capture pr-create /usr/bin/gh pr create --base master --head worktree-c10k-route-a --title 'Google Drive backup release and activation evidence' --body-file "$R/pr_body.md" |
| 92 | 106 | All exits 0, merged SHA saved, post-merge master CI green, no conflict. Before the shared-main update MAESTRO verifies it is clean and reserved. Reject current commit unless all seven deployment inputs match pins_v2; MERGED_SHA comes from the guarded merge result, not an unchecked command substitution. |
| 96 | 110 | capture deployment-bytes /usr/bin/python3 -B -c 'import hashlib,json,pathlib,sys; root=pathlib.Path(sys.argv[1]); pins=json.loads(pathlib.Path(sys.argv[2]).read_text()); files=[x for x in pins["files"] if x["path"] in ("tools/backup_gdrive.sh","tools/backup_gdrive_status.py","tools/backup_mirror.excludes","tools/launchd/MemitGdriveBackup.applescript","tools/launchd/build_gdrive_applet.sh","tools/launchd/stage_gdrive_release.sh","tools/launchd/com.rhu.memit-gdrive-backup.plist")]; assert len(files)==7; [print(x["path"],hashlib.sha256((root/x["path"]).read_bytes()).hexdigest()) for x in files]; assert all(hashlib.sha256((root/x["path"]).read_bytes()).hexdigest()==x["sha256"] for x in files)' "$M" "$R/pins_v2.json" |
| 115 | 129 | capture release-manifest /usr/bin/python3 -B -c 'import hashlib,json,pathlib,sys; d=pathlib.Path(sys.argv[1]); pins=json.loads(pathlib.Path(sys.argv[2]).read_text()); expected={pathlib.Path(x["path"]).name:x["sha256"] for x in pins["files"] if x["path"] in ("tools/backup_gdrive.sh","tools/backup_gdrive_status.py","tools/backup_mirror.excludes")}; assert set(x.name for x in d.iterdir())==set(expected).union({"MANIFEST"}); [print(n,hashlib.sha256((d/n).read_bytes()).hexdigest()) for n in expected]; assert all(hashlib.sha256((d/n).read_bytes()).hexdigest()==h for n,h in expected.items()); assert (d/"MANIFEST").read_text()=="".join(h+"  "+n+"\n" for n,h in expected.items())' "$D" "$R/pins_v2.json" |
| 137 | 151 | Every compare exits 0. MAESTRO records/commits the build manifest and build-time pins. Plist pin is 702868b81899f9f5624e9931af4586321dfccce3a46dda895d4ce6f9659cedce, excludes pin 45bb4e2a2e4629d494b6e5ccf41dd6885133b27e329a197fc6a85bcc55e48f3f; builder/stage/app-source pins are in pins_v2.json. |
| 276 | 290 | capture full-check /usr/bin/caffeinate -i -s /opt/homebrew/bin/rclone check "$SRC" "$DST" --one-way --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links --combined "$C/combined.txt" --differ "$C/differ.txt" --missing-on-dst "$C/missing-on-dst.txt" --error "$C/error.txt" --log-file "$C/check.log" --log-level DEBUG --stats 0 --retries 1 |
| 297 | 311 | capture full-check-download /usr/bin/caffeinate -i -s /opt/homebrew/bin/rclone check "$SRC" "$DST" --one-way --exclude-from "$D/backup_mirror.excludes" --exclude '**/.git/objects/**/tmp_obj_*' --exclude '**/.git/objects/tmp_obj_*' --exclude '/.git/objects/**/tmp_obj_*' --exclude '/.git/objects/tmp_obj_*' --links --combined "$CD/combined.txt" --differ "$CD/differ.txt" --missing-on-dst "$CD/missing-on-dst.txt" --error "$CD/error.txt" --log-file "$CD/check.log" --log-level DEBUG --stats 0 --retries 1 --download |
