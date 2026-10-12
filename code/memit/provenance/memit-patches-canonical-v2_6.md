# MEMIT Patches — Canonical Specification — v2.6 Amendment

> **Amendment status:** ADDITIVE to `memit-patches-canonical v2.5`. §1–§10 of v2.5 are preserved verbatim. v2.6 adds ONE new patch entry (`P-VRAM-CPU-SOLVE`) as a **conditional SOURCE_LAYER patch** and updates the §1 inventory, §7 application order, §8 manifest schema, and §9 upstream notes to reflect its addition. No existing-content edits to v2.5 §1–§9; the §10 Process Constraints gain one constraint (C-S232-CPUSOLVE-1).
>
> **Version:** 2.6 (supersedes v2.5 — adds `P-VRAM-CPU-SOLVE` conditional SOURCE_LAYER patch; provenance: S2.31 authoring + S2.32 codification + empirical re-validation)
> **Provenance:** `P-VRAM-CPU-SOLVE` authored S2.31 (VRAM-forced; isolated + exonerated against the Llama-3.1-8B ceiling per framework_finding v1.5 §4); codified to canonical S2.32 per the S2.32 kickoff deliverable + D-S231-PATCH-1. Empirically re-validated S2.32 (re-applied to pristine engine, fingerprinted, drove both the Qwen CLEAR and the Mistral re-confirm without numerical artifact).
> **Target codebase:** `kmeng01/memit` at SHA `80426fd9316cf9a50c5ba15e0912f2c2c5bfe84b` (unchanged)

---

## §3.9 — P-VRAM-CPU-SOLVE (NEW conditional SOURCE_LAYER patch)

### §3.9.1 Classification

| Property | Value |
|---|---|
| Patch ID | `P-VRAM-CPU-SOLVE` |
| Class | **SOURCE_LAYER** (fixes a resource-allocation behavior in the engine source; distinct from CONFIG_LAYER globals.yml patches) |
| Conditionality | **CONDITIONAL** — required only when the target model's `intermediate_size` inflates the MEMIT float64 linear solve past available VRAM headroom on the deployment GPU. Threshold: intermediate width ≳ 18k on a 24 GiB RTX 4090 alongside a resident 7B+ fp16 model. No-op-by-omission on narrower models (Llama-3.1-8B 14336, Mistral 14336, Llama-3.2-3B 8192 — all fit the GPU float64 solve). |
| Target file | `memit/memit_main.py` (`execute_memit`, ~L196 in the pinned SHA) |
| Numerical status | **NUMERICALLY INERT** — float64 CPU solve == float64 GPU solve for a well-posed system. Isolated + exonerated (§3.9.4). |
| Universality | NOT universal-safe-by-default; it is correctness-neutral but moves a large allocation off-GPU, so it is applied conditionally to avoid unnecessary CPU↔GPU transfer cost on models that do not need it. |

### §3.9.2 Motivation

MEMIT's per-layer update solves a linear system `A x = b` where `A = mom2_update_weight * cov.double() + layer_ks @ layer_ks.T`. The `cov.double()` term is the per-layer covariance second-moment promoted to float64; its size scales with `intermediate_size²`. For Qwen2.5-7B (`intermediate_size=18944`), `cov.double()` is ~2.67 GiB. On a 24 GiB RTX 4090 already holding the ~15 GiB fp16 model plus edit-time activations, allocating a fresh 2.67 GiB float64 tensor on-GPU OOMs at `torch.linalg.solve`. The edit cannot dispatch on the unmodified engine.

**Single-layer scope reduction does NOT mitigate** (D-S231-SCOPE-1): the allocation is a single per-layer float64 tensor, not a layer-count-driven aggregate. Reducing the band from 5 layers to 1 does not shrink the per-layer solve. The correct mitigation is solve-*location* (CPU), not solve-*scope*.

### §3.9.3 The patch (exact replacement text)

**Pre-patch (pristine, `memit/memit_main.py` ~L196, in `execute_memit`):**
```python
        adj_k = torch.linalg.solve(
            hparams.mom2_update_weight * cov.double() + layer_ks @ layer_ks.T,
            layer_ks,
        )
```

**Post-patch:**
```python
        # P-VRAM-CPU-SOLVE (S2.31): CPU-offload the float64 linear solve.
        # Move operands to CPU BEFORE the arithmetic so the intermediate**2 float64
        # tensor is born in system RAM, never VRAM. Numerically inert: float64 CPU
        # solve == float64 GPU solve. Required for wide-intermediate models (>=~18k)
        # whose cov.double() exceeds 4090 headroom alongside a resident 7B+ model.
        _cov_cpu = cov.cpu().double()
        _lk_cpu = layer_ks.cpu()
        _A = hparams.mom2_update_weight * _cov_cpu + _lk_cpu @ _lk_cpu.T
        adj_k = torch.linalg.solve(_A, _lk_cpu).to(layer_ks.device)
        del _cov_cpu, _lk_cpu, _A
```

**Load-bearing authoring note (the v1→v2 patch error, recorded for any re-derivation):** the operands MUST be moved to CPU *before* the arithmetic. The first patch attempt (`(hparams.mom2_update_weight * cov.double() + ...).cpu()`) still allocated the float64 tensor on-GPU before `.cpu()` ran, and OOM'd identically. The corrected form casts/moves each operand first (`cov.cpu().double()`, `layer_ks.cpu()`), so no float64 GPU allocation ever occurs. `adj_k` returns to the original device for the downstream weight write.

### §3.9.4 Confound isolation + exoneration (load-bearing — why a SOURCE_LAYER science-path patch is trustworthy)

