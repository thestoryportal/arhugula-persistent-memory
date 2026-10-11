# LabViz interactive brainstorming — 2026-10-11

Discussion record only. The binding contract remains `docs/LABVIZ_V2_SPEC.md`; this file grants no build or install authority.

## Decisions (with the operator's words)

- Session scope supplied by the operator: "This first session covers LabViz only; later sessions take the other areas of the review summary one at a time."
- Building hold supplied by the operator: "Discussion only." "no code, no edits to S, L, W or any existing file, no builds, test runs or browser runs, no installs or clones."
- Intended outcome supplied by the operator: "flesh out exactly how the LabViz functions, the UI and the front-end dashboard design" and how reviewed sources can provide context to builders.
- Home-page priority, operator verbatim: "1 leads, 3 next 2 last". This refers to the displayed choices: (1) the big picture — what we are investigating and how the questions connect; (3) evidence and progress — what we have learned and what remains unresolved; (2) current activity — what is running, waiting or stopped. Settled order: big picture first, evidence and progress second, current activity third. Status-strip placement was subsequently settled below.
- Journey scope, operator verbatim: "1...but flesh out all of them in this session". Start with question → experiments → findings → supporting records; also flesh out run comparison and inside-the-model exploration in this session. Those latter two are required agenda items, not optional future work. The build hold continues.
- Journey 1 approved, operator verbatim: "question > evidence path rec approved. Open a research question: 1 followed by 2 and 3". The approved path is overview → question page → experiment → supporting records. The question page leads with recorded findings and unresolved limits together, followed by the research story over time, followed by the latest experiment. Sources remain available throughout. This is design approval only; no build, spec edit or new scientific conclusion is authorized.
- Journey 2 approved, operator verbatim: "comparing 2 runs setup rec approved. After comparison notice: 1 then 2 and 3". Approved comparison journey: select two runs; keep identities and a notice explaining which measures can be compared visible; show outcome changes and measured side effects first, setup differences second, question-by-question answers third, with sources throughout. The recommended phone design pairs corresponding measurements within each section. The word "setup" in the operator's approval refers to the proposed comparison-page arrangement; the explicit following order puts outcome changes first. No scientific winner is inferred.
- Journey 3 conditionally approved, operator verbatim: "Inside the model approved with conditions: the inside the model diagrams and explanations need to have as granular data as possible, not just at the layer level. What is inside each layer? Zoom into the layer to explore inside of it. All related to the specific experiment data. And the playable timeline is meant to show the model diagrams, 2d and 3d, in animated as the data is applied in order to visualize exactly what is happeneing with the model during the experiment. Also, any word lists, etc that were used for the experiments must be included - this goes for any data journey, not just inside the model."
- Journey 3 presentation order, operator verbatim: "Lead with 1, then 2 and 3 for the presentation. Diagrams and relevant charts where applicable for data visualization in this Inside the Model section." This settles 2D diagram → 3D tower → guided explanation. Granularity must go below layers, remain specific to the selected experiment and include applicable charts. The playable timeline must drive the diagrams, not merely show text events. Input/word coverage is a cross-journey requirement. Historical completeness and richer future recording remain data-contract gaps; the existing re-creation/evidence separation is retained. Do not downgrade the requested detail to layer-level bars.
- Cross-journey research-source requirement, operator verbatim: "Also associated research papers, etc for all of these experiments". Include associated papers and other relevant research sources throughout the question, experiment, run, comparison and Inside-the-model journeys, tied to the specific experiment. This expands the input/source context requirement; no external search, download, upload or installation is requested or performed by this instruction alone.
- Player modes approved, operator verbatim: "All 3 selectable as their own modes". Provide three separately selectable modes: Experiment phases (apply changes → test answers → check side effects), One fact/question, and One component. Each mode controls the synchronized 2D/3D diagrams, applicable charts and input/answer text over source-labelled records. No single exclusive route is approved; initial default has not been explicitly selected.
- Granular-detail layout approved, operator verbatim: "1 and 2 detail panel to the side that can be opened and closed and never obstructs the focused views". Interpret the combined instruction as focused views at each zoom depth, expandable/scrollable detail, plus a collapsible side panel. The side panel must occupy its own layout space and must never overlay or obscure the focused diagram/chart. The selected experiment, component and player context remain stable. This combines the proposed focused-view and expanding-detail approaches with the operator's explicit non-obstructing side-panel condition; narrow-phone placement was subsequently settled below.
- Narrow-phone detail placement approved, operator verbatim: "1" (reply to the choice between below-diagram detail and a separate detail view). Place the same expandable/collapsible details below the focused diagram when side-by-side placement cannot remain readable. Wide screens retain the non-obstructing side panel. Selection and player position persist.
- Visual appearance approved, operator verbatim: "3" (reply to Dark, Light, or a light/dark switch). Provide a light/dark switch; both themes must meet the same typography, contrast, focus, color-independent state and chart-readability requirements. Source/evidence wording and scales must not change with the theme. Initial theme and persistence behavior have not been explicitly selected.
- Home activity placement approved, operator verbatim: "1" (reply to Compact strip at the top/activity details last, or All activity below big picture/evidence). Keep a compact source-dated activity strip at the top; the main home content is big-picture connections → findings and unresolved limits → detailed activity. Full logs open on request. This answer arrived before MAESTRO's context-stop message; preserve it as a settled decision even though that message calls the question open.
- Current build opening explicitly requested, operator verbatim: "Open the current build for me in my chrome browser first. The we begin questions." The operator subsequently confirmed "It is open". The existing HTML file was opened in Chrome via macOS; the sandboxed launch failed, the authorized desktop-access retry exited 0, and the operator confirmed it. No build, automated browser review or model process was run.

## Open questions

Opening discussion sequence; ask the first question now and the others in later turns:

1. RESOLVED: home-page emphasis, in the operator's priority order recorded above. The home still retains the required map and status strip until any proposed amendment is approved (`docs/LABVIZ_V2_SPEC.md:340-345`).
2. RESOLVED: question-to-evidence first; all three journeys must be covered, per the operator's words above.
3. Builder-context recommendations now recorded below: a short interface guide and chart guide, with narrowly selected Tabler layout and ECharts interaction examples as optional reference material. No adoption or library trial is approved. ECharts and Transformer Explainer READMEs were opened immediately before the context stop; other original sources remain unopened. Concrete documentation/example extracts are still pending.
4. RESOLVED: question page order is findings and unresolved limits → research story → latest experiment, per the operator's approved ordering above.
5. Still to flesh out: inside-the-model journey, detailed navigation and phone layout, source/missing-data presentation, how recorded files become the static site, and concrete source extracts for build-agent context. Journey 1 and Journey 2 have design approval; supporting details remain to discuss.
6. RESOLVED (comparison): outcome changes and measured side effects → setup differences → question-by-question answers, after the comparison notice.
7. RESOLVED (inside the model): 2D → 3D → guided explanation; conditionally approved with granular zoom, experiment-specific detail, applicable charts, synchronized diagram animation and input/word coverage across journeys.
8. DATA-CONTRACT GAP: the existing spec already separates actual recorded events/telemetry from separately labelled Phase 3 re-creations; those modes are not a new either/or choice. Exact historical internal activity cannot be recovered when it was not recorded (`docs/LABVIZ_V2_SPEC.md:320-328`). To satisfy the requested fine-grained actual playback for future experiments, propose a more complete observation-data contract, with coverage, granularity, resources and scientific review still to define. No instrumentation, replay execution or experiment launch is authorized here.
9. RESOLVED (player journey): all three are separately selectable modes, per the operator's words above. Initial default is an implementation/design detail still to settle; do not use it to remove any mode.
10. RESOLVED (granular zoom layout): focused views plus expandable/scrollable detail and a collapsible side panel, with no overlay or obstruction of the focused view. See the operator's words above.
11. RESOLVED (phone detail placement): below-diagram expandable/collapsible details, per the operator's choice above.
12. RESOLVED (visual appearance): selectable light and dark themes, equally readable, per the operator's choice above.
13. RESOLVED (home activity placement): operator chose option 1, compact source-dated strip at the top and activity details last. MAESTRO requests this question as the successor's first prompt; the handoff preserves both the requested question/options and the already-received answer, so no answer is lost. The strip is a recorded snapshot, not proof of current liveness.

## Spec changes proposed

- Proposed clarification: explicitly state the operator's home-page priority order in §4A.1 and §11.4 (`docs/LABVIZ_V2_SPEC.md:340`, `:1086-1096`). Approved placement retains a compact activity strip at the top and puts full activity detail last. The existing phone-home acceptance criterion still requires both map and status strip (`:405`). The LabViz spec has not been edited.
- The five destinations, selection carried between views, sourced measurements, explicit missing values and phone readability remain existing requirements (`docs/LABVIZ_V2_SPEC.md:14-32`, `:338-379`).
- Journey 1 design approved; proposed spec clarification pending: overview names plain-language research questions and shows documented connections; opening a question presents the question, sourced recorded findings and unresolved limits first, the research story second, the latest experiment third; experiments explain what was tried and the recorded outcome; supporting records expose the original file/key or document/line. Keep source-level identity visible without making internal IDs the only explanation. Existing line pages already require question, status, decisions, evidence entries, models and runs (`docs/LABVIZ_V2_SPEC.md:343`). The five-field evaluation caption is already specified for linked runs (`:584-587`); extending a reviewed summary to the leading question-page section would require a clarification in §4A.1 and §11.4. Missing or draft summaries must remain visibly missing or draft, never synthesized into a new verdict (`:16-20`, `:1050-1054`).
- Journey 2 design approved; proposed spec clarification pending: select two recorded runs from an experiment or Runs; keep both identities visible; explain which measurements can be compared and why others cannot; show an outcome-and-measured-side-effects summary, then recorded setup differences, then question-by-question answers and their sources. On phones, pair the two runs within each measurement section rather than requiring traversal of the entire first run to reach the corresponding second-run detail. Preserve shared scales only for matching units, per-fact eligibility rules, explicit missing values and the single-run uncertainty warning. This would clarify the existing stacked-phone design in §5 item 5 (`docs/LABVIZ_V2_SPEC.md:578-582`), not replace its evidence rules. A summary may calculate recorded differences; it may not declare a winner or that the approach improved generally.
- Journey 3 design conditionally approved; proposed spec clarification pending: carry the selected experiment/run/input/step into Inside the model; lead with 2D, followed by 3D, followed by guided explanation. Zoom model → layer → component → the finest available experiment-specific measurements, with sources at each depth. Components include attention, normalization, add-back paths and the MLP's internal parts, using the selected model's structure rather than hard-coded Qwen dimensions. Distinguish recorded changes from configured write ranges and method-based versus measured unchanged claims. Include appropriate recorded-detail charts, such as change-size bars, per-component or per-head maps, answer-signal charts and loss/step curves, only where those measurements exist. The timeline must synchronize the 2D diagram, 3D diagram, selected component, input/answer text and applicable charts as recorded or re-created steps advance. Static structure alone is insufficient for the requested playable experience. Relevant contract: `docs/LABVIZ_V2_SPEC.md:355`, `:567-575`, `:627-657`, `:856-875`, `:919-931`. The presentation order, granularity and synchronized timeline requirements should be explicit in §4A.1 and §5 items a–d, with the evidence/data-coverage distinction preserved in §4 and §7–8. The 13px text floor and touch rules remain binding (`:360-371`).
- Cross-journey inputs proposal implementing the operator's condition: offer an "Inputs and answers" section reachable from question, experiment, run, comparison and Inside-the-model views. Include the complete available experiment-specific word/fact lists, training text, canonical and evaluation questions, side-effect/probe questions, expected answers, observed answers, and recorded word-piece IDs/text where supplied. Keep training, evaluation and side-effect sets distinct and bind them to the exact configuration/source version; do not silently reuse a newer prompt list. A timeline step selects its corresponding input and output; comparison shows each run's own inputs and any mismatch. Not every run records every category; explicit missing/transcription labels and source-bound extraction remain mandatory. §5 item a already covers several of these fields (`docs/LABVIZ_V2_SPEC.md:619-625`); universal journey access and complete applicable input-set coverage need clarification in §4A.1, §5 and §6. No tokenizer tool or source transcription is run in this discussion.
- Playback data distinction, existing contract retained: actual run measurements are displayed as RECORDED or TELEMETRY according to their source; a separate observation rerun is a RE-CREATION / NOT EVIDENCE; a generic flow illustration is DIAGRAM / NOT RECORDED ACTIVITY. A diagram's animated state may show only the recorded measurement it represents; it must not invent finer events between snapshots. Matching final outcomes does not establish identical historical internal behavior (`docs/LABVIZ_V2_SPEC.md:896-917`). Proposed extension: future internal recording must provide the finer steps needed by the requested animated experience while preserving observer inertness, resource budgets and scientific scheduling; the current contract's sampled summaries do not provide every internal element (`:856-875`, `:325-328`). This is a data-contract proposal, not permission to capture new data now.
- Cross-journey research sources proposal implementing the operator's requirement: add a "Research and sources" section reachable from each relevant question, experiment, run, comparison and Inside-the-model detail. Show the paper/source title, authors/date where recorded, primary link or existing local document, a plain-language explanation of its role (method origin, test design, comparator, interpretation or limitation), and the program document/line establishing the association. Distinguish "cited or used by this experiment" from "related reading"; do not present a general method paper as proof of this run's result. Shared method-level sources may be inherited but must be labelled as method-level context. At a zoomed component or timeline step, surface only relevant associations while retaining access to the complete experiment bibliography. A comparison preserves each run's associations. Unknown bibliographic details and unverified associations stay explicit. This extends the context sources and node/edge model in §11.1–11.2 and the run card in §6 (`docs/LABVIZ_V2_SPEC.md:983-1023`, `:662-674`); the exact field design is proposed, not implemented. Prefer local source metadata and deliberate external links; no automatic paper fetching or research-data upload.
- Theme switch design approved; proposed spec extension: §4A.2 must apply to light and dark modes, including chart marks/axes, per-layer colors, missing-state patterns, source links, focus rings and control borders (`docs/LABVIZ_V2_SPEC.md:357-371`, `:405-420`). Add equivalent measured phone/desktop/zoom coverage for both themes to §4A.4–5. Both themes render the same source-bound measurements and evidence labels. Suggested routine default, not yet explicitly chosen: follow the device's theme until the operator chooses a mode, then remember that preference locally. This is local presentation state, never scientific state.
- Home arrangement design approved; proposed spec clarification pending: a compact source-dated activity strip at the top, then the question-centered connections overview, recorded findings/progress with unresolved limits, and expanded activity details last. Keep log/source detail accessible without making the entire raw log the leading content. This respects the existing top-strip requirement while applying the operator's visual priority (`docs/LABVIZ_V2_SPEC.md:340`, `:405`). Source time and recorded-snapshot wording remain visible; a local-page refresh must not imply freshly measured data.
- Player-mode clarification: §7.6 already has phase/fact/question/generated-piece tracks, synchronized diagrams and text; make the operator's three separately selectable routes explicit, including a component-focused route (`docs/LABVIZ_V2_SPEC.md:919-931`). Proposed switching behavior: retain the selected run and source-labelled step where that step exists in the new route; otherwise make the change of position explicit. Switching between 2D and 3D preserves mode, step, selected input and component. Extend §4A.1's linkable selection state to include player mode, step, input and zoom focus (`:353-355`); exact URL fields remain a design proposal. Do not mix recorded and re-created frames in one unlabeled route.
- Granular-zoom layout design approved; proposed spec clarification pending: a focused view per depth with a readable diagram/chart, a plain-language location breadcrumb (Model → Layer → Component → available finer detail), a Back control, and persistent experiment/player context. Provide expandable/scrollable details and a collapsible side panel with reserved layout space; never place the panel over the diagram. Details, words/inputs and research sources remain reachable at that depth. Approved narrow-phone adaptation: below-diagram expandable/collapsible details, maintaining readable text and controls. The focused phone view borrows the existing map's one-column drill-down approach (`docs/LABVIZ_V2_SPEC.md:1095`) and retains the global frame/readability requirements (`:348-355`, `:359-371`). Specify this for Inside the model in §5 items b–d rather than relying on the map's existing rule.

## Context for build agents

- Binding spec: `docs/LABVIZ_V2_SPEC.md:1-53` and `:332-434`. Extract the reader goals, evidence limits, five-view frame, phone rules and measured acceptance criteria. These anchor subsequent choices; no spec editing is authorized.
- Current implementation summary: `tools/labviz/README.md:12-24`. Extract the recorded-file-to-card-to-static-site flow, linked selection, deferred card loading and MathLab evidence wording. This is context about what exists, not authority to run anything.
- Existing review: `results/labviz_v2_phase1_design_review_r6.md:1-16`. The report records PASS, completed browser proof and 160 screenshots for the October 8 review. It predates the MathLab integration, so it does not establish visual acceptance for that later addition.
- Integration review: `results/dashboard_integration_review_20261011/SUMMARY.md:1-5`, `:15-17`, `:39-54`. Extract the recommendation to retain static LabViz and evaluate short layout/chart guides. These are trial proposals; scripts and secondary references were not fully audited. ECharts and Transformer Explainer READMEs were subsequently opened, as recorded below; no repo is adopted.
- Home-map context: `docs/LABVIZ_V2_SPEC.md:1086-1096` supplies the existing column layout, focus paths, source explanations, search and phone drill-down. Extract these mechanisms before proposing replacements. Connections mean documented relationships; they must not be presented as proof or causation (`:1020-1023`, `:1096`).
- Existing phone screenshot inspected: `results/labviz/review/20261008T130913325Z/chromium-phone-map.png`. Qualitative observation: a long activity/log block precedes the map heading and research navigation. This is an October 8 screenshot, not a fresh capture of the open build. The review's phone viewport is 390 × 844 (`results/labviz/review/20261008T130913325Z/measure.json:23-29`). No new browser run or measurement was performed.
- Existing science-line screenshot inspected: `results/labviz/review/20261008T130913325Z/chromium-phone-line-c10.png`. It shows framing, experiment groups, linked documents, observations over time and program decisions. The framing is marked draft. This is context for a proposed clearer question-to-evidence journey, not proof of the current build's appearance.
- Existing measurement inspected for the phone Map: `results/labviz/review/20261008T130913325Z/measure.json:825181-825210`. It records a 390 × 844 viewport, scroll width 390, client width 390 and document height 1905, with no horizontally outside elements. These measurements show horizontal fit, not that the ordering communicates the program well. Extract the distinction between mechanical readability proof and an operator's understanding; no new measurement was performed.
- Comparison context to use in the next journey: `docs/LABVIZ_V2_SPEC.md:578-582` requires matching fact identities and scoring kinds, explicit reasons for refused comparisons, shared rulers where units match, stacked phone cards and a single-run uncertainty warning. Borrow these existing rules before suggesting any comparison library.
- Existing comparison screenshot inspected: `results/labviz/review/20261008T130913325Z/chromium-phone-compare.png`. Qualitative observation: a comparison summary precedes two long stacked run cards, so corresponding detailed measures can be separated by a long scroll. Use as context for paired phone sections; it predates the math-lab addition and is not a new runtime check. Typed value/source/derived/missing rules remain the data contract (`docs/LABVIZ_V2_SPEC.md:664-674`).
- Existing Inside-the-model screenshot inspected: `results/labviz/review/20261008T130913325Z/chromium-phone-model-2d.png`. It presents recorded layers, selected-layer parts, static wiring, missing internal signals and recorded events. Its long layer listing is context for a compact phone overview, not evidence that unknown layers are unchanged. No new capture was performed.
- Inside-the-model source extract: `docs/LABVIZ_V2_SPEC.md:627-657`. Builders should receive the distinction between stored numbers, information flow and historical events; method-based or hash-based explanations for unchanged parts; diagram versus recorded activity labels; and the separation of untimed events from timestamped events. A bright answer signal does not locate a stored fact (`:594-595`); neither does a chosen write layer (`:603-604`). These guardrails apply equally to 2D and 3D.
- Granular player context: `docs/LABVIZ_V2_SPEC.md:856-875`, `:919-931`, `:938-952`. Extract the specific per-layer, per-head, sampled-inner-unit and per-input frame fields; the synchronization of tower, exploded layer, wiring and text; and separate actual telemetry versus re-created records. The existing replay tier's top-16 internal units are a sample, not all units. Proposed new recording detail requires scientific review; no model, tokenizer or GPU work is part of the static viewer or this session.
- Research-source context for builders: provide experiment-owned bibliography entries with their program-document citations and short relevance notes, alongside the run's input set and source card. A bibliography is contextual reading, not a second results authority. No experiment-associated research paper has been opened; associations and bibliographic completeness remain to audit during an authorized preparation phase. The two UI-reference READMEs opened below are a separate context lane.
- Reviewed-source shortlist read for later builder-context discussion: `results/dashboard_integration_review_20261011/uiskills_report.md:5-19` recommends one interface guide and one chart checklist, warns that scripts/secondary playbooks were not audited, and requires pinning mutable sources before later adoption. `results/dashboard_integration_review_20261011/web_report.md:5-23` recommends retaining static LabViz and treats ECharts/Tabler/Altair/Perspective as later trials; it does not establish file-URL/iPhone compatibility or telemetry safety. These are review findings, not fresh external-repo verification. Concrete source extracts still to discuss; no install is approved.

### Proposed builder context packets (references, not installs)

