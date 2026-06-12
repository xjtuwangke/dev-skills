#!/usr/bin/env python3
"""Inspect a Maven Java project and emit a JSON POM structure summary."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


IGNORED_DIRS = {".git", ".idea", ".gradle", "build", "target"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child(elem: ET.Element, name: str) -> ET.Element | None:
    for item in list(elem):
        if local_name(item.tag) == name:
            return item
    return None


def children(elem: ET.Element, name: str) -> list[ET.Element]:
    return [item for item in list(elem) if local_name(item.tag) == name]


def text(elem: ET.Element | None) -> str | None:
    if elem is None or elem.text is None:
        return None
    value = elem.text.strip()
    return value or None


def child_text(elem: ET.Element, name: str) -> str | None:
    return text(child(elem, name))


def direct_section(elem: ET.Element, name: str) -> ET.Element | None:
    return child(elem, name)


def parse_kv_section(section: ET.Element | None) -> dict[str, str]:
    if section is None:
        return {}
    result = {}
    for item in list(section):
        value = text(item)
        if value is not None:
            result[local_name(item.tag)] = value
    return result


def parse_parent(root: ET.Element) -> dict[str, str | None] | None:
    parent = child(root, "parent")
    if parent is None:
        return None
    return {
        "groupId": child_text(parent, "groupId"),
        "artifactId": child_text(parent, "artifactId"),
        "version": child_text(parent, "version"),
        "relativePath": child_text(parent, "relativePath"),
    }


def parse_dependency(dep: ET.Element) -> dict[str, str | None]:
    exclusions_node = child(dep, "exclusions")
    exclusions = []
    if exclusions_node is not None:
        for exclusion in children(exclusions_node, "exclusion"):
            exclusions.append(
                {
                    "groupId": child_text(exclusion, "groupId"),
                    "artifactId": child_text(exclusion, "artifactId"),
                }
            )

    return {
        "groupId": child_text(dep, "groupId"),
        "artifactId": child_text(dep, "artifactId"),
        "version": child_text(dep, "version"),
        "type": child_text(dep, "type"),
        "classifier": child_text(dep, "classifier"),
        "scope": child_text(dep, "scope"),
        "optional": child_text(dep, "optional"),
        "exclusions": exclusions,
    }


def parse_dependencies(section: ET.Element | None) -> list[dict[str, str | None]]:
    if section is None:
        return []
    return [parse_dependency(dep) for dep in children(section, "dependency")]


def parse_dependency_management(root: ET.Element) -> list[dict[str, str | None]]:
    dep_mgmt = child(root, "dependencyManagement")
    if dep_mgmt is None:
        return []
    return parse_dependencies(child(dep_mgmt, "dependencies"))


def parse_plugin(plugin: ET.Element) -> dict[str, Any]:
    executions = []
    executions_node = child(plugin, "executions")
    if executions_node is not None:
        for execution in children(executions_node, "execution"):
            goals_node = child(execution, "goals")
            goals = children(goals_node, "goal") if goals_node is not None else []
            executions.append(
                {
                    "id": child_text(execution, "id"),
                    "phase": child_text(execution, "phase"),
                    "goals": [text(goal) for goal in goals if text(goal) is not None],
                }
            )

    return {
        "groupId": child_text(plugin, "groupId"),
        "artifactId": child_text(plugin, "artifactId"),
        "version": child_text(plugin, "version"),
        "executions": executions,
    }


def parse_plugins(root: ET.Element) -> dict[str, list[dict[str, Any]]]:
    build = child(root, "build")
    if build is None:
        return {"plugins": [], "pluginManagement": []}

    plugins_node = child(build, "plugins")
    plugin_mgmt_node = child(build, "pluginManagement")
    plugin_mgmt_plugins = (
        child(plugin_mgmt_node, "plugins") if plugin_mgmt_node is not None else None
    )

    return {
        "plugins": [
            parse_plugin(plugin)
            for plugin in children(plugins_node, "plugin")
        ]
        if plugins_node is not None
        else [],
        "pluginManagement": [
            parse_plugin(plugin)
            for plugin in children(plugin_mgmt_plugins, "plugin")
        ]
        if plugin_mgmt_plugins is not None
        else [],
    }


def parse_profiles(root: ET.Element) -> list[dict[str, Any]]:
    profiles_node = child(root, "profiles")
    if profiles_node is None:
        return []

    profiles = []
    for profile in children(profiles_node, "profile"):
        profiles.append(
            {
                "id": child_text(profile, "id"),
                "properties": parse_kv_section(child(profile, "properties")),
                "dependencies": parse_dependencies(child(profile, "dependencies")),
                "dependencyManagement": parse_dependency_management(profile),
                "plugins": parse_plugins(profile),
            }
        )
    return profiles


def parse_modules(root: ET.Element) -> list[str]:
    modules_node = child(root, "modules")
    if modules_node is None:
        return []
    return [value for value in (text(module) for module in children(modules_node, "module")) if value]


def infer_java_version(properties: dict[str, str], plugins: dict[str, list[dict[str, Any]]]) -> str | None:
    for key in ("java.version", "maven.compiler.release", "maven.compiler.source", "maven.compiler.target"):
        if properties.get(key):
            return properties[key]

    all_plugins = plugins.get("plugins", []) + plugins.get("pluginManagement", [])
    for plugin in all_plugins:
        if plugin.get("artifactId") == "maven-compiler-plugin":
            return plugin.get("version")
    return None


def parse_pom(pom_path: Path, root_dir: Path, seen: set[Path]) -> dict[str, Any]:
    resolved = pom_path.resolve()
    relative_path = str(pom_path.relative_to(root_dir)) if pom_path.is_relative_to(root_dir) else str(pom_path)

    if resolved in seen:
        return {
            "path": str(pom_path),
            "relative_path": relative_path,
            "cycle_detected": True,
        }
    seen.add(resolved)

    try:
        xml_root = ET.parse(pom_path).getroot()
    except ET.ParseError as exc:
        return {
            "path": str(pom_path),
            "relative_path": relative_path,
            "parse_error": str(exc),
        }

    parent = parse_parent(xml_root)
    properties = parse_kv_section(child(xml_root, "properties"))
    plugins = parse_plugins(xml_root)
    modules = parse_modules(xml_root)
    module_details = []

    for module in modules:
        module_dir = (pom_path.parent / module).resolve()
        if any(part in IGNORED_DIRS for part in module_dir.parts):
            continue
        module_pom = module_dir / "pom.xml"
        if module_pom.exists():
            module_details.append(parse_pom(module_pom, root_dir, seen))
        else:
            module_details.append(
                {
                    "module": module,
                    "path": str(module_pom),
                    "relative_path": str(module_pom.relative_to(root_dir))
                    if module_pom.is_relative_to(root_dir)
                    else str(module_pom),
                    "missing_pom": True,
                }
            )

    group_id = child_text(xml_root, "groupId") or (parent or {}).get("groupId")
    artifact_id = child_text(xml_root, "artifactId")
    version = child_text(xml_root, "version") or (parent or {}).get("version")

    return {
        "path": str(pom_path),
        "relative_path": relative_path,
        "modelVersion": child_text(xml_root, "modelVersion"),
        "coordinates": {
            "groupId": group_id,
            "artifactId": artifact_id,
            "version": version,
            "packaging": child_text(xml_root, "packaging") or "jar",
        },
        "name": child_text(xml_root, "name"),
        "description": child_text(xml_root, "description"),
        "parent": parent,
        "properties": properties,
        "java_version_hint": infer_java_version(properties, plugins),
        "modules": modules,
        "dependencies": parse_dependencies(child(xml_root, "dependencies")),
        "dependencyManagement": parse_dependency_management(xml_root),
        "plugins": plugins,
        "profiles": parse_profiles(xml_root),
        "module_details": module_details,
    }


def find_maven_wrapper(root: Path) -> dict[str, Any]:
    files = []
    for name in ("mvnw", "mvnw.cmd", ".mvn/wrapper/maven-wrapper.properties"):
        path = root / name
        if path.exists():
            files.append(name)
    return {"present": bool(files), "files": files}


def inspect_project(project_root: Path) -> dict[str, Any]:
    root = project_root.expanduser().resolve()
    pom_path = root / "pom.xml"
    if not pom_path.exists():
        nested_poms = [
            p
            for p in root.rglob("pom.xml")
            if not any(part in IGNORED_DIRS for part in p.parts)
        ][:20]
        return {
            "root": str(root),
            "is_maven_project": False,
            "reason": "No pom.xml found at project root.",
            "nested_pom_candidates": [str(p.relative_to(root)) for p in nested_poms],
        }

    pom_tree = parse_pom(pom_path, root, set())
    return {
        "root": str(root),
        "is_maven_project": True,
        "maven_wrapper": find_maven_wrapper(root),
        "pom_tree": pom_tree,
    }


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".")
    if not root.exists() or not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}, indent=2))
        return 2

    print(json.dumps(inspect_project(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
