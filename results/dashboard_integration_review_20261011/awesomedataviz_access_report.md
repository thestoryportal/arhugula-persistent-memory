# awesomedataviz.com — access check (MAESTRO60, 2026-10-11 ~22:35Z)

Requested by the operator for the LabViz brainstorm's context. Checked from MAESTRO's Claude session with its web reader. MAESTRO's shell cannot make outside network calls, so the MCP handshake itself was not tested.

## Access
- `https://awesomedataviz.com/ai/`, `/llms.txt` and `/api/search` all loaded.
- `/api/search?q=react%20charts&limit=5` returned live JSON with 5 results (name, slug, category, stars, status). Example: react-chartjs-2, category "React chart & visualization libraries", 6937 stars, "maintained".
- The MCP server (`https://awesomedataviz.com/mcp`) was not reached directly (see above).

## What the site offers
- A directory of about 365 charting and data-visualization tools in 24 categories (JavaScript charts, React, React Native, Python, R, C++, maps, graphs, dashboards, diagrams-as-code, standalone apps) and 14 topics (maps, 3D/scientific, time series, ...). Content is CC BY 4.0 (attribute "Awesome Dataviz (awesomedataviz.com)"). Data is refreshed daily.
- **There is no icons or icon-set category**, so it does not help with the icon-family question.
- **MCP server:** `https://awesomedataviz.com/mcp`, Streamable HTTP, no login, read-only. Tools: `search_dataviz_tools` (filters: category, topic, language, maintenance status), `get_dataviz_tool` (stars, activity, license, install commands, alternatives), `compare_dataviz_tools` (2–5 tools side by side), `list_dataviz_categories`. Documented setups: Claude Code (`claude mcp add --transport http awesome-dataviz https://awesomedataviz.com/mcp`), Claude.ai/Desktop custom connector, Cursor, VS Code. Codex is not documented; any client that supports Streamable HTTP by URL should work, unconfirmed.
- **Plain HTTP alternatives (no MCP needed):** `/api/tools.json`, `/api/tools/{slug}.json`, `/api/categories.json`, `/api/topics.json`, `/api/search?q=...` (params category, topic, language, status, limit); `/llms.txt`, `/llms-full.txt` (whole directory as Markdown); any page + `.md`; `/sitemap.xml`; `/feed.xml`. No stated rate limits; free with attribution.

## Why the Codex session could not open it
Codex sessions here have outside network blocked for their shell, so the built-in web reader is their only route. That reader failed on the main page. The site states no crawler or user-agent restrictions, so the likely cause is the main page itself; this is unconfirmed. Try `https://awesomedataviz.com/llms.txt`, `/llms-full.txt` or `/api/tools.json` through the reader instead of the main page.

## Not done
The MCP server has not been added to any client. That changes the operator's setup and waits for their word. The operator can test the handshake with a `curl` POST of an MCP `initialize` request to `https://awesomedataviz.com/mcp`.
