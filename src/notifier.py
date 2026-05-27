# notifier.py
import requests

TOKEN = "YOU_BOT_TOKEN"
CHAT_ID ="CHAT_ID"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
