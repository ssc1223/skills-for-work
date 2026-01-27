# GDPR 合規性檢查清單 (GDPR Checklist)

使用此清單確認專案是否符合 GDPR 的關鍵要求。

## 1. 合法性、公平性與透明度 (Lawfulness, Fairness, and Transparency)
- [ ] **隱私權政策 (Privacy Policy)**: 是否有公開且易於理解的隱私權政策連結？
- [ ] **透明度**: 政策是否清楚說明收集了什麼資料、為什麼收集、保留多久以及與誰共享？
- [ ] **身分驗證**: 網站是否清楚標示擁有者/營運者的資訊？

## 2. 同意 (Consent)
- [ ] **Cookie Banner**: 是否有 Cookie 同意橫幅？且預設不勾選行銷/追蹤類 Cookie？
- [ ] **主動同意**: 註冊或訂閱時，是否要求用戶「主動」勾選同意條款（不能預設勾選）？
- [ ] **撤回同意**: 用戶是否可以像給予同意一樣容易地撤回同意（例如在設定中關閉追蹤）？

## 3. 資料主體權利 (Rights of the Data Subject)
- [ ] **存取權 (Right to Access)**: 用戶能否查看系統蒐集了關於他們的哪些資料？
- [ ] **更正權 (Right to Rectification)**: 用戶能否修改不正確的個人資料？
- [ ] **刪除權 (Right to Erasure / RTBF)**: 用戶能否要求刪除其帳號及所有關聯個資？（且系統確實執行刪除或匿名化）
- [ ] **資料可攜權 (Data Portability)**: 用戶能否將其資料匯出為通用格式 (JSON/CSV/XML)？

## 4. 資料安全 (Data Security)
- [ ] **加密**: 傳輸中資料 (Data in Transit) 是否使用 HTTPS？靜態資料 (Data at Rest) 是否有加密（尤其是密碼、敏感個資）？
- [ ] **最小化**: 是否只收集達成功能所必須的資料？（Data Minimization）
- [ ] **存取控制**: 是否只有授權人員/系統能存取敏感資料？

## 5. 資料外洩處理 (Data Breach)
- [ ] **記錄與通報**: 是否有即使與流程來偵測並記錄資料外洩事件？
