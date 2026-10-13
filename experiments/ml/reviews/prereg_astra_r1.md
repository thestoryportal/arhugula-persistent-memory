**FIX-FIRST**

The reviewed [preregistration](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md) matches SHA-256 `5d5008e0b2a4b59b18b91582d104620865a93a24237a613300a905af98d36b2d`. Review was read-only; no Python, model, or GPU job was run.

**BLOCKING**

1. **The specified wrappers cannot capture all promised solve operands.**

   `docs/MATHLAB_PREREG.md:49` limits recording to arguments/results of `compute_ks`, `get_module_input_output_at_words`, and `upd_matrix_match_shape`. None exposes `zs` or `resid`; those are locals created at `experiments/track_c/c10e_bandknob.py:189–204`. Nevertheless, prereg `:65` promises both.

   There is also an extra key-extraction pass after the five writes (`c10e_bandknob.py:218–220`). A recorder must distinguish these post-write cache keys from the five in-loop keys.

   **Required:** specify an explicit, read-only observation seam that captures the actual `zs`, `Kf`, `rf`, layer/index, projector identity, cache state and pre-cast update together. Freeze request/subject ordering and native dtypes. Each arm—and each wrapped/unwrapped parity trial—must start from restored weights **and a fresh zero cache**: `my_edit` mutates the cache, so restoring weights alone at prereg `:55` is insufficient.

2. **The historical-context fallback is incompatible with the named helper, and historical run identity is incomplete.**

   Prereg `:60` proposes using block F’s recorded contexts when they differ from C10Q. They do differ:

   - `results/c10u_mint2/r3/F_r0_mint1_s0.json:104–116` stores the authoritative nested templates under **`ctx`**, with recorded digest `8638d12c…`.
   - Under C10X’s own JSON serialization, those templates hash to `44a0d3d9…`.
   - `experiments/track_c/c10x_enginepath_arms.py:126–129` rejects every context set except `c7dabbe7…`.

   Thus `pinned_contexts` cannot implement this fallback unchanged. The nested `"contexts"` lists elsewhere in the mint record are audit structures, not the authoritative top-level template set.

   Additionally, prereg `:59–60` combines fresh C10Q A1/A2/A7 solves with historical block-F outcomes. A broad baseline envelope does not establish that a newly harvested update is the update behind a historical count.

   **Required:** define a lab-local pin accepting an explicitly frozen expected hash; identify `/ctx`, serialization and source hashes. Freeze target-file hashes and subject-to-row mapping. Specify whether calibration uses contemporaneous outcomes for the fresh harness arms or reproduces particular historical runs. For operand-only mint replay, require source identity, prompt/tokenization equivalence and recorded per-layer update-norm agreement before attaching the historical outcomes.

3. **The observer’s conversion contract is unsafe as written.**

   Prereg `:49` merely says wrappers “clone … to CPU.” It never prohibits combined device-and-dtype conversion. The measured audit documents both wrong results and possible source corruption, and explicitly rejects `clone().to("cpu", X)` as a reliable fix: `results/mps_offset_conversion_audit.md:7–37`.

   **Required:** mandate same-dtype CPU transfer before conversion, e.g. `detach().cpu().clone()` for native capture and subsequent CPU casts. Compute comparison norms in CPU float64. Add offset/noncontiguous-view and source-unchanged checks to observer validation.

   The fixed `1e-5` update tolerance at prereg `:95` is reasonable **for replaying the same CPU fp32 solve from identical operands**; it is not a justified fp32-versus-float64 tolerance. Keeping float64 diagnostic-only is correct. Actual tolerance attainment remains **UNVERIFIED**.

4. **The frozen proxy definitions still permit implementation choices that can change PASS.**

   Prereg `:63`, `:121–130`, and `:149` leave these consequential details unspecified:

   - Clean-forward batch grouping, padding and attention masks. The engine representation reader batches 128 contexts with padding (`memit_dry_run/memit/rome/repr_tools.py:135–147`); batch shape has already changed this program’s target vectors substantially (`CORPUS/51_C10S_SHAREDZ.md:14`).
   - Whether P-coll’s position sum excludes padding and precisely which token positions are included.
   - The even-sample median convention over 72 values: lower-middle versus averaging the two central values.
   - Proxy arithmetic dtype and handling of zero denominators/nonfinite values.
   - Bootstrap RNG implementation and exact resampling/reduction procedure.

   **Required:** freeze those choices. Resample 24 subject IDs with replacement, retain all three paraphrases for each sampled occurrence, recompute the original statistic including multiplicities, use strict `>` comparisons, and require at least **1,900/2,000** successes for each ordering. Invalid arithmetic must produce an explicit invalid outcome, never silent row exclusion or a selected epsilon.

