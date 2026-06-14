---
name: manage-memory
description: Manage a workspace memory and task system using MEMORY.md, memory/, and TASKS.md. Use this skill whenever the user wants to initialize memory, remember people/projects/acronyms/preferences, decode shorthand, manage tasks, create or update TASKS.md, refresh stale context, clean or reorganize MEMORY.md, sync todos, or run start/update-style workflows. Route progressively to scenario-specific references for initialization, memory lookup/update, task management, routine refresh, and comprehensive scan.
---

# Manage Memory

Manage durable workspace context for agents and users. This skill combines a
two-tier memory system with lightweight Markdown task tracking:

```text
MEMORY.md          # hot cache: frequent people, terms, projects, preferences
memory/            # deep memory: complete glossary and detailed profiles
  glossary.md
  people/
  projects/
  context/
TASKS.md           # shared task list
```

Keep this file as the router. Load only the reference files needed for the
current scenario.

## Route The Request

| Scenario | User intent | Read next |
| --- | --- | --- |
| Initialize | Set up memory/tasks for the first time, run start, create files | `references/start.md` |
| Decode or remember | Explain shorthand, store "X means Y", update people/projects/terms/preferences | `references/memory.md` |
| Tasks | Add/list/complete/triage tasks, create or edit `TASKS.md` | `references/tasks.md` |
| Routine refresh | Run update, sync tasks, find memory gaps, clean stale context | `references/update.md` |
| Deep scan | Run comprehensive update, scan connected chat/email/calendar/docs/project tools | `references/comprehensive-scan.md` and `references/connectors.md` |
| Connectors | User asks which tools can feed tasks or memory | `references/connectors.md` |

If the request spans multiple scenarios, load the smallest useful set of
references. For example, adding a task that contains an unknown project usually
needs `references/tasks.md` and `references/memory.md`, not the full update
workflow.

## Core Principles

- Treat `MEMORY.md` as a hot cache, not a full database. Keep it compact enough
  to read quickly at the start of a session.
- Use `memory/` for durable detail that can grow over time.
- Use `TASKS.md` for commitments and current work that both the user and agent
  can edit.
- Ask before adding tasks or inferred memories unless the user explicitly says
  to remember or record something.
- Preserve user-authored content. When updating existing files, merge instead
  of replacing.
- Mark uncertain facts as "Needs confirmation" rather than guessing.
- Avoid secrets. If a source contains credentials or sensitive tokens, store
  only safe pointers and handling notes.

## Default File Policy

Use the current working directory as the workspace root unless the user gives a
different path. Before editing:

1. Check whether `MEMORY.md`, `memory/`, and `TASKS.md` already exist.
2. Read existing files before changing them.
3. Keep unrelated files untouched.
4. Report what changed and what still needs user confirmation.
