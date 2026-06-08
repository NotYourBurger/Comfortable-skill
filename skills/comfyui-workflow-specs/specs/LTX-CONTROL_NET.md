# LTX-CONTROL_NET

Purpose: LTX 2.3 control-net video workflow with explicit buses for model, clip, latent scale, audio VAE, video VAE, and control-video geometry. It supports GGUF and split-asset loading, then stitches video/audio latents back together for output.

## Model Stack

- Base checkpoint / model switch: `CheckpointLoaderSimple` id 3940 and `GGUFLoaderKJ` id 5150.
- LoRAs: `LoraLoaderModelOnly` id 4922 (`ltx-2.3-22b-distilled-lora-384.safetensors | 0.5`) and IC-LoRA loader `LTXICLoRALoaderModelOnly` id 5011 (`ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors | 1`).
- Text encoders: `LTXAVTextEncoderLoader` id 5023 and `DualCLIPLoader` id 5166, with `Set_ltx_clip` id 5164 and `Get_ltx_clip` id 5167.
- Video/audio VAEs: `VAELoader` id 5151, `VAELoaderKJ` id 5153, plus bus setters `Set_ltx_video_vae` id 5085 and `Set_ltx_audio_vae` id 5083.

## Named Buses

- `ltx_model-AllLora`
- `ltx_clip`
- `ltx_latent_df`
- `ltx_video_vae`
- `ltx_audio_vae`
- `img_ref_1`
- `bypass_i2v`
- `video_controlnet`
- `cn_width`
- `cn_height`
- `cn_frames_count`
- `video_fps`
- `audio_src`

## Control and Guide Branches

- Reference image branch: `LoadImage` id 2004 -> `Set_img_ref_1` id 5096 -> `Get_img_ref_1` id 5097.
- Control video branch: `VHS_LoadVideo` id 5182 -> `LTXVPreprocess` id 3336 and the preprocessors `DepthAnythingV2Preprocessor` id 5064, `CannyEdgePreprocessor` id 4991, and `DWPreprocessor` id 4986.
- Control geometry branch: `ImageResizeKJv2` ids 5076 and 5080, `ResizeImageMaskNode` id 5028, `GetImageSize` id 5029, and the bus setters `Set_video_controlnet` id 5100, `Set_cn_width` id 5101, `Set_cn_height` id 5102, `Set_cn_frames_count` id 5103, `Set_video_fps` id 5104.
- IC-LoRA guide branch: `LTXAddVideoICLoRAGuide` id 5012 feeds `LTXVCropGuides` id 5013 and uses the latent downscale factor from `LTXICLoRALoaderModelOnly` id 5011.

## Sampling and Output

- Latent stack: `EmptyLTXVLatentVideo` id 3059, `LTXVEmptyLatentAudio` id 3980, `LTXVConcatAVLatent` id 4528, `LTXVSeparateAVLatent` id 4845.
- Sampler stack: `ManualSigmas` id 5025 -> `CFGGuider` id 4828 -> `SamplerCustomAdvanced` id 4829 with `KSamplerSelect` id 4831 and `RandomNoise` id 4832.
- Decode stack: `VAEDecodeTiled` id 4851, `LTXVAudioVAEDecode` id 4848, and `VHS_VideoCombine` ids 5069 and 5070.

## Invariants

- Keep the GGUF on/off switching logic intact (`PrimitiveBoolean` id 5158 and the `ComfySwitchNode` chain) so the workflow can swap between the distilled GGUF path and split model assets.
- Preserve the named buses, because the graph is built around Set/Get indirection rather than direct wiring.
- Keep the control-video resize sizes and frame-count buses aligned with the guide sequence.