| Source | What exactly to give a builder | Why it helps this design | Safety and verification boundary |
|---|---|---|---|
| Current LabViz spec, implementation and October 8 browser proof | Binding §4A rules, the relevant §5/§6/§7/§11 spans, this decision record, selected existing phone screenshots/measurements and the current README flow. | Preserves existing five-view navigation, experiment identity, evidence limits and measured readability while extending zoom/playback/input/paper coverage. | Existing proof predates MathLab; re-check the eventual changed product after the hold. No runs now. |
| dammyjay93/interface-design | A short reviewed extract covering hierarchy, consistent spacing, focus/detail layout and complete loading/empty/error states; pair it with the operator's chosen view order and panel behavior. Review source: `results/dashboard_integration_review_20261011/uiskills_report.md:28`, direct source links `:72`, `:82`. | Gives builders concrete layout/state criteria without loading several overlapping design skills. | Original repo/SKILL not opened in this session. Text-only context; no images sent externally, saved system file, skill execution or new tools. Keep spec font/native-control rules; inspect and pin any excerpt before later use. |
| Anthropic data-visualization | A short chart-selection/accuracy checklist: units, denominators, matching scales, uncertainty, missing gaps, readable labels and non-color cues. Review source: `results/dashboard_integration_review_20261011/uiskills_report.md:29`, source links `:73`, `:83`. | Guides change-size bars, comparison charts, per-part maps and time plots using the actual recorded operands. | Original SKILL not opened in this session. No Python examples run or packages installed. Scope its 3D-chart caution to numerical encodings; it must not remove the operator's required 3D structural diagrams. Licence checked before copying text. |
| Tabler | After direct verification, one narrow responsive layout example for adjacent panels and phone stacking; extract geometry/spacing behavior, not a full theme or dashboard template. Review source: `results/dashboard_integration_review_20261011/web_report.md:26`. | Provides context for the approved non-obstructing desktop side panel and below-diagram phone detail. | README not opened in this session. No CSS/JS adopted. Avoid remote fonts/CDNs/plugins; bundled licences and actual phone fit require separate checks before any later copy/trial. |
| Apache ECharts | After direct verification, one documentation example for interactive zoom/selection/source-aware tooltips and, if relevant, a per-component heatmap or linked step cursor. Review source: `results/dashboard_integration_review_20261011/web_report.md:37`, `:52`; [README](https://github.com/apache/echarts#readme) opened at the context gate. | Offers a chart-interaction pattern builders can compare with the existing SVG implementation; does not provide scientific records or the 3D model diagram. | README opened; second docs/example page not opened. No installation/adoption. Any future trial must use local assets, preserve missing values/source links, meet the total first-view budget and avoid canvas-drawn text under §4A. SVG-rendering details, file-URL/phone compatibility and performance remain unverified. |
| Axiom and dashboard-practice articles | A small panel worksheet: reader question → exact quantity → unit/denominator → source/operands → reason unavailable; plus reader tasks for each journey. Review sources: `results/dashboard_integration_review_20261011/uiskills_report.md:8`, `:48-51`; `practices_report.md:5-10`, `:20-29`. | Checks whether each new panel answers a real question and whether the operator understands both the result and its limits. | Original pages not opened in this session. Borrow criteria only; no Axiom API, dashboard mutation, tracking service, uploads or new acceptance authority. |

Other reviewed candidates are deferred context, not adoptions: Altair is an export candidate rather than the granular-player foundation; Perspective is relevant only if many-run analysis outgrows current filtering; uPlot/Charts.css are narrower chart alternatives. Do not introduce them alongside ECharts without a demonstrated need (`results/dashboard_integration_review_20261011/web_report.md:31`, `:33`, `:41-42`, `:54`). Aim's tracker/status must not replace recorded files or scientific labels (`:38`, `:44-46`).

### External reading completed immediately before the context stop

- [Apache ECharts README](https://github.com/apache/echarts#readme) opened via web, reading the README only. It documents a JavaScript chart library, official docs/examples and installation/CDN choices. No installation or example execution occurred. One additional documentation page remains within the per-repo reading allowance; it was not opened. Chart zoom, synchronized cursors, source-aware tooltips and SVG text compliance are candidate extract tasks, not newly verified implementation claims.
- [Transformer Explainer README](https://github.com/poloclub/transformer-explainer#readme) opened via web as a candidate for component-level explanatory context. It describes an interactive view of internal Transformer operations and runs live GPT-2 in the browser. Proposed builder extract: the README's component-explanation framing and its linked research-paper pointer; any concrete visual pattern needs inspection of at most one further page. Do not install, launch or embed its live model, copy its GPT-2 structure onto another model, or substitute its generated data for experiment records. Its linked paper, demo, code and dependencies were not opened or audited. Pattern usefulness for our granular player remains an inference to assess, not proven compatibility.

Neither new README finding has been discussed with the operator yet. No third-party data upload, cloning or tool execution occurred. The context stop interrupted this source-context topic; finish it in the successor, not here.

### Functioning explained from current files

Recorded JSON/logs and documentary context → source-linked run cards/context graph → generated static HTML/scripts/diagrams → browser views. The current builder reads records and joins documentary context; it does not run the experiments (`tools/labviz/README.md:14-16`). Detailed card scripts load on demand; selection carries between the five destinations (`:12`). Viewing the page does not generate new experimental measurements. Actual telemetry and observation re-creations enter through separately labelled readers/records, never through the generic scored-data reader (`docs/LABVIZ_V2_SPEC.md:962-965`). The proposed granular player needs suitable source frames; UI code cannot manufacture missing scientific measurements. The separate telemetry-serving path and observation tool remain outside this session's build/launch authority (`:836-838`, `:938-952`).

## Session continuity

Context rule: watch the "Context N% left" line. At or below 45% left, or on any "Context compacted", tell the operator, finish the current point, and write `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff.md` with topics covered, a pointer to these decisions, open questions, the next point and this same rule. Never put that handoff inside this notes file. The repo's earlier context gate also applies: at or below 40%, stop starting new work.

## LVB2 — builder-context packaging

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "How should we package the outside references for builders?" Option 1 was "Selected extracts per task — recommended. Clear examples with an explanation of what to borrow." Settled: a small task-specific packet with binding spec ranges, relevant agreed decisions and existing phone screenshots, one layout checklist, one chart-accuracy checklist, and outside examples relevant to the assignment. Candidate examples still need inspection; no package adoption or execution is authorized.

### Open questions

- Concrete extracts remain to select and verify. Next: what a recorded playback step needs so granular diagrams, charts and input/answer text stay synchronized. Historical gaps and the separation of recorded measurements, re-creations and explanatory diagrams remain binding (`docs/LABVIZ_V2_SPEC.md:320-328`, `:896-931`).

### Spec changes proposed

- No additional product-spec amendment is needed for the packet decision itself. Previously proposed granular-player and cross-journey amendments remain pending; the spec is unchanged.

### Context for build agents

- interface-design: hierarchy, spacing and loading/empty/error-state extracts; Anthropic data-visualization: units, scales, uncertainty, missing-data and readable-label extracts. Purpose: one focused layout guide and one chart guide per task. Original sources not opened in LVB2; scripts and secondary material remain unaudited (`results/dashboard_integration_review_20261011/uiskills_report.md:19`, `:28-29`). Supply source/version and check licence before copying; no skill execution.
- Tabler: one relevant layout/phone-stacking example; ECharts: one relevant chart-interaction example; Transformer Explainer: one relevant component-explanation example. Example pages remain unopened; previous README findings are above at lines 90-91. Candidate basis: `results/dashboard_integration_review_20261011/web_report.md:26`, `:37`, and the external-reading entries above. Keep each selected experiment's model structure and recorded data; the Explainer's live GPT-2 runtime is outside the viewer contract. No clone, install, remote assets or model execution.
- Each packet names the reader task, applicable spec lines, source/version, exact pattern to borrow, evidence/missing-data limits and unresolved checks. Existing October 8 screenshots predate MathLab and illustrate existing behavior rather than prove the proposed design.
- LVB2 context rule: at or below 45% remaining, or on any "Context compacted", finish the current point and write the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff2.md` with decisions pointer, open questions, exact next point and this rule. Start a new piece only at >=60% remaining. Never put the handoff in these notes.

## LVB2 — deep input-linked model detail and learning

### Decisions (with the operator's words)

- Operator verbatim: "Deep detail for inputs as well as any and all parts of the model that were/are effected by those inputs with that data associated to it along with any explnations for science and learning by a non-technical user."
- Preserve this as an input-linked, model-wide depth requirement: detailed inputs, all affected model parts and their associated measurements, plus nontechnical scientific explanations. The operator did not choose a restriction to selected demonstration inputs or a fixed sample of internal parts. The design must connect input -> sequence step -> model part -> recorded measurement -> explanation/source, and allow exploration from either the input or the part. This extends the earlier granular-zoom condition; it does not reduce it to layer summaries.
- Interpret "affected" with explicit distinctions: stored-number changes, changes in the signals passing through a part, and the part's role in processing the selected input. Unedited stored numbers do not establish unchanged activity (`docs/LABVIZ_V2_SPEC.md:636-641`). Recorded association is not by itself a causal explanation of an answer or a location where a fact is stored (`:595`, `:603-604`). Show the measurement and its comparison basis; unseen parts remain "not recorded", never "unaffected".

### Open questions

- How should nontechnical learning be presented: explanation beside the selected input/part/step, a guided walkthrough first, or both selectable? Next operator question concerns this learning preference.
- The full capture inventory and feasibility remain to define per experiment: exact model structure, all input sets, component coverage, sequence resolution, available before/after comparisons, sources and missing fields. Model-wide means input/output stages and intermediate parts, not only the edited layer band. Existing historical data cannot establish exhaustive affected-part coverage (`docs/LABVIZ_V2_SPEC.md:325-328`).
- Later preparation must assess recording/storage cost and observer effects before any scientific recording change. No instrumentation, observation rerun or model execution is authorized here.

### Spec changes proposed

- Extend §5 items a-d and §6-7 with an explicit input-to-component measurement link and coverage inventory. A frame identifies run/model/configuration and source version; input identity/role/text and recorded pieces; phase/step and recorded time or untimed source order; component/subcomponent identity; measurement, units and before/after comparison basis; source path/key or line; and unavailable fields/reasons. The same frame drives synchronized diagrams, charts and input/answer text. Proposed fields are a design target, not an implemented schema.
- Replace a fixed top-16 sample as the definition of sufficient granular coverage with an explicit requirement to assess the useful depth needed for all affected parts. Any practical sampling remains visibly disclosed and a limitation against the operator's broader target. Current sampling boundaries are at `docs/LABVIZ_V2_SPEC.md:328`, `:638`, `:863-872`; no exhaustive recording capability is established by the current spec.
- Extend the plain-language captions to selected inputs, components and playback steps: what the part normally does; what was measured for this input; what changed under the stated comparison; what the experiment's sourced interpretation says; and what is still unknown. Introduce technical words through a short plain-language definition. Separate general model explanation from experiment-specific observation and reviewed scientific interpretation. Existing relevant caption/evidence rules are `docs/LABVIZ_V2_SPEC.md:584-587`, `:619-625`, `:627-648`. No new verdict or causal claim may be generated by the viewer.

### Context for build agents

- Give the builder the verbatim requirement above, the selected model's own structure, input lists bound to the exact run version, a per-part/per-input data-coverage table, available measurement frames and their provenance, and approved explanatory text with source references. Show both recorded data and explicit gaps, including gaps at finer zoom levels.
- For component explanations, candidate external references supply a teaching pattern only. Adapt terminology and diagrams to the selected model; do not copy another model's structure or use its demonstration outputs as our experiment data. Add related papers through the already-required research-source links, with the documented basis for each association. Concrete external examples remain unopened.

## LVB2 — learning routes

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "How would you prefer to learn?" Option 1 was "Both — recommended: explore with explanations, or follow a guided walkthrough." Provide both free exploration with selection-specific explanations and an optional guided walkthrough of the same experiment data. These learning routes supplement the three already-approved player modes; they do not replace or narrow those modes.
- Both routes retain the selected experiment and source/evidence labels. A guided explanation must link each statement to the relevant input, model part, sequence step or research source; conceptual teaching is visibly distinguished from what this experiment recorded. Missing observations remain explicit in either route.

### Open questions

- Learning-route entry and return behavior will be fleshed out with navigation; no initial route preference was selected by this answer. Proposed routine default: exploration, with a visible walkthrough entry and a return to the prior selection.
- Next discussion: access to complete input sets and associated research papers across journeys, including how much plain-language paper context appears before opening the original source.

### Spec changes proposed

- Clarify §4A.1 and §5/§7.6: selection-specific learning explanations and an optional source-bound guided walkthrough are available within experiment exploration, with cross-links to the existing Learn and evaluations destination. Keep the five top-level destinations (`docs/LABVIZ_V2_SPEC.md:341-353`); use the existing plain-language evaluation fields as a basis for experiment interpretation (`:584-587`). Initial state and return behavior remain proposals until the navigation discussion.

### Context for build agents

- Give the builder paired reader tasks using the same run: freely select an input and explain a measured component change; follow a walkthrough to the corresponding step and find the same measurement/source. Include definitions of technical terms, reviewed captions, relevant associated papers, recorded/re-created/diagram labels and expected missing-data wording. This is a future reader-verification design; no test or browser run occurs now.

## LVB2 — paper reading cards

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "What should happen when you select a paper?" Option 1 was "Reading card first — recommended, with an 'Open original' link." Selecting an associated paper opens a short reading card: what the paper investigates in plain words, how this experiment uses it, the section supporting that association, and an explicit link to the original paper. The associated-papers requirement across journeys was already settled; this decision specifies presentation.
- Retain the prior distinction between sources cited/used by the experiment and related reading. An association needs its program-document citation; a paper-level statement needs its own supporting location. Where either has not been verified, show that gap rather than inventing a role or a page reference. Reading cards are source-bound context, not new experimental evidence.

### Open questions

- Next: input selection and detail order. Proposed browser: the complete available run-specific input set, searchable and grouped by purpose (facts supplied, training/practice text where applicable, evaluation questions, and side-effect checks). Highlight the input selected in the player while retaining access to the complete set; include expected/observed answers and the scoring explanation where available.
- Paper associations and summary completeness still need a later source audit. No experiment bibliography or paper has been freshly audited in this session. Return from a reading card should preserve the originating experiment/input/component/step; detailed navigation remains to discuss.

### Spec changes proposed

- Extend the previously proposed Research and sources section (§6 and §11.1-11.2, `docs/LABVIZ_V2_SPEC.md:662-674`, `:983-1023`) with reading-card fields: title and recorded bibliographic details, plain-language topic, experiment role with association source, supporting paper section/page where verified, original link, and association/summary verification gaps. Cross-journey access remains required. No spec edit is made.

### Context for build agents

- Supply verified bibliographic entries and concise reviewed reading-card text, with distinct citations for the experiment association and any paper claims. Extract the reading-card presentation pattern; preserve deliberately opened original links and explicit missing metadata. No automatic paper download, external summary service, research upload or live model-generated explanation is authorized.

## LVB2 — input-detail order

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "When you select an input, which order would you prefer?" Option 1 was "Input and answers -> model detail — recommended." On input selection, lead with exact input text and expected/observed answers, then the associated fine-grained model detail. Include the run's recorded scoring explanation; an absent expected or observed answer is explicitly missing. Do not generate an answer to fill the panel.
- This presentation applies when selecting an input across the journeys, including within the player or from a model part. It retains input-to-part links and all three player modes, and does not restrict exploration to final outcomes.

### Open questions

- The complete searchable input browser grouped by purpose remains the proposed implementation arrangement; this reply specifically settles detail order. Exact sets are bound to the selected run's recorded configuration/version, with supplied/training/evaluation/side-effect roles distinct and a complete-set route beside focused selections.
- Next: navigation and playback continuity. Proposed behavior: preserve run, input, component, player mode, step and zoom when opening details or papers, switching 2D/3D, entering/leaving a walkthrough or using Back. Extend linkable selection state; when a requested step does not exist in another route, show the mismatch and offer valid positions rather than silently jumping. Automatic pause while reading is the next operator preference.

### Spec changes proposed

- Clarify the cross-journey Inputs and answers section in §4A.1, §5 item a and §6 (`docs/LABVIZ_V2_SPEC.md:338-355`, `:619-625`, `:662-674`) with the approved input/answer-first arrangement and links to corresponding component measurements. Preserve source-precedence and version-bound input text (`:623`), explicit missing values and the recorded scoring rule (`:620`).

### Context for build agents

- Supply the input role, exact text, expected and observed answers where recorded, scoring kind/rule, run/configuration source identity, and linked component/step measurements. Match comparisons by fact/question identity and scoring kind, never row position (`docs/LABVIZ_V2_SPEC.md:580`). Design complete lists for phone use with expandable rows and search; the selected subset does not replace the full available set. Source text and unverified transcription remain visibly distinct.

## LVB2 — pause while reading

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "Which behavior do you prefer?" Option 1 was "Pause while reading — recommended." Automatically pause playback when the reader opens a detailed explanation or paper reading card. Returning retains that position; the reader presses Play to continue. Brief captions already visible beside the animated data do not themselves trigger a pause on every frame.

### Open questions

- Next: mode-switch continuity. Proposed option: preserve the selected source step when it exists in the new mode; if it does not, remain paused, explain that absence and offer valid recorded positions. Alternative: explicitly restart each new mode at its first available step. No silent jump or invented intermediate frame.
- Other proposed navigation defaults remain: preserve run/input/component/zoom when changing 2D/3D or opening/returning from source detail; retain an origin state for walkthrough return; expose selected mode/step/input/component/zoom in a link. A link opens paused and displays missing/unresolvable selection explicitly. These are design proposals, not behavior verified in the current build.

### Spec changes proposed

- Add the approved pause/return behavior to §7.6 and the focused-detail/reading-card requirements (`docs/LABVIZ_V2_SPEC.md:919-931`, `:353-355`). Expand selection state beyond the existing run/line/compare fields as previously proposed. Spec remains unchanged.

### Context for build agents

- Provide two reader-task examples: open a deeper component explanation during playback and return to the same paused frame; open its associated paper card and return without losing input/component context. Use the same source-labelled frame for diagrams, charts and text. Future verification must distinguish expanded reading from inline captions; no browser or test run now.

## LVB2 — mode continuity and phone player proposal

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "Which switching behavior do you prefer?" Option 1 was "Keep the matching step — recommended; choose another when unavailable." Switching between Experiment phases, One fact/question and One component preserves the matching source step where it exists. If unavailable in the new mode, playback stays paused, states why and offers available positions. Do not silently reset, choose an approximate step or invent intervening frames.

### Open questions

- Next phone-layout preference: keep essential playback controls visible in a compact band with reserved layout space, or let them scroll with the focused diagram. A persistent band must never overlay the diagram or approved detail panel; eventual phone/zoom checks must establish that its reserved height leaves the focused view useful.
- Proposed standard controls follow the existing contract: Play/Pause, Previous/Next step, a timeline selector, speed, and selectors appropriate to the three approved modes (`docs/LABVIZ_V2_SPEC.md:919-931`). Source/evidence status and current position remain readable. Untimed sequences use step/order wording, not an invented clock.

### Spec changes proposed

- Add approved mode-switch behavior and a paused unavailable-selection state to §4A.1 and §7.6 (`docs/LABVIZ_V2_SPEC.md:353-355`, `:919-931`). Phone control placement remains proposed. Preserve 44px touch targets, 360px no-horizontal-scroll behavior, 13px text floor and text/pattern state labels (`:360-373`).

### Context for build agents

- Existing screenshot re-inspected in LVB2: `results/labviz/review/20261008T130913325Z/chromium-phone-model-2d.png`. Qualitative observation: the page stacks a long layer listing, parts, static wiring and recorded events. It predates MathLab and does not show or validate the newly proposed granular player. Use it to explain why focused views and reachable controls matter; do not claim a current runtime defect from this historical image.
- Existing phone Map measurements re-read: `results/labviz/review/20261008T130913325Z/measure.json:825181-825210` records 390x844, matching 390px client/scroll widths and 1905px document height. This is Map horizontal-fit evidence only, not player control acceptance or proof that the model screenshot has those dimensions.
- Builder packet: these approved continuity/pause rules, relevant §4A and §7.6 extracts, the existing screenshot, and later reader tasks for switching modes at both a shared and an unavailable step. Include all synchronized diagrams/charts/input text and a source link at the selected frame. No new browser review or test occurs in this discussion.

## LVB2 — visible phone controls

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "Where should the essential controls sit?" Option 1 was "Stay visible in their own band — recommended." Keep Play/Pause and Previous/Next step visible while exploring on a phone, in a compact band occupying its own layout space. It never covers the focused diagram or detail panel. Maintain 44px targets and readable labels.

### Open questions

- Exact reserved height and phone-landscape/zoom behavior require later authorized design verification. Additional mode/input/component selectors, timeline and speed must remain reachable; the answer does not require putting every control into the persistent band.
- Remaining design work: specific reference extracts, chart and missing-data presentation, full navigation/reader-task handoff. Standard player proposals: all panes share a source-labelled step; playback stops at the end of the selected sequence rather than silently cycling; untimed data uses ordered steps, not a manufactured duration. These defaults remain proposals.

### Spec changes proposed

- Specify persistent essential phone controls with reserved non-obstructing space in §4A and §7.6. Retain the existing phone/text/contrast rules (`docs/LABVIZ_V2_SPEC.md:360-373`) and player controls (`:919-931`). Future measurements must cover both themes, narrow/landscape phone and zoom; existing October 8 proof does not cover this new band.

### Context for build agents

- Supply the approved control/panel/pause/mode-switch decisions alongside the historical phone screenshot and spec minimum sizes. Require the future reader to change a step, read its explanation and return without losing position or scrolling back to find essential controls. No current build, test or browser run is authorized.

## LVB2 — bounded primary-source checks for builder extracts

### Decisions (with the operator's words)

- No new operator decision in this section. These checks make the already-approved task-specific reference packaging concrete; they do not adopt packages or execute skills.

### Open questions

- Tabler's actual phone-stacking/side-panel markup and Transformer Explainer's concrete zoom/teaching visuals remain unverified. Their references cannot be treated as tested solutions. Source versions are mutable and not pinned; pin and check licences before a future builder packet copies text or code. No secondary skill reference or executable was audited.
- Next reader preference: one explained chart at a time on a phone, with all applicable measures reachable through a selector, or applicable charts stacked on the page. Preserve the input/component/step across chart switches. Missing data should remain labelled at the relevant part and in a coverage summary; no missing cell becomes zero or "unaffected".

### Spec changes proposed

- No amendment is required merely to supply reference extracts. Any new chart selector/arrangement should be documented under §5 items b-d, retaining §4A's source, text and non-color requirements (`docs/LABVIZ_V2_SPEC.md:360-373`, `:627-657`). Chart references do not override the required structural 3D view or the operator's model-wide depth target.

### Context for build agents

Primary pages opened read-only on 2026-10-11; no clone, install, demo launch, local scripts or model execution. Per-repo reading remains bounded to README plus at most one additional page. Reopening ranges of the same page does not establish its linked references.

| Source actually opened | Selected extract / exact builder context | Intended LabViz use and limits |
|---|---|---|
| [interface-design SKILL](https://raw.githubusercontent.com/dammyjay93/interface-design/main/.claude/skills/interface-design/SKILL.md), Design System Essentials and Static polish sections | Short checklist for hierarchy, consistent spacing, dedicated focus/control states and loading/empty/error states; tabular numbers prevent moving labels. | Check focused diagram/detail layout in both themes. Exclude its native-control replacement advice, default-font rejection, 40px minimum alternative and execution/save/image-generation workflow. LabViz's 44px floor and existing contract prevail. Source licence not freshly checked. |
| [Anthropic data-visualization SKILL](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/data/skills/data-visualization/SKILL.md), Accuracy and Accessibility sections | Checklist for zero-based magnitude bars, common scales for comparable units, labelled axes/units, supported uncertainty, non-color labels/patterns and a data-table alternative. | Explain recorded component changes and comparisons. Do not invent uncertainty intervals, copy Python examples, use insight titles as new verdicts, or apply its numerical-chart guidance to remove the required structural 3D model. The spec's rendered 13px text floor prevails over generic point sizes. Licence not freshly checked. |
| [ECharts Event and Action](https://echarts.apache.org/handbook/en/concepts/event/), event parameters and dispatchAction sections; README opened previously | Documentation example for identifying a clicked data item and programmatically highlighting a corresponding item/showing its detail. Give a builder the selected passages and a local-record selection task. | Proposed adaptation: selected chart point -> the same input/component/frame in diagrams, explanation and source panel. This adaptation is an inference, not tested LabViz integration. Omit example search links, database requests, sample business data and automatic timer cycling. SVG/text compliance, phone/file-URL behavior and asset budget remain unverified; renderer docs were not opened. README plus one extra page allowance is used. |
| [Tabler README](https://github.com/tabler/tabler) and [Layout index](https://docs.tabler.io/ui/layout) | A layout-context catalogue: consistent navigation, page titles/breadcrumbs/actions and page structure. | The index links to examples but contains no inspected side-panel/phone-stacking markup. Give its catalogue as optional reading; use our approved layout and existing screenshot as concrete geometry context. Do not claim Tabler proves the desired stacking behavior. Omit CDN starter assets and bundled plugins; actual subset licences/traffic/phone behavior remain unverified. README plus one extra page allowance is used. |
| [Transformer Explainer README](https://github.com/poloclub/transformer-explainer) | Its framing of explaining internal operations in relation to an input and next-word-piece output; paper pointer. | Candidate teaching context only; no concrete visual/zoom example verified. README explicitly runs live GPT-2 in-browser: no runtime/model/demo is embedded or executed. Use the selected experiment's own architecture and recorded signals. The linked ACM paper was attempted but returned Internal Error: **not opened**. No alternative paper/demo/code page was opened. |

- Axiom/practices panel worksheet remains review-derived context (`results/dashboard_integration_review_20261011/uiskills_report.md:48-51`): reader question, exact quantity, unit, source and explicit blocker. Original Axiom/article pages were not opened in LVB2; no platform/API work is authorized. Pinning and licence review are future preparation needs, not completed acceptance.

## LVB2 — phone charts and consolidated design draft

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to "Which arrangement would you prefer?" Option 1 was "One explained chart at a time — recommended." On phones, show one explained chart at a time, with every applicable available measure reachable through a selector. Each chart includes units, its source and plain-language meaning; unavailable measurements remain explicit. Chart switching preserves input, component and playback step. This is presentation, not a restriction on recorded coverage.

### Open questions

- All operator decisions above remain settled. Remaining discussion can pressure-test the connected design with an on-paper input walkthrough, refine diagram/chart teaching, or review the consolidated handoff. No further choice is required about the already-approved three journeys or activity placement.
- Routine design defaults proposed below have not been individually chosen: complete searchable input browser grouped by purpose; initial Experiment phases mode, paused; exploration with a visible optional walkthrough entry; initial theme follows the device and subsequent choice is remembered locally where supported; end-of-sequence stops playback; navigation/link state as listed below. Preserve these as proposals, not operator quotations.
- Preparation dependencies: model-specific component topology, source-version-bound complete input sets, per-input/per-part coverage inventory, reviewed explanations/bibliographies, immutable reference extracts and licence checks. Richer future observation requires its own recording plan, inertness/resource review and scientific authority. Current historical detail is incomplete; no viewer can infer the missing trajectory.

### Spec changes proposed

Consolidated draft for MAESTRO; binding spec remains unchanged:

| Area | Resulting behavior / amendment target | Existing anchor |
|---|---|---|
| Home and question journey | Compact dated activity strip, then big picture -> findings with limits -> detailed activity. Question page: findings/limits -> history -> latest experiment. | `docs/LABVIZ_V2_SPEC.md:340-345`, `:1086-1096` |
| Comparison | Identities/eligibility notice -> outcomes and measured side effects -> setup differences -> per-question answers. Pair corresponding measures on phones; keep source/scoring/unit differences visible. | `docs/LABVIZ_V2_SPEC.md:578-582` |
| Model exploration | 2D -> 3D -> guided explanation; model -> layer -> component -> finest available experiment-specific detail. Link inputs to all affected parts and their data; disclose unobserved parts/depths. | `docs/LABVIZ_V2_SPEC.md:627-657`, `:325-328` |
| Learning and research | Free exploration plus optional walkthrough over the same sourced data. Inputs lead with exact text and answers. Papers open a plain-language reading card with experiment role, supporting section and original link. | `docs/LABVIZ_V2_SPEC.md:584-587`, `:619-625`, `:983-1023` |
| Player and navigation | Three selectable modes; one source-labelled frame drives diagrams/charts/text. Opening deeper explanations or papers pauses; return stays paused. Mode switching retains the matching step, or pauses and offers available steps. Proposed Back/URL state retains run/input/component/mode/step/zoom and observation identity; unresolved selections are explicit. | `docs/LABVIZ_V2_SPEC.md:353-355`, `:919-931` |
| Phone and themes | Focused views with detail below on narrow phones, side panel in its own space on wider screens. Essential controls remain visible in a reserved band. One explained chart at a time, all applicable measures accessible. Light/dark switch with equivalent readability. | `docs/LABVIZ_V2_SPEC.md:357-373`, `:405-420` |
| Observation coverage | Each source step binds run/model/configuration/input/component identity, order/time, measurements/units/comparison basis, sources and missing fields. Assess needed depth beyond fixed top-16 summaries. Actual recordings, later re-creations and conceptual diagrams remain distinct. | `docs/LABVIZ_V2_SPEC.md:856-875`, `:896-931` |

Functioning, checked against current documentation: recorded files + documentary links -> source-linked run cards/context -> generated static page -> linked views. Cards preserve original precision and source hashes; derived values retain operands; display rounding never changes card values (`tools/labviz/README.md:12-16`, `docs/LABVIZ_V2_SPEC.md:662-676`). The browser visualizes supplied records; it does not run science or load models/tokenizers/weight files (`docs/LABVIZ_V2_SPEC.md:16-20`, `:31-32`). The existing Phase 1 generic reader excludes observation replays/telemetry and EXPLORATORY records; richer views require the separately labelled paths, not relaxing that reader (`tools/labviz/README.md:14`, `docs/LABVIZ_V2_SPEC.md:962-965`). MathLab retains its shared event reader and MATH-PROXY label; it is not model-internal evidence (`tools/labviz/README.md:18-20`).

Proposed source/missing-state defaults: a tapped number opens a source detail with original value/unit, exact file/key or document line, and calculation operands if derived. "Not recorded for this run" means absent measurement; "Could not read this data" describes load/parse failure with a visible reason; "Not comparable" states an eligibility mismatch; "Not judged yet" preserves absent scientific judgement. A measured zero remains zero, never missing. Unknown component activity is not "unaffected". Static activity wording includes source date and does not claim current liveness. Historic scientific results do not expire merely because they are old. Conceptual wiring motion says "diagram, not recorded activity"; later observation frames retain NOT EVIDENCE. A 3D rendering failure offers available 2D/text data without pretending 3D rendered (`docs/LABVIZ_V2_SPEC.md:32`, `:365-373`, `:580`, `:646`, `:906-917`; `tools/labviz/README.md:28`). These are proposed presentation defaults subject to the existing evidence rules.

### Context for build agents

- Assign narrow viewer work using the relevant rows above plus exact spec ranges, accepted operator quotations, selected existing phone images and the primary-source extracts table. The decision record cannot silently override the binding spec: MAESTRO needs explicit amendments and a scoped brief before building.
- Separate viewer preparation from data preparation/recording: topology, input provenance, paper association and coverage inventory must identify what actually exists before promising exhaustive playback. Observation capture, reruns, recording budgets and model access remain separately gated. A useful UI reference provides a pattern/checklist, never experiment data or scientific acceptance.
- Future reader verification: (1) reach a question's finding and explain its unresolved limit; (2) compare two runs and identify a refused comparison; (3) select an input, read its answers, trace available component measurements and identify a gap; (4) switch modes at a shared and an unavailable step; (5) open explanation/paper and return to the same paused position; (6) follow a walkthrough and find the same underlying source as free exploration. These are planned tasks, not tests performed.
- Future mechanical verification retains the binding spec counts/limits, including <=1 MB uncompressed initial view, no horizontal page scroll at 360px, 44px targets, >=13px rendered text, contrast and both themes (`docs/LABVIZ_V2_SPEC.md:354`, `:360-373`, `:405-420`). Existing October 8 measurements/screenshots do not validate new player, theme or later MathLab UI. No new scientific/UI acceptance is claimed.

- Citation corrections after numbered re-reading: the 3D fallback source for the paragraph at line 325 is `tools/labviz/README.md:26`, not `:28` (which describes review tooling). The 44px touch-target rule is `docs/LABVIZ_V2_SPEC.md:367`; an earlier phone-control chat link pointed to `:369` (stacked table rows). The requirements themselves are unchanged. Continuation/design handoff saved separately as `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff2.md`; it is not approval to build or a statement of new acceptance.

## LVB3 — one input end to end on paper

### Decisions (with the operator's words)

- Operator verbatim: "Start with 1", replying to the continuation choices: walk one input end to end on paper (recommended), refine diagram/chart teaching, or review the consolidated handoff. Begin with the on-paper walkthrough. This selects the discussion topic; the specific screen wording and missing-activity transition below remain proposals. All earlier decisions and the building hold persist.

### Open questions

- Proposed walkthrough uses C10W P1, oracle_p1, A7_coined_coined, Zorbland. Source: `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:49739-49752` records the subject, template `If you visit {}, its capital city is`, generated text ` Vindex Vaskul,` and `full:true`; the expected answer `Vindex Vask` and rewording hit array `[false,true,true]` are at `:58507-58517`. The recipe starts at `:37710`, before these records; oracle_canon_s0 starts at `:59673`. Filling the recorded template with the recorded subject yields the proposed displayed input "If you visit Zorbland, its capital city is"; this is a source-bound assembly, not a separately recorded full prompt. Any other prompt wrapper remains outside this excerpt.
- Proposed screen sequence: (1) exact input/expected/generated text and recorded scoring explanation; (2) selected experiment's model diagram, with stored-number edits distinguished from information passing through it; (3) sourced measurement/chart at the selected component and step, or an explicit gap; (4) plain-language explanation of that measurement and its limit; (5) associated paper reading card where the association and supporting section are verified, otherwise a visible association gap; (6) return to the same paused input/component/step. This is a paper design exercise, not an observed interaction or browser test.
- A layer's recorded write size summarizes a change to its stored numbers across the run; it is not a measurement of this input's effect or proof of where its fact is stored. The recorded input/output pair does not supply its historical internal trajectory. No input-to-component coverage audit or bibliography verification was performed. No missing observation is replaced with an invented value or intermediate animation.
- Next operator preference: when a guided walkthrough reaches unrecorded internal activity, continue with clearly labelled structural teaching and visible gaps (recommended), or pause the recorded walkthrough at its last supported observation and offer structural teaching as a separate learning segment. Both retain free exploration, complete available inputs and the broader affected-part coverage requirement; neither invents a trajectory.

### Spec changes proposed

- No new spec amendment is approved by the topic choice. The walkthrough makes the pending input/answer, measurement/source and paper-card proposals concrete. Existing anchors: exact facts/questions and scoring at `docs/LABVIZ_V2_SPEC.md:619-625`; stored-number changes versus changed flow at `:627-648`; unavailable historical internals at `:325-328`; synchronized player and re-creation labels at `:896-931`. The eventual transition between recorded observations and conceptual teaching must make its change of meaning explicit. Spec remains unchanged.

### Context for build agents

- Supply this source-bound example alongside the approved input-first/pause/return decisions and selected spec spans. Reader task: identify the actual generated words, explain why the recorded scoring calls them a match, find a measurement's source and scope, recognize the internal-activity gap, and return from reading without losing position. Preserve leading spaces/punctuation in exact source text. Do not substitute a literal string-equality test for the recorded scoring.
- Use the previously selected chart-accuracy checklist for measurement scope and missing values, and the layout checklist for the focused diagram/detail arrangement. External examples supply presentation patterns only. No new repository page, paper, screenshot, code, package or skill was opened/executed here; source revisions/licences and experiment paper associations still need authorized preparation. No build/test/model process was run. Worktree root and branch `worktree-c10k-route-a` were verified read-only.

## LVB3 — broader learning linked to experiments and papers

### Decisions (with the operator's words)

- Operator verbatim: "1 approved. Also include broader learnings about ML/LLM architecture, engineering, science that contextualizes the specific science learnings associated with the experiements. Also any context that might be relevant from the science research paper (s) to also use as learnings and understanding."
- Recording-gap transition approved: continue with clearly labelled "How this part works" teaching, separate from recorded activity. Retain the missing-record notice; conceptual teaching never supplies an invented historical measurement or animation.
- Learning scope expanded: explain broader machine-learning and language-model architecture, engineering practices, and scientific methods that help the reader understand the selected experiment. Include relevant explanations and context from its associated research papers, beyond bibliographic details alone. Teach from first principles for a reader without ML background, define necessary terms, and connect each topic back to the experiment. Both already-approved free exploration and guided learning remain available.

### Open questions

- Proposed learning structure: "How it works" (general architecture), "How we change and test it" (engineering), "What this experiment teaches us" (sourced scientific finding and limits), and "What the paper contributes" (its method, assumptions, relevant findings and limitations with supporting sections). Relevant science-method lessons include why training performance and answers to new wording differ, why other abilities are checked, and why a changed signal alone does not establish a cause or a fact's storage location. These are teaching-topic proposals, not new findings about the selected run.
- Proposed navigation: a short relevant lesson beside the selected experiment/input/part/chart, with optional deeper connected lessons in the existing Learn and evaluations destination. Returning preserves the same paused experiment state. Show distinct labels for general explanation, this experiment's recorded observation, its reviewed interpretation and a paper's claim; list important limitations beside the claim they limit. Technical depth remains available rather than flattening explanations to slogans.
- Next presentation preference: brief contextual lesson with expandable depth and an optional connected learning path (recommended), or the full relevant lesson displayed on the experiment page. This concerns the new broader material's initial presentation, not whether both exploration and guided learning exist; that is already settled.
- No associated paper has been opened or freshly verified in LVB3. Paper-derived lesson content, the exact bibliography, applicability to the selected model/method, and supporting section/page references remain preparation dependencies. General paper findings do not become this run's results or establish that this program's method works.

### Spec changes proposed

- Extend the existing era-aware Learn explainers (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`) with experiment-linked foundational architecture, engineering and scientific-method lessons; extend the pending paper-reading-card proposal to source-bound learning extracts and connections to those lessons. Keep the existing five destinations. The current plain-words evaluation fields at `:584-587` support experiment-specific finding/limit text but do not alone specify the broader teaching scope.
- Add the approved recording-gap teaching transition alongside the pending guided-player amendments (`docs/LABVIZ_V2_SPEC.md:325-328`, `:627-648`, `:919-931`). Preserve missing values and model-free/no-verdict boundaries (`:16-20`, `:31-32`). The source graph at `:983-1023` needs explicit lesson/paper associations if represented there; existing document links cannot silently be interpreted as scientific support. No spec edit or implementation authority is granted.

### Context for build agents

- Give a builder reviewed lesson text plus a lesson-to-experiment/input/component/paper association list, definitions of prerequisites, source locations, applicability and limitations. Architecture material must match the selected model; general engineering/science lessons must identify how they apply to this experiment. Paper lessons include the verified section supporting the explanation and a separate citation establishing this experiment's relationship to the paper. Missing associations stay visible.
- Use the previously selected component-teaching references as patterns only, and chart/layout checklists for readability and honest evidence wording. Supply paired reader tasks: explain a general concept, point to its role in this experiment, distinguish the paper's claim from the run's observation, state the unresolved limit, then return to the same paused position. Lessons are reviewed static content; no live explanation service, model execution, automatic paper fetching, package adoption or new browser/test run is authorized.

## LVB3 — expandable lessons and the Learn entry point

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to how the broader learning material should first appear. Option 1 was "Brief lesson with expandable depth — recommended, plus a connected 'Learn from the beginning' path." Settled: short relevant lessons at the selected experiment/input/part/chart, deeper material on demand, and a connected foundational learning path. This retains both free exploration and guided learning, the complete available detail and source-linked paper context.

### Open questions

- Next: the leading entry point within Learn. Recommendation: plain-language questions spanning architecture, engineering and science, with links to relevant model parts, experiments and papers. Alternatives: begin with model parts, or begin with associated papers. All remain accessible whichever leads; the earlier research-era/line tagging is retained. Proposed question examples: "How does a model learn?", "How do we change one fact?", and "What makes a test convincing?" These are curriculum/navigation examples, not scientific claims.
- Lesson prerequisites, exact lesson-to-source associations and reviewed wording still need preparation. No lesson curriculum or paper summary has been audited or implemented here.

### Spec changes proposed

- Clarify Learn's entry/navigation arrangement under `docs/LABVIZ_V2_SPEC.md:346`, `:1058`, preserving the five destinations, context/selection continuity and source links (`:341-355`). Add the approved brief/expandable lesson and foundational-path presentation to the pending broader-learning amendment. A question-first, part-first or paper-first entry would supplement the existing era-aware organisation; that choice is still open. Phone text, contrast and touch requirements remain `:357-373`.

### Context for build agents

- Existing image inspected: `results/labviz/review/20261008T130913325Z/chromium-phone-learn.png`. It shows research-era cards with several technical titles, draft labels and a "Reading a recorded picture" explanation. Use it as historical layout context for the proposed broader-learning entry. Matching measurement block `results/labviz/review/20261008T130913325Z/measure.json:1425370-1425388` identifies Learn, 390x844, 390px scroll/client widths and 2808px document height. Its content/summary at `:1425414-1425431` records 16px body text, 13px minimum rendered text, 44px minimum target height and zero clipped text nodes. These are October 8 measurements, not acceptance for the broader learning design, current MathLab addition or both themes.
- Supply the brief/expandable lesson decision, this historical screenshot/measurement extract, the relevant §4A rules and a future reader task: find a foundational lesson, reach a related experiment and supporting paper section, then return to the original paused context. Borrow hierarchy/spacing from the already-selected interface checklist; keep sources and unresolved limits reachable. No new screenshot, browser run, test, build or external source reading occurred.

## LVB3 — Learn ordering and tutoring/quizzes

### Decisions (with the operator's words)

- Operator verbatim: "1 then 2 then 3. Also, a feature that tutors or quizes a user against each section/card of the learning tab."
- Learn's entry order settled: plain-language questions first, model parts second, papers third. All remain reachable and retain the applicable research-era/line tags. This supplements the brief contextual lessons and connected foundational learning path already approved.
- New feature intent: tutoring or quizzes associated with each section/card of Learn. Do not narrow coverage to a single demonstration lesson or a few selected cards. The tutoring mechanism, answer interaction and progress persistence are not yet selected. This is design intent, not authority to implement or connect a service.

### Open questions

- Recommended interaction: each learning card offers "Teach me" and "Check my understanding". Guided teaching uses reviewed explanations, small questions and hints; quiz feedback explains the answer and links back to the exact lesson/source. Optional practice does not lock access to lessons, diagrams, experiments or papers. These labels and mechanics remain proposals.
- Next mechanism preference: (1) prepared guided tutor plus quizzes, recommended for the existing static/model-free site; (2) open-ended conversational AI tutoring plus quizzes, requiring a separately designed connection; (3) both. Prepared tutoring means authored branches, hints and feedback; it must not be advertised as an unrestricted conversational model. A conversational option remains a proposal with capability, source grounding, uncertainty, data handling and resource/dependency questions to resolve, not an implied install/model/service authorization.
- Example comprehension question derived from an existing guardrail: "Does a brighter answer signal prove the fact is stored in that layer?" Feedback must explain that the signal shows where an answer becomes readable, not where it was written (`docs/LABVIZ_V2_SPEC.md:589-595`). This checks understanding of a lesson, not the model or an experiment's scientific acceptance. Static multiple-choice feedback can be checked against reviewed answer keys; free-text grading cannot be promised without a suitable reviewed mechanism.
- Whether to remember learning progress, how to offer revisits and how deep a quiz should be remain future design points. Learner progress and answers must remain separate from research results, gate states and scientific verdicts. No learner account, external transmission or persistence mechanism has been selected.

### Spec changes proposed

- Clarify questions -> model parts -> papers under the existing Learn destination (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). Add tutoring/quiz coverage per section/card and its eventual selected interaction to the pending broader-learning amendment. No such learner-tutoring flow is specified in the currently inspected Learn anchors; the existing "General-knowledge quiz" at `:523` describes a model evaluation, a different concept.
- Keep source-linked feedback, visible scientific limits, preserved experiment/player context, phone readability and the model-free/no-verdict rules (`docs/LABVIZ_V2_SPEC.md:16-20`, `:31-32`, `:348-373`). Any conversational service would need its own explicit scoped design/amendment before implementation. Binding spec remains unchanged.

### Context for build agents

- Supply the operator's every-section/card requirement, accepted entry order, lesson/source associations and a reviewed question bank: question, targeted concept, answer key, explanation, hints and exact supporting lesson/paper location. Include questions that teach the difference between general principles, a paper's claim, an experiment's observation and unresolved limits. Material lacking reviewed support stays visibly pending rather than receiving invented feedback.
- Reader-task proposal: open a card, request a hint, answer, understand the explanation, revisit its source, and return to the same learning/experiment context. Verify the educational answer separately from scientific experiment scoring. Use the existing layout/chart checklists as text references only; no tutor package, model, account, cloud connector, scripts, build or tests were installed/run.

## LVB3 — prepared quizzes; guided tutor retained for the future

### Decisions (with the operator's words)

- Operator verbatim: "1 with guided tutor durably noted as a future feature."
- Selected mechanism is prepared, source-linked learning material and quizzes. Interpret the explicit future-feature qualification as deferring the guided tutor rather than requiring it in the initial quiz implementation. Preserve that qualification alongside the original option 1 ("Prepared guided tutor and quizzes — recommended: reviewed explanations, questions, hints and feedback") so no scope change is hidden. Guided tutoring remains durably on the LabViz roadmap in this discussion record. No conversational AI tutor, model/service connection or build is authorized.
- Quiz coverage remains each learning section/card. Earlier foundational lessons, expandable depth, sources and learning routes are retained; deferring tutoring does not remove those accepted learning requirements. The initial quiz's exact hint/feedback depth remains to flesh out.

### Open questions

- Next reader preference: remember learning progress on the current device (recommended), or retain it only during the current visit. Proposed remembered state names cards/questions attempted, answers and topics to revisit; it does not declare mastery merely because a card was opened. Persistence is a proposed convenience, not a verified capability in local-file browsers. If storage is unavailable, explain that visibly; do not claim progress was saved. No cross-device service, account or external transfer is assumed.
- Detailed question format, explanation/hint presentation, retries and review order remain open. Guided tutor stays future work; revisit its concrete scope in a later authorized design/build brief rather than silently including it now.

### Spec changes proposed

- In the pending Learn amendment, separate prepared quizzes for each section/card from the future guided-tutor feature. Current Learn anchors are `docs/LABVIZ_V2_SPEC.md:346`, `:1058`; broader-learning and quiz proposals supplement those anchors, while no-verdict/read-only boundaries remain `:16-20`, `:31-32`. Learner progress, if selected, is personal UI state and must never enter scientific results, source measurements, acceptance gates or program verdicts. Spec remains unchanged.

### Context for build agents

- Supply this exact future-feature qualification with the earlier quiz requirement. An eventual initial quiz brief receives reviewed questions, answer keys, explanations and supporting lesson/paper sections; it does not receive an instruction to build a guided or conversational tutor. Preserve source/missing-data labels and the selected experiment's paused state on reading/return. Define optional progress behavior only after the reader preference is settled and verify it under supported file-URL/phone conditions in a later authorized scope.
- Durable future item: guided tutor per learning section/card, using the selected lesson and source context, plain-language teaching and checked feedback. Its exact interaction, prerequisite handling and implementation remain unbuilt and unverified. This notes entry is the scoped durable record; no other memory, roadmap, spec, source or build file was edited.

## LVB3 — saved learning tracker and knowledge scores

### Decisions (with the operator's words)

- Operator verbatim: "1...and with a learning tracker that scores domain/topic/science knowledge plus overall knowledge scores."
- Progress is remembered on the current device, with the previously offered reset option. Add a learning tracker reporting domain, topic, science-knowledge and overall scores. This is learner assessment within LabViz, distinct from the experiments' model scores and scientific acceptance. No account, cross-device service or implementation is authorized by this choice.

### Open questions

- Recommended scope/labels: broad domains (model architecture, engineering, scientific reasoning); finer topics within them; experiment/research-line science understanding; and overall demonstrated understanding across assessed lessons. Domain/topic/science definitions and the exact taxonomy remain proposed. Paper-derived concepts connect to their applicable topics and experiments; one question may support several displayed views but counts once in the overall score.
- Proposed score display pairs accuracy with coverage. Illustrative only: "8 of 10 answered correctly; 10 of 30 questions attempted" (80% on attempted questions, with 20 unassessed). An unanswered question is unassessed, not wrong; an unavailable/unreviewed question does not enter the scored bank. With zero assessed questions show "Not assessed yet", never 0% knowledge. Scores describe demonstrated understanding of the reviewed material, not comprehensive expertise or proof of scientific ability.
- Proposed arithmetic: reviewed questions have equal points; topic/domain/overall summaries aggregate the applicable correct and assessed counts, not an unweighted average of differently sized topic percentages. Each overall question identity counts once, despite multiple paper/experiment tags or repeated attempts. No invented scientific certainty or calibrated ability estimate is attached to this simple learning score. The exact score denominator and attempt rule still need agreement.
- Next scoring preference: latest completed quiz attempt (recommended for current progress, with prior attempts visible), first completed attempt (baseline), or best attempt (achievement). Practice/hints/revealed answers should be distinguishable from scored answers; retaking known questions can reflect familiarity with the questions as well as understanding. The scored/practice interaction and retake details are still proposals.
- Saving must be confirmed by the interface; unsupported/failed local storage remains visible. Save question/lesson version identity with attempts so changed material does not silently inherit an old score. Preserve previous results as historical or request reassessment, rather than pretending the learner answered a new question. Reset applies only to learner progress, never research evidence. Persistence capabilities and quiz inventory remain unverified.

### Spec changes proposed

- Extend the pending Learn/quiz amendment with a device-local tracker, domain/topic/science/overall summaries, score and coverage definitions, version-bound attempts, visible missing/save-error states and a learner-only reset. Current anchors: Learn `docs/LABVIZ_V2_SPEC.md:346`, `:1058`; source/context/readability `:348-373`; scientific no-verdict/read-only boundary `:16-20`, `:31-32`. These anchors do not yet define personal knowledge scores. Any score may summarize learner responses only; it cannot become a scientific verdict or mutate experiment data. Spec unchanged.

### Context for build agents

- Supply the operator's exact tracker requirement, a reviewed lesson/topic/domain/science association table and question bank with stable/versioned identities, answer keys and source locations. Include illustrative score/coverage cases: no responses, partial coverage, mixed correctness, different topic sizes, a multi-tagged question, repeated attempts, changed questions and unavailable storage. Verify that overall totals do not double-count tags or attempts and that unanswered questions remain unassessed. These are future acceptance cases, not tests run.
- Reader task: identify a strong and a weak topic, distinguish accuracy from coverage, see which science lesson an answer relates to, inspect its explanation/source, revisit the lesson and resume learning. Use simple label/count summaries on phones before adding charts. Personal assessment belongs in Learn; experiment scores retain their original meanings elsewhere. No new code, storage, quiz execution, browser run, package or model/service was introduced.

## LVB3 — latest-attempt scoring and answer feedback

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which attempt determines the displayed score. Option 1 was "Latest — recommended: reflects your current performance and can rise or fall." Settled: the latest completed quiz attempt supplies current learner scores; earlier attempts remain visible as history, as included in the recommendation. First/best attempts do not silently replace the selected latest-attempt rule.

### Open questions

- Proposed scoring continuity: an unfinished retake leaves the previous completed result in place and is labelled in progress. On completion, the new result replaces the prior result for that quiz/version in current summaries. Changed lesson/question versions require explicit historical/reassessment handling; never count an old answer as an answer to a new question. This is a design proposal, not a verified data model.
- Next feedback preference: explain each answer after submission (recommended for learning), or reveal explanations at the end of the quiz. Feedback names the correct answer, explains the idea, addresses the selected misconception where reviewed feedback exists, and links to the applicable lesson/source. It preserves the submitted response; seeing the explanation does not let the reader revise that same response into an earned correct answer. A new completed attempt follows the approved latest-attempt scoring rule. Feedback timing is still open.
- Proposed authored question coverage: meanings of concepts, reading diagrams/charts, engineering choices, interpreting experiment evidence and identifying limits or a paper's applicable assumptions. Quizzes use the selected lesson/run/source context and checked answer keys. Exact formats, question counts and hint handling remain to define; no free-text semantic grading or guided tutor is added by this proposal.

### Spec changes proposed

- Add the accepted latest-completed-attempt rule and historical-results presentation to the pending learner-tracker amendment under Learn (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). The incomplete-retake and feedback rules above remain proposed. Preserve source/context/phone constraints at `:348-373` and scientific boundaries at `:16-20`, `:31-32`. No binding-spec edit occurred.

### Context for build agents

- Future cases for a scoped quiz/tracker brief: a higher latest score, a lower latest score, an unfinished retake, prior-result history, a revised question version and submitting an answer before viewing its explanation. Current aggregation uses each applicable question once from the selected completed attempts and shows coverage; no result from personal learning enters scientific cards/gates. These are planned cases only, not tests run.
- Provide reviewed feedback text with a supporting lesson/source reference and an optional selected-wrong-answer explanation. Reading explanation/source retains the selected learning card and experiment/player context. Guided tutoring stays a future feature. No new source reading, browser run, code, package, model or service was used.

## LVB3 — end-of-quiz review, connected summaries and science

### Decisions (with the operator's words)

- Operator verbatim: "2...and summaries each and their connections to each other. And connect this to the science as well."
- Explain answers at the end of the quiz, after assessment is completed. The earlier immediate-feedback recommendation is not selected. Provide summaries of the assessed material, explain how its ideas connect to one another, and connect those ideas to the relevant science. Keep this as a connected learning review, not only a percentage and isolated right/wrong markers.
- Interpret "summaries each" inclusively: individual answer explanations and learning-card/section summaries, with relevant topic connections. Each summary connects to the applicable experiments, reviewed findings/limits and research papers where associations are supported. Exact summary length and presentation remain proposals; do not silently narrow the request to a single overall summary.

### Open questions

- Proposed review order: score and coverage -> each submitted answer with explanation and relevant card/section summary -> how the ideas connect -> where they apply in the science -> topics/lessons to revisit. Feedback preserves submitted responses and links to original lessons and sources; latest completed-attempt scoring remains settled. No guided tutor is brought forward from the future-feature list.
- Proposed science connection explains the research question, why the idea matters to the experiment's design, what was observed, the reviewed interpretation and remaining limits; its paper connection names the relevant method/assumption/section. Distinguish teaching relationships from documented experiment/paper associations and from evidence supporting a claim. No conceptual arrow or shared topic implies causation or scientific validation.
- Next relationship-display preference: (1) both, short written connections first with an expandable visual map (recommended for phones); (2) linked written summaries; (3) visual map first with explanations on selection. All preserve access to summaries and science sources. The visual map would be a proposed learning aid, not a replacement for the existing home-map contract.
- Illustrative connected lesson: learning from practice questions, answering differently worded questions and checking other abilities are distinct parts of evaluating a change. A review explains their relationship and links to applicable source-bound experiment records. This is a teaching outline, not a new finding or claim about an unaudited paper.

### Spec changes proposed

- Extend the pending Learn/quiz amendment with end-of-assessment explanations, summaries per assessed card/section, explicit links between concepts and supported links to experiments/findings/limits/paper sections (`docs/LABVIZ_V2_SPEC.md:346`, `:584-587`, `:1058`). Carry context/selection/source/readability rules from `:348-373`.
- If a visual learning map is selected, adapt the home map's focused plain-word connection explanation and phone drill-down (`docs/LABVIZ_V2_SPEC.md:1086-1096`) while retaining its warning that a link is not evidence. Extend the context model explicitly for learning concepts/cards and their association sources (`:983-1023`); do not silently reinterpret existing edges. Display choice remains open. Spec unchanged.

### Context for build agents

- Supply reviewed end-of-quiz explanation/summary text, a concept-to-concept teaching relationship list with supporting sources, and lesson-to-experiment/paper associations. For each science link, include the research question, association source, applicable observation/interpretation, limitation and supporting record/document/paper location. Unsupported connections are pending, never inferred as established science. The learner score remains separate from experiment scores/verdicts.
- Future reader task: finish an assessment, explain an answer, describe how two assessed concepts relate, find their role in an experiment and its evidence/limit, inspect the associated paper section, then return to the learning review. Use the approved question-first Learn navigation, historical phone Learn screenshot, §4A rules and focused-map pattern as context. No new product, diagram artifact, source-model change, browser run, test, external reading or service was created/executed.

## LVB3 — connected review presentation and learning-design checkpoint

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to how learning-review connections appear. Option 1 was "Both — recommended: short written explanations, then an expandable map." Settled: written connections lead; an expandable visual map also lets readers explore the relationships between assessed ideas and their science/paper context. Keep sources and relationship meaning reachable. The selected quiz feedback still appears at the end, not after each question.

### Open questions

- Learning feature design is recorded across LVB3 entries; remaining details include the reviewed question bank, question formats/hints, curriculum and paper associations, taxonomy and exact score/coverage definitions, versioned attempt handling, local-storage support and phone map geometry. The proposed defaults in earlier entries have not all been individually approved. Guided tutoring remains future work.
- Next proposed discussion menu: (1) navigation and unavailable-data wording across LabViz, recommended to finish practical details of the connected journeys; (2) walk the expanded lesson/quiz/tracker journey end to end on paper; (3) review the consolidated proposed spec amendments. The operator has not answered this next menu. Do not reopen any prior settled choice.

### Spec changes proposed

- Add the selected written-first plus expandable-map learning review to the pending Learn amendment (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`), using source-explained relationships and readable focused/drill-down presentation (`:1086-1096`) under §4A (`:348-373`). Concept teaching, paper claims and experiment evidence stay explicitly distinguishable. The initial site/input walkthrough and all learning additions are proposals against an unchanged binding spec; no build approval follows from this checkpoint.

### Context for build agents

- Give any eventual learning builder the complete LVB3 decision chain, including feedback-at-end, latest-completed-attempt scores, device-local progress, per-card/section assessment coverage and guided-tutor deferral. The learner tracker and teaching map are separate from science scoring/authority. Separate UI work from reviewed curriculum/question/paper preparation and any future scientific observation capture.
- Continuation saved separately in `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff3.md`. This is an arc checkpoint, not a claim that all LabViz discussion or acceptance is complete. No context percentage is asserted; no compaction notice has been observed. No tests, builds, browser runs, installs, science or git mutations occurred.

## LVB3 — navigation and unavailable-data wording

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to the next agenda menu. Begin navigation and unavailable-data wording across LabViz. This selects the discussion topic; the new defaults below are proposals, not separately approved behavior. All prior pause/return, shared-mode-step and phone-panel decisions carry forward.

### Open questions

- Proposed navigation defaults: keep the selected question/experiment/run visible; name the return action by its origin ("Back to this input", "Back to quiz review"); preserve originating selection, paused step and focus/reading position on return. Deliberately following another experiment changes the active context to the named target while keeping an explicit route back to the origin. A requested run/input/step that no longer resolves is reported before offering available selections; never silently select a different run or restart the player. The detailed Back/URL design remains a pending extension to the existing selection contract.
- Proposed plain-language data messages: "Not recorded for this run" for absent observations; "Could not read this data: <plain reason>" for load/parse failure; "Not comparable: <reason>" for an ineligible comparison; "Not judged yet" for absent scientific judgement; "Progress could not be saved" for a failed learner-state write. Put the relevant message beside the affected value/section, with source/reason details available on request. Whole-view failures also receive a clear view-level notice. These refine the earlier defaults at notes `:325`; zeros remain zeros and unknown is never "unaffected" or "no work".
- Separate source-snapshot age from historical scientific validity. Activity says when its source was recorded and does not claim current liveness. A resolved old experiment record is not invalid merely because it is old. Paper associations and missing teaching/question content have their own explicit pending/verification messages. A 3D failure retains the available 2D/text route with a visible failure notice.
- Next personal navigation preference: the deliberate "Open original" research-paper link opens a new browser tab (recommended to retain LabViz), or the same tab. The internal paper reading card already pauses and preserves context; this question concerns only opening the original source. No paper is automatically downloaded/opened and no browser action occurs during this discussion.

### Spec changes proposed

- Clarify origin-named Back navigation, full run/input/component/mode/step/zoom state and visible unresolved selections under `docs/LABVIZ_V2_SPEC.md:348-355`, `:919-931`, without reopening accepted mode/pause behavior. Exact hash/history fields remain a design/implementation proposal.
- Document the distinct data-state wording under existing missing-value rules (`docs/LABVIZ_V2_SPEC.md:32`, `:664-670`), comparison refusal (`:578-582`) and missing linked evaluation (`:584-587`). Personal save failures and external-paper tab behavior belong to the pending Learn/source amendments. No read failure becomes an absent observation or zero. Source details retain exact values/units, file/key or document/line, and derivation operands. Spec unchanged.

### Context for build agents

- Supply the existing §4A navigation/source/phone rules, accepted pause/return decisions and these proposed state cases. Future reader tasks: follow a lesson to another experiment and return; open a source at a paused step; open a stale/unresolvable selection; distinguish absent, malformed/unreadable, ineligible, unjudged and learner-save-error states. Source-support and UI verification remain future work, not performed tests.
- Retain the previously selected interface-design loading/empty/error checklist as text context, excluding conflicting control/font advice and executable workflows. Use the existing phone Learn/model images as historical layout examples only. No source code, spec, build, tests, browser or external service was changed/run.

## LVB3 — original papers in a new tab

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to where a research paper's "Open original" link opens. Option 1 was "New tab — recommended." Original papers open in a new browser tab through the reader's deliberate action. LabViz retains the current selection and paused position; the internal paper reading card retains the existing pause-and-return behavior. No paper/browser was opened here.

### Open questions

- Navigation and missing-state presentation defaults in the preceding entry remain proposals; this answer selects the paper-tab behavior only. Do not silently count it as approval of every proposed default or a build.
- Next proposed agenda: (1) review the consolidated proposed spec amendments, recommended to assess the connected design and its remaining dependencies; (2) flesh out remaining quiz/tracker details; (3) review concrete context packets for build agents. The next agenda question is unanswered as of this entry. Preserve all settled choices if a new message steers elsewhere.

### Spec changes proposed

- Add explicit new-tab original-paper links to the pending Research and sources / reading-card amendment under `docs/LABVIZ_V2_SPEC.md:346`, `:983-1023`, with source identities, deliberate external links and preserved paused state (`:353-355`, `:919-931`). The binding spec is unchanged. Guided tutoring remains future work; original-paper links do not imply automatic fetching, AI summarization or verified bibliography completion.

### Context for build agents

- Include a future reader task: open the internal paper card from a selected frame, deliberately open the original in a new tab, return to LabViz and confirm the same paused selection. Paper metadata and claims need reviewed supporting sections/association sources before publication. Mark incomplete associations explicitly. Existing screenshots do not validate this new interaction; no browser/test run occurred.

## LVB3 — consolidated proposed spec amendments for review

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to the next agenda. Review the consolidated proposed spec changes. This selects review, not implementation or blanket approval of pending defaults. All previously settled choices remain settled; the operator may correct the draft without being asked to choose those behaviors again.

### Open questions

- This consolidation separates accepted intent from unapproved routine defaults and preparation dependencies. It is not a frozen replacement specification. MAESTRO still needs explicit amendments and scoped briefs before building. No acceptance or package adoption has occurred.
- Recommended next review slice: Learn, quizzes and tracker because they are the largest new extension to the existing site. Alternative slices: model-detail recording requirements, or the exact context packets for builders. The operator has not selected a slice yet.
- Still proposed: searchable complete input browser grouping; initial phases mode paused; initial free exploration with walkthrough entry; device-theme default/local preference; stop at sequence end; expanded Back/URL fields and origin-named returns; exact failure wording; score taxonomy/denominators/equal-point aggregation/coverage presentation; incomplete-retake/version handling; question formats/hints; lesson/paper summaries and relationship data. Preserve the accepted outcomes without treating these details as individually approved.

### Spec changes proposed

**Operation and boundary:** existing documented flow remains recorded result/log files and documentary links -> source-linked run cards/context -> generated static pages -> linked browser views (`tools/labviz/README.md:12-16`). Add reviewed lessons, verified paper metadata/sections and prepared question/feedback material as explicit learning inputs. Learner progress/attempts are separate local personal state, not research run records. Clarify that "read-only" protects scientific files/authority while the accepted learner tracker remembers personal progress. The site does not run experiments or load a model/tokenizer/weights; a source, explicit calculation or missing reason accompanies scientific values (`docs/LABVIZ_V2_SPEC.md:16-20`, `:31-32`, `:662-676`). No generated teaching text becomes a new scientific verdict.

| Area | Consolidated design intent | Contract effect and current anchor |
|---|---|---|
| Five destinations | Keep Map, Science lines, Runs, Inside the model, Learn and evaluations. Link the learning extension through the existing Learn destination. | Preserve §4A.1, `docs/LABVIZ_V2_SPEC.md:341-355`; no sixth destination or wholesale platform replacement. |
| Home and questions | Compact source-dated activity strip; main content big-picture connections -> findings with limits -> detailed activity. Question page findings/limits -> history -> latest experiment. | Clarify hierarchy at `:340-345`, `:1086-1096`; status is a dated source snapshot, not an invented live inventory. |
| Run comparison | Run identities and comparison notice -> outcomes and measured side effects -> setup differences -> per-question answers. Pair corresponding phone measures. | Clarify `:578-582`; retain identity/scoring eligibility, explicit refusal reasons, matching-unit scales and single-run uncertainty. No winner verdict. |
| Model exploration | 2D -> 3D -> guided explanation. Zoom below layers to experiment-specific components and available finer detail. Link detailed inputs to any and all affected parts, measurements, sources and teaching. | Extend `:627-657` and data/frame requirements; all-affected-part coverage remains the target, not a selected-demo or fixed top-16 definition. Unobserved parts stay unknown. Model structure must match the selected experiment. |
| Player | Three selectable modes: Experiment phases, One fact/question, One component. Diagrams/charts/text use the same source step. Keep matching steps when switching, otherwise pause and offer available positions. | Extend `:919-931`, `:353-355`; retain distinct recorded events, in-run observations and later re-creations. No invented intermediate motion/timestamps. |
| Reading continuity | Expanded explanations/paper cards pause; return at the same paused position, press Play to resume. Brief inline captions do not pause each frame. Original-paper links open a new tab. | Extend `:919-931`, `:353-355` and pending paper/source fields. Detailed origin/history fields remain proposed; pause/return and new-tab choice are settled. |
| Inputs and papers | Complete available applicable input sets across journeys; exact input/expected/observed answers first, scoring meaning and gaps explicit. Paper reading card gives topic, experiment role, supporting section and Open original. | Extend `:619-625`, §6 `:662-674`, context model `:983-1023`. Bind inputs to run/source version. Cited/used paper associations remain distinct from related reading. |
| Phone, detail and themes | Wide-screen side panel occupies its own space; narrow-phone details below diagram. Essential player controls remain visible in a reserved band. One explained chart at a time, all applicable measures accessible. Light/dark switch. | Extend `:357-373`, `:405-420`, model/player layout. Preserve 44px targets, >=13px text, readable contrast and no horizontal page scroll at 360px. Existing proof does not validate new layouts or themes. |
| Broader learning | Architecture, engineering and scientific-method foundations connect to specific experiments and paper concepts. Brief lessons expand to depth, with a Learn-from-the-beginning path. Free exploration and guided walkthrough both remain. | Extend Learn at `:346`, `:1058`, plain-words context at `:584-587`. General explanation, paper claim, run observation and reviewed interpretation have distinct meaning. |
| Learn entry and recording gaps | Questions -> model parts -> papers. At absent historical activity, retain the gap notice and continue explicitly labelled How-this-part-works teaching. | Extend `:346`, `:1058`, `:325-328`, `:627-648`. Structural teaching is not historical playback; broad coverage cannot be inferred from diagrams. |
| Quizzes and tutor scope | Prepared, source-linked quizzes for each Learn section/card; reviewed questions/keys/explanations. Guided tutor is a durably recorded future feature. | New Learn assessment contract under `:346`, `:1058`. Do not confuse a guided walkthrough with the deferred tutor. No conversational AI/service/model connection is selected. |
| Personal tracker | Remember progress on the current device, with reset. Domain/topic/science and overall scores; latest completed attempt supplies current score, previous attempts remain history. | New personal-state/assessment contract under Learn; clarify scientific read-only boundary at `:16-20`, `:31-32`. Accuracy/coverage taxonomy and precise aggregation remain proposed; local persistence remains unverified. |
| End-of-quiz review | Explain at the end; summaries per assessed answer/card/section, their idea connections and science/paper context. Written explanations lead, expandable relationship map also available. | New learning-review contract under `:346`, `:1058`, adapted from focused/source-explained phone map `:1086-1096`. Relationships do not imply causation or scientific support. |
| Missing/failure states | Proposed distinct messages for absent observation, unreadable data, ineligible comparison, unjudged science, failed learner save and unresolved navigation. Keep reason/source details reachable. | Clarify existing missing/comparison/evaluation rules `:32`, `:664-670`, `:578-587`; exact wording/new navigation defaults are not all individually approved. A measured zero remains zero. |
| Recording and preparation | Inventory exact model structure, source-version-bound inputs, per-input/per-component coverage, source frames, reviewed explanations/questions and experiment-owned bibliography before promising detail. | Extend §6-7 coverage beyond the current sampled summaries (`:856-875`, `:896-931`, `:325-328`). Viewer work cannot create missing historical measurements. Future scientific capture needs its own reviewed plan/resource/inertness authority. |

**Initial versus future scope:** the selected prepared quizzes, broader lessons and personal tracker are proposed additions for a future authorized build; none is currently implemented/accepted by this discussion. Guided tutoring is explicitly future work. A guided explanatory walkthrough is already accepted design and must not be deferred merely because the separate tutor is future work. Historical unrecorded trajectories remain unavailable. Exact source/paper/question preparation and scientific capture are separate assignments from viewer code.

**Verification still required after the hold:** original scientific source/value/hash rules; phone/theme/zoom/source-link/navigation checks; relevant player/reading continuity; prepared answer-key correctness; score/coverage aggregation; learner persistence/error/version handling; first-view size/resource limits. October 8 phone images and measurements are historical context only. No new builds, tests, browser runs, model processes, science or external-source audit occurred.

### Context for build agents

| Packet | Exact material to supply | Reference use and boundary |
|---|---|---|
| Science/navigation viewer | Relevant contract rows/spans, verbatim accepted decisions, known source-bound walkthrough, historical phone views/measurements and intended reader tasks. | interface-design hierarchy/spacing/empty/error extracts, with spec fonts/native controls/44px rule prevailing. No skill execution, remote images or design-file writes. |
| Model/chart/player viewer | Exact selected-model structure, input/component coverage and available source frames; measurement meanings/units and evidence labels; approved focus/player/phone rules. | Anthropic chart-accuracy/accessibility extract; ECharts Event and Action selection/highlight pattern only. Renderer/SVG/file-URL/phone/budget compatibility is unverified. Transformer Explainer README provides teaching framing only; no live GPT-2/runtime or verified visual zoom example. |
| Learn/quiz/tracker | Reviewed curriculum, prerequisites/definitions, stable versioned lesson/question identities, keys/feedback, concept links and source-bound paper/experiment associations; all accepted quiz/tracker decisions. | Existing focused-map pattern and short layout/chart checklists. No reference supplies the experiment findings, learner answer keys or a proven tracker. Guided tutor is explicitly excluded from an initial quiz brief. |
| Source/data preparation | Complete available input lists and provenance; bibliography/verified sections; model-specific topology and coverage audit; immutable extracts and licence checks. | Paper content is reviewed explanatory context, not a second science authority. Missing associations stay pending. Richer observation capture is separately gated and not part of static UI work. |

- Preserve the primary-reference checks/table at notes `:268-295` and per-repo read limits in handoff2 `:42-44`. Tabler's inspected Layout page was an index, not verified phone-stacking markup; give it as optional context only. Axiom/practices remain local-review-derived; original pages unopened. No package is adopted. Source versions/licences and hidden network behavior remain separate future checks before any copy/trial.
- This consolidated draft is the reviewable design artifact within the allowed notes file. MAESTRO should resolve the outstanding defaults/preparation dependencies and freeze explicit amendments before assigning scoped build agents. The operator's hold remains in force.

- Scope clarification for the Initial versus future scope paragraph above: the selected features **are accepted design intent**. "Implemented/accepted by this discussion" refers to implementation or runtime/scientific acceptance: this discussion did not build or validate them. It does not retract the operator's approvals or claim a fresh inventory of current implementation coverage.

## LVB3 — close review of Learn, quizzes and tracker

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which consolidated-design slice to inspect. Review Learn, quizzes and tracker. This selects the review slice; it does not approve all scoring/preparation defaults.

### Open questions

- Connected review journey: choose a plain-language question -> read its brief lesson and expand foundations as needed -> explore linked model parts, experiments and paper context -> take the section/card quiz -> finish assessment -> see answer explanations, individual summaries and concept/science links -> update the device-local tracker from the latest completed attempt -> revisit a relevant lesson/source or resume the originating paused experiment. This assembles accepted intent; specific card fields and score arithmetic below remain proposed. Guided tutor stays future work.
- Proposed learning-card content: the question/idea, prerequisite definitions, a short explanation, relevance to the selected science, relevant diagram/example, documented experiment/paper associations, limitations, and links to deeper material and the quiz. A paper's idea is distinguished from this experiment's observation; generic diagrams are distinguished from recorded model activity. Missing reviewed content or answer keys remain pending rather than receiving invented explanations/grades.
- Central scoring decision still open: show accuracy plus assessment coverage separately (recommended), or lead with the share of the complete reviewed question bank already demonstrated correctly. Illustrative reviewed bank: 30 questions; 10 assessed on completed quizzes, 8 correct. Option 1 shows "80% correct; 10 of 30 assessed". Option 2 shows "8 of 30 demonstrated" (about 27% learning progress), with 2 incorrect and 20 unassessed explicitly separate. Neither calls an unassessed answer wrong or claims comprehensive knowledge. These examples are design arithmetic, not actual learner results.
- This review refines earlier illustrative "attempted" coverage wording: score coverage should refer to assessed responses from the selected completed attempts; unfinished attempts are personal activity/in-progress state and do not silently replace current completed scores. Exact incomplete/skip rules remain proposed. A bank/lesson version change cannot inherit a previous answer as a response to a new question.
- Proposed tracker drill-down: overall summary -> domains -> topics and science-line/experiment understanding -> relevant cards and responses. Show question/lesson coverage and source-linked review recommendations at each applicable level. Multi-tagged questions count once overall; summaries aggregate counts from eligible responses. Equal points, exact taxonomy, bank contents, supported question formats and coverage denominator still require explicit definition before a scoped build.

### Spec changes proposed

- The learning journey expands `docs/LABVIZ_V2_SPEC.md:346`, `:1058` into reviewed foundational lessons, per-card/section quizzes, connected end-of-assessment review and personal tracker, while preserving the accepted five-view/selection/source frame (`:341-355`) and phone rules (`:357-373`). Experiment summaries retain sourced finding/limit fields (`:584-587`); lesson/paper associations explicitly extend the context model (`:983-1023`).
- Define score terms and eligible question/attempt/version populations in the new learner-assessment contract, separate from scientific run-card leaves and research verdicts (`docs/LABVIZ_V2_SPEC.md:16-20`, `:662-676`). The pending scoring preference above is not yet frozen. No spec edit or implementation occurred.

### Context for build agents

- Supply a complete example learning packet: reviewed lesson text/definitions, source-bound model/experiment/paper associations, checked question keys and feedback, concept links, stable question/lesson versions and explicit missing-content cases. The viewer renders these inputs; it is not responsible for inventing the science, paper summaries or answer keys. The deferred guided tutor must not be substituted for authored quiz feedback.
- Future acceptance cases include no assessment, small-sample high accuracy, broad coverage with mixed answers, multi-tagged questions, differently sized topics, a lower latest score, an unfinished retake, a changed question version and failed personal-state saving. Reader verification asks whether accuracy/coverage are distinguishable and whether the learner can reach the relevant science claim and its limitation. No tests, browser runs or new source reading were performed.

## LVB3 — context-gate close and session 4 continuation

### Decisions (with the operator's words)

- MAESTRO directive, verbatim: "MAESTRO context note: you are at about 44% context left. Finish the current point with the operator, then tell them you are writing the handoff, update results/dashboard_integration_review_20261011/labviz_brainstorm_handoff3.md (topics covered, settled choices, the open next point with your recommended options) and the notes, and say when it is saved. A fresh session 4 continues from it. If you have already finished it, just say READY."
- Stop at this context gate. No new design work or question is started. The current scoring-display point is preserved as open because the operator has not answered it. All prior design choices remain settled; no scoring-display approval is inferred from the context-stop instruction.

### Open questions

- Exact next question for session 4: "Which presentation should lead the tracker? 1. Accuracy and coverage separately — recommended: '80% correct; 10 of 30 assessed.' 2. Progress across the whole bank: '8 of 30 demonstrated correctly,' with incorrect and unassessed material shown separately." These are illustrative numbers (30 reviewed questions, 10 assessed, 8 correct), not real learner results. Explain the recommendation briefly: it separates performance on assessed material from how much material has been assessed. Await the operator's answer; do not choose one during the handoff.
- Score taxonomy, exact bank/denominators, equal-point aggregation, question formats/hints, incomplete/changed-version handling and local persistence remain proposed/preparation work. Guided tutor remains durably future work. Latest completed-attempt scoring, historical attempts, end-of-quiz feedback, connected summaries/map and science/paper links are already settled.

### Spec changes proposed

- No new spec change at this gate. Consolidated amendment draft remains at notes `:582-632`; close review of Learn/quizzes/tracker begins at `:634`. Binding `docs/LABVIZ_V2_SPEC.md` and all product/build files remain unchanged. Discussion/design approval is not implementation/scientific acceptance or permission to lift the building hold.

### Context for build agents

- Session 4's continuity authority is the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff3.md`, plus these append-only notes and predecessor settled decisions. Preserve reviewed-source allowances, scientific source/coverage gaps and all no-execution boundaries. No tests/build/browser/model/science/git mutation occurred at the gate.
- Binding context rule carried forward: watch "Context N% left" at the end of each reply before asking anything; start new work only at >=60% left. At <=45% left or any "Context compacted", tell the operator, finish the current point and write a separate handoff with completed/in-flight work, exact paths, settled choices, open risks and one exact next point. At <=40%, stop starting work. Never place the handoff inside notes or approach full-window compaction. Restate this rule in every successor/team handoff. The 44% figure here is MAESTRO-reported, not independently measured.

## LVB4 — tracker accuracy and coverage

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which presentation should lead the tracker. Option 1 was "Separate accuracy and coverage — recommended: '80% correct; 10 of 30 assessed.'" Settled: lead with accuracy on assessed material and assessment coverage as separate measures, at applicable overall/domain/topic/science levels. The example is illustrative, not actual learner data. Unassessed questions count as neither correct nor wrong. Preserve latest-completed-attempt scoring, earlier-attempt history and end-of-quiz feedback.

### Open questions

- Score taxonomy, eligible question/version populations, equal-point aggregation, incomplete-retake rules and local persistence remain proposed/preparation work. With no assessed responses, the proposed display remains "Not assessed yet", rather than a percentage of knowledge. This answer does not approve every earlier scoring default.
- Next quiz-format preference: answer-choice questions about concepts and reading diagrams/charts/experiment evidence, plus optional unscored "explain it in your own words" reflections (recommended), or answer-choice questions alone. Both use reviewed answer keys for scored responses and retain feedback at the end. Written reflections use authored comparison explanations for self-review; no automatic free-text grading or tutor is implied. This format proposal is not yet approved.

### Spec changes proposed

- Define accuracy and assessment coverage separately in the pending learner-tracker contract under Learn (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). Preserve scientific read-only/model-free boundaries (`:16-20`, `:31-32`), source-linked context and phone readability (`:348-373`). The current Learn anchors do not define personal quiz scores; the selected display is an explicit proposed extension, not an existing measured capability. Spec remains unchanged.
- The pending quiz contract must distinguish checked scored answers from any optional self-reviewed written reflection. Exact formats and hint/skip handling remain open. The personal learning score does not become an experiment score or scientific verdict.

### Context for build agents

- Supply the accepted accuracy/coverage wording with reviewed question/lesson versions, response eligibility and source-linked answer keys. Future reader cases include high accuracy with low coverage, mixed accuracy with broad coverage and no assessed responses; unanswered material must never appear as wrong or zero knowledge. These are planned checks only.
- If the proposed reflections are selected, prepare authored prompts and comparison explanations linked to the lesson/science/paper context; keep them separate from checked scores. Neither a chart library nor a UI reference supplies educational answer keys. Use the already-selected layout checklist and historical Learn phone image as context, retaining `docs/LABVIZ_V2_SPEC.md:360-371`. No build, test, browser run, package, model or scientific process was executed. Worktree root/branch were verified read-only; only this notes entry was appended.

## LVB4 — scored answer choices and optional written reflections

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which quiz format to use. Option 1 was "Both — recommended: scored answer choices plus optional written reflections." Settled: prepared answer-choice questions cover concepts, diagrams/charts and interpreting experiment evidence; optional written reflections invite the learner to explain an idea in their own words. Reflections have prepared comparison explanations for self-review and do not affect the checked score. No automatic free-text grading or guided tutor is selected. Feedback remains at quiz end; accuracy and coverage remain separate.

### Open questions

- Next hint preference: hints in optional practice, with scored quizzes answered without hints (recommended for an easily interpreted score), or hints during scored quizzes with helped answers explicitly identified. Practice means prepared questions/hints, not the deferred guided tutor. Exact eligibility/aggregation for helped responses would require a further rule if that option is selected. No hint rule is approved yet.
- Question inventory, number per card/section, skips/incomplete attempts, version handling, taxonomy and local persistence remain preparation or design work. The format choice does not change each-card/section coverage or make an unreviewed question scoreable.

### Spec changes proposed

- Add the selected scored-answer-choice and optional unscored-reflection formats to the pending Learn assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). Reviewed prompts/keys/explanations and clear score labels extend the existing Learn description; preserve scientific boundaries (`:16-20`, `:31-32`) and phone/source/navigation rules (`:348-373`). Hints and practice/scored-answer eligibility remain proposed. Binding spec unchanged.

### Context for build agents

- Provide checked answer choices/keys and source-linked end-of-quiz feedback, plus separately identified optional reflection prompts and authored comparison explanations. A reflection is not marked correct/incorrect by an invented semantic grader and does not enter accuracy/coverage counts for scored questions. Preserve submitted responses and the approved latest-completed-attempt rule.
- Future reader tasks: interpret a diagram/chart or evidence limitation, complete checked questions, read end-of-quiz explanations, optionally write a reflection and compare it with the prepared explanation, then reach the relevant lesson/science/paper source. Use the selected short layout/chart checklists and historical Learn phone context; no reference supplies answer keys. These are proposed verification tasks, not tests performed. Only notes were appended; no build, browser run, model/service, package or science execution occurred.

## LVB4 — hints in practice only

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to where hints should be available. Option 1 was "Practice only — recommended: explore with help, then check understanding without hints." Settled: prepared practice offers hints; scored quizzes are answered without hints. Checked quiz explanations remain at the end. Practice is learning activity and does not update scored accuracy/assessment coverage; this follows the distinction presented between practice and the scored check. Guided tutoring remains future work.

### Open questions

- Next skip preference: allow "Skip for now", keep the response unassessed and show skips separately (recommended to preserve accuracy/coverage meanings), or require an answer to each scored question before finishing. Both must preserve available source-linked explanations at quiz end and the distinction between an unanswered question and an incorrect submitted answer. Skip eligibility, completed-attempt coverage and retake replacement still need explicit rules if skipping is selected.
- Proposed example, not learner data: in a ten-question quiz, seven correct submitted answers, one incorrect and two skips would show "7 of 8 correct; 8 of 10 assessed; 2 skipped". The broader tracker also names its complete reviewed-bank denominator. A skip does not establish lack of knowledge; an unanswered quiz is not 0% knowledge.
- Review materials remain accessible outside the quiz; the interface cannot establish that a learner did not consult outside help. Scores describe performance on these reviewed questions, not a certified examination or comprehensive expertise. No new restriction on lesson/science access is proposed.

### Spec changes proposed

- Add the accepted practice-only hint rule and separate practice/scored eligibility to the pending Learn assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). End-of-quiz feedback, accuracy/coverage and no automatic reflection grading remain as previously settled. Skipping and completion rules below remain proposed. Preserve personal-state/scientific-authority separation (`:16-20`, `:31-32`) and phone readability/source links (`:348-373`). Spec unchanged.

### Context for build agents

- Supply authored practice hints with lesson/source references and a clearly labelled scored check. Practice completion or hinted responses do not replace the latest completed scored attempt. Keep optional reflections separate from checked-question counts. A practice flow uses prepared material and must not silently implement the deferred tutor.
- Future reader cases include using a hint in practice, entering a scored quiz, completing it and reading feedback. If skipping is selected, add separate correct/incorrect/unassessed counts and explicit empty-assessment behavior. These are planned cases only; no tests/build/browser/science/model/service were run. Only this notes entry was appended.

## LVB4 — skip for now and phone quiz layout proposal

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to how uncertain answers should work. Option 1 was "Allow skipping — recommended: skipped questions remain unassessed and appear in the review." Settled: offer "Skip for now"; skipped questions do not count as incorrect and remain visibly unassessed. Include them in the end-of-quiz review with applicable prepared explanations. Illustrative quiz-level display: "7 of 8 correct; 8 of 10 assessed; 2 skipped"; these are example counts, not learner results. Overall coverage uses the separately defined reviewed-bank population.

### Open questions

- Proposed completion/retake defaults, not separately approved: explicit Finish records a completed attempt with answered/skipped states; unfinished retakes retain the preceding completed score. On a completed retake of the same quiz/question versions, use that attempt throughout: skipped questions are currently unassessed and preceding answers stay historical. Do not silently fill skips with earlier correct answers. Finishing with all questions skipped produces "Not assessed yet" and visible skips, not a percentage. Exact overlapping-quiz/question identity rules and version handling still need preparation.
- Next phone quiz-layout preference: one question at a time (recommended), with position such as "Question 3 of 10", Previous/Next, Skip and an explicit Finish/review step; or all questions on one scrolling page. Either preserves selections when moving between questions and keeps correctness/explanations until quiz end. Navigation position is not assessment coverage; optional reflections stay unscored. The layout and detailed controls are proposed, not approved by the skip answer.

### Spec changes proposed

- Add the accepted skip/unassessed/review distinction to the pending Learn assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). Phone quiz layout extends the current Learn design under §4A (`:357-373`), retaining readable text, 44px targets, text-labelled state and no horizontal page scroll. Existing missing scientific data remains a different state from a personal unanswered quiz question. Binding spec unchanged.

