#!/usr/bin/env python3
"""Render draft AGENTS.md and agents/*.md files for a project."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
DETECTOR = SCRIPT_DIR / "detect_project.py"
MAVEN_INSPECTOR = SCRIPT_DIR / "templates" / "maven-java" / "inspect_maven_project.py"
SPRING_INSPECTOR = SCRIPT_DIR / "templates" / "springboot3-webflux" / "inspect_springboot_webflux.py"
KARATE_INSPECTOR = SCRIPT_DIR / "templates" / "karate-at" / "inspect_karate_project.py"
SUPPORTED_TEMPLATES = ["baseline", "maven-java", "springboot3-webflux", "karate-at"]


def run_json(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return {
            "error": "command failed",
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return {
            "error": "invalid json",
            "command": command,
            "parse_error": str(exc),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }


def normalize_templates(values: list[str] | None) -> list[str] | None:
    if not values:
        return None
    requested = []
    for value in values:
        for part in value.split(","):
            template = part.strip()
            if template:
                requested.append(template)
    unknown = sorted(set(requested) - set(SUPPORTED_TEMPLATES))
    if unknown:
        raise ValueError(f"Unsupported template(s): {', '.join(unknown)}")
    selected = {"baseline", *requested}
    return [template for template in SUPPORTED_TEMPLATES if template in selected]


def apply_template_override(
    detection: dict[str, Any],
    templates: list[str] | None,
    primary_purpose: str | None,
) -> dict[str, Any]:
    if not templates and not primary_purpose:
        return detection

    updated = dict(detection)
    if templates:
        updated["matched_templates"] = templates
        updated["template_reference_paths"] = {
            name: f"references/templates/{name}/index.md" for name in templates
        }
        signals = dict(updated.get("signals", {}))
        for template in templates:
            signals.setdefault(template, [])
            signals[template].append("template explicitly requested")
        updated["signals"] = signals

    if primary_purpose:
        updated["primary_purpose"] = primary_purpose
    elif templates:
        if "springboot3-webflux" in templates:
            updated["primary_purpose"] = "springboot3-webflux-service"
        elif "karate-at" in templates:
            updated["primary_purpose"] = "karate-acceptance-tests"
        elif "maven-java" in templates:
            updated["primary_purpose"] = "maven-java-project"
        else:
            updated["primary_purpose"] = "generic-project"

    return updated


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def find_files(root: Path, patterns: tuple[str, ...], limit: int = 20) -> list[str]:
    ignored = {".git", "target", "build", ".idea", ".gradle"}
    found: list[str] = []
    for pattern in patterns:
        for path in root.rglob(pattern):
            if any(part in ignored for part in path.parts):
                continue
            found.append(rel(path, root))
            if len(found) >= limit:
                return sorted(found)
    return sorted(found)


def bullet(items: list[str], empty: str = "Needs confirmation") -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- `{item}`" for item in items)


def plain_bullet(items: list[str], empty: str = "Needs confirmation") -> str:
    if not items:
        return f"- {empty}"
    return "\n".join(f"- {item}" for item in items)


def subsection_list(title: str, items: list[str], empty: str = "None detected") -> str:
    return f"### {title}\n{bullet(items, empty)}"


def matched_signals(detection: dict[str, Any]) -> dict[str, Any]:
    signals = detection.get("signals", {})
    return {
        template: signals.get(template, [])
        for template in detection.get("matched_templates", [])
    }


def coord_text(node: dict[str, Any] | None) -> str:
    if not node:
        return "Needs confirmation"
    c = node.get("coordinates", {})
    parts = [c.get("groupId"), c.get("artifactId"), c.get("version")]
    return ":".join(part for part in parts if part) or "Needs confirmation"


def dependency_id(dep: dict[str, Any]) -> str:
    group = dep.get("groupId") or "?"
    artifact = dep.get("artifactId") or "?"
    version = dep.get("version")
    scope = dep.get("scope") or "compile"
    base = f"{group}:{artifact}"
    if version:
        base += f":{version}"
    return f"{base} ({scope})"


def direct_dependencies(pom_tree: dict[str, Any] | None) -> list[str]:
    if not pom_tree:
        return []
    return [dependency_id(dep) for dep in pom_tree.get("dependencies", [])]


def dependency_management(pom_tree: dict[str, Any] | None) -> list[str]:
    if not pom_tree:
        return []
    return [dependency_id(dep) for dep in pom_tree.get("dependencyManagement", [])]


def exclusions(pom_tree: dict[str, Any] | None) -> list[str]:
    if not pom_tree:
        return []
    values = []
    for dep in pom_tree.get("dependencies", []):
        source = dependency_id(dep)
        for exclusion in dep.get("exclusions", []):
            values.append(
                f"{source} excludes {exclusion.get('groupId')}:{exclusion.get('artifactId')}"
            )
    return values


def java_hint(maven_info: dict[str, Any] | None) -> str:
    if not maven_info or not maven_info.get("is_maven_project"):
        return "Needs confirmation"
    tree = maven_info.get("pom_tree", {})
    return tree.get("java_version_hint") or "Needs confirmation"


def maven_command(root: Path, goal: str) -> str:
    return f"./mvnw {goal}" if (root / "mvnw").exists() else f"mvn {goal}"


def project_title(root: Path, maven_info: dict[str, Any] | None) -> str:
    if maven_info and maven_info.get("is_maven_project"):
        artifact = (
            maven_info.get("pom_tree", {})
            .get("coordinates", {})
            .get("artifactId")
        )
        if artifact:
            return artifact
    return root.name


def render_agents_md(
    root: Path,
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
) -> str:
    templates = detection.get("matched_templates", [])
    title = project_title(root, maven_info)
    test_cmd = maven_command(root, "test") if "maven-java" in templates else "Needs confirmation"
    build_cmd = (
        maven_command(root, "clean verify") if "maven-java" in templates else "Needs confirmation"
    )
    run_cmd = (
        maven_command(root, "spring-boot:run")
        if "springboot3-webflux" in templates
        else "Needs confirmation"
    )

    return f"""# AGENTS.md

