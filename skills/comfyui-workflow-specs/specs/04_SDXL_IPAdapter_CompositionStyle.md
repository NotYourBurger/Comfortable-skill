# 04_SDXL_IPAdapter_CompositionStyle

## Purpose
SDXL dual-pipeline workflow using IPAdapterStyleComposition to blend style and composition from two separate source images, with a parallel baseline KSampler for A/B comparison.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors`
- IPAdapter preset: "PLUS (high strength)"

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 4 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 6 | CLIPTextEncode | `["a guitar"]` (positive) |
| 7 | CLIPTextEncode | `["text, label, watermark"]` (negative) |
| 84 | LoadImage | `["pasted/image (10).png", "image"]` (style source) |
| 85 | LoadImage | `["pasted/image (11).png", "image"]` (composition source) |
| 71 | EmptyLatentImage | `[1024, 1024, 1]` |
| 26 | Reroute | *(passes MODEL)* |
| 30 | Reroute | *(passes VAE)* |
| 29 | Reroute | *(passes VAE)* |
| 28 | Reroute | *(passes LATENT)* |
| 33 | IPAdapterUnifiedLoader | `["PLUS (high strength)"]` |
| 77 | IPAdapterStyleComposition | `[1.0, 1.0, false, "average", 0, 1, "K+V"]` |
| 3 | KSampler | `[12345789, "fixed", 7, 1.5, "dpmpp_2m", "karras", 1]` (baseline pipeline) |
| 8 | VAEDecode | `[]` (baseline pipeline) |
| 62 | PreviewImage | `[]` (baseline preview) |
| 86 | KSampler | `[12345789, "fixed", 7, 2, "dpmpp_2m", "karras", 1]` (composition pipeline) |
| 87 | VAEDecode | `[]` (composition pipeline) |
| 88 | PreviewImage | `[]` (composition preview) |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 10 | 6.0 | 3.1 | CONDITIONING |
| 11 | 7.0 | 3.2 | CONDITIONING |
| 12 | 3.0 | 8.0 | LATENT |
| 17 | 4.0 | 26.0 | * |
| 21 | 28.0 | 3.3 | LATENT |
| 22 | 29.0 | 8.1 | VAE |
| 23 | 30.0 | 29.0 | * |
| 24 | 4.2 | 30.0 | * |
| 31 | 26.0 | 33.0 | MODEL |
| 86 | 8.0 | 62.0 | IMAGE |
| 88 | 71.0 | 28.0 | * |
| 89 | 4.1 | 6.0 | CLIP |
| 90 | 4.1 | 7.0 | CLIP |
| 101 | 85.0 | 77.3 | IMAGE |
| 102 | 84.0 | 77.2 | IMAGE |
| 103 | 33.0 | 77.0 | MODEL |
| 104 | 33.1 | 77.1 | IPADAPTER |
| 105 | 86.0 | 87.0 | LATENT |
| 106 | 77.0 | 86.0 | MODEL |
| 107 | 87.0 | 88.0 | IMAGE |
| 108 | 6.0 | 86.1 | CONDITIONING |
| 109 | 7.0 | 86.2 | CONDITIONING |
| 110 | 28.0 | 86.3 | LATENT |
| 111 | 29.0 | 87.1 | VAE |
| 112 | 33.0 | 3.0 | MODEL |

## Data Flow
**Shared infrastructure:** CheckpointLoaderSimple (node 4) loads `dreamshaperXL_lightningDPMSDE.safetensors` and outputs MODEL, CLIP, and VAE. MODEL passes through Reroute (node 26) to IPAdapterUnifiedLoader (node 33, preset "PLUS (high strength)"). CLIP feeds CLIPTextEncode (node 6, positive "a guitar") and CLIPTextEncode (node 7, negative "text, label, watermark"). VAE passes through Reroute (node 30) then Reroute (node 29). EmptyLatentImage (node 71, 1024x1024) passes through Reroute (node 28).

**Baseline pipeline:** IPAdapterUnifiedLoader (node 33) outputs MODEL directly to KSampler (node 3) via link 112. KSampler (node 3) receives positive CONDITIONING from node 6, negative CONDITIONING from node 7, and LATENT from Reroute (node 28). KSampler runs 7 steps with dpmpp_2m/karras at CFG 1.5 and denoise 1. VAEDecode (node 8) decodes using VAE from Reroute (node 29). PreviewImage (node 62) displays the result.

**Composition pipeline:** IPAdapterUnifiedLoader (node 33) outputs MODEL and IPADAPTER to IPAdapterStyleComposition (node 77), which also receives image_style from LoadImage (node 84) and image_composition from LoadImage (node 85). IPAdapterStyleComposition applies weight_style 1.0, weight_composition 1.0, expand_style false, combine_embeds "average", start_at 0, end_at 1, embeds_scaling "K+V". The composed MODEL feeds KSampler (node 86), which receives the same positive/negative CONDITIONING and LATENT as the baseline. KSampler (node 86) runs 7 steps with dpmpp_2m/karras at CFG 2 and denoise 1. VAEDecode (node 87) decodes using VAE from Reroute (node 29). PreviewImage (node 88) displays the result.

## Invariants
- Resolution: 1024x1024 (SDXL-native).
- Baseline KSampler (node 3): 7 steps, CFG 1.5, dpmpp_2m, karras, denoise 1.
- Composition KSampler (node 86): 7 steps, CFG 2, dpmpp_2m, karras, denoise 1.
- IPAdapterStyleComposition: weight_style 1.0, weight_composition 1.0, combine_embeds "average", embeds_scaling "K+V".
- IPAdapter preset: "PLUS (high strength)".
- Two separate LoadImage nodes provide distinct style (node 84) and composition (node 85) reference images.
- The dual-pipeline structure enables A/B comparison between baseline (no composition) and composition-applied outputs.
