---
name: init-project
description: Initialize a code project for agentic coding by creating AGENTS.md and related agents reference files. Use this skill whenever the user asks to initialize, bootstrap, prepare, onboard, document, or set up a code repository/project for Codex/Claude/agents, especially requests mentioning AGENTS.md, agent references, project conventions, Java, Maven, Spring Boot 3, WebFlux, Karate, API tests, AT projects, or Chinese requests such as "初始化项目", "创建 AGENTS.md", "生成 agents 参考文件", "让 agent 熟悉这个项目". The skill can use explicitly named templates or scan the project to select multiple matching template facets, and it loads each template detail progressively only after that facet matches.
---

# Init Project

Initialize an existing code project so future agents can work in it with less repeated discovery. The output is a root `AGENTS.md` plus supporting files under `agents/` that capture project facts, build/test commands, conventions, and template-specific guidance.

The skill supports two selection modes:

- User-specified templates: the user names one or more facets such as "Maven Java", "Spring Boot 3 WebFlux", or "Karate AT".
- Auto-detected templates: inspect the project and load each matching template facet only after detection.

## Core Principle

Create durable project memory, not generic documentation. The files should tell future agents what is true in this repository, how to verify changes, and where to find the important code. Avoid filling `AGENTS.md` with boilerplate that could apply to any project.

Use progressive disclosure: read the general workflow first, inspect the project, select matching template facets, then read only the `references/templates/{name}/index.md` files for those facets.

## Supported Templates

| Template id | When to use | Reference file |
| --- | --- | --- |
| `baseline` | Every initialized project; general coding-agent rules | `references/templates/baseline/index.md` |
| `maven-java` | Any Java project built with Maven | `references/templates/maven-java/index.md` |
| `springboot3-webflux` | Spring Boot 3 service using reactive WebFlux/Reactor | `references/templates/springboot3-webflux/index.md` |
| `karate-at` | Acceptance-test or API-test project using Karate feature files/runners | `references/templates/karate-at/index.md` |

Projects can match multiple templates. `baseline` applies to every project. For example, a Spring Boot 3 WebFlux service usually matches `baseline`, `maven-java`, and `springboot3-webflux`; a dedicated Karate Maven repo usually matches `baseline`, `maven-java`, and `karate-at`; a service repo with Karate tests may match all four.

If only `baseline` matches, create a conservative generic `AGENTS.md` and explain that no specialized stack template was applied. Do not load stack templates "just in case".

## Inputs

Resolve these before editing:

- Target project path. If omitted, use the current working directory only when it is clearly the project root.
- Optional template ids or stack description.
- Optional user preferences: output language, team conventions, commands, package boundaries, CI command, or files to avoid touching.

Ask only when a wrong assumption could create misleading project guidance. If the root is obvious and a template is detected with strong signals, proceed.

## Workflow

### 1. Inspect The Project Root

Start with low-cost discovery:

```bash
pwd
rg --files -g 'pom.xml' -g 'build.gradle*' -g 'settings.gradle*' -g '*.java' -g '*.feature' -g 'README*' -g '.github/**' -g 'Jenkinsfile' -g 'Dockerfile' | head -200
git status --short
```

Read only the files needed to classify the project and capture facts:

- Build files: `pom.xml`, Maven wrapper files, parent pom, module poms.
- README or existing docs when concise.
- CI files only if they define authoritative build/test commands.
- Representative source/test folders, not every file.

Respect any dirty worktree. Do not revert or overwrite unrelated user changes.

### 2. Detect Or Confirm Matching Templates

If the user specified templates, normalize them to supported template ids and verify the project has at least minimal matching signals for each requested facet.

If the user did not specify templates, run the detector when available:

```bash
python3 /path/to/init-project/scripts/detect_project.py /path/to/project
```

Use the detector output as a starting point, then sanity-check the evidence by reading the relevant files. The detector is intentionally conservative; your judgment should include project-specific clues.

Detection signals:

- `maven-java`: `pom.xml`, Java sources, Maven wrapper, Maven modules, Java version properties.
- `springboot3-webflux`: Spring Boot 3 parent/dependencies/properties, `spring-boot-starter-webflux`, Reactor usage, application entrypoint, `application*.yml`.
- `karate-at`: Karate dependencies, `.feature` files, Karate runners, `karate-config.js`, API-test naming, environment config.
- `baseline`: every project.

When multiple templates match, keep all meaningful facets but identify the repository's primary purpose:

- Application service repository with some Karate tests: primary purpose `springboot3-webflux`, plus `baseline`, `maven-java`, and possibly `karate-at`.
- Dedicated acceptance-test repository targeting external services: primary purpose `karate-at`, plus `baseline` and `maven-java`.

### 3. Load Only Matching Template References

After selecting templates, read only the matching files:

- `references/templates/maven-java/index.md`
- `references/templates/springboot3-webflux/index.md`
- `references/templates/karate-at/index.md`
- `references/templates/baseline/index.md`

Load `baseline` first, then broad/common stack templates, then the more specific facets. For example, load `baseline`, then `maven-java`, then `springboot3-webflux`. Do not read unmatched stack template files.

For Spring Boot backend projects where the user asks for richer architecture
guidance, endpoint catalogs, persistence/service/client/pubsub surfaces, or
request/event call chains, also read
`references/springboot-backend-agent-docs.zh.md`. Keep this as progressive
disclosure: do not load it for plain Maven Java or Karate-only repositories.

Template-specific scripts live under `scripts/templates/{template-id}/`. Use them only after that template facet matches or the user explicitly requests that facet. For example, after `maven-java` matches, use:

