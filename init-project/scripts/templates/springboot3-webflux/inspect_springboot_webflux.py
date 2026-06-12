#!/usr/bin/env python3
"""Inspect Spring Boot 3 WebFlux project signals."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from inspectors.common import java_files
from inspectors.config import inspect_config
from inspectors.endpoint import inspect_endpoints
from inspectors.java_summary import inspect_java_summary
from inspectors.persistence import inspect_persistence
from inspectors.pubsub import inspect_pubsub
from inspectors.service import inspect_services
from inspectors.tests import inspect_tests


def inspect(root: Path) -> dict:
    files = java_files(root)
    result = {
        "root": str(root),
    }
    result.update(inspect_java_summary(root, files))
    result.update(inspect_config(root))
    result.update(inspect_endpoints(root, files))
    result.update(inspect_services(root, files))
    result.update(inspect_persistence(root, files))
    result.update(inspect_pubsub(root, files))
    result.update(inspect_tests(root, files))
    return result


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}, indent=2))
        return 2
    print(json.dumps(inspect(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
