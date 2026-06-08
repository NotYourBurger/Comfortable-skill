# AI-VFX-1.0

## Purpose
WAN-based VFX video workflow that takes a driving video, start/reference images, control images, and an inpaint mask, then generates video frames through a VACE/SkyReels subgraph and outputs both a primary render video and a side-by-side comparison video.

## Model Stack
- WAN UNET: `wan-14B_vace_skyreels_v3_R2V_e4m3fn_v1.safetensors` (fp8_e4m3fn) via UNETLoader (3326)
- LoRA 1: `Wan2.1_T2V_14B_FusionX_LoRA.safetensors` strength 1 via LoraLoaderModelOnly (3327)
- LoRA 2: `wan\\Lenovo.safetensors` strength 1 via LoraLoaderModelOnly (3328) [BYPASSED]
- CLIP: `umt5_xxl_fp8_e4m3fn_scaled.safetensors` (wan, default) via CLIPLoader (3333)
- VAE: `wan_2.1_vae.safetensors` via VAELoader (3334)
- Model sampling: ModelSamplingSD3 (3329) with shift value 6.0

## Node Table

### Decorative/Label Nodes (omitted from functional table)
Nodes 1059, 1060, 1064, 1067 (Reroute, unconnected), 2375 (Note), 2394/2421/2422/2423/2905/3356/3517/3519 (MarkdownNote), 3516 (Label rgthree), 3524/3525/3526/3530/3531/3532/3533/3534/3535/3536/3537/3538 (MickmumpitzLabel)

