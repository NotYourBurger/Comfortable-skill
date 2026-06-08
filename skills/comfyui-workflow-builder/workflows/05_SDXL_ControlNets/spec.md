# 05_SDXL_ControlNets

## Purpose
SDXL multi-branch ControlNet template demonstrating four independent examples: depth ControlNet, depth ControlNet with LoRAs, sketch ControlNet, and canny ControlNet - all using the same SDXL Lightning base model.

## Model Stack
- Checkpoint: `SDXL\lightning\dreamshaperXL_lightningDPMSDE.safetensors` (loaded per-branch: nodes 148, 4, 190, 237)
- ControlNet (depth): `SDXL\control-lora-depth-rank256.safetensors` (nodes 146, 43)
- ControlNet (sketch): `SDXL\control-lora-sketch-rank256.safetensors` (node 188)
- ControlNet (canny): `SDXL\control-lora-canny-rank256.safetensors` (node 234)
- LoRA: `SDXL\CircuitryTechXL-000008.safetensors` strength_model 0.8, strength_clip 1 (node 136)
- LoRA: `SDXL\3l3ctronics-step00003000.safetensors` strength_model 0.5, strength_clip 1 (node 181)
- Depth preprocessor: `depth_anything_v2_vitl.pth` (nodes 135, 152)

## Node Table

### Branch A: Depth ControlNet (mode 0 = active)
| ID | class_type | Key Widget Values |
|---|---|---|
| 148 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 155 | LoadImage | `["google_earth.png", "image"]` |
| 157 | CLIPTextEncode (Positive) | `["computer, circuits, wires, RAM, computer chips, cmos, transistors, capacitors, cpu, city, night, electricity, glowing neon, cinematic, futuristic, realistic"]` |
| 158 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 152 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 512]` |
| 147 | PreviewImage | Depth map preview |
| 144 | Reroute | IMAGE passthrough |
| 146 | ControlNetLoader | `["SDXL\\control-lora-depth-rank256.safetensors"]` |
| 145 | ControlNetApplyAdvanced | `[1.0, 0, 0.5]` |
| 149 | Reroute | VAE passthrough |
| 141 | Reroute | VAE passthrough |
| 143 | EmptyLatentImage | `[1920, 1080, 1]` |
| 159 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 154 | VAEDecode | - |
| 153 | Image Comparer (rgthree) | Slide mode |
| 156 | Image Comparer (rgthree) | Slide mode |

### Branch B: Depth ControlNet + LoRAs (mode 4 = muted)
| ID | class_type | Key Widget Values |
|---|---|---|
| 4 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 31 | LoadImage | `["google_earth.png", "image"]` |
| 136 | LoraLoader | `["SDXL\\CircuitryTechXL-000008.safetensors", 0.8, 1]` |
| 181 | LoraLoader | `["SDXL\\3l3ctronics-step00003000.safetensors", 0.5, 1]` |
| 6 | CLIPTextEncode (Positive) | `["3l3ctronics, circuitrytech, computer, circuits, wires, RAM, computer chips, cmos, transistors, capacitors, cpu, city, night, electricity, glowing neon, cinematic, futuristic, realistic"]` |
| 86 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 135 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 512]` |
| 134 | PreviewImage | Depth map preview |
| 62 | Reroute | IMAGE passthrough |
| 43 | ControlNetLoader | `["SDXL\\control-lora-depth-rank256.safetensors"]` |
| 63 | ControlNetApplyAdvanced | `[1.0, 0, 0.5]` |
| 30 | Reroute | VAE passthrough |
| 29 | Reroute | VAE passthrough |
| 27 | Reroute | MODEL passthrough |
| 75 | EmptyLatentImage | `[1920, 1080, 1]` |
| 3 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 8 | VAEDecode | - |
| 132 | Image Comparer (rgthree) | Click mode |
| 140 | Image Comparer (rgthree) | Slide mode |

### Branch C: Sketch ControlNet (mode 4 = muted)
| ID | class_type | Key Widget Values |
|---|---|---|
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
| 197 | VAEDecode | - |
| 193 | Image Comparer (rgthree) | Slide mode |
| 198 | Image Comparer (rgthree) | Click mode |

