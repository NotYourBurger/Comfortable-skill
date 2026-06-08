# ComfyUI Skill Overhaul: From Spec Extractor → Workflow Builder

## Problem

The skill is currently framed as a **spec extraction tool** ("Converts one ComfyUI workflow JSON into a compact spec"). But the user wants it to be a **universal workflow builder** — a skill that lets any LLM (even small ones) create working ComfyUI workflows from scratch.

The existing specs are too vague to reconstruct workflows. Even the best spec (03_FLUX_Schnell_Text2Image) is missing entire nodes, complete link tables, widget values, and node positions. No spec can currently produce a valid workflow JSON.

### Root Causes
1. **SKILL.md is spec-extraction-focused** — 90% of its instructions are about *reading* workflows and *writing* specs, not building workflows
2. **No ComfyUI JSON format reference** — LLMs have no schema to follow when generating workflow JSON
3. **No node catalog** — LLMs don't know exact `class_type` names, slot orders, or `widgets_values` order
4. **Specs use vague language** — "~7 steps", "similar to v1", "various preprocessors"
5. **Specs omit critical wiring data** — No link tables, missing nodes, no slot indices

## User Review Required

> [!IMPORTANT]
> The skill folder will be renamed from `comfyui-workflow-specs` to `comfyui-workflow-builder` to match its new purpose. If you have other tools/configs referencing the old name, they'll need updating.

> [!IMPORTANT]  
> The specs will be **enriched** with structured node tables and link tables extracted from the reference JSONs. This will increase their size (roughly 2-3x) but dramatically improve their usefulness. They remain much smaller than the raw JSONs.

> [!WARNING]  
> For complex workflows with opaque custom nodes (e.g., LTX-V2V, AI-VFX-1.0), even enriched specs won't be fully self-contained. These will always need the reference JSON for exact wiring. The skill will instruct LLMs to fall back to the raw JSON for these cases.

## Open Questions

> [!IMPORTANT]
> **Skill folder renaming**: Should we rename `comfyui-workflow-specs` → `comfyui-workflow-builder`? Or keep the old name to avoid breaking existing setups?

> [!IMPORTANT]
> **Spec enrichment scope**: Should I enrich ALL 27 specs with node/link tables, or focus on the most important ones first? Enriching all 27 will take significant effort but gives the most complete result.

> [!IMPORTANT]
> **Node catalog scope**: The catalog will cover common built-in nodes (CheckpointLoaderSimple, KSampler, CLIPTextEncode, etc.). Should I also try to document the custom nodes used in your workflows (e.g., Florence2, SAM2, DepthCrafter, LTX nodes)? This would be very useful but harder since custom node APIs vary.

---

## Proposed Changes

### Core Skill Instruction

#### [MODIFY] [SKILL.md](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/SKILL.md)

**Complete rewrite.** The new SKILL.md will be structured as:

1. **Identity & Purpose** (new frontmatter) — "Use when building, modifying, or understanding ComfyUI workflows"
2. **Workflow Generation Process** — Step-by-step instructions for creating valid ComfyUI JSON:
   - Parse user requirements into functional lanes (inputs → preprocessing → model → guidance → generation → decode → output)
   - Look up matching reference specs for patterns
   - Build the node table (id, class_type, widgets_values)
   - Wire the link table ([linkID, fromNode, fromSlot, toNode, toSlot, type])
   - Assign positions using layout rules
   - Validate bidirectional link references
3. **Reference Priority** (kept from original) — Spec first → raw JSON if ambiguous → node catalog for slot/widget details
4. **Layout Rules** (kept from original, refined) — Left-to-right flow, lane-based organization
5. **Validation Checklist** (new) — Machine-checkable rules for valid workflow JSON:
   - All link IDs referenced bidirectionally
   - All node IDs unique
   - All type strings match between link tuple and node slots
   - widgets_values length matches node class requirements
   - last_node_id and last_link_id are correct
6. **Common Patterns** (new) — Template-level snippets for:
   - Basic text-to-image (SD1.5, SDXL, FLUX)
   - Image-to-image
   - ControlNet integration
   - LoRA loading
   - Video workflows

**Removed sections:**
- "Handle one workflow JSON at a time" (spec extraction instruction)
- "Reduce the graph to a short spec with these sections" (spec creation)
- "Spec Style" section (spec creation guidelines)
- All language about "summarizing" or "converting" workflows to specs

---

### New Reference Documents

#### [NEW] [COMFYUI_FORMAT.md](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/specs/COMFYUI_FORMAT.md)

A definitive JSON schema reference for the ComfyUI node-graph format. Covers:

1. **Top-level structure** — `id`, `revision`, `last_node_id`, `last_link_id`, `nodes[]`, `links[]`, `groups[]`, `config`, `extra`, `version`
2. **Node object schema** — Every field with type, required/optional, and examples:
   - `id` (int, required, unique)
   - `type` (string, required, exact class_type)
   - `pos` ([x, y], required)
   - `size` ([w, h], required)
   - `inputs[]` — connection inputs vs widget-backed inputs
   - `outputs[]` — with `links` array and `slot_index`
   - `widgets_values[]` — ordered array, class-specific
   - `mode` (0=active, 2=bypass, 4=never)
   - `order` (execution order)
   - `flags`, `properties`, `title`, `color`, `bgcolor`
