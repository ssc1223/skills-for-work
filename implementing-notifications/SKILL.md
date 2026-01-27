---
name: implementing-notifications
description: 協助為 Flask, Sanic, Vite, Angular, JS 專案加入 Discord 通知功能。當用戶想要實作通知、alerting、notify 功能時使用。
---

# 實作通知功能 (Implementing Notifications)

## 何時使用此技能
- 用戶需要在專案中加入錯誤通知或一般通知功能
- 用戶提到 "discord webhook", "alerting", "notify"
- 支援的框架：Flask, Sanic, Vite (Vue/React), Angular, Vanilla JS

## 工作流程
1. 確認用戶的專案類型 (Backend: Flask/Sanic, Frontend: Vite/Angular/JS)。
2. 根據類型，將對應的 `resources/` 下的檔案複製到用戶專案中。
3. 協助用戶設定環境變數 `DISCORD_WEBHOOK_URL`。
4. 提供使用範例程式碼。

## 指令
### Flask
將 `resources/flask/discord_notifier.py` 複製到專案工具目錄 (e.g., `utils/`)。
使用 `cp` 指令或 `write_to_file`。

### Sanic
將 `resources/sanic/discord_notifier.py` 複製到專案工具目錄。

### Vite / Frontend
將 `resources/vite/useNotification.js` (或 `.ts`) 複製到 `src/hooks/` 或 `src/utils/`。

### Vue (Universal)
將 `resources/vue/useNotification.js` 複製到 `src/composables/`。
此版本同時支援 Vite (`import.meta.env`) 與 Webpack (`process.env`)。

## 資源
- [Flask 模板](resources/flask/discord_notifier.py)
- [Sanic 模板](resources/sanic/discord_notifier.py)
- [Vite 模板](resources/vite/useNotification.js)
- [Vue 模板](resources/vue/useNotification.js)
- [Angular 模板](resources/angular/notification.service.ts)

- [JS 模板](resources/js/NotificationSystem.js)

## 使用範例

### Flask
```python
from utils.discord_notifier import DiscordNotifier, notify_on_error

notifier = DiscordNotifier()

# 1. 裝飾器用法 (推薦)
@app.route('/api/test')
@notify_on_error(notifier)
def test_route():
    raise ValueError("This error will be sent to Discord")

# 2. 手動發送
notifier.send_error(Exception("Something went wrong"), context="Database Connection")
notifier.send_info("System started successfully")
```

### Vue (Composables)
```javascript
import { useNotification } from '@/composables/useNotification';

export default {
    setup() {
        const { notifyError } = useNotification();

        const doSomething = async () => {
             try {
                 await apiCall();
             } catch (e) {
                 // 觸發錯誤通知
                 notifyError(e, 'API Call Failed');
             }
        };

        return { doSomething };
    }
}
```

### Vanilla JS
```javascript
const notifier = new NotificationSystem(process.env.DISCORD_WEBHOOK_URL);
notifier.send('Application Initialized');
```

### Angular
```typescript
constructor(private notificationService: NotificationService) {}

someMethod() {
    this.api.getData().subscribe({
        error: (err) => this.notificationService.notify(err.message, 'error')
    });
}
```