### Context for build agents

- Existing historical image inspected in LVB4: `results/labviz/review/20261008T130913325Z/chromium-phone-learn.png`. It shows stacked era cards and a long Learn page, not the proposed quiz interface. Matching `measure.json:1425370-1425388` records a 390x844 viewport, equal 390px client/scroll widths and 2808px document height. Summary at `:1425414-1425431` records 16px body, 13px minimum rendered text, 44px minimum target height and zero clipped text nodes. These October 8 measurements predate MathLab and the proposed learner features; they do not validate quiz geometry or new themes. A focused-question layout is a design inference from this historical context and §4A, not a diagnosed runtime defect.
- Give builders reviewed quiz keys/feedback, explicit answer/skip states and examples showing correctness, coverage and navigation position separately. Future cases include a skipped question revisited before finishing, mixed answers/skips, all skips, an unfinished retake and a completed retake with skips. Preserve checked-score versus optional-reflection separation and end-of-quiz feedback. Use the selected interface checklist for focus and distinct states. These are planned checks only; only this notes entry was appended, with no build/test/browser/science/model execution.

## LVB4 — one-question phone quiz and tracker organisation proposal

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which quiz layout to use. Option 1 was "One question at a time — recommended: focused view, with navigation between questions." Settled phone layout: one question with room for its diagram/chart and answer choices, visible position such as "Question 3 of 10", Previous/Next and Skip; selections persist when moving between questions. An explicit Finish ends assessment and leads to explanations/review. End-of-quiz feedback and optional unscored reflections remain settled. Exact geometry and desktop adaptation require later authorised design/verification.

