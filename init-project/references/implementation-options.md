# init-project implementation options

This note captures public references and implementation paths for evolving the
`init-project` skill. The goal is to generate useful agent project guidance
without turning repository context into a noisy second codebase.

## Current baseline

`init-project` currently provides:

- A thin `AGENTS.md` oriented around project-specific commands, layout, and
  constraints.
- Template fragments under `references/templates/{name}/index.md`, where a
  project may match multiple templates.
- Template scripts under `scripts/templates/{name}/`.
- Detection and rendering scripts that progressively load matched template
  content.
- Java/Maven inspection, dependency tree generation, Spring Boot WebFlux
  inspection, Karate AT inspection, and skill validation.

## Public patterns

### AGENTS.md as shared repository guidance

OpenAI Codex documents `AGENTS.md` as the file Codex reads before work. It also
describes hierarchical loading: global guidance, then repository guidance, then
nearer nested files, with later and more specific guidance taking precedence.
Codex also has a default combined instruction size cap, so large generated
files should be avoided.

Reference: [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)

The open AGENTS.md format presents `AGENTS.md` as a shared, tool-neutral place
for agent instructions.

Reference: [AGENTS.md open format](https://agents.md/)

### Scoped instructions for Copilot-style agents

GitHub Copilot supports repository instructions and also path-scoped
`.github/instructions/*.instructions.md` files with `applyTo` globs. GitHub also
recognizes nested `AGENTS.md` files, where the nearest one can take precedence
for files being edited.

Reference: [GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)

### Claude Code memory bridge

Claude Code primarily reads `CLAUDE.md`, not `AGENTS.md`, but its docs
recommend bridging by creating `CLAUDE.md` that imports `@AGENTS.md`. The same
docs emphasize that specific and concise instructions are followed more
consistently.

Reference: [Claude Code memory](https://code.claude.com/docs/en/memory)

### Small convention files and repo maps

Aider recommends small markdown convention files that are always loaded as
read-only context. Its repo map approach also shows a useful pattern: give the
agent a compact map of important symbols, classes, signatures, and files rather
than asking it to infer everything from raw file trees.

References:

- [Aider conventions](https://aider.chat/docs/usage/conventions.html)
- [Aider repo map](https://aider.chat/docs/repomap.html)

### Reusable instruction catalogs

`awesome-copilot` organizes reusable prompts, instructions, skills, hooks, and
workflows as a marketplace-like catalog. This is a useful model once
`init-project` has many templates and needs discoverable metadata.

Reference: [github/awesome-copilot](https://github.com/github/awesome-copilot)

## Research signals

Recent public research points in two directions:

- Repository context files can improve efficiency. One study reports lower
  median runtime and output tokens when `AGENTS.md` is present while preserving
  comparable task completion behavior.
- Context files can also hurt task success and cost when they include broad
  exploration advice or unnecessary requirements. Minimal, task-relevant
  guidance is safer than a large rule dump.
- Configuration files are the dominant current mechanism for customizing coding
  agents, and `AGENTS.md` is emerging as an interoperable standard across tools.

References:

- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)
- [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988)
- [Configuring Agentic AI Coding Tools: An Exploratory Study](https://arxiv.org/abs/2602.14690)

## Option V1: thin root plus evidence files

Generate a concise root `AGENTS.md` and keep most stack-specific details in
referenced files under `agents/` or another generated support directory.

What changes:

- Keep `AGENTS.md` short: commands, repo layout, test policy, and links to
  generated evidence files.
- Add length and noise budgets to the generation workflow or validator.
- Prefer generated facts over generic rules.

Pros:

- Best aligned with Codex instruction-size limits and research caution about
  context bloat.
- Easy to implement with the current template references and inspectors.
- Keeps the first context load cheap and stable.

Cons:

- The agent must decide to open linked files when needed.
- Some tools may not follow references as reliably as directly loaded text.

Implementation plan:

1. Add `max_root_lines`, `max_root_bytes`, and `max_template_summary_lines` to
   validation.
2. Add a generated `agents/project-evidence.md` containing detector output,
   Maven coordinates, module list, dependency tree location, and matched
   templates.
3. Keep template fragments phrased as short, scoped facts and commands.

Test plan:

- Snapshot render output for sample Maven, Spring WebFlux, and Karate projects.
- Validate root file size and absence of empty template sections.
- Verify linked evidence files exist when referenced.

## Option V2: scoped instruction pack

Generate root guidance plus path-specific instruction files when the repository
layout is clear.

What changes:

- Emit nested `AGENTS.md` files for high-signal subtrees such as `src/test`,
  `src/it`, `features`, or service modules.
- Optionally emit `.github/instructions/*.instructions.md` with `applyTo` globs
  for Copilot-compatible scoping.

Pros:

- Uses the same precedence model documented by Codex and GitHub.
- Reduces irrelevant rules for agents editing only tests or only WebFlux
  handlers.
- Fits projects that match multiple templates.

Cons:

- More generated files to review.
- Tool behavior differs: Codex, Copilot, and Claude do not load scoped files in
  exactly the same way.
- Bad path detection can put rules in the wrong scope.

Implementation plan:

1. Extend inspectors to return candidate scopes:
   `main_sources`, `test_sources`, `karate_features`, `webflux_handlers`.
2. Apply template guidance only to matching scopes.
3. Add a manual checklist showing each suggested file and why it should exist.

Test plan:

- Fixture with multi-module Maven project.
- Fixture with Karate features under non-standard paths.
- Validate generated scoped files do not duplicate root content.

## Option V3: cross-agent bridge

Use `AGENTS.md` as the source of truth, then optionally generate small bridge
files for other agents.

What changes:

- Generate `CLAUDE.md` containing `@AGENTS.md`.
- Optionally generate `.github/copilot-instructions.md` or
  `.github/instructions/*.instructions.md`.
- Add a manifest that records generated files and their source template hashes.

Pros:

- Makes one initialization pass useful for Codex, Claude Code, and Copilot.
- Reduces manual duplication.
- Keeps the skill aligned with public tool guidance.

Cons:

- Bridge files can drift if users edit generated outputs manually.
- Conflicting precedence rules are possible when a repo already has tool files.
- Requires careful overwrite policy.

Implementation plan:

1. Add `--emit-bridge claude,copilot` with default `none`.
2. Detect existing `CLAUDE.md`, `.github/copilot-instructions.md`, and scoped
   instruction files.
3. Use conservative merge mode: create missing files, append only inside marked
   generated regions, and never overwrite user-authored content by default.
4. Record generated file metadata in `agents/init-project-manifest.json`.

Test plan:

- Existing bridge file with no generated region.
- Existing bridge file with generated region.
- Repo with both root and nested `AGENTS.md`.

## Option V4: repo map enhancement

Add a compact repo map inspired by Aider: important files, Java packages,
classes, methods, Spring components, routes, Karate features, and build modules.

What changes:

- Generate `agents/repo-map.md` or `agents/repo-map.json`.
- Include top-level symbols and relationships instead of full source excerpts.
- Use stack-specific inspectors to enrich the map.

Pros:

- Gives agents useful topology without loading many files.
- Helps agents find the right abstraction and avoid duplicate implementations.
- Complements Maven and dependency-tree facts.

Cons:

- Java parsing can be complex, especially with annotation processors and
  generated code.
- Repo maps can become stale unless regenerated.
- Overly large maps recreate the same context-bloat problem.

Implementation plan:

1. Start with a simple regex or XML-backed Java map:
   packages, public classes, annotations, and method names.
2. Add Spring WebFlux route extraction for `@RestController`, functional
   router beans, and WebClient beans.
3. Add Karate feature map: feature files, scenario names, tags, and called
   helpers.
4. Limit output by module and file count; write overflow warnings.

Test plan:

- Validate JSON schema for repo-map output.
- Snapshot map for representative sample projects.
- Confirm generated Markdown stays below configured size budgets.

## Option V5: verification and eval loop

Turn `init-project` outputs into testable artifacts, not only generated docs.

What changes:

- Expand `validate_skill.py` into a quality gate for templates, scripts, and
  rendered output.
- Add fixtures and expected outputs.
- Add checks for missing commands, broken links, empty sections, and excessive
  generic advice.

Pros:

- Prevents template drift as more stacks are added.
- Makes changes safer before commit and push.
- Encourages measurable quality instead of subjective prompt tuning.

Cons:

- Requires sample repos or synthetic fixtures.
- Snapshot tests can be noisy if output formatting changes often.

Implementation plan:

1. Add fixtures under `init-project/evals/fixtures/`.
2. Add expected rendered file manifests, not full huge snapshots.
3. Check invariants: matched templates, generated files, file sizes, command
   extraction, and no broken references.
4. Add a README section describing the validation workflow.

Test plan:

- Run validation against each fixture.
- Fail on broken relative links and missing template script references.
- Compare detector JSON against expected template matches.

## Option V6: template registry

Introduce a machine-readable registry once template count grows.

What changes:

- Add `references/templates/index.json`.
- Each template declares name, description, detector hints, scripts, emitted
  sections, compatible bridge outputs, and dependencies on other templates.

Pros:

- Scales beyond a few hand-discovered templates.
- Makes template discovery, documentation, and validation easier.
- Enables marketplace-like browsing similar to reusable Copilot instruction
  catalogs.

Cons:

- Too much structure early can slow template authoring.
- Registry/schema maintenance becomes part of every change.

Implementation plan:

1. Keep the registry optional until there are at least 6-8 templates.
2. Define minimal schema:
   `name`, `summary`, `detects`, `scripts`, `outputs`, `dependencies`.
3. Update detector and validator to read the registry when present.
4. Generate a template index page from registry metadata.

Test plan:

- Validate every registered path exists.
- Validate dependencies refer to known templates.
- Ensure unregistered legacy templates still work during migration.

## Recommended roadmap

1. Implement V1 hardening first. It improves the current design without changing
   the user workflow.
2. Add V2 scoped instruction generation for Maven, Spring WebFlux, and Karate
   projects. This best fits the "project may match multiple templates" design.
3. Add V3 bridge output for Claude and Copilot, disabled by default.
4. Add V5 quality gates before adding many more templates.
5. Add V4 repo maps once fixture coverage exists.
6. Add V6 registry only when the template list becomes large enough that
   directory scanning is hard to maintain.

## Decision matrix

| Option | Fit now | Cost | Main risk | Priority |
| --- | --- | --- | --- | --- |
| V1 thin root plus evidence files | High | Low | Agents may skip linked evidence | 1 |
| V2 scoped instruction pack | High | Medium | Incorrect path scoping | 2 |
| V3 cross-agent bridge | Medium | Medium | Drift and precedence conflicts | 3 |
| V5 verification and eval loop | High | Medium | Fixture maintenance | 4 |
| V4 repo map enhancement | Medium | High | Parser complexity and stale maps | 5 |
| V6 template registry | Low now, high later | Medium | Premature schema overhead | 6 |
