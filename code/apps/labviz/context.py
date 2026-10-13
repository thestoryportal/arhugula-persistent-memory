"""Documented program connections and source-bound run context.

This reader performs no scientific computation. A connection records a document
relationship; its type distinguishes a quoted relationship from a curated one
and from a chain of those relationships.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REGISTRY = "program/registers/EXPERIMENT_REGISTRY.md"
OVERLAY = "knowledge/specs/SPEC_EXPERIMENT_OVERLAY.md"
CONDITIONS = "knowledge/findings/F1_DETERMINATION.md"
E2E = "knowledge/specs/SPEC_E2E_GROUND_TRUTH.md"
HYPOTHESES = "program/registers/HYPOTHESIS_REGISTER_2026-06-18.md"
RUNBOOK = "program/runbook"
TABLE = "code/apps/labviz/contexts.json"
MOVES = "code/apps/labviz/results_moves.json"
_DECISION = re.compile(r"(?<![A-Za-z0-9-])(D-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)(?![A-Za-z0-9-])")
_ANCHOR = re.compile(r"⟨(D-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)@[^⟩]+⟩")
# Sealed documents cite pre-v2 results/ paths; current ones cite run folders.
_RESULT_PATH = re.compile(r"(?<![A-Za-z0-9_])(?:/workspace/)?((?:results|experiments/[A-Za-z0-9_-]+/runs)/[A-Za-z0-9_./*{},+\-]+)")
_SPEC = re.compile(r"§\d+(?:\.\d+)*")


def _distinct(values):
    return list(dict.fromkeys(values))


def expand_braces(path):
    """Expand unnested brace alternatives, including the empty alternative."""
    if not isinstance(path, str):
        raise ValueError("result path must be a string")
    groups = list(re.finditer(r"\{([^{}]*)\}", path))
    stripped = re.sub(r"\{[^{}]*\}", "", path)
    if "{" in stripped or "}" in stripped:
        raise ValueError("nested or unmatched result-path braces")
    expanded = [""]
    end = 0
    for group in groups:
        prefix = path[end:group.start()]
        expanded = [value + prefix + alternative
                    for value in expanded for alternative in group[1].split(",")]
        end = group.end()
    return [value + path[end:] for value in expanded]


def decision_ids(text):
    """The D-ID grammar excludes literal D-ID and embedded status fragments."""
    return _distinct(value for value in _DECISION.findall(text)
                     if value not in ("D-ID", "D-IDs"))


def _chosen_decision(text, anchored_only=False):
    anchors = _distinct(value for value in _ANCHOR.findall(text) if value not in ("D-ID", "D-IDs"))
    candidates = anchors if anchors or anchored_only else decision_ids(text)
    return (candidates[0] if len(candidates) == 1 else None), candidates


def _corpus_refs(text):
    refs = []
    for match in re.finditer(r"evidence/CORPUS/(\d{2})(?:[–-](\d{2}))?", text):
        first, last = int(match[1]), int(match[2] or match[1])
        if last < first:
            raise ValueError("reversed CORPUS range")
        refs.extend((f"{number:02d}", match[0]) for number in range(first, last + 1))
    return list(dict.fromkeys(refs))


def _cells(line):
    return [part.strip() for part in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def _path_matches(pattern, source, allow_suffix=False):
    if pattern.endswith("/"):
        return source.startswith(pattern)
    expression = re.escape(pattern).replace(r"\*", "[^/]*")
    if re.fullmatch(expression, source):
        return True
    return bool(allow_suffix and len(pattern.split("/")) >= 2
                and re.search(r"(?:^|/)" + expression + r"$", source))


def _moved(pattern, moves):
    """A results/ pattern's v2 homes: under a moved folder, the same path under its new home; a moved path the
    pattern names whole, its new path (and, for a folder pattern, everything under it)."""
    homes = []
    for old, new in moves.items():
        if pattern.startswith(old + "/"):
            homes.append(new + pattern[len(old):])
        elif _path_matches(pattern, old):
            homes.extend((new, new + "/") if pattern.endswith("/") else (new,))
    return _distinct(homes)


def _json_path(parts):
    path = ""
    for part in parts:
        if isinstance(part, int):
            path += ("." if not path else "") + f"[{part}]"
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part):
            path += "." + part
        else:
            path += ("." if not path else "") + "[" + json.dumps(part, ensure_ascii=False) + "]"
    return path or "."


def _json_parts(path):
    if path == ".":
        return []
    if not path.startswith("."):
        raise ValueError("JSON source path must start at the root: " + path)
    offset, parts = (1 if path.startswith(".[") else 0), []
    token = re.compile(r'\.([A-Za-z_][A-Za-z0-9_]*)|\[("(?:[^"\\]|\\.)*"|\d+)\]')
    while offset < len(path):
        match = token.match(path, offset)
        if not match:
            raise ValueError("unsupported JSON source path: " + path)
        key = match[1] if match[1] else json.loads(match[2])
        parts.append(key)
        offset = match.end()
    return parts


def _resolve_json(data, path):
    """Resolve the emitted jq subset without launching a command."""
    for key in _json_parts(path):
        data = data[key]
    return data


def _missing(reason):
    return {"value": None, "missing": reason, "tier": 1}


class Program:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self._lines = {}
        self._json = {}
        self._real_program = (self.root / REGISTRY).is_file()
        local_table = self.root / TABLE
        self._table_file = local_table if local_table.is_file() else PACKAGE / "contexts.json"
        self.tables = json.loads(self._table_file.read_text(encoding="utf-8"))
        local_moves = self.root / MOVES
        self.moves = json.loads((local_moves if local_moves.is_file() else PACKAGE / "results_moves.json").read_text(encoding="utf-8"))["moves"]
        self._homes = {}
        self.registry = self._read_registry()
        self.headers = self._read_headers()
        self.hypotheses = self._read_hypotheses()
        self.sections = self._read_overlay()
        self.conditions = self._read_conditions()
        self.layers = self._read_layers()
        self.ledger = self._read_ledger()
        self.graph = self._build_graph()

    def _document(self, file):
        if file not in self._lines:
            path = self.root / file
            if self._real_program and file in (REGISTRY, OVERLAY, CONDITIONS, E2E, HYPOTHESES) and not path.is_file():
                raise FileNotFoundError("required context source is absent: " + file)
            self._lines[file] = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
        return self._lines[file]

    def _runbook(self):
        """The runbook's lines as (part file, line, text): it is split into parts, and a citation names the part
        that holds the line."""
        folder = self.root / RUNBOOK
        parts = sorted(folder.glob("*.md")) if folder.is_dir() else []
        if self._real_program and not parts:
            raise FileNotFoundError("required context source is absent: " + RUNBOOK)
        files = [str(part.relative_to(self.root)) for part in parts]
        return [(file, number, line) for file in files for number, line in enumerate(self._document(file), 1)]

    def _cites(self, pattern, source, allow_suffix=False):
        """A cited path names this source as written or, for a pre-v2 results/ path, at its v2 home."""
        if pattern not in self._homes:
            self._homes[pattern] = [pattern] + (_moved(pattern, self.moves) if pattern.startswith("results/") else [])
        return any(_path_matches(home, source, allow_suffix) for home in self._homes[pattern])

    def _doc(self, file, line, value, node_id=None, edge="direct", quote=None):
        source = self._document(file)
        if line < 1 or line > len(source):
            raise ValueError(f"unresolved document source {file}:{line}")
        quote = value if quote is None else quote
        if not isinstance(quote, str) or not quote or quote not in source[line - 1]:
            raise ValueError(f"unresolved quote {file}:{line}")
        if isinstance(value, str) and value not in quote:
            raise ValueError(f"document value not present in quote {file}:{line}")
        leaf = {"value": value, "src": {"file": file, "line": line, "quote": quote}}
        if node_id:
            leaf.update(node_id=node_id, edge=edge)
        return leaf

    def _table(self, *parts, node_id=None):
        value = self.tables
        for part in parts:
            value = value[part]
        leaf = {"value": copy.deepcopy(value), "src": {"file": TABLE, "path": _json_path(parts)}}
        if node_id:
            leaf.update(node_id=node_id, edge="curated")
        return leaf

    def _read_registry(self):
        rows = []
        for number, line in enumerate(self._document(REGISTRY), 1):
            if not re.match(r"\|\s*\*\*", line):
                continue
            # Only the first six cells have fixed positions. Status prose has
            # real, unescaped pipes (R2's max|ΔP|) and cannot be split blindly.
            cells = line.split("|")
            identity = re.search(r"\*\*(.+?)\*\*", cells[1])
            if not identity or len(cells) < 8:
                continue
            tail = "|".join(cells[7:]).strip().rstrip("|").strip()
            status_parts = tail.rsplit("|", 1)
            if len(status_parts) == 2 and re.fullmatch(
                    r"\s*D-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*(?:\s+⟨[^⟩]+⟩)?\s*", status_parts[1]):
                status = status_parts[0].strip()
            else:
                status = tail
            chosen, candidates = _chosen_decision(line)
            paths = []
            for quoted in re.findall(r"`([^`]+)`", cells[5]):
                if quoted.startswith("results/") or re.match(r"experiments/[^/]+/runs/", quoted):
                    paths.extend(expand_braces(quoted))
            question = cells[3].strip()
            rows.append({"id": identity[1], "track": cells[2].strip(),
                         "question": question, "status": status,
                         "decision": chosen, "decision_candidates": candidates,
                         "results": _distinct(paths),
                         "corpus": _distinct(nn for nn, _ in _corpus_refs(cells[6])),
                         "hypothesis": _distinct(re.findall(r"\bH-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*", question)),
                         "line": number})
        return rows

    def _read_headers(self):
        folder = self.root / "evidence/CORPUS"
        headers = []
        for path in sorted(folder.glob("[0-9][0-9]_*.md")) if folder.is_dir() else []:
            file = path.relative_to(self.root).as_posix()
            source = self._document(file)
            if not source:
                continue
            paths = []
            for number, line in enumerate(source[:12], 1):
                for match in _RESULT_PATH.finditer(line):
                    named_pattern = match[1].rstrip(",")
                    for pattern in expand_braces(named_pattern):
                        paths.append({"pattern": pattern, "named_pattern": named_pattern, "line": number})
            anchors = _distinct(value for line in source[:12] for value in _ANCHOR.findall(line)
                                if value not in ("D-ID", "D-IDs"))
            headers.append({"id": path.name[:2], "file": file, "title": source[0].lstrip("# "),
                            "paths": paths, "decision": anchors[0] if len(anchors) == 1 else None,
                            "decision_candidates": anchors})
        return headers

    def _read_hypotheses(self):
        entries = []
        section = None
        for number, line in enumerate(self._document(HYPOTHESES), 1):
            heading = re.match(r"^#{2,3}\s+([A-Z])(?:\.(\d+))?\b", line)
            if heading:
                section = heading[1] + (heading[2] or "")
            row = re.match(r"\|\s*(?:\*\*)?([A-G]\d+[a-z]?|H-[A-Za-z0-9-]+)(?:\*\*)?\s*\|", line)
            if section and row:
                parts = _cells(line)
                entries.append({"id": row[1], "section": section,
                                "node_id": f"hyp:{section}:{row[1]}", "line": number,
                                "label": parts[1] if len(parts) > 1 else row[1]})
        return entries

    def _read_overlay(self):
        entries = []
        for number, line in enumerate(self._document(OVERLAY), 1):
            if not line.startswith("|"):
                continue
            cell = _cells(line)[0]
            for section in _distinct(_SPEC.findall(cell)):
                entries.append({"id": section, "line": number, "cell": cell,
                                "decisions": decision_ids(line), "corpus": _corpus_refs(line),
                                "conditions": _distinct(re.findall(r"F1 condition\s+(C\d+)\b", line))})
        return entries

    def _read_conditions(self):
        entries = []
        for number, line in enumerate(self._document(CONDITIONS), 1):
            match = re.match(r"\|\s*\*\*(C\d+)\*\*\s*\|", line)
            if match:
                parts = _cells(line)
                entries.append({"id": match[1], "line": number, "label": parts[1],
                                "status": parts[3],
                                "sections": _distinct(_SPEC.findall(parts[1]))})
        return entries

    def _read_layers(self):
        entries = []
        for number, line in enumerate(self._document(E2E), 1):
            if not line.startswith("|"):
                continue
            cell = _cells(line)[0]
            match = re.search(r"([A-Za-z][A-Za-z ]+?)\s*\(§(\d+)\)", cell.replace("**", ""))
            if match:
                entries.append({"id": match[1].strip(), "section": "§" + match[2],
                                "line": number, "cell": cell})
        return entries

    def _read_ledger(self):
        entries, active = [], False
        for file, number, line in self._runbook():
            if re.match(r"^##\s+§5\b", line):
                active = True
                continue
            if active and re.match(r"^##\s+§6\b", line):
                break
            if not active or not line.startswith("|"):
                continue
            refs = decision_ids(line)
            if not refs:
                continue
            cells = _cells(line)
            heading, status = cells[0], cells[1]
            date = re.search(r"\b(20\d\d-\d\d-\d\d[^;)]*)", heading)
            # Authority references after the date are not the decision owned by
            # this row. Neither a referenced date nor row order supplies a date.
            owner_text = heading[:date.start()] if date else heading
            owner_ids = decision_ids(owner_text)
            if owner_ids:
                owner, _ = _chosen_decision(owner_text)
            else:
                owner, _ = _chosen_decision(status)
            entries.append({"id": owner, "file": file, "line": number, "heading": heading, "status": status,
                            "date": date[1].strip() if date and owner else None,
                            "decisions": refs, "corpus": _corpus_refs(line)})
        return entries

    def _registry_leaf(self, row, field, node_id=None):
        return self._doc(REGISTRY, row["line"], row[field], node_id)

    def _candidate(self, row):
        return self._registry_leaf(row, "id", "exp:" + row["id"])

    def _header_candidate(self, header):
        return self._doc(header["file"], 1, header["title"], "corpus:" + header["id"])

    def _unknown(self, candidates=(), tied=False):
        fields = ("experiment", "track", "decision", "corpus", "hypothesis", "question",
                  "condition", "section", "layer", "status_now", "era", "measure", "judge_bar")
        result = {field: _missing("context not recorded") for field in fields}
        result.update(spec_sections=[], corpus_entries=[], candidates=list(candidates), matched_by="unknown",
                      match_note=self._table("messages", "tie" if tied else "unknown"),
                      framing_status=_missing("era framing not recorded"))
        return result

    def _framing(self, context, group, identity):
        entry = self.tables.get(group, {}).get(identity)
        if not entry:
            return
        era = entry["era"]
        context["era"] = self._table(group, identity, "era", node_id="era:" + era)
        context["measure"] = self._table(group, identity, "measure")
        context["judge_bar"] = self._table(group, identity, "bar")
        context["framing_status"] = self._table(group, identity, "status")
        context["framing_note"] = self._table("messages", "draft")

    def _connections(self, context):
        decision = context["decision"]
        if decision["value"] is None:
            return
        overlays = [row for row in self.sections if decision["value"] in row["decisions"]]
        by_section = {}
        for row in overlays:
            by_section.setdefault(row["id"], row)
        sections = []
        for section, row in by_section.items():
            repeated_decision = self._doc(OVERLAY, row["line"], decision["value"], decision["node_id"])
            section_leaf = self._doc(OVERLAY, row["line"], section, "spec:" + section, quote=row["cell"])
            sections.append({"value": section, "node_id": "spec:" + section, "edge": "derived",
                             "derived": "context-section", "inputs": [copy.deepcopy(decision), repeated_decision, section_leaf],
                             "rule_src": {"spec": "§11.2"},
                             "unit": "spec section"})
        context["spec_sections"] = sections
        if len(sections) != 1:
            if sections:
                context["candidates"].extend(copy.deepcopy(sections))
            return
        section = sections[0]
        context["section"] = copy.deepcopy(section)
        row = by_section[section["value"]]
        conditions = [item for item in self.conditions if section["value"] in item["sections"]]
        if row["conditions"]:
            conditions = [item for item in conditions if item["id"] in row["conditions"]]
        inputs = copy.deepcopy(section["inputs"])
        if len(conditions) == 1:
            condition = conditions[0]
            f1_section = self._doc(CONDITIONS, condition["line"], section["value"], section["node_id"], quote=condition["label"])
            condition_leaf = self._doc(CONDITIONS, condition["line"], condition["id"], "cond:" + condition["id"],
                                       quote="**" + condition["id"] + "**")
            context["condition"] = {"value": condition["id"], "node_id": condition_leaf["node_id"], "edge": "derived",
                                    "derived": "context-condition", "inputs": inputs + [f1_section, condition_leaf],
                                    "rule_src": {"spec": "§11.2"}, "unit": "F1 condition"}
        elif conditions:
            context["candidates"].extend(self._doc(CONDITIONS, item["line"], item["id"], "cond:" + item["id"])
                                         for item in conditions)
        major = section["value"].split(".", 1)[0]
        layers = [item for item in self.layers if item["section"] == major]
        if len(layers) == 1:
            layer = layers[0]
            layer_leaf = self._doc(E2E, layer["line"], layer["id"], "layer:" + layer["id"], quote=layer["cell"])
            context["layer"] = {"value": layer["id"], "node_id": layer_leaf["node_id"], "edge": "derived",
                                "derived": "context-layer", "inputs": inputs + [copy.deepcopy(inputs[2]), layer_leaf],
                                "rule_src": {"spec": "§11.2"}, "unit": "architecture layer"}

    def context(self, source, data):
        """Apply the four ordered rules; ties and documentary matches terminate."""
        source = str(source).replace("\\", "/")
        if source.startswith("/") or ".." in Path(source).parts:
            raise ValueError("run context requires a repository-relative source")
        matches = []
        for row in self.registry:
            lengths = [len(path) for path in row["results"] if self._cites(path, source)]
            if lengths:
                matches.append((max(lengths), row))
        if matches:
            longest = max(length for length, _ in matches)
            winners = [row for length, row in matches if length == longest]
            if len(winners) != 1:
                return self._unknown([self._candidate(row) for row in winners], tied=True)
            return self._experiment_context(winners[0], "registry_path")
        documentary = []
        for header in self.headers:
            matches = [path for path in header["paths"] if self._cites(path["pattern"], source, allow_suffix=True)]
            if matches:
                documentary.append((header, matches[0]))
        if documentary:
            if len(documentary) != 1:
                return self._unknown([self._header_candidate(header) for header, _ in documentary], tied=True)
            header, matched = documentary[0]
            context = self._unknown()
            context["experiment"] = _missing("no registry row names this record")
            context["corpus"] = self._doc(header["file"], matched["line"], matched["named_pattern"], "corpus:" + header["id"])
            context["corpus_entries"] = [copy.deepcopy(context["corpus"])]
            context.update(matched_by="corpus_header", match_note=self._table("messages", "corpus_header"))
            if header["decision"]:
                number = next(number for number, line in enumerate(self._document(header["file"])[:12], 1)
                              if header["decision"] in _ANCHOR.findall(line))
                context["decision"] = self._doc(header["file"], number, header["decision"], "dec:" + header["decision"])
            else:
                for value in header["decision_candidates"]:
                    number = next(number for number, line in enumerate(self._document(header["file"])[:12], 1) if value in line)
                    context["candidates"].append(self._doc(header["file"], number, value, "dec:" + value))
            self._framing(context, "corpus_eras", header["id"])
            entry = self.tables.get("corpus_eras", {}).get(header["id"], {})
            if "question" in entry:
                context["question"] = self._table("corpus_eras", header["id"], "question")
            self._connections(context)
            return context
        decision = data.get("decision_id") if isinstance(data, dict) else None
        winners = [row for row in self.registry if decision is not None and row["decision"] == decision]
        if len(winners) == 1:
            key = "decision_attempt" if winners[0]["results"] else "registry_decision"
            return self._experiment_context(winners[0], key)
        if len(winners) > 1:
            return self._unknown([self._candidate(row) for row in winners], tied=True)
        candidates = []
        for entry in self.tables.get("candidate_patterns", []):
            if self._cites(entry["pattern"], source):
                candidates.extend(self._header_candidate(header) for header in self.headers if header["id"] == entry["corpus"])
        basename = Path(source).name
        for header in self.headers:
            if any(not path["pattern"].endswith("/") and _path_matches(Path(path["pattern"]).name, basename)
                   for path in header["paths"]):
                candidate = self._header_candidate(header)
                if candidate not in candidates:
                    candidates.append(candidate)
        return self._unknown(candidates)

    def _experiment_context(self, row, matched_by):
        context = self._unknown()
        context.update(matched_by=matched_by, match_note=self._table("messages", matched_by))
        context["experiment"] = self._registry_leaf(row, "id", "exp:" + row["id"])
        context["track"] = self._registry_leaf(row, "track", "track:" + row["track"])
        context["question"] = self._registry_leaf(row, "question")
        context["status_now"] = self._registry_leaf(row, "status")
        if row["decision"]:
            context["decision"] = self._registry_leaf(row, "decision", "dec:" + row["decision"])
        else:
            context["decision"] = _missing("no decision recorded" if not row["decision_candidates"] else "more than one decision recorded")
            context["candidates"].extend(self._doc(REGISTRY, row["line"], value, "dec:" + value)
                                         for value in row["decision_candidates"])
        for number in row["corpus"]:
            context["corpus_entries"].append(self._doc(REGISTRY, row["line"], "evidence/CORPUS/" + number, "corpus:" + number))
        if len(context["corpus_entries"]) == 1:
            context["corpus"] = copy.deepcopy(context["corpus_entries"][0])
        elif context["corpus_entries"]:
            context["corpus"] = _missing("more than one CORPUS entry recorded")
            context["candidates"].extend(copy.deepcopy(context["corpus_entries"]))
        hypotheses = [entry for entry in self.hypotheses if entry["id"] in row["hypothesis"]]
        if len(hypotheses) == 1:
            entry = hypotheses[0]
            context["hypothesis"] = self._doc(HYPOTHESES, entry["line"], entry["id"], entry["node_id"])
        elif hypotheses:
            context["candidates"].extend(self._doc(HYPOTHESES, entry["line"], entry["id"], entry["node_id"]) for entry in hypotheses)
        curated = self.tables.get("experiment_hypotheses", {}).get(row["id"])
        if curated:
            context["hypothesis"] = self._table("experiment_hypotheses", row["id"], "hypothesis", node_id=curated["hypothesis"])
        self._framing(context, "experiments", row["id"])
        self._connections(context)
        return context

    def registry_context(self, experiment_id):
        """An explicitly selected registry line, independent of run matching."""
        rows = [row for row in self.registry if row["id"] == experiment_id]
        if len(rows) != 1:
            return self._unknown([self._candidate(row) for row in rows], tied=bool(rows))
        return self._experiment_context(rows[0], "registry_line")

    def _build_graph(self):
        if not self._real_program:
            return {"nodes": [], "edges": []}
        nodes, edges, seen = {}, [], set()

        def node(node_id, label=None, **extra):
            nodes.setdefault(node_id, {"node_id": node_id, "label": label or node_id.split(":", 1)[1],
                                       "kind": node_id.split(":", 1)[0], **extra})

        def direct(source, target, file, line, source_words, target_words):
            key = (source, target, "direct", file, line)
            if key not in seen:
                seen.add(key)
                edges.append({"source": source, "target": target, "edge": "direct", "src": {"file": file, "line": line},
                              "quotes": {"source": source_words, "target": target_words}})
            return next(edge for edge in edges if (edge["source"], edge["target"], edge["edge"], edge.get("src", {}).get("file"), edge.get("src", {}).get("line")) == key)

        def curated(source, target, citation, table_parts):
            key = (source, target, "curated", json.dumps(citation, sort_keys=True))
            if key not in seen:
                seen.add(key)
                edges.append({"source": source, "target": target, "edge": "curated", "src": copy.deepcopy(citation),
                              "curation": {"file": TABLE, "path": _json_path(table_parts)}})

        for slug, framing in self.tables.get("eras", {}).items():
            node("era:" + slug, framing["label"], status=framing["status"], description=framing["question"])
        for header in self.headers:
            corpus = "corpus:" + header["id"]
            node(corpus, header["title"], src={"file": header["file"], "line": 1, "quote": header["title"]})
            entry = self.tables.get("corpus_eras", {}).get(header["id"], {})
            if "line_question" in entry:
                citation = entry["citations"]["line_question"]
                question = self._doc(citation["file"], citation["line"], entry["line_question"], quote=citation["quote"])
                nodes[corpus].update(question=question, description=copy.deepcopy(question),
                                     measure=self._table("corpus_eras", header["id"], "line_measure"),
                                     framing_status=self._table("corpus_eras", header["id"], "status"),
                                     era=entry["era"], citations=copy.deepcopy(entry["citations"]))
            if "short_label" in entry:
                citation = entry["citations"]["short_label"]
                nodes[corpus]["short_label"] = self._doc(citation["file"], citation["line"], entry["short_label"], quote=citation["quote"])
        for entry in self.hypotheses:
            node(entry["node_id"], entry["id"] + " · " + entry["label"], src={"file": HYPOTHESES, "line": entry["line"], "quote": entry["id"]})
        experiment_edges = {}
        for row in self.registry:
            exp, track = "exp:" + row["id"], "track:" + row["track"]
            node(exp, row["id"], description=row["question"], status=row["status"], src={"file": REGISTRY, "line": row["line"], "quote": row["id"]})
            node(track, row["track"])
            direct(track, exp, REGISTRY, row["line"], row["track"], row["id"])
            if row["decision"]:
                dec = "dec:" + row["decision"]
                node(dec)
                experiment_edges[row["id"]] = direct(exp, dec, REGISTRY, row["line"], row["id"], row["decision"])
            for number in row["corpus"]:
                target = "corpus:" + number
                node(target, "evidence/CORPUS/" + number)
                direct(exp, target, REGISTRY, row["line"], row["id"], "evidence/CORPUS/" + number)
                if row["decision"]:
                    direct("dec:" + row["decision"], target, REGISTRY, row["line"], row["decision"], "evidence/CORPUS/" + number)
            if row["id"] in self.tables.get("experiments", {}):
                entry = self.tables["experiments"][row["id"]]
                nodes[exp]["era"] = entry["era"]
                curated("era:" + entry["era"], exp, entry["citations"]["era"], ["experiments", row["id"]])
            hypotheses = [entry for entry in self.hypotheses if entry["id"] in row["hypothesis"]]
            for entry in hypotheses:
                if len([other for other in self.hypotheses if other["id"] == entry["id"]]) == 1:
                    direct(exp, entry["node_id"], REGISTRY, row["line"], row["id"], entry["id"])
        overlay_edges = {}
        for row in self.sections:
            spec = "spec:" + row["id"]
            node(spec, row["id"], src={"file": OVERLAY, "line": row["line"], "quote": row["cell"]})
            for decision in row["decisions"]:
                dec = "dec:" + decision
                node(dec)
                edge = direct(spec, dec, OVERLAY, row["line"], row["id"], decision)
                overlay_edges.setdefault((row["id"], decision), edge)
            for number, words in row["corpus"]:
                node("corpus:" + number, "evidence/CORPUS/" + number)
                direct(spec, "corpus:" + number, OVERLAY, row["line"], row["id"], words)
        for condition in self.conditions:
            cond = "cond:" + condition["id"]
            node(cond, condition["id"], description=condition["label"], src={"file": CONDITIONS, "line": condition["line"], "quote": condition["id"]})
            if condition["id"] == "C10":
                status = self._doc(CONDITIONS, condition["line"], condition["status"])
                nodes[cond].update(status=status, citations={"status": copy.deepcopy(status["src"])},
                                   framing_status=self._table("eras", "c10", "status"))
            for section in condition["sections"]:
                spec = "spec:" + section
                node(spec)
                f1_edge = direct(cond, spec, CONDITIONS, condition["line"], condition["id"], section)
                for row in self.registry:
                    overlay_edge = overlay_edges.get((section, row["decision"]))
                    experiment_edge = experiment_edges.get(row["id"])
                    if overlay_edge and experiment_edge:
                        edges.append({"source": cond, "target": "exp:" + row["id"], "edge": "derived",
                                      "inputs": [copy.deepcopy(f1_edge), copy.deepcopy(overlay_edge), copy.deepcopy(experiment_edge)]})
        for layer in self.layers:
            layer_id = "layer:" + layer["id"]
            node(layer_id, layer["id"], src={"file": E2E, "line": layer["line"], "quote": layer["cell"]})
            node("spec:" + layer["section"])
            direct(layer_id, "spec:" + layer["section"], E2E, layer["line"], layer["id"], layer["section"])
        for section, entry in self.tables.get("section_layers", {}).items():
            if "layer:" + entry["layer"] in nodes and "spec:" + section in nodes:
                curated("layer:" + entry["layer"], "spec:" + section, entry["citations"]["layer"], ["section_layers", section])
        for file, number, line in self._runbook():
            match = re.match(r"^###\s+(TRACK ([A-F])\b.*)", line)
            if match:
                node("runbook-track:" + match[2], match[1], src={"file": file, "line": number, "quote": match[1]})
        for arm, entry in self.tables.get("arms", {}).items():
            node("arm:" + arm, entry["label"], src=entry["citation"], status=entry["status"])
        for exp, entry in self.tables.get("experiment_hypotheses", {}).items():
            if "exp:" + exp in nodes and entry["hypothesis"] in nodes:
                curated("exp:" + exp, entry["hypothesis"], entry["citation"], ["experiment_hypotheses", exp])
        models_file = self.root / "code/apps/labviz/models.json"
        models = json.loads(models_file.read_text(encoding="utf-8")) if models_file.is_file() else {}
        for model, info in models.items():
            node("model:" + model, model, status=info.get("status"), src={"file": "code/apps/labviz/models.json", "path": _json_path([model, "status"])})
        for model, entry in self.tables.get("model_eras", {}).items():
            if not self._real_program:
                continue
            node("model:" + model, model)
            curated("era:" + entry["era"], "model:" + model, entry["citation"], ["model_eras", model])
        for index, entry in enumerate(self.tables.get("model_corpus", [])):
            corpus, model, citation = "corpus:" + entry["corpus"], "model:" + entry["model"], entry["citation"]
            if corpus not in nodes or model not in nodes:
                continue
            refs = [(number, words) for number, words in _corpus_refs(citation["quote"]) if number == entry["corpus"]]
            if refs:
                direct(corpus, model, citation["file"], citation["line"], refs[0][1], entry["model"])
            else:
                curated(corpus, model, citation, ["model_corpus", index])
        timeline = []
        dates = {}
        for entry in self.ledger:
            for decision in entry["decisions"]:
                node("dec:" + decision, src={"file": entry["file"], "line": entry["line"], "quote": decision})
            if not entry["id"]:
                continue
            owner = "dec:" + entry["id"]
            source = {"file": entry["file"], "line": entry["line"], "quote": entry["heading"]}
            date = self._doc(entry["file"], entry["line"], entry["date"]) if entry["date"] else _missing("no date recorded in the decision's ledger heading")
            timeline.append({"node_id": owner, "decision": self._doc(entry["file"], entry["line"], entry["id"], owner),
                             "date": date, "description": self._doc(entry["file"], entry["line"], entry["heading"]),
                             "status": self._doc(entry["file"], entry["line"], entry["status"])})
            nodes[owner]["ledger_src"] = source
            nodes[owner]["description"] = entry["heading"]
            dates.setdefault(owner, []).append(date)
            for decision in entry["decisions"]:
                if decision != entry["id"]:
                    direct(owner, "dec:" + decision, entry["file"], entry["line"], entry["id"], decision)
            for number, words in entry["corpus"]:
                node("corpus:" + number, "evidence/CORPUS/" + number)
                direct(owner, "corpus:" + number, entry["file"], entry["line"], entry["id"], words)
        for owner, recorded_dates in dates.items():
            nodes[owner]["dates"] = recorded_dates
            nodes[owner]["date"] = recorded_dates[0] if len(recorded_dates) == 1 else _missing("more than one ledger event is recorded; see dates")
        return {"nodes": list(nodes.values()), "edges": edges, "timeline": timeline}

    def focus(self, node_id):
        """Show the paths into and out of a selected node, preserving direction."""
        if node_id not in {node["node_id"] for node in self.graph["nodes"]}:
            return set()
        reached = {node_id}
        for start, end in (("source", "target"), ("target", "source")):
            pending, visited = [node_id], {node_id}
            while pending:
                here = pending.pop()
                for edge in self.graph["edges"]:
                    if edge[start] == here and edge[end] not in visited:
                        visited.add(edge[end])
                        pending.append(edge[end])
            reached.update(visited)
        return reached

    def _citation(self, citation):
        file = citation["file"]
        if "path" in citation:
            if file not in self._json:
                path = self._table_file if file == TABLE else self.root / file
                self._json[file] = json.loads(path.read_text(encoding="utf-8"))
            value = _resolve_json(self._json[file], citation["path"])
            if "value" in citation and value != citation["value"]:
                raise ValueError("JSON citation value mismatch: " + file + ":" + citation["path"])
            return value
        source = self._document(file)
        line, quote = citation["line"], citation["quote"]
        if not isinstance(line, int) or line < 1 or line > len(source) or not quote or quote not in source[line - 1]:
            raise ValueError(f"document citation mismatch: {file}:{line}")
        return quote

    def _end_words(self, node_id, words, file, line):
        kind, value = node_id.split(":", 1)
        if kind == "corpus":
            return value in [number for number, _ in _corpus_refs(words)]
        if kind == "exp":
            return any(row["id"] == value and row["line"] == line for row in self.registry) and value in words and file == REGISTRY
        if kind == "track":
            return file == REGISTRY and any(row["track"] == value and row["line"] == line for row in self.registry) and value in words
        if kind == "cond":
            return file == CONDITIONS and any(row["id"] == value and row["line"] == line for row in self.conditions) and value in words
        if kind == "spec":
            if file == OVERLAY:
                valid = any(row["id"] == value and row["line"] == line for row in self.sections)
            elif file == CONDITIONS:
                valid = any(value in row["sections"] and row["line"] == line for row in self.conditions)
            elif file == E2E:
                valid = any(row["section"] == value and row["line"] == line for row in self.layers)
            else:
                valid = False
            return valid and value in words
        if kind == "dec":
            return value in decision_ids(words)
        if kind == "layer":
            return file == E2E and any(row["id"] == value and row["line"] == line for row in self.layers) and value in words
        return value.split(":")[-1] in words

    def _validate_edge(self, edge, node_ids):
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            raise ValueError("graph edge names an absent node")
        kind = edge["edge"]
        if kind == "direct":
            src = edge["src"]
            for endpoint in ("source", "target"):
                words = edge["quotes"][endpoint]
                self._citation({**src, "quote": words})
                if not self._end_words(edge[endpoint], words, src["file"], src["line"]):
                    raise ValueError("direct edge quote does not name its typed endpoint")
        elif kind == "curated":
            self._citation(edge["src"])
            entry = self._citation(edge["curation"])
            if not isinstance(entry, dict) or entry.get("status") != "DRAFT":
                raise ValueError("curated edge has no draft table entry")
            group, identity = _json_parts(edge["curation"]["path"])
            if group == "experiments":
                expected = ("era:" + entry["era"], "exp:" + identity, entry["citations"]["era"])
            elif group == "model_eras":
                expected = ("era:" + entry["era"], "model:" + identity, entry["citation"])
            elif group == "experiment_hypotheses":
                expected = ("exp:" + identity, entry["hypothesis"], entry["citation"])
            elif group == "section_layers":
                expected = ("layer:" + entry["layer"], "spec:" + entry["section"], entry["citations"]["layer"])
            elif group == "model_corpus":
                expected = ("corpus:" + entry["corpus"], "model:" + entry["model"], entry["citation"])
            else:
                raise ValueError("unknown graph curation table")
            if (edge["source"], edge["target"], edge["src"]) != expected:
                raise ValueError("curated edge differs from its cited table entry")
        elif kind == "derived":
            inputs = edge.get("inputs", [])
            if len(inputs) < 2:
                raise ValueError("derived graph edge has an incomplete chain")
            current = edge["source"]
            for operand in inputs:
                self._validate_edge(operand, node_ids)
                ends = {operand["source"], operand["target"]}
                if current not in ends or len(ends) != 2:
                    raise ValueError("derived graph edge inputs do not form a chain")
                current = next(value for value in ends if value != current)
            if edge["target"] != current:
                raise ValueError("derived graph edge does not reach its target")
        else:
            raise ValueError("unknown graph edge type")

    def validate(self):
        """Check every curated citation and every explicit graph chain."""
        if not self._real_program:
            return
        expected = {row["id"] for row in self.registry}
        if expected != set(self.tables.get("experiments", {})):
            raise ValueError("each registry experiment must have exactly one explicit era")
        for identity, entry in self.tables["experiments"].items():
            if entry.get("status") != "DRAFT" or entry.get("era") not in self.tables["eras"]:
                raise ValueError("invalid draft experiment era: " + identity)
            for field in ("era", "question", "measure", "bar"):
                if field not in entry["citations"]:
                    raise ValueError("uncited framing field: " + identity + ":" + field)

        def citations(value):
            if isinstance(value, dict):
                if "status" in value and value["status"] != "DRAFT":
                    raise ValueError("context framing is not marked DRAFT")
                if "file" in value and ("line" in value or "path" in value):
                    self._citation(value)
                else:
                    for child in value.values():
                        citations(child)
            elif isinstance(value, list):
                for child in value:
                    citations(child)

        citations(self.tables)
        node_ids = {node["node_id"] for node in self.graph["nodes"]}
        if len(node_ids) != len(self.graph["nodes"]):
            raise ValueError("duplicate graph node ID")
        for node in self.graph["nodes"]:
            if "src" in node:
                self._citation(node["src"])
            for field in ("question", "description", "measure", "short_label", "status", "framing_status"):
                leaf = node.get(field)
                if isinstance(leaf, dict) and "value" in leaf:
                    citation = leaf["src"]
                    actual = self._citation(citation)
                    if ("path" in citation and leaf["value"] != actual
                            or "line" in citation and leaf["value"] not in actual):
                        raise ValueError("graph node leaf differs from source: " + node["node_id"] + ":" + field)
            if "ledger_src" in node:
                self._citation(node["ledger_src"])
            for date in node.get("dates", []):
                if "src" in date and date["value"] not in self._citation(date["src"]):
                    raise ValueError("ledger date differs from its quoted source")
        for event in self.graph.get("timeline", []):
            for field in ("decision", "date", "description", "status"):
                leaf = event[field]
                if "src" in leaf and leaf["value"] not in self._citation(leaf["src"]):
                    raise ValueError("ledger timeline value differs from its quoted source")
        for edge in self.graph["edges"]:
            self._validate_edge(edge, node_ids)


def load_program(root):
    return Program(root)
