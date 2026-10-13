# Historical documents from the backups SSD (imported 2026-10-11)

These 142 files are **superseded history**. They are early planning notes, council and session records, older runbook and manifest versions, and the original first findings, copied byte-for-byte from the external `/Volumes/backups` drive. None of them is current guidance; each one's newer repo counterpart is named in `PROVENANCE.tsv`.

- Source audit: `results/backups_audit_20261011T084030Z/audit_report.md` (GAP TABLE). It found no recorded RunPod loss that these files fill; they preserve history only.
- Operator ruling (2026-10-11): import all of them; delete the duplicate copies on the backups drive afterwards, against an exact approved list.
- `PROVENANCE.tsv` gives each file's SHA-256, size, original backup path(s), what it is, its newer counterpart and its audit match class. Every copy was re-hashed against the audit SHA-256 by `results/backups_audit_20261011T084030Z/scripts/import_history_20261011.py`.
- The backup's root `CLAUDE.md` is stored as `CLAUDE.historical.md`, so agent tools never load it as live instructions.
