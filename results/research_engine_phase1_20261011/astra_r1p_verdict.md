VERDICT: NO-GO

For **closing R1/I1c or authorizing provisioning**. The draft is useful preparation and correctly keeps installation blocked, but it does not yet supply the completed provisioning freeze R1 requires.

`RE/` means `results/research_engine_phase1_20261011/`; `P` below means `RE/intel_provisioning_freeze_v1.md`.

F1. [blocking] **All five R1 bullets have sections, but none is fully discharged.** Evidence: `RE/astra_intel_a1_verdict.md:42–46`; P references below.

| R1 bullet | Coverage | Remaining requirement |
|---|---|---|
| Host/base/effective tree | §1, P:24–35 | Complete host/base/config identities; tar provenance receipt; signature verification; effective-content comparison. |
| Selected packages and closure | §2, P:41–77 | Actual selections, complete dependency edges, exact variants and artifact identities. A procedure for obtaining them is not the completed lock. |
| Interpreter/Python artifacts | §3, P:155–182 | Selected interpreter and Intel wheel, verified lock membership, ABI and native linkage evidence. |
| Paths/inventory/budget | §4, P:186–221 | Accepted path map, complete preinventory, numerical peak-growth and time estimates. |
| Refusal/postinstall/commissioning | §5, P:227–287 | Executable comparisons and refusal controls; finalized commissioning interfaces; later actual Intel receipts. |

**Consequence:** retain I1c as pending. Native commissioning necessarily follows authorized installation; its absence should not be confused with the missing *preinstallation* freeze.

F2. [high] **The active-source correction is substantiated, but the retained-tar hash lacks the cited raw receipt.** Evidence: `RE/intel_r1_discovery_20261011T0906Z.txt:10–22,51–54` establishes the active source and three resolved recipe locations. `RE/intel_r1_tree_20261011T0907Z.txt:14–29,49–58` records index/Portfile hashes, commit and retained filenames—but no tarball/signature hash output. `RE/intel_r1_tree_script.sh:3` hashes possible tar files directly beneath `tarballs/`, whereas the retained artifact is beneath `tarballs/remote/`. The full tar hash appears in `RE/intel_r1_facts_20261011.md:10` and P:29.

**Consequence:** there are real content pins beyond directory existence, but the effective tree is **not yet verified against the pinned acquisition artifact**. Treat the tar digest as a reported, unverified baseline until its raw hashing receipt is attached. File modification time also does not independently establish acquisition time. P:35’s content comparison and signature verification remain necessary.

F3. [blocking] **The package set has no demonstrated fit within either provisioning limit.** Evidence: P:46,209–221; `RE/phase1_intel_amendment_v1.md:28,32,36`; `RE/intel_r1_discovery_20261011T0906Z.txt:80–81,159–181`.

**Consequence:** I would not admit the source-build route against ≤1 GB peak setup growth and ≤15 minutes: a bootstrap JDK, target JDK, native dependencies, retained downloads and build work make that an implausible planning assumption without contrary measurements. Binary archives could improve feasibility, but the supplied evidence does not establish that they fit either.

Require a numerical, conservative estimate covering compressed/extracted coexistence, installation images, caches, verification extraction, dependencies and retained failures. Define the provisioning clock’s boundaries; staged acquisition must not silently escape accounting. If the estimate exceeds a limit—or cannot bound it—**stop before mutation and return a concrete revised budget/scope proposal to the operator**. Neither spare disk space nor another category’s allowance authorizes borrowing.

