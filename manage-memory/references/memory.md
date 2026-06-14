# Memory System

Use this reference for decoding shorthand, recalling stored context, and adding
or reorganizing memory.

## Architecture

```text
MEMORY.md          # hot cache for daily decoding
memory/
  glossary.md      # full decoder ring
  people/          # full person profiles
  projects/        # project details
  context/         # company, team, tools, process notes
```

`MEMORY.md` should cover common daily needs. `memory/` stores detail and history.

## MEMORY.md Format

Keep `MEMORY.md` short, usually 50-100 lines.

```markdown
# Memory

## Me
[Name], [Role] on [Team]. [One sentence about current work.]

## People
| Who | Role |
| --- | --- |
| **Todd** | Todd Martinez, Finance lead |
| **Sarah** | Sarah Chen, Platform engineering |

See also: `memory/glossary.md` and `memory/people/`.

## Terms
| Term | Meaning |
| --- | --- |
| PSR | Pipeline Status Report |
| P0 | Drop-everything priority |

See also: `memory/glossary.md`.

## Projects
| Name | What |
| --- | --- |
| **Phoenix** | Database migration, active Q2 work |

See also: `memory/projects/`.

## Preferences
- Async-first when possible
- Prefer concise summaries with concrete next steps
```

## Deep Memory Formats

`memory/glossary.md` is the full decoder ring:

```markdown
# Glossary

## Acronyms
| Term | Meaning | Context |
| --- | --- | --- |
| PSR | Pipeline Status Report | Weekly sales or pipeline document |

## Internal Terms
| Term | Meaning |
| --- | --- |
| ship review | Release approval meeting |

## Nicknames
| Nickname | Person |
| --- | --- |
| Todd | Todd Martinez |

## Project Codenames
| Codename | Project |
| --- | --- |
| Phoenix | Database migration |
```

Use `memory/people/{name}.md` for person profiles:

```markdown
# Todd Martinez

**Also known as:** Todd, T
**Role:** Finance Lead

## Communication
- Prefers Slack DM
- Direct, concise updates work best

## Context
- Owns PSR preparation and finance reporting
```

Use `memory/projects/{name}.md` for project profiles:

```markdown
# Project Phoenix

**Also called:** Phoenix, the migration
**Status:** Active

## What It Is
Database migration from a legacy system to PostgreSQL.

## Key People
- Sarah Chen, technical lead
- Todd Martinez, budget owner
```

Use `memory/context/company.md` for durable organizational context.

## Naming Conventions

Use lowercase kebab-case filenames for deep memory:

- People: `memory/people/todd-martinez.md`
- Projects: `memory/projects/project-phoenix.md`
- Context: `memory/context/company.md`, `memory/context/tools.md`

Prefer stable full names for people when known. Preserve nicknames, initials,
team shorthand, and alternate project names inside the file body and
`memory/glossary.md`.

## Lookup Flow

When the user uses shorthand:

1. Check `MEMORY.md`.
2. If not found, check `memory/glossary.md`.
3. If richer detail is needed, read the relevant file under `memory/people/`,
   `memory/projects/`, or `memory/context/`.
4. If still unknown, ask the user what it means and offer to remember it.

Example:

```text
User: ask todd about the PSR for Phoenix
Lookup:
- Todd -> Todd Martinez, Finance lead
- PSR -> Pipeline Status Report
- Phoenix -> active database migration project
```

## Adding Memory

When the user says "remember this", "X means Y", or equivalent:

- Acronyms, shorthand, and internal terms go to `memory/glossary.md`.
- People go to `memory/people/{person}.md` and the glossary nickname table.
- Projects go to `memory/projects/{project}.md` and the glossary codename table.
- User preferences go to `MEMORY.md`.
- Frequently used people, terms, and active projects should also be promoted to
  `MEMORY.md`.

If the user is only speculating, store the note with "Needs confirmation" or ask
before writing.

## Promotion And Demotion

Promote information to `MEMORY.md` when:

- It is used frequently.
- It is part of active work.
- It helps decode common shorthand.

Demote information to `memory/` only when:

- A project is completed.
- A person is no longer a frequent contact.
- A term is rare or historical.

This keeps `MEMORY.md` useful without turning it into a long archive.
