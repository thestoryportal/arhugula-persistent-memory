# R2D revision report

Aliases: B = results/compute_storage_brainstorm_20261011T054507Z; V1 = B/shared_disk_clearance_contract_v1.md; V1.1 = B/shared_disk_clearance_contract_v1_1.md; AR = B/astra_r2c_verdict.md. Numbers below are file line numbers.
Status: requirements revision ready for review only; R1 OPEN/blocking and all real-pair cases UNRUN (V1.1:3,7,129,152,171–175; AR:3,51–55).

| Change | v1 lines | v1.1 lines | Astra item answered |
|---|---|---|---|
| Version title and revision-source/scope note; inherited schema unchanged, R1 remains OPEN | 1,5,36,45,117,154 | 1,7 | R2/R3 scope; R1 explicitly deferred (AR:51–55) |
| C11 extends UNRUN/preregistration to subcases and connects commissioning to the separate gates | 127 | 129,152 | R2/R3, F4/F6 (AR:33,47,53,55) |
| A14 preserves every original action and requires both release refusal and failed post-release delivery/retry; legitimate running child permitted | 85–87,144 | 146 | R2/F5 (AR:45,53) |
| A03a concurrent duplicate launch-ID registration | 55,133 | 156 | R2/F4 omission 1 (AR:37,53) |
| A02a science-clearance expiry on unchanged boot/epoch, including equality boundary and positive control | 75,85,100,132 | 157 | R2/F4 omission 2 (AR:38,53) |
| A13a M3 reboot with old grants/clearances and unresolved work | 51,85,106,143 | 158 | R2/F4 omission 3, reboot (AR:39,53) |
| A13b memit loss/remount, preserved exclusion and refusal of stale evidence | 104,109,143 | 159 | R2/F4 omission 3, mount (AR:39,53) |
| A06a authority invalidation during active unit without pending science; independent executor evidence | 47,79,98,105–106,136 | 160 | R2/F4 omission 4, V1 (AR:24,40,53) |
| A14a explicit surviving-capability refusal; legitimate running-child control | 85–87,144 | 161 | R2/F5 observation 1 (AR:45,53) |
| A14b actual delayed delivery/retry after durable terminal release | 85–87,144 | 162 | R2/F5 observation 2 (AR:45,53) |
| A16a successful ordinary-science sentinel through each unchanged applicable admission path with real coordinator/guard forms present | 61,83,85,113,127,131,146 | 163 | R2/F4 omission 5 and successful sentinel (AR:41,53) |
| A16b R2 refusal controls and A16c unchanged-admission refusal controls | 69,83,85,87,100,146 | 164–165 | R2 negative controls (AR:53) |
| C12 introductory separation and Gate 1: reviewed implementation freeze before affected build dispatch | 152–154 | 169,171 | R3/F6; R1 remains OPEN (AR:47,51,55) |
| Gate 2: separate bounded real-pair commissioning authorization after implementation | 127,152–154 | 172 | R3/F6 (AR:47,55) |
| Gate 3: complete real-pair evidence before acceptance, promotion or operational reliance | 127,152–156 | 173 | R3/F6, preserve OPEN/UNRUN (AR:3,47,55) |

Static verification: reviewed complete `diff -u V1 V1.1` (exit 1 = differences); no removed control. Only title/scope, C11/A14/subcases and C12 gating changed.
Three `cmp` checks returned 0: C1–C10 (V1:7–124 = V1.1:9–126); O1–O5/full finding map (V1:154–177 = V1.1:175–198); all 17 parent cases other than corrected A14 (V1:131–148 = V1.1:133–150, excluding A14).
Matrix counts: 18 parent cases, 10 named subcases. F7 optional simplifications not applied; every inherited OPEN/UNRUN qualification retained (V1.1:129,175–198).
V1 SHA-256 before/after: 866ba46246779034b39f64e3071d797e8db8fe17bb433789cfc71eedad3ac22c.
AR SHA-256 before/after: 94a2eff894df1df3a2241612bee82248cf6911f251da9820a15fa4b8412b705b.
V1.1 SHA-256: 25c93f5f584d5a1dfff3b0610b32922a289be6d91449765862de3331334062f1.
Scope: started V1.1 as a copy of V1; wrote only the two authorized new Markdown files. Worktree/branch verified; existing concurrent changes preserved. No code, commits, runtime tests, host/process operations or tmux actions.
UNVERIFIED: all implementation, latency, runtime safety, commissioning and host acceptance; this document closes none of those claims (V1.1:3,129,171–175; AR:63).
Session context: revision complete; nothing in flight. Next: MAESTRO reviews this revision; R1 freeze/review remains separately blocking before affected build dispatch (V1.1:7,171).
Context directive survives handoff: start a new step only at >=60% context left; at <=40% or any compaction stop starting work, preserve done/in-flight paths, exact next step and open risks in this report, and reply R2D HANDOFF.
