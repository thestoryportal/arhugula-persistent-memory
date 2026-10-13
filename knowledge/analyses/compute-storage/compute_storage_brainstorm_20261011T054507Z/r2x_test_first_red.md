# R2X test-first RED against unchanged F10/J9/P7

```text
$ /usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v10.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v10.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v9.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v7.json --round13-check verifier --profile-index 19
exit 1
FAIL: expected science occurrence missing: verifier profile 19

$ /usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v10.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v10.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v9.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v7.json --round13-check replication --profile-index 4
exit 1
FAIL: expected science occurrence missing: replication profile 4

$ /usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v10.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v10.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v9.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v7.json --round13-check replication --profile-index 5
exit 1
FAIL: expected science occurrence missing: replication profile 5

```
