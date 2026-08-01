import json
import os
import urllib.parse
import urllib.request


token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not token:
    raise RuntimeError("找不到 TELEGRAM_TOKEN")

if not chat_id:
    raise RuntimeError("找不到 TELEGRAM_CHAT_ID")

message = "✅ 測試成功！GitHub Actions 已經連接到 Telegram。"

url = f"https://api.telegram.org/bot{token}/sendMessage"

data = urllib.parse.urlencode(
    {
        "chat_id": chat_id,
        "text": message,
    }
).encode("utf-8")

request = urllib.request.Request(url, data=data, method="POST")

with urllib.request.urlopen(request, timeout=20) as response:
    result = json.loads(response.read().decode("utf-8"))

if not result.get("ok"):
    raise RuntimeError(f"Telegram 發送失敗：{result}")

print("Telegram 測試訊息已成功發送。")

