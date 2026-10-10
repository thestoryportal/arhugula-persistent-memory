---
name: local-only-no-rented-compute
description: "Standing rule from Robert (2026-10-04): all LLM-as-Database science runs on his MacBook M3 Pro; never propose rented servers/GPUs; find solutions that fit the local machine"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
  modified: 2026-10-04T18:12:55.880Z
---

Robert chose Route A for C10K and said: "We are running this entirely local on my computer. That was the whole point of this initial setup on this local environment. So, your goal and objective is to always work the science and find solutions that will run on my local environment, not on rented servers, etc. Stop suggesting it."

**Why:** the pod loss and the migration were about owning the hardware; a rental re-introduces the dependency and the cost he just eliminated.

**How to apply:** when a prereg or method assumes CUDA/A100, the task is to design the local-faithful version (declared device port, smaller/base model, fp16, CPU float64) and state its attribution limits — not to recommend hardware. Never list a rental as a route, even as a comparison. Related: [[operator-profile-and-standing-directive]], [[mbp-command-line-tools-broken]].
