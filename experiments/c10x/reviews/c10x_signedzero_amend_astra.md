FIX-FIRST

Reviewer: GPT-6-Astra (high)  
Runtime model/effort: UNVERIFIABLE.

**BLOCKING**

- **[draft:77](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10x_signedzero_amendment_draft.md:77), :83, :86 — report-only contradiction.** The count-based consistency HALT makes these fields acceptance-relevant. **Exact fix:** delete Z2(5) and the final sentence of :86; replace :83 with “`changed_elements`: number of unequal binary16 bit patterns, computed from contiguous CPU `int16` views.” Numeric `before != after` would miss signed-zero changes.

- **draft:4, :137 — observation boundary is overstated.** Candidate target optimization ran; the audit binaries persist initial/final logits, CE and losses (`c10x_enginepath_arms.py:940–962`). Their absence from `run.json` does not establish absence of recorded fit information. **Exact replacement:** “Candidate target optimizations ran, and two audit binaries retain initial/final logits, CE and losses. These binaries were not inspected for this amendment. No injection-screen or candidate-recipe recall/locality outcome was recorded.” Replace :137’s first sentence with “No candidate-recipe outcome informed this amendment.”

**ADVISORY**

- **Facts:** hashes and reported probe measurements check out, including layer-4 **21 changed bytes = 21 signed-zero changes**, zero residual/update, unchanged live weights and no recorded unsafe copies. Historical signed-zero attribution remains **I-INFER**. At **draft:134**, explicitly attribute the fifteen zero X2-(iv)(a) distances to **the probe**; process 1’s earlier parity checks establish tolerance passage, not recorded exact-zero distances (`inertness.py:381–386`).

- **Predicate/scope:** explicit shape + fp16 dtype + CPU `torch.equal` correctly admits signed-zero differences while rejecting numeric changes and NaNs; dtype checks are necessary ([PyTorch documentation](https://docs.pytorch.org/docs/stable/generated/torch.equal.html)). Residual/update zeros, observer, negative controls and scientific thresholds remain unchanged. No additional zero-write hash gate needs amendment; retain W0 and T8 byte identity.

- **Forward argument:** sound for finite, well-defined executions of the inspected operation graph. RMSNorm squares away zero signs and adds positive epsilon; attention scaling is constant; SiLU, RoPE, linear maps and residual additions cannot amplify zero signs into unequal finite values. No activation-dependent zero divisor, `atan2` or `copysign` appears. Qualify **draft:124**: the softmax denominator bound assumes a finite maximum; fully masked/nonfinite rows need separate treatment. At :129 say **“value-identical”**; universal MPS execution equivalence was not empirically established.

- **Governance:** describe this as a **post-observation correction that broadens the literal instrument predicate only for signed zeros**, while preserving numerical science criteria. Retaining process 1 as HALTED/INVALID and fully rerunning in `results/c10x_enginepath_rerun1/` agrees with T12 and D-C10w-p2rerun.

No model/GPU execution. CPU torch spot-check did not execute: import required a temporary-file probe blocked by the read-only sandbox.

🌱 graft saved ~219,417 tokens this turn, 1 successful call.

