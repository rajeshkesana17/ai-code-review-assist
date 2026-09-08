import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from typing import List

load_dotenv()

class CodeIssue(BaseModel):
    line: str = Field(description='The line number or section where the issue is')
    description: str = Field(description='Description of the issue')
    fix: str = Field(description='How to fix the issue')

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
        self.system_instruction = (
            'You are an expert Senior Software Engineer. Review the provided source code. '
            'Identify correctness bugs, security vulnerabilities, maintainability problems, '
            'and performance issues. Do not invent issues. Give actionable fixes and produce '
            'a complete improved version. Return only data matching the supplied schema.'
        )

    def analyze_code(self, code_snippet: str) -> dict:
        if not code_snippet:
            return {'error': 'No code provided.'}
        if not self.client:
            return {'error': 'GEMINI_API_KEY is not configured. Add it to your .env file.'}
        prompt = (
            'Review the following code. Preserve its intended behavior while improving '
            'correctness, security, readability, and efficiency. Mention the relevant line '
            'or section for every issue.\n\nCODE:\n```\n' + code_snippet + '\n```'
        )
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    'system_instruction': self.system_instruction,
                    'response_mime_type': 'application/json',
                    'response_schema': CodeReviewResponse,
                    'temperature': 0.2,
                },
            )
            if response.parsed is None:
                return {'error': 'Gemini returned an empty or invalid structured response.'}
            return response.parsed.model_dump()
        except Exception as exc:
            print(f'Gemini analysis error: {exc}')
            return {'error': 'Unable to analyze the code. Check the server logs and Gemini configuration.'}

gemini_service = GeminiService()
