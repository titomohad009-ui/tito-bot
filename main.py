import os
import time
import json
import urllib.request
import urllib.parse
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.environ.get("TOKEN")
BASE = f"https://api.telegram.org/bot{TOKEN}"

def api(method, data=None):
    url = BASE + "/" + method
    if data:
        data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def bot_loop():
    offset = 0
    print("Bot started...")
    while True:
        try:
            res = api("getUpdates", {"offset": offset, "timeout": 30})
            for u in res.get("result", []):
                offset = u["update_id"] + 1
                msg = u.get("message")
                if not msg:
                    continue
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                if text == "/start":
                    api("sendMessage", {"chat_id": chat_id, "text": "اهلا يا تيتو! البوت شغال 24 ساعة"})
                else:
                    api("sendMessage", {"chat_id": chat_id, "text": "وصلتني رسالتك: " + text})
        except Exception as e:
            print(e)
            time.sleep(3)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, *a):
        pass

def web():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), H).serve
