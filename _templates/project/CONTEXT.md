---
id: null
title: null
decision_ids: []
depends_on: []
outputs: []
---

# Project record

Use the frontmatter to locate the project's sources.
Read `program/program_state.json` for project state.
It is the only authority for project state.
Its queue item locates this folder with `artifact: {kind: project, path: projects/<id>}`.
Do not copy the locator or a state field into this file.

Standard record folders. A folder exists only when it has content.
- `brief/` holds the brief.
- `reviews/` holds reviews.
- `drafts/` holds drafts.
- `rulings/` holds operator rulings.
- `receipts/` holds checks and receipts.
