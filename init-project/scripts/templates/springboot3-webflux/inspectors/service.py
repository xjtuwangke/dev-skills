"""Service and collaborator extraction."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from inspectors.common import class_name, clean_type, read_text, rel


def collaborator_types(params: str) -> list[str]:
    collaborators = []
    for param in params.split(","):
        item = clean_type(param)
        if item and re.search(r"(Repository|Service|Publisher|Gateway|Client|UseCase)$", item):
            collaborators.append(item)
    return sorted(set(collaborators))


def public_methods(text: str) -> list[str]:
    methods = []
    pattern = re.compile(
        r"\bpublic\s+(?:[A-Za-z0-9_<>, ?]+)\s+([A-Za-z0-9_]+)\s*\(",
        re.M,
    )
    for match in pattern.finditer(text):
        name = match.group(1)
        if name not in {"getClass", "wait", "notify", "notifyAll"}:
            methods.append(name)
    return sorted(set(methods))


def extract_services(path: Path, root: Path, text: str) -> list[dict[str, Any]]:
    if "@Service" not in text:
        return []
    name = class_name(text, path)
    constructor = re.search(rf"\b{name}\s*\((?P<params>[^)]*)\)", text, re.S)
    return [
        {
            "class": name,
            "source": rel(path, root),
            "methods": public_methods(text),
            "collaborators": collaborator_types(constructor.group("params")) if constructor else [],
        }
    ]


def inspect_services(root: Path, files: list[Path]) -> dict[str, list[dict[str, Any]]]:
    services: list[dict[str, Any]] = []
    for path in files:
        services.extend(extract_services(path, root, read_text(path)))
    return {"services": services}
