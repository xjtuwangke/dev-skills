# Maven Java Template

Use this template when the project is Java built with Maven. It is a common foundation template and can be combined with more specific templates such as `springboot3-webflux` or `karate-at`.

## Detection Checklist

Strong signals:

- `pom.xml` exists at the project root or in modules.
- Java sources exist under `src/main/java` or `src/test/java`.
- Maven wrapper files exist: `mvnw`, `mvnw.cmd`, `.mvn/wrapper/`.

Supporting signals:

- `java.version`, `maven.compiler.release`, or compiler plugin configuration in `pom.xml`.
- Multi-module Maven layout with `<modules>`.
- CI invokes `mvn` or `./mvnw`.

## Files To Inspect

```text
pom.xml
mvnw
.mvn/wrapper/
README.md
src/main/java/
src/test/java/
.github/workflows/
Jenkinsfile
```

For multi-module repos, inspect the root pom and only the module poms relevant to the user's task or project role.

## Template Scripts

Use the Maven inspector after `maven-java` matches and before writing project docs:

```bash
python3 /path/to/init-project/scripts/templates/maven-java/inspect_maven_project.py /path/to/project
```

The script first checks whether the target root is a Maven project. If root `pom.xml` exists, it emits JSON containing:

- Maven wrapper presence.
- Root POM coordinates, parent, packaging, properties, modules, dependencies, dependency management, plugins, and profiles.
- Recursive module POM summaries for multi-module projects.
- Java version hints from common Maven properties or compiler plugin configuration.

Use this JSON as structured evidence for `agents/technical.md` and focused
technical cards such as `agents/technical/dependencies.md` when dependency
detail is worth preserving. If `is_maven_project` is false, do not force the
`maven-java` template unless the user explicitly identifies another root.

When dependency analysis matters, generate a dependency tree:

```bash
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project
```

The script uses the Maven Dependency Plugin `dependency:tree` goal with `outputType=json`, which is supported by plugin version 3.7.0+; the script defaults to `org.apache.maven.plugins:maven-dependency-plugin:3.11.0:tree` so JSON output is available even when the project does not pin a newer plugin. It emits a wrapper JSON containing one run per root/module, the Maven command used, the return code, stdout/stderr, filters, and the parsed dependency tree.

Useful filters:

```bash
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --scope test
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --includes org.springframework.boot
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --excludes org.slf4j
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --module service
python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --timeout 120
```

Use the dependency tree to document important transitive dependencies, conflict-prone libraries, logging bindings, security-sensitive dependencies, and places where exclusions explain why a dependency is or is not present.

## agents/technical/dependencies.md Content

Create `agents/technical/dependencies.md` only when dependency detail is useful
for future agents. Include:

- Coordinates for the root project and important modules.
- Java version hint and Maven wrapper status.
- BOMs and `dependencyManagement` imports.
- Direct dependencies grouped by scope.
- Important exclusions from direct dependencies.
- Dependency tree command used, filters, timeout, and whether it completed.
- Notable transitive dependencies: logging, HTTP clients, JSON/XML libraries, database drivers, test frameworks, security libraries.
- Known conflict-prone libraries or version-alignment rules.
- Guidance for adding dependencies: prefer existing BOM/version management, avoid unnecessary new dependencies, and explain exclusions.

If the dependency tree command times out or cannot resolve, still create the file with the direct POM evidence and mark dependency-tree findings as "Not verified".

## AGENTS.md Guidance

Root `AGENTS.md` should not carry Maven command detail. Keep only one-sentence
project positioning and `Where To Look`; put Maven/Java facts in
`agents/technical.md`.

```markdown
## Project
- [One sentence describing this Maven Java project and primary stack.]

## Where To Look

| Task | Start Here | Notes |
| --- | --- | --- |
| Technical change, review, build, or test | `agents/technical.md` | Maven commands, Java version, wrapper status, code style, and focused technical links. |
```

Prefer wrapper commands when `mvnw` exists. If no wrapper exists, use `mvn` and say no Maven wrapper was found.

## agents/technical.md Content

Capture:

- Root and module structure.
- Java version and Maven version requirements if discoverable.
- Source roots and test roots.
- Important build plugins, generated sources, annotation processors, or codegen steps.
- Local config files and CI files that define build behavior.

Use evidence language:

- "Verified from `pom.xml`"
- "Verified from `.github/workflows/build.yml`"
- "Inferred from source layout"
- "Needs confirmation"

## Maven Commands Content

Typical commands to adapt:

```bash
./mvnw clean verify
./mvnw test
./mvnw -Dtest=SomeTest test
./mvnw -DskipTests package
```

Document:

- Safe quick checks.
- Full verification commands.
- Module-specific commands for multi-module projects.
- Required environment variables or external services.
- Commands that are expensive, flaky, or CI-only.
- Low-context execution for agent-run Maven commands. Prefer `-B -ntp`, redirect
  full logs to `target/agent-maven-logs/`, and return only pass/fail, test
  counts, first actionable failures, Checkstyle/Jacoco failures, report paths,
  and next commands. This is required when no Maven Runner subagent is available.

Suggested no-subagent pattern:

```bash
mkdir -p target/agent-maven-logs
./mvnw -B -ntp clean verify > target/agent-maven-logs/clean-verify.log 2>&1
grep -E "Tests run:|BUILD SUCCESS|BUILD FAILURE|Total time|ERROR|FAILURE" target/agent-maven-logs/clean-verify.log | tail -40
```

If the command fails, inspect focused report files before reading the full log:

- `target/surefire-reports/*.txt`
- `target/checkstyle-result.xml`
- `target/site/jacoco/jacoco.xml`
- `tail -80 target/agent-maven-logs/clean-verify.log`

## Code Style Content

Infer style from existing code:

- Package naming.
- Class and test naming.
- Assertion library and mocking style.
- Logging style.
- Null handling and validation conventions.
- Formatter or Checkstyle/Spotless rules if configured.

Avoid inventing style rules. If style differs by module, tell future agents to follow the nearest edited package.
