"""Pub/Sub class extraction."""

from __future__ import annotations

from pathlib import Path

from inspectors.common import class_name, read_text, rel


def extract_pubsub_classes(path: Path, root: Path, text: str) -> list[dict[str, str]]:
    if "/src/test/" in str(path):
        return []
    signals = []
    if "PubSubTemplate" in text:
        signals.append("PubSubTemplate")
    if "OrderEventPublisher" in text or "PubSubGateway" in text:
        signals.append("publisher interface/gateway")
    if "@ConditionalOnProperty" in text and "pubsub" in text.lower():
        signals.append("conditional pubsub bean")
    in_pubsub_package = "/pubsub/" in str(path).lower()
    direct_adapter = "PubSubTemplate" in text or ("@ConditionalOnProperty" in text and "pubsub" in text.lower())
    if not in_pubsub_package and not direct_adapter:
        return []
    return [
        {
            "class": class_name(text, path),
            "source": rel(path, root),
            "signals": ", ".join(signals) if signals else "package path",
        }
    ]


def inspect_pubsub(root: Path, files: list[Path]) -> dict[str, list[dict[str, str]]]:
    pubsub = []
    for path in files:
        pubsub.extend(extract_pubsub_classes(path, root, read_text(path)))
    return {"pubsub": pubsub}
