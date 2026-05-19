# Implementation guide for Hermes users

## 1. Enable memory and LCM

Run Hermes setup or edit `~/.hermes/config.yaml`:

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
context:
  engine: lcm
compression:
  enabled: true
```

Add the environment guardrails from `configs/memory-stack.env.example` to `~/.hermes/.env`.

## 2. Pick a durable docs store

This kit supports either:

- QMD CLI, if installed and indexed, or
- a plain Markdown workspace via `MEMORY_STACK_DOCS_PATH`.

The router will use what is available.

## 3. Build the entity graph

```bash
python scripts/memory_stack_entity_graph.py --docs ~/notes --lcm-db ~/.hermes/lcm.db --out data/entity-graph.json
```

## 4. Test retrieval

```bash
python scripts/memory_stack_router.py "what did we decide last week?" --json
python scripts/memory_stack_focus_brief.py "continue the project plan" --out /tmp/brief.md
```

## 5. Add regression cases

Create `regression-cases.json`:

```json
[
  {
    "name": "old decision recall",
    "query": "what did we decide about memory routing?",
    "required_source_types": ["raw_lcm"],
    "required_hints": ["memory"]
  }
]
```

Run:

```bash
python scripts/memory_stack_retrieval_regression.py --cases regression-cases.json
```

## 6. Install the Hermes plugin wrapper

```bash
python scripts/install_hermes_plugin.py --hermes-home ~/.hermes --repo "$PWD" --force
```

Add the printed `MEMORY_STACK_REPO=...` line to `~/.hermes/.env`, then restart Hermes or run `/reset`.

Enable the `memory_stack` toolset if your Hermes setup does not auto-enable plugin toolsets. The wrapper exposes:

- `memory_stack_status`
- `memory_stack_route`
- `memory_stack_focus_brief`
- `memory_stack_regress`

## 7. Wire skills into memory routing

Read `docs/skills-and-memory.md`, then add regression cases for skill-memory behavior. At minimum, test one old-conversation query, one project-convention query, and one workflow query that should load a skill plus retrieved docs.

## 8. Schedule maintenance

Use Hermes cron or your system cron to run `memory_stack_maintenance.py` nightly. Keep it boring: update indexes, run checks, write a report, alert only on failures.
