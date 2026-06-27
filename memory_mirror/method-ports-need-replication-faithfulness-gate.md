---
date: 2026-06-27
source: C10i AnyEdit parity audit reflection
scope: LLM-as-Database method ports / experiment assurance
---

# Method Ports Need A Replication-Faithfulness Gate

Before interpreting a ported external method as science, prove the port is faithful on
easy positive controls. C10i showed how quickly a method port can become a local
hybrid: upstream AnyEdit planning matched local A1/A2 token/window/lookup/mask
traces, but active upstream execution still hit stack/hparam/wrapper compatibility
failures before behavioral evidence. A local result from such a path is not a
method-family result.

Future external-method experiments need a pre-science gate: identify upstream
commit and hparams; list every deviation from upstream; run unchanged or minimally
compatible upstream code on tiny easy controls; capture active trace (target norms,
losses, deltas, update norms, logits, behavior); require easy-control recovery
before hard cases; label all failures as diagnostic until the gate clears.
