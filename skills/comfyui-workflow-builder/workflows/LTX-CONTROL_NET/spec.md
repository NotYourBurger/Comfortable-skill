# LTX-CONTROL_NET

## Purpose

LTX 2.3 control-net video workflow with explicit buses for model, clip, latent scale, audio VAE, video VAE, and control-video geometry. It supports GGUF and split-asset loading, then stitches video/audio latents back together for output.

## Model Stack

- Base checkpoint path: `ltx-2.3-22b-dev.safetensors` via muted `CheckpointLoaderSimple` (3940).
- GGUF path: `ltx-2.3-22b-distilled-Q6_K.gguf` via `GGUFLoaderKJ` (5150), selected by `PrimitiveBoolean` (5158).
- LoRA path: `ltx-2.3-22b-distilled-lora-384.safetensors`, strength 0.5, via muted `LoraLoaderModelOnly` (4922).
- IC-LoRA: `ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors`, strength 1, via `LTXICLoRALoaderModelOnly` (5011).
- Text encoders: `gemma_ablit_fixed_bf16.safetensors` + `ltx-2.3-22b-dev.safetensors` via muted `LTXAVTextEncoderLoader` (5023), or `gemma_3_12B_it_fp4_mixed.safetensors` + `ltx-2.3_text_projection_bf16.safetensors` via `DualCLIPLoader` (5166).
- Video VAE: `LTX23_video_vae_bf16.safetensors`; audio VAE: `LTX23_audio_vae_bf16.safetensors`.

