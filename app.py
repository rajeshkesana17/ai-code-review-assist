import os
from flask import Flask, request, render_template, jsonify
from gemini_service import gemini_service

app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/api/analyze')
def analyze():
    data = request.get_json(silent=True) or {}
    code = str(data.get('code', '')).strip()
    language = str(data.get('language', 'Auto-detect')).strip() or 'Auto-detect'
    explanation_language = str(data.get('explanation_language', 'English')).strip() or 'English'
    if not code:
        return jsonify({'error': 'No code provided.'}), 400
    result = gemini_service.analyze_code(code, language, explanation_language)
    return jsonify(result), 200 if 'error' not in result else 502

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', '5001')))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
