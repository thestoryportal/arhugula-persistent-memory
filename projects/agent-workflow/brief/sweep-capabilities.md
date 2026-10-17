# Sweep brief: capabilities (output: P/drafts/inventory/capabilities.md)

Read M/projects/agent-workflow/brief/sweep-common.md first. Its roots, hard rules, evidence rules and output form apply here.

## Task
List every capability the team has TODAY: skills, plugins, subagent definitions, slash commands, hooks, MCP servers, permission rules, CLI tools, repo code tools, eval tools and schemas. For each one, record where it is configured and whether any belt doc or belt script names it. Operator, verbatim (2026-10-17): "We need to identify all skills, tools, MCP, API, knowledge context, schemas, etc our team needs to perform at their hisgest ideal capabilites inside our highly optimized ideal workflows and repo." You do the "what exists today" half only. Do not say what is missing or what the team needs.

"Belt-named" means a grep hit in one of: L/tools/ (not `.bak-*`), L/land.sh, S/, W/brief-template*.md, M/_system/governance/, M/CLAUDE.md, ~/.codex/AGENTS.md. Use one grep per capability class, for example `grep -rlF -e name1 -e name2 ...`, not one grep per item. A belt-named hit is the capability's route (sweep-common, "How to find things"). A capability with no hit gets `no` in that column and is counted in `## Off-route items` by class (do not list each unnamed skill there twice).

## Sources
- Claude: ~/.claude/settings.json (hooks, permissions, env key names only); M/.claude/settings.json and M/.claude/settings.local.json; ~/.claude/skills/ (each SKILL.md frontmatter `name` and `description` first sentence; check for symlinks with `ls -la`); ~/.claude/plugins/installed_plugins.json; ~/.claude/agents/; ~/.claude/commands/; ~/.claude/hooks/. MCP servers: the `mcpServers` keys in ~/.claude.json. Read them with `python3 -c` and print each name and the basename of its `command` only. Never print `args`, `env`, `headers` or `url` values: they can hold tokens.
- Codex: ~/.codex/config.toml, ~/.codex/arhugula-forward.config.toml, ~/.codex/arhugula-implementer.config.toml (model, effort, sandbox, approval policy, profiles, `mcp_servers` names); ~/.codex/skills/ (for each skill, `agents/openai.yaml` if present: record `allow_implicit_invocation`); ~/.codex/rules/; ~/.codex/hooks.json; ~/.codex/AGENTS.md (its size and the headings only; the context-stores sweep covers its content). Do not open ~/.codex/auth.json.
- Shell tools: every external command that L/tools/*.sh (not `.bak-*`), L/land.sh and S/scripts/tickets.py call (for example git, gh, python3, uv, jq, rg, duckdb, tmux, sandbox-exec, codex, claude, npx). For each tool, run `command -v`, and `--version` where sweep-common allows it.
- Repo code tools: the entries in M/map/CLAUDE.md that a belt doc names, and M/code/agents/, M/code/state/.
- Eval tools and their rulings: P/rulings/2026-10-17-equip-installs.md and P/drafts/research/equip-vet-and-installs.md (promptfoo pin, marimo, the 10 installed eval skills with their pinned commits and sha256 lines).
- Schemas: the ticket JSON schema and its limits in S/scripts/tickets.py (grep `2048`, `required`, the keys it validates); the TD/ledger.tsv header; M/program/program_state.json top-level keys and valid states; the review file format that L/tools/ship.sh or astra.sh parses (grep `GO`, `NO-GO`, `REVISE`); receipt formats that verify_ticket.sh reads.

## Sections
1. `## Summary counts`: one table: class | count | command.
2. `## Skills`: one table, one row per skill (Claude and Codex). Columns: name | side (Claude, Codex, both by symlink) | source (path; plugin or repo and commit if recorded) | belt-named (path:line of first hit, or `no`) | Codex implicit invocation (true, false, n/a).
3. `## Plugins, agents, commands, hooks`: tables with: name | path | what it injects or runs (one line, cited) | belt-named.
4. `## MCP servers`: name | side | command basename | belt-named.
5. `## Permission rules that touch the belt`: every allow, ask and deny rule whose pattern names L, S, M, W, a lane path (/Volumes/memit/llmdb-lanes), git, gh, codex or tmux. Columns: rule (verbatim) | file:line | effect.
6. `## Shell and repo tools`: name | path from `command -v` | version | called by (path:line).
7. `## Eval tools`: name | version or pin | installed (yes, no, run via npx) | ruling (path:line).
8. `## Schemas`: name | defined at (path:line) | fields | limits | readers (path:line).

## Acceptance
Every row has a source path. Every belt-named value is a grep hit or `no`. No secret value appears anywhere in the file. Check this before you finish with `grep -nE '(sk-|ghp_|xox|Bearer |api[_-]?key.*[:=] *[A-Za-z0-9]{12,})'` on your output file, and record the result in `## Commands run`.

## Bad and good rows
These rows show the form only. Their facts are not checked.
- BAD: "| promptfoo | installed | used for evals |" (no source; "used" is not shown)
- GOOD: "| promptfoo | 0.123.1 pin | no, run via `npx -y promptfoo@0.123.1` | P/rulings/2026-10-17-equip-installs.md:NN |"
