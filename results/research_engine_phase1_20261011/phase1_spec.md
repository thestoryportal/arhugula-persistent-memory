# Research engine phase 1 — independent answers and build specification

SPEC1 draft: resolve section 13 before freeze/dispatch. Proposed engineering requirements, not existing behavior or F1/science promotion (DISCIPLINE.md:7–18; D:229,239,245).

Citation aliases: **V** = `results/research_engine_brainstorm_20261011T032049Z/astra_r1_verdict.md`; **O** = `results/research_engine_brainstorm_20261011T032049Z/operator_phase1_choices_20261011.md`; **D** = `results/research_engine_brainstorm_20261011T032049Z/design.md`. Alias:line resolves to that exact file. C1–C9 bind this brief (V:20–47); hosting/resource choices are settled (O:5–13).

## 1. In plain words

This build copies five carefully checked examples into two searchable stores: numbers in one, connections in the other. Original files and Git history remain authoritative. Copies cannot rewrite findings or authorize experiments (D:110–121).

The examples cover a limited success, negative result, stopped test, replaced status and mathematical analysis. A separate author derives expected answers from originals; Astra reviews them before building. Both stores and the query tool must match, including refusals (V:20–22; D:233,239).

Answers show sources, limits and missing coverage. History stays visible; math stays distinct from model tests. Stopped output cannot become fresh scientific support or old approval become permission (V:39–43).

Stores publish together. Failed updates retain the age-labelled previous pair; in-flight questions keep their pair. Mixed updates cannot support a combined conclusion (V:37).

This runs on the Mac in the background: Community Neo4j through Homebrew, session-only; <=5 GB memit data, <=2 GB Neo4j memory, no model/GPU or automatic deletion. Next-phase approval requires MAESTRO verification and Astra review (O:5–13; V:45–47).

## 2. Binary acceptance criteria

Future commands only; SPEC1 ran none. With this worktree as cwd, set `P=results/research_engine_phase1_20261011`, `RE_PY=$PWD/.venv-research-engine/bin/python`, `CLI=tools/research_engine/cli.py`. Rerun each named test below using:

`LLMDB_ROOT=$PWD "$RE_PY" -I -B -m unittest discover -s tests/research_engine_phase1 -p '<test file>'`

Full suite uses `-p 'test_*.py'`. End-to-end command: `LLMDB_ROOT=$PWD "$RE_PY" -I -B "$CLI" verify --freeze "$P/freeze.json" --receipt <fresh-directory>`. Required administrative CLI operations are `preflight`, `capture`, `build`, `publish`, `verify`, `session-start`, `session-stop`; all take the frozen configuration and fresh receipt directory. Query agents cannot invoke them. Their detailed parameters/receipt shapes must be frozen with tests before implementation.

Codes: 0 success; 2 rejected/refused input; 3 explicitly incomplete answer; 4 dependency/observation unavailable; 5 resource/stop interruption; 1 unexpected defect. Expected refusals pass only with their frozen code/reason. Any missing case, mismatch, skip, expected-failure marker, missing diagnostic or skipped backend blocks engineering acceptance; unavailable dependencies mean UNVERIFIED (V:22). `acceptance.json` enumerates every AC/question/control and receipt. Builder verification can report `ENGINEERING_GREEN/PROMOTE_PENDING`; reviewer receipts remain required for promotion.

