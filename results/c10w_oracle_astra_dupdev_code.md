GO

BLOCKING: None.

Verified:

- `c10w_oracle_step0.py:177–192`: exact revision, 14,042/285 counts, both parquet hashes; no HEAD resolution.
- `c10w_oracle_step0.py:205–230`: recorded row hashes define duplicates; all five rows remain in source order; whole-dev summary retained.
- `c10w_oracle_read.py:20`: pin equals the actual amended prereg SHA-256, `d2aa240eede4556395373678e4fab757e0e55d5491a7d4105ef765c1eb35d2f0`.
- `c10w_oracle_read.py:408–428`: sensitivity is report-only; full-200 G6 and label/routing logic remain unchanged. Boundary tests at `c10w_oracle_selftest.py:1594–1624` are non-vacuous.
- Permitted CPU selftest: **79 passed, zero skips**. Real cached check exercised **9/9 require sites**, including schema checks; duplicate group `[50,53]`, affected items `[1427,1453]`, suffix failures **0/200** (`c10w_oracle_selftest.py:1564–1585`).
- Reviewed diff contains no compute_z, execute_memit, repr_tools, solve, or engine changes.

ADVISORY:

- `c10w_oracle_selftest.py:1540,1641`: absent cache files permit a skip while the suite still prints PASS. For future launch checks, require the explicit `C10W_DUPDEV_REAL_DATA PASS` marker and zero skips. This run satisfied both.

Graft: 1 failed call; no token savings reported.