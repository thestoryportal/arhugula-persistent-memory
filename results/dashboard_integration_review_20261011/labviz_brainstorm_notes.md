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
