FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING — exact replacements**

1. Replace [§15:402](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:402). “Equivalently” leaves two potentially different implementations:

> §2.2 check 4 and the fresh-arm historical comparison use, per layer, the `delta_norm` returned by the unchanged `H.my_edit` for that same observed write. Persist this scalar as `n_native`; do not substitute a recomputation. The producer computes `float(upd.float().norm())` on the CPU fp32 pre-cast update. Compare `|n_native − delta_norm_F| / delta_norm_F ≤ 1e-3`, with subtraction and division in CPU fp64. A1/A7 comparisons remain reported-only; mint retains per-arm admission semantics. Record the producer’s torch version and CPU thread count. Missing or nonfinite scalars fail closed.

The returned scalar is better-defined: it preserves the actual producer measurement, including reduction execution and layout. CPU recomputation is **not guaranteed identical** across thread counts/layouts/runtimes; CPU–MPS equality is likewise not guaranteed. Both relevant producer reductions here are CPU, despite MPS model execution. A7’s one/eight-thread equality proves only that control.

2. Replace [§15:403](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:403). “Never gates” conflicts with §3 gate 2a:

> The captured fp64 `upd_norm` remains diagnostic-only for historical norm agreement and cannot affect §2.2 check 4. It remains the unchanged reference for §3 gate 2a’s fp64 norm comparison for non-A7 arms. All other comparison arithmetic, gates and thresholds remain unchanged.

3. Replace the final sentence at [§15:408](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/MATHLAB_PREREG.md:408):

> Any mint arm failing the corrected check remains INVALID-REPLAY. Fewer than two admitted mint arms makes calibration INVALID; otherwise §4.3’s unchanged admission-dependent rule applies. No further metric change or additional harvest is authorized under this amendment, regardless of outcome.

This preserves the existing two-seed calibration rule.

**ADVISORY**

- **Diagnosis supports the correction.** All five A7 native norms equal historical scalars exactly; fp64 produces the recorded 0.00192–0.00602 discrepancies. I verified the saved scalar arithmetic, manifest SHA and admission records; I did not rerun tensor reductions. [Evidence](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/mathlab_staging/mint_norm_diagnosis_20261009T193234.646267Z/cpu_reductions.json:59).
- Tighten §15:399’s limit: **both first-harvest mint updates/native-return norms and historical full mint updates are unavailable**. Current projector agreement does not establish historical projector identity. Mint attribution remains strong inference.
- **Post-failure change: yes; unjustified relaxation: no, subject to these fixes.** An unchanged numeric bar alone would not justify changing the metric. The independent justification is the pre-existing producer expression plus the same-tensor A7 control. It repairs an unlike comparison; it establishes neither tensor identity nor mint success. **First-harvest failures stand.**
- Fresh identity, unchanged admission, one implementation round and one harvest are adequate boundaries. The fixture’s negative case must exceed **1e-3**, not merely differ.
- §15:406 correctly isolates the old step-2 run, but replace “remains a valid … reproduction” with **“remains an in-flight reproduction attempt for A1/A2/A7 only; validity awaits its unchanged gates.”** It cannot validate mint admission or calibration.

🌱 graft saved ~89,106 tokens (~$0.05), 1 successful call.

