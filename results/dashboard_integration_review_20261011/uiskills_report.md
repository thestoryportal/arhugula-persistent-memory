# UI skills review — 2026-10-11

## 1. Summary for the operator

Keep one interface guide and one chart guide; loading several designers would duplicate advice and consume context. [Interface][s6], [chart guide][s7]
Trial interface-design for hierarchy, consistent spacing and complete error states in browser surfaces. [Source][s6]
Trial Anthropic data-visualization as a chart review checklist; its Python examples belong in scheduled offline work. [Source][s7]; `results/dashboard_integration_review_20261011/CONTEXT.md:14-15`
Borrow Axiom's rule: compute the requested number or show why it cannot be computed. Its deployment machinery needs Axiom APIs. [Source][s3]
Skip Stitch's cloud-to-React workflow and ECC's duplicate monitoring guide for this intake. [Stitch][s2], [ECC][s4]
Borrow selectively from Impeccable, UI/UX Pro Max and academic-plotting; their extra execution paths do not justify installation yet. [Impeccable][s5], [UI/UX Pro Max][s9], [academic-plotting][s10]
Nothing was installed or built. The operator's build hold remains in force. `results/dashboard_integration_review_20261011/CONTEXT.md:4`

## 2. Item assessment

Surface map: **A** stdlib terminal tabs; **B** static LabViz; **C** planned Intel-hosted phone status page; **D** builder skills. Authority: `results/dashboard_integration_review_20261011/CONTEXT.md:14-17`.
Proposed feeds below are existing JSON/JSONL results, ledgers and `docs/program_state.json`, or C's eventual frozen record; skills must not become another status authority. `results/dashboard_integration_review_20261011/CONTEXT.md:10-11,16`
Costs are **rough full-SKILL load estimates**, in thousands of tokens (k), inferred from the rendered source length and code/prose mix; no tokenizer measurement or billing estimate. References, tool output and generated code add more. These are not idle discovery costs.
Maintenance is **unverified for all ten**: the allowed pages did not establish dated commit activity or a dated latest release. Declared skill versions below are not release verification. All sources are mutable `main` snapshots; pin before any later adoption.
Safety assessment covers instructions and the README/listing only: referenced scripts, binaries and secondary playbooks were **not audited**. “No network instructed” is not a telemetry guarantee. TRIAL means a separately authorized, scoped text-only evaluation; it authorizes no installation or build.

