# ComfyUI Workflow Builder

When building, modifying, validating, or explaining ComfyUI workflow JSON, use the skill at:

```text
skills/comfyui-workflow-builder/SKILL.md
```

Load order:

1. Read `SKILL.md` for the workflow generation process and validation checklist.
2. Read `specs/README.md` to choose a matching workflow pattern.
3. Read the matching `specs/*.md` file for node and link tables.
4. Read `specs/COMFYUI_FORMAT.md` and `specs/NODE_CATALOG.md` for exact schema and slot/widget order.
5. Read `references/workflows/*.json` only when a spec is ambiguous or a custom node must be copied exactly.

Always validate bidirectional links, node IDs, link IDs, widget order, and `last_node_id` / `last_link_id` before returning workflow JSON.
