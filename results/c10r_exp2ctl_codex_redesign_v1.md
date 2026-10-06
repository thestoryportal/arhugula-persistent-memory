Reviewer: gpt-6.1-sol (max effort), Codex CLI 0.160.1

Recommend **(b), one weight-1 common-position control**, for this one-slot budget. Replace the preserve-key locations while keeping their counts, inputs, forward calls, coefficient, and solve fixed. The baseline identity evidence makes (a) mainly a valuable implementation check; (c) primarily checks whether the historical winner repeats. Neither is as discriminating about the necessity of value-token locations. This is a proposed design, not a revised driver or a run authorization. The scientific scope remains the write/compile candidate, with no C10 or F1 closure (`docs/C10R_EXP2_ZEROPRESERVE_PREREG.md:9,38`; source contrast `fd16592:edit.py:64,72` / `92acd03:edit.py:94-104`; budget supplied in `/Users/robertrhu/.claude/jobs/4d71207f/tmp/codex_exp2ctl_redesign_packet.md:8,15`).

## 1. Verification

Citation definitions: `SB` means `/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10`. `fd16592:<file>:<line>` and `92acd03:<file>:<line>` are immutable Git objects read from SB, not its later working tree. `E08` = `results/autoresearch_c10_equivalence_2026-10-06T0815.json`; `E11` = `results/autoresearch_c10_equivalence.json`; `B` = `SB/runs/20261006-131156_nocommit/score.json`; `V` = `SB/runs/20261006-142644_nocommit/score.json`. `RR` and `RUN` mean the current `experiments/track_c/autoresearch_c10/replay_exp2/read_replay.py` and `run_replay.sh`; `ADV` = `results/c10r_exp2ctl_advisor_v1.md`. JSON citations below give actual keys and exact values in these files. `check_equivalence.py` names `experiments/track_c/autoresearch_c10/check_equivalence.py`; `BRIEF` names `/Users/robertrhu/.claude/jobs/4d71207f/tmp/codex_exp2ctl_redesign_packet.md`. Engine paths are program-worktree files; the recipe snapshots are pinned Git objects.

**Yes: all nine recorded hashes match.** I parsed the three files and compared their complete `saved_sha256` dictionaries, rather than comparing the advisor's prefixes. Each table cell is the exact value of `<column>:saved_sha256.<row>`:

| Arm/key | E08 | E11 | B |
| --- | --- | --- | --- |
| `A1_single` | `2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1` | `2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1` | `2f72fee29064643ce2214e7d644f88a71292e56c35ab657b3b3d355405cbaab1` |
| `A2_coherent2` | `f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56` | `f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56` | `f94e1be2258482a84201432aec35f88c59f25e7b9d325345a447a108e0e2dd56` |
| `A7_coined_coined` | `c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965` | `c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965` | `c30664a92b06be43485a2043b4512d08d977df2708289f558d5ba03a5a7da965` |

Both equivalence records have `verdict="PASS"`, `projectors_equal=true`, `scorer_exit=0`, and `recipe.<each arm>.bitwise_equal=true`. Their direct tensor comparison uses `torch.equal`, including equal changed-name lists (`experiments/track_c/autoresearch_c10/check_equivalence.py:22,25-36`). Thus the recorded evidence includes direct harness-versus-baseline tensor equality, as well as equal serialized artifacts across the three records. It does not include a zero-weight experiment-2 replay.

The starts are `E08:started="2026-10-06 08:15:43"` and `E11:started="2026-10-06 11:46:53"`. The baseline edit source hash is the same in both: `source_sha256.edit.py="0d03bf68549cc8a9fb3f725850222a31ad8fc822e7df5e69e9d50cc3c4cfb0f7"`, which I independently recomputed from `fd16592:edit.py:1-87`. The preparation hashes differ: `E08:source_sha256.prepare.py="5260f46d6b4008d5c6cdf6c356672d6eb79fbee923885da4f6827f1e16008385"`, versus `E11:source_sha256.prepare.py="8e577d546080f06bbd25a685e9af03016117d1e133ff9ff97aa92e5ac22f21f1"`; the latter matches both pinned commits' preparation source (`fd16592:prepare.py:1-312`; `92acd03:prepare.py:1-312`). This is evidence of reproducibility across these recorded contexts, not a universal guarantee for all future GPU calculations.

Both equivalence records contain 27 `scorer_vs_run_recipe` comparisons and every third element is `true`; for example `A7_coined_coined.para_full_n=[7,7,true]`, `A7_coined_coined.para_first_n=[40,40,true]`, and `A7_coined_coined.generic_ppl_post=[21.506,21.506,true]`. The comparison covers exactly the fields enumerated in `check_equivalence.py:58-61`, not every possible model behavior. Both have `templates_sha_this_process="e8605172dce0"`, `templates_sha_scorer="e8605172dce0"`, and `seed_reproduces_templates=true`.

**What weight zero restores.** The baseline creates a fresh CPU zero cache for each call and never reads its accumulated values during that call's writes:

```python
# fd16592:edit.py:64
cache = [torch.zeros(P[0].shape[0], P[0].shape[0]) for _ in LAYERS]
# fd16592:edit.py:72-74
A = P[i] @ (Kf @ Kf.T + cache[i]) + RIDGE * torch.eye(Kf.shape[0])
B = P[i] @ Kf @ rf.T
upd = upd_matrix_match_shape(torch.linalg.solve(A, B).T.float(), WEIGHTS[layer].shape)
```

The cache accumulation occurs only after all writes (`fd16592:edit.py:77-79`), with no subsequent consumer before return. Experiment 2 uses:

```python
# 92acd03:edit.py:97-99
A = P[i] @ (Kf @ Kf.T + PRESERVE_WEIGHT * Kp @ Kp.T) + RIDGE * torch.eye(Kf.shape[0])
B = P[i] @ Kf @ rf.T
upd = upd_matrix_match_shape(torch.linalg.solve(A, B).T.float(), WEIGHTS[layer].shape)
```

