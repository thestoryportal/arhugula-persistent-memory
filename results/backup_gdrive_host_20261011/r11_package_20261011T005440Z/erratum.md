# a091aec poll-loop erratum (current frozen test bytes)

a091aec's commit note says "the poll loop has no sleep (busy-wait <=3 s)". That statement is incorrect: tools/test_backup_gdrive_addendum.py:483 executes `time.sleep(0.01)`, a 10 ms sleep. The bound is not a busy-wait claim. Current SHA-256 is 3ff28cb712e97941476c1730928ff720f9a0dbcb2d8ba29344647ea8904501f8.

At tools/test_backup_gdrive_addendum.py:470, unguarded `json.loads(self.heartbeat.read_text())` can raise on malformed input. Astra r10's ruling remains binding: normal status publication is atomic (tools/backup_gdrive_status.py:228–235), so partial-write JSON is not an established race. Do not reclassify malformed-input failure as a proven publication race. See results/backup_gdrive_host_20261010/astra_r10_verdict.md:20–23.

The old pin set is preserved; b764938 is the a091aec test-file hash, not a pin-set hash. pins_v2.json records the full lineage and supersession.
