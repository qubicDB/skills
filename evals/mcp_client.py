"""Small stdlib client for disposable local QubicDB evaluations, not a production SDK."""

import argparse
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request


class Client:
    def __init__(self, url=None):
        self.url = url or os.environ.get("QUBICDB_EVAL_URL", "http://127.0.0.1:16060/mcp")
        parsed = urllib.parse.urlparse(self.url)
        if parsed.hostname not in ("127.0.0.1", "localhost", "::1"):
            raise ValueError("Evaluations require a disposable localhost instance")
        self.key = os.environ.get("QUBICDB_MCP_API_KEY", "")
        self.sequence = 0
        self.session = None
        self.rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                               "clientInfo": {"name": "qubicdb-skills-eval", "version": "1.0"}})

    def rpc(self, method, params):
        self.sequence += 1
        payload = {"jsonrpc": "2.0", "id": self.sequence, "method": method, "params": params}
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.key:
            headers["X-API-Key"] = self.key
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        request = urllib.request.Request(self.url, json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            self.session = response.headers.get("Mcp-Session-Id", self.session)
            raw = response.read().decode()
        if raw.lstrip().startswith("data:") or "\ndata:" in raw:
            messages = [json.loads(line[5:].strip()) for line in raw.splitlines() if line.startswith("data:")]
            result = next(m for m in messages if m.get("id") == self.sequence)
        else:
            result = json.loads(raw)
        if "error" in result:
            raise RuntimeError(result["error"])
        return result["result"]

    def call(self, name, **arguments):
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        log = os.environ.get("QUBICDB_EVAL_TRACE")
        if log:
            with Path(log).open("a") as stream:
                stream.write(json.dumps({"tool": name, "arguments": arguments, "result": result}) + "\n")
        if result.get("isError"):
            raise RuntimeError(result.get("content"))
        if result.get("structuredContent") is not None:
            return result["structuredContent"]
        for block in reversed(result.get("content", [])):
            if block.get("type") == "text":
                try:
                    return json.loads(block["text"])
                except json.JSONDecodeError:
                    pass
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tool", help="list or the exact MCP tool name")
    parser.add_argument("arguments", nargs="?", default="{}", help="JSON arguments")
    args = parser.parse_args()
    client = Client()
    result = client.rpc("tools/list", {}) if args.tool == "list" else client.call(args.tool, **json.loads(args.arguments))
    print(json.dumps(result, indent=2))
