import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables from the .env file
load_dotenv()

# Define the exact structure we want Gemini to return using Pydantic
class CodeIssue(BaseModel):
    line: str = Field(description="The line number or section where the issue is")
    description: str = Field(description="Description of the issue")
    fix: str = Field(description="How to fix the issue")

class CodeReviewResponse(BaseModel):
    overall_score: int = Field(description="A score from 0 to 100 representing code quality")
    summary: str = Field(description="A brief summary of the code review")
    issues: List[CodeIssue] = Field(description="List of detected bugs or code smells")
    refactored_code: str = Field(description="The fully refactored and optimized code")

class GeminiService:
    def __init__(self):
        # The genai SDK automatically looks for GEMINI_API_KEY in the environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY is not set in the .env file!")
            
        self.client = genai.Client()
        self.model_name = "gemini-2.5-pro"
        self.system_instruction = (
            "You are an expert Senior Software Engineer. Review the provided code. "
            "Identify bugs, security vulnerabilities, and bad practices. "
            "You must respond with valid JSON matching the requested schema."
        )

    def analyze_code(self, code_snippet: str) -> dict:
        """Sends code to Gemini and returns a structured JSON dictionary."""
        if not code_snippet:
            return {"error": "No code provided."}

        prompt = f"Please review the following code:\n\n```\n{code_snippet}\n```"

        try:
            # Call the Gemini API and force a structured JSON output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "system_instruction": self.system_instruction,
                    "response_mime_type": "application/json",
                    "response_schema": CodeReviewResponse,
                    "temperature": 0.2 # Keep it analytical and less creative
                }
            )
            # The SDK automatically parses the JSON text into a Pydantic object
            # We convert it back to a Python dictionary to easily pass to Flask/HTML
            return response.parsed.model_dump()
            
        except Exception as e:
            print(f"Error communicating with Gemini: {e}")
            return {"error": str(e)}

# Create a single instance to be used by our Flask app
gemini_service = GeminiService()