# ComfyUI Node Catalog

Quick-reference for common node `class_type` names, their inputs, outputs, and `widgets_values` order. Use this when building workflow JSON to ensure correct slot indices and widget ordering.

## How to Read This Catalog

For each node:
- **class_type**: The exact string to use in the node's `type` field
- **Connection Inputs**: Inputs that receive data via links (listed by slot index)
- **Widget Inputs**: Inputs backed by widgets (values come from `widgets_values` array)
- **Outputs**: Output slots (listed by slot index)
- **widgets_values**: The exact order and types for the `widgets_values` array

---

## Model Loaders

### CheckpointLoaderSimple
Load a checkpoint model (combined MODEL + CLIP + VAE).

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | ckpt_name | COMBO |
| **Out** | 0 | MODEL | MODEL |
| **Out** | 1 | CLIP | CLIP |
| **Out** | 2 | VAE | VAE |

**widgets_values**: `["checkpoint_filename.safetensors"]`

---

### UNETLoader
Load a standalone UNet/diffusion model (no CLIP or VAE).

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | unet_name | COMBO |
| **Widget** | — | weight_dtype | COMBO |
| **Out** | 0 | MODEL | MODEL |

**widgets_values**: `["model_filename.safetensors", "default"]`

---

### DualCLIPLoader
Load two CLIP models (e.g., for FLUX which uses both clip_l and t5xxl).

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | clip_name1 | COMBO |
| **Widget** | — | clip_name2 | COMBO |
| **Widget** | — | type | COMBO |
| **Out** | 0 | CLIP | CLIP |

**widgets_values**: `["clip_l.safetensors", "t5xxl_fp16.safetensors", "flux"]`

---

### VAELoader
Load a standalone VAE model.

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | vae_name | COMBO |
| **Out** | 0 | VAE | VAE |

**widgets_values**: `["vae_filename.safetensors"]`

---

### LoraLoader
Apply a LoRA to both MODEL and CLIP.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | model | MODEL |
| **In** | 1 | clip | CLIP |
| **Widget** | — | lora_name | COMBO |
| **Widget** | — | strength_model | FLOAT |
| **Widget** | — | strength_clip | FLOAT |
| **Out** | 0 | MODEL | MODEL |
| **Out** | 1 | CLIP | CLIP |

**widgets_values**: `["lora_filename.safetensors", 1.0, 1.0]`

---

### LoraLoaderModelOnly
Apply a LoRA to MODEL only (no CLIP modification).

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | model | MODEL |
| **Widget** | — | lora_name | COMBO |
| **Widget** | — | strength_model | FLOAT |
| **Out** | 0 | MODEL | MODEL |

**widgets_values**: `["lora_filename.safetensors", 1.0]`

---

### ControlNetLoader
Load a ControlNet model.

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | control_net_name | COMBO |
| **Out** | 0 | CONTROL_NET | CONTROL_NET |

**widgets_values**: `["controlnet_filename.safetensors"]`

---

## Text Encoding

### CLIPTextEncode
Encode text prompt into conditioning using CLIP.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | clip | CLIP |
| **Widget** | — | text | STRING |
| **Out** | 0 | CONDITIONING | CONDITIONING |

**widgets_values**: `["your prompt text here"]`

---

### CLIPSetLastLayer
Modify CLIP to stop at a specific layer (commonly -1 or -2).

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | clip | CLIP |
| **Widget** | — | stop_at_clip_layer | INT |
| **Out** | 0 | CLIP | CLIP |

**widgets_values**: `[-1]`

---

### CLIPVisionEncode
Encode an image using CLIP Vision (for IP-Adapter, style transfer).

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | clip_vision | CLIP_VISION |
| **In** | 1 | image | IMAGE |
| **Out** | 0 | CLIP_VISION_OUTPUT | CLIP_VISION_OUTPUT |

**widgets_values**: `[]`

---

### FluxGuidance
Apply guidance scaling for FLUX models (replaces CFG for FLUX).

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | conditioning | CONDITIONING |
| **Widget** | — | guidance | FLOAT |
| **Out** | 0 | CONDITIONING | CONDITIONING |

**widgets_values**: `[4.0]`

---

## Latent Image

### EmptyLatentImage
Create a blank latent (for SD 1.5 / SDXL).

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | width | INT |
| **Widget** | — | height | INT |
| **Widget** | — | batch_size | INT |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `[512, 512, 1]` (SD 1.5) or `[1024, 1024, 1]` (SDXL)

---

### EmptySD3LatentImage
Create a blank latent (for FLUX / SD3).

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | width | INT |
| **Widget** | — | height | INT |
| **Widget** | — | batch_size | INT |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `[1024, 1024, 1]`

