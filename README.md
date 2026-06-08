# ComfyUI Workflow Builder — Claude Skill

Builds valid ComfyUI workflow JSON from natural language requirements, reference specs, or existing workflow files. Works with Claude Code and any Claude agent that supports project-level `CLAUDE.md` instructions.

---

## Install for Claude Code

### Option A — Global install (recommended)

Installs the skill into your user-level Claude skills directory so it is available in every project.

**Windows (PowerShell):**
```powershell
.\packaging\install-skill.ps1 -Target claude
```

This copies `skills/comfyui-workflow-builder/` to `%USERPROFILE%\.claude\skills\comfyui-workflow-builder\`.

**macOS / Linux:**
```bash
./packaging/install-skill.sh claude
```

This copies `skills/comfyui-workflow-builder/` to `~/.claude/skills/comfyui-workflow-builder/`.

---

### Option B — Project-local install

Copy the skill folder into the `.claude/skills/` directory of the project where you want to use it:

```powershell
# Windows
Copy-Item -Recurse skills\comfyui-workflow-builder .claude\skills\comfyui-workflow-builder
```

```bash
# macOS / Linux
cp -r skills/comfyui-workflow-builder .claude/skills/comfyui-workflow-builder
```

---

### Option C — Work directly in this repo

This repo already contains a `CLAUDE.md` at the root. Open the repo folder in Claude Code and the skill instructions are loaded automatically — no copy needed.

```bash
cd /path/to/Comfortable-skill
claude   # or open in VS Code / JetBrains with Claude Code extension
```

---

### Option D — Manual (zip / download)

1. Download `dist/comfyui-workflow-builder.zip` (or `.tar.gz`).
2. Extract the archive — you get a folder named `comfyui-workflow-builder/`.
3. Move that folder to either:
   - **Global:** `~/.claude/skills/comfyui-workflow-builder/` (or `%USERPROFILE%\.claude\skills\` on Windows)
   - **Project-local:** `<your-project>/.claude/skills/comfyui-workflow-builder/`

---

## Activating the Skill in Claude Code

After installing, tell Claude to use the skill in one of two ways:

**In-conversation trigger (works anywhere):**
> "Use the comfyui-workflow-builder skill to build a FLUX Schnell text-to-image workflow."

**Persistent project activation** — add to your project's `.claude/CLAUDE.md` (or `CLAUDE.md`):
```markdown
Use skills/comfyui-workflow-builder/SKILL.md whenever the user asks to build, modify, or inspect ComfyUI workflow JSON.
```

---

## What the Skill Does

- Generates valid ComfyUI workflow JSON from a plain-language description
- Modifies existing workflows (add LoRA, swap model, insert ControlNet, etc.)
- Explains how a workflow is structured
- Validates a workflow against the ComfyUI format spec

## Skill Contents

| Path | Purpose |
|---|---|
| `skills/comfyui-workflow-builder/SKILL.md` | Skill entrypoint — process, validation checklist, layout rules |
| `skills/comfyui-workflow-builder/specs/` | Compact specs per workflow type; format reference; node catalog |
| `skills/comfyui-workflow-builder/references/workflows/` | Raw ComfyUI JSON files — definitive wiring source |
| `CLAUDE.md` | Root-level Claude Code project instruction (auto-loaded when this repo is open) |

## Reference Priority

When Claude needs exact details it reads in this order:

1. Matching spec in `specs/*.md` — fast lookup for node types, model names, wiring
2. Raw JSON in `references/workflows/` — exact node definitions and link IDs
3. `specs/NODE_CATALOG.md` — slot order and `widgets_values` format for any node
4. `specs/COMFYUI_FORMAT.md` — top-level JSON schema

## Rebuild the Distribution Archives

```powershell
.\packaging\make-package.ps1
```

Outputs `dist/comfyui-workflow-builder.zip` and `dist/comfyui-workflow-builder.tar.gz`.
