# Code Style

## Java Runner
- Keep runner classes under `src/test/java/com/acme/skillplayground/at/`.
- Runner classes should end with `Runner` so Surefire includes them.
- Keep hosted execution gated by `@EnabledIfSystemProperty(named = "at.enabled", matches = "true")`.
- Do not add demo service production classes as dependencies.

## Karate Features
- Put feature files under `src/test/resources/features/<surface>/`.
- Use tags for suite selection: `@smoke`, `@orders`, `@retail`, `@errors`.
- Keep `Background` small: base URL, content negotiation headers, and simple shared IDs only.
- Prefer behavior-level assertions over checking every field.
- Use `classpath:payloads/...` fixtures for reusable request bodies.

## Fixtures
- Put reusable request payloads under `src/test/resources/payloads/<surface>/`.
- Keep payloads free of real credentials, tokens, and personal data.
- Use obvious AT-only values such as `customer-at-001` and `SKU-AT-001`.

## Environment
- Keep environment-specific data in Maven/system properties: `demo.baseUrl`, `karate.env`, `karate.tags`, and `demo.requestTimeout`.
- Do not hard-code SIT/UAT/production URLs in source.
