# TUI integration review — 2026-10-11

## 1. Summary for the operator

Keep the eight existing tabs as the starting point; changing toolkits alone would not improve the phone workflow (`tools/team_dashboard.sh:16`, `tools/team_dashboard.sh:28–34`).  
Borrow the two skills' rules for narrow screens, readable states, and restrained decoration; they do not require a new toolkit. [Hyperb1iss skill][hs] [Gfargo skill][gs]  
Dashbrew is the strongest candidate for a later, limited trial because configuration can connect widgets to shell output. [README][db]  
WTF is a fallback candidate for file and command displays, with a repository rename underway. [README][wt] [Homepage][wh]  
Blessed-contrib and termui would mean maintaining another application; borrow display ideas before considering a rewrite. [Blessed-contrib][bc] [Termui][tu]  
Skip Void-Tools, Puffin, and Termux-TUI for research monitoring: their stated purposes are OSINT utilities, finance, and Android utilities. [Void][vo] [Puffin][pu] [Termux][tx]  
All trials below are proposals after operator review; the build hold remains in force (`results/dashboard_integration_review_20261011/CONTEXT.md:4`).

## 2. Item assessment

A = tmux/Termius; B = static LabViz; C = proposed Intel-hosted phone page; D = agent skills (`results/dashboard_integration_review_20261011/CONTEXT.md:14–17`).
Integration paths, phone suitability, and verdicts are this review's assessments; linked pages support the product facts. No runtime, phone, security, or performance trial was run. Install weight is qualitative; sizes were not measured. Commit dates were not exposed in the opened pages. “No GitHub releases” does not establish absence of package releases. Release dates below preserve the rendered day/month where the year was not exposed.
GPU interpretation follows `results/dashboard_integration_review_20261011/CONTEXT.md:14`: Node/Go/Rust themselves avoid the Python gate; a Python child command can still block launches. They still compete for shared resources. No candidate below is a ready-made replacement for B or the hosted browser interface in C.

