"""HTTP endpoint extraction for Spring controllers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from inspectors.common import class_name, clean_type, read_text, rel


MAPPING_METHODS = {
    "GetMapping": "GET",
    "PostMapping": "POST",
    "PutMapping": "PUT",
    "PatchMapping": "PATCH",
    "DeleteMapping": "DELETE",
}


def first_quoted(value: str | None) -> str:
    if not value:
        return ""
    match = re.search(r'"([^"]+)"', value)
    return match.group(1) if match else ""


def join_paths(base: str, child: str) -> str:
    parts = []
    for item in (base, child):
        if item:
            parts.append(item.strip("/"))
    joined = "/" + "/".join(parts)
    return joined if joined != "/" else "/"


def class_prefix(text: str) -> str:
    match = re.search(r"\b(?:class|interface|record|enum)\s+[A-Za-z0-9_]+", text)
    return text[: match.start()] if match else text[:1000]


def class_request_mapping(text: str) -> str:
    matches = list(re.finditer(r"@RequestMapping\s*\(([^)]*)\)", class_prefix(text), re.S))
    return first_quoted(matches[-1].group(1)) if matches else ""


def request_body_type(params: str) -> str:
    for param in params.split(","):
        if "@RequestBody" in param:
            return clean_type(param)
    return ""


def path_variable_names(params: str) -> list[str]:
    names = []
    for param in params.split(","):
        if "@PathVariable" not in param:
            continue
        match = re.search(r"([A-Za-z0-9_]+)\s*$", param.strip())
        if match:
            names.append(match.group(1))
    return names


def extract_endpoints(path: Path, root: Path, text: str) -> list[dict[str, str | list[str]]]:
    if "@RestController" not in text and "@Controller" not in text:
        return []

    base = class_request_mapping(text)
    controller = class_name(text, path)
    endpoints = []
    pattern = re.compile(
        r"@(?P<mapping>GetMapping|PostMapping|PutMapping|PatchMapping|DeleteMapping)"
        r"(?:\((?P<args>[^)]*)\))?"
        r"(?P<body>[\s\S]{0,900}?)"
        r"\bpublic\s+(?P<return>[A-Za-z0-9_<>, ?]+)\s+(?P<method>[A-Za-z0-9_]+)\s*"
        r"\((?P<params>[^)]*)\)",
        re.M,
    )
    for match in pattern.finditer(text):
        params = match.group("params")
        endpoints.append(
            {
                "method": MAPPING_METHODS[match.group("mapping")],
                "path": join_paths(base, first_quoted(match.group("args"))),
                "handler": f"{controller}#{match.group('method')}",
                "request": request_body_type(params) or "None detected",
                "response": re.sub(r"\s+", " ", match.group("return")).strip(),
                "path_variables": path_variable_names(params),
                "source": rel(path, root),
            }
        )
    return endpoints


def inspect_endpoints(root: Path, files: list[Path]) -> dict[str, list[dict[str, Any]]]:
    endpoints: list[dict[str, Any]] = []
    for path in files:
        endpoints.extend(extract_endpoints(path, root, read_text(path)))
    return {"endpoints": endpoints}
