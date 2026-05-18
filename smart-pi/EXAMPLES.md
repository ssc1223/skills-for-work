# Smart Pi 範例

## 範例 1：no-sdk-credit dry-run 規劃

適用情境：你想使用 Opus 做規劃，但不想消耗 `claude -p` / Agent SDK credit。

### 你對 Pi 說

```text
請使用 smart-pi no-sdk-credit 模式執行以下任務。
不要使用 claude -p、Agent SDK 或任何程式化 Claude 呼叫。
這是 dry-run，請不要修改任何檔案。

任務：
幫我分析這個專案的登入流程，規劃如何加入 Google OAuth，但先不要修改檔案。
```

### Pi 會回覆

```text
Smart Pi no-sdk-credit 模式已啟動。

我不會呼叫 claude -p / Agent SDK。
請手動將下方 prompt 貼到互動式 Claude，取得 JSON 後貼回 Pi：
...
```

### 你手動執行

開啟互動式 Claude Code：

```bash
claude
```

或開啟 Claude web，然後貼上 Pi 產生的 prompt。

### 你把 Claude 回傳的 JSON 貼回 Pi

```json
{
  "summary": "分析專案登入流程並規劃加入 Google OAuth",
  "difficulty": "medium",
  "recommended_executor": "pi-gpt5.5",
  "reason": "涉及多檔案但流程清楚，可由 Pi 執行",
  "risks": [
    "OAuth callback 設定錯誤",
    "既有登入流程被破壞"
  ],
  "implementation_plan": [
    "檢查目前登入相關檔案",
    "找出 auth route 與 session 管理方式",
    "規劃 Google OAuth callback 與環境變數"
  ],
  "files_likely_to_change": [
    "src/auth/*",
    ".env.example"
  ],
  "validation_checklist": [
    "確認既有帳密登入仍可用",
    "確認 Google OAuth redirect URI 正確",
    "執行測試與 lint"
  ],
  "estimated_claude_usage": "low"
}
```

### Pi 接著輸出

```text
Smart Pi dry-run 完成。

Opus 規劃：成功
規劃來源：no-sdk-credit manual paste-back
難度：medium
推薦執行者：pi-gpt5.5
Pi 分流決策：採用 pi-gpt5.5
驗證摘要：已確認未進行檔案修改
```

## 流程摘要

```text
你要求 no-sdk-credit
→ Pi 產生 Claude prompt
→ 你手動貼到 Claude interactive / web
→ 把 JSON 貼回 Pi
→ Pi 繼續分流 / 實作 / 驗證
```