## Node Table
| ID | class_type | Mode | Key Widget Values |
|---|---|---|---|
| 1241 | LTXVConditioning | 0 | `24` |
| 2004 | LoadImage | 0 | `["Runcomfy_Example_1372_1.png","image"]` |
| 2483 | CLIPTextEncode (CLIP Text Encode (Positive Prompt)) | 0 | `"Girl walking , smiling "` |
| 2612 | CLIPTextEncode (CLIP Text Encode (Negative Prompt)) | 0 | `"pc game, console game, video game, cartoon, childish, ugly"` |
| 3059 | EmptyLTXVLatentVideo | 0 | `[960,544,121,1]` |
| 3159 | LTXVImgToVideoConditionOnly | 0 | `[1,false]` |
| 3336 | LTXVPreprocess | 0 | `18` |
| 3940 | CheckpointLoaderSimple | 2 | `"ltx-2.3-22b-dev.safetensors"` |
| 3980 | LTXVEmptyLatentAudio | 0 | `[97,25,1]` |
| 4010 | LTXVAudioVAELoader | 2 | `"ltx-2.3-22b-dev.safetensors"` |
| 4528 | LTXVConcatAVLatent | 0 | `[]` |
| 4828 | CFGGuider | 0 | `1` |
| 4829 | SamplerCustomAdvanced | 0 | `[]` |
| 4831 | KSamplerSelect | 0 | `"res_multistep"` |
| 4832 | RandomNoise | 0 | `[42,"fixed"]` |
| 4845 | LTXVSeparateAVLatent | 0 | `[]` |
| 4848 | LTXVAudioVAEDecode | 4 | `[]` |
| 4851 | VAEDecodeTiled | 0 | `[512,64,512,4]` |
| 4922 | LoraLoaderModelOnly | 2 | `["ltx-2.3-22b-distilled-lora-384.safetensors",0.5]` |
| 4986 | DWPreprocessor | 0 | `["enable","enable","enable",512,"yolox_l.onnx","dw-ll_ucoco_384_bs5.torchscript.pt","enable"]` |
| 4991 | CannyEdgePreprocessor | 4 | `[92,200,512]` |
| 5011 | LTXICLoRALoaderModelOnly | 0 | `["ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors",1]` |
| 5012 | LTXAddVideoICLoRAGuide | 0 | `[0,0.75,1,"disabled",false,256,64]` |
| 5013 | LTXVCropGuides | 0 | `[]` |
| 5019 | PrimitiveBoolean (bypass_i2v) | 0 | `false` |
| 5023 | LTXAVTextEncoderLoader | 2 | `["gemma_ablit_fixed_bf16.safetensors","ltx-2.3-22b-dev.safetensors","default"]` |
| 5025 | ManualSigmas | 0 | `"1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0"` |
| 5028 | ResizeImageMaskNode | 0 | `["scale to multiple",32,"lanczos"]` |
| 5029 | GetImageSize | 0 | `[]` |
| 5064 | DepthAnythingV2Preprocessor | 4 | `["depth_anything_v2_vitl.pth",512]` |
| 5065 | CR Float To Integer | 0 | `[]` |
| 5069 | VHS_VideoCombine | 0 | `{"frame_rate":8,"loop_count":0,"filename_prefix":"AnimateDiff","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":true,"videopreview":{"hidden...` |
| 5070 | VHS_VideoCombine | 0 | `{"frame_rate":8,"loop_count":0,"filename_prefix":"ltx2-3_IC Union CN","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":true,"videopreview":{...` |
| 5073 | VHS_VideoInfoLoaded | 0 | `{}` |
| 5074 | SetNode (Set_audio_src) | 0 | `"audio_src"` |
| 5075 | GetNode (Get_audio_src) | 0 | `"audio_src"` |
| 5076 | ImageResizeKJv2 | 0 | `[1280,704,"lanczos","crop","0, 0, 0","center",2,"cpu"]` |
| 5077 | SetNode (Set_width) | 0 | `"width"` |
| 5078 | SetNode (Set_height) | 0 | `"height"` |
| 5079 | PreviewImage | 0 | `[]` |
| 5080 | ImageResizeKJv2 | 0 | `[512,896,"lanczos","pad","0, 0, 0","center",2,"cpu"]` |
| 5081 | GetNode (Get_width) | 0 | `"width"` |
| 5082 | GetNode (Get_height) | 0 | `"height"` |
| 5083 | SetNode (Set_ltx_audio_vae) | 0 | `"ltx_audio_vae"` |
| 5085 | SetNode (Set_ltx_video_vae) | 0 | `"ltx_video_vae"` |
| 5086 | SetNode (Set_ltx_model-AllLora) | 0 | `"ltx_model-AllLora"` |
| 5087 | SetNode (Set_ltx_latent_df) | 0 | `"ltx_latent_df"` |
| 5088 | GetNode (Get_ltx_latent_df) | 0 | `"ltx_latent_df"` |
| 5089 | Reroute | 0 | `[]` |
| 5090 | GetNode (Get_ltx_model-AllLora) | 0 | `"ltx_model-AllLora"` |
| 5091 | GetNode (Get_ltx_latent_df) | 0 | `"ltx_latent_df"` |
| 5092 | GetNode (Get_ltx_audio_vae) | 0 | `"ltx_audio_vae"` |
| 5093 | GetNode (Get_ltx_video_vae) | 0 | `"ltx_video_vae"` |
| 5094 | GetNode (Get_ltx_video_vae) | 0 | `"ltx_video_vae"` |
| 5095 | GetNode (Get_ltx_audio_vae) | 0 | `"ltx_audio_vae"` |
| 5096 | SetNode (Set_img_ref_1) | 0 | `"img_ref_1"` |
| 5097 | GetNode (Get_img_ref_1) | 0 | `"img_ref_1"` |
| 5098 | SetNode (Set_bypass_i2v) | 0 | `"bypass_i2v"` |
| 5099 | GetNode (Get_bypass_i2v) | 0 | `"bypass_i2v"` |
| 5100 | SetNode (Set_video_controlnet) | 0 | `"video_controlnet"` |
| 5101 | SetNode (Set_cn_width) | 0 | `"cn_width"` |
| 5102 | SetNode (Set_cn_height) | 0 | `"cn_height"` |
| 5103 | SetNode (Set_cn_frames_count) | 0 | `"cn_frames_count"` |
| 5104 | SetNode (Set_video_fps) | 0 | `"video_fps"` |
| 5105 | GetNode (Get_video_fps) | 0 | `"video_fps"` |
| 5106 | GetNode (Get_video_fps) | 0 | `"video_fps"` |
| 5107 | GetNode (Get_cn_frames_count) | 0 | `"cn_frames_count"` |
| 5108 | GetNode (Get_cn_width) | 0 | `"cn_width"` |
| 5109 | GetNode (Get_cn_height) | 0 | `"cn_height"` |
| 5110 | GetNode (Get_video_fps) | 0 | `"video_fps"` |
| 5111 | GetNode (Get_video_controlnet) | 0 | `"video_controlnet"` |
| 5138 | GetImageSize | 0 | `[]` |
| 5142 | SigmasPreview | 0 | `[false,"blue"]` |
| 5146 | LTXVAudioVAEEncode | 0 | `[]` |
| 5147 | SolidMask | 0 | `[0,512,512]` |
| 5148 | SetLatentNoiseMask | 0 | `[]` |
| 5149 | ComfySwitchNode (Switch - Custom Audio?) | 0 | `false` |
| 5150 | GGUFLoaderKJ | 0 | `["ltx-2.3-22b-distilled-Q6_K.gguf","none","default","default",false,true,"none"]` |
| 5151 | VAELoader | 0 | `"LTX23_video_vae_bf16.safetensors"` |
| 5153 | VAELoaderKJ | 0 | `["LTX23_audio_vae_bf16.safetensors","main_device","bf16"]` |
| 5154 | ComfySwitchNode | 0 | `false` |
| 5155 | ComfySwitchNode | 0 | `false` |
| 5156 | ComfySwitchNode | 0 | `false` |
| 5158 | PrimitiveBoolean (Boolean - Use GGUF?) | 0 | `true` |
| 5160 | GetNode (Get_ltx_audio_vae) | 0 | `"ltx_audio_vae"` |
| 5161 | GetNode (Get_audio_src) | 0 | `"audio_src"` |
| 5162 | Note | 0 | `"LTX-2.3 Checkpoint:\nhttps://huggingface.co/Lightricks/LTX-2.3/tree/main\n\n\nSplit For GGUF :\n\nLTX 2.3 GGUF : https://huggingface.co/unsloth/LTX-2.3-GGUF/tree/main/distilled\n\nSplit Files VAE : https://huggingface.c...` |
| 5163 | ComfySwitchNode | 0 | `false` |
| 5164 | SetNode (Set_ltx_clip) | 0 | `"ltx_clip"` |
| 5166 | DualCLIPLoader | 0 | `["gemma_3_12B_it_fp4_mixed.safetensors","ltx-2.3_text_projection_bf16.safetensors","ltxv","default"]` |
| 5167 | GetNode (Get_ltx_clip) | 0 | `"ltx_clip"` |
| 5176 | MathExpression|pysssss | 0 | `"a*32"` |
| 5177 | easy showAnything | 0 | `"896"` |
| 5179 | LTXVSpatioTemporalTiledVAEDecode | 4 | `[4,4,16,1,false,"auto","auto"]` |
| 5182 | VHS_LoadVideo | 0 | `{"video":"Runcomfy_Example_1372_2.mp4","force_rate":0,"custom_width":0,"custom_height":0,"frame_load_cap":121,"skip_first_frames":0,"select_every_nth":1,"format":"LTXV","videopreview":{"hidden":false,"params":{"type":"in...` |
| 5183 | Note (Source) | 0 | `"More Tutorials: https://www.youtube.com/@BenjisAIPlayground"` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 7065 | 2483.0 | 1241.0 | CONDITIONING |
| 7652 | 2612.0 | 1241.1 | CONDITIONING |
| 9768 | 3336.0 | 3159.1 | IMAGE |
| 11002 | 2004.0 | 2653.0 | IMAGE |
| 11401 | 3059.0 | 3159.2 | LATENT |
| 13089 | 4828.0 | 4829.1 | GUIDER |
| 13090 | 4831.0 | 4829.2 | SAMPLER |
| 13093 | 4832.0 | 4829.0 | NOISE |
| 13302 | 4528.0 | 4829.4 | LATENT |
| 13363 | 4829.0 | 4845.0 | LATENT |
| 13402 | 3159.0 | 5012.3 | LATENT |
| 13403 | 1241.0 | 5012.0 | CONDITIONING |
| 13404 | 1241.1 | 5012.1 | CONDITIONING |
| 13409 | 5012.0 | 4828.1 | CONDITIONING |
| 13410 | 5012.1 | 4828.2 | CONDITIONING |
| 13411 | 4845.0 | 5013.2 | LATENT |
| 13413 | 5012.0 | 5013.0 | CONDITIONING |
| 13414 | 5012.1 | 5013.1 | CONDITIONING |
| 13444 | 5012.2 | 4528.0 | LATENT |
| 13445 | 4845.1 | 4848.0 | LATENT |
| 13479 | 5028.0 | 5029.0 | IMAGE |
| 13542 | 5065.0 | 3980.2 | INT |
| 13560 | 5073.0 | 5069.4 | FLOAT |
| 13563 | 5075.0 | 5070.1 | AUDIO |
| 13564 | 2004.0 | 5076.0 | IMAGE |
| 13570 | 5080.0 | 5064.0 | IMAGE |
| 13571 | 5080.0 | 4991.0 | IMAGE |
| 13572 | 5080.0 | 4986.0 | IMAGE |
| 13573 | 5081.0 | 5080.2 | INT |
| 13574 | 5082.0 | 5080.3 | INT |
| 13577 | 5011.0 | 5086.0 | MODEL |
| 13578 | 5011.1 | 5087.0 | FLOAT |
| 13581 | 5089.0 | 5028.0 | IMAGE |
| 13582 | 5089.0 | 5069.0 | IMAGE |
| 13583 | 5090.0 | 4828.0 | MODEL |
| 13584 | 5091.0 | 5012.5 | FLOAT |
| 13585 | 5092.0 | 3980.0 | VAE |
| 13586 | 5093.0 | 3159.0 | VAE |
| 13587 | 5093.0 | 5012.2 | VAE |
| 13589 | 5095.0 | 4848.1 | VAE |
| 13591 | 5097.0 | 3336.0 | IMAGE |
| 13592 | 5019.0 | 5098.0 | BOOLEAN |
| 13593 | 5099.0 | 3159.3 | BOOLEAN |
| 13594 | 5028.0 | 5100.0 | IMAGE |
| 13595 | 5029.0 | 5101.0 | INT |
| 13596 | 5029.1 | 5102.0 | INT |
| 13597 | 5029.2 | 5103.0 | INT |
| 13598 | 5073.0 | 5104.0 | FLOAT |
| 13599 | 5105.0 | 1241.2 | FLOAT |
| 13600 | 5106.0 | 5065.0 | FLOAT |
| 13601 | 5107.0 | 3980.1 | INT |
| 13602 | 5107.0 | 3059.2 | INT |
| 13603 | 5108.0 | 3059.0 | INT |
| 13604 | 5109.0 | 3059.1 | INT |
| 13605 | 5110.0 | 5070.4 | FLOAT |
| 13606 | 5111.0 | 5012.4 | IMAGE |
| 13644 | 5076.0 | 5079.0 | IMAGE |
| 13646 | 5138.0 | 5077.0 | INT |
| 13647 | 5138.1 | 5078.0 | INT |
| 13651 | 5025.0 | 5142.0 | SIGMAS |
| 13659 | 5146.0 | 5148.0 | LATENT |
| 13660 | 5147.0 | 5148.1 | MASK |
| 13662 | 5148.0 | 5149.1 | LATENT |
| 13667 | 3940.0 | 4922.0 | MODEL |
| 13669 | 3940.2 | 5155.0 | VAE |
| 13670 | 4010.0 | 5154.0 | VAE |
| 13671 | 5151.0 | 5155.1 | VAE |
| 13672 | 5153.0 | 5154.1 | VAE |
| 13673 | 5150.0 | 5156.1 | MODEL |
| 13674 | 4922.0 | 5156.0 | MODEL |
| 13675 | 5154.0 | 5083.0 | VAE |
| 13676 | 5155.0 | 5085.0 | VAE |
| 13677 | 5156.0 | 5011.0 | MODEL |
| 13678 | 5158.0 | 5154.2 | BOOLEAN |
| 13679 | 5158.0 | 5155.2 | BOOLEAN |
| 13680 | 5158.0 | 5156.2 | BOOLEAN |
| 13683 | 5160.0 | 5146.1 | VAE |
| 13684 | 5161.0 | 5146.0 | AUDIO |
| 13685 | 3980.0 | 5149.0 | LATENT |
| 13686 | 5149.0 | 4528.1 | LATENT |
| 13688 | 5023.0 | 5163.0 | CLIP |
| 13689 | 5158.0 | 5163.2 | BOOLEAN |
| 13690 | 5163.0 | 5164.0 | CLIP |
| 13691 | 5166.0 | 5163.1 | CLIP |
| 13692 | 5167.0 | 2483.0 | CLIP |
| 13693 | 5167.0 | 2612.0 | CLIP |
| 13695 | 5076.0 | 5096.0 | IMAGE |
| 13696 | 5076.0 | 5138.0 | IMAGE |
| 13707 | 5025.0 | 4829.3 | SIGMAS |
| 13709 | 5088.0 | 5176.0 | FLOAT |
| 13710 | 5176.0 | 5028.1 | INT |
| 13711 | 5029.0 | 5177.0 | INT |
| 13718 | 5094.0 | 4851.1 | VAE |
| 13719 | 5013.2 | 4851.0 | LATENT |
| 13720 | 4851.0 | 5070.0 | IMAGE |
| 13722 | 4986.0 | 5089.0 | IMAGE |
| 13723 | 5182.0 | 5080.0 | IMAGE |
| 13724 | 5182.2 | 5074.0 | AUDIO |
| 13725 | 5182.3 | 5073.0 | VHS_VIDEOINFO |

