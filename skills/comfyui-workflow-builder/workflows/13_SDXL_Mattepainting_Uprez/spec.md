# 13_SDXL_Mattepainting_Uprez

## Purpose
Matte-painting plus uprez pipeline containing a bypassed SDXL depth-ControlNet generation stage and multiple upscale model comparison branches for evaluating different upscalers (RealESRGAN_x2, RealESRGAN_x4, 4x-UltraSharp, 4x-AnimeSharp, ESRGAN_4x) and UltimateSDUpscale tiled re-rendering.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors` (bypassed)
- ControlNet: `SDXL\control-lora-depth-rank256.safetensors` (bypassed)
- Depth preprocessor: `depth_anything_v2_vitl.pth` (bypassed)
- Upscale models: `RealESRGAN_x2.pth`, `RealESRGAN_x4.pth`, `4x-UltraSharp.pth`, `4x-AnimeSharp.pth`, `ESRGAN_4x.pth`

## Node Table

### SDXL Generation (all bypassed, mode 4)
| ID | class_type | Key Widget Values |
|---|---|---|
| 148 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 157 | CLIPTextEncode | Positive prompt (same as workflow 12) |
| 158 | CLIPTextEncode | Negative prompt (same as workflow 12) |
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

### UltimateSDUpscale (bypassed, mode 4)
| ID | class_type | Key Widget Values |
|---|---|---|
| 263 | UltimateSDUpscale | `[2, ..., 20, 1, "euler", "normal", 0.3, "Linear", 1024, 1024, 8, 32, "None", ...]` |
| 264 | UpscaleModelLoader | `["4x-UltraSharp.pth"]` |
| 254 | PreviewImage | UltimateSD result preview |
| 259 | Image Comparer (rgthree) | Slide compare (bypassed) |

### Standalone UltimateSDUpscale (bypassed)
| ID | class_type | Key Widget Values |
|---|---|---|
| 276 | UltimateSDUpscale | `[2, ..., 20, 1, "euler", "normal", 0.3, "Linear", 1024, 1024, 8, 32, "None", ...]` |
| 277 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 278 | CLIPTextEncode | Positive prompt |
| 279 | CLIPTextEncode | Negative prompt |
| 275 | UpscaleModelLoader | `["4x-UltraSharp.pth"]` |
| 280 | PreviewImage | result preview |

### Active Upscale Comparison (mode 0)
| ID | class_type | Key Widget Values |
|---|---|---|
| 281 | LoadImage | `["sendtoworkflow-...ComfyUI_temp_bnsxk_00001_.png"]` - input image |
| 289 | UpscaleModelLoader | `["RealESRGAN_x2.pth"]` |
| 290 | ImageUpscaleWithModel | RealESRGAN x2 upscale |
| 291 | Get resolution [Crystools] | resolution check |
| 294 | UpscaleModelLoader | `["RealESRGAN_x4.pth"]` |
| 293 | ImageUpscaleWithModel | RealESRGAN x4 upscale |
| 292 | Get resolution [Crystools] | resolution check |
| 295 | ImageScaleBy | `["nearest-exact", 0.5]` - scale down x4 result |
| 296 | Image Comparer (rgthree) | Compares RealESRGAN_x2 vs x4-downscaled |

### Bypassed Upscale Comparisons (mode 4)
| ID | class_type | Key Widget Values |
|---|---|---|
| 283 | UpscaleModelLoader | `["4x-UltraSharp.pth"]` |
| 282 | ImageUpscaleWithModel | 4x-UltraSharp upscale |
| 284 | Get resolution [Crystools] | resolution check |
| 285 | ImageScaleBy | `["nearest-exact", 0.5]` |
| 297 | UpscaleModelLoader | `["ESRGAN_4x.pth"]` |
| 298 | ImageUpscaleWithModel | ESRGAN 4x upscale |
| 300 | ImageScaleBy | `["nearest-exact", 0.5]` |
| 299 | Image Comparer (rgthree) | Compares ESRGAN vs RealESRGAN |
| 304 | UpscaleModelLoader | `["4x-AnimeSharp.pth"]` |
| 301 | ImageUpscaleWithModel | 4x-AnimeSharp upscale |
| 302 | Get resolution [Crystools] | resolution check |
| 303 | ImageScaleBy | `["nearest-exact", 0.5]` |
| 306 | Image Comparer (rgthree) | Compares AnimeSharp vs UltraSharp |

### Utility
| ID | class_type | Key Widget Values |
|---|---|---|
| 262 | Fast Groups Bypasser (rgthree) | group bypass control |

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
| 429 | 251.0 | 247.0 | IMAGE |
| 432 | 154.0 | 259.0 | IMAGE |
| 434 | 260.0 | 251.0 | IMAGE |
| 435 | 260.0 | 256.0 | IMAGE |
| 439 | 264.0 | 263.5 | UPSCALE_MODEL |
| 440 | 154.0 | 263.0 | IMAGE |
| 441 | 263.0 | 254.0 | IMAGE |
| 446 | 148.0 | 263.1 | MODEL |
| 448 | 249.0 | 263.2 | CONDITIONING |
| 449 | 249.1 | 263.3 | CONDITIONING |
| 450 | 256.0 | 249.3 | IMAGE |
| 451 | 141.0 | 263.4 | VAE |
| 452 | 260.0 | 259.1 | IMAGE |
| 456 | 275.0 | 276.5 | UPSCALE_MODEL |
| 457 | 278.0 | 276.2 | CONDITIONING |
| 458 | 279.0 | 276.3 | CONDITIONING |
| 460 | 277.0 | 276.1 | MODEL |
| 461 | 277.1 | 278.0 | CLIP |
| 462 | 277.1 | 279.0 | CLIP |
| 463 | 277.2 | 276.4 | VAE |
| 464 | 276.0 | 280.0 | IMAGE |
| 465 | 281.0 | 282.1 | IMAGE |
| 466 | 283.0 | 282.0 | UPSCALE_MODEL |
| 467 | 282.0 | 284.0 | IMAGE |
| 468 | 282.0 | 285.0 | IMAGE |
| 472 | 289.0 | 290.0 | UPSCALE_MODEL |
| 473 | 281.0 | 290.1 | IMAGE |
| 474 | 290.0 | 291.0 | IMAGE |
| 475 | 293.0 | 292.0 | IMAGE |
| 476 | 294.0 | 293.0 | UPSCALE_MODEL |
| 477 | 293.0 | 295.0 | IMAGE |
| 479 | 295.0 | 296.1 | IMAGE |
| 480 | 290.0 | 296.0 | IMAGE |
| 481 | 297.0 | 298.0 | UPSCALE_MODEL |
| 482 | 281.0 | 298.1 | IMAGE |
| 483 | 295.0 | 299.1 | IMAGE |
| 485 | 298.0 | 300.0 | IMAGE |
| 486 | 300.0 | 299.0 | IMAGE |
| 487 | 304.0 | 301.0 | UPSCALE_MODEL |
| 488 | 301.0 | 302.0 | IMAGE |
| 489 | 301.0 | 303.0 | IMAGE |
| 491 | 303.0 | 306.0 | IMAGE |
| 492 | 285.0 | 306.1 | IMAGE |
| 493 | 281.0 | 276.0 | IMAGE |

## Data Flow
LoadImage (281) loads the mattepainting image. In the active branch, this image feeds into ImageUpscaleWithModel (290) using RealESRGAN_x2 (289), and separately into ImageUpscaleWithModel (293) using RealESRGAN_x4 (294). The x4 output is scaled down to 50% via ImageScaleBy (295) for comparison. Image Comparer (296) compares the x2 result against the downscaled x4 result. Get resolution [Crystools] nodes (291, 292) display resolution info. The bypassed branches compare 4x-UltraSharp (283-282-285), ESRGAN_4x (297-298-300), and 4x-AnimeSharp (304-301-303) using additional Image Comparer nodes (299, 306). The entire SDXL generation stage (148, 157, 158, 159, 154, 249, 250, 251, 256) is bypassed. Two UltimateSDUpscale nodes (263, 276) are also bypassed - these perform tiled re-rendering at 2x with 20 steps, denoise 0.3, 1024x1024 tiles.

## Invariants
- All SDXL generation and UltimateSDUpscale nodes are bypassed (mode 4). Only the direct upscale model comparison branches are active.
- Active comparison: RealESRGAN_x2 vs RealESRGAN_x4 (downscaled 50%).
- UltimateSDUpscale (when enabled): upscale_by 2, 20 steps, CFG 1, euler/normal, denoise 0.3, Linear mode, 1024x1024 tiles, mask_blur 8, tile_padding 32.
- All ImageScaleBy nodes use nearest-exact at 0.5 scale factor for resolution-matched comparison.

