FIX-FIRST

Reviewer: GPT-6-Astra (high)

**BLOCKING**

1. [c10z_astra_arms.py:1736](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_arms.py:1736): `resident()` checks freeze but bypasses go/benchmark validation. With an in-memory FROZEN prereg, wrong population/prereg/amendment pins reached first publication; intercepted before writing or model import. **Fix:** before publication/Session, call `verify_launch_binding(launch, os.environ)` and require validated `go_record()` contents/SHA equal `launch["go"]`/`launch["go_sha256"]`.

2. [c10z_astra_read.py:728](/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/.claude/worktrees/c10k-route-a/experiments/track_c/c10z_astra_read.py:728): reader accepts altered launch/go bindings. Six independent mutations each retained `PARTIAL`, `scientific_verdict=True`. **Fix:** validate go population/prereg/amendment pins, benchmark population/prereg pins, and manifest `go_sha256 == launch["go_sha256"]`. Add rejection controls for both entry paths.

**ADVISORY**

- §12 text satisfies items 1–4. §§1–11 remain byte-identical: **156,213 bytes**, SHA `7aedd4ac…`.
- Artifact SHA `a477f1c4…` verified; **all 1,000 rows**, indices, text hashes, token IDs/counts match diagnostic pins: **95,610 tokens**. Model/tokenizer/cache pins match.
- Persistence and unchanged arithmetic verified. Protected engine/harness unchanged versus HEAD; **59/59 engine hashes match**, fingerprint PASS.
- Benchmark freeze guard is correctly placed; `TEMPLATES` unchanged. Report’s rerun-#3 and attempt-4 commands match interfaces; none executed.
- Isolate DRAFT-negative test fixtures from repository status before freezing. Correct the report’s current claim of resident revalidation.
- Reran **319 tests: 317 passed, 2 MPS skipped**. Additional review controls exposed the blockers above. No GPU/model execution; MPS equivalence remains UNVERIFIED.

🌱 graft reported ~96,387 tokens saved (~$0.05), 1 successful call.

