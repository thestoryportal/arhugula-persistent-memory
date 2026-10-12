---
status: brainstorming-closed-operator-directed
branch: worktree-c10k-route-a
closed_at_utc: 2026-10-12T00:06:19Z
observed_head: 71788d765c281abce2685347363904070d1c609d
files_written_by_lvb18:
  - results/dashboard_integration_review_20261011/labviz_brainstorm_notes.md
  - results/dashboard_integration_review_20261011/labviz_brainstorm_handoff18.md
maestro_delivery: pending-transport-verification
---
# LVB18 — final LabViz stack discussion closed; design packet for MAESTRO

The operator directs brainstorming closeout and return of the updated design documents to MAESTRO for next steps. No operator question remains pending here. MathLab stays accepted ("All good for now"). The documents are the updated discussion/reconciliation packet, not an edited/frozen S, binding review approval, wireframe approval or permission to build.

## Authority and efficient resumption

- Verified root: /Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a; branch worktree-c10k-route-a. HEAD at closeout observed as above; no Git mutation and no claim to own unrelated shared-worktree drift.
- R = results/dashboard_integration_review_20261011; S = docs/LABVIZ_V2_SPEC.md; L = tools/labviz; W = results/labviz/site; P = results/labviz/review/20261008T130913325Z.
- Read this handoff first; new stack packet starts at notes:4084, CSS/React selection at :4126, and final Chrome/review/closeout section follows that entry. Locate the final heading with an exact literal search, then read <=60-line ranges. Do not reread all notes/spec/code/data; handoff17 indexes accepted MathLab and inherited settled choices.
- Preserve handoff17's table, handoff16/15/14/13 tables and earlier navigation/learning/source/chart/geometry decisions indexed there. No token-by-token preference questions. Whole-site design governs every page, primary/sub-navigation, help and dialogs.

## New settled choices and recommendation scope

| Point | Operator words / exact scope | Durable packet |
|---|---|---|
| Final discussion topic | "This final session is to explore the dev stack and frameworks ..." — implementation-stack consideration within the existing build hold | notes:4084 onward |
| Interface direction | "1...what CSS framework?" — selects React + TypeScript over TypeScript without React | notes:4126 onward |
| Browser target | "LiveViz will run in Chrome. I am sure Tailwind is compatible with it." — Chrome for this same LabViz project; no new site/rebrand inferred | final notes section |
| CSS recommendation / assessment | "Note your recommendation and then ask for the reviewers to also assess the best framework for LiveViz." — record Tailwind recommendation and ask reviewers to assess best fit; no pinned dependency/runtime approval | final notes section |
| Closeout | "Not necessary right now. Please run the brainstorming close out as is governed ... back to Maestro for next steps." — close this interactive session; do not start further reviews or resume rejected Claude work | final notes section |

- Preferred proposed stack: existing Python saved-evidence readers; accepted React/TypeScript interface direction; Vite as a separately compiled, replaceable packaging layer; Tailwind with LabViz-owned shared visual values/components; specific reading/chart/math CSS; native SVG and existing optional three.js; selective ECharts; KaTeX conditional on actual notation/content. Retain existing Python/Node/Playwright verification roles.
- Only the React/TypeScript direction and Chrome target are explicit technical selections. Tailwind is recommended for later reviewer assessment; Vite/ECharts/KaTeX/icon assets/exact versions remain proposed or conditional. No dependency installation, migration or compatibility proof.
- Strong CSS alternative is ordinary component CSS with site-owned semantic variables. Bootstrap/Open Props are reference alternatives; do not layer every catalogue onto the site. No measured productivity/byte advantage supports the recommendation.

## Review receipts and limits

- Native fresh-context Astra, gpt-6-astra high, task /root/labviz_stack_review: **FIX-FIRST**, supports proposed stack conditionally; narrowly favors Tailwind. Weakest established part is compiled direct-file/classic-script packaging. Require asset/data compatibility/version binding, publication contract and component responsibility before implementation. Advisory native-agent review only, not MAESTRO's binding full-spec gate.
- Native fresh-context in-family Codex, task /root/labviz_css_review: **PROCEED** on the CSS recommendation, with ordinary CSS a serious alternative and accessible component behavior still to define. It had already completed when closeout interruption was issued. Different review scope explains the verdict difference; neither grants full-spec acceptance. Full returned responses were read; durable summaries are in the final notes section.
- Out-of-family Claude request **did not run**: existing Max auth verified on the host, but automatic approval review rejected sending the internal spec/paths/design packet to Claude without explicit payload/destination authorization. No bypass/retry or pending permission request. Operator closes review work for now; MAESTRO may revisit independently later. No science/model/GPU or product build was involved.
- No reviewer remains running; no CLI review process started. No build/test/browser run, install/clone, project Python/Node, Figma/MCP, mockup/image, Git mutation, deletion or global memory write.

## Cross-cutting reconciliation for MAESTRO

