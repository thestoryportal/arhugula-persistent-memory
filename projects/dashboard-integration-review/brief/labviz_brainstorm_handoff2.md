# LVB2 — LabViz design and continuation handoff

Prepared 2026-10-11 during consolidation. Continue the existing interactive conversation; do not restart it or reopen settled choices. This is a continuity/design draft, not implementation authority or new scientific/UI acceptance.

## Authority and record

Worktree: `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a`; git root and branch `worktree-c10k-route-a` verified at LVB2 start. No mutating git operation occurred. Binding spec remains `docs/LABVIZ_V2_SPEC.md`; it was not edited. Only the append-only notes and this handoff were written.

Authoritative operator quotations: `results/dashboard_integration_review_20261011/labviz_brainstorm_notes.md`. Predecessor choices are at `:7-22`; LVB2 choices are indexed below. Consolidated draft: `:297-334`, including amendment map `:313-321`, functioning `:323`, proposed source/missing wording `:325`, future reader tasks `:331` and verification limits `:332`. Citation corrections are appended at `:334`.

## Settled decisions — preserve the original wording in notes

| Topic | Settled behavior | Notes location |
|---|---|---|
| Prior session | Big picture -> evidence/limits -> detailed activity; compact dated activity strip at top. Question journey first, all three journeys required. Question page findings/limits -> history -> latest experiment. | `:10-12`, `:21` |
| Comparison | Notice -> outcomes/side effects -> setup differences -> question answers; corresponding phone measures paired. | `:13` |
| Model/detail | 2D -> 3D -> guided explanation; zoom below layers using experiment-specific data, with charts, inputs and research sources. Three player modes: phases, one fact/question, one component. Non-obstructing side detail; below diagram on narrow phones. Light/dark switch. | `:14-20` |
| Builder references | Selected extracts per task: spec/decisions/screenshots, one layout checklist, one chart checklist and relevant examples. No package adoption. | `:107` |
| Depth and learning | Deep inputs linked to **any and all affected model parts**, associated measurements and nontechnical scientific explanations. Do not reinterpret this as selected-demo-only or a fixed top-16 target. Distinguish stored-number edits, signal changes and input processing; unknown is not unaffected. | `:127-130` |
| Learning routes | Both free exploration with explanations and an optional guided walkthrough over the same source-linked experiment data. | `:152-154` |
| Papers | Reading card first: plain-language topic, experiment role, supporting section and Open original link. Cited/used sources remain distinct from related reading. | `:173-174` |
| Inputs | Exact input and expected/observed answers first, then linked model detail; recorded scoring meaning and missing answers explicit. | `:193-194` |
| Reading during play | Expanded explanation/paper pauses playback; return stays at that position, press Play to resume. Inline frame captions do not pause every frame. | `:213` |
| Mode changes | Preserve the matching source step; if absent, stay paused, explain and offer available steps. No hidden reset or invented frames. | `:232` |
| Phone controls | Essential Play/Pause and Previous/Next remain visible in their own reserved band, never over the diagram. | `:253` |
| Phone charts | One explained chart at a time; all applicable measures reachable through a selector; input/component/step preserved. Units, source, meaning and missing data explicit. | `:301` |

## Current next point

LVB2 has prepared the connected design draft. The next operator question presents: **1. Walk through one input end to end on paper (recommended); 2. Refine diagram/chart teaching; 3. Review the consolidated handoff.** The operator has not answered that question as of this checkpoint. Read the newest terminal reply before proceeding; append any new answer and update this handoff. Do not confuse these choices with the preceding chart question, which the operator already answered "1".

For option 1, use one source-bound input if suitable recorded material is available, or clearly label a generic reading task as illustrative. Trace exact input/answers -> selected component -> available measurement/source -> explanatory limit -> associated paper -> paused return. Historical internals must appear as gaps unless actually recorded. Do not invent example measurements or present an on-paper walkthrough as a browser test. No code or mockup file is authorized.

