# Bonus_Image23d

## Purpose
Convert a 2D image into a textured 3D model using Tripo AI's image-to-model and texture APIs, with dual 3D previews showing the untextured and textured results.

## Model Stack
- Tripo AI model version: `v2.5-20250123` (via TripoImageToModelNode, node 35)
- Texture quality: `standard`, alignment: `original_image`

## Node Table
| ID | class_type | Key Widget Values |
|---|---|---|
| 56 | LoadImage | `["rainbow_dinosaur_plushy.png", "image"]` |
| 35 | TripoImageToModelNode | `["v2.5-20250123", "None", true, true, 42, "default", 42, "standard", "original_image", -1, false, <result_url>]` |
| 40 | TripoTextureNode | `[true, true, 42, "standard", "original_image", <result_url>]` |
| 51 | Preview3D | `["tripo_model_23c9b41a-2c0d-45c0-b916-0b493f996b94.glb", ""]` |
| 52 | Preview3D | `["tripo_model_b9276420-8d8a-4641-829d-4227280dec3d.glb", ""]` |

## Link Table
| LinkID | From (node.slot) | To (node.slot) | Type |
|---|---|---|---|
| 11 | 35.1 | 40.0 | MODEL_TASK_ID |
| 19 | 35.0 | 51.1 | STRING |
| 20 | 40.0 | 52.1 | STRING |
| 25 | 56.0 | 35.0 | IMAGE |

## Data Flow
LoadImage (56) loads "rainbow_dinosaur_plushy.png" and sends IMAGE to TripoImageToModelNode (35). TripoImageToModelNode (35) generates a 3D model using Tripo v2.5-20250123 with texture=true, pbr=true, model_seed=42, and outputs the model_file path (STRING) to Preview3D (51) for the initial model preview, and the MODEL_TASK_ID to TripoTextureNode (40). TripoTextureNode (40) applies additional texturing with texture=true, pbr=true, texture_seed=42, quality=standard, alignment=original_image, and outputs the textured model_file path (STRING) to Preview3D (52) for the final textured model preview.

## Invariants
- TripoImageToModelNode (35): model_version="v2.5-20250123", style="None", texture=true, pbr=true, model_seed=42, orientation="default", face_limit=-1, quad=false.
- TripoTextureNode (40): texture=true, pbr=true, texture_seed=42, texture_quality="standard", texture_alignment="original_image".
- Both Preview3D nodes require valid GLB file paths from the Tripo API results.

