---
description: Analyze the backend with focused specialist agents and merge findings.
agent: backend-coordinator
---

Read `AGENTS.md`, then follow `agents/workflows/BACKEND_ANALYSIS.md`.

Use the custom agents in `.github/agents/` when available:
- `endpoint-specialist`
- `service-specialist`
- `persistence-specialist`
- `pubsub-specialist`
- `integration-specialist`
- `test-specialist`
- `maven-runner` only when Maven verification should run

Return the final coordinator output with file references and verification commands.
