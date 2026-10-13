LLMDB_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/rtk proxy /usr/bin/python3 -B -c 'import tempfile, unittest
from pathlib import Path
from tools import test_dashboard_storage as storage
names = ["tools.test_dashboard_live", "tools.test_dashboard_report", "tools.test_dashboard_gpu_detector", "tools.test_dashboard_mathlab", "tools.test_dashboard_storage"]
with tempfile.TemporaryDirectory(prefix="mb38_legacy_", dir="/private/tmp") as root:
    storage.FIXTURES = Path(root)
    storage.RECEIPTS = None
    suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
' > results/dashboard_audit_20261010/fix_20261010T234721Z/legacy_first.log 2>&1
