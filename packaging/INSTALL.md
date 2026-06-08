# ComfyUI Workflow Builder Packaging

This repository packages `skills/comfyui-workflow-builder` as a portable agent skill.

## Package Contents

- `skills/comfyui-workflow-builder/SKILL.md` - canonical skill entrypoint.
- `skills/comfyui-workflow-builder/specs/` - compact workflow specs, format reference, node catalog, and layout rules.
- `skills/comfyui-workflow-builder/references/workflows/` - raw ComfyUI workflow JSON references.
- `skills/comfyui-workflow-builder/agents/openai.yaml` - optional UI metadata for Codex/OpenAI-style skill lists.

## Install Targets

Use the same skill folder for every agent. The folder name must remain:

```text
comfyui-workflow-builder
```

Recommended global locations:

| Tool | Global Skill Location |
|---|---|
| Codex / OpenAI-style skills | `%USERPROFILE%\.codex\skills\comfyui-workflow-builder` or `$HOME/.codex/skills/comfyui-workflow-builder` |
| Claude Code-style skills | `%USERPROFILE%\.claude\skills\comfyui-workflow-builder` or `$HOME/.claude/skills/comfyui-workflow-builder` |
| Generic agentic coding tools | Any configured global skills directory, or a project-local `.agents/skills/comfyui-workflow-builder` |
| Gemini CLI-style project memory | Copy the skill folder anywhere stable and reference it from `GEMINI.md` using the adapter in `packaging/adapters/GEMINI.md` |

## Windows Install

Install globally for Codex:

```powershell
.\packaging\install-skill.ps1 -Target codex
```

Install globally for Claude-style skill directories:

```powershell
.\packaging\install-skill.ps1 -Target claude
```

Install to a custom directory:

```powershell
.\packaging\install-skill.ps1 -TargetDir "C:\path\to\skills"
```

## macOS / Linux Install

Install globally for Codex:

```bash
./packaging/install-skill.sh codex
```

Install globally for Claude-style skill directories:

```bash
./packaging/install-skill.sh claude
```

Install to a custom directory:

```bash
./packaging/install-skill.sh /path/to/skills
```

## Adapter Files

Some agents do not have a native skill loader. Use an adapter file in the relevant project/global instruction file:

- `packaging/adapters/AGENTS.md`
- `packaging/adapters/CLAUDE.md`
- `packaging/adapters/GEMINI.md`

Each adapter tells the agent to load `SKILL.md` first, then use specs and raw workflow JSONs progressively.

## Build Archives

From the repository root:

```powershell
.\packaging\make-package.ps1
```

Outputs:

- `dist/comfyui-workflow-builder.zip`
- `dist/comfyui-workflow-builder.tar.gz`

