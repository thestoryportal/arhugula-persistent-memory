VERDICT: GO-WITH-CONDITIONS

The Intel-first direction is consistent with V4. Resolve R1–R4 before treating this packet as permitting commissioning; operator choices and the separate go remain outstanding. Paths below use your B/P/D aliases.

F1. [medium] **O2 blurs historical host results with still-required host coverage.** Evidence: `D/activation_plan_intel_v1.md:109` calls the r13 counts historical and replaces M3 native acceptance with Intel compatibility/process evidence. But `P/activation_plan_v4.md:44` expressly requires the 22-case run, four local→local fixtures, isolated-config controls, native artifact assertions, and the frozen-suite result. O2’s generic qualification test at :119 does not identify which behavioral requirements survive or receive reviewed replacements. Consequence: the implementation brief could qualify placement and executables while omitting required failure-path coverage.

F2. [medium] **The content-check disposition omits AP’s explicit runtime-configuration preflight.** Evidence: `P/activation_plan_v4.md:335` requires successful status/preflight and rejection of inherited behavior-changing `RCLONE_*` and config overrides. `D/activation_plan_intel_v1.md:113,139,163,169` preserves source identity, filters and report checks but does not expressly preserve that rejection or test it. Consequence: the plan leaves ambiguous whether reviewed command arguments are sufficient when inherited settings alter execution.

F3. [medium] **The capacity boundary test has the wrong direction for a usage ceiling.** Evidence: `D/activation_plan_intel_v1.md:98` says “just-below-cap/free/reservation bounds … refuse,” while :86 permits `U+M+T ≤250 GB`. `B/r2_git_drive_redesign_v4.md:39,42` distinguishes insufficient free space from equality satisfying the relevant criterion. Consequence: this Test line conflates maximum usage with minimum available space and could accept an always-refusing implementation.

F4. [low] **O1’s rewrite drops two explicit v1 safeguards without a V4 conflict requiring their removal.** Evidence: `B/drive_intel_dedup_layout_v1.md:58` requires an **exclusive incoming part**; v2 :58 retains non-overwriting object publication but omits incoming-part exclusivity. V1 :116 explicitly retains **baseline/inertness gates**; v2 :116 says only “baseline gates,” although `B/design.md:190` still names both. `D/codexda1_brief.txt:24` requires every unaffected rule to remain. Consequence: L2 preservation is incomplete even though broader preservation language remains.

F5. [note] **The principal V4 boundaries and operator questions are preserved.** Evidence: `D/activation_plan_intel_v1.md:64–78,149,181–183` requires M3-originated capture, no Intel return route, science-priority interruption, and separately protected retirement/restoration. Its :18–34 gates review → choices → separate go → commissioning. Questions :38–40 match `B/r2_git_drive_redesign_v4.md:128–130` and explicitly disclose unencrypted automatic-login exposure. Consequence: no architecture reversal or additional operator question is needed.

F6. [note] **AP’s ten STOP classes and preservation rule are substantively carried forward.** Evidence: `D/activation_plan_intel_v1.md:191–208` maps `P/activation_plan_v4.md:486–497`; O2 :28–30 retains point-of-effect permissions from AP :499. Consequence: this review supplies no permission to upload, repair history, retire copies or restore into memit.

Required changes:

- **R1 — `D/activation_plan_intel_v1.md:109,119`:** Separate historical receipts from mandatory coverage. Preserve AP :44–46’s behavioral requirements, or require an explicit reviewed replacement for each affected case, including expected results, permitted skips and descendant clearance. Intel receipts must satisfy that matrix before upload.
- **R2 — `D/activation_plan_intel_v1.md:113,163,169`:** Explicitly preserve successful pinned status/preflight and rejection of inherited behavior-changing environment/config overrides. Add a failure control demonstrating rejection before transfer/check consumption.
- **R3 — `D/activation_plan_intel_v1.md:98`:** State separate boundaries: usage above a ceiling refuses; available space below the required floor/reservation refuses; equality satisfies that individual criterion with other gates met. Include an admissible positive control.
- **R4 — `B/drive_intel_dedup_layout_v2.md:58,116`:** Restore exclusive incoming-part creation and the explicit applicable baseline/inertness requirement. Update the changes list and affected O2 acceptance-map line references after editing.

**What I checked and did not check**

Checked all six supplied SHA-256 values at entry and exit: every value matched. O1 ends at 152 lines; O2 at 245, within their caps.

Read both layouts, O2, the brief, adopted V4, adoption/answers, I2/I3 and AP’s sections. All eleven old-freeze citation locations—v1 :64,68–73,75,100,131,137—have replacement/disposition text. No old-freeze citation remains outside O1’s changes list. The obsolete allowance/contained-clearance mechanisms are retired rather than presented as implemented safeguards.

Citation spot-checks included:

| Subject citation | Opened supporting evidence | Result |
|---|---|---|
| O1 :9 — protected recovery separation | `B/design.md:183,206` | Supported |
| O1 :28 — historical symlinks | `B/drive_intel_fit_facts.md:14` | Supported |
| O1 :49 — inventory correction needed | `B/drive_intel_fit_facts.md:21,205` | Supported |
| O1 :91–94 — payload/dedup arithmetic | `B/drive_intel_fit_facts.md:14,105–106,168` | Supported |
| O1 :104 — amended history obligation | `B/decisions_log.md:101,191`; V4 :91,111 | Supported |
| O1 :139 — later I3b location | `B/integration_plan.md:89`; `B/integration_r5_completion_table.md:101` | Supported |
| O2 :38 — physical-access exposure | `B/decisions_log.md:197,216` | Supported |
| O2 :44 — Intel-first choice | `B/design.md:273` | Supported |
| O2 :52 — parked-set overlap | `B/drive_intel_fit_facts.md:117–132` | Supported |
| O2 :82 — Intel caps | `B/decisions_log.md:191,222–228` | Supported |
| O2 :94 — bandwidth/history distinction | `P/activation_plan_v4.md:273,383` | Supported |
| O2 :127 — recovery barrier formula | `P/activation_plan_v4.md:239` | Supported |
| O2 :131 — completion-end freshness | `P/activation_plan_v4.md:299` | Supported |
| O2 :175 — scheduled settings | `P/activation_plan_v4.md:412–427` | Supported |

The remaining reviewed numbers are recorded values, labelled historical estimates, or proposed accounting expressions. Current population, allocation overhead, capacity and throughput are honestly unmeasured. The acceptance map points to the intended sections; its presence does not resolve F1–F4.

I did not verify HEAD/commit ancestry, the builder’s entire modification scope, current inventories, host enforcement, credentials, filesystem behavior or Drive contents. No tests, commissioning, transfers, edits or context-save writes were performed. Memory was used for orientation; current packet evidence governed.

Tool exception: a higher-priority hook forced one graft attempt despite your restriction; it failed with `node` unavailable and returned no results. Graft: one failed call; token savings unavailable.

