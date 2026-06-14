# Start Workflow

Use this reference when the user wants to initialize memory, create the
workspace files, or run a start-style setup.

## Goal

Create the files needed for a workspace memory and task system:

```text
MEMORY.md
memory/
  glossary.md
  people/
  projects/
  context/
TASKS.md
```

## Workflow

### 1. Check Existing State

Inspect the current working directory for:

- `TASKS.md`
- `MEMORY.md`
- `memory/`

Read existing files before modifying them. If the workspace is not obvious, ask
which directory should own the memory files.

### 2. Create Missing Files

If `TASKS.md` is missing, read `references/tasks.md`, then create it using the
standard task template.

If `MEMORY.md` is missing, create a compact starter file:

```markdown
# Memory

## Me
Needs confirmation.

## People
| Who | Role |
| --- | --- |

## Terms
| Term | Meaning |
| --- | --- |

## Projects
| Name | What |
| --- | --- |

## Preferences
- Needs confirmation.
```

If `memory/` is missing, create:

```text
memory/glossary.md
memory/people/
memory/projects/
memory/context/
```

Initialize `memory/glossary.md` with sections for acronyms, internal terms,
nicknames, and project codenames.

### 3. Bootstrap From Existing Tasks

The user's real tasks are often the best source of shorthand.

Ask where their task list lives if no local `TASKS.md` exists or if it is empty.
Accept a local file, pasted notes, or a connected task source if available.

For each task, identify:

- Names that may be nicknames.
- Acronyms or abbreviations.
- Project references or codenames.
- Internal terms or team-specific jargon.

Ask targeted questions only for terms that are not already decoded.

Example:

```text
Task: Send PSR to Todd about Phoenix blockers.

I need context for:
1. PSR - What does this stand for?
2. Todd - Who is Todd?
3. Phoenix - What project or topic is this?
```

Before writing decoded people, terms, projects, or preferences, read
`references/memory.md` and use its placement and filename conventions.

### 4. Optional Deep Setup

Offer a comprehensive scan only if connected tools are available or the user can
provide exports/pasted context. If they want it, read
`references/comprehensive-scan.md` and `references/connectors.md`.

### 5. Report Results

End with a concise summary:

```text
Memory system ready:
- MEMORY.md: created/updated
- memory/: X people, X terms, X projects
- TASKS.md: X active tasks
- Needs confirmation: [...]
```
