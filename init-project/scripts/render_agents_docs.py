#!/usr/bin/env python3
"""Render draft AGENTS.md and agents/*.md files for a project."""

from __future__ import annotations

import argparse
import json
import re
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
SPECIALISTS = [
    {
        "slug": "endpoint-specialist",
        "codex": "endpoint_specialist",
        "title": "Endpoint Specialist",
        "description": "Work on HTTP endpoint surfaces and API contracts with evidence.",
        "focus": "HTTP routes, request/response models, validation, OpenAPI annotations, WebFlux behavior.",
        "read": [
            "agents/SUBAGENTS.md",
            "agents/references/technical/endpoints.md",
            "agents/references/business/domain-overview.md",
            "agents/BACKEND_SURFACES.md",
            "agents/CALL_CHAINS.md",
            "agents/BUILD_AND_TEST.md",
        ],
        "mode": [
            "Analysis: map route contracts and risks with evidence.",
            "Implementation: change endpoint, model, exception, or endpoint-test files only when explicitly asked and wrapper permissions allow edits.",
            "Source inspection: after reading references, inspect concrete endpoint, request/response model, exception handler, and endpoint test files before finalizing API impact.",
            "Coordination: ask service-specialist for service semantics, test-specialist for test scope, and maven-runner for Maven verification.",
        ],
        "sandbox": "workspace-write",
        "opencode_edit": "ask",
        "github_tools": "'search/codebase', 'search/usages', 'read/problems', 'edit'",
        "user_invocable": True,
    },
    {
        "slug": "service-specialist",
        "codex": "service_specialist",
        "title": "Service Specialist",
        "description": "Work on service invariants, state transitions, and error behavior.",
        "focus": "Service invariants, state transitions, error behavior, transaction boundaries.",
        "read": [
            "agents/SUBAGENTS.md",
            "agents/references/technical/services.md",
            "agents/references/business/domain-overview.md",
            "agents/CALL_CHAINS.md",
            "agents/BACKEND_SURFACES.md",
        ],
        "mode": [
            "Analysis: trace behavior through services and collaborators.",
            "Implementation: change service/domain logic only when explicitly asked and wrapper permissions allow edits.",
            "Source inspection: after reading references, inspect concrete service, mapper, model, exception, and service test files before finalizing logic impact.",
            "Coordination: ask persistence-specialist for storage changes, pubsub-specialist for event side effects, and test-specialist for coverage.",
        ],
        "sandbox": "read-only",
        "opencode_edit": "deny",
        "github_tools": "'search/codebase', 'search/usages', 'read/problems'",
        "user_invocable": False,
    },
    {
        "slug": "persistence-specialist",
        "codex": "persistence_specialist",
        "title": "Persistence Specialist",
        "description": "Work on entities, repositories, migrations, and database config.",
        "focus": "JPA entities, repositories, Flyway migrations, Postgres/profile config.",
        "read": [
            "agents/SUBAGENTS.md",
            "agents/references/technical/persistence.md",
            "agents/BACKEND_SURFACES.md",
            "agents/PROJECT_PROFILE.md",
        ],
        "mode": [
            "Analysis: verify entity, repository, migration, and profile config alignment.",
            "Implementation: change persistence files only when explicitly asked and wrapper permissions allow edits.",
            "Source inspection: after reading references, inspect concrete migration, entity, repository, config, and affected service/model files before finalizing persistence impact.",
            "Coordination: ask service-specialist for behavioral impact and test-specialist for repository/service coverage.",
        ],
        "sandbox": "read-only",
        "opencode_edit": "deny",
        "github_tools": "'search/codebase', 'search/usages', 'read/problems'",
        "user_invocable": False,
    },
    {
        "slug": "pubsub-specialist",
        "codex": "pubsub_specialist",
        "title": "Pub/Sub Specialist",
        "description": "Work on Pub/Sub publishing behavior and topic configuration.",
        "focus": "Pub/Sub publisher/gateway behavior, topic config, payload contracts.",
        "read": [
            "agents/SUBAGENTS.md",
            "agents/references/technical/pubsub.md",
            "agents/references/business/events.md",
            "agents/BACKEND_SURFACES.md",
            "agents/CALL_CHAINS.md",
        ],
        "mode": [
            "Analysis: verify publisher, topic, payload, and failure behavior.",
            "Implementation: change Pub/Sub files only when explicitly asked and wrapper permissions allow edits.",
            "Source inspection: after reading references, inspect concrete publisher, gateway, config, event, and Pub/Sub test files before finalizing event impact.",
            "Coordination: ask service-specialist for event trigger timing and test-specialist for publication tests.",
        ],
        "sandbox": "read-only",
        "opencode_edit": "deny",
        "github_tools": "'search/codebase', 'search/usages', 'read/problems'",
        "user_invocable": False,
    },
    {
        "slug": "integration-specialist",
        "codex": "integration_specialist",
        "title": "Integration Specialist",
        "description": "Work on downstream calls, clients, and integration failure behavior.",
        "focus": "External system calls, clients, timeouts, retries, profile-sensitive integration config.",
        "read": [
            "agents/SUBAGENTS.md",
            "agents/references/technical/integrations.md",
            "agents/BACKEND_SURFACES.md",
            "agents/DEPENDENCIES.md",
        ],
        "mode": [
            "Analysis: identify external systems and integration failure behavior.",
            "Implementation: change integration boundary files only when explicitly asked and wrapper permissions allow edits.",
            "Source inspection: after reading references, inspect concrete client, config, service, and integration-boundary test files before finalizing integration impact.",
            "Coordination: ask pubsub-specialist for event systems, persistence-specialist for Postgres, and test-specialist for integration coverage.",
        ],
        "sandbox": "read-only",
        "opencode_edit": "deny",
        "github_tools": "'search/codebase', 'search/usages', 'read/problems'",
        "user_invocable": False,
    },
    {
        "slug": "test-specialist",
        "codex": "test_specialist",
        "title": "Test Specialist",
        "description": "Work on tests, coverage, Checkstyle, and verification commands.",
        "focus": "JUnit 5, Mockito, Reactor/WebTestClient tests, JaCoCo and Checkstyle gates.",
        "read": [
            "agents/SUBAGENTS.md",
            "agents/references/technical/testing.md",
            "agents/references/technical/maven.md",
            "agents/BUILD_AND_TEST.md",
            "agents/CODE_STYLE.md",
            "agents/BACKEND_SURFACES.md",
        ],
        "mode": [
            "Analysis: identify coverage, quality-gate, and verification gaps.",
            "Implementation: change tests only when explicitly asked and wrapper permissions allow edits.",
            "Source inspection: after reading references, inspect concrete production and test files before finalizing test scope or Maven commands.",
            "Coordination: ask maven-runner to execute approved Maven commands when verification is needed.",
        ],
        "sandbox": "read-only",
        "opencode_edit": "deny",
        "github_tools": "'search/codebase', 'search/usages', 'read/problems'",
        "user_invocable": False,
    },
]


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


def resolve_property(value: str | None, pom_tree: dict[str, Any] | None) -> str | None:
    if not value or not pom_tree:
        return value
    properties = pom_tree.get("properties", {})

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        return properties.get(key, match.group(0))

    return re.sub(r"\$\{([^}]+)\}", replace, value)


