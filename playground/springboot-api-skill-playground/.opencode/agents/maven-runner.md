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
    "mvn -B -ntp -version": allow
    "mvn -B -ntp -version > target/agent-maven-logs/*.log 2>&1": allow
    "mvn test": allow
    "mvn -B -ntp test": allow
    "mvn -B -ntp test > target/agent-maven-logs/*.log 2>&1": allow
    "mvn -Dtest=* test": allow
    "mvn -B -ntp -Dtest=* test": allow
    "mvn -B -ntp -Dtest=* test > target/agent-maven-logs/*.log 2>&1": allow
    "mvn checkstyle:check": allow
    "mvn -B -ntp checkstyle:check": allow
    "mvn -B -ntp checkstyle:check > target/agent-maven-logs/*.log 2>&1": allow
    "mvn test jacoco:report": allow
    "mvn -B -ntp test jacoco:report": allow
    "mvn -B -ntp test jacoco:report > target/agent-maven-logs/*.log 2>&1": allow
    "mvn clean verify": allow
    "mvn -B -ntp clean verify": allow
    "mvn -B -ntp clean verify > target/agent-maven-logs/*.log 2>&1": allow
    "./mvnw -version": allow
    "./mvnw -B -ntp -version": allow
    "./mvnw -B -ntp -version > target/agent-maven-logs/*.log 2>&1": allow
    "./mvnw test": allow
    "./mvnw -B -ntp test": allow
    "./mvnw -B -ntp test > target/agent-maven-logs/*.log 2>&1": allow
    "./mvnw -Dtest=* test": allow
    "./mvnw -B -ntp -Dtest=* test": allow
    "./mvnw -B -ntp -Dtest=* test > target/agent-maven-logs/*.log 2>&1": allow
    "./mvnw checkstyle:check": allow
    "./mvnw -B -ntp checkstyle:check": allow
    "./mvnw -B -ntp checkstyle:check > target/agent-maven-logs/*.log 2>&1": allow
    "./mvnw test jacoco:report": allow
    "./mvnw -B -ntp test jacoco:report": allow
    "./mvnw -B -ntp test jacoco:report > target/agent-maven-logs/*.log 2>&1": allow
    "./mvnw clean verify": allow
    "./mvnw -B -ntp clean verify": allow
    "./mvnw -B -ntp clean verify > target/agent-maven-logs/*.log 2>&1": allow
    "mkdir -p target/agent-maven-logs": allow
    'grep -E "Tests run:|BUILD SUCCESS|BUILD FAILURE|Total time|ERROR|FAILURE" target/agent-maven-logs/*.log': allow
    "tail -n 80 target/agent-maven-logs/*.log": allow
    "find target/surefire-reports target/site/jacoco -maxdepth 2 -type f -print": allow
---

Read `agents/SUBAGENTS.md`, then `agents/subagents/maven-runner.md`. Run only approved Maven verification commands and do not edit files. Prefer low-context logs and return concise summaries.