## Proposals and dependencies still open

- Routine defaults in notes `:306` are proposed, not individually approved: searchable complete input browser by purpose; initial phases mode, paused; exploration with walkthrough entry; device-theme default and local preference where supported; stop at sequence end; expanded URL/Back selection state. Preserve run/input/component/mode/step/zoom and observation identity, and make unavailable selections explicit. Do not reopen accepted mode-switch/pause choices.
- Data preparation needs exact selected-model structure, complete source-version-bound input sets, per-input/per-part coverage and sequence resolution, reviewed explanations and experiment-owned bibliography. No completeness audit or richer recording was run (`notes:307`, `:330`). Future scientific capture needs its own reviewed observation plan, inertness/resource budgets and operator authority. Past unrecorded trajectories cannot be recovered (`docs/LABVIZ_V2_SPEC.md:325-328`).
- MAESTRO must turn accepted intent into explicit spec amendments and a scoped brief before building; the notes cannot silently supersede the binding contract (`notes:329`). Viewer work, source/input/paper preparation, observation capture and possible library trials are separate scopes. No implementation plan or package adoption was approved.

## Reference checks and existing proof

Exact builder extracts and primary links are in notes `:268-295`. Opened read-only: interface-design SKILL (hierarchy/spacing/states), Anthropic data-visualization SKILL (accuracy/accessibility), ECharts Event and Action (selection/highlight example), Tabler README plus Layout index, Transformer Explainer README. Exclude conflicting font/native-control/minimum-size advice, Python samples, remote example requests, timers and live GPT-2 runtime. Source revisions/licences are not pinned/audited. Axiom/articles remain local-review-derived; original pages not opened in LVB2.

ECharts README + one additional page allowance is used; renderer/SVG compliance and local-file/phone/budget compatibility remain unverified. Tabler README + one additional page allowance is used; Layout is only an index, actual stacking/side-panel markup remains unopened. Transformer Explainer's linked ACM paper returned Internal Error: **not opened**; no demo, alternative paper, code or dependencies were opened/executed. Do not guess those details or exceed the reading allowance.

LVB2 re-inspected only `results/labviz/review/20261008T130913325Z/chromium-phone-model-2d.png` and Map measurements `measure.json:825181-825210` (390x844, 390px client/scroll widths, 1905px document height). Image observation: long layer listing, parts, wiring and events (`notes:245`). Map measurements do not prove model/player fit. October 8 proof predates MathLab and all new designs. No fresh screenshot, browser, build or test run occurred. Current README flow and MathLab source-label boundaries were re-read (`tools/labviz/README.md:12-26`); no current data-completeness or paper-association audit was performed.

## Operating and context rules — binding for every successor

Talk to an architect with no ML background, often reading an iPhone terminal: plain words, define essential terms, one question at a time, recommendation/reason first, two or three concrete options, phone-sized replies. Cite local path:line and primary web links. Keep accepted design, proposed defaults and scientific limits distinct.

Discussion only. Building hold remains. Write ONLY `results/dashboard_integration_review_20261011/labviz_brainstorm_notes.md` (append; never rewrite earlier entries) and this handoff. Read commands and existing-image viewer only; no product/spec/build edits, installs/clones, tests/browser automation, project Python/venv/uv/node, model/tokenizer/weight access, GPU/replays/science runs, commits or messages to others. Use `/opt/homebrew/bin/rtk proxy` for shell reads. No graft. Do not run a generic context-save workflow writing other files; this is the scoped continuation artifact.

**Watch "Context N% left" at the end of every reply before asking anything. At <=45% left, or on any "Context compacted", tell the operator, finish the current point and update this separate handoff with completed/in-flight work, exact paths, open risks, decisions pointer and one exact next point. A fresh successor continues. Never put a handoff inside the notes. Start a new piece only at >=60% left; at <=40%, stop starting work. Repeat this rule in every handoff.** No numeric remaining-context claim is made by this checkpoint.
