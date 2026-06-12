"""General Java and Spring WebFlux source summaries."""

from __future__ import annotations

import re
from pathlib import Path

from inspectors.common import read_text, rel, sample_matches


def package_roots(files: list[Path]) -> list[str]:
    packages = set()
    for path in files[:200]:
        match = re.search(r"^\s*package\s+([A-Za-z0-9_.]+)\s*;", read_text(path), re.M)
        if match:
            parts = match.group(1).split(".")
            packages.add(".".join(parts[: min(3, len(parts))]))
    return sorted(packages)


def inspect_java_summary(root: Path, files: list[Path]) -> dict:
    return {
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
        "package_roots": package_roots(files),
    }
