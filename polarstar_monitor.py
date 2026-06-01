import requests
import json

# ============ 配置区域 ============
POLARSTAR_API_URL = "https://api.polarstar.work/api/v1/b2b/wallet"
POLARSTAR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRJZCI6ImFjY19hNjBlMDNjOWU3ZGU1ZjI3YTkiLCJlbWFpbCI6IjE1Njk3NzM4NTU2QDE2My5jb20iLCJraW5kIjoiYjJiIiwiaWF0IjoxNzc4NzQzODI2LCJleHAiOjE3ODEzMzU4MjZ9.2NyxufXmsGTU3ao7NblFlq2f9GRaeNmH-x67CanUEcQ"
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/b7af34ba-b31d-4bab-9954-931b6c3e8270"
ALERT_THRESHOLD = 5000
# =================================

def get_polarstar_balance():
    headers = {
        "Authorization": f"Bearer {POLARSTAR_TOKEN}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(POLARSTAR_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["data"]["balanceCoins"]
    except Exception as e:
        print(f"获取余额失败: {str(e)}")
        return None

def send_feishu_message(content):
    message = {
        "msg_type": "text",
        "content": {"text": content}
    }
    try:
        requests.post(FEISHU_WEBHOOK, json=message, timeout=10)
    except Exception as e:
        print(f"发送飞书消息失败: {str(e)}")

if __name__ == "__main__":
    balance = get_polarstar_balance()
    if balance is None:
        exit(1)

    send_feishu_message(f"✅ Polarstar 余额通知\n当前余额: {balance} COIN")

    if balance < ALERT_THRESHOLD:
        send_feishu_message(f"⚠️ 余额告警！\n当前余额: {balance} COIN\n低于阈值: {ALERT_THRESHOLD} COIN")
