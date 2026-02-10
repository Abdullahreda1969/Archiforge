from google import genai
import json
from pathlib import Path

class AIEngine:
    def __init__(self, api_key: str):
        # استخدام المكتبة الجديدة الرسمية لعام 2026
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-1.5-flash-002" # النسخة الأحدث والأسرع

    def imagine_project(self, prompt: str):
        system_instruction = f"""
        You are a Master Software Architect. For the project: "{prompt}", 
        generate a complete structure with boilerplate code.
        Return ONLY a JSON object with this format:
        {{
            "directories": ["list/of/folders"],
            "files": {{
                "folder/file.py": "the source code here",
                "requirements.txt": "dependencies"
            }}
        }}
        """
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=system_instruction
        )
        
        # المكتبة الجديدة ترجع النص بشكل مباشر أكثر
        raw_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_json)