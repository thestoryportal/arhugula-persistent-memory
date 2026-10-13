# Group B leftovers: closed experiment scripts on the legacy output roots

These scripts belong to closed experiments and still use pre-v2 paths. Under policy B (G5) they are left as they are. Their output roots (`results/`, `architecture_profile/`, `logs/`) are ignored by `.gitignore`, so a re-run writes locally and never into git. Their other references name pre-v2 code or tool paths, or paths inside test fixtures, and a re-run that needs a moved file fails loudly. A script that becomes live again is repointed through `code/state/llmdb_records.py` first, and its output goes to its record's `runs/<slug>/`.

Generated from `unresolved-by-group.json` (sha256 `4291e5412a30d8e5b13a9fdda8cfdbaa7ed79f0804629f61dbc4eb5ef284dd2f`), key `B-closed-experiment-scripts`: 277 references in 49 scripts.

| Root | References |
|---|---|
| `results` | 136 |
| `logs` | 59 |
| `architecture_profile` | 53 |
| `tools` | 12 |
| `.claude` | 8 |
| `graft` | 5 |
| `docs` | 2 |
| `memit_dry_run` | 1 |
| `experiments` | 1 |

| Script | References | Roots | Lines |
|---|---|---|---|
| `code/lab/track_b/b1_size_dose_response.py` | 3 | `architecture_profile`, `results` | 128, 144, 224 |
| `code/lab/track_b/b3_run.sh` | 2 | `logs` | 19, 28 |
| `code/lab/track_c/autoresearch_band_search/run_edit.py` | 2 | `results` | 250 |
| `code/lab/track_c/autoresearch_c10/launch.sh` | 1 | `.claude` | 5 |
| `code/lab/track_c/autoresearch_c10/replay_exp2/lock_clone.py` | 3 | `graft` | 18, 19, 85 |
| `code/lab/track_c/autoresearch_c10/replay_exp2/read_replay.py` | 1 | `.claude` | 16 |
| `code/lab/track_c/autoresearch_c10/run_equivalence_tmux.sh` | 1 | `.claude` | 5 |
| `code/lab/track_c/autoresearch_c10/start_tmux.sh` | 1 | `.claude` | 5 |
| `code/lab/track_c/autoresearch_c10/test_plumbing.py` | 1 | `graft` | 95 |
| `code/lab/track_c/autoresearch_c10/v13_graft.py` | 1 | `graft` | 104 |
| `code/lab/track_c/autoresearch_c10/v13_law3_equivalence.sh` | 1 | `.claude` | 8 |
| `code/lab/track_c/autoresearch_c10/watch_audit.sh` | 1 | `.claude` | 5 |
| `code/lab/track_c/autoresearch_reaim/program.md` | 1 | `memit_dry_run` | 32 |
| `code/lab/track_c/band_corruption_compare.py` | 2 | `logs`, `results` | 48, 53 |
| `code/lab/track_c/c10h_anyedit_pilot.py` | 1 | `results` | 144 |
| `code/lab/track_c/c10k_route_a_gate_v2.py` | 2 | `logs` | 79 |
| `code/lab/track_c/c10k_route_a_launcher.py` | 2 | `experiments`, `logs` | 5, 230 |
| `code/lab/track_c/c10s_sharedz_arms.py` | 1 | `results` | 9 |
| `code/lab/track_c/c10s_sharedz_read.py` | 1 | `architecture_profile` | 67 |
| `code/lab/track_c/c10s_sharedz_selftest.py` | 1 | `architecture_profile` | 319 |
| `code/lab/track_c/c10u_mint2_arms.py` | 6 | `logs` | 1002, 1006, 1009, 1013, 1046, 1048 |
| `code/lab/track_c/c10v_layerpick_arms.py` | 1 | `architecture_profile` | 52 |
| `code/lab/track_c/c10v_layerpick_selftest.py` | 2 | `architecture_profile` | 635, 701 |
| `code/lab/track_c/c10w_oracle_selftest.py` | 39 | `architecture_profile`, `logs`, `results`, `tools` | 1648, 1677, 1683, 1684, 1687, 1698, 1776, 1795, 1806, 1962, 1982, 2060, 2086, 2088, 2101, 2102, 2104, 2120, 2125, 2126, 2140, 2174, 2178, 2190, 2194, 2195, 2197, 2198, 2199, 2200, 2201, 2202, 2203, 2233, 2234, 2246 |
| `code/lab/track_c/c10w_oracle_step0.py` | 1 | `architecture_profile` | 431 |
| `code/lab/track_c/c10x_enginepath_arms.py` | 12 | `architecture_profile`, `logs`, `results` | 195, 216, 287, 1399, 1405, 1409, 1451, 1462, 1468, 1475, 1477, 1482 |
| `code/lab/track_c/c10x_enginepath_read.py` | 1 | `results` | 1143 |
| `code/lab/track_c/c10x_enginepath_selftest.py` | 35 | `architecture_profile`, `logs`, `results` | 536, 679, 683, 725, 774, 831, 847, 875, 907, 957, 975, 1028, 1042, 1057, 1239, 1296, 1382, 1402, 1408, 1427, 1429, 1433, 1538, 1913, 1928, 1941, 1945, 2052, 2081, 2383 |
| `code/lab/track_c/c10x_enginepath_telemetry_check.py` | 3 | `results` | 53, 416, 432 |
| `code/lab/track_c/c10x_x2_probe.py` | 5 | `docs`, `results` | 363, 576, 647, 652 |
| `code/lab/track_c/c10y_directdw_arms.py` | 10 | `architecture_profile`, `logs`, `results` | 918, 923, 963, 1152, 1281, 1295, 1444, 1540, 1642, 1645 |
| `code/lab/track_c/c10y_directdw_selftest.py` | 69 | `.claude`, `architecture_profile`, `results` | 129, 130, 131, 132, 345, 352, 574, 757, 806, 807, 839, 928, 2170, 2217, 2235, 2327, 2328, 2332, 2339, 2347, 3124, 3136, 3137, 3143, 3147, 3160, 3168, 3177, 3187, 3206, 3239, 3247, 3253, 3412, 3475, 3641, 3841, 3857, 3858, 3917, 3930, 3945, 4085, 4093, 4095, 4609, 4610, 4633, 4635, 4681, 4682, 4757, 4762, 4796, 4797, 4837, 4856, 4959, 5096 |
| `code/lab/track_c/c10y_directdw_telemetry_check.py` | 2 | `results` | 50, 82 |
| `code/lab/track_c/c10y_precast_diag_selftest.py` | 3 | `docs`, `results`, `tools` | 258, 287, 755 |
| `code/lab/track_c/c10z_astra_arms.py` | 6 | `architecture_profile`, `logs`, `results` | 1661, 1730, 1765, 1766, 1849, 1887 |
| `code/lab/track_c/c10z_astra_benchmark_selftest.py` | 1 | `results` | 654 |
| `code/lab/track_c/c10z_astra_selftest.py` | 23 | `architecture_profile`, `logs`, `results`, `tools` | 385, 453, 1492, 1517, 1562, 1633, 1647, 1667, 1702, 1797, 2070, 2238, 2375, 2414, 2421, 2429, 2443, 2560, 2617, 2639, 3295, 3298, 3307 |
| `code/lab/track_c/c10z_astra_telemetry_check.py` | 2 | `results` | 41, 43 |
| `code/lab/track_c/c10z_v7_diag.py` | 1 | `tools` | 432 |
| `code/lab/track_c/c10z_v7_diag_selftest.py` | 3 | `tools` | 28, 409, 689 |
| `code/lab/track_d/c1_conditioning_diag.py` | 2 | `results` | 128, 129 |
| `code/lab/track_d/c1_kvc_grid.py` | 1 | `results` | 220 |
| `code/lab/track_d/d1_concentration_sweep.py` | 1 | `results` | 235 |
| `code/lab/track_d/d1_predictor_map.py` | 1 | `results` | 97 |
| `code/lab/track_d/d1_threshold_instrument.py` | 12 | `architecture_profile`, `results` | 148, 160, 228, 229, 275, 278, 317, 321, 354, 355, 360, 361 |
| `code/lab/track_d/d20_subbatch_sweep.py` | 1 | `results` | 214 |
| `code/lab/track_d/run_instrument_diagnostic.sh` | 2 | `logs` | 21, 31 |
| `code/lab/track_d/run_lowk_after_matrix.sh` | 2 | `logs` | 5, 9 |
| `code/lab/track_d/run_threshold_matrix.sh` | 1 | `logs` | 19 |
