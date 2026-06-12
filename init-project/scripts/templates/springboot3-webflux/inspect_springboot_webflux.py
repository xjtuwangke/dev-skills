#!/usr/bin/env python3
"""Inspect Spring Boot 3 WebFlux project signals."""

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


def java_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*.java") if visible(path)]


def sample_matches(files: list[Path], root: Path, patterns: tuple[str, ...], limit: int = 20) -> list[str]:
    matches = []
    for path in files:
        text = read_text(path)
        if any(pattern in text for pattern in patterns):
            matches.append(rel(path, root))
            if len(matches) >= limit:
                break
    return matches


def package_roots(files: list[Path]) -> list[str]:
    packages = set()
    for path in files[:200]:
        match = re.search(r"^\s*package\s+([A-Za-z0-9_.]+)\s*;", read_text(path), re.M)
        if match:
            parts = match.group(1).split(".")
            packages.add(".".join(parts[: min(3, len(parts))]))
    return sorted(packages)


def inspect(root: Path) -> dict[str, Any]:
    files = java_files(root)
    configs = [
        rel(path, root)
        for pattern in ("application*.yml", "application*.yaml", "application*.properties")
        for path in root.rglob(pattern)
        if visible(path)
    ]

    return {
        "root": str(root),
        "application_classes": sample_matches(files, root, ("@SpringBootApplication",)),
        "controllers_or_handlers": sample_matches(
            files,
            root,
            ("@RestController", "@Controller", "RouterFunction<", "ServerRequest", "ServerResponse"),
        ),
        "web_clients": sample_matches(files, root, ("WebClient", "HttpClient", "RestClient"), 20),
        "reactive_sources": sample_matches(files, root, ("Mono<", "Flux<", "reactor.core.publisher"), 30),
        "configuration_properties": sample_matches(
            files,
            root,
            ("@ConfigurationProperties", "@Value(", "@Profile", "@Bean"),
            30,
        ),
        "webflux_tests": sample_matches(files, root, ("WebTestClient", "StepVerifier", "@SpringBootTest"), 30),
        "package_roots": package_roots(files),
        "application_configs": sorted(configs),
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