| AC | Binary requirement | Rerun test file |
|---|---|---|
| AC1 | Distinct KEY1/BUILD1, permitting Astra key review and exact freeze hashes exist before importer development; changed/unreviewed key blocks dispatch. | `test_freeze.py` |
| AC2 | Observed versions match lock; isolated imports and write allowlist pass. | `test_environment.py` |
| AC3 | Admitted hashes/locations resolve; mutation rejects capture; commit/dirty attribution is accurate. | `test_capture.py` |
| AC4 | Required slots, original labels and seven statuses round-trip through JSON and both stores; invalid shapes reject. | `test_vocabulary.py` |
| AC5 | Every oracle query/refusal matches actual DuckDB, Neo4j and agent responses; shared projections agree; zero omitted IDs. | `test_oracle_queries.py` |
| AC6 | Section-5 ordering/null/duplicate/numeric/comparison boundary cases match frozen expectations. | `test_canonicalization.py` |
| AC7 | Every section-6 subcase yields exact disposition/diagnostic on production paths; silent drops/extra conclusions fail. | `test_negative_controls.py` |
| AC8 | One-store/publication/capture failures preserve old pair and immutable manifests, with durable diagnostics. | `test_publication_failures.py` |
| AC9 | G1 request remains pinned through G2 publication; new request selects G2; loss/mismatch returns incomplete; age shown. | `test_pinned_requests.py` |
| AC10 | Fresh identical-input builds reproduce canonical digests and actual two-store answers; physical bytes may differ. | `test_rebuild.py` |
| AC11 | All section-8 shapes/limits pass; prohibited operations refuse; queries start no service/build. | `test_agent_surface.py` |
| AC12 | Forged/stale/revoked/consumed approvals and imported records cannot dispatch/resume; no execution adapter. | `test_authority.py` |
| AC13 | Closeout coverage/currency/review stay separate; commit/terminal/check/exit-zero cannot independently promote. | `test_status_separation.py` |
| AC14 | Compromised links excluded with reasons; historical halted scope retained; new interpretations refuse. | `test_halted_history.py` |
| AC15 | MathLab FAIL stays MATH-PROXY, step 4 shelved/not frozen/not run; stage PASS cannot confer eligibility. | `test_mathlab_stop.py` |
| AC16 | Every prebuild disk check and at/inside/outside boundary passes; unavailable observation blocks. | `test_storage_budget.py` |
| AC17 | Resource/stop/observation/shutdown controls pass with actual RSS/stop receipts; breaches halt without cleanup. | `test_session_limits.py` |
| AC18 | Behavioral RED precedes implementation; production GREEN includes round-trip/boundary/HALT diagnostics; no skips. | `test_receipt_integrity.py` |
| AC19 | Protected hashes unchanged; edits within allowlist; concurrent drift preserved; no git mutation. | `test_scope.py` |
| AC20 | Packet hashes resolve; MAESTRO reruns; missing/nonpermitting Astra promote receipt blocks phase 2. | `test_completion_packet.py` |

| Condition | Satisfying ACs |
|---|---|
| C1 (V:20) | AC1, AC5, AC18, AC19 |
| C2 (V:22) | AC4–AC7, AC10, AC11, AC18 |
| C3 (V:24–35) | AC3, AC6, AC7, AC14, AC15 |
| C4 (V:37) | AC3, AC8–AC10, AC16 |
| C5 (V:39) | AC11, AC12, AC19 |
| C6 (V:41) | AC1, AC12, AC17, AC20 |
| C7 (V:43) | AC4, AC13–AC15 |
| C8 (V:45) | AC2, AC8, AC9, AC16, AC17 |
| C9 (V:47) | AC10, AC18–AC20 |

## 3. Roles and order

1. MAESTRO resolves section 13, names sessions and freezes spec/source/write/dependency scope (D:229).
2. KEY1 != BUILD1 reads originals/spec/authority only; writes `P/inputs/v1/`, `P/answer_key/v1/`. Confirms/replaces chains with reasons; independently writes expected records/links/numbers/scopes/labels/caveats/history/refusals and negative fixtures. Never derives answers from importer/database code or output.
3. Astra reads originals/spec/key; writes `P/reviews/answer_key_r1.md` with model/session/hashes/objections/disposition. MAESTRO freezes reviewed bytes in `P/freeze.json`. Corrections create new version/reason/diff and renewed review (V:20).
4. BUILD1 reads frozen originals/key/spec, writes only section 10. Tests first: behavioral RED, minimal implementation, GREEN; round-trip/boundary/HALT/persisted deciding evidence (`memory_mirror/test-first-one-round-builds.md:12–24`). Builder cannot edit key/inputs or generate expectations; oracle files are test-only. Suspected key defects/change halt development pending renewed freeze.
5. MAESTRO reads packet/originals, checks AC mapping and reruns actual paths; writes `P/reviews/maestro_verification.md`/fresh receipts.
6. Astra reads frozen packet/sources; writes `P/reviews/promote_r1.md`. MAESTRO records permission before expansion; builder GREEN is not promote review (V:47).

