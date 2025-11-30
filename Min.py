from flask import Flask, jsonify
import requests
from datetime import datetime, timezone
import os

app = Flask(__name__)

OPENAPI_URL = "https://api.opentimezone.com/convert"
TIMEZONE = "Asia/Almaty"  # Shymkent

def int_to_bcd(value):
    tens = value // 10
    ones = value % 10
    return format((tens << 4) | ones, '08b')

def fetch_minute():
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000")
    payload = {"dateTime": now_utc, "fromTimezone": "UTC", "toTimezone": TIMEZONE}
    try:
        response = requests.post(OPENAPI_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        dt = datetime.fromisoformat(response.json()['dateTime'])
        return int_to_bcd(dt.minute)
    except requests.exceptions.RequestException:
        return "00000000"

@app.route("/", methods=["GET"])
def minute():
    return jsonify({"value": fetch_minute()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
