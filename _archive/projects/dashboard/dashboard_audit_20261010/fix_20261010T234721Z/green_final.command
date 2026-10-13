LLMDB_ROOT=$PWD PYTHONDONTWRITECODE=1 PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B -c 'import unittest
suite = unittest.TestSuite(unittest.defaultTestLoader.discover("tests", pattern=pattern) for pattern in ("test_dashboard_live_refresh.py", "test_dashboard_host_runner.py"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
' > results/dashboard_audit_20261010/fix_20261010T234721Z/green_final.log 2>&1
