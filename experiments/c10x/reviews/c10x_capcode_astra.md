FIX-FIRST
Reviewer: GPT-6-Astra (high)

**BLOCKING — launch arguments only.** [c10x_enginepath_arms.py:1395](experiments/track_c/c10x_enginepath_arms.py#L1395) rejects the relative `--predecessor` supplied in the request; `:216` also requires absolute output. From the reviewed worktree, use:

```sh
--out "$PWD/results/c10x_enginepath_rerun3" \
--predecessor "$PWD/results/c10x_enginepath_rerun2" \
--cause STAGE_PROJECTION_REFUSED
```

**ADVISORY**

- Amendment B code: **GO**. Production changes are confined to pins, caps and budget enforcement. Projection rule, science gates and verdicts are unchanged.
- Reader limits are correctly **3600 / 16200 s** (`c10x_enginepath_read.py:1048–1061`). No production `15000`/`2400` enforcement remains.
- Prereg SHA matches `3eb899d9…`. Fresh selftest: **119 PASS**, 24.125 s; boundary acceptance/rejection passes; protected listing drift empty.
- Rerun 3 output and log directories are absent; predecessor/cause identity is correct. Live budget sufficiency remains **UNVERIFIED**; no dispatch performed.

🌱 graft saved ~251,603 tokens this turn, 1 successful call.

