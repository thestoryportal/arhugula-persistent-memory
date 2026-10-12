---
status: design-discussion-checkpoint
branch: worktree-c10k-route-a
files_written_by_lvb17:
  - results/dashboard_integration_review_20261011/labviz_brainstorm_notes.md
  - results/dashboard_integration_review_20261011/labviz_brainstorm_handoff17.md
---
# LVB17 — full MathLab notebook review and integration

The operator accepted the consolidated MathLab experience with "All good for now". No operator design question remains pending for this topic. Four explicit choices below are settled; technical/source preparation remains open. This checkpoint does not claim a context threshold, spec approval, wireframe approval, source completeness, implementation readiness or scientific acceptance.

## Authority and efficient resumption

- Reverified root: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a; branch worktree-c10k-route-a. No Git mutation.
- R = results/dashboard_integration_review_20261011; S = docs/LABVIZ_V2_SPEC.md; L = tools/labviz; W = results/labviz/site; P = results/labviz/review/20261008T130913325Z.
- Start with this handoff, notes:4017-4061 for the consolidated packet (45 lines), and :4063 onward for acceptance/checkpoint. Read individual decision ranges below only if needed. ML-1..ML-12 remain notes:3855-3877; handoff16 indexes earlier decisions/reference limits.
- Do not reread all notes/spec/code/data or all predecessor handoffs. Locate only needed points, then read ranges <=60 lines. Never read S, L/app.js, L/cards.py, L/contexts.json, W/data.js or W/context.json whole. Use /opt/homebrew/bin/rtk proxy for shell reads. No graft.
- Preserve all settled choices from handoff16, handoff15's new choices/navigation, handoff14/13 tables, handoff12:19-24, handoff11:36-42, handoff10:17-36 and handoff9:15-39. Do not ask again about source matching, quiz ownership/save behavior, outline sourcing, geometry/navigation/chart/learning choices or MathLab placement/reading/paired review/home organization.
- Discussion only. Write only authorized notes and the designated successor handoff. No edits to S/L/W/design guides/DESIGN.md, code, images/mockups/wireframes, builds/tests/browser runs, project Python/.venv/uv/node, model/science/calculation execution, installs/clones/assets, Git mutation/deletion, MCP/Figma calls or external agent/service messages. Read commands and image viewer remain available; public web only on operator request or consequential repo detail, bounded to README plus one more page per repo. Operator lifts the build hold.

## New settled choices and exact scope

| Point | Operator words / approval | Notes |
|---|---|---|
| Dual MathLab presence and full review | "MathLab needs to yes be integrated with its associated science lines, and there needs to be a location where MathLab lives and the user is able to fully review the notebook science and math it has completed in full." Both contextual science-line integration and a dedicated full-review MathLab home are required. The predecessor's either/or discoverability menu is resolved. | :3928-3961 |
| Notebook opening | "1": mathematical work leads; read the complete recorded argument in order with plain explanations, execution records/checks supporting it. | :3962-3988 |
| Paired notebook review | "1": corresponding sections alongside on desktop, stacked on phones; both complete notebooks accessible. Matching quantity/units was part of the presented proposal; exact correspondence/semantic eligibility still needs review. | :3989-4016 |
| Home composition | "1": research questions first; each introduces associated science lines, notebooks and recorded work. | :4017-4061 |
| Consolidated experience | "All good for now": accepted the presented connected journey; no missing MathLab experience named. No spec/build/science acceptance implied. | :4063 onward |

- Five primary destinations persist. Proposed dedicated MathLab home lives under Science lines; its associated science-line entries reach the same work records. No sixth primary destination/new F1 condition. Source-backed mapping, coherent identity and return persist.
- Full review cannot be reduced to run summaries, stages, outcome labels or only convenient currently ingested documents. Display complete recorded notebook science/math, identify missing portions, and preserve the actual estimate/publication scope.
- Approved paired reading is not an automatic matching algorithm, approved actual pair, computed difference, winner claim, library selection or new execution permission.

## Consolidated MathLab packet and remaining preparation

- Notes:4034-4046 is the surface/journey table: MathLab home; contextual science-line entry; full notebook; execution/check record; paired review; sources/publication; Map/Runs discovery; unavailable-model fallback; learning; phone/frame; saved-input static delivery.
- Integrate with ML-1..ML-12, not replace their scientific/source limits. Cross-cutting S targets: §0 :14-20, §2 :29-52, §4A :340-371, §5 :435-443/:578-582, §6 :662-679, §9 :953-965, §11 :997-1030/:1086-1096, final MathLab requirement :1169-1178.
- Explicitly add MATH-PROXY to the evidence vocabulary; source bytes being recorded do not make estimates RECORDED scored science. Reconcile canonical event-reader metadata/fold operands/hashes with ordinary JSON/document/derived/missing leaves and structural metadata.
- Distinguish mathematical-work/notebook document identity from execution attempts. Notebook content supplies its recorded argument; canonical tools/mathlab_events.read_events/fold remains the sole run-state definition. No second status authority.
- Full-content coverage inventory remains unverified: actual artifact formats/versions, method/assumptions/equations/symbol meanings, calculations/code, recorded outputs, conclusions/limitations and their source paths/lines. Do not assume an .ipynb exists or reconstruct unrecorded steps.
- Reviewed question/line/run/section associations remain unverified. Names, labels, titles, row order, chronology or adjacency do not establish scientific association, comparison correspondence or lineage.
- Comparison needs reviewed meaning/units/scope eligibility, visible assumptions, unmatched-section reasons and provenance for any derived difference. Preserve ordinary model-answer comparison refusal and no scientific winner/effect inference.
- Provisional/final publication, reviewed explanations, mathematical notation/phone overflow, coherent source capture and all-page/all-flow review remain open. These are preparation/engineering tasks, not another set of operator preference menus.
- Later audit concern retained: mathlab_events.py:285-307 suppresses provisional NEW1 findings, while cards.py:841-867 collects raw finding_staged documents and app.js:601-609 renders card.mathlab.findings. Investigate canonical-fold visibility parity before acceptance; no runtime defect/reproducer/fix was established or authorized here.