## 4. Five source-chain proposals

KEY1 confirms versions/spans/pointers or records replacements before freeze. Proposals are not the key. Bulk data stays identity-only; reviewed receipts may support scoped history. Mandatory missing artifacts block capture; optional exclusions cannot support new conclusions (D:121,142).

| Chain | Exact inspected files/locations | Category and required answer-key questions |
|---|---|---|
| S1 B3 scoped positive | `CORPUS/17_B3_QUANTIZATION_SURVIVAL.md:8–32`; `results/b3_quant_survival_result.json` `/edited_retention/{pct,surv,elig}`, `/native_country_retention/{pct,surv,elig}`, `/verdict`, `/threshold` (lines 8–25); `results/b3_margin_result.json` `/edited_top1_margin/median`, `/native_country_top1_margin/median`, `/interpretation` (lines 2–16). | Scoped quantization PASS; margin/single-run/model limits. Key: eligible counts/rounding, scope/caveats, historical deployment status, broader claims to refuse. |
| S2 A2b negative | `CORPUS/16_A2b_REFRESH_KS.md:8–36`; `results/a2b_refresh_ks_result.json` `/config/{model,seeds,lambdas,refresh_every,N,band}` (lines 2–20); KEY1 confirms additional bounded scalar pointers. | Scoped sentinel-staleness negative, not projection-refresh refutation. Key: paired/clean-seed metric validity, exposure compatibility, scalar pointers, measured vs inferred. |
| S3 C10K Route A halted | `CORPUS/42_C10K_ROUTEA_CONTROLS_NOT_RECOVERED.md:1–35`; `architecture_profile/c10k_route_a_halt_diagnostic.json` `/halt`, `/decision_id`, `/prereg`, `/controls/L2=10/A1_single/{canon,para}`, `/controls/L2=0.01/A1_single/{canon,para}` (lines 2–27). | HALTED controls; reviewed historical port scope only. Key: allowed findings/audit-only diagnostics, why canonical success cannot override HALT, forbidden A7/family inference, conflicts. |
| S4 C10W superseding | `CORPUS/55_C10W_ORACLE_P1_INTERIM.md:1–11,24–43`; `results/c10w_oracle/p1_20261007T223707_598959Z/verdict.json` `/status`, `/final_label`, `/routing`, `/reference_status` (lines 4–11); `CORPUS/57_C10W_ORACLE_FINAL.md:5–16,40–56`; `results/c10w_oracle_logs/p2-read-attempt2.json` `/status`, `/final_label`, `/routing`, `/ranks/16/count` (lines 4–14). | INCOMPLETE P1 superseded by replicated PARTIAL/BIGRAM, no clean reference. Key: current/as-of status, scoped supersession, promotion limits, compromised-P2 refusal. |
| S5 MathLab mathematical | `CORPUS/60_MATHLAB_HARVEST_REPLAY.md:73–134`; `results/mathlab/m3_20261009T225557.353172Z/calibration.json` `/outcome`, `/ordering_n`, `/proxies/rho/{status,passed,scores,point_orderings,bootstrap_counts}`, `/proxies/coll/{status,passed}` (inspected lines 2–42); same-directory `manifest.json` `/tier`, `/decision_id`, `/prereg_sha256`, `/files/calibration.json/{path,sha256}`, `/index/{tier,derived,rows}` (lines 2–16); `docs/MATHLAB_STEP4_PREREG.md:3–7,19`. | Valid MATH-PROXY FAIL, step 4 shelved. Key: harvest/rule/counts/tier, FAIL vs INVALID, stage-PASS distinction, NEW-1 separation, launch/queue refusal/history. |

