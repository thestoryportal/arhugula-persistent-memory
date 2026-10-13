# LVB handoff — interactive LabViz design discussion

Stopped on MAESTRO's explicit context gate at 40% remaining, 2026-10-11. Resume this conversation; do not restart the design or build anything.

## 1. FIRST successor question: activity-strip placement

MAESTRO explicitly requests this as the first question. Preserve the latest answer: the operator already replied **option 1** before the context-stop message. That settled decision is saved with the verbatim answer in `labviz_brainstorm_notes.md:21`; its resolved question is at `:40`. Do not treat it as unanswered or discard it.

First prompt, acknowledging the answer while retaining MAESTRO's requested options:

> You chose a compact activity strip at the top, with full activity details last. I recommend keeping that: the big-picture map remains visually dominant and the recorded status stays easy to find. Should we retain **1**, or would you prefer **2**?
>
> 1. **Compact strip at the top; activity details last** — recommended.
> 2. **All activity below the big picture and evidence** — would change the spec's strip placement.

Keep this to one question. The recommendation follows `docs/LABVIZ_V2_SPEC.md:340` and `:405`. If the operator simply wants to continue, retain their existing option 1 and proceed to the next topic; no new approval is needed for the already-settled choice.

## 2. Decision index — verbatim words remain in the notes

Authoritative discussion record, saved and current:

`/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/labviz_brainstorm_notes.md`

The pointers below reference that file. Read the cited lines for the operator's exact words; do not replace them with this summary. Every decision/condition recorded so far is indexed here.

| Notes line | Settled decision or standing condition |
|---|---|
| 7 | LabViz only; other review domains belong to later sessions. |
| 8 | Discussion/build hold; no product/spec edits, builds, tests, installs or clones. |
| 9 | Flesh out functioning, UI/front-end design and source context for builders. |
| 10 | Home emphasis: big picture first, evidence/progress second, activity third. |
| 11 | Flesh out all three journeys; question-to-evidence first. |
| 12 | Question → evidence journey approved; question page order is findings/limits → research history → latest experiment. |
| 13 | Two-run comparison arrangement approved; notice first, then outcomes/side effects → setup differences → question-by-question answers, with paired phone sections. |
| 14 | Inside-the-model approval is CONDITIONAL: granular zoom below layers, experiment-specific internals, animated 2D/3D timeline, and word/input lists across ALL journeys. |
| 15 | Inside-the-model order: 2D → 3D → guided explanation; include applicable diagrams/charts. Static layer bars alone do not satisfy the condition. |
| 16 | Associated papers and research sources for every experiment, accessible across journeys. |
| 17 | Three separate selectable player modes: Experiment phases, One fact/question, One component. |
| 18 | Focused zoom views plus expandable detail and collapsible side panel; panel never obstructs the focused view. |
| 19 | On narrow phones, the collapsible detail is below the focused diagram. |
| 20 | A light/dark switch; equivalent readability in both themes. |
| 21 | Compact source-dated activity strip at top; full activity detail last. Last operator reply before context stop was option 1. |
| 22 | Operator explicitly requested Chrome opening and confirmed it was open. Existing HTML was opened; no build/browser test was run. |

Interpretation preserved in notes: the comparison approval's word “setup” refers to the proposed page arrangement, not setup differences leading the page; the operator separately specified outcomes first. The zoom approval combines focused views, expandable/scrollable detail and the explicitly non-obstructing side panel. Do not silently narrow either instruction.

Design approval does not lift the build hold, authorize scientific instrumentation/replays, amend a frozen scientific plan or permit installation. Proposed spec changes are at notes `:42-55`; no spec file was edited.

## 3. Remaining topics, in order

1. **Activity placement:** use the first prompt above, while preserving the already-received option 1.
2. **Finish source context for builders, the topic interrupted by the stop.** Proposed packets are notes `:75-86`; fresh README reading is `:88-93`. Explain what builders receive: this decision record + binding spec + existing build/review screenshots + one short interface checklist + one chart checklist + narrowly chosen layout/chart/diagram examples. Sources are context/trial candidates, not adopted packages. ECharts and Transformer Explainer README findings have NOT yet been discussed with the operator. ECharts docs/example page and Transformer Explainer's second page remain unopened. Original interface-design, Anthropic data-visualization and Tabler pages also remain unopened in this session.
3. **Resolve the granular-playback data contract.** Notes `:35` records the major gap: old runs lack exact historical internals; UI cannot reconstruct those from final scores. The binding spec already distinguishes actual recorded events/telemetry, separately labelled NOT-EVIDENCE re-creations and conceptual diagrams. Do not reopen that as an arbitrary either/or choice. Define a proposed coverage inventory and richer recording needs for future experiments: run/model/configuration identity, inputs, phase/step, component detail, before/after signals, units, timestamps or untimed ordering, source links and missing fields. Specify what drives both diagrams/charts at each frame. This is design preparation only; actual observer changes, model loading, replay runs, resource budgets and scientific approval are separate. The user wants maximum useful granularity, not a layer-only fallback.
4. **Complete cross-journey inputs and research-source behavior.** All word/fact sets, training/evaluation/probe questions, expected and observed answers where available, exact source-version binding, associated papers with relevance and citation basis. Decide presentation/access for complete sets and focused subsets. Distinguish sources actually used/cited by the experiment from related reading. Current paper associations/completeness have NOT been audited. Missing values remain explicit; do not borrow a newer experiment's prompts silently.
5. **Complete navigation and state.** Keep the five binding destinations and selected run across views. Flesh out linkable mode/step/input/component/zoom state, comparison entry from a question/experiment, source/detail navigation and return/back behavior. Proposed switch-state behavior is not yet individually approved; avoid silent jumps when a step does not exist in another player route.
6. **Finish UI/chart/player details and reader verification design.** Three modes already approved; now specify play/pause, stepping, speed, phase/fact/component selection, synchronized diagrams/text/charts, pause/selection behavior, descriptive captions and data-coverage messages. Apply focused-view/non-obstructing-panel layout and the approved narrow-phone stacking. Retain minimum text/touch/contrast rules in both themes. Initial theme, persistence and initial player mode are routine defaults still proposed, not explicitly chosen. Verify reader tasks as well as mechanical readability in a future authorized review; no tests now.
7. **Consolidate a reviewable design handoff for MAESTRO.** Map accepted design intent to proposed LabViz spec amendments and separate viewer work from missing observation data, paper/input preparation and any later scoped library trial. Keep every unresolved dependency visible. No implementation, specification edits, builds, tests, commits or installs in this discussion session.

