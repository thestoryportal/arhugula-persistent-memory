<!-- POC artifact — generated from MEMORY.md via mcp__infranodus__generate_knowledge_graph (detectEntities).
     Demonstrates a durable, git-committable graph INDEX over the session-load memory.
     Keep or `rm` — not canonical until you decide. Regenerate, never hand-edit. -->

# Memory Index — Graph View (POC)

_9 clusters · 99 nodes · 304 edges · modularity 0.71 (very high) · state: dispersed_

## Clusters (topical map)
- **Survival Metrics** — edit · cpu · weight · quantization · survival · percent · native · gpu · inference · hybrid
- **Path Bias** — pass · downgrade · incremental · batch · side · viable · bias · core · corruption · store
- **Truth Framework** — spec · truth · memory · situate · ground · framework · read · bootstrap · lifecycle
- **Empirical Scope** — scope · cp · evidence · falsify · empirical · run · [[g6_g7]] · proven · single_source_of_truth
- **Code Coverage** — discourse · coverage · tool · lens · code · official · betaedit · infranodus · alphaedit
- **Prototype Claims** — promotable · prototype · trap · contract · claim · label · tautology · author · control_flow
- **Closeout Checks** — check · closeout · inversion · hang · memit · cov · green · sigma · lambda · gate
- **Roadmap Canonical** — experiment · corpus · single · runbook · readme · canonical · source · roadmap · section
- **Model Review** — cross · local · review · confounded · model · target · intel · deployment · operator

## Gateway concepts (highest betweenness — the hubs to navigate by)
`pass` (bc .48) · `edit` (.39) · `cpu` (.26) · `spec` (.24) · `scope` (.17) · `quantization` (.17) · `closeout` (.14) · `discourse` (.14)

## Structural gaps (under-connected cluster pairs = synthesis opportunities)
- Roadmap-Canonical → Model-Review
- Code-Coverage → Model-Review
- Closeout-Checks → Roadmap-Canonical
- Empirical-Scope → Prototype-Claims
- Survival-Metrics → Roadmap-Canonical

## Edges (DOT, from knowledgeGraphByCluster — git-diffable)
```dot
ground -> truth        // spec, read, framework, memory
canonical -> roadmap   // runbook, experiment, single
scope -> g6_g7         // cp, empirical, run
run -> falsify         // empirical
edit -> percent        // survival, cpu, quantization
edit -> weight         // necessity
downgrade -> bias      // path, pass
viable -> batch        // side
model -> review        // cross, confounded, deployment, target
coverage -> code       // lens, discourse, tool, betaedit
closeout -> check      // green
cov -> inversion       // memit, sigma, hang
claim -> prototype     // promotable, label, tautology, trap
```

> ⚠️ **What this view CANNOT carry** (proven by this generation): the fact `edited 100% vs native 97.4%` lost both numbers — `100` and `97.4` never became nodes. `PASS→CONFOUNDED` survives only as co-occurring tokens, not as a directional claim. **Facts live in the canonical markdown; this is the map, not the territory.**
