# LTX-2.3-EditAnything

Purpose: LTX 2.3 edit workflow for guided video/image editing with IC-LoRA, cropped guides, audio/video latent buses, and optional latent upscaling.

## Inputs

- Source video / source clip branch: `VHS_LoadVideo` (node id 5496) and related video-info buses.
- Prompt text: `CLIPTextEncode` manual prompt (node id 6033) plus a second CLIP encode path (node id 6031) for the main text conditioning.
- Reference/control images: image input routed into `LTXVPreprocess` (node id 6047) and `ImageResizeKJv2` (node id 6048) for guide preparation.
- Timings and sizes: named buses for `FPS`, `width`, `height`, `duration`, `frame_count`, and `DOWNSCALE FACTOR`.

## Model Stack

- Main model: `UnetLoaderGGUF` (node id 6040) using `LTX-2.3-distilled-Q3_K_M.gguf`.
- LoRA: `LoraLoaderModelOnly` (node id 6034) using `ltx23_edit_anything_global_rank128_v1_9000steps_adamw.safetensors`.
- Text encoder: `DualCLIPLoader` (node id 6041) for `gemma_3_12B_it_fp4_mixed.safetensors` + `ltx-2.3_text_projection_bf16.safetensors`.
- Video VAE: `VAELoaderKJ` (node id 6042) for `LTX23_video_vae_bf16.safetensors`.
- Audio VAE: `VAELoaderKJ` (node id 6043) for `LTX23_audio_vae_bf16.safetensors`.
- Spatial upscaler: `LatentUpscaleModelLoader` (node id 6044) with `ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors`.

## Branch Graph

- Main edit branch builds conditioning with `LTXVConditioning` (node id 6032), then merges positive/negative guides with `LTXVAddGuideMulti` (node ids 6024 and 6055).
- `CFGGuider` + `SamplerCustomAdvanced` drive the latent sampling path.
- `LTXVSeparateAVLatent` / `LTXVConcatAVLatent` split and rejoin video/audio latent streams.
- `LTXVEmptyLatentAudio` creates the audio latent seed.
- `LTXVLatentUpsampler` provides an optional higher-res latent pass before the final decode branch.
- `LTXVCropGuides` trims guide conditioning for the second-stage branch.

## Outputs

- Final result bus: `Set_result` / `Get_result` (nodes 5613 / 5699).
- Main video output: `VHS_VideoCombine` (node ids 5656 and 5720) for rendered video lanes.
- Secondary decode/output: `VAEDecodeTiled` (node id 6068) and `VAEDecode` (node id 6072) for preview and final image/video inspection.
- Audio output: `LTXVAudioVAEDecode` (node id 6063).

## Invariants To Preserve

- Keep the named buses intact: `FPS`, `video_vae`, `audio_vae`, `croped_latent`, `audio_latent`, `result`, `control_video`, `main_video`.
- Preserve the LoRA name and the GGUF checkpoint pairing; the workflow is built around that edit-anything config.
- Keep the two-stage guide path: one guide pass into the main conditioning and one cropped-guide pass for the later branch.
- Preserve the downscale factor (`0.5`) used by the edit-anything guidance flow.

## Open Questions

- The workflow contains multiple parallel save/preview lanes; when reconstructing, keep the main edit lane and the upscale lane separate so the graph stays debuggable.
- Custom nodes such as `LTXVPreprocess`, `LTXVAddGuideMulti`, and `LTXVLatentUpsampler` encapsulate behavior not inferable from wiring alone, so preserve their connections exactly.
