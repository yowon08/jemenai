import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GEMINI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask_gemini():
    if not API_KEY:
        return jsonify({"error": "API key not found"}), 500

    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        response_json = response.json()
        if "candidates" not in response_json:
            return jsonify({
                "error": "Gemini 응답 파싱 실패",
                "response": response_json
            }), 500

        result_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({ "result": result_text })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/check-api-key")
def check_api_key():
    if API_KEY:
        return jsonify({"message": "API key successfully loaded."})
    else:
        return jsonify({"error": "API key not found."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)