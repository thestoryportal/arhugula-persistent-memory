# RES1 — phase-1 / adopted R2 v4 scout map
SCOUT only; all implementation, provisioning and host acceptance remain gated. No plan draft.
Aliases (repository-relative): D = `results/research_engine_phase1_20261011`; RE = `results/research_engine_brainstorm_20261011T032049Z`; B = `results/compute_storage_brainstorm_20261011T054507Z`.
Further aliases: S = D/phase1_spec_v5.md; A = D/phase1_intel_amendment_v1.md; V = D/astra_spec_r5_verdict.md; IA = D/astra_intel_a1_verdict.md; P14 = D/astra_r1p14_verdict.md; REC = D/r1n_chain_record_20261011.md; C = RE/astra_r1_verdict.md; R = B/r2_git_drive_redesign_v4.md; AD = B/r2_redesign_operator_adoption.md. Alias:line resolves to exactly that file.
Status separates reviewed textual resolution from UNRUN replacement acceptance; adoption switches nothing on (AD:9–11).

## M1. Authority table

| Concern | Governing record / status | Evidence |
|---|---|---|
| Engine architecture/spec | RE/design.md is approved direction; S is preserved latest spec, NO-GO; R governs prospective route changes, amended brief review still required. | RE/operator_phase1_choices_20261011.md:3; V:2; R:109 |
| Intel host amendment | A conditionally reviewed current host basis; shared-disk clauses superseded by adopted R; not dispatch permission. | IA:1–3; R:109; AD:9–11 |
| Provisioning freeze | D/intel_provisioning_freeze_v2.md is candidate procedure, installation blocked; 5+2 GB replaces A's 5+1. | D/intel_provisioning_freeze_v2.md:3,9–11,23 |
| Provisioning manifest | D/intel_provisioning_manifest_v11.json is latest R1N budget revision, BLOCKED-PREINSTALL-EVIDENCE; no accepted manifest. | D/r1n_report.md:2,6,35–45; D/intel_provisioning_manifest_v11.json:3,17–23,1372–1376; P14:34 |
| R1 chain | DEFECTIVE accepted; observation workflow only; authorization spent, no retry. | P14:1–3,34,42; REC:77–84 |
| Science reservation v1 | Superseded by v2; historical bytes retained. | S:5 |
| Science reservation v2 | Superseded by v3; historical bytes retained. | S:7 |
| Science reservation v3 | Retired as Intel admission/termination authority; local shutdown survives. | A:40,73–80; R:109 |
| Shared-disk clearance | B/shared_disk_clearance_contract_v1_1.md and freeze_v11/schema/profile/checker/inventory dependencies retired as dispatch authority on adoption; R replaces them. | R:103,109; B/shared_disk_clearance_freeze_v11.md:2–4; AD:5,9 |
| Operator engine choices/answers | Community, 5 GB pilot, background/session limits retained; M3 hosting/note-yield shape replaced; six M3 library upgrades grant no Intel install. | RE/operator_phase1_choices_20261011.md:5–13; D/operator_answers_20261011T0518Z.md:3–7; IA:11; A:114; R:109 |
| Operator hardware/package/budget rulings | Current Intel placement/MacPorts, 2 GB setup and 7 GB combined; earlier 6 GB superseded. | B/integration_r5_completion_table.md:95; B/decisions_log.md:204–210,222–228; R:75,99 |
| Operator R1 authorizations | D/operator_ruling_r1_bind_20261011.md historical single-use; R1M and R1N spent; any next chain needs corrected checks, review and NEW authorization. | D/operator_ruling_r1_bind_20261011.md:5–7; D/operator_authorization_r1n_20261011T1637Z.md:9; P14:40–42; REC:78 |
| Operator route adoption | AD is current adoption authority, overrides R's pre-adoption status; separate activation go and three answers still due. | R:3; AD:3–11 |

## M2. Open conditions

