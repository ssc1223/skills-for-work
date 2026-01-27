#!/usr/bin/env bash

# 偵測系統
OS="$(uname -s)"
echo "偵測系統: $OS"

# 統一技能資料夾
UNIFIED_DIR="$HOME/agent-skills"

# 工具列表
TOOLS=("cursor" "antigravity" "claude" "gemini" "opencode")

# 建立統一技能資料夾
mkdir -p "$UNIFIED_DIR"

# 逐項處理
for tool in "${TOOLS[@]}"; do
  if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
    case "$tool" in
      cursor) TARGET="$HOME/.cursor/skills" ;;
      antigravity) TARGET="$HOME/.gemini/antigravity/skills" ;;
      claude) TARGET="$HOME/.claude/skills" ;;
      gemini) TARGET="$HOME/.gemini/skills" ;;
      opencode) TARGET="$HOME/.config/opencode/skills" ;;
    esac
  else
    # Windows (Git Bash/WSL)
    USERPROFILE_WIN=$(cmd.exe /c "echo %USERPROFILE%" | sed -e 's/\r//')
    case "$tool" in
      cursor) TARGET="$USERPROFILE_WIN\\.cursor\\skills" ;;
      antigravity) TARGET="$USERPROFILE_WIN\\.gemini\\antigravity\\skills" ;;
      claude) TARGET="$USERPROFILE_WIN\\.claude\\skills" ;;
      gemini) TARGET="$USERPROFILE_WIN\\.gemini\\skills" ;;
      opencode) TARGET="$USERPROFILE_WIN\\.config\\opencode\\skill" ;;
    esac
  fi

  # 如果 target 已存在
  if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
    BACKUP="${TARGET}_backup_$(date +%Y%m%d%H%M%S)"
    echo "備份原目錄: $TARGET -> $BACKUP"
    mv "$TARGET" "$BACKUP"
  fi

  # 建立父目錄
  mkdir -p "$(dirname "$TARGET")"

  # 建立 symlink
  echo "建立 symlink: $TARGET -> $UNIFIED_DIR"
  ln -s "$UNIFIED_DIR" "$TARGET"
done

echo "作業完成。統一技能目錄：$UNIFIED_DIR"