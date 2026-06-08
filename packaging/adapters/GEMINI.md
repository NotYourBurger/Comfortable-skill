# ComfyUI Workflow Builder Skill

For ComfyUI workflow tasks, use the portable skill folder:

```text
skills/comfyui-workflow-builder
```

Start with `SKILL.md`. Use `specs/*.md` for compact workflow patterns, `specs/COMFYUI_FORMAT.md` for the JSON graph schema, `specs/NODE_CATALOG.md` for common node slot/widget order, and `references/workflows/*.json` for exact custom-node wiring.

Before producing a workflow, verify every link appears in the top-level `links` array, the source output `links` array, and the target input `link` field.
