---
name: smart-pi
description: Smart Pi orchestration workflow for using Claude Code Opus to plan, routing implementation to Pi GPT-5.5 / Claude Sonnet / Claude Opus by difficulty, then validating with Pi. Supports no-sdk-credit mode where Pi generates prompts for manual interactive Claude use instead of claude -p / Agent SDK. Use when the user asks to run /smart-pi, smart-pi, Claude/Pi collaboration, Opus planning, Sonnet execution, Pi GPT-5.5 verification, or avoiding Claude Agent SDK credits.
---

# Smart Pi

Smart Pi is a cost-aware orchestration workflow:

```text
Claude Code Opus plans → Pi routes by difficulty → Pi/Sonnet/Opus implements → Pi validates
```

Use this skill when the user asks for Smart Pi, `/smart-pi`, Opus planning with automatic Sonnet/Opus/Pi routing, Pi GPT-5.5 validation, or a no-sdk-credit workflow that avoids `claude -p` / Agent SDK usage.

For concrete no-sdk-credit usage examples, see [EXAMPLES.md](EXAMPLES.md).

## Core Rules

- Respond in Traditional Chinese unless the user asks otherwise.
- Pi is the orchestrator and final validator.
- Claude Code Opus is used by default for planning only.
- If the user asks to avoid SDK credits, no Agent SDK, `claude -p`, scripted Claude invocation, or automated prompt submission may be used; Pi must generate a prompt and wait for the user to paste back the interactive Claude result.
- Save Opus implementation for `critical` tasks only.
- Use Claude Code Sonnet for `hard` implementation tasks.
- Prefer Pi GPT-5.5 for `easy` and `medium` tasks to reduce Claude Code usage.
- Always respect dry-run / no-file-change instructions.
- Do not claim Claude/Opus was used unless the command actually succeeded.
- If Claude Code or the requested model fails, clearly report the failure and fall back to Pi planning.

## Difficulty Routing

| Difficulty | Executor | Rule |
|---|---|---|
| `easy` | `pi-gpt5.5` | Small bugfix, single-file edit, docs, low risk |
| `medium` | `pi-gpt5.5` first; `claude-sonnet` if needed | Multi-file but clear logic, ordinary feature work |
| `hard` | `claude-sonnet` | Cross-module logic, complex reasoning, high implementation uncertainty |
| `critical` | `claude-opus` | Architecture rewrite, data migration, security, core high-risk logic |

## Claude Invocation Modes

### Automated Mode (default)

Avoid passing long prompts as a single quoted CLI argument. It can be truncated by the shell or TUI bridge.

Prefer Claude Code print mode with stdin:

```bash
claude -p --model opus <<'CLAUDE_PROMPT'
PROMPT HERE
CLAUDE_PROMPT
```

For Sonnet:

```bash
claude -p --model sonnet <<'CLAUDE_PROMPT'
PROMPT HERE
CLAUDE_PROMPT
```

If using `interactive_shell`, keep the startup prompt short or write handoff instructions to a project file first. For pure headless planning, `bash` with `claude -p --model ...` and stdin is usually more reliable.

### No-SDK-Credit Mode

Use this mode when the user says they do not want to use SDK credits, Agent SDK credits, programmatic usage, `claude -p`, headless Claude, or non-interactive Claude.

Rules:

1. Do **not** invoke `claude -p`, Claude Agent SDK, GitHub Actions, scripted Claude commands, or automated prompt submission.
2. Do **not** try to spoof interactive use or automate keystrokes to bypass billing or policy boundaries.
3. Pi generates the exact planning or implementation prompt for the user.
4. Pi asks the user to manually paste that prompt into an interactive Claude experience, such as `claude` TUI or Claude web.
5. Pi waits for the user to paste Claude's JSON / handoff result back into Pi.
6. Pi then continues routing, implementation, and validation from the pasted result.

This mode trades automation for compliance and avoids consuming `claude -p` / Agent SDK credits.

## Phase 1: Opus Planning

Ask Claude Code Opus to plan only. It must not edit files during planning.

If no-sdk-credit mode is active, do not run the suggested command. Instead, print the planning prompt for the user, ask them to run interactive Claude manually, and wait for the pasted JSON result before continuing.

Planning prompt template:

```text
你是 Smart Pi 流程中的 Claude Code Opus 規劃者。
請只做規劃，不要修改任何檔案，不要寫入任何檔案。

任務：
<USER_TASK>

請輸出單一 JSON 物件，不要使用 markdown code fence，不要加前後說明文字。

JSON schema:
{
  "summary": "任務摘要",
  "difficulty": "easy | medium | hard | critical",
  "recommended_executor": "pi-gpt5.5 | claude-sonnet | claude-opus",
  "reason": "分配原因",
  "risks": ["風險 1", "風險 2"],
  "implementation_plan": ["步驟 1", "步驟 2"],
  "files_likely_to_change": ["可能修改的檔案"],
  "validation_checklist": ["驗證項目 1", "驗證項目 2"],
  "estimated_claude_usage": "low | medium | high"
}
```

Suggested command:

