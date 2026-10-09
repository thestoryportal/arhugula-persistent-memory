# Pre-registration — D-ML-1: the offline math lab, steps 1–3 (operand harvest, offline solve reproduction, retro-prediction calibration) (FROZEN v4, 2026-10-08)

**Status: FROZEN v4 (2026-10-08) — GPT-6-Astra high FREEZE, `results/mathlab_staging/prereg_astra_r4.md`.** Freezing approves the design only. Tensor and behavioural inertness, replay norms, resource bounds and calibration remain UNVERIFIED until execution. Review history:
- **Round 1:** v1 (SHA `5d5008e0…`) came back FIX-FIRST from GPT-6-Astra (high), with 5 BLOCKING and 6 ADVISORY items (`results/mathlab_staging/prereg_astra_r1.md`). All were folded into v2.
- **Round 2:** v2 (SHA `b7cd0b13…`) came back FIX-FIRST, with B3 and B4 RESOLVED, B1, B2 and B5 still BLOCKING, and 4 ADVISORY items (`results/mathlab_staging/prereg_astra_r2.md`). All are folded into v3.
- **Round 3:** v3 (SHA `b0a41584…`) came back FIX-FIRST, with B1 and B5 RESOLVED, B3 and B4 still resolved, B2 still BLOCKING, and advisory items (`results/mathlab_staging/prereg_astra_r3.md`). All are folded into v4.
- **Round 4:** v4 (SHA `257e064c…`) came back **FREEZE**, with no BLOCKING item. Its one non-blocking advisory is noted at §2.2 check 3(c).
- **Fold logs:** §11 for round 1, §12 for round 2, §13 for round 3.
- **Next:** the model-free build (§10). Nothing has run and no driver or notebook exists. The harvest (step 1) also waits on the GPU queue: C10X re-run 3 and ASTRA attempt 3 must both have exited.