---

### LatentUpscale
Upscale a latent image.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | samples | LATENT |
| **Widget** | — | upscale_method | COMBO |
| **Widget** | — | width | INT |
| **Widget** | — | height | INT |
| **Widget** | — | crop | COMBO |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `["nearest-exact", 1024, 1024, "disabled"]`

---

### LatentUpscaleBy
Upscale a latent by a scale factor.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | samples | LATENT |
| **Widget** | — | upscale_method | COMBO |
| **Widget** | — | scale_by | FLOAT |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `["nearest-exact", 2.0]`

---

## Sampling

### KSampler
The primary sampling node. Has 4 connection inputs + 6 widget inputs.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | model | MODEL |
| **In** | 1 | positive | CONDITIONING |
| **In** | 2 | negative | CONDITIONING |
| **In** | 3 | latent_image | LATENT |
| **Widget** | 4 | seed | INT |
| **Widget** | 5 | control_after_generate (hidden) | COMBO |
| **Widget** | 6 | steps | INT |
| **Widget** | 7 | cfg | FLOAT |
| **Widget** | 8 | sampler_name | COMBO |
| **Widget** | 9 | scheduler | COMBO |
| **Widget** | 10 | denoise | FLOAT |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `[seed_number, "randomize", steps, cfg, "sampler_name", "scheduler", denoise]`

Example: `[156680208700286, "randomize", 20, 8, "euler", "normal", 1]`

Common sampler_name values: `"euler"`, `"euler_ancestral"`, `"dpmpp_2m"`, `"dpmpp_sde"`, `"dpmpp_2m_sde"`, `"uni_pc"`, `"ddim"`

Common scheduler values: `"normal"`, `"karras"`, `"exponential"`, `"sgm_uniform"`, `"simple"`, `"ddim_uniform"`, `"beta"`

---

### KSamplerAdvanced
Advanced sampler with separate start/end steps and noise control.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | model | MODEL |
| **In** | 1 | positive | CONDITIONING |
| **In** | 2 | negative | CONDITIONING |
| **In** | 3 | latent_image | LATENT |
| **Widget** | 4 | add_noise | COMBO |
| **Widget** | 5 | noise_seed | INT |
| **Widget** | 6 | control_after_generate (hidden) | COMBO |
| **Widget** | 7 | steps | INT |
| **Widget** | 8 | cfg | FLOAT |
| **Widget** | 9 | sampler_name | COMBO |
| **Widget** | 10 | scheduler | COMBO |
| **Widget** | 11 | start_at_step | INT |
| **Widget** | 12 | end_at_step | INT |
| **Widget** | 13 | return_with_leftover_noise | COMBO |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `["enable", seed, "randomize", 20, 8, "euler", "normal", 0, 20, "disable"]`

---

## Decode / Encode

### VAEDecode
Decode latent tensor to pixel image.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | samples | LATENT |
| **In** | 1 | vae | VAE |
| **Out** | 0 | IMAGE | IMAGE |

**widgets_values**: `[]`

---

### VAEEncode
Encode pixel image to latent tensor.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | pixels | IMAGE |
| **In** | 1 | vae | VAE |
| **Out** | 0 | LATENT | LATENT |

**widgets_values**: `[]`

---

### VAEDecodeTiled
Tiled VAE decode for high-resolution images (avoids VRAM limits).

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | samples | LATENT |
| **In** | 1 | vae | VAE |
| **Widget** | — | tile_size | INT |
| **Out** | 0 | IMAGE | IMAGE |

**widgets_values**: `[512]`

---

## Image I/O

### LoadImage
Load an image from disk.

| | Slot | Name | Type |
|--|------|------|------|
| **Widget** | — | image | COMBO |
| **Widget** | — | upload | IMAGEUPLOAD |
| **Out** | 0 | IMAGE | IMAGE |
| **Out** | 1 | MASK | MASK |

**widgets_values**: `["filename.png", "image"]`

---

### SaveImage
Save image to disk.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | images | IMAGE |
| **Widget** | — | filename_prefix | STRING |
| **Out** | — | — | — |

**widgets_values**: `["ComfyUI"]`

---

### PreviewImage
Preview image in the UI (does not save to disk).

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | images | IMAGE |
| **Out** | — | — | — |

**widgets_values**: `[]`

---

## Image Processing

### ImageScale
Resize an image to specific dimensions.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | image | IMAGE |
| **Widget** | — | upscale_method | COMBO |
| **Widget** | — | width | INT |
| **Widget** | — | height | INT |
| **Widget** | — | crop | COMBO |
| **Out** | 0 | IMAGE | IMAGE |

**widgets_values**: `["bilinear", 1024, 1024, "disabled"]`

