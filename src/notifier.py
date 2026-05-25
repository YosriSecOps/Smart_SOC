# notifier.py
import requests

TOKEN = "8683565076:AAEy60pNCkEymSVxg9t2AnhQ55VifvJexCk"
CHAT_ID ="6237076538"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
