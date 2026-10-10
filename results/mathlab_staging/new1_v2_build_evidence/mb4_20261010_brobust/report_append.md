

## Amendment B (D-NEW1-b) — B-ROBUST build (2026-10-10 UTC; Codex MB4)

**NEW1 B-ROBUST BUILD DONE.** The operator-adopted **Boundary-robust covariance geometry** variant is appended to the frozen prereg and built tests first. Complete prereg SHA-256: **`1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f`**. **95 unique NEW1 CPU tests PASS: 34 geometry +61 supervisor.** Fresh GPT-6-Astra static review: **BUILD-ACCEPT**, no corrective code request. These are build/fixture checks, not a real NEW1 run, real-input result, full-workload resource acceptance, calibration, queue change or F1 closure. No commits or repository deletions were performed; MathLab files remain untouched.

### Authority, frozen amendment and implementation

Read the complete `results/mathlab_staging/new1_b_variant_astra.md`, complete `new1_options_astra.md`, the MB3 measurement/draft from this report's original line 547, and the complete frozen v2/A1 contract and both production/test files before editing. The adopted ruling is the **recommended invariance variant**, not the original equal-count B. The map cell remains Write Engine §8 / C10 / §8.9 L2; descriptive stored-covariance geometry is not the behavioral post-write gate. No pinned matrix/factor/update payload was decoded for this build. Streaming hashes and recorded resource receipts are the only real-input reads.

`docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:190` adds **Amendment B (D-NEW1-b): boundary-robust covariance geometry** at the end, before any update-energy inspection. It explicitly supersedes original §3:51–59, affected §4 rules, §6 resources and A1:182–186, while preserving all earlier bytes. It explicitly replaces equal cutoff counts and universal cross-projector certification, renames H-COV, keeps every numeric margin and requires the same at least three layers to pass every cutoff. No L4 exception, favorable cutoff choice, layer drop or tolerance relaxation exists. Original halted attempts/old-hash receipts and MB3's original failed equal-count proposal retain their historical meanings.

| Requirement | Production behavior | CPU evidence |
|---|---|---|
| One native-fp32 and one float64 covariance SVD per layer | `new1_geometry.py:150` retains U32/s32/masks, releases native Vh, then decomposes unchanged fp32-normalized C promoted to double; float64 U/s define geometry | Two-call dtype/object/byte checks; rotated subnormal fixture; unchanged normalization; indefinite PSD rejection |
| Existing numerical gates on float64 geometry | Original symmetry 1e-6; SVD/PSD/orthogonality 1e-5; blocked float64 checks, k=1024 and existing tie rules | PSD/tie/blocked-product tests; native residuals do not gate geometry |
| Native captured identity/parity retained separately | `native_projector()` at :200 uses only native U32/mask; capture hashes/count/four probes remain; :421 gates native excluded energy at 1e-4 | Native count/hash/probe positive and negative controls; large float64 M excluded energy accepted while native energy is zero; native-energy violation rejected |
| Inclusive cutoff band in float64 order | `geometry_energies()` at :205 projects band columns once and derives every prefix partition, with complements checked for every integer cutoff | Hand-computed 1/2/3-cutoff energies; reverse/equal/zero/d count cases; no skipped intermediate cutoff |
| Every arm/control disclosed | Per-layer M, five adapters, 20 flat and 20 spectrum-matched random rows, and valid M16 carry band energy and all cutoff allocations; random means/q95 are computed per cutoff | Persisted 47-record fixture, complete cutoff keys/complements; every control draw retained; existing M16 invalid-subspace semantics retained |
| Same three layers at every cutoff | `predictions()` at :331 validates complete intervals and counts layers that pass all their own cutoff margins | Different passing three-layer sets cannot be unioned; one bad random guard removes that layer; missing cutoff is INVALID |
| Literal nonrobust label | Valid H-COV robust PASS requires ≥3/5 invariant layers; otherwise **BOUNDARY-SENSITIVE**, as the operator's explicit otherwise rule requires; nominal margin PASS/FAIL is separately recorded | Mixed-set and all-nominal-fail fixtures; other three endpoint rules unchanged |
| Publication without MathLab edits | `new1_supervisor.py:271` retains literal BOUNDARY-SENSITIVE in receipts/artifacts/summaries, omits its Boolean gate, uses INVALID stage/terminal envelopes | Actual publication/terminal fixtures inspect schema-valid events, receipt, summary and finding; no H-COV FAIL/PASS gate is fabricated |
| Measurement-sized enforcement | 2700-s total, 11-GiB strict observed RSS; native reserve 5+8=13 GiB, float64/check reserve 11+8=19 GiB | 18.9/19-GiB reserve boundary; strict 11/11.0001 RSS; 2700-s total; unchanged 300-s wait; monitoring/CPU refusal and worker/group termination tests |

