# 53 — Value-internal second key: NULL-LARGE-WRITE — modest held-out gain below the frozen advancement margin, with prefix-conditioned spillover on never-edited subjects

_Result 2026-10-07 UTC. Decision-ID D-C10t-secondkey. ⟨D-C10t-secondkey@76a722d3⟩ Pre-registration docs/C10T_SECONDKEY_PREREG.md v2 FROZEN + pre-run ruling D-C10t-p5rule (raw five-layer mean). Source commit 9e88912; all 69 declared hashes verified against that commit and the reviewed files, aggregate source digest 6f40d283905cc7c1e9d490b75e4e8fe23caffba69bb1b6930d4f53974a6313e6. Binding records results/c10t_secondkey_r2/{step0,run,pass1}.json; logs results/c10t_secondkey_logs/r2_{step0,pass1}.log. Run c10t-01e0f527186e421f87fbe3fc5d90e245; pass completed 2026-10-07T08:38:50Z. Engine unmodified, fingerprint d941a9fb/PASS, _cov_cpu=3. Verdict review: results/c10t_secondkey_codex_verdict.md. Lineage: CORPUS/43, CORPUS/44, CORPUS/51–52._

## Pre-registration and claim class

Mechanism screen on the §C write path, key/address definition, read against the §8.9 held-out full-sequence bar: Qwen2.5-3B fp16 MPS, band 4–8, N=24 frozen A7 facts × three held-out templates, one completed process. Keep each canonical subject-key request unchanged; add one value-internal key and an engine-computed remainder target per fact, solved jointly as 48 requests. No Z_OVERRIDE. The second-request KL prompt also changes with its extended subject; this is an address and objective configuration, not an isolated address manipulation.

The prior is NULL in this configuration. Step 0 selects internal positions by base-model surprisal or covariance leverage, subject to alignment admission and the spending screen. A1/A2 must each reach ≥68/72; the single-key reference must be inside [5,18]/72 held-out and [5,10]/24 canonical; fingerprint, LAW#5, observer inertness, provenance, wrapper and admission checks must pass. Failure of validity gives INVALID before any behavioral label.

LEAD requires ≥30/72 with locality held; PARTIAL requires 18<count<30 and gain≥10 over the same-run reference with locality held. A result of that size with a locality failure is TRADEOFF; otherwise NULL. LEAD/PARTIAL require a fresh second process. A write-norm ratio>1.5 appends LARGE-WRITE; it is not a validity or locality gate. The historical envelope is not a calibrated false-positive bound. Sources: docs/C10T_SECONDKEY_PREREG.md:15, :31, :55, :61–71.

## VERDICT — NULL-LARGE-WRITE; candidate not advanced

The rerun is valid. A1=A2=70/72. Observer repeat floor and observed relative distance are both 0.0 at the tested canonical and internal loci (tolerance 0.0001). LAW#5 is INERT: |Δexpr|=0.0, |Δloc|=0.21. Runtime alignment admits all 48 requests; wrapper substitutions candidate=1, duplicate=1, LAW#5=0; Z_OVERRIDE=None, hits=0. Source/positions identities bind. Sources: results/c10t_secondkey_r2/pass1.json:84, :105, :12750, :12766, :27248; results/c10t_secondkey_logs/r2_pass1.log:27–33.

Step 0 gives surprisal non-writable picks 0/24, leverage 15/24; leverage is dropped by the spending screen, not behaviorally falsified. Agreement before/after admission is 15/24, so B10 alone runs. Internal positions j=1/2/3 occur on 1/7/16 facts. Its 48-request digest is fbea3436ea41ad3f47a3f399a5b25ebdd035b3292242018c17ed3b70fff3d05d. The rerun preserves the original scientific selection, ordered facts/tokens and request payloads; new sampled-context audit rows, identity and the reviewed diagnostic-only source fix explain whole-file differences. Within the rerun, the positions-file SHA-256 is cf841b6e7be54b7b476dd32906fa57f530a061f4b950cdc9a4c42aa0da137114. Sources: results/c10t_secondkey_r2/step0.json:73535, :73970; results/c10t_secondkey_r2_selection_compare.json:49; results/c10t_secondkey_r2/run.json:83.

| Same-run arm | Canonical full /24 | Held-out full /72 | Held-out template split | First-token hits /72 | All-three-template facts /24 | Sum of layer ΔW norms |
|---|---:|---:|---|---:|---:|---:|
| A7-single | 7 | 15 | 5 / 5 / 5 | 51 | 2 | 87.382107 |
| A7-dup: canonical requests repeated | 8 | 15 | 5 / 5 / 5 | 51 | 2 | 89.495055 |
| A7-second-B10 | 15 | 23 | 6 / 8 / 9 | 44 | 3 | 179.376003 |