### Open questions

- Next tracker-detail ordering: broad learning domains/topics first, with research understanding also accessible (recommended for connecting foundations to the science), or understanding of our research questions/experiments first, with broad domains/topics also accessible. The overall accuracy/coverage summary leads either arrangement; both retain every required domain/topic/science view. This does not reopen questions -> model parts -> papers in Learn.
- Proposed broad-domain labels/definitions: Model architecture (how the model is built and processes inputs), Engineering (how changes are made, checked and operated), Scientific reasoning (how tests and evidence are judged). Proposed separate "Our research" grouping presents understanding of this program's research questions, experiments and paper connections. This is a proposed organisation, not a frozen curriculum or mutually exclusive partition: questions may have multiple associations but must count once overall.
- Previously proposed arithmetic/completion/version defaults still require an explicit contract review before a build brief. Exact topic hierarchy, reviewed-bank membership, question counts and local saving remain preparation work. A low assessed-topic accuracy and an unassessed topic must have different wording; neither establishes comprehensive ability.

### Spec changes proposed

- Add the approved focused phone quiz/navigation layout to the pending Learn assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`) under §4A readability, touch and navigation constraints (`:348-373`). Questionnaire position remains distinct from measured learner coverage; optional reflection state stays separate from checked answers. Binding spec unchanged.
- Define learner domain/topic/research associations and the eventual selected tracker ordering explicitly in the pending learner contract, separate from scientific context/evidence authority (`:16-20`, `:983-1023`). The tracker organisation and proposed labels above are not yet approved.

### Context for build agents

- Supply the complete LVB4 quiz decision chain: separate accuracy/coverage; checked answer choices and optional self-reviewed reflections; practice-only hints; skipped responses unassessed; focused phone questions; explanations at the end. Pair the historical phone Learn image/measurements from the preceding entry with the selected interface hierarchy/state checklist. They provide context, not acceptance for the new quiz.
- An eventual tracker builder needs reviewed lesson/question associations, named score populations and explicit aggregation rules, plus source-linked feedback and reader tasks for reaching a topic or research lesson from a score. No UI reference establishes curriculum validity or a scientific finding. Only this notes entry was appended; no product/spec edit, build/test/browser run, service, model or science process occurred.

## LVB4 — domains/topics lead tracker detail

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which tracker detail should lead. Option 1 was "Domains and topics — recommended, followed by our research." Settled: overall accuracy/coverage summary first, then domain/topic detail, then understanding of our research questions/experiments; all score views remain accessible. The presented broad grouping is Model architecture (how the model works), Engineering (how we change and operate it), Scientific reasoning (how we judge tests/evidence), and Our research (specific questions/experiments). Exact finer taxonomy, lesson bank and source associations still require preparation. Preserve the separate Learn entry ordering and the existing five top-level destinations.

### Open questions

- Next arithmetic preference: equal points per checked question, counting each stable question identity once overall despite multiple topic/research associations (recommended for transparent counts), or extra weight for harder questions, requiring reviewed difficulty labels and a distinct weighted-score definition. Equal-point summaries total correct and assessed eligible responses, not an average of unequal topic percentages. This arithmetic remains a proposal until the operator answers.
- Routine completion/version defaults from the skip entry remain proposed, including retention of the preceding completed score during an unfinished retake and explicit handling of skipped responses in a completed retake. Question/version identity and overlap between quizzes must be defined before a build brief. Device-local storage capability remains unverified.

### Spec changes proposed

- Add the accepted overall -> domains/topics -> our-research tracker ordering and broad-group definitions to the pending learner assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`), with links to reviewed lessons and relevant experiment/paper context. Domain/topic/research scores describe learner responses, never scientific run verdicts (`:16-20`). Arithmetic is still pending; exact mappings extend the context model explicitly (`:983-1023`). Phone controls/counts/readability retain §4A (`:357-373`). Spec unchanged.

### Context for build agents

- Supply the accepted hierarchy alongside question/lesson-to-domain/topic/research associations and applicable source locations. A question may appear in several relevant detail views without being duplicated in the overall population; do not assume domain subtotals form a disjoint partition. Show assessed accuracy and coverage together at each applicable level, with distinct not-assessed and needs-review states.
- Use the already-selected interface hierarchy checklist and historical phone Learn evidence to guide readable summaries and expandable detail. An eventual arithmetic packet must contain a multi-tagged question and differently sized topic populations, with approved expected totals. These are planned examples, not tests run. Only notes were appended; no product/spec edit, build/test/browser, package, model/service or science process occurred.

## LVB4 — equal-point scoring and completion/version rules for review

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to how questions should contribute to the score. Option 1 was "Equal points — recommended: every scored question counts equally." Settled: equal points per eligible checked question; count each question once overall despite several topic/research associations. Accuracy is correct responses divided by assessed responses, with the counts visible; coverage separately reports assessed questions against the applicable reviewed bank. Aggregate response counts rather than averaging differently sized topic percentages. Practice, optional reflections and skipped responses do not become scored correct/incorrect answers. These are learner scores, not comprehensive expertise or scientific acceptance.

### Open questions

- Proposed completion/version rules presented for a single design review: (1) an unfinished retake leaves the preceding completed score displayed and is labelled in progress; (2) explicitly finishing a retake makes that latest completed attempt current, including its skips as unassessed, while previous answers remain historical; (3) when a scored question changes, its preceding version's answer remains history and the new version needs reassessment. Unchanged reviewed questions retain their identity and applicable scores. These rules make the settled latest-completed-attempt rule explicit; they are not yet separately approved.
- A completed quiz with only skips has no assessed responses and displays "Not assessed yet" with visible skip counts, not 0% accuracy. Bank version/population labels must explain changes in coverage denominators. Exact question identity/quiz ownership and overlap resolution require a scoped contract; never count duplicate appearances as new overall questions or silently choose among conflicting current answers.
- The actual reviewed curriculum, question keys, source associations, question/version bank and local saving remain preparation dependencies. No device storage capability or learner behavior has been verified.

### Spec changes proposed

- Add approved equal-point/count-based score arithmetic, non-duplicated overall questions and explicit accuracy/coverage populations to the pending Learn assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). The proposed completion/version rules refine this new personal-state contract, separate from scientific record authority (`:16-20`, `:31-32`) and source-bound run cards (`:662-676`). Count labels, phone/readability and selection continuity retain §4A (`:348-373`). Binding spec unchanged.

### Context for build agents

- Provide an arithmetic worksheet with eligible correct/assessed/bank counts, equal points, multiple associations and uneven topic sizes. Include the original illustrative 8 correct/10 assessed/30 reviewed-bank questions and a multi-tagged question counted once overall. Topic/domain/research counts can overlap; overall totals must use unique eligible questions.
- A later completion/version packet must include an unfinished retake, completed retake with skips, all-skipped completion, changed versus unchanged questions and a bank denominator change. Retain prior attempts as history and clear current-versus-historical labels. These are planned cases, not tests performed. Only this notes entry was appended; no product/spec edit, build/test/browser run, model/service or science process occurred.

## LVB4 — completed-attempt and revised-question rules

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to whether the proposed handling rules fit. Option 1 was "Use these rules — recommended." Settled: an unfinished retake retains the preceding completed score and shows In progress; finishing a retake makes its answers current, including skips as unassessed, with prior answers kept as history; a changed question keeps its preceding answer in history and the revised question shows Needs reassessment. Unchanged questions retain their applicable scores. This selects completion/version behavior and does not lift the build hold or verify personal storage.

### Open questions

- The main learner quiz/tracker interaction and score rules are now recorded. Remaining preparation includes reviewed lessons/question keys/feedback, stable versioned question identities, exact domain/topic/research associations and bank populations, experiment/paper source verification, supported persistence/error behavior and eventual phone/theme verification. Handling duplicate appearances of one question across quizzes must follow explicit ownership/current-answer rules consistent with one overall question and latest completed scoring; no conflicting answer selection is established by this discussion.
- Next discussion choices: (1) finish whole-site navigation and missing-data wording, recommended to connect all journeys; (2) inspect the exact context packets for build agents; (3) refine model-detail recording requirements and historical gaps. Navigation/state defaults remain proposed in LVB3's corresponding entry; original-paper new-tab behavior, pause/return and shared-step switching are already settled and must not be asked again. Selected per-task builder extracts and all granular model/player requirements likewise remain settled.
- No new reference search is needed to resume these topics. Preserve the existing primary-source table/read allowances; UI references are patterns/checklists, not adopted packages, educational answer keys or scientific data.

### Spec changes proposed

- Add the accepted unfinished/finished-retake and revised-question rules to the pending versioned learner-state contract under Learn (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). Maintain separate scientific read-only authority (`:16-20`, `:31-32`), explicit score populations and source/context/phone requirements (`:348-373`). Current-versus-historical learner labels extend this contract; they do not reinterpret scientific evidence badges. Binding spec unchanged.

### Context for build agents

- A learner builder receives the complete LVB3/LVB4 chain and reviewed content/version/association inputs, with worked accuracy/coverage and retake examples. Include no-assessment, skips, changed questions, overlapping tags and failed save cases. Feedback stays at quiz end; hints stay in practice; optional reflections stay unscored; guided tutoring stays future work. A builder must not silently restore a skipped prior answer into a current completed retake.
- The relevant interface/chart extracts and historical phone evidence can guide presentation, but educational content validity and source associations need separate preparation. MAESTRO still needs explicit spec amendments and scoped briefs before any build. Only this notes entry was appended; no product/spec edit, build/test/browser run, install, model/service or science process occurred.

## LVB4 — whole-site navigation continuation

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which topic to discuss next. Option 1 was "Navigation and missing-data wording — recommended." Continue that unfinished whole-site design topic. This selects the agenda, not blanket approval of earlier navigation/state defaults. Previously approved original-paper new-tab links, reading pauses/same-position return, player mode continuity and non-obstructing phone layout remain settled.

### Open questions

- Proposed refinement: visible return links name the origin, for example "Back to quiz review", "Back to this input" or "Back to comparison", alongside the existing location trail. Following an internal cross-journey link opens the named destination; the return action restores the originating selection, paused position and reading/answer context as applicable. An explicitly different target experiment is named before selection changes. No silent change to another run or reset to the start.
- Next preference: named return links for cross-journey navigation (recommended for clarity), or reliance on browser Back and the location trail. Both preserve the already-approved paused return and selection behavior; the question is the visibility/wording of the return action, not whether state is retained. Source details and original external paper links keep their existing approved behavior.
- Proposed link/open defaults remain pending: a shared player link opens paused; unavailable run/input/step is identified and available alternatives offered explicitly. Exact state/history fields and supported return/scroll behavior require a later contract and verification. Missing-data wording is the next topic within this agenda.

### Spec changes proposed

- Clarify origin-named return links and expanded learning/player origin state under §4A (`docs/LABVIZ_V2_SPEC.md:348-355`) and §7.6 (`:919-931`). The current selection contract carries run/line/compare; learner card/review, input/component/mode/step/zoom and origin position are explicit proposed extensions. Do not change the existing five destinations or reopen settled pause/return choices. Binding spec unchanged.

### Context for build agents

- Current spec inspected: `docs/LABVIZ_V2_SPEC.md:348-355` provides the location/context/source frame and cross-view run selection; `:578-587` provides refused-comparison and missing-linked-evaluation cases; `:662-676` provides sourced/derived/missing leaf values and source hashes. A navigation builder needs actual target/origin identities, readable destination names and source-state cases, not fabricated links.
- Integration review `results/dashboard_integration_review_20261011/uiskills_report.md:19`, `:28-29` supports a scoped text-only hierarchy/focus/state checklist, with script/secondary-source safety unverified. Preserve its previously selected primary excerpts and exclusions rather than installing a skill. The historical Learn phone screenshot and measurements in the preceding entries illustrate available layout/context space; they do not prove new return behavior. Future reader task: quiz review -> linked experiment/input -> source detail -> same origin review/position, and comparison -> input -> comparison with both run identities retained. No tests/browser/build ran; only this notes entry was appended.

## LVB4 — named return links and distinct data-state wording

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to which navigation style to use. Option 1 was "Named return links — recommended: the destination is clear on screen." Settled: visible origin-named return links alongside the location trail, such as Back to quiz review, Back to this input and Back to comparison. Returning restores the originating context/position and preserves the already-approved paused state and selections. Browser Back remains a supported ordinary navigation action; the selected visible links do not replace its state requirements.

### Open questions

- Proposed distinct messages for review: absent observation -> "Not recorded for this run"; load/parse failure -> "Could not read this data" with a plain reason; ineligible comparison -> "Not comparable" with the mismatch reason; absent scientific judgement -> "Not judged yet"; missing linked explanation -> "Explanation not linked yet"; failed learner save -> "Progress could not be saved". Draft explanatory content is a separate reviewed-status state, not an absent observation or an unjudged experiment. These words remain proposed until the operator answers.
- Recommended placement: the relevant message beside the affected value/section, with reason/source details reachable; add a clear whole-view notice if the entire view cannot load. Show the data's recorded date where activity freshness matters. A measured zero stays zero; old historical evidence does not become invalid merely because it is old. Unknown activity never becomes idle/no work/unaffected. Missing lesson/key/paper association and unresolved navigation retain their own preparation/selection messages.
- Next wording review preference: use these plain-language messages (recommended), or revise specific wording while preserving all distinctions. Link-open paused defaults and exact origin/history fields remain pending; no silent selection substitution is proposed.

