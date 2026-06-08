import json
import os
import sys

WORKFLOWS = [
    "AI-VFX-1.0",
    "AI-VFX_PREPROCESS_1-0",
    "LTX-2.3-EditAnything",
    "LTX-CONTROL_NET",
    "LTX-V2V-CANNY-DEPTH-POSE-v3",
    "LTX-V2V-DEPTH",
    "LTX-V2V-DEPTH-v2",
]

JSON_DIR = r"t:\TAHMID\Comfy-Claudia\.claude\skills\comfyui-workflow-specs\references\workflows"
OUT_DIR = r"t:\TAHMID\Comfy-Claudia\.claude\skills\comfyui-workflow-specs\references\workflows"

for name in WORKFLOWS:
    json_path = os.path.join(JSON_DIR, f"{name}.json")
    out_path = os.path.join(OUT_DIR, f"{name}_extracted.txt")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    nodes = data.get("nodes", [])
    links = data.get("links", [])
    
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f"=== WORKFLOW: {name} ===\n")
        out.write(f"Total nodes: {len(nodes)}\n")
        out.write(f"Total links: {len(links)}\n\n")
        
        # Node table
        out.write("== NODES ==\n")
        for node in sorted(nodes, key=lambda n: n.get("id", 0)):
            nid = node.get("id")
            ntype = node.get("type")
            title = node.get("title", "")
            mode = node.get("mode", 0)
            wv = node.get("widgets_values", [])
            
            # Skip Note nodes
            if ntype == "Note":
                out.write(f"  ID={nid} | type=Note (SKIP) | title={title}\n")
                continue
            
            title_str = f" (title: {title})" if title and title != ntype else ""
            mode_str = f" [MUTED]" if mode == 2 else (" [BYPASSED]" if mode == 4 else "")
            
            # Compact widgets_values
            wv_str = json.dumps(wv, ensure_ascii=False) if wv else "[]"
            if len(wv_str) > 300:
                wv_str = wv_str[:300] + "..."
            
            out.write(f"  ID={nid} | type={ntype}{title_str}{mode_str} | widgets={wv_str}\n")
        
        out.write("\n== LINKS ==\n")
        for link in links:
            # link format: [linkID, sourceNodeID, sourceSlotIndex, targetNodeID, targetSlotIndex, dataType]
            if len(link) >= 6:
                out.write(f"  {link[0]} | {link[1]}.{link[2]} -> {link[3]}.{link[4]} | {link[5]}\n")
            else:
                out.write(f"  {link}\n")
        
        # Set/Get bus names
        out.write("\n== SET/GET BUSES ==\n")
        for node in nodes:
            if node.get("type") in ("SetNode", "GetNode"):
                bus_name = ""
                wv = node.get("widgets_values", [])
                if wv and len(wv) > 0:
                    bus_name = wv[0]
                title = node.get("title", "")
                ntype = node.get("type")
                nid = node.get("id")
                
                # Get the data type from inputs/outputs
                dtype = ""
                if ntype == "SetNode":
                    inputs = node.get("inputs", [])
                    if inputs:
                        dtype = inputs[0].get("type", "*")
                else:
                    outputs = node.get("outputs", [])
                    if outputs:
                        dtype = outputs[0].get("type", "*")
                
                out.write(f"  ID={nid} | {ntype} | bus={bus_name} | datatype={dtype} | title={title}\n")
        
        # Model references - look for checkpoint/lora/controlnet loaders
        out.write("\n== MODEL REFERENCES ==\n")
        for node in nodes:
            ntype = node.get("type", "")
            nid = node.get("id")
            wv = node.get("widgets_values", [])
            lower = ntype.lower()
            if any(k in lower for k in ["loader", "checkpoint", "lora", "controlnet", "unet", "clip"]):
                wv_str = json.dumps(wv, ensure_ascii=False) if wv else "[]"
                if len(wv_str) > 500:
                    wv_str = wv_str[:500] + "..."
                out.write(f"  ID={nid} | type={ntype} | widgets={wv_str}\n")
        
        out.write("\n\n")
    
    print(f"Extracted: {name} -> {out_path}")

print("Done!")
