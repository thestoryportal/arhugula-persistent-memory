# BK3 semantic review notes — not final match counts

## Completed comparison work

The 58 original PROGRAM SAME-NAME rows all have a reviewed comparison in
`program_same_name_review.tsv`. Counts are: 32 filesystem-byte copies, six
whitespace-content copies, one complete archive-payload copy, one parsed-JSON
copy, three older revisions, one older manifest subset, one different trial
cohort, one divergent URL list, one divergent manifest, two divergent Markdown
skill revisions, eight divergent archives, and one wrong-subject basename.
These are comparison outcomes, not the final original method's EXACT / CONTENT
/ UNIQUE categories. Final semantic content/rename adjudication is still open.

Every member of the 12 non-byte-copy skill archives was inspected in
`program_archive_comparisons.jsonl`. `framework-spec-writer.skill` contains two
members and lacks a same-role current archive; it remains a content-search
candidate. Do not execute any of these skills: they are audited data.

`llm-as-database/orchestration-comparativist.skill` contains one SKILL.md member;
the member name and entire payload are equal to the repo archive. Container
bytes differ. This resolves BK2's warning that one matching member would not
establish whole-archive payload identity. This is CONTENT identity, not EXACT.

The other role archives differ meaningfully: current role packages add
interface contracts, synthesis/verification gates and other instructions.
Full differences, including short/frontmatter lines omitted from BK2's
distinct-line index, are preserved. Neither 100% long-line coverage nor
container mtime is a whole-document identity or chronology receipt.

## Specific preservation candidates and cautions

- `stage_1_sect_runbook_v1_6.md` and its `(1)` copy explicitly identify the
  S2.17 hardening revision at backup :12; they are later revisions than
  `architecture_profile/runbooks/stage_1_sect_runbook_v1_5.md:12` in content,
  not merely mtime. Saved pair diff has 228 removed / 90 added lines when
  comparing backup v1.6 to current v1.5. v1.6 adds the canonical marker site,
  cache-inventory subset predicate, provenance field reconciliation and
  reference-table refresh. This does not establish that no later revision
  exists elsewhere, or authorize replacing a live runbook. The v1.6 copies
  have the same inventoried SHA256 and should be grouped as one payload.
- `llm-as-database/orchestration-comparativist.md` has 93 additional lines
  relative to the current role ZIP payload, headed Orchestration-Owned
  Interface Contracts and including IC-HIL-RETURN. Treat as a divergent
  revision; chronological ordering is not proven from this addition alone.
- The root reproducibility manifest contributes 181 leaf values under
  `sessions` not present in `reproducibility_manifest_merged_s236.json`,
  despite that counterpart containing 896 extra leaves. Six changed shared
  values are metadata. This is mixed history, not a globally newer backup.
- The llm-as-database manifest preserves 338 leaves that all exist unchanged
  in the merged worktree manifest, which adds 1,055 leaves. The old archived
  v2 manifest has no backup-only leaves versus that merged manifest; two
  changes are version/purpose metadata. The seed manifest is a different
  early GPT-J provenance structure with 139 backup-only paths, not a new
  complete version of the merged manifest.
- Root `llm_research_tools_repos.md` is a raw URL list, not the current
  same-name synthesis. Against `.source_urls.txt`, six backup lines differ
  and two counterpart lines differ: four URLs absent from that source list
  and two URL variants (repository root vs nested path / capitalization).
  Do not import a raw list over the current synthesis.
- `aggregate_verdict.json` describes the early nine-trial cohort; the repo's
  later result describes 15 different trials. `stage_2_sweep_verdict.json`
  instead has parsed object equality (436 equal leaves) to the sibling
  mirror result. Neither is a historical EXACT match.
- Backup ROME patches are explicit v0.1; repo patches are explicit v0.2
  absorbing S2.18 findings. Backup T1 high-AKD runbook differs in one line
  requiring operator-authored placeholders that the current source marks
  fully authored at repo :437. Both are older documentation states.
