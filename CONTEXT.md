# Where a new thing goes

`CLAUDE.md` says what to read. This file says where a new thing goes. Take the first rule that matches.

1. Secrets, environments, editor debris, graft caches: nowhere in the repo.
2. Output of an experiment run: `experiments/<id>/runs/<slug>/`. Large or regenerable output goes in `runs/<slug>/bulk/` (git-ignored), with a committed `bulk.sha256` in `runs/<slug>/`. A bulk folder exists only where a run wrote bulk (for example `experiments/new1/runs/*/bulk/`).
3. Design for one experiment: that record's design folder.
4. Review or ruling about one record: that record's reviews or rulings folder.
5. CORPUS ledger entry or verdict: `evidence/CORPUS/`.
6. Material for an open queue item: `projects/`.
7. Closed project work: a study to `knowledge/analyses/`, build receipts to `_archive/projects/`.
8. Source code: `code/` (folder by job).
9. External input (cache, covariance): `data/`.
10. Pod-era leftover that is not a run: `_archive/pod-era/`.
11. Agent memory or governance rule: `_system/`.

Nothing matches: mark the item REVIEW for a human. Do not guess a home. A wrong guess hides the item.