## Current source and observation limits

- Source inspected in LVB17: cards.py:828-881 event-derived cards/referenced Markdown findings; app.js:559-618 saved state/stages/checks/resources/findings/candidates; mathlab_events.py:43-74 event fields/check plan. Presence of these paths does not prove complete notebook content or browser/native/science acceptance.
- Additional S reads: :14-20, :29-52, :340-371, :435-486, :578-587, :662-690, :953-976, :997-1030, :1086-1113, :1169-1178. No S edits, builds/tests/browser runs or runtime acceptance checks.
- No screenshot/image, current build data file or web page opened this session. P predates MathLab. Preserve notes:2100: measure.json:1512162-1512190 is a blocked-CDN fallback record, not established as paired with chromium-phone-model-2d.png.
- Current root/branch verified; no unrelated working-tree changes inspected/modified. Only notes/handoff written. No process, agent, external call or tool cell remains in flight at closeout.

## Reference contribution and bounded reading retained

- Interface-design text extract notes:289 contributes hierarchy/spacing/complete states; Anthropic chart extract :290 contributes units/scales/non-colour/data alternatives; Tabler catalogue :292 supplies page-title/navigation vocabulary, not verified phone markup. Notes:273-301 reopened only as focused local reference context. No package/executable skill adopted.
- Inherited six supplied references, Tabler Icons, Gentelella playground, ECharts item-selection documentation, Transformer Explainer teaching framing and both operator design-guide adaptation map remain as indexed in handoff16/notes:2558-2596/:3465-3509. Read only the point needed. Previous README-plus-one-page allowances remain used; do not reopen new secondary pages indiscriminately.
- Awesome Dataviz remains broad chart/map/graph/dashboard/diagram discovery context. MAESTRO's R/awesomedataviz_access_report.md records HTTP/API/llms availability; MCP handshake/Codex compatibility is untested and it is not installed. Installation needs the operator's word. No lookup/MCP call here.
- Mathematical renderer/notebook-format candidates: unselected, not inspected. Give later readers actual source formats and file-URL/local-asset/readability requirements before judging candidates. No renderer chosen from a catalogue label.
- Historical memory quick pass oriented the static-versus-runtime boundary only; current handoff/source governs. No old test/hash/science acceptance imported and no global memory written. Custom authorized notes/handoff preserve context; no broader context-save file/Git workflow run.

## Separate wireframe/Figma gate

- After Astra approves updated S, a separate Codex agent draws every page and user flow for operator review before operator spec approval or any builder starts. MathLab home/question/notebook/execution/source/paired-review/error/unmatched/provisional/learning/model-fallback/return journeys must be explicit, on phone and desktop.
- Figma MCP is configured for Codex but off by default. Confirm account/plan in that later wireframe session. No Figma call, upload, DESIGN.md, mockup/image or wireframe generated here. Illustrative compositions remain illustrative.
- The approved discussion packet is not a frozen spec or an approved implementation plan. MAESTRO reconciles authority and scopes later preparation/build briefs.

## Exact next point on resumption

No MathLab operator question is pending. Do not re-ask settled choices or move to another review domain without direction. First useful preparation, within a resumed read-only LabViz session: map the complete mathematical-work content to exact saved source artifacts, separately from execution-event summaries, starting from the opened adapters above. Use bounded file inventory and exact source ranges; identify recorded/missing/unreviewed coverage and identities. Carry the resulting inventory into the detailed spec packet; do not claim complete notebook review from event/Markdown adapter presence alone. Other whole-site LabViz discussion may resume at a genuine uncovered journey after this accepted MathLab direction, without new control-by-control menus.

## BINDING context and interaction rule — survives every successor

Speak plainly to an architect without ML background, often on an iPhone. Short replies; recommend with reasons; one genuinely unsettled whole-experience question at a time, two/three concrete options when useful. Reference contributions need exact focused pointers. Separate proposal, operator design approval, implemented source, verified behavior and scientific acceptance. Record operator words/open questions/S changes proposed/builder context and announce notes updates. No invented science or causation from chronology/shared links.

Check available Context at every reply end before asking. Start new pieces only at >=60% left. At <=45%, any Context compacted or MAESTRO gate notice, stop starting work, finish only the current point, notify operator and write a SEPARATE designated successor handoff with topics/decisions/notes pointers, open questions, exact paths, in-flight work, risks and one next point. At <=40%, stop starting work; never approach compaction or put the handoff in notes. Restate this rule in every successor/team handoff. If no numerical reading is exposed, say so and never invent one. This LVB17 checkpoint follows the operator's accepted-topic answer, not an exposed context measurement.
