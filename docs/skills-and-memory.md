# Skills and memory in Hermes

Hermes skills are procedural memory. They tell the agent how to do a class of work: when to use a workflow, which commands to run, what pitfalls to avoid, and how to verify the result.

That does not replace the memory stack. It completes it.

## Short answer

Hermes already has strong skill calling. Skills answer **how**, while memory answers **what, who, when, where, and why this time**. Good memory makes skill calling sharper.

Use both:

- **Skills:** reusable procedures and tool recipes.
- **Native memory:** compact durable user facts, preferences, and environment conventions.
- **LCM:** exact raw conversation recovery after compression.
- **QMD or Markdown wiki:** larger durable docs, decisions, reports, and project notes.
- **Entity graph and router:** decide which source should answer the current question.
- **Focus brief:** inject only the relevant retrieved context for this task.

## What skills are good at

Skills are best for stable procedures:

- how to review a GitHub PR
- how to publish a social post safely
- how to run a specific benchmark
- how to operate a tool with known gotchas
- how to format a recurring report
- how to debug a known class of failure

A good skill is compact, trigger-driven, and verified. It should not contain raw chat history or a growing pile of one-off facts.

## What memory adds to skills

Memory makes skill calling precise.

A skill can say “use the GitHub PR workflow.” Memory tells Hermes:

- which repo matters today
- which branch or PR is active
- which user preference applies
- which prior decision constrains the work
- which failure happened last time
- which profile or Telegram topic owns the task
- which facts are durable enough to reuse

Without memory, skill calling becomes generic. The right skill may load, but it may not know the exact context that makes the workflow safe.

## Promotion policy

Use this routing rule when new information appears.

### Keep in LCM only

Use LCM for raw detail that may matter later but is not a durable rule:

- exact wording from a prior exchange
- old task discussion
- transient debugging logs
- a one-time decision with short shelf life

### Save to native memory

Use native memory for compact facts that should affect future behavior:

- user preferences
- stable environment facts
- recurring project conventions
- durable correction from the user
- known tool quirk that affects future work

Keep it short. Native memory should not become a transcript.

### Write to wiki or docs

Use QMD or Markdown docs for larger structured knowledge:

- design docs
- benchmark reports
- implementation notes
- public-safe research summaries
- project background that is too large for native memory

### Create or update a skill

Use a skill when the lesson is procedural:

- a workflow with steps
- a repeated troubleshooting path
- a tool-specific command sequence
- a review checklist
- a reusable safety rule

If an existing umbrella skill fits, update it. Do not create narrow one-session skills unless the workflow is truly new.

## Skill retrieval should be memory-aware

The best Hermes behavior is:

1. Classify the task.
2. Retrieve relevant memory, LCM, docs, and graph context.
3. Load matching skills.
4. Build a short focus brief with citations.
5. Execute the skill using the retrieved context.
6. Promote any durable lesson back to the right layer.

This avoids two failure modes:

- **Skill without context:** the agent knows the workflow but misses the current constraint.
- **Memory without procedure:** the agent remembers facts but improvises the steps.

## Regression cases for skills

Add regression checks for skill-memory behavior, not only document retrieval.

Good cases:

- A query about an old conversation should route to raw LCM before skills.
- A query about a known workflow should retrieve the skill and the project docs.
- A user correction should be found as native memory and should update the relevant skill when procedural.
- A project task should load the project convention before running a generic skill.

## Practical rule

Hermes skill calling can be excellent and still need memory.

Skills are the playbooks. Memory is the map, the current location, and the notes from the last time you ran the playbook.
