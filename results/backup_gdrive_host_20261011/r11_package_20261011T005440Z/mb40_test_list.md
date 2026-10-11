# MB40 continuation checks (before edits)

Preserve MB39 REDs; no production/frozen-runner changes. Budget remains <200 MB.

1. Runner fixture placement: isolated single LockedReleaseTest.test_good_release_dispatches_release_path through the candidate runner. RED must show the checkout staging refusal. GREEN must reach staging, dispatch the committed stub, clear owned groups and preserve real-path inventory. Respect the explicit BACKUP_TEST_RECEIPTS=/private/tmp escape used by LockedReleaseTest; normal coverage fixtures remain inside isolated HOME.
2. Existing package acceptance: 33 test_package.py cases already RED before implementation; GREEN after plan, pins and erratum, with no assertions weakened.
3. Existing checker: captured CLI RED on preserved plan v1, GREEN on plan v2.
4. Sandbox addendum: all 151 non-native cases, 14 real-rclone skips, no failure/error, all owned groups gone and byte-identical real inventories. Four native cases remain host UNRUN.
5. E: preserve valid RED and GREEN, rerun the non-native probe on final bytes; provide host E replay/native commands.
6. Final pins: all required bytes OK with count, protected starting hashes unchanged. Host coverage/content/native tests remain UNRUN.

Placement hypotheses: (A) global temp remap overrides LockedReleaseTest explicit external-fixture root; (B) production outside-checkout guard is wrong; (C) environment/cwd confusion. Raw traceback plus staging source favors A; the single-case control will distinguish it without changing production.