The native numerical factorization residual is not promoted into a geometry gate; no native/float64 subspace equivalence is claimed. Float64 excluded M energy may exceed 1e-4 because it is a geometric endpoint; the **separate native-basis** 1e-4 parity gate remains binding. Boundary-sensitive INVALID is a conservative transport envelope required by the unchanged shared three-valued event schema, not an arithmetic-failure claim. Each literal prediction remains in fsynced output/receipts; `events.jsonl` remains the run-state authority. All specificity comparisons are recorded per cutoff; any eligible three-layer NON-SPECIFIC contrast blocks a semantic reading. Calibration and prospective utility still gate every queue recommendation.

### Test-first RED/GREEN trail

Evidence is durable under **`results/mathlab_staging/new1_v2_build_evidence/mb4_20261010_brobust/`**, with no temporary symlink target. `before/` holds the exact original sources/tests/prereg/report, `baseline.json` the initial identity/scope, and individual `.json` receipts the exact argv, exit code, elapsed time, prereg pin and log path. The prereg amendment and RED tests preceded production changes; both production hashes were asserted unchanged immediately before the RED runs.

| Run | Tests | Exit | Result | Log |
|---|---:|---:|---|---|
| RED geometry, original production | 34 | 1 | 10 failures +5 errors including subtests | `red_test_new1_geometry.log` |
| RED supervisor, original production | 61 | 1 | 3 failures +4 errors including subtests | `red_test_new1_supervisor.log` |
| Initial GREEN geometry | 34 | 1 | One fixture assertion rejected the already-allowed ≤256-column norm promotions | `green_test_new1_geometry.log` |
| Initial GREEN supervisor | 61 | 0 | PASS | `green_test_new1_supervisor.log` |
| Final GREEN geometry | **34** | **0** | **PASS, 1.185 s** | `green_r2_test_new1_geometry.log` |
| Final GREEN supervisor | **61** | **0** | **PASS, 3.715 s** | `green_r2_test_new1_supervisor.log` |

RED failures/errors were the required absent behavior: original code performed only the native SVD and gated its deliberately perturbed factorization; ignored cutoff tables and could select different passing-layer sets; rejected the new boundary label; and enforced old caps/reserves. Logs/receipts are preserved without reclassifying those errors as numerical observations. The one intermediate GREEN failure was a fixture expectation, corrected to require **exactly one full normalized-C promotion plus only ≤256-column reductions**; production was unchanged for that correction. Final results are **95 unique methods, zero failures/errors/skips**, not 190 tests from counting both iterations.

Exact final suite command shape (the receipts preserve absolute argv):

```sh
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT="$PWD" TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/private/tmp/new1_mb4_green_r2_cache .venv/bin/python -B -m unittest -v tests.test_new1_geometry
/opt/homebrew/bin/rtk proxy env LLMDB_ROOT="$PWD" TMPDIR=/private/tmp LLMDB_DEVICE=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/private/tmp/new1_mb4_green_r2_cache .venv/bin/python -B -m unittest -v tests.test_new1_supervisor
```

