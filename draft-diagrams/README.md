# draft-diagrams

Draft, add, and modify maintainable technical design diagrams as Mermaid or PlantUML ASCII source.

## What It Does

This skill helps an agent choose, produce, and revise the right text-based diagram format for:

- Flowcharts and workflow diagrams
- Sequence diagrams
- UML class diagrams
- ER diagrams
- Architecture box diagrams
- C4 context, container, and component diagrams
- State diagrams
- Terminal-friendly PlantUML ASCII diagrams
- Updates to existing Mermaid or PlantUML diagram source

The root `SKILL.md` uses progressive disclosure. It routes the agent to one small reference file per diagram family instead of loading every diagram syntax guide at once.

## Source Attribution

This skill is based on and adapted from these public skills:

- [`softaworks/agent-toolkit@mermaid-diagrams`](https://skills.sh/softaworks/agent-toolkit/mermaid-diagrams), with source available in [`softaworks/agent-toolkit`](https://github.com/softaworks/agent-toolkit). The local version adopts its Mermaid-first scope, diagram type selection, and progressive reference structure while rewriting and condensing the guidance for this repository.
- [`github/awesome-copilot@plantuml-ascii`](https://skills.sh/github/awesome-copilot/plantuml-ascii), with source available in [`github/awesome-copilot`](https://github.com/github/awesome-copilot). The local version adapts its PlantUML text-mode workflow for ASCII and Unicode diagram output.

This local skill does not vendor the upstream skill directories. It is a rewritten, consolidated skill tailored for Markdown-native technical design diagrams, PlantUML ASCII output, and progressive disclosure by diagram type.

## Layout

```text
draft-diagrams/
  SKILL.md
  README.md
  evals/
  references/
    mermaid-architecture-c4.md
    mermaid-class.md
    mermaid-erd.md
    mermaid-flowcharts.md
    mermaid-sequence.md
    mermaid-state.md
    plantuml-ascii.md
    rendering-and-embedding.md
```

## Recommended Defaults

- Use Mermaid for diagrams that should render in Markdown or live in repository documentation.
- Use PlantUML ASCII for terminal output, plain-text comments, email, or environments without graphical rendering.
- When modifying an existing diagram, preserve the current format and style unless the user asks for a conversion.
- Keep diagrams as editable source. Export PNG/SVG only as a generated artifact when needed.
