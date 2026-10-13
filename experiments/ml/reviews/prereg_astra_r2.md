**FIX-FIRST**

Reviewed v2 matches SHA-256 `b7cd0b1369000291f80cc23042db587c5f12ee2e504828ccb004fa42cae18b72`, checked again at completion. Read-only review; no model, tokenizer, torch or GPU execution. A small stdlib-only profiling probe verified the frame-identity issue below.

| Round-1 item | Disposition | Evidence |
|---|---|---|
| **B1 — observation seam** | **NOT RESOLVED** | The seam can expose the operands, but its caller predicate names the rebound function: `docs/MATHLAB_PREREG.md:84–91`. |
| **B2 — historical replay identity** | **NOT RESOLVED** | Context pinning and hashes are corrected, but `docs/MATHLAB_PREREG.md:76` requires historical tokenization fields absent from the records. |
| **B3 — conversion safety** | **RESOLVED, design-level** | Same-dtype CPU transfer, subsequent CPU casts, fp64 comparisons and source-unchanged checks are explicit at `docs/MATHLAB_PREREG.md:92–93,146`; consistent with `results/mps_offset_conversion_audit.md:24–37`. |
| **B4 — proxy definitions** | **RESOLVED, design-level** | Batching, positions, arithmetic, median, invalid denominators and exact paired bootstrap are frozen at `docs/MATHLAB_PREREG.md:119,164–184,203`. |
| **B5 — launch/resource contract** | **NOT RESOLVED overall** | The two-function gate reuse is correct (`docs/MATHLAB_PREREG.md:57–63`); the CPU exception at `:226` can nevertheless override inventory failures. |

**BLOCKING**

1. **B1: compare against the saved original function, not rebound `H.my_edit`.**

   [Prereg:84–90](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:84) first assigns `H.my_edit = observed_my_edit`, then requires the shape-helper caller to be `H.my_edit`. The immediate caller is the **original** function executing [c10e_bandknob.py:212](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10e_bandknob.py:212), not its wrapper. The cited precedent saves `ORIGINAL_EDIT` before rebinding (`c10x_enginepath_arms.py:468–473`).

   The stdlib probe returned `rebound_matches=False`, `original_matches=True`, with all seven requested locals present.

   **Required replacement:** save the original edit and shape-helper code objects before rebinding; match `frame.f_code` against the helper and `frame.f_back.f_code` against the **original edit**. Use that original code object for the return event too. Require exactly five ordered layer captures per science write; zero captures must never pass inertness validation.

   Also make LAW#5 tagging precede the 24-subject assertion. Its actual request list contains only Zorbland/Cairo (`c10e_bandknob.py:430–433`), whereas prereg `:91` otherwise requires all of `H.FICTION`.

   **What is sound:** at the corrected `call` event, `zs/K/Kf/rf/resid/cur/upd` exist together after the solve (`c10e_bandknob.py:189–212`). The cache pass at `:218–220` makes no shape-helper call and is excluded. LAW#5 records can be discarded using the flag, which remains true throughout its call.

2. **B2: the frozen historical comparison requires data that was not recorded.**

   [Prereg:76](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:76) requires canonical `input_ids` and `subject_last` indices to equal historical fields, leaving their locations for the build to discover.

   Structural inspection of all three mint records found no such arrays or indices. The actual evidence is:

   - `F_r0_mint1_s0.json:953–962`: successful P2 audit, `inventory_unchanged=true`, 2,376 inventory prompts.
   - `:965–1008`: target IDs and **boolean** contextual tokenization checks.
   - [c10u_mint2_arms.py:234–256](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10u_mint2_arms.py:234): the writer stores those booleans and target IDs, not canonical input IDs or lookup indices.

   Consequently, the specified missing-field rule produces **INVALID-REPLAY**, making six-arm calibration impossible as written.

   **Required:** replace this with an explicit, source-backed equivalence contract using the recorded P2 audit, pinned tokenizer identity, frozen prompts/context inventory and lookup routine; distinguish reconstructed indices from historically recorded ones. Alternatively, cite an existing artifact containing the required historical fields. Resolve this before spending GPU time.

