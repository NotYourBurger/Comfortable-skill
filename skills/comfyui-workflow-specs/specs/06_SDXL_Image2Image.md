# 06_SDXL_Image2Image

## Purpose
SDXL image-to-image pipeline that encodes an input image into latent space, applies guided denoising with the Dreamshaper XL Lightning checkpoint, and decodes the result back to an image for comparison.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors`

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 148 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 155 | LoadImage | `["sketch_tattoo.jpg", "image"]` |
| 157 | CLIPTextEncode (Positive) | `["basketball on fire"]` |
| 158 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting, realistic"]` |
| 149 | Reroute | VAE passthrough |
| 141 | Reroute | VAE passthrough |
| 243 | VAEEncode | — |
| 159 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 0.9]` |
| 154 | VAEDecode | — |
| 156 | Image Comparer (rgthree) | Slide mode |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 227 | 149.0 | 141.0 | * |
| 235 | 148.2 | 149.0 | * |
| 241 | 159.0 | 154.0 | LATENT |
| 242 | 141.0 | 154.1 | VAE |
| 243 | 154.0 | 156.0 | IMAGE |
| 246 | 148.1 | 158.0 | CLIP |
| 252 | 148.1 | 157.0 | CLIP |
| 253 | 148.0 | 159.0 | MODEL |
| 395 | 157.0 | 159.1 | CONDITIONING |
| 396 | 158.0 | 159.2 | CONDITIONING |
| 397 | 155.0 | 243.0 | IMAGE |
| 398 | 243.0 | 159.3 | LATENT |
| 399 | 155.0 | 156.1 | IMAGE |
| 400 | 149.0 | 243.1 | VAE |

## Data Flow
CheckpointLoaderSimple (148) loads the SDXL Lightning model, providing MODEL to KSampler (159), CLIP to both CLIPTextEncode nodes (157 positive, 158 negative), and VAE through Reroute (149). LoadImage (155) provides the input image ("sketch_tattoo.jpg") to VAEEncode (243), which also receives VAE from Reroute (149). VAEEncode (243) produces the LATENT input for KSampler (159). CLIPTextEncode (157) provides positive CONDITIONING and CLIPTextEncode (158) provides negative CONDITIONING to KSampler (159). KSampler (159) runs with seed 123456789, 15 steps, CFG 2, euler_ancestral sampler, karras scheduler, and denoise 0.9. The sampled latent goes to VAEDecode (154), which receives VAE through Reroute (141). The decoded image feeds Image Comparer (156) alongside the original input image from LoadImage (155) for side-by-side comparison.

## Invariants
- KSampler denoise is 0.9 (not 1.0) — this is the image-to-image denoise strength, critical for preserving input structure.
- KSampler CFG is 2, suited for the Lightning distilled model.
- KSampler uses 15 steps with euler_ancestral sampler and karras scheduler.
- VAEEncode must receive the same VAE as VAEDecode for consistent encoding/decoding.
- No EmptyLatentImage node — the latent is derived from the input image via VAEEncode.