3. **Link tuple format** — `[linkID, srcNode, srcSlot, tgtNode, tgtSlot, dataType]`
4. **Bidirectional reference rule** — Every link must appear in both the source output's `links[]` and the target input's `link`
5. **Data type system** — MODEL, CLIP, VAE, CONDITIONING, LATENT, IMAGE, MASK, etc.
6. **Minimal valid workflow template** — A complete, copy-pasteable JSON for the simplest possible text-to-image workflow

---

#### [NEW] [NODE_CATALOG.md](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/specs/NODE_CATALOG.md)

A lookup table of common node class_types with exact slot orders and widget_values format:

For each node:
- **class_type** (exact string)
- **Inputs** — ordered list with name, type, connection-or-widget
- **Outputs** — ordered list with name, type, slot_index
- **widgets_values format** — ordered array with types and example values
- **Default size** — typical [w, h]

Nodes to cover:
- **Loaders**: CheckpointLoaderSimple, UNETLoader, DualCLIPLoader, CLIPLoader, VAELoader, LoraLoader, LoraLoaderModelOnly, ControlNetLoader
- **Encoders**: CLIPTextEncode, CLIPSetLastLayer, CLIPVisionEncode, FluxGuidance
- **Latent**: EmptyLatentImage, EmptySD3LatentImage, LatentUpscale, LatentUpscaleBy, LatentComposite
- **Sampling**: KSampler, KSamplerAdvanced, SamplerCustom
- **Decode/Encode**: VAEDecode, VAEEncode, VAEDecodeTiled, VAEEncodeTiled
- **Image**: LoadImage, SaveImage, PreviewImage, ImageScale, ImageScaleBy, ImageResize
- **ControlNet**: ControlNetApply, ControlNetApplyAdvanced
- **Conditioning**: ConditioningCombine, ConditioningSetArea, ConditioningSetMask
- **Mask**: MaskToImage, ImageToMask, InvertMask
- **Video**: VHS_LoadVideo, VHS_VideoCombine (if used in references)
- **Utility**: Note, Reroute, SetNode, GetNode

---

### Spec Enrichment

#### [MODIFY] All 27 spec files in [specs/](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/specs/)

Each spec will be upgraded with a consistent structure:

```markdown
# [Workflow Name]

## Purpose
[1-2 sentence functional description]

## Model Stack
[Exact model filenames, LoRA names with strengths]

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 4  | CheckpointLoaderSimple | `["model.safetensors"]` |
| 6  | CLIPTextEncode | `["positive prompt text"]` |
| ...| ... | ... |

## Link Table  
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 1 | 4.0 | 3.0 | MODEL |
| 2 | 4.1 | 6.0 | CLIP |
| ...| ... | ... | ... |

## Data Flow
[Concise prose description of the pipeline, kept from existing specs but with vague language removed]

## Bus Names (if applicable)
[Set/Get bus names and what they connect]

## Invariants
[Critical constraints that must be preserved]
```

**Key improvements per spec:**
- Remove ALL vague language ("~7 steps" → "7 steps", "similar to v1" → exact details)
- Add complete node table extracted from reference JSON
- Add complete link table extracted from reference JSON
- Ensure no nodes are omitted (the best current spec still misses CLIPSetLastLayer)
- Use exact `class_type` strings, not display titles

---

### Meta Documents

#### [MODIFY] [README.md](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/README.md)

Update to reflect the new purpose:
- "Builds any ComfyUI workflow from requirements or reference specs"
- Remove "Converts one ComfyUI workflow JSON into a compact, high-signal spec"
- Update the "Use" section to focus on workflow creation
- Keep the reference priority section

#### [MODIFY] [LAYOUT_BLUEPRINT.md](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/specs/LAYOUT_BLUEPRINT.md)

Add concrete coordinate ranges and spacing guidelines:
- Default canvas origin and node spacing values
- Per-lane Y-offset ranges (e.g., loaders at Y=0-200, preprocessing at Y=300-500)
- Minimum node separation to avoid overlap

#### [MODIFY] [specs/README.md](file:///t:/TAHMID/Comfy-Claudia/.claude/skills/comfyui-workflow-specs/specs/README.md)

Update to explain the new spec format and how LLMs should use them.

---

## Verification Plan

### Manual Verification
1. **Format validation**: Pick 2-3 enriched specs (default, 03_FLUX, 05_SDXL_ControlNets) and verify every node ID and link ID matches the reference JSON
2. **Reconstruction test**: Ask an LLM to generate a workflow JSON from the enriched default spec + COMFYUI_FORMAT.md + NODE_CATALOG.md, then diff against the original JSON to verify functional equivalence
3. **New workflow test**: Ask an LLM to build a novel workflow (e.g., "SDXL text-to-image with 2 LoRAs and depth ControlNet") using only the skill documents, and verify the output is valid ComfyUI JSON
