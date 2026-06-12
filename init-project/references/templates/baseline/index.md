# Coding Agent Baseline Template

Use this template for every project initialized by `init-project`. It captures general coding-agent rules that are independent of language or framework. Load it before stack-specific templates such as `maven-java`, `springboot3-webflux`, or `karate-at`.

## Public Guidance Used

This baseline distills stable public guidance from:

- OpenAI Codex AGENTS.md guidance: AGENTS files provide consistent project instructions, can be layered by scope, and should include repository expectations and verification commands.
  https://developers.openai.com/codex/guides/agents-md
- AGENTS.md open format: AGENTS.md is a predictable README-like place for agent instructions, setup commands, tests, and code style.
  https://agents.md/
- GitHub Copilot repository instructions: agent onboarding instructions should describe how a cloud agent can work efficiently in a repo; nearest AGENTS.md can take precedence.
  https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions
- VS Code custom instructions: effective instructions are short, self-contained, explain why, include concrete examples for preferred/avoided patterns, and focus on non-obvious rules.
  https://code.visualstudio.com/docs/agent-customization/custom-instructions
- Aider conventions and repo map docs: convention files can capture preferred libraries/style, and repo maps help agents understand files, symbols, and relationships before editing.
  https://aider.chat/docs/usage/conventions.html
  https://aider.chat/docs/repomap.html
- Wiz secure rules-file guidance: rules should be clear, concise, actionable, scoped, composable, and include security-focused guardrails.
  https://www.wiz.io/blog/safer-vibe-coding-rules-files

## Baseline AGENTS.md Shape

Use this baseline shape unless the project already has a stronger local convention:

```markdown
# AGENTS.md

## Project
- Purpose: [what this repository does]
- Primary language/framework: [discovered stack]
- Template facets: baseline[, stack facets]

## Start Here
- Project profile: agents/PROJECT_PROFILE.md
- Build and test commands: agents/BUILD_AND_TEST.md
- Code style: agents/CODE_STYLE.md
- Architecture notes: agents/ARCHITECTURE_NOTES.md
- Template notes: agents/TEMPLATE_NOTES.md

## Baseline Working Rules
- Read existing code before editing; prefer local patterns over new abstractions.
- Keep changes scoped to the user request and avoid unrelated refactors.
- Preserve public APIs, data contracts, and migration behavior unless the task explicitly changes them.
- Add or update focused tests for behavior changes.
- Run the smallest useful verification command first, then broader checks when risk warrants it.
- Document any verification you could not run and why.
- Do not commit secrets, credentials, generated build output, or local machine state.
- Ask before adding new production dependencies or changing build/deploy behavior.

## Verification Checklist
- [ ] Relevant files were inspected before editing.
- [ ] Existing conventions were followed or the deviation is explained.
- [ ] Tests/build/lint were run, or skipped with a reason.
- [ ] Security-sensitive changes were reviewed for input validation, auth, secrets, and unsafe I/O.
```

## Baseline Agent Rules

Put these rules in `AGENTS.md` or `agents/TEMPLATE_NOTES.md` after adapting wording to the project:

### Discovery Before Editing

- Identify the project root and active instruction files.
- Read README, existing `AGENTS.md`, build files, and the closest examples of code you will modify.
- Build a compact repo map: important modules, entrypoints, source roots, test roots, configs, and generated files.
- Prefer existing helpers, frameworks, and test utilities over introducing new patterns.

Why: public guidance across agent tools emphasizes giving agents project context and conventions up front. A short repo map prevents repeated rediscovery and makes future edits fit the codebase.

### Scope Control

- Keep edits tightly tied to the requested behavior.
- Avoid broad formatting, dependency churn, file moves, or opportunistic cleanup unless required.
- If a better refactor is tempting but not necessary, note it as follow-up.

Why: coding agents are most reliable when the task boundary is explicit and small enough to verify.

### Verification

- Capture the canonical build/test/lint commands in `agents/BUILD_AND_TEST.md`.
- Prefer the smallest relevant command for quick feedback, such as a targeted test.
- Run broader verification for shared code, cross-module contracts, or risky changes.
- When checks cannot run, record the reason and the residual risk.

Why: AGENTS-style guidance commonly includes setup and test commands because agents need executable feedback, not just prose.

### Safety And Security

- Never expose or copy secrets from `.env`, credentials files, tokens, private keys, CI secrets, or local config.
- Validate and sanitize untrusted input when touching command execution, deserialization, upload, auth, file paths, XML, SQL, templates, or network calls.
- Quote shell variables and avoid shelling out unless the project already does so safely.
- Treat generated code, fixtures, and external API contracts as risk areas.

Why: secure rules files are useful because they centralize concise guardrails for common AI-generated-code failure modes.

### Instruction Quality

- Keep rules short, concrete, and project-specific.
- Include the reason for non-obvious rules.
- Use examples only where they clarify preferred or avoided patterns.
- Split stack-specific rules into template sections instead of bloating the baseline.

Why: concise, scoped, composable rules are easier for agents to follow and less likely to crowd out the user's task.

## File Placement Guidance

- `AGENTS.md`: short always-read entry point and high-signal rules.
- `agents/PROJECT_PROFILE.md`: repo map and discovered facts.
- `agents/BUILD_AND_TEST.md`: commands and verification strategy.
- `agents/CODE_STYLE.md`: coding conventions inferred from the repo.
- `agents/ARCHITECTURE_NOTES.md`: architecture boundaries and risky areas.
- `agents/TEMPLATE_NOTES.md`: baseline notes plus stack-specific template sections.

If a project supports nested instruction files, keep broad rules at the root and put specialized rules close to the relevant subdirectory.