---

### ImageScaleBy
Scale an image by a factor.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | image | IMAGE |
| **Widget** | — | upscale_method | COMBO |
| **Widget** | — | scale_by | FLOAT |
| **Out** | 0 | IMAGE | IMAGE |

**widgets_values**: `["bilinear", 2.0]`

---

## ControlNet

### ControlNetApplyAdvanced
Apply a ControlNet with strength and range control.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | positive | CONDITIONING |
| **In** | 1 | negative | CONDITIONING |
| **In** | 2 | control_net | CONTROL_NET |
| **In** | 3 | image | IMAGE |
| **Widget** | — | strength | FLOAT |
| **Widget** | — | start_percent | FLOAT |
| **Widget** | — | end_percent | FLOAT |
| **Out** | 0 | positive | CONDITIONING |
| **Out** | 1 | negative | CONDITIONING |

**widgets_values**: `[1.0, 0.0, 1.0]`

---

## Conditioning

### ConditioningCombine
Combine two conditioning inputs.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | conditioning_1 | CONDITIONING |
| **In** | 1 | conditioning_2 | CONDITIONING |
| **Out** | 0 | CONDITIONING | CONDITIONING |

**widgets_values**: `[]`

---

### ConditioningSetMask
Apply a mask to conditioning for inpainting.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | conditioning | CONDITIONING |
| **In** | 1 | mask | MASK |
| **Widget** | — | strength | FLOAT |
| **Widget** | — | set_cond_area | COMBO |
| **Out** | 0 | CONDITIONING | CONDITIONING |

**widgets_values**: `[1.0, "default"]`

---

## Mask Operations

### InvertMask

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | mask | MASK |
| **Out** | 0 | MASK | MASK |

**widgets_values**: `[]`

---

### ImageToMask
Extract a channel from an image as a mask.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | image | IMAGE |
| **Widget** | — | channel | COMBO |
| **Out** | 0 | MASK | MASK |

**widgets_values**: `["red"]`

---

### MaskToImage
Convert a mask to an image.

| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | mask | MASK |
| **Out** | 0 | IMAGE | IMAGE |

**widgets_values**: `[]`

---

## Utility Nodes

### Note
Visual-only note node. Does not affect execution.

**widgets_values**: `["note text"]`

No inputs or outputs.

---

### SetNode / GetNode (Set/Get Buses)
Named data buses for passing data without visible links.

**SetNode**:
| | Slot | Name | Type |
|--|------|------|------|
| **In** | 0 | (dynamic) | (dynamic) |

**GetNode**:
| | Slot | Name | Type |
|--|------|------|------|
| **Out** | 0 | (dynamic) | (dynamic) |

Set/Get pairs are matched by their internal bus name. The type is determined by whatever connects to the Set node.

---

## Common Workflow Patterns

### SD 1.5 / SDXL Text-to-Image
```
CheckpointLoaderSimple → MODEL → KSampler
                       → CLIP → CLIPTextEncode (positive) → KSampler
                       → CLIP → CLIPTextEncode (negative) → KSampler
                       → VAE → VAEDecode
EmptyLatentImage → LATENT → KSampler → LATENT → VAEDecode → IMAGE → SaveImage
```

### FLUX Text-to-Image
```
CheckpointLoaderSimple → MODEL → KSampler
                       → CLIP → CLIPSetLastLayer → CLIPTextEncode (positive) → FluxGuidance → KSampler
                       → CLIP → CLIPTextEncode (negative) → KSampler
                       → VAE → VAEDecode
EmptySD3LatentImage → LATENT → KSampler → LATENT → VAEDecode → IMAGE → SaveImage
```
Key differences from SD: uses `EmptySD3LatentImage`, adds `CLIPSetLastLayer` and `FluxGuidance`, CFG=1, 4 steps for Schnell / 20 for Dev.

### Adding a LoRA
Insert `LoraLoader` between CheckpointLoaderSimple and the rest:
```
CheckpointLoaderSimple → MODEL → LoraLoader → MODEL → KSampler
                       → CLIP → LoraLoader → CLIP → CLIPTextEncode...
```

### Adding ControlNet
```
ControlNetLoader → CONTROL_NET ─┐
LoadImage (control image) → IMAGE ─┤
                                    ├→ ControlNetApplyAdvanced → positive CONDITIONING → KSampler
CLIPTextEncode (positive) → CONDITIONING ─┘                   → negative CONDITIONING → KSampler
CLIPTextEncode (negative) → CONDITIONING ─┘
```

### Image-to-Image
Replace `EmptyLatentImage` with:
```
LoadImage → IMAGE → VAEEncode → LATENT → KSampler (denoise < 1.0)
```
