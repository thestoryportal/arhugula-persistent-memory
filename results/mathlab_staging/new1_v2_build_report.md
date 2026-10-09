# NEW1 DRAFT v2 and CPU build — 2026-10-09

Scope: fold `results/mathlab_staging/new1_prereg_astra_r1.md` into `docs/NEW1_ADAPTER_GEOMETRY_PREREG.md`, build NEW1-specific supervisor and computation worker tests first. Real geometry NOT RUN; no GPU/model/engine import, commits, restarts or producer/shared-file edits authorized.

DRAFT v2 folds B1 verbatim, harvest 1 only, descriptive M16 and spectrum-matched random controls, removes the undefined random-like veto and retains complete-workload budget UNVERIFIED. Fold log is in prereg §9.

Build in flight. Intended owned files: `tools/new1_supervisor.py`, `tools/new1_geometry.py`, `tests/test_new1_supervisor.py`, `tests/test_new1_geometry.py`. Evidence: `results/mathlab_staging/new1_v2_build_evidence/`. Design review: `results/mathlab_staging/new1_v2_build_design_review.md`; Claude auth exit 1 loggedIn=false, so same-family fallback has weaker independence.

Context rule: watch Context N% left; before ~20%, stop starting new work, write done/in-flight/exact paths/next step/risks in this report, and say so for a fresh successor. Every handoff restates this rule.
