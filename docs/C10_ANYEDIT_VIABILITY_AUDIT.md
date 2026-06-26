# C10 AnyEdit Viability Audit

**Date:** 2026-06-26  
**Status:** DONE as code-level audit; NOT empirical evidence; NOT a CORPUS finding.  
**Decision context:** `D-C10h-anyedit-triage` / EV-6.

## Verdict

**PROCEED to prereg + advisor + harness design, with one required correction:** upstream AnyEdit's default `window_size=50` is not a valid primary test of the C10 per-token/window hypothesis. The C10 A7 target values are only 4-6 Qwen2.5 tokens, so `window_size=50` collapses every example to one window.

The viable next design is a harness-side transplant of the official `jianghoucheng/AnyEdit` ARE target-vector/window loop into the local Track C Qwen2.5-3B harness, preserving the local MEMIT/AlphaEdit engine package. The pilot must preregister a small-window primary condition, likely `window_size=1`, plus a default-window diagnostic if useful.

## Scope

This audit answers only whether the AnyEdit code path is plausible enough to draft a prereg and harness. It does not show that AnyEdit rescues C10, and it does not justify a CORPUS entry.

## Evidence Inspected

- `/tmp/AnyEdit` remote verifies as `https://github.com/jianghoucheng/AnyEdit.git`.
- Upstream files inspected:
  - `/tmp/AnyEdit/AlphaEdit_ARE/compute_z.py`
  - `/tmp/AnyEdit/AlphaEdit_ARE/AlphaEdit_ARE_main.py`
  - `/tmp/AnyEdit/AlphaEdit_ARE/AlphaEdit_ARE_hparams.py`
  - `/tmp/AnyEdit/memit_ARE/compute_z.py`
  - `/tmp/AnyEdit/memit_ARE/memit_ARE_main.py`
  - `/tmp/AnyEdit/hparams/AlphaEdit_ARE/Qwen2.5-7B-Instruct.json`
  - `/tmp/AnyEdit/README.md`
- Local files inspected:
  - `configs/hparams/qwen25_3b_memit_hparams.json`
  - local MEMIT hparams / `compute_z` / main solve helpers
  - `experiments/track_c/c10e_bandknob.py`
  - `experiments/track_c/c10g_strength_layer_sweep.py`

## Findings

1. **Repository identity is clean.** The relevant LLM editing repo is `jianghoucheng/AnyEdit`. `DCDmllm/AnyEdit` and RefEdit remain image-editing name collisions and should not feed C10 implementation.

2. **Upstream as-is is not comparable.** AnyEdit documents `pytorch==1.12.1`, `transformers==4.23.1`, and one A100 80G. The local repo is pinned to `transformers==4.51.0`, uses Qwen2.5-3B, and has local MEMIT engine mitigations such as CPU-offloaded solves and covariance dispatch. Do not downgrade or run upstream as evidence.

3. **Dependency compatibility is not the blocker.** The fragile upstream import from `transformers.modeling_attn_mask_utils` succeeds under local `transformers==4.51.0`. The blocker is scientific and harness-level, not an immediate import failure.

4. **The transplant boundary is clear.** The minimal code to adapt is the ARE target construction:
   - tokenize `answer`;
   - split by `window_size` / `overlap`;
   - optimize one delta per window;
   - carry previous window deltas into later-window optimization;
   - return selected target indices plus target vectors.

   This can live in a Track C harness. It does not require editing the engine package.

5. **Local hparams need a wrapper.** Local `MEMITHyperParams` is strict and has no `window_size`, `overlap`, `nullspace_threshold`, or `L2` fields. Do not add those to the engine schema. Use a harness-side wrapper/config or dynamic fields around the loaded local hparams.

6. **Default AnyEdit windowing would miss the C10 mechanism.** Tokenizer-only Qwen2.5-3B check on the A7 coined-coined values:

| condition | value |
|---|---:|
| A7 target token length min | 4 |
| A7 target token length max | 6 |
| A7 target token length mean | 5.5 |
| windows at `window_size=50` | 1 for every value |
| windows at `window_size=1` | 4-6 per value, mean 5.5 |
| windows at `window_size=2` | 2-3 per value, mean 2.96 |
| windows at `window_size=3` | 2 per value |

Therefore, `window_size=50` is a useful diagnostic for "ARE with upstream defaults," but not a primary test of "per-token editing rescues C10." A primary C10 pilot should use `window_size=1`, or preregister a small-window comparison that can actually create multiple target vectors for A7.

7. **LAW#5 still needs to be earned for the new harness.** The existing C10 harnesses already prove inertness for their local MEMIT reimplementation against the engine. AnyEdit has no local engine baseline. The next harness must add an AnyEdit-specific null/identity gate before any A7 result is trusted: an identity/no-op path must produce near-zero weight/output change and stable locality. A positive A7 result without that gate is not evidence.

8. **Advisor-review is still required before harness authoring.** Attempting the out-of-family advisor invocation was blocked by the environment safety reviewer because it would export private workspace research context. Do not work around that. Before harness authoring, get explicit operator approval for the data export or use an approved local review route.

## Next Gate

Before any code is written:

1. Draft `docs/C10_ANYEDIT_PILOT_PREREG.md`.
2. Include a primary small-window condition (`window_size=1` unless advisor rejects it) and a default-window diagnostic (`window_size=50`) only as a mechanism check.
3. Include A1/A2 controls, A7 binding held-out full-sequence, context-prefix diagnostic, per-token/window continuation, and locality/bystander deltas.
4. Get advisor-review approval with explicit operator authorization for external model data export, or an approved equivalent.
5. Only then author a narrow Track C harness.

