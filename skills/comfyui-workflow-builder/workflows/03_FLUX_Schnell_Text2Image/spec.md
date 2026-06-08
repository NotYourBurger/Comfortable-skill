# 03_FLUX_Schnell_Text2Image

## Purpose
FLUX Schnell distilled text-to-image workflow with FluxGuidance conditioning and CLIPSetLastLayer for fast 4-step generation, outputting a preview image.

## Model Stack
- Checkpoint: `FLUX\Schnell\flux1-schnell-fp8.safetensors`

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 30 | CheckpointLoaderSimple | `["FLUX\\Schnell\\flux1-schnell-fp8.safetensors"]` |
| 41 | CLIPSetLastLayer | `[-1]` |
| 6 | CLIPTextEncode | `["hairless cat in a sweater, santa hat, (christmas tree:1.5), (christmas lights:3.0), fireplace"]` (titled "CLIP Text Encode (Positive Prompt)") |
| 33 | CLIPTextEncode | `[""]` (titled "CLIP Text Encode (Negative Prompt)", collapsed) |
| 38 | FluxGuidance | `[4]` |
| 27 | EmptySD3LatentImage | `[1024, 1024, 1]` |
| 39 | KSampler | `[123456789, "fixed", 4, 1, "dpmpp_sde", "karras", 1]` |
| 8 | VAEDecode | `[]` |
| 40 | PreviewImage | `[]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 46 | 30.2 | 8.1 | VAE |
| 54 | 30.1 | 33.0 | CLIP |
| 59 | 6.0 | 38.0 | CONDITIONING |
| 61 | 38.0 | 39.1 | CONDITIONING |
| 62 | 33.0 | 39.2 | CONDITIONING |
| 63 | 30.0 | 39.0 | MODEL |
| 64 | 27.0 | 39.3 | LATENT |
| 66 | 8.0 | 40.0 | IMAGE |
| 67 | 39.0 | 8.0 | LATENT |
| 68 | 30.1 | 41.0 | CLIP |
| 69 | 41.0 | 6.0 | CLIP |

## Data Flow
CheckpointLoaderSimple (node 30) loads `flux1-schnell-fp8.safetensors` and outputs MODEL, CLIP, and VAE. CLIP feeds CLIPSetLastLayer (node 41, stop_at_clip_layer=-1), which then feeds CLIPTextEncode (node 6, positive prompt). CLIP also feeds CLIPTextEncode (node 33, negative prompt, empty string). The positive CONDITIONING from node 6 passes through FluxGuidance (node 38, guidance=4) before entering KSampler (node 39) as positive conditioning. The negative CONDITIONING from node 33 enters KSampler as negative conditioning. EmptySD3LatentImage (node 27) provides a 1024x1024 blank latent to KSampler. MODEL from node 30 feeds KSampler directly. KSampler runs 4 steps with dpmpp_sde/karras at CFG 1 and denoise 1, outputting LATENT to VAEDecode (node 8). VAEDecode uses VAE from node 30 and outputs IMAGE to PreviewImage (node 40).

## Invariants
- Resolution: 1024x1024 (FLUX-native).
- KSampler: 4 steps, CFG 1, dpmpp_sde sampler, karras scheduler, denoise 1. Schnell is a distilled model optimized for 4-step generation.
- CFG must be 1 because FLUX Schnell does not use negative prompts; setting CFG to 1 causes the negative prompt to be ignored.
- FluxGuidance guidance value: 4.
- CLIPSetLastLayer stop_at_clip_layer: -1.