### Branch D: Canny ControlNet (mode 4 = muted)
| ID | class_type | Key Widget Values |
|---|---|---|
| 237 | CheckpointLoaderSimple | `["SDXL\\lightning\\dreamshaperXL_lightningDPMSDE.safetensors"]` |
| 240 | LoadImage | `["robot_pose.png", "image"]` |
| 242 | Canny | `[0.15, 0.71]` |
| 235 | PreviewImage | Canny edge preview |
| 238 | CLIPTextEncode (Positive) | `["a robot"]` |
| 241 | CLIPTextEncode (Negative) | `["low quality, drawing, illustration, sketch, painting"]` |
| 234 | ControlNetLoader | `["SDXL\\control-lora-canny-rank256.safetensors"]` |
| 239 | ControlNetApplyAdvanced | `[1.0, 0, 1]` |
| 228 | Reroute | MODEL passthrough |
| 229 | Reroute | VAE passthrough |
| 227 | Reroute | VAE passthrough |
| 236 | EmptyLatentImage | `[1920, 1080, 1]` |
| 231 | KSampler | `[123456789, "fixed", 15, 2, "euler_ancestral", "karras", 1]` |
| 232 | VAEDecode | - |
| 233 | Image Comparer (rgthree) | Click mode |
| 230 | Image Comparer (rgthree) | Slide mode |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
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
| 287 | 181.0 | 27.0 | * |
| 288 | 136.1 | 181.1 | CLIP |
| 289 | 181.1 | 6.0 | CLIP |
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
| 357 | 239.0 | 231.1 | CONDITIONING |
| 358 | 239.1 | 231.2 | CONDITIONING |
| 359 | 236.0 | 231.3 | LATENT |
| 360 | 231.0 | 232.0 | LATENT |
| 361 | 227.0 | 232.1 | VAE |
| 362 | 232.0 | 233.0 | IMAGE |
| 364 | 237.1 | 238.0 | CLIP |
| 365 | 238.0 | 239.0 | CONDITIONING |
| 366 | 241.0 | 239.1 | CONDITIONING |
| 367 | 234.0 | 239.2 | CONTROL_NET |
| 369 | 237.1 | 241.0 | CLIP |
| 370 | 240.0 | 242.0 | IMAGE |
| 371 | 242.0 | 235.0 | IMAGE |
| 372 | 242.0 | 239.3 | IMAGE |
| 373 | 242.0 | 230.1 | IMAGE |

## Data Flow

**Branch A (Depth ControlNet - active):** CheckpointLoaderSimple (148) provides MODEL, CLIP, and VAE. LoadImage (155) loads "google_earth.png" and feeds DepthAnythingV2Preprocessor (152) which produces a depth map at resolution 512. The depth map passes through Reroute (144) to ControlNetApplyAdvanced (145) and PreviewImage (147). ControlNetLoader (146) loads "control-lora-depth-rank256.safetensors" and feeds ControlNetApplyAdvanced (145). CLIPTextEncode (157) positive and CLIPTextEncode (158) negative provide conditioning to ControlNetApplyAdvanced (145), which outputs modified conditioning at strength 1.0, start 0, end 0.5. KSampler (159) receives MODEL from node 148, conditioning from node 145, and latent from EmptyLatentImage (143) at 1920x1080. VAEDecode (154) decodes the result using VAE via Reroutes (149-141). Image Comparer nodes (153, 156) compare the output against the input and depth map.

**Branch B (Depth + LoRAs - muted):** CheckpointLoaderSimple (4) feeds LoraLoader (136) with CircuitryTechXL at strength 0.8, then LoraLoader (181) with 3l3ctronics at strength 0.5. The LoRA chain outputs MODEL through Reroute (27) to KSampler (3) and CLIP to CLIPTextEncode (6) positive. LoadImage (31) feeds DepthAnythingV2Preprocessor (135) at resolution 512, producing a depth map through Reroute (62) to ControlNetApplyAdvanced (63). ControlNetLoader (43) provides the depth ControlNet. KSampler (3) uses EmptyLatentImage (75) at 1920x1080. VAEDecode (8) decodes using VAE via Reroutes (30-29). Image Comparer nodes (132, 140) provide QA comparison.

**Branch C (Sketch ControlNet - muted):** CheckpointLoaderSimple (190) provides MODEL through Reroute (184) to KSampler (196), CLIP to CLIPTextEncode (199 positive, 194 negative), and VAE through Reroutes (191-183). LoadImage (195) loads "sketch.png" and feeds directly to ControlNetApplyAdvanced (187) as the control image. ControlNetLoader (188) loads "control-lora-sketch-rank256.safetensors". KSampler (196) uses EmptyLatentImage (185) at 1920x1080. VAEDecode (197) decodes the result. Image Comparer nodes (193, 198) compare output against input.

**Branch D (Canny ControlNet - muted):** CheckpointLoaderSimple (237) provides MODEL through Reroute (228) to KSampler (231), CLIP to CLIPTextEncode (238 positive, 241 negative), and VAE through Reroutes (229-227). LoadImage (240) loads "robot_pose.png" and feeds Canny (242) with low_threshold 0.15, high_threshold 0.71. The Canny output feeds ControlNetApplyAdvanced (239), PreviewImage (235), and Image Comparer (230). ControlNetLoader (234) loads "control-lora-canny-rank256.safetensors". ControlNetApplyAdvanced (239) applies at strength 1.0, start 0, end 1 (full range). KSampler (231) uses EmptyLatentImage (236) at 1920x1080. VAEDecode (232) decodes the result. Image Comparer nodes (233, 230) provide QA.

## Invariants
- All four branches are independent pipelines; only one should be active (mode 0) at a time. Branch A is currently active.
- All KSampler nodes use identical settings: seed 123456789, 15 steps, CFG 2, euler_ancestral, karras, denoise 1.0.
- All EmptyLatentImage nodes use 1920x1080 batch 1.
- ControlNet strength is 1.0 across all branches. End_percent varies: 0.5 for depth and sketch, 1.0 for canny.
- LoRA load order in Branch B is critical: CircuitryTechXL (136) first at 0.8, then 3l3ctronics (181) at 0.5.
- Canny thresholds in Branch D are low_threshold 0.15 and high_threshold 0.71.
- DepthAnythingV2Preprocessor resolution is 512 in both depth branches.
- The sketch branch feeds the raw sketch image directly to ControlNetApplyAdvanced (no preprocessing).

