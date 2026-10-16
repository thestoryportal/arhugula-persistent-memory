VERDICT: NO-GO

1. **BLOCKING — contradictory merge instructions remain in both stores.**  
   [_system/memory/merge-gate-first-use-learnings.md:18](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/_system/memory/merge-gate-first-use-learnings.md:18), and the identical auto-memory copy.

   Commands run:
   ```sh
   /opt/homebrew/bin/rtk proxy sed -n '1,28p' _system/memory/merge-gate-first-use-learnings.md
   /opt/homebrew/bin/rtk proxy sed -n '1,16p' _system/governance/MERGING.md
   ```
   Output excerpts: the note says “Land PRs one at a time (update, fresh CI, gate).” Its line 14 and MERGING.md:7 instead permit a stale base with no changed-file overlap and `MERGEABLE`. Line 8 also retains “Ask in chat before step 5,” despite the documented allow rule.

   Exact fixes, applied identically to both copies:
   - Replace `Ask in chat before step 5; never route around the check.` with `The chat-approval requirement was superseded by the 15 Oct allow rule; never route around a permission refusal.`
   - Replace `The gate refuses any PR whose head lacks the current origin/master` with `Before T035 on 16 Oct, the gate refused any PR whose head lacked the current origin/master`.
   - Replace `Land PRs one at a time (update, fresh CI, gate).` with `Land PRs one at a time through the gate with green candidate-head CI. Only an overlapping stale-base PR needs the merge-master/fresh-CI loop; a non-overlapping stale base is accepted when GitHub reports MERGEABLE.`

2. **BLOCKING — the auto-memory index contradicts its linked Figma guidance.**  
   [Auto-memory MEMORY.md:13](/Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/MEMORY.md:13).

   Commands run:
   ```sh
   /opt/homebrew/bin/rtk proxy sed -n '13,19p' /Users/robertrhu/.claude/projects/-Volumes-memit-llm-database-poc-mirror-arhugula-persistent-memory/memory/MEMORY.md
   /opt/homebrew/bin/rtk proxy sed -n '9,12p' _system/memory/labviz-wireframe-before-spec-approval.md
   /opt/homebrew/bin/rtk proxy rg -n -A 5 '^\[mcp_servers.figma\]' /Users/robertrhu/.codex/config.toml
   ```
   Output excerpts: the index says `Pencil MCP in Codex, no Figma yet`; the note says `Figma MCP now configured for Codex, disabled by default`. Config confirms:
   ```text
   298:[mcp_servers.figma]
   299-url = "https://mcp.figma.com/mcp"
   300-enabled = false
   ```

   Exact fix: replace `Pencil MCP in Codex, no Figma yet` with `Pencil MCP in Codex; Figma MCP configured, disabled by default`.

Non-blocking checks: all 14 E1 shared notes are byte-identical; both indexes’ links resolve; index sizes are **23,985** and **10,426 bytes**. The reviewed diff hunks match current files. The explicitly excluded governance contradictions are not counted above.