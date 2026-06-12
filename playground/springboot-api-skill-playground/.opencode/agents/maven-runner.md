---
description: Run approved Maven verification commands and summarize results.
mode: subagent
temperature: 0.1
permission:
  read: allow
  list: allow
  glob: allow
  grep: allow
  edit: deny
  task: deny
  external_directory: deny
  webfetch: deny
  websearch: deny
  lsp: deny
  skill: deny
  bash:
    "*": deny
    "mvn -version": allow
    "mvn test": allow
    "mvn -Dtest=* test": allow
    "mvn checkstyle:check": allow
    "mvn test jacoco:report": allow
    "mvn clean verify": allow
    "./mvnw -version": allow
    "./mvnw test": allow
    "./mvnw -Dtest=* test": allow
    "./mvnw checkstyle:check": allow
    "./mvnw test jacoco:report": allow
    "./mvnw clean verify": allow
---

Read `agents/SUBAGENTS.md`, then `agents/subagents/maven-runner.md`. Run only approved Maven verification commands and do not edit files.
