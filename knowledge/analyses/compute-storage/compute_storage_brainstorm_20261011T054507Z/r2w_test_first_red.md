# R2W test-first RED — recorded before building F10/J9/P7

Each control executes the new semantic check against unchanged F9/J8/P6, independently.

```text
/usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v9.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v9.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v8.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v6.json --round12-check counts
exit 1
FAIL: R12 loaded_data count represented by an unpinned constant: verifier-p3
```

```text
/usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v9.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v9.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v8.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v6.json --round12-check route-equality
exit 1
FAIL: R12 routes merged without pinned pre-spawn operand equality: profile 38
```

Protected input/source SHA-256 baseline (computed before edits):
```json
{
  "results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v9.md": "7eb7fda15e9e4d426f58556ad6490432de2fc49f34b9b41eb2a03b576851d223",
  "results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v8.json": "9c5c28bcee74fd1c1dfb3f2417fb9910b5f08c03950fd870ab689ef19ebec46e",
  "results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v8.py": "9e7e59cda909b320af2d32b082b99b2713ee634b67263daa065b741a3192e0c6",
  "results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v6.json": "583db6d3317b948e2da94b5933da43168addf4a9d9600236d31d849f85be0cd3",
  "results/compute_storage_brainstorm_20261011T054507Z/science_launch_inventory_v8.md": "5bd7762f4b6afb2e8371a3d83855215b430b2067e49bcf793a79390b8b6114a0",
  "results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_contract_v1_1.md": "25c93f5f584d5a1dfff3b0610b32922a289be6d91449765862de3331334062f1",
  "results/compute_storage_brainstorm_20261011T054507Z/astra_r2n_verdict.md": "40e619a68da77c7481f4d4e401c1aab662bea791833e70259ccd0ddc7e256d77",
  "results/compute_storage_brainstorm_20261011T054507Z/r2_round12_decisions.md": "abd2a5c951460f24507726863d5150678eaa92444c87582476ced27a61d31f81",
  "results/compute_storage_brainstorm_20261011T054507Z/r2_round11_decisions.md": "1a845ae801c912d0f650cd9cd832c01c4183492eea9b6143fb3af745e6a510cd",
  "results/compute_storage_brainstorm_20261011T054507Z/r2_round10_decisions.md": "8d9f39f2f6aee4bb37ff50dd2155648aabc9dcf3c836b6ed85f5d7395611ecfc",
  "results/compute_storage_brainstorm_20261011T054507Z/r2_round9_decisions.md": "c09211290f698753fef0af57e23a8ce4381291892a3b44197bacd50e014cbce0",
  "tools/c10w_p2_gate.py": "fb6568a6e159e84b22971aa893c3a83bcaaa16085f4abd9c76ca50b4a3362a26",
  "experiments/track_c/c10w_oracle_train.py": "64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463",
  "experiments/track_c/c10w_oracle_read.py": "162966119cf49967f39c402c73e63ebc9c673401c74f335154696eb5ab859b0b"
}
```

F10/J9/P7/I9 do not exist at this RED gate. Fixtures R12A/R12B also passed independently via --round12-fixture; production acceptance remains pending.
