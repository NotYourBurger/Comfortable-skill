# 05_SDXL_ControlNets_v2

## Purpose
Second version of the SDXL ControlNet template, featuring four branches (depth, depth+LoRAs, sketch, canny+depth dual-ControlNet) with updated LoRA selections, higher depth preprocessor resolution, and a dual-ControlNet chaining example in the canny branch.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors` (loaded per-branch: nodes 148, 4, 190, 237)
- ControlNet (depth): `SDXL\control-lora-depth-rank256.safetensors` (nodes 146, 43, 250)
- ControlNet (sketch): `SDXL\control-lora-sketch-rank256.safetensors` (node 188)
- ControlNet (canny): `SDXL\control-lora-canny-rank256.safetensors` (node 234)
- LoRA: `CircuitryTech_WM_IL.safetensors` strength_model 0.8, strength_clip 1 (node 136)
- LoRA: `3l3ctronics-step00003000.safetensors` strength_model 1, strength_clip 1 (node 181)
- LoRA: `Cinematic_Movie_Look.safetensors` strength_model 1, strength_clip 1 (node 243)
- Depth preprocessor: `depth_anything_v2_vitl.pth` (nodes 135, 152, 245)

## Node Table

### Branch A: Depth ControlNet (mode 4 = muted)
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 148 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 155 | LoadImage | `["google_earth.png", "image"]` |
| 157 | CLIPTextEncode (Positive) | `["computer, circuits, wires, RAM, computer chips, cmos, transistors, capacitors, cpu, city, night, electricity, glowing neon, cinematic, futuristic, realistic"]` |
| 158 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 152 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 512]` |
| 147 | PreviewImage | Depth map preview |
| 144 | Reroute | IMAGE passthrough |
| 146 | ControlNetLoader | `["SDXL\\control-lora-depth-rank256.safetensors"]` |
| 145 | ControlNetApplyAdvanced | `[1.0, 0, 1]` |
| 149 | Reroute | VAE passthrough |
| 141 | Reroute | VAE passthrough |
| 143 | EmptyLatentImage | `[1920, 1080, 1]` |
| 159 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 154 | VAEDecode | — |
| 153 | Image Comparer (rgthree) | Slide mode |
| 156 | Image Comparer (rgthree) | Slide mode |

