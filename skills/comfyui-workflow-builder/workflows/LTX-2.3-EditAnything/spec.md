# LTX-2.3-EditAnything

## Purpose

LTX 2.3 edit workflow for guided video/image editing with IC-LoRA, cropped guides, audio/video latent buses, and optional latent upscaling.

## Model Stack

- Main model: `LTX-2.3-distilled-Q3_K_M.gguf` via `UnetLoaderGGUF` (6040).
- LoRA: `ltx23_edit_anything_global_rank128_v1_9000steps_adamw.safetensors`, strength 1, via `LoraLoaderModelOnly` (6034).
- Text encoders: `gemma_3_12B_it_fp4_mixed.safetensors` and `ltx-2.3_text_projection_bf16.safetensors` via `DualCLIPLoader` (6041).
- Video VAE: `LTX23_video_vae_bf16.safetensors` via `VAELoaderKJ` (6042).
- Audio VAE: `LTX23_audio_vae_bf16.safetensors` via `VAELoaderKJ` (6043).
- Upscaler: `ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors` via `LatentUpscaleModelLoader` (6044).

## Node Table
| ID | class_type | Mode | Key Widget Values |
|---|---|---|---|
| 5496 | VHS_LoadVideo | 0 | `{"video":"Car Videos, Download The BEST Free 4k Stock Video Footage \u0026 Car HD Video Clips.mp4","force_rate":24,"custom_width":0,"custom_height":0,"frame_load_cap":121,"skip_first_frames":30,"select_every_nth":1,"form...` |
| 5574 | VHS_VideoInfo | 0 | `{}` |
| 5580 | GetNode (Get_audio_vae) | 0 | `"audio_vae"` |
| 5597 | SetNode (Set_positive_croped_guides) | 0 | `"positive_croped_guides"` |
| 5600 | GetNode (Get_FPS) | 0 | `"FPS"` |
| 5604 | SetNode (Set_audio_latent) | 0 | `"audio_latent"` |
| 5612 | SetNode (Set_negative_croped_guides) | 0 | `"negative_croped_guides"` |
| 5613 | SetNode (Set_result) | 0 | `"result"` |
| 5614 | GetNode (Get_video_vae) | 0 | `"video_vae"` |
| 5615 | SetNode (Set_croped_latent) | 0 | `"croped_latent"` |
| 5622 | LTXVCropGuides | 0 | `[]` |
| 5631 | SetNode (Set_FPS) | 0 | `"FPS"` |
| 5632 | SetNode (Set_video_vae) | 0 | `"video_vae"` |
| 5635 | GetNode (Get_FPS) | 0 | `"FPS"` |
| 5637 | SetNode (Set_audio_vae) | 0 | `"audio_vae"` |
| 5642 | SetNode (Set_control_video) | 0 | `"control_video"` |
| 5643 | GetNode (Get_control_video) | 0 | `"control_video"` |
| 5645 | SetNode (Set_frame_count) | 0 | `"frame_count"` |
| 5646 | SetNode (Set_loaded_duration) | 0 | `"loaded_duration"` |
| 5647 | SetNode (Set_audio) | 0 | `"audio"` |
| 5652 | GetNode (Get_frame_count) | 0 | `"frame_count"` |
| 5656 | VHS_VideoCombine | 0 | `{"frame_rate":8,"loop_count":0,"filename_prefix":"AnimateDiff","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":true,"videopreview":{"hidden...` |
| 5657 | GetNode (Get_audio) | 0 | `"audio"` |
| 5681 | GetNode (Get_video_vae) | 0 | `"video_vae"` |
| 5686 | GetNode (Get_upscale_model) | 0 | `"upscale_model"` |
| 5687 | GetNode (Get_video_vae) | 0 | `"video_vae"` |
| 5688 | GetNode (Get_croped_latent) | 0 | `"croped_latent"` |
| 5692 | GetNode (Get_audio_vae) | 0 | `"audio_vae"` |
| 5695 | GetNode (Get_audio_latent) | 0 | `"audio_latent"` |
| 5696 | GetNode (Get_positive_croped_guides) | 0 | `"positive_croped_guides"` |
| 5697 | GetNode (Get_negative_croped_guides) | 0 | `"negative_croped_guides"` |
| 5699 | GetNode (Get_result) | 0 | `"result"` |
| 5708 | SetNode (Set_upscale_model) | 0 | `"upscale_model"` |
| 5709 | SetNode (Set_models) | 0 | `"models"` |
| 5710 | GetNode (Get_models) | 0 | `"models"` |
| 5712 | GetNode (Get_FPS) | 0 | `"FPS"` |
| 5713 | GetNode (Get_audio) | 0 | `"audio"` |
| 5714 | SetNode (Set_audio_latest) | 0 | `"audio_latest"` |
| 5717 | Fast Groups Bypasser (rgthree) | 0 | `[]` |
| 5720 | VHS_VideoCombine | 0 | `{"frame_rate":8,"loop_count":0,"filename_prefix":"AnimateDiff","format":"video/h264-mp4","pix_fmt":"yuv420p","crf":19,"save_metadata":true,"trim_to_audio":false,"pingpong":false,"save_output":true,"videopreview":{"hidden...` |
| 5723 | SetNode (Set_main_video) | 0 | `"main_video"` |
| 5730 | GetNode (Get_FPS) | 0 | `"FPS"` |
| 6017 | LTXVEmptyLatentAudio | 0 | `[97,24,1]` |
| 6018 | CM_FloatToInt | 0 | `0` |
| 6019 | VAEEncode | 0 | `[]` |
| 6020 | KSamplerSelect | 0 | `"euler_ancestral_cfg_pp"` |
| 6021 | RandomNoise | 0 | `[42,"fixed"]` |
| 6023 | BasicScheduler | 0 | `["simple",8,1]` |
| 6024 | LTXVAddGuideMulti | 0 | `["1",0,1]` |
| 6026 | LTXVSeparateAVLatent | 0 | `[]` |
| 6027 | SamplerCustomAdvanced | 0 | `[]` |
| 6028 | easy cleanGpuUsed | 0 | `[]` |
| 6029 | LTXVConcatAVLatent | 0 | `[]` |
| 6030 | CFGGuider | 0 | `1` |
| 6031 | CLIPTextEncode | 0 | `""` |
| 6032 | LTXVConditioning | 0 | `24` |
| 6033 | CLIPTextEncode (Manual Prompt) | 0 | `"change the car to ferrari car with mettalic red color."` |
| 6034 | LoraLoaderModelOnly (EditAnything LoRA) | 0 | `["ltx23_edit_anything_global_rank128_v1_9000steps_adamw.safetensors",1]` |
| 6035 | easy cleanGpuUsed | 0 | `[]` |
| 6036 | easy cleanGpuUsed | 0 | `[]` |
| 6037 | easy cleanGpuUsed | 0 | `[]` |
| 6038 | easy cleanGpuUsed | 0 | `[]` |
| 6039 | easy cleanGpuUsed | 0 | `[]` |
| 6040 | UnetLoaderGGUF | 0 | `"LTX-2.3-distilled-Q3_K_M.gguf"` |
| 6041 | DualCLIPLoader | 0 | `["gemma_3_12B_it_fp4_mixed.safetensors","ltx-2.3_text_projection_bf16.safetensors","ltxv","default"]` |
| 6042 | VAELoaderKJ | 0 | `["LTX23_video_vae_bf16.safetensors","main_device","bf16"]` |
| 6043 | VAELoaderKJ | 0 | `["LTX23_audio_vae_bf16.safetensors","main_device","bf16"]` |
| 6044 | LatentUpscaleModelLoader | 0 | `"ltx-2.3-spatial-upscaler-x1.5-1.0.safetensors"` |
| 6045 | ImageScaleBy | 0 | `["lanczos",1]` |
| 6047 | LTXVPreprocess | 0 | `18` |
| 6048 | ImageResizeKJv2 | 0 | `[0,512,"nearest-exact","stretch","0, 0, 0","center",2,"cpu"]` |
| 6049 | easy int (height) | 0 | `1920` |
| 6050 | easy int (width) | 0 | `1080` |
| 6051 | easy int (duration) | 0 | `121` |
| 6053 | PrimitiveFloat (DOWNSCALE FACTOR) | 0 | `0.5` |
| 6055 | LTXVAddGuideMulti | 0 | `["1",0,1]` |
| 6056 | RandomNoise | 0 | `[42,"fixed"]` |
| 6057 | KSamplerSelect | 0 | `"euler_cfg_pp"` |
| 6058 | LTXVLatentUpsampler | 0 | `[]` |
| 6059 | ManualSigmas | 0 | `"0.85, 0.7250, 0.4219, 0.0"` |
| 6060 | CFGGuider | 0 | `1` |
| 6061 | LTXVSeparateAVLatent | 0 | `[]` |
| 6062 | GetNode (Get_video_vae) | 0 | `"video_vae"` |
| 6063 | LTXVAudioVAEDecode | 0 | `[]` |
| 6064 | SamplerCustomAdvanced | 0 | `[]` |
| 6065 | LTXVConcatAVLatent | 0 | `[]` |
| 6068 | VAEDecodeTiled | 0 | `[768,64,1024,4]` |
| 6069 | LTXVCropGuides | 0 | `[]` |
| 6070 | easy cleanGpuUsed | 0 | `[]` |
| 6072 | VAEDecode | 0 | `[]` |
| 6073 | Note (USED PROMPT) | 0 | `"ADD\n1-add red leather jacket to the woman.\n2-add sunglass to the man face.\n\nREMOVE\n1-remove the woman on the right\n\nSTYLE\n1-Convert/ transform the video style into anime style\n\nCHANGE\n1-change the black shirt...` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 13931 | 5496.3 | 5574.0 | VHS_VIDEOINFO |
| 13954 | 5622.0 | 5597.0 | CONDITIONING |
| 13968 | 5622.1 | 5612.0 | CONDITIONING |
| 13970 | 5622.2 | 5615.0 | LATENT |
| 14000 | 5574.5 | 5631.0 | FLOAT |
| 14035 | 5574.6 | 5645.0 | INT |
| 14036 | 5574.7 | 5646.0 | FLOAT |
| 14037 | 5496.2 | 5647.0 | AUDIO |
| 14057 | 5635.0 | 5656.4 | FLOAT |
| 14059 | 5657.0 | 5656.1 | AUDIO |
| 14143 | 5712.0 | 5720.4 | FLOAT |
| 14145 | 5713.0 | 5720.1 | AUDIO |
| 14146 | 5496.0 | 5723.0 | IMAGE |
| 14229 | 5580.0 | 6017.0 | VAE |
| 14230 | 5652.0 | 6017.1 | INT |
| 14231 | 6018.0 | 6017.2 | INT |
| 14232 | 5730.0 | 6018.0 | FLOAT |
| 14234 | 6017.0 | 5714.0 | LATENT |
| 14235 | 6024.0 | 6030.1 | CONDITIONING |
| 14236 | 6024.1 | 6030.2 | CONDITIONING |
| 14237 | 6019.0 | 6024.3 | LATENT |
| 14238 | 6024.2 | 6028.0 | LATENT |
| 14239 | 6021.0 | 6027.0 | NOISE |
| 14240 | 6030.0 | 6027.1 | GUIDER |
| 14241 | 6020.0 | 6027.2 | SAMPLER |
| 14242 | 6023.0 | 6027.3 | SIGMAS |
| 14243 | 6027.0 | 6026.0 | LATENT |
| 14244 | 5643.0 | 6019.0 | IMAGE |
| 14245 | 5643.0 | 6024.4 | IMAGE |
| 14252 | 6024.0 | 5622.0 | CONDITIONING |
| 14253 | 6024.1 | 5622.1 | CONDITIONING |
| 14254 | 6026.1 | 5604.0 | LATENT |
| 14255 | 6029.0 | 6027.4 | LATENT |
| 14256 | 6028.0 | 6029.0 | LATENT |
| 14257 | 6017.0 | 6029.1 | LATENT |
| 14258 | 6033.0 | 6032.0 | CONDITIONING |
| 14259 | 6031.0 | 6032.1 | CONDITIONING |
| 14262 | 5600.0 | 6032.2 | FLOAT |
| 14263 | 6032.0 | 6024.0 | CONDITIONING |
| 14264 | 6032.1 | 6024.1 | CONDITIONING |
| 14265 | 6034.0 | 6039.0 | MODEL |
| 14266 | 6039.0 | 5709.0 | * |
| 14267 | 6039.0 | 6030.0 | MODEL |
| 14268 | 6039.0 | 6023.0 | MODEL |
| 14269 | 6041.0 | 6038.0 | CLIP |
| 14270 | 6038.0 | 6031.0 | CLIP |
| 14271 | 6038.0 | 6033.0 | CLIP |
| 14272 | 6042.0 | 6037.0 | VAE |
| 14273 | 6037.0 | 5632.0 | * |
| 14274 | 6037.0 | 6019.1 | VAE |
| 14275 | 6037.0 | 6024.2 | VAE |
| 14276 | 6043.0 | 6035.0 | VAE |
| 14277 | 6035.0 | 5637.0 | * |
| 14278 | 6044.0 | 6036.0 | LATENT_UPSCALE_MODEL |
| 14279 | 6036.0 | 5708.0 | * |
| 14280 | 6040.0 | 6034.0 | MODEL |
| 14282 | 6045.0 | 6047.0 | IMAGE |
| 14286 | 5496.0 | 6048.0 | IMAGE |
| 14287 | 6048.0 | 6045.0 | IMAGE |
| 14288 | 6050.0 | 6048.2 | INT |
| 14289 | 6049.0 | 6048.3 | INT |
| 14290 | 6051.0 | 5496.2 | INT |
| 14291 | 6053.0 | 6045.1 | FLOAT |
| 14292 | 6058.0 | 6055.3 | LATENT |
| 14294 | 6055.0 | 6060.1 | CONDITIONING |
| 14295 | 6055.1 | 6060.2 | CONDITIONING |
| 14296 | 6064.0 | 6061.0 | LATENT |
| 14300 | 6061.1 | 6063.0 | LATENT |
| 14301 | 6056.0 | 6064.0 | NOISE |
| 14302 | 6060.0 | 6064.1 | GUIDER |
| 14303 | 6057.0 | 6064.2 | SAMPLER |
| 14305 | 6065.0 | 6064.4 | LATENT |
| 14306 | 6055.2 | 6065.0 | LATENT |
| 14308 | 5696.0 | 6055.0 | CONDITIONING |
| 14309 | 5697.0 | 6055.1 | CONDITIONING |
| 14310 | 5681.0 | 6055.2 | VAE |
| 14311 | 5688.0 | 6058.0 | LATENT |
| 14312 | 5686.0 | 6058.1 | LATENT_UPSCALE_MODEL |
| 14313 | 5687.0 | 6058.2 | VAE |
| 14314 | 5710.0 | 6060.0 | MODEL |
| 14315 | 5692.0 | 6063.1 | VAE |
| 14316 | 5695.0 | 6065.1 | LATENT |
| 14326 | 6026.0 | 5622.2 | LATENT |
| 14327 | 5699.0 | 6055.4 | IMAGE |
| 14329 | 5614.0 | 6068.1 | VAE |
| 14330 | 6068.0 | 5656.0 | IMAGE |
| 14331 | 5622.2 | 6068.0 | LATENT |
| 14335 | 6055.0 | 6069.0 | CONDITIONING |
| 14336 | 6055.1 | 6069.1 | CONDITIONING |
| 14337 | 6068.0 | 5613.0 | IMAGE |
| 14338 | 6064.0 | 6070.0 | LATENT |
| 14339 | 6070.0 | 6069.2 | LATENT |
| 14341 | 6059.0 | 6064.3 | SIGMAS |
| 14344 | 6070.0 | 6072.0 | LATENT |
| 14345 | 6062.0 | 6072.1 | VAE |
| 14346 | 6072.0 | 5720.0 | IMAGE |
| 14347 | 6047.0 | 5642.0 | IMAGE |

