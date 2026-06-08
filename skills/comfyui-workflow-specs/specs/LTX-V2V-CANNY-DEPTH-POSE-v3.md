# LTX-V2V-CANNY-DEPTH-POSE-v3

## Purpose
LTX 2.3 multi-control IC-LoRA workflow that drives generation from a first-frame reference image with three separate pre-rendered control videos (canny, depth, pose), each resized to 640×360 and fed into distinct control input slots of the edit subgraph.

## Model Stack
- Checkpoint: `ltx-2.3-22b-distilled-fp8.safetensors` (inside subgraph node 129)
- Text encoder: `gemma_3_12B_it_fp4_mixed.safetensors` (inside subgraph node 129)
- IC-LoRA: `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` (inside subgraph node 129)
- Abliteration LoRA: `gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors` (inside subgraph node 129)
- Depth estimation: `moge_2_vitl_normal_fp16.safetensors` (referenced in MarkdownNote)

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 68 | SaveVideo | `["video/ltx2.3_ic_lora", "auto", "auto"]` |
| 79 | MarkdownNote | (Model Links documentation note) |
| 129 | f9f61b10-b689-4d67-b4fa-0acc1d9b5390 | `[]` (subgraph: "First-Last-Frame to Video (LTX-2.3)") |
| 200 | LoadImage | `["retouch_this_girl_don't_change_202606071946.jpeg", "image"]` |
| 698 | MarkdownNote | (IC-LoRA usage note) |
| 720 | LoadVideo | `["CANNY_00004.mp4", "image"]` |
| 721 | GetVideoComponents | `[]` (title: "CANNY: components") |
| 722 | ImageResizeKJv2 | `[640, 360, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` (title: "CANNY: resize -> control 1") |
| 723 | LoadVideo | `["DEPTH_00001.mp4", "image"]` |
| 724 | GetVideoComponents | `[]` (title: "DEPTH: components") |
| 725 | ImageResizeKJv2 | `[640, 360, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` (title: "DEPTH: resize -> control 13") |
| 726 | LoadVideo | `["POSE_00001.mp4", "image"]` |
| 727 | GetVideoComponents | `[]` (title: "POSE: components") |
| 728 | ImageResizeKJv2 | `[640, 360, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` (title: "POSE: resize -> control 14") |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 256 | 129.0 | 68.0 | VIDEO |
| 297 | 200.0 | 129.0 | IMAGE |
| 1800 | 722.0 | 129.1 | IMAGE |
| 1810 | 720.0 | 721.0 | VIDEO |
| 1811 | 721.0 | 722.0 | IMAGE |
| 1812 | 723.0 | 724.0 | VIDEO |
| 1813 | 724.0 | 725.0 | IMAGE |
| 1814 | 725.0 | 129.13 | IMAGE |
| 1815 | 726.0 | 727.0 | VIDEO |
| 1816 | 727.0 | 728.0 | IMAGE |
| 1817 | 728.0 | 129.14 | IMAGE |

## Data Flow
LoadImage (200) provides the first_frame reference to subgraph node 129 (f9f61b10-b689-4d67-b4fa-0acc1d9b5390) at slot 0. Three parallel control branches feed into node 129: **Canny** — LoadVideo (720) → GetVideoComponents (721) → ImageResizeKJv2 (722, 640×360) → node 129 slot 1 (control_images). **Depth** — LoadVideo (723) → GetVideoComponents (724) → ImageResizeKJv2 (725, 640×360) → node 129 slot 13 (control_images_2). **Pose** — LoadVideo (726) → GetVideoComponents (727) → ImageResizeKJv2 (728, 640×360) → node 129 slot 14 (control_images_3). Node 129 outputs VIDEO to SaveVideo (68).

## Invariants
- All three control resize nodes use identical settings: 640×360, nearest-exact, stretch, divisible_by=2, cpu.
- The three control streams are kept separate and frame-aligned; canny goes to slot 1, depth to slot 13, pose to slot 14.
- Node 129 is a subgraph named "First-Last-Frame to Video (LTX-2.3)" — its internal wiring must be preserved exactly.
- Reference downscale factor inside the IC-LoRA subgraph is `0.5`.
- Save path is `video/ltx2.3_ic_lora`.
