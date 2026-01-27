# GDPR 實作範例指南

以下提供常見 GDPR 需求的實作範例參考。

## 1. 資料刪除 (Right to Erasure) 範例

### Python (Flask/SQLAlchemy)
當用戶請求刪除帳號時，務必連同關聯資料一起刪除或匿名化。

```python
# 只是範例，請根據專案架構調整
@app.route('/api/user/delete', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    
    # 1. 刪除或匿名化關聯資料
    # Option A: 級聯刪除 (Cascade Delete) - 如果資料庫 schema 有設定
    # Option B: 手動匿名化其他表中的資料
    orders = Order.query.filter_by(user_id=user_id).all()
    for order in orders:
        order.user_id = None # 或設定為匿名用戶 ID
        order.user_email = "anonymized@example.com"
        order.user_name = "Deleted User"
        
    # 2. 刪除用戶本體
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    
    logout_user()
    return jsonify({"message": "帳號已永久刪除，您的個人資料已被移除或匿名化。"}), 200
```

## 2. 資料匯出 (Data Portability) 範例

### Python (回傳 JSON)
允許用戶下載其個人資料。

```python
@app.route('/api/user/export', methods=['GET'])
@login_required
def export_data():
    user = current_user
    
    # 收集用戶資料
    data_package = {
        "profile": {
            "name": user.name,
            "email": user.email,
            "joined_at": user.created_at.isoformat()
        },
        "activity_logs": [log.to_dict() for log in user.logs],
        "preferences": user.preferences
    }
    
    # 回傳 JSON 檔案下載
    return Response(
        json.dumps(data_package, ensure_ascii=False, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment;filename=my_data.json'}
    )
```

## 3. Cookie 同意橫幅 (Consent Banner)

### HTML/JS (簡易版)
這只是一個簡單的前端範例。

```html
<!-- 加在 layout.html 或 index.html 底部 -->
<div id="cookie-consent" style="position: fixed; bottom: 0; left: 0; right: 0; background: #333; color: white; padding: 20px; display: none; text-align: center;">
    <p>我們使用 Cookies 來改善您的體驗。繼續瀏覽即代表您同意我們的隱私權政策。</p>
    <button onclick="acceptCookies()" style="background: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer;">同意</button>
    <a href="/privacy-policy" style="color: #ddd; margin-left: 10px;">了解更多</a>
</div>

<script>
    function checkCookieConsent() {
        if (!localStorage.getItem('cookie_consent_accepted')) {
            document.getElementById('cookie-consent').style.display = 'block';
        }
    }

    function acceptCookies() {
        localStorage.setItem('cookie_consent_accepted', 'true');
        document.getElementById('cookie-consent').style.display = 'none';
        // 在此觸發 GA 或其他追蹤腳本
    }
    
    window.onload = checkCookieConsent;
</script>
```

## 4. 隱私權政策大綱 (Markdown Template)

你的專案應該包含一個 `/privacy-policy` 頁面：

```markdown
# 隱私權政策 (Privacy Policy)

**生效日期**: YYYY/MM/DD

## 1. 我們收集的資料
- 帳戶資訊 (Email, 姓名...)
- 使用數據 (Log, 裝置資訊...)

## 2. 我們如何使用資料
- 提供服務
- 改善體驗

## 3. 您的權利
根據 GDPR，您擁有以下權利：
- **存取權**: 要求我們提供您的資料副本。
- **刪除權**: 要求我們刪除您的帳號。
- **更正權**: 修改錯誤的資料。

## 4. 聯絡我們
如有隱私問題，請來信: privacy@example.com
```
