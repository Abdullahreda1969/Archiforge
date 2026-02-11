from google import genai
import json
import re

class AIEngine:
    def __init__(self, api_key):
        # نكتفي بالمفتاح، المكتبة ستتولى الباقي بأمان
        self.client = genai.Client(api_key=api_key)
        self.model_id = "models/gemma-3-1b-it" # أو أي موديل آخر من القائمة التي ظهرت لك سابقاً
    def imagine(self, prompt):
        # ندمج التعليمات والهيكل داخل النص مباشرة لنتجنب أخطاء Config
        refined_prompt = f"""
        You are an expert web developer. Build a professional project based on: {prompt}

        STRICT STANDARDS:
        1. Every HTML file MUST start with <!DOCTYPE html>.
        2. The <html> tag MUST include a 'lang' attribute.
        3. Include <meta charset="UTF-8"> and <meta name="viewport" content="width=device-width, initial-scale=1.0">.
        4. Ensure all images have 'alt' attributes for accessibility.

        OUTPUT FORMAT:
        Return ONLY a valid JSON object following this schema:
        {{
        "project_name": "ProjectName",
        "files": [
            {{"path": "index.html", "content": "..."}},
            {{"path": "app.py", "content": "..."}}
        ]
        }}
        """
        try:
            # أبسط شكل للاستدعاء لتجنب مشاكل التوافقية
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=refined_prompt
            )
            
            text = response.text
            
            # تنظيف النص باستخدام Regex لاستخراج الـ JSON فقط مهما كانت الظروف
            json_match = re.search(r'(\{.*\})', text, re.DOTALL)
            if json_match:
                clean_json = json_match.group(1)
                return json.loads(clean_json)
            
            return json.loads(text.strip())
            
        except Exception as e:
            return {"error": str(e)}