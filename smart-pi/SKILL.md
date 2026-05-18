---
name: smart-pi
description: Smart Pi orchestration workflow for using Claude Code Opus to plan, routing implementation to Pi GPT-5.5 / Claude Sonnet / Claude Opus by difficulty, then validating with Pi. Use when the user asks to run /smart-pi, smart-pi, Claude/Pi collaboration, Opus planning, Sonnet execution, or Pi GPT-5.5 verification.
---

# Smart Pi

Smart Pi is a cost-aware orchestration workflow:

```text
Claude Code Opus plans → Pi routes by difficulty → Pi/Sonnet/Opus implements → Pi validates
```

Use this skill when the user asks for Smart Pi, `/smart-pi`, Opus planning with automatic Sonnet/Opus/Pi routing, or Pi GPT-5.5 validation.

## Core Rules

- Respond in Traditional Chinese unless the user asks otherwise.
- Pi is the orchestrator and final validator.
- Claude Code Opus is used by default for planning only.
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

## Robust Claude Code Invocation

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

## Phase 1: Opus Planning

Ask Claude Code Opus to plan only. It must not edit files during planning.

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

After receiving the result:

1. Confirm whether it is valid JSON or at least structurally parseable.
2. Extract `difficulty`, `recommended_executor`, `implementation_plan`, and `validation_checklist`.
3. If Opus recommended an executor that conflicts with the routing table, Pi may override it, but must explain why.

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

If selected executor is Claude Code:

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

If the implementation should be visible to the user or interactive, use `interactive_shell` dispatch/hands-free with a concise prompt and ask the subagent to write a handoff file such as `.pi/delegation/smart-pi-handoff.md`.

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
難度：...
推薦執行者：...
Pi 分流決策：...
驗證摘要：已確認未進行檔案修改 / 無法使用 git diff，原因：...
```
