import requests
import time
import json

# ============ 配置区域（修改这里即可） ============
# Polarstar 配置
POLARSTAR_API_URL = "https://api.polarstar.work/api/v1/b2b/wallet"
POLARSTAR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRJZCI6ImFjY19hNjBlMDNjOWU3ZGU1ZjI3YTkiLCJlbWFpbCI6IjE1Njk3NzM4NTU2QDE2My5jb20iLCJraW5kIjoiYjJiIiwiaWF0IjoxNzc4NzQzODI2LCJleHAiOjE3ODEzMzU4MjZ9.2NyxufXmsGTU3ao7NblFlq2f9GRaeNmH-x67CanUEcQ"

# 飞书 Webhook 地址
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/b7af34ba-b31d-4bab-9954-931b6c3e8270"

# 检查间隔（单位：秒，这里设置为5分钟检查一次）
CHECK_INTERVAL = 10

# 余额告警阈值（低于这个值会额外发提醒）
ALERT_THRESHOLD = 5000

# =================================================

last_balance = None

def get_polarstar_balance():
    """获取 Polarstar 账户余额"""
    headers = {
        "Authorization": f"Bearer {POLARSTAR_TOKEN}",
        "Accept": "application/json"
    }
    try:
        response = requests.get(POLARSTAR_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        balance = data["data"]["balanceCoins"]
        return balance
    except Exception as e:
        print(f"获取余额失败: {str(e)}")
        return None

def send_feishu_message(content):
    """发送消息到飞书"""
    message = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    try:
        response = requests.post(FEISHU_WEBHOOK, json=message, timeout=10)
        response.raise_for_status()
        print("飞书消息发送成功")
    except Exception as e:
        print(f"发送飞书消息失败: {str(e)}")

if __name__ == "__main__":
    print("Polarstar 余额监控脚本已启动...")
    # 启动时先发送一次当前余额
    initial_balance = get_polarstar_balance()
    if initial_balance is not None:
        last_balance = initial_balance
        send_feishu_message(f"✅ Polarstar 余额监控已启动\n当前余额: {initial_balance} COIN")

    while True:
        time.sleep(CHECK_INTERVAL)
        current_balance = get_polarstar_balance()
        if current_balance is None:
            continue

        # 余额变动通知
        # if last_balance is not None and current_balance != last_balance:
            delta = current_balance - last_balance
            if delta > 0:
                msg = f"📈 Polarstar 余额变动\n余额: {last_balance} → {current_balance} COIN\n变动: +{delta} COIN"
            else:
                msg = f"📉 Polarstar 余额变动\n余额: {last_balance} → {current_balance} COIN\n变动: {delta} COIN"
            send_feishu_message(msg)#

        # 余额低于阈值告警
        if current_balance < ALERT_THRESHOLD:
            alert_msg = f"⚠️ Polarstar 余额告警\n当前余额: {current_balance} COIN（低于阈值 {ALERT_THRESHOLD} COIN）\n请及时充值！"
            send_feishu_message(alert_msg)

        last_balance = current_balance