### Spec changes proposed

- Add the accepted origin-named returns to §4A selection/navigation (`docs/LABVIZ_V2_SPEC.md:348-355`) and the pending learning/player origin-state amendments (`:919-931`). Define distinct absent/read-failure/comparison/judgement/explanation/save states under existing missing rules (`:32`, `:664-670`), comparison/evaluation requirements (`:578-587`) and the new learner contract (`:346`, `:1058`). Exact new wording/placement is pending. Binding spec unchanged.

### Context for build agents

- Supply source-state examples independently: absent field in otherwise readable source, unreadable/malformed source, eligible/ineligible comparison, missing judgement, missing linked explanation, draft explanation, failed personal saving and dated activity. Preserve source identity and visible reasons. Do not infer an absent scientific verdict merely from an absent plain-language evaluation link.
- Borrow the already-selected interface-design complete-state checklist, grounded in the current spec and historical phone Learn context. `results/dashboard_integration_review_20261011/SUMMARY.md:26-28`, `:55-56` separates honest failure/phone checks from unverified LabViz appearance; terminal findings do not prove a LabViz runtime bug. Future reader tasks must distinguish these states rather than merely find a generic empty message. No tests/browser/build or external source/model/service ran; only this notes entry was appended.

## LVB4 — data-state wording accepted; continuation checkpoint

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to whether to use the proposed messages. Option 1 was "Yes — recommended: retain these distinctions and wording." Settled: Not recorded for this run (absent measurement); Could not read this data (read/parse failure); Not comparable (refused comparison); Not judged yet (absent scientific judgement); Explanation not linked yet (absent linked explanation); Progress could not be saved (failed personal saving). Place the relevant message beside the affected item, retain accessible reason/source details and give a prominent notice for whole-view failure. Absence of an explanation does not establish absence of scientific judgement. Draft content remains a distinct reviewed-status case.
- All preceding LVB4 operator choices remain settled. This checkpoint grants no building, specification edit, scientific acceptance, package adoption or installation authority.

### Open questions

- Recommended exact next topic for a fresh successor: make the Learn/quiz/tracker build-agent context packet concrete, using the now-settled reader journey and rules plus the previously selected task-specific reference approach. Present what material a builder receives and what separate reviewed-content preparation supplies; do not ask again whether to use task-specific extracts or reopen any approved learner/navigation decision.
- Outstanding dependencies: reviewed lessons/questions/keys/feedback and paper sections/associations; finer taxonomy and reviewed-bank populations; question identity/ownership for overlapping quizzes; source-bound model topology/input/component coverage; future capture feasibility; local storage/error behavior and eventual phone/theme/player acceptance. Shared-link paused entry/unresolvable selection behavior, initial theme/mode/exploration defaults and end-of-sequence behavior remain proposed where not separately selected.

### Spec changes proposed

- Add the accepted distinct data-state wording/placement under existing missing and comparison/evaluation rules (`docs/LABVIZ_V2_SPEC.md:32`, `:578-587`, `:664-670`) and the pending learner-state contract (`:346`, `:1058`). Keep scientific authority/read-only boundaries (`:16-20`, `:31-32`) and §4A readability/source/navigation rules (`:348-373`). All accumulated amendments remain proposals against the unchanged binding spec; MAESTRO must freeze explicit amendments and scoped briefs before building.

### Context for build agents

- Supply all six distinct state cases and whole-view failure, with actual reason/source identity rather than a generic empty state. Preserve measured zero, dated static activity, historical evidence validity and the separation between judgement, explanation and draft review. Borrow the selected interface state checklist as text, with existing spec rules prevailing. No trial, runtime check or scientific acceptance occurred.
- Continuation is saved separately in `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff4.md`. This is a proactive learning/navigation arc checkpoint; no numerical context reading is available in the session messages and no percentage is asserted. Start no further piece in LVB4. Binding rule survives: watch Context N% left at the end of every reply before asking anything; start new work only at >=60% left; at <=45% or any Context compacted, tell the operator, finish the current point and write a separate handoff; at <=40%, stop starting work. Never put the handoff inside notes or approach full-window compaction. Restate the rule in every successor/team handoff.

## LVB5 — concrete Learn/quiz/tracker builder packet

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to the continuation menu. Option 1 was "Continue with that packet — recommended." Continue making the Learn/quiz/tracker context packet concrete so a builder knows exactly what material they receive. This selects the discussion topic; the packet details and first example below are proposals. All LVB1–LVB4 settled choices and the building hold carry forward.

### Open questions

- Proposed first complete content-and-screen example: a small foundations section connected to one experiment. Start with how a model uses an input (recommended), how we change a fact, or how we judge an experiment's evidence. This selects the example, not a reduced delivery scope: quizzes for every Learn card/section remain required.
- Reviewed lessons/questions/keys/feedback, supporting paper sections and associations remain preparation dependencies. Stable question identity/ownership across quizzes, exact bank membership and local saving support remain unresolved. No reviewed curriculum or new source verification is claimed.

### Spec changes proposed

- Packaging the context adds no independent product requirement. The packet carries the already-proposed Learn/quiz/tracker extension at `docs/LABVIZ_V2_SPEC.md:346`, `:1058`, with selection/source rules at `:348-355` and readability rules at `:357-373`. These anchors were read in LVB5; they specify era-aware Learn and the existing frame, not the proposed personal assessment system. MAESTRO must freeze explicit amendments and scoped briefs before building. Binding spec unchanged.

### Context for build agents

Proposed packet, following `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff4.md:43-47`:

1. Relevant binding spec spans, accepted LVB3/LVB4 decisions and one complete reader journey: lesson -> quiz -> end review -> tracker -> linked experiment/paper -> named return.
2. Separately prepared and reviewed lesson/question bank: definitions/prerequisites, stable identities/versions, checked choices/keys, end feedback, practice-only hints and optional unscored reflection explanations. The UI builder receives reviewed educational content rather than inventing keys or scientific interpretations.
3. Domain/topic/research associations, documented concept connections and verified experiment/paper sections; explicit pending-content and missing-source cases.
4. Worked accuracy/coverage, unequal topic sizes, overlapping associations, retake/skip/version/save-failure cases and planned phone reader tasks. Illustrative counts remain labelled examples, not real learner results. Conflicting answers across quizzes need a defined ownership rule before examples can assert their resolution.
5. Selected interface/chart checklist excerpts and historical phone Learn image/measurements as presentation context. Preserve the primary-source table at notes `:268-295`, exclusions and used reading allowances. Interface-design supplies hierarchy/states; the chart guide supplies honest scales/units/missing values; ECharts supplies only a selection/highlight pattern; Tabler remains an optional layout catalogue and Transformer Explainer supplies teaching framing only. Source pins/licences, hidden network behavior and new UI acceptance remain unverified. No install or skill execution is authorized.

- Worktree root and branch `worktree-c10k-route-a` verified read-only. LVB5 uses the brainstorming skill for conversational design only; operator scope overrides its generic separate-design-file, commit, browser and implementation workflow. Only this notes entry was appended; no spec/product/build edit, build/test/browser run, model/science process, install/clone or git mutation occurred.
- Context rule remains binding: check available context at the end of every reply before asking anything; start new work only at >=60% left; at <=45% or any Context compacted, finish the current point and write `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff5.md`; at <=40%, stop starting work. No numerical context reading is exposed, so no percentage is asserted. Keep the handoff separate and restate the rule there.

## LVB5 — all three foundations subjects in the worked example

### Decisions (with the operator's words)

- Operator verbatim: "All 3", replying to which subject the first complete example should start with: (1) how a model uses an input; (2) how we change a fact; (3) how we judge an experiment's evidence. Include all three in the worked content-and-screen example. Do not narrow it to one subject. The existing every-Learn-card/section quiz requirement remains; this example is builder context, not the entire curriculum or build permission.

### Open questions

- Proposed arrangement: three connected foundation cards, in the offered order input -> changing a fact -> judging evidence. Each has a brief explanation, expandable depth, a relevant source-labelled diagram/example and its own prepared quiz. Its end review connects the assessed ideas to the other cards and to the selected science; tracker associations follow the accepted domain/topic/Our-research rules. This assembles prior decisions rather than reopening quiz mechanics. Exact lesson wording, question count, keys and source associations still need reviewed preparation.
- Next meaningful example-design preference: follow the same recorded fact/question through all three lessons (recommended for continuity), or use the most suitable recorded example for each lesson within the selected experiment. Shared-example usefulness must be checked against actual available records; conceptual teaching cannot fill historical internal-activity gaps.

### Spec changes proposed

- No additional feature amendment follows solely from including all three example subjects. They illustrate the existing proposed broader-learning and assessment extension (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`). Keep input/scoring provenance (`:619-625`), stored-number versus information-flow distinctions (`:627-648`) and sourced finding/limit captions (`:584-587`). These relevant spans were read in LVB5; binding spec unchanged.

### Context for build agents

- Card 1, input: exact question/input and recorded answer; explain model structure with an explicitly labelled teaching diagram; show available experiment-specific measurements and any gaps. Do not invent word-piece text, input-specific internals or a historical trajectory.
- Card 2, changing a fact: teach the selected run's actual change method and which stored numbers its records identify as changed. Separate that from how information passing through other parts may change; never equate an unchanged parameter with unchanged activity. Do not substitute MEMIT for another run's recorded method.
- Card 3, evidence: explain the recorded scoring rule, differently worded questions, applicable other-ability checks, sourced findings and limits. A recorded scoring match need not be literal string equality; an answer-readable signal does not locate stored knowledge (`docs/LABVIZ_V2_SPEC.md:619-625`, `:589-595`). Missing checks remain missing and the viewer creates no verdict.
- Include reviewed lesson/paper/experiment connections, keys and end feedback separately from UI layout context. Source references: accepted broader-learning chain at notes `:361-426`, current spec spans above, and the primary-reference table at notes `:268-295`. Local review re-read at `results/dashboard_integration_review_20261011/uiskills_report.md:19`, `:28-29`: interface/chart guidance is scoped text context with scripts/secondary references unaudited, not installation or execution authority. No external page, build/test/browser run, model/science or new acceptance occurred; only this notes entry was appended.

## LVB5 — one fact throughout; example records checked

### Decisions (with the operator's words)

- Operator verbatim: "1", replying to the example approach. Option 1 was "Same fact throughout — recommended." Follow the same recorded fact through all three foundations lessons. Do not substitute separate examples as the leading journey. All three subjects and every-card/section quiz coverage remain required; the example is discussion/builder context, not a build or scientific run.

### Open questions

- Proposed working subject is the already-discussed Zorbland example. Re-read `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:49739-49752`: subject Zorbland, template "If you visit {}, its capital city is", output " Vindex Vaskul," and `full:true`. Re-read `:58507-58517`: A7_coined_coined summary has target "Vindex Vask" and reworded-question hit flags `[false,true,true]`. The template filled with its subject is a source-bound assembly, not a separately recorded full prompt or complete prompt wrapper. Exact spaces/punctuation remain preserved in source detail. These are recorded scoring fields, not a new scoring-rule audit or program-wide verdict. Prior example selection/context is at notes `:347-356`.
- Lesson outline: input/answer -> how the selected variant changes a fact -> what the recorded checks support and leave open. Each has a distinct concept check, with explanations at its quiz end and links between the three lessons. Selecting the exact variant's change-method source and verified supporting paper sections remains preparation work; do not apply a generic C10W/MEMIT description without confirming that variant's method.
- Next remaining learner-state fork for the builder packet: if one checked question appears in multiple quizzes, (1) share one current result, supplied by the most recent completed quiz containing that question/version, recommended for consistency; or (2) give each checked question one owning quiz, with other cards linking to it. The existing once-overall rule and latest-completed scoring are settled; how overlapping quizzes select that single current result is not. Under proposed option 1, a skip in the most recent completed quiz leaves that question unassessed everywhere; the older answer is history, not a fill-in. An unfinished quiz does not replace its current result. Canonical identities/versions and deterministic completion ordering still require a scoped contract.

### Spec changes proposed

- The chosen same-fact example adds no independent feature requirement; it supplies context for the pending Learn/quiz/tracker amendment at `docs/LABVIZ_V2_SPEC.md:346`, `:1058`. Explicit question ownership/current-result selection must be part of that amendment before an eventual tracker brief. Existing scientific result/value rules remain distinct (`:619-625`, `:662-676`). No spec edit occurred.

### Context for build agents

- Supply three linked draft lesson outlines around the same fact, the exact source excerpts above and the adopted reader/quiz/tracker rules. Draft questions can assess input-versus-diagram meaning, stored-number versus information-flow distinctions and the limited meaning of recorded answer checks. Answer keys/explanations remain reviewed-content preparation, not a UI builder's invention or already-accepted educational bank.
- Preserve internal-activity gaps: `docs/LABVIZ_V2_SPEC.md:324-328`, re-read in LVB5, distinguishes unavailable historical internals, unstored full change matrices and sampled summaries. A conceptual diagram must not animate this input's purported historical path. No new coverage audit, capture, scoring computation, paper verification, test/build/browser run or scientific acceptance occurred.
- Include an overlap worksheet once the preference is settled: same version answered differently in two completed quizzes, an unfinished second quiz, a completed second quiz with a skip, a revised question and unchanged questions. Keep one overall count, previous response history and the accepted latest/completion/version behavior. This is an explicitly proposed resolution of the handoff's ownership gap, not a reopening of arithmetic or quiz format. Only this notes entry was appended.

## LVB5 — shared current results and varied questions across cards

### Decisions (with the operator's words)

- Operator verbatim: "1...and questions should remain as unique as possible across cards, even if quizing on the same knowledge. They can be phrased differently, approach from different perspectives, etc. That way the learnings become more durable and ingrained."
- Option 1 selected was "Shared latest result — recommended: consistent wherever the question appears." The presented rule is accepted: the same question/version reused across quizzes has one current result from the most recent completed quiz containing it; previous answers remain history, an unfinished quiz does not replace it, and a skip in the latest completed quiz makes it unassessed. The same question still counts once overall.
- Additional content requirement: make questions as unique as possible across cards, including differently phrased questions and different perspectives on the same knowledge. Shared question reuse is supported, not the default authoring strategy. Preserve the operator's durable/ingrained-learning intention as the design goal; this session did not measure educational effectiveness.

### Open questions

- Proposed authoring distinction: independently prepared assessment variants have their own stable identities/versions and share a targeted concept association; identical question reuse shares an identity/result. A correction or revision of an existing question follows the accepted version/reassessment rule, rather than being silently counted as a new item. Explicit bank authoring/review must distinguish these cases; do not deduplicate all questions about one idea, or generate new identities merely from string differences.
- Three draft perspectives on the same distinction (stored numbers versus information passing through a part): input lesson asks whether information through a part can change while its stored numbers stay fixed; editing lesson asks whether untouched parts must behave identically after another part is changed; evidence lesson asks whether changed activity alone proves a part's stored numbers were edited. These are illustrative authored-question outlines, not reviewed bank entries. Their basis is `docs/LABVIZ_V2_SPEC.md:636-641`; scored delivery still uses reviewed answer choices/keys and feedback at quiz end.
- No operator question remains pending after this answer. Next useful packet work: develop the complete three-card phone reader journey and draft content/question fields around the same Zorbland fact, with varied checks and connected review/tracker examples. Confirm the selected variant's change-method source before drafting its experiment-specific editing explanation. Missing paper associations, internal observations and unreviewed educational material remain explicit preparation gaps.

### Spec changes proposed

- Add accepted shared-current-result selection and the across-card question-variety requirement to the pending learner contract under `docs/LABVIZ_V2_SPEC.md:346`, `:1058`. Keep concept/topic association separate from question identity and retain once-overall equal-point aggregation, completion/skips, latest-current/history and revision/reassessment rules. The exact stable-identity and completion-order representation remains an implementation-contract dependency, not a schema frozen here. Binding spec unchanged.

### Context for build agents

- Reviewed-content preparation supplies varied questions targeting concepts from several perspectives, with question identities/versions, card/quiz placement, concept/topic/domain/research associations, reviewed keys and source-linked end feedback. The viewer builder renders and tracks that bank; it does not automatically paraphrase or grade fresh questions. Optional written reflections remain self-reviewed/unscored, practice hints remain outside scored assessment, and guided tutoring remains future work.
- Include two distinct worksheets: identical question reused in two quizzes -> one latest completed current result/one overall count; different authored questions on the same idea -> separate checked items linked to that concept. Coverage/accuracy describe reviewed questions, not a count of independent concepts or demonstrated comprehensive mastery. Question variety alone does not establish a calibrated durability score.
- Preserve the selected all-three/same-fact reader journey and primary-reference exclusions. No new external page, code/spec/build edit, test/browser run, model/science process, install/clone or git mutation occurred; only this notes entry was appended. Context directive remains binding and must survive the separate handoff.

## LVB5 — learning-packet checkpoint

- All three subjects, one fact throughout, shared latest results for identical reused questions and varied question authoring across cards are recorded above. No operator question remains unanswered. Stop starting new work at this proactive arc checkpoint; no context percentage is exposed or asserted, and no compaction notice was observed.
- Continuation saved separately in `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff5.md`. Exact next point: make the three-card same-fact reader journey/content packet concrete, using varied question perspectives and connected review/tracker examples; verify the selected variant's method source before an experiment-specific editing explanation. Existing spec/hold and all prior settled decisions remain.
- Context directive survives: check Context N% left at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted, finish the current point and write a separate successor handoff; at <=40%, stop starting work. Never put the handoff inside notes or approach full-window compaction; restate this rule in every successor/team handoff. Only notes and the designated handoff were written; no implementation or runtime/scientific acceptance is claimed.

## LVB6 — first learning card approved; selected change method located

### Decisions (with the operator's words)

- Operator verbatim: "approved", replying to the complete proposed Card 1 and its short-opening versus fuller-opening question. Accept the short explanation with expandable foundations and source details, a teaching diagram distinct from the recorded example, visible missing-data wording, a checked-choice question and feedback at quiz end. This is design approval, not permission to build or a reviewed educational answer bank.
- Approved card: "What happens between my question and the model's reply?" Explain that information from a question passes through model parts, which use stored numbers to shape the reply; different questions can change activity without changing those numbers. Expand Foundations for model parts, stored numbers and information flow. Diagram: Question -> model parts -> reply, labelled Teaching illustration; it is not a replay of this experiment.
- Example: assemble "If you visit Zorbland, its capital city is" from the saved template and subject; preserve saved reply " Vindex Vaskul,". Expand Source details for the original record. Visible limitation: "This record does not provide the information's path inside the model or a complete saved input." Basis re-read in LVB6: `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:49739-49752`; distinction in `docs/LABVIZ_V2_SPEC.md:636-648`. A broader historical-internals coverage audit was not performed.
- Draft quiz: "You ask two different questions. Must the model's stored numbers change for its internal activity to differ?" Choices: A Yes; B No - different inputs can produce different activity. At quiz end explain B and connect to Card 2's deliberate change to stored numbers. The approved presentation remains subject to lesson/key/source review before publication; the question is not a calibrated educational measure.

### Open questions

- Next discussion slice: Card 2 around the same Zorbland fact, with the selected variant's trained-adapter method rather than a blanket MEMIT description. Proposed opening: "How did this experiment change the model?" Train a small added correction while holding the original stored numbers fixed, then combine that correction with selected parts for the recorded evaluation. An adapter is a small learned correction, not a fact table or a guarantee of isolated knowledge storage. Proposed varied question: after one part's stored numbers change, must an untouched part process exactly the same information? No; unchanged stored numbers do not guarantee unchanged activity. Feedback remains at quiz end and connects to evidence checks in Card 3.
- Expanded detail may distinguish training (base numbers fixed), evaluation (merged effective numbers changed) and restoration after evaluation. Diagram remains a teaching illustration; write-size records do not reconstruct Zorbland's internal path. Exact lesson wording, checked choices, key, source/paper associations and displayed layer naming still require reviewed preparation. Card 2 has not yet been approved.

### Spec changes proposed

- Card 1 supplies a concrete accepted example for the pending Learn/quiz/tracker extension (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`), not an independently frozen schema or a reduced curriculum. Preserve context/source selection (`:348-355`) and the diagram/activity distinction (`:636-648`). The selected method clarifies the existing C10W adapter caption at `:635-641`; no binding spec edit occurred.

### Context for build agents

- Selected configuration: P1 / oracle_p1 / A7_coined_coined / Zorbland. `experiments/track_c/c10w_oracle_read.py:24-27` associates the recipe and training units; `experiments/track_c/c10w_oracle_eval.py:339-342`, `:384-387` chooses the matching training record. `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:72196-72213` records A7, seed 0, rank 16, 400 steps and trainer provenance; `:72435-72440` records its saved adapter reference and frozen_parameters_unchanged:true. No adapter/weight file was opened.
- Method source inspected as text: `experiments/track_c/c10w_oracle_train.py:166-181` freezes original parameters, adds LoRA corrections to band down_proj parts and optimizes only the correction parameters; `:196-206` performs fitting. `experiments/track_c/c10w_oracle_eval.py:89-116` loads the saved correction and adds its delta to the selected weights for evaluation. Recorded band `[4,5,6,7,8]` is at `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:37710-37718`; matching initial/final band hashes at `:65339-65351` record restoration. Hash equality is recorded evidence, not a fresh recomputation here. Current source bytes were not hash-compared to the run's historical trainer hash; final reviewed content must bind to frozen method source.
- Supply the approved Card 1 as content/layout context and the above selected-method excerpts for Card 2 preparation. The current hparams filename alone does not establish MEMIT as oracle_p1's change method. A final packet still needs reviewed source-bound lessons/questions/keys and supporting paper sections. No new repository adoption, installation, external page, source/spec/product edit, model/science process, build/test/browser run or git mutation occurred.
- Root and branch worktree-c10k-route-a were verified read-only. Brainstorming skill used for conversational design only; generic commit/spec/browser/implementation actions excluded by operator scope. Only this notes entry was appended. No numerical context percentage is exposed or asserted. Check available context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. Never approach compaction; restate the rule in the handoff.

## LVB6 — second learning card approved; evidence card prepared

### Decisions (with the operator's words)

- Operator verbatim: "Approved", replying to Card 2's two-stage explanation versus more training detail upfront. Accept "How did this experiment change the model?" with (1) learn a correction while original stored numbers stay fixed and (2) apply the correction to selected parts for testing. Define adapter as a small learned correction. Keep deeper changed-part details expandable and the teaching diagram distinct from information-flow observations. This approves the presentation, not reviewed content or building.
- Accepted Card 2 draft quiz: "One part's stored numbers changed. Must an untouched part now process exactly the same information as before?" A Yes - its numbers stayed fixed; B No - the information reaching it may have changed. At quiz end explain B and connect to Card 3's recorded checks. Source and internal-path limitations remain visible; final source/key review is still required. All prior lessons, question-variety, quiz/tracker and scope rules carry forward.

### Open questions

- Next slice: "What do these results let us say?" Show Zorbland's expected answer Vindex Vask and the three recorded rewording flags as miss / match / match; preserve the full saved reply rather than silently replacing it with the target. Explain that a recorded scoring match is not necessarily literal equality of the entire visible reply. Expand Foundations for answer pieces, scoring rules, checks for unwanted effects on other questions and independent repeat runs.
- Proposed teaching diagram: differently worded questions -> answer checks -> side-effect checks -> repeat-run checks, explicitly an explanation of evaluation, not a result trace. Recorded observation panel holds the Zorbland flags. A separate selected-P1 context note holds the recorded side-effect-check failure and lack of a final judgement in that snapshot. Do not turn per-fact flags, a whole-configuration count or a later phase's finding into one another.
- Proposed varied evidence question: "A recorded measurement shows different activity in a model part. What can that observation establish on its own?" A That this part's stored numbers were edited; B That its activity differed - stored-number changes need separate evidence. End feedback explains B, reconnecting input-dependent flow (Card 1) and deliberate stored-number changes (Card 2); a bright answer signal also does not locate where a fact is stored. Card 3 wording is proposed, not approved or a reviewed bank entry.

### Spec changes proposed

- Card 2 is a concrete accepted example under the pending Learn/assessment extension at `docs/LABVIZ_V2_SPEC.md:346`, `:1058`; preserve the stored-number/activity distinction at `:636-648`. Card 3 follows recorded scoring/source rules at `:619-625`, sourced evaluation context at `:584-587` and answer-readable versus stored-fact distinction at `:589-595`. No additional feature amendment follows merely from these examples; binding spec remains unchanged.

### Context for build agents

- Zorbland target and ordered full-answer flags re-read at `results/c10w_oracle/p1_20261007T223707_598959Z/eval.json:58507-58517`; saved generated reply remains at `:49739-49752`. Current scoring implementation inspected as text: `experiments/track_c/c10e_bandknob.py:109-117` compares generated answer-piece IDs for the target's length; `:358-373` records the canonical/reworded checks. `experiments/track_c/c10w_oracle_eval.py:181-196` records a longer continuation, with full determined by the first n IDs and contains separately determined from text. These are distinct recorded checks, not a new scoring run. Current code was not hash-compared to historical source pins; final educational review must bind to the frozen version.
- Selected P1 context: `results/c10w_oracle/p1_20261007T223707_598959Z/interim_reader_configuration_v2.json:4` is INTERIM / seed 0 / no final label; `:18-29` records count 70 and G4:false alongside the other configuration gates. `results/c10w_oracle/p1_20261007T223707_598959Z/verdict.json:4-6` records INCOMPLETE, final_label:null and routing:null for this P1 reader snapshot. These do not establish the current whole-program state or supersede later phases. Historical interpretation read at `CORPUS/55_C10W_ORACLE_P1_INTERIM.md:13-45`; it describes training, source-bound results, same-frame side effects and limits. No fresh scientific verdict is made.
- Provide the lesson builder with exact scoring-source excerpts, preserved output/flags, the selected snapshot's recorded interpretation and reviewed feedback/connections. Keep missing internal observations and missing final judgement distinct from failed measured checks. Supporting paper sections and a reviewed curriculum remain preparation gaps. No new external page, install/clone, source/spec/product edit, test/build/browser run, model/science process or git mutation occurred; only this notes entry was appended.
- Context rule remains: check available Context before each question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical percentage is exposed or asserted. Preserve the same rule in the successor handoff.

## LVB6 — third learning card approved; connected review and tracker example

### Decisions (with the operator's words)

- Operator verbatim: "Approved", replying to Card 3's proposed balance of results/limits versus giving the differently worded questions more space. Accept the balanced card "What do these results let us say?" with Zorbland's target, recorded miss / match / match flags, preserved saved reply, scoring-rule explanation, visible selected-P1 side-effect/final-judgement limits, expandable foundations and an explicitly labelled evaluation teaching diagram. This completes design approval of the three worked cards, not the reviewed curriculum, whole viewer or a scientific conclusion.
- Accepted Card 3 draft quiz asks what different activity in a recorded measurement establishes on its own: A stored numbers were edited; B activity differed, edits need separate evidence. End feedback explains B and connects input, deliberate changes and evidence. Exact sources/review dependencies remain at the preceding LVB6 evidence-card entry; no new source audit or scientific verdict follows from approval.

### Open questions

- Proposed next worked slice: the connected review and personal tracker across the three card quizzes. Each card retains its own end feedback; an aggregate example does not replace every-card/section assessment or introduce an unapproved combined-quiz requirement. Written connections lead, with an expandable relationship map, following settled LVB3 rules at notes `:609` and handoff4 `:39`.
- Illustrative learner responses in this three-question example only: Card 1 correct, Card 2 incorrect, Card 3 skipped; assessed accuracy = 1/2 = 50%, coverage = 2/3, skipped = 1. This is a worked worksheet, not actual learner data, whole-bank overall coverage or expertise. Proposed review wording links the three ideas: a new input can change activity without editing stored numbers; the experiment deliberately applies a learned correction; recorded checks determine what may be concluded. Link the missed answer to the stored-number/activity explanation and the skip to its evidence question.
- One remaining navigation preference to discuss: Review this idea opens the explanation of the specific misunderstood idea (recommended), or starts its lesson card at the top. Preserve Back to quiz review and the prior selections/location; practice remains optional/unscored, no hints in scored quizzes, and no automatic grading/tutor is added.

### Spec changes proposed

