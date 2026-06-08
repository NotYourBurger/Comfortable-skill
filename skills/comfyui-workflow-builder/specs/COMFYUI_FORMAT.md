# ComfyUI Workflow JSON Format Reference

This document is the definitive schema reference for the ComfyUI node-graph JSON format. Use it when generating or modifying workflow JSON files.

## Top-Level Structure

```json
{
  "id": "uuid-string",
  "revision": 0,
  "last_node_id": 9,
  "last_link_id": 9,
  "nodes": [],
  "links": [],
  "groups": [],
  "config": {},
  "extra": {
    "ds": { "scale": 1.0, "offset": [0, 0] }
  },
  "version": 0.4
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | UUID for the workflow |
| `revision` | int | yes | Revision counter, start at 0 |
| `last_node_id` | int | yes | Highest node ID used. Must equal max of all `nodes[].id` |
| `last_link_id` | int | yes | Highest link ID used. Must equal max of all `links[][0]` |
| `nodes` | array | yes | Array of node objects |
| `links` | array | yes | Array of link tuples |
| `groups` | array | yes | Array of visual group objects (can be empty `[]`) |
| `config` | object | yes | Usually empty `{}` |
| `extra` | object | yes | UI metadata. Must contain `ds` with `scale` and `offset` |
| `version` | float | yes | Always `0.4` |

## Node Object

```json
{
  "id": 3,
  "type": "KSampler",
  "pos": [863, 186],
  "size": [315, 262],
  "flags": {},
  "order": 4,
  "mode": 0,
  "inputs": [],
  "outputs": [],
  "properties": { "Node name for S&R": "KSampler" },
  "widgets_values": [156680208700286, "randomize", 20, 8, "euler", "normal", 1],
  "title": "My Custom Title",
  "color": "#322",
  "bgcolor": "#533"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | int | yes | Unique integer ID within the workflow |
| `type` | string | yes | Exact registered `class_type` name. Must match ComfyUI's node registry exactly |
| `pos` | [x, y] | yes | Canvas position. x increases rightward, y increases downward |
| `size` | [w, h] | yes | Node widget dimensions |
| `flags` | object | yes | Visual flags. Can be `{}` or `{"collapsed": true}` |
| `order` | int | yes | Execution order (topological sort). 0 = first to execute |
| `mode` | int | yes | 0 = active, 2 = bypassed, 4 = never execute |
| `inputs` | array | yes | Array of input slot objects |
| `outputs` | array | yes | Array of output slot objects |
| `properties` | object | yes | Metadata. Typically `{"Node name for S&R": "ClassName"}` |
| `widgets_values` | array | yes | Ordered array of widget default values. Order is class-specific |
| `title` | string | no | Custom display title (overrides default) |
| `color` | string | no | Custom border color (hex) |
| `bgcolor` | string | no | Custom background color (hex) |

### Input Slot Object

Two kinds of inputs exist:

**Connection-only input** (receives data from another node's output):
```json
{
  "name": "model",
  "type": "MODEL",
  "link": 1
}
```

**Widget-backed input** (can receive connection OR use widgets_values):
```json
{
  "name": "seed",
  "type": "INT",
  "widget": { "name": "seed" },
  "link": null
}
```

| Field | Type | Description |
|---|---|---|
| `name` | string | Internal slot name (required) |
| `type` | string | Data type. Must match the connected output's type |
| `link` | int or null | Link ID connecting to this input. `null` if unconnected |
| `widget` | object | Present ONLY for widget-backed inputs. Contains `{"name": "widget_name"}` |
| `localized_name` | string | Display name (optional, often same as `name`) |

**Rule**: An input can have at most ONE link (fan-in = 1).

### Output Slot Object

```json
{
  "name": "MODEL",
  "type": "MODEL",
  "slot_index": 0,
  "links": [1, 12]
}
```

| Field | Type | Description |
|---|---|---|
| `name` | string | Output slot name (required) |
| `type` | string | Data type (required) |
| `slot_index` | int | Position index of this output slot |
| `links` | array or null | Array of link IDs going FROM this output. `null` or `[]` if unconnected |
| `localized_name` | string | Display name (optional) |

**Rule**: An output can have MULTIPLE links (fan-out = unlimited).

## Link Tuple Format

Each link in the top-level `links` array is a 6-element tuple:

```
[link_id, source_node_id, source_slot_index, target_node_id, target_slot_index, data_type]
```

| Position | Type | Description |
|---|---|---|
| 0 | int | Unique link ID |
| 1 | int | Source node's `id` |
| 2 | int | Source node's output `slot_index` |
| 3 | int | Target node's `id` |
| 4 | int | Position in target node's `inputs` array |
| 5 | string | Data type (must match source output type AND target input type) |

### Example

```json
[3, 4, 1, 6, 0, "CLIP"]
```
Means: Link #3 connects node 4's output slot 1 (CLIP) to node 6's input slot 0 (clip).

## Bidirectional Reference Rule (CRITICAL)

Every link must be referenced in THREE places:

1. **Top-level `links` array**: `[linkID, srcNode, srcSlot, tgtNode, tgtSlot, type]`
2. **Source node's output**: `outputs[srcSlot].links` array must contain `linkID`
3. **Target node's input**: `inputs[tgtSlot].link` must equal `linkID`

**If any of these three references is missing, the workflow will fail to load.**

### Verification Example

For link `[3, 4, 1, 6, 0, "CLIP"]`:
- - `links` array contains `[3, 4, 1, 6, 0, "CLIP"]`
- - Node 4's `outputs[1].links` contains `3`
- - Node 6's `inputs[0].link` equals `3`

## Data Type System

| Type | Description | Typical Producers | Typical Consumers |
|---|---|---|---|
| `MODEL` | Diffusion model (UNet) | CheckpointLoaderSimple, UNETLoader, LoraLoader | KSampler, ControlNetApply |
| `CLIP` | Text encoder | CheckpointLoaderSimple, DualCLIPLoader, LoraLoader | CLIPTextEncode, CLIPSetLastLayer |
| `VAE` | Variational autoencoder | CheckpointLoaderSimple, VAELoader | VAEDecode, VAEEncode |
| `CONDITIONING` | Encoded prompt/guidance | CLIPTextEncode, ControlNetApply, FluxGuidance | KSampler (positive/negative) |
| `LATENT` | Latent space tensor | EmptyLatentImage, KSampler, VAEEncode | KSampler, VAEDecode |
| `IMAGE` | Pixel image tensor | LoadImage, VAEDecode, PreviewImage | SaveImage, VAEEncode, ControlNetApply |
| `MASK` | Single-channel mask | LoadImage (slot 1), MaskToImage | ConditioningSetMask, ImageCompositeMasked |
| `CONTROL_NET` | ControlNet model | ControlNetLoader | ControlNetApply |
| `INT` | Integer | PrimitiveNode | Widget inputs |
| `FLOAT` | Float | PrimitiveNode | Widget inputs |
| `STRING` | Text string | PrimitiveNode | Widget inputs |

## Execution Order

The `order` field on each node must be a valid topological sort of the DAG:
- Nodes with no input connections get the lowest `order` values
- A node's `order` must be greater than the `order` of all nodes it depends on
- Multiple independent nodes can share the same `order` level

## Minimal Valid Workflow (SD 1.5 Text-to-Image)

This is a complete, valid workflow JSON for basic text-to-image generation:

```json
{
  "id": "00000000-0000-0000-0000-000000000000",
  "revision": 0,
  "last_node_id": 9,
  "last_link_id": 9,
  "nodes": [
    {
      "id": 4,
      "type": "CheckpointLoaderSimple",
      "pos": [26, 474],
      "size": [315, 98],
      "flags": {},
      "order": 0,
      "mode": 0,
      "inputs": [
        {"name": "ckpt_name", "type": "COMBO", "widget": {"name": "ckpt_name"}, "link": null}
      ],
      "outputs": [
        {"name": "MODEL", "type": "MODEL", "slot_index": 0, "links": [1]},
        {"name": "CLIP", "type": "CLIP", "slot_index": 1, "links": [3, 5]},
        {"name": "VAE", "type": "VAE", "slot_index": 2, "links": [8]}
      ],
      "properties": {"Node name for S&R": "CheckpointLoaderSimple"},
      "widgets_values": ["v1-5-pruned-emaonly-fp16.safetensors"]
    },
    {
      "id": 6,
      "type": "CLIPTextEncode",
      "pos": [415, 186],
      "size": [422, 164],
      "flags": {},
      "order": 1,
      "mode": 0,
      "inputs": [
        {"name": "clip", "type": "CLIP", "link": 3},
        {"name": "text", "type": "STRING", "widget": {"name": "text"}, "link": null}
      ],
      "outputs": [
        {"name": "CONDITIONING", "type": "CONDITIONING", "slot_index": 0, "links": [4]}
      ],
      "properties": {"Node name for S&R": "CLIPTextEncode"},
      "widgets_values": ["beautiful scenery nature glass bottle landscape, purple galaxy bottle"]
    },
    {
      "id": 7,
      "type": "CLIPTextEncode",
      "pos": [413, 389],
      "size": [425, 180],
      "flags": {},
      "order": 2,
      "mode": 0,
      "inputs": [
        {"name": "clip", "type": "CLIP", "link": 5},
        {"name": "text", "type": "STRING", "widget": {"name": "text"}, "link": null}
      ],
      "outputs": [
        {"name": "CONDITIONING", "type": "CONDITIONING", "slot_index": 0, "links": [6]}
      ],
      "properties": {"Node name for S&R": "CLIPTextEncode"},
      "widgets_values": ["text, watermark"]
    },
    {
      "id": 5,
      "type": "EmptyLatentImage",
      "pos": [473, 609],
      "size": [315, 106],
      "flags": {},
      "order": 3,
      "mode": 0,
      "inputs": [
        {"name": "width", "type": "INT", "widget": {"name": "width"}, "link": null},
        {"name": "height", "type": "INT", "widget": {"name": "height"}, "link": null},
        {"name": "batch_size", "type": "INT", "widget": {"name": "batch_size"}, "link": null}
      ],
      "outputs": [
        {"name": "LATENT", "type": "LATENT", "slot_index": 0, "links": [2]}
      ],
      "properties": {"Node name for S&R": "EmptyLatentImage"},
      "widgets_values": [512, 512, 1]
    },
    {
      "id": 3,
      "type": "KSampler",
      "pos": [863, 186],
      "size": [315, 262],
      "flags": {},
      "order": 4,
      "mode": 0,
      "inputs": [
        {"name": "model", "type": "MODEL", "link": 1},
        {"name": "positive", "type": "CONDITIONING", "link": 4},
        {"name": "negative", "type": "CONDITIONING", "link": 6},
        {"name": "latent_image", "type": "LATENT", "link": 2},
        {"name": "seed", "type": "INT", "widget": {"name": "seed"}, "link": null},
        {"name": "steps", "type": "INT", "widget": {"name": "steps"}, "link": null},
        {"name": "cfg", "type": "FLOAT", "widget": {"name": "cfg"}, "link": null},
        {"name": "sampler_name", "type": "COMBO", "widget": {"name": "sampler_name"}, "link": null},
        {"name": "scheduler", "type": "COMBO", "widget": {"name": "scheduler"}, "link": null},
        {"name": "denoise", "type": "FLOAT", "widget": {"name": "denoise"}, "link": null}
      ],
      "outputs": [
        {"name": "LATENT", "type": "LATENT", "slot_index": 0, "links": [7]}
      ],
      "properties": {"Node name for S&R": "KSampler"},
      "widgets_values": [156680208700286, "randomize", 20, 8, "euler", "normal", 1]
    },
    {
      "id": 8,
      "type": "VAEDecode",
      "pos": [1209, 188],
      "size": [210, 46],
      "flags": {},
      "order": 5,
      "mode": 0,
      "inputs": [
        {"name": "samples", "type": "LATENT", "link": 7},
        {"name": "vae", "type": "VAE", "link": 8}
      ],
      "outputs": [
        {"name": "IMAGE", "type": "IMAGE", "slot_index": 0, "links": [9]}
      ],
      "properties": {"Node name for S&R": "VAEDecode"},
      "widgets_values": []
    },
    {
      "id": 9,
      "type": "SaveImage",
      "pos": [1451, 189],
      "size": [210, 58],
      "flags": {},
      "order": 6,
      "mode": 0,
      "inputs": [
        {"name": "images", "type": "IMAGE", "link": 9},
        {"name": "filename_prefix", "type": "STRING", "widget": {"name": "filename_prefix"}, "link": null}
      ],
      "outputs": [],
      "properties": {},
      "widgets_values": ["ComfyUI"]
    }
  ],
  "links": [
    [1, 4, 0, 3, 0, "MODEL"],
    [2, 5, 0, 3, 3, "LATENT"],
    [3, 4, 1, 6, 0, "CLIP"],
    [4, 6, 0, 3, 1, "CONDITIONING"],
    [5, 4, 1, 7, 0, "CLIP"],
    [6, 7, 0, 3, 2, "CONDITIONING"],
    [7, 3, 0, 8, 0, "LATENT"],
    [8, 4, 2, 8, 1, "VAE"],
    [9, 8, 0, 9, 0, "IMAGE"]
  ],
  "groups": [],
  "config": {},
  "extra": { "ds": { "scale": 1, "offset": [0, 0] } },
  "version": 0.4
}
```

## Common Pitfalls

1. **Forgetting bidirectional link references** - Every link ID must appear in the `links` array, the source output's `links` array, AND the target input's `link` field
2. **Wrong widgets_values order** - Each node class has its own implicit widget order. Check the NODE_CATALOG.md for exact ordering
3. **Wrong slot indices** - KSampler has 4 connection inputs (model, positive, negative, latent_image) at slots 0-3, then 6 widget inputs (seed, steps, cfg, sampler_name, scheduler, denoise) at slots 4-9
4. **Mismatched data types** - The type in the link tuple must match both the source output type and target input type exactly
5. **Missing `version: 0.4`** - Required for ComfyUI to load the workflow
6. **Wrong `last_node_id` / `last_link_id`** - Must equal the maximum ID actually used
7. **Invalid `order` values** - Must reflect a valid topological sort

