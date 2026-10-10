---
name: readme-plain-words-summary
description: "Standing rule (operator 2026-10-06): refresh README's 'In plain words' section (date, progress, one record line) on every progress push"
metadata:
  type: feedback
---

The operator asked for the plain description of the program to sit at the top of the repo's README, written for the general public. Every push that changes progress must also update it, as an easy-to-digest summary and progress record.

**Why:** the operator and outside readers need to follow the program without reading the technical trackers.

**How to apply:** before committing a progress change, update `## In plain words` in README.md: the date, the progress paragraph if the picture changed, and one newest-first line in its progress record. Use everyday words, with no IDs, file names or jargon. The rule also sits in DISCIPLINE §1.1 so other sessions and Codex follow it. See [[plain-language-to-operator]].
