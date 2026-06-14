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
```

The `init-project/evals/fixtures/springboot-commerce-webflux` fixture is a
realistic Spring WebFlux business service used to verify expected generated
agent documentation.

## Development Check

Before committing:

```bash
python3 init-project/scripts/validate_skill.py
python3 -m json.tool manage-memory/evals/evals.json >/dev/null
git diff --check
```
