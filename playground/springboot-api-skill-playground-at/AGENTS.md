# AGENTS.md

## Project
- Name: `springboot-api-skill-playground-at`
- Primary purpose: Karate acceptance-test project for `../springboot-api-skill-playground`
- Template facets: `baseline`, `maven-java`, `karate-at`
- Build system: Maven
- Java version: 17 via `maven.compiler.release`

## Start Here
- Project profile: `agents/PROJECT_PROFILE.md`
- Evidence snapshot: `agents/PROJECT_EVIDENCE.md`
- Build and test commands: `agents/BUILD_AND_TEST.md`
- Code style: `agents/CODE_STYLE.md`
- Architecture notes: `agents/ARCHITECTURE_NOTES.md`
- Dependency notes: `agents/DEPENDENCIES.md`
- Template notes: `agents/TEMPLATE_NOTES.md`

## Working Rules
- Treat this project as a black-box AT suite; do not import demo service production classes.
- Keep feature files behavior-focused and reuse payload fixtures from `src/test/resources/payloads/`.
- Preserve tag semantics: `@smoke`, `@orders`, `@retail`, and `@errors`.
- Do not hard-code environment hostnames, credentials, or tokens in feature files.
- Keep default Maven verification service-safe; hosted Karate runs must require `-Dat.enabled=true`.
- When running Maven directly, use `-B -ntp` and redirect noisy logs to `target/agent-maven-logs/` when output may be long.

## Fast Commands
- Compile without calling the service: `mvn -B -ntp -DskipTests test`
- Run all ATs against local service: `mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080`
- Run smoke ATs: `mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080 -Dkarate.tags=@smoke`

## Verification Checklist
- [ ] The demo service target and base URL were confirmed before hosted AT execution.
- [ ] Feature tags and payload fixtures stayed aligned.
- [ ] Maven compile or hosted AT command was run, or skipped with a reason.
- [ ] Generated reports under `target/` were not committed.