## Project
- Name: {title}
- Primary purpose: {detection.get("primary_purpose") or "Needs confirmation"}
- Template facets: {", ".join(templates) if templates else "baseline"}
- Java version: {java_hint(maven_info)}

## Start Here
- Project profile: `agents/PROJECT_PROFILE.md`
- Build and test commands: `agents/BUILD_AND_TEST.md`
- Code style: `agents/CODE_STYLE.md`
- Architecture notes: `agents/ARCHITECTURE_NOTES.md`
- Dependency notes: `agents/DEPENDENCIES.md`
- Template notes: `agents/TEMPLATE_NOTES.md`

## Baseline Working Rules
- Read existing code before editing; prefer local patterns over new abstractions.
- Keep changes scoped to the user request and avoid unrelated refactors.
- Preserve public APIs, data contracts, and migration behavior unless the task explicitly changes them.
- Add or update focused tests for behavior changes.
- Run the smallest useful verification command first, then broader checks when risk warrants it.
- Document any verification you could not run and why.
- Do not commit secrets, credentials, generated build output, or local machine state.
- Ask before adding new production dependencies or changing build/deploy behavior.

## Fast Commands
- Build: `{build_cmd}`
- Unit tests: `{test_cmd}`
- Run locally: `{run_cmd}`

## Verification Checklist
- [ ] Relevant files were inspected before editing.
- [ ] Existing conventions were followed or the deviation is explained.
- [ ] Tests/build/lint were run, or skipped with a reason.
- [ ] Security-sensitive changes were reviewed for input validation, auth, secrets, and unsafe I/O.
"""


def render_project_profile(
    root: Path,
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
    spring_info: dict[str, Any] | None,
    karate_info: dict[str, Any] | None,
) -> str:
    source_roots = find_files(root, ("src/main/java", "src/test/java", "src/test/resources"), 30)
    configs = find_files(root, ("application*.yml", "application*.yaml", "karate-config.js"), 30)
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    modules = pom_tree.get("modules", []) if pom_tree else []
    app_classes = spring_info.get("application_classes", []) if spring_info else []
    package_roots = spring_info.get("package_roots", []) if spring_info else []
    feature_roots = karate_info.get("feature_files", []) if karate_info else []
    runner_classes = karate_info.get("runner_classes", []) if karate_info else []
    spring_section = ""
    if spring_info:
        spring_section = f"""
