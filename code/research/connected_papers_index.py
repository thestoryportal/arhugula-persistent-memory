#!/usr/bin/env python3
"""Merge the operator's Connected Papers .bib exports into one index: per paper, how many of the seed neighbourhoods it
appears in (co-occurrence = centrality around the program's seeds), its year, and whether the repo already cites it
(title-prefix search over docs/, evidence/CORPUS/, _system/memory/, program/runbook/). Writes docs/CONNECTED_PAPERS_GRAPH_INDEX_<date>.md.
Usage: python3 code/research/connected_papers_index.py <corpus_dir> [--date YYYY-MM-DD]"""
import os, re, sys, glob, json, datetime, urllib.parse
from collections import defaultdict
ROOT = os.environ.get("LLMDB_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
corpus = sys.argv[1]; date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else datetime.date.today().isoformat()
ENTRY = re.compile(r"@\w+\{([^,]+),(.*?)\n\}", re.S)
FIELD = lambda body, k: (re.search(r"\b" + k + r"\s*=\s*\{(.*?)\}\s*,?\s*\n", body, re.S) or re.search(r"\b" + k + r"\s*=\s*\{(.*?)\}", body, re.S))
def norm(t): return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
seeds, papers = [], {}
for f in sorted(glob.glob(os.path.join(corpus, "**", "*.bib"), recursive=True)):   # includes INBOX/ and any later subfolders
    seed = urllib.parse.unquote(os.path.basename(f)).replace("ConnectedPapers-for-", "").replace(".bib", "").replace("-", " ")
    seed = re.sub(r"\s*\(\d+\)$", "", seed)
    if seed in seeds: continue
    seeds.append(seed); txt = open(f, encoding="utf-8", errors="replace").read()
    for m in ENTRY.finditer(txt):
        body = m.group(2); t = FIELD(body, "title"); y = FIELD(body, "year"); a = FIELD(body, "author")
        if not t: continue
        title = re.sub(r"\s+", " ", t.group(1)).strip(); key = norm(title)
        p = papers.setdefault(key, {"title": title, "year": (y.group(1).strip() if y else ""), "author": (a.group(1).split(" and ")[0].strip() if a else ""), "graphs": set()})
        p["graphs"].add(seed)
# repo coverage by title prefix (first 6 words) over the program's docs
hay = ""
for pat in ("docs/*.md", "evidence/CORPUS/*.md", "_system/memory/*.md", "program/runbook/", "program/EVIDENCE_INDEX.md"):
    for f in glob.glob(os.path.join(ROOT, pat)):
        if "CONNECTED_PAPERS_GRAPH_INDEX" in f: continue   # never read a previous index back as coverage
        hay += open(f, encoding="utf-8", errors="replace").read().lower() + "\n"
hay_n = norm(hay)
GENERIC = {"editing", "model", "knowledge", "memory", "learning", "editing large", "beyond", "towards", "rethinking", "evaluating", "understanding"}
for p in papers.values():
    words = p["title"].split(); pref = norm(" ".join(words[:6])) if len(words) >= 4 else norm(p["title"])
    short = p["title"].split(":")[0].strip() if ":" in p["title"] and len(p["title"].split(":")[0].split()) <= 2 else ""
    name_hit = bool(short) and len(short) >= 5 and short.lower() not in GENERIC and re.search(r"\b" + re.escape(short.lower()) + r"\b", hay) is not None
    p["in_repo"] = (bool(pref) and pref in hay_n) or name_hit
    p["match"] = "title" if (bool(pref) and pref in hay_n) else ("name" if name_hit else "")
rows = sorted(papers.values(), key=lambda p: (-len(p["graphs"]), p["year"], p["title"]))
n_graphs = len(seeds); recurring = [p for p in rows if len(p["graphs"]) >= 3]; new_recurring = [p for p in recurring if not p["in_repo"]]
out = [f"# Connected Papers graph index — {date}", "",
       f"_Merged from {n_graphs} Connected Papers exports supplied by the operator (`{corpus}`, kept outside git). {len(papers)} distinct papers. A paper's **graphs** count is the number of seed neighbourhoods it appears in; ≥ 3 marks the recurring spine of the field around the program's seeds. **in repo** = a title-prefix match somewhere in docs/, evidence/CORPUS/, _system/memory/ or the runbook (presence, not depth of reading)._", "",
       "## Seeds (one graph each)", ""] + [f"- {s}" for s in seeds] + ["", f"## Recurring papers (in ≥ 3 of {n_graphs} graphs): {len(recurring)}; not yet in repo context: {len(new_recurring)}", "",
       "| graphs | year | first author | title | in repo |", "|---|---|---|---|---|"]
for p in recurring: out.append(f"| {len(p['graphs'])} | {p['year']} | {p['author']} | {p['title']} | {('yes (' + p['match'] + ')') if p['in_repo'] else '**no**'} |")
out += ["", "## Recurring and not yet in repo context (reading candidates, by centrality)", ""] + [f"- ({len(p['graphs'])} graphs, {p['year']}) **{p['title']}** — {p['author']}" for p in new_recurring[:40]]
out += ["", f"## Year profile of all {len(papers)} papers", ""]
yc = defaultdict(int)
for p in rows: yc[p["year"] or "?"] += 1
out += [", ".join(f"{y}: {c}" for y, c in sorted(yc.items()))]
path = os.path.join(ROOT, f"docs/CONNECTED_PAPERS_GRAPH_INDEX_{date}.md"); open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
json.dump({"seeds": seeds, "papers": [{**p, "graphs": sorted(p["graphs"])} for p in rows]}, open(os.path.join(ROOT, f"results/connected_papers_index_{date}.json"), "w"), indent=1)
print(f"graphs={n_graphs} papers={len(papers)} recurring(>=3)={len(recurring)} new_recurring={len(new_recurring)} -> {path}")
