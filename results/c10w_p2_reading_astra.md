CONFIRM

Reviewer: GPT-6-Astra (high)

**BLOCKING:** None. Recorded evidence supports the label and routing.

**ADVISORY:**

- **Label:** Independently applying [prereg §3](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/C10W_ORACLE_PREREG.md:329), min(70,71) = **70/72**; seed 0 misses G4, seed 1 misses G4/G6. Their union yields **PARTIAL-CEILING-LOCALITY-COST(G4,G6), BIGRAM**. BIGRAM has C=24 at both seeds, X=17/14 against threshold 12.
- **Routing:** `p3_required=false` follows :372/:378. `canon_split="c"` is correct: canonical-only seeds score 2/3, but L3=12/17 against ≥29 and canonical-frame flips=3/4 against ≤2 invalidate the split. No completed rank passes every gate at both seeds; therefore `reference_count=null`, `NO-GATE-CLEAN-REFERENCE` follow :388/:395.
- **Recorded validity:** [P1 eval](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/p1_20261007T223707_598959Z/eval.json) and [P2 eval](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/c10w_oracle/p2_20261008T034226_086980Z/eval.json) report all six validity flags true. Nine full-template adapters fit **480/480**, both canonical adapters **24/24**, all at 400 steps; frozen-parameter hashes match. Positive controls: P1 O-A1/O-A2 **72/72 each**, P2 O-A1 **72/72**. Matched shuffled cross-scores **0/72 throughout**. Denominators and string≥full checks hold.
- **LAW#3/#5:** Preflight/P1/P2 closed-form A1,A2 = **72,72 / 72,70 / 71,71**; A7 full/first/canonical = **16/54/8, 9/52/9, 11/54/7**, all within envelopes; U and stimulus counts zero. Standing LAW#5 Δexpr/Δloc = **0.0017/0.04, 0.0004/0.27, 0.0002/0.91**. Null counts/probes/weights identical, perplexity Δ=0, described-as=100; delegation/restores pass; zero hits **1/1**, trained hits **5/5 and 6/6**. Nonzero seam maximum errors **1.993×10⁻⁷ / 1.211×10⁻⁷**, below 10⁻⁵.
- **Stability/budget:** Seed gap **1≤15**; retrain **70→70**, agreement **72/72**, unchanged band and G1–G7 outcomes. Float64 cosines span **0.9999999999992969–0.9999999999994948**. Merged/mounted counts match throughout: no MERGE-LOSS or UNSTABLE. Maximum training projection **8.32<90 minutes**, sampled driver memory **29.858<40 GB**; P2 evaluation **99.25<240 minutes**; projection including halted evaluation **363.07<448 minutes**.
- **Provenance:** Reading and P2 eval carry A1 SHA `4791183a…`; its diff changes only cosine accumulation to float64. The two supplied readings are JSON-equal. Archived attempt outcomes supply no scientific reading; its manifest and elapsed time remain audit/budget provenance. Hash-check passes are recorded; I did not independently rehash binaries or rerun anything.

**Plain meaning:** This finite training recipe recalled 70 and 71 of 72 held-out reworded prompts, demonstrating strong recall on this fixed benchmark. It does not establish the program’s ≥61/72 goal with clean locality: G4 misses 15/20 training frames at each seed (including 5 flips versus 1 allowed and 4 versus 1), seed 1 also has 3 canonical-frame flips versus 2 allowed, and MMLU net losses are 4/200 and 6/200 against 4/200 allowed—so this remains an oracle measurement, with C10 OPEN/BLOCKING and F1 unchanged.

Graft: one failed call; no token savings reported.

