import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add resources path
sys.path.append(os.path.join(os.path.dirname(__file__), "../resources/flask"))

from discord_notifier import DiscordNotifier, notify_on_error


class TestDiscordNotifier(unittest.TestCase):
    def setUp(self):
        self.mock_url = "https://discord.com/api/webhooks/test"
        self.notifier = DiscordNotifier(webhook_url=self.mock_url)

    @patch("requests.post")
    def test_send_info(self, mock_post):
        mock_post.return_value.status_code = 204

        success = self.notifier.send_info("Test Message")

        self.assertTrue(success)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], self.mock_url)
        payload = kwargs["json"]
        self.assertEqual(payload["embeds"][0]["description"], "Test Message")
        self.assertEqual(payload["embeds"][0]["color"], 0x3498DB)

    @patch("requests.post")
    def test_send_error(self, mock_post):
        mock_post.return_value.status_code = 204

        try:
            raise ValueError("Test Exception")
        except ValueError as e:
            success = self.notifier.send_error(e, "Test Context")

        self.assertTrue(success)
        payload = mock_post.call_args[1]["json"]
        fields = payload["embeds"][0]["fields"]

        # Check fields
        self.assertTrue(
            any(f["name"] == "錯誤類型" and f["value"] == "ValueError" for f in fields)
        )
        self.assertTrue(
            any(
                f["name"] == "錯誤訊息" and "Test Exception" in f["value"]
                for f in fields
            )
        )
        self.assertTrue(
            any(
                f["name"] == "📍 上下文" and f["value"] == "Test Context"
                for f in fields
            )
        )

    @patch("requests.post")
    def test_decorator(self, mock_post):
        mock_post.return_value.status_code = 204

        @notify_on_error(self.notifier)
        def fail_func():
            raise RuntimeError("Decorator Test")

        with self.assertRaises(RuntimeError):
            fail_func()

        mock_post.assert_called_once()
        payload = mock_post.call_args[1]["json"]
        self.assertIn("Decorator Test", str(payload))


if __name__ == "__main__":
    unittest.main()
