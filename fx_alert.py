import json
import os
import urllib.error
import urllib.parse
import urllib.request


token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not token:
    raise RuntimeError("找不到 TELEGRAM_TOKEN")

if not chat_id:
    raise RuntimeError("找不到 TELEGRAM_CHAT_ID")

url = f"https://api.telegram.org/bot{token}/sendMessage"

data = urllib.parse.urlencode(
    {
        "chat_id": chat_id,
        "text": "✅ Telegram 測試訊息",
    }
).encode("utf-8")

request = urllib.request.Request(url, data=data, method="POST")

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        result = json.loads(response.read().decode("utf-8"))
        print(result)

except urllib.error.HTTPError as error:
    details = error.read().decode("utf-8")
    print("Telegram 詳細錯誤：", details)
    raise
