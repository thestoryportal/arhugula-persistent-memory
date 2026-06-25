import os, json, time, hashlib
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")

# ============================================================================
# R11 — Content-scoped authoritative-medium & severity ON READ.
# Pre-reg: docs/R11_MEDIUM_ON_READ_PREREG.md (frozen). NOT a falsifier (matrix
# category ③, medium-delegated per §11.2). SPEC-COHERENCE / spec-gap audit.
#
# The harness contains NO resolver we grade ourselves against (that would be the
# prototype-tautology-trap the advisor flagged). It asserts ONLY over the spec's
# read-surface inventory (each field carries its spec line citation), builds a
# 2-medium store, injects a Git<->.vindex divergence per content-class, and
# mechanically derives, per class, whether (a) medium/class and (b) severity are
# determinable AT READ from a spec-stated read-result field — else which off-read
# mechanism (D43/§11.7/A8) covers it, else SPEC-GAP. CPU-only, no model.
# ============================================================================

SPEC = "research_and_specs/llm-as-database-v1_2-integrated-spec.md"

# ---- ⚠ DISCRIMINATING FINDING (advisor 2026-06-25, post-run): the spec ships NO
#      formal query-language section / query-RESULT schema. The only SELECT mention
#      (§8.9 line 391) is an EXISTENCE read-back; §8.5 .larql is the WRITE patch
#      format, not a query result. So the read-RETURN SHAPE IS ITSELF UNSPECIFIED.
#      Consequence: we CANNOT assert "reads don't return entity_type" (the original
#      runner silently baked that in). §7.2/C4 mandates every entity IS typed -> IF
#      a read returns the typed entity, content-class AND severity are DERIVABLE
#      (severity via the SAME §11.7 function). The residual is therefore the ONE
#      already-recorded root gap ("no formal query-language section"), NOT three new
#      gaps -> F1 must NOT double-count. See verdict.
#
# ---- read-surface inventory: every field the spec exposes in a read/query RESULT,
#      each with its exact spec citation. Verified by exhaustive grep (see pre-reg).
#      A reviewer falsifies the verdict by citing a read-result field omitted here. ----
READ_RESULT_SURFACE = [
    {"field": "provenance_flag", "values": ["STALE", "UNAVAILABLE"],
     "spec": "§26.3 (line 1871)", "scope": "Layer-4 EXTERNAL-sourced facts only",
     "carries_class": False, "carries_medium": False, "carries_severity": False,
     "note": "advisory staleness of an external source; not content-class, not medium, not recoverability-severity"},
    {"field": "coverage_quality", "values": ["(flag)"],
     "spec": "IC4 (line 2130)", "scope": "all query results",
     "carries_class": False, "carries_medium": False, "carries_severity": False,
     "note": "empty/low-coverage routing to doc ingestion; not class/medium/severity"},
    {"field": "select_readback_exists", "values": [True, False],
     "spec": "§8.9 L1 (line 391)", "scope": "all committed edges",
     "carries_class": False, "carries_medium": False, "carries_severity": False,
     "note": "confirms the edge was written (existence); no class/medium/severity on the returned value"},
]

# ---- OFF-READ mechanisms the spec specifies for content-class / divergence /
#      severity (none on the read path). Used to score DELEGATED-COHERENT. ----
OFF_READ_MECHANISMS = [
    {"name": "CONTENT_CLASSIFICATION (write-time)", "spec": "§11.2/D42 (line 638)",
     "phase": "write", "covers": "class assignment + authoritative medium (Git vs .vindex)",
     "on_read_path": False},
    {"name": "class-differentiated compensation", "spec": "§11.7/D47 (line 690)",
     "phase": "commit/compensation", "covers": "severity asymmetry (structural=auto-revert Git; L4=retry x5, Git-revert needs human)",
     "on_read_path": False},
    {"name": "strong consistency / reads block, no stale-read fallback", "spec": "§11.3/D43 (line 642)",
     "phase": "read-mount", "covers": "PREVENTS steady-state read divergence (reads block during mount)",
     "on_read_path": True, "prevents_divergence": True, "resolves_at_read": False},
    {"name": "circuit-breaker -> READ_ONLY + originating_category", "spec": "§11.8/A8 (lines 706/2411)",
     "phase": "fault", "covers": "DIVERGED_STATE -> immediate system-wide trip; category for reset branch (INTEGRITY/CONSISTENCY/SECURITY)",
     "on_read_path": False, "system_wide": True, "is_content_class": False},
]

