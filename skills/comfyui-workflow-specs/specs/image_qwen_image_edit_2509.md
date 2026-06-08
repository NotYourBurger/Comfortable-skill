# image_qwen_image_edit_2509

## Purpose
Qwen Image Edit 2509 template with two parallel edit branches (subgraph nodes) from the same base image and prompt, each containing a full Qwen image-edit pipeline with Lightning LoRA turbo mode switching.

## Model Stack
- Diffusion model: `qwen_image_edit_2509_fp8_e4m3fn.safetensors` (UNETLoader inside subgraphs)
- LoRA: `Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors` (LoraLoaderModelOnly, strength=1)
- Text encoder: `qwen_2.5_vl_7b_fp8_scaled.safetensors` (CLIPLoader, type=qwen_image)
- VAE: `qwen_image_vae.safetensors` (VAELoader)

## Node Table

### Top-Level Nodes
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 99 | MarkdownNote | Model links and setup instructions |
| 78 | LoadImage | `["BASE_IMAGE.png", "image"]` |
| 435 | PrimitiveStringMultiline | `["retouch this girl don't change her face but increase the glamour..."]` |
| 433 | eba40a3a-f6c5-48ac-b58e-55525d06b373 | Subgraph: "Image Edit (Qwen 2509)" — mode 0 (active) |
| 60 | SaveImage | `["ComfyUI"]` — mode 0 (active) |
| 466 | c7f5c302-e46e-4a0f-91bd-0aec474e7659 | Subgraph: "Image Edit (Qwen 2509 Raw Latent)" — mode 4 (bypassed) |
| 342 | SaveImage | `["ComfyUI"]` — mode 4 (bypassed) |

### Subgraph "Image Edit (Qwen 2509)" (id: eba40a3a) — Internal Nodes
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 37 | UNETLoader | `["Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors", "default"]` |
| 38 | CLIPLoader | `["qwen_2.5_vl_7b_fp8_scaled.safetensors", "qwen_image", "default"]` |
| 39 | VAELoader | `["qwen_image_vae.safetensors"]` |
| 117 | FluxKontextImageScale | `[]` |
| 88 | VAEEncode | `[]` |
| 110 | TextEncodeQwenImageEditPlus | `[""]` (negative conditioning) |
| 111 | TextEncodeQwenImageEditPlus | `[""]` (positive conditioning) |
| 89 | LoraLoaderModelOnly | `["Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors", 1]` |
| 438 | PrimitiveInt | Steps (original): `[20, "fixed"]` |
| 439 | PrimitiveFloat | CFG (original): `[4]` |
| 436 | PrimitiveInt | Steps (lightning): `[4, "fixed"]` |
| 437 | PrimitiveFloat | CFG (lightning): `[1]` |
| 443 | PrimitiveBoolean | Enable Lightning LoRA: `[true]` |
| 440 | ComfySwitchNode | Switch (Model): `[false]` |
| 441 | ComfySwitchNode | Switch (Steps): `[false]` |
| 442 | ComfySwitchNode | Switch (CFG): `[false]` |
| 66 | ModelSamplingAuraFlow | `[3]` |
| 75 | CFGNorm | `[1, false]` |
| 3 | KSampler | `[<seed>, "randomize", 4, 1, "euler", "simple", 1]` |
| 8 | VAEDecode | `[]` |
| 444 | MarkdownNote | KSampler settings reference table |

### Subgraph "Image Edit (Qwen 2509 Raw Latent)" (id: c7f5c302) — Internal Nodes
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 448 | UNETLoader | `["qwen_image_edit_2509_fp8_e4m3fn.safetensors", "default"]` |
| 447 | CLIPLoader | `["qwen_2.5_vl_7b_fp8_scaled.safetensors", "qwen_image", "default"]` |
| 446 | VAELoader | `["qwen_image_vae.safetensors"]` |
| 455 | FluxKontextImageScale | `[]` |
| 452 | VAEEncode | `[]` |
| 449 | TextEncodeQwenImageEditPlus | `[""]` (negative conditioning) |
| 451 | TextEncodeQwenImageEditPlus | `[""]` (positive conditioning) |
| 454 | LoraLoaderModelOnly | `["Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors", 1]` |
| 459 | PrimitiveInt | Steps (original): `[20, "fixed"]` |
| 460 | PrimitiveFloat | CFG (original): `[4]` |
| 457 | PrimitiveInt | Steps (lightning): `[4, "fixed"]` |
| 458 | PrimitiveFloat | CFG (lightning): `[1]` |
| 464 | PrimitiveBoolean | Enable Lightning LoRA: `[true]` |
| 461 | ComfySwitchNode | Switch (Model): `[false]` |
| 462 | ComfySwitchNode | Switch (Steps): `[false]` |
| 463 | ComfySwitchNode | Switch (CFG): `[false]` |
| 450 | ModelSamplingAuraFlow | `[3]` |
| 445 | CFGNorm | `[1, false]` |
| 456 | KSampler | `[<seed>, "randomize", 4, 1, "euler", "simple", 1]` |
| 453 | VAEDecode | `[]` |
| 467 | ReferenceLatent | `[]` (positive path) |
| 468 | ReferenceLatent | `[]` (negative path) |
| 465 | MarkdownNote | KSampler settings reference table |

