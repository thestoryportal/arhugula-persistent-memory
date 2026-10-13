#!/usr/bin/env python3
"""Small helper for the local OpenResearch dashboard API. Usage:
  orx_api.py GET <route>
  orx_api.py POST <route> '<json>'
"""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:4791"


def main() -> int:
    method, route = sys.argv[1], sys.argv[2]
    data = sys.argv[3].encode() if len(sys.argv) > 3 else None
    req = urllib.request.Request(BASE + route, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            body = r.read().decode()
            print(r.status)
            try:
                print(json.dumps(json.loads(body), indent=1)[:4000])
            except json.JSONDecodeError:
                print(body[:4000])
            return 0
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:4000])
        return 1


if __name__ == "__main__":
    sys.exit(main())
