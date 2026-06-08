# 09_Inpainting_Cleanplates

## Purpose
Flux Fill-dev inpainting pipeline for cleanplates. It splits the Flux model into separate UNET/CLIP/VAE components, injects a mask and init image via InpaintModelConditioning, applies DifferentialDiffusion for coherent fill regions, and uses FluxGuidance for strong prompt adherence.

## Model Stack
- UNET: `FLUX.1-Fill-dev/flux1-fill-dev.safetensors` (default weight type)
- CLIP: `clip_l.safetensors` + `t5xxl_fp16.safetensors` (flux type, default)
- VAE: `flux_vae.safetensors`

## Node Table

### Video Input
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 160 | VHS_LoadVideo | `video: "shot1_3.mp4", force_rate: 16, frame_load_cap: 81, format: "AnimateDiff"` |
| 213 | VHS_VideoInfo | extracts source dimensions |
| 187 | ImageResizeKJ | `[512, 512, "lanczos", false, 2, 0]` — resizes using source dimensions |
| 144 | VHS_SelectImages | `indexes: "0"` — selects first frame |

### Model Loading
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 232 | UNETLoader | `["FLUX.1-Fill-dev/flux1-fill-dev.safetensors", "default"]` |
| 233 | DualCLIPLoader | `["clip_l.safetensors", "t5xxl_fp16.safetensors", "flux", "default"]` |
| 234 | VAELoader | `["flux_vae.safetensors"]` |
| 240 | DifferentialDiffusion | wraps UNET model for coherent inpainting |

### Prompt / Conditioning
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 205 | StringConstantMultiline | `["empty city street, concrete road barricade, a car", true]` |
| 236 | CLIPTextEncode | `["A concrete wall"]` (Positive — receives text from bus) |
| 237 | CLIPTextEncode | `[""]` (Negative — empty) |
| 239 | FluxGuidance | `[30]` |
| 244 | InpaintModelConditioning | `[false]` — combines positive, negative, vae, image, mask |

### Mask / Init Image
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 248 | LoadImage | `["clipspace/clipspace-mask-1722309.6000000238.png [input]", "image"]` |

### Sampling / Decode
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 241 | KSampler | `[27051285186574, "fixed", 20, 1, "euler", "normal", 1]` |
| 242 | VAEDecode | `[]` |

### Preview / QA
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 259 | PreviewImage | first frame preview |
| 260 | Image Comparer (rgthree) | Slide compare — inpainted vs init_image |
| 161 | Fast Groups Bypasser (rgthree) | group bypass control |

### Set/Get Bus Nodes
| ID | class_type | Title |
|----|-----------|-------|
| 157 | SetNode | Set_init_video |
| 159 | SetNode | Set_num_frames |
| 194 | SetNode | Set_height |
| 195 | SetNode | Set_width |
| 199 | SetNode | Set_first_frame |
| 206 | SetNode | Set_pos_prompt |
| 245 | SetNode | Set_flux_vae |
| 249 | SetNode | Set_init_image |
| 250 | SetNode | Set_init_image_mask |
| 253 | SetNode | Set_diffusion_model |
| 257 | SetNode | Set_inpainted_frame |
| 143 | GetNode | Get_init_video |
| 215 | SetNode | SetNode (unused) |
| 216 | GetNode | GetNode (unused) |
| 238 | GetNode | Get_pos_prompt |
| 246 | GetNode | Get_flux_vae |
| 247 | GetNode | Get_flux_vae |
| 251 | GetNode | Get_init_image |
| 252 | GetNode | Get_init_image_mask |
| 254 | GetNode | Get_diffusion_model |
| 261 | GetNode | Get_init_image |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 295 | 143.0 | 144.0 | IMAGE |
| 304 | 160.1 | 159.0 | * |
| 377 | 160.0 | 187.0 | IMAGE |
| 380 | 187.0 | 157.0 | IMAGE |
| 417 | 144.0 | 199.0 | * |
| 427 | 205.0 | 206.0 | * |
| 436 | 160.3 | 213.0 | VHS_VIDEOINFO |
| 437 | 213.3 | 195.0 | INT |
| 438 | 213.3 | 187.2 | INT |
| 439 | 213.4 | 194.0 | INT |
| 440 | 213.4 | 187.3 | INT |
| 456 | 238.0 | 236.1 | STRING |
| 457 | 232.0 | 240.0 | MODEL |
| 459 | 236.0 | 239.0 | CONDITIONING |
| 462 | 233.0 | 236.0 | CLIP |
| 463 | 233.0 | 237.0 | CLIP |
| 464 | 241.0 | 242.0 | LATENT |
| 466 | 234.0 | 245.0 | * |
| 467 | 246.0 | 242.1 | VAE |
| 468 | 247.0 | 244.2 | VAE |
| 469 | 239.0 | 244.0 | CONDITIONING |
| 470 | 237.0 | 244.1 | CONDITIONING |
| 471 | 248.0 | 249.0 | * |
| 472 | 248.1 | 250.0 | * |
| 473 | 251.0 | 244.3 | IMAGE |
| 474 | 252.0 | 244.4 | MASK |
| 475 | 240.0 | 253.0 | * |
| 476 | 254.0 | 241.0 | MODEL |
| 477 | 244.0 | 241.1 | CONDITIONING |
| 478 | 244.1 | 241.2 | CONDITIONING |
| 479 | 244.2 | 241.3 | LATENT |
| 481 | 242.0 | 257.0 | * |
| 487 | 144.0 | 259.0 | IMAGE |
| 488 | 242.0 | 260.0 | IMAGE |
| 489 | 261.0 | 260.1 | IMAGE |

