"""Extract compact node/link tables from bundled ComfyUI workflow JSON files.

This helper is for maintaining the Markdown specs. It reads every workflow in
references/workflows and prints a compact summary that can be copied into a
spec or used to verify an existing table.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = ROOT / "references" / "workflows"


def compact_json(value: object, limit: int = 240) -> str:
    if value is None:
        return "[]"
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = text.replace("\n", " ")
    if len(text) > limit:
        return text[:limit] + "..."
    return text


def main() -> None:
    for path in sorted(WORKFLOW_DIR.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        nodes = sorted(data.get("nodes", []), key=lambda node: node.get("id", 0))
        links = data.get("links", [])

        print(f"=== {path.stem} ===")
        print(
            f"nodes={len(nodes)} links={len(links)} "
            f"last_node_id={data.get('last_node_id')} "
            f"last_link_id={data.get('last_link_id')}"
        )

        print("\n## Node Table")
        print("| ID | class_type | Mode | Key Widget Values |")
        print("|---|---|---|---|")
        for node in nodes:
            title = node.get("title")
            node_type = node.get("type")
            label = f"{node_type} ({title})" if title and title != node_type else node_type
            widgets = compact_json(node.get("widgets_values", []))
            print(f"| {node.get('id')} | {label} | {node.get('mode', 0)} | `{widgets}` |")

        print("\n## Link Table")
        print("| LinkID | From (node.slot) | To (node.slot) | Type |")
        print("|---|---|---|---|")
        for link in links:
            print(f"| {link[0]} | {link[1]}.{link[2]} | {link[3]}.{link[4]} | {link[5]} |")

        buses = [node for node in nodes if node.get("type") in {"SetNode", "GetNode"}]
        if buses:
            print("\n## Bus Names")
            print("| ID | Node | Bus | Purpose |")
            print("|---|---|---|---|")
            for node in buses:
                values = node.get("widgets_values", [])
                bus = values[0] if isinstance(values, list) and values else values
                print(f"| {node.get('id')} | {node.get('type')} | `{bus}` | {node.get('title', '')} |")

        print()


if __name__ == "__main__":
    main()