```bash
claude -p --model opus <<'CLAUDE_PROMPT'
你是 Smart Pi 流程中的 Claude Code Opus 規劃者。
請只做規劃，不要修改任何檔案，不要寫入任何檔案。

任務：
<USER_TASK>

請輸出單一 JSON 物件，不要使用 markdown code fence，不要加前後說明文字。

JSON schema:
{
  "summary": "任務摘要",
  "difficulty": "easy | medium | hard | critical",
  "recommended_executor": "pi-gpt5.5 | claude-sonnet | claude-opus",
  "reason": "分配原因",
  "risks": ["風險 1", "風險 2"],
  "implementation_plan": ["步驟 1", "步驟 2"],
  "files_likely_to_change": ["可能修改的檔案"],
  "validation_checklist": ["驗證項目 1", "驗證項目 2"],
  "estimated_claude_usage": "low | medium | high"
}
CLAUDE_PROMPT
```

No-sdk-credit handoff message:

```text
請手動開啟互動式 Claude Code（例如執行 `claude`，不要使用 `claude -p`）或 Claude web，貼上下方 prompt。
取得回覆後，請把完整 JSON 貼回 Pi，我會繼續做難度分流與驗證。

<PROMPT HERE>
```

After receiving the result:

1. Confirm whether it is valid JSON or at least structurally parseable.
2. Extract `difficulty`, `recommended_executor`, `implementation_plan`, and `validation_checklist`.
3. If Opus recommended an executor that conflicts with the routing table, Pi may override it, but must explain why.
4. Record whether the planning source was automated `claude -p`, manual no-sdk-credit paste-back, or Pi fallback.

## Phase 2: Executor Selection

Select one executor:

- `easy` → Pi GPT-5.5.
- `medium` → Pi GPT-5.5 unless the plan requires broader codebase edits or uncertain reasoning.
- `hard` → Claude Code Sonnet.
- `critical` → Claude Code Opus.

If user specified dry-run:

- Do not implement.
- Do not modify files.
- Only output planning, routing decision, and validation summary.

## Phase 3: Implementation

### Pi GPT-5.5 Implementation

If selected executor is Pi:

1. Read relevant files.
2. Apply minimal edits.
3. Avoid unnecessary refactors.
4. Keep changes aligned with the Opus plan.

### Claude Code Sonnet / Opus Implementation

If selected executor is Claude Code and automated mode is allowed:

Use stdin to avoid truncation:

```bash
claude -p --model sonnet <<'CLAUDE_PROMPT'
你是 Smart Pi 流程中的實作代理。
請依照下列計畫實作，完成後輸出交接摘要。

限制：
1. 嚴格遵守 implementation_plan。
2. 不要做計畫外大型重構。
3. 完成後說明修改檔案、變更摘要、剩餘風險、建議驗證方式。

計畫：
<OPUS_PLAN_JSON>
CLAUDE_PROMPT
```

For `critical`, replace `sonnet` with `opus`.

If no-sdk-credit mode is active and selected executor is Claude Code, do not invoke Claude automatically. Print a manual implementation handoff prompt and ask the user to run it in interactive Claude, then paste the handoff result back into Pi. Pi remains responsible for final validation.

Manual implementation handoff prompt:

```text
你是 Smart Pi 流程中的實作代理。
請依照下列計畫實作，完成後輸出交接摘要。

限制：
1. 嚴格遵守 implementation_plan。
2. 不要做計畫外大型重構。
3. 完成後說明修改檔案、變更摘要、剩餘風險、建議驗證方式。
4. 若無法修改檔案，請只輸出建議 patch 與原因。

計畫：
<OPUS_PLAN_JSON>
```

If the implementation should be visible to the user or interactive and automated mode is allowed, use `interactive_shell` dispatch/hands-free with a concise prompt and ask the subagent to write a handoff file such as `.pi/delegation/smart-pi-handoff.md`.

## Phase 4: Pi Validation

Always validate from Pi after implementation, regardless of executor.

Validation checklist:

1. Inspect `git diff` if the directory is a git repository.
2. Confirm changes match the Opus plan.
3. Check bugs, type errors, logic errors, security risks, and over-broad changes.
4. Run appropriate tests, lint, typecheck, or build when available.
5. If no git repository exists, state that `git diff` cannot be used and validate by file inspection / command output instead.
6. If issues are found, fix them directly or route a follow-up to the appropriate executor.

## Final Response Format

Use Traditional Chinese and keep the final report concise:

```text
Smart Pi 執行完成。

規劃摘要：...
難度：easy | medium | hard | critical
選擇的執行者：...
原因：...
修改摘要：...
驗證結果：...
剩餘風險 / 待辦：...
```

For dry-run, use:

```text
Smart Pi dry-run 完成。

Opus 規劃：成功 / 失敗（原因）
規劃來源：automated claude -p / no-sdk-credit manual paste-back / Pi fallback
難度：...
推薦執行者：...
Pi 分流決策：...
驗證摘要：已確認未進行檔案修改 / 無法使用 git diff，原因：...
```

For no-sdk-credit mode, if waiting for the user, use:

```text
Smart Pi no-sdk-credit 模式已啟動。

我不會呼叫 claude -p / Agent SDK。
請手動將下方 prompt 貼到互動式 Claude，取得 JSON 後貼回 Pi：
...
```