**I-INFER:** with coefficient zero, finite `Kp`, and identical `P,Kf,rf` and numeric execution, the added matrix is zero and the solve has the baseline operands and operation sequence. Python's left-associative `*`/`@` expression scales `Kp` before multiplying by `Kp.T`; it is not an independently evaluated overflowing Gram matrix multiplied by zero. The baseline cache is float32 CPU zero storage, matching this solve's CPU float32 operands (`fd16592:edit.py:64,71-74`; `92acd03:edit.py:75,96-99`). The expected result is bit identity, not a ±4 behavioral band.

However, **empirical bit identity of the complete zero-weight run is UNVERIFIABLE in this read-only task**. Experiment 2 additionally computes `gap0`, value-key forwards, overlap/leak diagnostics, and the final residual; its body is not the baseline body (`92acd03:edit.py:60-76,86-106` versus `fd16592:edit.py:58-79`). The shared model is in evaluation mode (`92acd03:c10e_bandknob.py:48`), and no new sampling call appears in those added operations, supporting the inertness prediction. A finite-key check and actual output identity remain the correct way to test that prediction.

An important precision: `saved_sha256` hashes each `<arm>.pt` file's bytes, not a canonical whole-model tensor stream (`92acd03:prepare.py:259-261`). Equal file hashes are strong evidence of identical saved tensors under the recorded serialization. A file-hash mismatch is not, by itself, proof that tensors differ; first exclude a serialization or manifest difference. The saved files are removed at `prepare.py:295`; re-reading the historical tensors themselves here is **UNVERIFIABLE**.

The relevant baseline outcomes are exact: `B:summary.heldout_full=7`, `canon=7`, `first_token=40`, `A1=69`, `A2=69`, `dw_total=88.974`, `guards="ok"`, `seed=0`, `edit_budget=2700`. The winner is `V:summary.heldout_full=18`, `canon=24`, `first_token=35`, `A1=69`, `A2=69`, `dw_total=131.421`, `guards="ok"`. Its saved hashes, useful for option (c), are:

| V JSON key | Exact value |
| --- | --- |
| `saved_sha256.A1_single` | `fd24387467284a225f663248671c26c956ed65df7fa4e131b781b406bbb3b882` |
| `saved_sha256.A2_coherent2` | `0edc1e365d8469d858023e9fe48aa677e7a53294846c9ced0a7d3cac00f442ac` |
| `saved_sha256.A7_coined_coined` | `5b43681d14fb68254315845738a1936e6145108e6f7bdba057e0dcb5e4ee2f1b` |

**Historical-source caveat kept explicit:** both `B:edits.commit="nocommit"` and `V:edits.commit="nocommit"`. The ledger associates `fd16592\t7\t89.0` and `92acd03\t18\t131.4` with the two recipes (`SB/results.tsv:2,4`), but does not record the executed source hash. Therefore exact execution of `92acd03` in V is **UNVERIFIABLE**. Any one-run historical contrast below is conditional on that mapping; none silently supplies a contemporaneous weight-1 replication (`92acd03:prepare.py:194-221,292-293`).

## 2. Ruling within one edit/scorer slot

**I-INFER — hypotheses to distinguish:** H-location: the value-key locations are necessary for the recorded gain; H-geometry: a nonspecific preserve Gram matrix or changed update geometry/norm is sufficient; H-record: source/runtime drift or an unanchored historical record explains some of the contrast. These are hypotheses, not findings. Their basis is the zero-versus-value-key equations, the source caveat above, and the observed update-size change (`fd16592:edit.py:72`; `92acd03:edit.py:97`; `V:edits.commit="nocommit"`; `B:summary.dw_total=88.974`; `V:summary.dw_total=131.421`).

The historical winner used `V:summary.edit_seconds=2011.0` and `score_seconds=862.0`: 2873 seconds = 47.88 minutes, excluding any unmeasured overhead. All three proposed runs fit the user's single-slot framing by estimate; their actual runtimes are **UNVERIFIABLE**. Option (b) preserves the original number and length of value-key forwards, so it does not require another full edit or another scorer (`92acd03:edit.py:66-76`; `92acd03:prepare.py:201-225`). No second GPU run is hidden in the recommendation.

| Single run | Outcome and what it shows | What it does not show |
| --- | --- | --- |
| **(a) Weight 0, baseline bit-identity gate** | All three baseline file hashes match, with exact 7 and 88.974: the instrumented zero-term path reproduced the saved baseline. This validates the predicted numerical inertness of retained extras on this stack, conditional on serialization and unchanged base/evaluator. | It does not separate value-token preservation from nonspecific regularization or update size; zero deletes every preserve direction. It does not source-anchor the historical 18 leg. |
| (a), hashes match but count/norm differs | Inconsistent scoring/base-model/reporting or artifact association; INVALID/HALT. Matching edited artifacts alone is not enough to accept a changed result. | Not evidence for a preserve mechanism; the result must be diagnosed. |
| (a), a hash differs, any count including 7 or 18 | Identity expectation failed; HALT and investigate changed tensors versus serialization/configuration. Descriptive count only; no band-based SUPPORTS label. | Count 7 does not prove inertness. Count 18 does not cleanly refute the term while the implementation/environment identity gate has failed. |
| **(b) Weight 1, count-matched common-prefix keys** | At least 18 total hits without using value-token keys is a counterexample to their necessity for attaining the recorded total; reproducing at least 13 collision hits makes that counterexample match the targeted subgroup too. Guards and norm qualify the interpretation as specified in §3. | Not proof that the real term is an artifact, nor proof that update norm alone or “regularization” is the cause. Different key locations change the Gram matrix's direction, spectrum, and magnitude. |
| (b), at most 7 total hits | The chosen non-value control retains no gain above the recorded baseline. With no collision recovery, clean guards, and an update at least as large as the recorded winner, it supports a location-sensitive candidate and rejects simple norm sufficiency for this chosen control. | A weaker update or damaged control leaves a magnitude/quality confound; even a large clean update does not establish the proposed head-trigger mechanism or prove that every other key placement fails. |
| (b), 8–17 total hits, or conflicting total/collision results | A partial historical gain or a subgroup tradeoff. Report the exact pattern; the value-location necessity claim remains only partly tested. | No dose response, no calibrated process-noise interpretation, and no definitive mechanistic attribution. |
| **(c) Science-unmodified 92acd03 with provenance logging** | The three V hashes, 18, and 131.421 all repeat: source-anchored replication of the recorded winner on this stack. This is the best run if verifying the historical winner is the main objective. | No ablation: it cannot distinguish the location mechanism from generic preserve geometry/norm. |
| (c), different hashes but gain repeats | Source-anchored behavioral improvement, without bit replication. Inspect artifacts, contexts, base/configuration, and serialization; a different count has no inherited ±4 allowance. | Does not validate exact historical identity or isolate value-key specificity. |
| (c), 7 or another loss of the historical gain | The winner did not reproduce under the anchored conditions. Halt promotion and report a reproduction failure. | Does not tell whether value-key preservation is intrinsically ineffective, the old source mapping was wrong, or the stack changed. |
| Any run, validity/launch gate fails or incomplete result | INVALID/HALT; diagnostic data only. | No mechanism label. |

