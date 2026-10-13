# NEW-1 construction diagnostic — predeclared scope (D-NEW1-b, MB5)

**BUILD ONLY; real inputs NOT RUN / UNVERIFIED.** This scope is written before the synthetic tests and implementation. Binding authorization is `results/mathlab_staging/new1_construction_diag_authorization.md` (operator, 2026-10-10T06:40Z); the measurement and interpretation follow `results/mathlab_staging/new1_identity_diag_astra.md` Q2/Q3. MAESTRO3 owns review and the single authorized launch. This diagnostic addresses a blocking provenance discrepancy relevant to F1; it supplies no adapter geometry, locality, projector-fidelity, prediction verdict or F1 conclusion.

## Frozen arithmetic and four constructions

Read only the pinned L4 moment cache, historical capture and manifest. Normalize **once** using the unchanged worker recipe: `torch.from_numpy(np.divide(moment, count, dtype=np.float32))`, without centering. Require finite square NumPy float32 moments, positive scalar NumPy int64 count and production dimensions `(11008, 11008)`. Record normalized C bytes, shape, dtype and stride.

Compute **one** CPU fp32 `torch.linalg.svd(C, full_matrices=False)`. Keep the same native `U`, `s`, mask `s < 0.005` and selected indices throughout all four constructions. No float64 decomposition, blocked geometry checks, adapter loading, update/energy computation or alternative normalization. Release C and Vh before constructing projectors. Record U/s/mask/LongTensor index hashes and metadata before and after the four constructions; any mutation is INVALID. The allowed Python list is precisely the LongTensor indices converted with `.tolist()`; record its canonical JSON SHA and count.

The order is fixed before measurement:

| ID | Index argument | Operand construction | Gather operations |
|---|---|---|---|
| `list_shared` | Python list | `Q=U[:,idx]; P=Q@Q.T` | one |
| `list_separate` | Python list | `left=U[:,idx]; right=U[:,idx].T; P=left@right` | two |
| `long_shared` | CPU LongTensor | `Q=U[:,idx]; P=Q@Q.T` | one |
| `long_separate` | CPU LongTensor | `left=U[:,idx]; right=U[:,idx].T; P=left@right` | two |

Separate operands retain the two temporaries so their facts can be inspected; they execute the same two gathers and matmul as `U[:,idx] @ U[:,idx].T`. Record operand facts **after** matmul, without hashing between gathers and matmul. Every iteration releases its projector, gathered operands and transposed views before the next construction. Only common U/s/mask/indices and four captured vectors survive the loop. No dense tensor is returned or persisted.

For each construction record the left and right operand's row-major byte SHA, shape, dtype, device, stride, storage offset and storage byte size; whether they share storage with each other or U; whether right's value hash equals left-transpose's value hash; and whether the gather operation count is one or two. Storage relationships use live storage identity, including the empty-storage case; addresses are not interpreted as backend evidence. Hash/stride inspection after matmul cannot certify an identical historical allocation interval.

For **every** projector invoke `new1_geometry.projector_matches(P, actual_allowed, captured_allowed, captured_sha, probes)` unchanged. Independently record actual allowed/excluded counts, captured allowed/excluded counts, count agreement, projector SHA/captured SHA and agreement, and all four seeded probe residuals **even when count or SHA short-circuits the gate**. Actual probes use CPU fp32 `P @ torch.randn(d, generator=torch.Generator().manual_seed(j))`, j=0..3. Record absolute L2 and maximum coordinate residuals, actual/reference L2 norms, relative error in float64, and `MATCH` iff relative error **<=1e-6**. Also record all-probe agreement and maximum relative error. No tolerance change or substitute gate. Missing, nonfinite, wrong-shaped/dtyped or zero-norm references and invalid count/SHA metadata abort as INVALID.

## Pins, caps, receipts and launch

Reuse the exact pinned prior diagnostic's stdlib supervisor, admission, family-RSS observation, bounded cleanup, exclusive output writer and probe residual function. Source `tools/new1_identity_diag.py` must remain SHA `93a7b317f8078c63c3c0d40d35fb419dfd24132a10577387af93c3790d461cb1`. Its `SOURCE_PINS`, historical harvest commit `6ea8e7c07156133667a8d6d28364f759ba1d7a31` / full-source SHA `9dbc58afef1aa290d5e01622d3324b052e3f19169bfeb8d38ad19148cfe869bb`, and three `INPUT_PINS` are retained. No prior normalization or path-report arithmetic is called. The private worker marker remains `NEW1_IDENTITY_PARENT` solely because the pinned supervisor supplies it; the new script checks the real immediate parent PID and uses its own scope/source pins and output namespace.

