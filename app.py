import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/check-api-key', methods=['GET'])
def check_api_key():
    # 환경 변수에서 API 키 읽기
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key is None:
        return jsonify({"error": "API key is not set in environment variables."}), 400
    else:
        return jsonify({"message": "API key successfully loaded.", "api_key": api_key}), 200

if __name__ == "__main__":
    app.run(debug=True)