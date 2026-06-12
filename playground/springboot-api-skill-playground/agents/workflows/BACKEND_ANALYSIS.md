# Backend Analysis Workflow

Use this workflow for backend onboarding, review, API-impact analysis, or planning changes that touch more than one surface.

## Load Order
1. `AGENTS.md`
2. `agents/REFERENCES.md`
3. `agents/PROJECT_PROFILE.md`
4. `agents/BACKEND_SURFACES.md`
5. `agents/CALL_CHAINS.md`
6. `agents/BUILD_AND_TEST.md`
7. A focused technical/business reference from `agents/references/` when that context matters.
8. A focused subagent file from `agents/subagents/` when the tool supports subagents.

## Dispatch Plan
For full analysis, run these specialist checks. Parallelize when the current agent tool supports it and the user explicitly asked for parallel work.

| Specialist | Reads first | Typical questions |
| --- | --- | --- |
| Endpoint | `agents/subagents/endpoint-specialist.md` | What routes exist? Are request/response/status/error contracts covered? |
| Service | `agents/subagents/service-specialist.md` | What invariants and state changes are enforced? Where can errors leak? |
| Persistence | `agents/subagents/persistence-specialist.md` | Do entities, repositories, migrations, and profile DB settings align? |
| Pub/Sub | `agents/subagents/pubsub-specialist.md` | Which events publish? Are topics, payloads, and failure behavior clear? |
| Integration | `agents/subagents/integration-specialist.md` | Which external calls exist and what runtime config do they need? |
| Test | `agents/subagents/test-specialist.md` | Which behavior is covered and which verification command should run? |
| Maven runner | `agents/subagents/maven-runner.md` | Which approved Maven commands should execute, and what did they report? |

## Merge Rules
- Prefer source code over generated evidence when they disagree.
- Treat `agents/PROJECT_EVIDENCE.md`, `agents/BACKEND_SURFACES.md`, and `agents/CALL_CHAINS.md` as reading guides, not final truth.
- Use references to choose source files; do not stop at references when concrete API/model/service behavior matters.
- Separate confirmed findings from assumptions.
- Keep final recommendations tied to one or more verification commands from `agents/BUILD_AND_TEST.md`.
- Delegate Maven command execution to Maven Runner when verification should actually run.
- Do not add new analysis tooling in this playground experiment.

## Example Prompts

Codex:

The main/default Codex thread is the coordinator. Spawn the project-scoped custom agents from `.codex/agents/` only for specialist analysis or domain-scoped implementation.

```text
Use parallel subagents to analyze this backend. Spawn endpoint_specialist, service_specialist, persistence_specialist, pubsub_specialist, integration_specialist, and test_specialist. Use maven_runner only for approved Maven verification commands. Wait for all results, then merge findings by severity with file references and verification commands.
```

OpenCode:

```text
Use @endpoint-specialist, @service-specialist, @persistence-specialist, @pubsub-specialist, @integration-specialist, and @test-specialist to analyze this backend. Use @maven-runner only for approved Maven verification commands. Merge their outputs using agents/SUBAGENTS.md.
```

VS Code Copilot Chat:

```text
/backend-analysis
Analyze this Spring Boot backend with the custom agents in .github/agents. Use the standard specialist output schema and cite files.
```

## Final Coordinator Output
Return:

```text
Summary:
- 2-4 bullets on the backend shape and important risks.

Findings:
- Severity, title, evidence, impact, next step.

Cross-surface map:
- Endpoint -> service -> repository/pubsub/config/test links that matter.

Verification:
- Commands run or recommended.

Open questions:
- Facts that need a human, environment, or runtime confirmation.
```
