# Independent D-C10u-mint2 HALT review — model: GPT-6 (Codex); effort: high

**PROCEED — keep the unchanged `frozen` stage running and retain the false-HALT record.** The saved reproduction marker is byte-for-byte correct; its comparison fails because four tuples become JSON lists. The known-baseline gate independently passes. **Correction to the program's forecast: no recurrence is expected at the normal successful ends of the later scheduled stages.** Empty blocks and pending replication are different from partially populated blocks.

Review scope: the requested read-only review, with only this report written. Offline checks used Python `-B`, the model-free reader/driver, and existing synthetic fixture constructors; no model, tokenizer, torch, GPU job, server, stage command, or process-control operation was invoked. All 74 source hashes in the saved run identity were revalidated against this worktree. This is a review of a C10 write-path diagnostic serving F1, not an experiment verdict or an F1 closure (`docs/C10U_MINT2_PREREG.md:9–11`, `:111`).

## 1. Diagnosis: confirmed, with a precise persistence caveat

`experiments/track_c/c10u_mint2_arms.py:45–54` serializes the object, exclusively creates the file, closes it, reads it back, and then checks both text equality and parsed-object equality. `experiments/track_c/c10u_mint2_read.py:386–402` builds `missing` as a sorted **list of tuples**, with both tuple elements converted to strings. The incomplete-population return exposes that list in `block_reading` at `:455–456`.

I reconstructed the exact original marker object from the three saved `F_r0_mint1_s{0,1,2}.json` records, using the frozen `block_reading` for F and V2 and retaining the marker's saved identity, stage and timestamp. Results:

| Offline observation | Result |
|---|---|
| Saved marker | `results/c10u_mint2/reproduce_complete.json`, 10,194 bytes |
| SHA-256 | `f70d5b362792143c72b5618e4ddb4c74bbf358958f73a5f8a4f1b1e6c8718618` |
| Saved bytes equal reconstructed UTF-8 payload, including newline | **True** |
| Parsed saved JSON equals original in-memory object | **False** |
| Parsed saved JSON equals JSON-normalized original object | **True** |
| Recursive differences | **Exactly four tuple → list differences; no scalar or key differences** |
| Nonfinite floats / non-string dictionary keys / other unsupported values | **None** |

The four differences are `$.readings.F.missing[0..3]`: `('modifier', '0')`, `('modifier', '1')`, `('modifier', '2')`, and `('multi', 'None')` become corresponding lists. The saved entries are at `results/c10u_mint2/reproduce_complete.json:101–118`. Its `replication_missing` is empty (`:119`); V2 is entirely empty and returns no missing-population fields (`:121–128`). This mismatch alone necessarily triggers the reported exception.

I considered three explanations: non-JSON-native structure; numeric/encoding changes; and an actual persistence/readback failure. The first is both necessary and sufficient for this reconstructed comparison. `allow_nan=False` rejects NaN/infinity during serialization, before the output is opened (`arms.py:48–50`), rather than producing this post-write RuntimeError. No finite float changed value in the recursive comparison, and every dictionary key was already a string. The exact UTF-8 byte comparison rules out an encoding/newline discrepancy or currently truncated/changed payload. Unsupported objects or decode errors would raise elsewhere; neither occurred here.

**Caveat kept explicit:** the original immediate readback buffer was not saved, so this offline check cannot exclude an unrelated transient filesystem discrepancy at that instant or guarantee future durability. The writer also has no `fsync` (`arms.py:45–54`). Nevertheless, a filesystem fault is unnecessary to explain the observed HALT, and the current saved bytes fully validate. This review establishes a deterministic false positive, not a general filesystem-health claim.

The diagnostic identifies only the final marker comparison: `architecture_profile/c10u_mint2_halt_diagnostic.json:95–98` traces `main:1102` → `stages:1031` → `write_json:54`. The three behavior jobs completed before the HALT, and the stage returned 1 (`results/c10u_mint2_logs/reproduce.log:3–9`).

Reproducible offline comparison, from this worktree root; it performs no writes:

