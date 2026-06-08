# 15_CONSISTENT_DEPTH

## Purpose
Generate temporally consistent depth maps across a video using DepthCrafter, with resizing for standardized input dimensions and video output of the depth sequence.

## Model Stack
- DepthCrafter model: auto-downloaded via DownloadAndLoadDepthCrafterModel (node 2), fp16 enabled, bf16 disabled

## Node Table
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 3 | VHS_LoadVideo | `{video: "SHOT.mp4", force_rate: 0, custom_width: 0, custom_height: 0, frame_load_cap: 0, skip_first_frames: 0, select_every_nth: 1, format: "AnimateDiff"}` |
| 5 | ImageResizeKJv2 | `[960, 540, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` |
| 2 | DownloadAndLoadDepthCrafterModel | `[true, false]` |
| 1 | DepthCrafter | `[true, 4, 1, 110, 25]` |
| 4 | VHS_VideoCombine | `{frame_rate: 25, loop_count: 0, filename_prefix: "AIVFX-PREPROCESS/DEPTH", format: "video/h264-mp4", pix_fmt: "yuv420p", crf: 19, save_metadata: true, trim_to_audio: false, pingpong: false, save_output: true}` |
| 6 | VHS_VideoInfo | `{}` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 1 | 2.0 | 1.0 | DEPTHCRAFTER_MODEL |
| 3 | 1.0 | 4.0 | IMAGE |
| 4 | 3.0 | 5.0 | IMAGE |
| 5 | 5.0 | 1.1 | IMAGE |
| 6 | 3.3 | 6.0 | VHS_VIDEOINFO |

## Data Flow
VHS_LoadVideo (3) loads "SHOT.mp4" and outputs IMAGE frames to ImageResizeKJv2 (5) and VHS_VIDEOINFO to VHS_VideoInfo (6). ImageResizeKJv2 (5) resizes frames to 960x540 using nearest-exact interpolation with stretch mode and sends them to DepthCrafter (1). DownloadAndLoadDepthCrafterModel (2) provides the DEPTHCRAFTER_MODEL to DepthCrafter (1). DepthCrafter (1) computes depth maps and outputs them as IMAGE to VHS_VideoCombine (4), which saves as "AIVFX-PREPROCESS/DEPTH" in h264-mp4 format. VHS_VideoInfo (6) is connected for reference but has no outgoing links.

## Invariants
- ImageResizeKJv2 (5) must resize to 960x540 with nearest-exact interpolation, stretch mode, divisible_by=2.
- DepthCrafter (1) parameters: guidance=true, num_inference_steps=4, overlap=1, max_len=110, target_fps=25.
- DownloadAndLoadDepthCrafterModel (2): fp16=true, bf16=false.
- VHS_VideoCombine (4) output: frame_rate=25, crf=19, format=video/h264-mp4, filename_prefix="AIVFX-PREPROCESS/DEPTH".
