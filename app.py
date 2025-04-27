from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Get API keys from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta3/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        
        # More robust response parsing
        if 'candidates' not in response.json():
            print("Gemini response missing 'candidates' key")
            return None
            
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"Gemini API request failed: {str(e)}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Gemini response parsing error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected Gemini error: {str(e)}")
        return None

def ask_openrouter(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://yourdomain.com",  # Required by OpenRouter
            "X-Title": "Super Alpha Assistant"  # Required by OpenRouter
        }
        data = {
            "model": "openrouter/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        # More robust response parsing
        if 'choices' not in response.json():
            print("OpenRouter response missing 'choices' key")
            return None
            
        reply = response.json()['choices'][0]['message']['content']
        return reply.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"OpenRouter API request failed: {str(e)}")
        return None
    except (KeyError, IndexError) as e:
        print(f"OpenRouter response parsing error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected OpenRouter error: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data['message']
    
    # Log the incoming request
    print(f"\n[{datetime.now()}] Received message: {user_message}")

    # First try Gemini
    reply = ask_gemini(user_message)
    source = "Gemini"
    
    # If Gemini fails, fallback to OpenRouter
    if reply is None:
        reply = ask_openrouter(user_message)
        source = "OpenRouter"
    
    # If both fail, provide a helpful default message
    if reply is None:
        reply = "I'm currently experiencing technical difficulties. Please try again in a few moments."
        source = "Fallback"
    
    # Log the response
    print(f"[{datetime.now()}] Responded with ({source}): {reply}")
    
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)