```bash
python3 /path/to/init-project/scripts/templates/maven-java/inspect_maven_project.py /path/to/project
```

Keep template inspectors modular. When a template needs more extraction depth,
split logic by technology point under that template's script directory instead
of building one large Python file. For Spring Boot WebFlux, the top-level
`inspect_springboot_webflux.py` should orchestrate focused modules such as
endpoint, service, persistence, config, pub/sub, tests, and Java summary
inspectors.

If dependency analysis is relevant, the `maven-java` template also provides:

```bash
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project
```

Do not use a generic document renderer. Use Python only for detection and
evidence extraction. The LLM should create or merge `AGENTS.md` and `agents/*`
directly from:

- matched template reference files,
- inspector JSON output,
- existing project docs,
- representative source/config/test files.

Write concise project-specific docs. Do not generate raw evidence dumps by
default; keep only compact source pointers in the focused cards. Mark
unsupported guesses as "Needs confirmation".

For Spring Boot backend projects, use reference-first progressive disclosure by
default. `AGENTS.md` should route future agents to `agents/technical.md` for
technical work and to `agents/business/` for behavior semantics.
`agents/technical.md` is the next-level technical directory page: it should
contain common Maven commands, Checkstyle usage, coding standards, and links to
focused cards under `agents/technical/`. Use subagents, tool wrappers, call
chain maps, or evidence-heavy files only when the user explicitly asks or the
project risk clearly justifies the maintenance cost.

### 4. Create Or Update Agent Files

Default output layout:

```text
AGENTS.md
agents/
  technical.md          # technical directory page plus common commands/style
  technical/
    endpoints.md        # when an API surface exists
    services.md         # when service/application logic exists
    persistence.md      # when repositories/entities/migrations exist
    clients.md          # when outbound HTTP/WebClient calls exist
    integrations.md     # when external systems exist
    pubsub.md           # when messaging exists
    testing.md
  business/
    *.md                # only when behavior semantics are worth preserving
```

`AGENTS.md` should be the entry point. Keep it to project one-sentence
positioning and a `Where To Look` table. Put commands, conventions, validation
rules, best practices, and verification detail into `agents/technical.md` or
focused technical/business cards.

If files already exist:

1. Read them first.
2. Preserve project-specific guidance and user-authored notes.
3. Merge rather than replace unless the user explicitly asks for regeneration.
4. Mark uncertain facts as "Needs confirmation" instead of pretending certainty.

### 5. What To Capture

Capture facts future agents need before editing code:

- Project type, matched templates, and primary purpose.
- Main modules, packages, and source roots.
- Build, test, formatting, and local run commands.
- Required Java/Maven versions when discoverable.
- Important configs and environment variables.
- Testing strategy and where to add tests.
- Code conventions that are visible in the repository.
- Risk areas: generated files, contracts, snapshots, fixtures, shared test utilities, or fragile integration points.
- Verification checklist for common changes.

Avoid secrets. If config files contain credentials or tokens, mention only the file path and safe handling guidance.

### 6. Recommended File Roles

Use these roles unless the existing project suggests a better structure:

`AGENTS.md`
: Short orientation for all future agents. Include only one-sentence project
  positioning and a `Where To Look` table that routes to `agents/technical.md`
  and domain/business cards.

`agents/technical.md`
: Technical directory page for the next level of progressive disclosure.
  Include common Maven commands, `mvn checkstyle:check`, Checkstyle config and
  report paths, low-context Maven log handling, and coding standards inferred
  from nearby code.

`agents/technical/*.md`
: Focused technical context by surface, such as endpoints, services,
  persistence, clients, Pub/Sub, integrations, and testing. Each focused
  technical card should include a `Best Practices` section with a compact
  code, config, SQL, shell, or test demo that shows the recommended local
  pattern.

`agents/business/*.md`
: Business/domain context separated from technical structure. Generate only
  useful domain cards. Mark policy facts as "Needs confirmation" unless code,
  tests, OpenAPI, product docs, or the user confirm them. After code-changing
  evals or feature work, update affected business cards so future zero-context
  agents are not guided by stale domain language.

Default verification posture:

- Maven output must be low-context by default. Maven references
  should tell agents to prefer `-B -ntp`, redirect full stdout/stderr to
  `target/agent-maven-logs/`, and return only pass/fail, test counts, first
  actionable failures, Checkstyle/Jacoco failures, report paths, and next
  commands.
- After an agent changes source, update the affected focused cards when public
  APIs, persistence fields, business rules, or event payloads changed.

### 7. Verification

After writing files:

1. Re-read the created files.
2. Check that every command is either verified from project files or marked as inferred.
3. Run a lightweight validation when safe, using the generated low-context
   Maven protocol when Maven is involved, such as `mvn -B -ntp -DskipTests
   test > target/agent-maven-logs/skip-tests.log 2>&1` only if it is
   appropriate for the project and not obviously expensive.
4. At minimum, run:

```bash
find . -maxdepth 2 -name 'AGENTS.md' -o -path './agents/*.md'
```

Report what was created, which templates matched, which purpose you treated as primary, and any commands you did not run.

For skill development or regression checks, run the bundled self-validation:

```bash
python3 /path/to/init-project/scripts/validate_skill.py
```

It creates temporary Maven, Spring Boot WebFlux, and Karate projects, then verifies detection, template inspectors, Maven POM inspection, dependency exclusions, and dependency-tree JSON generation with a fake Maven executable.

## Output Quality Bar

A good initialization lets a future agent start a task by reading `AGENTS.md`, then only the relevant files under `agents/`. It should be specific enough to prevent repeated rediscovery, cautious enough not to encode guesses as facts, and compact enough that future agents will actually read it.
