# 04_SDXL_IPAdapter

## Purpose
SDXL text-to-image workflow with IPAdapter style transfer applied via IPAdapterUnifiedLoader and IPAdapterAdvanced, using a reference image to influence generation style.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors`
- IPAdapter preset: "PLUS (high strength)"

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 4 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 6 | CLIPTextEncode | `["a guitar"]` (positive) |
| 7 | CLIPTextEncode | `["text, label, watermark"]` (negative) |
| 84 | LoadImage | `["pasted/image (10).png", "image"]` |
| 71 | EmptyLatentImage | `[1024, 1024, 1]` |
| 26 | Reroute | *(passes MODEL)* |
| 30 | Reroute | *(passes VAE)* |
| 29 | Reroute | *(passes VAE)* |
| 28 | Reroute | *(passes LATENT)* |
| 33 | IPAdapterUnifiedLoader | `["PLUS (high strength)"]` |
| 74 | IPAdapterAdvanced | `[0.5, "style transfer", "concat", 0, 1, "K+V"]` |
| 77 | IPAdapterStyleComposition | `[1, 1, false, "average", 0, 1, "V only"]` (disconnected) |
| 3 | KSampler | `[12345789, "fixed", 7, 1.5, "dpmpp_2m", "karras", 1]` |
| 8 | VAEDecode | `[]` |
| 62 | PreviewImage | `[]` |

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
| 91 | 33.0 | 74.0 | MODEL |
| 92 | 33.1 | 74.1 | IPADAPTER |
| 96 | 74.0 | 3.0 | MODEL |
| 100 | 84.0 | 74.2 | IMAGE |

## Data Flow
CheckpointLoaderSimple (node 4) loads `dreamshaperXL_lightningDPMSDE.safetensors` and outputs MODEL, CLIP, and VAE. MODEL passes through Reroute (node 26) to IPAdapterUnifiedLoader (node 33, preset "PLUS (high strength)"). IPAdapterUnifiedLoader outputs MODEL and IPADAPTER to IPAdapterAdvanced (node 74), which also receives the reference IMAGE from LoadImage (node 84). IPAdapterAdvanced applies style transfer with weight 0.5, weight_type "style transfer", combine_embeds "concat", start_at 0, end_at 1, embeds_scaling "K+V", and outputs the adapted MODEL to KSampler (node 3). CLIP from node 4 feeds CLIPTextEncode (node 6, positive "a guitar") and CLIPTextEncode (node 7, negative "text, label, watermark"). VAE from node 4 passes through Reroute (node 30) then Reroute (node 29) to VAEDecode (node 8). EmptyLatentImage (node 71, 1024x1024) passes through Reroute (node 28) to KSampler. KSampler runs 7 steps with dpmpp_2m/karras at CFG 1.5 and denoise 1. VAEDecode (node 8) decodes the output LATENT and sends IMAGE to PreviewImage (node 62). IPAdapterStyleComposition (node 77) is present but fully disconnected.

## Invariants
- Resolution: 1024x1024 (SDXL-native).
- KSampler: 7 steps, CFG 1.5, dpmpp_2m sampler, karras scheduler, denoise 1.
- IPAdapterAdvanced weight: 0.5, weight_type: "style transfer", combine_embeds: "concat", embeds_scaling: "K+V".
- IPAdapter preset: "PLUS (high strength)".
- IPAdapterStyleComposition (node 77) is disconnected and unused in the active pipeline.
- SDXL optimal resolutions: 1024x1024 (square), 896x1152 (3:4 portrait), 1152x896 (4:3 landscape), and others listed in note nodes.