5. **Launch isolation and autonomous resource enforcement need an executable contract.**

   Prereg `:52–53` names the fingerprint command and GPU exclusivity conditions but does not bind dispatch to the existing fail-closed process inspection. This matters because:

   - Importing `H` loads the model immediately (`c10e_bandknob.py:45–48`).
   - The fingerprint tool accepts inherited `LLMDB_ROOT` (`tools/engine_fingerprint.py:31–32`).
   - The existing gate explicitly binds the root and checks process inventory plus autoresearch sessions (`tools/c10w_p2_gate.py:67–84`).

   **Required:** specify an external pre-import launcher, explicit worktree root, existing GPU-check reuse, and coordinator/queue admission evidence. Do not invoke the P2-specific dispatcher with a fabricated math-lab stage.

   For CPU notebooks, prereg `:172` checks available memory only before a cell and gives a peak **target**, while low-memory waiting is unbounded. Specify bounded waiting/runtime and a measured or conservative allocation reserve. Eight GiB available before allocating several GiB does not preserve an eight-GiB floor. AUTONOMY requires hard deadlines and bounded units (`AUTONOMY.md:15–22`).

**ADVISORY**

- **Evidence restrictions and DuckDB design are sound.** Prereg `:11`, `:161–167` prohibit promotion/closure, require staging, and make DuckDB rebuildable with source path, JSON pointer and SHA. Clarify `:185`: stopping stages a note immediately; canonical closeout occurs later through the supervised lead, as `AUTONOMY.md:25–27` requires.

- **The nine-ordering rule is a legitimate falsifiable screen.** Both proxies and the “either passes” rule are declared in advance; neither needs to be selected after observation. Injection is correctly excluded as tautological calibration (`:153–157`). Nothing in the formulas proves passing impossible or automatic. However, `1/60` and `≤2/60` are combinatorial probabilities under uniformly random rankings, **not calibrated false-positive rates** for correlated mint seeds and deliberately chosen arm families (`:148–151`).

- **Narrow the promised predictive use.** Prereg `:119` correctly disclaims prediction of top-1 recall, but `:15` promises identifying candidates “unlikely to move the GPU count.” Six known, widely separated tier examples do not establish sensitivity to improvements within A7. Replace that promise with “passes retrospective tier discrimination; prospective queue-ranking utility remains unverified.”

- **Distinguish solved update from deployed weight change.** The saved reference is the fp32 update before application (`:49`, `:66`), whereas the harness casts and adds into fp16 weights (`c10e_bandknob.py:217`). It is not exactly `W_after − W_before`. Name it `upd_precast`; either record the effective weight difference or explicitly retain fp16 cast/add rounding among the proxy approximations.

- **Correct the audit shape claim.** Prereg `:44` says both audits contain `24 × 151936` logits/log-probs. Static inspection of their serialized tensor metadata gives **A1: `6 × 151936`; A7: `24 × 151936`**, both fp16. Their classification as target-solve audits containing no keys or ΔW is correct.

- **The runtime recipe is incomplete.** Prereg `:87` names torch 2.8.0 and a pydantic model, while the displayed command supplies only marimo and DuckDB; `:172` additionally requires psutil. Freeze the complete PEP 723 dependency set and tested headless invocation. The claimed ≤6-GiB peak and ≤60-minute harvest remain estimates.

**Citation verification — more than ten checks completed**

| Claim checked | Source evidence | Finding |
|---|---|---|
| Actual C10 solve is projected ridge, CPU fp32 | `c10e_bandknob.py:205–211` | Correct |
| Engine solve is invoked by LAW#5 | `c10e_bandknob.py:423`; `memit_main.py:200–206` | Correct for this harness path |
| Sequential updates precede subsequent operand extraction | `c10e_bandknob.py:194–217` | Correct |
| Projector uses CPU SVD and threshold 0.005 | `c10e_bandknob.py:166–175`, `:28` | Correct |
| Keys average within context types, then across types | `memit/compute_ks.py:39–50` | Correct |
| Band 4–8 and subject-last lookup | `configs/hparams/qwen25_3b_memit_hparams.json:2–5` | Correct |
| Audit fields and Zorbland-only capture | `c10x_enginepath_arms.py:1006–1029` | Correct; A1 shape correction above |
| Canon 7→4; injection 49/72; baseline envelope | `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:23–25`, `:39` | Correct |
| Mint G/N 39/46; rare 25; A1 68–72 | `CORPUS/45_C10L_MINT_TOKEN.md:14–18` | Correct |
| Mint seeds 46/34/36; edited injection 23; recomputed target 55 | `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:17–22` | Correct |
| Canonical/shared injection 51/69 | `CORPUS/51_C10S_SHAREDZ.md:12` | Correct; injection-only, shared arm UNDERFIT |
| Block-F mint 46/37/40 and multi 14 | `CORPUS/54_C10U_MINT2.md:25–28`; four cited `F_r0_*.json` records, `/arm/para_full_binding_n` | Correct |
| Block-F A1 control 68 | `CORPUS/54_C10U_MINT2.md:68`; `F_r0_mint1_s0.json:6944` | Correct |
| Non-exempt Python blocks GPU dispatch | `tools/c10w_p2_gate.py:19–53` | Correct; marimo is not exempt |

“Parallel” is honestly narrowed at prereg `:173` to ungated tails and the lead’s work. It must remain subject to the launch and resource fixes above.

🌱 graft reported ~238,266 tokens saved this turn, 1 successful call.

