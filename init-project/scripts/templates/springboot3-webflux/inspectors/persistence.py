"""Persistence extraction for Spring Data and migration files."""

from __future__ import annotations

import re
from pathlib import Path

from inspectors.common import class_name, read_text, rel, visible


def extract_repositories(path: Path, root: Path, text: str) -> list[dict[str, str]]:
    if "Repository" not in text:
        return []
    match = re.search(
        r"interface\s+([A-Za-z0-9_]+)\s+extends\s+[A-Za-z0-9_.]*Repository"
        r"\s*<\s*([A-Za-z0-9_.$]+)\s*,\s*([A-Za-z0-9_.$]+)\s*>",
        text,
        re.S,
    )
    if not match:
        return []
    return [
        {
            "repository": match.group(1),
            "entity": match.group(2),
            "id_type": match.group(3),
            "source": rel(path, root),
        }
    ]


def extract_entities(path: Path, root: Path, text: str) -> list[dict[str, str]]:
    if "@Entity" not in text:
        return []
    table_match = re.search(r"@Table\s*\([^)]*name\s*=\s*\"([^\"]+)\"", text, re.S)
    return [
        {
            "entity": class_name(text, path),
            "table": table_match.group(1) if table_match else "Needs confirmation",
            "source": rel(path, root),
        }
    ]


def migrations(root: Path) -> list[str]:
    return sorted(
        rel(path, root)
        for path in root.rglob("db/migration/*")
        if visible(path) and path.is_file()
    )


def inspect_persistence(root: Path, files: list[Path]) -> dict[str, list]:
    repositories: list[dict[str, str]] = []
    entities: list[dict[str, str]] = []
    for path in files:
        text = read_text(path)
        repositories.extend(extract_repositories(path, root, text))
        entities.extend(extract_entities(path, root, text))
    return {
        "repositories": repositories,
        "entities": entities,
        "migrations": migrations(root),
    }
