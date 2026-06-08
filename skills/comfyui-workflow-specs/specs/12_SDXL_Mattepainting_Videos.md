# 12_SDXL_Mattepainting_Videos

## Purpose
SDXL matte-painting workflow that generates a still image using depth ControlNet from a reference photo, then fans that still out to Kling and Moonvalley image-to-video services for animated flyover shots.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors`
- ControlNet: `SDXL\control-lora-depth-rank256.safetensors`
- Depth preprocessor: `depth_anything_v2_vitl.pth`
- Video gen: `kling-v2-master` (Kling), Moonvalley img2video

## Node Table

### Mattepainting Generation
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
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
| 260 | VHS_LoadImagePath | `google_earth_shot2.PNG` |
| 149 | Reroute | VAE passthrough |
| 141 | Reroute | VAE passthrough |

### Video Generation (bypassed, mode 4)
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 270 | LoadImage | source still for video gen |
| 272 | KlingImage2VideoNode | `["a drone camera slowly flies over...", ..., "kling-v2-master", 0.8, "std", "16:9", "5"]` (mode 4) |
| 273 | MoonvalleyImg2VideoNode | `["a drone camera slowly flies over...", ..., "16:9 (1920 x 1080)", 7, ...]` (mode 4) |
| 271 | SaveVideo | `["video/ComfyUI", "auto", "auto"]` (mode 4) |

### Preview / QA
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 254 | PreviewImage | Final output preview |
| 259 | Image Comparer (rgthree) | Slide mode — compares output vs input |
| 262 | Fast Groups Bypasser (rgthree) | group bypass control |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
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
| 429 | 251.0 | 247.0 | IMAGE |
| 432 | 154.0 | 259.0 | IMAGE |
| 434 | 260.0 | 251.0 | IMAGE |
| 435 | 260.0 | 256.0 | IMAGE |
| 450 | 256.0 | 249.3 | IMAGE |
| 452 | 260.0 | 259.1 | IMAGE |
| 454 | 272.0 | 271.0 | VIDEO |
| 455 | 270.0 | 272.0 | IMAGE |
| 456 | 154.0 | 254.0 | IMAGE |
| 457 | 270.0 | 273.0 | IMAGE |

## Data Flow
VHS_LoadImagePath (260) loads the Google Earth reference image. That image feeds into Canny (251) for edge detection and DepthAnythingV2Preprocessor (256) for depth estimation. The Canny edges go to VAEEncode (247) as the latent input. The depth map goes to ControlNetApplyAdvanced (249) which applies depth ControlNet (250) at strength 0.8 and end_percent 0.7. CheckpointLoaderSimple (148) provides MODEL, CLIP, and VAE. CLIPTextEncode (157) encodes the positive prompt, CLIPTextEncode (158) encodes the negative. KSampler (159) runs 15 steps with euler_ancestral/karras, CFG 2, denoise 0.98. VAEDecode (154) decodes the result to PreviewImage (254) and Image Comparer (259). For video generation (currently bypassed), LoadImage (270) feeds KlingImage2VideoNode (272) and MoonvalleyImg2VideoNode (273). SaveVideo (271) stores the Kling output.

## Invariants
- KSampler: 15 steps, euler_ancestral, karras, CFG 2, denoise 0.98.
- ControlNet depth: strength 0.8, start_percent 0, end_percent 0.7.
- Canny thresholds: low=0.02, high=0.06.
- Depth preprocessor resolution: 1024.
- Video generation nodes (270, 271, 272, 273) are bypassed (mode 4). Kling uses kling-v2-master model, std mode, 16:9, 5s duration. Moonvalley uses 16:9 (1920x1080), prompt_adherence 7.
