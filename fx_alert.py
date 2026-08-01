import json
import os
import urllib.parse
import urllib.request


# ===== 可以自行修改的設定 =====
BASE_CURRENCY = "EUR"
TARGET_CURRENCY = "HKD"
ALERT_RATE = 9.50
# ============================


def get_exchange_rate():
    url = f"https://open.er-api.com/v6/latest/{BASE_CURRENCY}"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    if data.get("result") != "success":
        raise RuntimeError(f"未能取得匯率：{data}")

    rate = float(data["rates"][TARGET_CURRENCY])
    updated_time = data.get("time_last_update_utc", "未知")

    return rate, updated_time


def send_telegram_message(message):
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
            "text": message,
        }
    ).encode("utf-8")

    request = urllib.request.Request(url, data=data, method="POST")

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    if not result.get("ok"):
        raise RuntimeError(f"Telegram 發送失敗：{result}")


rate, updated_time = get_exchange_rate()

print(
    f"目前匯率：1 {BASE_CURRENCY} = "
    f"{rate:.4f} {TARGET_CURRENCY}"
)

if rate >= ALERT_RATE:
    message = (
        "🔔 匯率提示\n\n"
        f"1 {BASE_CURRENCY} = {rate:.4f} {TARGET_CURRENCY}\n"
        f"已達到你設定的目標：{ALERT_RATE:.4f}\n"
        f"資料時間：{updated_time}"
    )

    send_telegram_message(message)
    print("已發送 Telegram 匯率提示。")

else:
    print(
        f"尚未達到目標匯率 {ALERT_RATE:.4f}，"
        "今次不會發送 Telegram 訊息。"
    )
