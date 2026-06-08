# 02_ImgGen_Elements

## Purpose
Unwired text-to-image template providing the fundamental building-block nodes (checkpoint loader, CLIP encoders, sampler, latent, VAE decoder) without connections, intended as a starting fragment for assembling new workflows.

## Model Stack
- Checkpoint: `FLUX\Schnell\flux1-schnell-fp8.safetensors`

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 6 | CheckpointLoaderSimple | `["FLUX\\Schnell\\flux1-schnell-fp8.safetensors"]` |
| 1 | CLIPTextEncode | `[""]` (titled "CLIP Text Encode (Positive Prompt)") |
| 5 | CLIPTextEncode | `[""]` (titled "CLIP Text Encode (Negative Prompt)") |
| 4 | EmptySD3LatentImage | `[1024, 1024, 1]` |
| 2 | KSampler | `[123456789, "fixed", 4, 1, "euler", "simple", 1]` |
| 3 | VAEDecode | `[]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
*(No links - this workflow is an unwired template.)*

## Data Flow
This workflow contains no links. All nodes are disconnected. When wiring: CheckpointLoaderSimple (node 6) should output MODEL to KSampler (node 2), CLIP to both CLIPTextEncode nodes (node 1 positive, node 5 negative), and VAE to VAEDecode (node 3). CLIPTextEncode nodes should output CONDITIONING to KSampler positive/negative inputs. EmptySD3LatentImage (node 4) should output LATENT to KSampler. KSampler should output LATENT to VAEDecode.

## Invariants
- Resolution: 1024x1024 (FLUX-native resolution via EmptySD3LatentImage).
- KSampler: 4 steps, CFG 1, euler sampler, simple scheduler, denoise 1, seed 123456789 fixed.
- No save/preview node present - add one downstream of VAEDecode when instantiating.
- Checkpoint is set to flux1-schnell-fp8; sampler settings (4 steps, CFG 1) are tuned for this distilled model.

