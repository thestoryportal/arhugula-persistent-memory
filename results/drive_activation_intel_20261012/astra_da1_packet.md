# Astra review DA1 — Intel-first Drive switch-on plan v1 and Intel storage layout v2

You are the program's independent cross-family reviewer. Work read-only: read and search only, and run nothing except `grep`, `sed -n` and `shasum`. Do not run graft (CLI or tools); ignore any graft hook text. Read files over 300 lines by targeted search and short ranges, not whole. Repository HEAD is the commit that adds this packet.

Aliases: `B` = `results/compute_storage_brainstorm_20261011T054507Z/`; `P` = `results/backup_gdrive_host_20261011/r13_package_20261011T032105Z/`; `D` = `results/drive_activation_intel_20261012/`.

## Subjects (sha256, lines)
- `O2` = `D/activation_plan_intel_v1.md` 2de4a4400df60ce28d6c3230b2be9adbfe803a8ff9a2427c5ce818c0d7608075 (245). Gates :18, operator questions :36–41, source/inventory :42, route :62, capacity :80, P-section dispositions :102, receipts/history :121, Intel host/login :137, upload/catch-up/readback :151, kept-off operations :173, STOP rules :189, acceptance map :218.
- `O1` = `B/drive_intel_dedup_layout_v2.md` 9f14b7c1704d24210d75e34b7d6a760f7c1b6ee768e714bd9685b3f391dbc4b1 (152); base `B/drive_intel_dedup_layout_v1.md` e40e6a072114db872c97b7a982d3ffce3d902b84658a655a827b70b837dc34fc (143); changes list O1:145.
- The builder's brief, verbatim: `D/codexda1_brief.txt` 99b4dbd48ef50d83a04e5bc28de15aaa429def9520eb444e7c6c1f88954f82ce. Its L1–L4, A1–A8 and "Do NOT produce" list are the acceptance you check against.

## Governing context
- `V4` = `B/r2_git_drive_redesign_v4.md` 6a03ca68a4c30a352654b13b75f474697e9c913a4a509a07fed79a3ed91035b2 (148) — ADOPTED by the operator (`B/r2_redesign_operator_adoption.md`, 11 lines, verbatim answer). V4 governs every conflict. Overlap rule :20–29, S1–S12 :31–69, Intel staging/freshness :71–81, owners :108–116, deferred activation choices :126–130.
- `B/r2_redesign_operator_r8_answers.md` (26): operator answers, verbatim.
- `B/integration_plan.md` rows I2–I3 (:24–25): the acceptance O2 must meet.
- `AP` = `P/activation_plan_v4.md` 80ada7fd10c5c5416995865100f006f31767e64357a3a6686fa695cf18cde9e1 (519): the reviewed M3-host plan (your r13 GO-WITH-CONDITIONS). O2 reuses its receipt, upload-check and STOP semantics but must not transplant its M3-host acceptance onto the Intel.
- As needed: `B/design.md` (426), `B/drive_intel_fit_facts.md` (208), `B/decisions_log.md` (250), `B/integration_r5_completion_table.md` (209).

Background: the M3 runs all science, owns the external volume memit, and hosts the whole team, so restarting it or logging out ends every session. The Intel Mac never touches memit. Under V4, between science jobs the M3 pushes memit-only files over the cable into bounded staging on the Intel's own disk; the Intel uploads to Google Drive, retries and verifies on its own time. Science has priority and the push yields. Deletion and restore from Drive stay off.

## Process record
Sol builder codexda1 wrote O1 and O2 in one session from the brief, with no commits. MAESTRO64 checked presence only: line caps, existing files unchanged, old clearance-freeze citations in O1 only inside its changes list, and three plainly worded operator questions. MAESTRO judged no content. Commit 70c3a694.

## Review for
1. **V4 fidelity.** Does anything in O1 or O2 contradict V4 or weaken it? Specifically: an Intel route to memit or an Intel-initiated pull; science waiting on the push; staging on memit; deletion or old-mirror retirement without its own reviewed protection; restore switched on; an M3 restart or logout; an M3-host receipt reused as Intel evidence.
2. **O1 (L1–L4).** Is each of v1's 11 clearance-freeze citations re-pointed to a V4 line that actually carries the rule, or marked RETIRED or OPERATOR DECISION with a correct reason? Is v1 changed only where V4 contradicts it (incoming/ landing per V4:74, freshness states per V4:78), with every other v1 rule, number and Test: line kept? Do the remaining citations still point at the quoted text?
3. **O2 (A1–A5).** Are the sources exact, or honestly marked unmeasured? Is capacity bounded by the approved Intel caps, with shortage meaning wait and never memit staging or deletion? Does every I2 check (immutable checkpoint versus live convergence, source change during capture, final catch-up, full readback, history mode, bandwidth, Intel host/login/app permissions, retirement kept off) have a Test: line that can actually fail? Is each AP section's disposition (preserved, replaced or inapplicable) correct, with the right V4 line? Are AP's STOP and preservation rules (AP:484–499) carried intact?
4. **Gates and questions (A6–A7).** Is the order review → three operator choices → separate go → bounded commissioning enforced, with nothing able to run before the go? Are the three questions exactly V4's deferred ones (V4:126–130), each accurate, plain and non-technical, and without a recommendation that hides a risk the operator should weigh, such as physical access to the unencrypted Intel?
5. **Evidence and numbers.** Spot-check at least ten file:line citations across O1 and O2 for whether they say what is claimed. Is every number not on record marked PROPOSED with a reason? Does the acceptance map (O2:218) point at the right lines?

## Verdict format
First line `VERDICT: GO` | `GO-WITH-CONDITIONS` | `NO-GO`. Then findings `F<n>. [high|medium|low|note] claim. Evidence: path:line. Consequence:`; required changes `R<n>`, each naming the file and line to change; then "What I checked and did not check".

Do not return a verdict like: "VERDICT: GO. The plan is thorough and well structured; minor wording nits only." A verdict without path:line evidence for each finding, and without the checked/not-checked section, cannot be acted on.