# ---- §11.2/D42 authoritative-medium-by-content-class (the contract under test) ----
AUTH_MEDIUM = {  # entity_type -> (CONTENT_CLASSIFICATION, authoritative medium, recoverability-severity if read-error)
    "structural_entity": ("structural",   "git",     "RECOVERABLE (Git is authoritative; re-read/restore from Git)"),
    "domain_concept":    ("layer4_domain", "vindex",  "DATA_LOSS_RISK (.vindex authoritative; no Git ground truth for L4)"),
    "constraint_rule":   ("layer4_domain", "vindex",  "DATA_LOSS_RISK + SAFETY (.vindex authoritative; a lost constraint is a silent safety gap)"),
}

# ---- 2-medium store with an injected Git<->.vindex divergence per class ----
def build_diverged_store():
    facts = [
        # (entity, type, relation, git_value, vindex_value)  -- values DISAGREE (injected divergence)
        ("auth_module",   "structural_entity", "defined_in",   "src/auth/v2.py", "src/auth/v1.py"),
        ("OAuth2",        "domain_concept",    "describes",    "RFC-6749-draft", "RFC-6749"),
        ("no_plaintext",  "constraint_rule",   "must_not_contain", "logs-only",   "logs+db"),
    ]
    store = []
    for ent, etyp, rel, gitv, vidxv in facts:
        cc, medium, severity = AUTH_MEDIUM[etyp]
        store.append({"entity": ent, "entity_type": etyp, "relation": rel,
                      "content_classification": cc, "authoritative_medium": medium,
                      "recoverability_severity": severity,
                      "git_value": gitv, "vindex_value": vidxv,
                      "diverged": gitv != vidxv})
    return store

# ---- The read: a SELECT that may consult ONLY the spec-stated read-result surface ----
def select_via_spec_read_surface(fact):
    """Return what a querying agent can observe at read time per the spec, and
    whether (a) medium/class and (b) severity are determinable from it.
    Crucially: provenance_flag is L4-EXTERNAL only; our L4 facts are Genesis/
    Architect-authored (§7.7 L4), NOT external-sourced -> the flag does not apply."""
    observable = {}
    for f in READ_RESULT_SURFACE:
        if f["field"] == "provenance_flag":
            # §26.3 scope: external-sourced L4 only. Genesis-authored L4 + structural -> N/A.
            observable[f["field"]] = None  # not populated for any fact in this store
        elif f["field"] == "coverage_quality":
            observable[f["field"]] = "OK"  # non-empty result; no class/medium/severity content
        elif f["field"] == "select_readback_exists":
            observable[f["field"]] = True  # the edge exists in (at least) one medium
    # Can the agent determine (a) authoritative medium / content-class from a READ-RESULT field?
    medium_determinable_at_read = any(
        f["carries_medium"] or f["carries_class"] for f in READ_RESULT_SURFACE
    )
    # Can the agent class-differentiate (b) severity from a READ-RESULT field?
    severity_determinable_at_read = any(f["carries_severity"] for f in READ_RESULT_SURFACE)
    return observable, medium_determinable_at_read, severity_determinable_at_read

