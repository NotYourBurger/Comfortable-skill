# AI-VFX_PREPROCESS_1-0

## Purpose
Preprocessing workflow for AI-VFX 1.0 that takes a driving video and produces five output layers: background plate (50% grey), depth map (DepthCrafter), canny edges, DW pose estimation, camera tracking shapes, plus SAM3 segmentation masks. All outputs are saved as separate video files in the AIVFX-PREPROCESS subfolder.

## Model Stack
- DepthCrafter model: loaded via DownloadAndLoadDepthCrafterModel (3517)
- DWPose: `yolox_l.onnx` + `dw-ll_ucoco_384_bs5.torchscript.pt` via DWPreprocessor (3528)
- SAM3: loaded via SAM3Segment (3537, prompt: "person")
- CoTracker: via CoTrackerNode (3418)

## Node Table

### Decorative/Label Nodes (omitted)
Nodes 1059 (Reroute), 1064 (Reroute), 3607 (Reroute), 3610/3611/3612/3613/3615/3616 (MickmumpitzLabel), 3563 (Fast Groups Bypasser rgthree), 3617 (Note)

### Input / Settings
| ID | class_type | Key Widget Values |
|---|---|---|
| 265 | VHS_LoadVideo | `{"video": "water-shot-01.mp4", "force_rate": 0, "format": "AnimateDiff", ...}` (title: "INPUT VIDEO") |
| 2607 | VHS_VideoInfo | `{}` |
| 2845 | 3d3e41f0-5880-459f-8b57-8311a154436c | `[]` (subgraph: "SETTINGS" - outputs width, height, frame_load_cap) |

### Set/Get Bus Nodes
| ID | class_type | Key Widget Values |
|---|---|---|
| 2859 | SetNode | `["height"]` (title: "Set_height") |
| 2860 | SetNode | `["width"]` (title: "Set_width") |
| 2687 | SetNode | `["fps"]` (title: "Set_fps") |
| 3460 | SetNode | `["input-video"]` (title: "Set_input-video") |
| 3507 | SetNode | `["video_info"]` (title: "Set_video_info") |
| 3547 | SetNode | `["grey_video"]` (title: "Set_grey_video") |
| 3551 | SetNode | `["MASK"]` (title: "Set_MASK") |
| 3566 | SetNode | `["MASK_OUT"]` (title: "Set_MASK_OUT") |
| 3581 | SetNode | `["05_TRACK"]` (title: "Set_05_TRACK") |
| 3588 | SetNode | `["01_BACKGROUND"]` (title: "Set_01_BACKGROUND") |
| 3589 | SetNode | `["02_DEPTH"]` (title: "Set_02_DEPTH") |
| 3590 | SetNode | `["03_CANNY"]` (title: "Set_03_CANNY") |
| 3591 | SetNode | `["04_POSE"]` (title: "Set_04_POSE") |
| 3593 | SetNode | `["MASK_IMG"]` (title: "Set_MASK_IMG") |
| 3461 | GetNode | `["input-video"]` |
| 3465 | GetNode | `["width"]` |
| 3466 | GetNode | `["height"]` |
| 3484 | GetNode | `["input-video"]` |
| 3511 | GetNode | `["input-video"]` |
| 3519 | GetNode | `["video_info"]` |
| 3524 | GetNode | `["video_info"]` |
| 3526 | GetNode | `["video_info"]` |
| 3529 | GetNode | `["input-video"]` |
| 3530 | GetNode | `["input-video"]` |
| 3552 | GetNode | `["MASK"]` |
| 3554 | GetNode | `["video_info"]` |
| 3564 | GetNode | `["input-video"]` |
| 3567 | GetNode | `["05_TRACK"]` |
| 3584 | GetNode | `["input-video"]` |
| 3585 | GetNode | `["MASK"]` |
| 3594 | GetNode | `["MASK_IMG"]` |
| 3417 | GetNode | `["input-video"]` |

### Background Plate
| ID | class_type | Key Widget Values |
|---|---|---|
| 3463 | easy imageCount | `[]` |
| 3462 | EmptyImage | `[1280, 720, 1, 8421504]` (title: "EmptyImage 50% Grey") |

