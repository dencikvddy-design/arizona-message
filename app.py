from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ---- КОНФИГУРАЦИЯ (обязательно замените) ----
BOT_TOKEN = "8938774818:AAFlDhE4eFRWZHb7mYXzTiUjQXs4QXlZPXM"
DEFAULT_CHAT_ID = "1457285528"
# -----------------------------------------------

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        text = data.get("text")
        chat_id = data.get("chat_id", DEFAULT_CHAT_ID)
        if not text:
            return jsonify({"error": "No text"}), 400

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            return jsonify({"status": "ok"}), 200
        else:
            return jsonify({"error": "Telegram API error", "details": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Bot proxy is running!"

@app.route('/health')
def health():
    return "OK"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)