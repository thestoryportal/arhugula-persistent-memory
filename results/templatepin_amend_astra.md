FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **[C10Z draft:43–48](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_v4fix_amendment_draft.md:43): selection claim is too strong.** The benchmark predates the halt; choosing its templates for the writer does not. Replace the independence claim with: “This is a post-V4, pre-candidate input amendment. The selected set has an independently recorded pre-halt benchmark identity; adopting it now changes both comparator and candidate inputs. Results remain conditional on this fixed set.” Replace “Any ASTRA gain … would be inflated” with: “The effect on gain is unknown: changing templates changes both n and a.” Benchmark alignment justifies the remedy; favorable historical counts do not establish freedom from selection bias.

- **[C10X draft:10](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10x_templatepin_amendment_draft.md:10), [C10Y draft:11](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10y_templatepin_amendment_draft.md:11), [C10Z draft:16](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_v4fix_amendment_draft.md:16): preserve the inference boundary.** Replace unconditional seed/set attribution with: “Earlier seed-0 processes recorded `e8605172dce0`; ASTRA’s unrecorded set is inferred from matching call order and baseline measurements, not directly observed. Reproduction depends on matching RNG consumption and execution conditions.” C10Z:21 acknowledges this; X/Y must too.

- **[C10X draft:6,33](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10x_templatepin_amendment_draft.md:33): incomplete supersession.** Prereg:124 still permits different sampled contexts and frames when combining processes. Quote that sentence and replace it with: “The reader combines processes only if scientific configuration, source, weights, stimuli and pre-registration hash match, and both context lists and frame texts match the §12 pin; independently recomputed targets remain subject to existing checks. Same-file or same-process reuse is not replication.” Add: “Replication now tests fixed-template regeneration, not robustness across template draws.”

- **[C10Z draft:61–64](/Users/robertrhu/.claude/jobs/8ac4cacf/tmp/c10z_v4fix_amendment_draft.md:61): launch substitutions overwrite historical logs.** The referenced launch line retains `> results/c10z_astra_chain.log`, which already contains attempt 1’s halt. Add replacements for both redirected log paths: `c10z_astra_attempt2_chain.log` and `c10z_astra_attempt2_stage3.log`.

**ADVISORY**

- Pinning is a principled **prospective remedy after a halt**, with the disclosure above. It preserves the scientific gates, thresholds, arms and verdict rules. It is preferable here to retroactively passing V4, an outcome-conditioned redraw, or an unchanged repeat.
- Verified: C10Q/benchmark template identities and digests; pre-halt benchmark timing; baseline-only HALTED-V4 records; exact quoted replacement passages; supplied X/Y prereg hashes; no matching X/Y run directories. C10Y’s seed-before-sampling contradiction is correctly identified.
- Benchmark rerun as the one drift-forced replacement, new go record, fresh attempt2 directory, retained halted records, and final V4 halt under the pin are consistent with the frozen rules.
- Refresh driver citations against named source snapshots: current implementations have moved. C10Z:15’s third-process artifact was not found at the cited path; repair its citation or mark that corroboration UNVERIFIED.
- Review only; no model/GPU code or tests run.

🌱 graft reported ~147,392 tokens saved; 2 invocations, 1 successful.

