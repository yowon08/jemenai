from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = 'AI_STUDIO_API_KEY'  # AI Studio에서 받은 키

@app.route('/gemini', methods=['POST'])
def gemini_proxy():
    user_input = request.json.get('prompt')

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_input
                    }
                ]
            }
        ]
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    res = requests.post(url, headers=headers, json=payload)
    data = res.json()

    try:
        reply = data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        reply = f"Gemini 응답 파싱 실패: {e}\n전체 응답: {data}"

    return jsonify({"response": reply})