1. Merge the full settled discussion packet into updated S, preserving source/authority and all-page experience. This session updated only notes/handoff. MathLab ML-1..ML-12 and accepted notes:4034-4046 remain part of the same reconciliation, not displaced by frontend selection.
2. Reconcile S:29-52: retain canonical readers/fold, runtime source validation, missing/evidence-tier distinctions, deterministic changed-bytes-only output and exact recurring Python command/no-child-process budgets. A React type does not validate original bytes.
3. Reconcile S:340-371: coherent reusable components and Chrome-target delivery, shared selection/hash/source/return states, local classic scripts and lazy chunks, <=1 MB uncompressed initial load (including direct deep links), actual measurable labels/contrast/targets/overflow/focus. Default Vite app output or relative paths alone are not proof.
4. Reconcile S:953-965: separate one-time frontend asset compilation from periodic recorded-data rebuild; define schema/asset versions and atomic/coherent publication responsibility; update implementation estimates. Build failure must remain visible. No compiler/Node/package-manager subprocess in the recurring Python builder.
5. Complete or explicitly retain MathLab source/format/identity/association/publication/correspondence gaps before selecting renderer/content adapters. S:1169-1178 needs the full notebook experience and reviewed local notation behavior. Deferred source mapping never started; no .ipynb or full-content coverage inferred.
6. Give later builders short named reference extracts, approved wireframes and component/type/state contracts. Shared components should cover frame/context/breadcrumb/evidence/source/measurement/picker/disclosure/dialog and complete notebook/learning journeys. Specify accessible behavior; add a headless interaction library only for demonstrated need.

## Reference contribution and bounded reads retained

- Existing six operator dashboard references, Tabler Icons, interface-design, Anthropic chart text, both design guides and Awesome Dataviz contributions remain indexed in handoff17/16 and notes:3465-3509. They are curated context, not installations or wholesale themes. Reference-source allowances remain used.
- New reads: official React add-to-existing-page guide; TypeScript handbook introduction; Vite production/library-mode guide; ECharts refreshed README; KaTeX README plus options page; operator CSS catalogue README; Tailwind README plus compatibility page; Bootstrap and Open Props READMEs. URLs/exact rendered sections/jobs/exclusions are in notes:4108 onward and :4145 onward. No arbitrary secondary-page expansion, package/source audit or runtime trial.
- Tailwind contributes utility styling/build-time CSS/native-variable patterns; one site-owned visual vocabulary and React component catalogue keep pages coherent. Ordinary CSS remains viable. Chrome target is settled; later pin/runtime support checks are engineering work, not another Safari preference menu.
- KaTeX supports much, not all, LaTeX; local CSS/fonts, accessible output, explicit unsupported source and long-equation treatment need actual-source review. ECharts contributes chart interactions, not scientific provenance, associations or metric definitions. Optional three.js currently documents CDN fallback, so fully local/offline 3D requires later reconciliation.
- Current S/source opened only in bounded ranges. No screenshot or generated W data opened in LVB18. P predates MathLab. Preserve notes:2100: measure.json:1512162-1512190 is a blocked-CDN fallback record, not established as paired with chromium-phone-model-2d.png.

## Exact next action and approval sequence

**MAESTRO: take this handoff and the updated notes as the final brainstorming packet; begin whole-spec reconciliation, with the best-framework question explicitly included in the later review brief.** No new operator brainstorming menu is pending.

After updated S passes Astra review, a separate Codex agent draws static wireframes of every page and user flow, phone and desktop, for operator review before operator spec approval or any builder starts. Figma is configured but off; confirm account/plan in that later session. The build hold remains until the operator releases it. The framework proof suggested by both advisory readers belongs only in a later authorized build/probe brief, not this closeout.

## Context-save / reflection / delivery

- The context-save workflow is preserved in the authorized notes and this separate handoff. Scope overrides generic skill checkpoint/telemetry/auto-commit destinations; no additional state file, memory/config change or commit was created.
- Reflection: browser compatibility, packaging, styling mechanics, accessible component behavior and scientific authority are separate contracts. Documented framework support and favourable advisory judgement cannot establish actual offline/site behavior or source completeness.
- Delivery status is updated only after a verified MAESTRO transport attempt. File presence alone is not a sent-message receipt. If transport is unavailable, this packet remains ready at the exact paths above and that limitation must be reported.

## BINDING context and interaction rule — survives every successor

Plain language for an architect without ML background; short phone-readable replies; one genuinely unsettled whole-experience question with a recommendation and two/three concrete options when needed. Preserve settled choices and exact source pointers; never invent science/causation or convert advice into authority.

Check available Context at every reply end before asking. Start new pieces only at >=60% left. At <=45%, any Context compacted or MAESTRO gate notice, stop new work, finish the current point, notify the operator and write a SEPARATE designated successor handoff containing topics/decisions/notes pointers, open questions, exact paths, in-flight work, risks and one next point. At <=40%, stop starting work; never approach compaction or put the handoff inside notes. Restate this rule in every handoff/team session. No numerical meter is exposed; never invent a reading. LVB18 closes at operator request, not a claimed threshold.