## 4. Exact paths and reading discipline

Worktree:

`/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`

Branch verified at start: `worktree-c10k-route-a`; git top level matched this worktree. No mutating git operations occurred.

| Purpose | Exact path |
|---|---|
| Notes / verbatim decisions | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/labviz_brainstorm_notes.md` |
| This handoff | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/labviz_brainstorm_handoff.md` |
| Integration review context | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/CONTEXT.md` |
| Review summary | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/SUMMARY.md` |
| Binding LabViz contract | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/docs/LABVIZ_V2_SPEC.md` |
| Current implementation summary | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/labviz/README.md` |
| Current source directory | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/tools/labviz/` |
| Current build entry, already open in Chrome | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/labviz/site/index.html` |
| Current built data (never read whole) | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/labviz/site/data.js` |
| Current built context (never read whole) | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/labviz/site/context.json` |
| PASS review report | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/labviz_v2_phase1_design_review_r6.md` |
| Existing screenshot/measurement directory | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/labviz/review/20261008T130913325Z/` |
| Web candidate report | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/web_report.md` |
| UI/skills candidate report | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/uiskills_report.md` |
| Practices candidate report | `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/results/dashboard_integration_review_20261011/practices_report.md` |

Spec spans already read: `1-53`, `285-434`, `435-494`, `566-721`, `836-976`, `977-1113`. Re-read only the relevant spans; each `sed` range must be at most 60 lines. Never read the whole spec or large JS/context/card files. `measure.json` has millions of lines: the inspected phone Map measurement is `825181-825210`, recording 390px scroll/client width and 1905px document height. Use narrow locations, not broad repeated scans.

Four existing screenshots were inspected, each from the October 8 review: `chromium-phone-map.png`, `chromium-phone-line-c10.png`, `chromium-phone-compare.png`, `chromium-phone-model-2d.png`. Their exact parent directory is in the table above. At most two screenshots per inspection; prefer phone screenshots. They predate MathLab. The review's PASS and 160 screenshots do not establish acceptance of newly proposed features or later MathLab appearance. No fresh screenshots, browser measurements or tests were generated.

New external reading, README only:

- `https://github.com/apache/echarts` — JavaScript charts; README opened, second documentation page not opened. SVG/text-compliance details and concrete linked-cursor/zoom examples remain to verify.
- `https://github.com/poloclub/transformer-explainer` — potential component-explanation context. README explicitly runs live GPT-2 in the browser. Use only explanatory context; no install/live demo/model runtime, no assumption that GPT-2 architecture matches our selected model. Linked paper/demo/code/dependencies not opened. Its pattern value for LabViz is an inference, not a tested integration.

Web reading is allowed only when the operator asks or repo details matter; at most README plus one additional page per repo. Do not upload research data, run a demo, clone or install anything. Retain “not opened” where appropriate. Original interface-design/Anthropic data-visualization/Tabler details currently come from the local review, not fresh upstream verification.

## 5. Operating limits and continuity

Operator is an architect with no ML background, often on an iPhone. Plain words; define essential terms; one question at a time; recommendation and reason first; two or three concrete options. Keep responses phone-sized. Do not ask them to decide settled spec rules or routine reversible implementation details. Cite file:line for local facts and direct primary links for web facts.

Write ONLY the notes and this handoff. Discussion only: no code, no edits to spec/source/build/other existing files, no builds, test/browser runs, installs, clones, model/tokenizer/GPU work, commits or science execution. Chrome opening was a separately explicit request already completed; it is not authority for further browser automation. Use read commands and the image viewer; no project Python, venv, uv, node, build.py, review.mjs or Playwright. Do not run graft. Follow RTK via `/opt/homebrew/bin/rtk proxy` for shell reads. Do not run a generic context-save workflow that writes outside the two allowed files; this named handoff is the scoped context artifact.

**BINDING CONTEXT RULE, repeated for every successor:** Watch the “Context N% left” line. Web reading and screenshots burn context fast. At or below **45% left**, or on any **“Context compacted”**, tell the operator, finish the current point, and write `results/dashboard_integration_review_20261011/labviz_brainstorm_handoff.md` with topics covered, decisions so far (pointer to the notes), open questions, the next point and this same rule. A fresh session continues from it. Never put the handoff inside the notes. The repo additionally requires starting a new piece only at ≥60% left and stopping new work at ≤40%. MAESTRO explicitly stopped this session at 40%; no new topic was started after that stop.

Session status: notes updated with every received answer, including activity option 1; handoff written; source-context topic is in flight; all product/scientific acceptance remains unverified. The building hold is still in force.
