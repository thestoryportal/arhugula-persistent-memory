# Official Figma MCP setup — 2026-10-11

BLOCKED: OAuth login succeeded, but the read-only Codex identity response could not be validated. Figma remains disabled.

Guide answers (checked live; source wording below):

- Remote is recommended: “preferred”; endpoint https://mcp.figma.com/mcp. Codex supports remote, desktop, and remote canvas writing. [Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server).
- Remote allows “all seats and plans”, including free Starter. Desktop requires a Dev or Full seat on a “paid” plan. [Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server).
- Native creation/editing is supported: agents can “build and update frames”; remote writing is currently “free” during beta and is intended to become paid by usage. Wireframe construction is therefore supported in principle, with edit permission. [Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server).
- Starter limit: “Starter plan (20 tool calls per month)”. Limits cover reading; some tools are exempt, including whoami, create_new_file, and add_code_connect_map. Starter per-minute and fixed beta writing quotas are not specified. [Limits](https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/).
- use_figma can “create, edit, delete, or inspect objects”, including frames; whoami reports identity, plans, and seats. [Tools](https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/).
- The linked remote setup page recommends the remote service and lists Codex: [Remote setup](https://help.figma.com/hc/en-us/articles/35281350665623-Figma-MCP-collection-How-to-set-up-the-Figma-remote-MCP-server).

Local inspection: codex-cli 0.160.1; mcp --help, mcp list, and config MCP-table headings checked before changes. Existing servers: graft, pencil, perplexity, node_repl.
Add command: `/opt/homebrew/bin/codex mcp add figma --url https://mcp.figma.com/mcp` (exit 0); then append enabled = false before login.
Codex HTTP add/login syntax and disabling are documented in [OpenAI MCP docs](https://developers.openai.com/codex/mcp); no separate Figma Codex installation page was opened.
Backup: `/Users/robertrhu/.codex/config.toml.bak-figma-20261011T211249Z` (private mode 0600).
Original and backup SHA256: `862e48921c6bfad5bb4931f9bddca72bc302067d52332ff44d053d5eb3dc76a3`.
New config SHA256: `e7c31e19916e2d1f82be108540a0d00ced0faa75162ed28b6cb51db739fac491`.
Exact diff; every original config byte is preserved:

```diff
--- /Users/robertrhu/.codex/config.toml.bak-figma-20261011T211249Z
+++ /Users/robertrhu/.codex/config.toml
@@ -287,2 +287,6 @@
 followUpQueueMode = "queue"
 dock-icon-preference = "codex-system"
+
+[mcp_servers.figma]
+url = "https://mcp.figma.com/mcp"
+enabled = false
```

Sign-in: `/opt/homebrew/bin/codex mcp login figma` exited 0 and reported successful login; credential handling stayed within Codex.
Check: one ephemeral codex exec, read-only, Figma enabled and graft/pencil/perplexity/node_repl disabled only for that process; exit 0.
Identity: exactly one whoami call completed without a flagged tool error; the client response parser could not validate identity or extract plans/seats. Actual account plan and seat remain UNVERIFIED.
Local check result: `/private/tmp/figma-mcp-check-20261011T211249Z/result.json` (no secrets or personal identity in this summary).
Tools shown: 42; names below omit the `mcp__figma__` prefix:

- `add_code_connect_map`, `create_generative_plugin`, `create_new_file`, `create_shader`, `download_assets`, `export_video`, `generate_diagram`, `generate_figma_design`, `generate_image`.
- `get_code_connect_map`, `get_code_connect_suggestions`, `get_context_for_code_connect`, `get_design_context`, `get_figjam`, `get_generative_plugin`, `get_libraries`, `get_metadata`, `get_motion_context`.
- `get_screenshot`, `get_shader`, `get_variable_defs`, `list_file_components_for_code_connect`, `list_file_shaders`, `list_generative_plugins`, `list_shaders`, `open_figma_mcp_app_in_thread`, `search_design_system`.
- `send_code_connect_mappings`, `update_generative_plugin`, `update_shader`, `upload_assets`, `use_figma`, `weave_cancel_tool_run`, `weave_find_model`, `weave_get_model_run_output`, `weave_get_tool_inputs`.
- `weave_get_tool_run_output`, `weave_list_tools`, `weave_run_model`, `weave_run_tool`, `weave_upload_asset`, `whoami`.
Canvas tools exposed: use_figma (direct frame creation/editing), create_new_file, generate_figma_design, upload_assets; generate_diagram creates FigJam diagrams. No design-writing test was performed.
Existing client warnings: ignored full/lean profile settings; SessionStart, UserPromptSubmit, and Stop hooks reported failure. These settings/hooks were left unchanged.
Final verification: codex mcp list shows figma disabled; its Auth column says Unsupported while disabled. Existing servers/settings still match the backup byte for byte.
Later wireframe session (after resolving identity verification): `codex -c mcp_servers.figma.enabled=true -c mcp_servers.graft.enabled=false`.
Next step for MAESTRO: review the client identity-parsing failure before approving wireframe work; no retry or alternate authentication was attempted.
Context rule: at 45% left, a MAESTRO context message, or compaction, stop new work, write figma_mcp_handoff.md with config/backup state and next step, restate this rule, and reply FIGMA HANDOFF; if finished, reply READY instead.