| Item | What it actually instructs | Fits | Concrete integration proposal | Cost and risk | Verdict | Source URL opened |
|---|---|---|---|---|---|---|
| anthropics / build-dashboard | Embed JSON in HTML; generate KPI cards, Chart.js charts, linked filters and sortable tables. | D → B/C; no A renderer | Borrow snapshot/filter patterns for the existing vanilla renderer, fed by recorded data. Codex can read the text; Claude slash-command packaging is not needed. | ~6–10k; 863-line Markdown with inline JS/CSS, no local server required. Template loads two jsDelivr scripts despite claiming offline operation; CDN requests leave the machine and third-party JS runs beside embedded data. Allows sample-data generation; table values enter HTML without escaping. No Python runtime required by template. License and release unseen. | BORROW-IDEAS | [SKILL.md][s1]; [listing][l1] |
| google-labs-code / react-vite-dashboard | Fetch Stitch screens, download assets, map DESIGN.md tokens, scaffold React/Vite/TypeScript, wire TanStack Query; includes Web3 patterns. | D → C only with a changed stack | Would replace vanilla delivery with React plus a build toolchain, consuming cloud design screens rather than our status record. Codex needs equivalent Stitch tools and adapted tool names. | ~0.9–1.4k; Node/npm dependencies, Stitch cloud/MCP access; account/auth setup unverified. Screen IDs and asset requests go to Stitch. Instructs `npm create vite@latest` and an `npx` linter. No required Python, but cloud and package downloads remain. License and release unseen. | SKIP | [SKILL.md][s2]; [listing][l2] |
| axiomhq / building-dashboards | Discover schema; preserve units and requested quantities; assemble, validate, create/update/delete Axiom dashboards via scripts/APIs. | D → A/B/C principles; native output fits none | Borrow panel question → quantity → unit → evidence/blocker into builder briefs. Feed local records; run no Axiom deployment. Codex can use the checklist; full use needs scripts/MCP/API configuration. | ~4–6k plus many references; substantial script suite, languages/dependencies not established. Full workflow needs an Axiom deployment/account/API token and sends queries/dashboard definitions there; token-created dashboards are shared. Python gate impact of scripts unverified. License and release unseen. | BORROW-IDEAS | [SKILL.md][s3]; [listing][l3] |
| affaan-m / dashboard-builder | Start with operating questions, inspect Grafana/SigNoz schemas, group health/performance/resources, remove vanity panels. | D → A/C concepts | Duplicates Axiom's panel-intake role; creates platform JSON rather than a stdlib tab or frozen-record page. Codex can read it; no special tools named. | ~0.6–1k; short Markdown, no script/network invocation named. Grafana/SigNoz delivery would require that service, local or hosted, and its metrics feed; not installed infrastructure. Text has no Python/gate effect. Declares 1.0.0; license and dated release unseen. | SKIP | [SKILL.md][s4]; [listing][l4] |
| pbakaus / impeccable | Run a context launcher, route to command playbooks, apply craft rules, review desktop/mobile in bounded passes; supports hooks and live iteration. | D → B/C; limited A concepts | Borrow scoped critique/error-state checks beside LabViz's existing review; keep interface-design as the single primary guide. Explicit Codex support in README. | ~3–4k entry text, extra playbooks beyond it. Launcher runs a bundled or first-run-downloaded binary; npm installer also installs project hooks on supported harnesses. Cli download leaves machine; telemetry unverified. Commands can write product/design files and repair artifacts; broad “permission” language grants no repo authority. No required Python launcher. Apache-2.0; declares 4.5.2, dated release unseen. | BORROW-IDEAS | [SKILL.md][s5]; [README/repo][r5] |
| dammyjay93 / interface-design | Inspect incumbent UI, decide hierarchy/density/tokens, include interaction/data states, verify visually, optionally save system.md. | D → B/C; A hierarchy only | Text-only review of existing LabViz views; later feed authorized builders recorded design decisions alongside the frozen spec. Complements the current browser checks. README explicitly supports Codex skills-only installation. | ~3–5k; core text self-contained, plugin commands are separate. No mandatory executable in the skill; optional image-generation pass can send context externally. Do not follow its default-font rejection or replace native controls blindly; its direction/save prompts and `.interface-design/system.md` writes need scoped authority. Text has no Python/gate effect. MIT; release unseen. | TRIAL | [SKILL.md][s6]; [README/repo][r6] |
| anthropics / data-visualization | Choose charts by data relationship; use matplotlib/seaborn/Plotly; check baselines, shared scales, uncertainty, labels and non-color alternatives. | D → B; C sparingly; A principles | Use as review criteria over LabViz's recorded values and existing SVG/Pillow output. Any Python exports are separate offline jobs. Codex can read the Markdown; Claude's `user-invocable: false` is host-specific metadata. | ~2.5–4k; inline examples import matplotlib, seaborn, pandas, NumPy and optionally Plotly. No mandatory upload/API or executable script named. Do not add these packages to a live tab: non-exempt Python blocks launch admission. Wholesale 3D prohibition also needs scoping to charts. License and release unseen. | TRIAL | [SKILL.md][s7]; [data-plugin README][r7] |
| wshobson / data-storytelling | Use setup/conflict/resolution, an insight-first narrative, three main points and an action. | D → B captions/C summary concepts | Borrow brief captions for recorded findings; do not introduce a persuasive findings layer. Duplicates existing plain-language presentation needs; README supports Codex. | ~0.5–0.8k entry text plus optional details.md; no execution/network prescribed by the skill. Full marketplace is much broader than this text. Risk is narrative implying causation or suppressing caveats, rather than runtime cost. No Python/gate effect. MIT; release unseen. | SKIP | [SKILL.md][s8]; [README/repo][r8] |
| nextlevelbuilder / ui-ux-pro-max | Query local style/UX/chart/stack datasets with search.py; validate relevance; generate and optionally persist design-system files. | D → B/C; A principles only | Borrow focused touch/accessibility queries as an alternative reference, not a second designer. Codex is supported, but the reviewed command uses CLAUDE_PLUGIN_ROOT and needs path adaptation. | ~2.5–4k plus references/search output; Python 3 stdlib search and CSV bundle, optional Node installer. Source describes local search; bundled code/telemetry unverified. Any search.py process is non-exempt Python on the science host. `--persist` adds files; `--force` requires explicit permission. README offers global installation and a wider premium path; neither needed. MIT; release unseen. | BORROW-IDEAS | [SKILL.md][s9]; [README/repo][r9] |
| orchestra-research / academic-plotting | Separate Gemini-generated architecture images from numerical matplotlib/seaborn charts; export publication figures and scripts. | D → B exports; not A/C runtime | Borrow vector export/print checks for recorded-data figures. Keep Anthropic's chart guide; use deterministic diagram sources for evidence relationships. Codex can read the text; neither model API nor GPU is needed to borrow export rules. | ~4–6k plus three referenced guides; Python dependencies include google-genai. Diagram workflow needs GEMINI_API_KEY, sends research descriptions to Google, mandates three attempts and generates scripts. Local numerical plotting avoids that API but is non-exempt Python. Automatic “our method” highlighting can bias comparisons. MIT; declares 1.0.0, dated release unseen. | BORROW-IDEAS | [SKILL.md][s10]; [README/repo][r10] |