Sources: results/c10t_secondkey_r2/pass1.json:27344, :43287, :72907, :102583, :102610, :102637; rows at :103845, :104423, :105001. String counts equal full-sequence id counts for all three A7 arms.

The candidate's per-fact held-out vector in frozen FICTION order is [1,0,2,0,0,2,0,2,0,3,3,2,0,0,1,0,0,3,0,0,0,2,0,2], summing to 23. Brinduun, Trannak and Kessivar pass all three templates. The candidate gains 15 individual prompt hits and loses seven reference hits: net +8, or 11.1 percentage points, below the required +10-hit margin. Thus 23 outside the envelope is still NULL. Canonical gain +8/24 is non-binding. Source: results/c10t_secondkey_r2/pass1.json:105001; rule: docs/C10T_SECONDKEY_PREREG.md:65–67.

The prescribed summed-layer norm ratio is 179.376003/87.382107=2.052777, adding LARGE-WRITE. This is not a measured overlay-byte or runtime ratio. A7-dup's held-out gain is zero, with the same per-fact/template hit pattern as the reference; REQUEST-COUNT is absent. The duplicate control's norm is only 1.024181 times the reference, so it does not match B10's magnitude. Sources: results/c10t_secondkey_r2/pass1.json:102583, :102610, :102637; docs/C10T_SECONDKEY_PREREG.md:71.

## Locality — per-prefix failures kept beside the gain

F1 supplies each value's selected j-token prefix in the capital frame to six never-edited subjects. Relative to base, A7-single induces zero new next-token or full-remainder hits across the 144 prompts. B10 induces 44 new next-token hits and 18 new full-remainder hits. Ten of 24 per-prefix next-token gates fail (allowed reference+1 of six):

| Prefix identified by edited fact | Reference new next /6 | B10 new next /6 | B10 new full remainder /6 |
|---|---:|---:|---:|
| Zorbland | 0 | 5 | 5 |
| Quaxil | 0 | 2 | 1 |
| Plurnak | 0 | 2 | 2 |
| Glimsto | 0 | 6 | 3 |
| Mophgar | 0 | 6 | 0 |
| Zephquin | 0 | 2 | 1 |
| Pradnoll | 0 | 6 | 0 |
| Halquin | 0 | 4 | 0 |
| Vorlex | 0 | 3 | 0 |
| Quenby | 0 | 6 | 6 |

The other 14 gates pass; Drennik and Skornwell each add one next-token hit within slack, bringing the total to 44. These are induced completions on prompts with the gold prefix supplied, not spontaneous recall on unprefixed bystanders. “Prefix” means all tokens through the chosen internal key, not uniformly the first BPE piece. Sources: results/c10t_secondkey_r2/pass1.json:27418, :72981; docs/C10T_SECONDKEY_PREREG.md:48, :69.

The remaining gates pass: L1 flips 0→0/12; F0 flips 1→1/6; L3 agreement 30→30/30; described-as 87.16→87.89 (floor 84.16); generic perplexity 21.743→21.723 (ceiling 22.243). Those probes do not erase the prefix-conditioned failure. The neutral “The name is <prefix>” probe changes from zero to four next-token and one full-remainder hit out of 24. One full hit does not exceed reference+1, so SUBJECT-FREE is absent; this is not proof of subject dependence. The is-a and associated-with probes remain diagnostics, not additional frozen gates. Sources: results/c10t_secondkey_r2/pass1.json:27344, :72907, :28166, :73729, :74151.

The F1 failures would make a PARTIAL- or LEAD-sized gain TRADEOFF. Here +8 is unsized, so the label remains NULL-LARGE-WRITE while the failed locality axis is recorded explicitly. No second process is triggered or pending; this is not a replicated result. Sources: docs/C10T_SECONDKEY_PREREG.md:55, :66–71; experiments/track_c/c10t_secondkey_read.py:182, :425.

## Mechanism — what this resolves and does not resolve

EVIDENCE-SHOWS: in this process the second-key configuration increases full-sequence held-out recall from 15 to 23 and canonical recall from 7 to 15, at about twice the summed write norm and with value-prefix-conditioned spillover across unedited subjects. The duplicate control does not produce the held-out gain. Continuation diagnostics improve (teacher-forced continuation 64.5%→77.5%; P(full|first) 0.294→0.523), but first-token success falls 51→44 and natural reach of the selected prefix falls 48→41/72. Sources: results/c10t_secondkey_r2/pass1.json:27344, :72907, :28314, :73877.