# ---- The read-RETURN shape is itself UNSPECIFIED (no query-result schema in the
#      spec). But §7.2/C4 mandates every entity IS typed. So content-class is a
#      deterministic function of entity_type, and severity is the SAME function
#      §11.7 already uses. => IF a read returns the typed entity (the natural shape
#      given C4), both axes are DERIVABLE. We record this conditional explicitly. ----
READ_RETURN_SHAPE_SPECIFIED = False  # grep: §8.9 SELECT = existence read-back only; no query-result schema
ENTITY_TYPING_MANDATED = True        # §7.2/C4: untyped entity = schema violation
def derivable_if_type_returned():
    # class derivable from type (§11.2 maps type->class); severity derivable via §11.7's class function
    return ENTITY_TYPING_MANDATED

# ---- Scoring (revised post-advisor: credit DERIVATION, be consistent with axis-a) ----
def score_axis(determinable_from_read_field, off_read_prevents):
    if determinable_from_read_field:
        return "COHERENT"                     # a read-RESULT field carries it directly
    if derivable_if_type_returned() and not READ_RETURN_SHAPE_SPECIFIED:
        return "DERIVABLE-IF-TYPE-RETURNED"   # coherent IF the (unspecified) query-result schema returns entity_type
    if off_read_prevents:
        return "DELEGATED-COHERENT"           # off-read mechanism forecloses the failure mode
    return "SPEC-GAP"

