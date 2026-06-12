---
description: Coordinate backend surface analysis using focused specialist subagents.
mode: primary
temperature: 0.1
permission:
  read: allow
  list: allow
  glob: allow
  grep: allow
  task:
    "*": deny
    endpoint-specialist: allow
    service-specialist: allow
    persistence-specialist: allow
    pubsub-specialist: allow
    integration-specialist: allow
    test-specialist: allow
    maven-runner: allow
  edit: deny
  bash: deny
  external_directory: deny
  webfetch: deny
  websearch: deny
  lsp: deny
  skill: deny
---

Read `AGENTS.md` and `agents/workflows/BACKEND_ANALYSIS.md`.

When parallel analysis is useful, invoke the specialist agents and merge their outputs:
- `@endpoint-specialist`
- `@service-specialist`
- `@persistence-specialist`
- `@pubsub-specialist`
- `@integration-specialist`
- `@test-specialist`
- `@maven-runner` only when Maven verification should run

Use the final coordinator output from `agents/workflows/BACKEND_ANALYSIS.md`.
