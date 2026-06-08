# LTX-V2V-DEPTH

## Purpose
Depth-guided LTX 2.3 video-to-video workflow that slices a source video, runs it through a depth estimation subgraph, and feeds the depth output plus a first-frame reference image into an IC-LoRA edit subgraph to generate an edited output video.

## Model Stack
- Checkpoint: `ltx-2.3-22b-distilled-fp8.safetensors` (inside subgraph node 129)
- Text encoder: `gemma_3_12B_it_fp4_mixed.safetensors` (inside subgraph node 129)
- IC-LoRA: `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` (inside subgraph node 129)
- Abliteration LoRA: `gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors` (inside subgraph node 129)
- Depth estimation: `moge_2_vitl_normal_fp16.safetensors` (inside subgraph node 697)

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 68 | SaveVideo | `["video/ltx2.3_ic_lora", "auto", "auto"]` |
| 79 | MarkdownNote | (Model Links documentation note) |
| 129 | f9f61b10-b689-4d67-b4fa-0acc1d9b5390 | `[]` (subgraph: "First-Last-Frame to Video (LTX-2.3)") |
| 199 | LoadVideo | `["Row Footage (10.50 Sec).mp4", "image"]` |
| 200 | LoadImage | `["ChatGPT Image Jun 7, 2026, 02_25_19 PM.png", "image"]` |
| 692 | Video Slice | `[0, 4, true]` |
| 693 | PreviewImage | `[]` |
| 697 | ed545fa5-009c-4ccc-b318-4c00dd239751 | `[]` (subgraph: depth estimation) |
| 698 | MarkdownNote | (IC-LoRA usage note) |
| 705 | VHS_VideoInfo | `{}` (unconnected) |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 256 | 129.0 | 68.0 | VIDEO |
| 297 | 200.0 | 129.0 | IMAGE |
| 1759 | 199.0 | 692.0 | VIDEO |
| 1771 | 692.0 | 697.1 | VIDEO |
| 1772 | 697.1 | 129.1 | IMAGE |
| 1773 | 697.1 | 693.0 | IMAGE |

## Data Flow
LoadVideo (199) loads source video and passes it to Video Slice (692) which trims it to 0-4 seconds. The sliced video feeds into subgraph node 697 (ed545fa5-009c-4ccc-b318-4c00dd239751) at slot 1 for depth estimation. The depth output (slot 1) goes to subgraph node 129 (f9f61b10-b689-4d67-b4fa-0acc1d9b5390) at the control_images input (slot 1), and also to PreviewImage (693) for visualization. LoadImage (200) provides the first_frame reference image to node 129 at slot 0. Node 129 generates a VIDEO output that goes to SaveVideo (68). VHS_VideoInfo (705) is present but unconnected.

## Invariants
- Video Slice (692) must receive the source video before the depth subgraph; slice parameters `[0, 4, true]` control the segment duration.
- Reference downscale factor inside the IC-LoRA subgraph is `0.5`.
- Node 129 is a subgraph named "First-Last-Frame to Video (LTX-2.3)" - its internal wiring must be preserved exactly.
- Node 697 is a subgraph for depth estimation - its internal wiring must be preserved exactly.
- Save path is `video/ltx2.3_ic_lora`.

