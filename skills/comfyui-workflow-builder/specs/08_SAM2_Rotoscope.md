# 08_SAM2_Rotoscope

## Purpose

Manual-plus-assisted roto workflow that uses SAM2 segmentation, Florence2 grounding, point/spline edits, and mask compositing to build rotoscoped video lanes.

## Model Stack

- SAM2 models: `sam2_hiera_base_plus.safetensors` (nodes 3, 25) and `sam2.1_hiera_base_plus.safetensors` (node 47).
- Florence2 model: `microsoft/Florence-2-base` (node 43).
- SegmentV2 models: `sam_vit_h (2.56GB)` and `GroundingDINO_SwinT_OGC (694MB)` (node 67).
- RMBG model: `BEN2` (node 63).

## Node Table
| ID | class_type | Mode | Key Widget Values |
|---|---|---|---|
| 2 | Sam2Segmentation | 0 | `[true,false]` |
| 3 | DownloadAndLoadSAM2Model | 0 | `["sam2_hiera_base_plus.safetensors","video","cuda","bf16"]` |
| 10 | VHS_LoadVideoPath | 0 | `{"video":"Z:\\Doug\\dug_co\\actionvfx\\ComfyUI_Course\\footage\\Course_Shot_Rec709_Low_Quality.mp4","force_rate":0,"custom_width":0,"custom_height":0,"frame_load_cap":30,"skip_first_frames":50,"select_every_nth":1,"forma...` |
| 11 | Note | 0 | `"1-443"` |
| 15 | MaskComposite | 0 | `[0,0,"add"]` |
| 18 | PointsEditor | 0 | `["{\"positive\":[{\"x\":1242.4026383878995,\"y\":661.4043273254997},{\"x\":1523.542459999999,\"y\":626.4883899999995},{\"x\":629.1999999999997,\"y\":822.7999999999996},{\"x\":1070.9891499999992,\"y\":776.2658199999995},{...` |
| 19 | Display Any (rgthree) | 0 | `"23.976023976023978"` |
| 20 | VHS_VideoInfo | 0 | `{}` |
| 24 | VHS_LoadVideoPath | 4 | `{"video":"Z:\\Doug\\dug_co\\actionvfx\\ComfyUI_Course\\footage\\Course_Shot_Rec709_Low_Quality.mp4","force_rate":0,"custom_width":0,"custom_height":0,"frame_load_cap":100,"skip_first_frames":50,"select_every_nth":1,"form...` |
| 25 | DownloadAndLoadSAM2Model | 4 | `["sam2_hiera_base_plus.safetensors","video","cuda","bf16"]` |
| 26 | Sam2Segmentation | 4 | `[true,false]` |
| 27 | SplineEditor | 4 | `["[{\"points\":[{\"x\":675.2304751500002,\"y\":767.4047939800001},{\"x\":1256.1430426600002,\"y\":664.5125311000002},{\"x\":1890.2555869999962,\"y\":693.7432875999987}],\"color\":\"#1f77b4\",\"name\":\"Spline 1\"}]","[[{...` |
| 28 | VHS_VideoInfo | 4 | `{}` |
| 29 | ImageAndMaskPreview | 0 | `[1,"255, 0, 0",false]` |
| 30 | Note | 4 | `"New Canvas\nright click\nLoad background image (png)"` |
| 31 | ImageAndMaskPreview | 4 | `[1,"255, 0, 0",false]` |
| 32 | VHS_VideoCombine | 0 | `{"frame_rate":8,"loop_count":0,"filename_prefix":"AnimateDiff","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":false,"videopreview":{"hidde...` |
| 35 | VHS_LoadVideoPath | 4 | `{"video":"Z:\\Doug\\dug_co\\actionvfx\\ComfyUI_Course\\footage\\Course_Shot_Rec709_Low_Quality.mp4","force_rate":0,"custom_width":0,"custom_height":0,"frame_load_cap":30,"skip_first_frames":301,"select_every_nth":1,"form...` |
| 40 | VHS_VideoInfo | 4 | `{}` |
| 42 | GetImageRangeFromBatch | 4 | `[0,30]` |
| 43 | DownloadAndLoadFlorence2Model | 4 | `["microsoft/Florence-2-base","fp16","sdpa",false]` |
| 44 | Florence2Run | 4 | `["man, weapon","caption_to_phrase_grounding",true,false,1024,3,true,"",189401254745880,"fixed"]` |
| 45 | PreviewImage | 4 | `[]` |
| 46 | Florence2toCoordinates | 4 | `["0",false]` |
| 47 | DownloadAndLoadSAM2Model | 4 | `["sam2.1_hiera_base_plus.safetensors","video","cuda","bf16"]` |
| 48 | Sam2Segmentation | 4 | `[true,false]` |
| 49 | MaskToImage | 4 | `[]` |
| 50 | ImageCompositeMasked | 4 | `[0,0,false]` |
| 51 | VHS_VideoCombine | 4 | `{"frame_rate":24,"loop_count":0,"filename_prefix":"AnimateDiff","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":false,"videopreview":{"hidd...` |
| 52 | VHS_VideoCombine | 4 | `{"frame_rate":24,"loop_count":0,"filename_prefix":"AnimateDiff","format":"image/gif","pingpong":false,"save_output":false,"videopreview":{"hidden":false,"paused":false,"params":{"filename":"AnimateDiff_00035.gif","subfol...` |
| 60 | MaskPreview | 4 | `[]` |
| 62 | VHS_LoadVideoPath | 4 | `{"video":"Z:\\Doug\\dug_co\\actionvfx\\ComfyUI_Course\\footage\\Course_Shot_Rec709_Low_Quality.mp4","force_rate":0,"custom_width":0,"custom_height":0,"frame_load_cap":30,"skip_first_frames":301,"select_every_nth":1,"form...` |
| 63 | RMBG | 4 | `["BEN2",1,1024,0,0,false,false,"Color","#00ff11"]` |
| 64 | PreviewImage | 4 | `[]` |
| 65 | ImageListToImageBatch | 4 | `[]` |
| 66 | VHS_VideoCombine | 4 | `{"frame_rate":24,"loop_count":0,"filename_prefix":"AnimateDiff","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":false,"videopreview":{"hidd...` |
| 67 | SegmentV2 | 4 | `["weapon","sam_vit_h (2.56GB)","GroundingDINO_SwinT_OGC (694MB)",0.3,0,0,false,"Alpha","#222222"]` |
| 68 | PreviewImage | 4 | `[]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 1 | 3.0 | 2.0 | SAM2MODEL |
| 22 | 10.0 | 2.1 | IMAGE |
| 24 | 2.0 | 15.0 | MASK |
| 25 | 10.0 | 18.0 | IMAGE |
| 27 | 10.3 | 20.0 | VHS_VIDEOINFO |
| 29 | 20.0 | 19.0 | * |
| 31 | 20.3 | 18.7 | INT |
| 32 | 20.4 | 18.8 | INT |
| 36 | 18.0 | 2.2 | STRING |
| 37 | 18.1 | 2.3 | STRING |
| 45 | 25.0 | 26.0 | SAM2MODEL |
| 46 | 24.0 | 26.1 | IMAGE |
| 47 | 27.1 | 26.2 | STRING |
| 48 | 24.3 | 28.0 | VHS_VIDEOINFO |
| 49 | 28.3 | 27.3 | INT |
| 50 | 28.4 | 27.4 | INT |
| 51 | 10.0 | 29.0 | IMAGE |
| 52 | 2.0 | 29.1 | MASK |
| 53 | 26.0 | 31.1 | MASK |
| 54 | 24.0 | 31.0 | IMAGE |
| 55 | 29.0 | 32.0 | IMAGE |
| 62 | 35.3 | 40.0 | VHS_VIDEOINFO |
| 65 | 35.0 | 42.0 | IMAGE |
| 66 | 42.0 | 44.0 | IMAGE |
| 67 | 43.0 | 44.1 | FL2MODEL |
| 68 | 44.0 | 45.0 | IMAGE |
| 69 | 44.3 | 46.0 | JSON |
| 70 | 47.0 | 48.0 | SAM2MODEL |
| 71 | 46.0 | 48.2 | STRING |
| 72 | 35.0 | 48.1 | IMAGE |
| 74 | 49.0 | 50.1 | IMAGE |
| 76 | 50.0 | 51.0 | IMAGE |
| 77 | 49.0 | 52.0 | IMAGE |
| 78 | 35.0 | 50.0 | IMAGE |
| 84 | 48.0 | 50.2 | MASK |
| 85 | 48.0 | 49.0 | MASK |
| 94 | 48.0 | 60.0 | MASK |
| 97 | 62.0 | 63.0 | IMAGE |
| 98 | 63.0 | 64.0 | IMAGE |
| 99 | 63.0 | 65.0 | IMAGE |
| 100 | 65.0 | 66.0 | IMAGE |
| 101 | 62.0 | 67.0 | IMAGE |
| 102 | 67.0 | 68.0 | IMAGE |

## Data Flow

The active points-editor branch loads a video clip through `VHS_LoadVideoPath` (10), extracts video info (20), and uses `PointsEditor` (18) coordinates to guide `Sam2Segmentation` (2). The mask is previewed with the source image through `ImageAndMaskPreview` (29) and rendered by `VHS_VideoCombine` (32). The spline branch repeats the same SAM2 structure with `SplineEditor` (27), `Sam2Segmentation` (26), and `ImageAndMaskPreview` (31). The Florence branch loads video frames (35), narrows them with `GetImageRangeFromBatch` (42), grounds prompt text through Florence2 (43, 44, 46), then uses SAM2 (47, 48) and mask compositing (49, 50, 51, 52, 60). The RMBG/SegmentV2 branch provides two muted alternative extraction lanes from video node 62 into `RMBG` (63) or `SegmentV2` (67).

## Invariants

- Preserve manual editor spatial values; `PointsEditor` and `SplineEditor` annotations are tied to the source frame dimensions from `VHS_VideoInfo`.
- Keep branches independent: points editor is active, spline/Florence/RMBG/SegmentV2 lanes are muted examples.
- Preserve SAM2 model pairing and Florence prompt/coordinate conversion; these custom nodes are extension-dependent.
- Reference JSON is authoritative for editor payloads because the point and spline widget values are large serialized annotation blobs.

