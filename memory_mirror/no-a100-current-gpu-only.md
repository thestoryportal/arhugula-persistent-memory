---
date: 2026-06-27
source: operator correction during C10K AnyEdit planning
scope: experiment route constraints / hardware envelope
---

# No A100 Route: Current GPU Only

Do not propose A100-class rental or moving to another GPU as part of the AnyEdit/C10 science route. The science has been run on the current pod hardware (`RTX 4090 24GB`) and the north-star deployment target is a local 2020 Intel MacBook Pro with 16GB RAM.

Large-GPU results would test edit-time mechanism existence, not deployment viability, and are out of scope by operator direction. For official AnyEdit, the vital first validation is source faithfulness to the paper/repo on the current hardware envelope. If the official path cannot run source-faithfully on the 4090 without unapproved VRAM/source modifications, record a hardware-envelope diagnostic and pivot to source-grounded smaller configs or other in-weight methods, not A100 rental.
