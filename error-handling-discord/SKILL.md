---
name: handling-errors-discord
description: 實作錯誤處理、邊界條件處理，並透過 Discord Webhook 發送錯誤通知。當用戶需要加入錯誤處理、exception handling、邊界檢查、或 Discord 通知功能時使用。
---

# 錯誤處理與 Discord 通知

為程式碼加入健全的錯誤處理機制，並在發生錯誤時透過多種管道發送即時通知。

## 何時使用此技能

- 需要為現有程式碼加入錯誤處理
- 實作邊界條件檢查（null、空值、型別驗證）
- 設定 Discord/Slack/Email 錯誤通知機制
- 建立統一的例外處理架構

## 工作流程

```
[ ] 1. 辨識需要錯誤處理的程式碼區塊
[ ] 2. 確認邊界條件（輸入驗證、null 檢查、型別檢查）
[ ] 3. 實作 try-except 區塊
[ ] 4. 設定通知管道（Discord/Slack/Email）
[ ] 5. 加入錯誤日誌記錄
[ ] 6. 測試錯誤情境
```

## 邊界條件檢查模式

### 輸入驗證

```python
def validate_input(data: dict, required_fields: list[str]) -> tuple[bool, str]:
    """驗證必填欄位是否存在且非空"""
    for field in required_fields:
        if field not in data:
            return False, f"缺少必填欄位: {field}"
        if data[field] is None or data[field] == "":
            return False, f"欄位不可為空: {field}"
    return True, ""
```

### 型別與範圍檢查

```python
def validate_positive_int(value, field_name: str) -> int:
    """確保值為正整數"""
    if not isinstance(value, int):
        raise TypeError(f"{field_name} 必須為整數")
    if value <= 0:
        raise ValueError(f"{field_name} 必須為正數")
    return value
```

## 核心模組

使用 `framework_error_notifier.py` 作為核心通知模組，支援多種通知管道。

### 快速開始

```python
from utils.framework_error_notifier import (
    NotificationConfig,
    FrameworkErrorNotifier,
    create_flask_error_handler,
    create_sanic_error_handler,
    notify_on_error,
)

# 方式一：從環境變數建立配置
config = NotificationConfig.from_env()

# 方式二：手動建立配置
config = NotificationConfig(
    discord_webhook_url="https://discord.com/api/webhooks/...",
    discord_enabled=True,
    service_name="My API",
    environment="production",
)

# 建立通知器
notifier = FrameworkErrorNotifier(config)
```

### 環境變數配置

```bash
# .env
ERROR_NOTIFICATION_SERVICE_NAME=CiteReady API
ERROR_NOTIFICATION_ENVIRONMENT=production
ERROR_NOTIFICATION_DISCORD_ENABLED=true
ERROR_NOTIFICATION_DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Slack（選用）
ERROR_NOTIFICATION_SLACK_ENABLED=true
ERROR_NOTIFICATION_SLACK_WEBHOOK_URL=https://hooks.slack.com/...

# Email SMTP（選用）
ERROR_NOTIFICATION_EMAIL_ENABLED=true
ERROR_NOTIFICATION_EMAIL_METHOD=smtp
ERROR_NOTIFICATION_SMTP_HOST=smtp.gmail.com
ERROR_NOTIFICATION_SMTP_PORT=587
ERROR_NOTIFICATION_SMTP_USERNAME=your@email.com
ERROR_NOTIFICATION_SMTP_PASSWORD=your-app-password
ERROR_NOTIFICATION_EMAIL_RECIPIENTS=admin@example.com,dev@example.com

# 頻率控制
ERROR_NOTIFICATION_RATE_LIMIT_SECONDS=300  # 5 分鐘內相同錯誤只通知一次
```

### Flask 整合

```python
from flask import Flask
from utils.framework_error_notifier import (
    NotificationConfig,
    FrameworkErrorNotifier,
    create_flask_error_handler,
)

app = Flask(__name__)
config = NotificationConfig.from_env()
notifier = FrameworkErrorNotifier(config)

# 註冊全域錯誤處理器
app.register_error_handler(Exception, create_flask_error_handler(notifier))
```

### Sanic 整合

```python
from sanic import Sanic
from utils.framework_error_notifier import (
    NotificationConfig,
    FrameworkErrorNotifier,
    create_sanic_error_handler,
)

app = Sanic("MyApp")
config = NotificationConfig.from_env()
notifier = FrameworkErrorNotifier(config)

# 註冊全域錯誤處理器
app.exception(Exception)(create_sanic_error_handler(notifier))
```

### 裝飾器模式

```python
from utils.framework_error_notifier import notify_on_error

# 同步函式
@notify_on_error(notifier)
def process_payment(order_id: int):
    # 你的邏輯
    pass

# 非同步函式
@notify_on_error(notifier)
async def handle_request(request):
    # 你的邏輯
    pass
```

### 手動發送通知

```python
# 非同步發送
try:
    process_data()
except Exception as e:
    await notifier.notify_error(e, context={"user_id": 123, "action": "process"})
    raise

# 同步發送（無事件循環時）
try:
    process_data()
except Exception as e:
    notifier.notify_error_sync(e, context={"user_id": 123})
    raise
```

### 測試連線

```python
# 測試所有已啟用的通知管道
result = await notifier.test_connection()
print(result)
# {'discord': {'success': True, 'message': '測試通知發送成功'}, ...}

# 測試特定管道
result = await notifier.test_connection(["discord"])
```

## 錯誤分級

模組會自動根據錯誤訊息判斷錯誤級別：

| 級別 | 觸發關鍵字 | Discord 顏色 |
|------|-----------|-------------|
| critical | connection, timeout, authentication, payment, database | 🔴 紅色 |
| high | api, file, service | 🟠 橘色 |
| medium | validation, rate limit | 🟡 黃色 |
| low | 其他 | 🟢 綠色 |

## 資源

- [scripts/discord_notifier.py](scripts/discord_notifier.py) - 簡化版 Discord 專用通知模組
- 完整模組參考：`utils/framework_error_notifier.py`

> [!IMPORTANT]
> Webhook URL 應透過環境變數載入，切勿寫死在程式碼中。