These are **proposed interpretations**, grounded in the cited source equations and B/V endpoints, not outcomes of executed runs. Recommendation: **(b)** tests H-location directly while leaving the coefficient present. Keep (a) as the right later identity diagnostic and (c) as the right later source-replication diagnostic, rather than silently scheduling either within this budget. If unconditional causal attribution to the historical 7 → 18 contrast is required, one unreplicated historical positive plus a new control cannot deliver it; that requirement remains **UNVERIFIABLE** within the one-slot design.

## 3. Buildable replacement spec, proposed for freezing before implementation/run

### 3.1 Exact positions and inputs

Start from detached `92acd03` in a new standalone clone. Keep `PRESERVE_WEIGHT=1.0`, layers `[4,5,6,7,8]`, every hyperparameter, subject/target construction, target solve, residual calculation, solve, cast, and weight-update order unchanged. The **only science change** is which positions the existing forward hook gathers into `Kp`; provenance and readout additions must be separately identifiable in the exact allowed diff (`92acd03:edit.py:25-33,60-104`). Do not edit the engine or fixed preparation/harness files (`CLAUDE.md:32`; `92acd03:prepare.py:63-76`).

Use the same input as real `value_keys` for every arm, fact, template, and layer:

1. `tgt = tok(rq["target_new"]["str"], add_special_tokens=False)["input_ids"]`.
2. `prefix = t.format(rq["prompt"].format(rq["subject"]))`, with `t` traversed in the original flattened `ctx` order.
3. `ids = tok(prefix)["input_ids"]`.
4. Run **exactly** `model(torch.tensor([ids + tgt], device=DEV))`, with the same down-projection input hook, once per fact/template/layer.
5. The real positions are `range(len(ids), len(ids)+len(tgt))`. The control positions are the prefix positions below. No suffix is appended, no target is changed, no extra model forward is needed.

These input/token conventions are the actual original helper (`92acd03:edit.py:66-76`), including the target's leading space from `92acd03:c10e_bandknob.py:96-97`. Apply the control to **all three arms**, not just A7; changing only A7 would introduce another design difference (`92acd03:prepare.py:96,201-209`).

The canonical training template is exactly `"The capital of {} is the city of"` (`92acd03:c10e_bandknob.py:51`). Inside that canonical portion of each wrapped prefix, define seven candidate **word occurrences**, in this order:

```text
C[0] = The
C[1] = capital
C[2] = of       (before the subject)
C[3] = is       (after the subject)
C[4] = the
C[5] = city
C[6] = of       (at the end of the canonical prompt)
```

Each occurrence maps to its one actual token index using the **loaded tokenizer's offset mapping on the full wrapped prefix**. Find character spans from the literal portions of `rq["prompt"].split("{}")`; shift them by the template's literal prefix length and the subject length. A qualifying token's non-whitespace character span must equal that word's span exactly. Ignore zero-length/special-token offsets. Require exactly one qualifying token for each of the seven occurrences, identical token IDs to the original `tok(prefix)` call, and no overlap with the subject or appended target. This chooses positions inside ordinary canonical words, including the two separate “of” occurrences; it selects neither generated preamble words nor any part of a coined value. Do not use token-ID exclusion as a substitute for position exclusion: the rule concerns where the input token occurs.

For zero-based fact index `f` in the fixed request order, zero-based flattened template index `q`, and `m=len(tgt)`, gather:

```python
start = (f + q) % 7
indices = [C[(start + j) % 7] for j in range(m)]
```

This is a **design choice**, independent of any success flags, optimizer, model activations, or RNG. The cyclic start distributes the chosen common words over facts/templates. Require `1 <= m <= 7` and `len(set(indices)) == m`; HALT on shortage or failed offset mapping. No duplicate positions, fallback, sampling-with-replacement, new prompts, reweighting, or tuning after observing a score.

After the original forward, gather `grabbed[0][indices].float().cpu()` rather than `grabbed[0][len(ids):].float().cpu()`; concatenate blocks in the original fact/template order and transpose exactly as the existing helper does (`92acd03:edit.py:65-76`). **Do not use `get_reprs_at_idxs` with a list of positions:** it averages an index list into one representation (`memit_dry_run/memit/rome/repr_tools.py:129-134`), which would destroy the required number of Kp columns. The existing hook already exposes each token separately.

The original value-position block can also be read from that same captured activation for audit-only counts/key-norm diagnostics; it must not enter the control solve. Mark the unchanged overlap/leak formulas as `Kp_source=common_canonical_prefix` so their labels remain honest (`92acd03:edit.py:100-102`). Inside the actual recipe, obtain subjects/values from `requests`; never read historical score files or held-out prompts to make this selection (`92acd03:prepare.py:67-76,101-108`).

**Count matching is exact per fact, per template, per layer, and per arm.** Real Kp has m columns per fact/template; the control gathers m distinct columns from the same forward. The cached context list contains six flattened templates, shown in `results/autoresearch_c10_equivalence_rerun.log:25` and `results/autoresearch_c10_equivalence.log:24`, consistent with `memit_dry_run/memit/memit/memit_main.py:304-323`. Therefore each fact contributes `6*m` columns per layer. Its control count equals its real count, regardless of the token lengths of other facts.

