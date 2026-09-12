#!/usr/bin/env python3
"""Enumerate API-visible neuron documents without semantic search or firing them.

This is a logical JSONL export, not a transaction snapshot or a .nrdb backup.
Use the configured, authorized endpoint explicitly. Authentication is read from
QUBICDB_MCP_API_KEY when present; no credentials are written to the output.
"""

import argparse
import json
import os
from pathlib import Path
import tempfile
import urllib.parse
import urllib.request


def export_neurons(url, index_id, output, metadata_filter=None, page_size=200):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Provide the configured HTTP(S) QubicDB base URL")
    if not index_id or not 1 <= page_size <= 500:
        raise ValueError("An index ID and page size between 1 and 500 are required")
    base = url.rstrip("/")
    if base.endswith("/mcp"):
        base = base[:-4]
    headers = {"Content-Type": "application/json", "X-Index-ID": index_id}
    key = os.environ.get("QUBICDB_MCP_API_KEY")
    if key:
        headers["X-API-Key"] = key
    output = Path(output)
    manifest_path = Path(str(output) + ".manifest.json")
    if output.exists() or manifest_path.exists():
        raise FileExistsError("Choose a new output path; existing exports are preserved")
    output.parent.mkdir(parents=True, exist_ok=True)

    def command(kind, options=None):
        body = {"type": kind, "collection": "neurons", "filter": metadata_filter or {}}
        if options:
            body["options"] = options
        request = urllib.request.Request(base + "/v1/command", json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
        if result.get("success") is not True:
            raise RuntimeError("QubicDB command failed: " + str(result.get("error")))
        return result

    before = command("count").get("count", 0)
    seen = set()
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, delete=False) as stream:
            temp_path = Path(stream.name)
            # Never use an empty page as the sole stop condition: this server's
            # skip >= count boundary can repeat the first page.
            for skip in range(0, before, page_size):
                result = command("find", {"sort": {"_id": 1}, "skip": skip, "limit": page_size})
                rows = result.get("data") or []
                if len(rows) != min(page_size, before - skip):
                    raise RuntimeError("Page count changed during enumeration; no complete export produced")
                for row in rows:
                    neuron_id = row.get("_id")
                    if not neuron_id or neuron_id in seen:
                        raise RuntimeError("Repeated/missing neuron ID; pagination is not complete")
                    seen.add(neuron_id)
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        after = command("count").get("count", 0)
        if before != after or len(seen) != before:
            raise RuntimeError("Index changed during enumeration; retry against a stable collection")
        summary = {"index_id": index_id, "filter": metadata_filter or {}, "count_before": before,
                   "count_after": after, "unique_neurons": len(seen), "page_size": page_size,
                   "enumeration_consistent": True, "transaction_snapshot": False,
                   "scope": "API-visible neuron documents; excludes internal embeddings and synapses",
                   "output": str(output.resolve())}
        # Exclusive creation avoids replacing a file created while the query ran.
        with output.open("x", encoding="utf-8") as target, temp_path.open(encoding="utf-8") as source:
            for line in source:
                target.write(line)
        manifest_path.write_text(json.dumps(summary, indent=2) + "\n")
        return summary
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--index", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--filter", default="{}", help="Exact command filter as JSON; metadata keys are top-level")
    parser.add_argument("--page-size", type=int, default=200)
    args = parser.parse_args()
    query_filter = json.loads(args.filter)
    if not isinstance(query_filter, dict):
        parser.error("--filter must be a JSON object")
    print(json.dumps(export_neurons(args.url, args.index, args.output, query_filter, args.page_size), indent=2))
