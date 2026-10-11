#!/usr/bin/env python3
"""organize_llm_as_database.py v2

Artifact organizer for the LLM-as-Database project.

Discovers all files under SOURCE, classifies each via priority-ordered
regex rules, identifies current vs. superseded versions per family,
detects duplicate-suffix candidates, and reorganizes into a canonical
directory structure under TARGET.

CHANGELOG (v1 → v2):
    Defect closures from v1 manifest audit:
      A. @stem family collapse — fixed via mandatory v-prefix in strip regex
      B. Version extraction failures — fixed via anchored [-_]v(<ver>)
      C. Specialist-skill miscategorization — three new rules
      D. Session-form narrowness — five new rules
      E. Council transcripts split — new transcript-session-N rule
    Schema additions:
      spec/transcripts/, spec/predecessor_design/, spec/calibration/,
      spec/proposals/, sessions/workstream_1/blocks/, sessions/
      workstream_1/_substep/, sessions/workstream_1/_ancillary/,
      skills/friction_logs/, skills/raw_skill_files/, meta/
    New capabilities:
      Improved validation diagnostics; duplicate-suffix detection;
      manifest-extended; --trace for rule-index emission.

USAGE
    # Dry-run (default — no filesystem mutation; full plan printed)
    python3 organize_llm_as_database.py ~/Downloads/llm-as-databse

    # Execute (copy mode — source preserved)
    python3 organize_llm_as_database.py ~/Downloads/llm-as-databse --execute

    # Execute (move mode — source destroyed)
    python3 organize_llm_as_database.py ~/Downloads/llm-as-databse --execute --move

    # Override target
    python3 organize_llm_as_database.py SRC --target ~/projects/lad --execute

    # Trace rule-index per file (debugging rule-set)
    python3 organize_llm_as_database.py SRC --trace

EXIT CODES
    0  success (or successful dry-run)
    1  source path invalid (missing / file / broken symlink / not a dir)
    2  source == target (refusing to operate)
    3  one or more I/O errors during execution
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────
# Categorization rules — priority-ordered. First match wins.
#
# Each rule:
#   pattern : regex matched against filename only (case-insensitive),
#             optional named group 'ver' captures version string
#   target  : subdirectory under TARGET_ROOT for current files;
#             superseded files land under target/_archive/
#   family  : grouping policy — controls current-vs-superseded
#             '@unique'  : each file is its own family
#             '@stem'    : derive family from filename stem (strip v-version)
#             '@dynamic' : derive family from named regex group 'sess'
#             other str  : literal shared-family identifier
# ─────────────────────────────────────────────────────────────────────────

CATEGORY_RULES: list[dict] = [
    # ═════════════════════════════════════════════════════════════════
    # SPEC — versioned canonical artifacts
    # ═════════════════════════════════════════════════════════════════
    {
        # llm-as-database-v1_2-integrated-spec.md, .txt
        'pattern': r'^llm-as-database[-_]v(?P<ver>[\d_.]+)[-_].*integrated.*spec.*\.(md|txt)$',
        'target': 'spec/integrated',
        'family': 'llm-as-database-integrated-spec',
    },
    {
        # memit-patches-canonical-v2.4.md, memit-patches-canonical_v1.md, memit-patches-canonical-2.md
        'pattern': r'^memit-patches-canonical[-_]?v?(?P<ver>[\d.]+)\.md$',
        'target': 'spec/memit-patches-canonical',
        'family': 'memit-patches-canonical',
    },

    # ═════════════════════════════════════════════════════════════════
    # SPEC — runbooks (anchored version extraction; v2 fix)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^stage_1_sect_runbook[-_]v(?P<ver>[\d.]+)\.md$',
        'target': 'spec/runbooks/stage_1_sect',
        'family': 'stage_1_sect_runbook',
    },
    {
        # Unversioned + duplicate-suffix variants (manifest showed three)
        'pattern': r'^stage_1_sect_runbook(\s*\(\d+\)|\s+copy)?\.md$',
        'target': 'spec/runbooks/stage_1_sect',
        'family': 'stage_1_sect_runbook',
    },
    {
        'pattern': r'^pre_(?P<sess>s\d+_\d+[a-z]?)_fork_work_runbook(?:[-_]v(?P<ver>[\d.]+))?\.md$',
        'target': 'spec/runbooks/pre_fork_work',
        'family': '@dynamic',
    },
    {
        'pattern': r'^.*[-_]runbook(?:[-_]v(?P<ver>[\d.]+))?\.md$',
        'target': 'spec/runbooks/misc',
        'family': '@stem',
    },

    # ═════════════════════════════════════════════════════════════════
    # SPEC — Council transcripts (NEW v2; closes defect E)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^transcript[-_]session[-_]\d+.*\.md$',
        'target': 'spec/transcripts',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SPEC — Predecessor design artifacts (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^(llm-as-database-agent-harness-framework|'
                   r'llm-memory-layer|'
                   r'llm-harness-memory-framework-gemini-chat|'
                   r'ontological-schema-llm-databse?-agent-framework|'
                   r'syncing-git-vindex-two-phase-commit|'
                   r'threat-modeling-write-layer-access-control|'
                   r'validation-architecture-reflexion-loop-design)\.md$',
        'target': 'spec/predecessor_design',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SPEC — Calibration protocols (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^(compaction-probe-calib|epsilon-calib|judge-calib|'
                   r'memit-compat)[-_]proto[-_]\d+\.md$',
        'target': 'spec/calibration',
        'family': '@unique',
    },
    {
        'pattern': r'^stage_\d+_compat_assessment\.md$',
        'target': 'spec/calibration',
        'family': '@unique',
    },
    {
        'pattern': r'^interface-contracts-ic-review[-_]v(?P<ver>[\d.]+)\.md$',
        'target': 'spec/calibration',
        'family': 'interface-contracts-ic-review',
    },

    # ═════════════════════════════════════════════════════════════════
    # SPEC — Proposals / decision records (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^(MEMIT_Target_Model_Recommendation.*|'
                   r'GPU_Procurement.*|'
                   r'write-engine-poc-scope.*|'
                   r'workstream-1_5-master-plan.*|'
                   r'Claude-Orchestration.*|'
                   r'poc-execution-plan-and-spec-revision-rule.*)\.md$',
        'target': 'spec/proposals',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SESSIONS — Workstream 1 canonical summary blocks
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^session[_-]2[._]\d+[a-z]?[_-]summary[_-]block.*\.md$',
        'target': 'sessions/workstream_1',
        'family': '@unique',
    },
    {
        'pattern': r'^pre_s2_\d+[a-z]?_fork_work_summary_block.*\.md$',
        'target': 'sessions/workstream_1',
        'family': '@unique',
    },
    {
        'pattern': r'^s2\d+[a-z]?_summary_block.*\.md$',
        'target': 'sessions/workstream_1',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SESSIONS — Workstream 1 sub-step summaries (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^session_2_\d+[a-z]?_step_\d+_\d+[_-].*\.md$',
        'target': 'sessions/workstream_1/_substep',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SESSIONS — Workstream 1 ancillary (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^session[_-]2[._]\d+[a-z]?[_-]'
                   r'(entry[-_]note|prompt|starter[_-]package|'
                   r'partial[-_]summary|resume[-_]prompt|starter[-_]prompt|'
                   r'to[_-]2[_.]\d+).*\.md$',
        'target': 'sessions/workstream_1/_ancillary',
        'family': '@unique',
    },
    {
        'pattern': r'^session-2_\d+-to-2_\d+.*\.md$',
        'target': 'sessions/workstream_1/_ancillary',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SESSIONS — Workstream 1 Block-N execution (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^block-\d+(-\d+)?-(execution-plan|session-prompt|'
                   r'resume-execution-plan|runpod-notebook|'
                   r'runbook-deltas).*\.md$',
        'target': 'sessions/workstream_1/blocks',
        'family': '@unique',
    },
    {
        'pattern': r'^session-2_\d+-runbook-deltas\.md$',
        'target': 'sessions/workstream_1/blocks',
        'family': '@unique',
    },
    {
        'pattern': r'^kaggle-canonical-notebook\.md$',
        'target': 'sessions/workstream_1/blocks',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SESSIONS — Phase 2 (historical)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^gap-session-\d+.*summary.*\.md$',
        'target': 'sessions/phase_2_archive/gap_sessions',
        'family': '@unique',
    },
    {
        'pattern': r'^gap-session-\d+.*\.md$',
        'target': 'sessions/phase_2_archive/gap_sessions',
        'family': '@unique',
    },
    {
        # gap-backlog-v5.md, gap-backlog-v1.md (v2 anchored extraction)
        'pattern': r'^gap[-_]backlog[-_]v(?P<ver>[\d.]+)\.md$',
        'target': 'sessions/phase_2_archive/backlog',
        'family': 'gap-backlog',
    },
    {
        # tension-map-v1.md, tension-map-v5.md (v2 anchored extraction)
        'pattern': r'^tension[-_]map[-_]v(?P<ver>[\d.]+)\.md$',
        'target': 'sessions/phase_2_archive/tension_analysis',
        'family': 'tension-map',
    },
    {
        'pattern': r'.*tension.*\.md$',
        'target': 'sessions/phase_2_archive/tension_analysis',
        'family': '@unique',
    },
    {
        'pattern': r'.*council.*\.md$',
        'target': 'sessions/phase_2_archive/council',
        'family': '@unique',
    },
    {
        'pattern': r'^oq[-_].*backlog[-_]?v?(?P<ver>[\d.]+)?\.md$',
        'target': 'sessions/phase_2_archive/oq_backlog',
        'family': '@stem',
    },

    # ═════════════════════════════════════════════════════════════════
    # HANDOFFS + KICKOFFS
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'.*kickoff.*\.md$',
        'target': 'handoffs/kickoffs',
        'family': '@unique',
    },
    {
        'pattern': r'.*handoff.*\.md$',
        'target': 'handoffs/handoff_guides',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # SKILLS — specialist artifacts (v2 closes defect C)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^(memit-specialist|graph-data-architect|'
                   r'ai[-_]?sec[-_]?ops?-specialist|'
                   r'state-consistency-theorist|orchestration-comparativist|'
                   r'validation-contract-architect|framework-council|'
                   r'framework-spec-writer)(\.skill)?\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        'pattern': r'^.*-friction-analysis\.md$',
        'target': 'skills/friction_logs',
        'family': '@unique',
    },
    {
        'pattern': r'^(memit-specialist|graph-data-architect|'
                   r'ai[-_]?sec[-_]?ops?-specialist|'
                   r'state-consistency-theorist|orchestration-comparativist|'
                   r'validation-contract-architect|framework-council|'
                   r'framework-spec-writer)-spec-design\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        'pattern': r'^.*-SKILL(-v\d+)?\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        'pattern': r'^SKILL\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        'pattern': r'^skill-design-decisions(-.*)?\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        'pattern': r'^.*-skills?-starter-descriptions\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        'pattern': r'^skill[-_](friction-log|refinement-log|refinement-priority-list)'
                   r'[-_]v(?P<ver>[\d.]+)\.md$',
        'target': 'skills/refinement_logs',
        'family': '@stem',
    },
    {
        'pattern': r'.*[-_]skill.*\.md$',
        'target': 'skills',
        'family': '@unique',
    },
    {
        # .skill extension — closes 8 unmatched from v1
        'pattern': r'.*\.skill$',
        'target': 'skills/raw_skill_files',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # CORPORA
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^cfb[-_]v(?P<ver>[\d.]+)\.(yaml|yml|md)$',
        'target': 'corpora/cfb',
        'family': 'cfb',
    },
    {
        'pattern': r'^cfb[-_].*\.(yaml|yml|md)$',
        'target': 'corpora/cfb',
        'family': '@stem',
    },
    {
        'pattern': r'^probe[-_]set[-_]v(?P<ver>[\d.]+)\.(yaml|yml|md)$',
        'target': 'corpora/probe_set',
        'family': 'probe-set',
    },
    {
        'pattern': r'^probe[-_]set.*\.(yaml|yml|md)$',
        'target': 'corpora/probe_set',
        'family': '@stem',
    },
    {
        'pattern': r'.*hparams.*\.json$',
        'target': 'corpora/configs',
        'family': '@unique',
    },
    {
        'pattern': r'^meta-llama.*\.json$',
        'target': 'corpora/configs',
        'family': '@unique',
    },
    {
        'pattern': r'^reproducibility_manifest.*\.json$',
        'target': 'corpora/configs',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # META — project meta-artifacts (NEW v2)
    # ═════════════════════════════════════════════════════════════════
    {
        'pattern': r'^(project-system-prompt-revised|'
                   r'framework-spec-iteration-guide|'
                   r'framework-spec-project-guide|'
                   r'v\d+-spec-synthesis-prompt)\.md$',
        'target': 'meta',
        'family': '@unique',
    },
    {
        'pattern': r'^gap-session-starter-prompts(-v(?P<ver>[\d.]+))?\.md$',
        'target': 'meta',
        'family': 'gap-session-starter-prompts',
    },
    {
        'pattern': r'^gap-session-schedule-v(?P<ver>[\d.]+)\.md$',
        'target': 'meta',
        'family': 'gap-session-schedule',
    },
    {
        'pattern': r'^(capture_.*|smoke_test|.*_helper|.*_script)\.py$',
        'target': 'meta/scripts',
        'family': '@unique',
    },
    {
        'pattern': r'^s2_\d+[a-z]?_artifact_checksums\.txt$',
        'target': 'meta/checksums',
        'family': '@unique',
    },

    # ═════════════════════════════════════════════════════════════════
    # GENERIC FALLTHROUGH (by extension)
    # ═════════════════════════════════════════════════════════════════
    {'pattern': r'.*\.json$',         'target': '_unsorted/json',     'family': '@unique'},
    {'pattern': r'.*\.(yaml|yml)$',   'target': '_unsorted/yaml',     'family': '@unique'},
    {'pattern': r'.*\.py$',           'target': '_unsorted/scripts',  'family': '@unique'},
    {'pattern': r'.*\.txt$',          'target': '_unsorted/text',     'family': '@unique'},
    {'pattern': r'.*\.md$',           'target': '_unsorted/markdown', 'family': '@unique'},
]


# ─────────────────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ParsedVersion:
    """Sortable version representation. Tolerates v1, v1.0, v1_2, v1.0.1."""
    raw: str
    tup: tuple

    @classmethod
    def parse(cls, raw: Optional[str]) -> Optional['ParsedVersion']:
        if not raw:
            return None
        norm = raw.replace('_', '.')
        parts = re.findall(r'\d+', norm)
        if not parts:
            return None
        return cls(raw=raw, tup=tuple(int(p) for p in parts))

    def __lt__(self, other: 'ParsedVersion') -> bool:
        return self.tup < other.tup

    def __str__(self) -> str:
        return self.raw


@dataclass
class ClassifiedFile:
    source_path: Path
    target_subdir: str
    family: str
    version: Optional[ParsedVersion]
    rule_index: int
    is_current: bool = True
    target_path: Optional[Path] = None
    duplicate_of: Optional[str] = None


# ─────────────────────────────────────────────────────────────────────────
# Classification (v2 — fixed @stem regex per defect A closure)
# ─────────────────────────────────────────────────────────────────────────

# v2 fix — defect A: require explicit v-prefix on stem-strip regex
_V2_STEM_STRIP = re.compile(r'[\s_-]*v[\d._]+.*$', re.IGNORECASE)

# v2 NEW — duplicate-suffix detection
_DUP_SUFFIX = re.compile(r'\s*(\(\d+\)|copy)\s*$', re.IGNORECASE)


def _detect_duplicate_marker(stem: str) -> Optional[str]:
    """Return the duplicate-marker substring if stem ends in (N) or 'copy'."""
    m = _DUP_SUFFIX.search(stem)
    return m.group(0) if m else None


def classify(source_path: Path) -> Optional[ClassifiedFile]:
    """Apply category rules to a file. Returns None if no rule matches."""
    name = source_path.name
    for idx, rule in enumerate(CATEGORY_RULES):
        m = re.match(rule['pattern'], name, flags=re.IGNORECASE)
        if not m:
            continue

        family_spec = rule['family']
        if family_spec == '@unique':
            family = f'__unique__::{name}'
        elif family_spec == '@stem':
            stem = _V2_STEM_STRIP.sub('', source_path.stem)
            family = f'@stem::{stem.lower()}'
        elif family_spec == '@dynamic':
            sess = m.groupdict().get('sess', 'unknown')
            family = f'pre_{sess}_fork_work_runbook'
        else:
            family = family_spec

        version = ParsedVersion.parse(m.groupdict().get('ver'))
        dup_marker = _detect_duplicate_marker(source_path.stem)

        return ClassifiedFile(
            source_path=source_path,
            target_subdir=rule['target'],
            family=family,
            version=version,
            rule_index=idx,
            duplicate_of=dup_marker,
        )
    return None


# ─────────────────────────────────────────────────────────────────────────
# Planning
# ─────────────────────────────────────────────────────────────────────────

def discover_files(source_root: Path) -> list[Path]:
    """Recursively find regular files under source_root, skipping hidden."""
    return [
        p for p in source_root.rglob('*')
        if p.is_file()
        and not any(part.startswith('.') for part in p.relative_to(source_root).parts)
    ]


def plan_operations(
    source_root: Path,
    target_root: Path,
) -> tuple[list[ClassifiedFile], list[Path]]:
    """Classify all files; mark current vs. superseded; compute target paths.

    Returns (classified, unmatched).
    """
    files = discover_files(source_root)
    classified: list[ClassifiedFile] = []
    unmatched: list[Path] = []

    for f in files:
        c = classify(f)
        if c is None:
            unmatched.append(f)
        else:
            classified.append(c)

    family_groups: dict[str, list[ClassifiedFile]] = defaultdict(list)
    for c in classified:
        family_groups[c.family].append(c)

    for family, members in family_groups.items():
        if family.startswith('__unique__::'):
            for m in members:
                m.is_current = True
            continue

        versioned = [m for m in members if m.version is not None]
        if versioned:
            latest = max(versioned, key=lambda x: x.version)
            for m in members:
                m.is_current = (m is latest)
        else:
            for m in members:
                m.is_current = True

    for c in classified:
        if c.is_current:
            target_dir = target_root / c.target_subdir
        else:
            target_dir = target_root / c.target_subdir / '_archive'
        c.target_path = target_dir / c.source_path.name

    return classified, unmatched


# ─────────────────────────────────────────────────────────────────────────
# Execution
# ─────────────────────────────────────────────────────────────────────────

def execute_plan(
    classified: list[ClassifiedFile],
    unmatched: list[Path],
    target_root: Path,
    *,
    move: bool,
    dry_run: bool,
    verbose: bool,
    trace: bool,
) -> dict:
    summary = {
        'total': len(classified) + len(unmatched),
        'classified': len(classified),
        'unmatched': len(unmatched),
        'current': sum(1 for c in classified if c.is_current),
        'superseded': sum(1 for c in classified if not c.is_current),
        'duplicates_flagged': sum(1 for c in classified if c.duplicate_of),
        'operations': 0,
        'errors': 0,
    }

    op_word = 'MOVE' if move else 'COPY'
    if dry_run:
        op_word = '[DRY-RUN] ' + op_word

    bar = '═' * 78
    print(f"\n{bar}")
    print(f"PLAN — {summary['total']} files (v2 ruleset)")
    print(f"  Classified : {summary['classified']} "
          f"({summary['current']} current / {summary['superseded']} superseded)")
    print(f"  Duplicates : {summary['duplicates_flagged']} "
          f"(filenames carrying (N) or 'copy' suffix)")
    print(f"  Unmatched  : {summary['unmatched']} "
          f"(→ _unsorted/__unmatched__/ — should be 0 with v2 fallthrough)")
    print(f"  Mode       : {op_word}")
    print(f"  Target     : {target_root}")
    print(f"{bar}\n")

    for c in classified:
        try:
            if not dry_run:
                c.target_path.parent.mkdir(parents=True, exist_ok=True)
                if move:
                    shutil.move(str(c.source_path), str(c.target_path))
                else:
                    shutil.copy2(str(c.source_path), str(c.target_path))
            summary['operations'] += 1
            if verbose or dry_run:
                marker = '★' if c.is_current else '○'
                if c.duplicate_of:
                    marker = '⚠'
                rel_target = c.target_path.relative_to(target_root)
                trace_suffix = f' [rule #{c.rule_index}]' if trace else ''
                print(f"  {marker} {op_word}: {c.source_path.name}{trace_suffix}")
                print(f"           → {rel_target}")
                if c.duplicate_of:
                    print(f"           ⚠ duplicate marker detected: "
                          f"{c.duplicate_of!r} — manual diff recommended")
        except Exception as e:
            summary['errors'] += 1
            print(f"  ✗ ERROR: {c.source_path.name}: {e}", file=sys.stderr)

    unmatched_root = target_root / '_unsorted' / '__unmatched__'
    for u in unmatched:
        try:
            target = unmatched_root / u.name
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                if move:
                    shutil.move(str(u), str(target))
                else:
                    shutil.copy2(str(u), str(target))
            summary['operations'] += 1
            if verbose or dry_run:
                print(f"  ? {op_word}: {u.name}")
                print(f"           → _unsorted/__unmatched__/")
        except Exception as e:
            summary['errors'] += 1
            print(f"  ✗ ERROR: {u.name}: {e}", file=sys.stderr)

    return summary


def write_manifest(
    target_root: Path,
    classified: list[ClassifiedFile],
    unmatched: list[Path],
) -> None:
    manifest_path = target_root / '_manifest.md'

    family_groups: dict[str, list[ClassifiedFile]] = defaultdict(list)
    for c in classified:
        family_groups[c.family].append(c)

    versioned_families = sorted(
        k for k in family_groups if not k.startswith('__unique__::')
    )
    unique_files = [
        c for c in classified if c.family.startswith('__unique__::')
    ]
    duplicates = [c for c in classified if c.duplicate_of]

    with open(manifest_path, 'w') as f:
        f.write(f"# Artifact Organization Manifest (v2)\n\n")
        f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
        f.write(f"**Script version:** v2 (defect-corrected ruleset)\n\n")
        f.write(f"**Total files processed:** "
                f"{len(classified) + len(unmatched)}\n\n")
        f.write(f"- Versioned families: {len(versioned_families)}\n")
        f.write(f"- Unique files: {len(unique_files)}\n")
        f.write(f"- Duplicate-marker flags: {len(duplicates)}\n")
        f.write(f"- Unmatched (manual review): {len(unmatched)}\n\n")
        f.write("---\n\n")

        if duplicates:
            f.write(f"## ⚠ Duplicate-Marker Flags ({len(duplicates)})\n\n")
            f.write("Files whose names carry `(N)`, `copy`, or similar "
                    "suffixes indicating possible browser/Finder duplication. "
                    "Manual diff recommended before deduplicating.\n\n")
            f.write(f"| Filename | Marker | Target |\n")
            f.write(f"|---|---|---|\n")
            for c in sorted(duplicates, key=lambda x: x.source_path.name):
                rel = c.target_path.relative_to(target_root) if c.target_path else '?'
                f.write(f"| `{c.source_path.name}` | `{c.duplicate_of}` | "
                        f"`{rel}` |\n")
            f.write('\n---\n\n')

        f.write(f"## Versioned Families ({len(versioned_families)})\n\n")
        for family in versioned_families:
            members = sorted(
                family_groups[family],
                key=lambda x: (x.version.tup if x.version else (0,)),
                reverse=True,
            )
            f.write(f"### {family}\n\n")
            f.write(f"| Filename | Version | Status | Rule # |\n")
            f.write(f"|---|---|---|---|\n")
            for m in members:
                ver = str(m.version) if m.version else '—'
                status = '**CURRENT**' if m.is_current else 'archive'
                f.write(f"| `{m.source_path.name}` | {ver} | {status} | "
                        f"{m.rule_index} |\n")
            f.write('\n')

        f.write(f"## Unique Files ({len(unique_files)})\n\n")
        by_target: dict[str, list[str]] = defaultdict(list)
        for c in unique_files:
            by_target[c.target_subdir].append(c.source_path.name)
        for tgt in sorted(by_target):
            f.write(f"### `{tgt}/` ({len(by_target[tgt])} files)\n\n")
            for name in sorted(by_target[tgt]):
                f.write(f"- `{name}`\n")
            f.write('\n')

        if unmatched:
            f.write(f"## Unmatched Files ({len(unmatched)})\n\n")
            f.write("These files matched no categorization rule and "
                    "were placed in `_unsorted/__unmatched__/` for "
                    "manual review.\n\n")
            for u in sorted(unmatched, key=lambda p: p.name):
                f.write(f"- `{u.name}`\n")


# ─────────────────────────────────────────────────────────────────────────
# Validation (v2 — improved diagnostics)
# ─────────────────────────────────────────────────────────────────────────

def validate_paths(source: Path, target: Path, execute: bool) -> None:
    """Validate source / target paths; emit discriminating diagnostics."""
    if not source.exists():
        print(f"ERROR: source path does not exist: {source}", file=sys.stderr)
        parent = source.parent
        if parent.exists():
            siblings = sorted(p.name for p in parent.iterdir())
            matches = [s for s in siblings
                       if source.name.lower() in s.lower()
                       or s.lower() in source.name.lower()]
            if matches:
                print(f"  Similar entries in {parent}:", file=sys.stderr)
                for m in matches:
                    print(f"    - {m!r}", file=sys.stderr)
            else:
                print(f"  No similar entries in {parent}.", file=sys.stderr)
                print(f"  First 10 entries: {siblings[:10]}", file=sys.stderr)
        else:
            print(f"  Parent directory also missing: {parent}", file=sys.stderr)
        sys.exit(1)

    if source.is_file():
        print(f"ERROR: source path is a file, not a directory: {source}",
              file=sys.stderr)
        print(f"  Size: {source.stat().st_size} bytes", file=sys.stderr)
        print(f"  If this is an archive, extract it first.", file=sys.stderr)
        sys.exit(1)

    if source.is_symlink() and not source.resolve().exists():
        print(f"ERROR: source is a broken symlink: {source}", file=sys.stderr)
        print(f"  Points to: {source.readlink()}", file=sys.stderr)
        sys.exit(1)

    if not source.is_dir():
        print(f"ERROR: source exists but is not a usable directory: {source}",
              file=sys.stderr)
        print(f"  stat mode: {oct(source.stat().st_mode)}", file=sys.stderr)
        print(f"  Possible causes: permission denied, special file type, "
              f"iCloud dataless placeholder.", file=sys.stderr)
        sys.exit(1)

    if source == target:
        print(f"ERROR: source and target resolve to the same path: {source}",
              file=sys.stderr)
        sys.exit(2)

    if target.exists() and any(target.iterdir()) and execute:
        print(f"WARNING: target {target} exists and is non-empty.",
              file=sys.stderr)
        print(f"         Operations will merge into existing tree.",
              file=sys.stderr)
        print(f"         Press Ctrl-C within 5 seconds to abort...",
              file=sys.stderr)
        time.sleep(5)


# ─────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Organize LLM-as-Database project artifacts (v2).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        'source', type=Path,
        help='Source directory (e.g. ~/Downloads/llm-as-databse)',
    )
    parser.add_argument(
        '--target', type=Path,
        default=Path.home() / 'llm-as-database',
        help='Target directory (default: ~/llm-as-database)',
    )
    parser.add_argument(
        '--execute', action='store_true',
        help='Actually perform operations (default: dry-run)',
    )
    parser.add_argument(
        '--move', action='store_true',
        help='Move instead of copy (default: copy preserves source)',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Print every operation in execute mode '
             '(dry-run mode is always verbose)',
    )
    parser.add_argument(
        '--trace', action='store_true',
        help='Emit rule-index per file for ruleset debugging',
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    target = args.target.expanduser().resolve()

    validate_paths(source, target, args.execute)

    classified, unmatched = plan_operations(source, target)

    summary = execute_plan(
        classified, unmatched, target,
        move=args.move,
        dry_run=not args.execute,
        verbose=args.verbose,
        trace=args.trace,
    )

    if args.execute:
        target.mkdir(parents=True, exist_ok=True)
        write_manifest(target, classified, unmatched)
        print(f"\nManifest written: {target / '_manifest.md'}")

    bar = '═' * 78
    print(f"\n{bar}")
    print(f"SUMMARY")
    print(f"  Total processed     : {summary['total']}")
    print(f"  Operations          : {summary['operations']}")
    print(f"  Duplicates flagged  : {summary['duplicates_flagged']}")
    print(f"  Errors              : {summary['errors']}")
    if not args.execute:
        print(f"\n  This was a DRY-RUN. Re-run with --execute to apply.")
    print(f"{bar}\n")

    sys.exit(3 if summary['errors'] else 0)


if __name__ == '__main__':
    main()
