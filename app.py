
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = "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"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    try:
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "openrouter/openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}]
        }
        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=headers, json=data)
        reply = response.json()['choices'][0]['message']['content']
    except Exception as e:
        reply = "Sorry, Alpha is having trouble answering right now. Try again later."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
