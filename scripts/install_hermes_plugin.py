#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SRC = ROOT / "plugins" / "hermes_memory_stack"


def main() -> None:
    ap = argparse.ArgumentParser(description="Install the Hermes MemoryKit plugin wrapper.")
    ap.add_argument("--hermes-home", default="~/.hermes", help="Hermes home path, default: ~/.hermes")
    ap.add_argument("--repo", default=str(ROOT), help="Memory stack repo path used by plugin tools")
    ap.add_argument("--force", action="store_true", help="Replace an existing plugin directory")
    args = ap.parse_args()

    hermes_home = Path(args.hermes_home).expanduser()
    dest = hermes_home / "plugins" / "hermes_memory_stack"
    if dest.exists():
        if not args.force:
            raise SystemExit(f"Plugin already exists: {dest}. Re-run with --force to replace it.")
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(PLUGIN_SRC, dest)
    env_line = f"MEMORY_STACK_REPO={Path(args.repo).expanduser().resolve()}"
    print(f"installed={dest}")
    print(env_line)
    print("Add the MEMORY_STACK_REPO line to your Hermes .env, then restart Hermes or run /reset.")


if __name__ == "__main__":
    main()