### Branch B: Depth ControlNet + LoRAs (mode 4 = muted)
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 4 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 31 | LoadImage | `["viber_image_2026-06-05_18-47-26-299.jpg", "image"]` |
| 136 | LoraLoader | `["CircuitryTech_WM_IL.safetensors", 0.8, 1]` |
| 181 | LoraLoader | `["3l3ctronics-step00003000.safetensors", 1, 1]` |
| 243 | LoraLoader | `["Cinematic_Movie_Look.safetensors", 1, 1]` |
| 6 | CLIPTextEncode (Positive) | `["C1nematic, destroyed post apocalyptic city"]` |
| 86 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 135 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 1024]` |
| 134 | PreviewImage | Depth map preview |
| 62 | Reroute | IMAGE passthrough |
| 43 | ControlNetLoader | `["SDXL\\control-lora-depth-rank256.safetensors"]` |
| 63 | ControlNetApplyAdvanced | `[1.0, 0, 1]` |
| 30 | Reroute | VAE passthrough |
| 29 | Reroute | VAE passthrough |
| 27 | Reroute | MODEL passthrough |
| 75 | EmptyLatentImage | `[1440, 1080, 1]` |
| 3 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 8 | VAEDecode | — |
| 132 | Image Comparer (rgthree) | Click mode |
| 140 | Image Comparer (rgthree) | Slide mode |

### Branch C: Sketch ControlNet (mode 4 = muted)
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 190 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 195 | LoadImage | `["sketch.png", "image"]` |
| 199 | CLIPTextEncode (Positive) | `["city, day, cinematic, futuristic, realistic"]` |
| 194 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 188 | ControlNetLoader | `["SDXL\\control-lora-sketch-rank256.safetensors"]` |
| 187 | ControlNetApplyAdvanced | `[1.0, 0, 0.5]` |
| 184 | Reroute | MODEL passthrough |
| 191 | Reroute | VAE passthrough |
| 183 | Reroute | VAE passthrough |
| 185 | EmptyLatentImage | `[1920, 1080, 1]` |
| 196 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 197 | VAEDecode | — |
| 193 | Image Comparer (rgthree) | Slide mode |
| 198 | Image Comparer (rgthree) | Click mode |

### Branch D: Dual Canny+Depth ControlNet (mode 0 = active)
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 237 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 240 | LoadImage | `["Preview.png", "image"]` |
| 244 | Image Resize (rgthree) | `["pixels", 1920, 1080, "crop", "nearest-exact"]` |
| 242 | Canny | `[0.15, 0.71]` |
| 245 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 1024]` |
| 235 | PreviewImage | Canny edge preview |
| 246 | PreviewImage | Depth map preview |
| 238 | CLIPTextEncode (Positive) | `["C1nematic foggy atmospheric spooky, destroyed post apocalyptic city, overgrown with vines and greens."]` |
| 241 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 234 | ControlNetLoader | `["SDXL\\control-lora-canny-rank256.safetensors"]` |
| 250 | ControlNetLoader | `["SDXL\\control-lora-depth-rank256.safetensors"]` |
| 239 | ControlNetApplyAdvanced | `[1.0, 0, 0.5]` (canny, first in chain) |
| 249 | ControlNetApplyAdvanced | `[1.0, 0.5, 1]` (depth, second in chain) |
| 228 | Reroute | MODEL passthrough |
| 229 | Reroute | VAE passthrough |
| 227 | Reroute | VAE passthrough |
| 236 | EmptyLatentImage | `[1920, 1080, 1]` |
| 231 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 232 | VAEDecode | — |
| 233 | Image Comparer (rgthree) | Click mode |
| 230 | Image Comparer (rgthree) | Slide mode |
| 252 | SetNode | `[""]` (unused) |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 7 | 3.0 | 8.0 | LATENT |
| 36 | 27.0 | 3.0 | MODEL |
| 40 | 29.0 | 8.1 | VAE |
| 43 | 4.2 | 30.0 | * |
| 111 | 6.0 | 63.0 | CONDITIONING |
| 113 | 43.0 | 63.2 | CONTROL_NET |
| 119 | 63.0 | 3.1 | CONDITIONING |
| 120 | 63.1 | 3.2 | CONDITIONING |
| 135 | 62.0 | 63.3 | IMAGE |
| 141 | 75.0 | 3.3 | LATENT |
| 149 | 86.0 | 63.1 | CONDITIONING |
| 150 | 30.0 | 29.0 | * |
| 202 | 4.1 | 86.0 | CLIP |
| 206 | 8.0 | 132.0 | IMAGE |
| 207 | 62.0 | 132.1 | IMAGE |
| 211 | 31.0 | 135.0 | IMAGE |
| 212 | 135.0 | 62.0 | * |
| 213 | 135.0 | 134.0 | IMAGE |
| 216 | 4.1 | 136.1 | CLIP |
| 218 | 4.0 | 136.0 | MODEL |
| 225 | 8.0 | 140.0 | IMAGE |
| 226 | 31.0 | 140.1 | IMAGE |
| 227 | 149.0 | 141.0 | * |
| 229 | 152.0 | 144.0 | * |
| 230 | 157.0 | 145.0 | CONDITIONING |
| 231 | 158.0 | 145.1 | CONDITIONING |
| 232 | 146.0 | 145.2 | CONTROL_NET |
| 233 | 144.0 | 145.3 | IMAGE |
| 234 | 152.0 | 147.0 | IMAGE |
| 235 | 148.2 | 149.0 | * |
| 238 | 155.0 | 152.0 | IMAGE |
| 239 | 154.0 | 153.0 | IMAGE |
| 240 | 155.0 | 153.1 | IMAGE |
| 241 | 159.0 | 154.0 | LATENT |
| 242 | 141.0 | 154.1 | VAE |
| 243 | 154.0 | 156.0 | IMAGE |
| 244 | 144.0 | 156.1 | IMAGE |
| 246 | 148.1 | 158.0 | CLIP |
| 248 | 145.0 | 159.1 | CONDITIONING |
| 249 | 145.1 | 159.2 | CONDITIONING |
| 250 | 143.0 | 159.3 | LATENT |
| 252 | 148.1 | 157.0 | CLIP |
| 253 | 148.0 | 159.0 | MODEL |
| 286 | 136.0 | 181.0 | MODEL |
| 288 | 136.1 | 181.1 | CLIP |
| 290 | 191.0 | 183.0 | * |
| 293 | 199.0 | 187.0 | CONDITIONING |
| 294 | 194.0 | 187.1 | CONDITIONING |
| 295 | 188.0 | 187.2 | CONTROL_NET |
| 298 | 190.2 | 191.0 | * |
| 300 | 197.0 | 193.0 | IMAGE |
| 301 | 195.0 | 193.1 | IMAGE |
| 302 | 190.1 | 194.0 | CLIP |
| 303 | 184.0 | 196.0 | MODEL |
| 304 | 187.0 | 196.1 | CONDITIONING |
| 305 | 187.1 | 196.2 | CONDITIONING |
| 306 | 185.0 | 196.3 | LATENT |
| 307 | 196.0 | 197.0 | LATENT |
| 308 | 183.0 | 197.1 | VAE |
| 309 | 197.0 | 198.0 | IMAGE |
| 318 | 190.0 | 184.0 | * |
| 319 | 190.1 | 199.0 | CLIP |
| 322 | 195.0 | 187.3 | IMAGE |
| 323 | 195.0 | 198.1 | IMAGE |
| 351 | 229.0 | 227.0 | * |
| 352 | 237.0 | 228.0 | * |
| 353 | 237.2 | 229.0 | * |
| 354 | 232.0 | 230.0 | IMAGE |
| 356 | 228.0 | 231.0 | MODEL |
| 359 | 236.0 | 231.3 | LATENT |
| 360 | 231.0 | 232.0 | LATENT |
| 361 | 227.0 | 232.1 | VAE |
| 362 | 232.0 | 233.0 | IMAGE |
| 364 | 237.1 | 238.0 | CLIP |
| 365 | 238.0 | 239.0 | CONDITIONING |
| 366 | 241.0 | 239.1 | CONDITIONING |
| 367 | 234.0 | 239.2 | CONTROL_NET |
| 369 | 237.1 | 241.0 | CLIP |
| 371 | 242.0 | 235.0 | IMAGE |
| 372 | 242.0 | 239.3 | IMAGE |
| 373 | 242.0 | 230.1 | IMAGE |
| 378 | 181.0 | 243.0 | MODEL |
| 379 | 181.1 | 243.1 | CLIP |
| 380 | 243.1 | 6.0 | CLIP |
| 381 | 243.0 | 27.0 | MODEL |
| 382 | 240.0 | 244.0 | IMAGE |
| 383 | 244.0 | 242.0 | IMAGE |
| 384 | 244.0 | 245.0 | IMAGE |
| 385 | 245.0 | 246.0 | IMAGE |
| 389 | 239.0 | 249.0 | CONDITIONING |
| 390 | 239.1 | 249.1 | CONDITIONING |
| 391 | 250.0 | 249.2 | CONTROL_NET |
| 392 | 249.0 | 231.1 | CONDITIONING |
| 393 | 249.1 | 231.2 | CONDITIONING |
| 394 | 245.0 | 249.3 | IMAGE |
| 400 | 244.0 | 233.1 | IMAGE |

