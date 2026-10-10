---
name: local-only-no-rented-compute
description: "Standing rule (operator 2026-10-04): all science runs on the MacBook M3 Pro; never propose rented servers/GPUs; design local-faithful ports"
metadata:
  type: feedback
---

Robert chose Route A for C10K and said: "We are running this entirely local on my computer. That was the whole point of this initial setup on this local environment. So, your goal and objective is to always work the science and find solutions that will run on my local environment, not on rented servers, etc. Stop suggesting it."

**Why:** the pod loss and the migration were about owning the hardware; a rental re-introduces the dependency and the cost he just eliminated. The M3 Pro (48 GB unified memory) is both science hardware and deployment target (D-HW-1, CLAUDE.md:3).

**How to apply:** when a prereg or method assumes CUDA/A100, the task is to design the local-faithful version (declared device port, smaller/base model, fp16, CPU float64) and state its attribution limits — not to recommend hardware. Never list a rental as a route, a comparison, or a fallback. Route A for C10K is pre-registered in `docs/C10K_ROUTEA_LOCAL_PORT_PREREG.md`. Related: [[operator-profile-and-standing-directive]], [[mbp-command-line-tools-broken]].
