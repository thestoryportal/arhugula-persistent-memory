---
name: debug-mantra-scrutinize
description: >-
  Repo-local debugging and outsider-review discipline inspired by audited 9arm
  skills. Use when a command fails, a harness stalls, a fix is tempting, or a
  change needs path-level scrutiny. No upstream text is vendored.
license: repo-local-derived
---

# Debug Mantra + Scrutinize

Use this for failures and for skeptical review of implementation claims.

## Debug Mantra

1. Reproduce the failure and save the exact command/artifact.
2. Trace the failing path to the narrowest boundary.
3. Form falsifiable hypotheses and try to disprove the favored one.
4. Apply one fix, rerun the same gate, then halt with the diagnostic.

## Scrutinize

- Question whether the change answers the intended requirement.
- Trace the actual code path, not just the diff.
- Prefer simpler controls that can overturn the claim.
- Cite files, lines, commands, and artifacts.
- Do not rubber-stamp a green result if the metric is adjacent.

## Program Binding

For C10/AnyEdit-style method ports, do not proceed to hard A7 cases until the
source-faithful easy A1/A2 active trace and behavior pass.
## Output Contract

Do **not** output the mantra as a checklist. Return the live debugging state:

- `Observed failure:` exact command/artifact/error.
- `Narrowest known boundary:` file/function/line or UNVERIFIED.
- `Competing hypotheses:` at least three, including harness error.
- `One allowed fix/test:` the single next intervention and same-gate rerun.
- `Halt condition:` when to stop and write a diagnostic instead of iterating.

For method ports, distinguish official upstream behavior from local wrappers or
transplants. A local-wrapper failure is not method evidence unless source-faithful
active easy controls passed first.