Latest R1 verdict determination: parsed round numbers 1–14 numerically (unnumbered r1p = 1), then checked commit history: r13/addendum 062ce38a precedes A–E commits cfc83e4f → 7ccf0778; r14 packet ba099289 → verdict/disposition 13d9477d (17:00:26Z), followed by retrospective attestation 3af5ee77 (17:01:54Z). Source cross-checks: D/operator_authorization_r1n_20261011T1637Z.md:3; P14:32,48; REC:77–84. Thus P14, not lexical filename order or r13's conditional GO, governs.
Each OPEN row has no qualifying closure receipt in these records; CLOSED rows cite the specific closing evidence. Historical resolved U IDs are included to prevent reopening them (IA:36).

| ID / condition | Source | State / closing evidence |
|---|---|---|
| T2 local shutdown / transfer-owner remainder | IA:36; A:160 | OPEN; relocation is requirement replacement only. |
| T3 elapsed-limit / transfer-deadline remainder | IA:36; A:161 | OPEN. |
| T4 release/restoration remainder | IA:36; A:162 | OPEN. |
| U1 orphan escalation defect | V:8 | CLOSED historically: V:8; Intel completeness remains V3. |
| U2 post-publication inventory defect | V:10 | CLOSED historically: V:10; replacement acceptance open. |
| U3 incomplete release lifecycle | V:12,35–41 | OPEN; maps to V2. |
| U4 circular handshake defect | V:14 | CLOSED historically: V:14; replacement coverage remains V1/V3. |
| U5 deadline/terminal-path gap | V:16,51–55 | OPEN; maps to V4. |
| U6 unusable-root/restoration gap | V:18,57–61 | OPEN; maps to V5. |
| U7 clean hash-lock parse defect | V:20 | CLOSED historically: V:20; Intel artifact/platform pin still open (A:172). |
| U8 identity/mutation-fault gaps | V:22,75–81 | OPEN; maps to V2/V8. |
| V1 failure-triggered termination | V:26–33 | OPEN Intel enforcement remainder (A:174). |
| V2 registration/completion/cancellation/release | V:35–41 | OPEN replacement disposition/acceptance (A:175). |
| V3 complete ownership and consistent invocations/helpers | V:43–49 | OPEN (A:176). |
| V4 invocation-to-return, blocked output/descendants | V:51–55 | OPEN local stop proof (A:177). |
| V5 restored-authority stale clearance | V:57–61 | OPEN replacement disposition/acceptance (A:178). |
| V6 brief-text false positives | V:63–67 | OPEN replacement disposition (A:179). |
| V7 omitted no-resume rule | V:69–73 | OPEN Intel behavior; textual omission CLOSED: A:86 and IA:13–20. |
| V8 failed creation/rename/durability, invalid inventories | V:75–81 | OPEN replacement disposition/acceptance (A:181). |
| SF89 concrete CLI/receipt/key/source/scope/D-ID freeze | V:89; S:31,73–75 | OPEN. |
| SF93 real-process commissioning before promote | V:93; A:80 | OPEN; fixtures insufficient. |
| IA-F1 Intel repin / D-RE-1 amendment / I1a-I1c closure | IA:7 | OPEN; conditional design review closes none (IA:3). |
| IA-F5 reconcile discovery candidates, unavailable ports, Python/DuckDB versions and six libraries | IA:22–34 | OPEN; candidate freeze is not accepted pin (D/intel_provisioning_freeze_v2.md:9–11). |
| IA-R1 freeze host/base/tree provenance; complete package/artifact closure; interpreter/hash lock/ABI; paths/preinventory/peak/headroom; mismatch/postinstall/native checks | IA:40–48 | OPEN; P14:34 establishes no provisioning readiness. |
| IA-R2 external dependency version/hash/review/owner/shapes/cases and host acceptance | IA:50 | OPEN replacement contract/brief/host acceptance; adoption only (R:109,116; AD:11). |
| IA-R3 Intel KEY1/BUILD1, recorded amendment, execution/receipt freeze, independent ownership/shutdown/resource/no-resume, MAESTRO/Astra/currency closure | IA:52 | OPEN. |
| P14-R1 complete receipt/scratch census and retrospective budget reconciliation | P14:36 | OPEN; partial correction explicitly leaves other receipts unenumerated (REC:79). |
| P14-R2 contemporaneous reservations/surveys; otherwise label writer/drift unverified | P14:38 | Labels/raw surveys supplied, factual control OPEN: REC:80,84; retrospective operator answer is not reservation. |
| P14-R3 correct/review DRV D1–D8 before reuse, preserve executed version | P14:15–24,40 | OPEN; REC:81 records gaps, not fixes. |
| P14-R4 append correction; preserve outcomes/anchors; spent authority | P14:42 | CLOSED record correction: REC:78–82; future execution remains separately gated. |
| P14-F4 old-state content identity / unpreserved post-E measurements | P14:26 | OPEN empirical claim; overclaim corrected at REC:82, not verified. |
| P14-F7-source_url qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-size_bytes qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-sha256 qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-signature_trust qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-recipe qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-build_closure qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-abi qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-linkage qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-installer_interface qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-compiler qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-sdk qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-tree_content qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-host qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-paths qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-budget qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-payloads qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-review_binding qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-archive_candidates qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| P14-F7-wheel_lock_membership qualification | P14:34; D/r1j_inventory_0_a32411006dc3.json:222906 | OPEN; established=[]; REC:83. |
| C1 independent reviewed five-chain oracle author/packet before importer | C:20 | OPEN Intel key freeze/review (A:153; IA:52). |
| C2 actual two-store + agent binary parity, complete cases/canonicalization | C:22 | OPEN; S:33,41–43,233 are requirements, not execution receipts. |
| C3 exact seeded negatives/dispositions | C:24–35 | OPEN actual production controls (S:43,124–139). |
| C4 immutable paired publication, pinned readers, failures/source mutation | C:37 | OPEN actual publication/rebuild proof (S:44–46,143–155). |
| C5 bounded non-executing agent surface | C:39 | OPEN actual interface/refusal proof (S:47–48,159–172). |
| C6 actors/manager coverage/dispatch-resume authority | C:41 | OPEN descriptive authority controls (S:48,174–185). |
| C7 separate evidence/state/currency/review, compromised-output prohibition | C:43 | OPEN actual round-trip/refusal proof (S:49–51,102–122). |
| C8 lifecycle paths/peak/resources/stop/install scope/no automatic deletion | C:45 | OPEN host accounting/commissioning (IA:40–52; P14:34). |
| C9 frozen packet/RED-GREEN/actual queries/rebuild/resources/MAESTRO/Astra before expansion | C:47 | OPEN; builder GREEN remains PROMOTE_PENDING (S:221–233). |
| I1a forward Intel amendment, all reservation/AC/finding dispositions | B/integration_plan.md:23; B/integration_r5_completion_table.md:95 | OPEN permitting amended brief (R:109). |
| I1b reviewed science-priority dependency replacing shared-disk clearance | B/integration_plan.md:23; B/integration_r5_completion_table.md:96 | OPEN replacement implementation/host proof (R:109,116). |
| I1c Intel/Sonoma repin; M3 six-library grant not transferable | B/integration_plan.md:23; B/integration_r5_completion_table.md:97 | OPEN; R1 observation cannot close it (P14:34). |