Separate fresh CPU processes used small synthetic tensors and controlled stub workers only. The geometry fixtures use one torch thread for short tests; the real worker retains its pinned eight threads. Fresh pycache namespaces prevent stale bytecode without deleting caches. No model/tokenizer/engine job, real NEW1 supervisor dispatch, covariance SVD on a pinned cache, adapter analysis, live CPU admission or GPU/MPS arithmetic occurred. Other project suites were not run: the requested verification scope is the short NEW1 CPU suites.

### Five-layer full-workload resource projection and caps

Detailed machine-readable projection: `resource_projection.json`. It validates the preserved **16-record** L4 receipt and its SHA **9461275cb091469ee3ffda3af8c51e62ba75e361c93133d4100ded522cb7637a** against the derived summary; no SVD was rerun. Source high-water is Darwin `getrusage` **8,650,915,840 bytes /8.056793212890625 GiB**, not sampled RSS. Source pair/check time is **256.7851474173367 s**, whole profile **258.0238978751004 s**, measured native/double excluded counts **2363/2364**. These recorded values motivate the layer-independent rule; no update energy was observed.

| Five sequential L4-equivalent layers | Projected time |
|---|---:|
| Five native-fp32 covariance SVDs | **381.368877500 s** |
| Five float64 covariance SVDs | **796.480735211 s** |
| Five sets of measured blocked checks | **106.076124376 s** |
| Covariance phase subtotal | **1283.925737087 s** |
| Whole-profile extrapolation including measured parent overhead | **1290.119489376 s** |
| Covariance subtotal +600-s allowance for other work | **1883.925737087 s** |
| **Full-workload planning envelope: 1.50×covariance subtotal +600** | **2525.888605630 s** |
| **Adopted total monotonic cap; planning headroom** | **2700 s; 174.111394370 s** |

The 600 s is an **unmeasured planning allowance** covering admission/hashing/imports, native projector construction and excluded-energy parity, five saved dense-update SVDs, all five adapter/control families, blocked projections at every cutoff, waits, durability and output. The 50% margin applies to the five measured covariance profiles. It is not a measurement of the remaining work or a certified upper bound. The total cap rounds this envelope up to the next 300-s increment and starts before admission/hashing/imports; waits consume that same budget.

| Peak RSS planning for the complete five-layer stream | GiB |
|---|---:|
| Measured one-layer high-water anchor | **8.056793213** |
| **25% margin envelope, 1.25×anchor** | **10.070991516** |
| **Adopted observed process-family cap; planning headroom** | **11; 0.929008484** |
| Extra retained C32 during this worker's double SVD, absent from MB3's profile | **0.451416016** |
| All 25 saved adapter factor pairs | **0.019454956** |
| Saved dense M64, used after covariance workspace release | **0.167968750** |

Peak RSS is **not multiplied by five**. The worker streams each layer, releases native Vh before the double SVD, lets double input/check workspace go before native-projector/update work, releases C32 after the basis call, and releases layer bases/M before the next layer. The two bases occupy U32 **0.451416016 GiB** and U64 **0.902832031 GiB**; Pnative is another **0.451416016 GiB** during its separate check and is released before update analysis. Known additional C32+adapter residency is about **0.471 GiB**, within the explicit 2.014-GiB profile margin; later M/SVD/control/workspace/allocator/mmap/process-family overhead shares that allowance. These byte-size calculations do **not** establish simultaneous RSS or allocator release. The 10.071-GiB number is a planning envelope for the full sequential workload, not an observed peak.

| Heavy cell | Reserve above 8-GiB floor | Required available GiB |
|---|---:|---:|
| Imports | 1 | 9 |
| Operand load | 2 | 10 |
| Native covariance SVD | 5 | 13 |
| Float64 covariance SVD | **11** | **19** |
| Covariance/native-projector checks | **11** | **19** |
| Update SVD / adapter QR | 2 | 10 |
| Projections | 2 | 10 |
| Random controls | 1 | 9 |
| Output | 1 | 9 |

