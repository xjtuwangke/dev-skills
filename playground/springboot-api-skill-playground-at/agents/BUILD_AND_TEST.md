# Build And Test

## Core Commands
- Compile without executing hosted ATs: `mvn -B -ntp -DskipTests test`
- Default Maven test: `mvn -B -ntp test`
- Run hosted ATs locally: `mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080`
- Run smoke scenarios: `mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080 -Dkarate.tags=@smoke`
- Run one tag group: `mvn -B -ntp test -Dat.enabled=true -Dkarate.tags=@orders`
- Run a named environment: `mvn -B -ntp test -Dat.enabled=true -Dkarate.env=sit -Ddemo.baseUrl=https://sit.example.test`

## Execution Model
- `DemoServiceAtRunner` is disabled unless system property `at.enabled=true` is present.
- Default `mvn test` should compile and skip hosted scenarios, which keeps local validation safe when the demo service is not running.
- Hosted AT commands require a separately started demo service and whatever database/profile the service needs.
- Karate reports: `target/karate-reports/karate-summary.html`.

## Low-Context Maven Output
Use this pattern when command output may be long:

```bash
mkdir -p target/agent-maven-logs
mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080 > target/agent-maven-logs/hosted-at.log 2>&1
grep -E "Tests run:|BUILD SUCCESS|BUILD FAILURE|Karate version|failed|ERROR|FAILURE" target/agent-maven-logs/hosted-at.log | tail -60
```

If hosted ATs fail, inspect:

- `target/karate-reports/karate-summary.html`
- `target/karate-reports/*.json`
- `target/surefire-reports/*.txt`
- `tail -100 target/agent-maven-logs/hosted-at.log`

## Safe Verification Before Finishing
- For project structure or docs changes, run `mvn -B -ntp -DskipTests test`.
- For feature/payload changes, run hosted ATs only after confirming the target service is available.
