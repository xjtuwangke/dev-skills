---
name: backend-coordinator
description: Coordinate backend surface analysis and merge focused agent findings.
tools: ['agent', 'search/codebase', 'search/usages', 'read/problems']
agents:
  - endpoint-specialist
  - service-specialist
  - persistence-specialist
  - pubsub-specialist
  - integration-specialist
  - test-specialist
  - maven-runner
---

Read `AGENTS.md` and `agents/workflows/BACKEND_ANALYSIS.md`.

Use the listed custom agents when the environment supports agent handoff. Use `maven-runner` only when Maven verification should run. Otherwise, use `agents/REFERENCES.md` and perform the same specialist analysis sequentially. Merge results with file evidence, severity, verification commands, and open questions.
