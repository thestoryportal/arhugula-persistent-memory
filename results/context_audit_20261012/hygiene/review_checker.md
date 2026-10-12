# Checker adversarial review

Status: CHANGES REQUIRED before dispatch. Existing suite: 21/21 PASS on `/usr/bin/python3 -B`, actual runtime Python 3.9.6. Both source files also parse using Python 3.9 grammar. Reviewed checker and test files in full; parsed lanes.json completely and inspected its lane schema/base protocol; read planner brief in full. Probes used only disposable Git object fixtures, with no git commit command or repo/host mutation.

## Actionable defects

1. **BLOCKING — dispatch is mutable scope authority.** `check_lane.py:87-98,115-116` trusts a dispatch receipt from the builder worktree, lets it replace the base, and removes its path from scope failures unconditionally. `input_hashes` is never read. Reproduction: write forbidden `outside.md`, create a temporary fixture commit containing it with the suite's `snapshot`, then write `dispatch/FIX.json` with that new commit and empty input hashes. Checker returns `[]`; the forbidden edit disappears into its self-selected base. Even an ordinary dispatch-content edit is excluded from scope. Also, absent dispatch silently falls back to the planning commit although PLAN.md:11 freezes a predecessor-specific dispatch base. Required fix: make the trusted receipt external/read-only or require its MAESTRO-frozen digest supplied from trusted checker/plan state; require presence for dispatch-protocol lanes, validate lane/base/input-hash schema, and refuse changed/untrusted receipts. Tests must fail for missing, malformed, mismatched, edited and arbitrary valid-commit receipts; preserve a valid frozen-dispatch positive fixture. Merely checking that a commit exists is insufficient.

2. **HIGH — wrong relative target can pass through another directory.** `check_lane.py:148-150` gives normal Markdown links the same fallback directories as wiki links. Reproduction with existing fixture `memory_mirror/MEMORY.md` and absent root `MEMORY.md`: change `allowed.md` to `[index](MEMORY.md)`; returns `[]`. The link actually resolves beside `allowed.md`, where its target does not exist. Required fix: distinguish wiki-link lookup policy from standard Markdown/HTML file-relative resolution. Add positive/negative fixtures with colliding basenames so a target in the mirror or root cannot rescue a broken relative link. Apply the same rule to staging-relative links.

3. **HIGH — valid parenthesized Markdown destinations are silently omitted.** `check_lane.py:56,65` stops at the first closing parenthesis. Reproduction: `allowed.md` containing `[bad](missing(foo).md)` returns `[]`; missing relative .md target is not checked. Required fix: parse balanced destination parentheses and escapes (or explicitly fail unsupported local link syntax, rather than silently skipping it). Add paired fixtures for present/missing `foo(bar).md`, percent-encoded parentheses and escaped parentheses; angle destinations already have a separate path.

4. **HIGH — links in edited non-Markdown files are never checked.** `check_lane.py:129-130` skips the entire file before body-link checking. Reproduction: add `allowed.py` to temporary lane allowlist and write `# [[missing]]`; returns `[]`. Brief item 3 requires a broken wiki/relative .md link in an edited file to fail, without a .md extension restriction; lanes include JSON, Python, shell and hook sources containing documentation pointers. Required fix: scan edited textual files for links regardless of extension, keeping frontmatter checks specific to notes; explicitly handle binary files. Add a passing and failing non-.md fixture.

5. **MEDIUM — empty YAML block scalars satisfy required frontmatter.** `check_lane.py:32-47` counts the block marker itself as a nonempty field. Reproduction: note frontmatter `name: |`, followed immediately by `description: A rule`, then `metadata:` / `  type: feedback`, returns `[]` although name has no value. Flat `metadata.type: feedback` also passes without an actual metadata mapping. Required fix: validate actual supported frontmatter structure/values; a strict documented scalar subset is sufficient with stdlib, but unsupported block/collection syntax must not be treated as a populated scalar. Add empty-block, duplicate-null-overwrite and flat-key fixtures along with a supported positive example.

## What the present tests establish

