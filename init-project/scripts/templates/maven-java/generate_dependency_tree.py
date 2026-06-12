#!/usr/bin/env python3
"""Generate Maven dependency tree JSON for a project or module."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


PLUGIN_COORD = "org.apache.maven.plugins:maven-dependency-plugin:3.11.0:tree"
IGNORED_DIRS = {".git", ".idea", ".gradle", "build", "target"}


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def child(elem: ET.Element, name: str) -> ET.Element | None:
    for item in list(elem):
        if local_name(item.tag) == name:
            return item
    return None


def text(elem: ET.Element | None) -> str | None:
    if elem is None or elem.text is None:
        return None
    value = elem.text.strip()
    return value or None


def read_modules(pom_path: Path) -> list[str]:
    if not pom_path.exists():
        return []
    try:
        root = ET.parse(pom_path).getroot()
    except ET.ParseError:
        return []
    modules_node = child(root, "modules")
    if modules_node is None:
        return []
    modules = []
    for module in list(modules_node):
        if local_name(module.tag) == "module" and text(module):
            modules.append(text(module) or "")
    return modules


def has_visible_pom(root: Path, module: str) -> bool:
    module_path = (root / module).resolve()
    if any(part in IGNORED_DIRS for part in module_path.parts):
        return False
    return (module_path / "pom.xml").exists()


def choose_maven(root: Path, explicit: str | None) -> list[str]:
    if explicit:
        return [explicit]
    wrapper = root / "mvnw"
    if wrapper.exists():
        return [str(wrapper)]
    if shutil.which("mvn"):
        return ["mvn"]
    return ["mvn"]


def build_command(
    maven: list[str],
    root: Path,
    output_file: Path,
    module: str | None,
    scope: str | None,
    includes: str | None,
    excludes: str | None,
    plugin_coord: str,
    extra_maven_args: list[str],
) -> list[str]:
    command = list(maven)
    command.extend(["-q", "-f", str(root / "pom.xml")])
    if module:
        command.extend(["-pl", module])
    command.extend(extra_maven_args)
    command.append(plugin_coord)
    command.append("-DoutputType=json")
    command.append(f"-DoutputFile={output_file}")
    if scope:
        command.append(f"-Dscope={scope}")
    if includes:
        command.append(f"-Dincludes={includes}")
    if excludes:
        command.append(f"-Dexcludes={excludes}")
    return command


def load_tree(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"parse_error": str(exc), "raw": path.read_text(encoding="utf-8")}


def run_tree(
    root: Path,
    module: str | None,
    args: argparse.Namespace,
    temp_dir: Path,
) -> dict[str, Any]:
    label = module or "root"
    output_file = temp_dir / f"{label.replace('/', '__')}-dependency-tree.json"
    command = build_command(
        choose_maven(root, args.maven),
        root,
        output_file,
        module,
        args.scope,
        args.includes,
        args.excludes,
        args.plugin,
        args.maven_args or [],
    )
    try:
        result = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "module": module,
            "command": command,
            "returncode": None,
            "timed_out": True,
            "timeout_seconds": args.timeout,
            "stdout": (exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
            "stderr": (exc.stderr or "").strip() if isinstance(exc.stderr, str) else "",
            "tree": None,
        }

    return {
        "module": module,
        "command": command,
        "returncode": result.returncode,
        "timed_out": False,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "tree": load_tree(output_file),
    }


def module_targets(root: Path, args: argparse.Namespace) -> list[str | None]:
    if args.module:
        return [args.module]
    if args.root_only:
        return [None]

    modules = [module for module in read_modules(root / "pom.xml") if has_visible_pom(root, module)]
    if modules:
        return [None] + modules
    return [None]


def generate(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    if not (root / "pom.xml").exists():
        return {
            "root": str(root),
            "is_maven_project": False,
            "error": "No pom.xml found at project root.",
        }

    with tempfile.TemporaryDirectory(prefix="maven-deps-tree-") as temp_name:
        temp_dir = Path(temp_name)
        runs = [run_tree(root, module, args, temp_dir) for module in module_targets(root, args)]

    ok = all(run["returncode"] == 0 and run["tree"] is not None for run in runs)
    return {
        "root": str(root),
        "is_maven_project": True,
        "ok": ok,
        "plugin": args.plugin,
        "filters": {
            "scope": args.scope,
            "includes": args.includes,
            "excludes": args.excludes,
        },
        "runs": runs,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Maven dependency:tree JSON for a project."
    )
    parser.add_argument("project", nargs="?", default=".", help="Project root")
    parser.add_argument("--module", help="Run dependency tree for one Maven module")
    parser.add_argument("--root-only", action="store_true", help="Only run the root project")
    parser.add_argument("--scope", help="Maven dependency:tree scope filter")
    parser.add_argument("--includes", help="Maven dependency:tree includes filter")
    parser.add_argument("--excludes", help="Maven dependency:tree excludes filter")
    parser.add_argument("--maven", help="Maven executable, defaults to ./mvnw then mvn")
    parser.add_argument(
        "--plugin",
        default=PLUGIN_COORD,
        help=f"Dependency plugin goal, default: {PLUGIN_COORD}",
    )
    parser.add_argument(
        "--maven-arg",
        dest="maven_args",
        action="append",
        help="Extra Maven argument, can be repeated, e.g. --maven-arg=-DskipTests",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout in seconds for each Maven dependency:tree run",
    )
    parser.add_argument("--output", help="Write JSON result to this file")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv[1:])
    root = Path(args.project).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}, indent=2))
        return 2

    result = generate(root, args)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).expanduser().write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if result.get("ok", not result.get("is_maven_project")) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