The expected context list is shown here to make the prompt rule self-contained. It is an **acceptance anchor**, not a list to inject in place of the engine's original sampling (`results/autoresearch_c10_equivalence_rerun.log:25`; `memit_dry_run/memit/memit/memit_main.py:304-323`):

```python
ctx = [
    ["{}"],
    [
        "The following is a single-choice question from a Chinese. {}",
        "Therefore, the number of ways to choose the remaining. {}",
        "Because the number of students in the class is not. {}",
        "I am trying to use the [CouchDB. {}",
        "You are an AI assistant that follows instruction extremely well. {}",
    ],
]
```

For A7, the following m values are the exact `V:arms.A7_coined_coined.rows[i].ntok` values, with row subjects/values quoted from those rows. Counts in the final column are derived as 6*m, not measured GPU outputs:

| i | Subject → value | m | Real and control columns per layer |
| --- | --- | ---: | ---: |
| 0 | Zorbland → Vindex Vask | 4 | 24 |
| 1 | Quaxil → Drennik Brakk | 5 | 30 |
| 2 | Plurnak → Vythorn Stavik | 6 | 36 |
| 3 | Vythorn → Vorlex Yornel | 5 | 30 |
| 4 | Glimsto → Lurmax Spraxil | 6 | 36 |
| 5 | Drennik → Kessivar Ulvenn | 6 | 36 |
| 6 | Yastovel → Halquin Cindel | 5 | 30 |
| 7 | Crulpane → Marsduq Drelth | 6 | 36 |
| 8 | Mophgar → Glimsto Vask | 5 | 30 |
| 9 | Brinduun → Brindu Brakk | 5 | 30 |
| 10 | Trannak → Fluvane Stavik | 6 | 36 |
| 11 | Skornwell → Yastov Yornel | 6 | 36 |
| 12 | Fluvane → Vindex Spraxil | 5 | 30 |
| 13 | Oxbarrow → Drennik Ulvenn | 6 | 36 |
| 14 | Zephquin → Vythorn Cindel | 6 | 36 |
| 15 | Lurmaxen → Vorlex Drelth | 5 | 30 |
| 16 | Pradnoll → Lurmax Vask | 5 | 30 |
| 17 | Kessivar → Kessivar Brakk | 5 | 30 |
| 18 | Wombryne → Halquin Stavik | 5 | 30 |
| 19 | Halquin → Marsduq Yornel | 6 | 36 |
| 20 | Vorlex → Glimsto Spraxil | 6 | 36 |
| 21 | Quenby → Brindu Ulvenn | 6 | 36 |
| 22 | Marsduq → Fluvane Cindel | 6 | 36 |
| 23 | Thelby → Yastov Drelth | 6 | 36 |

A1 has `V:arms.A1_single.rows[*].ntok=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]`; A2 has `V:arms.A2_coherent2.rows[*].ntok=[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]`. The resulting required real/control counts are:

| Arm | Sum of target token counts | Columns per layer | Across five layers |
| --- | ---: | ---: | ---: |
| A1_single | 24 | 144 | 720 |
| A2_coherent2 | 48 | 288 | 1440 |
| A7_coined_coined | 132 | 792 | 3960 |
| All arms combined | 204 | 1224 | 6120 |

The arithmetic uses the preceding JSON lengths, six logged contexts, and the five layers in `92acd03:edit.py:25`. These column counts do not mean another model forward per column: the original helper obtains all selected positions from one captured activation for a fact/template (`92acd03:edit.py:65-76`).

The bare-template Zorbland example has prefix `"The capital of Zorbland is the city of"`; the control candidates are `[0,1,2,6,7,8,9]`, m=4, start=0, chosen indices `[0,1,2,6]` = The/capital/of/is. I checked this and every fact/template on the cached tokenizer only. The snapshot tokenizer path is `hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/tokenizer.json`; its JSON has `model.type="BPE"` and `post_processor={"type":"ByteLevel","add_prefix_space":false,"trim_offsets":false,"use_regex":false}`. The concrete check below is reproducible read-only evidence for the index/count rule; it does not establish runtime hidden-state geometry.

### 3.2 Norm reporting and what remains unmatched

Retain the fixed scorer's **exact** `dw_total`: the sum of per-changed-tensor Frobenius norms of float32 `w[n]-_BASE[n]`, rounded to three decimals. It is not the single Frobenius norm of a concatenated whole-model update, nor a direct activation-energy metric (`92acd03:prepare.py:273,289`).

Report the control's `summary.dw_total`, all three `arms.<arm>.dw_total`, `D-88.974`, `D-131.421`, `D/88.974`, and `D/131.421`, beside total/collision/other hits and all guards. The reference increase is 42.447, or approximately 47.706% (`B:summary.dw_total=88.974`; `V:summary.dw_total=131.421`). For diagnostic comparison, log each layer's actual float32 update norm before the fp16 weight cast and the actual and control Kp column counts, sum of squared column norms, and `||P[i] @ Kp||_F` for both key sets. Mark these as different quantities from the scorer's installed-weight norm (`92acd03:edit.py:99,104`; `92acd03:prepare.py:273`).

**Proposed reporting bins**, based only on those two recorded norms: `D <= 88.974`; `88.974 < D < 131.421`; `D >= 131.421`. These are descriptive reference comparisons, not noise bands or validity gates. Do not tune the weight, rescale Kp columns, or rescale the update to fit a norm band: that would add a second science intervention to the weight-1 location control.

**I-INFER:** a ≥18 result at D≤88.974 counters “a larger sum-of-norms is necessary” as well as value-location necessity for this count. A ≤7 result at D≥131.421 counters “a sum-of-norms at least as large is sufficient” for this chosen control. Other combinations leave magnitude as an explanation. Even equal `dw_total` does not match update direction, per-layer allocation, or Kp Gram spectrum: counts and coefficient are matched, not geometry (`92acd03:edit.py:94-104`; norm definition `92acd03:prepare.py:273`). This caveat prevents treating a low common-position score as a universal proof of collision-head preservation.

