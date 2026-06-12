# AGENTS.md

## Project
- Name: springboot-api-skill-playground
- Primary purpose: springboot3-webflux-service
- Template facets: baseline, maven-java, springboot3-webflux
- Java version: 21

## Available Context
Do not read every file in this list up front. Start with this root file, then load only the context needed for the current task.

- Project profile: `agents/PROJECT_PROFILE.md`
- Evidence snapshot: `agents/PROJECT_EVIDENCE.md`
- Build and test commands: `agents/BUILD_AND_TEST.md`
- Code style: `agents/CODE_STYLE.md`
- Architecture notes: `agents/ARCHITECTURE_NOTES.md`
- Dependency notes: `agents/DEPENDENCIES.md`
- Template notes: `agents/TEMPLATE_NOTES.md`
- Backend surfaces: `agents/BACKEND_SURFACES.md`
- Call chains: `agents/CALL_CHAINS.md`
- Reference index: `agents/REFERENCES.md`
- Subagent protocol: `agents/SUBAGENTS.md`
- Backend analysis workflow: `agents/workflows/BACKEND_ANALYSIS.md`
- Evaluation notes: `agents/EVALUATION_NOTES.md`

## Agent Workflows
- Use the root file as the baseline only; load deeper files on demand.
- When the user asks for parallel analysis or subagents, use the specialist roles in `agents/subagents/`.
- Use `maven-runner` for Maven command execution; non-runner specialists should only recommend verification commands.
- When the current tool does not support subagents, use `agents/REFERENCES.md` for progressive disclosure instead.
- For Codex, project-scoped custom agents live in `.codex/agents/*.toml`.
- For OpenCode, wrappers live in `.opencode/agents/*.md`.
- For VS Code Copilot Chat, wrappers live in `.github/agents/*.agent.md` and prompts in `.github/prompts/`.
- If the current tool cannot spawn or invoke subagents, use `agents/REFERENCES.md` and run the same specialist checks sequentially.


## Baseline Working Rules
- Read existing code before editing; prefer local patterns over new abstractions.
- Keep changes scoped to the user request and avoid unrelated refactors.
- Preserve public APIs, data contracts, and migration behavior unless the task explicitly changes them.
- Add or update focused tests for behavior changes.
- Run the smallest useful verification command first, then broader checks when risk warrants it.
- Document any verification you could not run and why.
- Do not commit secrets, credentials, generated build output, or local machine state.
- Ask before adding new production dependencies or changing build/deploy behavior.

## Fast Commands
- Build: `mvn clean verify`
- Unit tests: `mvn test`
- Run locally: `mvn spring-boot:run`

## Verification Checklist
- [ ] Relevant files were inspected before editing.
- [ ] Existing conventions were followed or the deviation is explained.
- [ ] Tests/build/lint were run, or skipped with a reason.
- [ ] Security-sensitive changes were reviewed for input validation, auth, secrets, and unsafe I/O.
