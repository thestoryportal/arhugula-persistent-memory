#!/usr/bin/env python3
"""Fetch Connected Papers graphs through the official API client (github.com/ConnectedPapers/connectedpapers-py).

Run without installing anything:
    uv run --with connectedpapers-py python tools/connected_papers_fetch.py --usages
    uv run --with connectedpapers-py python tools/connected_papers_fetch.py arXiv:2410.02355 DOI:10.48550/arXiv.2210.07229 <semantic-scholar-sha>

Paper ids: a Semantic Scholar sha id (40 hex chars), or arXiv:<id> / DOI:<doi> / CorpusId:<n>, resolved through the public
Semantic Scholar API. Each graph is written as JSON to the Connected Papers collection (default
/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/api/), beside the exported .bib graphs.

API key: the CONNECTED_PAPERS_API_KEY environment variable, else the macOS keychain item "connectedpapers-api-key"
(store it once: security add-generic-password -a "$USER" -s connectedpapers-api-key -w <key>). No key -> refuse
(the client's test token reaches one demo paper only). A fetched graph stays free to re-fetch for a month.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_OUT = "/Volumes/memit/llm-database-poc-mirror/connected-papers-knowledge-graphs/api"
KEYCHAIN_SERVICE = "connectedpapers-api-key"
SHA = re.compile(r"^[0-9a-f]{40}$")


def api_key():
    key = os.environ.get("CONNECTED_PAPERS_API_KEY", "").strip()
    if key:
        return key
    r = subprocess.run(["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    sys.exit(f"no Connected Papers API key: set CONNECTED_PAPERS_API_KEY or store keychain item '{KEYCHAIN_SERVICE}'")


def resolve(paper):
    """Any supported id -> Semantic Scholar sha id (the id the Connected Papers API uses)."""
    if SHA.match(paper.lower()):
        return paper.lower(), paper
    url = f"https://api.semanticscholar.org/graph/v1/paper/{urllib.parse.quote(paper, safe=':/')}?fields=paperId,title,year"
    req = urllib.request.Request(url, headers={"User-Agent": "llm-as-database-research"})
    for attempt, wait in enumerate((0, 5, 15, 30, 60)):   # the anonymous Semantic Scholar pool is shared and rate-limits bursts (HTTP 429)
        time.sleep(wait)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                d = json.load(resp)
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                sys.exit(f"Semantic Scholar lookup of {paper!r} failed: HTTP {e.code}")
    if not d.get("paperId"):
        sys.exit(f"Semantic Scholar could not resolve {paper!r}")
    return d["paperId"], f"{d.get('title')} ({d.get('year')})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("papers", nargs="*", help="paper ids (sha, arXiv:..., DOI:..., CorpusId:...)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory for graph JSON")
    ap.add_argument("--usages", action="store_true", help="print the remaining API usages and exit")
    a = ap.parse_args()

    from connectedpapers import ConnectedPapersClient
    client = ConnectedPapersClient(access_token=api_key())
    print(f"remaining usages: {client.get_remaining_usages_sync()}")
    if a.usages or not a.papers:
        return
    os.makedirs(a.out, exist_ok=True)
    for paper in a.papers:
        sha, label = resolve(paper)
        g = client.get_graph_sync(sha).graph_json
        path = os.path.join(a.out, f"{sha}.json")
        with open(path, "w") as f:
            json.dump(g, f, indent=1, default=lambda o: getattr(o, "__dict__", str(o)))
        print(f"{paper} -> {label}: {len(g.nodes)} papers, {len(g.common_references)} prior, {len(g.common_citations)} derivative -> {path}")
    print(f"remaining usages: {client.get_remaining_usages_sync()}")


if __name__ == "__main__":
    main()
