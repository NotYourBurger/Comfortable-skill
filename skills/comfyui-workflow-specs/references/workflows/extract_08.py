import json, sys

with open(r't:\TAHMID\Comfy-Claudia\.claude\skills\comfyui-workflow-specs\references\workflows\08_SAM2_Rotoscope.json', 'r') as f:
    data = json.load(f)

# Output nodes
with open(r't:\TAHMID\Comfy-Claudia\.claude\skills\comfyui-workflow-specs\references\workflows\08_nodes.txt', 'w') as out:
    for n in data['nodes']:
        nid = n.get('id', '')
        ntype = n.get('type', '')
        mode = n.get('mode', 0)
        title = n.get('title', '')
        wv = n.get('widgets_values', [])
        # Truncate long values
        if isinstance(wv, list):
            clean = []
            for v in wv:
                if isinstance(v, str) and len(v) > 100:
                    clean.append(v[:60] + "...")
                elif isinstance(v, dict):
                    clean.append("{...}")
                else:
                    clean.append(v)
            wv_str = str(clean)[:300]
        elif isinstance(wv, dict):
            wv_str = str(wv)[:100]
        else:
            wv_str = str(wv)
        out.write(f"ID={nid} | TYPE={ntype} | MODE={mode} | TITLE={title} | WV={wv_str}\n")

# Output links
with open(r't:\TAHMID\Comfy-Claudia\.claude\skills\comfyui-workflow-specs\references\workflows\08_links.txt', 'w') as out:
    for l in data['links']:
        out.write(f"{l[0]} | {l[1]}.{l[2]} | {l[3]}.{l[4]} | {l[5]}\n")

print("Done")