KEY1 confirms original definitions/preregs/reviews and selected state/registry pointers. `docs/program_state.json:2` identifies canonical generated status; `docs/experiment_registry.json:3–13` shows provenance links. Exclusions are not untested. `mathlab/index.py:1,10–31` is a read-only derived-index reference, not runtime dependency.

## 5. Vocabulary and normalization

Single frozen `vocabulary.json`: kinds, required slots/enums and typed link endpoints. JSON validator; LinkML tooling deferred (recommended at D:111), no inference model/second vocabulary.

Kinds: Question, Hypothesis, ScopedClaim, Preregistration, ExperimentDefinition, Run, Arm, Measurement, Finding, Decision, ReviewVerdict, SpecObligation, Agent, Task, Approval, SourceVersion, ArtifactVersion; instances limited to five chains. Papers/idea/search/optimizer workflows excluded with reasons. Foundations: D:125–132.

Common slots: record ID, enduring identity ID, kind, source-version ID, original IDs/labels, explicit aliases, source refs, scope ID/definition, caveats. Required separate claims (V:43; D:134–138):

| Field | Values/details |
|---|---|
| execution_state | NOT_RUN/RUNNING/COMPLETED/HALTED/INCOMPLETE/UNKNOWN/N_A; original label retained. |
| scientific_outcome | Exact source label or reasoned null; administrative PASS cannot convert. |
| evidence_tier | SCIENCE/SOFTWARE_FIXTURE/MATH_PROXY/EXPLORATORY/PAPER/UNKNOWN/N_A; original tier and evidence/inference attribution. |
| link_review_state | PENDING/CHECKED/REJECTED/SUPERSEDED/STALE/N_A; separate origin EXPLICIT/MACHINE_INFERRED. |
| source_currency | MATCHES_CAPTURE/STALE/UNRESOLVED/UNKNOWN; check time/dirty-live flags; never perpetual currency. |
| closeout_check_coverage | NOT_RUN/PRESENCE_ONLY/PRESENCE_AND_CURRENCY/UNKNOWN/N_A; exit/presence/fingerprint results, expected/observed token, receipt. |
| promotion_review_disposition | NOT_REVIEWED/GO/GO_WITH_CONDITIONS/FIX_FIRST/NO_GO/CONFIRM/UNKNOWN/N_A; original wording/scope/receipt. |

CONFIRM retains reviewed scope; unknown currency stays unknown. Import receipts only, no checker repair/execution; exit zero/commit/terminal/check alone cannot promote (V:12,43; DISCIPLINE.md:48–50,86).

Kind slots: question/hypothesis text/coverage; finding/claim outcome/scope/caveats; prereg revision/hash/freeze; distinct experiment/run/arm IDs/setup; decision/review actor/subject/time/disposition; task/approval issuer/scope/attempt/stop or explicit unknowns (descriptive only). Source/artifact: relative location, revision/SHA-256, media/size, span/RFC6901 pointer, availability/retrieval requirements.

Measurement: exact decimal value_text, unit/metric definition, numerator/denominator/basis, split/exposure, model/setup/seed/run/arm, scope/source. Derived numbers also frozen operand IDs/source-stated recipe; no new compromised-output inference. DuckDB keeps all admitted scalars/records/links; graph keeps connections/selected scalar summaries; no tensors (D:112–113,136–138).

Links: TESTS/SUPPORTS/REFUTES/REGISTERED_BY/PRODUCED_BY/MEASURED_IN/DERIVED_FROM/SUPERSEDES/QUALIFIES/REVIEWED_BY/BEARS_ON/CITES/BLOCKED_BY/USES_SOURCE/ASSIGNED_TO/REQUIRES_APPROVAL/HALTED_BY. Required: ID, typed versioned endpoints, citation/hash, meaning/scope, origin/review history and reviewed-set receipt. SUPERSEDES scopes status replaced; no erasure/transitive scientific proof (D:125–140). Semantic admission requires reviewed payload/hash/scope in `P/inputs/v1/reviewed_links.jsonl`; forged CHECKED/new meaning quarantines UNSUPPORTED_MEANING. Prose suggestions stay pending. Reviewed input is separate from test-only `answer_key/v1/expected*.json`.