### Depth
| ID | class_type | Key Widget Values |
|---|---|---|
| 3517 | DownloadAndLoadDepthCrafterModel | `[true, false]` |
| 3518 | ImageResizeKJv2 | `[720, 720, "nearest-exact", "resize", "0, 0, 0", "center", 64, "cpu"]` |
| 3516 | DepthCrafter | `[true, 5, 1, 81, 14]` |
| 3520 | VHS_VideoInfo | `{}` |
| 3521 | ImageResizeKJv2 | `[720, 720, "nearest-exact", "resize", "0, 0, 0", "center", 2, "cpu"]` |

### Canny
| ID | class_type | Key Widget Values |
|---|---|---|
| 3604 | ImpactImageBatchToImageList | `[]` |
| 3606 | Canny | `[0.4, 0.8]` |
| 3605 | ImageListToImageBatch | `[]` |
| 3522 | VHS_VideoInfo | `{}` |
| 3523 | ImageResizeKJv2 | `[720, 720, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` |

### Pose
| ID | class_type | Key Widget Values |
|---|---|---|
| 3528 | DWPreprocessor | `["enable", "enable", "enable", 768, "yolox_l.onnx", "dw-ll_ucoco_384_bs5.torchscript.pt", "disable"]` |
| 3525 | VHS_VideoInfo | `{}` |
| 3527 | ImageResizeKJv2 | `[720, 720, "nearest-exact", "stretch", "0, 0, 0", "center", 2, "cpu"]` |

### Camera Tracking
| ID | class_type | Key Widget Values |
|---|---|---|
| 3555 | VHS_VideoInfo | `{}` |
| 3596 | GetImageRangeFromBatch | `[0, 1]` |
| 3597 | GrowMask | `[-15, true]` |
| 3418 | CoTrackerNode | `["", 50, 12, 0.04, 200, true, true]` |
| 3420 | CreateShapeImageOnPath | `["square", 1280, 720, 32, 32, "black", "black", 0.5, 1, 1, 2, "white"]` |

### Segmentation (Mask)
| ID | class_type | Key Widget Values |
|---|---|---|
| 3537 | SAM3Segment | `["person", "Merged", 0.35, 0, 0, 0, 0, "Auto", false, false, "Color", "#808080"]` |
| 3546 | InvertMask | `[]` |

### Driving Video Composite
| ID | class_type | Key Widget Values |
|---|---|---|
| 3592 | GrowMask | `[-35, true]` [BYPASSED] |
| 3586 | InvertMask | `[]` |
| 3580 | ImageCompositeMasked | `[0, 0, true]` |

### Start Image / Save Nodes
| ID | class_type | Key Widget Values |
|---|---|---|
| 3464 | ImageFromBatch | `[0, 1]` |
| 3382 | SaveImage | `["AIVFX-PREPROCESS/STARTIMG"]` |

