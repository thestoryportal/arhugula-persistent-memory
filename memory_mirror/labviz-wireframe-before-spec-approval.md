---
name: labviz-wireframe-before-spec-approval
description: "Operator 2026-10-11: after Astra approves the LabViz spec, a Codex agent makes static wireframes of every page + reviewable user flow BEFORE the operator approves the spec or any builder starts"
metadata:
  type: feedback
---
Operator, 2026-10-11 ~21:00Z: "Once Astra approves the spec, I would like a Codex agent to generate a static wireframe of the speced out pages and any user flow that needs to be reviewed before I approve the spec or we proceed with the builder agents. If there are available skills, MCP or other context for wireframing that needs to be given to the agent we will do that in a focused way. Figma MCP may be available for this with the free usage plan."

**Why:** the operator (an architect) approves designs by looking at them; a text spec alone is not enough to approve page layout and flow.

**How to apply:** LabViz order after the brainstorm closes = notes → scoped package → spec amendment (S) → Astra GO → **static wireframes + user-flow walkthroughs by a Codex agent** → operator reviews wireframes, then approves the spec and lifts the build hold → test-first builders. Wireframes are static (no app code, no live data, no model runs), labelled illustrative, phone and desktop. Give the wireframe agent only focused tool context. Checked 2026-10-11: no Figma MCP is configured for Codex or Claude (`codex mcp list`, `claude mcp list`); Codex already has the Pencil MCP (Pencil.app 1.2.0, `~/.codex/config.toml` [mcp_servers.pencil]); gstack design-html/design-shotgun/diagram skills exist. Figma needs the operator's own sign-in and its free-plan limits must be checked before relying on it. Related: [[context-management-every-session]].
