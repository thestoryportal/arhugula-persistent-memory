# MAESTRO decisions for R2 round 8 (MAESTRO53, 2026-10-11 ~18:00Z)

Trigger: Astra round 7 says NO-GO (`astra_r2j_verdict.md`, V7). Its required changes R1–R6 are at :63–75. The options analysis is `r2_round8_options.md` (O8). MAESTRO53 reran its Mac checks: `csrutil status` gives "enabled", `sw_vers` gives 26.6.2 / 25G83, and `ls -lO` shows `restricted` on `/bin/bash` and `/usr/bin/git`. Its quotes of C at :87, :89, :115 and :117 are verbatim.

This file is an addendum. It does not edit C (`shared_disk_clearance_contract_v1_1.md`), DR (`r2_round7_decisions.md`), DS or DC. Where it contradicts DR, this file governs. Astra judges A1 and D4–D6 in round 8 as freeze changes; A1 is the operator's own ruling, so Astra checks only that the freeze applies it faithfully and no more widely.

## A1 (answers R1): operator-approved narrow amendment to C:87 and C:115 — Decision-ID D-R2C-A1

**Operator ruling, 2026-10-11 ~17:58Z.** MAESTRO asked, in AskUserQuestion: "The drive-sharing rules say every program must be registered BEFORE it is allowed to start. Our science program starts small helper programs of its own (a file check, a git lookup), and on this Mac there's no proven way to register those before they start without changing the science code or the Mac's protected tools. How should we handle that rule?" The operator chose **"Narrow change (Recommended)"**. The option read: "The main science program is still checked and registered before it starts. Its own helper programs are listed in advance and tracked as they appear, not registered one by one beforehand. Anything unexpected stays flagged and the drive stays locked. The written rule says plainly that a surprise helper could run briefly before it's caught. Science code stays untouched." This is the explicit, separately approved relaxation that V7 R1 requires. It corresponds to O8 option 1C.

**Amended text.** The following applies in place of C:87's "Every dispatch-capable science helper is registered before release to run" and C:115's pre-release registration and "failed registration must leave no released I/O child", for science descendants only:

1. A **science root** keeps C:115 in full. Before release it must be registered with its exact executable and argv structure, PID plus start identity, parent/group identity and capability scope. If that registration fails, it is not released.
2. A **science descendant** is any process whose ancestry leads to a registered science root through that root's declared recipes (entrypoint, variant, argv template, bindings and dependency identities, as DR D3 declared them). A science descendant may be released before its own process identity is registered. Its recipe must be declared in the root's admission record before the root is released.
3. Each observed science descendant is bound to its root's launch by exact recipe match and recorded with its identities after the fact. A descendant that matches no declared recipe, and any observation gap, loss or uncertainty, marks the launch `UNRESOLVED`. Exclusion stays in place and the launch gets no terminal release (C:89).
4. The record must say plainly that an unexpected science descendant **may already have executed** before it was detected. Detection after release is never presented as prevention.
5. Not amended: C:85 (the gate stays unchanged), C:89 (release conditions; unknown means `UNRESOLVED` with exclusion kept), C:91 (no automatic resume), C:117 (independent accounting of the whole population, including orphaned and untagged helpers), and pre-release registration for every non-science helper (transfer, I/O, network, capture, verification, stop, admission and broker processes).

**Consequence for this round.** A1 needs an independent, gap-detecting observation of the descendant population that satisfies C:117. O8 shows that no such mechanism is established on this Mac yet. Kqueue gives notification, not a latch, and snapshots miss short-lived processes (O8, 1C). So the freeze must specify one and state its known gaps (D4). Until Gate 2 proves it on hardware, no science root that has descendants gets positive R2 clearance. The O8 1A refusal holds in the meantime. Gate 1 stays OPEN until Astra says GO.

## D4 (replaces DR D3): recipe declaration under A1, plus a specified observation mechanism

DR D3's declared-tree registration survives as the recipe declaration in A1 item 2. DR D3's claim that this "satisfies C:115" is withdrawn (V7 F1). The label `DECLARED_AT_ROOT_ADMISSION` stays, but the freeze must cite A1 as its authority, not C:115. The freeze must name the observation mechanism for science descendants. For it, the freeze states:
- the native facility and its documented basis (e.g. kqueue `EVFILT_PROC` with `NOTE_FORK`/`NOTE_EXEC`/`NOTE_EXIT` on each tracked process, plus libproc/sysctl snapshots);
- each known gap: short-lived children, reparented orphans, missed events, observer restart;
- for each gap, how it is detected, and that every gap leads to `UNRESOLVED` with no terminal release (A1 item 3).

Proving the mechanism on hardware is Gate 2 work. The freeze must not claim it is proven.

## D5 (answers R2): a sandboxed guard plus a separate science launch broker (O8 option 2A)

- `science-guard` stays the owner of SCIENCE `/invocation` (DR D2). Its invocation becomes an ordinary InvocationProfile carrying the GUARD SandboxProfile, so the type no longer conflicts with the GUARD Process's required sandbox (V7 F2). The guard keeps `exec_paths=[]` and `deny_fork_exec=true`. It consumes clearance, commits `RUNNING` and then delegates; it never spawns.
- A new Process role, `SCIENCE_LAUNCH_BROKER`, with its own invocation type, is the only component that spawns admission and payload. It is unsandboxed and named as an explicit exemption from F5:70's all-ordinary-roles sandbox rule. It is never disguised as SCIENCE_PAYLOAD, and transfer brokers get no exemption from it. Its capability is limited to spawning the exact admission and payload of one delegated launch. It has no authority write and no bulk write.
- The broker is provisioned and registered (C:115 in full) from a parent without the guard's restrictions, before any delegation; sandbox inheritance (O8, `sandbox(7)`) rules out spawning it from the guard. Delegation is authenticated, single-use and bound to one launch context (D6). The broker creates the admission process suspended (`POSIX_SPAWN_START_SUSPENDED`), registers it, releases it and waits for success. Only then does it do the same for the payload root, under the same launch and nonce. A failed admission keeps exclusion until explicit cancellation (C:87–89). A missing or failed broker means refusal.
- Why 2A over 2B: the component that consumes clearance keeps its containment, and spawn power sits in one narrowly scoped role. No C amendment is needed (O8, Fork 2).

## D6 (answers R3–R6): construction directions for the builder

- **R3 / V7 F3.** Direct P2 evaluation and direct trainer routes that can select a P2 certificate become CHILD_ONLY under the coordinator chain, or are refused with `NOT_ADMITTED_NO_PROFILE:`. A TOP_LEVEL profile keeps a `/usr/bin/true` admission only where a cited source line shows that no outer admission obligation exists in any launch chain that reaches it. Correct the inventory's "P2 has no admitted root route" claim (I4:157–163, :259).
- **R4 / V7 F4.** Raise the admission ActionReceipt `input_receipts` maxItems from 32 to 64. That covers the largest production need (profile 46 needs 35) with stated headroom; also check any byte-size bound. The checker builds the actual admission receipt for every TOP_LEVEL production profile and validates it against the frozen bounds.
- **R5 / V7 F5.** Refusal variants become structured, with a variant name and required operand slots giving count and kind. Matching uses real argv including operands. Parent argv declarations get their required operands. Tests use invocations taken from cited source lines (e.g. `tools/run_c10w_p2.sh:9–17`, `tools/run_c10w_p2_stage.sh:11–13`).
- **R6 / V7 F6.** Every binding in one production tree (guard, broker, admission, payload, descendants) references one launch context. The checker enforces this, and an isolated cross-context substitution control is RED.
