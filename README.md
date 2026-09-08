# CodeLens — AI Code Review Assist

Flask + Google Gemini application that reviews source code and returns a quality score, actionable issues, fixes, and refactored code.

## Run locally
1. `pip install -r requirements.txt`
2. Create `.env` with `GEMINI_API_KEY=...`
3. `python app.py`
4. Open `http://localhost:5001`

`PORT`, `FLASK_HOST`, `FLASK_PORT`, `FLASK_DEBUG`, and `GEMINI_MODEL` can be configured through environment variables.