**Full-workload time, actual process-family peak, every complete-shape reserve, other-layer behavior and nice-10 completion remain UNVERIFIED.** The earlier profiling `/bin/ps` and niceness refusals remain limitations, not admission passes. Keep fail-closed CPU admission before numerical imports, worker/group monitoring, 6-GiB emergency available floor, one-second cadence plus bounded probe latency, supervisor-only acknowledgments, original retry/history/durability protections and the **300-s maximum cell wait**. No cap or reserve auto-adjustment exists. Any later resource/deadline/I/O refusal is STOPPED with no prediction verdict; execution needs separate authorization, a fresh namespace and complete-shape resource validation. This build grants none of those.

### Complete prereg, every pin and launch bindings

The complete launch pin is **`1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f`**. `prereg_pin_check.json` records successful stdlib-only verification of the actual amended document and **INVALID-PREREG refusal of the former complete v2+A1 hash** (`216e8cfab513f0b555d8ae7908bd629e99e3b848cd2b43c054690962572cf771`). It records every current relevant source line. No numerical package was imported by that check. Do not relabel old criteria receipts.

| Binding | Current source |
|---|---|
| Required supervisor launch hash | `tools/new1_supervisor.py:433`, `--prereg-sha` |
| Full-byte/header verification before parent CPU admission | `tools/new1_supervisor.py:66`, :442 |
| Durable criteria receipt using the same hash | `tools/new1_supervisor.py:443` |
| Same pin passed to private worker | `tools/new1_supervisor.py:440` |
| Worker verifies before numerical/import/input work | `tools/new1_geometry.py:501` |
| Worker required CLI and consumption | `tools/new1_geometry.py:571`, :573 |
| Final geometry artifact binds amended prereg and original input pins | `tools/new1_geometry.py:555–556` |

`input_pins.json` records all **20 unchanged input-file pins**, sizes and streaming actual SHA-256 **before and after** this build. No pinned payload was decoded. Full identities:

