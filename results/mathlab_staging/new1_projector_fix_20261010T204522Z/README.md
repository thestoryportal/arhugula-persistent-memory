# NEW1 projector fix — MB26 build receipt

The build acceptance contract is satisfied. The deterministic regression is **construction-contract evidence; full-worker recovery remains unverified.**

Receipt directory: `results/mathlab_staging/new1_projector_fix_20261010T204522Z/`.

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; branch: `worktree-c10k-route-a`.

Authority: `results/mathlab_staging/new1_construction_diag_astra_r8.md:28–47`, Q3, `VERDICT: BRANCH-1-FIX`.

## Change and regression

`native_projector` now performs two independent gathers from the same native U with the same allowed indices, then multiplies the first gather by the transpose of the second. The only production-source diff is the two-line replacement inside this function. Normalization, decompositions, masks, execution order outside this construction, thresholds, `tensor_sha`, and `projector_matches` are unchanged.

The new `test_native_projector_uses_two_independent_native_gathers` directly calls production `native_projector` with a fixed, nonempty 4×4 CPU fp32 U and indices `[3, 1]`. Its observers delegate indexing to the original `Tensor.__getitem__` and multiplication to the original `Tensor.__matmul__`. They retain the actual tensors rather than fabricate operation results. Assertions require two gathers from that exact U with the same index object; unchanged index values, native values and dtype; independent matmul operand storage; and right-hand values equal to the left transpose. The result must equal an independently evaluated two-gather reference byte-for-byte and pass the unchanged capture gate with the reference SHA and matching count.

No matrix search or rounding-inequality discriminator is used. RED and RED-again both fail specifically at `len(gathers) == 2`, with `AssertionError: 1 != 2 : native projector must gather twice from native U`.

All 34 pre-existing tests are unchanged and pass in GREEN. The existing count-mismatch and SHA-success controls in `test_native_parity_is_retained_when_float64_excluded_energy_is_large`, and the four-probe fallback/failing-probe controls in `test_projector_matches_all_four_frozen_probes_and_update_parity`, remain intact.

The acceptance contract remains exactly **matching count AND (matching SHA OR all four probe relative errors <= 1e-6)**.

## Start and final SHA-256

Both supplied start pins were verified before the first edit, and again when creating this receipt. [start.sha256](start.sha256) and [final.sha256](final.sha256) contain the recorded hashes.

| Changed file | Start SHA-256 | Final SHA-256 |
| --- | --- | --- |
| `tools/new1_geometry.py` | `018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e` | `ce43a26d24fb9cd0e2a2ff4d4ddd63bdd7de9ff4d2349b017f77914a31271f77` |
| `tests/test_new1_geometry.py` | `57afd2504c9ce065e85be5e5d4237122bea3e329324ff557775cea9e9faa260f` | `dba1606f9938498d1469fcfc69cbf3f7d320c2aa3ed3834e7cd2a12a47931e3d` |

The pinned originals are preserved as [new1_geometry.before.py](new1_geometry.before.py) and [test_new1_geometry.before.py](test_new1_geometry.before.py). The GREEN source is preserved as [new1_geometry.green.py](new1_geometry.green.py).

## Behavioral evidence

This exact command ran once per log, three invocations total, from the verified worktree root. Each log contains raw stdout and stderr:

```sh
LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest -v tests.test_new1_geometry
```

| Moment | Log path | Exit | Total | Passed | Failed | Errors / skipped | Suite time |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RED, new test against unchanged production source | [results/mathlab_staging/new1_projector_fix_20261010T204522Z/RED.log](RED.log) | 1 | 35 | 34 | 1 | 0 / 0 | 1.141 s |
| GREEN, corrected production source | [results/mathlab_staging/new1_projector_fix_20261010T204522Z/GREEN.log](GREEN.log) | 0 | 35 | 35 | 0 | 0 / 0 | 0.577 s |
| RED-again, temporarily reverted to original `Q@Q.T` source | [results/mathlab_staging/new1_projector_fix_20261010T204522Z/RED-again.log](RED-again.log) | 1 | 35 | 34 | 1 | 0 / 0 | 0.609 s |

| Moment | `tools/new1_geometry.py` SHA-256 immediately before the run | Hash / exit receipts |
| --- | --- | --- |
| RED | `018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e` | [RED.sha256](RED.sha256), [RED.exit](RED.exit) |
| GREEN | `ce43a26d24fb9cd0e2a2ff4d4ddd63bdd7de9ff4d2349b017f77914a31271f77` | [GREEN.sha256](GREEN.sha256), [GREEN.exit](GREEN.exit) |
| RED-again | `018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e` | [RED-again.sha256](RED-again.sha256), [RED-again.exit](RED-again.exit) |

The test-file SHA is `dba1606f9938498d1469fcfc69cbf3f7d320c2aa3ed3834e7cd2a12a47931e3d` for all three runs. After RED-again the fix was restored. `cmp` verified that final production source equals `new1_geometry.green.py` byte-for-byte, and that `final.sha256` equals `GREEN.sha256`. Final source and tests therefore have the exact hashes exercised by the saved 35/35 GREEN run. No fourth suite invocation was made.

## Final production-source diff

```diff
diff --git a/tools/new1_geometry.py b/tools/new1_geometry.py
index 2328810..4642c79 100644
--- a/tools/new1_geometry.py
+++ b/tools/new1_geometry.py
@@ -198,8 +198,8 @@ def covariance_basis(C,k=1024,cell=None):
 
 
 def native_projector(basis):
-    Q=basis['native']['Q'][:,basis['native']['allowed']]
-    return Q@Q.T
+    U=basis['native']['Q']; allowed=basis['native']['allowed']
+    return U[:,allowed]@U[:,allowed].T
 
 
 def geometry_energies(Z,basis):
```

## Scope and review handoff

MB26 writes are confined to `tools/new1_geometry.py` inside `native_projector`, one new method in `tests/test_new1_geometry.py`, and this fresh receipt directory. The source/test diff was inspected: exactly one production hunk and one insertion-only test hunk. No producer, identity diagnostic, construction diagnostic, engine, dashboard or MB27 supervisor files were edited by MB26. MB27's concurrent work was left alone. No real model, covariance, capture or GPU run, deletion, commit, push, merge or PR mutation was performed.

The fix is restored, with no half-applied changes or tests in flight. MAESTRO24 can verify the host evidence and hand the build to GPT-6-Astra for review. Full-worker recovery, real capture agreement and scientific outcomes remain UNVERIFIED.

Binding context directive for every successor: watch `Context N% left`. Start a new piece of work only at 60% left or more. At 40% left or less, stop starting work, append a handoff here with completed and half-applied work, exact paths and SHA-256 of changed files, failing tests and exact commands, open risks and next step, then reply exactly `CONTEXT HANDOFF WRITTEN`. If `Context compacted` appears, do this immediately. Never approach full-window compaction; restate this directive in every handoff.
