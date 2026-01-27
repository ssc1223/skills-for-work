import os
import aiohttp
import traceback
from datetime import datetime
from functools import wraps
from typing import Optional
from sanic.log import logger


class DiscordNotifier:
    """Discord Webhook 通知器 for Sanic (Async)"""

    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            logger.warning(
                "DISCORD_WEBHOOK_URL not set. Notifications will satisfy silence."
            )

    async def send_error(self, error: Exception, context: str = "") -> bool:
        if not self.webhook_url:
            return False

        embed = {
            "title": "🚨 Sanic 應用程式錯誤",
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

        return await self._send({"embeds": [embed]})

    async def send_info(self, message: str, title: str = "ℹ️ 通知") -> bool:
        if not self.webhook_url:
            return False
        embed = {
            "title": title,
            "color": 0x3498DB,
            "description": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        return await self._send({"embeds": [embed]})

    async def _send(self, payload: dict) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    return response.status == 204
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")
            return False


def notify_on_error(notifier: DiscordNotifier, context: str = ""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                await notifier.send_error(e, context or f"Function: {func.__name__}")
                raise

        return wrapper

    return decorator
