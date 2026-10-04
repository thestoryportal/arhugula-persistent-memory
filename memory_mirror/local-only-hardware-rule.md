---
name: local-only-hardware-rule
description: "Operator standing rule (2026-10-04): all science runs on the local MacBook M3 Pro; never propose rented servers/GPUs; design local-faithful ports instead"
metadata:
  type: feedback
  source: operator, choosing Route A for C10K (D-C10k-route-a)
---

The operator chose Route A for C10K and ruled: the program runs entirely on the local machine; that was the point of the migration. **Do not propose rented compute as a route, a comparison, or a fallback.** When a prereg or upstream method assumes CUDA/A100, the task is to design the local-faithful version — a declared device port, a smaller or base model, fp16 loading, CPU float64 — and to state its attribution limits honestly, not to recommend hardware.

**Why:** the pod loss was the cost of depending on rented infrastructure; the M3 Pro (48 GB unified memory) is both science hardware and deployment target (D-HW-1). A rental re-introduces the dependency the operator just removed.

**How to apply:** this supersedes the deleted `no-a100-current-gpu-only` note's *mechanism* (pod only) with its *spirit* (owned hardware only). Route A for C10K is pre-registered in `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md`. Related: [[deployment-target-intel-cpu]] (superseded section), [[anyedit-is-best-remaining-c10-rescue-not-assumed-fix]].