## Bus Names
| ID | Node | Bus | Purpose |
|---|---|---|---|
| 5074 | SetNode | `audio_src` | Set_audio_src |
| 5075 | GetNode | `audio_src` | Get_audio_src |
| 5077 | SetNode | `width` | Set_width |
| 5078 | SetNode | `height` | Set_height |
| 5081 | GetNode | `width` | Get_width |
| 5082 | GetNode | `height` | Get_height |
| 5083 | SetNode | `ltx_audio_vae` | Set_ltx_audio_vae |
| 5085 | SetNode | `ltx_video_vae` | Set_ltx_video_vae |
| 5086 | SetNode | `ltx_model-AllLora` | Set_ltx_model-AllLora |
| 5087 | SetNode | `ltx_latent_df` | Set_ltx_latent_df |
| 5088 | GetNode | `ltx_latent_df` | Get_ltx_latent_df |
| 5090 | GetNode | `ltx_model-AllLora` | Get_ltx_model-AllLora |
| 5091 | GetNode | `ltx_latent_df` | Get_ltx_latent_df |
| 5092 | GetNode | `ltx_audio_vae` | Get_ltx_audio_vae |
| 5093 | GetNode | `ltx_video_vae` | Get_ltx_video_vae |
| 5094 | GetNode | `ltx_video_vae` | Get_ltx_video_vae |
| 5095 | GetNode | `ltx_audio_vae` | Get_ltx_audio_vae |
| 5096 | SetNode | `img_ref_1` | Set_img_ref_1 |
| 5097 | GetNode | `img_ref_1` | Get_img_ref_1 |
| 5098 | SetNode | `bypass_i2v` | Set_bypass_i2v |
| 5099 | GetNode | `bypass_i2v` | Get_bypass_i2v |
| 5100 | SetNode | `video_controlnet` | Set_video_controlnet |
| 5101 | SetNode | `cn_width` | Set_cn_width |
| 5102 | SetNode | `cn_height` | Set_cn_height |
| 5103 | SetNode | `cn_frames_count` | Set_cn_frames_count |
| 5104 | SetNode | `video_fps` | Set_video_fps |
| 5105 | GetNode | `video_fps` | Get_video_fps |
| 5106 | GetNode | `video_fps` | Get_video_fps |
| 5107 | GetNode | `cn_frames_count` | Get_cn_frames_count |
| 5108 | GetNode | `cn_width` | Get_cn_width |
| 5109 | GetNode | `cn_height` | Get_cn_height |
| 5110 | GetNode | `video_fps` | Get_video_fps |
| 5111 | GetNode | `video_controlnet` | Get_video_controlnet |
| 5160 | GetNode | `ltx_audio_vae` | Get_ltx_audio_vae |
| 5161 | GetNode | `audio_src` | Get_audio_src |
| 5164 | SetNode | `ltx_clip` | Set_ltx_clip |
| 5167 | GetNode | `ltx_clip` | Get_ltx_clip |

