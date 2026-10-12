# System map schema

This schema uses the supplied system-map object and process templates. Team, job, governance, and pattern nodes belong to other map forms. They are outside this graph.

## Closed node types

| type | Role | Required fields |
|---|---|---|
| object | One durable kind | type, cluster, universe, status, entity |
| process | One repeated movement | type, status, consumes, produces |

Catalogs, guides, the inventory, the schema, templates, and indexes are navigation files. They are not graph nodes. Slice 1 creates no object or process bodies.

## Fields

- type: object or process.
- cluster: one cluster slug from the catalog.
- universe: live, leftover, or ghost. The inventory holds its evidence.
- status: stub, verified, or stale. Slice 1 uses stub only.
- entity: the owning source path. Cite a concrete existing file. State family patterns separately.
- consumes and produces: lists of object links. Fill them when process cards are authorized.

Verified status requires a date, branch or revision, and checked source citations. A stub carries no behavior claim. A stale card needs source review.

## Names and sections

Use kebab-case for future cluster and card slugs. Future object cards live under objects/<cluster>/. Do not create those folders in slice 1.

An object card has: one sentence; Why this shape; Shape; Connected to; If you change this; Surfaces; See. The change section separates Hits and Does not hit.

A process card has: one sentence; Input → Movement → Output; Why this shape; Steps; If you change this; Surfaces; See. Every step needs a source citation.

The object and process templates contain placeholders. A placeholder is an instruction to the future author. It is not a source citation.

## Index

The noun index has four columns: name, cluster, source path, status. It has one row per inventory noun. All current rows use stub. Product names and family scopes stay in the inventory. Edit the index by hand after an approved inventory change.

The catalog entry is CLAUDE.md. MAESTRO generates AGENTS.md and routing.md. Do not hand-edit the twins.
