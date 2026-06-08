# 06_SDXL_Image2Image_with_ControlNet

## Purpose
SDXL image-to-image pipeline that adds a Canny ControlNet to guide structural generation, combining latent-space image encoding with edge-detected control guidance for shape-preserving transforms.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors`
- ControlNet: `SDXL\control-lora-canny-rank256.safetensors`

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 148 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 246 | LoadImage | `["dino_tattoo.jpg", "image"]` |
| 157 | CLIPTextEncode (Positive) | `["dinosaur, rainbow"]` |
| 158 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting, realistic"]` |
| 248 | ImageScale | `["nearest-exact", 1024, 1024, "disabled"]` |
| 251 | Canny | `[0.1, 0.8]` |
| 250 | ControlNetLoader | `["SDXL\\control-lora-canny-rank256.safetensors"]` |
| 249 | ControlNetApplyAdvanced | `[0.25, 0, 0.5]` |
| 149 | Reroute | VAE passthrough |
| 141 | Reroute | VAE passthrough |
| 247 | VAEEncode | - |
| 159 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 0.8]` |
| 154 | VAEDecode | - |
| 156 | Image Comparer (rgthree) | Slide mode |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 227 | 149.0 | 141.0 | * |
| 235 | 148.2 | 149.0 | * |
| 241 | 159.0 | 154.0 | LATENT |
| 242 | 141.0 | 154.1 | VAE |
| 243 | 154.0 | 156.0 | IMAGE |
| 246 | 148.1 | 158.0 | CLIP |
| 252 | 148.1 | 157.0 | CLIP |
| 253 | 148.0 | 159.0 | MODEL |
| 404 | 247.0 | 159.3 | LATENT |
| 405 | 149.0 | 247.1 | VAE |
| 407 | 246.0 | 248.0 | IMAGE |
| 408 | 248.0 | 247.0 | IMAGE |
| 409 | 248.0 | 156.1 | IMAGE |
| 410 | 250.0 | 249.2 | CONTROL_NET |
| 411 | 157.0 | 249.0 | CONDITIONING |
| 412 | 158.0 | 249.1 | CONDITIONING |
| 414 | 149.0 | 249.4 | VAE |
| 415 | 249.0 | 159.1 | CONDITIONING |
| 416 | 249.1 | 159.2 | CONDITIONING |
| 418 | 251.0 | 249.3 | IMAGE |
| 419 | 248.0 | 251.0 | IMAGE |

## Data Flow
CheckpointLoaderSimple (148) loads the SDXL Lightning model, providing MODEL to KSampler (159), CLIP to CLIPTextEncode nodes (157 positive, 158 negative), and VAE through Reroute (149). LoadImage (246) loads "dino_tattoo.jpg" and passes it to ImageScale (248) which resizes to 1024x1024 using nearest-exact. The scaled image feeds three paths: (1) VAEEncode (247) for latent encoding using VAE from Reroute (149), producing the latent input for KSampler (159); (2) Canny (251) for edge detection with low_threshold 0.1 and high_threshold 0.8; (3) Image Comparer (156) for side-by-side comparison. The Canny output feeds ControlNetApplyAdvanced (249), which also receives the ControlNet model from ControlNetLoader (250), positive/negative conditioning from CLIPTextEncode (157/158), and VAE from Reroute (149). ControlNetApplyAdvanced (249) applies at strength 0.25, start_percent 0, end_percent 0.5, outputting modified positive/negative conditioning to KSampler (159). KSampler (159) runs with seed 123456789, 15 steps, CFG 2, euler_ancestral, karras, denoise 0.8. The sampled latent goes to VAEDecode (154) via VAE from Reroute (141), and the decoded image feeds Image Comparer (156).

## Invariants
- KSampler denoise is 0.8 - lower than pure img2img to allow the ControlNet more influence.
- ControlNet strength is 0.25 with end_percent 0.5 - intentionally light guidance to avoid overpowering the img2img process.
- ImageScale resizes to 1024x1024 with crop disabled - this is the working resolution for the pipeline.
- Canny thresholds are low_threshold 0.1 and high_threshold 0.8.
- KSampler uses CFG 2, 15 steps, euler_ancestral sampler, karras scheduler - tuned for SDXL Lightning.
- VAE is shared across VAEEncode, VAEDecode, and ControlNetApplyAdvanced via the same Reroute chain.

