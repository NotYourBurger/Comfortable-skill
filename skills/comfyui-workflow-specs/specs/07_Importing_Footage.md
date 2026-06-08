# 07_Importing_Footage

## Purpose
Demonstrates three methods for importing footage into ComfyUI: EXR sequence loading/saving, video file loading with depth preprocessing, and a manual expression-driven per-frame render pipeline for depth map sequences.

## Model Stack
- No diffusion models. Uses DepthAnythingV2 preprocessor model: `depth_anything_v2_vitl.pth`

## Node Table

### Group: Load / Save EXRs
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 1 | LoadExrSequence | `["Z:\\Doug\\...\\Course_Shot_2K.####.exr", 1, 24, 1, true]` |
| 2 | PreviewImage | — |
| 14 | Display Any (rgthree) | Displays EXR metadata |
| 5 | SaverNode | `["", "ComfyUI", "sequence", false, "exr"]` |

### Group: Video File Load
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 24 | VHS_LoadVideoPath | `video: "...Course_Shot_Rec709_Low_Quality.mp4", frame_load_cap: 443, skip_first_frames: 1, select_every_nth: 1` |
| 22 | VHS_VideoInfo | Extracts source metadata |
| 23 | Display Any (rgthree) | Displays source_height |
| 29 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 512]` |
| 30 | PreviewImage | — |
| 21 | VHS_VideoCombine | `frame_rate: 24, filename_prefix: "Canny", format: "video/h264-mp4", crf: 19` |

### Group: Manual Expressioned Render Method
| ID | class_type | Key Widget Values |
|----|-----------|-------------------|
| 17 | PrimitiveNode | `[28, "increment"]` |
| 20 | Primitive integer [Crystools] | `[28]` |
| 19 | MathExpression\|pysssss | `["a - 1"]` |
| 3 | VHS_LoadVideoPath | `video: "...Course_Shot_Rec709_Low_Quality.mp4", frame_load_cap: 1, skip_first_frames: 4, select_every_nth: 1` |
| 8 | VHS_VideoInfo | Extracts source metadata |
| 11 | Display Any (rgthree) | Displays source_height |
| 12 | DepthAnythingV2Preprocessor | `["depth_anything_v2_vitl.pth", 512]` |
| 13 | PreviewImage | — |
| 16 | Save Image Sequence (mtb) | `["depth_sequence_manual", 4]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|--------|-------------------|-----------------|------|
| 1 | 1.0 | 2.0 | IMAGE |
| 5 | 3.3 | 8.0 | VHS_VIDEOINFO |
| 10 | 3.0 | 12.0 | IMAGE |
| 11 | 12.0 | 13.0 | IMAGE |
| 15 | 1.6 | 14.0 | * |
| 16 | 1.0 | 5.0 | IMAGE |
| 18 | 8.4 | 11.0 | * |
| 20 | 12.0 | 16.0 | IMAGE |
| 23 | 20.0 | 19.0 | INT,FLOAT,IMAGE,LATENT |
| 24 | 19.0 | 3.7 | INT |
| 25 | 20.0 | 16.2 | INT |
| 26 | 17.0 | 20.0 | INT |
| 27 | 29.0 | 21.0 | IMAGE |
| 28 | 24.3 | 22.0 | VHS_VIDEOINFO |
| 29 | 22.4 | 23.0 | * |
| 35 | 24.0 | 29.0 | IMAGE |
| 36 | 29.0 | 30.0 | IMAGE |

## Data Flow

**EXR Pipeline:** LoadExrSequence (1) reads EXR frames 1-24 from a #### pattern path with normalization enabled. The sequence goes to PreviewImage (2) for display and SaverNode (5) for re-exporting as EXR. The metadata output feeds Display Any (14) for inspection.

**Video File Load Pipeline:** VHS_LoadVideoPath (24) loads the MP4 video (443 frames, skipping frame 1). The image output feeds DepthAnythingV2Preprocessor (29) at resolution 512. The depth output goes to VHS_VideoCombine (21) which encodes it as h264-mp4 at 24fps with CRF 19, and to PreviewImage (30). VHS_VideoInfo (22) extracts metadata from the video and passes source_height to Display Any (23).

**Manual Render Pipeline:** PrimitiveNode (17) provides an incrementing integer (starting at 28) to Primitive integer [Crystools] (20). MathExpression (19) computes `a - 1` from that value, and the result feeds VHS_LoadVideoPath (3) as skip_first_frames, loading 1 frame at a time. The single frame goes to DepthAnythingV2Preprocessor (12) at resolution 512. The depth output goes to PreviewImage (13) and Save Image Sequence (16) with prefix "depth_sequence_manual". The current_frame input of Save Image Sequence (16) comes from Primitive integer (20). VHS_VideoInfo (8) extracts metadata from the single-frame load, and source_height feeds Display Any (11).

## Invariants
- LoadExrSequence normalize must be true for proper HDR-to-LDR conversion.
- SaverNode file_type must remain "exr" and save_mode "sequence" for correct EXR output.
- VHS_VideoCombine frame_rate is 24 fps — must match source footage.
- DepthAnythingV2Preprocessor resolution is 512 in both depth pipelines.
- The manual render method uses `a - 1` math expression to convert 1-based frame number to 0-based skip count.
- PrimitiveNode uses "increment" mode for sequential frame rendering across queue runs.
- VHS_LoadVideoPath (3) frame_load_cap is 1 for single-frame processing in the manual pipeline.
