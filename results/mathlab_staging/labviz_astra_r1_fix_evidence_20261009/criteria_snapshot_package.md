MathLab snapshot acceptance criteria, 2026-10-09

Required live check failed against the active m2 mirrored stream: card operand .events differs from copied evidence (live-check.log). Source appended between Reader.read and mirror. Shared reader/fold remains correct; do not modify its producer-fingerprinted module.

Tests first: append once after shared reader returns -> consistent retry; append after card completion before mirror -> exact earlier raw snapshot, index/chunk/card/evidence agree; next rebuild advances to new events; append on every read -> clear error after three attempts. Existing fixtures/call-count assertions retained.

Consumer-only change: compare raw bytes before/after the existing shared read_events call, accept only identical bytes, record exact SHA, cache raw snapshot, mirror cached bytes. No JSONL parser, schema, status sidecar, producer edit, GPU or server restart.
