#!/usr/bin/env python3
"""Inspect Karate acceptance-test project signals."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


IGNORED_DIRS = {".git", ".idea", ".gradle", "build", "target"}


def visible(path: Path) -> bool:
    return not any(part in IGNORED_DIRS for part in path.parts)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def feature_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.feature") if visible(path)]


def java_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.java") if visible(path)]


def collect_tags(features: list[Path]) -> list[str]:
    tags = set()
    for path in features[:200]:
        for match in re.finditer(r"(?m)^\s*(@[A-Za-z0-9_.:-]+(?:\s+@[A-Za-z0-9_.:-]+)*)", read_text(path)):
            for tag in match.group(1).split():
                tags.add(tag)
    return sorted(tags)


def collect_feature_samples(features: list[Path], root: Path, limit: int = 40) -> list[str]:
    return [rel(path, root) for path in sorted(features)[:limit]]


def collect_runners(files: list[Path], root: Path) -> list[str]:
    runners = []
    for path in files:
        text = read_text(path)
        if "Karate.run" in text or "com.intuit.karate" in text or "@Karate.Test" in text:
            runners.append(rel(path, root))
    return sorted(runners)


def collect_env_hints(root: Path) -> dict[str, Any]:
    configs = [path for path in root.rglob("karate-config.js") if visible(path)]
    envs = set()
    config_paths = []
    for path in configs:
        config_paths.append(rel(path, root))
        text = read_text(path)
        for match in re.finditer(r"karate\.env\s*\|\|\s*['\"]([^'\"]+)['\"]", text):
            envs.add(match.group(1))
        for match in re.finditer(r"karate\.env\s*==?\s*['\"]([^'\"]+)['\"]", text):
            envs.add(match.group(1))
        for match in re.finditer(r"env\s*==?\s*['\"]([^'\"]+)['\"]", text):
            envs.add(match.group(1))
    return {"karate_config": sorted(config_paths), "env_hints": sorted(envs)}


def collect_fixtures(root: Path) -> list[str]:
    candidates = []
    for pattern in ("*.json", "*.js", "*.yaml", "*.yml", "*.csv"):
        for path in root.rglob(pattern):
            if visible(path) and any(part in {"data", "payloads", "schemas", "fixtures", "resources"} for part in path.parts):
                candidates.append(rel(path, root))
    return sorted(candidates)[:60]


def inspect(root: Path) -> dict[str, Any]:
    features = feature_files(root)
    files = java_files(root)
    env = collect_env_hints(root)
    return {
        "root": str(root),
        "feature_files": collect_feature_samples(features, root),
        "feature_count": len(features),
        "tags": collect_tags(features),
        "runner_classes": collect_runners(files, root),
        "karate_config": env["karate_config"],
        "env_hints": env["env_hints"],
        "fixtures": collect_fixtures(root),
    }


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}, indent=2))
        return 2
    print(json.dumps(inspect(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
