**Accept the recorded MATH-PROXY outcome, subject to the reporting corrections below.** The arithmetic completed; H-COV is BOUNDARY-SENSITIVE and NON-SPECIFIC; no queue change follows. (`geometry.json:18161–18173`; `dispatch_receipt.json:72–108`; `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md:210–212`.)

Citations below use these exact directories:

- Run files: `results/mathlab_staging/runs/new1_20261010T235740.858576Z/`
- Dispatch files: `results/mathlab_staging/new1_dispatch_20261010T235738.2180209160Z/`
- Outcome note: `results/mathlab_staging/new1_outcome_20261011/maestro_outcome_note.md`
- “Prereg” means `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`.

**Q1. C1 and C5 are CLOSED at dispatch, with a separate quiet-host deviation during execution.**

Recorder and supervisor niceness were 0; the identified worker was observed at absolute niceness 10. This establishes the required initial observation, not continuous niceness enforcement. (`recorder.json:1`; `supervisor.json:1`; `worker.json:1`; `results/mathlab_staging/new1_launch_closure_astra.md:21`.)

Disk availability was 83,955,632 KiB against the 22,020,096-KiB floor. Fingerprint and dry admission passed before consumption; the pinned recorder orders those checks before writing `invocation.json`. Supervisor admission then independently passed before numerical imports. (`disk.json:1`; `2g.json:1`; `2h.json:1`; `tools/new1_dispatch.sh:169–209`; `events.jsonl:3–8`.)

The record supports one consumed authorization and one resulting namespace, COMPLETE execution, CLEAN worker/group disposition, no stop, and zero resource/deadline aborts. “No live processes” should mean the monitored worker/group, not an empty host. (`invocation.json:1`; `dispatch_receipt.json:45–108`; `tools/new1_dispatch.sh:288–302`.)

Do **not** extend dispatch closure into “the host remained quiet throughout”: the previous closure required that coordination, and MAESTRO reports violating it after admission. (`results/mathlab_staging/new1_launch_closure_astra.md:9`; `maestro_outcome_note.md:33`.)

**Q2. The prediction labels follow from geometry.json.**

I independently recalculated the margins and the nearest-rank q95 values from the saved flat-spectrum draws. The required thresholds are unchanged: H-COV needs excluded energy ≥0.25, excess over M ≥0.15, and excess over random q95 ≥0.10. (`Prereg:85–92,210`; `geometry.json:709–2275,4536–5986,8095–9545,11654–13104,15213–16663`.)

| Layer / cutoff | EX(D) | EX(D)−EX(M) | EX(D)−q95(random) | Nominal |
|---|---:|---:|---:|---|
| L4 / 2363 | 0.273876 | 0.270936 | 0.056614 | FAIL |
| L4 / 2364 | 0.273940 | 0.270401 | 0.056548 | FAIL |
| L5 / 3889 | 0.542227 | 0.542226 | 0.185402 | PASS |
| L6 / 5270 | 0.534583 | 0.534580 | 0.054096 | FAIL |
| L7 / 6843 | 0.679731 | 0.679725 | 0.056189 | FAIL |
| L8 / 9425 | 0.904324 | 0.904145 | 0.045928 | FAIL |

Sources, respectively: `geometry.json:3880–3921,7459–7480,11018–11039,14577–14598,18136–18157`.

Only **L5** passes every cutoff in its inclusive band: **1/5**, below the required same-layer ≥3/5. All five fixed layers and their applicable cutoffs are present. Therefore **BOUNDARY-SENSITIVE** is correct; neither aggregate FAIL nor missing-data INVALID is correct. (`geometry.json:31–66,3925–3958,7484–7517,11043–11076,14602–14635,18167–18169`; `Prereg:206–210`.)

Crucially, **no layer’s nominal result flips across cutoffs**. BOUNDARY-SENSITIVE is the amendment’s prescribed label for failing the robust aggregate; it must not be paraphrased as an observed cutoff-induced reversal. (`geometry.json:3880–3921,7459–7480,11018–11039,14577–14598,18136–18157`; `Prereg:210`.)

The other endpoints give:

| Layer | H-TOP: ΔT / excess over q95 | H-RANK: rD / rM / ratio | H-OVERLAP: O16 / excess over q95 |
|---|---|---|---|
| 4 | 0.204128 / 0.109843 | 1.042376 / 19.930520 / 0.052300 | 0.004891 / 0.003341 |
| 5 | 0.315770 / 0.221321 | 1.250951 / 19.407699 / 0.064456 | 0.016987 / 0.015350 |
| 6 | 0.283222 / 0.188631 | 1.363359 / 18.154076 / 0.075099 | 0.012955 / 0.011276 |
| 7 | 0.348960 / 0.254985 | 1.337089 / 21.022064 / 0.063604 | 0.004154 / 0.002561 |
| 8 | 0.378608 / 0.285092 | 1.329730 / 21.828227 / 0.060918 | 0.002001 / 0.000390 |

Sources: `geometry.json:525–618,2274–2275`; `:4386–4461,5985–5986`; `:7945–8020,9544–9545`; `:11504–11579,13103–13104`; `:15063–15138,16662–16663`.

Thus:

- **H-TOP PASS, 5/5:** both ≥0.10 contrast and ≥0.05 random-excess margins hold together.
- **H-RANK FAIL, 0/5:** neither rD≥8 nor ratio≥1.25 holds.
- **H-OVERLAP FAIL, 0/5:** O16≤0.25 holds, but the required ≥0.05 random excess fails everywhere.

