# 1. Headline

Keep the current dashboards; first check honest failure messages and phone readability. (practices_report.md §1; tui_report.md §1)
Small chart trials and short design/research checklists merit consideration; overlapping skills and full dashboard platforms add little here. (web_report.md §1; uiskills_report.md §1; researchskills_report.md §1)
These are proposals for approval. The build hold remains; tool trials and live dashboard appearance are unverified. (web_report.md §2; practices_report.md §1)

## 2. By area

**Web tools:** TRIAL ECharts for interactive charts, Tabler for phone layout, Altair for repeatable exports, Perspective for difficult run comparisons, uPlot for small line charts, and Charts.css for simple tables.
Keep static LabViz; heavier platforms add services or frontend work. **6 SKIPs.** (web_report.md §§1–2)

**Terminal tools:** TRIAL Dashbrew for command-fed displays; WTF is the fallback. Borrow Hyperb1iss/Gfargo's narrow-screen rules without installing skills.
Keep the eight tabs until a reading benefit is shown. **4 SKIPs**, including termui's rewrite/maintenance burden. (tui_report.md §§1–3)

**Dashboard/design skills:** TRIAL interface-design for layout/error states and Anthropic data-visualization for chart accuracy; borrow Axiom's exact-number-or-blocker rule.
Use one interface guide and one chart guide to avoid repeated advice. **3 SKIPs; no ADOPT.** (uiskills_report.md §§1–2)

**Research skills:** TRIAL RigorPilot's candidate worksheet and ai-ml-data-science's leakage questions; BORROW citation-verification's claim checks.
These complement existing evidence gates; scripts remain unaudited. **6 SKIPs; no ADOPT.** (researchskills_report.md §§1–2)

**Design practices:** No TRIAL/ADOPT labels: borrow source checks, honest scales, phone layout and reader testing from the articles.
No platform or package is needed. **3 SKIPs**: UW–Madison, RIB and Julius. (practices_report.md §§1–2)

## 3. Top five proposals, ordered by value for effort

1. **Check failure wording on paper.** Compare failed, valid-empty and malformed inputs with Active/helpers' displayed words. Proof in a later approved test: failures say UNAVAILABLE, only valid-empty says no work, and parse errors stay visible. (practices_report.md §3)
2. **Check the phone's first answer.** Request read-only captures of all eight tabs at actual Termius dimensions; borrow the TUI checklist. Worth it if attention/error text is visible without rotation, the headline takes ≤5 seconds to find, and helper rows fit. (practices_report.md §3; tui_report.md §3)
3. **Check LabViz's existing promises.** Compare the current review record and phone capture with its spec and interface-design checklist; edit nothing. Proof: measured phone text/contrast/source links and a correct operator explanation; keep the extra guide only if it finds ≥2 missed, repeatable problems. (practices_report.md §3; uiskills_report.md §3)
4. **Check ten public claims.** Propose a read-only citation audit using existing source notes and original identifiers. Worth it if every accepted claim has page/section support, unsupported claims are flagged, and an independent reader finds zero invented verifications. (researchskills_report.md §3)
5. **Try one candidate worksheet.** Describe a completed candidate from its frozen plan and records, using RigorPilot text only. Worth it if evaluation, budget, changed assumptions and stop conditions are explicit, and a reader can distinguish a candidate from accepted evidence. (researchskills_report.md §3)

## 4. Safety

- Skill scripts and secondary references were not fully audited; text-only proposals give no install or execution authority. (uiskills_report.md §2; researchskills_report.md §2; tui_report.md §2)
- Web libraries: remote scripts/fonts/connectors can send data out; local hosting is not a check for hidden network traffic. Tabler's bundled plugin licences need separate review. (web_report.md §2)
- Python dashboard services/exports and plotting/search helpers can block experiment admission; Go/Node/Rust commands can also spawn Python. (web_report.md §2; tui_report.md §2; uiskills_report.md §2)
- Aim's stalled-to-finished status cannot prove freshness or scientific acceptance. (web_report.md §2)
- Dashbrew shell bindings can change files; its API widgets and WTF's online modules make requests. Glint's optional LLM summaries send content out. (tui_report.md §2)
- Void-Tools and Termux-TUI use network services; Gfargo offers an installer plus Python/network maintenance scripts; neither TUI skill package was fully audited. (tui_report.md §2)
- Anthropic build-dashboard loads remote scripts despite its offline claim, permits sample data, and inserts table values without escaping them. (uiskills_report.md §2)
- Stitch downloads packages/assets and uses cloud tools; Axiom scripts send queries/dashboard definitions to its service and can create/change/delete dashboards. (uiskills_report.md §2)
- Impeccable can download/run a binary, install hooks and write files; its permission language grants no authority here. (uiskills_report.md §2)
- Interface-design's optional images can send context out and its saved design file needs scope approval; UI/UX Pro Max runs Python and can persist/force files. (uiskills_report.md §2)
- Academic-plotting sends descriptions to Gemini, mandates three attempts and highlights “our method”; storytelling can hide caveats or imply causation. (uiskills_report.md §2)
- Hugging-science fetches catalogs/resources; providers may receive inputs, and resource execution can load weights/custom code. (researchskills_report.md §2)
- RigorPilot run helpers are unaudited; data-science's automatic keep/revert loops and learning writes conflict with brief scope unless removed. (researchskills_report.md §2)
- Experiment-code's retries/nonzero-accuracy demand and paper-to-code's retry-until-success conflict with halt discipline and frozen acceptance. (researchskills_report.md §§1–2)
- InfraNodus's relation quotas/no-metadata rule weakens cited evidence; graph handoff sends content to its service. (researchskills_report.md §§1–2)
- Citation-verification's repeated Scholar searches, unsupported statistic, citation-count proxy and year tolerance need correction; queries leave the machine. (researchskills_report.md §2)
- Broad ML/MLOps skills add hooks, training, servers or remote tracking; senior-data-scientist's scripts/formulas are unaudited and its sampling assumptions differ from ours. (researchskills_report.md §2)
- Julius promotes uploads; UW's live feedback must not change preregistered science. Reject persuasion that suppresses recorded limitations. (practices_report.md §§2,4)

## 5. Biggest current gaps: rules marked “not met”

- **Rule 13:** Active can report “No agent is working” after a failed inventory read; failure must remain visible. This is a code finding, not a live observation. (practices_report.md §2)
- **Rule 9:** Helpers' fixed columns exceed a 40-column phone pane. Live appearance was not captured; LabViz's visual promises remain unverified, not “not met.” (practices_report.md §2)

## 6. Questions for the operator

1. Which three questions, two tabs and hardest decision should the first phone screen serve; should later effort target terminal or hosted phone views, and citation defects, candidate history or leakage? (practices_report.md §5; tui_report.md §5; uiskills_report.md §5; researchskills_report.md §5)
2. What iPhone/iOS, Termius rows/columns, font size and orientation must work; are Shift shortcuts comfortable? (web_report.md §5; tui_report.md §5; practices_report.md §5)
3. Do you prefer compact detail or larger labels; does ten-second rotation help; are chart/report downloads useful? (uiskills_report.md §5; practices_report.md §5; web_report.md §5)
4. Should the hosted page work only at home or remotely, through which approved route, at what maximum source age, and with status only or separate interactive history? (web_report.md §5)
5. May scholarly queries include unpublished titles, or only public identifiers? (researchskills_report.md §5)
6. What extra agent-token/subscription budget would make a trial worthwhile? (researchskills_report.md §5)
