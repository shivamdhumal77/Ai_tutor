import google.generativeai as genai
import os
from dotenv import load_dotenv

class GeminiService:
    _configured = False
    _model_cache = {}

    def __init__(self, model_name="gemini-pro"):
        self._ensure_configured()
        if model_name not in self._model_cache:
            self._model_cache[model_name] = genai.GenerativeModel(model_name)
        self.model = self._model_cache[model_name]
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]

    @classmethod
    def _ensure_configured(cls):
        if not cls._configured:
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise EnvironmentError("GEMINI_API_KEY not set in environment or .env file.")
            genai.configure(api_key=api_key)
            cls._configured = True

    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(temperature=0.7),
                safety_settings=self.safety_settings
            )
            # Some Gemini SDKs return .text, some .candidates[0].text, handle both
            if hasattr(response, "text"):
                return response.text
            elif hasattr(response, "candidates") and response.candidates:
                return response.candidates[0].text
            else:
                return str(response)
        except Exception as e:
            return f"Error generating content: {str(e)}"