## M3. R2 v4 impact

Every M2 ID is mapped below; grouped IDs share the stated disposition. Replacement means assigned requirements, never a closed host condition (R:109,116).
| M2 condition(s) | Disposition / v4 evidence / reason |
|---|---|
| T2; V1 | REPLACED: R:109,22–25 — Intel local stop survives; science-triggered Intel termination retires; M3 source-read-only push yields. |
| T3; U5; V4 | REPLACED: R:23–25,109 — retain bounded Intel operations/stop; commission bounded probe teardown/handoff, not old SR pending deadline. |
| T4; U3; V2 | REPLACED: R:11–17,65–66,109 — remove Intel allowance/release lifecycle; pin sources, reject unavailable acquisition and reconcile interrupted maintenance. No old descendant roster. |
| U1; V3 | PRESERVED: R:109 — independent Intel local ownership/helper/shutdown proof still required; Intel is not a science termination target (A:73,80). |
| U2 | REPLACED: R:17,23–25,109 — historical fix remains resolved; actual no-return-route and push/probe handoff evidence replaces shared-disk clearance. |
| U4 | INAPPLICABLE ON INTEL: old SR handshake/registry remains removed (A:40; R:109); local V1/V3 proof survives. |
| U6; V5 | REPLACED: R:12–13,65–66,78,109 — stale authority cannot grant a memit route; source generations, partial commitments and restoration must remain honest. |
| U7 | PRESERVED: R:99,109 — clean lock history remains resolved; Intel-selected artifact/hash/platform evidence is still needed. |
| U8; V8 | REPLACED: R:12–13,17,25,76,109 — retired SR mutation predicates give way to validated acquisition/capture failures and local unavailable-observation refusal. |
| V6 | INAPPLICABLE ON INTEL: retired SR fixed-string science backstop has no admission role (R:109); M3's unchanged classifier and actual push/helpers still need proof (R:21–25). |
| V7 | PRESERVED: R:109 — local session limits include explicit no automatic resume (A:86–88); continued unended Intel work is allowed. |
| SF89 | PRESERVED: R:109,116 — freeze concrete Intel commands/receipts/key/source/scope/D-ID; replace obsolete R2 interface prerequisite. |
| SF93 | REPLACED: R:17,25,109,116 — actual Intel commissioning plus new boundary/push controls replace SR pending/release commissioning. |
| IA-F1 | REPLACED: R:109 — amend forward under Git/Drive-only acquisition; repin and record supersession, not blanket waiver. |
| IA-F5; IA-R1; I1c | PRESERVED: R:99,109 — MacPorts/native identity/closure/compatibility gates survive; updated 7 GB cap applies (R:75). |
| IA-R2; I1b | REPLACED: R:109,116 — R1 no-route plus M3-local R2/S criteria replaces allowance/pause/real-pair API; reviewed implementation and new host controls remain due. |
| IA-R3 | REPLACED: R:109,116 — retain Intel roles/freeze/ownership/stop/no-resume/closeout, add adopted-route identities and replacement host receipts. |
| P14-R1 | PRESERVED: R:109,116 — historical census defect stays open; redesign cannot retroactively qualify old admission. |
| P14-R2 | PRESERVED: R:109,116 — writer-control/drift evidence gap remains; future Intel work needs reviewed actual reservations/bounds. |
| P14-R3 | PRESERVED: R:109 — corrected checker/review required before any reuse; no old Gate D GO inherited. |
| P14-R4 | PRESERVED: R:116; AD:11 — appended correction stands; outcomes/anchors remain, fresh execution go still needed. |
| P14-F4 | PRESERVED: R:116 — retained historical size/attestation evidence cannot become verified content identity. |
| P14-F7-source_url; P14-F7-size_bytes; P14-F7-sha256; P14-F7-signature_trust; P14-F7-recipe; P14-F7-build_closure; P14-F7-abi; P14-F7-linkage; P14-F7-installer_interface; P14-F7-compiler; P14-F7-sdk; P14-F7-tree_content; P14-F7-host; P14-F7-paths; P14-F7-budget; P14-F7-payloads; P14-F7-review_binding; P14-F7-archive_candidates; P14-F7-wheel_lock_membership | PRESERVED: R:99,109 — all 19 qualification gaps survive; OBSERVATION-ONLY is not provisioned compatibility. |
| C1; C2; C3; C4; C5; C6; C7; C9 | PRESERVED: R:11–13,109 — source authority, five-chain oracle/parity/refusals, paired publication, non-executing agent and reviewer/currency gates survive. |
| C8 | REPLACED: R:75,99,109 — complete Intel-local lifecycle budget/stop proof; original no-deletion and resource duties survive. |
| I1a | REPLACED: R:109 — new permitting forward brief explicitly reconciles all old findings and route/AC changes. |

