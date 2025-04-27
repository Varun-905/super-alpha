from flask import Flask, render_template, request, jsonify
import requests
import os
from gtts import gTTS
import base64

app = Flask(__name__)

# API KEYS
GEMINI_API_KEY = "AIzaSyDaHaq_H2Kr4GiO10sCyB4E5hHyKluQ7NM"
OPENROUTER_API_KEY = "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"

@app.route('/')
def index():
    return render_template('index.html')

def chat_with_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(url, json=payload)
    try:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return "I'm sorry, I couldn't get a response."

def chat_with_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a friendly assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        return response.json()['choices'][0]['message']['content']
    except:
        return "I'm sorry, I couldn't get a response."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    try:
        bot_response = chat_with_gemini(user_message)
    except:
        bot_response = chat_with_openrouter(user_message)

    tts = gTTS(text=bot_response, lang='en')
    tts.save("/tmp/response.mp3")

    with open("/tmp/response.mp3", "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

    return jsonify({'response': bot_response, 'audio': encoded_string})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)