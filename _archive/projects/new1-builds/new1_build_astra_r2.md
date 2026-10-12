FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

- **B1 — RESOLVED.** `tools/new1_supervisor.py:177–231`: absolute cell deadline covers probes, persistence and final admission. Controls reject the **301-s** successful probe and blocked persistence; 300/1,800-s limits remain intact.
- **B2 — NOT RESOLVED.** `tools/mathlab_events.py:132–134` appends the terminal line before fsync; `:232` treats that readable line as committed. Synthetic terminal-fsync timeout returned **STOPPED-DEADLINE**, while `fold()` exposed **finished/PASS, all four prediction verdicts and the finding**. Persistent terminal I/O failure plus failed halt persistence reproduced the same false completion (`tools/new1_supervisor.py:363–380`). Ordinary `finding.json` failure now hides predictions correctly. **Fix:** make terminal publication fail closed when halt persistence is impossible; add both controls. Existing deadline test sleeps **before** terminal append (`tests/test_new1_supervisor.py:510`), missing this boundary.
- **B3 — RESOLVED.** `tools/new1_geometry.py:372–373`: top/bottom D−M differences and separate validity flags persist. Synthetic/serialization controls verify **1**, **−204/4900**, and top-invalid/bottom-valid preservation.

**ADVISORY**

- Independently passed **66/66 NEW1 tests** and **70/70 dashboard/LabViz tests**. Initial sandbox denied temporary writes; authorized rerun passed.
- Shared events delta is **+16/−0**, confined to `fold()`; schema/emitter and committed consumers are unchanged. Existing compatibility tests pass, but do not cover the terminal failure above.
- Frozen prereg is byte-identical to HEAD; SHA **`eaf7bc21…024741`**. §6 semantics and resource caps remain unchanged; **B2 still violates its no-verdict requirement**.
- Recorded launch command remains correct: arguments, SHA and installed runtime versions match; `--help` passes. Real geometry, admission and workload feasibility remain **UNVERIFIED**.
- Whole-basis promotion advisory resolved at `tools/new1_geometry.py:120`; fixture verifies selected-column conversion.

🌱 graft reported ~231,120 tokens saved (~$0.12), 1 successful call.