```python
# Run with python3 -B; imports are model-free.
import json, sys
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root / "experiments/track_c"))
import c10u_mint2_read as R

out = root / "results/c10u_mint2"
actual = (out / "reproduce_complete.json").read_bytes()
saved = json.loads(actual.decode("utf-8"))
records = [json.loads((out / f"F_r0_mint1_s{s}.json").read_text())
           for s in (0, 1, 2)]
obj = {**saved, "readings": {
    b: R.block_reading([r for r in records if r["block"] == b])
    for b in ("F", "V2")}}
payload = json.dumps(obj, indent=2, allow_nan=False, ensure_ascii=False) + "\n"
assert actual == payload.encode("utf-8")
assert json.loads(actual) != obj
assert json.loads(actual) == json.loads(payload)
gate = R.reproduction_gate(records)
assert gate == json.loads((root / "results/c10u_mint2_logs/"
                          "reproduce_law3_gate.json").read_text())
assert gate["ok"]
```

## 2. Continuing to `frozen`: sound under the frozen criteria

The binding reproduction requirement is median ≥ 30 and seed windows {0:[32,56], 1:[24,44], 2:[26,46]}, followed by the frozen multi reference's three envelopes (`docs/C10U_MINT2_PREREG.md:76–78`; LAW#3 itself: `CLAUDE.md:30`). The unchanged reader recomputed **40, 36, 41; median 40; `ok=True`; no reasons; `multi_checked=False`**, exactly matching `results/c10u_mint2_logs/reproduce_law3_gate.json:1–11`. Each of the three saved runs independently returned no `run_validity` errors. This check also verifies same-block material and distinct processes, not just counts (`experiments/track_c/c10u_mint2_read.py:361–383`).