Because `P-VRAM-CPU-SOLVE` modifies the science-bearing edit path and was first introduced in the same session that produced the anomalous Qwen CLEAR, it was isolated against a known result before any verdict promotion (the discipline now codified as C-S231-2 / t_branch v1.4 §6''''):

**Isolation control (S2.31):** Llama-3.1-8B (most-confirmed ceiling, 7 axes), Bo Jackson→guitar, canonical hparams, run BOTH engine paths:

| Run | Engine path | post-edit P(guitar) | Verdict |
|---|---|---|---|
| A | patched (CPU-solve) | 7.9053e-08 | ceiling held (floor) |
| B | pristine (GPU-solve) | 1.0697e-05 | ceiling held (floor) |

Both hold the Llama ceiling at the floor; per-layer `upd norm` and `z error` match across A/B to ~3 sig figs (L4 upd 0.2638 vs 0.2655; z error 5.2070 vs 5.2069). The patch is **provably equivalent** on the configuration where the ceiling is most over-determined — it cannot manufacture a CLEAR.

**S2.32 re-validation (both directions):** the same patched engine (a) drove the Qwen CLEAR (5/5, stable ×4) AND (b) reproduced the Mistral-7B-v0.3 ceiling at 0/5 (S2.29-identical config). The patch manufactures neither a clear nor a hold — it is inert with respect to the science. Confound thread closed both sides.

### §3.9.5 Application + verification

- **Apply:** the canonical patch file `cpu_solve_patch.diff` is in `diff -c` **normal format** (NOT unified). Apply with `patch -p0 memit/memit_main.py < cpu_solve_patch.diff` — `git apply` rejects normal-format diffs with `error: unrecognized input` (C-S232-1).
- **Verify live:** `grep -c "_cov_cpu" memit/memit_main.py` returns **3** when the patch is live (the three operand-bearing lines); `0` when pristine. The old GPU-solve line `hparams.mom2_update_weight * cov.double() + layer_ks` is absent post-patch.
- **Fingerprint:** patched `memit_main.py` SHA-256 `5c0c706a66c385273d0a48ebbb8274a1c31bf3e101ca309e47db9cb8b6c78770`; pristine `186e961633211046379cd594016b9f879741121bee3bb8cf163173c832f75b69`. The five sibling engine files (`compute_z`, `compute_ks`, `rome/layer_stats`, `rome/compute_u`, `util/nethook`) are UNCHANGED by this patch — verify their SHAs are unmodified (P-VRAM-CPU-SOLVE touches exactly one file).
- **Pristine backup:** keep `memit/memit_main.py.upstream_pristine_s<NNN>` per session for the restore point.

---

## §1 — Inventory update (additive)

`P-VRAM-CPU-SOLVE` is added to the patch inventory as the **ninth** named patch (after P-1, P-2, P-4, P-5, P-6, P-7, Pad-Token, Copy-Unmount; with P-3'/Device-Map conditional). It is the **second SOURCE_LAYER patch in the CONFIG_LAYER-vs-SOURCE_LAYER taxonomy** that is conditional on the *model* (intermediate width) rather than the environment (datasets/transformers version). Inventory disposition: **CONDITIONAL — wide-intermediate models only (≳18k on 24 GiB)**.

## §7 — Application order update (additive)

`P-VRAM-CPU-SOLVE` applies to `memit/memit_main.py` independently of P-1/P-2/P-4/P-5/P-6/P-7 (different file region — the `execute_memit` solve, not the cov-compute or module-substitution paths). It has no ordering dependency on the other patches; apply it after the standard patch set, conditionally, when the target model's intermediate width exceeds the GPU float64-solve threshold. On narrow-intermediate models, omit it (no-op-by-omission).

## §8 — Manifest schema update (additive)

The reproducibility-manifest patch-state dict gains an optional `P-VRAM-CPU-SOLVE` key: `{applied: bool, required_by_width: bool, patched_main_sha: str, isolation_exonerated: bool}`. When omitted (narrow model), record `{applied: false, required_by_width: false}`.

## §9 — Upstream notes update (additive)

`P-VRAM-CPU-SOLVE` is a candidate upstream contribution distinct from P-4/P-5/P-6/P-7: it addresses a VRAM-scaling limitation that affects any MEMIT user editing a wide-intermediate model (Qwen-7B class and larger) on a single ≤24 GiB consumer GPU. It is numerically inert and single-file, so it carries cleanly. The CPU↔GPU transfer cost is the only tradeoff (negligible relative to the per-layer optimization), which is why it is conditional rather than universal — narrow-intermediate models pay the transfer cost for no benefit.

## §10.5 — Process Constraint (additive)

**C-S232-CPUSOLVE-1 (in-session science-path-patch isolation discipline).** Any patch classified SOURCE_LAYER that touches the science-bearing edit path (e.g. `P-VRAM-CPU-SOLVE`) MUST be isolated against a known result before any verdict produced under it is promoted — run the patched engine on a known-ceiling Llama config and confirm the known result reproduces (per t_branch v1.4 §6'''' / C-S231-2). A SOURCE_LAYER patch on the solve path is not assumed inert; inertness is demonstrated. (Established S2.31; re-validated both directions S2.32.)

---

**v2.6 amendment RATIFIED S2.32 close 2026-06-15.** ADDITIVE; v2.5 §1–§10 preserved verbatim. Adds `P-VRAM-CPU-SOLVE` as a conditional SOURCE_LAYER patch (wide-intermediate models ≳18k on 24 GiB); numerically inert, isolated + exonerated (framework_finding v1.5 §4), re-validated both directions S2.32. Inventory / application-order / manifest-schema / upstream-notes / process-constraints updated additively.