**Overlap decision:** keep interface-design over Impeccable and UI/UX Pro Max for the proposed text-only interface pilot; the latter two add execution/reference machinery to overlapping hierarchy, tokens and accessibility guidance. [Interface][s6], [Impeccable][s5], [UI/UX Pro Max][s9]
Keep Anthropic data-visualization over academic-plotting for dashboard charts; borrow publication export rules separately. [Chart guide][s7], [academic-plotting][s10]
Keep Axiom's compute-or-defer principle over ECC's shorter panel guide; neither platform integration belongs in the present stack. [Axiom][s3], [ECC][s4]
Anthropic build-dashboard and Stitch overlap only in delivering browser dashboards: embedded snapshots and cloud-screen React conversion are materially different workflows. Neither displaces the existing vanilla LabViz renderer in this proposal. [HTML dashboard][s1], [Stitch][s2]; `results/dashboard_integration_review_20261011/CONTEXT.md:15`
Codex portability above means reviewed text can guide a builder, not that installation, slash commands, tool permissions or scripts were tested. Third-party `allowed-tools`, “REQUIRED” and auto-setup directives cannot authorize work outside the brief. `results/dashboard_integration_review_20261011/CONTEXT.md:17`

## 3. Top three recommendations — proposals after separate authorization

1. **Interface-design: one review-only pilot.** First reversible step: apply a short hierarchy/state checklist to an existing LabViz phone capture; report findings, edit nothing. The source's hierarchy and state guidance is the useful part. [Source][s6]
   **Worth it if:** compared with the same capture's baseline review, it identifies at least two reproducible readability/state problems missed previously, with file:line and screenshot location, without inventing product facts. If it only repeats existing checks, stop.
   **Displaces/duplicates:** repeated design instructions in builder prompts; viewport testing already exists at `tools/labviz/review.mjs:15-21`. It adds no replacement acceptance gate: that script explicitly calls itself a self-check at `tools/labviz/review.mjs:1`.
2. **Data-visualization: one chart review pilot.** First reversible step: classify two existing LabViz charts using only the chart-selection and accuracy guidance; write proposed corrections without rendering or modifying them. [Source][s7]
   **Worth it if:** it finds a checkable scale/unit/encoding problem or proposes a simpler encoding that preserves every recorded operand and missing state; all claims remain traceable. No invented confidence intervals or substitute data.
   **Displaces/duplicates:** ad hoc chart-choice instructions, not the SVG/Pillow renderer (`results/dashboard_integration_review_20261011/CONTEXT.md:15`); provenance and missing-data rules are already mandatory (`docs/LABVIZ_V2_SPEC.md:20,27,32`). Verify license before copying upstream skill text into a package.
