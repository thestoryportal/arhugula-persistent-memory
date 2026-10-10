CONFIRM

1. **Independent recomputation confirms UNDERFIT-LARGE-WRITE-SUBJECT-FREE-STAGE1.** Below, P=`docs/C10Z_ASTRA_PREREG.md`, E=`results/c10z_astra_attempt4/pass_p1.json`, R=`experiments/track_c/c10z_astra_read.py`.

   I ran `/opt/homebrew/bin/rtk proxy .venv/bin/python -B experiments/track_c/c10z_astra_read.py results/c10z_astra_attempt4`: exit **0**, `scientific_verdict=true`, exact classification above, `next_stage=null`.

   Independently summing the recorded per-prompt hits gives **n=14/72**, **a=12/72**, **gain=2**. Both K1 count predicates fail: 14<19 and 2<10 (E:453285,658638; P:265).

   Recounting the final native leads gives **m=103, M=792**: **20m=2,060 < 19M=15,048**. Positive identity facts=**18<23**; canonical successes=**18<23**. Thus **all three FIT predicates fail** (E:654147–654153,658858; P:229–234; R:112–124).

   | Gate | Recomputed comparison | Result |
   |---|---|---|
   | G1 | 12 flips > 0+1 | false |
   | G2 | Z views [5,6,6,6,6,5]; A [1,0,1,1,2,0]; every Z>A+1 | false |
   | G3 | 89.36 ≥ 89.31−3=86.31 | true |
   | G4 | 1 agreement <29 | false |
   | G5 | 56.216 >21.606+0.5=22.106 | false |
   | G7 | 1,040/1,296 cell/hit-type comparisons fail; example (view=0,fact=0,depth=3,next): 6>0+1 | false |

   Sources: E:452953–453279,658306–658632; F0 E:445830,651184; prefix records E:454599,660758; rules R:299–349.

   Decoding stored pristine/final fp16 weights gives median relative column change **≈0.672940>0.55**: LARGE-WRITE. Recomputing subject-free hits from generated IDs gives **21 facts versus A’s 1**, exceeding 1+1: SUBJECT-FREE. Write time **1,091.841 seconds<3,600**, so no EXCEEDS-TTL (E:646254,852406,864114,867973; P:272–274). T1 yields NULL, rule U replaces it with UNDERFIT, and K1 adds STAGE1 (P:253,261,265). `run.json:8–18` confirms closed=true, completed=1, halt=null.

2. **Permitted close-out sentence:** “Under the frozen attempt-4 configuration and exact R1000 reference population, this single-process, stage-1 test on 24 A7 facts failed advancement: held-out recall was 14/72 versus 12/72 for recipe A, with UNDERFIT, excessive carrier-column changes, and locality/subject-free violations.”

   UNDERFIT means **inconclusive under this solve budget**, not a fitted null or demonstrated paraphrase-transfer ceiling (P:261). Forbid generalizing to ASTRA generally, other populations/configurations/models, or inability to store values (P:46). H-Z2 is not established because FIT failed (P:52). G0, Z-band attribution and replication were unrun; artifact identity and numerical reproduction remain NOT-EVALUATED—not failed (P:265–267). No route, compaction, deployment or real-time qualification follows (P:42).

3. **Terminal under the currently frozen authorization.** K1 closes this count-killed run; stage 2 and process 2 are not permitted (P:265–266). The separately budgeted diagnostic provision concerns a **disqualified count survivor**; this result is not one (P:265). §12 authorizes the specific attempt 4, fixes R1000, and grants no further population search, redraw, automatic retry or amendment branch (P:834–835,868–870). New experimental work would require separate prospective authorization; terminal here does not mean universally falsified.

graft savings: unreported; lookup failed.
