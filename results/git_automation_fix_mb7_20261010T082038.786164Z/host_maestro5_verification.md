# MAESTRO5 host verification of MB7 (2026-10-10T08:41:32Z)

- SHA-256 of the four changed files match the build report's "after" column.
- Reran: git-automation suite 74 OK (42.9 s); model-free suites 80 OK (2.4 s); /usr/bin/python3 3.9.6, -B -S.
- Live first-parent adapter (closes MB7 UNVERIFIED item): `Gh.first_parent('f6c1f421af6f183f8545739280852b245f05964a')` (latest merge on origin/master) returned 0224b5c39ca95f2a80ffd50bc29d5470fe40e275 = local `git rev-parse f6c1f421^1` → MATCH. Bogus SHA 000…0 → Refusal "gh exited 1: gh: Not Found (HTTP 404)".
- Ubuntu/Python 3.11: pending the live CI run on the commit that carries this build.
