# default

## Purpose
Minimal SD1.5 text-to-image template that generates an image from positive/negative text prompts using a single checkpoint, sampler, and VAE decode pipeline.

## Model Stack
- Checkpoint: `v1-5-pruned-emaonly-fp16.safetensors`

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 4 | CheckpointLoaderSimple | `["v1-5-pruned-emaonly-fp16.safetensors"]` |
| 6 | CLIPTextEncode | `["beautiful scenery nature glass bottle landscape, , purple galaxy bottle,"]` |
| 7 | CLIPTextEncode | `["text, watermark"]` |
| 5 | EmptyLatentImage | `[512, 512, 1]` |
| 3 | KSampler | `[156680208700286, "randomize", 20, 8, "euler", "normal", 1]` |
| 8 | VAEDecode | `[]` |
| 9 | SaveImage | `["ComfyUI"]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 1 | 4.0 | 3.0 | MODEL |
| 2 | 5.0 | 3.3 | LATENT |
| 3 | 4.1 | 6.0 | CLIP |
| 4 | 6.0 | 3.1 | CONDITIONING |
| 5 | 4.1 | 7.0 | CLIP |
| 6 | 7.0 | 3.2 | CONDITIONING |
| 7 | 3.0 | 8.0 | LATENT |
| 8 | 4.2 | 8.1 | VAE |
| 9 | 8.0 | 9.0 | IMAGE |

## Data Flow
CheckpointLoaderSimple (node 4) loads `v1-5-pruned-emaonly-fp16.safetensors` and outputs MODEL, CLIP, and VAE. CLIP feeds both CLIPTextEncode (node 6, positive prompt) and CLIPTextEncode (node 7, negative prompt). EmptyLatentImage (node 5) creates a 512x512 blank latent. KSampler (node 3) receives MODEL from node 4, positive CONDITIONING from node 6, negative CONDITIONING from node 7, and LATENT from node 5, then samples with euler/normal scheduler for 20 steps at CFG 8 and denoise 1. VAEDecode (node 8) decodes the sampled LATENT using VAE from node 4. SaveImage (node 9) saves the decoded IMAGE with prefix "ComfyUI".

## Invariants
- Resolution: 512x512 (SD1.5 native resolution).
- KSampler: 20 steps, CFG 8, euler sampler, normal scheduler, denoise 1.
- Checkpoint must be an SD1.5 compatible model.