## Link Table

### Top-Level Links
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 695 | 78.0 | 433.0 | IMAGE |
| 696 | 433.0 | 60.0 | IMAGE |
| 705 | 435.0 | 433.3 | STRING |
| 723 | 78.0 | 466.0 | IMAGE |
| 724 | 435.0 | 466.3 | STRING |
| 725 | 466.0 | 342.0 | IMAGE |

### Subgraph "eba40a3a" Internal Links
| LinkID | From → To | Type |
|--------|-----------|------|
| 141 | 66.0 → 75.0 | MODEL |
| 128 | 3.0 → 8.0 | LATENT |
| 76 | 39.0 → 8.1 | VAE |
| 184 | 37.0 → 89.0 | MODEL |
| 186 | 75.0 → 3.0 | MODEL |
| 211 | 111.0 → 3.1 | CONDITIONING |
| 210 | 110.0 → 3.2 | CONDITIONING |
| 168 | 39.0 → 88.1 | VAE |
| 204 | 38.0 → 110.0 | CLIP |
| 206 | 39.0 → 110.1 | VAE |
| 205 | 38.0 → 111.0 | CLIP |
| 207 | 39.0 → 111.1 | VAE |
| 110 | 8.0 → output | IMAGE |
| 235 | input.1 → 111.3 | IMAGE |
| 236 | input.1 → 110.3 | IMAGE |
| 237 | input.2 → 111.4 | IMAGE |
| 238 | input.2 → 110.4 | IMAGE |
| 244 | input.3 → 111.5 | STRING |
| 246 | 88.0 → 3.3 | LATENT |
| 248 | input.0 → 117.0 | IMAGE |
| 249 | 117.0 → 88.0 | IMAGE |
| 250 | 117.0 → 111.2 | IMAGE |
| 251 | 117.0 → 110.2 | IMAGE |
| 706 | 442.0 → 3.6 | FLOAT |
| 707 | 441.0 → 3.5 | INT |
| 708 | 440.0 → 66.0 | MODEL |
| 709 | 89.0 → 440.1 | MODEL |
| 710 | 37.0 → 440.0 | MODEL |
| 711 | 438.0 → 441.0 | INT |
| 712 | 439.0 → 442.0 | FLOAT |
| 713 | 436.0 → 441.1 | INT |
| 714 | 437.0 → 442.1 | FLOAT |
| 715 | 443.0 → 440.2 | BOOLEAN |
| 716 | 443.0 → 441.2 | BOOLEAN |
| 717 | 443.0 → 442.2 | BOOLEAN |
| 718 | input.4 → 3.4 | INT |
| 719 | input.5 → 443.0 | BOOLEAN |
| 720 | input.6 → 37.0 | COMBO |
| 721 | input.7 → 38.0 | COMBO |
| 722 | input.8 → 39.0 | COMBO |

