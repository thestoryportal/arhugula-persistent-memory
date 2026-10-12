# MB39 criterion test list — frozen before tests and implementation

Budget: less than 200 MB; observed free space 79.89 GiB on memit and 194.67 GiB in tmp. This is backup release preparation for preserving F1 evidence, not scientific or deployment acceptance. Only tools/test_backup_gdrive_addendum.py (E) and this receipt may change.

| Criterion | Test/check written first | RED target | GREEN acceptance |
|---|---|---|---|
| 2.1 | CheckTemplateTest | Missing exact hash-check template/filter/report/exit capture | Default hashes, one-way rationale, identical filters/links, four reports, stdout/stderr/exit, full-population download fallback |
| 2.2 | VerifyCheckTest | Unsafe accept-all verifier | Clean PASS; differing, missing destination, unreadable, unchecked hash, missing/truncated reports, nonzero exit with empty reports FAIL with counts; population/log cross-check |
| 2.3 | host local-check fixture | Same-size corruption | Four tiny local cases; corrupt file named; excluded-only, links and clean PASS |
| 2.4 | PlanCriteriaTest | v1 timestamp/warning waiver | Upload, named-writer pause and stopped-process evidence, catch-up, full check, inventory, explicit GO, budgets, no waiver |
| 3.1 | RunnerContractTest and host exact suite | Missing runner safety/selection | Exact 10 base + 9 Heartbeat + 3 Launcher; Python 3.9.6/nice 0; isolated HOME/config positive control; forbidden argv; process groups; observed ps; identical real inventory |
| 3.2 | PinsTest and shasum -c | Missing final pin set | All deployment/test/runner/checker/plan bytes; supersedes old 33-line pins with hash; full lineage; future bundle manifest/source cmp |
| 3.3 | ErratumTest | Missing erratum | Current sleep/parsing lines and Astra atomic-publication ruling |
| 4.1 | PlanCriteriaTest and fresh inventory | Stale receipt/floor assumption | Empty-history branch exact command/output/state and no-lost-history GO; any evidence STOP/operator reassessment |
| 4.2 | PlanCriteriaTest | checkout/venv status | Every status/recover invocation uses hash-checked deployed tool and /usr/bin/python3 |
| 4.3 | PlanCriteriaTest | start-relative deadline/status masking | Strict end+13 h, separate owner/child/progress evidence |
| 4.4 | PlanCriteriaTest | routine recovery/fixed successors | Diagnose/clear/re-open only with GO; observed successors; recovery only damaged history |
| 4.5 | PlanCriteriaTest | Missing assertion check | caffeinate -i -s open -W -g and saved pmset assertions; AC required |
| 4.6 | PlanCriteriaTest | Non-mandatory orphan check | Immediately before 3.1, eight PIDs plus native fixture scan; any found STOP |
| 4.7 | PlanCriteriaTest | Premature retirement | Content checkpoint + fresh scheduled completion; bootout/disable + disabled-state/process proof |
| 5.1 | CheckPlanTest | v1 defects at 67/81/87/94/104-117 | v1 semantic findings with line references; v2 no hidden exits/unmarked effects/weak integrity/fixed generations |
| 5.2 | PlanCriteriaTest | Missing deployment/bundle pins | Full source cmp and manifest; enabled state; RunAtLoad false/21600 login timing |
| 5.3 | PlanCriteriaTest | Missing ordering/GO/STOP preservation | Verbatim r10 ordering, mapped steps; every old GO/STOP retained; c1a06ea preservation |
| E.1 | LauncherHomeExportTest | Current shared native transform without export | Real sh/perl probe in both properties with absent HOME and sentinel parent; fixture HOME in all four subcases |
| E.2 | Same probe | Missing export HOME | Shared transform injects assignment + export; no production edits |
| E.3 | strengthened existing native failing-wrapper test | Native assertion added only after E RED | Receipt, counter and unresolved artifacts in fixture applet-home |
| E.4 | inventory envelope for host E/native/full runs | No host execution before E GREEN | Real roots identical before/after; no sandbox-native acceptance claim |

Host gates are PENDING. Sandbox runs use /usr/bin/python3 -B, BACKUP_TEST_NO_RCLONE=1, isolated HOME, and no native commands. New host runners are tested without launching native tools or real rclone; live acceptance requires the supplied host commands. Archive's five real-rclone cases remain unverified, independent of activation.
