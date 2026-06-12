"""Spring WebFlux test extraction."""

from __future__ import annotations

from pathlib import Path

from inspectors.common import read_text, rel, sample_matches


def test_catalog(files: list[Path], root: Path) -> list[dict[str, str]]:
    tests = []
    for path in files:
        if "/src/test/" not in str(path):
            continue
        text = read_text(path)
        signals = []
        for name in ("Mockito", "WebTestClient", "StepVerifier", "@SpringBootTest", "@WebFluxTest"):
            if name in text:
                signals.append(name)
        tests.append(
            {
                "class": path.stem,
                "source": rel(path, root),
                "signals": ", ".join(signals) if signals else "JUnit",
            }
        )
    return tests


def inspect_tests(root: Path, files: list[Path]) -> dict:
    return {
        "webflux_tests": sample_matches(files, root, ("WebTestClient", "StepVerifier", "@SpringBootTest"), 30),
        "tests": test_catalog(files, root),
    }
