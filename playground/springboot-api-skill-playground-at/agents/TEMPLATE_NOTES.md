# Template Notes

## baseline
- Keep project memory concise and specific to this AT suite.
- Inspect existing feature and payload patterns before adding scenarios.
- Run the smallest useful Maven command and document hosted checks that could not run.

## maven-java
- Java release is 17 via `maven.compiler.release`.
- Prefer `mvn -B -ntp` for agent-run commands.
- Do not commit `target/`, Karate reports, or local Maven logs.

## karate-at
- `karate-config.js` owns `baseUrl`, timeouts, and shared headers.
- Use `-Dat.enabled=true` to opt into hosted HTTP execution.
- Use `-Dkarate.tags=@tag` to select scenarios.
- Keep tags stable because they are the CI and local selection contract.
- Do not hard-code credentials, environment URLs, or service tokens.
