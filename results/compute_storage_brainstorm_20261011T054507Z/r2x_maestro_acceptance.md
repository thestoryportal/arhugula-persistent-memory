# R2X acceptance re-run by MAESTRO59 (2026-10-11 22:16Z)

Builder codexr2x replied `R2X FIX READY` at 66% context (22:10:48Z), with `r2x_report.md` written. MAESTRO59 reran every check from its own shell on these subject bytes. The script is reproduced at the end.

- Subject sha256, recomputed: F11 044a0ce9…, J10 5a5d7c45…, K10 ce61568c…, P8 1c607ec7…, I10 d7028444…, test-first record 418f7e29…, report 5bf5e437…. The five subjects match `r2x_report.md`. F11 pins J10, P8 and I10 (each full hash found once in F11).
- Inputs and sources: after the builder's reply, `git status --short` over B, `experiments/` and `tools/c10w_p2_gate.py` shows no modified tracked file. Every input (F10, J9, K9, P7, I9, C, V12, D16f, D15f, D14f, D13f, D9, D8) and source equals HEAD.
- Acceptance 1: `/usr/bin/python3 -B B/check_r2_schemas_v10.py`, exit 0.
- Acceptance 2 and 3 ran under `/usr/bin/sandbox-exec -p '(version 1)(allow default)(deny file-write*)'`, both exit 0. Positive control first: the same profile refused a Python file write into B (PermissionError, Errno 1), and no file appeared.
- Acceptance 3 ran a second time under the stricter profile that also denies `process-exec` of both Git binaries, `.venv/bin/python` and its resolved uv target. Exit 0, with the same 59 RED lines (identical by `diff`). Positive controls under that profile: child `/usr/bin/git` and child `.venv/bin/python` refused (PermissionError), child `shasum` ran (rc 0), file write into B refused with no file left. The R11B/R12A/R12B/R13B/R13C probes are therefore mocked, not real process starts.
- My GREEN/RED lines for acceptance 2 and 3 are identical by `diff` to the builder's receipts `r2x_acceptance_profiles.md` and `r2x_mutation_output.md`.
- Acceptance 2 key lines: D16 expected science families checked for 55 science profiles, independent of children; D15 ADMISSION count pinned_constant=37 loaded_data=6, operand-source pinned_literal=24 loaded_data=19; SCIENCE count 234/55, operand-source 109/180; D13 trace 13 recorded queries, 43 admission-origin occurrences (unchanged from round 12).
- Census (scope per D16f "Census scope"): the builder's readable census over B and $TMPDIR shows 0 files and 0 directories created, OS-denied macOS subtrees listed as unverified (`r2x_census.json`). The host-level proof is this run: `find B $TMPDIR -newer <mark>` after all runs lists only `$TMPDIR/` and macOS-owned `TemporaryItems` directories, the same as round 12. No file appeared in B.
- Mutation controls: 59 distinct RED lines (56 preserved + 3 D16: R13A verifier missing for profile 19; R13B replication missing for profile 4, P1 evaluator; R13C replication missing for profile 5, P2 evaluator).

These are presence and recomputation checks. MAESTRO did not judge the D16 reachability classification, the replication refusals or the source-prefix expectation rule; that is Astra's round 13.

Script:
```
#!/bin/zsh
W=/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a
B=$W/results/compute_storage_brainstorm_20261011T054507Z
O=${0:h}/r2x_accept_out; rm -rf $O; mkdir -p $O
K=$B/check_r2_schemas_v10.py; P=$B/science_launch_profiles_v8.json
W1='(version 1)(allow default)(deny file-write*)'
W2='(version 1)(allow default)(deny file-write*)(deny process-exec (literal "/usr/bin/git") (literal "/Library/Developer/CommandLineTools/usr/bin/git") (literal "'$W'/.venv/bin/python") (literal "/Users/robertrhu/.local/share/uv/python/cpython-3.11.16-macos-aarch64-none/bin/python3.11"))'
cd $W
touch $O/mark; sleep 1
echo "A1"; /usr/bin/python3 -B $K > $O/a1.txt 2>&1; echo "A1 rc=$?"
echo "PC1 deny-write"; /usr/bin/sandbox-exec -p "$W1" /usr/bin/python3 -B -c "open('$B/__pc_probe','w')" > $O/pc1.txt 2>&1; echo "PC1 rc=$? exists=$([[ -e $B/__pc_probe ]] && echo YES || echo no)"; tail -1 $O/pc1.txt
echo "A2 deny-write"; /usr/bin/sandbox-exec -p "$W1" /usr/bin/python3 -B $K --profiles $P > $O/a2.txt 2>&1; echo "A2 rc=$?"
echo "A3 deny-write"; /usr/bin/sandbox-exec -p "$W1" /usr/bin/python3 -B $K --mutation-controls > $O/a3.txt 2>&1; echo "A3 rc=$?"
echo "PC2 strict"; for c in /usr/bin/git $W/.venv/bin/python; do /usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B -c "import subprocess,sys; subprocess.run(['$c','--version'])" > $O/pc2.txt 2>&1; echo "  $c rc=$? $(tail -1 $O/pc2.txt)"; done
/usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B -c "import subprocess; print(subprocess.run(['shasum','-a','256','$K'],capture_output=True).returncode)" > $O/pc2s.txt 2>&1; echo "  shasum child rc=$(cat $O/pc2s.txt)"
/usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B -c "open('$B/__pc_probe','w')" > $O/pc2w.txt 2>&1; echo "  write rc=$? exists=$([[ -e $B/__pc_probe ]] && echo YES || echo no) $(tail -1 $O/pc2w.txt)"
echo "A3 strict"; /usr/bin/sandbox-exec -p "$W2" /usr/bin/python3 -B $K --mutation-controls > $O/a3s.txt 2>&1; echo "A3s rc=$?"
diff <(grep '^RED' $O/a3.txt) <(grep '^RED' $O/a3s.txt) > /dev/null && echo "RED identical" || echo "RED DIFFER"
echo "RED count a3=$(grep -c '^RED' $O/a3.txt) distinct=$(grep '^RED' $O/a3.txt | sort -u | wc -l | tr -d ' ')"
grep -E 'mocked|R13A|R13B|R13C' $O/a3s.txt | cut -c1-200 | head -6
echo "CENSUS"; find $B $TMPDIR -newer $O/mark 2>/dev/null | grep -v "^${O:h}" | head -20
echo DONE
```
