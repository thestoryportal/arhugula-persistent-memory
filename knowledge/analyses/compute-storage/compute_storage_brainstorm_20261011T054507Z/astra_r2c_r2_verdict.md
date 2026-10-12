VERDICT: GO-WITH-CONDITIONS

Round-1 **R2 and R3 are fully met at the requirements level**. R1 remains OPEN and blocks affected build dispatch. This verdict grants no dispatch, commissioning or operational acceptance.

Aliases: `B/` = `results/compute_storage_brainstorm_20261011T054507Z/`; `C` = `B/shared_disk_clearance_contract_v1_1.md`; `AR` = `B/astra_r2c_verdict.md`.

F1. [note] **Every F4 omission now has an explicit controlled subcase.** Evidence: `AR:33–43`; the mapping below.

| F4 omission | Required subcase | Evidence |
|---|---|---|
| Concurrent duplicate launch-ID registration | A03a: one durable registration, loser refused, no double dispatch | `C:156` |
| Same-boot/epoch science-clearance expiry | A02a: equality/after-expiry refusal, before-expiry positive control, exclusion retained | `C:157` |
| M3 reboot | A13a: recovery state, old-token refusal, reconciliation before reopening | `C:158` |
| memit loss/remount | A13b: preserved metadata/exclusion; remount and stale evidence cannot clear work | `C:159` |
| Active authority invalidation without pending science | A06a: independent executor behavior and timing evidence without a science trigger | `C:160` |
| Actual coordinator/guard compatibility with unchanged admission | A16a: successful sentinel through each applicable real entrypoint with surviving runtime forms present | `C:163` |

Consequence: the coverage omissions are closed in the specification; their runtime outcomes remain UNRUN.

F2. [note] **A14a/A14b resolve both F5 observations without prohibiting legitimate running-launch children.** Evidence: `AR:45`; `C:146,161–162`. A14a refuses release while any dispatch capability survives, including after launcher death. A14b requires actual delivery/retry attempts after durable terminal release, including stale-clearance reuse, and requires no dispatch. Consequence: neither a pre-release snapshot nor premature release can satisfy the revised predicate.

F3. [note] **The ordinary-science sentinel and negative controls meet round-1 R2.** Evidence: `AR:53`; `C:163–165`. A16a requires actual successful dispatch with Intel disconnected, all other prerequisites satisfied, unchanged gate bytes and no bypass or stubbed verdict. A16b tests R2 refusal; A16c tests existing-admission refusal despite valid R2 clearance. Consequence: blanket refusal cannot masquerade as compatibility, and passing either gate cannot override the other.

F4. [note] **No v1 safety control is weakened by this revision.** Evidence: complete v1→v1.1 diff; `C:20,49–63,85–111,129,146,152`. C1–C10, the other 17 parent cases, and the open-item/finding map are unchanged. The four replaced lines expand the title, acceptance preamble, A14 and C12. New subcases supplement all 18 parent cases. Consequence: no new default-to-proceed, Intel reachability prerequisite for ordinary science, or science-triggered termination of Intel-local work is introduced. Unresolved shared-disk work still withholds clearance; that is the preserved safety condition.

F5. [condition] **R3 is satisfied, while R1 remains correctly OPEN and blocking.** Evidence: `AR:51,55`; `C:7,169–175`. Gate 1 requires the reviewed implementation freeze before affected build dispatch; Gate 2 requires separately authorized commissioning after implementation; Gate 3 requires complete parent-case and subcase evidence before acceptance, promotion or operational reliance. Consequence: accepting this requirements revision cannot satisfy any of those gates or close R2/I1b.

R1. **Retain the outstanding round-1 implementation freeze before affected dispatch.** Complete and review owners, entrypoints, transport/authentication, containment/observations, durability/guard mechanisms, numeric bounds, discriminated schemas/invariants/transitions, repair fencing of old writers/lock holders, and exact profile/interface hashes (`AR:51`; `C:171,175`).

R2. **Satisfied by this revision.** No further requirements-text correction identified; all acceptance cases remain UNRUN.

R3. **Satisfied by this revision.** Preserve the three separate gates and their evidence/authorization requirements.

**What I checked and did not check**

I read both complete contracts, the round-1 verdict and builder report, and inspected the complete diff. HEAD was `48d58e0ce261abce176349e28df5ddd1e7baa634`. Reviewed files matched HEAD; v1 had no change in that commit. Before/after hashes matched:

- v1.1: `25c93f5f584d5a1dfff3b0610b32922a289be6d91449765862de3331334062f1`
- v1: `866ba46246779034b39f64e3071d797e8db8fe17bb433789cfc71eedad3ac22c`

This was static review. I wrote no files and ran no acceptance tests, host inventories, transfers, services, models or commissioning. Implementation feasibility, latency and runtime safety remain UNVERIFIED.

A higher-priority tool instruction caused one graft lookup attempt; it failed because `node` was unavailable and supplied no evidence. Graft savings: none reported.