### 3.3 Exact proposed readings and the noise question

Let H = control `summary.heldout_full` /72. Let C be the sum of `para_full_hits` over the sixteen facts whose value head is in `{Drennik,Vythorn,Vorlex,Kessivar,Halquin,Marsduq,Glimsto,Fluvane}`; O is the other eight facts' sum. Verify H=C+O, with C in [0,48] and O in [0,24]. This subgroup definition follows the actual subject/value collisions (`92acd03:c10e_bandknob.py:57-61,229-249`; `results/autoresearch_c10_exp2_codex_review.md:37-48`). The historical sums are C_B=0, O_B=7, C_V=13, O_V=5, derived from `B/V:arms.A7_coined_coined.rows[*].para_full_hits` using those exact heads; H_B=7 and H_V=18 are their summary values.

**PROPOSED primary count labels, only after validity passes:**

| Exact H condition | Label | Justification |
| --- | --- | --- |
| 0 ≤ H ≤ 7 | `NO-BASELINE-EXCEEDING-GAIN` | At or below the verified baseline endpoint, `B:summary.heldout_full=7`. |
| 8 ≤ H ≤ 17 | `PARTIAL-RECORDED-GAIN` | Above 7, but below `V:summary.heldout_full=18`; describes retaining 1–10 of the historical 11 extra hits. |
| 18 ≤ H ≤ 72 | `FULL-RECORDED-GAIN-WITHOUT-VALUE-POSITIONS` | Reaches/exceeds the recorded winner endpoint without gathering value-token keys. |

**PROPOSED secondary collision labels:**

| Exact C condition | Label |
| --- | --- |
| C = 0 | `NO-COLLISION-RECOVERY` |
| 1 ≤ C ≤ 12 | `PARTIAL-COLLISION-RECOVERY` |
| 13 ≤ C ≤ 48 | `FULL-RECORDED-COLLISION-RECOVERY` |

These endpoints are the exact subgroup baseline and winner sums just cited. Print every fact's hit vector and O as well; total success can move to another group.

**PROPOSED interpretation, kept separate from the mechanical labels:**

- H≥18, C≥13, and every fixed guard passes: a clean counterexample to value-token positions being necessary to reproduce this recorded total and collision gain, conditional on the historical-source premise. It leaves the nonspecific geometry/norm explanation open.
- H≥18 but C<13: a counterexample for the total count, with the original collision explanation unresolved; do not claim its targeted pattern repeated.
- H≤7, C=0, every guard passes, and D≥131.421: this chosen alternative fails despite a sum-of-norms at least as large as the winner. The location-sensitive candidate survives this falsifier; its proposed causal head-trigger mechanism is still **UNVERIFIABLE**.
- H≤7 with a smaller D, or any loss of guard quality: weaker-update or damaged-control confounds remain. Do not award a mechanistic SUPPORTS label.
- Intermediate H, or a positive C gain offset by falling O: partial/mixed result, not dose response and not noise. Report it without a binary mechanism conclusion.

All interpretation rows use the same source endpoints and fixed guards (`B/V:summary.heldout_full=7/18`, `summary.dw_total=88.974/131.421`; `92acd03:prepare.py:42-52`). For locality failures that are not instrument-validity failures, retain the raw count label plus `quality=DEGRADED`, report the exact failing guards, and withhold a **clean** mechanism/usable-win conclusion. Such a failure never turns H≥18 into support for value-location necessity. This consciously separates count necessity from safe/usable improvement; the existing prereg also reports locality guards beside its count (`docs/C10R_EXP2_ZEROPRESERVE_PREREG.md:32,34`).

**No ±4 allowance is justified for either contrast here.** The baseline records exhibit exact equality, whereas the older ±4–5 discussion explicitly concerns separately sampled process contexts (`E08/E11/B:saved_sha256`, full values in §1; `CORPUS/50_C10Q_STACKED_SOLVE.md:30`). In (b), different weights are intentional: identity to B or V is neither required nor expected as a validity gate. A baseline's exact repetition does not estimate the process variance of a different solve. Cross-process numerical variance for this specific common-position algorithm is **UNVERIFIABLE until it is actually repeated**. Thus the above thresholds are descriptive, prechosen endpoint comparisons, not confidence intervals, a measured stochastic envelope, significance cutoffs, or permission to call 8–11 “baseline noise.” No probability calculation treats the three paraphrases per fact as independent samples (`92acd03:c10e_bandknob.py:358-399`).

### 3.4 Validity and launch gates, including advisor issues 2, 3, 4, and 9

The following are **proposed mandatory gates for the replacement**, not changes made to the current prereg. Any instrument/provenance/schema gate failure yields INVALID/HALT, exit 2, and no binding count/mechanism label. Optional count-only diagnostics remain explicitly NON-BINDING, preserving the operator's strict-fixture treatment implemented at `RR:164-177,188-192`.

1. **Frozen source and independent checkout.** Require full HEAD `92acd0378d23f4935df9a8bccc0137b36695a40f`, independent clone objects, fixed evaluator bytes, and the exact implementation-approved patch: weight stays 1; only the selector/gather changes scientifically; logging is isolated. Record and verify the executed edit hash and pre-launch diff hash before/after the run. Freeze their actual computed values when the replacement is built, before any GPU launch; their future byte hashes are **UNVERIFIABLE in this design-only task**. Existing checks to retain are `RR:65-89`, adapting `expected_edit` rather than retaining its weight-zero replacement (`RR:41-55`).

2. **Engine fingerprint before any model dispatch — issue 3.** Run the standard-library fingerprint script with `LLMDB_ROOT=PROGRAM_ROOT` explicitly and the pinned program interpreter; require exit 0 and its nonempty, expected output before the MPS preflight/edit. The tool imports only standard-library modules, uses the env root, and checks both the engine SHA and three covariance sites (`tools/engine_fingerprint.py:24-43`; obligation `CLAUDE.md:28`). Save the complete output and print the scorer's exact `gates.fingerprint`, not just a boolean. Require the scorer's fixed LAW#5 and scope gates true (`92acd03:prepare.py:135-163,242-244,262-266`). The current RUN lacks the pre-dispatch fingerprint (`RUN:12-46`); a later scorer failure cannot refund edit time.

