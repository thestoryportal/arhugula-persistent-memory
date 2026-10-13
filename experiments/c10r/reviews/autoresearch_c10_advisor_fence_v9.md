**FIX-FIRST**

**Next:** deny `/Users/robertrhu/.cache/gh` in all three layers, regenerate the fence, and retest before the sixth launch.

1. **Confirmed history leak:** under a freshly generated v9 Seatbelt profile, [this cached GitHub response](/Users/robertrhu/.cache/gh/54/c3/f73cf887f77fa8012c2d89cc9ee363ec60af81b439e88a226967276bdeb7) remained readable—**2,596 bytes**, containing PR #17’s “CORPUS/49 two-pass NULL + CORPUS/50 stacked TRADEOFF-PERM-UNMATCHED” and PR #16’s direction finding. This exposes prior findings beyond the accepted screens.

2. **Controlled verification:** the same probe denied CORPUS and `~/llm-as-database/_manifest.md`, allowed required hparams, and exited **0**. Generated settings contained **zero matching Bash/Read denials** for the cache path. [Saved probe evidence](/Users/robertrhu/.gstack/projects/thestoryportal-arhugula-persistent-memory/checkpoints/20261006-121112-autoresearch-fence-v9-review.md). Actual optimizer consumption is **UNVERIFIABLE**.

**Cheapest overturning test:** make that exact cache read fail under Seatbelt and live Claude Bash/Read, while runtime controls succeed.

**Drift:** this protects C10 candidate-generation integrity toward F1. Equivalence PASS remains independently necessary; it cannot establish context isolation.