The suite covers ordinary tracked/untracked scope, a post-base fixture commit, basic missing/empty frontmatter, simple wiki/relative/reference links, links inside inline code, exact byte-cap boundary/UTF-8 overage, basic staged host behavior, an escaping symlink, and a nonexistent commit. These pass. It does not exercise dispatch receipts, their integrity/input hashes, basename fallback ambiguity, balanced destination syntax, non-.md links or empty block frontmatter. Thus its GREEN does not cover the reproduced defects above. No cap bypass was reproduced: 24,400 bytes passes and 24,402 UTF-8 bytes fails as required. Python 3.9 compatibility is exercised by the actual test runtime, not only inferred from syntax.

Fixes should save behavioral RED for each reproduction, then GREEN without weakening scope or link meaning. Re-run this review's probes after the edits. No checker/plan edits were made during this review.

## Reviewed snapshot

- `check_lane.py` SHA-256 `a7cc47bc0fb33534d9482292336cf0c293721b0d074e57c28b1ddeaae0f2c52f`
- `test_check_lane.py` SHA-256 `3c45b3676c685e785e409921ae95391801b254ed11b54c6f6bf2ec121505bbd8`

## Corrected verification after first fixes

This status supersedes the first reviewed snapshot above. Updated checker and tests were read in full. `/usr/bin/python3 -B .../test_check_lane.py`: **33/33 PASS** on Python 3.9.6. All original probes now fail as intended: mutable dispatch base → BASE; wrong relative basename → LINK; missing parenthesized path → LINK; broken wiki in Python comment → LINK; empty YAML block and flat metadata key → FRONTMATTER. Required missing dispatch also fails. Existing cap fixtures still pass/fail at the byte boundary. Python fixture string values are correctly treated as input data rather than prose; comments/docstrings remain scanned.

**Two remaining defects reproduced with disposable fixtures; CHANGES REQUIRED:**

- `frontmatter_ok` retains earlier required fields when a duplicate/null mapping replaces them. Exact repro: valid `name: N`, `description: D`, `metadata:` / `  type: feedback`, followed by `metadata: null` before closing frontmatter. Result `[]`; final metadata lacks type. Reject duplicate required keys/mappings (simple fail-closed approach), or resolve actual final values and invalidate child fields when their parent changes. Add saved RED/GREEN for duplicate metadata-null and duplicate name-null.
- The private-seed loop validates only seeds that currently are files and exemption-eligible; missing seeds generate no failure. Freeze receipt with a declared, untracked private `.codex/config.toml` seed/hash, then remove that temp seed. Result `[]`: Git cannot report deletion of a never-tracked seed. Validate every receipt-declared private seed for existence, regular-file/path safety and exact digest before exclusions, with an explicit failure for each observation/mutation miss. Add saved RED/GREEN for deleted, malformed/unsafe and mutated private seeds. This preserves the no-deletion and immutable-private-input contract.

Only review_checker.md was appended. No plan/checker/test edits, project Python, host writes, git commit command or network action ran.

Updated snapshot hashes:
- `check_lane.py` SHA-256 `f0f4bf2fd73d61e6cd3ddf8717908895d08fc7e1a93d894a34c7bb2095be8413`
- `test_check_lane.py` SHA-256 `0a93027695abebf6b56f321c590c7c7faf7d2e1ece4a0bef6d9f0872462c90d5`

## Final narrow verification — resolved

This status supersedes both earlier CHANGES REQUIRED statuses for the reviewed defects. Suite rerun: **36/36 PASS**, `/usr/bin/python3 -B`, actual Python 3.9.6. Read the changed frontmatter/private-seed branches and added fixtures. Re-ran both independent residual temp probes: duplicate `metadata: null` now returns FRONTMATTER; deleted untracked frozen private seed now returns BASE missing/unsafe private seed. Quoted flow metadata positive control passes. All defects reproduced in this review are resolved at this snapshot; no remaining contract blocker was found within the requested narrow verification. Earlier results remain above as history. No new broad sweep or implementation edit ran; only this review was appended.

Final reviewed snapshot hashes:
- `check_lane.py` SHA-256 `540e0c888439b7e25a6f4a76fd032f3a83e2ae029b38fc7538f691bef7c72fb0`
- `test_check_lane.py` SHA-256 `68eedffa1677adb1c114e425bdc5fc4c396ea25f6246e1f900c9aa075f8e2fa1`
