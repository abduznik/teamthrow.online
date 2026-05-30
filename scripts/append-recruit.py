#!/usr/bin/env python3
"""Append a recruit entry to the JSONL file (append-only, no full rewrite).
Usage: python3 scripts/append-recruit.py <json_payload>
   or:  echo $PAYLOAD | python3 scripts/append-recruit.py

Each line is one JSON recruit entry. Git only stores the diff (one line)."""

import json, sys, os

def main():
    # Read payload from stdin (pipe) or argv[1]
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        raw = sys.argv[1] if len(sys.argv) > 1 else ''

    if not raw:
        print("ERROR: no payload provided")
        sys.exit(1)

    payload = json.loads(raw)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    jsonl_path = os.path.join(script_dir, "data", "recruits.jsonl")

    # Ensure file exists
    if not os.path.exists(jsonl_path):
        with open(jsonl_path, 'w') as f:
            f.write('')

    # Append one line
    with open(jsonl_path, 'a') as f:
        f.write(json.dumps(payload, ensure_ascii=False) + '\n')

    print(f"Appended: {payload.get('tag', payload.get('battletag', '?'))}")
    sys.exit(0)

if __name__ == "__main__":
    main()
