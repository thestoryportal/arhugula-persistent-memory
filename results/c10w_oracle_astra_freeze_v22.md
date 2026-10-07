**FREEZE.**

**BLOCKING:** None. The budget fix is complete. Independently recomputed from §2.9’s row components: P1 **335–465**, P2 **310–448**, P3 **230–327** minutes; mandatory total **645–913**, including P3 **875–1240**. Fixed projection limits and authorization requirements are explicit (`docs/C10W_ORACLE_PREREG.md:309–316`). No new blocking defect found in the diff.

**ADVISORY:** Not every advisory was fully applied:

- Stale S7-pending assertions remain at **:104 and :494**. Mark these historical and point to the **22 ACCEPT / 0 REJECT** adjudication at **:139–164**. The verdicts themselves are present.
- **:27** still says the canonical variant “separates the first from the other two” without the requested qualifier. Append **“for contrasts matched as specified in §2.2.”** The operative restriction already exists at **:53**.
- P3’s authorization wording and the historical FIX-FIRST dating are fixed (**:372–384, :531**).

These are editorial remnants, not missing scientific gates. No files changed.

🌱 graft reported ~17,716 tokens saved ($0.01), 1 successful call.

