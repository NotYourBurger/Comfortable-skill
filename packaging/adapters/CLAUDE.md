# ComfyUI Workflow Builder Skill

Use `skills/comfyui-workflow-builder/SKILL.md` whenever the user asks to build, modify, inspect, repair, or validate ComfyUI workflow JSON.

Follow the skill's reference priority:

1. Matching spec in `skills/comfyui-workflow-builder/specs/`.
2. Raw workflow JSON in `skills/comfyui-workflow-builder/references/workflows/` when exact wiring is needed.
3. `COMFYUI_FORMAT.md` and `NODE_CATALOG.md` for schema, slot order, and widget order.

For opaque custom nodes, copy exact node definitions from the raw workflow JSON rather than guessing.
