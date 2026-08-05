# AI Code Review Assist - Agent Instructions

## Project Overview
A Flask web application that uses the Google Gemini API to provide AI-powered code reviews. Users paste code into the frontend, and the backend sends it to Gemini for analysis, returning a structured review with score, issues, and refactored code.

## Architecture
- **Backend**: Flask (`app.py`) serving a REST API at `/api/analyze`
- **AI Service**: `gemini_service.py` using `google-genai` SDK with Pydantic models for structured JSON output
- **Frontend**: Server-rendered HTML (`templates/index.html`) + vanilla JS (`static/js/app.js`) + CSS (`static/css/style.css`)

## Key Files
- `app.py` - Flask app with `/` (UI) and `/api/analyze` (POST) routes
- `gemini_service.py` - Gemini API client with Pydantic schemas (`CodeIssue`, `CodeReviewResponse`)
- `templates/index.html` - Main frontend template
- `static/css/style.css` - Dark-themed styling
- `static/js/app.js` - Frontend logic (fetch API, DOM rendering)

## Setup
1. Copy `.env` and add your `GEMINI_API_KEY`
2. Install deps: `pip install -r requirements.txt`
3. Run: `python app.py` (port 5001)

## Important Notes
- The `GeminiService` uses `gemini-2.5-pro` model with structured JSON output via Pydantic schemas
- The `.env` file must contain `GEMINI_API_KEY` for the API to work
- `python-dotenv` is used to load environment variables from `.env`