| Input file | Unchanged SHA-256 |
|---|---|
| `results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A1_single_s0_r16.safetensors` | `23c199f91412da368d5e2c9204cbac06f2153dd8958da572d69c1ba7785cefe1` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/train/A1_single_s0_r16.json` | `11d1dbef51b0babfd8ceb1cb794ff6a84080b0b08da82c84250d7449dbfe99dc` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A2_coherent2_s0_r16.safetensors` | `d5d9832620fb2db0c6f1ed984ef5e79b34361f61efb253ccc873c07885b35e90` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/train/A2_coherent2_s0_r16.json` | `37c32338c1420a2f385e5d8281c97c30fd9b2b6ab5b83ae0a990753b26220e0e` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_canon_s0_r16.safetensors` | `869905010f81fd3c6e006b3a5cf0a809221ac7b5b315f7a3665ee2f58874cd53` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/train/A7_canon_s0_r16.json` | `dd35028e619ed762a6ed430de056f6eb6b3c71153b425eba711b1847dd84e3c4` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_coined_coined_s0_r16.safetensors` | `4e2ae47a450f7014b4d3b003c125796beeb9b37ac94a32f937a65f6187cd124f` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/train/A7_coined_coined_s0_r16.json` | `a4c4757f6251f8600c47689738b0ba0525827018126f543d376fe49794939977` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_shuf_s0_r16.safetensors` | `9ce29297d07622e47d5354bd769b26cc0ce89d07128769cfeea39e84a5df094b` |
| `results/c10w_oracle/p1_20261007T223707_598959Z/train/A7_shuf_s0_r16.json` | `3938136ee161d8afdc55b47798854c8ea92e53badffd23ba5463c3f83194d6a0` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz` | `f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.5.mlp.down_proj_float32_mom2_t100_100000.npz` | `26773779c5f95647c844fb42c553221aa81e48206cb3e61602237b3da4e53b3d` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.6.mlp.down_proj_float32_mom2_t100_100000.npz` | `72a4a42bf7586f1b7de5bfce365263d2a84b66f6ffc4ce20f9fa113d115887fd` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.7.mlp.down_proj_float32_mom2_t100_100000.npz` | `ed2f4c64356fc6388ae4623ccc2bfc9101660fe92a787c193d593a24992aaba5` |
| `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.8.mlp.down_proj_float32_mom2_t100_100000.npz` | `430c1aa56a7cde6626ff02e241b45fd706d02d81d97931536fbed38d8974dd2a` |
| `results/mathlab/harvest_20261009T184950.056951Z/manifest.json` | `bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e` |
| `results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt` | `abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f` |
| `experiments/track_c/c10w_oracle_train.py` | `64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463` |
| `results/c10w_oracle/step0_20261007T223638_531381Z/train_inputs.json` | `d0fa96af0de8d98c5b0fbd90609cd2f2fa1d27a03013c1db9c530e3ec804c050` |
| `results/c10w_oracle/step0_20261007T223638_531381Z/step0.json` | `82ef86437b5ba00fa78a1b55cfe64e4d85baaceb37aa0726f3015c2b2f7d673e` |

Additional unchanged fixed pins: **Qwen/Qwen2.5-3B @ `3aab1f1954e9cc14eb9509a215f9e5ca08227a9b`**; historical harvest prereg **`4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507`**, distinct from this NEW1 launch pin; layers **[4,5,6,7,8]**, original 24-subject order/A7 map identity; saved scale **1.0**, rank **16**, adapter A F32[16,11008]/B F32[2048,16], M F32[2048,11008], caches F32[11008,11008] with positive scalar int64 count. Dependencies were re-probed: **Python 3.11.16, torch 2.8.0, NumPy 2.4.6, safetensors 0.8.0**. Worker CPU/eight threads/nice 10, CPU-only mmap/weights_only bundle load, k=1024, 0.005 native and double count definitions, 256-column blocks, all tolerances and update numerical-rank/tie rules remain fixed.

Random/control pins: **20 draws per layer per family**, NumPy 2.4.6 `Generator(PCG64(20261009+100*l+j))`, j=0…19; output QR then input QR, positive diagonal signs; flat norm match and original nearest-rank **19th-of-20 q95** remain. Spectrum-matched controls reuse those same orientations. Real generated factor/spectrum hashes are **NOT GENERATED / NOT RUN**; their artifacts must be saved/hashed before their statistics on a separately authorized run. Synthetic fixture hashes are not substituted for real controls. Shared CPU admission still checks its own current MathLab prereg/engine/inventories/lead evidence; no new fixed MathLab hash or coordinator clearance was invented.

### Preservation, source hashes and independent review

`scope_audit_before_report.json` rehashes **265 protected files with zero drift**, including MathLab source/prereg files, the historical run directories/receipts, the two ruling artifacts, the A1 diagnostic and measurement receipt. All 20 input hashes also remain unchanged. Complete old prereg **34,841-byte prefix /SHA `216e8cfab513f0b555d8ae7908bd629e99e3b848cd2b43c054690962572cf771`** and report **103,357-byte prefix /SHA `eef2d29a70da1e62492cee43b787eae0305b1b95d5973929ad942686bd7ca2e0`** are preserved byte for byte. Baseline-relative `.diff` files are retained. `git diff --check` passed; the final audit will record the complete appended report SHA and confirm the exact written suffix. No protected record, producer, engine, shared MathLab module, tracker, dashboard or ledger was edited. Existing concurrent worktree changes are not reverted; Graft indexing/cache effects are excluded from protected-file claims.

| Reviewed build file | SHA-256 |
|---|---|
| `tools/new1_geometry.py` | `018ce4d97f817ecd816a4fd3fb47316e78fda7007984449e93f423d0eb1f4a5e` |
| `tools/new1_supervisor.py` | `a69d410724b65a5dbacaf8e34fc45b73c9f545daf54eda9b6cfeb150e344557b` |
| `tests/test_new1_geometry.py` | `57afd2504c9ce065e85be5e5d4237122bea3e329324ff557775cea9e9faa260f` |
| `tests/test_new1_supervisor.py` | `33c61282862cea1d0297396cb860963bfc48adf33d054db3f933fed11d6d23ec` |
| `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md` | `1616c860c38b65acbabb7ec472a1233b30291337e86a7739271df0c4bd1c9d0f` |
| `astra_build_review.md` | `f360001a9d35cc519c104eb6c1cd59c6d8a196957203fd914bf2ce3649192036` |

Fresh reviewer identity is **GPT-6-Astra**, requested review model, with no builder transcript. It read the actual two rulings, full amended prereg, both production/test files, baseline diffs, RED/GREEN records and resource receipt, then re-read the late audit receipts. Its independent checks rehashed the reviewed source files and **15 selected MathLab files**; the 265-file and 20-pin full audits are builder receipts inspected by the reviewer, not an invented independent rerun. The review found **BUILD-ACCEPT, no corrective code request**. It independently reproduced the resource sizing arithmetic and explicitly kept runtime/full-workload science **UNVERIFIED**. Same GPT family means weaker out-of-family independence; this is the operator-requested Astra static review, not a behavioral or execution gate. Exact artifact: `results/mathlab_staging/new1_v2_build_evidence/mb4_20261010_brobust/astra_build_review.md`. The appended report itself receives the builder's final readback/audit rather than an unclaimed additional Astra review.

### Context-save and handoff to MAESTRO2

**Done:** adopted append-only B; RED before production; minimal native/float64 separation and cutoff-band implementation; unchanged margins/native identity/parity; conservative boundary publication; 95-test GREEN; full pin/resource/preservation inventory; actual fresh Astra BUILD-ACCEPT artifact; this append-only report. **In flight:** final report readback/hash/scope validation and local context checkpoint only. **Exact paths:** `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`, `tools/new1_geometry.py`, `tools/new1_supervisor.py`, `tests/test_new1_geometry.py`, `tests/test_new1_supervisor.py`, this report, and durable evidence `results/mathlab_staging/new1_v2_build_evidence/mb4_20261010_brobust/`. **Next:** MAESTRO2 uses the new complete prereg pin to review/handoff the build; any complete-shape validation or real study is separately authorized in a fresh namespace, never an automatic launch. **Open risks:** projected resources/reserves/nice-10/live admission remain UNVERIFIED; real geometry/predictions/control hashes remain NOT RUN; proxy calibration and prospective utility do not exist here. No GPU/model run, commit, deletion or queue promotion follows from this completion.

Context-save is scoped to this report and `checkpoints/new1_brobust.md` under the durable evidence directory, within the user-authorized workspace. Root **/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a**, branch **worktree-c10k-route-a**, initial HEAD **a2deb37e5ecedd14e0a5e3513ea64e4bd3ff00d0**, closeout-observed HEAD **c7e337e1530f7c262077b9d96e1f7850ee8e3c6a**. Status/diff snapshots are recorded locally without mutating Git. This task writes only its named prereg/code/tests/report and build evidence; evidence disk use is recorded in the final manifest. User instructions prohibit commits and leave MathLab untouched.

**Binding context directive restated:** watch **Context N% left** for this and every orchestrated team session; before approximately **20%** remains, stop starting new work, write done/in-flight work, exact paths, next step and open risks into the task report, tell MAESTRO2 and request a fresh successor. Every handoff must restate this rule; never approach full-window compaction. No unfinished builder implementation is being delegated at closeout.