Canonical strict UTF-8 JSON: reject duplicate keys/nonfinite/omitted slots. Null reason MISSING/NOT_RUN/N_A/UNKNOWN/NOT_ISSUED; empty list inspected-empty. Sort records/links/aliases/refs by IDs; retain ordered arm arrays. Unique record ID and identity/version pair; historical versions legal, ambiguous aliases never merge. Exact integers/source decimal strings, tolerance zero; rounded percentages distinct from ratios, no legacy correction. Rebuild digest omits only generation IDs/build times, retains provenance. Comparisons require compatible metric/unit/denominator basis/exposure/scope/setup or a source-stated KEY1-frozen conversion; unknowns refuse, no pooling/ranking/automatic contradiction (D:136,142).

## 6. Frozen negative controls

KEY1 freezes fixtures/baseline positives/diagnostics (V:24–35). Mutate test copies only. Reject: no publication, old pointer intact. Quarantine: persist ID/source/reason/excluded uses, expose coverage/history. Incomplete: code3/named reason/no combined conclusion.

| ID/fault | Exact disposition/code |
|---|---|
| N01 valid citation/IDs, unsupported B3 full-deployment claim/forged CHECKED | Quarantine link UNSUPPORTED_MEANING; no SUPPORTS use. |
| N02a duplicate ID; b duplicate identity/version; c ambiguous alias | Reject generation DUPLICATE_ID/DUPLICATE_VERSION; quarantine alias AMBIGUOUS_ALIAS, lookup incomplete/candidates/no merge. |
| N03a changed hash; b unresolved location; c malformed source; d missing mandatory artifact | Reject generation SOURCE_HASH_CHANGED/SOURCE_LOCATION_UNRESOLVED/MALFORMED_SOURCE/REQUIRED_ARTIFACT_MISSING. Optional missing artifact inventoried; dependent query incomplete MISSING_ARTIFACT. |
| N04a units; b denominator basis/missing denominator; c exposure/split; d scope/setup | Incomplete INCOMPATIBLE_UNITS/INCOMPATIBLE_DENOMINATORS/INCOMPATIBLE_EXPOSURE/INCOMPATIBLE_SCOPE; separate facts only, no pooling. |
| N05 superseded P1 returned current | Incomplete SUPERSEDED_AS_CURRENT; normal selector uses successor; history preserves P1. |
| N06 compromised-P2 support/refutation/comparison or new halted-A7 interpretation | Quarantine link COMPROMISED_SUPPORT/HALTED_SCOPE_EXCEEDED; dependent scientific answer incomplete; reviewed historical scope retained. |
| N07 calibration FAIL + stage PASS promoted to step-4 eligibility | Quarantine eligibility link CALIBRATION_FAIL_BLOCKS_STEP4; factual answer complete “not eligible/shelved”; contrary inference incomplete. |
| N08 out-of-slice question | Incomplete OUT_OF_SLICE with coverage; never UNTESTED/NO_EVIDENCE. |

Conflicting originals: quarantine claim/measurement, incomplete SOURCE_CONFLICT. KEY1 freezes refusal or seeks separate correction; BUILD1 never edits originals.

## 7. Publication and failure tests

Single publisher lock; exclusive-create UUID candidates. Capture frozen allowlist; record Git HEAD and per-file committed/dirty/live attribution. Before/after original and captured hashes must match freeze; mutation aborts. Live bytes require reviewed immutable capture (D:119; V:37).

Build DuckDB `runtime/generations/<g>/measurements.duckdb` and Neo4j logical partition generation_id=<g> from SAME bundle. Community shares physical storage; every node/edge query constrains selected partition. Published content immutable; logs/runtime metadata mutable. Writer creates fresh partitions only; partial partitions remain diagnostic/invisible.

Validate actual stores, canonical table/graph/coverage digests; close/checkpoint/hash DuckDB. Exclusive-create/fsync file+directory/re-read `generation_manifest.json`: Git/source/bundle/key/reviewed-link/schema/importer/dependency hashes, coverage, DuckDB path/hash, graph partition/digest, validation receipt/time. Sync failure rejects.

