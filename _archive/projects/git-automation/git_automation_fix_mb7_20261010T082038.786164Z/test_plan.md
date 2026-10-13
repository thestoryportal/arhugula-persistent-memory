# MB7 test-first plan

Authority: MAESTRO5 brief and `results/git_automation_build_20261010T064202.457112Z/astra_binding_verdict.md`, findings 1–2. This is model-free infrastructure work protecting the F1 research evidence and CI path. Findings 3–6 do not authorize expanded scope.

Before implementation, execute and save RED for every new or revised regression:

1. Clean eligible worktrees remain on disk and in the worktree inventory after apply; manual-removal candidates include path, branch, inspected head SHA, and positive size. Both local and remote attached branches remain. A second apply has no actions. Recorded production commands contain no worktree removal or pruning.
2. In a real temporary repo, inject an ignored packet after the second completed inspection of the eligible worktree (the old code's final removal inspection). It must survive apply. With removal disabled, the second inspection is the final overall inspection. Assert the writer fired and no later inspection of this worktree happened.
3. At the same boundary, detach and make a real empty commit. Apply must retain the worktree and make the new commit reachable from its HEAD/reflog.
4. Flip CI to PENDING inside ready(), or to FAIL/PENDING/ABSENT/another head after the final hygiene inventory. No merge dispatch is permitted; report a pre-merge refusal and merged=false.
5. Advance real master inside merge dispatch, after the final stable() read. The resulting merge's first parent differs from the recorded base. Report merged=true, merge_sha, and merged-on-moved-base failure; never ok=true.
6. Post-merge CI failure, bounded timeout, master movement, unavailable parent evidence, and failed post-hygiene each retain merged=true and the exact merge SHA with a distinct post-merge failure status. The CLI also reports the merged outcome.
7. Execute the commit-parent adapter against documented GitHub JSON; wrong-SHA, missing or malformed parent evidence refuses.
8. Patch os.stat with a result lacking st_birthtime and run both run_rows() and the complete legacy render() path, including log sorting and completed-run duration. Native-birthtime subtests check unchanged macOS duration behavior.

Acceptance commands (raw foreground system Python, bytecode disabled):

```sh
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest discover -s tests -p test_git_automation.py -v
LLMDB_ROOT=$PWD /usr/bin/python3 -B -S -m unittest -v tools.test_c10w_p2_gate tools.test_dashboard_live tools.test_dashboard_gpu_detector
```

TMPDIR will be exported to this receipt's fixtures directory, so all fixture mutations and cleanup stay inside receipts. Production code changes wait until RED is persisted. Ubuntu/Python 3.11 and live GitHub merge behavior remain UNVERIFIED; merging awaits Astra GO.
