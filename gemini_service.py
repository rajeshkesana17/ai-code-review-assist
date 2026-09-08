import os
from typing import List
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

SUPPORTED_LANGUAGES = ['Auto-detect', 'Python', 'Java', 'C', 'C++', 'C#', 'JavaScript', 'TypeScript', 'HTML', 'CSS', 'SQL', 'PHP', 'Go', 'Rust', 'Kotlin', 'Swift', 'Ruby', 'Dart', 'R', 'Scala', 'Bash', 'PowerShell', 'Lua', 'Perl', 'Julia']

class CodeIssue(BaseModel):
    line: str = Field(description='The line number or section where the issue is')
    description: str = Field(description='Technical description of the issue')
    fix: str = Field(description='How to fix the issue')
    simple_explanation: str = Field(description='A beginner-friendly explanation in plain human language that explains what is wrong, why it matters, and what the user should understand')

class CodeReviewResponse(BaseModel):
    overall_score: int = Field(ge=0, le=100, description='Code quality score from 0 to 100')
    summary: str = Field(description='Brief summary of the code review')
    issues: List[CodeIssue] = Field(description='Detected bugs, vulnerabilities, or code smells')
    refactored_code: str = Field(description='Fully refactored and optimized code')

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-pro')
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.system_instruction = ('You are an expert Senior Software Engineer and multilingual code reviewer. Review code according to the selected programming language. Identify only real correctness bugs, security vulnerabilities, maintainability problems, performance issues, and language-specific bad practices. Do not invent issues. Give actionable fixes and produce a complete improved version in the SAME language. Respect language syntax, idioms, standard libraries, conventions, and ecosystem. For every real issue, explain it twice: first technically for a developer, and then in simple, human-friendly language that a beginner can understand. The simple explanation must clearly say what the code is doing wrong, why it can cause a problem, and what the user should do. Avoid unexplained jargon, and when jargon is necessary, define it briefly. Return only data matching the supplied schema.')

    def analyze_code(self, code_snippet: str, language: str = 'Auto-detect') -> dict:
        if not code_snippet:
            return {'error': 'No code provided.'}
        if not self.client:
            return {'error': 'GEMINI_API_KEY is not configured. Add it to your .env file.'}
        selected_language = language if language in SUPPORTED_LANGUAGES else 'Auto-detect'
        language_instruction = ('Detect the programming language from the code.' if selected_language == 'Auto-detect' else f'The selected programming language is {selected_language}. Review it specifically as {selected_language} code.')
        prompt = (f'{language_instruction} Preserve intended behavior while improving correctness, security, readability, and efficiency. Mention the relevant line or section for every issue. For each issue, provide a beginner-friendly simple_explanation in plain human language. Do not merely repeat the technical description. Return refactored code in the same programming language.\n\nCODE:\n' + code_snippet)
        try:
            response = self.client.models.generate_content(model=self.model_name, contents=prompt, config={'system_instruction': self.system_instruction, 'response_mime_type': 'application/json', 'response_schema': CodeReviewResponse, 'temperature': 0.2})
            if response.parsed is None:
                return {'error': 'Gemini returned an empty or invalid structured response.'}
            result = response.parsed.model_dump()
            result['language'] = selected_language
            return result
        except Exception as exc:
            print(f'Gemini analysis error: {exc}')
            return {'error': 'Unable to analyze the code. Check the server logs and Gemini configuration.'}

gemini_service = GeminiService()