## Bus Names
| ID | Node | Bus | Purpose |
|---|---|---|---|
| 5580 | GetNode | `audio_vae` | Get_audio_vae |
| 5597 | SetNode | `positive_croped_guides` | Set_positive_croped_guides |
| 5600 | GetNode | `FPS` | Get_FPS |
| 5604 | SetNode | `audio_latent` | Set_audio_latent |
| 5612 | SetNode | `negative_croped_guides` | Set_negative_croped_guides |
| 5613 | SetNode | `result` | Set_result |
| 5614 | GetNode | `video_vae` | Get_video_vae |
| 5615 | SetNode | `croped_latent` | Set_croped_latent |
| 5631 | SetNode | `FPS` | Set_FPS |
| 5632 | SetNode | `video_vae` | Set_video_vae |
| 5635 | GetNode | `FPS` | Get_FPS |
| 5637 | SetNode | `audio_vae` | Set_audio_vae |
| 5642 | SetNode | `control_video` | Set_control_video |
| 5643 | GetNode | `control_video` | Get_control_video |
| 5645 | SetNode | `frame_count` | Set_frame_count |
| 5646 | SetNode | `loaded_duration` | Set_loaded_duration |
| 5647 | SetNode | `audio` | Set_audio |
| 5652 | GetNode | `frame_count` | Get_frame_count |
| 5657 | GetNode | `audio` | Get_audio |
| 5681 | GetNode | `video_vae` | Get_video_vae |
| 5686 | GetNode | `upscale_model` | Get_upscale_model |
| 5687 | GetNode | `video_vae` | Get_video_vae |
| 5688 | GetNode | `croped_latent` | Get_croped_latent |
| 5692 | GetNode | `audio_vae` | Get_audio_vae |
| 5695 | GetNode | `audio_latent` | Get_audio_latent |
| 5696 | GetNode | `positive_croped_guides` | Get_positive_croped_guides |
| 5697 | GetNode | `negative_croped_guides` | Get_negative_croped_guides |
| 5699 | GetNode | `result` | Get_result |
| 5708 | SetNode | `upscale_model` | Set_upscale_model |
| 5709 | SetNode | `models` | Set_models |
| 5710 | GetNode | `models` | Get_models |
| 5712 | GetNode | `FPS` | Get_FPS |
| 5713 | GetNode | `audio` | Get_audio |
| 5714 | SetNode | `audio_latest` | Set_audio_latest |
| 5723 | SetNode | `main_video` | Set_main_video |
| 5730 | GetNode | `FPS` | Get_FPS |
| 6062 | GetNode | `video_vae` | Get_video_vae |

