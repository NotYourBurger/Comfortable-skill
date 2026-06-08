# 08_SAM2_Rotoscope

Purpose: Manual-plus-assisted roto workflow that uses SAM2 segmentation, Florence2 grounding, point/spline edits, and mask compositing to build rotoscoped video lanes.

## Branch A: SAM2 Segmentation / Manual Mask Work

- `DownloadAndLoadSAM2Model` ids 3, 25, and 47 load `sam2_hiera_base_plus.safetensors` and `sam2.1_hiera_base_plus.safetensors`.
- `Sam2Segmentation` ids 2, 26, and 48 are the segmentation cores.
- Video/image sources: `VHS_LoadVideoPath` ids 10, 24, 35, and 62.
- Manual guidance: `PointsEditor` id 18 and `SplineEditor` id 27.
- Mask conversion / composition: `MaskComposite` id 15, `MaskToImage` id 16, `InvertMask` id 19, `ImageAndMaskPreview` ids 29 and 31, and `MaskPreview` id 60.

## Branch B: Florence2-Assisted Grounding

- `DownloadAndLoadFlorence2Model` id 43 loads `microsoft/Florence-2-base`.
- `Florence2Run` id 44 generates grounding from the prompt.
- `Florence2toCoordinates` id 46 converts that grounding to coordinates.
- `ImageCompositeMasked` id 50, `VHS_VideoCombine` ids 51 and 52, and `PreviewImage` ids 45, 64, and 68 are used for the grounded lane output.

## Branch C: SegmentV2 / RMBG Alternative Lane

- `SegmentV2` id 67 is a separate grounding-segmentation lane using `sam_vit_h` and `GroundingDINO_SwinT_OGC`.
- `RMBG` id 63 is another isolation path, with `PreviewImage` ids 64 and 68 for inspection.
- `ImageListToImageBatch` id 65 and `VHS_VideoCombine` id 66 aggregate the resulting masks/images.

## Invariants

- Keep the SAM2 and Florence2 branches distinct; this workflow contains two example roto strategies.
- Preserve the point editor mode (`xyxy`) and canvas size (`2048x1080`) because the manual annotations are spatially coupled to the mask outputs.
