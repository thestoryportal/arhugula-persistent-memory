FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **R1 #1 — RESOLVED.** Both output families are excluded by `tools/labviz/cards.py:136`. Real-layout fixtures and positive controls cover JSON/log/label/scale ingestion (`tools/labviz/test_mathlab.py:159`). `RECONSTRUCTED` is absent from the verdict table; zero generic MathLab cards remain.
- **R1 #2 — RESOLVED.** `results/labviz/site/cards/run-33210915fe8228a8.json:1` renders terminal PASS, all three mint-norm failures, derived **0/3 eligible arms**, the staged finding, and MATH-PROXY. All seven cards match their index/chunk/evidence snapshots; harvest evidence matches the completed source.
- **Step 2 — NOT RESOLVED: stale publication.** `results/labviz/site/cards/run-c4e08b61f2cb7ab4.json:1` still renders running, without outcome or finding. Its coherent 1,361-event snapshot omits 186 events. The canonical `results/mathlab_staging/runs/m2_20261009T192821Z_82233/events.jsonl:1543–1547` records **2a PASS, 2b OPERANDS-ONLY/FAIL, finding, terminal PASS**. Refresh card/index/chunk/evidence together, retaining MATH-PROXY and the utility-UNVERIFIED caveat.

**ADVISORY**

Fresh checks: **Python 79/79; Node 111/111**. Generated renderer exercised; browser layout remains UNVERIFIED. No server or production rebuild run.

🌱 graft saved ~72,369 tokens (~$0.04), 1 successful call.