## Data Flow

The workflow loads a source video (5496), extracts FPS/frame/audio metadata (5574), and publishes those values through Set/Get buses. The model stack loads GGUF model, edit-anything LoRA, dual CLIP, video VAE, audio VAE, and latent upscaler, then publishes reusable buses for models, VAEs, audio, frame count, and control video. The main edit lane encodes manual prompt text (6033) plus an empty negative/text lane (6031), wraps them through `LTXVConditioning` (6032), adds image/video guidance through `LTXVAddGuideMulti` (6024), and samples with `CFGGuider` (6030), `KSamplerSelect` (6020), `BasicScheduler` (6023), `RandomNoise` (6021), and `SamplerCustomAdvanced` (6027). Video and audio latents are split/rejoined through `LTXVSeparateAVLatent`, `LTXVConcatAVLatent`, and `LTXVEmptyLatentAudio`. The second-stage branch upsamples with `LTXVLatentUpsampler` (6058), adds a second guide pass (6055), samples again (6064), then decodes through `VAEDecodeTiled` (6068), `VAEDecode` (6072), `LTXVAudioVAEDecode` (6063), and video combines (5656, 5720).

## Invariants

- Preserve the named buses: `FPS`, `video_vae`, `audio_vae`, `croped_latent`, `audio_latent`, `result`, `control_video`, `main_video`, `models`, and `upscale_model`.
- Preserve downscale factor `0.5` from `PrimitiveFloat` (6053) and the 1080x1920 resize values (6050, 6049, 6048).
- Keep the two-stage guide path: first `LTXVAddGuideMulti` (6024), then upscaled/cropped guide pass through `LTXVAddGuideMulti` (6055) and `LTXVCropGuides` (6069).
- Custom LTX/KJ/easy-use nodes are opaque; copy their node definitions from the reference JSON when reconstructing exact workflows.

