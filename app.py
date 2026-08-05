import os
from flask import Flask, request, render_template, jsonify
from gemini_service import gemini_service

# Initialize the Flask application
app = Flask(__name__)

# 1. Route to serve our beautiful HTML page
@app.route('/')
def index():
    # Flask automatically looks for HTML files in a folder named 'templates'
    return render_template('index.html')

# 2. API Route to handle the code analysis securely in the backend
@app.route('/api/analyze', methods=['POST'])
def analyze():
    # Get the JSON data sent from our frontend JavaScript
    data = request.get_json()
    code = data.get('code', '').strip()
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
        
    print("Code received! Sending to Gemini API...")
    
    # Call our Gemini service
    result_dict = gemini_service.analyze_code(code)
    
    # Return the JSON back to the frontend
    return jsonify(result_dict)

if __name__ == '__main__':
    # Running on port 5001 to avoid the Mac AirPlay conflict
    app.run(host='0.0.0.0', port=5001, debug=True)