| Item | What it is | Surface fit | Concrete integration and phone assessment | Cost and risk | Verdict | Source URL opened |
|---|---|---|---|---|---|---|
| yaronn/blessed-contrib | JavaScript widgets on Blessed, including charts, logs, tables, Markdown. | A, if rewritten | New Node renderer in a tmux window would replace a tab display. File IO, JSON/JSONL parsing, and command execution require maintained JavaScript; Markdown accepts supplied text. Phone: sparklines/text could fit; the sample grid consumes scarce cells. | Node LTS + Blessed + npm dependencies; custom application upkeep. MIT. No GitHub releases seen; maintenance recency unverified. Local-only rendering is a possible configuration, not a telemetry audit. Node itself does not trip the gate. | BORROW-IDEAS | [README][bc]; [releases][br] |
| gizak/termui | Go terminal widget library, not a configured dashboard. | A, if rewritten | Build a Go executable replacing a tab renderer; we own every file reader and JSON/JSONL/Markdown/command adapter. Phone: resize events help, but a narrow layout must be implemented. | Go toolchain/dependencies at build time; compiled runtime. MIT. Author explicitly warns of irregular updates and seeks maintainers; no GitHub releases seen. Local rendering possible; network behavior belongs to our application. No Python gate impact from Go itself. | SKIP | [README][tu]; [releases][tr] |
| wtfutil/wtf / wtfutil.com | Configured Go dashboard with modules. | A | Separate tmux window on either Mac; Textfile/CmdRunner are listed. Proposed input: existing text files or read-only shell output. JSON/JSONL can be displayed as text; readable fields need maintained filters. Markdown rendering/module behavior not verified. Phone: trial one full-width module, not the example grid. | Standalone binary or Homebrew; YAML configuration. MPL-2.0. Volunteer maintenance; README announces move to linodians/tessera. Last release not verified within the two-page limit. Online modules contact third parties; proposed local modules need no account/server. Go avoids gate; Python commands would not. | TRIAL | [README][wt]; [homepage/module index][wh] |
| rasjonell/dashbrew | Go/Bubble Tea dashboard configured with JSON; script/API sources. | A | Separate tmux window; script source can run `cat`/bounded log tails. This needs configuration, not a custom renderer. JSON/JSONL field extraction still needs maintained shell/jq filters; arbitrary Markdown is raw text, not a documented Markdown renderer. Phone: one stacked column; Shift navigation needs checking in Termius. | Go build/install and dependencies, then binary/config. MIT. Latest observed v1.1.0, “15 May”; release fixes layout overflow. No default egress guarantee verified: API widgets send requests; local commands can stay local. Shell bindings can mutate files; omit them for a read-only trial. Go avoids gate unless commands spawn Python. | TRIAL | [README][db]; [v1.1.0][dr] |
| v0id4real/Void-Tools | Python/Rich OSINT and network utility menu. | none | No documented general research-record reader; adapting JSON/JSONL/Markdown would be a fork. No tab replacement recommended. Phone: numbered menus, but not a monitoring layout. | Python 3.11+ and third-party dependencies; Windows batch setup documented. README says this is the legacy v1 archive and advertises v2 elsewhere; no GitHub releases seen here. README claims AGPL-3.0; license file not verified. Network lookups contact external services. Running it on the science host would block launches. | SKIP | [README][vo]; [releases][vr] |
| ntrospect0/glint | Rust/Ratatui personal dashboard with optional service widgets. | A, ideas | Borrow focus zoom/stacked views; adopting the executable would duplicate system monitoring. Local `.md` notes exist in its own config tree, but no generic JSON/JSONL/shell research feed is documented; adding one means Rust code. Phone: zoom may rescue a dense grid; untested. | Source-only Rust 1.81+ build; optional compile-time widgets. GPL-3.0. No GitHub releases seen; maintenance recency unverified. README says no telemetry; weather/finance/mail integrations contact providers and optional LLM summaries send content externally. Rust itself avoids gate. | BORROW-IDEAS | [README][gl]; [releases][gr] |
| siddhantac/puffin | Go/Bubble Tea dashboard for hledger finances. | none | Reads an hledger journal and reports; JSON is configuration, not our result schema. No general JSONL/Markdown reader documented. Custom report commands remain finance-oriented; repurposing would duplicate tab navigation. Phone: report filters/detail views are ideas, not verified fit. | Puffin binary plus required hledger executable; Go compiler if building. MIT. README says v3 work paused on 2026-02-17; latest observed release v2.1.5, “16 Apr”. Local journal/report workflow documented; telemetry not audited. Neither normal executable is Python; a substituted Python command would trip gate. | SKIP | [README][pu]; [v2.1.5][pr] |
| opsonusdh/Termux-TUI | Python/Textual dashboard for Termux phone utilities. | none | Runs in Android Termux, not the iPhone's remote Mac tmux session. It displays Termux API JSON and shell output; not a general research JSON/JSONL/Markdown dashboard. Phone orientation does not establish Termius/iPhone compatibility. | Python + Textual/dependencies + Termux:API/Android permissions. MIT. Latest observed v2.9.5, “10 Jun”; current commit recency unverified. Weather uses wttr.in; other utilities can use network services. A Mac port would add non-exempt Python and block launches. | SKIP | [README][tx]; [v2.9.5][xr] |
| hyperb1iss/hyperskills/tui-design | Framework-independent design guidance in SKILL.md. | D; informs A | Manually borrow labels/units/freshness, content priorities on resize, ASCII fallback, and sanitization of displayed logs. No data reader or replacement runtime. These rules apply to stdlib tabs. | Prose has no resident process or inherent data upload. MIT per repository. Entry says primary docs checked 2026-09-04; latest release unverified. Linked references/package contents were not audited; installation would add agent instructions with tool access. No GPU impact from reading prose. | BORROW-IDEAS | skills.sh **not opened**; [primary SKILL.md][hs]; [repository README/licence][hr] |
| gfargo/tui-design-skill/tui-design | Design/review guidance with a clutter audit and viewport checks. | D; informs A | Borrow countable clutter checks, stable panel roles, explicit error/disconnected/too-small states, and meaning without color. No data reader; manually use rules in future tab review. | Prose/reference package; MIT. README describes CI and reference audits; latest release unverified. Optional npx installer requires Node 22.20+; unnecessary for borrowing. Maintenance scripts include Python and network audits: running those on the science host could trip gate/send requests. Core reading has no egress; other package instructions remain unreviewed. | BORROW-IDEAS | skills.sh **not opened**; [primary SKILL.md][gs]; [repository README][gf] |

## 3. Top three recommendations

1. **Borrow the skills as review criteria, without installing either package.**
   First reversible step: after operator review, annotate existing captures of the eight tabs with a narrow-screen/clutter review; no runtime change. Use Hyperb1iss for freshness/capabilities and Gfargo for countable decoration and viewport checks. [Hyperb1iss][hs] [Gfargo][gs]
   Worth-it criterion: at the actual Termius dimensions plus 40×30, 60×24, and 80×24, identify specific hidden attention/error text or wasted rows; propose changes only for observed failures. Require text labels in monochrome and readable fallback glyphs.
   Displacement/duplication: replaces ad hoc styling judgments, not tabs. Queue already puts “Needs you” before optional details, enforces a 40-column floor, and compresses overflow (`tools/dashboard_queue.py:329–357`, `tools/dashboard_queue.py:396–427`); preserve those behaviors rather than proposing them as missing.

