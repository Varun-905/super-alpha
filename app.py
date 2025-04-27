
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ====== CONFIG ======
GEMINI_API_KEY = "AIzaSyDaHaq_H2Kr4GiO10sCyB4E5hHyKluQ7NM"
OPENROUTER_API_KEY = "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"

# ====== FUNCTIONS ======

def chat_with_gemini(message):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
        payload = {
            "contents": [{"parts": [{"text": message}]}]
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply
    except Exception as e:
        print("Gemini failed:", e)
        return None

def chat_with_openrouter(message):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message}]
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return reply
    except Exception as e:
        print("OpenRouter failed:", e)
        return "Sorry, Alpha is having trouble answering right now. Try again later."

# ====== ROUTES ======

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    
    # First try Gemini
    reply = chat_with_gemini(user_input)
    
    # If Gemini fails, try OpenRouter
    if not reply:
        reply = chat_with_openrouter(user_input)

    return jsonify({"reply": reply})

# ====== RUN APP ======

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