## Spring Boot WebFlux Evidence
- Application classes: {", ".join(f"`{item}`" for item in app_classes) if app_classes else "None detected"}
- Package roots: {", ".join(f"`{item}`" for item in package_roots) if package_roots else "None detected"}
"""
    karate_section = ""
    if karate_info:
        karate_section = f"""
## Karate Evidence
- Feature files sampled: {len(feature_roots)}
- Runner classes: {", ".join(f"`{item}`" for item in runner_classes) if runner_classes else "None detected"}
"""

    return f"""# Project Profile

## Identity
- Root: `{root}`
- Coordinates: `{coord_text(pom_tree)}`
- Primary purpose: {detection.get("primary_purpose") or "Needs confirmation"}
- Template facets: {", ".join(detection.get("matched_templates", []))}

## Structure
- Maven modules: {", ".join(f"`{m}`" for m in modules) if modules else "None detected"}

## Source And Test Roots
{bullet(source_roots)}

## Configuration Files
{bullet(configs)}
{spring_section}{karate_section}
## Detection Evidence
```json
{json.dumps(matched_signals(detection), indent=2, ensure_ascii=False)}
```

## Notes
- Facts in this file were generated from repository inspection and should be corrected when project-specific knowledge is available.
- Mark uncertain runtime assumptions as "Needs confirmation" instead of guessing.
"""


def render_build_and_test(
    root: Path,
    detection: dict[str, Any],
    karate_info: dict[str, Any] | None,
) -> str:
    templates = detection.get("matched_templates", [])
    if "maven-java" in templates:
        build = maven_command(root, "clean verify")
        test = maven_command(root, "test")
        package = maven_command(root, "-DskipTests package")
        targeted = maven_command(root, "-Dtest=SomeTest test")
    else:
        build = test = package = targeted = "Needs confirmation"

    karate = ""
    if "karate-at" in templates:
        tags = karate_info.get("tags", []) if karate_info else []
        envs = karate_info.get("env_hints", []) if karate_info else []
        runners = karate_info.get("runner_classes", []) if karate_info else []
        runner_name = "SomeRunner"
        if runners:
            runner_name = Path(runners[0]).stem
        karate = f"""
## Karate Commands
- Smoke/tag run: `{maven_command(root, 'test -Dkarate.options=\"--tags @smoke\"')}`
- Environment run: `{maven_command(root, 'test -Dkarate.env=dev')}`
- Single runner: `{maven_command(root, f'test -Dtest={runner_name}')}`

## Karate Suite Evidence
- Tags detected: {", ".join(f"`{tag}`" for tag in tags) if tags else "Needs confirmation"}
- Environment hints: {", ".join(f"`{env}`" for env in envs) if envs else "Needs confirmation"}
- Runner classes: {", ".join(f"`{runner}`" for runner in runners) if runners else "Needs confirmation"}
"""

    webflux = ""
    if "springboot3-webflux" in templates:
        webflux = f"""
## Spring Boot Commands
- Run locally: `{maven_command(root, 'spring-boot:run')}`
- Package without tests: `{package}`
"""

    return f"""# Build And Test

