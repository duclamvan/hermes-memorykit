"""Hermes plugin wrapper for Hermes MemoryKit.

Install by copying this directory to ``~/.hermes/plugins/hermes_memory_stack``
or by pointing ``MEMORY_STACK_REPO`` at a clone of this repository. The plugin
registers thin Hermes tools that call the public scripts in ``scripts/``.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

PLUGIN_DIR = Path(__file__).resolve().parent


def _repo_root() -> Path:
    env = os.getenv("MEMORY_STACK_REPO")
    if env:
        return Path(env).expanduser().resolve()
    # In this repo: plugins/hermes_memory_stack/__init__.py -> repo root.
    candidate = PLUGIN_DIR.parents[1]
    if (candidate / "scripts" / "memory_stack_router.py").exists():
        return candidate
    # If the plugin is copied alone, allow a sibling checkout next to it.
    sibling = PLUGIN_DIR.parent / "hermes-memorykit"
    if (sibling / "scripts" / "memory_stack_router.py").exists():
        return sibling
    return candidate


def _json_result(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _script(name: str) -> Path:
    return _repo_root() / "scripts" / name


def _run_script(script_name: str, args: list[str], timeout: int = 60) -> dict[str, Any]:
    script = _script(script_name)
    if not script.exists():
        return {
            "status": "error",
            "error": f"missing script: {script}",
            "hint": "Set MEMORY_STACK_REPO to a clone of duclamvan/hermes-memorykit.",
        }
    proc = subprocess.run(
        [sys.executable, str(script), *args],
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    parsed: Any = None
    if proc.stdout.strip():
        try:
            parsed = json.loads(proc.stdout)
        except json.JSONDecodeError:
            parsed = proc.stdout.strip()
    return {
        "status": "pass" if proc.returncode == 0 else "error",
        "returncode": proc.returncode,
        "data": parsed,
        "stdout": proc.stdout.strip()[:4000],
        "stderr": proc.stderr.strip()[:4000],
    }


def _handle_memory_stack_status(args: dict[str, Any], **_: Any) -> str:
    root = _repo_root()
    hermes_home = Path(str(args.get("hermes_home") or os.getenv("HERMES_HOME") or "~/.hermes")).expanduser()
    workspace = Path(str(args.get("workspace") or os.getenv("MEMORY_STACK_WORKSPACE") or root)).expanduser()
    return _json_result(_run_script("memory_stack_verify.py", ["--hermes-home", str(hermes_home), "--workspace", str(workspace)], timeout=45))


def _handle_memory_stack_route(args: dict[str, Any], **_: Any) -> str:
    query = str(args.get("query") or "").strip()
    if not query:
        return _json_result({"status": "error", "error": "query is required"})
    cli = [query, "--json", "--limit", str(int(args.get("limit") or 8))]
    for key, flag in (("docs", "--docs"), ("lcm_db", "--lcm-db"), ("graph", "--graph")):
        value = args.get(key)
        if value:
            cli.extend([flag, str(value)])
    return _json_result(_run_script("memory_stack_router.py", cli, timeout=60))


def _handle_memory_stack_focus_brief(args: dict[str, Any], **_: Any) -> str:
    task = str(args.get("task") or "").strip()
    if not task:
        return _json_result({"status": "error", "error": "task is required"})
    out = str(args.get("out") or "/tmp/hermes-memory-focus-brief.md")
    cli = [task, "--out", out]
    for key, flag in (("docs", "--docs"), ("lcm_db", "--lcm-db"), ("graph", "--graph")):
        value = args.get(key)
        if value:
            cli.extend([flag, str(value)])
    return _json_result(_run_script("memory_stack_focus_brief.py", cli, timeout=60))


def _handle_memory_stack_regress(args: dict[str, Any], **_: Any) -> str:
    cli: list[str] = []
    cases = args.get("cases")
    if cases:
        cli.extend(["--cases", str(cases)])
    return _json_result(_run_script("memory_stack_retrieval_regression.py", cli, timeout=int(args.get("timeout") or 120)))


def _schema(name: str, description: str, properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required or [],
        },
    }


TOOLS = (
    (
        "memory_stack_status",
        _schema(
            "memory_stack_status",
            "Check Hermes MemoryKit health and path readiness.",
            {
                "hermes_home": {"type": "string", "description": "Hermes home path. Defaults to HERMES_HOME or ~/.hermes."},
                "workspace": {"type": "string", "description": "Workspace/repo path to verify. Defaults to MEMORY_STACK_WORKSPACE or the repo."},
            },
        ),
        _handle_memory_stack_status,
        "🧠",
    ),
    (
        "memory_stack_route",
        _schema(
            "memory_stack_route",
            "Route a memory query across docs, LCM transcript, QMD, and entity graph sources.",
            {
                "query": {"type": "string"},
                "docs": {"type": "string"},
                "lcm_db": {"type": "string"},
                "graph": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 25},
            },
            ["query"],
        ),
        _handle_memory_stack_route,
        "🔎",
    ),
    (
        "memory_stack_focus_brief",
        _schema(
            "memory_stack_focus_brief",
            "Generate a cited task-local focus brief from routed memory results.",
            {
                "task": {"type": "string"},
                "out": {"type": "string"},
                "docs": {"type": "string"},
                "lcm_db": {"type": "string"},
                "graph": {"type": "string"},
            },
            ["task"],
        ),
        _handle_memory_stack_focus_brief,
        "📌",
    ),
    (
        "memory_stack_regress",
        _schema(
            "memory_stack_regress",
            "Run memory retrieval regression checks for the stack.",
            {
                "cases": {"type": "string", "description": "Optional regression cases JSON path."},
                "timeout": {"type": "integer", "minimum": 10, "maximum": 600},
            },
        ),
        _handle_memory_stack_regress,
        "✅",
    ),
)


def register(ctx) -> None:
    """Register Hermes MemoryKit tools."""
    for name, schema, handler, emoji in TOOLS:
        ctx.register_tool(
            name=name,
            toolset="memory_stack",
            schema=schema,
            handler=handler,
            emoji=emoji,
        )