## Data Flow
VHS_LoadVideo (160) loads the source video at 16fps with 81-frame cap. VHS_VideoInfo (213) extracts source_width and source_height, which feed to Set_width (195), Set_height (194), and ImageResizeKJ (187) to resize the video to source dimensions. The resized video goes to Set_init_video (157). Get_init_video (143) feeds VHS_SelectImages (144) to extract frame 0, which goes to Set_first_frame (199) and PreviewImage (259).

UNETLoader (232) loads the Flux Fill-dev model, which passes through DifferentialDiffusion (240) and stores via Set_diffusion_model (253). DualCLIPLoader (233) provides CLIP to both CLIPTextEncode nodes. VAELoader (234) stores via Set_flux_vae (245).

StringConstantMultiline (205) provides the prompt text to Set_pos_prompt (206). Get_pos_prompt (238) feeds the text to CLIPTextEncode (236) positive encoder, which passes through FluxGuidance (239) at guidance value 30. CLIPTextEncode (237) creates an empty negative conditioning.

LoadImage (248) provides both the init image (IMAGE→Set_init_image 249) and the mask (MASK→Set_init_image_mask 250). Get_init_image (251) and Get_init_image_mask (252) feed into InpaintModelConditioning (244) along with Get_flux_vae (247) and both conditionings from FluxGuidance and negative encoder. InpaintModelConditioning (244) outputs positive, negative, and latent to KSampler (241).

Get_diffusion_model (254) provides the DifferentialDiffusion-wrapped model to KSampler (241), which runs 20 steps with euler/normal at CFG 1 and denoise 1. VAEDecode (242) decodes using Get_flux_vae (246). The result goes to Set_inpainted_frame (257) and Image Comparer (260) which compares against Get_init_image (261).

## Bus Names
- `init_video` → source video frames (Set: 157, Get: 143)
- `num_frames` → frame count from VHS_LoadVideo (Set: 159)
- `width` → source video width (Set: 195)
- `height` → source video height (Set: 194)
- `first_frame` → first frame from video (Set: 199)
- `pos_prompt` → positive prompt text (Set: 206, Get: 238)
- `flux_vae` → Flux VAE model (Set: 245, Get: 246, 247)
- `init_image` → mask reference image from LoadImage (Set: 249, Get: 251, 261)
- `init_image_mask` → mask from LoadImage (Set: 250, Get: 252)
- `diffusion_model` → DifferentialDiffusion-wrapped UNET (Set: 253, Get: 254)
- `inpainted_frame` → final inpainted output (Set: 257)

## Invariants
- FluxGuidance value must be 30 for proper inpainting behavior.
- KSampler: 20 steps, euler sampler, normal scheduler, CFG 1, denoise 1.
- Model split must use separate UNETLoader, DualCLIPLoader, and VAELoader (not CheckpointLoaderSimple) because Flux Fill-dev requires special model setup.
- DifferentialDiffusion wraps the model for coherent fill regions.
- InpaintModelConditioning is set with noise_mask=false.
- Preserve all named Set/Get bus routing — the workflow depends on named constants rather than direct wiring.
- ImageResizeKJ uses source video dimensions from VHS_VideoInfo with lanczos interpolation and divisible_by=2.