### Subgraph "c7f5c302" Internal Links
| LinkID | From → To | Type |
|--------|-----------|------|
| 141 | 450.0 → 445.0 | MODEL |
| 128 | 456.0 → 453.0 | LATENT |
| 76 | 446.0 → 453.1 | VAE |
| 184 | 448.0 → 454.0 | MODEL |
| 186 | 445.0 → 456.0 | MODEL |
| 168 | 446.0 → 452.1 | VAE |
| 204 | 447.0 → 449.0 | CLIP |
| 206 | 446.0 → 449.1 | VAE |
| 205 | 447.0 → 451.0 | CLIP |
| 207 | 446.0 → 451.1 | VAE |
| 110 | 453.0 → output | IMAGE |
| 235 | input.1 → 451.3 | IMAGE |
| 236 | input.1 → 449.3 | IMAGE |
| 237 | input.2 → 451.4 | IMAGE |
| 238 | input.2 → 449.4 | IMAGE |
| 244 | input.3 → 451.5 | STRING |
| 246 | 452.0 → 456.3 | LATENT |
| 248 | input.0 → 455.0 | IMAGE |
| 249 | 455.0 → 452.0 | IMAGE |
| 250 | 455.0 → 451.2 | IMAGE |
| 251 | 455.0 → 449.2 | IMAGE |
| 706 | 463.0 → 456.6 | FLOAT |
| 707 | 462.0 → 456.5 | INT |
| 708 | 461.0 → 450.0 | MODEL |
| 709 | 454.0 → 461.1 | MODEL |
| 710 | 448.0 → 461.0 | MODEL |
| 711 | 459.0 → 462.0 | INT |
| 712 | 460.0 → 463.0 | FLOAT |
| 713 | 457.0 → 462.1 | INT |
| 714 | 458.0 → 463.1 | FLOAT |
| 715 | 464.0 → 461.2 | BOOLEAN |
| 716 | 464.0 → 462.2 | BOOLEAN |
| 717 | 464.0 → 463.2 | BOOLEAN |
| 718 | input.4 → 456.4 | INT |
| 719 | input.5 → 464.0 | BOOLEAN |
| 720 | input.6 → 448.0 | COMBO |
| 721 | input.7 → 447.0 | COMBO |
| 722 | input.8 → 446.0 | COMBO |
| 726 | 452.0 → 467.1 | LATENT |
| 727 | 451.0 → 467.0 | CONDITIONING |
| 728 | 467.0 → 456.1 | CONDITIONING |
| 729 | 449.0 → 468.0 | CONDITIONING |
| 730 | 452.0 → 468.1 | LATENT |
| 731 | 468.0 → 456.2 | CONDITIONING |

## Data Flow
**Top level:** LoadImage (78) loads "BASE_IMAGE.png" and sends IMAGE to both subgraph node 433 (active, "Image Edit (Qwen 2509)") and subgraph node 466 (bypassed, "Image Edit (Qwen 2509 Raw Latent)"). PrimitiveStringMultiline (435) provides the edit prompt STRING to both subgraphs at slot 3. Subgraph 433 outputs IMAGE to SaveImage (60). Subgraph 466 outputs IMAGE to SaveImage (342).

**Inside each subgraph:** Input image passes through FluxKontextImageScale for proper sizing, then to VAEEncode for latent encoding and to both TextEncodeQwenImageEditPlus nodes (positive prompt node and negative/empty conditioning node) as image1. UNETLoader loads the diffusion model, which optionally passes through LoraLoaderModelOnly (Lightning LoRA), controlled by PrimitiveBoolean "Enable Lightning LoRA" via three ComfySwitchNode instances that select between original settings (20 steps, CFG 4) and lightning settings (4 steps, CFG 1) for model, steps, and CFG. The selected model goes through ModelSamplingAuraFlow (shift=3) then CFGNorm (strength=1). KSampler receives the patched model, positive conditioning, negative conditioning, and encoded latent, then outputs to VAEDecode for final IMAGE.

**Raw Latent subgraph difference:** The "c7f5c302" subgraph additionally uses ReferenceLatent nodes (467, 468) which combine the positive and negative conditioning with the source latent before passing to KSampler.

## Invariants
- Keep both edit branches; subgraph 433 is active (mode 0), subgraph 466 is bypassed (mode 4).
- Model filenames must be preserved exactly: `qwen_image_edit_2509_fp8_e4m3fn.safetensors`, `Qwen-Image-Edit-2509-Lightning-4steps-V1.0-bf16.safetensors`, `qwen_2.5_vl_7b_fp8_scaled.safetensors`, `qwen_image_vae.safetensors`.
- CLIPLoader type must be "qwen_image".
- ModelSamplingAuraFlow shift=3 in both subgraphs.
- CFGNorm strength=1, unconditioned=false in both subgraphs.
- KSampler: sampler="euler", scheduler="simple", denoise=1.
- Lightning mode defaults: steps=4, CFG=1, LoRA strength=1. Original mode: steps=20, CFG=4.
- PrimitiveBoolean "Enable Lightning LoRA" defaults to true in both subgraphs.