Separately named pointer `runtime/publication/current.json`: write/fsync temp, atomic same-filesystem replacement, directory fsync. Pointer selects manifest path/hash/sequence; retain predecessor receipts. Manifests never overwritten; crash accepts only validated old/new COMPLETE pair (V:37,45).

Request reads pointer ONCE, retains lease until finish/cancel; opens selected DuckDB read-only and selected graph partition. Generation IDs must agree; publication cannot change lease/delete data. Include capture/publication times/age. Loss/mismatch/no publication returns explicitly incomplete; separately labelled available facts cannot form mixed scientific conclusion.

Deterministic barriers: failure after DuckDB only/before graph commit/after graph ready-before manifest; interruption before/after pointer replacement/directory sync; source mutation between hashes; G2 publication during held G1 query; backend loss/wrong generation. Assert pointer state, immutable data/manifests, durable diagnostics and actual old-pair oracle answer with age. Rejected negative imports also query the prior pair through both stores/interface. No sleeps/retries/cleanup.

## 8. Agent interface

Local JSON stdin/stdout: `LLMDB_ROOT=$PWD "$RE_PY" -I -B "$CLI" agent`; no browser/listener/MCP needed. Data operations use BOTH stores for provenance/parity. `describe` is local metadata. Never auto-start stores/services. Inputs: request ID, operation, typed arguments, optional expected generation; unknown fields reject. Outputs: request ID, disposition/code, pinned generation/manifest hash, records/source refs, statuses/caveats, coverage/missing reasons and next action. Repeated query IDs cannot create tasks/renew permission.

| Operation | Inputs | Output/bound |
|---|---|---|
| describe | None | Version, operations, limits, absent capabilities. |
| get_record | Exact record/version ID | Scoped record/provenance; ambiguous alias refuses. |
| trace_chain | Admitted root, in/out, allowed link kinds, depth 1–3 | <=100 records/200 links; incomplete on truncation. |
| measurements | Run/arm and frozen metric IDs | <=100 scalars with units/denominators/exposure/scope. |
| compare | Two measurement IDs | Compatible side-by-side facts or N04 refusal; no pooling. |
| history | Enduring ID, optional frozen as-of version | <=20 versions, supersession scope/current selection. |
| coverage | Slice or admitted chain ID | Indexed/excluded/missing/unsupported/quarantined/pending-review IDs/counts. |
| answer_question | Frozen question ID | Fixed typed answer; unknown/out-of-slice N08. |

KEY1 freezes cases/backend projections for every operation. Per request: 16 KiB input, 256 KiB output, 2 s/backend, 5 s total, one active request. Limit gives incomplete `LIMIT_REACHED`, never silent truncation. Fixed parameterized queries; disable DuckDB external access/extension autoload. Reject arbitrary SQL/Cypher, paths/URLs, procedures/extensions, callbacks/code/shell, bulk retrieval/export and online fetching. Absent: submission, approval requests/grants, task creation, dispatch, launch/resume, queue writes, canonical writes, closeout/promotion and model/GPU operations. Imported records confer no capabilities (V:39).

## 9. Authority (no later execution adapter)

| Operation | Propose | Review | Authorize | Execute | Promote |
|---|---|---|---|---|---|
| Spec/key change | KEY1/MAESTRO | Astra | MAESTRO; operator changed limits | KEY1 new packet/MAESTRO freeze | MAESTRO after review |
| Install/start/build/query/publish | BUILD1/MAESTRO | Frozen review/limits | O allowance bound by MAESTRO | Named provisioner/BUILD1; users read | MAESTRO verifies/Astra expansion |
| Scientific link/source change | Assigned agent/person | Applicable reviewers | Existing MAESTRO; operator amendments | Source owner, absent here | Canonical workflow |
| Experiment/resume/closeout | Agent/MAESTRO | Prospective/binding | Operator + manager gates | Existing manager, absent here | Reviewed closeout |
| Delete/spend/export/credentials/cap | Owner exact scope | MAESTRO/applicable | Operator; deletion path/size/method | Authorized owner, absent here | Verified receipt |
| Phase 2 | MAESTRO | Binding Astra | MAESTRO within reviewed/operator scope | New session | Separate review |

