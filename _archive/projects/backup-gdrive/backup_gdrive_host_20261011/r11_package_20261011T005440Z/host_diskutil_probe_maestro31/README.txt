commands run by MAESTRO31 on host 2026-10-11T02:08:08Z (read-only):
/usr/sbin/diskutil info -plist /private/tmp  -> rc 1 (see info_private_tmp.plist)
/usr/sbin/diskutil info -plist /Volumes/memit -> rc 0
/usr/sbin/diskutil apfs list -plist -> rc 0
/usr/sbin/diskutil info -plist /System/Volumes/Data -> rc 0 (extra: /private/tmp lives on this volume per df)