2. **Keep Dashbrew as the first possible executable trial after the hold is lifted.**
   First reversible step: a separate, single-pane tmux session on the helper Intel Mac, with one approved text snapshot and one bounded log tail; local script sources only, no action bindings. Its README supports script-fed text and charts. [README][db]
   Worth-it criterion: at 40×30, the operator can find state, source age, and error within ten seconds; missing/malformed/old input visibly becomes UNAVAILABLE under a pre-agreed age threshold. Reject the trial if this needs another maintained implementation of research-record interpretation. Record all child processes; zero non-exempt Python and zero external requests for these sources.
   Displacement/duplication: initially duplicates the science display launched at `tools/team_dashboard.sh:32`; only a demonstrated reading benefit could justify replacing its display. Keep the existing evidence producers. The helper-host role is stated in `results/dashboard_integration_review_20261011/CONTEXT.md:7`; this terminal trial would not implement the web page proposed at `results/dashboard_integration_review_20261011/CONTEXT.md:16`.

3. **Keep WTF as a fallback trial, not a second dashboard to run alongside Dashbrew.**
   First reversible step: after the hold is lifted, if Dashbrew fails the reading/configuration check, compare one Textfile/CmdRunner module in an isolated helper-host tmux session using the same approved inputs. The homepage lists these modules; their exact configuration/error behavior still needs verification before execution. [Homepage][wh]
   Worth-it criterion: the same phone, unavailable-state, child-process, and egress checks as above, with no Go changes and less maintained configuration/filtering than Dashbrew. Resolve the WTF/Tessera version/URL before any installation. [README][wt]
   Displacement/duplication: candidate display replacement for the storage tab launched at `tools/team_dashboard.sh:33`, not an additional tab or new storage collector. Nothing here proves compatibility with its cache or freshness semantics.

## 4. Ideas worth borrowing even from SKIP items

- Small sparklines beside exact values/units, instead of large gauges or pictures. [Blessed-contrib][bc] [Termui][tu]
- Resize as a real input event; recompute the layout instead of assuming the initial size. [Termui][tu]
- Explicit filters and a detail view for dense reports; keep the active filter visible. [Puffin][pu]
- Label JSON values as key/value rows instead of exposing a raw JSON blob. [Termux-TUI][tx]
- Use full-width detail views while preserving the reader's position; avoid a permanently crowded grid. [Glint][gl]
- Hyperb1iss: show age/error text, sanitize control sequences, use terminal cell widths, and test tmux/SSH with ASCII and color disabled. [SKILL.md][hs]
- Gfargo: count redundant badges/borders; give narrow layouts a single-pane fallback and explicit partial/disconnected/too-small states. [SKILL.md][gs]

## 5. Questions only the operator can answer

- Which two tabs matter most during a quick phone check, and what information must be visible without scrolling?
- What Termius font size/orientation do you normally use, and are Shift-based shortcuts comfortable there?
- After reviewing this report, should a later trial focus on Surface A or wait for the separate Surface C decision (`results/dashboard_integration_review_20261011/CONTEXT.md:4`, `results/dashboard_integration_review_20261011/CONTEXT.md:16`)?

[bc]: https://github.com/yaronn/blessed-contrib
[br]: https://github.com/yaronn/blessed-contrib/releases
[tu]: https://github.com/gizak/termui
[tr]: https://github.com/gizak/termui/releases
[wt]: https://github.com/wtfutil/wtf
[wh]: https://wtfutil.com/
[db]: https://github.com/rasjonell/dashbrew
[dr]: https://github.com/rasjonell/dashbrew/releases/tag/v1.1.0
[vo]: https://github.com/v0id4real/Void-Tools
[vr]: https://github.com/v0id4real/Void-Tools/releases
[gl]: https://github.com/ntrospect0/glint
[gr]: https://github.com/ntrospect0/glint/releases
[pu]: https://github.com/siddhantac/puffin
[pr]: https://github.com/siddhantac/puffin/releases/tag/v2.1.5
[tx]: https://github.com/opsonusdh/Termux-TUI
[xr]: https://github.com/opsonusdh/Termux-TUI/releases/tag/v2.9.5
[hs]: https://raw.githubusercontent.com/hyperb1iss/hyperskills/main/skills/tui-design/SKILL.md
[hr]: https://github.com/hyperb1iss/hyperskills
[gs]: https://raw.githubusercontent.com/gfargo/tui-design-skill/main/plugins/tui-design/skills/tui-design/SKILL.md
[gf]: https://github.com/gfargo/tui-design-skill