Trusted resource issuer is O, not a database row. Future coverage must name authoritative manager/issuer, workload/resources, receipt hash/validity/revocation source; absence grants no exemption. Dispatch AND resume revalidate code/source IDs, stop/revocation and remaining attempt allowance; stable IDs never renew consumption. Coverage cannot authorize science/deletion/spend/prereg amendment; backup coverage is not database permission (V:41; D:179–185). AC12 tests descriptive/unsupported paths only.

## 10. Environment, paths and allowed edits

Dedicated `.venv-research-engine/`, no system site-packages/science `.venv` reuse. Proposed exact pins: **CPython 3.12.14**, **duckdb==1.5.5**; stdlib unittest/JSON/HTTP/hash tools only. Justification: local cache `/Users/robertrhu/.cache/uv/archive-v0/waLE3HFo0DjN44MZ/duckdb-1.5.5.dist-info/METADATA:2–3,21–23`, `WHEEL:4` names cp312/macOS arm64; interpreter directory `/Users/robertrhu/.local/share/uv/python/cpython-3.12.14-macos-aarch64-none/` exists. These are candidate pins, not runtime validation. Provisioning verifies versions/hashes. Science dependencies remain untouched (`pyproject.toml:14–18`). Deny imports/dependencies of torch, transformers, model/tokenizer/science/MathLab runtime; JSON/text capture only.

Neo4j Community/Homebrew/Mac is settled (O:5–7). Server/formula/JDK/bottle versions await section 13; no floating/latest substitutions. Use supported localhost HTTP transaction API with fixed stdlib requests after provisioning smoke verification. No Neo4j Python driver, LinkML runtime, APOC/GDS/plugins/framework. Authentication on; loopback bind; secret mode 0600, excluded from receipts. Session-owner access; no claim of Community per-generation privileges.

Paths below resolve under this memit worktree; builder allowlist (new paths unless freeze inventories prior contents):

- `tools/research_engine/{cli.py,capture.py,vocabulary.py,adapters.py,stores.py,publication.py,queries.py,limits.py,README.md,vocabulary.json,requirements.lock}`.
- `tests/research_engine_phase1/`: twenty named tests plus `__init__.py`, `helpers.py` only.
- `.venv-research-engine/`: named provisioner only, after freeze.
- `P/runtime/{neo4j/{conf,data,logs,transactions,run,tmp},generations/<g>/,publication/,leases/,credentials/,control/,tmp/}`: all data/temp writes.
- `P/builds/<fresh-id>/`: receipts/logs/outputs/resources/hash inventories/report.

KEY1 owns inputs/key; MAESTRO/Astra own reviews/freeze. Builder cannot edit them or spec. Other paths, including canonical evidence/existing results/MathLab stores/managers, stay read-only. No git writes, experiments, tmux changes/deletions. Homebrew provisioning is separately assigned, not builder repository scope; disable automatic install cleanup. Use explicit interpreter invocation; any new directly executed script needs reviewed scope and execute-bit test (`memory_mirror/test-first-one-round-builds.md:16`).

## 11. Resource/storage/stop budget

Memit TOTAL <=**5,000,000,000 bytes**, environment/code/key/captures/stores/failures/temp/logs included. Homebrew binary/JDK/cache on normal volume separately budgeted before dispatch: O:7 estimates about1 GB, not verified total growth. Memit installs count within cap; database/temp stays on memit.

Decimal ceilings: env/code/tests600 MB; key/inputs200; DuckDB600; graph1,200; transactions/checkpoints600; temp/tests800; receipts/logs300; reserve700 = **5,000 MB**. <=2 complete generations + <=8 failed/test candidates; capture <=50 MB, <=1,000 records/2,000 links/1,000 scalars each. Retained artifacts count; exhaustion stops, no cleanup/rollover.

