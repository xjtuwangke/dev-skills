# Coding Agent Baseline Template

Use this template for every project initialized by `init-project`. It captures general coding-agent rules that are independent of language or framework. Load it before stack-specific templates such as `maven-java`, `springboot3-webflux`, or `karate-at`.

## Public Guidance Used

This baseline distills stable public guidance from:

- OpenAI Codex AGENTS.md guidance: AGENTS files provide consistent project instructions and can be layered by scope; this template routes detailed expectations and verification commands into `agents/technical.md`.
  https://developers.openai.com/codex/guides/agents-md
- AGENTS.md open format: AGENTS.md is a predictable README-like place for agent instructions; this template keeps the root file as a router and moves setup, tests, and code style into focused docs.
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
- [One sentence describing what this repository is and its primary stack.]

## Where To Look

| Task | Start Here | Notes |
| --- | --- | --- |
| Technical change, review, build, or test | `agents/technical.md` | Commands, coding standards, verification discipline, and focused technical links. |
| Analyze business logic | `agents/business/` | Read only the relevant domain card before changing semantics. |
```

## Baseline Agent Rules

Put these rules in `agents/technical.md` or focused cards after adapting
wording to the project. Keep root `AGENTS.md` to project positioning and
`Where To Look`.

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

- Capture the canonical build/test/lint commands in `agents/technical.md`.
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

- `AGENTS.md`: short always-read entry point with one-sentence project
  positioning and `Where To Look`.
- `agents/technical.md`: technical directory page, commands, verification
  strategy, coding conventions, and common guardrails.
- `agents/technical/*.md`: focused technical cards by surface.
- `agents/business/*.md`: business/domain cards when behavior semantics matter.

If a project supports nested instruction files, keep the root as a router and
put specialized rules close to the relevant subdirectory or focused card.
