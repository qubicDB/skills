"""Behavioral contract tests against a disposable Docker Hub bundled instance.

Run with the variables documented in evals/README.md. All created indexes use a
unique eval prefix. Admin alpha changes are restored even when an assertion fails.
"""

import base64
import importlib.util
import json
import math
import os
from pathlib import Path
import tempfile
import time
import unittest
import urllib.error
import urllib.request
import uuid

from mcp_client import Client


class LiveContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("QUBICDB_EVAL_DISPOSABLE") != "1":
            raise RuntimeError("Set QUBICDB_EVAL_DISPOSABLE=1 only for the disposable evaluation instance")
        cls.client = Client()
        cls.base = cls.client.url.rsplit("/mcp", 1)[0]
        cls.prefix = "eval-" + uuid.uuid4().hex[:12]

    def index(self, suffix):
        name = self.prefix + "-" + suffix
        self.client.call("qubicdb_registry_find_or_create", uuid=name)
        return name

    def write(self, index, content, **metadata):
        return self.client.call("qubicdb_write", index_id=index, content=content,
                                metadata=json.dumps(metadata))

    def rest(self, path, data=None, index=None, method=None, admin=False):
        headers = {"Content-Type": "application/json"}
        if index:
            headers["X-Index-ID"] = index
        if admin:
            credentials = os.environ["QUBICDB_EVAL_ADMIN"]
            headers["Authorization"] = "Basic " + base64.b64encode(credentials.encode()).decode()
        request = urllib.request.Request(self.base + path,
                                         None if data is None else json.dumps(data).encode(),
                                         headers=headers, method=method)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    def test_discovered_mcp_contract(self):
        tools = {t["name"]: t["inputSchema"] for t in self.client.rpc("tools/list", {})["tools"]}
        expected = {"write", "read", "search", "recall", "context", "registry_find_or_create",
                    "list_indexes", "global_search", "multi_search", "recent_indexes"}
        self.assertEqual(set(tools), {"qubicdb_" + n for n in expected})
        self.assertEqual(tools["qubicdb_write"]["properties"]["metadata"]["type"], "string")
        self.assertEqual(tools["qubicdb_multi_search"]["properties"]["index_ids"]["type"], "string")
        self.assertNotIn("strict", tools["qubicdb_multi_search"]["properties"])
        self.assertNotIn("metadata", tools["qubicdb_context"]["properties"])
        self.assertNotIn("vector", tools["qubicdb_search"]["properties"])

    def test_registration_does_not_load_index(self):
        index = self.index("registered-only")
        again = self.client.call("qubicdb_registry_find_or_create", uuid=index)
        self.assertFalse(again["created"])
        active = self.client.call("qubicdb_list_indexes", active_only=True, limit=1000)
        self.assertNotIn(index, {x["index_id"] for x in active.get("indexes") or []})
        registered = self.client.call("qubicdb_list_indexes", active_only=False, limit=1000)
        self.assertIn(index, {x["index_id"] for x in registered["indexes"]})

    def test_duplicate_does_not_update_metadata(self):
        index = self.index("duplicate")
        first = self.write(index, "Cedar selects PostgreSQL for receipt storage.", status="proposed")
        second = self.write(index, first["content"], status="approved")
        self.assertEqual(first["_id"], second["_id"])
        self.assertEqual(second["metadata"]["status"], "proposed")
        self.assertGreater(second["accessCount"], first["accessCount"])
        correction = self.write(index, "Cedar now selects SQLite for receipt storage (ADR-12).",
                                supersedes=first["_id"], status="approved")
        self.assertNotEqual(correction["_id"], first["_id"])
        original = self.client.call("qubicdb_read", index_id=index, id=first["_id"])
        self.assertEqual(original["content"], first["content"])

    def test_strict_search_and_soft_multi_search(self):
        index = self.index("filter")
        approved = self.write(index, "Receipt storage policy is approved.", status="approved")
        draft = self.write(index, "Receipt storage draft suggests another approach.", status="draft")
        args = dict(index_id=index, query="receipt storage", limit=10, metadata='{"status":"approved"}')
        strict = self.client.call("qubicdb_search", **args, strict=True)
        self.assertEqual({n["_id"] for n in strict["results"]}, {approved["_id"]})
        soft = self.client.call("qubicdb_multi_search", index_ids=json.dumps([index]), query="receipt storage",
                                limit=10, metadata='{"status":"approved"}')
        self.assertIn(draft["_id"], {n["_id"] for n in soft["results"]})
        self.assertFalse(soft["errors"])

    def test_search_scope_and_recent_indexes(self):
        a, b, outside = [self.index(n) for n in ("scope-a", "scope-b", "scope-outside")]
        for index in (a, b, outside):
            self.write(index, "Receipt API uses an idempotency key: " + index)
        scoped = self.client.call("qubicdb_multi_search", index_ids=json.dumps([a, b]), query="receipt API", limit=2)
        self.assertEqual({n["_index"] for n in scoped["results"]}, {a, b})
        global_result = self.client.call("qubicdb_global_search", query="receipt API", limit=50)
        self.assertIn(outside, {n["_index"] for n in global_result["results"]})
        recent = self.client.call("qubicdb_recent_indexes", limit=1000, min_neurons=1)
        self.assertIn(a, {n["index_id"] for n in recent.get("indexes") or []})

    def test_context_budget_and_depth_zero(self):
        index = self.index("context")
        self.write(index, "Database receipts use an idempotency key to avoid duplicate charges.")
        search = self.client.call("qubicdb_search", index_id=index, query="receipts", depth=0)
        self.assertEqual(search["depth"], 2)
        context = self.client.call("qubicdb_context", index_id=index, cue="receipts", max_tokens=40)
        self.assertIn("idempotency", context["context"])
        self.assertLessEqual(context["estimatedTokens"], 40)
        tiny = self.client.call("qubicdb_context", index_id=index, cue="receipts", max_tokens=1)
        self.assertEqual(tiny["neuronsUsed"], 0)

    def test_exact_filter_without_semantic_search(self):
        index = self.index("exact")
        expected = self.write(index, "Receipt retry incident ERR-CEDAR-17.", incident="ERR-CEDAR-17")
        self.write(index, "Receipt retry incident ERR-CEDAR-170.", incident="ERR-CEDAR-170")
        result = self.rest("/v1/command", {"type": "find", "collection": "neurons",
                                          "filter": {"incident": "ERR-CEDAR-17"},
                                          "options": {"limit": 5}}, index=index)
        self.assertTrue(result["success"])
        self.assertEqual([n["_id"] for n in result["data"]], [expected["_id"]])
        count = self.rest("/v1/command", {"type": "count", "collection": "neurons",
                                         "filter": {"incident": "ERR-CEDAR-17"}}, index=index)
        self.assertEqual(count["count"], 1)

    def test_neuron_mutation_is_disabled(self):
        index = self.index("immutable")
        neuron = self.write(index, "Keep this approved receipt decision.")
        for command in ("update", "delete", "activate"):
            with self.assertRaises(urllib.error.HTTPError) as error:
                self.rest("/v1/command", {"type": command, "collection": "neurons",
                                          "filter": {"_id": neuron["_id"]},
                                          "update": {"$set": {"content": "changed"}}}, index=index)
            self.assertEqual(error.exception.code, 400)
            self.assertIn("mutation", error.exception.read().decode().lower())
        self.assertEqual(self.client.call("qubicdb_read", index_id=index, id=neuron["_id"])["content"], neuron["content"])

    def test_real_embedding_changes_nonlexical_retrieval(self):
        index = self.index("vector")
        neuron = self.write(index, "Canines nap peacefully beside fireplaces.")
        original = self.rest("/v1/config", admin=True)["vector"]
        self.assertTrue(original["enabled"])
        self.assertIn("MiniLM", original["modelPath"])
        try:
            self.rest("/v1/config", {"vector": {"alpha": 0}}, admin=True)
            lexical = self.client.call("qubicdb_search", index_id=index, query="Dogs sleep", depth=1)
            self.assertEqual(lexical["count"], 0)
            self.rest("/v1/config", {"vector": {"alpha": 0.6}}, admin=True)
            semantic = self.client.call("qubicdb_search", index_id=index, query="Dogs sleep", depth=1)
            self.assertIn(neuron["_id"], {n["_id"] for n in semantic["results"]})
        finally:
            self.rest("/v1/config", {"vector": {"alpha": original["alpha"]}}, admin=True)

    def test_inspection_and_lifecycle(self):
        index = self.index("inspect")
        self.write(index, "Inspect receipt memory graph and lifecycle.")
        for path in ("/v1/brain/state", "/v1/brain/stats", "/v1/graph", "/v1/synapses", "/v1/activity"):
            self.assertIsInstance(self.rest(path, index=index), (dict, list))
        self.rest("/v1/brain/sleep", {}, index=index)
        self.rest("/v1/brain/wake", {}, index=index)
        self.assertEqual(self.client.call("qubicdb_recall", index_id=index, limit=5)["count"], 1)

    def test_coactivation_strengthens_and_moves_related_neurons(self):
        index = self.index("spatial")
        a = self.write(index, "Gateway retries retain the payment key.")
        b = self.write(index, "Payment key deduplication prevents duplicate charges.")
        initial = self.rest("/v1/graph", index=index)
        edge = self.rest("/v1/synapses", index=index)["synapses"][0]
        self.assertAlmostEqual(edge["weight"], 0.2, places=3)
        self.client.call("qubicdb_recall", index_id=index, limit=10)
        scanned = self.rest("/v1/synapses", index=index)["synapses"][0]
        self.assertEqual(scanned["co_fire_count"], edge["co_fire_count"])
        for _ in range(4):
            self.client.call("qubicdb_read", index_id=index, id=a["_id"])
            self.client.call("qubicdb_read", index_id=index, id=b["_id"])
        changed = self.rest("/v1/synapses", index=index)["synapses"][0]
        self.assertGreater(changed["weight"], edge["weight"])
        self.assertGreater(changed["co_fire_count"], edge["co_fire_count"])

        def distance(graph):
            nodes = {n["id"]: n["position"] for n in graph["nodes"]}
            return math.sqrt(sum((x-y)**2 for x, y in zip(nodes[a["_id"]], nodes[b["_id"]])))

        original_distance = distance(initial)
        deadline = time.monotonic() + 2
        while True:
            current = distance(self.rest("/v1/graph", index=index))
            if current < original_distance or time.monotonic() > deadline:
                break
            time.sleep(0.02)
        self.assertLess(current, original_distance)

    def test_rest_parent_position_is_distinct_from_metadata_and_tags(self):
        index = self.index("parent")
        parent = self.write(index, "Gateway protocol contract.")
        child = self.rest("/v1/write", {"content": "Retention exception for archived transfer receipts.",
                                        "parent_id": parent["_id"], "metadata": {"source": "contract.md"},
                                        "tags": ["requested-tag"]}, index=index)
        self.assertTrue(all(abs(a-b) <= 0.100001 for a,b in zip(parent["position"], child["position"])))
        self.assertEqual(child["metadata"]["source"], "contract.md")
        self.assertEqual(child["tags"], [])

    def test_complete_data_export_beyond_recall_limits(self):
        index = self.index("full-corpus")
        for number in range(520):
            self.rest("/v1/write", {"content": f"Archived manifest {number:04d} passed verification.",
                                    "metadata": {"record_number": str(number)}}, index=index)
            time.sleep(0.025)
        self.assertEqual(self.client.call("qubicdb_recall", index_id=index, limit=1000)["count"], 500)
        self.assertEqual(self.rest("/v1/recall?offset=400&limit=1000", index=index)["count"], 100)
        repeated = self.rest("/v1/command", {"type": "find", "collection": "neurons",
                                             "options": {"skip": 520, "limit": 2}}, index=index)
        self.assertEqual(repeated["count"], 2)
        source = Path(__file__).resolve().parents[1] / "plugins/qubicdb-skills/skills/qubic-search/scripts/read_all.py"
        spec = importlib.util.spec_from_file_location("read_all", source)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        with tempfile.TemporaryDirectory(prefix="qubic-export-test-") as temporary:
            output = Path(temporary) / "neurons.jsonl"
            summary = helper.export_neurons(self.base, index, output)
            rows = [json.loads(line) for line in output.read_text().splitlines()]
            self.assertEqual(summary["unique_neurons"], 520)
            self.assertEqual({int(n["metadata"]["record_number"]) for n in rows}, set(range(520)))
            self.assertTrue(all(n["accessCount"] == 1 for n in rows))
            with self.assertRaises(FileExistsError):
                helper.export_neurons(self.base, index, output)
        stats = self.rest("/v1/brain/stats", index=index)
        self.assertEqual(stats["current_dimension"], 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
