# 04_FLUX_Schnell_LORA

## Purpose
FLUX Schnell text-to-image workflow with a LoRA applied (pixel art style) and FluxGuidance, including an Image Comparer node for visual A/B diffing against a reference image.

## Model Stack
- Checkpoint: `FLUX\Schnell\flux1-schnell-fp8.safetensors`
- LoRA: `FLUX\Schnell\pixelart_schnell_v1.safetensors` (strength_model=2.0, strength_clip=1.0)

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 30 | CheckpointLoaderSimple | `["FLUX\\Schnell\\flux1-schnell-fp8.safetensors"]` |
| 52 | LoraLoader | `["FLUX\\Schnell\\pixelart_schnell_v1.safetensors", 2.0, 1.0]` |
| 6 | CLIPTextEncode | `["pixel art, hairless cat in a sweater, santa hat, (christmas tree:1.5), (christmas lights:3.0), fireplace"]` (titled "CLIP Text Encode (Positive Prompt)") |
| 33 | CLIPTextEncode | `[""]` (titled "CLIP Text Encode (Negative Prompt)") |
| 35 | FluxGuidance | `[4]` |
| 27 | EmptySD3LatentImage | `[1024, 1024, 1]` |
| 31 | KSampler | `[123456789, "fixed", 4, 1, "dpmpp_sde", "karras", 1]` |
| 8 | VAEDecode | `[]` |
| 50 | PreviewImage | `[]` |
| 55 | LoadImage | `["pasted/image (7).png", "image"]` |
| 54 | Image Comparer (rgthree) | *(comparer_mode: "Click")* |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 46 | 30.2 | 8.1 | VAE |
| 51 | 27.0 | 31.3 | LATENT |
| 52 | 31.0 | 8.0 | LATENT |
| 54 | 30.1 | 33.0 | CLIP |
| 55 | 33.0 | 31.2 | CONDITIONING |
| 56 | 6.0 | 35.0 | CONDITIONING |
| 57 | 35.0 | 31.1 | CONDITIONING |
| 70 | 8.0 | 50.0 | IMAGE |
| 73 | 30.1 | 52.1 | CLIP |
| 74 | 52.1 | 6.0 | CLIP |
| 75 | 30.0 | 52.0 | MODEL |
| 76 | 52.0 | 31.0 | MODEL |
| 78 | 8.0 | 54.0 | IMAGE |
| 79 | 55.0 | 54.1 | IMAGE |

## Data Flow
CheckpointLoaderSimple (node 30) loads `flux1-schnell-fp8.safetensors` and outputs MODEL, CLIP, and VAE. MODEL and CLIP feed into LoraLoader (node 52), which applies `pixelart_schnell_v1.safetensors` at model strength 2.0 and clip strength 1.0. LoRA-modified CLIP feeds CLIPTextEncode (node 6, positive prompt). Original CLIP from node 30 feeds CLIPTextEncode (node 33, negative prompt, empty). Positive CONDITIONING from node 6 passes through FluxGuidance (node 35, guidance=4) into KSampler (node 31) as positive. Negative CONDITIONING from node 33 enters KSampler as negative. EmptySD3LatentImage (node 27) provides a 1024x1024 latent to KSampler. LoRA-modified MODEL from node 52 feeds KSampler. KSampler runs 4 steps with dpmpp_sde/karras at CFG 1 and denoise 1. VAEDecode (node 8) decodes the output LATENT using VAE from node 30. The decoded IMAGE goes to PreviewImage (node 50) and to Image Comparer (rgthree) (node 54) as image_a. LoadImage (node 55) provides a reference image to Image Comparer as image_b.

## Invariants
- Resolution: 1024x1024 (FLUX-native).
- KSampler: 4 steps, CFG 1, dpmpp_sde sampler, karras scheduler, denoise 1.
- CFG must be 1 because FLUX Schnell does not use negative prompts.
- FluxGuidance guidance value: 4.
- LoRA strength_model: 2.0, strength_clip: 1.0 - the high model strength is intentional for pixel art style.
- LoRA application order: CheckpointLoaderSimple - LoraLoader - KSampler (MODEL and CLIP must pass through LoRA before use).