Neo4j’s documented 10 GB development storage guideline is not an archive-size measurement and does not alone prove this small pilot impossible. It does require an explicit compatibility disposition. [Neo4j system requirements](https://neo4j.com/docs/operations-manual/current/installation/requirements/)

F4. [high] **Section 5.1 specifies refusal policy, not an executable mechanism that demonstrates refusal before installation.** Evidence: P:33,63–65,161,227–255. The displayed commands print observations; they contain neither expected-value comparisons nor a guarded installation entry point. Exact MacPorts install commands and enforced archive-only/source-only behavior remain unspecified.

**Consequence:** a mismatch would stop installation only if the future provisioner correctly implements the prose. Before dispatch, freeze the exact command sequence, expected manifest, checked exit/parse predicates, writer-coordination mechanism, route enforcement and retained-artifact behavior. Distinguish separately authorized staging/build writes from installation.

Postinstall coverage is broadly appropriate, but **recording hashes is not itself verification**. Compare installed payloads to verified archive/staged-build manifests, explicitly account for generated files, and reject unexpected files, versions, linkage or ports. Source-build outputs need an approved build-to-install identity chain rather than impossible preknowledge of their final hashes.

F5. [high] **Commissioning has useful advance predicates, but its executable coverage remains incomplete.** Evidence: P:261–287.

- C3 correctly requires HTTP status, parsed result and empty errors, plus an unauthenticated negative control.
- C4 covers authenticated Bolt, but its credential mechanism and exact output parser remain unfrozen.
- C5 correctly distinguishes resource observation from enforcement; the workload, ownership oracle and cap controls remain R3 dependencies.
- C6 requires clean shutdown evidence and closed listeners, but the foreground `console` start and separate `stop` command still need proof that they address the same owned instance.
- C7 leaves executable fault controls and receipt shapes to R3.
- C2’s literal `nice -n 10` invocation does not preserve inherited niceness 10 or greater as required. P:276 acknowledges this, but the usable launch path remains unresolved.

**Consequence:** keep these as commissioning requirements, not completed commissioning instructions. Freeze the referenced R3 version/hash and exact commands before dispatch. Include a bounded external stop controller, exact clean-shutdown predicates, independent ownership completeness, and no-resume observations. No native acceptance follows from the table alone.

F6. [note] **The four recommendations are reasonable; technical repinning does not automatically require a new operator decision.** Evidence: P:41–44; `RE/phase1_spec_v5.md:244–246`; `RE/phase1_intel_amendment_v1.md:114–120,139`; `results/compute_storage_brainstorm_20261011T054507Z/decisions_log.md:204–210`.

| Choice | Review disposition |
|---|---|
| Python 3.12.15 port versus 3.12.14 source | Prefer P1 conditionally. Patch-version change needs an explicit reviewed amendment and compatibility proof. |
| Neo4j 2026.09.0 versus 5.26.32 | Prefer N1 to preserve the reviewed application line. N2 needs a substantive compatibility amendment, but does not inherently change operator-approved Community/local/session-only behavior. |
| DuckDB locked 1.5.5 wheel versus 1.5.6 port | Prefer D1. D2 requires amended version/artifact requirements and actual Python-binding proof. |
| Binary archive versus source | Prefer verified A1. A2 needs a separately reviewed complete build plan; no automatic fallback. |

The official archive index currently lists the Python 3.12.15 default-variant Darwin-23/x86_64 archive, supporting investigation of P1/A1; that listing does not verify downloaded bytes or the dependency closure. [MacPorts Python archives](https://packages.macports.org/python312/)

**Consequence:** none of these choices alone necessarily requires operator approval beyond a reviewed amendment. **Changing budgets, hosting, edition, approved behavior or other operator constraints does.** Source-build expense cannot be approved merely as a technical route change.

Neo4j’s transactional HTTP API is deprecated; that is not evidence it is absent. Verify the pinned line’s required endpoint rather than silently substituting Query API. [Neo4j deprecations](https://neo4j.com/docs/operations-manual/current/deprecations/)

F7. [medium] **Overall pending status is honest, but “FROZEN” conflates fixed expectations with verified observations.** Evidence: P:3,18,24–31,52,287.

**Consequence:** the draft does not falsely claim installation or acceptance. Nevertheless, separate **expected pin**, **reported observation**, **verified identity**, and **pending selection**. In particular, P:29’s tar identity needs the provenance qualification in F2. The Neo4j checksum strings are correctly kept pending actual acquisition verification.

Required changes:

R1. Complete one selected, machine-consumable provisioning manifest with exact closure, artifacts, paths and authorization boundaries; preserve unresolved status until then.

R2. Attach raw retained-tar/key/signature receipts and verify effective recipe, PortGroup, patch and supporting-file content against the admitted artifact.

R3. Supply numerical peak-space/time admission evidence. Over-limit or unbounded plans require operator disposition before mutation.

R4. Freeze executable mismatch guards, delivery-route enforcement and postinstall comparisons, including the source-build identity chain if selected.

R5. Bind finalized commissioning commands to the reviewed R3 artifact; resolve priority preservation, credentials, ownership, deadlines and shutdown predicates before dispatch.

**What I checked and did not check**

I read the freeze, builder report, prior R1 verdict, facts, both supplied raw receipts and scripts, relevant v5/amendment provisions, Python lock/receipt and operator decision records. Both supplied SHA-256 values matched before and after review; the lock and v5 hashes also matched. I consulted official Neo4j and MacPorts documentation.

HEAD advanced during review from `71c4ccce…` to `67b6a0b1…`; the branch stayed unchanged, and the two pinned subject files remained byte-identical and matched the latter HEAD.

I did not access Intel, acquire packages, install, run tests, start services, write files or evaluate the excluded workstreams. Host enforcement and native compatibility remain unverified. A higher-priority hook required one graft invocation; it failed before startup because `node` was unavailable. No graft evidence or token-savings result was produced.