I-INFER: a value-internal key can reinforce prefix→remainder completion without sufficiently preserving the written subject's scope. This supports the bleed component of H-T2, not a unique causal account of the +8 or a demonstration that all keys are subject-free. The reference-sized canonical duplication control weakens a request-count-only explanation but does not separate the candidate's added address, remainder target, KL objective and larger write. Joint-solve interference and small process/numerical effects remain alternatives; no new experiment here separates them.

Step-0 median cross-template cosine is 0.995322 for second keys versus 0.988231 for subject keys, so H-T4 is not the standing reading. These measurements supply the gold prefix; they do not guarantee that free generation reaches it. During the solve, second-block raw key means 0.052–0.091 and effective ranks 9.75–13.38, and projected-key means 0.033–0.043/ranks 7.10–13.80, do not show the global near-rank-one collapse seen for CORPUS/43's frame keys. Some pairs are nearly collinear; the aggregates alone do not explain which prefixes bleed. Sources: results/c10t_secondkey_r2/step0.json:75959; results/c10t_secondkey_r2/pass1.json:76173.

Subject-key remaining-residual fractions worsen from 0.032650/0.233728 (canonical/held-out) to 0.087119/0.344323 under B10; its value-internal fractions are 0.301390/0.400941. These are norm fractions remaining, not recall or percentages of facts installed; held-out internal measurements are conditioned on the gold prefix. Second-request teacher-forced fit at stop has median 0.993061 and minimum 0.097786; 14/24 exhaust the 25-evaluation budget, all 24 hit the clamp. Fit heterogeneity is recorded, not an unfrozen invalidity criterion. Sources: results/c10t_secondkey_r2/pass1.json:30083, :89040, :74681; docs/C10T_SECONDKEY_PREREG.md:53, :61.

## Caveats kept flush

One completed process, 24 facts, one relation label, one admitted position per fact and one solve budget; the numerical +8 is not a replicated or calibrated-significant effect. B5 was dropped for spending, not tested. The prefixes in F1 are supplied, and the held-out internal-position geometry is teacher-forced. H-T1 is not earned: the result is NULL and locality fails. A7-dup controls canonical request duplication, not write magnitude or the target/KL changes. Passing the observer checks at two loci and the standing LAW#5 test is scoped evidence, not exhaustive equivalence across every intervention.

The first attempt HALTED at a diagnostic MPS float64 conversion, with no completed pass artifact. The reviewed fix moves four diagnostic readouts to CPU before the float64 upcast; the fresh rerun has its own identity and complete controls. Published scientific selection/request contents are preserved despite changed sampled-context audit rows. This is a repaired rerun, not two scientific replicates. Sources: architecture_profile/c10t_secondkey_halt_diagnostic.json:81; results/c10t_secondkey_fix2_codex_review.md; results/c10t_secondkey_r2_selection_compare.json:49.

No existing CORPUS label is revised. This configuration's non-advancement does not falsify internal keys in general, H-10/H-5, the frame account or other realization recipes. The research sequence's old “3% installed” premise is not reused: the relevant residual statistic is a fraction remaining. The held-out 23/72 remains below the 61/72 program bar and fails prefix locality; this is no §8.9 closure, route closure, CPU/quantization validation or F1 readiness change. C10 remains OPEN/BLOCKING. Sources: docs/C10T_SECONDKEY_PREREG.md:11, :13, :82; results/research_pass_2026-10-06/recommended_sequence.md:36.

## Decision-ID and FORK

D-C10t-secondkey: valid NULL-LARGE-WRITE with ten failed per-prefix locality gates; candidate not advanced; no replication pending. H-10/H-5 remain open with a NOT-ADVANCED note scoped to this configuration; H-5's arm was spending-screened out, not behaviorally falsified.

Continue the agreed sequence to step 3, D-C10u-mint2 ⟨D-C10u-mint2@5c772e4a⟩ v3: both separate blocks, with block F's mint-1(frozen) seed reproduction gate first, then F, then V2, retaining the bigram/subject-swap and per-position diagnostics. Step 4, D-C10v-layerpick v2, follows step 3 under its own gates. No adoption of step 1's unadvanced shared target or this second-key recipe; engine steps 6–7 retain their later place. Sources: docs/C10U_MINT2_PREREG.md:9, :76–78; docs/C10V_LAYERPICK_PREREG.md:86; docs/C10T_SECONDKEY_PREREG.md:75–77.

Candidate only: a separately pre-registered write-size-matched second-key control with the same prefix-gate family could test whether the modest continuation improvement survives a reference-sized displacement and whether spillover changes with that budget. It would narrow one confound, not identify a subject-address mechanism by itself; no run or adoption is implied.

_Text proposed by the Codex verdict review (`results/c10t_secondkey_codex_verdict.md` §5) and adopted by the program session under D-C10r-rulings-8._
