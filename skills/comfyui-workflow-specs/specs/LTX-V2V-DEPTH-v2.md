# LTX-V2V-DEPTH-v2

## Purpose
Depth-guided LTX 2.3 video-to-video workflow that slices a source video, generates depth maps via DepthCrafter, and feeds the depth output plus a first-frame reference image into an IC-LoRA edit subgraph. This version replaces the internal depth subgraph from v1 with an explicit DepthCrafter pipeline at 640×360.

## Model Stack
- Checkpoint: `ltx-2.3-22b-distilled-fp8.safetensors` (inside subgraph node 129)
- Text encoder: `gemma_3_12B_it_fp4_mixed.safetensors` (inside subgraph node 129)
- IC-LoRA: `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` (inside subgraph node 129)
- Abliteration LoRA: `gemma-3-12b-it-abliterated_lora_rank64_bf16.safetensors` (inside subgraph node 129)
- DepthCrafter model: loaded via DownloadAndLoadDepthCrafterModel (710)

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 68 | SaveVideo | `["video/ltx2.3_ic_lora", "auto", "auto"]` |
| 79 | MarkdownNote | (Model Links documentation note) |
| 129 | f9f61b10-b689-4d67-b4fa-0acc1d9b5390 | `[]` (subgraph: "First-Last-Frame to Video (LTX-2.3)") |
| 199 | LoadVideo | `["BASE_VIDEO_0117-0200.mp4", "image"]` |
| 200 | LoadImage | `["retouch_this_girl_don't_change_202606071946.jpeg", "image"]` |
| 692 | Video Slice | `[0, 3.36, true]` |
| 693 | PreviewImage | `[]` [BYPASSED] |
| 697 | ed545fa5-009c-4ccc-b318-4c00dd239751 | `[]` (subgraph: depth estimation) [BYPASSED] |
| 698 | MarkdownNote | (IC-LoRA usage note) |
| 705 | VHS_VideoInfo | `{}` (unconnected) |
| 707 | DepthCrafter | `[true, 5, 1, 81, 14]` |
| 708 | GetVideoComponents | `[]` |
| 710 | DownloadAndLoadDepthCrafterModel | `[true, false]` |
| 711 | ImageResizeKJv2 | `[640, 360, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` |
| 712 | PreviewImage | `[]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 256 | 129.0 | 68.0 | VIDEO |
| 297 | 200.0 | 129.0 | IMAGE |
| 1759 | 199.0 | 692.0 | VIDEO |
| 1771 | 692.0 | 697.1 | VIDEO |
| 1773 | 697.1 | 693.0 | IMAGE |
| 1794 | 692.0 | 708.0 | VIDEO |
| 1796 | 710.0 | 707.0 | DEPTHCRAFTER_MODEL |
| 1797 | 708.0 | 711.0 | IMAGE |
| 1798 | 711.0 | 707.1 | IMAGE |
| 1799 | 707.0 | 712.0 | IMAGE |
| 1800 | 707.0 | 129.1 | IMAGE |

## Data Flow
LoadVideo (199) loads source video and passes it to Video Slice (692) with parameters `[0, 3.36, true]`. The sliced video feeds two branches: (1) the bypassed subgraph node 697 (ed545fa5-009c-4ccc-b318-4c00dd239751) which is inactive, and (2) GetVideoComponents (708) which extracts images. Those images are resized by ImageResizeKJv2 (711) to 640×360 and fed into DepthCrafter (707) along with the DepthCrafter model from DownloadAndLoadDepthCrafterModel (710). DepthCrafter (707) outputs depth_maps to both PreviewImage (712) and the control_images input (slot 1) of subgraph node 129 (f9f61b10-b689-4d67-b4fa-0acc1d9b5390). LoadImage (200) provides the first_frame reference to node 129 at slot 0. Node 129 outputs VIDEO to SaveVideo (68).

## Invariants
- Video Slice (692) parameters `[0, 3.36, true]` control the segment duration; the slice length determines output video length.
- DepthCrafter (707) settings: `[true, 5, 1, 81, 14]` — keep these values for consistent depth estimation.
- Depth input resize is 640×360, nearest-exact, stretch, divisible_by=2, cpu.
- Node 697 (internal depth subgraph) is BYPASSED (mode=4); the explicit DepthCrafter pipeline is the active depth path.
- Reference downscale factor inside the IC-LoRA subgraph is `0.5`.
- Save path is `video/ltx2.3_ic_lora`.
