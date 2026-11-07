
from flask import Flask, request
import requests

app = Flask(__name__)

# FREE - You will change these later in Meta
TOKEN = "12345"
PHONE_ID = "12345"
VERIFY = "mybot123"

MUSIC = {
"1": "🎵 AMAPIANO\n1. Kabza - https://youtu.be/dQw4w9WgXcQ\n2. DJ Maphorisa - https://youtu.be/dQw4w9WgXcQ",
"2": "🎤 HIP HOP BW\n1. Scar - https://youtu.be/dQw4w9WgXcQ\n2. Veezo - https://youtu.be/dQw4w9WgXcQ",
"3": "🙏 GOSPEL\n1. Dr Tawanda - https://youtu.be/dQw4w9WgXcQ",
"4": "💰 PRICES\nSingle: P50\nEP: P200\nFull Promo: P500"
}

def send(to, msg):
    url = f"https://graph.facebook.com/v21.0/{PHONE_ID}/messages"
    h = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    d = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": msg}}
    requests.post(url, headers=h, json=d)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY:
        return request.args.get("hub.challenge")
    return "wrong", 403

@app.route("/webhook", methods=["POST"])
def hook():
    data = request.json
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        frm = msg["from"]
        txt = msg["text"]["body"].lower().strip()
        if txt in ["hi", "hello", "hey", "menu"]:
            reply = "🎵 WELCOME TO BW MUSIC BOT\n\nReply with number:\n1 - Amapiano\n2 - Hip Hop BW\n3 - Gospel\n4 - Prices"
        elif txt in MUSIC:
            reply = MUSIC[txt]
        else:
            reply = "Send HI for menu Boss!"
        send(frm, reply)
    except:
	    pass
	    return "ok", 200

@app.route("/")
def home():
    return "Music Bot is ON!"

app.run(host="0.0.0.0", port=5000)
