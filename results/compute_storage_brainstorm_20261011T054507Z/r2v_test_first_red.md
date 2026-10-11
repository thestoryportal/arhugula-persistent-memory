# R2V test-first RED against unchanged F8/J7/P5
New K8 checks written before F9/J8/P6 exist; each check reports its own D14 defect.

```
/usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v8.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v8.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v7.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v5.json --round11-check reachability
exit 1
FAIL: R11 reachable admission occurrence missing: verifier-descendant Git, p2-shuf-s1, adapter 0
```

```
/usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v8.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v8.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v7.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v5.json --round11-check selectors
exit 1
FAIL: R11 process site selector kind missing: gate-root
```

```
/usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v8.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v8.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v7.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v5.json --round11-check exclusion
exit 1
FAIL: R11 first-stage exclusion unpinned: stage domain
```

Final selector check prioritizes the V10 F1 defect:
```
/usr/bin/python3 -B results/compute_storage_brainstorm_20261011T054507Z/check_r2_schemas_v8.py --freeze results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_freeze_v8.md --schemas results/compute_storage_brainstorm_20261011T054507Z/shared_disk_clearance_schemas_v7.json --profiles results/compute_storage_brainstorm_20261011T054507Z/science_launch_profiles_v5.json --round11-check selectors
exit 1
FAIL: R11 loaded_data site filtered by argv stage: git-ls-files
```