| Data input (pins copied from unchanged geometry/identity diagnostic) | SHA-256 |
|---|---|
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz` | `f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58` |
| `results/mathlab/harvest_20261009T184950.056951Z/manifest.json` | `bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e` |
| `results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt` | `abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f` |

Additional immutable pins bind this authorization, Astra Q2/Q3, geometry, supervisor, shared admission/runtime/events and frozen NEW-1 preregistration. Launch requires the exact final construction scope and script SHA. Both parent and worker verify all source, historical and input pins before arithmetic; inputs are checked again around consumption by `bound_input`. The manifest's L4 covariance path/SHA must equal the pinned cache. Capture loading is CPU `weights_only=True, mmap=True`; clone only count/hash/four probes, never inspect adapter or update tensors. Report probe identity hashes, all pins, scope/script SHA, package versions, CPU/default SVD driver, configured eight threads, backend build string, parent/worker nice and capture version metadata. Historical capture threads remain **UNKNOWN**.

**Caps are unchanged:** 600 seconds total, observed process-family RSS **strictly below 11 GiB** (stop at equality), eight CPU threads, final parent/worker niceness **exactly 10**, CPU environment with CUDA visibility empty, fresh fail-closed `mathlab_admit.probe('cpu')`, one isolated worker, **no retries**. Parent remains stdlib-only until admission; watchdog interrupts blocked SVD/IO, counts its own descendants, and refuses denied/empty/incomplete/malformed observations. Five seconds each bound kill/reap cleanup and terminal error recording after abort; neither permits more arithmetic. Numerical/resource/backend behavior on real inputs is UNVERIFIED here.

The launching shell may already be nice 10. The printed launch command obtains current niceness in a stdlib probe and passes **`10-current_nice`** to `nice -n`, rather than adding 10. A starting value above 10 refuses; a starting value of 10 uses increment 0. The script independently refuses a final value other than 10. Exact pinned command is supplied with the build receipts; MB5 does not execute it.

**Disk:** exclusive `result.json` and `receipt.jsonl`, together **strictly less than 1,000,000 bytes**, in a fresh `results/mathlab_staging/new1_construction_diag/construction_<UTC>/` directory. Scalar JSON/provenance only; no dense persistence, auxiliary tensor files, plots or logs. The reused writer reserves error-recording space before nonterminal writes. Acceptance requires exit 0 and the final `terminal`, `MEASURED` receipt binding the exact result SHA; a result alone is uncommitted. Preserve any partial result and append a bounded `halted`, `INVALID`, `result_committed:false` receipt on late failure when IO permits. Never reuse an output directory. Build receipts are separate and budgeted at 4 MB; observed free space before writing was 91,823,214,592 bytes, above 4 MB plus 20 GiB.

## Predeclared outcome table

The unchanged gate is the primary capture-agreement observation; all counts/SHA/probes remain visible so a short-circuit is not misread as multiple failures. Diagnostic status `MEASURED` indicates a valid measurement, including four failed gates; it is not a scientific PASS.

| Observation across the fixed four constructions | Means within this configuration | Does not mean / next permitted action |
|---|---|---|
| All four agree with capture | No construction separation measured | Original worker cause remains unresolved; no repair or NEW-1 retry is authorized |
| Some agree, some fail, with unchanged U/s/mask and capture arguments | Construction alone separates capture agreement in this measurement | Does not establish historical cause or general fp32 reproducibility; propose **one reviewed, failing-first construction fix**, bring it and any new real attempt to the operator |
| Separation follows shared versus separate in both index representations | Shared/separate operand construction is the discriminated factor here | No inference about adapters, full subspace distance, historical runtime or tolerances |
| Separation follows list versus LongTensor in both gathering styles | Index representation is the discriminated factor here | No automatic production substitution, retry or attribution beyond this configuration |
| Mixed interaction, count/SHA/probe inconsistencies or isolated separation | Preserve the exact four-row evidence; narrow mechanism remains unresolved | No convenient winning-path repair without review and operator ruling |
| None agree | Construction alone does not reproduce capture | No speculative fix; exact-worker L4 execution with float64/check interval and supervisor context needs **separate authorization** |
| Pin/admission/resource/metadata/mutation/output failure | INVALID diagnostic, no accepted measurement | Preserve original HALT and new failure; no retry, relaxed gate, amended preregistration or patched verdict |

Equal counts or four probes cannot certify equal subspaces, full operator distance, projector fidelity or behavioral locality. The float64/check interval and adapter/allocation history in the original worker are deliberately outside this one-SVD diagnostic and remain untested. Nothing edits the original HALT, geometry, supervisor, preregistration or the NEW-1 result.

## Build evidence and context handoff

Evidence directory: `results/mathlab_staging/new1_construction_diag_build_20261010T071253.399810Z/`. Initial scope, baseline protected hashes, test-first RED/GREEN receipts, final audit and exact launch command will be recorded there; documentation-only closeout will be appended below. All fixtures are synthetic CPU operands; no real input is opened or hashed by the builder and no real admission is run.

**BINDING context directive (operator 2026-10-09):** watch `Context N% left` in every root/team session. Before approximately **20%**, stop starting new work, write done/in-flight/exact paths/next step/open risks into this scope, notify MAESTRO3 and request a fresh successor. Every handoff restates this rule; never approach full-window compaction.
