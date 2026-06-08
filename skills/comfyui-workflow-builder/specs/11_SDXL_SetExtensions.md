# 11_SDXL_SetExtensions

## Purpose
SDXL img2img pipeline that generates set extension images from a reference photo using depth ControlNet guidance, Canny edge detection, and depth remapping for scene-consistent outputs.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors`
- ControlNet: `SDXL\control-lora-depth-rank256.safetensors`
- Depth preprocessor: `depth_anything_v2_vitl.pth`

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 148 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 157 | CLIPTextEncode | `["(destroyed buildings, rubble, downtown, main street, destroyed city skyline, destruction, war, realistic, 4k, 8k, night, outside),(alien mothership), cinematic"]` (Positive) |
| 158 | CLIPTextEncode | `["low quality, drawing, illustration, sketch, painting, city lights, fire"]` (Negative) |
| 159 | KSampler | `[697135137283251, "fixed", 15, 2, "euler_ancestral", "karras", 0.98]` |
| 154 | VAEDecode | `[]` |
| 247 | VAEEncode | `[]` |
| 249 | ControlNetApplyAdvanced | `[0.8, 0, 0.7]` |
| 250 | ControlNetLoader | `["SDXL\\control-lora-depth-rank256.safetensors"]` |
| 251 | Canny | `[0.02, 0.06]` |
| 256 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 1024]` |
| 258 | VHS_LoadImagePath | set_extension_light_270_wide.png (unused second loader) |
| 259 | Image Comparer (rgthree) | Slide mode |
| 260 | VHS_LoadImagePath | `set_extension_light_270_wide.png` (main input) |
| 261 | RemapDepth | `[0.03, 1.0, true]` (mode 4 / bypassed) |
| 253 | PreviewImage | Canny preview |
| 254 | PreviewImage | Final output preview |
| 257 | PreviewImage | Depth remap preview |
| 262 | Fast Groups Bypasser (rgthree) | group bypass control |
| 149 | Reroute | VAE passthrough |
| 141 | Reroute | VAE passthrough |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 227 | 149.0 | 141.0 | * |
| 235 | 148.2 | 149.0 | * |
| 241 | 159.0 | 154.0 | LATENT |
| 242 | 141.0 | 154.1 | VAE |
| 246 | 148.1 | 158.0 | CLIP |
| 252 | 148.1 | 157.0 | CLIP |
| 253 | 148.0 | 159.0 | MODEL |
| 404 | 247.0 | 159.3 | LATENT |
| 405 | 149.0 | 247.1 | VAE |
| 410 | 250.0 | 249.2 | CONTROL_NET |
| 411 | 157.0 | 249.0 | CONDITIONING |
| 412 | 158.0 | 249.1 | CONDITIONING |
| 414 | 149.0 | 249.4 | VAE |
| 415 | 249.0 | 159.1 | CONDITIONING |
| 416 | 249.1 | 159.2 | CONDITIONING |
| 421 | 251.0 | 253.0 | IMAGE |
| 422 | 154.0 | 254.0 | IMAGE |
| 429 | 251.0 | 247.0 | IMAGE |
| 432 | 154.0 | 259.0 | IMAGE |
| 433 | 256.0 | 259.1 | IMAGE |
| 434 | 260.0 | 251.0 | IMAGE |
| 435 | 260.0 | 256.0 | IMAGE |
| 436 | 256.0 | 261.0 | IMAGE |
| 437 | 261.0 | 249.3 | IMAGE |
| 438 | 261.0 | 257.0 | IMAGE |

## Data Flow
VHS_LoadImagePath (260) loads the set extension reference image. That image feeds into Canny (251) for edge detection and DepthAnythingV2Preprocessor (256) for depth estimation. The Canny output goes to VAEEncode (247) which encodes to latent space, and also to PreviewImage (253) for inspection. The depth output goes to RemapDepth (261, currently bypassed) and then to ControlNetApplyAdvanced (249). CheckpointLoaderSimple (148) loads the SDXL DreamShaper Lightning model, providing MODEL to KSampler (159) and CLIP to both CLIPTextEncode nodes (157 positive, 158 negative). The positive and negative conditioning flow through ControlNetApplyAdvanced (249) which applies depth ControlNet (250) guidance with strength 0.8 and end_percent 0.7. KSampler (159) runs 15 steps with euler_ancestral/karras at CFG 2 and denoise 0.98. VAEDecode (154) decodes the result. The output goes to PreviewImage (254) and Image Comparer (259) which compares with the depth map.

## Invariants
- KSampler uses 15 steps, euler_ancestral sampler, karras scheduler, CFG 2, denoise 0.98.
- ControlNet depth strength is 0.8, start_percent 0, end_percent 0.7.
- Canny thresholds are low=0.02, high=0.06.
- RemapDepth (261) is bypassed (mode 4) but configured with min=0.03, max=1.0, clamp=true.
- Depth preprocessor resolution is 1024.

