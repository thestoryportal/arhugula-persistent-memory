You are the cross-family reviewer acting for the team: the operator is asleep and delegated decisions to the team ("All questions are to be decided with the team"; prior authority D-C10r-rulings-14). Rule, with file:line evidence. Read-only.

ASTRA (D-C10z-astra) attempt 3 HALTED at stage 0 on pre-named check V7 (prereg docs/C10Z_ASTRA_PREREG.md :158, :323, :332; diagnostic architecture_profile/c10z_astra_halt_diagnostic_20261009T022838.229295Z.json). Spearman per layer 4–12: .986 .980 .953 .873 .772 .814 .801 .808 .767; bar ≥ .80. Our diagnosis (results/c10z_astra_attempt3/v7_diagnosis.md, profile v7_cache_profile.json): PROPERTY, not a bug — verify it against experiments/track_c/c10z_astra_arms.py (cited lines) and memit layer_stats.py. Also a secondary defect: the halt at :1107 precedes the dstats.pt save at :1113, so m was not saved.

Rule on:
1. Do you agree PROPERTY (not BUG)? If BUG, name the line.
2. The diagnostic probe the diagnosis recommends (~10 GPU-min, forward-only, outside ASTRA; saves m for the frozen first-1,000 rows, 1,000 rows from the cache's own sampler, optionally 5,000 random rows; reports Spearman and median |log(m/cache)| per layer). Is it an admissible measurement that does not read around attempt 3 (D-C10w-p2rerun) and does not count as an ASTRA attempt? What must its pre-registered decision rule be, mapping probe outcomes → amendment option A1 (cache-sampler 1,000 rows) / A2 (5–10k random rows + budget amendment) / C (change V7 statistic) / D (accept HALTED-V7 as ASTRA's outcome)? Fix that mapping NOW, before any probe data exists, so no option is chosen after seeing numbers.
3. Whether option C may be considered at all at this point, and if so its exact statistic and bar, ruled now.
4. The driftcap: a further benchmark re-run would be the third (D-C10z-driftcap sends it to the operator); with the operator's delegation, may the team authorize it, and under what condition?
5. The required driver change to save m before V7 for any attempt 4 — is it a science-path change (LAW#5 isolation needed) or a record-only change?
Give a numbered ruling, then the exact amendment text skeleton the drafter should write.