def dependency_id(dep: dict[str, Any], pom_tree: dict[str, Any] | None = None) -> str:
    group = dep.get("groupId") or "?"
    artifact = dep.get("artifactId") or "?"
    version = resolve_property(dep.get("version"), pom_tree)
    scope = dep.get("scope") or "compile"
    base = f"{group}:{artifact}"
    if version:
        base += f":{version}"
    return f"{base} ({scope})"


def direct_dependencies(pom_tree: dict[str, Any] | None) -> list[str]:
    if not pom_tree:
        return []
    return [dependency_id(dep, pom_tree) for dep in pom_tree.get("dependencies", [])]


def dependency_management(pom_tree: dict[str, Any] | None) -> list[str]:
    if not pom_tree:
        return []
    return [dependency_id(dep, pom_tree) for dep in pom_tree.get("dependencyManagement", [])]


def exclusions(pom_tree: dict[str, Any] | None) -> list[str]:
    if not pom_tree:
        return []
    values = []
    for dep in pom_tree.get("dependencies", []):
        source = dependency_id(dep, pom_tree)
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


def all_plugins(pom_tree: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not pom_tree:
        return []
    plugins = []
    build_plugins = pom_tree.get("plugins", {})
    plugins.extend(build_plugins.get("plugins", []))
    plugins.extend(build_plugins.get("pluginManagement", []))
    for profile in pom_tree.get("profiles", []):
        profile_plugins = profile.get("plugins", {})
        plugins.extend(profile_plugins.get("plugins", []))
        plugins.extend(profile_plugins.get("pluginManagement", []))
    return plugins


def plugin_ids(pom_tree: dict[str, Any] | None) -> list[str]:
    values = []
    for plugin in all_plugins(pom_tree):
        artifact = plugin.get("artifactId")
        if not artifact:
            continue
        group = plugin.get("groupId") or "org.apache.maven.plugins"
        version = resolve_property(plugin.get("version"), pom_tree)
        values.append(":".join(part for part in [group, artifact, version] if part))
    return sorted(set(values))


def has_plugin(pom_tree: dict[str, Any] | None, artifact_id: str) -> bool:
    return any(plugin.get("artifactId") == artifact_id for plugin in all_plugins(pom_tree))


def has_dependency(pom_tree: dict[str, Any] | None, artifact_fragment: str) -> bool:
    if not pom_tree:
        return False
    for dep in pom_tree.get("dependencies", []):
        artifact = dep.get("artifactId") or ""
        group = dep.get("groupId") or ""
        if artifact_fragment in artifact or artifact_fragment in group:
            return True
    return False


def checkstyle_files(root: Path) -> list[str]:
    return sorted(set(find_files(root, ("checkstyle*.xml", "*checkstyle*.xml"), 20)))


def checkstyle_rule_hints(root: Path) -> list[str]:
    hints = []
    for relative in checkstyle_files(root):
        path = root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rules = {
            "AvoidStarImport": "wildcard imports are banned",
            "RegexpHeader": "source files require a license/copyright header",
            "Header": "source files require a license/copyright header",
            "FinalLocalVariable": "locals that can be final should be final",
            "FinalParameters": "method parameters should be final",
        }
        for needle, label in rules.items():
            if needle in text:
                hints.append(f"{label} (`{relative}`)")
    return sorted(set(hints))


def table_rows(rows: list[list[str]]) -> str:
    return "\n".join("| " + " | ".join(row) + " |" for row in rows)


def short_json(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False)


def render_agents_md(
    root: Path,
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
    spring_info: dict[str, Any] | None,
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
    backend_refs = ""
    if spring_info:
        backend_refs = """- Reference index: `agents/REFERENCES.md`
- Backend surfaces: `agents/BACKEND_SURFACES.md`
- Call chains: `agents/CALL_CHAINS.md`
- Backend workflow: `agents/workflows/BACKEND_ANALYSIS.md`
- Optional subagent protocol: `agents/SUBAGENTS.md`
"""

    return f"""# AGENTS.md

## Project
- Name: {title}
- Primary purpose: {detection.get("primary_purpose") or "Needs confirmation"}
- Template facets: {", ".join(templates) if templates else "baseline"}
- Java version: {java_hint(maven_info)}

## Start Here
- Project profile: `agents/PROJECT_PROFILE.md`
- Evidence snapshot: `agents/PROJECT_EVIDENCE.md`
- Build and test commands: `agents/BUILD_AND_TEST.md`
- Code style: `agents/CODE_STYLE.md`
- Architecture notes: `agents/ARCHITECTURE_NOTES.md`
- Dependency notes: `agents/DEPENDENCIES.md`
- Template notes: `agents/TEMPLATE_NOTES.md`
{backend_refs}

## Baseline Working Rules
- Read existing code before editing; prefer local patterns over new abstractions.
- Use reference-first progressive disclosure: load the smallest relevant file under `agents/references/`, then inspect source files before changing behavior.
- Use specialist subagents only for broad, risky, ambiguous, or cross-surface work where independent parallel review is worth the extra context cost.
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
    profiles = spring_info.get("profiles", []) if spring_info else []
    env_vars = spring_info.get("environment_variables", []) if spring_info else []
    endpoints = spring_info.get("endpoints", []) if spring_info else []
    services = spring_info.get("services", []) if spring_info else []
    repositories = spring_info.get("repositories", []) if spring_info else []
    entities = spring_info.get("entities", []) if spring_info else []
    migrations = spring_info.get("migrations", []) if spring_info else []
    feature_roots = karate_info.get("feature_files", []) if karate_info else []
    runner_classes = karate_info.get("runner_classes", []) if karate_info else []
    spring_section = ""
    if spring_info:
        spring_section = f"""
## Spring Boot WebFlux Evidence
- Application classes: {", ".join(f"`{item}`" for item in app_classes) if app_classes else "None detected"}
- Package roots: {", ".join(f"`{item}`" for item in package_roots) if package_roots else "None detected"}
- Profiles: {", ".join(f"`{item}`" for item in profiles) if profiles else "None detected"}
- Environment variables referenced: {", ".join(f"`{item}`" for item in env_vars) if env_vars else "None detected"}
- Endpoint count: {len(endpoints)}
- Service count: {len(services)}
- Repository count: {len(repositories)}
- Entity count: {len(entities)}
- Flyway migrations: {", ".join(f"`{item}`" for item in migrations) if migrations else "None detected"}
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
- Maven plugins: {", ".join(f"`{p}`" for p in plugin_ids(pom_tree)) if plugin_ids(pom_tree) else "None detected"}

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
    maven_info: dict[str, Any] | None,
    spring_info: dict[str, Any] | None,
    karate_info: dict[str, Any] | None,
) -> str:
    templates = detection.get("matched_templates", [])
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    if "maven-java" in templates:
        build = maven_command(root, "clean verify")
        test = maven_command(root, "test")
        package = maven_command(root, "-DskipTests package")
        targeted = maven_command(root, "-Dtest=SomeTest test")
        checkstyle = maven_command(root, "checkstyle:check") if has_plugin(pom_tree, "maven-checkstyle-plugin") else "Needs confirmation"
        coverage = maven_command(root, "test jacoco:report") if has_plugin(pom_tree, "jacoco-maven-plugin") else "Needs confirmation"
    else:
        build = test = package = targeted = "Needs confirmation"
        checkstyle = coverage = "Needs confirmation"

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
        profiles = spring_info.get("profiles", []) if spring_info else []
        webflux = f"""
## Spring Boot Commands
- Run locally: `{maven_command(root, 'spring-boot:run')}`
- Package without tests: `{package}`
- Run with a profile: `{maven_command(root, 'spring-boot:run -Dspring-boot.run.profiles=dev')}`
- Profiles detected: {", ".join(f"`{item}`" for item in profiles) if profiles else "Needs confirmation"}
"""

    return f"""# Build And Test

## Core Commands
- Build: `{build}`
- Unit tests: `{test}`
- Targeted test: `{targeted}`
- Package without tests: `{package}`
- Checkstyle: `{checkstyle}`
- Coverage report: `{coverage}`
{webflux}{karate}
## Quality Gates Detected
- Checkstyle plugin: {has_plugin(pom_tree, "maven-checkstyle-plugin")}
- JaCoCo plugin: {has_plugin(pom_tree, "jacoco-maven-plugin")}
- Spring Boot Maven plugin: {has_plugin(pom_tree, "spring-boot-maven-plugin")}

## Verification Strategy
- Prefer targeted tests while editing.
- Run full build before finishing changes that affect shared behavior.
- If external services, shared environments, or slow dependency resolution block a command, record the command and reason.
"""


def render_code_style(
    root: Path,
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
) -> str:
    templates = detection.get("matched_templates", [])
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    style_files = checkstyle_files(root)
    rule_hints = checkstyle_rule_hints(root)
    lines = [
        "# Code Style",
        "",
        "## General",
        "- Follow the nearest existing package/module style.",
        "- Prefer existing helpers and test utilities over new abstractions.",
        "- Keep naming, assertions, logging, and error handling consistent with nearby code.",
        "- Avoid broad formatting-only churn unless the project formatter requires it.",
    ]
    if has_plugin(pom_tree, "maven-checkstyle-plugin") or style_files:
        lines.extend(
            [
                "",
                "## Checkstyle",
                f"- Maven Checkstyle plugin detected: {has_plugin(pom_tree, 'maven-checkstyle-plugin')}.",
                f"- Config files: {', '.join(f'`{item}`' for item in style_files) if style_files else 'Needs confirmation'}.",
                f"- Rule hints: {', '.join(rule_hints) if rule_hints else 'Needs confirmation'}.",
                f"- Run: `{maven_command(root, 'checkstyle:check')}`.",
            ]
        )
    if "springboot3-webflux" in templates:
        lines.extend(
            [
                "",
                "## Spring Boot WebFlux",
                "- Preserve reactive composition with `Mono` and `Flux`.",
                "- Avoid blocking calls in request handling paths. If the project uses Hibernate/JPA, keep blocking repository work isolated and documented.",
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
{subsection_list("Flyway migrations", spring_info.get("migrations", []))}

### Surface Counts
- Endpoints: {len(spring_info.get("endpoints", []))}
- Services: {len(spring_info.get("services", []))}
- Repositories: {len(spring_info.get("repositories", []))}
- Entities: {len(spring_info.get("entities", []))}
- Pub/Sub classes: {len(spring_info.get("pubsub", []))}
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


def render_project_evidence(
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
    spring_info: dict[str, Any] | None,
    karate_info: dict[str, Any] | None,
) -> str:
    return f"""# Project Evidence

This file is a generated evidence snapshot for future agents. Prefer the human-oriented files first, then use this file when you need the raw signals behind a claim.

## Detection
```json
{short_json(detection)}
```

## Maven Inspection
```json
{short_json(maven_info or {})}
```

## Spring Boot WebFlux Inspection
```json
{short_json(spring_info or {})}
```

## Karate Inspection
```json
{short_json(karate_info or {})}
```
"""


def render_backend_surfaces(spring_info: dict[str, Any] | None) -> str:
    if not spring_info:
        return "# Backend Surfaces\n\nNo Spring Boot backend surface evidence was detected.\n"

    endpoint_rows = [["Method", "Path", "Handler", "Request", "Response", "Source"]]
    endpoint_rows.append(["---", "---", "---", "---", "---", "---"])
    for endpoint in spring_info.get("endpoints", []):
        endpoint_rows.append(
            [
                endpoint.get("method", "?"),
                f"`{endpoint.get('path', '?')}`",
                f"`{endpoint.get('handler', '?')}`",
                f"`{endpoint.get('request', 'Needs confirmation')}`",
                f"`{endpoint.get('response', 'Needs confirmation')}`",
                f"`{endpoint.get('source', 'Needs confirmation')}`",
            ]
        )

    service_rows = [["Service", "Public methods", "Collaborators", "Source"], ["---", "---", "---", "---"]]
    for service in spring_info.get("services", []):
        service_rows.append(
            [
                f"`{service.get('class', '?')}`",
                ", ".join(f"`{item}`" for item in service.get("methods", [])) or "Needs confirmation",
                ", ".join(f"`{item}`" for item in service.get("collaborators", [])) or "None detected",
                f"`{service.get('source', 'Needs confirmation')}`",
            ]
        )

    repo_rows = [["Repository", "Entity", "ID", "Source"], ["---", "---", "---", "---"]]
    for repo in spring_info.get("repositories", []):
        repo_rows.append(
            [
                f"`{repo.get('repository', '?')}`",
                f"`{repo.get('entity', 'Needs confirmation')}`",
                f"`{repo.get('id_type', 'Needs confirmation')}`",
                f"`{repo.get('source', 'Needs confirmation')}`",
            ]
        )

    entity_rows = [["Entity", "Table", "Source"], ["---", "---", "---"]]
    for entity in spring_info.get("entities", []):
        entity_rows.append(
            [
                f"`{entity.get('entity', '?')}`",
                f"`{entity.get('table', 'Needs confirmation')}`",
                f"`{entity.get('source', 'Needs confirmation')}`",
            ]
        )

    pubsub_rows = [["Class", "Signals", "Source"], ["---", "---", "---"]]
    for pubsub in spring_info.get("pubsub", []):
        pubsub_rows.append(
            [
                f"`{pubsub.get('class', '?')}`",
                pubsub.get("signals", "Needs confirmation"),
                f"`{pubsub.get('source', 'Needs confirmation')}`",
            ]
        )

    tests = spring_info.get("tests", [])
    test_lines = [
        f"- `{test.get('source')}`: {test.get('signals', 'JUnit')}"
        for test in tests
    ]
    topic_lines = [
        f"- `{hint.get('source')}`: `{hint.get('line')}`"
        for hint in spring_info.get("pubsub_topic_hints", [])
    ]

    return f"""# Backend Surfaces

Use this before changing endpoints, persistence, service behavior, Pub/Sub publication, or profile-specific config. The content is generated from static source/config scans, so confirm runtime-only behavior in code when risk is high.

## Endpoints
{table_rows(endpoint_rows) if len(endpoint_rows) > 2 else "- None detected"}

## Services
{table_rows(service_rows) if len(service_rows) > 2 else "- None detected"}

## Persistence

### Repositories
{table_rows(repo_rows) if len(repo_rows) > 2 else "- None detected"}

### Entities
{table_rows(entity_rows) if len(entity_rows) > 2 else "- None detected"}

### Migrations
{bullet(spring_info.get("migrations", []), "None detected")}

## Pub/Sub
{table_rows(pubsub_rows) if len(pubsub_rows) > 2 else "- None detected"}

### Topic Hints
{chr(10).join(topic_lines) if topic_lines else "- None detected"}

## Profiles And Config
- Profiles: {", ".join(f"`{item}`" for item in spring_info.get("profiles", [])) if spring_info.get("profiles") else "None detected"}
- Environment variables: {", ".join(f"`{item}`" for item in spring_info.get("environment_variables", [])) if spring_info.get("environment_variables") else "None detected"}
- Application configs: {", ".join(f"`{item}`" for item in spring_info.get("application_configs", [])) if spring_info.get("application_configs") else "None detected"}

## Tests
{chr(10).join(test_lines) if test_lines else "- None detected"}
"""


def service_for_endpoint(endpoint: dict[str, Any], services: list[dict[str, Any]]) -> dict[str, Any] | None:
    handler = endpoint.get("handler", "")
    prefix = re.sub(r"(Endpoint|Controller|Handler)#.*", "", handler)
    for service in services:
        name = service.get("class", "")
        if prefix and prefix in name:
            return service
    return services[0] if services else None


def render_call_chains(spring_info: dict[str, Any] | None) -> str:
    if not spring_info:
        return "# Call Chains\n\nNo Spring Boot call-chain evidence was detected.\n"

    services = spring_info.get("services", [])
    sections = ["# Call Chains", ""]
    sections.append(
        "These chains are static/inferred. Use them as a reading guide, then confirm the exact branch, transaction, and error behavior in code."
    )
    sections.append("")

    for endpoint in spring_info.get("endpoints", [])[:20]:
        service = service_for_endpoint(endpoint, services)
        service_name = service.get("class") if service else "Needs confirmation"
        collaborators = service.get("collaborators", []) if service else []
        sections.extend(
            [
                f"## {endpoint.get('method')} {endpoint.get('path')}",
                "",
                "Confidence: `static + inferred`",
                "",
                "```text",
                f"{endpoint.get('handler')} -> {service_name}"
                + (f" -> {', '.join(collaborators)}" if collaborators else ""),
                "```",
                "",
                "Evidence:",
                f"- Endpoint source: `{endpoint.get('source')}`",
                f"- Request type: `{endpoint.get('request')}`",
                f"- Response type: `{endpoint.get('response')}`",
                f"- Service source: `{service.get('source')}`" if service else "- Service source: Needs confirmation",
                "",
                "Change checklist:",
                "- If request/response changes, update endpoint tests and OpenAPI annotations/specs.",
                "- If persistence behavior changes, update service/repository tests and migrations as needed.",
                "- If Pub/Sub behavior changes, verify topic config, payload shape, and idempotency/error handling.",
                "",
            ]
        )

    if spring_info.get("pubsub"):
        sections.extend(["## Pub/Sub Publication", "", "Confidence: `static + config`", ""])
        for item in spring_info.get("pubsub", []):
            sections.append(f"- `{item.get('class')}` in `{item.get('source')}`: {item.get('signals')}")
        sections.append("")
        if spring_info.get("pubsub_topic_hints"):
            sections.append("Topic/config evidence:")
            for hint in spring_info.get("pubsub_topic_hints", []):
                sections.append(f"- `{hint.get('source')}`: `{hint.get('line')}`")
            sections.append("")

    return "\n".join(sections)


def class_source_rows(items: list[dict[str, Any]], class_key: str) -> str:
    rows = [["Name", "Source"], ["---", "---"]]
    for item in items:
        rows.append(
            [
                f"`{item.get(class_key, item.get('class', '?'))}`",
                f"`{item.get('source', 'Needs confirmation')}`",
            ]
        )
    return table_rows(rows) if len(rows) > 2 else "- None detected"


def endpoint_path_families(spring_info: dict[str, Any]) -> list[str]:
    families = []
    for endpoint in spring_info.get("endpoints", []):
        path = endpoint.get("path") or ""
        parts = [part for part in path.split("/") if part and not part.startswith("{")]
        if len(parts) >= 2 and parts[0] == "api":
            families.append("/" + "/".join(parts[:2]))
        elif parts:
            families.append("/" + parts[0])
    return sorted(set(families))


def render_references_index(spring_info: dict[str, Any]) -> str:
    business_rows = [
        ["Topic", "File", "Use when"],
        ["---", "---", "---"],
        [
            "Domain overview",
            "`agents/references/business/domain-overview.md`",
            "Understanding detected domain names, source areas, and behavior that needs confirmation.",
        ],
        [
            "Business rules",
            "`agents/references/business/business-rules.md`",
            "Changing service decisions, validation, status transitions, totals, or eligibility logic.",
        ],
        [
            "Events",
            "`agents/references/business/events.md`",
            "Changing published/consumed events, payload meaning, idempotency, or consumer expectations.",
        ],
    ]
    technical_rows = [
        ["Topic", "File", "Use when"],
        ["---", "---", "---"],
        [
            "Endpoints",
            "`agents/references/technical/endpoints.md`",
            "Changing HTTP routes, request/response contracts, validation, or endpoint tests.",
        ],
        [
            "Services",
            "`agents/references/technical/services.md`",
            "Changing orchestration, state transitions, errors, transactions, or collaborator usage.",
        ],
        [
            "Persistence",
            "`agents/references/technical/persistence.md`",
            "Changing entities, repositories, Flyway migrations, or database profile config.",
        ],
        [
            "Pub/Sub",
            "`agents/references/technical/pubsub.md`",
            "Changing event publication, topic config, payloads, retry, or Pub/Sub tests.",
        ],
        [
            "Integrations",
            "`agents/references/technical/integrations.md`",
            "Reviewing external systems, clients, timeouts, retries, or runtime config.",
        ],
        [
            "Testing",
            "`agents/references/technical/testing.md`",
            "Planning JUnit, Mockito, Reactor/WebTestClient, Checkstyle, or JaCoCo verification.",
        ],
        [
            "Maven",
            "`agents/references/technical/maven.md`",
            "Choosing build/test/checkstyle/coverage commands or interpreting Maven output.",
        ],
    ]
    return f"""# References

Use these files for progressive disclosure. They contain reusable project context only; they are not tool-specific subagent definitions.

## Technical References
{table_rows(technical_rows)}

## Business References
{table_rows(business_rows)}

## Loading Rule
- Start with the smallest relevant technical file.
- Add business context when behavior, naming, status transitions, event meaning, or user-facing acceptance criteria matter.
- Treat generated evidence as a map, then inspect source files listed in each reference before giving confidence above medium.
- Prefer source code over generated evidence when they disagree.

## Current Detected Scale
- Endpoints: {len(spring_info.get("endpoints", []))}
- Services: {len(spring_info.get("services", []))}
- Repositories: {len(spring_info.get("repositories", []))}
- Entities: {len(spring_info.get("entities", []))}
- Pub/Sub classes: {len(spring_info.get("pubsub", []))}
"""


def render_technical_endpoints(spring_info: dict[str, Any]) -> str:
    rows = [["Method", "Path", "Handler", "Request", "Response", "Source"], ["---", "---", "---", "---", "---", "---"]]
    for endpoint in spring_info.get("endpoints", []):
        rows.append(
            [
                endpoint.get("method", "?"),
                f"`{endpoint.get('path', '?')}`",
                f"`{endpoint.get('handler', '?')}`",
                f"`{endpoint.get('request', 'Needs confirmation')}`",
                f"`{endpoint.get('response', 'Needs confirmation')}`",
                f"`{endpoint.get('source', 'Needs confirmation')}`",
            ]
        )
    return f"""# Endpoint Reference

Use this for HTTP API changes. This file is generated from static source evidence; confirm request validation, status codes, exception mapping, and OpenAPI annotations in source before editing.

## Source Areas
{subsection_list("Controllers, handlers, or router functions", spring_info.get("controllers_or_handlers", []))}
{subsection_list("WebFlux tests", spring_info.get("webflux_tests", []))}

## Endpoint Catalog
{table_rows(rows) if len(rows) > 2 else "- None detected"}

## Change Checklist
- Inspect the concrete handler, request/response model, validation annotations, exception handler, and endpoint tests.
- If an API contract changes, update tests and OpenAPI or SpringDoc annotations/specs when present.
- If behavior changes behind an existing route, read `agents/references/technical/services.md` and `agents/CALL_CHAINS.md`.
"""


def render_technical_services(spring_info: dict[str, Any]) -> str:
    rows = [["Service", "Public methods", "Collaborators", "Source"], ["---", "---", "---", "---"]]
    for service in spring_info.get("services", []):
        rows.append(
            [
                f"`{service.get('class', '?')}`",
                ", ".join(f"`{item}`" for item in service.get("methods", [])) or "Needs confirmation",
                ", ".join(f"`{item}`" for item in service.get("collaborators", [])) or "None detected",
                f"`{service.get('source', 'Needs confirmation')}`",
            ]
        )
    return f"""# Service Reference

Use this for business orchestration, state transitions, errors, and collaborator changes. Generated collaborator lists are a reading guide, not a complete call graph.

## Source Areas
{class_source_rows(spring_info.get("services", []), "class")}

## Service Catalog
{table_rows(rows) if len(rows) > 2 else "- None detected"}

## Change Checklist
- Inspect the concrete service method and the model, mapper, exception, repository, Pub/Sub, and test files it touches.
- Confirm transaction, idempotency, validation, and error mapping behavior in code.
- Read business references when names, statuses, totals, eligibility, or user-facing rules matter.
"""


def render_technical_persistence(spring_info: dict[str, Any]) -> str:
    repo_rows = [["Repository", "Entity", "ID", "Source"], ["---", "---", "---", "---"]]
    for repo in spring_info.get("repositories", []):
        repo_rows.append(
            [
                f"`{repo.get('repository', '?')}`",
                f"`{repo.get('entity', 'Needs confirmation')}`",
                f"`{repo.get('id_type', 'Needs confirmation')}`",
                f"`{repo.get('source', 'Needs confirmation')}`",
            ]
        )
    entity_rows = [["Entity", "Table", "Source"], ["---", "---", "---"]]
    for entity in spring_info.get("entities", []):
        entity_rows.append(
            [
                f"`{entity.get('entity', '?')}`",
                f"`{entity.get('table', 'Needs confirmation')}`",
                f"`{entity.get('source', 'Needs confirmation')}`",
            ]
        )
    return f"""# Persistence Reference

Use this for database schema, repository, entity, and migration changes. For WebFlux plus JPA/Hibernate, confirm how blocking repository work is isolated before changing request paths.

## Repositories
{table_rows(repo_rows) if len(repo_rows) > 2 else "- None detected"}

## Entities
{table_rows(entity_rows) if len(entity_rows) > 2 else "- None detected"}

## Migrations
{bullet(spring_info.get("migrations", []), "None detected")}

## Profiles And Config
- Profiles: {", ".join(f"`{item}`" for item in spring_info.get("profiles", [])) if spring_info.get("profiles") else "None detected"}
- Application configs: {", ".join(f"`{item}`" for item in spring_info.get("application_configs", [])) if spring_info.get("application_configs") else "None detected"}

## Change Checklist
- Inspect the affected entity, repository, migration, service method, and tests together.
- Verify table names, column constraints, indexes, default values, and rollback/deployment risks.
- Update persistence/service tests and migration documentation when schema behavior changes.
"""


def render_technical_pubsub(spring_info: dict[str, Any]) -> str:
    rows = [["Class", "Signals", "Source"], ["---", "---", "---"]]
    for item in spring_info.get("pubsub", []):
        rows.append(
            [
                f"`{item.get('class', '?')}`",
                item.get("signals", "Needs confirmation"),
                f"`{item.get('source', 'Needs confirmation')}`",
            ]
        )
    hints = [
        f"- `{hint.get('source')}`: `{hint.get('line')}`"
        for hint in spring_info.get("pubsub_topic_hints", [])
    ]
    return f"""# Pub/Sub Reference

Use this for message publication, consumption, topic config, payload, retry, DLQ, and idempotency changes.

## Pub/Sub Classes
{table_rows(rows) if len(rows) > 2 else "- None detected"}

## Topic Or Binding Hints
{chr(10).join(hints) if hints else "- None detected"}

## Change Checklist
- Inspect publisher/consumer code, event payloads, application config, and Pub/Sub tests.
- Confirm publish timing, transaction boundary, duplicate handling, retry/DLQ behavior, and topic names.
- Read `agents/references/business/events.md` before changing event meaning.
"""


def render_technical_integrations(spring_info: dict[str, Any]) -> str:
    return f"""# Integration Reference

Use this for external systems such as databases, Pub/Sub, HTTP clients, SDK clients, auth providers, and runtime profile config.

## Source Areas
{subsection_list("Web clients or HTTP clients", spring_info.get("web_clients", []))}
{subsection_list("Configuration/property classes", spring_info.get("configuration_properties", []))}
{subsection_list("Application configs", spring_info.get("application_configs", []))}

## Runtime Config
- Profiles: {", ".join(f"`{item}`" for item in spring_info.get("profiles", [])) if spring_info.get("profiles") else "None detected"}
- Environment variables: {", ".join(f"`{item}`" for item in spring_info.get("environment_variables", [])) if spring_info.get("environment_variables") else "None detected"}

## Change Checklist
- Inspect config binding, profile-specific values, timeout/retry/error mapping, and tests before changing an integration boundary.
- Do not record secret values in agent docs; record only safe config keys and source paths.
- Coordinate with persistence-specialist for database changes and pubsub-specialist for event systems.
"""


def render_technical_testing(
    root: Path,
    maven_info: dict[str, Any] | None,
    spring_info: dict[str, Any],
) -> str:
    tests = [
        f"- `{test.get('source')}`: {test.get('signals', 'JUnit')}"
        for test in spring_info.get("tests", [])
    ]
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    return f"""# Testing Reference

Use this for test planning, coverage, Checkstyle, and verification scope.

## Test Sources
{chr(10).join(tests) if tests else "- None detected"}

## Quality Gates
- Checkstyle plugin: {has_plugin(pom_tree, "maven-checkstyle-plugin")}
- JaCoCo plugin: {has_plugin(pom_tree, "jacoco-maven-plugin")}
- Spring Boot test hints: {has_dependency(pom_tree, "starter-test")}
- Reactor test hints: {has_dependency(pom_tree, "reactor-test")}

## Commands
- Unit tests: `{maven_command(root, 'test')}`
- Targeted test: `{maven_command(root, '-Dtest=SomeTest test')}`
- Checkstyle: `{maven_command(root, 'checkstyle:check')}`
- Coverage: `{maven_command(root, 'test jacoco:report')}`
- Full verification: `{maven_command(root, 'clean verify')}`

## Change Checklist
- Prefer focused unit tests for service logic and WebTestClient/Spring tests for endpoint wiring.
- Keep Mockito, Reactor, and fixture style consistent with nearby tests.
- Use `maven-runner` for actual Maven execution when subagents are available.
"""


def render_technical_maven(root: Path, maven_info: dict[str, Any] | None) -> str:
    wrapper = maven_info.get("maven_wrapper", {}) if maven_info else {}
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    return f"""# Maven Reference

Use this for build commands, dependency changes, plugin behavior, and interpreting Maven failures.

## Project
- Maven wrapper: {wrapper.get("present", False)}
- Coordinates: `{coord_text(pom_tree)}`
- Java version hint: {java_hint(maven_info)}

## Approved Verification Commands
- `{maven_command(root, '-version')}`
- `{maven_command(root, 'test')}`
- `{maven_command(root, '-Dtest=SomeTest test')}`
- `{maven_command(root, 'checkstyle:check')}`
- `{maven_command(root, 'test jacoco:report')}`
- `{maven_command(root, 'clean verify')}`

## Maven Runner Rule
- `agents/subagents/maven-runner.md` is the only generated role intended to execute Maven commands.
- Other specialists should recommend commands and ask Maven Runner or the coordinator to run them.
"""


def render_business_domain_overview(spring_info: dict[str, Any]) -> str:
    families = endpoint_path_families(spring_info)
    return f"""# Business Domain Overview

This file captures business context that can be inferred from code names only. Treat it as a map of likely domain areas, not confirmed product policy.

## Detected Domain Clues
- API path families: {", ".join(f"`{item}`" for item in families) if families else "None detected"}
- Services: {", ".join(f"`{item.get('class')}`" for item in spring_info.get("services", [])) if spring_info.get("services") else "None detected"}
- Entities: {", ".join(f"`{item.get('entity')}`" for item in spring_info.get("entities", [])) if spring_info.get("entities") else "None detected"}

## How To Use
- Load this after the relevant technical reference when names, user-facing behavior, statuses, totals, or eligibility decisions matter.
- Confirm every business rule in source code, tests, OpenAPI, product docs, or user-provided requirements before changing behavior.
- Record newly confirmed domain rules here rather than expanding root `AGENTS.md`.
"""


def render_business_rules(spring_info: dict[str, Any]) -> str:
    return f"""# Business Rules

Generated status: Needs confirmation. The renderer does not infer detailed product policy from naming alone.

## Likely Rule Locations
{class_source_rows(spring_info.get("services", []), "class")}

## Review Checklist
- Identify validation, eligibility, status transition, amount/quantity calculation, and error mapping code.
- Compare behavior against tests and API contracts before editing.
- If a rule is confirmed by code or requirements, add a short note with file evidence.
"""


def render_business_events(spring_info: dict[str, Any]) -> str:
    rows = [["Class", "Signals", "Source"], ["---", "---", "---"]]
    for item in spring_info.get("pubsub", []):
        rows.append(
            [
                f"`{item.get('class', '?')}`",
                item.get("signals", "Needs confirmation"),
                f"`{item.get('source', 'Needs confirmation')}`",
            ]
        )
    return f"""# Business Events

Use this for event meaning, payload compatibility, publish timing, and downstream expectations.

## Event Evidence
{table_rows(rows) if len(rows) > 2 else "- No Pub/Sub classes detected"}

## Review Checklist
- Confirm which user or system action causes each event.
- Confirm payload fields, idempotency key, ordering expectations, retry/DLQ behavior, and consumers when known.
- If no event evidence exists, keep this file as a placeholder for future confirmed event contracts.
"""


def render_subagents_doc() -> str:
    role_rows = [["Role", "Neutral file", "Primary focus"], ["---", "---", "---"]]
    for item in SPECIALISTS:
        role_rows.append(
            [
                item["title"],
                f"`agents/subagents/{item['slug']}.md`",
                item["focus"],
            ]
        )
    role_rows.append(
        [
            "Maven Runner",
            "`agents/subagents/maven-runner.md`",
            "Execute approved Maven verification commands and summarize results.",
        ]
    )
    return f"""# Subagents

This project separates reusable references from tool-specific subagent wrappers. Keep project facts in `agents/references/`; keep neutral role behavior in `agents/subagents/`; wrappers should only point back to these files.

## Default Strategy
- Prefer reference-only progressive disclosure for narrow tasks: read `AGENTS.md`, `agents/REFERENCES.md`, the smallest relevant reference, then source files.
- Use subagents for backend analysis, review, onboarding, risky refactors, cross-surface change planning, or domain-scoped implementation.
- Do not spawn subagents for tiny edits where one file and one test are enough.
- Specialist names describe ownership, not permission. A specialist may edit only when the parent task asks for implementation and the active wrapper permits edits.
- The coordinator owns final decisions, cross-surface tradeoffs, and merge conflict resolution.
- The Maven Runner is the only generated subagent intended to run build/test commands. It must not edit files.
- Do not add extra MCP, web, LSP, skill, or generated analyzer tools unless the user explicitly asks.

## Supported Surfaces
| Tool | Native wrapper location | Notes |
| --- | --- | --- |
| Codex | `.codex/agents/*.toml` | Project-scoped custom agents. The main Codex thread coordinates specialists. |
| OpenCode | `.opencode/agents/*.md` | Markdown agents can be invoked by name or automatic routing. |
| VS Code Copilot Chat | `.github/agents/*.agent.md` | Custom agents and prompt files are used when the VS Code build supports them. |

## Roles
{table_rows(role_rows)}

## Coordinator Protocol
1. Read `AGENTS.md`, then load only the evidence files needed for the task.
2. For whole-backend analysis, read `agents/workflows/BACKEND_ANALYSIS.md`.
3. Use `agents/REFERENCES.md` to select technical and business context.
4. Dispatch specialist roles in parallel only when the tool supports it and the task benefits from independent review.
5. After reading references, inspect relevant source files before giving confidence above medium.
6. Require every specialist result to cite concrete files and call out unknowns.
7. Merge duplicate findings, resolve conflicts against source code, and map findings to verification commands.

## Standard Specialist Output
```text
Scope:
- What was inspected and what was intentionally skipped.

Files read:
- path/to/File.java

Findings:
- [severity] Finding title
  Evidence: file path and symbol or config key.
  Impact: user-visible or maintenance risk.
  Suggested next step: concrete change or verification.

Cross-surface notes:
- Dependencies on endpoints, service logic, persistence, Pub/Sub, config, or tests.

Unknowns:
- Runtime behavior, environment facts, or contracts that need confirmation.

Confidence:
- high | medium | low, with one short reason.
```

Use `No findings` when the inspected surface looks consistent.

## Standard Maven Runner Output
```text
Commands:
- mvn ...

Result:
- pass | fail | blocked

Important output:
- Short excerpts only: failing test names, Checkstyle files, coverage rule failures, or build lifecycle error.

Artifacts:
- Generated report paths such as target/site/jacoco/index.html, when relevant.

Next step:
- The smallest useful follow-up command or the owner surface that should inspect the failure.
```
"""


def render_subagent_role(item: dict[str, Any]) -> str:
    return f"""# {item['title']}

## Role
{item['focus']} Analyze, plan, or implement this surface only when the parent task and active tool wrapper permit edits.

## Read First
{bullet(item["read"])}

## Mode
{plain_bullet(item["mode"])}

## Output
Use the standard specialist output in `agents/SUBAGENTS.md`. Cite concrete files and separate confirmed facts from unknowns.
"""


def render_maven_runner_role() -> str:
    return """# Maven Runner

## Role
Execute approved Maven verification commands and summarize the result. This is an execution role, not a code-editing role.

## Read First
- `agents/SUBAGENTS.md`
- `agents/references/technical/maven.md`
- `agents/BUILD_AND_TEST.md`
- `agents/CODE_STYLE.md`
- `pom.xml`
- `.mvn/maven.config`

## Allowed Commands
Run only these commands from the repository root unless the user explicitly approves a different Maven command:

- `mvn -version`
- `mvn test`
- `mvn -Dtest=SomeTest test`, replacing `SomeTest` with a concrete test class or pattern
- `mvn checkstyle:check`
- `mvn test jacoco:report`
- `mvn clean verify`

If a Maven wrapper exists, the same command set may be run with `./mvnw` instead of `mvn`.

## Guardrails
- Do not edit source, tests, config, docs, or build files.
- Do not install packages, change dependencies, run curl/wget, or invoke non-Maven shell commands.
- Do not start long-lived servers such as `mvn spring-boot:run`.
- Build output under `target/` is expected and does not count as a source edit.
- Stop after the first failing command unless the coordinator explicitly asks for additional verification.

## Output
Use the standard Maven Runner output in `agents/SUBAGENTS.md`. Keep logs short and include the first actionable failure.
"""


def render_backend_workflow() -> str:
    role_rows = [["Specialist", "Reads first", "Typical questions"], ["---", "---", "---"]]
    for item in SPECIALISTS:
        role_rows.append(
            [
                item["title"].replace(" Specialist", ""),
                f"`agents/subagents/{item['slug']}.md`",
                item["focus"],
            ]
        )
    role_rows.append(
        [
            "Maven runner",
            "`agents/subagents/maven-runner.md`",
            "Which approved Maven commands should execute, and what did they report?",
        ]
    )
    return f"""# Backend Analysis Workflow

Use this workflow for backend onboarding, review, API-impact analysis, or planning changes that touch more than one surface.

## Load Order
1. `AGENTS.md`
2. `agents/REFERENCES.md`
3. The smallest relevant file under `agents/references/technical/`
4. A focused file under `agents/references/business/` only when behavior semantics matter
5. `agents/BACKEND_SURFACES.md` and `agents/CALL_CHAINS.md` when cross-surface impact matters
6. `agents/BUILD_AND_TEST.md`
7. A focused subagent file from `agents/subagents/` only when the tool supports subagents and the task benefits

## Dispatch Plan
For full analysis, run these specialist checks. Parallelize only when independent review is worth the extra context and elapsed time.

{table_rows(role_rows)}

## Merge Rules
- Prefer source code over generated evidence when they disagree.
- Treat `agents/PROJECT_EVIDENCE.md`, `agents/BACKEND_SURFACES.md`, and `agents/CALL_CHAINS.md` as reading guides, not final truth.
- Use references to choose source files; do not stop at references when concrete API/model/service behavior matters.
- Separate confirmed findings from assumptions.
- Keep final recommendations tied to one or more verification commands from `agents/BUILD_AND_TEST.md`.
- Delegate Maven command execution to Maven Runner when verification should actually run.
- Do not add new analysis tooling unless the user explicitly asks.

## Example Prompts

Codex:

```text
Use parallel subagents to analyze this backend. Spawn endpoint_specialist, service_specialist, persistence_specialist, pubsub_specialist, integration_specialist, and test_specialist. Use maven_runner only for approved Maven verification commands. Wait for all results, then merge findings by severity with file references and verification commands.
```

OpenCode:

```text
Use @endpoint-specialist, @service-specialist, @persistence-specialist, @pubsub-specialist, @integration-specialist, and @test-specialist to analyze this backend. Use @maven-runner only for approved Maven verification commands. Merge their outputs using agents/SUBAGENTS.md.
```

VS Code Copilot Chat:

```text
/backend-analysis
Analyze this Spring Boot backend with the custom agents in .github/agents. Use the standard specialist output schema and cite files.
```

## Final Coordinator Output
```text
Summary:
- 2-4 bullets on the backend shape and important risks.

Findings:
- Severity, title, evidence, impact, next step.

Cross-surface map:
- Endpoint -> service -> repository/pubsub/config/test links that matter.

Verification:
- Commands run or recommended.

Open questions:
- Facts that need a human, environment, or runtime confirmation.
```
"""


def render_codex_config() -> str:
    return """[agents]
max_threads = 7
max_depth = 1
"""


def render_codex_agent(item: dict[str, Any]) -> str:
    edit_note = ""
    if item["sandbox"] != "read-only":
        edit_note = (
            "Edit only files owned by this specialist when the parent task explicitly asks for implementation.\n"
        )
    else:
        edit_note = "Do not edit files.\n"
    return f'''name = "{item["codex"]}"
description = "{item["description"]}"
sandbox_mode = "{item["sandbox"]}"
developer_instructions = """
Read agents/SUBAGENTS.md, then agents/subagents/{item["slug"]}.md.
Follow the neutral protocol exactly.
{edit_note}Do not run Maven; ask maven_runner for verification.
Return the standard specialist output with concrete file references.
"""
'''


def render_codex_maven_runner() -> str:
    return '''name = "maven_runner"
description = "Runs approved Maven verification commands and summarizes build, test, Checkstyle, or JaCoCo results."
sandbox_mode = "workspace-write"
developer_instructions = """
Read agents/SUBAGENTS.md, agents/subagents/maven-runner.md, and agents/BUILD_AND_TEST.md.
Run only the approved Maven commands listed in agents/subagents/maven-runner.md unless the user explicitly approves another Maven command.
Do not edit files. Do not run non-Maven shell commands. Do not start long-lived servers.
Return the standard Maven Runner output with concise failure excerpts and generated report paths.
"""
'''


def render_opencode_coordinator() -> str:
    allowed = "\n".join(f"    {item['slug']}: allow" for item in SPECIALISTS)
    return f"""---
description: Coordinate backend surface analysis using focused specialist subagents.
mode: primary
temperature: 0.1
permission:
  read: allow
  list: allow
  glob: allow
  grep: allow
  task:
    "*": deny
{allowed}
    maven-runner: allow
  edit: deny
  bash: deny
  external_directory: deny
  webfetch: deny
  websearch: deny
  lsp: deny
  skill: deny
---

Read `AGENTS.md` and `agents/workflows/BACKEND_ANALYSIS.md`.

When parallel analysis is useful, invoke the specialist agents and merge their outputs:
{bullet([f"@{item['slug']}" for item in SPECIALISTS] + ["@maven-runner only when Maven verification should run"])}

Use the final coordinator output from `agents/workflows/BACKEND_ANALYSIS.md`.
"""


def render_opencode_agent(item: dict[str, Any]) -> str:
    return f"""---
description: {item['description']}
mode: subagent
temperature: 0.1
permission:
  read: allow
  list: allow
  glob: allow
  grep: allow
  edit: {item['opencode_edit']}
  bash: deny
  task: deny
  external_directory: deny
  webfetch: deny
  websearch: deny
  lsp: deny
  skill: deny
---

Read `agents/SUBAGENTS.md`, then `agents/subagents/{item['slug']}.md`. Follow the neutral protocol exactly. Edit only when the parent task asks for implementation and this wrapper permits edits.
"""


def render_opencode_maven_runner() -> str:
    return """---
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
"""


def render_github_copilot_instructions() -> str:
    return """# Copilot Instructions

Read `AGENTS.md` first. For backend analysis, use `agents/REFERENCES.md`, `agents/SUBAGENTS.md`, and `agents/workflows/BACKEND_ANALYSIS.md`.

When VS Code custom agents are available, use the agents in `.github/agents/` for focused specialist analysis or domain-scoped implementation. If they are not available, use `agents/REFERENCES.md` and run the same specialist checks sequentially.

Do not introduce new analysis tools unless the user explicitly asks. Cite concrete files for every finding.
"""


def render_github_prompt() -> str:
    return """---
description: Analyze the backend with focused specialist agents and merge findings.
agent: backend-coordinator
---

Read `AGENTS.md`, then follow `agents/workflows/BACKEND_ANALYSIS.md`.

Use the custom agents in `.github/agents/` when available:
- `endpoint-specialist`
- `service-specialist`
- `persistence-specialist`
- `pubsub-specialist`
- `integration-specialist`
- `test-specialist`
- `maven-runner` only when Maven verification should run

Return the final coordinator output with file references and verification commands.
"""


def render_github_coordinator() -> str:
    agents = "\n".join(f"  - {item['slug']}" for item in SPECIALISTS)
    return f"""---
name: backend-coordinator
description: Coordinate backend surface analysis and merge focused agent findings.
tools: ['agent', 'search/codebase', 'search/usages', 'read/problems']
agents:
{agents}
  - maven-runner
---

Read `AGENTS.md` and `agents/workflows/BACKEND_ANALYSIS.md`.

Use the listed custom agents when the environment supports agent handoff. Use `maven-runner` only when Maven verification should run. Otherwise, use `agents/REFERENCES.md` and perform the same specialist analysis sequentially. Merge results with file evidence, severity, verification commands, and open questions.
"""


def render_github_agent(item: dict[str, Any]) -> str:
    invocable = "" if item["user_invocable"] else "user-invocable: false\n"
    return f"""---
name: {item['slug']}
description: {item['description']}
tools: [{item['github_tools']}]
agents: []
{invocable}---

Read `agents/SUBAGENTS.md`, then `agents/subagents/{item['slug']}.md`. Follow the neutral protocol exactly. Edit only when the parent task asks for implementation and this wrapper permits edits.
"""


def render_github_maven_runner() -> str:
    return """---
name: maven-runner
description: Run approved Maven verification commands and summarize build, test, Checkstyle, or JaCoCo results.
tools: ['search/codebase', 'read/problems', 'terminal']
agents: []
---

Read `agents/SUBAGENTS.md`, then `agents/subagents/maven-runner.md`.

Run only approved Maven commands from the repository root. Do not edit files, do not install packages, and do not start long-lived servers.
"""


def spring_backend_context_files(
    root: Path,
    maven_info: dict[str, Any] | None,
    spring_info: dict[str, Any],
) -> dict[str, str]:
    files = {
        "agents/REFERENCES.md": render_references_index(spring_info),
        "agents/references/technical/endpoints.md": render_technical_endpoints(spring_info),
        "agents/references/technical/services.md": render_technical_services(spring_info),
        "agents/references/technical/persistence.md": render_technical_persistence(spring_info),
        "agents/references/technical/pubsub.md": render_technical_pubsub(spring_info),
        "agents/references/technical/integrations.md": render_technical_integrations(spring_info),
        "agents/references/technical/testing.md": render_technical_testing(root, maven_info, spring_info),
        "agents/references/technical/maven.md": render_technical_maven(root, maven_info),
        "agents/references/business/domain-overview.md": render_business_domain_overview(spring_info),
        "agents/references/business/business-rules.md": render_business_rules(spring_info),
        "agents/references/business/events.md": render_business_events(spring_info),
        "agents/SUBAGENTS.md": render_subagents_doc(),
        "agents/subagents/maven-runner.md": render_maven_runner_role(),
        "agents/workflows/BACKEND_ANALYSIS.md": render_backend_workflow(),
        ".codex/config.toml": render_codex_config(),
        ".codex/agents/maven-runner.toml": render_codex_maven_runner(),
        ".opencode/agents/backend-coordinator.md": render_opencode_coordinator(),
        ".opencode/agents/maven-runner.md": render_opencode_maven_runner(),
        ".github/copilot-instructions.md": render_github_copilot_instructions(),
        ".github/prompts/backend-analysis.prompt.md": render_github_prompt(),
        ".github/agents/backend-coordinator.agent.md": render_github_coordinator(),
        ".github/agents/maven-runner.agent.md": render_github_maven_runner(),
    }
    for item in SPECIALISTS:
        files[f"agents/subagents/{item['slug']}.md"] = render_subagent_role(item)
        files[f".codex/agents/{item['slug']}.toml"] = render_codex_agent(item)
        files[f".opencode/agents/{item['slug']}.md"] = render_opencode_agent(item)
        files[f".github/agents/{item['slug']}.agent.md"] = render_github_agent(item)
    return files


def render_dependencies(
    detection: dict[str, Any],
    maven_info: dict[str, Any] | None,
) -> str:
    pom_tree = maven_info.get("pom_tree") if maven_info else None
    wrapper = maven_info.get("maven_wrapper", {}) if maven_info else {}
    stack_hints = []
    for label, fragment in [
        ("Spring WebFlux", "webflux"),
        ("Hibernate/JPA", "data-jpa"),
        ("PostgreSQL", "postgresql"),
        ("Flyway", "flyway"),
        ("SpringDoc OpenAPI", "springdoc-openapi"),
        ("GCP Pub/Sub", "pubsub"),
        ("JUnit/Spring Boot Test", "starter-test"),
        ("Reactor Test", "reactor-test"),
    ]:
        if has_dependency(pom_tree, fragment):
            stack_hints.append(label)
    return f"""# Dependencies

## Maven Project
- Maven detected: {bool(maven_info and maven_info.get("is_maven_project"))}
- Maven wrapper: {wrapper.get("present", False)}
- Coordinates: `{coord_text(pom_tree)}`
- Java version hint: {java_hint(maven_info)}
- Stack hints: {", ".join(stack_hints) if stack_hints else "Needs confirmation"}

## Dependency Management And BOMs
{bullet(dependency_management(pom_tree))}

## Direct Dependencies
{bullet(direct_dependencies(pom_tree))}

## Direct Dependency Exclusions
{bullet(exclusions(pom_tree), "None detected")}

## Maven Plugins
{bullet(plugin_ids(pom_tree))}

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
                "- If the service combines WebFlux with Hibernate/JPA, treat repository calls as blocking work and verify how the project isolates them.",
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
        "AGENTS.md": render_agents_md(project, detection, maven_info, spring_info),
        "agents/PROJECT_PROFILE.md": render_project_profile(
            project, detection, maven_info, spring_info, karate_info
        ),
        "agents/PROJECT_EVIDENCE.md": render_project_evidence(
            detection, maven_info, spring_info, karate_info
        ),
        "agents/BUILD_AND_TEST.md": render_build_and_test(
            project, detection, maven_info, spring_info, karate_info
        ),
        "agents/CODE_STYLE.md": render_code_style(project, detection, maven_info),
        "agents/ARCHITECTURE_NOTES.md": render_architecture(
            project, detection, spring_info, karate_info
        ),
        "agents/DEPENDENCIES.md": render_dependencies(detection, maven_info),
        "agents/TEMPLATE_NOTES.md": render_template_notes(detection),
    }
    if spring_info:
        files["agents/BACKEND_SURFACES.md"] = render_backend_surfaces(spring_info)
        files["agents/CALL_CHAINS.md"] = render_call_chains(spring_info)
        files.update(spring_backend_context_files(project, maven_info, spring_info))

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
