#!/usr/bin/env python3
"""Detect supported init-project template facets for a repository."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SUPPORTED = [
    "baseline",
    "maven-java",
    "springboot3-webflux",
    "karate-at",
]


def text_of(elem: ET.Element | None) -> str:
    return (elem.text or "").strip() if elem is not None else ""


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def iter_named(root: ET.Element, name: str):
    for elem in root.iter():
        if local_name(elem.tag) == name:
            yield elem


def parse_pom(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "dependencies": [], "properties": {}, "parent": {}}

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return {
            "exists": True,
            "parse_error": str(exc),
            "dependencies": [],
            "properties": {},
            "parent": {},
            "modules": [],
        }

    deps = []
    for dep in iter_named(root, "dependency"):
        group_id = text_of(next((c for c in dep if local_name(c.tag) == "groupId"), None))
        artifact_id = text_of(next((c for c in dep if local_name(c.tag) == "artifactId"), None))
        version = text_of(next((c for c in dep if local_name(c.tag) == "version"), None))
        if group_id or artifact_id:
            deps.append(
                {"groupId": group_id, "artifactId": artifact_id, "version": version}
            )

    props = {}
    props_node = next(iter_named(root, "properties"), None)
    if props_node is not None:
        for child in list(props_node):
            props[local_name(child.tag)] = text_of(child)

    parent_node = next(iter_named(root, "parent"), None)
    parent = {}
    if parent_node is not None:
        for key in ("groupId", "artifactId", "version"):
            parent[key] = text_of(
                next((c for c in parent_node if local_name(c.tag) == key), None)
            )

    modules = [text_of(module) for module in iter_named(root, "module")]

    return {
        "exists": True,
        "dependencies": deps,
        "properties": props,
        "parent": parent,
        "modules": modules,
    }


def has_dep(
    pom: dict, group_contains: str | None = None, artifact_contains: str | None = None
) -> bool:
    for dep in pom.get("dependencies", []):
        group = dep.get("groupId", "")
        artifact = dep.get("artifactId", "")
        if group_contains and group_contains not in group:
            continue
        if artifact_contains and artifact_contains not in artifact:
            continue
        return True
    return False


def version_starts_with(value: str | None, prefix: str) -> bool:
    return bool(value) and value.strip().startswith(prefix)


def collect_files(root: Path) -> dict:
    ignored_parts = {"target", ".git", ".idea", ".gradle", "build"}

    def visible(path: Path) -> bool:
        return not any(part in ignored_parts for part in path.parts)

    feature_files = [p for p in root.rglob("*.feature") if visible(p)]
    java_files = [p for p in root.rglob("*.java") if visible(p)]
    app_configs = [
        p
        for p in root.rglob("application*.yml")
        if visible(p)
    ] + [
        p
        for p in root.rglob("application*.yaml")
        if visible(p)
    ]
    karate_config = [p for p in root.rglob("karate-config.js") if visible(p)]
    maven_wrappers = [p for p in [root / "mvnw", root / "mvnw.cmd"] if p.exists()]

    return {
        "feature_files": feature_files,
        "java_files": java_files,
        "app_configs": app_configs,
        "karate_config": karate_config,
        "maven_wrappers": maven_wrappers,
    }


def confidence_for(score: int, high: int, medium: int, low: int = 1) -> str:
    if score >= high:
        return "high"
    if score >= medium:
        return "medium"
    if score >= low:
        return "low"
    return "none"


def detect(root: Path) -> dict:
    pom = parse_pom(root / "pom.xml")
    files = collect_files(root)
    signals: dict[str, list[str]] = {name: [] for name in SUPPORTED}
    scores = {name: 0 for name in SUPPORTED}

    signals["baseline"].append("baseline applies to every project")
    scores["baseline"] = 10

    if pom.get("exists"):
        signals["maven-java"].append("pom.xml found")
        scores["maven-java"] += 4

    if files["java_files"]:
        signals["maven-java"].append(f"{len(files['java_files'])} Java files found")
        scores["maven-java"] += 2

    if files["maven_wrappers"]:
        signals["maven-java"].append("Maven wrapper found")
        scores["maven-java"] += 1

    props = pom.get("properties", {})
    java_version = props.get("java.version") or props.get("maven.compiler.release")
    if java_version:
        signals["maven-java"].append(f"Java version property: {java_version}")
        scores["maven-java"] += 1

    if pom.get("modules"):
        signals["maven-java"].append(f"{len(pom['modules'])} Maven modules found")
        scores["maven-java"] += 1

    parent = pom.get("parent", {})
    if (
        parent.get("artifactId") == "spring-boot-starter-parent"
        and version_starts_with(parent.get("version"), "3.")
    ):
        signals["springboot3-webflux"].append("Spring Boot 3 parent found")
        scores["springboot3-webflux"] += 3

    spring_boot_property = props.get("spring-boot.version") or props.get("spring.boot.version")
    if version_starts_with(spring_boot_property, "3."):
        signals["springboot3-webflux"].append("Spring Boot 3 property found")
        scores["springboot3-webflux"] += 2

    if has_dep(pom, "org.springframework.boot", "spring-boot-starter-webflux"):
        signals["springboot3-webflux"].append("spring-boot-starter-webflux dependency found")
        scores["springboot3-webflux"] += 4

    if has_dep(pom, "io.projectreactor", None):
        signals["springboot3-webflux"].append("Project Reactor dependency found")
        scores["springboot3-webflux"] += 1

    if files["app_configs"]:
        signals["springboot3-webflux"].append("application*.yml/yaml config found")
        scores["springboot3-webflux"] += 1

    if has_dep(pom, "com.intuit.karate", None):
        signals["karate-at"].append("Karate dependency found")
        scores["karate-at"] += 4

    if files["feature_files"]:
        signals["karate-at"].append(f"{len(files['feature_files'])} .feature files found")
        scores["karate-at"] += 3

    if files["karate_config"]:
        signals["karate-at"].append("karate-config.js found")
        scores["karate-at"] += 2

    runner_hits = [
        p
        for p in files["java_files"][:500]
        if "runner" in p.name.lower() or "karate" in p.name.lower()
    ]
    if runner_hits:
        signals["karate-at"].append("Karate/runner-like Java test classes found")
        scores["karate-at"] += 1

    confidence = {
        "baseline": "high",
        "maven-java": confidence_for(scores["maven-java"], high=6, medium=4),
        "springboot3-webflux": confidence_for(
            scores["springboot3-webflux"], high=7, medium=4, low=2
        ),
        "karate-at": confidence_for(scores["karate-at"], high=7, medium=4, low=2),
    }

    matched_templates = [
        name for name in SUPPORTED if confidence[name] in {"high", "medium"}
    ]

    if "springboot3-webflux" in matched_templates:
        primary_purpose = "springboot3-webflux-service"
    elif "karate-at" in matched_templates:
        primary_purpose = "karate-acceptance-tests"
    elif "maven-java" in matched_templates:
        primary_purpose = "maven-java-project"
    elif "baseline" in matched_templates:
        primary_purpose = "generic-project"
    else:
        primary_purpose = None

    return {
        "root": str(root),
        "matched_templates": matched_templates,
        "primary_purpose": primary_purpose,
        "confidence": confidence,
        "scores": scores,
        "signals": signals,
        "template_reference_paths": {
            name: f"references/templates/{name}/index.md" for name in matched_templates
        },
        "pom": {
            "exists": pom.get("exists", False),
            "parent": pom.get("parent", {}),
            "modules": pom.get("modules", []),
            "properties": {
                k: v
                for k, v in pom.get("properties", {}).items()
                if k
                in {
                    "java.version",
                    "maven.compiler.release",
                    "spring-boot.version",
                    "spring.boot.version",
                }
            },
            "dependency_count": len(pom.get("dependencies", [])),
            "parse_error": pom.get("parse_error"),
        },
        "file_counts": {
            "java": len(files["java_files"]),
            "feature": len(files["feature_files"]),
            "application_config": len(files["app_configs"]),
            "karate_config": len(files["karate_config"]),
            "maven_wrapper": len(files["maven_wrappers"]),
        },
    }


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}, indent=2))
        return 2

    print(json.dumps(detect(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