## Core Commands
- Build: `{build}`
- Unit tests: `{test}`
- Targeted test: `{targeted}`
- Package without tests: `{package}`
{webflux}{karate}
## Verification Strategy
- Prefer targeted tests while editing.
- Run full build before finishing changes that affect shared behavior.
- If external services, shared environments, or slow dependency resolution block a command, record the command and reason.
"""


def render_code_style(detection: dict[str, Any]) -> str:
    templates = detection.get("matched_templates", [])
    lines = [
        "# Code Style",
        "",
        "## General",
        "- Follow the nearest existing package/module style.",
        "- Prefer existing helpers and test utilities over new abstractions.",
        "- Keep naming, assertions, logging, and error handling consistent with nearby code.",
        "- Avoid broad formatting-only churn unless the project formatter requires it.",
    ]
    if "springboot3-webflux" in templates:
        lines.extend(
            [
                "",
                "## Spring Boot WebFlux",
                "- Preserve reactive composition with `Mono` and `Flux`.",
                "- Avoid blocking calls in request handling paths.",
                "- Follow existing controller/router/handler, DTO, validation, and exception mapping style.",
            ]
        )
    if "karate-at" in templates:
        lines.extend(
            [
                "",
                "## Karate",
                "- Keep scenarios behavior-focused and readable.",
                "- Reuse existing `Background`, helper features, JS utilities, fixtures, schemas, and tags.",
                "- Prefer meaningful assertions on body, schema, headers, and business fields.",
            ]
        )
    return "\n".join(lines) + "\n"


def render_architecture(
    root: Path,
    detection: dict[str, Any],
    spring_info: dict[str, Any] | None,
    karate_info: dict[str, Any] | None,
) -> str:
    templates = detection.get("matched_templates", [])
    java_files = find_files(root, ("*.java",), 40)
    feature_files = find_files(root, ("*.feature",), 40)
    flow = "Needs confirmation"
    if "springboot3-webflux" in templates:
        flow = "HTTP route/controller -> handler/service -> client/repository -> external dependency"
    elif "karate-at" in templates:
        flow = "Maven command -> JUnit/Karate runner -> karate-config.js -> feature files -> helpers/fixtures -> system under test"

    spring_section = ""
    if spring_info:
        spring_section = f"""
## Spring Boot WebFlux Evidence
{subsection_list("Application classes", spring_info.get("application_classes", []))}
{subsection_list("Controllers, handlers, or router functions", spring_info.get("controllers_or_handlers", []))}
{subsection_list("Web clients or HTTP clients", spring_info.get("web_clients", []))}
{subsection_list("Reactive sources", spring_info.get("reactive_sources", []))}
{subsection_list("Configuration/property classes", spring_info.get("configuration_properties", []))}
{subsection_list("WebFlux tests", spring_info.get("webflux_tests", []))}
"""

    karate_section = ""
    if karate_info:
        karate_section = f"""
## Karate Suite Evidence
- Feature count: {karate_info.get("feature_count", 0)}
{subsection_list("Feature files", karate_info.get("feature_files", []))}
### Tags
{plain_bullet(karate_info.get("tags", []), "None detected")}
{subsection_list("Runner classes", karate_info.get("runner_classes", []))}
{subsection_list("Config files", karate_info.get("karate_config", []))}
{subsection_list("Fixtures, schemas, payloads", karate_info.get("fixtures", []))}
"""

    return f"""# Architecture Notes

## Primary Flow
```text
{flow}
```
{spring_section}{karate_section}

## Representative Java Files
{bullet(java_files, "None detected")}

## Representative Feature Files
{bullet(feature_files, "None detected")}

## Risk Areas
- Generated files, fixtures, contracts, shared helpers, and environment-specific config.
- Public APIs and serialization/deserialization behavior.
- Authentication, authorization, secrets handling, file paths, shell execution, XML/JSON parsing, and network calls.
"""


def render_dependencies(
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
) -> str:
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    wrapper = maven_info.get("maven_wrapper", {}) if maven_info else {}
    return f"""# Dependencies

## Maven Project
- Maven detected: {bool(maven_info and maven_info.get("is_maven_project"))}
- Maven wrapper: {wrapper.get("present", False)}
- Coordinates: `{coord_text(pom_tree)}`
- Java version hint: {java_hint(maven_info)}

## Dependency Management And BOMs
{bullet(dependency_management(pom_tree))}

## Direct Dependencies
{bullet(direct_dependencies(pom_tree))}

## Direct Dependency Exclusions
{bullet(exclusions(pom_tree), "None detected")}

## Dependency Tree
- Command: `python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --timeout 300`
- Status: Not run by the renderer. Run the command when transitive dependency analysis matters.

