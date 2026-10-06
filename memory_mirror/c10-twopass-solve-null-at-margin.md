---
name: c10-twopass-solve-null-at-margin
description: "CORPUS/49 (D-C10p-twopass, 2026-10-05): a fresh band-4–8 edit aimed at the target re-solved on the once-edited model reaches 21/72 held-out (canon 12/24) vs 13/72 (7/24) — gain 8 under the pre-registered 10 → NULL, with a ×1.31 write and a 3.08 described_as drop; the injection-found direction does not survive as a fresh weight edit at the margin. Harness seam Z_OVERRIDE (aim the solve at supplied targets) is inert and audited."
metadata:
  node_type: memory
  type: project
  originSessionId: 4d71207f-24bf-4199-894f-d2f977d9f609
---

The two-pass solve was the mechanism arm routed by CORPUS/48. Three harness passes in one process: baseline, a sham fresh edit aimed at the pre-edit targets (identical to baseline on every readout and every per-layer ΔW — the seam is inert), and the fresh edit aimed at the re-solved targets. The last moved held-out recall 13 → 21/72 and canon 7 → 12/24 with a 31 % larger write and a described_as drop that missed its 3.0 gate by 0.08; controls and the other S-3 axes (incl. a same-frame fictional probe) held.

**Why:** a weight edit is a different intervention from injection (CORPUS/44 F-A3): the direction that restores decoding when injected does not, at the pre-registered margin, restore it when written. The prereg's NULL branch routes to the engine-path arms (I-1 OverTone / I-2 forward replay); the iterated re-solve and the stacked variant are cheaper harness-side alternatives for the operator to choose.

**How to apply:** reuse `Z_OVERRIDE` (keyed by (subject, " " + value); bypassed in the LAW#5 check; count the hits) for any arm that aims the harness solve at supplied targets; always run a sham pass; pre-register the ΔW ratio cap and the same-frame probe. See [[c10-edit-rotates-required-target-direction]], CORPUS/48–49.