### Video Save Nodes
| ID | class_type | Key Widget Values |
|---|---|---|
| 3509 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/BACKGROUND", "format": "video/h264-mp4", "crf": 19, "save_output": false}` |
| 3001 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/DEPTH", "format": "video/h264-mp4", "crf": 19}` |
| 3377 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/CANNY", "format": "video/h264-mp4", "crf": 19}` |
| 3378 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/POSE", "format": "video/h264-mp4", "crf": 19}` |
| 3419 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/TRACK", "format": "video/h264-mp4", "crf": 19}` |
| 3459 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/DRIVING-VIDEO", "format": "video/h264-mp4", "crf": 19}` |
| 3548 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/MASK-PLATE", "format": "video/h264-mp4", "crf": 19}` |
| 3549 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/MASK", "format": "video/h264-mp4", "crf": 19}` |
| 3595 | VHS_VideoCombine | `{"filename_prefix": "AIVFX-PREPROCESS/MASK", "format": "video/h264-mp4", "crf": 19}` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 4406 | 265.3 | 2607.0 | VHS_VIDEOINFO |
| 5219 | 2607.0 | 2687.0 | FLOAT |
| 6045 | 2845.0 | 2860.0 | INT |
| 6046 | 2845.0 | 265.2 | INT |
| 6048 | 2845.1 | 2859.0 | INT |
| 6049 | 2845.1 | 265.3 | INT |
| 6221 | 2845.2 | 265.4 | INT |
| 6331 | 3418.0 | 3420.0 | STRING |
| 6396 | 265.0 | 3460.0 | IMAGE |
| 6398 | 3461.0 | 3463.0 | IMAGE |
| 6400 | 3464.0 | 3382.0 | IMAGE |
| 6401 | 3463.0 | 3462.2 | INT |
| 6402 | 3465.0 | 3462.0 | INT |
| 6403 | 3466.0 | 3462.1 | INT |
| 6465 | 265.3 | 3507.0 | VHS_VIDEOINFO |
| 6470 | 3462.0 | 3509.0 | IMAGE |
| 6483 | 3517.0 | 3516.0 | DEPTHCRAFTER_MODEL |
| 6486 | 3511.0 | 3518.0 | IMAGE |
| 6488 | 3518.0 | 3516.1 | IMAGE |
| 6489 | 3516.0 | 3001.0 | IMAGE |
| 6490 | 3519.0 | 3520.0 | VHS_VIDEOINFO |
| 6491 | 3516.0 | 3521.0 | IMAGE |
| 6492 | 3520.8 | 3521.2 | INT |
| 6493 | 3520.9 | 3521.3 | INT |
| 6494 | 3524.0 | 3522.0 | VHS_VIDEOINFO |
| 6495 | 3522.8 | 3523.2 | INT |
| 6496 | 3522.9 | 3523.3 | INT |
| 6498 | 3523.0 | 3377.0 | IMAGE |
| 6499 | 3526.0 | 3525.0 | VHS_VIDEOINFO |
| 6500 | 3525.8 | 3527.2 | INT |
| 6501 | 3525.9 | 3527.3 | INT |
| 6503 | 3527.0 | 3378.0 | IMAGE |
| 6504 | 3530.0 | 3528.0 | IMAGE |
| 6506 | 3528.0 | 3527.0 | IMAGE |
| 6512 | 3484.0 | 3537.0 | IMAGE |
| 6544 | 3537.1 | 3546.0 | MASK |
| 6546 | 3462.0 | 3547.0 | IMAGE |
| 6548 | 3537.0 | 3548.0 | IMAGE |
| 6549 | 3537.2 | 3549.0 | IMAGE |
| 6550 | 3546.0 | 3551.0 | MASK |
| 6552 | 3417.0 | 3418.0 | IMAGE |
| 6557 | 3554.0 | 3555.0 | VHS_VIDEOINFO |
| 6558 | 3555.8 | 3420.2 | INT |
| 6559 | 3555.9 | 3420.3 | INT |
| 6577 | 3564.0 | 3464.0 | IMAGE |
| 6623 | 3420.0 | 3581.0 | IMAGE |
| 6625 | 3584.0 | 3580.1 | IMAGE |
| 6626 | 3567.0 | 3580.0 | IMAGE |
| 6627 | 3580.0 | 3459.0 | IMAGE |
| 6634 | 3462.0 | 3588.0 | IMAGE |
| 6635 | 3521.0 | 3589.0 | IMAGE |
| 6636 | 3523.0 | 3590.0 | IMAGE |
| 6637 | 3527.0 | 3591.0 | IMAGE |
| 6640 | 3537.0 | 3566.0 | IMAGE |
| 6641 | 3420.0 | 3419.0 | IMAGE |
| 6649 | 3585.0 | 3592.0 | MASK |
| 6651 | 3592.0 | 3586.0 | MASK |
| 6652 | 3586.0 | 3580.2 | MASK |
| 6653 | 3537.2 | 3593.0 | IMAGE |
| 6654 | 3594.0 | 3595.0 | IMAGE |
| 6655 | 3552.0 | 3596.1 | MASK |
| 6657 | 3596.1 | 3597.0 | MASK |
| 6658 | 3597.0 | 3418.1 | MASK |
| 6672 | 3529.0 | 3604.0 | IMAGE |
| 6673 | 3604.0 | 3606.0 | IMAGE |
| 6674 | 3606.0 | 3605.0 | IMAGE |
| 6675 | 3605.0 | 3523.0 | IMAGE |

## Data Flow
VHS_LoadVideo (265, "INPUT VIDEO") loads the source video with size/cap from subgraph 2845 ("SETTINGS"). Image frames go to SetNode (3460, Set_input-video) and video_info goes to VHS_VideoInfo (2607) for fps extraction and SetNode (3507, Set_video_info).

