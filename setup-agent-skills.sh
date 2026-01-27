#!/usr/bin/env bash

echo "偵測系統: $(uname -s)"

# 統一技能資料夾
UNIFIED_DIR="$HOME/agent-skills"

# 工具名稱與預設路徑陣列
TOOLS=("cursor" "antigravity" "claude" "gemini" "opencode")

# 根據 OS 指定對應路徑
for tool in "${TOOLS[@]}"; do
  if [[ "$(uname -s)" == "Darwin" || "$(uname -s)" == "Linux" ]]; then
    case "$tool" in
      cursor) TARGET_PATH="$HOME/.cursor/skills" ;;
      antigravity) TARGET_PATH="$HOME/.gemini/antigravity/skills" ;;
      claude) TARGET_PATH="$HOME/.claude/skills" ;;
      gemini) TARGET_PATH="$HOME/.gemini/skills" ;;
      opencode) TARGET_PATH="$HOME/.config/opencode/skills" ;;
    esac
  else
    # 假設是在 Git Bash / Cygwin 或 WSL
    USERPROFILE_WIN=$(cmd.exe /c "echo %USERPROFILE%" | sed -e 's/\r//')
    case "$tool" in
      cursor) TARGET_PATH="$USERPROFILE_WIN\\.cursor\\skills" ;;
      antigravity) TARGET_PATH="$USERPROFILE_WIN\\.gemini\\antigravity\\skills" ;;
      claude) TARGET_PATH="$USERPROFILE_WIN\\.claude\\skills" ;;
      gemini) TARGET_PATH="$USERPROFILE_WIN\\.gemini\\skills" ;;
      opencode) TARGET_PATH="$USERPROFILE_WIN\\.config\\opencode\\skill" ;;
    esac
  fi

  # 建立統一技能目錄
  mkdir -p "$UNIFIED_DIR"
  # 建立父目錄 & 移除舊的
  mkdir -p "$(dirname "$TARGET_PATH")"
  rm -rf "$TARGET_PATH"
  # 建 symlink
  ln -s "$UNIFIED_DIR" "$TARGET_PATH"
  echo "已設 symlink: $TARGET_PATH -> $UNIFIED_DIR"
done

echo "完成: 統一 Skills 目錄 ($UNIFIED_DIR)"