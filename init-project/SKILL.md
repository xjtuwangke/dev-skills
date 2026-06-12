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

To create the first draft of all project agent docs after detection, use:

```bash
python3 /path/to/init-project/scripts/render_agents_docs.py /path/to/project
```

For user-specified templates, pass explicit facets:

```bash
python3 /path/to/init-project/scripts/render_agents_docs.py /path/to/project \
  --template maven-java \
  --template springboot3-webflux
```

The renderer writes conservative drafts for `AGENTS.md`, `agents/*.md`, focused reference files, and optional tool-specific subagent wrappers using detected or explicit facets and structured template inspection. It always includes `baseline`, skips existing files unless `--overwrite` is passed, and can accept comma-separated templates such as `--template maven-java,springboot3-webflux`. After rendering, read the created files and refine them with project-specific facts from the matching template references.

For Spring Boot backend projects, use reference-first progressive disclosure by
default. `AGENTS.md` should route future agents to `agents/REFERENCES.md` and
focused technical/business references. Use subagents only for broad, risky,
ambiguous, or cross-surface work where independent parallel review is worth the
extra elapsed time and token cost. Do not rely on `AGENTS.md` to configure
subagents for every tool; generate native thin wrappers for tools that support
them and keep reusable project context in `agents/references/`.

### 4. Create Or Update Agent Files

Default output layout:

```text
AGENTS.md
agents/
  REFERENCES.md
  PROJECT_PROFILE.md
  PROJECT_EVIDENCE.md
  BUILD_AND_TEST.md
  CODE_STYLE.md
  ARCHITECTURE_NOTES.md
  DEPENDENCIES.md
  TEMPLATE_NOTES.md
  references/
    technical/
    business/
```

`AGENTS.md` should be the entry point. Keep it concise and route detailed material into `agents/`.

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
: Short orientation for all future agents. Include matched template ids, primary project purpose, essential commands, where deeper docs live, and rules that apply to every change.

`agents/PROJECT_PROFILE.md`
: Repository map, module ownership, source/test roots, important configs, runtime assumptions.

`agents/PROJECT_EVIDENCE.md`
: Raw detection and inspection evidence used to generate the other files. Keep this file evidence-heavy so `AGENTS.md` can remain short.

`agents/BUILD_AND_TEST.md`
: Build commands, targeted test commands, common failure modes, CI parity notes.

`agents/CODE_STYLE.md`
: Local coding style inferred from the repo, naming conventions, error-handling style, logging style, test style.

`agents/ARCHITECTURE_NOTES.md`
: System boundaries, request/test flow, dependency patterns, extension points, known risks.

`agents/DEPENDENCIES.md`
: Dependency inventory and dependency-tree findings when the project has a package manager or dependency graph worth documenting. For Maven Java projects, include direct dependencies, important transitive dependencies, dependency management/BOMs, exclusions, logging bindings, security-sensitive libraries, and any dependency-tree command output path or summary.

`agents/TEMPLATE_NOTES.md`
: Template-specific guidance copied and adapted from every matched template reference. Group notes by template id so future agents can read only the relevant section.

`agents/REFERENCES.md`
: Index for progressive disclosure. It should route future agents to the
  smallest relevant technical reference and, only when behavior semantics
  matter, the matching business reference.

`agents/references/technical/`
: Focused technical context by surface, such as endpoints, services,
  persistence, Pub/Sub, integrations, testing, and Maven commands.

`agents/references/business/`
: Business/domain context separated from technical structure. For generated
  drafts, mark policy facts as "Needs confirmation" unless code, tests,
  OpenAPI, product docs, or the user confirm them.
  After code-changing evals or feature work, update affected business
  references so future zero-context agents are not guided by stale domain
  language.

For Spring Boot backend services, prefer adding these focused files when enough
evidence exists:

`agents/BACKEND_SURFACES.md`
: Endpoint, service, persistence, outbound client, pub/sub, config, and test
  catalogs generated from project evidence. For Maven Spring Boot API services,
  include environment profiles, Flyway migrations, JPA/Hibernate repositories
  and entities, SpringDoc/OpenAPI clues, Pub/Sub topic/config hints, and unit
  test locations when detected.

`agents/CALL_CHAINS.md`
: Request, event, scheduler, or message-entry chains with confidence labels and
  evidence sources, such as static scan, OpenAPI, actuator mappings, or runtime
  traces. Keep chains explicitly labeled as static/inferred unless they were
  verified from runtime mappings or traces.

`agents/SUBAGENTS.md`
: Neutral subagent protocol. It explains when subagents are worth using, the
  specialist output schema, coordinator merge rules, and Maven Runner behavior.

`agents/subagents/*.md`
: Neutral role files such as `endpoint-specialist.md`,
  `service-specialist.md`, `persistence-specialist.md`,
  `pubsub-specialist.md`, `integration-specialist.md`,
  `test-specialist.md`, and `maven-runner.md`. Specialist names indicate
  ownership, not permissions.

`agents/workflows/BACKEND_ANALYSIS.md`
: Whole-backend analysis workflow and example prompts for tools that support
  subagent handoff.

`.codex/agents/*.toml`, `.opencode/agents/*.md`, `.github/agents/*.agent.md`
: Thin native wrappers for Codex, OpenCode, and VS Code Copilot Chat. Wrappers
  should point back to neutral `agents/subagents/*.md` files and define tool
  permissions. Keep project facts out of wrappers.

Default specialist posture:

- `endpoint-specialist` may implement endpoint-layer changes when the parent
  task asks for implementation and the wrapper permits edits.
- Other generated specialists are read-first by default and may be made
  implementation-capable later by changing native wrappers intentionally.
- `maven-runner` is the only generated role intended to execute Maven
  verification commands. Other specialists recommend commands.
- Every specialist should inspect source files after reading references before
  giving confidence above medium.
- After a specialist or single agent changes source, update the affected
  focused references when public APIs, persistence fields, business rules, or
  event payloads changed.

### 7. Verification

After writing files:

1. Re-read the created files.
2. Check that every command is either verified from project files or marked as inferred.
3. Run a lightweight validation when safe, such as `mvn -q -DskipTests test` only if it is appropriate for the project and not obviously expensive.
4. At minimum, run:

```bash
find . -maxdepth 2 -name 'AGENTS.md' -o -path './agents/*.md'
```

Report what was created, which templates matched, which purpose you treated as primary, and any commands you did not run.

For skill development or regression checks, run the bundled self-validation:

```bash
python3 /path/to/init-project/scripts/validate_skill.py
```

It creates temporary Maven, Spring Boot WebFlux, and Karate projects, then verifies detection, explicit template rendering, generated documentation content, Maven POM inspection, dependency exclusions, and dependency-tree JSON generation with a fake Maven executable.

## Output Quality Bar

A good initialization lets a future agent start a task by reading `AGENTS.md`, then only the relevant files under `agents/`. It should be specific enough to prevent repeated rediscovery, cautious enough not to encode guesses as facts, and compact enough that future agents will actually read it.