| v5/amendment requirement spans mentioning hosts/reservation/disk/clearance | Disposition / reason |
|---|---|
| S:23,189–193,199–203,244–246; A:20,90–139 | REPLACED R:12,75,109: frozen Intel-local root/isolation and reviewed x86_64/MacPorts identities; M3 ARM/Homebrew baselines are historical. |
| S:39,84,116,132,143,248; A:22,58 | REPLACED R:11–13,76–81: published Git commit/path/hash capture and exact verified Drive objects; unpublished/missing newest bulk waits, no M3 fallback; phase-1 bulk remains identity-only. |
| S:207–211,245; A:28,34–36,60 | REPLACED R:75,99,109: 5 GB pilot + 2 GB setup = 7 GB Intel-local; retain subcaps/retained-generation peaks/+20 GiB and 80 GB Intel floor. |
| S:53,213; A:29–32,61,71–75 | PRESERVED R:109 for Intel RSS/CPU/niceness/concurrency/time/ownership; INAPPLICABLE ON INTEL only “no concurrent M3 science.” |
| S:53,57,66–68,78,196–197,215,247; A:40–48,52,56,65,76,78–80 | REPLACED R:17,22–25,109: AC17 local proof, AC21 boundary/acquisition failure mapping, fresh commissioning; retire shared SR writer/root/lock/enforcer and old case PASS. |
| A:44–48,71–72,74,76,78,80,88,147,153 | REPLACED R:109: allowance/pause-ack/clearance/remote coordination dependency removed; M3-local maintenance handoff and Git/Drive coverage take its place. |
| S:172,185,217; A:32,73–75,84–88 | PRESERVED R:109: bounded Intel session/request shutdown, identity-safe escalation, durable failure, no services/autostart/schedule/auto-resume; M3 science does not kill Intel. |
| S:211,213,215; A:34,48 | REPLACED R:21–25,33–69: unchanged science gate; M3-local peak reservations/support-writer prevention and bounded capture, never an Intel lock on M3. |
| S:3–7,253–290; A:12,82,157–181 | PRESERVED history, REPLACED prospective obligations R:103,109: annotate all 23 finding IDs and SR cases without reactivating superseded protocols. |
| A:16,114,143–147,183; S:243–247 | REPLACED R:92,99,109; AD:9–11: later host/route approval changes shape; M3 upgrade approval stays M3-only; new reviewed Intel assignments/dispatch needed. |
| S:56,73–80,221–235; A:64,151–153 | PRESERVED R:109,116: full actual-path evidence, independent review, currency-active closeout, retained failures/context handoff; old R2 receipt slots get new host evidence. |
| A:159–181 | REPLACED R:109: retain historical T1/T5/T6/T7/U1/U2/U4/U7 resolutions (IA:36); fifteen replacements need local/route-specific acceptance, not blanket CLOSED. |

