---
name: commit-msg-staged-zh-tw
description: Generates Git commit messages and code review comments strictly from Staged Changes (git diff --staged) using Conventional Commits prefixes (feat:, fix:, chore:, etc.) in Traditional Chinese (Taiwan). Use when the user asks to write a commit message, commit comment, PR summary, or review notes.
---

# Commit Message / Comment（僅限 Staged Changes，繁中台灣）

## 目的與硬性規則

### 僅限來源

- **只能根據 Staged Changes** 產生內容：以 `git diff --staged`（或 `git diff --cached`）為唯一依據。
- **不得**引用 Unstaged、未追蹤檔案、工作目錄變更、推測的改動、或「可能有」的內容。

### Conventional Commits 格式

- **必須**以類型前綴開頭：`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `test:`, `perf:`, `style:`, `build:`, `ci:`, `revert:`
- **標題（第一行）**：
    - **< 50 字元**（包含前綴）
    - **祈使句**（例如「新增」「修正」「更新」「移除」）
    - 聚焦 **做了什麼 / 為什麼**，避免寫「怎麼做」
- **內文（可選）**：用 1–3 行說明動機、影響面；同樣只根據 staged 內容。
- **一律使用繁體中文（台灣用語）**。

### 輸出規則（很重要）

- 產生 **git commit message** 時：**只輸出 commit message 本體**（不要加任何解釋、前後綴、或多餘文字）。
- 產生 **comment / review notes** 時：輸出簡潔條列，仍然**只能根據 staged**。

## 操作流程（給助理的固定步驟）

1. 先取得 staged 內容：
    - `git diff --staged`
    - （需要檔案清單時）`git diff --staged --name-only`
2. 用 staged 變更判斷類型前綴：
    - **feat:** 新增可被使用者/呼叫端感知的功能或行為
    - **fix:** 修 bug、修錯誤處理、修邏輯導致的不正確結果
    - **chore:** 不影響產品行為的維護（依賴、工具、雜項調整）
    - **refactor:** 重構但不改外部行為
    - **docs/test/perf/style/build/ci:** 對應領域的改動
3. 產生標題與（必要時）內文：
    - 標題要能總結 staged 變更的核心目的
    - 內文只補充「為什麼」或「影響」；避免細節清單
4. 若 staged 內容不足以確定目的：
    - **不要猜**；改輸出最保守、可被 staged 支撐的描述（通常是 `chore:` 或 `refactor:`，並用中性字眼）
5. 若完全沒有 staged changes：
    - 明確回覆「目前沒有 Staged Changes，無法產生 commit message；請先 stage 變更（git add ...）。」

## Commit message 模板

### 單行（最常用）

`<type>: <一句話摘要（繁中台灣用語，祈使句）>`

### 兩段式（需要原因/影響時）

```
<type>: <一句話摘要（繁中台灣用語，祈使句）>

<1–3 行補充：動機 / 影響範圍 / 風險或相容性（只依 staged）>
```

## Review comment 模板（基於 staged）

用精簡條列（繁中台灣用語）：

- **重點**：一句話總結這次 staged 變更目的
- **風險/注意事項**：僅指出從 staged 可直接推得的風險（例如錯誤處理、輸入驗證、回溯相容）
- **建議（可選）**：若 staged 顯示可改進處，用「建議…」描述，不要強加未證實假設

## 範例

### 範例 1（功能）

```
feat: 新增 OAuth 登入回呼的錯誤回應
```

### 範例 2（修正）

```
fix: 修正 Token 過期判斷避免誤拒

避免在邊界時間點將仍有效的 token 判定為過期。
```

### 範例 3（維護）

```
chore: 調整部署腳本以支援新環境變數
```
