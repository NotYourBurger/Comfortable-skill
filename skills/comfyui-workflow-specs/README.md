# ComfyUI Workflow Builder Skill

This skill enables building any ComfyUI workflow from requirements, reference specs, or existing workflow JSONs.

## What It Does

- Builds valid ComfyUI workflow JSON from natural language requirements
- Uses reference specs as compact pattern guides for common workflow types
- Uses raw workflow JSONs as exact wiring references when needed
- Includes a node catalog and JSON format reference for precise generation

## Contents

- `SKILL.md` — The skill instructions (workflow building process, validation, layout rules)
- `specs/` — Reference specs and supporting documents:
  - `COMFYUI_FORMAT.md` — Complete JSON schema reference for the workflow format
  - `NODE_CATALOG.md` — Node class_types with exact slot orders and widgets_values format
  - `LAYOUT_BLUEPRINT.md` — Visual layout rules and concrete spacing defaults
  - `*.md` — One compact spec per reference workflow (node tables, link tables, data flow)
- `references/workflows/` — Raw workflow JSON files (the definitive wiring source)

## Install

### Claude Code user install

1. Download or clone the skill folder.
2. Place it in your Claude Code skills directory.
3. Ensure the folder name matches the skill name: `comfyui-workflow-specs`.

### Suggested folder location

- Workspace/local install: `.claude/skills/comfyui-workflow-specs/`
- User install: your Claude Code user skills directory, if you keep skills outside the repo.

## Use

Ask Claude to use the skill when you want to:

- build a new ComfyUI workflow from a description,
- modify an existing workflow (add LoRA, change model, add ControlNet, etc.),
- understand how a workflow is structured,
- or generate a workflow inspired by a reference spec.

## Reference Priority

When Claude needs exact details, it follows this order:

1. Read the compact spec for node types, model names, and wiring patterns.
2. If wiring is still ambiguous, open the matching raw JSON in `references/workflows/`.
3. Use the node catalog (`specs/NODE_CATALOG.md`) for slot order and widgets_values format.
4. Use the format reference (`specs/COMFYUI_FORMAT.md`) for the JSON structure itself.

## Package Note

This folder is designed to be portable as-is. A zip of the skill folder is the easiest way to share it with another Claude Code workspace.