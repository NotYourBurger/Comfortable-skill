---
name: comfyui-workflow-specs
description: "Use when building, modifying, or understanding ComfyUI workflows. Generates valid ComfyUI workflow JSON from requirements, specs, or reference workflows. Reference specs provide quick pattern lookup; raw JSONs provide exact wiring."
---

# ComfyUI Workflow Builder

This skill builds valid ComfyUI workflow JSON files. It uses reference specs for pattern recognition and reference workflow JSONs for exact wiring details.

## How to Build a Workflow

### Step 1: Understand the Request

Parse the user's requirements into functional lanes:
1. **Inputs** — What source data enters the workflow (text prompts, images, video, masks)
2. **Model stack** — Which checkpoint, LoRAs, ControlNets, or custom models are needed
3. **Preprocessing** — Any image/video processing before generation (resize, depth extraction, canny, pose)
4. **Conditioning** — How prompts and control signals combine (positive/negative, ControlNet apply, FluxGuidance)
5. **Generation** — The KSampler or equivalent sampling node
6. **Decode** — VAEDecode to convert latent to pixels
7. **Output** — SaveImage, PreviewImage, or video output

### Step 2: Find Matching Reference Patterns

1. Check `specs/` for a spec that matches the requested workflow type
2. The spec gives you the exact node types, model filenames, widget values, and link wiring
3. If the spec's wiring is ambiguous, open the matching raw JSON in `references/workflows/`
4. If no matching spec exists, compose from the common patterns in `specs/NODE_CATALOG.md`

### Step 3: Build the Node Table

For each node in the workflow:
1. Assign a unique integer `id` (start from 1, increment)
2. Set `type` to the exact `class_type` string from the node catalog
3. Set `widgets_values` in the exact order specified by the node catalog
4. Define `inputs` and `outputs` arrays with correct names, types, and slot indices
5. Set `mode` to 0 (active)

### Step 4: Wire the Link Table

For every data connection:
1. Assign a unique integer `link_id` (start from 1, increment)
2. Create the link tuple: `[link_id, source_node_id, source_slot_index, target_node_id, target_slot_index, data_type]`
3. Add `link_id` to the source node's `outputs[source_slot_index].links` array
4. Set the target node's `inputs[target_slot_index].link` to `link_id`
5. Verify `data_type` matches both the source output type and target input type

### Step 5: Assign Layout Positions

Follow the layout rules in `specs/LAYOUT_BLUEPRINT.md`:
- Left-to-right flow: inputs → preprocess → model → conditioning → sampler → decode → output
- One functional branch per horizontal band
- X spacing: 400px between columns
- Y spacing: 250px between rows
- Starting position: [100, 100]

### Step 6: Set Execution Order

Assign `order` values as a topological sort:
- Nodes with no input connections get the lowest values (0, 1, ...)
- Each node's `order` must be higher than all nodes it depends on

### Step 7: Assemble and Validate

Wrap everything in the top-level structure:
```json
{
  "id": "generate-a-uuid",
  "revision": 0,
  "last_node_id": <max node id>,
  "last_link_id": <max link id>,
  "nodes": [...],
  "links": [...],
  "groups": [],
  "config": {},
  "extra": { "ds": { "scale": 1, "offset": [0, 0] } },
  "version": 0.4
}
```

Run the validation checklist before outputting.

## Reference Priority

When you need exact details, follow this order:

1. **Spec** (`specs/*.md`) — Fast lookup for node types, model names, widget values, link wiring
2. **Raw JSON** (`references/workflows/*.json`) — Final authority for exact node definitions, link IDs, and layout
3. **Node Catalog** (`specs/NODE_CATALOG.md`) — Lookup for slot order and widgets_values format for any node type
4. **Format Reference** (`specs/COMFYUI_FORMAT.md`) — Schema reference for the JSON structure itself

## Validation Checklist

Before outputting any workflow JSON, verify:

- [ ] Every node has a unique integer `id`
- [ ] Every node's `type` is an exact ComfyUI `class_type` string
- [ ] Every link tuple `[lid, src, srcSlot, tgt, tgtSlot, type]` exists in the top-level `links` array
- [ ] Every link's `lid` appears in the source node's `outputs[srcSlot].links` array
- [ ] Every link's `lid` equals the target node's `inputs[tgtSlot].link` field
- [ ] Every link's `type` matches both source output type and target input type
- [ ] `widgets_values` arrays follow the exact order from the node catalog
- [ ] `last_node_id` equals the maximum node `id` used
- [ ] `last_link_id` equals the maximum link `id` used
- [ ] `order` values reflect a valid topological sort
- [ ] `version` is `0.4`
- [ ] No node IDs or link IDs are duplicated
- [ ] Unconnected inputs have `"link": null`
- [ ] Unconnected outputs have `"links": []` or `"links": null`

## Layout Rules

When generating or rearranging nodes, keep the graph readable first and compact second.

- Use a left-to-right flow: inputs → preprocess → model → guidance → sampler/generation → decode → output
- Keep one functional branch per horizontal band when multiple alternatives exist
- Group related nodes in consistent spacing blocks
- Keep control images, masks, and reference images in their own sublane before they enter the generator
- Keep output previews and save nodes separated from the generation spine
- If a workflow has parallel examples, place each as a clearly labeled lane with matching vertical alignment
- Preserve the exact functional order from the spec even if coordinate layout changes

### Concrete Spacing Defaults

| Lane | X Range | Description |
|------|---------|-------------|
| Sources / Inputs | 0–400 | LoadImage, LoadVideo, text inputs |
| Model Loading | 400–800 | CheckpointLoader, LoraLoader, VAELoader |
| Preprocessing | 800–1200 | Depth extraction, canny, resize, ControlNet prep |
| Conditioning | 1200–1600 | CLIPTextEncode, FluxGuidance, ControlNetApply |
| Generation | 1600–2000 | KSampler |
| Decode | 2000–2400 | VAEDecode |
| Output | 2400–2800 | SaveImage, PreviewImage |

- Y offset per branch: start at 100, add 300 per additional branch
- Node width: typically 270–420
- Node height: varies by widget count (100 for simple, 250–500 for complex)
- Minimum gap between nodes: 50px horizontal, 30px vertical

## Workflow Modification

When modifying an existing workflow:

1. Load and parse the existing JSON
2. Identify what needs to change (add nodes, remove nodes, change connections, update values)
3. When adding nodes: use IDs higher than `last_node_id`, create new links with IDs higher than `last_link_id`
4. When removing nodes: remove all links referencing that node from both the `links` array and from other nodes' input/output references
5. Update `last_node_id` and `last_link_id` after changes
6. Re-validate using the checklist

## Clean Organization Checklist

Before considering a workflow finished, confirm that:

- No important nodes overlap each other
- Each branch can be traced visually from source to output
- Control lanes are not mixed with model-loading lanes
- All buses used by Set/Get pairs are easy to spot
- Reroutes are only used to tidy connections, not hide structure

## Custom and Opaque Nodes

Some workflows use custom nodes whose internal behavior cannot be inferred from the graph alone. When encountering these:

1. Check if the spec documents the node's behavior
2. If not, check the reference JSON for the exact node definition
3. Copy the node definition exactly from the reference — do not guess widgets_values for custom nodes
4. Note the custom node in comments so users know a specific extension is required
