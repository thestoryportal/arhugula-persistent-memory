## Appendix E — Sealed Corpora Inventory

Seven Tier 2 sealed corpora in v1.2 (five from v1.1 + `corpus-author-registry/` GAP-8 + `hook-registry/v1/` GAP-54):

| Corpus | Purpose | Access Pattern | Minimum Viable Size | Retention |
|---|---|---|---|---|
| `meta-validator-suite/` | Held-out cases for Meta-Validator | Time-bounded capability at Meta-* runs | 20 cases (IC-CORPUS-AUTH) | Permanent additive versioning |
| `meta-tga-corpus/` | Held-out `(spec, gold_tests)` for Meta-TGA | Time-bounded capability at Meta-* runs | 20 cases (IC-CORPUS-AUTH) | Permanent additive versioning |
| `constitutional-suite/` | Architectural invariant tests | Validator persistent read | No minimum specced | Permanent additive versioning |
| `write-scope-definitions/` | Per-agent write authority | Authorization Gate persistent read | n/a | Permanent additive versioning |
| `reconciliation-reviewers/` | Authorized reviewer list for Reconciliation Queue | Gate read on reviewer verification | n/a | Permanent additive versioning |
| `corpus-author-registry/` | Authoritative list of identities authorized to submit cases to Meta-* corpora (GAP-8) | IC-SL7 token issuance; §24 submission ingress; boot-time verification | ≥ 1 identity (the bootstrap identity from `corpus_author_bootstrap_identity`) | Permanent additive versioning |
| `hook-registry/v1/` | Boot-time + runtime hook binary hash registry (GAP-54) | Boot sequence IC-HOOK-BOOT; any hook-reload ceremony | No minimum specced | Permanent additive versioning |

All seven follow identical storage, signing, dual-store, and boot-verification mechanics.

