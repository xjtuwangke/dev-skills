"""Application profile and configuration extraction."""

from __future__ import annotations

import re
from pathlib import Path

from inspectors.common import read_text, rel, visible


def collect_configs(root: Path) -> list[Path]:
    return sorted(
        path
        for pattern in ("application*.yml", "application*.yaml", "application*.properties")
        for path in root.rglob(pattern)
        if visible(path)
    )


def profile_name(path: Path) -> str | None:
    match = re.match(r"application-([A-Za-z0-9_-]+)\.(?:yml|yaml|properties)$", path.name)
    return match.group(1) if match else None


def env_placeholders(configs: list[Path]) -> list[str]:
    values = set()
    for path in configs:
        for match in re.finditer(r"\$\{([A-Za-z0-9_]+)(?::[^}]*)?\}", read_text(path)):
            values.add(match.group(1))
    return sorted(values)


def topic_hints(configs: list[Path], root: Path) -> list[dict[str, str]]:
    hints = []
    for path in configs:
        for line in read_text(path).splitlines():
            if "topic:" in line or "created-topic:" in line or "status-changed-topic:" in line:
                hints.append({"source": rel(path, root), "line": line.strip()})
    return hints


def inspect_config(root: Path) -> dict:
    configs = collect_configs(root)
    return {
        "application_configs": [rel(path, root) for path in configs],
        "profiles": sorted(name for path in configs if (name := profile_name(path))),
        "environment_variables": env_placeholders(configs),
        "pubsub_topic_hints": topic_hints(configs, root),
    }