## Data Flow

The graph loads a reference image (2004) and a control video (5182), resizes them through `ImageResizeKJv2` (5076, 5080), and publishes image, width, height, frame count, FPS, audio, and control-video buses. The model section switches between a muted checkpoint/LoRA path and the active GGUF path, applies the IC-LoRA loader, publishes the final model and latent downscale factor, and switches between text encoder options before publishing `ltx_clip`. Prompt conditioning (2483, 2612, 1241) combines with image-to-video conditioning (3159), audio/video latents (3059, 3980, 4528), and IC-LoRA guides (5012, 5013). Sampling uses `CFGGuider` (4828), `KSamplerSelect` (4831), `RandomNoise` (4832), `ManualSigmas` (5025), and `SamplerCustomAdvanced` (4829). Output splits audio/video latents (4845), optionally decodes audio (4848), decodes video with tiled VAE (4851), and renders video outputs (5069, 5070). The active preprocessor feeding the control branch is `DWPreprocessor` (4986); depth and canny preprocessors are present but muted.

## Invariants

- Preserve Set/Get bus names because most long-distance wiring depends on them: `ltx_model-AllLora`, `ltx_clip`, `ltx_latent_df`, `ltx_video_vae`, `ltx_audio_vae`, `img_ref_1`, `bypass_i2v`, `video_controlnet`, `cn_width`, `cn_height`, `cn_frames_count`, `video_fps`, and `audio_src`.
- Preserve GGUF switching logic using `PrimitiveBoolean` (5158) and `ComfySwitchNode` nodes (5154, 5155, 5156, 5163).
- Keep control-video resize geometry aligned with the buses: 1280x704 reference branch and 512x896 padded control branch.
- Custom LTX/KJ/controlnet preprocessors are extension-dependent; use the raw JSON as the authority for exact widget payloads and switch behavior.