## Data Flow

**Branch A (Depth ControlNet — muted):** CheckpointLoaderSimple (148) provides MODEL, CLIP, and VAE. LoadImage (155) loads "google_earth.png" and feeds DepthAnythingV2Preprocessor (152) at resolution 512. The depth map passes through Reroute (144) to ControlNetApplyAdvanced (145) and PreviewImage (147). ControlNetLoader (146) loads the depth ControlNet. CLIPTextEncode (157/158) provide conditioning to ControlNetApplyAdvanced (145) at strength 1.0, start 0, end 1.0. KSampler (159) receives MODEL, conditioning, and latent from EmptyLatentImage (143) at 1920x1080. VAEDecode (154) decodes via VAE through Reroutes (149→141).

**Branch B (Depth + LoRAs — muted):** CheckpointLoaderSimple (4) feeds a three-LoRA chain: LoraLoader (136) CircuitryTech_WM_IL at 0.8 → LoraLoader (181) 3l3ctronics at 1.0 → LoraLoader (243) Cinematic_Movie_Look at 1.0. The final MODEL flows through Reroute (27) to KSampler (3), and final CLIP flows to CLIPTextEncode (6). LoadImage (31) feeds DepthAnythingV2Preprocessor (135) at resolution 1024 (higher than v1). The depth map passes through Reroute (62) to ControlNetApplyAdvanced (63) at strength 1.0, start 0, end 1.0. EmptyLatentImage (75) produces 1440x1080 latent. KSampler (3) samples and VAEDecode (8) decodes.

