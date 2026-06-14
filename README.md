# dev-skills

Coding and repository-operation skills for agentic development workflows.

This repository is the development-focused split from the old mixed `skills`
repository. Its skills should help agents understand codebases, initialize
project memory, inspect build systems, document architecture, and verify
changes.

## Skills

| Skill | Purpose | Status |
| --- | --- | --- |
| `init-project` | Initialize an existing code project by generating `AGENTS.md` and supporting `agents/*.md` reference files | active |
| `manage-memory` | Manage workspace memory and task tracking with `MEMORY.md`, `memory/`, and `TASKS.md` | draft |
| `draft-diagrams` | Draft, add, and modify Markdown-native Mermaid technical design diagrams and PlantUML ASCII diagrams with progressive references by diagram type | draft |
| `design-arch` | Create and review ADRs, architecture decisions, and trade-off analysis | draft |
| `design-tech` | Create and review technical design documents for systems, services, APIs, workflows, and implementation plans | draft |

## init-project

`init-project` creates durable project memory for future coding agents. It can
scan a target project, detect matching templates, and guide the LLM to create a
concise root `AGENTS.md` plus supporting reference files from template guidance
and structured evidence.

Supported template facets:

- `baseline`: general coding-agent project rules.
- `maven-java`: Java projects built with Maven.
- `springboot3-webflux`: Spring Boot WebFlux/Reactor services.
- `karate-at`: Karate API/acceptance-test projects.

The skill uses progressive disclosure: it loads the common workflow first, then
only reads template references and scripts after a project facet is detected or
explicitly requested.

## manage-memory

`manage-memory` consolidates a workspace memory system and a Markdown task list
into one skill. It uses progressive disclosure: the root `SKILL.md` routes the
agent to scenario-specific references for initialization, memory lookup/update,
task management, routine refresh, comprehensive scans, and connector usage.

This skill is sourced from and adapted from Anthropic's
[`knowledge-work-plugins`](https://github.com/anthropics/knowledge-work-plugins)
productivity skills: `memory-management`, `start`, `update`, and
`task-management`. The local version changes the hot-cache file from
`CLAUDE.md` to `MEMORY.md` and merges the four workflows into one skill with
progressively loaded reference files.

## draft-diagrams

`draft-diagrams` drafts, adds, and modifies technical design diagrams as
editable text source. It defaults to Mermaid for Markdown-native diagrams and
uses PlantUML text mode for ASCII or Unicode terminal-friendly diagrams. The
skill uses progressive disclosure by loading only the reference for the
requested diagram family: flowchart, sequence, UML class, ERD,
architecture/C4, state, PlantUML ASCII, or rendering/export guidance.

This skill is sourced from and adapted from
[`softaworks/agent-toolkit@mermaid-diagrams`](https://skills.sh/softaworks/agent-toolkit/mermaid-diagrams)
and
[`github/awesome-copilot@plantuml-ascii`](https://skills.sh/github/awesome-copilot/plantuml-ascii).
See `draft-diagrams/README.md` for source attribution details.

## design-arch

`design-arch` creates, reviews, and refines architecture decision records
(ADRs). It focuses on architecture choices, option comparison, trade-offs,
consequences, risks, and follow-up actions.

This skill is sourced from and adapted from Anthropic's
[`knowledge-work-plugins`](https://github.com/anthropics/knowledge-work-plugins)
`architecture` skill. The local version renames the skill to `design-arch` and
adds progressive references for ADR creation, architecture review, trade-off
analysis, and connector-aware context gathering.

## design-tech

`design-tech` creates, reviews, and refines technical design documents for
systems, services, APIs, workflows, migrations, and implementation plans. It
covers system structure, behavior and flows, APIs, data models, testing,
observability, rollout, and rollback.

This skill is sourced from and adapted from Anthropic's
[`knowledge-work-plugins`](https://github.com/anthropics/knowledge-work-plugins)
`system-design` skill. The local version renames the skill to `design-tech` and
expands it into a technical-design workflow with progressive references for
system design, behavior flows, implementation planning, and design review.

## Useful Commands

Validate the skill:

```bash
python3 init-project/scripts/validate_skill.py
```

Detect a target project:

```bash
python3 init-project/scripts/detect_project.py /path/to/project
```

Inspect a Maven project:

```bash
python3 init-project/scripts/templates/maven-java/inspect_maven_project.py /path/to/project
```

Generate a Maven dependency tree report:

```bash
python3 init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project
```

## Repository Layout

```text
init-project/
  SKILL.md
  evals/
  references/
  scripts/
manage-memory/
  SKILL.md
  evals/
  references/
draft-diagrams/
  SKILL.md
  README.md
  evals/
  references/
design-arch/
  SKILL.md
  evals/
  references/
design-tech/
  SKILL.md
  evals/
  references/
```

The `init-project/evals/fixtures/springboot-commerce-webflux` fixture is a
realistic Spring WebFlux business service used to verify expected generated
agent documentation.

## Development Check

Before committing:

```bash
python3 init-project/scripts/validate_skill.py
python3 -m json.tool manage-memory/evals/evals.json >/dev/null
python3 -m json.tool draft-diagrams/evals/evals.json >/dev/null
python3 -m json.tool design-arch/evals/evals.json >/dev/null
python3 -m json.tool design-tech/evals/evals.json >/dev/null
git diff --check
```
