# Layout Blueprint

Reusable visual blueprint for generating clean ComfyUI graphs. Use these rules when placing nodes in workflow JSON.

## Default Lane Order (Left to Right)

1. Source / inputs (X: 0-400)
2. Model loading / adapters / LoRAs (X: 400-800)
3. Preprocessing / extraction (X: 800-1200)
4. Guidance / control / conditioning (X: 1200-1600)
5. Sampling / generation (X: 1600-2000)
6. Decode / postprocess (X: 2000-2400)
7. Preview / save outputs (X: 2400-2800)

## Concrete Position Defaults

### X Positions (Columns)
| Lane | X Start | Typical Node Width |
|---|---|---|
| Sources (LoadImage, LoadVideo) | 100 | 315 |
| Checkpoint / LoRA loaders | 500 | 315 |
| Preprocessing (resize, depth, canny) | 900 | 270-315 |
| Text encoding / ControlNet apply | 1300 | 420 |
| KSampler | 1800 | 315 |
| VAEDecode | 2200 | 210 |
| SaveImage / PreviewImage | 2500 | 210-570 |

### Y Positions (Rows)
| Branch | Y Start |
|---|---|
| Primary pipeline | 100 |
| Negative prompt branch | 400 |
| ControlNet / control branch | 700 |
| Second control branch | 1000 |
| Auxiliary (notes, previews) | 1300 |

### Spacing Rules
- Minimum horizontal gap between nodes: 80px
- Minimum vertical gap between nodes: 50px
- Gap between unrelated lanes: 150px vertical
- Do not stack loaders, samplers, previews, and save nodes on top of each other
- Use reroutes only to simplify crossings, not to hide structure

## Placement Rules

- Place source nodes in the far-left column
- Place the main generation spine (KSampler) in the center
- Place outputs in the far-right column
- Put parallel branches in separate horizontal bands
- Keep each control lane isolated until it enters the generator
- Keep model loaders together in one cluster for easy inspection and swapping
- Keep Set/Get bus nodes vertically aligned by bus name
- Put notes and labels outside the runnable lanes (top or bottom margin)

## Output Pattern

- If a workflow has one output: keep a single rightmost save lane
- If a workflow has multiple outputs: order them top to bottom by priority or by branch name
- If a workflow has comparison previews: place preview nodes near the decode lane, not inside the main generation lane

## Example: Simple Text-to-Image Layout

```
Y=100:  [CheckpointLoader @ 100,100] - [CLIPTextEncode+ @ 600,100] - [KSampler @ 1100,100] - [VAEDecode @ 1500,100] - [SaveImage @ 1800,100]
Y=350:                                  [CLIPTextEncode- @ 600,350] -
Y=550:                                  [EmptyLatentImage @ 600,550] -
```

