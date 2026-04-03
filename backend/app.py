from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random
from flask import render_template

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

def analyze_logic(text_data):
    words = text_data.lower().split()
    unique_ratio = len(set(words)) / len(words) if len(words) > 0 else 0

    if unique_ratio < 0.4:
        return random.randint(20, 45), "Suspicious (Repetitive Vocabulary)"
    return random.randint(65, 95), "Authentic Patterns"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "Failed to fetch website"
            }), 400

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('span', {'id': 'productTitle'})
        product_name = title.get_text().strip() if title else "Unknown Product"

        all_text = " ".join([p.get_text() for p in soup.find_all('p')])

        score, verdict = analyze_logic(all_text)

        return jsonify({
            "status": "success",
            "product": product_name[:50] + "...",
            "score": score,
            "verdict": verdict
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    print("Sentinel Backend is Running on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000)