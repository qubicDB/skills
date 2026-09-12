#!/usr/bin/env python3
"""Check release/discovery invariants without connecting to a database or account."""
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {"qubicdb-skills": 4, "qubicdb-experimental": 6}


def read(path):
    return json.loads(path.read_text())


class PackagingTests(unittest.TestCase):
    def test_both_marketplaces_resolve_the_same_packages(self):
        codex = read(ROOT / ".agents/plugins/marketplace.json")
        claude = read(ROOT / ".claude-plugin/marketplace.json")
        self.assertEqual(codex["name"], claude["name"])
        for marketplace in (codex, claude):
            self.assertEqual({p["name"] for p in marketplace["plugins"]}, set(PACKAGES))
            for entry in marketplace["plugins"]:
                source = entry["source"]
                if isinstance(source, dict):
                    self.assertEqual(source["source"], "local")
                    source = source["path"]
                self.assertEqual((ROOT / source).resolve(), ROOT / "plugins" / entry["name"])

    def test_client_and_portable_release_identity_agree(self):
        entries = {p["name"]: p for p in read(ROOT / ".claude-plugin/marketplace.json")["plugins"]}
        for name in PACKAGES:
            folder = ROOT / "plugins" / name
            portable = read(folder / "plugin.json")
            self.assertEqual(portable["$schema"], "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json")
            for relative in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
                native = read(folder / relative)
                for key in ("name", "version", "description", "author", "repository", "license"):
                    self.assertEqual(native[key], portable[key], (name, relative, key))
            self.assertEqual(portable["name"], name)
            self.assertEqual(portable["version"], entries[name]["version"])
            self.assertEqual(portable["extensions"]["com.openai"]["interface"],
                             read(folder / ".codex-plugin/plugin.json")["interface"])

    def test_discovery_preserves_skill_resources(self):
        for name, expected in PACKAGES.items():
            folder = ROOT / "plugins" / name
            self.assertEqual(read(folder / ".codex-plugin/plugin.json")["skills"], "./skills/")
            skills = list((folder / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(skills), expected)
            for skill in skills:
                self.assertTrue(skill.read_text().startswith("---\n"), skill)
                self.assertTrue((skill.parent / "agents/openai.yaml").is_file(), skill)
        core = ROOT / "plugins/qubicdb-skills/skills"
        self.assertTrue((core / "qubic/references/capabilities.md").is_file())
        self.assertTrue((core / "qubic-init/references/setup.md").is_file())
        self.assertTrue((core / "qubic-search/scripts/read_all.py").is_file())

    def test_install_does_not_add_a_second_mcp_connection(self):
        for name in PACKAGES:
            folder = ROOT / "plugins" / name
            for relative in ("mcp.json", ".mcp.json", "hooks/hooks.json"):
                self.assertFalse((folder / relative).exists(), relative)
            for relative in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
                manifest = read(folder / relative)
                self.assertNotIn("mcpServers", manifest)
                self.assertNotIn("apps", manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
