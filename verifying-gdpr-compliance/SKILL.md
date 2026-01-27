---
name: verifying-gdpr-compliance
description: 驗證專案是否符合 GDPR 規範。當用戶要求檢查 GDPR 合規性、隱私權政策或資料保護措施時使用。
---
# 驗證 GDPR 合規性 (Verifying GDPR Compliance)

## 何時使用此技能
- 當用戶要求檢查專案是否符合 GDPR (一般資料保護規則) 時
- 當用戶詢問隱私權政策、Cookie 同意或資料保護措施時
- 需要進行隱私權審計 (Privacy Audit) 時

## 工作流程
1. **關鍵字掃描**:
   執行 `scripts/scan_gdpr_keywords.py` 腳本，快速掃描專案中是否存在 GDPR 相關的實作跡象（如條款、同意機制、刪除資料的函數）。
   ```bash
   python3 .agent/skills/verifying-gdpr-compliance/scripts/scan_gdpr_keywords.py
   ```

2. **人工審查對照**:
   參考 `resources/gdpr_checklist.md` 中的檢查清單，根據掃描結果與實際程式碼邏輯，逐項確認合規性。特別注意：
   - 是否有清晰的隱私權政策頁面
   - 是否有 Cookie 同意橫幅 (Consent Banner)
   - 用戶能否匯出個人資料 (Data Portability)
   - 用戶能否刪除帳號 (Right to Erasure)

3. **提供改善建議與實作範例**:
   對於缺少的項目，使用 `examples/implementation_guide.md` 中的範例程式碼與文件模板，提供具體的改善方向。
   - 不要只說「缺了這個」，要給出「可以這樣加：...」

## 指令
- 在回報時，請明確列出：
  - ✅ 已符合的項目 (及證據)
  - ❌ 缺失的項目
  - ⚠️ 建議改進的項目
- 針對缺失項目，主動提供實作程式碼片段（參考 examples）。

## 資源
- [GDPR 檢查清單](resources/gdpr_checklist.md)
- [實作範例與指南](examples/implementation_guide.md)