3. **Edit-time template identity — issue 2.** Require exactly three provenance records, one each for the fixed arm order, with arm identifiers `A1_single,A2_coherent2,A7_coined_coined` (`92acd03:prepare.py:96,201-209`). Require every full context hash to equal:
   `e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330`.
   This full SHA was computed from the actual list printed in `results/autoresearch_c10_equivalence_rerun.log:25`, using the same `json.dumps(ctx).encode()` serialization as `92acd03:prepare.py:163`; the list also appears in `results/autoresearch_c10_equivalence.log:24`. Require identical lists/hashes across arms, full-list rehash integrity, six flattened templates, and scorer `gates.templates_sha="e8605172dce0"`. Preserve the immediate-after-template print and run-local records (`RR:24-37`). This is an external realized-list anchor, stronger than rehashing only each record's own list (`RR:117-121`).

4. **Count/position/primitive gates.** Require the counts in §3.1 at every layer, m distinct prefix indices per fact/template, exactly the seven allowed word occurrences, matching original prefix IDs, no target/subject index, and finite gathered keys/updates. Save a manifest of arm/fact/template/input IDs and selected indices; it must be identical across layers, except for activations. Demonstrate the unchanged capture primitive's identity mode: on the same captured forward, gather the original target range by explicit indices and require bit equality to the original suffix slice before trusting the alternate indices. This costs no additional model run. Do not mistake the fixed harness LAW#5 for validation of the deliberately different candidate solve: it tests `H.my_edit` (`92acd03:prepare.py:149-155`; `92acd03:c10e_bandknob.py:415-444`), while primitive isolation is required by `CLAUDE.md:32`.

5. **Exclusive GPU window — issue 4.** Require the operator's paused-loop/no-relaunch window for the whole edit/scorer pair; this is a launch precondition, not an action authorized here (`docs/C10R_EXP2_ZEROPRESERVE_PREREG.md:19,22-23`; `BRIEF:14-15`). Inspect the complete process list before dispatch, after preflight, and during the run; reject other Python/model/notebook jobs, including `edit.py`, `prepare.py`, `check_equivalence.py`, `c10*` stage/harness drivers, `ipykernel/jupyter`, `ollama`, and the loop's `safe-mode` session. Include interpreter invocations such as `python`, `Python`, and `.venv/bin/python`; do not depend solely on a script's basename. Identify/exclude only the runner's exact own process chain and, after launch, its recorded child/scorer PIDs. Log full matches and fail on probe errors, not just positive matches. This fixes the current four-name pattern (`RUN:12`; the equivalence checker itself loads a model at `check_equivalence.py:14-16`; the imported harness does at `92acd03:c10e_bandknob.py:45-48`). A regex/snapshot cannot enforce “nobody launches later”; if the operator cannot maintain exclusive ownership, the launch remains GATED. MPS availability must pass before edit; do not allocate another model as a preflight (`RUN:39-44`).

6. **Fixed score metadata and controls — issue 9.** Require `seed=0`, `edit_budget=2700`, and `edits.commit="92acd03"` in the replacement's score; these are what the fixed seeded clone emits (`92acd03:prepare.py:35-36,194,220-221,292-293`). Require exactly the three arm keys and changed-name sets restricted to the five written down-projection weights at layers 4–8, legal dimensions/counts, and all mandatory fields. Require `summary.law5_ok=true`, `summary.scope_ok=true`, and integer A1/A2 each in **[68,72]**, the fixed control floor plus the physical /72 ceiling (`92acd03:prepare.py:43-44`; `92acd03:c10e_bandknob.py:399`). This replacement deliberately does not impose exact 69 or the old arbitrary upper cap 71: unlike (a), it changes these arms' weights legitimately. Compare/report the fixed 69 references instead (`B/V:summary.A1=69`, `summary.A2=69`). Leave the existing zero-control prereg untouched.

7. **Complete fresh run and score/provenance association — issue 9.** A new clone/invocation must begin without prior run outputs; refuse reuse. Make an invocation ID with OS entropy, independent of torch's seeded RNG, before dispatch; record it, the expected source/diff/context hashes, destination, and child identity in the launch manifest. Each arm's provenance record includes that invocation ID, actual arm, and canonical absolute run_dir obtained from the fixed evaluator's caller frame (`RR:35-37`; `92acd03:prepare.py:195,201-209`). After child exit, require exit 0, exactly one fresh completed run directory, exactly one score.json, the three complete matching records, and the fixed scorer fields. Before invoking the reader, write a runner receipt binding this invocation/run path, the full score-file SHA, executed source hash, all three `saved_sha256` values, and the successful child exit code. Invoke the reader on that exact score and receipt, then append the reader's actual exit code to the receipt and preserve it in `run.rc`; the reader never gates on its own future exit status. Print the exact score path and propagate the reader's status. Parse rather than silently choosing “latest.” No score/failed scorer/partial provenance is INVALID, exit 2, with a precise reason (`92acd03:prepare.py:222-225,292-295`; current `RUN:46-51`).
   
   **Scope of the receipt:** this detects accidental stale/cross-run association under a trusted runner; it is not cryptographic proof against an owner who fabricates the entire directory. Reject explicitly synthetic fixtures for live acceptance; use them only for reader self-tests. Because (b) has intentionally new weights, compare its recorded hashes for consistency and print them, but never require equality to the B/V hashes. The current synthetic test intentionally demonstrates that source provenance plus copied score numbers can satisfy structural gates (`results/c10r_exp2ctl_codex_impl_v1.md:322-392`; current association logic `RR:102-128`).

