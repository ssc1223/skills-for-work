"""
Discord 錯誤通知模組

使用方式:
    from utils.discord_notifier import DiscordNotifier, notify_on_error

    discord = DiscordNotifier(os.getenv("DISCORD_WEBHOOK_URL"))

    # 方式一：手動發送
    discord.send_error(exception, "處理訂單時發生錯誤")

    # 方式二：裝飾器自動發送
    @notify_on_error(discord, "處理用戶請求")
    def my_function():
        pass
"""

import os
import requests
import traceback
from datetime import datetime
from functools import wraps
from typing import Optional


class DiscordNotifier:
    """Discord Webhook 通知器"""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        初始化通知器

        Args:
            webhook_url: Discord Webhook URL，若未提供則從環境變數讀取
        """
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError("必須提供 DISCORD_WEBHOOK_URL")

    def send_error(self, error: Exception, context: str = "") -> bool:
        """
        發送錯誤通知到 Discord

        Args:
            error: 捕獲的例外物件
            context: 錯誤發生的上下文描述

        Returns:
            bool: 是否發送成功
        """
        embed = {
            "title": "🚨 錯誤通知",
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

        # 加入堆疊追蹤（截斷以符合 Discord 限制）
        stack_trace = traceback.format_exc()
        if stack_trace and stack_trace != "NoneType: None\n":
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

    def send_warning(self, message: str, context: str = "") -> bool:
        """
        發送警告通知

        Args:
            message: 警告訊息
            context: 上下文描述
        """
        embed = {
            "title": "⚠️ 警告通知",
            "color": 0xFFA500,
            "description": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        if context:
            embed["fields"] = [{"name": "📍 上下文", "value": context}]

        return self._send({"embeds": [embed]})

    def send_info(self, message: str, title: str = "ℹ️ 資訊通知") -> bool:
        """
        發送一般資訊通知

        Args:
            message: 通知訊息
            title: 標題
        """
        embed = {
            "title": title,
            "color": 0x3498DB,
            "description": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        return self._send({"embeds": [embed]})

    def _send(self, payload: dict) -> bool:
        """
        發送 payload 到 Discord

        Returns:
            bool: 是否發送成功
        """
        try:
            response = requests.post(self.webhook_url, json=payload, timeout=5)
            return response.status_code == 204
        except Exception:
            # 避免通知失敗導致更多問題
            return False


def notify_on_error(notifier: DiscordNotifier, context: str = ""):
    """
    裝飾器：在函式發生錯誤時自動發送 Discord 通知

    Args:
        notifier: DiscordNotifier 實例
        context: 錯誤上下文描述，若未提供則使用函式名稱

    使用範例:
        @notify_on_error(discord, "處理付款")
        def process_payment(order_id):
            # 你的邏輯
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                notifier.send_error(e, context or f"函式: {func.__name__}")
                raise  # 重新拋出讓上層決定如何處理

        return wrapper

    return decorator


def async_notify_on_error(notifier: DiscordNotifier, context: str = ""):
    """
    非同步版本的錯誤通知裝飾器

    使用範例:
        @async_notify_on_error(discord, "處理 API 請求")
        async def handle_request(request):
            pass
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                notifier.send_error(e, context or f"函式: {func.__name__}")
                raise

        return wrapper

    return decorator