These apply the same-layer rule without mixing layers across conditions. (`Prereg:85–92`; geometry sources immediately above.)

Shuffle differences are **0.004207 / 0.004205** for L4’s two cutoffs, then **0.005256, 0.001388, 0.029207, 0.013029** for L5–L8. Every comparison is ≤0.05: **all five layers are shuffle-near at every applicable cutoff**, so **NON-SPECIFIC applies**. It blocks semantic-specific interpretation; it does not invalidate otherwise complete geometry. (`geometry.json:3880–3921,7459–7480,11018–11039,14577–14598,18136–18157`; `Prereg:94,212`.)

**Q3. INVALID / rc 3 is the required conservative encoding here.**

H-COV’s stage records INVALID while retaining literal BOUNDARY-SENSITIVE, without a Boolean H-COV prediction gate. The arithmetic stage finishes successfully; the terminal envelope is INVALID. The supervisor maps that outcome to exit 3. There is no additional abort or stop recorded. (`events.jsonl:1648–1662`; `tools/new1_supervisor.py:586–595,646–648`; `dispatch_receipt.json:77–108`; `Prereg:212`.)

The reporter’s “no prediction verdict” is its conservative envelope wording; the individual artifact labels remain separately readable. Do not translate COMPLETE into a scientific PASS. (`tools/new1_dispatch_report.py:35–42`; `finding.json:2–11`; `Prereg:83`.)

**Q4. No queue change is correct.**

BOUNDARY-SENSITIVE explicitly yields no geometry-specific recommendation; NON-SPECIFIC independently blocks semantic-specific interpretation. H-TOP alone does not activate the H-COV PASS row. (`Prereg:139,143,212`; `finding.json:11`.)

The conditional rows that could change priority are H-COV PASS, H-COV FAIL, and H-OVERLAP PASS—each still subject to calibration and demonstrated prospective utility. None authorizes a change for this result; the amendment supersedes aggregate H-COV FAIL, and H-OVERLAP/rank failure preserves existing order. (`Prereg:135–142,210–212`.)

**Q5. No demonstrated measurement compromise requires a rerun, but the note is not entirely free of overclaim.**

- **Brief Python process:** its duration, exact command, and absence of writes are **UNVERIFIED beyond MAESTRO’s account**. It violates the reported quiet-host obligation; successful initial admission cannot certify later host exclusivity. Recorded resource observations show no breach: minimum available memory **20.152191 GiB**, maximum family RSS **8.643097 GiB**. These are sampled extrema, not continuous guarantees. (`maestro_outcome_note.md:33`; `events.jsonl:411,1281`; `Prereg:115,218,222`.)
- **Memory-drop wording:** the actual nearby sequence is **23.173782 → 20.859085 → 21.417648 GiB**, with RSS **3.770401 → 7.382309 GiB**. The SVD gate coincides with it, but causal attribution excluding the external process is UNVERIFIED. Replace “never fell below” with “minimum sampled available memory.” (`events.jsonl:95–98`; `maestro_outcome_note.md:33`.)
- **`mv` warning:** check 2a records successful directory creation, and its capture survives. The claimed warning’s original stream and ownership explanation are **UNVERIFIED from the supplied capture**; the note is the available account. This is not evidence of damaged numerical artifacts. (`2a.json:1`; `maestro_outcome_note.md:34`.)
- **Dashboard poll:** pausing it is consistent with C5. Byte-identical restoration is **UNVERIFIED beyond the note**; the admission receipt verifies only that its sampled inventory had no blockers. (`maestro_outcome_note.md:35`; `results/mathlab_staging/new1_launch_c4_20261011/launch_manifest.md:28–30`; `receipts/admission_aaa9300344584a8e9f5792b009dbfa9f.json:15–20`.)

The rerun rule applies to halted or compromised measurements. This record completed, and these deviations do not establish such compromise; no rerun is required on the supplied evidence. This is not certification that every reported external action was harmless. (`memory_mirror/rerun-never-patch.md:7–11`; `events.jsonl:1642,1659–1662`.)

**Conditions before tracker propagation:**

1. Add the verified **NON-SPECIFIC** reading and preserve the distinction between BOUNDARY-SENSITIVE and an observed cutoff reversal. (`maestro_outcome_note.md:29`; `geometry.json:18167–18170`; `Prereg:210–212`.)
2. Correct the resource wording/numbers and label the external-process, warning-provenance, and dashboard-restoration details as MAESTRO-reported where independent verification is absent. Preserve the quiet-host deviation rather than claiming continuous C5 compliance. (`maestro_outcome_note.md:33–35`; `events.jsonl:95–98,411,1281`.)

**Q6. Propagate this exact outcome sentence**, supported by `finding.json:2–11`, `geometry.json:18167–18173`, and `dispatch_receipt.json:72–108`:

> D-NEW1-b: one authorized execution COMPLETE/CLEAN; MATH-PROXY—math estimate, not evidence; H-COV BOUNDARY-SENSITIVE, excluded-energy contrast NON-SPECIFIC, H-TOP PASS, H-RANK FAIL, H-OVERLAP FAIL; INVALID envelope/rc 3 as prescribed; no queue change; quiet-host deviation retained.

Do not claim semantic specificity, behavioral causation, recall/locality improvement, native/float64 subspace equivalence, F1 closure, general resource guarantees, or permission for another invocation. (`Prereg:3,105,202,208,212,218`; `results/mathlab_staging/new1_launch_c4_20261011/new1_b2_one_invocation_authorization.md:16–18`.)

VERDICT: ACCEPT-WITH-CONDITIONS
