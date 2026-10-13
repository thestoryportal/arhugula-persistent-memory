# MAESTRO decision for R2 round 6: science invocations are observed, not sandboxed (MAESTRO49, 2026-10-11 ~15:55Z)

Trigger: codexr2n replied `R2N BLOCKED tools/run_c10w_p2_stage.sh — F3:115,120 requires a reviewed science SandboxProfile/native policy pin`. F3 makes `InvocationProfile.sandbox_profile_sha256` required for every invocation, science included, and no science sandbox policy exists. So every science launch path became not admitted.

Evidence: the contract never mentions a sandbox. C9 (B/shared_disk_clearance_contract_v1_1.md:115–119) requires every invocation's executable, exact argument structure, identity and capability scope to be enumerated, registered and independently observed, and it leaves capability containment as an OPEN runtime-profile item. The clearance design protects science I/O from support copies; science is the protected party, not the restricted one.

Decision: SCIENCE launch profiles use their own invocation type with no sandbox field. Everything else is unchanged; executor, Intel, observer and recovery invocations keep a required sandbox hash.
- `ScienceInvocationProfile`: executable_path, executable_sha256, argv, environment, dependencies (as InvocationProfile after round-6 changes a–c), plus required `shared_disk_access`: an array (0–64) of `{"path": Path, "mode": "READ" | "WRITE"}`, the declared capability scope C9 asks for. No sandbox_profile_sha256 field at all (absent, not null). additionalProperties false.
- `ScienceChildProfile`: as ChildProfile, but `invocation` is a ScienceInvocationProfile.
- The LaunchProfile SCIENCE variant uses ScienceInvocationProfile for invocation, existing_admission and authorized_payload, and ScienceChildProfile for children. The RECOVERY variant and every other profile keep InvocationProfile and ChildProfile.
- Enforcement of `shared_disk_access` is by C9 registration and independent observation; F4 says so plainly and claims no native containment for science.

Astra reviews this decision in round 6 like any other freeze change.