**Background**: GetNode (3461) gets input-video - easy imageCount (3463) counts frames - EmptyImage (3462, 50% grey, 8421504) generates a grey plate at loaded width/height - saves to BACKGROUND via VHS_VideoCombine (3509) and SetNode (3588, Set_01_BACKGROUND).

**Depth**: GetNode (3511) gets input-video - ImageResizeKJv2 (3518, 720-720, divisible_by=64) - DepthCrafter (3516) with model from (3517) - depth output saves to DEPTH via VHS_VideoCombine (3001) and is resized back to loaded dimensions via VHS_VideoInfo (3520) - ImageResizeKJv2 (3521) - SetNode (3589, Set_02_DEPTH).

**Canny**: GetNode (3529) gets input-video - ImpactImageBatchToImageList (3604) - Canny (3606, low=0.4, high=0.8) - ImageListToImageBatch (3605) - ImageResizeKJv2 (3523, loaded dimensions via VHS_VideoInfo 3522) - saves to CANNY via VHS_VideoCombine (3377) and SetNode (3590, Set_03_CANNY).

**Pose**: GetNode (3530) gets input-video - DWPreprocessor (3528) - ImageResizeKJv2 (3527, loaded dimensions via VHS_VideoInfo 3525) - saves to POSE via VHS_VideoCombine (3378) and SetNode (3591, Set_04_POSE).

**Camera Tracking**: GetNode (3417) gets input-video - CoTrackerNode (3418) with tracking_mask from GetNode (3552, MASK) - GetImageRangeFromBatch (3596) - GrowMask (3597, -15) - tracking_results string - CreateShapeImageOnPath (3420) with loaded dims from VHS_VideoInfo (3555) - saves to TRACK via VHS_VideoCombine (3419) and SetNode (3581, Set_05_TRACK).

**Segmentation**: GetNode (3484) gets input-video - SAM3Segment (3537, "person") - outputs IMAGE to MASK-PLATE (3548), MASK_IMAGE to MASK (3549) and SetNode (3593, Set_MASK_IMG), MASK to InvertMask (3546) - SetNode (3551, Set_MASK) and SetNode (3566, Set_MASK_OUT).

**Driving Video Composite**: GetNode (3567, Get_05_TRACK) as destination, GetNode (3584, Get_input-video) as source, with GrowMask (3592, -35, BYPASSED) - InvertMask (3586) - ImageCompositeMasked (3580) - saves as DRIVING-VIDEO via VHS_VideoCombine (3459).

**Start Image**: GetNode (3564) - ImageFromBatch (3464, frame 0, 1 frame) - SaveImage (3382, "AIVFX-PREPROCESS/STARTIMG").

## Bus Names
| Bus | Data Type | Set Node | Get Node(s) |
|---|---|---|---|
| width | INT/\* | 2860 | 3465 |
| height | INT/\* | 2859 | 3466 |
| fps | FLOAT | 2687 | - |
| input-video | IMAGE | 3460 | 3461, 3484, 3511, 3529, 3530, 3564, 3584, 3417 |
| video_info | VHS_VIDEOINFO | 3507 | 3519, 3524, 3526, 3554 |
| MASK | MASK | 3551 | 3552, 3585 |
| MASK_OUT | IMAGE | 3566 | - |
| MASK_IMG | IMAGE | 3593 | 3594 |
| grey_video | IMAGE | 3547 | - |
| 01_BACKGROUND | IMAGE | 3588 | - |
| 02_DEPTH | IMAGE | 3589 | - |
| 03_CANNY | IMAGE | 3590 | - |
| 04_POSE | IMAGE | 3591 | - |
| 05_TRACK | IMAGE | 3581 | 3567 |

## Invariants
- Subgraph 2845 (3d3e41f0-5880-459f-8b57-8311a154436c, "SETTINGS") provides width, height, frame_load_cap for the video loader.
- DepthCrafter input resize uses divisible_by=64; all other resize nodes use divisible_by=2.
- Canny thresholds: low=0.4, high=0.8.
- CoTracker params: grid_size=50, window_length=12, backward_tracking=true, bidirectional=true.
- SAM3Segment prompt is "person" with threshold 0.35.
- GrowMask (3592) is BYPASSED; the driving video composite uses InvertMask (3586) directly from MASK bus.
- All VHS_VideoCombine nodes output to AIVFX-PREPROCESS/ subfolder, CRF 19, h264-mp4.
- EmptyImage color value 8421504 = 50% grey.