8. **Malformed-input behavior — issue 9.** Require 24 exact registered subject/value rows per arm, nonempty string values, exactly three boolean hit flags per row, and the correct 16/8 partition with sums matching arm/summary counts. Validate types before indexing/splitting, and turn missing fields, malformed JSON, empty values, and indexing errors into INVALID/HALT, exit 2. The current `RR:153-154` may index an empty split, while `RR:199-204` does not catch `IndexError`; that gap must close. Reject booleans as integer counts and nonfinite reported numbers. Check the reader's boundary and invalid-input paths before any GPU dispatch.

9. **Fidelity manifest and quality report.** Capture the interpreter's resolved path, package versions without importing models, OS version, hparams/screens, engine support sources, tokenizer/model revision, and relevant cache identities before/after execution; abort if pinned inputs change during the run. The actual program harness uses a fixed revision default `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b` (`92acd03:c10e_bandknob.py:25-26,45-48`), and refuses inherited model/root-affecting knobs through preparation (`92acd03:prepare.py:55-60`). Historical model/cache/config byte identity is **UNVERIFIABLE** because those old score records do not contain such a manifest. Do not use mtimes or matching edited-subset hashes to claim otherwise. Print and recompute every fixed guard from its exact thresholds (`92acd03:prepare.py:42-52,289-291`), plus the per-fact vectors, first-token/canonical counts, all norms, and template/source hashes. Failed locality guards are reported as DEGRADED per §3.3, not swallowed.

### 3.5 Read-only position-rule verification

The following command exercised only a cached tokenizer, JSON/log parsing, and deterministic index selection. It did **not** import transformers or torch, run a model, or execute any recipe/replay/fence script. It checks the proposed indices twice per input and compares target lengths with the recorded `V:arms.<arm>.rows[i].ntok`. Full-context anchoring comes from the cited log; no model generation was needed.

```bash
/opt/homebrew/bin/rtk proxy .venv/bin/python -B - <<'PY'
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from tokenizers import Tokenizer

log = Path('results/autoresearch_c10_equivalence_rerun.log')
line_no, line = next((i, s) for i, s in enumerate(log.read_bytes().decode().split('\n'), 1) if s.startswith('Cached context templates '))
ctx = ast.literal_eval(line[len('Cached context templates '):])
ctx_sha = hashlib.sha256(json.dumps(ctx).encode()).hexdigest()
print(f'Context source: {log}:{line_no}')
print('edit_context_templates_sha256:', ctx_sha)
assert ctx_sha.startswith('e8605172dce0')
flat = [t for group in ctx for t in group]
assert len(flat) == 6
path = Path('hf_cache/hub/models--Qwen--Qwen2.5-3B/snapshots/3aab1f1954e9cc14eb9509a215f9e5ca08227a9b/tokenizer.json')
tok = Tokenizer.from_file(str(path))
score = json.loads(Path('/Volumes/memit/llm-database-poc-mirror/autoresearch_sandbox_c10/runs/20261006-142644_nocommit/score.json').read_text())
canon = 'The capital of {} is the city of'
before, after = canon.split('{}')

def select(subject, value, template, fact_i, template_i):
    lead, tail = template.split('{}')
    prefix = template.format(canon.format(subject))
    e = tok.encode(prefix, add_special_tokens=True)
    spans = [(m.group(), len(lead) + m.start(), len(lead) + m.end()) for m in re.finditer(r'\S+', before)]
    spans += [(m.group(), len(lead) + len(before) + len(subject) + m.start(), len(lead) + len(before) + len(subject) + m.end()) for m in re.finditer(r'\S+', after)]
    candidates = []
    for word, word_a, word_b in spans:
        matching = []
        for idx, (a, b) in enumerate(e.offsets):
            piece = prefix[a:b]
            aa = a + len(piece) - len(piece.lstrip())
            bb = b - len(piece) + len(piece.rstrip())
            if (aa, bb) == (word_a, word_b) and piece.strip() == word:
                matching.append(idx)
        assert len(matching) == 1, (subject, template, word, matching)
        candidates.append(matching[0])
    assert len(candidates) == 7
    target = tok.encode(' ' + value, add_special_tokens=False).ids
    m = len(target)
    assert 1 <= m <= 7
    start = (fact_i + template_i) % 7
    chosen = [candidates[(start + j) % 7] for j in range(m)]
    assert len(set(chosen)) == m
    assert all(0 <= idx < len(e.ids) for idx in chosen)
    return e.ids, target, candidates, chosen, [prefix[slice(*e.offsets[idx])].strip() for idx in chosen]

counts = {}
checks = 0
for arm, data in score['arms'].items():
    columns = 0
    lengths = []
    for fact_i, row in enumerate(data['rows']):
        lengths.append(row['ntok'])
        for template_i, template in enumerate(flat):
            result = select(row['subj'], row['val'], template, fact_i, template_i)
            assert result == select(row['subj'], row['val'], template, fact_i, template_i)
            assert len(result[1]) == row['ntok']
            columns += len(result[3])
            checks += 1
    counts[arm] = columns
    print(f'{arm}: facts=24 templates=6 sum_target_tokens={sum(lengths)} Kp_columns_per_layer={columns} Kp_columns_all_5_layers={5 * columns}')
example = score['arms']['A7_coined_coined']['rows'][0]
_, target, candidates, chosen, words = select(example['subj'], example['val'], flat[0], 0, 0)
print('Identity-template example: subject=' + example['subj'] + ' value=' + example['val'])
print('Candidates:', candidates)
print('Selected:', chosen, 'words=', words, 'target_token_count=', len(target))
print('Fact/template checks:', checks)
print('All-arm Kp columns per layer:', sum(counts.values()))
print('All-arm Kp columns across five layers:', 5 * sum(counts.values()))
assert counts == {'A1_single': 144, 'A2_coherent2': 288, 'A7_coined_coined': 792}
assert 'torch' not in sys.modules and 'transformers' not in sys.modules
print('PASS: deterministic distinct common-word prefix positions, exactly count-matched; tokenizer only, no model or torch import.')
PY
```

Captured output verbatim:

