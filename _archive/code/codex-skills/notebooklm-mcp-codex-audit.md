# NotebookLM MCP Codex Audit

Date: 2026-06-07

> **⚠ The "Current Local State" section below is the STALE 2026-06-07 record — superseded by the FRESH-INSTALL block here (2026-06-21).** The original setup had been wiped (no `.mcp.json`; CLI absent; not importable — pod-restart wipe, [[pod-restart-wipes-system-python-ml-stack]]).
>
> **FRESH INSTALL (2026-06-21, per the operator + the repo's recommended instructions):**
> - `pip install uv` → `uv tool install "notebooklm-py[browser]"` → **`notebooklm-py==0.7.2`** installed; CLI at **`/root/.local/bin/notebooklm`** (v0.7.2). (`~/.local/bin` must be on PATH: `export PATH="$HOME/.local/bin:$PATH"`.)
> - **Auth state: NOT logged in** (`notebooklm auth check --test --json` → `storage_exists: false`). **Operator step required (interactive, gated): `notebooklm login`** (opens a browser for Google sign-in; the `[browser]` extra auto-downloads Chromium ~170 MB on first login — may need `playwright install chromium` + a headless/display path on this pod). Verify: `notebooklm auth check --test --json`.
> - **Then point it at the RELEVANT notebooks (operator-provided 2026-06-21), NOT the old `Agent Harness Engineering` pin below:** `notebooklm use <id>` with one of —
>   - **`f667f1f2-7624-4039-b521-6ca37b437b6b`** (https://notebooklm.google.com/notebook/f667f1f2-7624-4039-b521-6ca37b437b6b)
>   - **`23ba5f2d-8317-4412-bb8a-f7c30af4c017`** (https://notebooklm.google.com/notebook/23ba5f2d-8317-4412-bb8a-f7c30af4c017)
>
>   (`notebooklm list` after login to confirm titles/access; switch between them with `notebooklm use <id>`.)
> - **⚠ Pod-restart wipes `~/.local` installs** (it wiped the prior setup) — re-run the `uv tool install` after any restart; the auth `storage_state.json` under `~/.notebooklm/` likewise needs re-login if wiped.
> - **Discipline unchanged:** NotebookLM = corpus-grounded **advisory synthesis**, NOT authoritative for load-bearing claims (RESEARCH-FIRST: check our own `research_and_specs/` corpus first); outputs are leads/context, evidence still comes from `CORPUS/` + primary source.

## Scope

This note records the small Codex-side setup/audit pass for using the harness
NotebookLM corpus as an advisory research surface. It does not install a new
MCP server, move credentials, run a NotebookLM content query, or replace any
existing repository source of truth.

## Current Local State

- The repository already registers a `notebooklm` MCP server in `.mcp.json`:
  `notebooklm-mcp --transport stdio`.
- The installed command behind that entry is the existing Python/`uv tool`
  install, not the PleasePrompto npm package:
  `notebooklm-mcp-cli v0.6.13` provides `nlm` and `notebooklm-mcp`.
- The Python NotebookLM skill is also installed:
  `notebooklm-py v0.6.0` provides `notebooklm`.
- `notebooklm status` is pinned to notebook
  `57b8d946-830c-42dd-b201-ac117a8af951` with title
  `Agent Harness Engineering`.
- `.mcp.json` is valid JSON and contains no credential material.

## Auth And Exposure Findings

- `nlm login --check` succeeds against Google and sees the operator's
  NotebookLM library. The account identifier is intentionally not recorded here.
- `notebooklm auth check --json` can parse the local cookie store, but
  `notebooklm auth check --test --json` fails token fetch and asks for
  `notebooklm login`. That means the skill path is stale even though the MCP
  CLI path is currently authenticated.
- `codex mcp list` in the current Codex app session exposes only the app/plugin
  MCP servers (`node_repl` and the OpenAI key helper). It does not expose the
  project `.mcp.json` `notebooklm` server as callable tools in this session.
- `tool_search` likewise did not expose NotebookLM tools in the current app
  context. Treat NotebookLM access from Codex as unavailable until a later
  session explicitly confirms project MCP loading or a Codex-compatible server
  registration.

## PleasePrompto MCP Assessment

The supplied candidate `PleasePrompto/notebooklm-mcp` is a distinct
Node/Chrome/Patchright implementation whose documented Codex path uses
`npx notebooklm-mcp@latest`. That package name overlaps the existing local
`notebooklm-mcp` command name, so it should not replace the current `.mcp.json`
entry blindly.

If piloted, use a distinct MCP server name such as `notebooklm-pleaseprompto`,
pin the package version instead of using `@latest`, start with the minimal tool
profile, and disable destructive/auth-reset tools unless the operator is
actively present.

## Usage Policy

NotebookLM is useful for advisory synthesis when repository-local evidence is
underdetermined, especially:

- selecting self-hosting, deployment, or sandbox framework options;
- checking whether the original harness research corpus considered a choice;
- external-canon checks when static repo excerpts cannot adjudicate a tension;
- post-source-cutoff state-of-the-art questions.

NotebookLM is not authoritative for load-bearing implementation claims. Code
behavior still comes from repository files and tests. `C-*`, `U-*`, `ADR-*`,
`H_T-*`, and CXA seam claims still require the semantic overlay or primary
source grounding.

## Next Live Gate

A live Codex-side NotebookLM query remains gated on one of these operator-led
actions:

1. Make the project `.mcp.json` `notebooklm` server visible to the Codex app or
   run a Codex CLI session that loads project MCP servers.
2. Re-authenticate the Python skill path with `notebooklm login` if the skill
   path, rather than the `nlm` MCP path, will be used.
3. If testing PleasePrompto specifically, approve a separate network/install
   arc for a pinned `npx notebooklm-mcp@<version>` server under a distinct MCP
   name.

No paid provider call is expected for these gates, but they do use the
operator's Google/NotebookLM account and local browser/auth state.
