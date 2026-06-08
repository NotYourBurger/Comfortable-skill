# 10_Video_Cleanplates

## Purpose
Video cleanplate pipeline with four concrete lanes: roto mask prep from rendered mattes, RMBG background-removal masking, MiniMax video-inpainting removal, and ProPainter temporal-aware inpainting. Uses Set/Get bus nodes for data routing.

## Model Stack
- MiniMax: MinimaxModelLoader (auto scheduler, float16, auto device)
- RMBG: `RMBG-2.0`
- SegmentV2: `sam_vit_h (2.56GB)` + `GroundingDINO_SwinT_OGC (694MB)` (bypassed)
- ProPainter: ProPainterInpaint (bypassed)

## Node Table

### Input / Shared
| ID | class_type | Key Widget Values |
|---|---|---|
| 160 | VHS_LoadVideo | `video: "SHOT.mp4", force_rate: 24, frame_load_cap: 48` |
| 213 | VHS_VideoInfo | extracts source dimensions and loaded frame count |
| 289 | ImageResizeKJv2 | `[1024, 540, "lanczos", "stretch", "0, 0, 0", "center", 2, "cpu"]` |
| 157 | SetNode | Set_init_video |
| 195 | SetNode | Set_width |
| 194 | SetNode | Set_height |
| 294 | SetNode | Set_frame_count_load |
| 159 | SetNode | Set_num_frames |
| 303 | GetNode | Get_init_video |
| 215 | SetNode | SetNode (unused) |
| 216 | GetNode | GetNode (unused) |

### Lane A: Roto / Mask Prep
| ID | class_type | Key Widget Values |
|---|---|---|
| 331 | VHS_LoadVideo | `video: "0001-0040 (1).mp4", frame_load_cap: 48` - roto matte video |
| 336 | ImageResizeKJv2 | `[1024, 540, "lanczos", "stretch", "0, 0, 0", "center", 2, "cpu"]` |
| 332 | ImageToMask | `["red"]` - extracts mask from red channel |
| 333 | SetNode | Set_init_roto |
| 340 | VHS_LoadVideo | `video: "0001-0040 (1).mp4", frame_load_cap: 48` - second roto source |
| 341 | ImageResizeKJv2 | `[1024, 540, "lanczos", "stretch", "0, 0, 0", "center", 2, "cpu"]` |
| 342 | ImageToMask | `["red"]` |

### Lane B: Background Removal
| ID | class_type | Key Widget Values |
|---|---|---|
| 317 | RMBG | `["RMBG-2.0", 1, 1024, 0, 0, false, false, "Alpha", "#222222"]` |
| 319 | SetNode | Set_inpaint_mask |

### Lane C: MiniMax Video Removal
| ID | class_type | Key Widget Values |
|---|---|---|
| 302 | MinimaxModelLoader | `["Auto", "float16", "auto", false]` |
| 301 | MinimaxVideoRemover | `[12, 6, 982571694301738, "fixed"]` |
| 305 | ImageSizeAdjuster | `[16, "crop", 0.5, "black"]` |

### Lane D: ProPainter (bypassed, mode 4)
| ID | class_type | Key Widget Values |
|---|---|---|
| 283 | ProPainterInpaint | `[1024, 540, 5, 8, 48, 48, 48, 20, "enable"]` |
| 329 | GetNode | Get_init_video (mode 4) |
| 334 | GetNode | Get_init_roto (mode 4) |

### Segmentation (bypassed, mode 4)
| ID | class_type | Key Widget Values |
|---|---|---|
| 310 | SegmentV2 | `["humans", "sam_vit_h (2.56GB)", "GroundingDINO_SwinT_OGC (694MB)", 0.35, 0, 0, false, "Alpha", "#222222"]` |

### Output / Preview
| ID | class_type | Key Widget Values |
|---|---|---|
| 297 | VHS_VideoCombine | ProPainter output `Propainter, h264-mp4, crf 19` (mode 4) |
| 299 | VHS_VideoCombine | init_video preview GIF `AnimateDiff, gif` (mode 4) |
| 328 | VHS_VideoCombine | MiniMax output `Minimax, h264-mp4, frame_rate 25, crf 19, save_output true` |
| 330 | VHS_VideoCombine | init_video preview GIF `AnimateDiff, gif` |
| 307 | AILab_Preview | image+mask preview |

### Get Nodes (data retrieval)
| ID | class_type | Key Widget Values |
|---|---|---|
| 320 | GetNode | Get_inpaint_mask |
| 321 | GetNode | Get_inpaint_mask |
| 335 | GetNode | Get_init_roto (unused) |
| 339 | GetNode | Get_init_roto |