```text
Context source: results/autoresearch_c10_equivalence_rerun.log:25
edit_context_templates_sha256: e8605172dce01aaafbf3f23a4d68d05dde756a9b65ec9060962fedc1369fb330
A1_single: facts=24 templates=6 sum_target_tokens=24 Kp_columns_per_layer=144 Kp_columns_all_5_layers=720
A2_coherent2: facts=24 templates=6 sum_target_tokens=48 Kp_columns_per_layer=288 Kp_columns_all_5_layers=1440
A7_coined_coined: facts=24 templates=6 sum_target_tokens=132 Kp_columns_per_layer=792 Kp_columns_all_5_layers=3960
Identity-template example: subject=Zorbland value=Vindex Vask
Candidates: [0, 1, 2, 6, 7, 8, 9]
Selected: [0, 1, 2, 6] words= ['The', 'capital', 'of', 'is'] target_token_count= 4
Fact/template checks: 432
All-arm Kp columns per layer: 1224
All-arm Kp columns across five layers: 6120
PASS: deterministic distinct common-word prefix positions, exactly count-matched; tokenizer only, no model or torch import.
```

Exit code: `0`. This establishes token/count feasibility for the pinned cached tokenizer and recorded stimuli. Loaded-model execution, hidden-state key norms, the control's weights/count/norm, and its own repeated-process variance remain **UNVERIFIABLE** until the separately authorized run.

## 4. Disagreements and qualifications to the advisor

1. **GPU priority.** I accept the exact-identity correction for (a), but disagree that (a) should consume this only slot and the location control be a second slot. The weight-zero equation already predicts the saved baseline, while the location control tests the competing necessity claim. This is an information/budget judgment, not new evidence (`ADV:28,34,38,99-104`; `fd16592:edit.py:64,72`; `92acd03:edit.py:97`; `BRIEF:8`).

2. **“Bitwise” is an expectation to verify, not an executed zero-run finding.** The matching baseline records are verified; they do not contain the modified zero-weight run. Also, file hashes cover serialized changed tensors, not every unchanged model parameter or the evaluator. Therefore a baseline hash match does not by itself cover every drift item “at once,” and a hash difference first needs tensor/serialization diagnosis (`ADV:28,81,129`; `check_equivalence.py:25-36`; `92acd03:prepare.py:217,259-268`). The proposed (a) gate remains exact on the matched stack; it is not generalized to (b).

3. **Attribution to the entire 7 → 18 difference is too strong.** A baseline-identical zero replay would support removal of the term as the difference between the two source recipes, conditional on the historical mapping. It cannot prove that the unanchored historical 18 execution was that recipe, nor isolate why a different Gram matrix helped (`ADV:38,83-85`; `V:edits.commit="nocommit"`; `SB/results.tsv:4`; `92acd03:prepare.py:220-221`). I retain this premise instead of declaring the whole gain causally closed.

4. **Template-cache inference.** The later `check_equivalence.py:63` call observes an already cached list: earlier edits and run_recipe call `get_context_templates`. It does not demonstrate that a fresh first sample is insensitive to preceding random draws. Likewise, a cached list can survive later draws unchanged. The claim “if any random draw ever lands before sampling, the prefix changes” is not a universal guarantee. Require the realized list's external anchor, which I recovered in full, rather than infer RNG-state identity from a cached-list comparison (`ADV:46`; `check_equivalence.py:28,32,40,63-68`; `92acd03:edit.py:82`; `memit_dry_run/memit/memit/memit_main.py:304-323`; `results/autoresearch_c10_equivalence_rerun.log:25`).

5. **What the discriminating control can conclude.** I agree it is sharper, but “gain persists → regularisation or norm, not preservation at collision heads” overstates identification. A successful non-value control refutes necessity for its observed gain; alternative directional constraints, changed spectrum, or a subgroup shift remain possible. A failing control may simply have a different update size. Count matching is not energy/geometry matching (`ADV:101-104`; `92acd03:edit.py:94-104`; `92acd03:prepare.py:273`). The exact norm and collision readings in §3 expose rather than hide this limitation.

6. **A1/A2 exact equality does not transfer to (b).** The advisor's 69/69 anchor is appropriate for a faithful zero-weight identity replay, but the location control legitimately changes all arms' preserve matrices. For it I propose the existing ≥68 control floor and /72 ceiling, with 69/69 reported; improvements to 72 or accepted floor values are not provenance failures (`ADV:115`; `92acd03:prepare.py:43-44,201-209`; `B/V:summary.A1=69`, `summary.A2=69`). This is an explicit proposed replacement criterion, not an exemption in the current strict reader.

7. **Hash-plus-commit does not authenticate score origin.** A copied baseline score with fabricated provenance and a changed commit field could still have the expected baseline saved hashes. That combination does not close deliberate fabrication, even for (a); for (b) baseline hash equality would be scientifically wrong anyway. Fresh-run ownership, invocation/arm association, and a score-byte receipt close accidental association, with the trust boundary stated (`ADV:113`; `RR:102-128`; synthetic fixture `results/c10r_exp2ctl_codex_impl_v1.md:322-392`; saved-file hashing `92acd03:prepare.py:259-260`).

8. **Model revision and process exclusion precision.** The source's revision default is verifiable, not unpinned: `92acd03:c10e_bandknob.py:26,45,48` supplies it. Whether historical cache bytes faithfully matched it is still **UNVERIFIABLE**, so this only narrows `ADV:76`. Widening the GPU regex is useful, but cannot enforce no later relaunch and can match the runner's own path/interpreter. Use explicit PID ownership plus the reserved window, not a claim that a wider grep guarantees exclusion (`ADV:58-64`; `RUN:12,46-49`; `docs/C10R_EXP2_ZEROPRESERVE_PREREG.md:22-23`).

I agree with adding the pre-dispatch fingerprint, three arm-specific records, realized edit-context anchor, score metadata/schema checks, exact run-path/exit reporting, and freeze/bookkeeping clarity (`ADV:48,50-56,110-118,120-124`). The existing ±4/11/17 rule should not be justified as a noise envelope for this seeded identity control; the replacement uses the observed 7/18 and 0/13 endpoints descriptively, with the limitations above (`ADV:22`; `E08/E11/B:saved_sha256`, full values in §1; `docs/C10R_EXP2_ZEROPRESERVE_PREREG.md:30-34`).