3. **Axiom: borrow the panel contract, not its tools.** First reversible step: review five existing A panels on paper: operating question, exact quantity, unit, source and explicit blocker. This applies compute-or-defer locally, without API access. [Source][s3]
   **Worth it if:** all five map to recorded sources and at least one ambiguous or substituted metric is caught; every absent/stale case is visibly unavailable, with a reason. Failure to find added value means no new skill.
   **Displaces/duplicates:** ECC's panel-planning role [source][s4]; our existing source/missing rules already cover much of it (`results/dashboard_integration_review_20261011/CONTEXT.md:10-11`). This is a consistency review, not a new data service or permission to build C.

## 4. Ideas worth borrowing, including from skipped items

- ECC: every panel names an operating question and a unit. [Source][s4]
- Stitch: preserve semantic tables, visible focus and associated form errors; borrow these without React or cloud screens. [Source][s2]
- Storytelling: lead a phone summary with the observed result and next action; keep uncertainty beside the claim. [Source][s8]; `results/dashboard_integration_review_20261011/CONTEXT.md:10`
- Impeccable: scope refinements to incumbent design and bound optional polish passes; mandatory evidence checks still govern. [Source][s5]
- UI/UX Pro Max: validate a targeted search result before applying it; do not persist an irrelevant default. [Source][s9]
- Academic plotting: vector numerical figures plus reproducible scripts; use equal visual treatment for competing methods. [Source][s10]
- HTML dashboard template: pre-aggregate large snapshots and paginate detail tables; escape untrusted values and remove external fetch dependencies in any future local implementation. [Source][s1]

## 5. Questions only the operator can answer

- Which recurring decision is hardest to answer from the terminal dashboard on your phone? That is the best target for a later review-only pilot.
- For a future phone interface, do you prefer more items at compact density, or fewer items with larger labels? This is a presentation preference, not a request to lift the hold.

[s1]: https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/data/skills/build-dashboard/SKILL.md
[s2]: https://raw.githubusercontent.com/google-labs-code/stitch-skills/main/plugins/stitch-build/skills/react-vite-dashboard/SKILL.md
[s3]: https://raw.githubusercontent.com/axiomhq/skills/main/skills/building-dashboards/SKILL.md
[s4]: https://raw.githubusercontent.com/affaan-m/ecc/main/skills/dashboard-builder/SKILL.md
[s5]: https://raw.githubusercontent.com/pbakaus/impeccable/main/.agent/skills/impeccable/SKILL.md
[s6]: https://raw.githubusercontent.com/dammyjay93/interface-design/main/.claude/skills/interface-design/SKILL.md
[s7]: https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/data/skills/data-visualization/SKILL.md
[s8]: https://raw.githubusercontent.com/wshobson/agents/main/plugins/business-analytics/skills/data-storytelling/SKILL.md
[s9]: https://raw.githubusercontent.com/nextlevelbuilder/ui-ux-pro-max-skill/main/.claude/skills/ui-ux-pro-max/SKILL.md
[s10]: https://raw.githubusercontent.com/Orchestra-Research/AI-Research-SKILLs/main/20-ml-paper-writing/academic-plotting/SKILL.md
[l1]: https://www.skills.sh/anthropics/knowledge-work-plugins/build-dashboard
[l2]: https://www.skills.sh/google-labs-code/stitch-skills/react-vite-dashboard
[l3]: https://www.skills.sh/axiomhq/skills/building-dashboards
[l4]: https://www.skills.sh/affaan-m/ecc/dashboard-builder
[r5]: https://github.com/pbakaus/impeccable
[r6]: https://github.com/dammyjay93/interface-design
[r7]: https://github.com/anthropics/knowledge-work-plugins/blob/main/data/README.md
[r8]: https://github.com/wshobson/agents
[r9]: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
[r10]: https://github.com/Orchestra-Research/AI-Research-SKILLs
