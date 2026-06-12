"""Shared helpers for static Spring Boot source inspection."""

from __future__ import annotations

import re
from pathlib import Path


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
    return sorted(path for path in root.rglob("*.java") if visible(path))


def sample_matches(files: list[Path], root: Path, patterns: tuple[str, ...], limit: int = 20) -> list[str]:
    matches = []
    for path in files:
        text = read_text(path)
        if any(pattern in text for pattern in patterns):
            matches.append(rel(path, root))
            if len(matches) >= limit:
                break
    return matches


def class_name(text: str, fallback: Path) -> str:
    match = re.search(r"\b(?:class|interface|record|enum)\s+([A-Za-z0-9_]+)", text)
    return match.group(1) if match else fallback.stem


def clean_type(value: str) -> str:
    value = re.sub(r"@[A-Za-z0-9_.]+(?:\([^)]*\))?", " ", value)
    value = value.replace("final ", " ")
    value = re.sub(r"\s+", " ", value).strip()
    parts = value.split(" ")
    if len(parts) >= 2:
        return " ".join(parts[:-1])
    return value