**Branch C (Sketch ControlNet — muted):** Identical structure to v1. CheckpointLoaderSimple (190) feeds through Reroutes. LoadImage (195) loads "sketch.png" directly to ControlNetApplyAdvanced (187) with sketch ControlNet from node 188, at strength 1.0, start 0, end 0.5. KSampler (196) uses EmptyLatentImage (185) at 1920x1080.

**Branch D (Dual Canny+Depth ControlNet — active):** CheckpointLoaderSimple (237) provides MODEL through Reroute (228) and CLIP to CLIPTextEncode (238 positive, 241 negative). LoadImage (240) loads "Preview.png" and feeds Image Resize (244) which crops/scales to 1920x1080. The resized image feeds three paths: (1) Canny (242) with thresholds 0.15/0.71 for edge detection; (2) DepthAnythingV2Preprocessor (245) at resolution 1024 for depth estimation; (3) Image Comparer (233) for reference. The Canny output feeds the first ControlNetApplyAdvanced (239) with canny ControlNet from node 234, at strength 1.0, start 0, end 0.5. The depth output from node 245 feeds the second ControlNetApplyAdvanced (249) with depth ControlNet from node 250, at strength 1.0, start 0.5, end 1.0. The two ControlNets are chained: conditioning flows from node 239 to node 249, creating a sequential canny-then-depth pipeline. KSampler (231) receives the final conditioning and latent from EmptyLatentImage (236) at 1920x1080. VAEDecode (232) decodes the result.

## Invariants
- All KSampler nodes use identical settings: seed 123456789, 15 steps, CFG 2, euler_ancestral, karras, denoise 1.0.
- Branch D demonstrates dual ControlNet chaining: canny (start 0, end 0.5) feeds into depth (start 0.5, end 1.0) — they split the denoising timeline in half.
- LoRA load order in Branch B: CircuitryTech_WM_IL (136) at 0.8 → 3l3ctronics (181) at 1.0 → Cinematic_Movie_Look (243) at 1.0.
- Branch B uses 1440x1080 latent; all other branches use 1920x1080.
- DepthAnythingV2Preprocessor resolution is 1024 in Branch B and Branch D (higher than v1's 512). Branch A still uses 512.
- Branch D uses Image Resize (rgthree) to normalize input image to 1920x1080 before preprocessing.
- Canny thresholds are 0.15 (low) and 0.71 (high) in both Branch D canny nodes.
- Branch A ControlNet end_percent is 1.0 (changed from v1's 0.5).
- Branch B ControlNet end_percent is 1.0 (changed from v1's 0.5).
