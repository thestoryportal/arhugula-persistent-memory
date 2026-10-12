# Quarantined selftest leak (2026-10-08 ~01:55 MDT, program session)

Created at 01:50:56-01:51:01 MDT by a test in experiments/track_c/c10w_oracle_selftest.py run by the codexw2 build (P2-rerun brief); the test dispatched a real P2 training stage against the live tree; it halted on INVALID-ENVIRONMENT (no MPS in the Codex sandbox; no GPU used). Not a science record. Moved here so tools/run_c10w_p2.sh newest_p2() never selects it. Never delete. SHA-256 before the move:

d6f619bd94138484f8e27886efdd0fb889ed532f8ae123eca99aedde0a9da808  results/c10w_oracle/p2_20261008T075056_661871Z/p2-a7-s1.log
b3af96deb8eda65aa60dd1dd7a63275c782e577f7b88b3d87e0c4e035103c1ff  results/c10w_oracle/p2_20261008T075056_661871Z/HALT.json
12b0c539786dada7a46665cc351ad79a8746f0f8073665243ed1e6eefbb8f3a3  results/c10w_oracle/p2_20261008T075056_661871Z/preflight.json
b3af96deb8eda65aa60dd1dd7a63275c782e577f7b88b3d87e0c4e035103c1ff  architecture_profile/c10w_oracle_halt_diagnostic_20261008T075101_137852Z.json
