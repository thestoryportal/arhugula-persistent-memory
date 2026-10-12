# evidence/manifests

**Job:** Holds the reproducibility manifests and the archive manifest.
**Read it when:** You verify the hashes of a run or a replay.
**Written by:** `code/ops/backup/archive_to_gdrive.sh` appends verified archive entries to `evidence/manifests/ARCHIVE_MANIFEST.tsv`. Other manifests: none found.
**Read by:** `code/ops/backup/archive_to_gdrive.sh` (reads the header before it appends). Other readers: none found.
**Not here:** Retired manifests: `_archive/manifests/`. Rules: `_system/governance/REPRODUCIBILITY.md`.
