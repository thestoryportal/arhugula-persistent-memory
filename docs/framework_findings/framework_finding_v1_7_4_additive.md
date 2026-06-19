# framework_finding v1.7.4 — ADDITIVE (S2.40): containment cannot salvage Qwen-as-Database; final viability verdict
# Tests the write->verify-biography->rollback escape route for Qwen attribute-entanglement (v1.7.1/.2/.3).
# For human KB merge. Engine UNMODIFIED.

## Provenance
- Engine `5c0c706a…c78770` (gate PASS, _cov_cpu=3); P-VRAM-CPU-SOLVE. Probe-B style (apply+restore), no engine change.
- Qwen2.5-7B, 5 cfb-v3 facts. Verification BATTERY = locked generalization probes (3/fact). HELD-OUT = S2.40-authored auxiliary biographical attributes (sport/team/era/role; 4/fact), disjoint from each subject's battery — to test detection leakage. Auxiliary probes NOT added to the LOCKED probe-set-v3. Flag rule: top-1 flip OR next-token KL>0.5.

## §X.2.5 — Containment is a reliable tripwire but rejects 100% of multi-field writes
| metric (n=5) | value | meaning |
|---|---|---|
| detection rate | **1.0** | battery flags the corruption on every edit |
| held-out corruption rate | **1.0** | an unprobed biographical attribute is corrupted on every edit |
| leak rate | **0.0** | no case where held-out corrupted while battery clean (battery never missed) |
| accept rate | **0.0** | zero edits pass verification → all rolled back |

Held-out corruptions hit CORE identity, not trivia: Tiger Woods sport `golf→tennis`; Deion Sanders sport/identity `football→baseball`; Lindsey Vonn sport `skiing→"what"`; Hakeem sport `basketball→":\n"`; multiple team/era attributes scrambled.

Findings:
1. **Detection works; salvage does not.** A write→verify→rollback layer reliably DETECTS the entanglement (detection 1.0, leak 0.0 in this set) — but because every Qwen edit corrupts same-subject biography, it REJECTS every write (accept 0.0). Containment converts a silent-corruption failure into a loud-rejection failure; it does not yield a usable multi-field write path.
2. **The corruption is semantic, not cosmetic.** It overwrites the entity's defining attributes (the subject's actual sport), confirming the v1.7.1/.2 picture that the edit moves the whole entity representation, not the targeted field.
3. **Leakage caveat.** leak=0 holds for THIS battery (3 probes) and THIS held-out design under pervasive corruption; with sparser corruption or a smaller battery, a bounded battery could miss off-battery corruption. The dominant result (0% accept) does not depend on this.

## FINAL Qwen-as-Database viability verdict (cumulative v1.7 → v1.7.4)
- **Writable:** Qwen is the ONLY model that expresses the write (converges 5/5); Llama-lineage + Mistral stall (architectural-invariant ceiling).
- **Cross-record isolation:** exact (KL=0 across entities, every arm).
- **Intra-record field isolation:** FAILS — every edit corrupts same-subject attributes, including core identity (v1.7.1/.2).
- **Not tunable:** solve-regularization does not separate expression from entanglement (v1.7.3).
- **Not containable into usefulness:** verify→rollback detects reliably but rejects 100% of multi-field writes (this finding).
- **Net:** Qwen is viable as an LLM-as-Database backend ONLY for **single-attribute-per-entity / key→value** stores (no co-resident attributes to corrupt) or where **whole-entity overwrite** is acceptable. It is NOT viable for multi-field relational records under MEMIT-class editing. A genuinely viable multi-field Qwen-DB would require a DIFFERENT, attribute-local write engine — not a knob or a wrapper on this one.
- Scope: MEMIT-class engine, cfb-v3 (5 facts, athletes, one relation), single edits. The qualitative verdict is consistent across all arms; magnitudes are corpus-scoped.