### Notes (informational)
| ID | class_type | Key Widget Values |
|---|---|---|
| 217 | Note | "uses this node to set a constant..." |
| 325 | Note | "ROTO" |
| 326 | Note | "BG Removal" |
| 327 | Note | "SEG2 Removal" |
| 337 | Note | "Optional Roto" |
| 338 | Note | "<- Downsizing by half for memory issues" |
| 161 | Fast Groups Bypasser (rgthree) | group bypass control |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 304 | 160.1 | 159.0 | * |
| 436 | 160.3 | 213.0 | VHS_VIDEOINFO |
| 535 | 160.0 | 289.0 | IMAGE |
| 538 | 289.0 | 157.0 | IMAGE |
| 539 | 289.1 | 195.0 | INT |
| 540 | 289.2 | 194.0 | INT |
| 545 | 213.6 | 294.0 | * |
| 550 | 283.0 | 297.0 | IMAGE |
| 553 | 305.0 | 301.0 | IMAGE |
| 555 | 302.0 | 301.2 | VAE |
| 556 | 302.1 | 301.3 | TRANSFORMER |
| 557 | 302.2 | 301.4 | SCHEDULER |
| 559 | 303.0 | 305.0 | IMAGE |
| 578 | 305.0 | 307.0 | IMAGE |
| 579 | 303.0 | 317.0 | IMAGE |
| 580 | 303.0 | 310.0 | IMAGE |
| 581 | 305.1 | 301.1 | MASK |
| 590 | 301.0 | 328.0 | IMAGE |
| 591 | 329.0 | 299.0 | IMAGE |
| 593 | 329.0 | 283.0 | IMAGE |
| 594 | 303.0 | 330.0 | IMAGE |
| 596 | 332.0 | 333.0 | * |
| 597 | 334.0 | 283.1 | MASK |
| 598 | 331.0 | 336.0 | IMAGE |
| 599 | 336.0 | 332.0 | IMAGE |
| 602 | 340.0 | 341.0 | IMAGE |
| 603 | 341.0 | 342.0 | IMAGE |
| 606 | 317.1 | 319.0 | MASK |
| 607 | 320.0 | 305.1 | MASK |
| 608 | 321.0 | 307.1 | MASK |

## Data Flow
VHS_LoadVideo (160) loads the source video at 24fps with 48-frame cap. ImageResizeKJv2 (289) downscales to 1024x540 for memory efficiency, outputs go to Set_init_video (157), Set_width (195), and Set_height (194). VHS_VideoInfo (213) extracts loaded_frame_count to Set_frame_count_load (294).

For roto prep, VHS_LoadVideo (331) loads a rendered roto matte video, ImageResizeKJv2 (336) resizes it, and ImageToMask (332) extracts the red channel as a mask stored via Set_init_roto (333). A second loader (340-341-342) handles an additional roto source.

For background removal, Get_init_video (303) feeds RMBG (317) which generates a foreground mask stored via Set_inpaint_mask (319).

For MiniMax removal, Get_init_video (303) goes to ImageSizeAdjuster (305) which crops to divisible-by-16 at 0.5 scale. Get_inpaint_mask (320) provides the adjusted mask. MinimaxModelLoader (302) provides vae, transformer, scheduler to MinimaxVideoRemover (301) which runs 12 inference steps with 6 mask dilation iterations. Output goes to VHS_VideoCombine (328) at 25fps h264-mp4.

ProPainter (283) is bypassed - when active, it takes init_video and init_roto mask at 1024x540 with settings `5|8|48|48|48|20|enable`.

## Bus Names
- `init_video` - source video frames (Set: 157, Get: 303, 329)
- `width` - source width (Set: 195)
- `height` - source height (Set: 194)
- `frame_count_load` - loaded frame count (Set: 294)
- `num_frames` - frame_count from VHS_LoadVideo (Set: 159)
- `init_roto` - roto mask from rendered matte (Set: 333, Get: 334, 335, 339)
- `inpaint_mask` - RMBG background-removal mask (Set: 319, Get: 320, 321)

## Invariants
- Source video is resized to 1024x540 via ImageResizeKJv2 with lanczos interpolation and divisible-by-2 constraint.
- ImageToMask nodes extract the red channel from roto matte videos.
- MiniMax uses 12 inference steps, 6 mask dilation iterations, and crops to divisible-by-16.
- MiniMax output saves at 25fps with h264-mp4 encoding, CRF 19.
- ProPainter preset (when enabled): width=1024, height=540, mask_dilates=5, flow_mask_dilates=8, ref_stride=48, neighbor_length=48, subvideo_length=48, raft_iter=20, fp16=enable.
- Named Set/Get buses must be preserved - the graph depends on named constants rather than direct wires.

