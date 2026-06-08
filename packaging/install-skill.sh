#!/usr/bin/env bash
set -euo pipefail

skill_name="comfyui-workflow-builder"
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/$skill_name"

if [[ ! -d "$source_dir" ]]; then
  echo "Skill source not found: $source_dir" >&2
  exit 1
fi

target="${1:-}"
case "$target" in
  codex)
    base="${CODEX_HOME:-$HOME/.codex}"
    target_dir="$base/skills"
    ;;
  claude)
    target_dir="$HOME/.claude/skills"
    ;;
  "")
    echo "Usage: $0 codex|claude|/path/to/skills" >&2
    exit 1
    ;;
  *)
    target_dir="$target"
    ;;
esac

mkdir -p "$target_dir"
rm -rf "$target_dir/$skill_name"
cp -R "$source_dir" "$target_dir/$skill_name"
echo "Installed $skill_name to $target_dir/$skill_name"
