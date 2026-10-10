FIX-FIRST

Notation: **D** = `experiments/track_c/c10y_precast_diag.py`; **R** = `results/c10y_precast_diag/20261009T225619Z`; **S** = `R/OPERANDS_MANIFEST_sizes.txt`; **B** = `results/c10y_precast_diag/amendment_budget_draft.md`.

1. **The current-writer ledger checks out.** My read-only `/opt/homebrew/bin/rtk proxy /opt/homebrew/bin/node -e …` audits independently reconstructed all 13 families in (a): **622 packets / 117,364,108,482 B**, including **131 manifest packets / 112,269,967,565 B**. Every family count and byte total agrees. The audit compared retained-file sizes, parsed JSON tensor descriptors, and checked every completed L4/L5 corresponding packet size; it did not load tensors or verify archived payloads.

   Specific (b) checks:

   | Family | Verified bytes × projected count | Evidence |
   |---|---:|---|
   | Pristine | 6,172,004,127 × 1 | S:112; D:644–646 |
   | Projectors | 2,423,523,673 × 1 | S:113; D:653–658 |
   | Q intermediates | 486,819,809 × 30 | S:83; D:285–305 |
   | Native factors | 488,270,357 × 10 | S:76; D:360–369 |
   | Float64 system | 1,152,272,541 × 10 | S:25; D:461–464 |
   | Realizations | 225,445,669 × 160 | S:7; D:578–584 |
   | Aggregate updates | 1,893,733,235 × 10 | S:129; D:565–576 |

   JSON checks confirmed the corresponding dimensions/dtypes, including `[2048,11008]` updates and fp16 weights plus fp64 realized differences (`R/controls_A7_coined_coined_L4_realized_recipe_A.json:9–25`).

   **16 candidates/cell** is correct: seven at D:565–574 plus nine at D:459–480. Thus **120 update pairs + 16 weight comparisons = 136 packets/cell**, or **1,360 across ten cells**, not per cell (D:586–591). Twelve additional statistic groups reside inside each numeric packet (D:600–603).

   All 32 multiplication rows passed arithmetic checks. The reconstructed projection is **2,103 .pt packets / 271,939,207,019 B**, plus estimated JSON, giving **293,436,873,323 B including reserve** (B:199–205). Remaining row sizes were checked through inventory/histograms; **A1 native/control equivalence and unwritten cells remain UNVERIFIED projections**, not observed writes.

2. **B1/B4 require retained evidence, not redundant serialization.** References are compatible with `docs/C10Y_PRECAST_DIAG_SCOPE.md:19–23,69–71` if they resolve to immutable, already-fsynced full payloads and predicates still evaluate verified, decoded inputs.

   | Replace duplicate payload with references to | Full-run bytes removed |
   |---|---:|
   | Previously saved observer snapshots | 23,024,320,516 |
   | Previously saved device off/on weights | 2,705,380,950 |
   | Previously saved individual pre-cast updates | 18,937,332,350 |
   | Recipe-A operand packet plus saved common-factor X | 17,739,288,250 |

   These follow respectively from D:429–432; D:505–508; D:457–480,565–576; and D:455,558–565, using S:81–82,129,4 and the audited coverage-file sizes.

   The first three reduce the floor to **248,769,839,507 B**; including control-input references gives **231,030,551,257 B = 215.164 GiB**, **plus new reference metadata/scratch**. These are conditional budgets, not measured rewritten output.

   **All require reviewed writer/reader behavior**, source repinning and failure tests (D:44–60,89–106). Never assume observer-on equals observer-off; preserve both actual observations. Likewise, the realized packets cannot replace pre-cast updates: casting loses information, while frozen measurement 5 independently requires realized weights/differences (`scope:38`; D:578–584). Further native-copy deduplication is **unchecked and receives no savings credit**.

3. **No currently validated option admits dispatch, but larger storage is not proven unavoidable.** A concrete candidate combines those four reference changes with verified Drive archival of each path’s snapshots immediately after its inertness gate, each completed control cell, and each completed arm’s remaining native records. Snapshots have no subsequent reads in native comparison (D:432–448).

   My Node calculation gives conservative tensor peaks of **66,392,659,826 B during native capture** and **67,653,245,654 B during controls**. Adding the existing JSON allowance and reserve yields **89,150,911,958 B = 83.028 GiB**, before new overhead. Inputs are the audited subtotals and S:98,100 snapshot sizes.

   Live `fs.statfsSync('/Volumes/memit',{bigint:true})` showed **91,812,069,376 B available**: only **2,661,157,418 B** remains for additional overhead. This is a potentially fitting schedule, **not admission evidence**. It requires authorized archival, verified remote durability, fail-closed transfer handling, bounded scratch/time, and explicit acceptance of peak-occupancy accounting under `EXPERIMENT_RUNBOOK.md:263`.

4. **Accept Z4’s baseline arithmetic; fix the incomplete storage recommendation.** A larger volume is defensible for the unchanged writer. It is not established as necessary after evidence-preserving references and earlier archival. Z4 correctly acknowledges that its 108.139 GiB schedule is not universal (B:219–223), but omits a quantitatively material alternative.

Required fixes:

1. Add the reference option, conditional floors, and pre-cast-versus-realized distinction.
2. Add a last-use archival schedule with measured overhead, failure behavior, replay and time bounds.
3. Qualify the recommendation as the unchanged-writer option; retain dispatch blocking until implementation review and fresh disk admission.

🌱 graft reported ~187,865 tokens saved (~$0.11), 1 successful call.