def main():
    store = build_diverged_store()
    per_class = []

    # off-read coverage facts (same for all classes; cited)
    d43 = next(m for m in OFF_READ_MECHANISMS if "D43" in m["spec"])
    comp = next(m for m in OFF_READ_MECHANISMS if "D47" in m["spec"])
    a8 = next(m for m in OFF_READ_MECHANISMS if "A8" in m["spec"])

    for fact in store:
        observable, med_at_read, sev_at_read = select_via_spec_read_surface(fact)

        # (a) MEDIUM/CLASS-ON-READ
        # No read-RESULT field carries medium/class (med_at_read=False), AND the read-return
        # shape is unspecified -> DERIVABLE-IF-TYPE-RETURNED (class = f(entity_type), §11.2).
        # ADDITIONALLY: D43 PREVENTS the "wrong medium wins on read" divergence failure mode
        # (reads block during mount, no stale-read fallback) -> that failure is foreclosed
        # regardless of return shape. So axis (a) is doubly coherent.
        a_verdict = score_axis(med_at_read, off_read_prevents=d43.get("prevents_divergence", False))
        a_off = {"derivation": "class = f(entity_type) via §11.2/D42; entity_type mandated §7.2/C4",
                 "prevention_of_divergence": {"covers": d43.get("prevents_divergence", False),
                                              "mechanism": d43["name"], "spec": d43["spec"]},
                 "note": "medium identification is derivable IF the (unspecified) query result returns entity_type; "
                         "the 'wrong medium wins on read' FAILURE is separately foreclosed by D43 prevention."}

        # (b) SEVERITY-ON-READ
        # No read-RESULT field carries severity (sev_at_read=False). No off-READ mechanism
        # PREVENTS a missing read-severity (severity asymmetry exists at commit §11.7 and
        # fault A8, but neither surfaces per-read content-class severity). So the only
        # coherence path is DERIVATION: severity = the SAME §11.7 function of content-class,
        # which is f(entity_type) -> DERIVABLE-IF-TYPE-RETURNED.
        b_verdict = score_axis(sev_at_read, off_read_prevents=False)
        b_off = {"derivation": "severity = §11.7 class-function of content-class = f(entity_type); "
                               "DERIVABLE IF the read returns entity_type",
                 "compensation_severity": {"mechanism": comp["name"], "spec": comp["spec"], "phase": comp["phase"]},
                 "circuit_category": {"mechanism": a8["name"], "spec": a8["spec"], "phase": a8["phase"],
                                      "system_wide": a8.get("system_wide"), "is_content_class": a8.get("is_content_class")},
                 "note": "severity differentiation is specified at commit & fault, NOT at read; "
                         "no read-result severity field (cf. §26.3 provenance_flag exists but is L4-external-only). "
                         "Coherent ONLY via type-derivation, which depends on the unspecified query-result schema."}

        per_class.append({
            "entity": fact["entity"], "entity_type": fact["entity_type"],
            "content_classification": fact["content_classification"],
            "authoritative_medium_per_spec": fact["authoritative_medium"],
            "recoverability_severity_per_spec": fact["recoverability_severity"],
            "diverged_git_vs_vindex": {"git": fact["git_value"], "vindex": fact["vindex_value"],
                                       "diverged": fact["diverged"]},
            "read_observable_fields": observable,
            "provenance_flag_applies": fact["content_classification"] == "layer4_domain" and False,  # external-only; these are Genesis-authored
            "axis_a_medium_on_read": {"determinable_at_read": med_at_read, "off_read": a_off, "verdict": a_verdict},
            "axis_b_severity_on_read": {"determinable_at_read": sev_at_read, "off_read": b_off, "verdict": b_verdict},
        })

    # Aggregate verdicts (consistent across classes by construction of the spec surface)
    a_verdicts = {c["axis_a_medium_on_read"]["verdict"] for c in per_class}
    b_verdicts = {c["axis_b_severity_on_read"]["verdict"] for c in per_class}

    # Sub-finding: provenance_flag (§26.3) is the ONE read-result quality field, but
    # scoped to L4-EXTERNAL only -> Genesis-authored L4 + ALL structural facts get no
    # read-time quality/medium/severity surface at all.
    coverage_holes = {
        "structural_entity": "no read-result quality field at all (provenance_flag is L4-external-only)",
        "domain_concept_genesis": "Genesis/Architect-authored L4 (not external) -> provenance_flag N/A -> no read-result quality field",
        "domain_concept_external": "provenance_flag applies (STALE/UNAVAILABLE) -> staleness surfaced, but still no medium/recoverability-severity field",
        "constraint_rule": "same as L4 domain; a lost/diverged constraint is silent at read (no severity surface) -> safety-relevant gap",
    }

    result = {
        "experiment": "R11_medium_on_read",
        "decision_id": "D-R11-1",
        "class": "SPEC-COHERENCE / SPEC-GAP AUDIT (NOT a falsifier; matrix category 3; NOT promotable)",
        "spec_file": SPEC,
        "ts": round(time.time(), 3),
        "read_result_surface_inventory": READ_RESULT_SURFACE,
        "off_read_mechanisms": OFF_READ_MECHANISMS,
        "auth_medium_contract_under_test": {k: {"content_classification": v[0], "medium": v[1], "severity": v[2]}
                                             for k, v in AUTH_MEDIUM.items()},
        "per_class": per_class,
        "aggregate": {
            "axis_a_medium_on_read": sorted(a_verdicts),
            "axis_b_severity_on_read": sorted(b_verdicts),
        },
        "coverage_holes": coverage_holes,
        "self_consistency_note_NOT_validation": {
            "warning": "This is NOT empirical validation. The runner's output is fully determined by the "
                       "hardcoded carries_class/medium/severity=False flags on READ_RESULT_SURFACE, which are "
                       "MY encoding of MY spec-reading. A 'match' here = my encoding agreeing with my reading "
                       "(a documentation echo), not an independent check. The finding's entire validity = the "
                       "COMPLETENESS of the spec read (falsifiable by citing an omitted read-result field).",
            "a_observed": sorted(a_verdicts), "b_observed": sorted(b_verdicts),
        },
        "read_return_shape_specified": READ_RETURN_SHAPE_SPECIFIED,
        "verdict": None,  # set below
        "root_gap_attribution": (
            "R11 is an INSTANCE of the ONE already-recorded root gap, NOT a set of new independent gaps. "
            "Matrix already records: 'the spec specifies read requirements (exact/reverse/traverse) but ships "
            "NO formal query-language section — the least-specified production surface.' Because the "
            "read-RETURN shape is unspecified, R11's medium-on-read and severity-on-read questions cannot be "
            "answered from spec text -> they restate that gap at the medium/severity altitude. F1 MUST NOT "
            "double-count these as new conditions."),
        "spec_observations": [
            "O-R11-1: NO query-result schema. The read-RETURN shape is unspecified (§8.9 SELECT = existence "
            "read-back only; §8.5 .larql is the WRITE format). => whether a read returns entity_type, class, "
            "medium, or severity is simply not stated.",
            "O-R11-2: IF the (unspecified) query result returns the typed entity (the natural shape, since "
            "§7.2/C4 MANDATES every entity is typed), THEN content-class = f(entity_type) via §11.2/D42, and "
            "severity = the SAME §11.7 class-function -> BOTH axes become COHERENT-via-derivation. The residual "
            "is therefore narrow: the spec should pin the query-result schema to include entity_type (or a "
            "derived class/severity convenience field). This is a clarification, not a deep under-specification.",
            "O-R11-3: ONE read-result quality field DOES exist (§26.3 provenance_flag STALE/UNAVAILABLE) but is "
            "scoped to L4-EXTERNAL facts only -> the pattern of surfacing read-quality exists; structural + "
            "Genesis-authored-L4 + constraint facts get no analogous flag. A diverged/lost constraint_rule is "
            "silent at read (safety-adjacent; ties to C8/R15) UNLESS class/severity is derived from a returned type.",
        ],
        "what_is_coherent": [
            "C-R11-1: 'wrong medium wins on a read divergence' is FORECLOSED BY PREVENTION (§11.3/D43 strong "
            "consistency: reads block during mount, no stale-read fallback) + DIVERGED_STATE -> immediate "
            "system-wide circuit trip (§11.8). The spec answers the failure mode by prevention, not by a "
            "read-time medium resolver -> no tautological 'our resolver picks right' claim is needed.",
            "C-R11-2: content-class authoritative-medium IS fully specified at write/commit (§11.2/§11.7) -> "
            "R11 is correctly medium-delegated (matrix category 3). class+severity are DERIVABLE from the "
            "mandated entity_type. The only residual is whether the query-result schema (unspecified) surfaces/returns it.",
        ],
        "scope_caveats": "Spec-coherence audit of v1.2 read surface; CPU-only; no model; 3 content-classes, "
                         "injected divergence. NOT a falsifier, NOT a CP-class delivery, NOT promotable. Output is "
                         "a documentation echo of the spec reading, not an independent check (see self_consistency_note). "
                         "Falsifiable by a reviewer citing a read-result field / query-result schema clause omitted here.",
    }

    # Verdict string
    a = "/".join(sorted(a_verdicts)); b = "/".join(sorted(b_verdicts))
    result["verdict"] = (
        f"axis-(a) medium/class-on-read = {a} (+ divergence-failure foreclosed by D43 prevention); "
        f"axis-(b) severity-on-read = {b}. Net: R11 medium-AUTHORITY is coherent — divergence is "
        "prevented (D43) and class/severity are DERIVABLE from the §7.2/C4-mandated entity_type via "
        "§11.2/§11.7. The ONLY residual is that the spec ships no query-result schema, so it does not "
        "state the read RETURNS the type (or a derived class/severity field). That residual is an INSTANCE "
        "of the already-recorded root gap ('no formal query-language section'), NOT a new condition -> do "
        "not double-count in F1. Recommendation: pin the query-result schema to include entity_type. "
        "Prototyped-not-empirical; characterization; NOT promotable.")

    out = f"{LLMDB_ROOT}/results/r11_medium_on_read.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(result, open(out, "w"), indent=2)
    print("WROTE", out)
    print("axis-(a) medium-on-read :", sorted(a_verdicts))
    print("axis-(b) severity-on-read:", sorted(b_verdicts))
    print("read_return_shape_specified:", READ_RETURN_SHAPE_SPECIFIED)
    print("spec_observations:", len(result["spec_observations"]),
          "| root-gap attribution: instance of known 'no query-language' gap (NOT new)")

if __name__ == "__main__":
    main()
