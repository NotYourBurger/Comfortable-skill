# Raw Workflow References

This folder contains the authoritative ComfyUI workflow JSON files that back the compact specs in `../specs/`.

## How To Use

- Read the matching spec first.
- If node placement or wiring is still unclear, open the corresponding JSON file here.
- Treat these files as the source of truth for exact node ids, links, and layout-sensitive behavior.

## Path Convention

- `references/workflows/<workflow-name>.json`

## Priority

1. Spec for fast reasoning.
2. Raw JSON for exact wiring.
3. Layout blueprint for clean node placement.