- Card 3 is an accepted example for the pending Learn/assessment extension (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`); scoring/source/evaluation limits retain `:584-595`, `:619-625`. Connected written end review and personal tracker are already accepted proposed extensions, not new features introduced by this example. A precise review-link target would refine selection/return continuity (`:348-355`), with the accepted origin-named return behavior retained. Binding spec unchanged.

### Context for build agents

- Give the content/UI builders the three approved worked cards, their source excerpts and distinct draft question perspectives, separately reviewed lesson/keys/feedback, and this labelled response/count worksheet. Exact topic/domain/research associations remain preparation work. Model architecture, Engineering and Scientific reasoning are the accepted broad domain labels; Our research is the accepted experiment/question detail view (handoff4 `:29`). The sample is a subset of the eventual reviewed bank, never its asserted entire population.
- Score rules re-read at notes `:807`, `:828`: count correct/assessed responses, count each eligible question once overall despite associations, show coverage separately, keep latest completed answers/history, leave skips unassessed and revised questions needing reassessment. Same question/version reused elsewhere follows notes `:985`; distinct authored questions about the same concept remain distinct items. An unfinished retake does not update current scores. No arithmetic test or product run occurred; the worksheet follows settled rules.
- Reviewed paper associations remain pending; show Explanation not linked yet where applicable rather than invent a supporting paper/section. Local saving is unverified; Progress could not be saved must remain visible on failure. Only this notes entry was appended; no product/spec/build edit, external page/install, model/science process, build/test/browser run or git mutation occurred.
- Context directive persists: check available Context before questions; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting new work. No numerical percentage is exposed or asserted. Restate this rule in the handoff.
- Reference clarification after re-reading: the written-first connected end-review rule above is at notes `:612` and `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff4.md:37`, correcting the preceding `:609` / `:39` pointers. The design is unchanged.

## LVB6 — review links open the relevant explanation directly

### Decisions (with the operator's words)

- Operator verbatim: "Open explanation directly", selecting the recommended Review this idea target. Open the specific explanation associated with the misunderstood idea; keep the full lesson card reachable. Retain the settled Back to quiz review action, prior selections/location, optional unscored practice and end-only quiz feedback. This is navigation design approval, not build or storage verification.
- The approved three-card same-fact journey now has a concrete end-review link target. The labelled three-response score/coverage worksheet illustrates settled arithmetic; the operator's last answer specifically selects the link target and does not separately approve every draft phrase or hypothetical response.

### Open questions

- Next navigation detail, carried from handoff5 `:65` and notes `:218`, `:897`: a valid shared link to a selected run/input/player step opens paused (recommended), or starts playing automatically. Existing reading pauses/paused return and cross-mode source-step continuity are settled; first entry from a link is the remaining preference. Unresolvable selections, initial theme/mode/exploration and sequence-end behavior remain proposed for later discussion.
- Reviewed content, exact concept-to-explanation targets, paper associations, stable question/version identity, source coverage and local storage/error behavior remain preparation dependencies. No new runtime or scientific acceptance is claimed.

### Spec changes proposed

- Add the accepted direct-explanation review-link target to the pending Learn/assessment contract (`docs/LABVIZ_V2_SPEC.md:346`, `:1058`) with origin-named return continuity. Shared-link initial playback state would refine existing linked selections (`:353`) and player controls (`:919-931`); the current binding spans were re-read and do not select autoplay versus paused first entry. No spec edit occurred.

### Context for build agents

- Prepare a reviewed association from each checked question's concept to its relevant explanation section, with a full-card link and origin return information. Do not generate an explanation or answer key at click time. Failure to find a prepared explanation must be visible under the settled Explanation not linked yet message; preserve reviewed-content/source distinction.
- Supply the complete LVB6 approved three-card example, the hypothetical 1/2 accuracy and 2/3 coverage worksheet, the direct-review target and accepted learner-state cases from notes `:807`, `:828`, `:985`. Builder preparation still needs worksheet cases for retakes/skips/revisions/overlap/save failure, reviewed content and phone tasks; none were executed. Only this notes entry was appended; no code/spec/product edit, build/test/browser run, install/clone, model/science process, external page or git mutation occurred.
- Context rule remains binding: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical context percentage is exposed or asserted; restate this rule in the handoff.

## LVB6 — linked player positions open paused

### Decisions (with the operator's words)

- Operator verbatim: "1", choosing "Open paused - recommended. Press Play when ready." A valid link to a selected run/question/player step opens at that linked position and stays paused until the reader presses Play. Preserve exact selected context and evidence/source labels; do not fabricate activity for an unavailable step. Previously accepted reading pauses/paused return and mode continuity remain settled.

### Open questions

- Next proposed case: the linked input/step cannot be found in this build. Recommended: retain the exact available run/context, show the requested target and a visible "Cannot find the linked step in this build" notice, then offer an explicit choice of available steps in that same run. If the run itself is unavailable, offer Choose a run without selecting a replacement automatically. Alternative presentation: a dedicated link-problem page, with explicit recovery actions. Neither option silently substitutes another run/step or treats an unresolved link as proof that the historical observation was never recorded.
- This is a navigation-resolution notice, distinct from the six accepted data messages. The reason may be missing target, malformed selection, unsupported field or content absent from this build; show a known reason and retain unknown reasons honestly. Exact URL/state fields and resolution behavior still need a scoped contract.

### Spec changes proposed

- Add accepted paused entry from valid links to §4A selection/link state (`docs/LABVIZ_V2_SPEC.md:353`) and player controls (`:919-931`). An unresolved-link presentation would refine the same selection contract, preserving source/missing-data rules. Binding spec unchanged.

### Context for build agents

- Give the viewer builder valid linked selections plus unresolved-step/input and unresolved-run examples, accepted paused first entry and prior origin-return requirements. Preserve the requested identity, report which fields resolve, and require an explicit reader action before changing selections. Examples are planned behavior cases, not tests run or proof of current link support. No new read beyond the preceding verified navigation spans was needed; only this notes entry was appended.
- All discussion/build boundaries and preparation gaps persist. Check context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical percentage is exposed or asserted; restate the rule in the handoff.

## LVB6 — unresolved links keep available run context visible

### Decisions (with the operator's words)

- Operator verbatim: "1", choosing "Notice within the run page - recommended." When the linked step cannot be found, retain the exact available run/context and display the requested target with "Cannot find the linked step in this build" and Choose an available step. Wait for the reader to select a replacement. If the run itself is unavailable, offer Choose a run without automatic substitution. This accepts the presented recovery behavior, not a finding that historical data never existed. The six scientific/personal-data messages remain distinct.

### Open questions

- Next player default carried from notes `:258` and handoff5 `:65`: at the final available step, stop and remain there with "End of available sequence" and Replay from start (recommended), or automatically repeat the selected sequence with visible repeat behavior. Preserve source order, distinguish sequence end from missing detail, and never invent intermediate frames or a completion verdict. Sequence-end behavior has not been selected yet.

### Spec changes proposed

- Add accepted unresolved-link notice/recovery to the linked-selection contract (`docs/LABVIZ_V2_SPEC.md:353`), preserving resolved identity and explicit selection changes. An end-of-sequence default would refine player controls (`:919-931`). Binding spec unchanged.

### Context for build agents

- Supply unresolved step/input/run cases, known versus unknown reasons, requested-versus-resolved identity display and explicit recovery actions. Missing requested content must not silently select a different experiment or restart playback; an unavailable run gets recovery controls without falsely labelling another run as the requested one. Preserve return-to-origin where an origin exists. These are planned cases, not executed tests.
- Only this notes entry was appended. All discussion/build holds and unverified preparation/persistence/source-coverage limits persist. Check context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write the separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical percentage is exposed or asserted; preserve the rule in the handoff.

## LVB6 — playback stops at the last available step

### Decisions (with the operator's words)

- Operator verbatim: "1", choosing "Stop at the end - recommended." Stop playback at the final available step, retain the diagram/answer and show "End of available sequence" with Replay from start. No automatic loop. The message describes this sequence's end, not experiment completion or scientific acceptance; visible source/missing-detail labels persist.

### Open questions

- Next initial preference carried from notes `:52`: follow the device's light/dark appearance until the reader explicitly chooses a theme, then remember that choice on the device (recommended); alternatively initially use light or initially use dark. The light/dark switch itself is already approved and is not reopened. Persistence remains unverified; no account/cloud state is selected.
- Initial player mode/exploration defaults and exact state/source/content preparation remain pending. Do not convert these defaults into build authority.

### Spec changes proposed

- Add accepted sequence-end stop/replay behavior to player controls (`docs/LABVIZ_V2_SPEC.md:919-931`). Starting-theme behavior would refine the accepted light/dark extension; preserve readable text, contrast, non-colour cues, touch sizes and equivalent eventual verification in both themes (`:357-373`, `:405-420`, re-read in this turn). No spec edit occurred.

### Context for build agents

- Include a last-step/replay reader case and distinguish no available sequence, a stopped complete displayed sequence, gaps within available content and the experiment's independent recorded status. Theme preparation requires reviewed palettes for both modes and device/default/explicit-choice cases; no screenshot or current implementation claim establishes the new theme behavior. Both modes show identical scientific data and evidence labels.
- Only this notes entry was appended; no source/spec/product edit, build/test/browser run, model/science process, external page/install or git mutation occurred. Check context before questions; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical percentage is exposed or asserted; preserve the rule in the handoff.

## LVB6 — starting theme follows the device

### Decisions (with the operator's words)

- Operator verbatim: "1", choosing "Follow the device - recommended." Initially use the phone/computer's light or dark appearance; after an explicit LabViz theme choice, remember that choice on the same device. The approved theme switch remains. This is intended local presentation behavior, not a verified storage capability or account/cloud feature. Both themes retain the same source-bound values and evidence labels.

### Open questions

- Next normal-entry preference, previously proposed at notes `:158`, `:306`: for a selected run when entering Inside the model without a link to a specific step, start with the 2D overview and free exploration, keeping Start walkthrough visible (recommended), or enter the guided walkthrough first. Both exploration and walkthrough are already required; 2D -> 3D -> explanation order remains settled. A valid specific link continues to override general entry with its selected paused position. Initial player mode remains a separate proposed default.

### Spec changes proposed

- Add accepted device-following initial theme/explicit local override to the proposed light/dark extension, preserving §4A readability and equivalent future theme checks (`docs/LABVIZ_V2_SPEC.md:357-373`, `:405-420`). Exploration/walkthrough entry would refine Inside-the-model navigation (`:345`, `:353`) and diagram/player presentation (`:643-657`). Binding spec unchanged.

### Context for build agents

- Include system light/dark preference, explicit override and reload cases; validate actual supported device/file-URL persistence in a later authorized build. Initial theme is presentation state, independent of scientific records. Preserve equivalent text/mark contrast, labels, touch targets and non-colour states; historical screenshots do not prove the proposed modes.
- Viewer entry context distinguishes direct navigation, valid specific links, named returns and unresolved selections; do not let a generic entry default erase a valid linked or returning selection. Selected-model topology and measurement coverage remain preparation inputs; the inspected spec's Qwen-specific structural example is not a universal model diagram. Only this notes entry was appended; all holds/unverified preparation limits persist.
- Check context before questions; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical percentage is exposed or asserted; restate the rule in the handoff.

## LVB6 — normal Inside-the-model entry starts with exploration

### Decisions (with the operator's words)

- Operator verbatim: "1", choosing "Explore first - recommended." Normal Inside-the-model entry for a selected run starts with the 2D overview and free exploration, with a visible Start walkthrough action. Both exploration and guided walkthrough remain available; the established 2D -> 3D -> explanation order persists. Specific linked positions and named returns preserve their requested/origin state instead of resetting to the normal-entry overview.

### Open questions

- Remaining initial player-mode preference from notes `:306`: Experiment phases, paused (recommended for broad context), One fact/question, paused, or One component, paused. Experiment phases means the recorded change/test/side-effect stages; the other modes focus on a selected input or model part. This is a fresh-entry default, not a reset during mode switching, a valid specific link or a named return. The three modes themselves are already accepted. Available records constrain every mode; empty/missing routes must be explicit.

### Spec changes proposed

- Add accepted exploration-first normal entry with visible walkthrough to Inside-the-model navigation/linked state (`docs/LABVIZ_V2_SPEC.md:345`, `:353`) and model/player presentation (`:643-657`, `:919-931`). Initial player mode would refine the accepted three-route extension at those anchors. No spec edit occurred.

### Context for build agents

- Supply separate fresh-entry, specific-link and origin-return reader cases, model-specific 2D overview context and a visible optional walkthrough entry. General teaching must be labelled and not presented as historical activity. Preserve all three player routes, granular depth, source-step continuity and source/missing notices. Builder preparation still requires actual source coverage; no mode default creates missing observations.
- Only this notes entry was appended. All discussion/build holds and unverified content/source/persistence limits remain. Check context before questions; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write separate `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; at <=40% stop starting work. No numerical percentage is exposed or asserted; preserve the rule in the handoff.

## LVB6 — initial player mode settled; planned continuity checkpoint

### Decisions (with the operator's words)

- Operator verbatim: "1", choosing "Experiment phases, paused - recommended." On fresh normal entry for a selected run, initially select Experiment phases and leave playback paused. This gives the recorded change/test/side-effect sequence as the broad starting route; all three accepted modes remain available. Valid specific links, named returns and source-step-preserving mode switches retain their own selections rather than being reset by this default. Available records and explicit gaps constrain every route.

### Open questions

- No operator question remains pending. The three-card same-Zorbland example, direct explanation review links, paused linked positions, in-context unresolved-link recovery, stop/replay at sequence end, device-following initial theme and exploration-first/phases-paused normal entry are settled.
- Exact content/key/paper review, question/version identities and completed-attempt ordering, finer topic/bank population, source/model/input/component coverage, future capture authority, local persistence and eventual phone/theme verification remain preparation work. The short three-question worksheet was shown; complete retake/reuse/revision/save-failure examples are still needed in the final builder packet.

### Spec changes proposed

- Add accepted initial phases-paused default alongside exploration-first entry and specific-link/return precedence to §4A navigation and the player extension (`docs/LABVIZ_V2_SPEC.md:345`, `:353`, `:643-657`, `:919-931`). All LVB6 choices remain proposed amendments to the unchanged binding spec; MAESTRO must freeze amendments/scoped briefs before building.

### Context for build agents

- Supply the LVB6 accepted examples and navigation defaults with separate fresh-entry/link/return cases; follow available source steps and show gaps, never fabricate internal activity or scientific labels. Lesson and question-key review remains separate from viewer construction; primary-reference extracts remain contextual trials, not adoptions.
- Proactive arc checkpoint: no numerical context percentage is exposed or asserted, and no compaction notice was observed. Save continuation separately in `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff6.md`; start no further piece in LVB6. Exact next point: complete a phone-sized tracker behavior worksheet around the three drafted questions using settled retake/skip/reuse/revision/save-failure rules, then continue source/model coverage preparation. Do not reopen settled choices or present a new subject-selection menu.
- Only the append-only notes and designated handoff are authorized writes. No code/spec/product edit, build/test/browser run, install/clone, model/weight/tokenizer/science access, external page or git mutation occurred. Context directive survives: check available Context at the end of every reply before questions; start new pieces only at >=60%; at <=45% or any Context compacted finish the point and write a separate successor handoff; at <=40% stop starting work. Never approach compaction or put the handoff in notes; restate this rule in every successor handoff.

## LVB7 — tracker consequences worksheet; coverage preparation begins

### Decisions (with the operator's words)

- No new operator decision yet. Continue LVB6 without reopening its accepted cards, review links, player/navigation defaults or device-following theme. The building hold remains. The operator's dispatch requests: "The rules are settled, so show their consequences rather than re-asking them" and "never shrink it to a selected demo or a fixed top-16 scope".
- This worksheet applies already accepted rules at notes :807-833 and :980-1002. All learner responses and counts below are hypothetical; they describe only the three worked questions, not actual progress, the whole reviewed bank or measured mastery. A, B and C are conceptual labels for the three distinct authored questions, each at illustrative version 1; they do not establish an implemented identity format or a reviewed bank. Every branch below starts independently from the same baseline unless stated otherwise.
- Baseline: A correct, B incorrect, C skipped -> 1 correct / 2 assessed = 50% accuracy; 2 / 3 assessed coverage; 1 skip. A, B and C remain distinct questions even though they approach related knowledge from different perspectives.
- Unfinished retake: draft A skipped and B correct, without finishing -> baseline stays current: 1 / 2 correct, 2 / 3 coverage; retake is In progress. C is outside that retake.
- Completed retake containing only A and B: A skipped, B correct -> A becomes unassessed, B correct, C retains its preceding skip. Current example becomes 1 / 1 correct = 100% accuracy, 1 / 3 coverage, 2 skips. Prior completed responses remain history; completion replaces results only for questions/versions contained in the retake. The high percentage does not mean full coverage.
- Identical reuse: B version 1 appears elsewhere and its latest completed response is correct -> all appearances share B's current result, counted once overall; A and C unchanged. Example becomes 2 / 2 correct = 100%, 2 / 3 coverage. If that latest completed B response were skipped instead, B would be unassessed -> 1 / 1 correct, 1 / 3 coverage. Reuse itself adds no question to the denominator.
- Distinct authoring: A, B and C already illustrate separate questions about related knowledge; each remains eligible separately. Concept associations do not merge identities. Authors/reviewers must distinguish deliberate new questions from revisions and identical reuse; string differences alone are not an identity policy.
- Revision: replace reviewed B version 1 with reviewed B version 2 -> old B response stays history and current B needs reassessment. A remains correct and C skipped -> 1 / 1 correct, 1 / 3 assessed coverage; 1 skip and 1 needs reassessment. These are different unassessed reasons. No extra current item is created just to retain B's historical version.
- All-skipped completion, supplementary case: a completed retake containing A, B and C with all skipped -> 0 / 3 coverage and 3 skips; accuracy says Not assessed yet, never 0% or 100%.
- Saving failure: display Progress could not be saved beside affected personal progress; do not claim durable saving, infer success from visible feedback, or silently erase the failure. This worksheet does not settle detailed temporary-state/recovery behavior or prove file-URL/device storage. Scientific records remain separate from personal progress.

### Open questions

- Proposed next presentation choice: a compact Recording coverage summary visible above the selected model diagram (recommended, so readers can distinguish model structure from recorded observations immediately), or the same summary behind a clearly labelled Recording coverage button. This is summary prominence only; existing missing-data notices stay beside affected details in either option. No operator answer yet.
- Prepare coverage for the complete required model-wide/granular scope, across applicable models/runs/inputs/parts; the three-card example is neither the scope nor the coverage audit. Exact available populations, historical sources and gaps have not been inventoried in LVB7. Full historical internal paths cannot be inferred from structure, teaching animation, configured write locations or write sizes.
- Reviewed question identities/versions/keys, associations and bank populations, explicit completion ordering and supported storage/recovery remain builder-contract dependencies. Conceptual identity preparation calls for question identity, reviewed version, concept association, placement, reviewed key/feedback/source, and completed-attempt ordering; no schema is frozen here.

### Spec changes proposed

- Worksheet clarifies previously accepted Learn/tracker extensions under docs/LABVIZ_V2_SPEC.md:346 and :1058; binding spec unchanged. Counts refer to personal responses, not run verdicts.
- Coverage preparation retains input-source precedence and complete applicable input categories (docs/LABVIZ_V2_SPEC.md:619-625; notes :49), selected-model component structure and stored-number/activity distinction (spec :627-648; notes :48). The Qwen-shaped example and top-16 sampled replay description at spec :630-639 do not set universal model dimensions or satisfy the accepted model-wide depth. The proposed compact coverage summary would clarify presentation in Inside the model (:345), alongside existing source/evidence framing (:348-352) and recorded-event limits (:651-657).

### Context for build agents

- Give tracker builders this independently branched worksheet with reviewed identities/versions and explicit current-versus-history expectations. Give content reviewers the separate question-versus-concept distinction; the viewer must not generate a bank or keys. No arithmetic test, product run or educational validation occurred.
- Proposed source-coverage worksheet: for each required model/run, identify source/version-bound model structure; the complete applicable training/evaluation/side-effect/probe inputs and expected/observed answers; model/layer/component/finer observations; available step order/times; source locations and known limits at each depth. Separate structure, configured or observed stored-number changes, recorded activity, labelled teaching diagrams and separately authorized re-creations. Never infer absence across uninspected records or fill historical gaps with animation.
- Assignments remain separate: source inventory/content review prepares records and lessons; static viewer construction displays them; future scientific capture must obtain its own reviewed plan/resource authority. Do not silently reduce granular scope because a historical record lacks observations. Proposed coverage summary must state only verified coverage and keep unknown/uninspected coverage explicit.
- Reviewed repos/checklists remain context trials, not adoptions. No new external reference opened; do not claim reviewed code or paper sections from an inherited repository mention. SUMMARY.md:37-55 retains script/network/model/scope risks. No install, clone, live model or remote asset is authorized.
- Root and branch worktree-c10k-route-a verified read-only. Brainstorming skill used for design conversation only; operator scope excludes generic spec-writing/commit/browser/implementation steps. Only this notes entry appended; no spec/source/site edit, build/test/browser run, project Python/node, model/weight/tokenizer/science access or git mutation. General memory search supplied no additional design authority; current handoff/notes/spec ground this slice.
- Context rule: check available Context at the end of every reply before asking anything. Start new pieces only at >=60%; at <=45% or any Context compacted, tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md with completed/in-flight topics, exact paths, settled pointers, open risks and one next point; at <=40% stop starting work. No numerical percentage is exposed or asserted. Never approach compaction or put the handoff inside notes; restate this rule in every successor/team handoff.

## LVB7 — recording coverage summary stays visible

### Decisions (with the operator's words)

- Operator verbatim: "1", selecting "Always visible - recommended, with expandable detail." Keep a compact Recording coverage summary above the selected model diagram. Detailed coverage expands on request; existing source/missing/read-failure messages remain beside affected parts. This approves presentation, not historical coverage, a new schema, recording work or building.
- Preserve the entire model-wide granular intent and all applicable inputs. A missing observation does not remove the corresponding model part from the structure or prove that it was unaffected. Coverage describes the available source material for the selected context; it is separate from learner assessment coverage and scientific judgement.

### Open questions

- Proposed wording example for a hypothetical run, not a claim about the selected C10W record: "Model structure: source linked. Inputs and replies: some details available. Internal activity: Not recorded for this run." Expand detail to identify exact available inputs, missing fields and sources. Use Not recorded only after checking the relevant readable records; a failed read says Could not read this data and an uninspected source remains explicitly unverified. No aggregate completeness percentage or denominator is asserted.
- Recommended next preference: expanded coverage follows model -> layer -> part, with the input/question and available steps attached to each observation, matching model exploration. Alternative: input/question first, then its covered model parts. Either retains whole-model coverage, complete applicable input lists and source links; this is the coverage report's reading order, not a reduction to one input or an alteration of the three player modes. No answer yet.

### Spec changes proposed

- Add the accepted always-visible summary and expandable coverage detail to Inside the model and its source/evidence frame (docs/LABVIZ_V2_SPEC.md:345, :348-352). Preserve model-specific parts and distinctions between stored-number changes, activity and teaching diagrams (:627-648); retain actual recorded-event ordering/limits (:651-657). The existing feasibility table and sampled-summary limits (:305-328) describe the binding version's historical/phase scope, not satisfaction of the operator's wider granular intent. No spec edit occurred.

### Context for build agents

- Supply summary states for verified complete/partial input sets, missing observations, malformed/unreadable records and uninspected coverage, with source/version/context identities. Complete/partial must be defined against an explicit applicable inventory; readable data is not automatically complete. Reviewed structure and teaching explanations cannot stand in for measured historical activity. Notes :889-905 preserve accepted six-message distinctions and whole-view failure placement.
- Source preparation must inventory model structure, applicable input roles, expected/observed responses, component/finer measurements, source-step order and paper/method associations. Viewer preparation renders that reviewed coverage; any future recording remains a separately reviewed scientific assignment. No source inventory, external page, new reference adoption or runtime verification occurred in this slice. Only notes appended; building hold and all execution exclusions remain.
- Context directive persists: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md; at <=40% stop starting work. No numerical percentage is exposed or asserted. Preserve exact paths, decisions, open risks and one next step in the handoff; never place it inside notes.

## LVB7 — model-first coverage order; proposed per-part builder sheet

### Decisions (with the operator's words)

- Operator verbatim: "1", selecting "Model parts first - recommended." Expanded Recording coverage follows model -> layer -> part, with relevant questions/inputs and available recorded steps attached. Preserve all applicable input lists and whole-model granular coverage; ordering does not reduce scope, change player modes or imply observations exist. The preceding always-visible compact summary remains settled.

### Open questions

- Proposed builder content format: a repeated evidence sheet for each model part, continuing to finer detail wherever sources support it. Four sections: (1) What it is - plain explanation, technical name, location and verified selected-model structure source; (2) Stored-number changes - configured write scope versus actual recorded changes, method basis versus measured verification, with units where applicable; (3) Recorded activity - observations tied to exact input/question and available step, separate from stored-number changes, with explicit gaps/read failures/uninspected coverage; (4) Inputs and sources - exact applicable input/expected/observed text, source location/version, associated reviewed explanation and experiment-owned paper/method reference where prepared. Put part/run identity and source version in the sheet's context; finer elements inherit that context explicitly rather than being invented.
- Next operator question: use this four-section sheet as the repeated builder format (recommended for consistent explanations and evidence), or deepen a specified section before accepting the format. This is content/design review, not approval for implementation, scientific capture or a frozen schema. Model coverage must still include every required part; absent data is displayed honestly.
- Source preparation has not yet verified an all-model population or historical per-part coverage. Paper sections, reviewed explanation links, stable internal identities and future finer recording remain open preparation assignments. Never infer a full historical prompt from a saved template/subject or internal motion from write sizes.

### Spec changes proposed

- Accepted model-first coverage ordering clarifies Inside the model/source framing (docs/LABVIZ_V2_SPEC.md:345, :348-352) and part/finer navigation (:627-648). The proposed four-section sheet consolidates accepted requirements, not an adopted implementation schema. Preserve input precedence and source-version binding (:182-213); keep JSON/document/derived/missing leaves and source hashes (:662-676). No spec edit occurred.
- Existing spec distinguishes method-based untouched claims from verification and training/evaluation/restoration (docs/LABVIZ_V2_SPEC.md:180-183). A current model/config/hparams file is not automatically evidence for a historical run; the format must retain its binding rule. The static builder reads source text/records and must not import experiment code to fill gaps (:211-213).

### Context for build agents

- Source/content preparers receive the proposed per-part sheet, selected-model/source-binding rules, complete applicable input roles, exact quoted output/scoring-source requirements, historical/re-creation/teaching distinctions and the accepted data-state messages. Viewer builders receive reviewed populated sheets and coverage states; a format alone is not prepared content or measured coverage. Future scientific recording remains separately planned/reviewed/resource-authorized.
- Keep selected reference extracts at notes :283-295 as task-specific context: interface-design's hierarchy/focus/loading/empty/error checklist for layout/state review; Anthropic data-visualization's units/scales/non-colour/table checklist for recorded measurements; ECharts Event and Action selection/highlight passages as optional cross-view selection context. Tabler's layout index supplies a catalogue only, not verified phone stacking. Transformer Explainer's README supplies component/input/output teaching framing only, not source-grounded model internals or a live model. No new original page opened, no package adopted; existing per-repo read allowances, licensing/pinning/traffic gaps and execution exclusions persist.
- No screenshot/current UI inspected in this slice, so this is builder-content preparation, not a newly validated visual layout. Approved phone detail remains below the diagram with reserved/non-obstructing layout space (notes :55). Only notes appended; no code/spec/site change, build/test/browser run, project Python/node, install/clone, model/science access or git mutation.
- Context rule survives: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the current point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md containing completed/in-flight topics, exact paths, settled-decision pointers, open risks and one next step. At <=40% stop starting work. No numerical percentage is exposed or asserted; never approach compaction or place the handoff inside notes.

## LVB7 — four-section evidence sheet accepted; targeted external lookup proposed

### Decisions (with the operator's words)

- Operator verbatim: "1...and would it be valuable to give builder agents mcp or web search to pull in context gaps for specific models via sites such as hugging face or other LLM knowledge sources?" The initial 1 accepts the repeated four-section evidence sheet: What it is; Stored-number changes; Recorded activity; Inputs and sources. Preserve run/model/source-version context, all required model parts and finer source-supported detail. The additional sentence asks for a recommendation about lookup access; it does not install/configure MCP, lift the build hold or authorize scientific execution.
- Respond yes: targeted read-only lookup can help prepare model-specific explanation/structure context. General public documentation cannot establish the historical experiment's internal activity, stored-number changes, inputs or verdict. The accepted distinction between source preparation, viewer rendering and future scientific capture remains.

### Open questions

- Recommended future workflow: preparation supplies reviewed source notes; preparation and builder agents may use read-only MCP/web lookup for a named remaining context gap, after checking existing local sources. Save each candidate claim with model ID/version, exact source location, relevance and unresolved conflict; review before it becomes published educational/source content. Builder discovery does not silently amend scientific records, frozen pins or agreed scope. Alternative: only preparation agents search; builders use prepared source notes and report remaining gaps. No operator choice yet.
- MCP means Model Context Protocol, a connection through which an agent uses a service's tools. It is an access route, not an evidence guarantee. Proposed Hugging Face capability must be restricted to inspected search/read operations; broad MCP access is not assumed read-only. Exact exposed-tool filtering/enforcement, authentication and inherited builder availability remain unverified. No Hugging Face named tools were exposed in this session's callable tool metadata; installed/configured status was not audited.
- Public-model identifiers and public technical questions are sufficient for these lookups; private research records/prompts/outputs must not be sent out under this proposal. Unresolved public-source conflicts or missing matching revisions remain visible rather than being resolved by inference. No per-query operator approval flow is proposed for future authorized public read-only lookup.

### Spec changes proposed

- Add a scoped builder-context acquisition clause to the preparation/build contract: local sources first; named model/version-bound gap; read-only primary-source lookup; cited candidate extract and review; unresolved-gap reporting. Preserve model/config/hparams binding (docs/LABVIZ_V2_SPEC.md:182-183), recorded-input precedence (:201-213), typed source/missing representations and hashes (:662-676). No external lookup can satisfy missing historical measurements by substitution. Binding spec unchanged.

### Context for build agents

- Proposed source order: already-held run/model records and reviewed notes; exact model publisher's Hugging Face model card/configuration or official technical documentation; original model paper and relevant library documentation. Community tutorials can identify terminology/leads but must not supply unsupported model-specific dimensions or experimental claims. Configuration text/source text may be read within an authorized text-only preparation brief; model files, execution and bulk downloads remain excluded.
- Official pages opened in this slice, on the operator's question: [Hugging Face MCP Server](https://huggingface.co/docs/hub/en/agents-mcp), What you can do / Built-in Tools / Spaces options, documents model/paper/documentation exploration and also Jobs, sandbox/repository writes and callable community Spaces. Extract only discovery/reading context; do not configure/run Jobs, Spaces, inference or repository writes. Its documented hf_fs access is not independently proven read-only here. [Model Cards](https://huggingface.co/docs/hub/model-cards), What are Model Cards, describes the model repository README as the descriptive model card, including intended use/limits, training and evaluations; required contents are guidance, not a guarantee every card is complete.
- Read-only web search and these two official documentation pages were used. No specific model card/config, model paper, MCP server implementation or third-party source was opened. Other search results were not adopted or treated as verified context. Configuration/install/credentials/tool execution were not attempted. No claim of MCP deployment, safety audit or version-specific model coverage follows.
- SUMMARY.md:37-55 and existing reference restrictions continue to exclude unaudited script/network/model actions. Future lookup must preserve local static LabViz: the built site does not search remotely at runtime. New external context should be stored as reviewed, version-bound preparation material so subsequent builds are reproducible; exact artifact location awaits a scoped brief because this session writes only notes/handoff.
- Only notes appended; no source/spec/site edit, build/test/browser run, install/clone, project Python/node, model/science access or git mutation. Context directive persists: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md with decisions/pointers, in-flight work, exact paths, open risks and one next step; at <=40% stop starting work. No numerical percentage is exposed or asserted. Never put the handoff in notes or approach compaction; restate this rule in every successor/team handoff.

## LVB7 — prepared context plus targeted lookup accepted

### Decisions (with the operator's words)

- Operator verbatim: "1", selecting "Prepared context plus targeted lookup - recommended." Future builder briefs allow the reviewed preparation material plus scoped read-only lookup for named remaining context gaps. Preserve local-first lookup, exact model/version, primary-source support, review before publication, public-only outbound queries and separation from missing historical experiment observations. This is the accepted future brief policy; no tool installation/configuration, code/building or scientific execution is authorized by this choice.
- No new operator preference is required to implement the already accepted policy conceptually. Do not turn routine source/version checks into per-query approval questions. Tool capability review and any actual configuration remain separate future authorized work.

### Open questions

- Preparation checklist now needs actual populations and content: all required models and recorded revisions; their source-bound structures and granular parts; complete applicable run input sets; observed changes/activity/step coverage; reviewed explanations/paper sections; unresolved model/context source gaps. Those items have not been inventoried by this discussion. Current scientific pins and the building hold persist.
- The next substantive discussion can refine the content of model foundations and associations to the accepted learner domains/topics, or respond to the operator's next concern. No new menu or installation decision is presented in this entry. The three worked cards remain examples rather than the whole bank or a coverage ceiling.

### Spec changes proposed

- Freeze the accepted lookup policy into a future scoped preparation/builder brief, alongside the proposed per-part source/coverage extension; keep run/model structure binding (docs/LABVIZ_V2_SPEC.md:183), source precedence (:201-213), source hashes/missing/derived fields (:662-676) and reviewed-publication rule for draft explanatory context (:1048-1052). Exact new source-note schema/location remains unfrozen. No spec edit occurred.

### Context for build agents

- Recommended working sequence: receive the binding spec/accepted amendments and scoped brief; read prepared model/run/source coverage; name the remaining public context gap; search/read matching primary sources; record exact claim/source/version and review status; have new explanatory context reviewed before publication; leave unresolved gaps explicit. Do not use search snippets, generated summaries or a general architecture diagram as experimental observations.
- Illustrative lookup, not a performed query: "How are attention parts arranged in [public model ID] at [recorded revision]?" Start from the matching held model configuration, then use the model publisher's corresponding documentation/source text if explanation is missing. A supported structure explanation may populate What it is; it does not populate that run's Recorded activity. Stored-number changes and exact prompts/responses still need their own run-bound records or permitted source-bound transcription.
- Reuse a reviewed model reference across runs only where identity/version/applicability checks establish the same structure; keep each run's inputs, edits, observations and scientific labels run-specific. Do not merge different sizes, revisions, derivatives or documentary-only era records under a familiar family name. Spec :183 provides structure-binding context; :1048-1058 separates era/run framing and reviewed explanations. This is a preparation recommendation, not a newly implemented authority or model inventory.
- No new web page, MCP call, model/config file, paper or UI screenshot opened in this slice; only relevant spec/notes ranges read and this entry appended. Official Hugging Face pages/read limits remain at the preceding entry. No build/test/browser run, install/clone, source/spec/site edit, model/science process or git mutation occurred.
- Context directive survives: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md with completed/in-flight topics, exact paths, decisions/pointers, open risks and one next point. At <=40% stop starting work. No numerical percentage is exposed or asserted. Never put the handoff in notes or approach compaction; restate the same rule in every successor/team handoff.

## LVB7 — v1/v2 comparison resumed; open-page update behavior proposed

### Decisions (with the operator's words)

- Operator verbatim: "Continue brainstorming and digging into clarfying LabViz functionality, design, features, etc against the spec v1 and v2". Continue interactive design/source inspection within the unchanged discussion-only hold; no build/install/spec edit authority is inferred. Prior accepted comparisons, navigation, learning and granular model coverage remain settled.
- Located original v1 build brief results/labviz_codex_brief.md, whose title is a Lab View build task rather than a separately titled v1 spec. It calls for whole history and every model (:22-26), a generated static site with a 60-second rebuild/server loop (:29), and tabbed views (:31-44). This is historical intent/context, not permission to follow its old build commands or override binding v2 rules. No separate v1-spec absence is asserted.
- Binding v2 docs/LABVIZ_V2_SPEC.md:340-355 supplies the connected five-view frame, run/line/compare linked selection and file-URL loading constraints; :938-949 distinguishes a future hosted telemetry path that polls every 30 seconds from static site rebuilds. Rebuilding site files alone does not establish how a page already open will adopt updated data. Existing notes :53 and :550 preserve source-dated snapshots and historical evidence validity.

### Open questions

- Proposed unresolved reader choice for hosted/connected viewing when a newer built snapshot becomes available: notify and let the reader explicitly Update view (recommended to preserve reading/quiz/player context), or automatically apply updates while preserving position and selection. No operator answer yet. This is whole-view snapshot adoption; Phase-2 live telemetry remains a separate source-labelled path, whose reader behavior can be discussed after this choice.
- Proposed notification text: "Newer snapshot available - Update view". Keep the displayed snapshot/source dates clear; do not show the newer generation's status as though all currently displayed records have refreshed. Updating retains the selected run/input/component/player position, comparison/filter state, place and quiz drafts. If a target no longer resolves, use the settled requested-target/recovery notice and await explicit selection; never silently replace the run or step.
- Detecting and adopting a coherent newer snapshot, preserving state and handling an interrupted update require a future scoped technical contract and verification. No supported detection method or existing auto-refresh implementation is asserted. When opened directly from disk, automatic checks are not promised: v2 :355's classic-script/file-URL loading distinction remains, and :354 notes local fetch restrictions. Source freshness is separate from experiment liveness and scientific validity.

### Spec changes proposed

- An accepted snapshot-adoption behavior would refine linked/retained selection (:353), compact activity/source-snapshot framing (:340, notes :53), and hosted telemetry versus built-page boundaries (:945-949). Preserve URL reload semantics (:419), minimum phone readability/touch sizes (:357-373, :405-420), personal-state independence and evidence/source labels. Binding spec unchanged.
- Comparison core was checked rather than reopened: v2 :578-582 requires matching subject/answer/template/scoring for per-fact comparisons, explicit refusal reasons and single-observation uncertainty; notes :13 and :47 retain the approved outcome/side-effects -> setup -> individual answers order with paired phone sections. No new comparison preference was asked.

### Context for build agents

- Supply original v1 brief :22-44 as historical intent and v2 :340-355, :938-949 as current navigation/loading/live-path context; settled brainstorm amendments must still be frozen by MAESTRO before implementation. Do not revive v1's C10-only history scale or fixed Qwen illustration as universal model scope; v1's own whole-program/every-model additions and v2's era/model framing prevail.
- Existing image viewed in this slice: results/labviz/review/20261008T130913325Z/chromium-phone-map.png. It shows source time and Log snapshot wording in a large top block; no newer-snapshot notification is visible in this historical capture. This is context for placing a compact readable update notice beside source age, not proof of current runtime update behavior or a fresh defect finding. Approved compact activity strip is already settled; do not ask its placement again. Review viewport entries at measure.json:23-34 specify 390x844 phone and 360x780 narrow. No new text/contrast/width measurement was performed.
- Future validation cases must include a newer served snapshot during reading/paused playback/quiz draft/comparison; coherent data/source-date adoption; unreadable update; unavailable retained target; and direct-file opening with honest refresh capability. These are planned cases, not tests run. No live service, browser automation, project Python/node, code/spec/site edit, install/clone, model/science access or git mutation occurred. Only notes appended; screenshot viewing and read-only source/spec searches performed. No new external page opened.
- Context directive persists: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md with completed/in-flight work, exact paths, settled pointers, open risks and one next point; at <=40% stop starting work. No numerical percentage is exposed or asserted. Never place the handoff in notes or approach compaction; restate this rule in every successor/team handoff.
- Citation precision after exact line lookup: selected-state carryover is docs/LABVIZ_V2_SPEC.md:352; progressive loading is :353; classic scripts and file-URL fetch restrictions are both :354; machine-readable adjacent run cards are :355. References above to :353 for linked selection or :355 for classic-script loading mean these corrected spans. URL reload semantics are :419. Design/authority unchanged; prior entries preserved.

## LVB7 — context gate and successor handoff

### Decisions (with the operator's words)

- MAESTRO verbatim: "your context is at 43% left, below your 45% rule. View no more screenshots. Tell the operator, finish the current point in this reply, and write results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md". Operator informed; stop starting new work. No additional screenshot viewed.
- No response selected the pending ordinary-page refresh proposal. Do not treat the context-stop instruction as notify-first or automatic-update approval. All earlier accepted designs and the building hold persist.

### Open questions

- One exact next point: hosted/connected view detects a newer built snapshot -> notify and wait for Update view (recommended), or apply automatically while preserving place/selections. Future Phase-2 live telemetry and direct-file limitations remain distinct. No new menu, build or source audit is started at the gate.

### Spec changes proposed

- Refresh behavior remains a proposed amendment, not an accepted/frozen requirement. S:352-354 and :419 retain selection/loading/reload constraints; :945-949 distinguishes telemetry polling and static rebuilds. No spec edit occurred.

### Context for build agents

- Continuation saved separately in results/dashboard_integration_review_20261011/labviz_brainstorm_handoff7.md with topics/settled notes pointers, inspected references, gaps/exclusions and the one pending question. Fresh successor resumes, does not restart or reopen settled choices. No build/test/browser run, code/site/spec edit, install/model/science/git action occurred.
- Binding rule survives: check Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write the separate designated successor handoff with completed/in-flight work, exact paths, settled pointers, open risks and one next point; at <=40% stop starting work. Never approach compaction or place the handoff inside notes. Restate the same rule in every successor/team handoff. MAESTRO reports 43% here; LVB7 stops.

## LVB8 — newer built snapshots wait for an explicit update

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Show Newer snapshot available / Update view and wait for your tap." In a hosted/connected view, notification does not automatically replace the displayed built snapshot. This continues LVB7’s pending ordinary-page choice (handoff7:51-59); it does not approve building or alter separately labelled telemetry polling.
- Preserve reading position, valid run/input/component/player/comparison/filter selections and unfinished learner work when the reader updates. Unresolvable selected targets use the settled explicit recovery behavior. Keep the displayed snapshot/source dates clear; do not blend newer status into older displayed records. Direct-file opening must describe its actual supported refresh capability; no hosted polling promise is inferred.

### Open questions

- Future scoped preparation must define coherent snapshot identity/adoption, detection in each supported viewing mode, interrupted/unreadable update handling and preservation of learner drafts. No existing runtime behavior was inspected or verified here.
- Continue the full model-wide source/model/input/component preparation. Complete applicable populations, version-bound sources, reviewed explanations and finer observations remain preparation dependencies; no selected-demo or top-16 scope substitution.

### Spec changes proposed

- Add the accepted notification-and-tap behavior beside selection/loading rules (docs/LABVIZ_V2_SPEC.md:352-355) and distinguish it from Phase-2 telemetry polling (:938-950). Binding spec unchanged. Detailed URL recovery remains anchored by the prior verified :419 reference.

### Context for build agents

- Give builders the accepted refresh journey and planned cases: a new snapshot while reading/paused playback/comparing/drafting answers; reader-triggered coherent adoption; retained valid context; unresolved selected target; failed update; honest direct-file behavior. These are future validation cases, not tests run or claims of implementation.
- Current root and branch worktree-c10k-route-a verified read-only. Brainstorming skill supplies conversation structure only; explicit operator restrictions override its generic spec/commit/implementation steps. No code/spec/site edits, builds/tests/browser runs, project Python/node, install/clone, model/science execution or git mutation occurred. Only this notes entry appended.
- Context directive survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted, tell the operator, finish the point and write the separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point. At <=40% stop starting work. Never approach compaction or place the handoff inside notes; restate this same rule in every successor/team handoff. No numerical context percentage is exposed or asserted.

## LVB8 — complete searchable inputs grouped by purpose

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "One searchable list with purpose groups — recommended." Provide one searchable browser of every applicable recorded input for the selected run, grouped by purpose: facts being added, practice wording, test questions, and checks for unwanted changes. Preserve additional source-supported roles where needed; the four illustrative labels do not redefine historical input roles or exclude probes/other applicable inputs.
- Keep the already accepted input-and-answers-first detail order (notes:190-203), then associated model detail. Display expected and observed answers and the recorded scoring explanation where available; unavailable fields remain explicit. Selecting an input in the player or from a model part retains access to the complete applicable set. Search/filtering changes the displayed subset, never the underlying coverage or evidence population.

### Open questions

- Actual all-model/all-run input populations, role assignments, exact recorded wording, source-bound permitted transcription, expected/observed answers and finer model/input observations still require preparation. Do not deduce completeness from a readable list or invent a full prompt from an incomplete template.
- Routine builder preparation must retain occurrence/source context when identical wording is used for different purposes; grouping must follow reviewed source roles rather than text similarity. Exact identifiers and future data-contract fields remain unfrozen.

### Spec changes proposed

- Expand the words/phrases panel (docs/LABVIZ_V2_SPEC.md:619-625) into the accepted complete searchable purpose-grouped browser, preserving recorded-source precedence (:201-213), selected-state continuity (:352), source links (:348-351) and phone readability/touch requirements (§4A). This supplements model-first coverage ordering; it does not reverse that accepted structure or edit the binding spec.

### Context for build agents

- Give source preparers an inventory requirement spanning every required model/run and applicable input role, exact text or explicit gap, expected/observed response, recorded scoring rule, source/version and associated model-part/recorded-step coverage. Give viewer builders reviewed inventory records, input-first detail order and the complete-list route beside focused selections; none is populated or validated by this choice alone.
- Keep identical text in distinct experiment purposes/context distinguishable. A source-reading failure, uninspected role coverage and confirmed missing recording remain different states; do not group every problem under an empty list.
- No new external reference, screenshot, source population audit or runtime test occurred for this decision. Building hold persists; only notes appended. Context rule remains: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the current point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with completed/in-flight work, decisions/notes pointers, open risks/questions and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate this rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — proposed input coverage display inside a model part

### Decisions (with the operator’s words)

- No new operator choice yet. Complete model-wide/granular scope, model-first coverage order, purpose-grouped searchable inputs and input-and-answers-first details remain settled. This question concerns only the initial displayed subset when browsing inputs from a selected model part.

### Open questions

- Recommended: initially show all applicable run inputs in the part’s searchable browser, with an observation-coverage label for that part beside each input; provide filters to focus on recorded observations. Alternative: initially show only inputs with recorded observations for that part, with a clearly visible All inputs control. Both retain the complete applicable input population and the always-visible coverage summary. No answer yet.
- Proposed coverage wording must distinguish recorded observations here, confirmed not recorded here, coverage not yet checked and could not read the relevant data. Recorded observation labels never imply a complete historical internal trajectory. Do not claim that an input did not pass through a part just because no observation exists.

### Spec changes proposed

- Clarify the default input subset in per-part exploration (docs/LABVIZ_V2_SPEC.md:619-648), preserving recording/teaching distinctions (:648-657), source framing (:348-352) and existing phone rules (:357-371). This is proposed UI behavior, not a populated data contract, implementation or binding-spec edit.

### Context for build agents

- Existing historical capture inspected: results/labviz/review/20261008T130913325Z/chromium-phone-model-2d.png. It shows vertically stacked selected-run, layer-write, part, wiring, answer-signal and recorded-event sections. This is an older capture, not a current browser run or proof of the proposed input browser. measure.json:1512162-1512180 identifies the matching view, a 390x844 viewport, 390px root scroll/client width and 7706px page scroll height. No fresh rendering, text/contrast analysis or acceptance claim follows.
- Phone presentation must keep coverage labels readable in stacked rows and controls at the spec’s touch/readability sizes. Existing interface-design trial guidance at results/dashboard_integration_review_20261011/uiskills_report.md:42-44 supports hierarchy/state review; reuse the already selected checklist context, not an installed skill or copied unaudited scripts. The proposed input browser does not call for a new chart package.
- Source preparers must supply verified input-to-part observation associations and explicit coverage gaps before the viewer can label them. A readable result file alone does not establish observation coverage. No external lookup, build/test/browser run, project Python/node, science/model process or code/spec/site edit occurred; only notes appended and one existing screenshot viewed.
- Binding context rule: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write the separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate this same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — per-part input browsing starts with complete coverage

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "All inputs, with recording labels — recommended. You can filter to recorded observations." When browsing from a model part, initially display all applicable inputs for the selected run, grouped by the already accepted purpose groups, with observation-coverage labels for the selected part. Provide filters for recorded observations without silently hiding gaps in the default display.
- Preserve the distinction between recorded observations here, confirmed not recorded here, not yet checked and failed reads. No recording does not mean that the input bypassed this part or that its internal activity was unchanged. Opening a row retains the accepted exact-input/expected-answer/observed-answer/scoring-first detail order and access to source-supported finer observations.

### Open questions

- Preparation must establish the applicable input population and verified per-input/per-part coverage before publishing those labels. Unknown population sizes cannot be presented as complete coverage or zero missing observations. Exact data-contract identifiers/fields remain unfrozen; no full inventory has been performed.
- The next design point may distinguish coverage gaps from the separately reviewed work needed to address them. Showing such work would describe a dependency, not approve recording, execution or building.

### Spec changes proposed

- Add the accepted default complete-list display and recording filters to per-part/input exploration (docs/LABVIZ_V2_SPEC.md:619-648) and model-first coverage preparation. Retain source framing (:348-352), phone rules (:357-371) and recorded/teaching/re-creation boundaries (:648-657). Binding spec unchanged.

### Context for build agents

- Source preparation supplies version-bound model structure, complete applicable input populations, recorded stored-number changes, input-to-part observations/available steps, reviewed explanations/paper sections and explicit gaps. Viewer builders render reviewed content and the accepted opening display; they cannot infer coverage from missing arrays, animation or configured write locations.
- Prepare cases for a fully observed input, a partially observed input, confirmed absent observation, uninspected coverage and failed source read, while preserving full model-wide/finer scope. These are planned content/validation cases, not tests run.
- No new source, screenshot, external page, runtime test or inventory opened for this decision; only notes appended. The building hold persists. Context directive remains binding: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate this same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — recording gaps explain reasons and preparation needs

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "The gap plus its explanation and preparation needs — recommended." In expanded coverage detail, readers can see the recording status, Why this is missing and What would be needed, beside the affected model/input/part context. Preserve the compact always-visible summary and already accepted complete scope/navigation.
- Explanation must distinguish a verified absence from an uninspected source or failed read. When the cause has not been established, say so. Preparation needs describe reviewed dependencies, not an approval to act, a scheduled job, an available recording or a promise that the gap will be filled.
- Unrecorded historical internal activity cannot be restored as historical evidence. A separately authorized future recording pertains to a future run; a re-creation remains labelled NOT EVIDENCE. A missing context explanation may instead be addressable by the accepted local-first, version-bound public-source lookup. These are different gap types, not interchangeable remedies.

### Open questions

- Actual gap reasons, relevant source checks and preparation dependencies still require the full source inventory/content review. No all-model survey or current source/pin audit has occurred. Unknown needs stay explicitly unresolved rather than inferred from a generic model diagram.

### Spec changes proposed

- Extend accepted expanded Recording coverage/per-part evidence detail (docs/LABVIZ_V2_SPEC.md:345, :348-352, :619-657) with the reason/need explanation. Preserve the historical limits documented at :325-328 without treating the binding sampled scope as satisfaction of the accepted full model-wide/finer intent. No binding-spec edit occurred.

### Context for build agents

- Give source preparers a gap record concept containing affected model/run/version/input/part/step, recording status, checked source locations, supported reason or explicit unknown, and reviewed preparation need or unresolved dependency. This is content preparation, not a frozen schema. Give viewer builders reviewed explanations with source links and appropriate evidence labels; builders do not invent causes or commission science.
- Example categories for future reviewed content: matching model reference missing -> find/review the exact public revision; observation absent from readable historical records -> historical detail unavailable, future recording requires a separate scientific plan; malformed/unreadable source -> display the read failure, preserve raw evidence, await scoped investigation; uninspected coverage -> source inspection still needed. None is a current diagnosis of a particular run.
- Only notes appended; no new source/screenshot/external page, build/test/browser run, project Python/node, install/clone, model/science process or git mutation. Context directive survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate this same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — readable source details open within LabViz

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Expand readable source details inside LabViz — recommended, keeping your place." Tapping a displayed number or its source link opens readable details in the current LabViz context, rather than opening the original recorded file first. Retain the original-file link as a further deliberate action and preserve position/selections.
- Source detail shows the recorded value, units where applicable, exact file/field or document-line location, and the rule/input values for a derived calculation. It must respect the binding source-leaf contract (docs/LABVIZ_V2_SPEC.md:662-676), retaining original precision and distinguishing recorded, derived and missing data. Existing phone details remain in reserved/below-diagram space rather than an obstructing overlay.

### Open questions

- Future scoped builder contract must define readable extracts and original-file link behavior for direct-file and hosted viewing, including source/version availability and failures. No current source-link runtime was tested; the selected UI is design, not acceptance.
- Source details must remain tied to the displayed snapshot even when a newer snapshot is available. A mutable original-file path alone cannot establish that the opened bytes match the displayed recorded value. Exact archival/link resolution and mismatch handling need scoped design/verification; source identity may not be inferred from a current path.

### Spec changes proposed

- Add the accepted in-view source-detail opening behavior to consistent source/navigation framing (docs/LABVIZ_V2_SPEC.md:348-352), existing data-for-view links (:615-617) and typed source/value/hash requirements (:662-676). Preserve phone readability/touch sizing (:357-371), paused context/return behavior and reader-triggered snapshot adoption. Binding spec unchanged.

### Context for build agents

- Source preparers supply reviewed, snapshot/version-bound value and source extracts, units, supporting document quote where appropriate and every calculation input required by the binding leaf rules. Viewer builders present readable details plus deliberate original-file access; a card or public-model explanation is not a substitute for a recorded experiment value.
- Keep plain-language calculation explanation first with exact recorded inputs available; this is a routine implementation recommendation, not a new operator choice. Missing/unreadable source and version mismatch remain explicit rather than substituted with current data or a guessed number. No frozen source-extract schema, archival strategy or implementation is asserted.
- Reuse the selected interface hierarchy/state checklist for focused readable detail, Anthropic chart accuracy/units guidance for numeric presentation and the review-derived Axiom quantity/unit/source/blocker worksheet as text-only context (notes:283-295). Original Axiom pages were not opened; no new package/skill adoption, install or external lookup occurred. The previously inspected phone model capture supplies historical layout context only.
- Only notes appended; no code/spec/site edit, build/test/browser run, project Python/node, model/science process or git mutation. Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate the same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — compare two runs within the selected model part

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Compare within the selected model-part view — recommended." Add focused two-run comparison at the currently inspected model part, preserving the reader’s location and access to recorded changes, inputs, observations, gaps and sources. On a phone, the two runs stack. This supplements the existing run-level comparison destination and retains the four-section evidence sheet for each run.
- Preserve full model-wide/finer scope. A run without a recorded observation remains present with its explicit gap; do not omit it, substitute zero or silently select a different part. Source links and snapshot/version context remain separate for each run.

### Open questions

- Source preparation must establish valid part/input/measurement/phase correspondences. Matching a component name or layer number alone does not prove equivalent structure or a common measurement. Comparable displays require reviewed meaning, units, evidence tier and appropriate run/input/state context; exact eligibility remains a future scoped contract.
- Playback positions and any synchronization need clarification. Do not infer that the same step number or elapsed time means the same scientific state in two runs. Existing paused entry, retained selections and explicit unresolved-target recovery remain settled.

### Spec changes proposed

- Extend existing comparison behavior (docs/LABVIZ_V2_SPEC.md:577-582) into Inside the model/per-part exploration (:627-657), preserving shared scales only for comparable units, evidence/source framing (:348-352), phone layout/readability (:357-371) and recorded-event/re-creation limits. Do not change the settled global comparison order or claim a generic numerical difference proves an effect. Binding spec unchanged.

### Context for build agents

- Source/content preparation supplies each run’s reviewed four-section sheet, exact model/configuration/version, selected input text/role and scoring where applicable, stored-number/activity measurement definitions and units, source-supported available positions and explicit correspondence or refusal reasons. Viewer builders provide a focused stacked pair with each run’s identity/source visible and stable context/return navigation.
- Keep individual run evidence viewable when a requested paired measurement is not comparable; display the refusal reason beside that comparison. Eligibility for the existing per-fact derived row remains the exact fact/template/scoring contract at spec:579; do not replace it with a looser part-comparison rule. Single-observation uncertainty at :582 still applies.
- Borrow the already selected interface hierarchy/state and Anthropic unit/scale/table guidance as text-only context; ECharts selection/highlight documentation is optional context, not an adopted renderer or authorization to load remote assets. Existing phone model screenshot supplies historical one-column context, not validation of this proposed paired view.
- Only notes appended; no new screenshot/external source, code/spec/site edit, build/test/browser run, project Python/node, model/science process, install/clone or git mutation. Context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate this same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — comparison playback offers independent and linked modes

### Decisions (with the operator’s words)

- Operator verbatim: "Both options with a toggle switch". Provide both independent playback and playback linked at verified corresponding recorded points, controlled by a visible Link playback toggle in the focused two-run model-part comparison. Off means each run has separate controls; on means corresponding positions advance together. Each run’s own diagram/chart/input text remains synchronized internally in either mode.
- Linked playback does not equate arbitrary step numbers, durations or merely similar phase names. Display each run’s actual selected position and the supported correspondence; keep source/model/input/phase/recording context and source links distinct. Missing observations remain explicit; alignment does not certify scientific comparability or a causal effect.

### Open questions

- Recommended routine initial setting is independent playback, with both views paused, because cross-run alignment requires prepared correspondences. The operator approved availability/toggle, not an explicit initial on/off preference. No separate preference question is required for this sensible reversible recommendation; it remains distinguishable from the operator’s words.
- Exact source-supported correspondence records, compatibility rules and availability across all required models/runs/player modes remain preparation dependencies. No alignment population has been inventoried or inferred from experiment labels.

### Spec changes proposed

- Extend focused two-run comparison and playback under docs/LABVIZ_V2_SPEC.md:577-582, :651-657 and :919-931 with independent/linked modes and a Link playback toggle. Preserve the settled missing-target recovery: if the next requested linked point cannot resolve, pause, keep current evidence/selections visible and explain the missing match rather than silently moving one run or switching modes. Existing within-run synchronization remains mandatory. Binding spec unchanged.

### Context for build agents

- Preparation supplies explicit verified point correspondences, source references and eligibility/refusal reasons. A correspondence is navigational alignment, not automatically measurement eligibility; existing exact fact/template/scoring comparison rules, shared-unit/evidence-tier scales and single-observation caveats still apply.
- Viewer builders label the toggle and both actual source positions; support independent control when off and reviewed paired movement when on. If linking the current positions cannot resolve, show an explicit choice among supported matches or return to independent mode; do not silently jump. Switching off keeps the positions currently displayed. These are proposed routine consequences of the accepted modes/retention/recovery rules, not a frozen interaction schema.
- Planned verification cases include different step counts, missing corresponding points, source/version mismatch, one-sided unreadable data, toggling while paused and continuity across model-part/input navigation. They are future cases, not tests run. Apply the existing 44px touch requirement and non-color/explicit-label rules (spec:363-371); no switch component/library is adopted.
- Only notes appended; no source/code/spec/site edit, build/test/browser run, project Python/node, science/model process, install/clone, external query or git mutation. Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate this same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — comparable measurements include a sourced numerical difference

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Original values plus a clearly labelled difference — recommended." In the focused two-run model-part comparison, retain both original measurements and additionally show their numerical difference where the measurement pairing is valid. Label the difference as calculated and expose both source values and the calculation rule through the accepted readable source detail.
- A difference describes the selected reported quantity; it is not automatically a causal effect, scientific verdict, significance estimate or difference between unsaved internal tensors. Matching playback points alone does not make measurements comparable. If comparison is ineligible or a value is missing/unreadable, preserve available individual values and show the applicable refusal/gap instead of a numerical difference.

### Open questions

- Preparation must freeze applicable measurement eligibility/definitions, units, source version and evidence tier, operand roles and subtraction direction. No comparable-pair population, schema or implementation has been verified in this discussion.
- Routine recommendation: state the subtraction direction with the two actual run identities, retain units/full underlying precision and round only presentation; avoid a bare signed number or color-only emphasis. This follows the source/display rules, not an additional operator-selected preference.

### Spec changes proposed

- Extend focused model-part comparison alongside docs/LABVIZ_V2_SPEC.md:577-582 and :627-657 with the accepted calculated difference. Preserve the full operand/rule source contract (:668), source hashes (:674), comparable-unit/evidence scales (:566-574), single-observation limits (:582) and phone/readability/non-color rules (:357-371). Binding spec unchanged.

### Context for build agents

- Source/content preparation supplies the reviewed paired quantity definitions, eligibility/rejection reason, individual source leaves, units and explicit difference rule. Viewer builders retain the original paired values, display the eligible derived result and provide readable source detail listing both operands; they do not derive a missing tensor change from write-size summaries or infer scientific improvement from a larger/smaller value.
- Planned content/validation cases: equal values yield a measured/calculated zero; incompatible units/refused pairing yield no difference; missing/unreadable operand remains explicit; source-revision mismatch cannot silently use current data; displayed rounding does not alter recorded arithmetic. These are future cases, not tests run.
- Reuse the selected Anthropic accuracy/units/non-color/table extract and interface state/hierarchy checklist as text-only builder context (notes:283-295). No new library, remote service or skill adoption is required or authorized. Only notes appended; no new source/screenshot/external query, code/spec/site edit, build/test/browser run, project Python/node, science/model process or git mutation.
- Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate the same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — compact recording coverage includes verified counts

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Verified counts plus plain-language states — recommended." The always-visible Recording coverage summary includes counts where the complete applicable population and available recordings have been checked, alongside plain-language states for other coverage. Expanded detail remains available in the settled model -> layer -> part order.
- The offered example "Saved replies: 8 of 10 inputs; Internal activity: coverage not yet checked" is hypothetical, not a measured run, actual inventory or frozen set of summary fields. Reply availability is recording coverage, not answer accuracy or personal learning progress. No aggregate all-data completeness percentage or universal model population is approved.
- Unknown/uninspected populations cannot supply a denominator; failed reads stay visible rather than becoming zero coverage. Counts retain exact applicable model/run/version/role/part context and readable operand/source details. A small complete subset cannot be presented as full model-wide/finer coverage.

### Open questions

- Preparation still must inventory all required models/revisions, applicable input roles/populations, structures/parts/finer observations, source versions, reviewed explanations and correspondence eligibility. Coverage counts need explicit counting units and deduplication/occurrence rules appropriate to the recorded population; educational question-bank identity rules must not be silently applied to experiment-input occurrences.
- Which summary fields are valid for each model/run/recording category depends on that reviewed inventory. No fixed universal fields, denominators, all-model totals or current coverage audit have been established.

### Spec changes proposed

- Add sourced counts to the accepted compact Recording coverage summary (docs/LABVIZ_V2_SPEC.md:345, :348-352), following count/unit formatting (:372) and derived-input source rules (:668), while preserving explicit missing states (:669) and full model-specific input/component scope (:619-657). Binding spec unchanged.

### Context for build agents

- Source preparers supply the reviewed applicable population, available-recording membership, counting unit, source/context identities and unknown/read-failure states. Viewer builders display counts with their named denominator and independent plain-language states, then allow source/detail expansion. Do not average incompatible populations or infer completeness from successful parsing.
- Example future cases: complete known population with partial reply availability; known zero observations after verified source inspection; uninspected population; unreadable source; filtered list whose full-population denominator must remain explicit. These are preparation/validation cases, not tests run.
- Citation correction for the immediately preceding numerical-difference entry: Every source file is hashed is docs/LABVIZ_V2_SPEC.md:673, rather than the neighbouring blank :674. Derived full-operand arithmetic is :668; design and authority unchanged. Earlier entries remain append-only.
- Only notes appended; no source/code/spec/site edit, build/test/browser run, project Python/node, model/science process, install/clone, new screenshot/external query or git mutation. Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate the same rule in every successor/team handoff. No numerical percentage is exposed or asserted.

## LVB8 — each compared run retains its own coverage summary

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Each run’s own summary above its panel — recommended." In the focused two-run comparison, each run has its own compact Recording coverage summary above its panel, including verified counts and plain-language states as applicable. Preserve each run’s identity/version/source context, individual expansion and explicit gaps. Do not combine the pair into a single completeness score.
- On a phone, each summary travels with its corresponding stacked run panel. Linked playback and calculated comparable differences do not merge coverage populations or source authority. Existing model-first expanded coverage, complete input browser and retained source-detail context remain settled.

### Open questions

- No operator question is pending at this checkpoint. Next: make the full model-wide source-preparation worksheet concrete, assembling the accepted inventory/identity/coverage/explanation/source/paired-point requirements without another feature-selection menu or reduced demo scope.
- The source inventory, all applicable population sizes, matching historical versions, actual finer recordings, paired-point/measurement eligibility and source-link archival behavior remain unverified preparation dependencies. Interface design choices alone do not supply those records.

### Spec changes proposed

- Add per-run summaries to the focused Inside-the-model comparison amendment (docs/LABVIZ_V2_SPEC.md:577-582, :627-657), retaining source/evidence framing (:348-352), phone stacking/readability (:357-371), sourced count arithmetic (:668) and explicit missing leaves (:669). Binding spec unchanged.
- Citation correction: the count/unit formatting requirement is docs/LABVIZ_V2_SPEC.md:371, rather than the neighbouring blank :372 referenced in the preceding count entry. The exact source-leaf and hash line verification performed in LVB8 remains :666 JSON source, :667 document source, :668 derived arithmetic, :669 missing, :673 source hashes. Earlier notes remain append-only.

### Context for build agents

- Give viewer builders two reviewed independent coverage records, source-bound counts/statuses and the accepted stacked pair/expansion behavior. Give source preparers the whole model/run/input/part inventory requirement; diagrams, public explanations, successful parsing or synchronized playback cannot stand in for recorded coverage.
- Planned cases: differing recording coverage across two runs; one unknown population; one failed read; matching playback positions with unequal observation coverage; filtered inputs retaining named full-population counts. No tests, build or runtime verification occurred.
- LVB8 closes this design arc proactively with a separate continuation handoff at results/dashboard_integration_review_20261011/labviz_brainstorm_handoff8.md. No numerical Context reading is exposed or claimed. This is an arc checkpoint, not a claim that the 45% threshold was observed or that LabViz/source preparation is complete.
- Building hold and all execution exclusions remain. Only notes and the designated handoff are written. Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write the separate designated successor handoff with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff in notes; restate the same rule in every successor/team handoff.

## LVB8 — operator corrects premature closure

### Decisions (with the operator’s words)

- Operator verbatim: "Questions do remain". The preceding last-choice answer settled only placement of each compared run’s recording summary. It did not close LabViz brainstorming, exhaust the operator’s questions or establish readiness for a builder. Resume the interactive conversation and preserve every settled choice and the building hold.
- Correct the prior checkpoint wording: no unanswered multiple-choice prompt remained at that instant, but substantive design questions and the operator’s own questions remain open. Do not use completion of a presented choice as a reason to end this discussion.

### Open questions

- Invite the operator’s next question before imposing another feature-selection sequence. Its subject is not yet supplied; do not guess it or constrain it to a new topic menu.
- Existing unresolved work remains: coherent snapshot/source-version access; full model/run/input/component inventory and granular coverage; verified comparison point/measurement compatibility; reviewed model explanations/paper associations; concrete full-scope preparation material and eventual authorized product verification. These are not all operator preference questions; resolve source/technical facts through scoped inspection rather than asking the operator to supply them.

### Spec changes proposed

- No new spec amendment from this correction. The binding spec is unchanged; accepted design extensions still require MAESTRO’s frozen amendments/scoped briefs before building. No readiness or scientific acceptance is inferred.

### Context for build agents

- The separately saved handoff is a continuity record, not a declaration that the operator’s questions are exhausted or a requirement to replace their next question with the proposed worksheet. Append a corresponding correction there; earlier records remain intact.
- Only notes/handoff updated; no code/spec/site edit, build/test/browser run, project Python/node, model/science process, install/clone, external query or git mutation. The context rule remains binding: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the current point, tell the operator and write/update the separate designated successor handoff with topics, decisions/notes pointers, in-flight work, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff inside notes; restate this rule in every successor/team handoff. No numerical Context reading is exposed or asserted.

## LVB8 — front-end topic selected; operator invokes context ceiling

### Decisions (with the operator’s words)

- Operator verbatim: "LabViz front end, UI, UX and UI/UX information architecture design". This is the chosen next discussion topic. Address the coherent reader-facing interface: information hierarchy, navigation, layout, visual presentation and interaction across screens. Do not substitute further source-contract/coverage questions or impose the previously proposed preparation worksheet.
- Operator verbatim: "You need to handoff first for a fresh session. You have reached your context ceiling". Stop discussion/new work now, update the designated separate handoff and yield for a fresh successor. Do not ask another design question in LVB8.

### Open questions

- Front-end/UX/information-architecture discussion remains open. No new navigation-placement, sticky-header/bottom-bar, global layout or visual-system proposal was presented to or chosen by the operator in this final topic slice.
- Successor must assemble the existing settled pieces into a coherent screen/navigation design, preserving the five destinations, Map home, context continuity, phone layout, source/coverage and focused-comparison choices. Read only relevant spec/notes/current-build review spans as needed; do not reopen settled choices.

### Spec changes proposed

- No additional spec amendment was accepted in this slice. docs/LABVIZ_V2_SPEC.md:338-355 supplies existing information architecture; :357-371 phone/readability rules; :405-420 navigation/phone acceptance; :1095 phone map drill-down. Spec remains unchanged.

### Context for build agents

- The last completed read-only tool call inspected S:338-355, :405-420, :1090-1113 and handoff6:14-38. It finished successfully before the interruption; no background process or pending mutation was launched. Its combined output was truncated; do not claim complete inspection of omitted portions or fresh acceptance results.
- Next discussion is interface design, not implementation/source-inventory execution. Existing screenshot/source context and all building/execution exclusions persist. Only this notes entry and the designated handoff update are written at the gate.
- Binding context directive: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write the separate designated successor handoff with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting work. Never approach compaction or place the handoff inside notes; restate this same rule in every successor/team handoff. The operator reports the context ceiling now; LVB8 stops.

## LVB9 — mobile hamburger and collapsible desktop sidebar

### Decisions (with the operator’s words)

- Operator verbatim: "For mobile a hamburger menu and for desktop a sidebar that can open with the complete text based nav and minimized, still vertical, but with icons".
- On mobile, open the main navigation through a hamburger menu button. On desktop, use a vertical sidebar with an expanded full-text navigation state and a minimized vertical icon state. This supersedes LVB9’s initial proposed phone top-row/bottom-bar choice; neither earlier option was accepted.
- Retain the existing five destinations and Map home (docs/LABVIZ_V2_SPEC.md:340-346), all prior selected-context continuity, full model-wide/finer scope, source/coverage and comparison choices. This is a design decision only; the building hold remains.

### Open questions

- Next proposed discussion: should the phone hamburger open a side drawer with the current page still visible beside it, or a full-screen navigation panel? Recommend a side drawer to retain visual context, subject to the long labels fitting at required text/touch sizes. Neither opening style is accepted yet.
- Sidebar starting state, remembered expanded/minimized preference, exact icons, breakpoint between phone/desktop layouts, sticky behavior and shared screen layout remain unspecified. Resolve routine implementation details in future scoped design without reopening the accepted navigation forms.
- Recommended accessibility consequences, not new operator choices: expose each icon’s full name to assistive reading tools; show its text label on pointer hover or keyboard focus; visibly identify the current destination; provide a labelled expansion control. Mobile opening/closing must preserve selected context and return keyboard focus appropriately.

### Spec changes proposed

- Amend navigation presentation beside docs/LABVIZ_V2_SPEC.md:340-352 to specify the accepted hamburger and expanded/minimized vertical sidebar forms. Update the acceptance wording at :406 so the same five destinations are available on every page through the phone menu or desktop sidebar, rather than requiring all five text labels to be simultaneously visible while collapsed.
- Retain phone readability and 44px touch targets (:359-369; :418), selection carryover (:352), keyboard/focus requirements (:420) and direct contextual routes required by the tap-count criteria (:411). Do not assume that an added hamburger-opening tap permits weakening the existing direct run-to-line/map routes. The binding spec is unchanged.

### Context for build agents

- Give builders the operator’s exact navigation decision, the two desktop states, the eventual chosen mobile opening behavior and preserved context/accessibility requirements. Current generated navigation is five top buttons (results/labviz/site/index.html:17-23); this source inspection is not a fresh runtime check.
- Existing historical phone capture inspected in LVB9: results/labviz/review/20261008T130913325Z/chromium-phone-map.png. It shows the existing five-button top row and a substantial recorded-status block before map content; it predates MathLab integration and supplies layout context only. No measured defect or current acceptance result is asserted.
- Use the reviewed interface-design hierarchy/state extract as text-only context (results/dashboard_integration_review_20261011/uiskills_report.md:42-44), focused on navigation states and retained page context. No original external page opened, package/skill adoption, installation, copied component or execution authorized. Follow SUMMARY.md:36-57 safety findings; optional images/scripts/services remain outside scope.
- Worktree root and branch worktree-c10k-route-a verified read-only in LVB9. Only this notes entry appended; no code/spec/site edits, builds/tests/browser runs, project Python/node, installs/clones, science/model access, git mutation, graft, external search or agent/service messages.
- Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the current point and write the separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or place the handoff inside notes; restate this same rule in every handoff. No numerical Context reading is exposed or asserted.

## LVB9 — phone navigation opens as a side drawer

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Side drawer — recommended: menu slides in from the left; tap outside to close." The hamburger opens a left-side drawer with full navigation labels and part of the current page still visible behind it, rather than a full-screen menu.
- Opening and closing the menu retains the current view, selected context and reading position. The accepted desktop expanded/full-text and minimized/icon vertical sidebar remains unchanged. This decision describes navigation only; it does not reverse earlier below-diagram/reserved-space rules for evidence details.

### Open questions

- Next interface choice: should a compact phone bar containing the hamburger button and current destination name remain visible while scrolling, or scroll away with the page? Recommend keeping that small bar visible so the menu remains within reach. No sticky behavior is accepted yet.
- Desktop sidebar anchoring/initial state, exact icons, other header contents and the placement of status/context/content remain open. A sticky phone bar would not by itself approve keeping the full status block or full context frame fixed on screen.

### Spec changes proposed

- Add the accepted left-side drawer to the navigation presentation amendment beside docs/LABVIZ_V2_SPEC.md:340-352 and the revised five-destination acceptance wording at :406. Retain the :367/:418 touch-target requirement and :420 keyboard/focus behavior.
- Recommended routine behavior: provide a visible labelled close control, support Escape, keep keyboard navigation within the open menu, and return focus to the hamburger on dismissal. Tapping outside is an additional dismissal route. Closed menu content must not intercept page controls or keyboard navigation. These are design requirements proposed for future scoped validation; no runtime check or spec edit occurred.

### Context for build agents

- Give builders the accepted hamburger-to-left-drawer journey, full destination labels, current-destination indication, outside-tap/explicit-close dismissal and retained reading context. Accessibility names and keyboard behavior belong to the same component brief, not a separate installed skill.
- Reuse the text-only interface hierarchy/state context already inspected at results/dashboard_integration_review_20261011/uiskills_report.md:42-44. No new external reference or drawer library has been inspected/adopted; no package, remote assets or execution is authorized.
- Only notes appended. Building hold and all LVB9 execution exclusions persist. Binding context rule remains: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write the separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with completed/in-flight work, decisions/notes pointers, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or put the handoff in notes; restate this rule in every handoff. No numerical context percentage is exposed or asserted.

## LVB9 — compact phone navigation remains visible while scrolling

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Small bar stays visible — recommended: navigation remains available; uses a little screen space." Keep a compact phone top bar containing the hamburger button and current destination name visible while the page scrolls.
- This approves the small navigation bar only. It does not approve fixing the entire status block, breadcrumb, evidence detail or player controls to the screen. The accepted phone left-side navigation drawer and desktop expanded/minimized vertical sidebar remain settled.
- Prior status placement is already settled at this notes file:21 and :44: compact source-dated activity strip at the top, full activity detail last on Home, logs on request. LVB9’s provisional progress update about considering status density does not reopen that choice. Preserve it in the shared screen design.

### Open questions

- Next preference: desktop sidebar’s first-visit state. Recommend expanded full text initially, so the destinations are understandable before the reader chooses to minimize them. Alternative: initially minimized icons for more content width. Neither initial state has been chosen.
- Routine proposed consequence: retain the reader’s sidebar choice between desktop views; any cross-visit persistence must describe its actual support in the viewing mode. Initial-state approval alone does not approve a particular storage mechanism or claim persistent behavior already exists.
- Main screen hierarchy, exact sidebar/content dimensions, desktop anchoring, current-context presentation, typography/color refinements and icons remain to discuss where not already settled. Retain inherited light/dark choice and non-obstructing evidence detail layouts.

### Spec changes proposed

- Add accepted sticky compact phone navigation beside docs/LABVIZ_V2_SPEC.md:340-352, retaining :359-369 readability/touch rules and :420 keyboard/focus requirements. Future acceptance must check that the bar leaves content readable and does not hide the focused control or linked target. No test/build/browser run or spec edit occurred.
- Preserve the prior compact activity-strip amendment recorded at this notes file:44; do not substitute a large fixed status header for the accepted small menu bar. Existing binding docs/LABVIZ_V2_SPEC.md:340/:405 remain the source for top status/home coverage.

### Context for build agents

- Give builders the accepted phone shell states: compact visible bar; hamburger opens left drawer with full labels; closing retains page position and context. Distinguish navigation from the scrollable sourced activity/context and main content. Exact bar height and final layout are not frozen by this conversation.
- Use the reviewed text-only interface-design hierarchy/state extract (results/dashboard_integration_review_20261011/uiskills_report.md:42-44) to check expanded/closed menu state, current destination and retained reading context. No new library, skill installation or original external page inspected.
- Only notes appended. Building hold and all execution exclusions persist. Binding context rule survives: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or put the handoff in notes; restate this rule in every handoff. No numerical Context reading is exposed or asserted.

## LVB9 — desktop sidebar starts expanded; main workspace next

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Expanded — recommended: full navigation names." On a first desktop visit, start with the vertical sidebar expanded to full text; the reader can minimize it to vertical icons.
- Preserve the phone hamburger/left drawer and compact persistent navigation bar. Sidebar-state retention between views remains a recommended routine consequence, not an independently selected storage/persistence mechanism.
- Carry forward the already accepted main workspace/detail relationship: focused diagram/chart area; desktop evidence detail panel occupies its own space without covering it; phone detail expands below it (this notes file:18-19). Phone charts show one explained measure at a time with all applicable measures accessible (:301). Essential phone Play/Pause and Previous/Next controls already remain visible in reserved non-obstructing space (:262; :607).
- Clarification of this notes file:1750: LVB9’s phone-header answer added navigation persistence only. It did not remove the independently accepted persistent essential player controls. Both need room in the eventual phone layout; no current combined-height acceptance has been established.

### Open questions

- Next visual preference: selected chart placement relative to the focused model diagram on wide screens. Recommend the diagram followed by the selected chart underneath, preserving a broad main area when the navigation and optional detail panel are open. Alternative: diagram and selected chart side by side when sufficient width exists. Both retain synchronized selections and the accepted phone one-chart display.
- Exact dimensions, adaptation at narrow/landscape widths, positioning of reserved player controls relative to the persistent navigation bar, sidebar anchoring and context/header arrangement remain unfrozen. Readable labels and non-obstructing details remain binding constraints, not reasons to shrink charts or hide required context.

### Spec changes proposed

- Add first-visit expanded desktop navigation to the pending docs/LABVIZ_V2_SPEC.md:340-352 amendment and updated :406 navigation acceptance. No binding-spec edit occurred.
- Future chart-placement clarification belongs beside per-part/wiring/player views (:627-657), retaining chart captions and limitations (:413), typography/touch rules (:359-371) and source/context frame (:347-352). The proposed placement is not yet accepted; the diagrams’ fixed Qwen dimensions and sampled scope in the binding span do not replace prior accepted full model-specific/finer scope.

### Context for build agents

- Supply navigation states together with the already accepted wide-screen reserved detail panel, below-diagram phone detail, one-chart phone selector and persistent essential phone controls. Evaluate the eventual combination rather than treating each isolated control as proof of a usable screen.
- Use the existing historical phone model capture cited at this notes file:241 and the inspected interface hierarchy/state extract (results/dashboard_integration_review_20261011/uiskills_report.md:42-44). Chart units/scales/non-color/source guidance remains the existing task-specific text-only reference context (:283-295). No new original external page or rendering-library adoption.
- Only notes appended; no code/spec/site changes, builds/tests/browser runs, project Python/node, installs/clones, model/science access, git mutation or external queries. Building hold persists.
- Binding context rule: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or place the handoff in notes; restate this rule in every handoff. No numerical Context reading is exposed or asserted.

## LVB9 — focused diagram above its selected chart

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Diagram above chart — recommended: each uses the main area’s width." In Inside the model, place the focused model diagram first and the selected applicable chart underneath, including on wide desktop screens. This settles the pending beside-versus-below arrangement; navigation and the optional non-obstructing desktop detail panel retain their separate areas.
- Retain the already accepted phone one-chart selector with all applicable measures accessible (this notes file:301); shared input/component/playback position across diagram, chart and text; full model-wide/finer scope; readable captions/limits/sources and coverage; and below-diagram phone detail. This layout choice does not redefine focused two-run comparison or the source-supported before/after content within a diagram/chart.

### Open questions

- Next phone preference: keep a readable summary of the current run, input, mode, model part and recorded position visible, with selection controls expandable on request, or show the full selection controls open above the diagram. Recommend the compact summary plus expandable controls to give the main visual more room initially. The summary must show actual selected state; missing/unresolved selections remain explicit.
- This question concerns selectors, not the already accepted persistent essential Play/Pause and Previous/Next band, visible compact recording coverage, source/evidence labels or the full recorded input/answers available in detail. It does not propose hiding those requirements.
- Desktop selector presentation, exact control grouping and vertical-space budgets remain unfrozen. All three accepted player modes, complete grouped searchable run/input browsers and model-part navigation remain accessible in either option.

### Spec changes proposed

- Add accepted diagram-then-selected-chart placement to per-part/wiring/player design beside docs/LABVIZ_V2_SPEC.md:627-657, retaining contextual source framing (:347-352), readable typography/touch rules (:359-371) and visible chart caption/limitations (:413). Binding spec unchanged.
- An eventual compact selector amendment would refine the grouped run picker (:345), linked selection (:352) and player controls (:919-931). Neither summary content nor an expansion label is frozen by this pending preference question; no implementation exists by virtue of the proposal.

### Context for build agents

- Give builders the accepted diagram/selected-chart order, preserved focus/synchronization, independent navigation/detail areas and one-chart phone selector. Sources, missing states and chart meaning remain attached to the selected measure. No unsupported scientific measurement or eligibility is supplied by layout.
- Reuse the reviewed interface-design hierarchy/state extract (results/dashboard_integration_review_20261011/uiskills_report.md:42-44) and existing chart-accuracy context (this notes file:283-295); the historical model capture remains context for long stacked content, not proof of any new layout or measured defect. No external source, component library or skill adoption added.
- Only notes appended; the building hold and all execution exclusions persist. Binding context rule survives: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the current point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or put the handoff in notes; restate this same rule in every handoff. No numerical Context reading is exposed or asserted.

## LVB9 — operator redirects to visual front-end design and review context

### Decisions (with the operator’s words)

- Operator verbatim: "1...but have we already covered this? And I conceded this is UI/UX, if we are being redundant I suggest we brainstorm the front-end/dashboard design focused. What does the interface look like visually, how are screens/pages organized, what UI/UX features can be leveraged for easy and enjoyable user experience. Do we need additional context to reference to effectively do this type of brainstorming work? I provided some in the first agent session and those are starting points. I also provided a list of possible skills to leverage."
- The initial "1" accepts the immediately offered compact phone selection summary with expandable selection menus. Keep current run/input/mode/model-part/step readable above the diagram, with essential player controls and required coverage/source context available as separately settled. This refines selector presentation; it does not remove complete input browsers, recorded text or finer model coverage.
- Operator verbatim: "There is a SUMMARY.md doc in results/dashboard_integration". Read-only path probe found results/dashboard_integration_review_20261011, and SUMMARY.md there was reread in full. Its LabViz recommendations, original supplied references and selected skills remain the discussion grounding; do not replace them with a generic checklist or more repetitive control questions.
- Shift the discussion to whole-screen visual compositions, coherent page organization, visual language and enjoyable exploration. Retain all settled navigation, context, evidence, player, detail, chart and theme choices. Do not ask the operator to choose them again.

### Open questions

- Proposed visual direction, not yet accepted: a calm research workspace using readable type, neutral backgrounds in both accepted themes, restrained accent color for selection, fewer heavy box borders, clear page titles and generous diagram/chart space. Alternative: a bolder visual explorer with stronger grouping, larger diagram presentation and more expressive selected-object emphasis. Both preserve all destinations, granular scope and evidence requirements.
- Need to work through complete compositions of Home/Map, Science lines, Runs, Inside the model and Learn, keeping the same navigation/context conventions while matching each page’s purpose. Their purposes and journeys are already settled; composition, visual weight, spacing, shape, typography within the floor, color roles and interaction polish are not frozen by the previous micro-choices.
- Existing context is sufficient to begin those designs. Additional context should fill a specific visual gap, such as an inspected whole-screen layout example, rather than restart broad tool intake. Tabler’s inspected layout index supplies a catalogue, not verified phone/panel markup; Transformer Explainer supplies README teaching framing, not an inspected zoom interface. No new external page is opened here.
- Candidate experience polish: a selected object highlighted consistently across diagrams/chart/text; clear focus/back transitions; readable contextual help and source detail; restrained transitions with reduced-motion support. These are proposals or refinements of existing selections, not new scientific activity, renderer adoption or implemented features.

### Spec changes proposed

- Add accepted compact phone selectors beside docs/LABVIZ_V2_SPEC.md:345/:352 and :919-931, retaining mandatory source/context framing (:347-352), coverage and essential visible playback controls. Exact expansion label/storage/control geometry remains unfrozen.
- Future accepted visual language and complete page compositions would extend §4A (:338-371) and relevant per-view §5/§11 spans, preserving all readability, non-color, source and chart-limit requirements. No binding-spec or product-code edit occurred.

### Context for build agents

- Relevant SUMMARY.md anchors verified by full reread: web/chart/layout trial candidates (:9-10), one interface guide and one chart guide (:15-16), proposed LabViz phone/spec review (:29), and safety (:33 onward). These are review recommendations and text-reference scope, not adoptions or permission to run scripts.
- Use the actual primary-reference extracts already recorded at this notes file:283-295: interface-design hierarchy/spacing/states; Anthropic chart accuracy/accessibility; ECharts selected-item highlighting; Tabler layout catalogue; Transformer Explainer README explanation framing. Earlier uncertainty wording at :79-83 predates these later inspections; follow the later record for what was actually opened. Licence/pin/compatibility and uninspected examples remain preparation needs.
- LVB9 reread web_report.md:5-23 and uiskills_report.md:5-35 for candidate fit/overlap/safety. It read only the description/preamble of the available gstack design-consultation skill to assess applicability; that workflow was not applied, no preamble commands run, and no design-system/preview file created. Its preview-generation workflow is unnecessary for this discussion-only existing-site task.
- Additional historical capture inspected in LVB9: results/labviz/review/20261008T130913325Z/chromium-desktop-map.png. It shows five horizontal navigation buttons, a status block and a seven-column map of bordered nodes. It supplies existing visual context only, predates MathLab, and is not a fresh appearance/acceptance check. Comparison with chromium-phone-map.png can guide proposed visual hierarchy without modifying either image.
- Only notes appended; no code/spec/site change, build/test/browser run, project Python/node, install/clone, model/science access, git mutation, graft, external search or agent/service message. Building hold persists.
- Binding context rule survives: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted finish the point, tell the operator and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or place the handoff in notes; restate this same rule in every handoff. No numerical Context reading is exposed or asserted.

## LVB9 — calm workspace accepted; complete Home composition proposed

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Calm research workspace — recommended: understated surroundings; diagrams and findings carry the emphasis." Adopt that visual direction for subsequent screen proposals: neutral backgrounds in both accepted themes, strong page headings, restrained borders, generous visual space and a limited accent for selection. Exact colors, typeface, geometry and motion are not frozen by this choice.
- Apply the same visual language across all five destinations, while composing each screen around its existing purpose and accepted journey. Preserve the operator’s earlier Home order: big-picture connections, then sourced findings with unresolved limits, then detailed activity; retain the compact dated activity strip at the top (this notes file:10/:21/:53).

### Open questions

- Proposed complete desktop Home composition: expanded/minimizable left navigation; compact source-dated activity strip at the top of the main area; clear How the research connects title and short explanation; a small search/focus row; a broad layered map; findings and unresolved-limit summaries below; detailed activity last. An opened connection/source panel reserves its own space. This is a composition proposal, not implementation or a completed summary inventory.
- In the map, propose quieter node surfaces/dividers, readable plain-language names with exact IDs secondary, and accent plus non-color emphasis on the selected path. Retain the required column organization, documented edge/source semantics, source-bound selection and access to the full graph. No scientific importance is encoded by decorative emphasis.
- Proposed phone adaptation uses the accepted persistent menu bar and left drawer, then the compact source-dated activity row, title/search, one-column drill-down, findings/limits and expanded activity. Sources/details remain below or reserved, not over the focused content. Actual first-screen fit and phone geometry remain future authorized verification.
- Next whole-page preference: recommend a map-led Home, where the connections area receives the strongest visual emphasis and the findings/limits follow beneath. Alternative: a balanced Home where the map and findings section have similar visual weight, preserving their already accepted order. This question concerns composition/weight, not changing destinations or reopening the content order.

### Spec changes proposed

- Record the accepted calm visual direction beside docs/LABVIZ_V2_SPEC.md:357-371 and pending theme/navigation amendments. Any selected tokens must meet existing readability, contrast, non-color and focus requirements in both themes.
- Complete Home composition would clarify §4A.1 (:338-352) and §11.4 (:1086-1096); preserve map columns (:1088), focus/source panel (:1089-1092), phone drill-down (:1095), honest edge legend (:1096) and Home map/status coverage (:405). Existing graph content is not a newly approved featured subset. Binding spec unchanged.

### Context for build agents

- Give future builders the calm direction, accepted Home content order and eventual approved complete-page composition as one coherent task packet. Use the inspected desktop/phone Map captures as incumbent context, not the final target design. Preserve all required scope and documentary identity when changing visual weight.
- Reference roles stay focused: interface-design extracts for visual hierarchy/spacing/interaction states; Anthropic chart guide for scientific visual accuracy; Tabler’s inspected catalogue for optional structural context; ECharts event/action excerpt for selection-linked highlighting. See this notes file:283-295 and results/dashboard_integration_review_20261011/SUMMARY.md:9/:15-16. No external reference is installed, adopted or newly opened.
- Only notes appended. Building hold and all execution exclusions persist. Binding context rule remains: check available Context before every question; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the point and write separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or put the handoff in notes; restate this same rule in every handoff. No numerical Context reading is exposed or asserted.

## LVB9 — map-led Home accepted; visual-design continuation checkpoint

### Decisions (with the operator’s words)

- Operator verbatim: "1", selecting "Map-led — recommended: connections receive the strongest visual emphasis." Adopt the proposed map-led Home composition: existing left desktop sidebar/phone menu, compact source-dated activity strip, clear title, search/focus controls, a visually dominant connections map, findings with unresolved limits below, detailed activity last. Connection details receive reserved side space on desktop and below-map space on phones.
- Use the accepted calm visual language: neutral backgrounds, clear headings, thin separators, quieter map-node borders and selected-path emphasis through accent color plus outline. Plain-language names lead with exact internal identities secondary. Retain the full documented graph and phone drill-down; no featured-only scope or new scientific importance claim is accepted.
- This settles whole-page emphasis/composition, not pixel geometry, final colors/typeface, code, runtime acceptance or content readiness. All earlier evidence/source/selection/coverage/player/model-wide requirements and the building hold remain.

### Open questions

- Next discussion: the complete Science lines and selected research-question page composition in the same calm visual system. Its content order is already settled: findings and unresolved limits together, then the research story over time, then the latest experiment (this notes file:12/:46). Do not ask that order again.
- Other whole-screen compositions remain to discuss: Runs/comparison, Inside the model, Learn/evaluations. Visual polish, exact styling, transitions, icons, adaptation, source preparation and eventual scoped verification remain open where not already settled. No last-choice prompt is pending, but substantive design questions remain.
- LVB9 takes a proactive visual-design arc/context checkpoint with a separate results/dashboard_integration_review_20261011/labviz_brainstorm_handoff9.md. No numerical Context percentage is exposed; no threshold observation or brainstorming completion is claimed.

### Spec changes proposed

- Add the accepted map-led visual composition to the pending Home amendment beside docs/LABVIZ_V2_SPEC.md:340/:405/:1088-1096, together with the accepted calm visual language and navigation variants. Preserve the documented graph semantics, visible/source-bound context and phone drill-down. Binding spec unchanged; MAESTRO must freeze amendments and briefs before any build.

### Context for build agents

- Give future Home builders the accepted whole-screen composition plus its phone adaptation, referenced incumbent desktop/phone captures, relevant §4A/§11.4 spans and the actual interface/chart extracts recorded at this notes file:283-295. This is design context, not an inventory of prepared summaries or validation of a package.
- Only notes and the designated continuation handoff are written. No code/spec/site edits, builds/tests/browser runs, project Python/node, installs/clones, model/science access, git mutation, graft, new external lookup or agent/service messages.
- Binding context rule survives: check available Context at the end of every reply before asking anything; start new pieces only at >=60%; at <=45% or any Context compacted tell the operator, finish the current point and write a separate designated successor handoff with topics, decisions/notes pointers, in-flight work, exact paths, open questions/risks and one exact next point; at <=40% stop starting new work. Never approach compaction or put the handoff inside notes; restate this same rule in every handoff. No numerical Context reading is exposed or asserted.