**Decision-ID:** `D-ML-1`. The format is `D-<TRACK><n>` (`EXPERIMENT_RUNBOOK.md:217`); the instrument track follows the `D-HW-1` precedent in §5.3. **Origin:** an operator request on 2026-10-08 for a math lab that runs in parallel with GPU work and reads existing findings as context. It runs through the math in Python, inside a marimo notebook, without loading the model. The operator approved starting on 2026-10-08 and asked for DuckDB and InfraNodus to be included (§5, §7). **Engine and harness facts below come from `cat -n` reads on 2026-10-08 (LAW#4).** The engine, the harness file `experiments/track_c/c10e_bandknob.py`, LARQL and git stay unmodified. Every lab seam is confined to the lab's own processes and is proven inert before its data is used (§2.3).

## 0. Where this sits, and what it can and cannot conclude

**On the e2e map.** The lab is an instrument, not a framework component. It analyses the per-commit solve inside the write path's compile step (`docs/SPEC_E2E_GROUND_TRUTH.md` §C, `:22–31`), which is the same cell C10X occupies. It touches no read, governance or deployment layer, and it can never produce §F's L2 behavioural evidence. The bar there is the held-out paraphrase decoded greedily, full sequence, top-1, on the model, and the lab never decodes.

**Evidence tier: MATH-PROXY (binding, §5).** Every lab output carries the label `MATH-PROXY`. A MATH-PROXY result may reorder or prune the GPU queue. It may never promote a claim, close a route, or enter `CORPUS/` above `I-INFER (MATH-PROXY)`.

**Prior, stated before design.** This program has already run an offline proxy against behaviour once, and the proxy lost. CORPUS/44 step 0 reconstructed the harness loop offline and predicted that canonical realisation improves under P := I (H-I8a). That prediction was **false behaviourally**: canon went 7 → 4 (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:25`). The advisor also ruled out reading ρ_c ≈ 0.03 as proof that the edit realises its target (`:40`; ρ is a remaining-residual ratio, correction at `:43`). **The default expectation is therefore that a residual-type proxy fails calibration (§4).** The design makes that failure cheap and decisive.

**What a pass buys, and what it does not.** A pass means **the proxy passes retrospective tier discrimination on six measured arms.** Its prospective use for ranking the queue, including its sensitivity to improvements *within* the A7 tier, **remains unverified** and must earn its own evidence before any queue decision leans on it. **A fail** stops the lab (§8). Its total cost is one GPU harvest (an estimated ≤ 60 min) plus bounded CPU runs.

## 1. Engine and harness facts the design depends on (read 2026-10-08)

- **The C10 write is the harness solve, not the engine's λC solve.** Every C10 arm writes through `my_edit(hp, requests, P, cache_c)` (`c10e_bandknob.py:181–221`), called by its module-global name inside `run_recipe` (`:489`).
  - `zs` comes from `Z_OVERRIDE` (`:185–189`) or `compute_z` at layer 8 (`:191`).
  - Per layer `i`:
    - `K = compute_ks(...).T` (`:196`).
    - `cur` is the block output at `z_layer = 8` on the canonical prompt at the subject's last token (`:184`, `:197–201`).
    - `tgt = zs − cur` (`:202`), repeated (`:203`).
    - `resid = tgt / (len(layers) − i)` (`:204`).
    - `Kf = K.float()` and `rf = resid.float()` (`:205–206`).
    - `Pi` is the projector, or `I` under one knob (`:207`); `ca = cache_c[i]` (`:208`).
    - `A = Pi(Kf Kfᵀ + ca) + L2·I` and `B = Pi Kf rfᵀ` (`:209–210`).
    - `upd = solve(A, B)ᵀ` in fp32 on CPU (`:211`), passed through `upd_matrix_match_shape(upd.float(), …)` (`:212`).
    - The update is **cast to the weight dtype and added in place** (`:216–217`).
  - After the five layers, a **second key pass** updates the cache: `cache_c[i] += K Kᵀ` (`:218–220`).
  - Constants: `L2 = 1.0` (`:29`). `P[i]` comes from `compute_P`, a CPU fp32 SVD of `get_cov(...)` that keeps singular vectors with `S < NULL_THRESH = 0.005` (`:28`, `:166–178`). The cache is zeroed per arm (`:474`).
  - The engine's solve, `adj_k = solve(mom2_update_weight·C + K Kᵀ, K)` with `upd = resid @ adj_kᵀ` (`memit_dry_run/memit/memit/memit_main.py:200–206`), runs only in the LAW#5 parity check (`c10e_bandknob.py:423`).
- **The solve is sequential.** Because the add at `:216–217` is in place, at layer `i` both `K` (`:196`) and `cur` (`:197–201`) are read **after** layers `< i` were edited.
- **Keys.** `compute_ks` reads the down_proj input at the subject's last token (`fact_token = subject_last`, `configs/hparams/qwen25_3b_memit_hparams.json:5`) over every context template. It averages within each template type, then across types (`memit_dry_run/memit/memit/compute_ks.py:19–50`). The engine reader pads and batches up to 128 contexts per forward (`memit_dry_run/memit/rome/repr_tools.py:135–147`). Batch shape has moved target vectors by a relative 0.098 in this program (`CORPUS/51_C10S_SHAREDZ.md:14`).
- **Context templates.** They are sampled once per process (`memit_main.py:304–323`; CORPUS/44 F-A4 `:32`). C10X's `pinned_contexts` accepts only the C10Q set, under `json.dumps(ctx)` default serialization, `c7dabbe7…` (`c10x_enginepath_arms.py:32`, `:126–137`). **Block F of C10U used a different set.** It is stored authoritatively at `/ctx` in its records (`results/c10u_mint2/r3/F_r0_mint1_s0.json:104–115`), with `ctx_sha256 = 8638d12c6d5844168e1577a459103fa309bcf995fc1225df7e716de11a87cdc9` (`:116`). That digest is `json_digest` = sha256 of `json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False)` (`experiments/track_c/c10u_mint2_read.py:29–30`). Under C10X's serialization the same set hashes to `44a0d3d9…` (Astra r1, B2), and C10X's helper rejects it. The nested `"contexts"` lists elsewhere in the record are audit structures, not the template set.
- **Block F identity data (bound in §2.2).**
  - Each record stores per-layer `delta_norm` for its in-run `A1_single` control and its `candidate` arm at `/recipe/delta_norms` (`F_r0_mint1_s0.json:7999–8052`: `A1_single` from `:7999`, `candidate` from `:8027`; s0 candidate 15.910 / 11.994 / 11.703 / 19.392 / 26.730 for layers 4–8).
  - **No canonical `input_ids` or `subject_last` indices were recorded.** What was recorded is the P2 tokenisation audit, `/admission/P2` (`F_r0_mint1_s0.json:953–1008`):
    - `ok: true`, `inventory_unchanged: true`, `inventory_n` 2,376, `plain_n` 396;
    - per subject, `target_ids` and `expected_ids`, plus **boolean** contextual checks (`prefix_ids`, `whole_ids`, `last_id`) under each of the six templates.

    The writer is `p2_audit` (`experiments/track_c/c10u_mint2_arms.py:210–256`). The writer's behaviour process builds the prompt list with **`audit_prompts(H, M, root)`** (`c10u_mint2_arms.py:273–282`, called at `:793`, passed to `p2_audit` at `:794`). That list is the library helper's inventory (`c10l_mint_lib.all_harness_prompts`, `experiments/track_c/c10l_mint_lib.py:178–185`) **extended** with:
    - the forms `CANON`, `PTEST`, `"{} is described as"`, `"{} is a"` and `"{} is associated with"` over `H.FICTION + FRAME_SUBJECTS + ["Zorbland"]`;
    - `CANON` over every country in the two screen configs;
    - `H.GENERIC`, `M.UNRELATED`, and `" " + capital` for every screened capital;
    - de-duplicated, preserving order.

    The screen configs are `configs/screens/g6_screen_qwen3b{,_v2}.json`. `p2_audit` then adds every context template applied to each plain prompt (`c10u_mint2_arms.py:212–213`). The library helper alone yields at most 233 plain and 1,398 contextual strings (Astra r3), so **only `audit_prompts` can reproduce the recorded 396 / 2,376.** `inventory_unchanged` means the base tokenizer and the minted tokenizer give identical ids for every inventory string (`:214–215`, `ids_of` with `add_special_tokens=False`, `:206–207`; Qwen's `tokenizer_config.json` has `"add_bos_token": false`).
  - The minted ids are 151665–151688 (`/minted_ids`). They lie in the 271 spare rows above the base vocabulary (`CORPUS/45_C10L_MINT_TOKEN.md:22`, `:45`), and the base tokenizer cannot emit them.
  - The mint target files have on-disk SHA-256s `2b1ba555…` (s0), `a931e805…` (s1) and `88c8e6a5…` (s2), each also present as a `zs_file_sha256` in `results/c10u_mint2/r3/step0/*.json`.
  - Target rows follow `H.FICTION` order (`experiments/track_c/c10u_mint2_arms.py:187–188`, `:447–464`).
- **Covariance.** `STATS_DIR` is `arhugula-persistent-memory/covariance_caches` (`memit_dry_run/memit/globals.yml:6`). File names follow `c10e_bandknob.py:349`. The layer 4–8 files are present, 462.3 MiB each (fp32 11008²).
- **Model.** Qwen/Qwen2.5-3B at revision `3aab1f19…` (`c10e_bandknob.py:25–26`), fp16 on MPS (`:47`). **Importing the harness loads the model at import time** (`:45–48`). Its `config.json` gives hidden 2048, intermediate 11008, 36 layers, tied embeddings, vocab 151936. The band is [4, 5, 6, 7, 8] (`qwen25_3b_memit_hparams.json:2`).
- **Stimuli and evaluation.**
  - `CANON` (`c10e_bandknob.py:51`), `PTEST` with three templates (`:52–56`), `FICTION` with 24 subjects (`:57–61`), `described_as` (`:475`), L1 with 12 and L3 with 30 (`:259–277`).
  - Evaluation runs **one prompt per forward with no padding** (`predict` `:101–105`, `full_seq_match` `:109–117`).
  - Arms are selected with `C10_ARMS` (`:254–255`). `ARM_HOOKS` run after each arm's evaluation, with the edit still applied (`:494–495`).
- **What is on disk now.**
  - The covariance files and the three mint target files above.
  - `results/c10x_enginepath_rerun3/audit_{A1_single,A7_coined_coined}.pt` are **OverTone target-solve audit snapshots** for Zorbland, written by `c10x_enginepath_arms.py:1006–1027`. Their logits and log-probs are **6 × 151936 (A1) and 24 × 151936 (A7)**, both fp16. **They hold no ΔW and no keys.**
  - No keys, residuals or ΔW are persisted anywhere. CORPUS/44 step 0 kept only a JSON summary (`experiments/track_c/c10l_covgeom_step0.py:1`).
- **The MPS conversion hazard.** On torch 2.8.0 MPS, any MPS→CPU copy that **also changes dtype** can return wrong values from offset views (Mode A) or corrupt the MPS source in place (Mode B). `.cpu()` / `.to("cpu")` at the same dtype is safe, as is a same-device cast. `clone().to("cpu", X)` is **not** reliable (`results/mps_offset_conversion_audit.md:7–37`).

## 2. Step 1 — the operand harvest (GPU, one process)

### 2.1 Launch contract (external, before any import of the harness)

- **Launcher: `tools/run_mathlab_harvest.sh`** (new, shell). It sets `W` to the worktree root explicitly (`git -C <script dir> rev-parse --show-toplevel`), exports `LLMDB_ROOT=$W`, and runs the admission check as a **separate, model-free** process: `"$W/.venv/bin/python" -B "$W/tools/mathlab_admit.py" --kind harvest --admission <file>`. On exit 0 it `exec`s the harvest driver. On any other exit it stops and stages the admission JSON.
- **`tools/mathlab_admit.py` (new, model-free; it never imports torch or the harness)** reuses the existing gate inventory logic. It imports `tools/c10w_p2_gate.py`, whose module-level imports are stdlib only (`:12–14`), and calls exactly two functions:
  - `check_fingerprint()` (`:67–70`), which runs `tools/engine_fingerprint.py` with `LLMDB_ROOT` bound to `W`. This closes the inherited-root hole in `engine_fingerprint.py:31–32`. PASS requires `d941a9fb…` and `_cov_cpu == 3`.
  - `check_gpu()` (`:73–84`), which fails closed on any non-exempt compute process in `ps -axww` and on an exact-name `autoresearch` tmux session.

  It **never** calls `_check_dispatch_guards` (`:87`) or any P2 dispatcher, and it fabricates no P2 stage. It also checks free memory ≥ 8 GiB (the C10Y floor, `experiments/track_c/c10y_directdw_arms.py:665`).
- **Queue admission evidence.** `--admission` names a JSON record written by the lead at `results/mathlab/admission_<UTC>.json`. It lists the terminal status files of C10X re-run 3 and ASTRA attempt 3 with their SHA-256s, each showing a terminal status, and states that no other coordinator is live or pending. `mathlab_admit.py` re-hashes those files and requires a terminal status in each, or it refuses.

### 2.2 Context, arms, and which outcome calibrates each arm

- **One context set for all six arms: block F's `/ctx`.** A lab-local context manager, `lab_pinned_contexts(H, ctx, expected_digest)`, in the harvest driver uses the same mechanics as `c10x_enginepath_arms.py:126–137`: it swaps `CONTEXT_TEMPLATES_CACHE` in `H.get_context_templates.__globals__`, checks for drift on exit, and restores on exit. **Unlike C10X's helper, it takes the expected digest as a parameter.**
  - **Frozen inputs:** `ctx` is read from `/ctx` of `results/c10u_mint2/r3/F_r0_mint1_s0.json` (file SHA-256 `ade8ba1678dc45850168ff8303afd28359b33c1c7a9f0731feee1143eca2c8f9`).
  - **Required checks:** `json_digest(ctx)` must equal `8638d12c6d5844168e1577a459103fa309bcf995fc1225df7e716de11a87cdc9` (serialization above), and `/ctx` must be identical in `F_r0_mint1_s1.json` (`ab4cc4ec…`), `F_r0_mint1_s2.json` (`626750bc…`) and `F_r0_multi_snone.json` (`0ec55d87…`).
  - The C10X-serialization hash is also recorded.
  - `C10_CTX_TEMPLATES` must be unset (default "on", `c10e_bandknob.py:182`).
- **Harness arms, with contemporaneous outcomes.** `A1_single`, `A2_coherent2` and `A7_coined_coined` run through `H.run_recipe("baseline", H.HP_BASE)` with `C10_ARMS=A1_single,A2_coherent2,A7_coined_coined`. That gives the harness's own LAW#5 gate, per-arm restore and zero cache (`:473–474`), `my_edit` (`:489`) and `eval_arm`. **The calibration outcome for each of these arms is the count measured in the harvest process itself**, so the update and its outcome come from the same process. Block F's historical A1 (68) and A7 (14) are **reported in a separate column** and never replace or combine with the fresh count (§4.2). **Stage order (binding):** the three fresh arms must complete and pass their LAW#3 baseline checks (§2.4 gate 4) **before** any mint replay runs or any mint datum is admitted.
- **Mint arms, operand-only replays of historical runs.** `mint-1 s0`, `s1` and `s2` are written with `my_edit` on restored weights and a fresh zero cache. Targets come from `results/c10u_mint2/r3/zs/F_r0_mint1_s{k}.pt` through `Z_OVERRIDE`, keyed by the driver's own requests `H.req(CANON, c, v)`; rows are in `H.FICTION` order. No vocabulary row is minted, because the canonical prompt contains no value token. **The historical outcome (46 / 37 / 40) attaches to a replay only if all four checks pass:**
  1. **Source identity.** The target file's SHA-256 equals the frozen value above and the step-0 record's `zs_file_sha256`. The record's file SHA matches.
  2. **Context identity.** The `json_digest` of `/ctx` is as above.
  3. **Tokenisation equivalence: an explicit contract with source-backed parts.** The historical ids and indices were not recorded (§1), so this check does **not** compare against recorded arrays. It establishes equivalence through the following parts, all checked at harvest time on CPU:
     - (a) **Pinned tokenizer identity.** The harvest's tokenizer is `AutoTokenizer.from_pretrained` at the pinned `ID`/`REV` (`c10e_bandknob.py:25–26`, `:44–46`), the same identity as block F's base tokenizer. The SHA-256 of the snapshot's `tokenizer.json` and `tokenizer_config.json` is recorded.
     - (b) **Reconstructed minted tokenizer.** A CPU copy of the base tokenizer gets block F's `/minted_words` registered through the writer's own `c10l_mint_lib.register` (`experiments/track_c/c10l_mint_lib.py:24–37`). That function covers the `AddedToken` flags, the exact added count, the contiguous spare-id assertion and the single-id round trip per word. The returned ids must equal `/minted_ids`, exactly as the writer's own replay requires (`c10u_mint2_arms.py:787–790`).
     - (c) **Recorded audit re-derived, using the writer's own inventory.** The steps follow the writer's caller (`c10u_mint2_arms.py:791–794`):
       1. **Inventory.** Obtain `prompts, countries, capitals = c10u_mint2_arms.audit_prompts(H, M, W)` (`:273–282`), with `M = c10l_mint_lib` and `W` the explicit worktree root.
       2. **Source identity.** Before the call, the current SHA-256 of every source that call reads must equal the block-F record's `/identity/source_sha256` entry. That covers `experiments/track_c/c10u_mint2_arms.py` (`a0380133…`), `experiments/track_c/c10l_mint_lib.py` (`5277e65d…`), `experiments/track_c/c10e_bandknob.py` (`1f6be581…`), `configs/screens/g6_screen_qwen3b.json` (`a5181334…`) and `configs/screens/g6_screen_qwen3b_v2.json` (`482c05f8…`). All five matched on 2026-10-08 by static `shasum` against `F_r0_mint1_s0.json` `/identity/source_sha256`. A mismatch is a shared failure.
       3. **Audit.** Pass that `prompts` to the original `p2_audit` together with block F's frozen `/ctx`, `H.FICTION`, `FRAME_SUBJECTS` from the writer module, the recorded `/minted_words` and `/minted_ids`, the values, `kind` and `block`, mirroring `:794`.

       The **required counts are not lowered.** Its result must equal the recorded `/admission/P2` in `ok`, every `checks` boolean, `changed == []`, `inventory_n == 2376`, `plain_n == 396`, and every row's `target_ids`, `expected_ids` and per-template booleans.
       *Note (Astra r4 advisory):* the saved `/admission/P2` also holds `wordlist_replay`, which the step-0 writer appended (`c10u_mint2_arms.py:711–712`) and persisted (`:857`). The enumerated comparison above is therefore correct, and a raw whole-object `p2_audit(...) == saved_P2` would fail on that key. Astra separately reproduced `wordlist_replay` exactly for all three records.
     - (d) **Lookup substrings.** The engine's lookup routine (`repr_tools.get_words_idxs_in_templates`, `memit_dry_run/memit/rome/repr_tools.py:43–…`, called by `compute_z.find_fact_lookup_idx`, `compute_z.py:234–267`) also tokenizes template prefixes, words and suffixes separately, and these are not in the P2 inventory. So for the 24 canonical requests under every `/ctx` template, the ids of each such substring and the resulting `subject_last` index must be identical under the base and the reconstructed tokenizer.

     **The indices used by the harvest are labelled `RECONSTRUCTED`** (recomputed with the engine routine under the proven-equivalent tokenizer), **never `RECORDED`**.

     **What a mismatch does.** Parts (a)–(d) are shared by all three mint arms: the same `/ctx`, subjects, prompts and tokenizer. A failure in any of them therefore makes **all three mint arms INVALID-REPLAY**, and calibration is **INVALID** (§4.3). That is not a per-arm outcome, because a shared failure says nothing seed-specific.
  4. **Update-norm agreement (per arm).** For each layer, `|‖upd_precast‖_F − delta_norm_F| / delta_norm_F ≤ 1e-3` against the arm's own record's `/recipe/delta_norms/candidate`. This is a consistency check on norms, **not tensor identity**.

  **Per-arm failures.** Checks 1 and 4 are seed-specific. A failure in either makes **that arm only** INVALID-REPLAY, and calibration proceeds on the admitted arms under §4.3's reduced rule, provided at least two mint arms are admitted. With fewer than two, calibration is INVALID.
- **The same norm check for the fresh harness arms (a consistency check, reported only).** The harvested A1 and A7 per-layer norms are compared with `/recipe/delta_norms/A1_single` and with the multi record's `/recipe/delta_norms/candidate`, at 1e-3. The result is reported beside the separate historical-count column. It is **not** an identity proof, and it does not make the historical count a second observation of the fresh update.

### 2.3 The observation seam (read-only; harness and engine unmodified)

- **Mechanism.** A `sys.setprofile` observer in the harvest process, the same class of seam as C10X's `stopping_observer` (`c10x_enginepath_arms.py:912–929`, which requires that no profiler was already installed). **Installation is lab-side and confined to the harvest process.** The driver rebinds `H.my_edit` to `observed_my_edit`, the same rebinding precedent as `c10x_enginepath_arms.py:467–473`. That function:
  1. requires `sys.getprofile() is None`;
  2. installs the observer;
  3. calls the **original** `my_edit` object with its arguments unchanged;
  4. restores the previous profile in a `finally` block.

  - **Code identity is frozen before rebinding.** The driver saves `ORIGINAL_EDIT = H.my_edit`, `EDIT_CODE = ORIGINAL_EDIT.__code__` and `SHAPE_CODE = H.upd_matrix_match_shape.__code__` **before** it assigns `H.my_edit = observed_my_edit`. This is the same order as the precedent, which saves `ORIGINAL_EDIT` first (`c10x_enginepath_arms.py:468`, `:473`).
  - **Matching rule.** A capture fires only on `event == "call"` with `frame.f_code is SHAPE_CODE` **and** `frame.f_back.f_code is EDIT_CODE`. The immediate caller at `:212` is the **original** function, never the wrapper; Astra's stdlib probe found `rebound_matches=False` and `original_matches=True`. The post-write record fires only on `event == "return"` with `frame.f_code is EDIT_CODE`. The engine's own calls to the shape helper (`memit_main.py:51`, `:210`) have a different caller code and never match. The second key pass (`:218–220`) makes no shape-helper call.
  - **LAW#5 tagging comes first.** On every matching event, the observer reads `H._LAW5_DEFAULT_CTX` **before** any other check. While it is True (set at `:430`, true throughout `run_law5`'s `my_edit` call at `:433`, whose request list is only Zorbland → Cairo), the capture is tagged `law5`, checked for count and order only, and discarded. **Only untagged (science) captures** are subjected to the 24-subject assertion (`[r["subject"] for r in requests] == H.FICTION`).
  - **Coverage is required.**
    - Every science `my_edit` call must yield **exactly five** captures, with `(i, layer)` = (0, 4), (1, 5), (2, 6), (3, 7), (4, 8) in that order, plus exactly one return record.
    - Every LAW#5 call must yield exactly five tagged captures in the same order, which proves the observer was live during the LAW#5 gate.
    - Any other count, including **zero**, makes that write INVALID and HALTs the harvest. **Zero captures can never pass the inertness gate.**
  - `run_recipe` (`:489`) and `run_law5` (`:433`) both reach `observed_my_edit` through the global name, so the LAW#5 gate runs **with** the observer installed. Profiling is active only inside `my_edit`, never during evaluation.
  - At the matching call, the original frame's locals hold the layer's actual operands (`:189–212`).
- **Captured per layer, together:** `i`, `layer`, `zs`, `K`, `Kf`, `rf`, `resid`, `cur`, the projector identity (the null-space count of `Pi`, the SHA-256 of its fp32 bytes, and `Pi v_j` for four probes `v_j` drawn from `torch.Generator().manual_seed(j)`, j = 0–3), `ca` (its fp64 norm and SHA-256; it must be exactly zero), and **`upd_precast`**, the fp32 update before the dtype cast and add of `:216–217`. For science captures only, request order and subjects are frozen as `H.FICTION` and asserted, after the LAW#5 tag check above. Tensors are stored in their native dtypes.
- **Conversion contract (MPS audit).** Every capture is `t.detach().cpu().clone()`: **a same-dtype transfer first**, so there is never a combined device-and-dtype conversion. Any cast happens afterwards, on CPU. Comparison norms are computed in CPU float64. The observer never writes into `f_locals`.
- **Observer self-validation (a build self-test, before any harvest).** On MPS tensors that include offset and non-contiguous views (`x[1:]`, `x[0, -1]`, `chunk` pieces after the first, and a transposed view), the capture must be bitwise equal to a reference `.cpu()` of the same view. The MPS source must be bitwise unchanged after capture, verified by a second `.cpu()` copy compared with `torch.equal`.
- **Inertness parity trial (a harvest gate, LAW#5).** For the reference arm (A7), with `Z_OVERRIDE` fixed to its harvested `zs`:
  1. Trial U: restore the band weights from the pristine `snap_layers` snapshot (`:150–152`, `:155–159`) and make a **fresh zero cache**, then call the original `my_edit` object directly, **without** the observer. Capture the band weights (`.cpu()`, same dtype).
  2. Trial O: restore again and make a fresh zero cache again, then call through `observed_my_edit` **with** the observer, and capture.
  3. Restore.

  **PASS requires** Trial O to have produced exactly five ordered science captures (zero or any other count is FAIL), **and** `torch.equal` on every band layer's weights. Otherwise, the relative Frobenius difference of the applied deltas `(W − W_pristine)` is ≤ 1e-6 in fp64 on every layer, and which branch passed is recorded. **FAIL: HALT.** `H.run_law5` must also report INERT with the observer installed (`|Δexpr| < 0.05` and `|Δloc| < 3`, `:444`).

### 2.4 Gates (each failure is a HALT with `architecture_profile/mathlab_harvest_halt_diagnostic_<UTC>.json`)

1. Admission (§2.1).
2. The context pin (§2.2).
3. LAW#5 inertness: the harness gate plus the parity trial (§2.3).
4. **LAW#3 known baseline**, from the contemporaneous evaluation. A7 must fall inside the envelope: `para_full` in [5, 18]/72, `para_first` in [42, 59]/72, canon in [5, 10]/24 (`CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:39`). A1 must be ≥ 68/72, the A1 floor (`CORPUS/54_C10U_MINT2.md:68`). A2 must also be ≥ 68/72; **this is the floor chosen by this pre-registration**, not a cited A2 threshold (the historical A2 is ≥ 70, `CORPUS/44:21`). A miss is a HALT, and no operand from that run is used. This gate must pass before any mint replay (§2.2 stage order).
5. Budget (§2.6).
6. Free memory ≥ 8 GiB at each stage boundary.

### 2.5 Contents (`results/mathlab/harvest_<UTC>/`, a new directory, never overwritten)

Each file is a flat dict of CPU tensors saved with `torch.save` and loadable with `weights_only=True`. `manifest.json` records:
- SHA-256, shape and dtype for every file;
- the fingerprint, git commit and torch version (2.8.0);
- the context digests and the source-file hashes from §2.2;
- every gate outcome, every identity-check value, and the observer self-test record.

The files:
- **`clean.pt` (unedited model).** For every prompt in CANON(24), PTEST(72), described_as(24), L1(12) and L3(30): the down_proj input (11008, fp16) and the block output (2048, fp16) at layers 4–8 at **every** token position, captured by a forward pre-hook on `model.model.layers[l].mlp.down_proj` and a forward hook on `model.model.layers[l]`. Also the token ids and the `subject_last` index. **Batching is frozen to one prompt per forward with no padding**, as `tok(prompt, return_tensors="pt")`, which matches the evaluation path (`:101–117`). Also the per-template subject-last keys behind `compute_ks`, read through the engine's own `get_module_input_output_at_words` exactly as the harness calls it.
- **`inloop_<arm>.pt` (all six arms).** Per layer, the §2.3 capture. `upd_precast` itself is kept only for A7; the other arms keep its SHA-256 and fp64 norm.
- **`weights_A7.pt`.** The band weights before and after the A7 write, fp16, captured `.cpu()` at the same dtype. Their difference is the **effective deployed change**. It differs from `upd_precast` by the fp16 cast-and-add rounding of `:217`.
- **`postedit_<arm>.pt` (diagnostic).** Captured by an `ARM_HOOKS` entry, or directly after a mint replay, before restore. It holds the layer-8 block output at every CANON and PTEST position and the post-edit subject-last keys at layers 4–8, with the same batching as `clean.pt`.

**Size (estimate; the manifest records actual sizes):** `clean.pt` ≤ 0.34 GB, in-loop files ≈ 6 × 6 MB, `upd_precast` for A7 ≈ 0.45 GB, `weights_A7.pt` ≈ 0.45 GB, post-edit files ≈ 6 × 6 MB. **Total ≲ 1.4 GB** against 117 GiB free on `/Volumes/memit` (`df`, 2026-10-08).

### 2.6 GPU budget (estimates; the caps are binding)

Process cap 3,600 s. Stage caps, in seconds:
- setup, gates and the parity trial: 900
- clean pass: 300
- `run_recipe` for three arms (targets, writes, evaluation): 1,800
- three operand-only mint replays, run only after the fresh arms' LAW#3 pass, including the §2.2 CPU tokenisation contract: 300
- post-edit captures: 300

A stage whose projected end crosses the process cap is refused (HALT-BUDGET), with its projection inputs recorded.

## 3. Step 2 — offline solve reproduction (marimo, CPU only)

**Notebooks:** `mathlab/m2_solve_repro.py`, and `mathlab/m3_calibration.py` for §4. Both are plain-`.py` marimo notebooks following the `marimo-notebook` skill, with parameters in one pydantic model per the `marimo-batch` skill. **Frozen PEP 723 dependency set:** `marimo`, `duckdb`, `pydantic`, `psutil`, `numpy`, and `torch==2.8.0`, which must equal `.venv`'s version; the notebook asserts this. **Headless invocation, launched only through §6's runner:** `uv run --script mathlab/m2_solve_repro.py`. Nothing is installed into `.venv`. The build's self-test runs this exact invocation once on synthetic inputs and records the result. The notebooks read only the harvest directory and the covariance files, and they never touch MPS.

**Gate 2a — exact reproduction (PASS / FAIL, binding).** Recompute `P[i]` with `compute_P`'s exact operations (`c10e_bandknob.py:169–175`). Then, for every arm and layer, replay the harness's fp32 operations (`:205–211`) on the harvested `Kf`, `rf` and `ca`. **PASS** requires all three:
1. **Projector match.** The null-space count matches, and either the projector SHA-256 matches or every probe satisfies `‖P_off v_j − P_h v_j‖ / ‖P_h v_j‖ ≤ 1e-6`.
2. **Full-tensor match (A7).** `‖upd_off − upd_precast‖_F / ‖upd_precast‖_F ≤ 1e-5` per layer.
3. **Norm match (other five arms).** The fp64 norm of the replayed update agrees with the harvested norm to ≤ 1e-5 relative per layer.

The 1e-5 tolerance is set for a **replay of the same CPU fp32 solve from identical operands**. Whether it is attained is unverified until run. A float64 variant and `cond(A)` per layer are recorded only as diagnostics; there is no fp32-versus-fp64 tolerance. **FAIL:** under the halt discipline, one diagnosis after a `cat -n` read of the relevant source. If that one fix does not clear 2a, the lab STOPS (§8).

**Gate 2b — the additive-residual approximation (a scope gate; it never stops the lab).** Re-solve the band from **clean** operands only:
- `K_i^clean` is the clean `compute_ks` average.
- `cur^{(i)} ≈ cur^{(0)} + Σ_{j<i} upd_j K_j^clean`.

Compare the result with A7's `upd_precast`.
- **ALT-SOLVES-ADMITTED:** every layer has relative Frobenius error ≤ 0.25 and cosine ≥ 0.95. Step 4 may then evaluate alternative solves offline, each labelled first-order.
- **OPERANDS-ONLY:** anything else. Every alternative then needs its own harvest.

The fp16 rounding `‖ΔW_eff − upd_precast‖_F / ‖upd_precast‖_F` per layer is recorded and kept as a named approximation in §4.

## 4. Step 3 — retro-prediction calibration (CPU only)

### 4.1 The two proxies (frozen; no third proxy, no re-tuning after the numbers are seen)

**Inputs.**
- `ΔW_l^a` is arm `a`'s update at layer `l`, replayed offline (valid once 2a passes). It is the pre-cast update; the fp16 cast-and-add rounding is a retained approximation.
- All arithmetic is in **CPU float64**, after a same-dtype `.cpu()` and a CPU `.double()`.
- For prompt `p`, position `t` (one prompt, no padding; `n = len(tok(p)["input_ids"])`, positions `0 … n−1`), the first-order layer-8 change is

  `δh(p, t) = Σ_{l=4..8} ΔW_l^a k_l^clean(p, t)`

  This is the additive-residual approximation. It ignores attention and every later layer's response, which makes it **a proxy, not a prediction of top-1 recall**.
- `s(p)` is the `subject_last` index (`compute_z.py:234–267`). `z_f` is row `f` of the arm's `zs`, in `H.FICTION` order. `h8` is the clean layer-8 block output.

**P-ρ (keyed transfer).** For each of the 72 paraphrases:

  `τ(p) = ⟨δh(p, s), z_f − h8(p, s)⟩ / ‖z_f − h8(p, s)‖²`

The score is `S_ρ(a) = mean_p clip(τ(p), 0, 1)`.

**P-coll (collateral; the H1 bucket of F-D1, `CORPUS/46_C10M_DIAG_READPARTITION_EDITINJECT.md:30`).** For each paraphrase:

  `κ(p) = Σ_{t ∈ {0..n−1} \ {s}} ‖δh(p, t)‖² / ‖δh(p, s)‖²`

The sum covers every real token position except `s`; there is no padding. The score is `S_coll(a) = − median_p κ(p)`, where the median is `numpy.median`, which averages the two central values of 72.

**Invalid arithmetic.** If any denominator is exactly 0, or any `τ`, `κ` or score is non-finite, the arm's proxy is **INVALID-ARITHMETIC**, and that proxy fails calibration. There is no row exclusion and no epsilon.

### 4.2 Calibration arms and outcomes (held-out `para_full`, binding count /72)

Fresh and historical counts sit in **separate columns**. **Only the "used for calibration" column enters §4.3.** The historical column is reported, never combined with the fresh count, and never averaged with it.

| Tier | Arm | Used for calibration | Fresh harvest count | Historical count (reported only) | Source of the historical count |
|---|---|---|---|---|---|
| top | A1_single | fresh | measured in the harvest; LAW#3 floor ≥ 68 | 68–72 across runs; 68 in block F | `CORPUS/45_C10L_MINT_TOKEN.md:1`; `CORPUS/54_C10U_MINT2.md:68` |
| top | A2_coherent2 | fresh | measured in the harvest; this pre-registration's floor ≥ 68 | ≥ 70 | `CORPUS/44_C10L_COVGEOM_SPARSEBAND.md:21` |
| middle | mint-1 seed 0 | historical, if admitted under §2.2 checks 1–4 | — (operand-only replay) | 46 | `CORPUS/54_C10U_MINT2.md:26`; `F_r0_mint1_s0.json` `/arm/para_full_binding_n` |
| middle | mint-1 seed 1 | historical, if admitted | — | 37 | `CORPUS/54_C10U_MINT2.md:27`; `F_r0_mint1_s1.json` |
| middle | mint-1 seed 2 | historical, if admitted | — | 40 | `CORPUS/54_C10U_MINT2.md:28`; `F_r0_mint1_s2.json` |
| bottom | A7_coined_coined | fresh | measured in the harvest; LAW#3 envelope [5, 18] | 14 in block F; 8–15 across five observations | `CORPUS/54_C10U_MINT2.md:25`; `F_r0_multi_snone.json`; `CORPUS/44:32`, `:39` |

**Tier validity is checked on the actual outcomes before scoring.** It requires `min(top) − max(middle) ≥ 10` and `min(middle) − max(bottom) ≥ 10`. Otherwise the step is **INVALID-TIERS**: no verdict, and the case goes to the operator. The LAW#3 gate makes these margins at least 22 and 19. Orderings *within* a tier are reported and never gate: mint 46 > 40 > 37 is seed-sensitive (CORPUS/46 F-D4, `:33`), and A1 vs A2 sit within the per-process spread of ±3–5/72 (`CORPUS/44:41`).

### 4.3 Pass criterion (fixed before any computation)

A proxy **passes** when both conditions hold:
1. **All orderings, strictly.** Every top arm scores `>` every **admitted** middle arm, and every admitted middle arm scores `>` A7, on the point estimate. With all three mint arms admitted, that is 6 + 3 = nine orderings. With exactly two admitted (§2.2, per-arm INVALID-REPLAY), it is 4 + 2 = six orderings; the chance level under a random ranking of five arms is then 2!·2!·1!/5! = 1/30.
2. **Paired subject bootstrap.** The generator is `numpy.random.Generator(numpy.random.PCG64(0))`. For each of `b = 0 … 1999`, draw once `idx = rng.integers(0, 24, size=24)` (24 subject IDs with replacement) and share that draw across all arms and both proxies. For each arm, recompute the original statistic over the 72 paraphrase values `[(f, j) for f in idx for j in 0, 1, 2]`, keeping multiplicities: S_ρ as the mean of the clipped τ, S_coll as minus `numpy.median`. Use strict `>`. **Each required ordering must hold in ≥ 1,900 of 2,000 resamples.**

**The lab passes calibration when at least one proxy passes.** The result is **INVALID** (neither PASS nor FAIL, and the case goes to the operator) when any of these holds:
- a shared tokenisation or context check fails (§2.2 check 2 or 3), making all mint arms INVALID-REPLAY;
- fewer than two mint arms are admitted;
- the step is INVALID-TIERS;
- both proxies are INVALID-ARITHMETIC.

A single per-arm INVALID-REPLAY does **not** invalidate calibration; it moves the criterion to the six-ordering form above. *Note:* 1/60 per proxy (2!·3!·1!/6!), or ≤ 2/60 for two proxies with all six arms, is the combinatorial probability of the required orderings under a **uniformly random ranking**. In the reduced five-arm case it is 1/30 per proxy (2!·2!·1!/5!) and **≤ 2/30 for two proxies**. Neither figure is a calibrated false-positive rate, because the mint seeds are correlated and the arm families were chosen deliberately. **Admission is independent of proxy scores.** Whether a mint arm is admitted is decided solely by §2.2's checks 1–4, which are computed and recorded **before** any proxy is evaluated. No proxy value may influence admission, exclusion or the choice between the nine- and six-ordering rules.

**Consistency checks (non-gating, never evidence).**
- **Injection versus write:** the target injected into the unedited model (49/72, `CORPUS/44:23`; 51–54/72, `CORPUS/46:34`) against the write's 8–15/72. P-ρ agrees with this **by construction**, since an injected `z` has `τ = 1`, so it calibrates nothing.
- **The edited-model injection** (23/72, `CORPUS/46:30`) lies downstream of the edited layers. P-coll's value is recorded beside it.

**FAIL (neither proxy passes):** the lab STOPS (§8). An amended proxy needs a written amendment and calibration on arms **not** used here, such as the next GPU results, or CORPUS/45's G 39/72 and A1-rare 25/72 (`CORPUS/45_C10L_MINT_TOKEN.md:8`, `:29`). Re-scoring these six arms is not a calibration.

## 5. Evidence tier, outputs, and the DuckDB index

- **Label.** Every output and staged note carries `MATH-PROXY`. It may reorder or prune the GPU queue: an arm rated "no movement" may be deprioritised, never closed, and only after a pass *and* a demonstration of prospective utility (§0). Nothing enters `CORPUS/` above `I-INFER (MATH-PROXY)`.
- **Staging.** Outputs go to `results/mathlab/<step>_<UTC>/` with SHA-256 manifests. Findings, including any stop under §8, are **staged immediately** as `logs/pending_findings/NN_mathlab_<unit>.md` (`AUTONOMY.md:25`). The canonical close-out (`tools/closeout_check.py D-ML-1`, CORPUS, ledgers) happens **later, at the supervised fold-in by the lead** (`AUTONOMY.md:25–27`). The lab itself never writes `CORPUS/`, ledgers, the runbook or the checkpoint.
- **DuckDB, a derived index and never an authority.** `results/mathlab/calibration.duckdb` is built by one cell under the frozen dependency set, using `read_json` over the cited records and the harvest manifest.
  - Each row carries arm, block, run, metric, value, source path, JSON pointer, and the source file's SHA-256.
  - The index is **rebuilt from scratch, never edited**.
  - When it disagrees with a source file, the source wins and the index is rebuilt.
  - Citations never name the index.

## 6. Resource rules and bounded execution (CPU notebooks)

- **Runner: `tools/run_mathlab_cpu.sh <notebook> <deadline_s>`** (new, shell).
  - **Admission.** The runner first runs `mathlab_admit.py --kind cpu`. This applies the same `check_gpu()` (`tools/c10w_p2_gate.py:73–84`), because the notebook is a non-exempt python that would itself block a gated GPU dispatch (`:22`). Its result is handled **fail-closed**, in this order:
    1. **Probe errors are unconditional refusals.** A result carrying `reason` refuses, with no exception. That covers a failed or empty process inventory (`:75–77`) and a tmux inventory error other than tmux's exact "no server running" (`:79–82`).
    2. **An autoresearch session is an unconditional refusal.** A non-empty `blocking_tmux` (`:83`) refuses.
    3. **The coordinator-tail exception** applies only after **successful** collection of both inventories, with `blocking_tmux` empty and every line of `blocking_processes` (`:78`, `:84`) **accounted for one-to-one** in the lead-written admission record. Each entry names the exact pid and command line, its coordinator, and that coordinator's status file with SHA-256, which `mathlab_admit.py` re-hashes. The status file must show the coordinator is **past its last gated stage**. Any unaccounted process, a pid or command mismatch, a hash mismatch, or a status not past the last gated stage refuses.

    The **harvest** (`--kind harvest`, §2.1) has **no** exception: any `check_gpu()` refusal refuses.
  - **Execution.** The runner then executes `nice -n 10 /opt/homebrew/bin/timeout -k 30 <deadline_s> uv run --script <notebook>`. **Hard deadlines:** m2 2,700 s, m3 1,800 s, index build 300 s.
- **Memory.**
  - **Watchdog.** The runner samples available memory every 5 s, as free + inactive + speculative pages × 16,384 from `vm_stat`. It kills the notebook if available memory drops below **6 GiB**. That run ends as STOPPED-RESOURCE.
  - **Pre-cell admission.** Before each heavy cell, the notebook requires available ≥ 8 GiB **plus** that cell's reserve: **4 GiB** for each 11008² SVD (input, U and Vh at 0.485 GB each plus LAPACK workspace, conservatively ≈ 3.4 GB), **2 GiB** for loading harvest files, **1 GiB** for the bootstrap. If memory is short, it re-checks every 10 s for **at most 300 s**, then ends as STOPPED-RESOURCE.
  - **Limits on aborts.** A STOPPED-RESOURCE or STOPPED-DEADLINE run is staged, and it is not a lab stop. A third such abort on the same step goes to the operator.
  - **Estimates.** The ≤ 6 GiB peak and the deadlines are estimates. The build measures peak RSS on synthetic tensors of the same shapes and raises a reserve if the measurement exceeds it, before freeze-confirmation.
- **CPU only.** Torch threads are fixed at 8 of 16. No tensor ever goes to MPS.

## 7. InfraNodus — the source of step-4 candidate questions (operator request 2026-10-08; outside steps 1–3)

InfraNodus is the planned source of **candidate questions** for step 4. A structural gap audit over `CORPUS/` (the `infranodus-gap-audit` skill) looks for topics that are each discussed heavily but never connected to each other. Another agent is running it separately, as a trial (`results/mathlab_staging/infranodus_trial/`); this pre-registration does not run it.
- Its output is **candidate questions only**.
- Each candidate must pass its own written pre-registration and the math-lab gate (MATH-PROXY tier, a calibrated proxy, §4) before it can claim GPU time.
- A gap is never evidence and never, by itself, a hypothesis-register entry.
- Sending corpus text to the InfraNodus service is an outward-facing action the operator authorised for that trial. It is not re-authorised here.

## 8. Stop rules

The lab **STOPS**, and the stop is **staged immediately** (§5) and folded in later by the lead through the close-out gate, when any of the following happens:
1. **Gate 2a fails** after the single allowed diagnosis.
2. **Calibration FAILs** (§4.3).
3. **The harvest HALTs twice** on the same gate. This goes to the operator under the drift-cap convention, not a third launch.

**INVALID outcomes** (INVALID-REPLAY, INVALID-TIERS, INVALID-ARITHMETIC in both proxies) are neither PASS nor FAIL; they go to the operator. Gate 2b never stops the lab. A stop leaves the harvest directory in place as an archive.

## 9. Corrections to the brief (checked against the files on 2026-10-08)

1. **"ΔW = R Kᵀ(λC + K Kᵀ)⁻¹."** The C10 arms write through the harness's null-space-projected ridge solve, `upd = solve(P(K Kᵀ) + I, P K Rᵀ)ᵀ` (`c10e_bandknob.py:205–211`). The λC form is the engine's and runs only in the LAW#5 check (`:423`). The solve is sequential, so exact reproduction needs in-loop operands.
2. **The audit snapshots** are OverTone target-solve snapshots, 6 × 151936 (A1) and 24 × 151936 (A7), with no ΔW and no keys.
3. **"Mint 39–46/72."** That is CORPUS/45's two inits (G 39, N 46; `CORPUS/45:8`). Across seeds the same recipe spans 34–46 (`CORPUS/46:22`; block F 46/37/40, `CORPUS/54:26–28`).
4. **"Injection 49–61/72."** 61/72 is the PASS bar (`CORPUS/02_VANDV_CHAIN.md:179`). Measured injection into the unedited model is 49, 51–54 and 51/72 (`CORPUS/44:23`, `CORPUS/46:34`, `CORPUS/51:12`); a recomputed target gave 55/72 (`CORPUS/46:32`); the shared target gave 69/72 (`CORPUS/51:12`). Injection into the edited model gave 23/72 (`CORPUS/46:30`).
5. **"A7 12/72."** That is the unfinished C10X re-run 3 log line. The sourced values are 14 in block F, 8–15 across observations, and the envelope [5, 18].
6. **"A1/A2 ≈ 70."** A1 is 68–72 (68 in block F); A2 is ≥ 70.

## 10. Review route and scope

- **Freeze:** DONE. Astra confirmed v4 with FREEZE in round 4; the coordinator sent the packets. Records go under `results/mathlab_staging/`.
- **Build after freeze:** the launcher, the admission check, the harvest driver with its observer, and the two notebooks, by a Codex session under the test-first one-round convention. The self-tests are the observer validation (§2.3), the headless-invocation and peak-RSS measurement (§3, §6), and the identity-check unit tests on the frozen hashes (§2.2). Nothing GPU-side runs until the build passes **and** the admission record exists.
- **Out of scope:** step 4, the autonomous loop. It gets its own pre-registration, written only if §4 passes, with its scope set by gate 2b and its candidate questions from §7.

## 11. Fold log — Astra r1 (`results/mathlab_staging/prereg_astra_r1.md`, FIX-FIRST)

| Item | Disposition | Where / how |
|---|---|---|
| **B1** Wrappers cannot capture `zs` / `resid`; the second key pass is indistinguishable; the cache is not reset | FOLDED | §2.3. The pass-through wrappers are replaced by a read-only `sys.setprofile` observer, installed through a lab-side rebinding of `H.my_edit` that calls the original unchanged (precedent `c10x_enginepath_arms.py:467–473`) and confined to the harvest process. It fires only on `my_edit` → `upd_matrix_match_shape` calls (`:212`). It captures `zs`, `K`, `Kf`, `rf`, `resid`, `cur`, `i`/`layer`, projector identity, `ca` and the pre-cast update together. The second pass (`:218–220`) cannot match. Request order and native dtypes are frozen. Every arm and both parity trials start from restored weights **and a fresh zero cache**. The parity trial is a gate. |
| **B2** The historical-context fallback is incompatible with `pinned_contexts`; historical run identity is incomplete | FOLDED | §1 (context facts, block F identity data) and §2.2. The lab-local pin takes an explicit expected digest; `/ctx`, the `json_digest` serialization (`c10u_mint2_read.py:29–30`), and file and target SHA-256s are frozen; subject-to-row mapping is `H.FICTION` (`c10u_mint2_arms.py:187–188`). Calibration uses **contemporaneous** outcomes for A1, A2 and A7, and **historical** outcomes for the mint replays only after four identity checks: source, context, tokenisation, and per-layer norm agreement ≤ 1e-3 with `/recipe/delta_norms/candidate`. |
| **B3** The conversion contract is unsafe | FOLDED | §1 (MPS hazard) and §2.3. Captures are `detach().cpu().clone()` with CPU casts afterwards; norms are computed in CPU fp64; the observer self-test covers offset and non-contiguous views and checks the source is unchanged. The 1e-5 tolerance is scoped to a same-fp32 replay, and fp64 stays diagnostic (§3). |
| **B4** Proxy implementation choices left open | FOLDED | §2.5 (clean batching frozen to one prompt per forward, no padding, matching `:101–117`) and §4.1 (positions `0..n−1` without `s`, `numpy.median`, fp64 arithmetic, INVALID-ARITHMETIC instead of exclusion or epsilon). §4.3 freezes the bootstrap: PCG64(0), paired subject draws, multiplicities kept, strict `>`, ≥ 1,900 of 2,000. |
| **B5** Launch isolation and resource enforcement | FOLDED | §2.1: an external pre-import launcher; `W` explicit; `mathlab_admit.py` reuses `c10w_p2_gate.check_fingerprint` and `check_gpu` only, with no P2 dispatcher and no fabricated stage; lead-written queue admission evidence is re-hashed. §6: hard deadlines through `timeout`, a 6 GiB kill watchdog, a per-cell reserve above the 8 GiB floor, bounded 300 s waits, and an abort count. |
| **A1** Clarify stop staging versus closeout | FOLDED | §5 and §8: stops are staged immediately; the canonical close-out happens at the supervised fold-in (`AUTONOMY.md:25–27`). |
| **A2** 1/60 is not a calibrated false-positive rate | FOLDED | §4.3 note. |
| **A3** Narrow the promised predictive use | FOLDED | §0: "passes retrospective tier discrimination; prospective queue-ranking utility remains unverified". §5 makes any deprioritising conditional on demonstrated prospective utility. |
| **A4** Distinguish the solved update from the deployed change | FOLDED | `upd_precast` is named (§2.3), the effective change is recorded through `weights_A7.pt` (§2.5), and the fp16 rounding is measured (§3) and retained as an approximation (§4.1). |
| **A5** Audit shape | FOLDED | §1 and §9: 6 × 151936 (A1) and 24 × 151936 (A7). |
| **A6** Runtime recipe incomplete; estimates | FOLDED | §3 freezes the PEP 723 set (marimo, duckdb, pydantic, psutil, numpy, torch==2.8.0) and a `uv run --script` headless invocation tested in the build; §2.6 and §6 label the time and memory figures as estimates with binding caps. |

No item was rejected.

## 12. Fold log — Astra r2 (`results/mathlab_staging/prereg_astra_r2.md`, FIX-FIRST; B3 and B4 RESOLVED)

| Item | Disposition | Where / how |
|---|---|---|
| **B1** The caller predicate named the rebound `H.my_edit` | FOLDED | §2.3. `ORIGINAL_EDIT`, `EDIT_CODE` and `SHAPE_CODE` are saved **before** rebinding (precedent `c10x_enginepath_arms.py:468`, `:473`). A capture needs `frame.f_code is SHAPE_CODE` and `frame.f_back.f_code is EDIT_CODE`; the return event uses `EDIT_CODE` too. Each science write needs exactly five ordered captures plus one return; any other count, including zero, HALTs, and the parity trial's PASS requires five. The LAW#5 tag (`H._LAW5_DEFAULT_CTX`, `c10e_bandknob.py:430–433`) is checked **before** the 24-subject assertion, which applies only to science captures. |
| **B2** The historical `input_ids` / `subject_last` fields do not exist | FOLDED (Astra's first option) | §1 records what exists: the P2 audit (`F_r0_mint1_s0.json:953–1008`, writer `c10u_mint2_arms.py:210–256`) and `/minted_ids`. §2.2 check 3 is now an explicit equivalence contract: (a) pinned tokenizer identity with file hashes; (b) a minted tokenizer reconstructed through the writer's own `register`; (c) the recorded P2 audit re-derived by the writer's own `p2_audit` and required to match every recorded field (**corrected in v4:** the v3 text fed it the wrong inventory, `all_harness_prompts`; see §13 B2); (d) the lookup-routine substrings checked across both tokenizers. The indices are labelled `RECONSTRUCTED`, never `RECORDED`. **Mismatch consequence:** a failure in (a)–(d) is shared by all three mint arms, so all become INVALID-REPLAY and calibration is INVALID. A per-arm, seed-specific check fails only that arm, and calibration continues on ≥ 2 admitted mint arms under the six-ordering rule (§4.3). Making every shared failure per-arm would not be defensible, because a shared failure carries no seed-specific information. |
| **B5** The CPU exception could override inventory-probe errors | FOLDED | §6 admission is fail-closed in order: any `check_gpu()` probe error (`c10w_p2_gate.py:75–82`) refuses unconditionally; a blocking autoresearch session (`:83`) refuses unconditionally; the coordinator-tail exception applies only after both inventories succeed, with every blocking process accounted for one-to-one (pid, command, coordinator, re-hashed status file past its last gated stage). The harvest has no exception. |
| **ADV** Separate fresh and historical counts | FOLDED | §4.2 has separate columns, and only the "used for calibration" column enters §4.3. |
| **ADV** Norm agreement is not identity | FOLDED | §2.2 check 4 and the harness-arm bullet call it a "consistency check on norms, not tensor identity"; the "second, consistent observation" wording is removed. |
| **ADV** A2 ≥ 68 is this pre-registration's floor | FOLDED | §2.4 gate 4 and §4.2: `CORPUS/54:68` is cited for A1 only, and A2 ≥ 68 is stated as the chosen floor. |
| **ADV** Finish fresh baselines before admitting mint data | FOLDED | §2.2 stage order (binding), §2.4 gate 4, and §2.6's mint stage, which runs only after the fresh arms pass LAW#3. |
| **Citation** Candidate norms start at `:8027` | FOLDED | §1 now cites `F_r0_mint1_s0.json:7999–8052` (`A1_single` from `:7999`, `candidate` from `:8027`). |

No item was rejected.

## 13. Fold log — Astra r3 (`results/mathlab_staging/prereg_astra_r3.md`, FIX-FIRST; B1 and B5 RESOLVED; B3 and B4 still resolved)

| Item | Disposition | Where / how |
|---|---|---|
| **B2** `p2_audit` was fed the wrong inventory (`all_harness_prompts`), so 396 / 2,376 could not match | FOLDED (Astra's required replacement) | §2.2 check 3(c) now takes `prompts, countries, capitals = c10u_mint2_arms.audit_prompts(H, M, W)` (`:273–282`) and passes `prompts` to the original `p2_audit`, mirroring the writer's caller (`:791–794`). The frozen inputs and the recorded-field comparisons are preserved, and **the required counts are not lowered**. New: every source that call reads (the three writer and harness `.py` files and both screen configs) must match the record's `/identity/source_sha256`; all five matched on 2026-10-08. §1's inventory description is corrected (`:47` in v3). The round-2 B2 fold row in §12 is annotated as corrected. |
| **ADV** The two-proxy caveat in the reduced case; admission independent of proxy scores | FOLDED | §4.3 note: ≤ 2/30 for two proxies in the five-arm case (1/30 per proxy), with neither figure a false-positive rate. Admission is decided by §2.2's checks 1–4 alone, recorded before any proxy is computed, and no proxy value can affect admission, exclusion or the choice of the 9- or 6-ordering rule. |
| **Citation** `c10l_mint_lib.py:24–27` → `:24–37` | FOLDED | §2.2 check 3(b) cites `:24–37` (flags, exact added count, contiguous spare-id assertion, per-word single-id round trip) and the writer's replay requirement (`c10u_mint2_arms.py:787–790`). |
| **Editorial** `:302` still said v2 | FOLDED | §10 now says "Astra confirmation of v4"; the status header is updated to v4. |
| **ADV** (no action) B1 stdlib probe passed; B2's remaining design is defensible; six orderings are a meaningful screen; earlier folds survive | NOTED | No text change. Empirical tensor and behavioural inertness remains UNVERIFIED until the harvest runs (§2.3 gate). |

No item was rejected.
