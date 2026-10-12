# R2C report — draft ready for Astra, host acceptance OPEN

Aliases: `B/` and `RE/` have the brief's meanings; `C` = `B/shared_disk_clearance_contract_v1.md`; `IM` = `B/integration_r5_completion_table.md`.
Drafted C1–C12: parties, M3-local allowance authority, ordering, verified pause, bounded refusal, release/resume, restoration, ownership, disk budgets, future acceptance and finding coverage (`C:7–177`).
Selected proposal: one M3 authority/lock and one active resumable unit; all shared-disk I/O crosses a registered M3 executor. Ordinary science needs no Intel reachability; Intel-local work continues (`C:20–26,53–71`).
Learning preserved in the draft: snapshots/zero matches are insufficient, registration precedes capability release, and a deadline must include output and descendants (`RE/astra_spec_r3_verdict.md:18–24`; `RE/astra_spec_r4_verdict.md:26–41`; `RE/astra_spec_r5_verdict.md:35–61`; `C:53–117`).

## Static receipt and scope

Local document-check output: PASS; 12 clauses; 15 R2 replacement findings plus 3 historical lessons; A01–A18 present; 110 citation occurrences resolve within source line ranges. This checks structure/ranges, not runtime behavior (`C:125–177`).
Contract SHA-256: `866ba46246779034b39f64e3071d797e8db8fe17bb433789cfc71eedad3ac22c`.
Only the two requested deliverables were deliberately written. No code edits, commits, builds, installs, host/fixture acceptance tests, Intel access, services, transfers, models or tmux operations were performed.
Tool side-effect disclosure: the required graft lookup reported “refreshed the graph (1 file changed)”; graph state was not independently audited. Its results supplied no contract evidence. Graft reported ~68,857 tokens saved, one successful lookup.
Tracked diff still lists unrelated `tools/test_dashboard_mathlab.py`; it was left untouched. No extra context-save/memory artifact was written; this report preserves continuation within the two-file scope.
All ten authority/gate inputs below had identical before/after SHA-256 observations; the unchanged gate hash is included explicitly.

| Input | SHA-256 before = after |
|---|---|
| B/design.md | `20f88e7c50acff3e0061dd9c6dee0e70e68627a197e5921e9acb344a075717b1` |
| B/astra_r1_verdict.md | `ef273bede821f9d82b828dccb8728db5ccca8fc893db70664359c3eb335ad26f` |
| IM | `8f43668d555d02e553e5513ecb1ba3428dd31b1631a0d7d393a7a4012ff4fd81` |
| B/decisions_log.md | `d8dda823e63ceb4297dbfda5897cf689b394aded5a096b5b468a809ef2c0db03` |
| RE/phase1_intel_amendment_v1.md | `e6b0199782b6155a4d4813399b449796e00a007f6059746eb0122af1780a99a0` |
| RE/astra_intel_a1_verdict.md | `20a4a6d2226a833ad9266eeb5fea6f227cfec6a582434db68c134dc3c3d490a0` |
| tools/c10w_p2_gate.py | `fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26` |
| RE/astra_spec_r3_verdict.md | `d8b7e404668595ae7fe057e511c6ba15bbb6fd046ba2a73afe2c42309c416d71` |
| RE/astra_spec_r4_verdict.md | `006d3b78b95b7165a784a2af4f77398964b18355937725050938f688279f2289` |
| RE/astra_spec_r5_verdict.md | `9fb5c4376111a87bbb9002b7e0616d8a6c4d0a614f91d8f8a499b054ba11e4cb` |

## Every R2 replacement finding: requirement coverage, not resolved implementation

| Finding/source | Clause meeting the class; open proof |
|---|---|
| T2 (IM:172) | C2–C3,C5–C6,C8–C9; coordinator loss/descendants; containment/timing OPEN. |
| T3 (IM:173) | C6; single monotonic origin/refusal; numeric latency and host proof OPEN. |
| T4 (IM:174) | C3–C4,C7–C8; serialized identity/durability/release; primitives OPEN. |
| U3 (IM:180) | C4,C7; complete launch/cancellation/capability closure; invocation proof OPEN. |
| U5 (IM:182) | C6; whole-operation deadline; bounded output/child handling OPEN. |
| U6 (IM:183) | C3,C5,C8; authority off memit/no exception clearance; runtime availability OPEN. |
| U8 (IM:185) | C3,C11; validated grammar and creation/rename/durability controls; wire freeze OPEN. |
| V1 (IM:186) | C2,C5–C6,C8; no new unit, verified close or halt uncleared; executor proof OPEN. |
| V2 (IM:187) | C3–C4,C7; registered pending/running/terminal lifecycle; exact launch freeze OPEN. |
| V3 (IM:188) | C2,C9; independent descendant/endpoint accounting; no-bypass proof OPEN. |
| V4 (IM:189) | C6,C8; blocked output and late-mutation fencing; concrete bounds OPEN. |
| V5 (IM:190) | C3,C7–C8; epoch/nonces/persistent exclusion through repair; host proof OPEN. |
| V6 (IM:191) | C7,C9; unchanged gate, structured identity and brief negative control; argv proof OPEN. |
| V7 (IM:192) | C7–C8; explicit MAESTRO review plus fresh allowance, no automatic resume; host proof OPEN. |
| V8 (IM:193) | C3,C5,C9,C11; pre-create failure and validated absence; fault receipts OPEN. |
Historical T1/U2/T5 lessons are also mapped without reopening them (`IM:171,175,179`; `C:150–177`).

## Open questions and continuation

MAESTRO must name implementers/worker owners; freeze actual transfer/launch/helper interfaces and no-bypass closure proof; freeze numeric latency/lifetimes, authentication/wire/receipt shapes, runtime paths/permissions/metadata budget/durability and cancellation mechanisms (`C:150–156`; `IM:205`).
Next: Astra reviews this exact contract hash, then MAESTRO scopes those freezes and real-pair A01–A18 commissioning. R2/I1b stays OPEN; no RE fixture or this draft permits affected dispatch (`RE/astra_intel_a1_verdict.md:9,50`; `C:125–156`).
Context directive for every successor/team session: start a new piece only at ≥60% context left; at ≤40% or any compaction stop new work, preserve completed/in-flight work, exact paths, next step and risks in this report, and reply R2C HANDOFF. Current deliverables are the two B/ files; no R2 job was launched. Open risks are the C12 freezes and all host acceptance, not a scientific finding.
