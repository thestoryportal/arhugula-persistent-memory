# FS1 — adversarial assessment of fsspec adoption

Assessed 2026-10-11 in `worktree-c10k-route-a`; installed fsspec 2026.6.0 and torch 2.8.0. This evaluates storage infrastructure supporting reproducible F1 work, not scientific acceptance. Only this report, the permitted script/output, and one bounded temporary fixture were written; no installation, Drive/credential access, model load, commit, or tmux operation occurred.

## Claims

C1 — PARTLY — The backend is small and explicitly beta, but maintenance continued in 2025–2026, it has a June 2026 PyPI release, and fsspec lists it as a known experimental implementation, so abandonment or exclusion would be false — [commit history][history], [PyPI][pypi], [issues][issues], [known implementations][known].
C2 — PARTLY — A different OAuth app normally lacks access to rclone-created files under `drive.file`, but app identity rather than Python versus rclone controls that restriction, making the same-client route plausible and its actual visibility UNRESOLVED without an authorized live test — [Google scope documentation][scope], [gdrive auth source][gdrive], [PyDrive2 source][pydrive].
C3 — PARTLY — The three disk caching filesystems have no built-in aggregate byte cap, but installed `simplecache` disables expiry and the separate RAM `BlockCache` does have LRU size eviction, so “only age-based expiry” is inaccurate — installed `fsspec/implementations/cached.py:67–110,190–199,241–269,791–815`, `cache_metadata.py:85–136`, `fsspec/caching.py:331–373`, and [local raw output](cache_experiment_output.txt).
C4 — PARTLY — Ordinary file-like `torch.load` eagerly reads referenced tensor storages without a selected-tensor option, but local-path `mmap` supports lazy storage and FakeTensorMode supports metadata inspection without payload loading — installed `torch/serialization.py:1271–1278,1331–1336,1506–1518,2002–2039,2071–2087,2110–2119`, [PyTorch 2.8 documentation][torchdocs].
C5 — PARTLY — Ungated remote opens could hide transfers, but explicit URI schemes and a budgeted staging boundary can retain every policy requirement while sharing reader code — [storage policy](../../EXPERIMENT_RUNBOOK.md#33a--storage--archival-policy-operator-2026-10-09-binding-after-the-110-gb-disk-full-incident), installed `fsspec/implementations/http.py:36–99`, [rclone HTTP serving][serve].
C6 — CONFIRMED — MAESTRO's blanket dismissal misses an rclone-compatible adapter, a read-only HTTP bridge, and backend-specific stored-hash metadata, although none establishes a reason to replace the current transfer wrappers — [rclone-filesystem repository][adapter], [HTTP serving][serve], [PyDrive2 metadata][pydrive], [Google hashes][files], installed `fsspec/generic.py:40–139,349–388`.

Installed-source references above and below are relative to `/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.venv/lib/python3.11/site-packages/`; `.venv` in this worktree resolves there. Public pages were retrieved on the assessment date; their crawl dates vary, so a retrieved history page is not guaranteed to represent the current remote head.

## Evidence and limits

**C1.** `gdrivefs` was renamed to `gdrive-fsspec` in June 2025; the installed registry points `gdrive` to `gdrive_fsspec.GoogleDriveFileSystem` (`fsspec/registry.py:127–130`). The returned history's newest visible commit is `01bcca8`, dated 2026-06-29, modernizing CI; June 19 includes directory-cache and upload-cache fixes. PyPI's latest displayed version is 0.4.1, released 2026-06-11, with one maintainer; GitHub's Releases page displays no releases, which does not mean there are no published packages. [Sources: history][history], [PyPI][pypi], [GitHub Releases][releases].

The issue listing displays 16 open issues, including directory `put` silently doing nothing (#60, 2026-06-19), permanent deletion (#68, 2026-06-28), and old Shared Drive requests. The README still warns against production reliance. These support caution about a small beta backend, not a claim that it has been untouched since 2024. The repository landing page reports 43 commits, whereas an older returned landing-page snapshot reported 37; exact current-head freshness remains UNRESOLVED. [Sources: issues][issues], [current landing page][landing].

**C2.** Google documents per-file access for files created or opened with the app; knowing a path or file ID does not bypass that authorization. Our setup note records a custom Google Cloud app and `drive.file`, so a fresh, unrelated OAuth app cannot be assumed to inherit its visible archive. [Sources: Google][scope], [our setup note](../../memory_mirror/gdrive-rclone-remote.md).

The gdrive backend passes `auth_kwargs` through to `pydata_google_auth.get_user_credentials`, whose signature accepts `client_id` and `client_secret`; sharing the exact client and user therefore has a source-supported configuration route. However, gdrive's `access` mapping only offers full Drive or Drive read-only scopes: passing the same client alone does **not** preserve `drive.file`, and passing `scopes` through `auth_kwargs` would collide with the positional scopes argument. [Sources: gdrive `core.py:13–16,65–114,149–152`][gdrive], [auth helper:228–236][auth].

A cleaner scope-preserving route is PyDrive2's fsspec-compatible `GDriveFileSystem(path=..., google_auth=...)`, supplying an independently authenticated `GoogleAuth` configured with our exact OAuth client, same user, and only `drive.file`. The injected auth bypasses its broader default scopes. This is an inference from the app-access rule and injection code, **not** a demonstrated login or successful read; no token/config was opened and no Drive operation was attempted. [Source: PyDrive2 `spec.py:22–28,145–219`][pydrive].

**C3.** Reviewed the installed disk-cache classes and metadata implementation: `cache_size()` measures size; it does not enforce a ceiling. `filecache` and disk `blockcache` use age/UID validity checks and explicit expiry clearing; merely expiring an entry is not a guaranteed background cleanup. `simplecache` sets `expiry_time=False` and does not retain download-time metadata. Its cached files can therefore persist without automatic age expiry. Sources: installed `cached.py:190–199,241–269,791–832`; `cache_metadata.py:94–129`.

Do not conflate disk `fsspec.filesystem("blockcache", ...)` with RAM `cache_type="blockcache"`: the latter's `BlockCache` retains at most `blocksize * maxblocks` payload bytes per file through `functools.lru_cache`. Returned read buffers, other open files, and metadata add memory beyond that bound. Sources: installed `cached.py:391–393`; `caching.py:331–373`.

The newer published fsspec 2026.9.0 documentation still shows no aggregate disk-cache byte limit; it does add explicit mtime-based `simplecache.clear_expired_cache(expiry_time=...)`. Third-party alternatives exist: Zarr 2.18.5's `LRUStoreCache(max_size=bytes)` bounds a mapping cache in memory, not a drop-in `.pt` disk cache; rclone VFS has size/free-space eviction targets, but its documentation permits overshoot for open files and between polling intervals. Neither substitutes for our admission budget. [Sources: newer disk-cache source][newcache], [Zarr][zarr], [rclone VFS][vfs].

Local measurement: each of `filecache`, disk `blockcache`, and `simplecache` retained 4, 8, then 12 MiB payload as three 4 MiB files were read twice; each delivered 24 MiB total. RAM `BlockCache(maxblocks=2, blocksize=256 KiB)` read 8 MiB with 32 misses and retained two blocks, at most 512 KiB. Fixture logical bytes totaled 50,333,587; runtime was 0.0783 s, with a 64 MiB budget and 208,370,057,216 free bytes before execution. [Source: raw output](cache_experiment_output.txt).

The retained directory is `/private/tmp/fs1_fsspec_09t6wg5z`. The script uses a local range adapter implementing `AbstractBufferedFile`, because ordinary `LocalFileOpener.read` bypasses its cache. Its backend counter records requested ranges, including readahead, despite the `fetched_bytes` label; whole-file copies can bypass that counter. This experiment proves retention and the RAM LRU distinction, not network efficiency or performance. [Source: script](cache_experiment.py), installed `fsspec/implementations/local.py:410–416,468–469`.

**C4.** Normal ZIP-format loading unpickles the object graph and calls `load_tensor` for each referenced storage, which calls `get_storage_from_record`; indexing one key after `torch.load` returns does not avoid reading the others. `weights_only` restricts unpickling, not tensor selection, and `map_location` receives already-deserialized storage. “Whole file” is shorthand for the required storage payloads, not proof that every ZIP byte is read. Sources: installed `torch/serialization.py:1293–1297,1327–1329,2035–2039,2071–2087,2110–2119`.

`mmap=True` instead maps a local filename and slices storages by offset; CPU payload access can be lazy, but an fsspec file-like object is explicitly rejected for mmap. `simplecache` followed by mmap still downloads the full file first. FakeTensorMode records checkpoint offsets without materializing storage, enabling metadata audits and potentially a custom range reader, but ordinary `torch.load` does not expose selected-tensor loading. The gdrive backend implements HTTP Range requests; selective remote tensor retrieval would require additional validated reader work. Sources: installed `serialization.py:1506–1518,2004–2023`, [PyTorch][torchdocs], [gdrive `core.py:386–404`][gdrive].

**C5.** The failure mode is policy bypass through an apparently ordinary `open`, particularly an implicit whole-file cache on the internal SSD; the policy's exact guard is free space ≥ projected writes + 20 GiB. A counter-design records the archive URI, expected size/hash, byte budget, and explicit staging receipt before returning a local filename. Shared reader code can then operate on local or remote metadata without claiming that a remote file has become local. This is a proposed design, not an implemented gate. [Sources: runbook lines 270–282](../../EXPERIMENT_RUNBOOK.md), [installed HTTP reader](../../.venv/lib/python3.11/site-packages/fsspec/implementations/http.py).

**C6.** `zincware/rclone-filesystem` documents `RCloneFileSystem(remote="...")`; PyPI displays 0.2.0 released 2026-03-06 and configurable transfer temporary directories. It could expose the existing rclone remote to Python while retaining rclone's OAuth identity, but its implementation fetches failed in the available web path and its seek/range, temporary-file, and error behavior are unqualified here. Do not adopt it on API resemblance alone. [Sources: repository][adapter], [package metadata][adapterpypi].

A simpler candidate needs no new backend package: serve an explicitly named archive subtree with `rclone serve http`, loopback binding, read-only access and VFS disk cache off, then use installed `HTTPFileSystem` with a bounded per-file RAM block cache. `aiohttp` and `requests` directories are present locally. It adds a managed server process and still needs a host test, but avoids a second OAuth app, an internal-SSD cache, and dependence on gdrive-fsspec. [Sources: rclone][serve], installed `http.py:52–99,360–397`, `caching.py:331–362`.

Hash distinction matters: the default `fsspec.checksum()` is a token of `info()` metadata, not a content digest (`spec.py:716–727`). Current gdrive-fsspec does not request MD5/SHA hash fields, whereas PyDrive2 exposes Drive MD5 as `info()["checksum"]`; Google's v3 API additionally offers SHA-256 when available. A metadata audit could compare stored hashes with pinned manifests without redownloading tensors, refusing missing hashes or algorithms that do not match. [Sources: gdrive `core.py:19–29`][gdrive], [PyDrive2:385–394][pydrive], [Google][files].

That improvement is not exclusive to fsspec: existing rclone `lsjson --hash` already exposes supported remote hashes. `tools/archive_to_gdrive.sh:44–49` currently uses immutable copy plus full download verification, so a hash-only audit would be a separately reviewed verification mode, not an automatic replacement for that guarantee. The runbook's 1.16 MB/s is measured **upload** speed; it does not establish download speed or a measured saving. [Sources: rclone][lsjson], [archive tool](../../tools/archive_to_gdrive.sh), [runbook lines 270–282](../../EXPERIMENT_RUNBOOK.md).

`fsspec.generic.rsync` offers cross-backend copying and configurable comparison fields, but defaults to size comparison; its cross-filesystem copy helper stages entire files through a temporary directory, defaults to ignoring returned errors, and batches 20 operations. It supplies neither our disk admission nor wrapper receipts/immutability rules. A future heterogeneous export could use it behind those guards; it is a poor replacement for today's archive and backup flows. Source: installed `fsspec/generic.py:40–91,123–139,349–388`.

## Strongest case for adopting fsspec here

Adopt it narrowly as an archive **reader interface**, retaining rclone as the transfer and authentication boundary. A proposed reader in `tools/` would accept explicit archive URIs and byte ceilings, use the HTTP bridge with bounded RAM caching for small archived JSON/manifests, and support local/memory backends for fixtures. Changes to `tools/archive_to_gdrive.sh` would be limited to producing reader-facing location/size/hash receipts after its existing verification; `tools/backup_gdrive.sh` would retain its transfer controls. This is a concrete proposal, not an implementation or authorization to change those files. [Sources: current archive tool](../../tools/archive_to_gdrive.sh), [adapter][adapter], [bridge][serve], installed `caching.py:331–373`.

The strongest advocate's argument is that rejecting fsspec because one experimental Drive backend and its disk caches are unsuitable rejects separable components unnecessarily: the installed HTTP reader, bounded RAM cache, and explicit budget gate can coexist. The likely gain is simpler read-back tooling and less manual staging of small archived records, not faster full-tensor uploads or automatic storage management. Its incremental benefit over `rclone cat` plus ordinary local readers remains unmeasured; require a useful read-back task before adding a persistent service. [Sources: installed `http.py:52–99`, `caching.py:331–373`, [rclone bridge][serve].]

## Overall

**verdict partly wrong**
MAESTRO's recommendation against replacing our current bulk-storage tools stands because fsspec does not itself enforce the required disk budget or provide selected-tensor `torch.load` over remote file-like objects.
Its blanket rejection is too broad: active backend maintenance, shared-client authentication routes, bounded RAM caching, and an rclone-backed HTTP reader all weaken the stated reasons.
The honest adoption candidate is a small, explicitly budgeted archive-reading pilot; neither a broad migration nor a net engineering saving has been demonstrated.

## One cheap operator-approved test

Run one isolated same-client visibility pilot against a newly named ≤64 KiB fixture uploaded through our existing rclone remote: the operator supplies independently authenticated PyDrive2 `GoogleAuth` objects for the same user using only `drive.file`, first with the exact rclone OAuth client and then an unrelated client with clean auth caches. Inject each into `GDriveFileSystem`, root it at the fixture folder ID, retrieve `info()` and read/hash the fixture; do not use Picker/Open-with to grant the unrelated client access. Prerequisite: an operator-provisioned PyDrive2 environment; any dependency installation needs separate approval and its own disk budget, outside the pilot budget below. No installation was performed here. [Sources: auth injection][pydrive], [scope rule][scope].

Budget: ≤4 MiB total new local disk including receipts/auth-cache allowance on memit, ≤64 KiB new Drive data, serial execution, two-minute timeout excluding operator login, free space ≥4 MiB + 20 GiB; retain the fixture and redact credentials from receipts. PASS: exact-client reader sees the pre-existing rclone upload and returns matching size/content hash, while the unrelated-client negative control cannot read it; FAIL: the authenticated exact-client arm cannot read the known existing object; INVALID: wrong client/user/scope, broad scopes, stale credentials, or missing rclone positive control. A PASS refutes an inherent cross-library visibility barrier; it does not qualify gdrive-fsspec's scope interface or prove adoption pays for itself.

## FS1 HANDOFF

Done: C1–C6 classified and sourced; installed cache/torch behavior checked; one bounded local cache experiment and its raw output saved; adoption counter-case and approval-gated next test specified.
Remaining: exact current remote-head freshness, live same-client visibility, adapter implementation behavior, and practical read-back benefit remain unverified; none was silently treated as acceptance.
Next single step: if the operator authorizes further work, run the visibility pilot above; do not access Drive or credentials under this assessment's authorization.
Context directive: start new work only at ≥60% context left; at ≤40% or any compaction stop starting work, preserve done/in-flight paths, next step and risks in a handoff, and carry this directive through successor sessions. MAESTRO ordered source reading stopped at 45%; this report uses only evidence already obtained.

## Source links and local pins

[history]: https://github.com/fsspec/gdrive-fsspec/commits/master/
[pypi]: https://pypi.org/project/gdrive-fsspec/
[issues]: https://github.com/fsspec/gdrive-fsspec/issues
[known]: https://filesystem-spec.readthedocs.io/en/latest/api.html#other-known-implementations
[releases]: https://github.com/fsspec/gdrive-fsspec/releases
[landing]: https://github.com/fsspec/gdrive-fsspec
[scope]: https://developers.google.com/workspace/drive/api/guides/api-specific-auth
[gdrive]: https://raw.githubusercontent.com/fsspec/gdrive-fsspec/master/src/gdrive_fsspec/core.py
[auth]: https://raw.githubusercontent.com/pydata/pydata-google-auth/main/pydata_google_auth/auth.py
[pydrive]: https://raw.githubusercontent.com/iterative/PyDrive2/master/pydrive2/fs/spec.py
[torchdocs]: https://docs.pytorch.org/docs/2.8/notes/serialization.html
[newcache]: https://filesystem-spec.readthedocs.io/en/latest/_modules/fsspec/implementations/cached.html
[zarr]: https://zarr.readthedocs.io/en/v2.18.5/api/storage.html#zarr.storage.LRUStoreCache
[vfs]: https://github.com/rclone/rclone/blob/master/vfs/vfs.md
[adapter]: https://github.com/zincware/rclone-filesystem
[adapterpypi]: https://pypi.org/project/rclone-filesystem/
[serve]: https://rclone.org/commands/rclone_serve_http/
[files]: https://developers.google.com/workspace/drive/api/reference/rest/v3/files
[lsjson]: https://rclone.org/commands/rclone_lsjson/

Installed SHA-256 pins: `fsspec/implementations/cached.py` = `dfc078a950c35d187ae596ff257cb6fa524ec6d76051d06035dcbea017ba8c6c`; `fsspec/caching.py` = `6099bb4a3413c4e8326af2af004d02493fc64749a99c48e7208582744d506cb9`; `torch/serialization.py` = `b50f806f9aee71df8c412db95332218deca1ebcb74e694d3e5241da8eefc056c`.
