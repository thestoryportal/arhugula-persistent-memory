**FIX-FIRST**

**Next: replace the directory-wide `configs/` allowance with minimal runtime inputs.** “Knob values, no results” is false.

1. **Historical results remain reachable.** Under the freshly generated v6 Seatbelt profile, both reads succeeded (exit **0**):
   - [`configs/hparams/cfb-v4-highAKD.yaml:22`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/configs/hparams/cfb-v4-highAKD.yaml:22) records **0/5 consistency** and develops the model-family versus low-AKD hypotheses.
   - [`configs/probes/b3_probes.json:15`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/configs/probes/b3_probes.json:15) records **100 edits**, including France→Oslo with `hf_top1=" Oslo"` and `hf_match_target=true`.

   These are research history, not merely alternative settings. Actual agent consumption is **UNVERIFIABLE**; reachability is demonstrated.

2. **Narrowing filenames alone leaves unnecessary screen measurements.** [`g6_screen_qwen3b.json:6`](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/configs/screens/g6_screen_qwen3b.json:6) includes baseline top-1 `" Paris"` with **p=0.539**. For the literal no-history contract, expose projections containing only consumed fields—selected country keys and capital truths—plus the baseline hparams. Exclude historical alternative-arm configs.

3. **The reference fix works; equivalence remains pending.** My regenerated-profile probe denied the full reference JSON and successfully read the **71/70** extract. The existing equivalence record still reports PASS for the old `prepare.py` hash; it does not establish v6 equivalence. [Verified probe record and saved context](/Users/robertrhu/.gstack/projects/thestoryportal-arhugula-persistent-memory/checkpoints/20261006-114326-autoresearch-fence-v6-review.md).

**Cheapest overturning test:** already run—the two historical config reads falsify isolation. After narrowing, require those reads to fail through the actual launch layers while required-input reads, setup and GPU execution succeed; retain the current-hash equivalence PASS gate.

**Drift:** this supports C10 candidate generation toward F1. Isolation and equivalence are separate requirements; neither makes an optimizer candidate conclusive evidence.

