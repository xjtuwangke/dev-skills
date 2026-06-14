# Update Workflow

Use this reference for routine refreshes: update memory, sync tasks, identify
unknown terms, and clean stale context.

## Modes

- Default update: read local files, triage tasks, fill memory gaps, and sync
  connected task sources when available.
- Comprehensive update: also scan recent chat, email, calendar, documents, and
  project tools. For this mode, read `references/comprehensive-scan.md`.

## Default Workflow

### 1. Load Current State

Read:

- `TASKS.md`
- `MEMORY.md`
- `memory/glossary.md`
- Relevant files under `memory/people/`, `memory/projects/`, or
  `memory/context/` when needed.

If the files do not exist, use `references/start.md` first.

If task edits are needed, read `references/tasks.md`. If memory edits are
needed, read `references/memory.md`.

### 2. Sync External Tasks When Available

If a project tracker or GitHub CLI is available, compare assigned open tasks to
`TASKS.md`.

Use fuzzy matching by title and context:

| External task | TASKS.md match | Suggested action |
| --- | --- | --- |
| Found externally, not local | No match | Offer to add |
| Found externally and local | Match | Skip or enrich local context |
| Local but not external | No match | Flag as potentially stale |
| Completed externally | Active locally | Offer to mark done |

Ask before making changes unless the user explicitly requested automatic sync.

### 3. Triage Stale Local Tasks

Review `Active` and `Waiting On` for:

- Due dates in the past.
- Items active for 30+ days.
- Tasks with no person, project, or next action.
- Waiting items without a "since" date.

Offer concrete options: mark done, reschedule, move to `Someday`, move to
`Waiting On`, or keep active.

### 4. Decode Tasks For Memory Gaps

For each active task, decode entities:

```text
Task: Send PSR to Todd about Phoenix blockers
- PSR -> Pipeline Status Report
- Todd -> Todd Martinez
- Phoenix -> unknown
```

Group unknown terms and ask concise questions. Add answers after reading
`references/memory.md`.

### 5. Enrich Existing Memory

Extract useful context from tasks:

- Links to project docs or tickets.
- New deadlines.
- Project status changes.
- Relationships between people, projects, and approvals.
- Alternate names and nicknames.

Promote frequent active items to `MEMORY.md`; demote stale items to `memory/`
only.

### 6. Report

Use a short summary:

```text
Update complete:
- Tasks: +3 added, 1 completed, 2 need triage
- Memory: 2 gaps filled, 1 project enriched
- Needs confirmation: [...]
```