## M4. Rewrite plan, PROPOSED

| Item | Proposed briefing instruction / evidence |
|---|---|
| Bases/output | Preserve S and A; reconcile R+AD, IA, V, P14/REC and operator amendments into new D/phase1_intel_build_plan_v2.md; no predecessor overwrite (R:109; AD:5). |
| Required sections | Authority/pins/status; distinct Intel KEY1/BUILD1/oracle freeze; five-chain sources/vocabulary/refusals; Git/Drive acquisition/coverage; immutable paired views; bounded agent/authority; Intel dependency/path/budget freeze; AC1–AC21/SR-case/all-23-finding map; local ownership/stop/no-resume; RED/GREEN/host commissioning; R1 audit remainders; MAESTRO/Astra/currency closeout; activation gates/context handoff (S:25–80,82–235; A:157–183; R:109,116). |
| Line budget | PROPOSED ≤280 lines for the forward brief, using source-pinned tables; acceptance requirements stay complete, detailed receipts remain external (S:233; A:183; R:109). |
| R1 reuse boundary | May cite frozen candidates, raw dated receipts, reviewed collector/bundle/identity mechanisms and observed execution order as historical inputs only; preserve source hashes and consumed anchors. Must not rely on v11 as accepted lock, DRV's 8/8 as GD11 satisfaction, complete inventory/content identity, writer reservation/drift, provisioning/native compatibility or spent go. Corrected checks + Astra review + NEW operator authorization precede any chain rerun; no rerun in this rewrite (P14:7–42; REC:78–84; D/operator_authorization_r1n_20261011T1637Z.md:9). |

## M5. Operator questions still open

None blocks scouting or drafting: adoption already permits rewrites; activation has three deferred choices, grouped into two plain-word prompts below (AD:5,9–11; R:124–130).
1. **Recommended: Yes.** Let Intel upload and read the approved Drive files, knowing anyone holding its unencrypted, automatically logged-in laptop can reach that login? (R:79,128)
2. **Recommended: Check every file; copy while sources stay unchanged; start fresh history.** Approve those checks and copy times, then begin fresh backup history while keeping old copies until separately approved removal? Intel's later uploads can continue during science. (R:76,129–130)