### Functional Nodes
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 265 | VHS_LoadVideo | `{"video": "DRIVING_VIDEO_030001-0081.mp4", "force_rate": 25, ...}` (title: "DRIVING VIDEO") |
| 280 | ImageResizeKJv2 | `[512, 512, "lanczos", "pad_edge_pixel", "0, 0, 0", "center", 2, "cpu"]` |
| 282 | LoadImage | `["Environment_change_post_apocalyp…_202606070137.jpeg", "image"]` (title: "Start Image / Reference Image 1") |
| 373 | GetNode | `["height"]` (title: "Get_height") |
| 374 | GetNode | `["width"]` (title: "Get_width") |
| 1795 | SetNode | `["startimage"]` (title: "Set_startimage") |
| 2607 | VHS_VideoInfo | `{}` |
| 2687 | SetNode | `["fps"]` (title: "Set_fps") |
| 2845 | 3d3e41f0-5880-459f-8b57-8311a154436c | `[]` (subgraph: "SETTINGS" — outputs width, height, frame_load_cap, skip_frames) |
| 2859 | SetNode | `["height"]` (title: "Set_height") |
| 2860 | SetNode | `["width"]` (title: "Set_width") |
| 3002 | SetNode | `["control"]` (title: "Set_control") |
| 3071 | GetNode | `["modelCLIP"]` (title: "Get_modelCLIP") |
| 3076 | GetNode | `["modelWAN"]` (title: "Get_modelWAN") |
| 3083 | GetNode | `["fps"]` (title: "Get_fps") |
| 3087 | GetNode | `["startimage"]` (title: "Get_startimage") |
| 3088 | GetNode | `["control"]` (title: "Get_control") |
| 3091 | GetNode | `["modelVAE"]` (title: "Get_modelVAE") |
| 3106 | VHS_VideoCombine | `{"frame_rate": 24, "filename_prefix": "AI-VFX", "format": "video/h264-mp4", "crf": 19}` |
| 3228 | c475d739-ec74-430f-a7bd-aab0fdd85070 | `[]` (subgraph: VACE generation node) |
| 3326 | UNETLoader | `["wan-14B_vace_skyreels_v3_R2V_e4m3fn_v1.safetensors", "fp8_e4m3fn"]` |
| 3327 | LoraLoaderModelOnly | `["Wan2.1_T2V_14B_FusionX_LoRA.safetensors", 1]` |
| 3328 | LoraLoaderModelOnly | `["wan\\Lenovo.safetensors", 1]` [BYPASSED] |
| 3329 | ModelSamplingSD3 | `[6.000000000000001]` |
| 3332 | SetNode | `["modelWAN"]` (title: "Set_modelWAN") |
| 3333 | CLIPLoader | `["umt5_xxl_fp8_e4m3fn_scaled.safetensors", "wan", "default"]` |
| 3334 | VAELoader | `["wan_2.1_vae.safetensors"]` |
| 3335 | SetNode | `["modelCLIP"]` (title: "Set_modelCLIP") |
| 3336 | SetNode | `["modelVAE"]` (title: "Set_modelVAE") |
| 3349 | LoadImage | `["pasted/image (4).png", "image"]` (title: "Reference Image 2") [BYPASSED] |
| 3350 | LoadImage | `["pasted/image (4).png", "image"]` (title: "Reference Image 3") [BYPASSED] |
| 3353 | LoadImage | `["Gemini_Generated_Image_wuixp7wuixp7wuix.png", "image"]` (title: "Reference Image 4") [BYPASSED] |
| 3354 | SetNode | `["refimage"]` (title: "Set_refimage") |
| 3359 | GetNode | `["refimage"]` (title: "Get_refimage") |
| 3362 | ImageResizeKJv2 | `[512, 512, "lanczos", "pad_edge_pixel", "0, 0, 0", "center", 2, "cpu"]` [BYPASSED] |
| 3364 | ImageResizeKJv2 | `[512, 512, "lanczos", "pad_edge_pixel", "0, 0, 0", "center", 2, "cpu"]` [BYPASSED] |
| 3365 | ImageResizeKJv2 | `[512, 512, "lanczos", "pad_edge_pixel", "0, 0, 0", "center", 2, "cpu"]` [BYPASSED] |
| 3380 | VHS_LoadVideo | `{"video": "INPAIN_MASK0001-0081.mp4", "force_rate": 25, ...}` (title: "MASK") |
| 3381 | ImageToMask | `["red"]` |
| 3398 | ImageConcatMulti | `[2, "right", true, null]` |
| 3399 | VHS_VideoCombine | `{"frame_rate": 24, "filename_prefix": "AI_Render", "format": "video/h264-mp4", "crf": 19}` |
| 3420 | ImageBatchMulti | `[4, null]` |
| 3431 | SetNode | `["mask"]` (title: "Set_mask") |
| 3432 | GetNode | `["mask"]` (title: "Get_mask") |
| 3468 | GetNode | `["control"]` (title: "Get_control") |
| 3544 | SetNode | `["REF_IMAGE"]` (title: "Set_REF_IMAGE") |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 761 | 374.0 | 280.2 | INT |
| 762 | 373.0 | 280.3 | INT |
| 3111 | 280.0 | 1795.0 | * |
| 4109 | 282.0 | 280.0 | IMAGE |
| 4406 | 265.3 | 2607.0 | VHS_VIDEOINFO |
| 5219 | 2607.0 | 2687.0 | FLOAT |
| 5732 | 3083.0 | 3106.4 | FLOAT |
| 6014 | 3228.0 | 3106.0 | IMAGE |
| 6045 | 2845.0 | 2860.0 | INT |
| 6046 | 2845.0 | 265.2 | INT |
| 6048 | 2845.1 | 2859.0 | INT |
| 6049 | 2845.1 | 265.3 | INT |
| 6185 | 3328.0 | 3329.0 | MODEL |
| 6186 | 3329.0 | 3332.0 | MODEL |
| 6189 | 3333.0 | 3335.0 | CLIP |
| 6190 | 3334.0 | 3336.0 | VAE |
| 6221 | 2845.2 | 265.4 | INT |
| 6236 | 374.0 | 3362.2 | INT |
| 6237 | 373.0 | 3362.3 | INT |
| 6238 | 3349.0 | 3362.0 | IMAGE |
| 6243 | 3076.0 | 3228.0 | MODEL |
| 6244 | 3071.0 | 3228.1 | CLIP |
| 6245 | 3091.0 | 3228.2 | VAE |
| 6249 | 3088.0 | 3228.5 | IMAGE |
| 6250 | 3359.0 | 3228.4 | IMAGE |
| 6252 | 374.0 | 3364.2 | INT |
| 6253 | 373.0 | 3364.3 | INT |
| 6254 | 3350.0 | 3364.0 | IMAGE |
| 6257 | 374.0 | 3365.2 | INT |
| 6258 | 373.0 | 3365.3 | INT |
| 6259 | 3353.0 | 3365.0 | IMAGE |
| 6295 | 2845.0 | 3380.2 | INT |
| 6296 | 2845.1 | 3380.3 | INT |
| 6297 | 2845.2 | 3380.4 | INT |
| 6335 | 3228.0 | 3398.0 | IMAGE |
| 6337 | 3398.0 | 3399.0 | IMAGE |
| 6338 | 3083.0 | 3399.4 | FLOAT |
| 6376 | 3380.0 | 3381.0 | IMAGE |
| 6381 | 3362.0 | 3420.1 | IMAGE |
| 6383 | 3420.0 | 3354.0 | IMAGE |
| 6384 | 3365.0 | 3420.3 | IMAGE |
| 6385 | 3364.0 | 3420.2 | IMAGE |
| 6404 | 2845.3 | 265.5 | INT |
| 6405 | 2845.3 | 3380.5 | INT |
| 6411 | 265.0 | 3002.0 | IMAGE |
| 6420 | 3381.0 | 3431.0 | MASK |
| 6421 | 3432.0 | 3228.6 | MASK |
| 6447 | 280.0 | 3420.0 | IMAGE |
| 6474 | 3468.0 | 3398.1 | IMAGE |
| 6487 | 3087.0 | 3228.3 | IMAGE |
| 6497 | 3327.0 | 3328.0 | MODEL |
| 6606 | 3326.0 | 3327.0 | MODEL |
| 6610 | 282.0 | 3544.0 | IMAGE |

