# Plan v3 to v4 erratum

Only the finding-dependent receipt declarations/pins/re-review and candidate integration rows change. The activation, recovery, launch, content checks, install, successor and retirement rows retain their command bytes (pin filename references advance to v4). Historical v3 is copied unchanged for K12 regression tests; v4 alone is executable.

| Change | Frozen v3 lines | v4 lines |
|---|---|---|
| replace | [1, 1] | [1, 1] |
| replace | [16, 16] | [16, 17] |
| replace | [30, 30] | [31, 31] |
| replace | [34, 35] | [35, 36] |
| replace | [43, 43] | [44, 44] |
| replace | [45, 45] | [46, 46] |
| replace | [47, 47] | [48, 48] |
| replace | [73, 73] | [74, 74] |
| replace | [77, 77] | [78, 78] |
| replace | [80, 80] | [81, 81] |
| replace | [82, 82] | [83, 105] |
| replace | [98, 98] | [121, 121] |
| replace | [101, 101] | [124, 156] |
| replace | [106, 106] | [161, 161] |
| replace | [110, 110] | [165, 165] |
| replace | [129, 129] | [184, 184] |
| replace | [151, 151] | [206, 206] |

All unchanged line mappings and exact changed text are in plan_v3_v4_line_map.json.
