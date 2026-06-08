# 14_SAM_3.1_ROTO

## Purpose
SAM 3.1 rotoscoping workflow with two independent lanes: a still-image detection lane (mode 2 / muted) for single-frame mask generation, and a video tracking lane for propagating masks across video frames.

## Model Stack
- Checkpoint: `sam3.1_multiplex_fp16.safetensors` (node 2, CheckpointLoaderSimple)

## Node Table

### Still-Image Detection Lane (mode 2 - muted)
| ID | class_type | Key Widget Values |
|---|---|---|
| 2 | CheckpointLoaderSimple | `["sam3.1_multiplex_fp16.safetensors"]` |
| 4 | LoadImage | `["01 (1).png", "image"]` |
| 3 | CLIPTextEncode | `["a bird"]` |
| 1 | SAM3_Detect | `[0.5, 2, false]` |
| 5 | MaskPreview+ | `[]` |
| 6 | DrawBBoxes | `[]` |
| 7 | PreviewImage | `[]` |

### Video Tracking Lane (mode 0 - active)
| ID | class_type | Key Widget Values |
|---|---|---|
| 21 | VHS_LoadVideo | `{video: "SHOT.mp4", force_rate: 0, custom_width: 0, custom_height: 0, frame_load_cap: 0, skip_first_frames: 0, select_every_nth: 1, format: "AnimateDiff"}` |
| 18 | VHS_VideoInfoLoaded | `{}` |
| 15 | ImageFromBatch | `[0, 1]` |
| 14 | CLIPTextEncode | `["Phone"]` |
| 26 | PointsEditor | `[<json_points>, <positive>, <negative>, <bbox>, <bbox_mask>, "xyxy", 2560, 1440, false, "", ""]` |
| 13 | SAM3_Detect | `[0.5, 5, false]` |
| 8 | SAM3_VideoTrack | `[0.5, 1, 1]` |
| 9 | SAM3_TrackToMask | `["0,12"]` |
| 19 | InvertMask | `[]` (mode 4 - bypassed) |
| 16 | MaskToImage | `[]` |
| 10 | SAM3_TrackPreview | `[0.5, 24]` |
| 28 | PreviewImage | `[]` |
| 17 | VHS_VideoCombine | `{frame_rate: 25, loop_count: 0, filename_prefix: "RunComfy_examples_1407_video", format: "video/h264-mp4", pix_fmt: "yuv420p", crf: 19, save_output: false}` |
| 29 | VHS_VideoCombine | `{frame_rate: 25, loop_count: 0, filename_prefix: "AnimateDiff", format: "video/h264-mp4", pix_fmt: "yuv420p", crf: 19, save_output: true}` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 1 | 2.0 | 1.0 | MODEL |
| 2 | 3.0 | 1.2 | CONDITIONING |
| 3 | 2.1 | 3.0 | CLIP |
| 5 | 1.0 | 5.0 | MASK |
| 6 | 1.1 | 6.0 | BOUNDING_BOX |
| 7 | 6.0 | 7.0 | IMAGE |
| 10 | 2.0 | 8.1 | MODEL |
| 11 | 13.0 | 8.2 | MASK |
| 12 | 14.0 | 13.2 | CONDITIONING |
| 13 | 14.0 | 8.3 | CONDITIONING |
| 15 | 15.0 | 13.1 | IMAGE |
| 16 | 2.0 | 13.0 | MODEL |
| 17 | 2.1 | 14.0 | CLIP |
| 18 | 8.0 | 9.0 | SAM3_TRACK_DATA |
| 19 | 8.0 | 10.0 | SAM3_TRACK_DATA |
| 22 | 16.0 | 17.0 | IMAGE |
| 24 | 18.0 | 10.2 | FLOAT |
| 26 | 9.0 | 19.0 | MASK |
| 27 | 19.0 | 16.0 | MASK |
| 30 | 4.0 | 1.1 | IMAGE |
| 31 | 4.0 | 6.1 | IMAGE |
| 32 | 21.0 | 15.0 | IMAGE |
| 33 | 21.3 | 18.0 | VHS_VIDEOINFO |
| 34 | 21.0 | 10.1 | IMAGE |
| 35 | 21.0 | 8.0 | IMAGE |
| 36 | 26.0 | 13.4 | STRING |
| 37 | 26.1 | 13.5 | STRING |
| 38 | 21.0 | 26.0 | IMAGE |
| 40 | 16.0 | 28.0 | IMAGE |
| 41 | 16.0 | 29.0 | IMAGE |

## Data Flow
**Still-Image Lane (muted):** LoadImage (4) sends its IMAGE to SAM3_Detect (1) and DrawBBoxes (6). CheckpointLoaderSimple (2) provides MODEL to SAM3_Detect (1) and CLIP to CLIPTextEncode (3), which sends CONDITIONING to SAM3_Detect (1). SAM3_Detect (1) outputs masks to MaskPreview+ (5) and bounding boxes to DrawBBoxes (6), which outputs to PreviewImage (7).

**Video Tracking Lane (active):** VHS_LoadVideo (21) provides IMAGE frames to ImageFromBatch (15), SAM3_VideoTrack (8), SAM3_TrackPreview (10), and PointsEditor (26). VHS_LoadVideo (21) also sends VHS_VIDEOINFO to VHS_VideoInfoLoaded (18), which extracts fps for SAM3_TrackPreview (10). CheckpointLoaderSimple (2) provides MODEL to SAM3_Detect (13) and SAM3_VideoTrack (8), and CLIP to CLIPTextEncode (14). ImageFromBatch (15) extracts frame 0 for SAM3_Detect (13). PointsEditor (26) provides positive_coords and negative_coords to SAM3_Detect (13). CLIPTextEncode (14) sends CONDITIONING to SAM3_Detect (13) and SAM3_VideoTrack (8). SAM3_Detect (13) produces an initial mask for SAM3_VideoTrack (8). SAM3_VideoTrack (8) outputs SAM3_TRACK_DATA to SAM3_TrackToMask (9) and SAM3_TrackPreview (10). SAM3_TrackToMask (9) converts tracks "0,12" to masks, then InvertMask (19, bypassed) passes to MaskToImage (16). MaskToImage (16) sends IMAGE to VHS_VideoCombine (17), PreviewImage (28), and VHS_VideoCombine (29).

## Invariants
- Keep the SAM3 model file `sam3.1_multiplex_fp16.safetensors` and the two separate lanes; the still-image lane is muted (mode 2) and serves as a reference example.
- Preserve PointsEditor (26) coordinate space: 2560x1440, format "xyxy".
- SAM3_Detect (1) threshold=0.5, max_detections=2; SAM3_Detect (13) threshold=0.5, max_detections=5.
- SAM3_VideoTrack (8) threshold=0.5, max_objects=1, max_frames=1.
- SAM3_TrackToMask (9) object_ids="0,12".
- VHS_VideoCombine output settings: frame_rate=25, crf=19, format=video/h264-mp4.