**The multi-reference gate remains owed.** `frozen` runs multi before modifiers (`read.py`'s actual file: `experiments/track_c/c10u_mint2_read.py:536`); the driver checks its envelope immediately after that job, before dispatching a modifier (`experiments/track_c/c10u_mint2_arms.py:1018–1025`). A real miss still halts both blocks. Proceeding does not treat the missing multi result as a pass.

| Downstream consumer | Actual dependency and gate |
|---|---|
| `frozen` | Re-reads raw records and re-runs `reproduction_or_halt` **before its permanent started marker** (`arms.py:979–983`, `:1013–1014`); no previous completion-marker input. |
| `v2`, `control`, `replicate-V2`, `p4-save` | Require the frozen mint-1/multi reproduction gate and seven original F records (`arms.py:984–987`). Conditional plans/eligibility are checked before their markers (`:988–991`). |
| `replicate-F` | Requires the original F reproduction including multi, and its complete valid initial population/replication trigger (`arms.py:984–988`; `read.py:540–550`). Checks reproduced F mint-1 and multi again during the fresh block (`arms.py:1022–1025`). |
| Controls and replication routing | Derived from initial raw populations, frozen direction rules and replication need (`experiments/track_c/c10u_mint2_read.py:531–550`), not marker success or diagnostic absence. |
| P4 save | Selects only replicated advanced configurations from original/replica records, replays them, rechecks the replay, and writes per-configuration admission records (`arms.py:934–976`). |
| P4 compiled-artifact chain | Reads its admission/original/replay records, checks source/artifact hashes and replicated advancement (`experiments/track_c/c10u_mint2_p4_probe.py:96–126`); writes its separately checked P4 verdict (`:171–177`). |
| Reader | Accepts only filenames matching the F/V2 individual-run regex, then reconstructs block readings (`experiments/track_c/c10u_mint2_read.py:633–655`). Completion/started markers and the architecture-profile diagnostic are excluded. |
| CORPUS verdict | No C10u CORPUS entry exists at review time. The prescribed future verdict uses the frozen readings, applicable replication/control/P4 gates and close-out, with this exception disclosed (`docs/C10U_MINT2_PREREG.md:78`, `:86`, `:90–107`, `:115–119`). No prerequisite demands that `reproduce_complete.json` came from a non-raising call. An unwritten future verdict cannot be independently verified now. |

Here `arms.py` and `read.py` in the table abbreviate the two full `experiments/track_c/c10u_mint2_*.py` paths cited above. `read_records` itself filters out stage markers (`arms.py:871–873`), and the output-collision checks concern **the current stage's** paths (`:993–1013`). Diagnostic existence is consulted only to choose a fresh diagnostic filename on another HALT (`:63–74`); it is not a later-stage blocking condition. Existing identity loading revalidates pinned sources and the LAW#3 reference (`:135–148`), and main performs its preflight before dispatch (`:1078–1102`). My read-only hash comparison found all 74 pinned sources unchanged.

Precision correction: the saved `frozen_started.json:125` timestamps the marker at **2026-10-07 11:06:34.315945 UTC**, rather than the brief's approximate 11:10. This does not change the gate analysis.

## 3. Recurrence: absent at normal later stage ends; possible with leftover partial populations

The decisive distinction is `block_reading([])` returning immediately without a `missing` field (`experiments/track_c/c10u_mint2_read.py:438–441`), versus a **nonempty, otherwise valid incomplete** population returning the tuple-bearing fields (`:449–456`). `PENDING-REPLICATION` also contains no tuple-bearing missing list when no replica has started (`:504–505`). Therefore the broad expectation in `SESSION_CHECKPOINT.md:7` needs narrowing:

| Marker, on the normal serial schedule | Population at marker time | Same tuple false positive? |
|---|---|---|
| `reproduce_complete.json` | F has only mint-1 ×3: 3/7, four missing entries. V2 empty. | **Yes; observed.** |
| `frozen_complete.json` | F 7/7; V2 empty, not partially populated. | **No.** |
| `v2_complete.json` | Original F and V2 each 7/7; unstarted replicas absent. | **No.** |
| `control_complete.json`, if needed | Both original blocks complete; all three controls finished. | **No.** |
| `replicate-F_complete.json`, if needed | F original and fresh populations each 7/7; V2 original complete, or still entirely empty if F replication is scheduled earlier. | **No.** |
| `replicate-V2_complete.json`, if needed | V2 original and fresh populations each 7/7; F original complete; any F replica either absent or complete. | **No.** |
| `p4-save_complete.json`, if eligible | Both original blocks complete; selected configurations have required replicas; save replays are outside the raw-run regex. | **No.** |

The plans come from `experiments/track_c/c10u_mint2_read.py:526–550`; all planned jobs finish before both block readings and the stage-end write (`experiments/track_c/c10u_mint2_arms.py:1015–1031`). Optional explicit `step0_*_complete.json` markers contain descriptors rather than block readings (`:1035–1057`), so this specific defect is absent there too.

I checked these seven population shapes offline with the existing, individually valid synthetic records (`experiments/track_c/c10u_mint2_selftest.py:23–110`). JSON round-trip equality was false only for `reproduce`, and true for all six normal later stage-end shapes. These are **schema checks, not predictions of scientific labels or pass outcomes**.

**Yes, `replication_missing` carries tuples too** whenever a nonempty valid replica is incomplete: it is exactly `b["missing"]` from the same `_population` function (`read.py:402`, `:450`, `:455–456`). A leftover partially written V2 original or F/V2 replica can therefore make **any subsequently reached stage-end marker** fail, since the driver includes both blocks in every marker (`arms.py:1026–1031`). Positive controls confirmed both cases: F complete plus only V2 multi failed round-trip equality through six V2 `missing` tuples; complete original blocks plus only F replica multi failed through six F `replication_missing` tuples. Neither is the clean serial schedule. Invalid populations take the earlier INVALID return (`read.py:452–454`), so even "every partial block always triggers this" is too broad.

At the specific final-marker exception, **no already persisted science data are deleted and no preceding dispatch/reproduction gate is skipped**. Individual results are written before their validity checks and child return (`arms.py:852–868`); the stage-end read/write occurs after the child loop (`:1018–1031`). The exclusively created completion file also remains on disk after the comparison raises (`:45–54`). What is lost is the final console print and normal zero return (`:1032`, `:1103–1105`). A gate requiring genuinely missing runs remains unevaluated/INCOMPLETE and must not be claimed passed.

The nonzero status can still stop an external command chain. The actual one-stage wrapper propagates it (`/Users/robertrhu/.claude/jobs/4d71207f/tmp/run_c10u_stage.sh:11–14`). Re-running the same stage would hit occupied paths before dispatch (`arms.py:993–1014`); do not delete or overwrite markers to retry it. None of this makes another failure safe to ignore.

## 4. Recommendation

**PROCEED.** Continue the already running unchanged `frozen` stage under its existing gates. Preserve the reproduction marker, diagnostic, exit status and this review as the explanation for this one narrowly established bookkeeping failure. Correct the later-stage recurrence expectation: no routine recurrence is predicted; a recurrence warrants checking for a partial initial/replica population or a different failure before any continuation. Any genuine reproduction, source-identity, child-job, admission, validity or P4 failure retains its existing HALT/gating consequence. The final experimental verdict and CORPUS close-out remain outstanding.
