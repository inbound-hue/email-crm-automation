from flask import Flask, request
import requests
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
REDIRECT_URI = "https://147d43603447.ngrok-free.app/callback"

@app.route("/callback")
def callback():
    code = request.args.get("code")

    token_url = "https://api.hubapi.com/oauth/v1/token"

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)

    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    return "Authorization successful. You can close this tab."

