import json
import os
import urllib.parse
import urllib.request


# ===== 你日後只需要改呢三個設定 =====
BASE_CURRENCY = "EUR"
TARGET_CURRENCY = "HKD"
ALERT_RATE = 9.50
# ====================================


def send_telegram(message):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode("utf-8")

    request = urllib.request.Request(url, data=data, method="POST")

    with urllib.request.urlopen(request, timeout=20):
        pass


api_url = (
    f"https://api.frankfurter.app/latest"
    f"?from={BASE_CURRENCY}&to={TARGET_CURRENCY}"
)

with urllib.request.urlopen(api_url, timeout=20) as response:
    exchange_data = json.loads(response.read().decode("utf-8"))

current_rate = float(exchange_data["rates"][TARGET_CURRENCY])
rate_date = exchange_data.get("date", "未知日期")

print(
    f"目前匯率：1 {BASE_CURRENCY} = "
    f"{current_rate:.4f} {TARGET_CURRENCY}"
)

if current_rate >= ALERT_RATE:
    message = (
        "🔔 匯率提示\n"
        f"1 {BASE_CURRENCY} = "
        f"{current_rate:.4f} {TARGET_CURRENCY}\n"
        f"已達到你設定的 {ALERT_RATE:.2f}\n"
        f"資料日期：{rate_date}"
    )

    send_telegram(message)
    print("已發送 Telegram 通知。")
else:
    print(
        f"尚未達到 {ALERT_RATE:.2f}，"
        "今次不發通知。"
    )
