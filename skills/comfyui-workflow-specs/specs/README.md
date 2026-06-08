# Workflow Specs

Each spec is a compact, structured reference for one ComfyUI workflow. Specs are designed to give an LLM enough information to rebuild or remix a workflow without reading the full JSON.

## Spec Format

Every spec follows this structure:

- **Purpose** — What the workflow does (1-2 sentences)
- **Model Stack** — Exact checkpoint, LoRA, ControlNet filenames
- **Node Table** — Every functional node with ID, class_type, and key widget values
- **Link Table** — Every connection as `[linkID, fromNode.slot, toNode.slot, type]`
- **Data Flow** — Concise prose describing the pipeline
- **Bus Names** — Set/Get bus names and what they connect (if applicable)
- **Invariants** — Critical constraints (resolution, CFG, step count, etc.)

## How to Use Specs

1. **Building a similar workflow**: Use the spec's node table and link table as a template. Modify widget values (prompts, model names, seeds) to match new requirements.
2. **Understanding a workflow**: Read the Purpose and Data Flow sections for a quick overview.
3. **Exact wiring details**: If the spec is ambiguous, open the matching JSON in `references/workflows/`.

## Supporting Documents

- `COMFYUI_FORMAT.md` — Complete JSON schema reference
- `NODE_CATALOG.md` — Node class_types with exact slot orders and widget_values format
- `LAYOUT_BLUEPRINT.md` — Visual layout rules and concrete spacing defaults
