# Subagents

This project uses reusable references, neutral subagent protocols, and thin tool-specific wrappers. Keep project context in `agents/references/`; keep role behavior in `agents/subagents/`; wrappers should only point back to these files.

## Supported Surfaces
| Tool | Native wrapper location | Notes |
| --- | --- | --- |
| Codex | `.codex/agents/*.toml` | Project-scoped custom agents. The main Codex thread should coordinate parallel specialist agents. |
| OpenCode | `.opencode/agents/*.md` | Markdown agents can be invoked by name or by automatic subagent routing. |
| VS Code Copilot Chat | `.github/agents/*.agent.md` | Custom agents and prompt files are used when the VS Code build supports them. |

## When To Use
- Use subagents for backend analysis, review, onboarding, risky refactors, cross-surface change planning, or domain-scoped implementation.
- Do not spawn subagents for tiny edits where one file and one test are enough.
- Specialist names describe ownership, not permission. A specialist may edit only when the parent task asks for implementation and the active wrapper permits edits.
- The coordinator owns final decisions, cross-surface tradeoffs, and merge conflict resolution.
- The Maven Runner is the only subagent intended to run build/test commands. It must not edit files.
- When Maven Runner is unavailable, the coordinator may run Maven directly, but must redirect full logs to `target/agent-maven-logs/` and return only summarized output.
- This playground experiment avoids additional inspector tools. Agents should use repository files, code search, and existing build/test commands only.
- For this experiment, parent sessions should not enable extra MCP, web, LSP, skill, or generated analyzer tools for specialist agents unless the user explicitly asks.

## Roles
| Role | Neutral file | Primary focus |
| --- | --- | --- |
| Endpoint Specialist | `agents/subagents/endpoint-specialist.md` | HTTP routes, request/response models, validation, OpenAPI annotations, WebFlux behavior. |
| Service Specialist | `agents/subagents/service-specialist.md` | Service invariants, state transitions, error behavior, transaction boundaries. |
| Persistence Specialist | `agents/subagents/persistence-specialist.md` | JPA entities, repositories, Flyway migrations, Postgres/profile config. |
| Pub/Sub Specialist | `agents/subagents/pubsub-specialist.md` | GCP Pub/Sub publisher/gateway behavior, topic config, payload contracts. |
| Integration Specialist | `agents/subagents/integration-specialist.md` | External system calls, clients, timeouts, retries, profile-sensitive integration config. |
| Test Specialist | `agents/subagents/test-specialist.md` | JUnit 5, Mockito, Reactor/WebTestClient tests, JaCoCo and Checkstyle gates. |
| Maven Runner | `agents/subagents/maven-runner.md` | Execute approved Maven verification commands and summarize results. |

## Coordinator Protocol
1. Read `AGENTS.md`, then load only the evidence files needed for the task.
2. For whole-backend analysis, read `agents/workflows/BACKEND_ANALYSIS.md`.
3. Use `agents/REFERENCES.md` to select technical and business context.
4. Dispatch specialist roles in parallel when the tool supports it and the user asked for parallel work.
5. After reading references, inspect the relevant source files listed in the reference `Source Areas` before giving confidence above medium.
6. Require every specialist result to cite concrete files and call out unknowns.
7. Merge duplicate findings, resolve conflicts against source code, and map findings to verification commands.

## Standard Specialist Output
Each specialist agent should return:

```text
Scope:
- What was inspected and what was intentionally skipped.

Files read:
- path/to/File.java

Findings:
- [severity] Finding title
  Evidence: file path and symbol or config key.
  Impact: user-visible or maintenance risk.
  Suggested next step: concrete change or verification.

Cross-surface notes:
- Dependencies on endpoints, service logic, persistence, Pub/Sub, config, or tests.

Unknowns:
- Runtime behavior, environment facts, or contracts that need confirmation.

Confidence:
- high | medium | low, with one short reason.
```

Use `No findings` when the inspected surface looks consistent.

## Standard Maven Runner Output
The Maven Runner should return:

```text
Commands:
- mvn ...
- Full log: target/agent-maven-logs/<name>.log

Result:
- pass | fail | blocked

Important output:
- Short excerpts only: test counts, failing test names, Checkstyle files, coverage rule failures, or build lifecycle error.

Artifacts:
- Generated report paths such as target/site/jacoco/index.html, when relevant.

Next step:
- The smallest useful follow-up command or the owner surface that should inspect the failure.
```
