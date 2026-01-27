import os
import requests
import traceback
from datetime import datetime
from functools import wraps
from typing import Optional


class DiscordNotifier:
    """
    Discord Webhook 通知器 for Flask

    Note: 此實作使用同步 requests，會阻塞請求。
    在高流量生產環境建議改用 Celery 或其他非同步任務隊列。
    """

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            print(
                "Warning: DISCORD_WEBHOOK_URL not set. Notifications will satisfy silence."
            )

    def send_error(self, error: Exception, context: str = "") -> bool:
        if not self.webhook_url:
            return False

        embed = {
            "title": "🚨 Flask 應用程式錯誤",
            "color": 0xFF0000,
            "fields": [
                {"name": "錯誤類型", "value": type(error).__name__, "inline": True},
                {
                    "name": "時間",
                    "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "inline": True,
                },
                {
                    "name": "錯誤訊息",
                    "value": str(error)[:1000] or "無訊息",
                    "inline": False,
                },
            ],
            "timestamp": datetime.utcnow().isoformat(),
        }

        stack_trace = traceback.format_exc()
        if stack_trace:
            embed["fields"].append(
                {
                    "name": "堆疊追蹤",
                    "value": f"```python\n{stack_trace[:1000]}```",
                    "inline": False,
                }
            )

        if context:
            embed["fields"].insert(
                0, {"name": "📍 上下文", "value": context, "inline": False}
            )

        return self._send({"embeds": [embed]})

    def send_info(self, message: str, title: str = "ℹ️ 通知") -> bool:
        if not self.webhook_url:
            return False
        embed = {
            "title": title,
            "color": 0x3498DB,
            "description": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        return self._send({"embeds": [embed]})

    def _send(self, payload: dict) -> bool:
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            return response.status_code == 204
        except Exception as e:
            print(f"Failed to send Discord notification: {e}")
            return False


def notify_on_error(notifier: DiscordNotifier, context: str = ""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                notifier.send_error(e, context or f"Function: {func.__name__}")
                raise

        return wrapper

    return decorator
