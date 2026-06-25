# R9 — In-weight deletion residue (pre-registration, CHARACTERIZATION)

**Hypothesis-register id:** R9 (CP2 read-contract matrix). **Decision-ID (on close):** `D-R9-1`.
**Status:** PRE-REGISTRATION — advisor pre-authoring done (R2-redux check + spec read). **Date:** 2026-06-24.
**Harness scope:** band[4–8] / Qwen2.5-3B / AlphaEdit in-solve / fixed-base P / accumulating batches. Engine UNMODIFIED; `my_edit`/`compute_P`/`predict`/`single_tok` VERBATIM from `experiments/scale/g6_scale_n_param.py`. LAW#5 gate first.

> **⚠ LABEL PRE-COMMITTED (advisor, BEFORE the run): this is CHARACTERIZATION, NOT falsification.** Spec read (2026-06-24): **§11.2/D42 makes Git/`.vindex` the authoritative medium for EVERY content class — NO class is weights-authoritative** (zero "weights authoritative" hits), AND there is **no delete-time "must-not-fire"/closed-world/erasure clause** (zero hits). So a secret resurfacing in raw weights **confirms** deletion lives in the overlay/tombstone/authoritative-medium layer (R2-class architecture finding) — it does **NOT falsify** the spec. The result will be written as: *(a) empirical grounding of §11.2 (in-weight corrective-delete is/ isn't complete → the overlay is/isn't load-bearing for deletion+confidentiality)* + *(b) a delete-time-L2 spec-gap flag*. **No "R9 falsified in-weight" claim will be made.**

## The question (characterization)
The spec's DELETE goes "via the standard write path" (IC-PA4) = a MEMIT operation. CORPUS/08 found LARQL's DELETE is a feature-level **patch-overlay** delete. The prior program showed only **T2.1 snapshot-revert** (bit-identical un-write — resurfaces nowhere by construction, tautological for deletion-completeness). **UNTESTED:** does a **corrective** in-weight delete (a NEW write-path edit driving the fact off, NOT a snapshot restore) **completely** remove a fact, or does it leave **residue** that resurfaces on a held-out paraphrase it never explicitly touched?

## Design — fictional-secret write → corrective delete → held-out resurfacing
### Stimulus
N=24 fictional secrets, single entities, single-token "code" targets. Edit prompt `"The secret access code for {} is"` / subject=entity / `target_new=" <CODE>"` (single-token, screened). Fictional → no native prior.

### Phases
1. **WRITE** (single joint AlphaEdit batch, canonical-only, cache_c from 0). Capture each secret's **pre-write canonical top-1** token (the delete target — restores "no such fact" behavior, a faithful corrective un-write, NOT a snapshot restore).
2. **WRITE GATES + distribution:** per secret record canonical-took (top-1==CODE) and **held-out-paraphrase firing pre-delete** (does the write *generalize* to a paraphrase neither write nor delete will touch — `"Only insiders know that {}'s access code is"`, `"{}'s secret access code happens to be"`). Only secrets that (canonical-took) AND (generalized to ≥1 held-out paraphrase) are **informative** for resurfacing (else "resurfacing" is vacuous).
3. **DELETE** (second accumulating AlphaEdit batch, **canonical-only — matched breadth to the write**) on **half** the secrets (the DELETE group, 12); the other half (CONTROL group, 12) is left written. Delete target = the captured pre-write canonical top-1. **DELETE-TOOK GATE:** post-delete canonical top-1 must be the redaction token (CODE no longer top-1) at strength comparable to the original write — else that secret is excluded (a failed delete is not "residue").
4. **POST-delete probes:** canonical (CODE gone?) + held-out paraphrase (does CODE **resurface** / still rank top-1?), for both groups.

### Controls (advisor-mandated, matched-breadth)
- **Matched breadth:** write & delete BOTH canonical-only; resurfacing tested on a **held-out paraphrase neither touched** → "write-canonical generalized to held-out paraphrase, but delete-canonical fails to suppress it there" is a *fair* asymmetry (not an artifact of deleting more narrowly than writing).
- **Undeleted CONTROL group:** the 12 non-deleted secrets must still fire on canonical + held-out paraphrase → deletion is **specific**, not a global wipe (and not weight damage).
- **Delete-took gate** (above) — excludes failed-deletes from the residue numerator.

### Metric (matched to the characterization claim)
Primary = among DELETE-group secrets passing {write-took ∧ pre-delete paraphrase-fired ∧ delete-took}, the **fraction that still show CODE (top-1 or high-rank) on the held-out paraphrase post-delete** = **residue rate**. Paired vs the CONTROL group's post "delete" (no-op) paraphrase firing. Hand-adjudicate top-k if the top-1 oracle is ambiguous ([[pass-label-not-equal-promotable-claim]]).

## Pre-registered readout (CHARACTERIZATION — both directions informative, NEITHER falsifies)
- **Residue HIGH** (deleted secrets resurface on held-out paraphrase despite canonical redaction): in-weight corrective-delete is **incomplete** → **empirically grounds §11.2** — weights cannot be the authoritative medium for deletion/confidentiality; the overlay/tombstone layer is **load-bearing** (architecture confirmed, the deletion analog of the corruption evidence behind D-B3N-1). + delete-time-L2 spec-gap flag.
- **Residue LOW** (deletion suppresses the secret even on untouched paraphrases): in-weight corrective-delete is **surprisingly complete** at this scope → weight-deletion is *sufficient* for the behavioral half here (still doesn't make weights *authoritative* — that's a §11.2 contract, not an empirical property).
- **CONTROL violated** (undeleted secrets stop firing, or deletion is global): instrument fail → HALT/re-scope.

## Honest scope / caveats
- Single model (3B) / single band / 1 seed / N=24 / fictional-secret domain / deterministic top-1 + hand-adjudication. Composition/multi-hop deferred. "Corrective delete = edit toward pre-write top-1" is ONE faithful operationalization of write-path deletion; redaction-to-sentinel is an alternative (v2).
- Does NOT test the overlay/`.vindex` tombstone path (that's the GOV-authoritative half, by construction effective) — this isolates the **weights-derived** behavior the spec treats as non-authoritative.