3. **B5: preserve fail-closed inventory handling through the CPU exception.**

   [Prereg:226](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:226) permits a lead-written record to override **any** `check_gpu()` refusal. But refusals include failed/empty process inspection and tmux inspection errors—not merely identified coordinators awaiting no further gates (`tools/c10w_p2_gate.py:75–84`).

   **Required:** inventory-probe errors must remain unconditional refusals. Permit the coordinator-tail exception only after successful inventory collection, with every blocking process accounted for by the admission record and no blocking autoresearch session.

   **The requested reuse itself is correct:** module imports are stdlib-only (`:12–14`); `check_fingerprint()` binds `LLMDB_ROOT` to its module’s worktree (`:16–17,67–70`); `check_gpu()` excludes its own PID (`:49,78`). Neither requires `_check_dispatch_guards` or a fabricated P2 stage.

**ADVISORY**

- **The shared block-F context is sound and does not itself break LAW#3.** All four source records have identical `/ctx`; I recomputed `8638d12c…` using the specified serialization and `44a0d3d9…` using C10X’s serialization. Fresh A1/A2/A7 calibration uses contemporaneous counts, and the baseline envelopes remain mandatory (`docs/MATHLAB_PREREG.md:67–80,106`). Historical norm attachment is separate and non-gating for these fresh arms. Complete their baseline checks before admitting mint calibration data.

- **The parity design is adequate for the specified observer once B1 is fixed and capture coverage is asserted.** Fixed targets, identical pinned contexts, pristine weight restoration and independent zero caches remove the identified state confound (`docs/MATHLAB_PREREG.md:94–99`; `c10e_bandknob.py:150–159,218–220`). The accompanying observed harness LAW#5 gate supplies the behavioral comparison. This is an acceptable preregistered proof procedure, **not an empirically established INERT result**.

- **Norm agreement is a consistency check, not tensor identity.** Keep the `1e-3` historical comparison, but avoid calling it a “second, consistent observation” solely because norms match (`docs/MATHLAB_PREREG.md:80`). Report fresh and historical counts separately. Also, `CORPUS/54:68` supports the **A1** floor, not an A2-specific threshold; describe A2 ≥68 as this preregistration’s chosen floor.

- **Evidence and output boundaries survived.** `docs/MATHLAB_PREREG.md:11,15,215–216` retains MATH-PROXY, unverified prospective utility, staging and supervised canonical fold-in. Lines `217–221` retain DuckDB’s derived-only status, source paths/JSON pointers/hashes, rebuild-on-disagreement and prohibition on citing the index.

**New citation checks — ten sampled**

| Citation newly checked against source | Result |
|---|---|
| `c10x_enginepath_arms.py:467–473` | Rebinding precedent confirmed; original function is explicitly retained. |
| `c10x_enginepath_arms.py:912–929` | Preexisting-profiler rejection and `finally` restoration confirmed. |
| `c10u_mint2_read.py:29–30` | Exact digest serialization confirmed. |
| Four `results/c10u_mint2/r3/F_r0_*.json` context/source identities | File hashes and identical contexts confirmed. |
| Three `step0/F_r0_mint1_s{k}.json:7563` target hashes | All match the corresponding on-disk `.pt` files. |
| `F_r0_mint1_s0.json:7999–8052` | A1 and candidate norms confirmed; candidate values begin at **8027**, beyond the cited `7999–8022` region. |
| `c10u_mint2_arms.py:187–188,447–465` | Subject-order assertion and target stacking confirmed. |
| `memit/compute_z.py:234–267` | Subject lookup implementation confirmed; this does not establish historical persistence. |
| `c10y_directdw_arms.py:661–665` | Eight-GiB available-memory floor confirmed. |
| `AUTONOMY.md:25–27` | Staging and supervised closeout boundary confirmed. |

🌱 graft reported ~120,565 tokens saved (~$0.06), 1 successful call.

