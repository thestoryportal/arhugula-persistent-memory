FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

- [cards.py:136](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/labviz/cards.py:136): exclusion covers `mathlab_staging` but misses `results/mathlab/**`. Consequently, harvest logs become ordinary **RECORDED** cards without proxy warnings, and the harvest manifest’s `RECONSTRUCTED` annotation enters verdict-label discovery. **Fix:** exclude both MathLab output families from generic JSON/log/label/scale ingestion; add fixtures for the actual `results/mathlab/` layout. Do not fix this by adding `RECONSTRUCTED` to the verdict table.

- [Harvest card:1](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/labviz/site/cards/run-33210915fe8228a8.json:1): published snapshot still says `running`, with no outcome, mint failures, or finding. Its source hash differs from the completed stream. **Fix:** after correcting ingestion, regenerate the site and verify terminal PASS alongside all three mint-norm failures, zero admitted mint arms, and the MATH-PROXY boundary. Refresh index/chunks and evidence snapshots together.

**ADVISORY**

Shared `read_events → fold`, producer-outcome preservation, Markdown containment/escaping, and candidate labeling are sound on the dedicated MathLab path. No DuckDB authority found. Both legacy corrections match CORPUS/58 and the genuine C10X registry row; assertions were strengthened.

Tests are non-vacuous but miss the second output directory. Fresh results: **Python 73/74**, failing label completeness on `RECONSTRUCTED`; **Node 110/110**. Browser acceptance remains **UNVERIFIED**; no live build performed.

🌱 graft saved ~228,075 tokens this turn, 1 call.

