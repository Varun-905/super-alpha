
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Your API keys
GEMINI_API_KEY = "AIzaSyBRotbHWozOM-ER999UOa_iF36TnvMDZyM"
OPENROUTER_API_KEY = "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"

def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta3/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply.strip()
    except Exception as e:
        print("Gemini error:", e)
        return None

def ask_openrouter(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "openrouter/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        reply = response.json()['choices'][0]['message']['content']
        return reply.strip()
    except Exception as e:
        print("OpenRouter error:", e)
        return "Sorry, Alpha is having trouble answering right now. Try again later."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data['message']

    # First try Gemini
    reply = ask_gemini(user_message)

    # If Gemini fails, fallback to OpenRouter
    if reply is None:
        reply = ask_openrouter(user_message)

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