Before EVERY build receipt B(existing)/P(additional conservative PEAK)/free/path/time. Require B+P<=5,000,000,000 and free>=P+21,474,836,480 (20 GiB). P includes copies/retained stores/temp/graph overhead/transactions/tests/logs; unknown overhead reserves remaining ceilings. Unavailable observation blocks. Install-volume check separately projected writes+20 GiB. Deletion needs operator exact path/size/method (O:13; V:45; user AGENTS.md).

One writer/Neo4j/query, no concurrent science; nice+10; importer/DuckDB one worker/thread. Heap256 initial/512 MiB max; page cache256 MiB; Java active processors2. Neo4j TOTAL RSS<=**2,000,000,000 bytes**, importer<=512 MiB, aggregate<=3 GB. CPU<=200% Neo4j/100% importer; observe CPU/RSS/disk each second; unavailable admission/host/stop observation blocks (O:11; D:179–185).

Build/verify<=300 s, provisioning<=15 min, session<=30 min. Cap/stop/revocation/timeout: fsync phase/IDs/observed bars/traceback, halt without publish/cancel queries. Stop proven owned Neo4j gracefully<=30 s, escalate that process if needed; retain files. Unconfirmed stop blocks UNVERIFIED. Dedicated session paths; no brew-services/launchd/autostart/schedule. Disable automatic transaction-log pruning; stop at cap instead. Actual normal/error RSS/start/stop receipts required; fixture PASS cannot prove host caps (O:11–13; V:45).

## 12. Completion packet

P/builds/<id>/completion_manifest.json hashes/indexes:

- Frozen originals/capture/spec/key/author/review/freeze/reviewed-link identities.
- Code/tests/schema/lock hashes, observed versions/install scope/size.
- AC/question/control mapping, behavioral RED/GREEN command/stdout/stderr/exit/time, full suite, round-trip/boundary/HALT receipts; no skips.
- EVERY actual two-store query/parameters/backend IDs/raw rows/canonical comparisons and agent transcript/refusal.
- Manifests/pointer history/barriers/leases/prior-age and fresh rebuild comparison.
- Observed peak disk/temp/transaction growth, preflight math, CPU/RSS/time/threads/concurrency/start/stop receipts.
- Protected/scope hashes/drift/report, exclusions/limitations/UNVERIFIED; no science claim.
- MAESTRO rerun/Astra promote receipts; builder hands back PENDING slots, never treats them as present.

Mismatch/omission/key change/missing diagnostic/backend/cap breach blocks acceptance. Preserve failures/fresh namespaces; key changes need renewed review. Phase2 requires MAESTRO verification + permitting binding Astra promote (V:47; D:229,239,245).

CONTEXT for every team/successor: watch Context N% left; new work only >=60%. At <=40%/Context compacted: stop starting work, save, append done/open/single next step/exact paths to P/handoff.md, restate directive/report handoff; never finish in-flight test after compaction.

## 13. Unsettled assignment/provisioning facts

No architecture/Git/HIL reopening (SPEC-FIRST: DISCIPLINE.md:30–33).

| Decision | Owner/recommendation |
|---|---|
| Sessions/chains/questions | MAESTRO names KEY1!=BUILD1/reviewer/provisioner; KEY1 confirms/replaces before review. |
| Homebrew server/formula/JDK/bottle pins, HTTP/config compatibility, install-growth ceiling | MAESTRO/provisioner freezes package/interface receipt; operator if scope exceeds O. Never guess/substitute hosting. |
| Python/DuckDB/JSON vocabulary | MAESTRO validates/freezes candidates; incompatibility needs reviewed correction. |
| Admission/stop receipt/ownership | MAESTRO names existing authority/path; bounded reservation, no scheduler/backup exemption. |
| Commit/dirty capture | MAESTRO/KEY1 freezes hashes/flags; honest attribution, no importer-driven commit. |
| Retention exhaustion | Operator exact deletion/revised scope; recommend stop/preserve prior pair. |

SPEC1 inspected documents/bounded JSON/package metadata only; no builds/tests/services/installs/downloads/experiments/git mutation. Numbers are historical reports. C1–C9 mapped; chain/dependency/host confirmation gated.