- `deep-research-report.md` has a relevant content counterpart at
  `research_and_specs/predecessor_design/memit-llama-deep-research-distillation.md`.
  Four of 32 phrase anchors match; the full pair diff is saved. It is a
  distinct source report in the same failed-cache-search research family,
  not covariance bytes or independently verified external evidence.
- Both `framework_finding_memit_ceiling_archival` copies have the relevant
  counterpart `docs/framework_findings/framework_finding_memit_ceiling_archival_v1_1.md`.
  The counterpart says it is an additive amendment of permanent v1.0 with
  S2.18 ROME findings. This is stronger than BK2's no-hit queue; inspect the
  saved full diffs and narrative before deciding whether original v1.0
  merits history preservation. Do not label these UNIQUE merely because
  the original exact-line search found no hits.

## Contextual HTML relevance

The five fallback HTML pages are ADF/ArhuGula planning artifacts, not empirical
LLM-as-Database results. `09-design-architecture.html:228-241` has substantive
frozen-base / .vindex / .larql / MEMIT / transaction-controller mapping.
`index.html:451-452` discusses mapping approved artifacts to .larql patches.
`07-augmentation-models.html:189` uses LLM-as-database as an activation example.
`08-v1-approaches.html:235-253` discusses a graph-native alternative and a
council kernel. `12-visual-mindmap-infographic.html:400-401,577-593` explicitly
distinguishes its session/context/state management from an LLM-as-database
design. Their final relevance labels must reflect these differences; the
original 292-row cohort should remain traceable through any overrides.

## BK3C referrals

BK3C's 67 groups cover all 10,029 original ADJACENT rows. It referred six root
role `.skill` files plus `s3-spec-writer-architecture.md` for PROGRAM review.
The six role descriptions explicitly scope themselves to this program;
all six are verified historical EXACT in `program_referral_receipts.jsonl`.
Their inventory hashes were rechecked. Treat them as PROGRAM in a final
relevance override, while preserving the original C denominator. They add
six program rows if no other relevance changes are made.

`s3-spec-writer-architecture.md:66-73` explicitly drops artifacts from the
prior LLM-as-DB council for a different slate. The document's main subject
is that new slate's Spec-Writer architecture (source :1-7). Retaining it as
ADJACENT/contextual reference is supported; it does not restore lost science.
It has not been declared UNIQUE as a program document.

## Content-search limits and next review

The corrected supplemental search in `program_anchor_evidence.jsonl` searches
six-token phrases independent of capitalization, punctuation and wrapping.
It covered 41,399 filesystem research text/archive files and 12,475 historical
blobs, including larger historical research text excluded by BK2. There are
164 file/member queries, all with nonempty anchor sets; 51 have candidate
hits and 113 have none. These are NOT file match counts or UNIQUE verdicts.
Twenty-two historical and 101 filesystem JSON/IPYNB files >2 MiB remain
excluded from text indexing; byte searches still cover same-size copies.
Dependency/cache trees and unreachable Git history remain outside scope.

The first BK3 phrase run wrongly demanded anchors unique among all backup
documents, which left duplicated/version-family documents without anchors.
That run is superseded by the corrected run: shared rare phrases are now
used when unique anchors are insufficient. The final state and evidence
were rewritten only after successful completion. The successor must use
the corrected state, not the earlier stdout/summary.

`program_document_review.jsonl` preserves per-section bounded extracts for
all non-EXACT non-archive documents. `program_pair_diffs.jsonl` combines the
initial same-name counterpart, BK2 content candidates, corrected phrase
candidates, and merged-manifest comparisons. Whole-body diff reads are only
for sources <=200 KiB; larger sources have streamed section extracts/search
evidence and explicit unavailable-whole-diff flags. Candidate overlap is
not whole-document equality. Resolve the 140 initial CONTENT-PENDING files
with these receipts before generating final match counts and gap rows.

Use `loss_evidence.md` and the saved systematic search for loss mapping. No
recorded-loss mapping has been guessed, and no lost tensor/model/cache/build
bytes have been claimed recovered. For ordinary historical documents without
an explicit loss record, the requested gap-table entry is `none`.