## Notes For Future Changes
- Prefer existing BOM or dependency management when adding versions.
- Explain new exclusions and verify the dependency tree when changing logging, HTTP, JSON/XML, database, security, or test framework dependencies.
"""


def render_template_notes(detection: dict[str, Any]) -> str:
    templates = detection.get("matched_templates", [])
    sections = [
        "# Template Notes",
        "",
        "## baseline",
        "- Keep instructions short, concrete, scoped, and project-specific.",
        "- Verify changes with the smallest useful command and document skipped checks.",
        "- Do not expose secrets or commit generated build output/local state.",
    ]
    if "maven-java" in templates:
        sections.extend(
            [
                "",
                "## maven-java",
                "- Prefer `./mvnw` when present; otherwise use `mvn`.",
                "- Inspect root and module POMs before changing dependencies or build plugins.",
                "- Use `agents/DEPENDENCIES.md` for dependency management, exclusions, and tree findings.",
            ]
        )
    if "springboot3-webflux" in templates:
        sections.extend(
            [
                "",
                "## springboot3-webflux",
                "- Preserve non-blocking reactive flows.",
                "- Use existing `WebTestClient`, `StepVerifier`, Spring test, and configuration patterns.",
                "- Spring Boot 3 implies Java 17+ and Jakarta namespaces unless the project proves otherwise.",
            ]
        )
    if "karate-at" in templates:
        sections.extend(
            [
                "",
                "## karate-at",
                "- Keep tag and environment behavior aligned with CI.",
                "- Reuse existing helpers, fixtures, schemas, and setup flows.",
                "- Treat shared test environments and test data as stateful risk areas.",
            ]
        )
    return "\n".join(sections) + "\n"


def write_file(path: Path, content: str, overwrite: bool) -> str:
    if path.exists() and not overwrite:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "written"


def render(
    project: Path,
    overwrite: bool,
    templates: list[str] | None,
    primary_purpose: str | None,
) -> dict[str, Any]:
    detection = run_json([sys.executable, str(DETECTOR), str(project)])
    detection = apply_template_override(detection, templates, primary_purpose)
    templates = detection.get("matched_templates", [])
    maven_info = None
    spring_info = None
    karate_info = None
    if "maven-java" in templates:
        maven_info = run_json([sys.executable, str(MAVEN_INSPECTOR), str(project)])
    if "springboot3-webflux" in templates:
        spring_info = run_json([sys.executable, str(SPRING_INSPECTOR), str(project)])
    if "karate-at" in templates:
        karate_info = run_json([sys.executable, str(KARATE_INSPECTOR), str(project)])

    files = {
        "AGENTS.md": render_agents_md(project, detection, maven_info),
        "agents/PROJECT_PROFILE.md": render_project_profile(
            project, detection, maven_info, spring_info, karate_info
        ),
        "agents/BUILD_AND_TEST.md": render_build_and_test(project, detection, karate_info),
        "agents/CODE_STYLE.md": render_code_style(detection),
        "agents/ARCHITECTURE_NOTES.md": render_architecture(
            project, detection, spring_info, karate_info
        ),
        "agents/DEPENDENCIES.md": render_dependencies(detection, maven_info),
        "agents/TEMPLATE_NOTES.md": render_template_notes(detection),
    }

    results = {}
    for relative, content in files.items():
        results[relative] = write_file(project / relative, content, overwrite)

    return {
        "project": str(project),
        "matched_templates": detection.get("matched_templates", []),
        "primary_purpose": detection.get("primary_purpose"),
        "files": results,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render draft AGENTS.md and agents/*.md files."
    )
    parser.add_argument("project", nargs="?", default=".", help="Project root")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing AGENTS.md and agents/*.md files",
    )
    parser.add_argument(
        "--template",
        action="append",
        help=(
            "Explicit template facet. Can be repeated or comma-separated. "
            "Supported: baseline, maven-java, springboot3-webflux, karate-at"
        ),
    )
    parser.add_argument(
        "--primary-purpose",
        help="Explicit project purpose label for AGENTS.md and PROJECT_PROFILE.md",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv[1:])
    project = Path(args.project).expanduser().resolve()
    if not project.exists() or not project.is_dir():
        print(json.dumps({"error": f"Not a directory: {project}"}, indent=2))
        return 2
    try:
        templates = normalize_templates(args.template)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 2
    result = render(project, args.overwrite, templates, args.primary_purpose)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
