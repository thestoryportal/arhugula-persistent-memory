# User-approved scope amendment

During MB44, read-only ls-tree comparisons found these required inputs identical
in bytes and modes between HEAD 4c5d98d018b1df6218837b054f55cf7e073cd178 and
origin/master: tools/backup_gdrive.sh, tools/backup_mirror.excludes,
tools/launchd/com.rhu.memit-gdrive-backup.plist, tools/test_backup_gdrive.py.

The user answered: "Allow unchanged pinned paths; require exact remaining diff
(recommended)". This supersedes literal diff=full-allowlist equality only for
unchanged pinned paths. scope_allowlist.txt still names all nine production/test
paths and every chosen evidence file. scope_unchanged.txt names the exception;
the gate proves those committed bytes/modes equal origin/master, rejects a false
declaration and checks exact diff=allowlist-minus-unchanged plus every SHA-256 pin.
No production/test byte or mode change is required or authorized by this amendment.

Two new controls are written before implementing this amendment: a real unchanged
pinned input must pass, and falsely declaring a changed input unchanged must fail.
