import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class FakeContext:
    def __init__(self):
        self.tools = {}

    def register_tool(self, **kwargs):
        self.tools[kwargs["name"]] = kwargs


def test_plugin_registers_memory_stack_tools(monkeypatch):
    monkeypatch.setenv("MEMORY_STACK_REPO", str(ROOT))
    plugin = importlib.import_module("plugins.hermes_memory_stack")
    ctx = FakeContext()
    plugin.register(ctx)
    assert set(ctx.tools) == {
        "memory_stack_status",
        "memory_stack_route",
        "memory_stack_focus_brief",
        "memory_stack_regress",
    }
    assert all(tool["toolset"] == "memory_stack" for tool in ctx.tools.values())


def test_plugin_route_handler_uses_public_scripts(tmp_path, monkeypatch):
    monkeypatch.setenv("MEMORY_STACK_REPO", str(ROOT))
    plugin = importlib.import_module("plugins.hermes_memory_stack")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "decision.md").write_text("Hermes skills need memory context for project-specific decisions.")

    payload = json.loads(plugin._handle_memory_stack_route({
        "query": "skills memory project decisions",
        "docs": str(docs),
        "limit": 5,
    }))

    assert payload["status"] == "pass"
    assert payload["data"]["results"]
    assert payload["data"]["results"][0]["source_type"] == "curated_doc"


def test_install_hermes_plugin_copies_wrapper(tmp_path):
    hermes_home = tmp_path / "hermes"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "install_hermes_plugin.py"), "--hermes-home", str(hermes_home), "--repo", str(ROOT)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    installed = hermes_home / "plugins" / "hermes_memory_stack"
    assert (installed / "plugin.yaml").exists()
    assert (installed / "__init__.py").exists()
    assert "MEMORY_STACK_REPO=" in proc.stdout


def test_skills_memory_doc_states_policy():
    text = (ROOT / "docs" / "skills-and-memory.md").read_text()
    assert "Skills answer **how**" in text
    assert "Save to native memory" in text
    assert "Create or update a skill" in text