## Data Flow
Subgraph node 2845 (3d3e41f0-5880-459f-8b57-8311a154436c, "SETTINGS") outputs width, height, frame_load_cap, and skip_frames to both VHS_LoadVideo (265, "DRIVING VIDEO") and VHS_LoadVideo (3380, "MASK"). VHS_LoadVideo (265) outputs frames to SetNode (3002, Set_control) and video_info to VHS_VideoInfo (2607) which extracts source_fps to SetNode (2687, Set_fps). LoadImage (282) feeds into ImageResizeKJv2 (280) at 512×512 (lanczos), which outputs to SetNode (1795, Set_startimage) and ImageBatchMulti (3420). Three additional LoadImage nodes (3349/3350/3353, all BYPASSED) feed through ImageResizeKJv2 nodes (3362/3364/3365, all BYPASSED) into ImageBatchMulti (3420), which batches up to 4 images and outputs to SetNode (3354, Set_refimage). VHS_LoadVideo (3380, "MASK") outputs frames to ImageToMask (3381, channel=red) then to SetNode (3431, Set_mask). UNETLoader (3326) → LoraLoaderModelOnly (3327) → LoraLoaderModelOnly (3328, BYPASSED) → ModelSamplingSD3 (3329, shift=6.0) → SetNode (3332, Set_modelWAN). CLIPLoader (3333) → SetNode (3335, Set_modelCLIP). VAELoader (3334) → SetNode (3336, Set_modelVAE). GetNode nodes (3076/3071/3091/3087/3359/3088/3432) retrieve these buses and feed subgraph node 3228 (c475d739-ec74-430f-a7bd-aab0fdd85070) with model, clip, vae, startimage, refimage, control_images, and inpaint_mask. Node 3228 outputs all_frames to VHS_VideoCombine (3106, "AI-VFX") and to ImageConcatMulti (3398) which concatenates with control images from GetNode (3468), then to VHS_VideoCombine (3399, "AI_Render").

## Bus Names
| Bus | Data Type | Set Node | Get Node(s) |
|-----|-----------|----------|-------------|
| width | INT/\* | 2860 | 374 |
| height | INT/\* | 2859 | 373 |
| fps | FLOAT | 2687 | 3083 |
| modelWAN | MODEL | 3332 | 3076 |
| modelCLIP | CLIP | 3335 | 3071 |
| modelVAE | VAE | 3336 | 3091 |
| startimage | IMAGE | 1795 | 3087 |
| refimage | IMAGE | 3354 | 3359 |
| control | IMAGE | 3002 | 3088, 3468 |
| mask | MASK | 3431 | 3432 |
| REF_IMAGE | IMAGE | 3544 | (unused) |

## Invariants
- All resize nodes (280, 3362, 3364, 3365) use 512×512, lanczos, pad_edge_pixel, center, divisible_by=2, cpu.
- Width, height, frame_load_cap, and skip_first_frames values all come from subgraph node 2845 ("SETTINGS").
- Model loader chain order: UNETLoader (3326) → LoraLoaderModelOnly (3327) → LoraLoaderModelOnly (3328) → ModelSamplingSD3 (3329, shift=6.0) → Set_modelWAN.
- Node 3228 (c475d739-ec74-430f-a7bd-aab0fdd85070) is a subgraph that encapsulates VACE generation; preserve its wiring exactly.
- Node 2845 (3d3e41f0-5880-459f-8b57-8311a154436c) is a subgraph named "SETTINGS" that provides resolution/frame presets.
- Keep Set/Get bus names unchanged — they act as named buses across the graph.
- Dual output structure: primary render (3106, "AI-VFX") plus comparison/debug (3399, "AI_Render").
- VHS_VideoCombine nodes use h264-mp4, CRF 19, yuv420p.
