import google.generativeai as genai

class GeminiModel:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def segment_text(self, text, prompt1, system_prompt):
        response = self.model.generate_content(
            contents=[
                {
                    "parts": [
                        {"text": system_prompt, "role": "system"},
                        {"text": f"{prompt1}: {text}", "role": "user"}
                    ]
                }
            ]
        )
        return response.candidates[0].content.parts[0].text.split("#")

    def extract_rules_from_text(self, segment, prompt2, system_prompt):
        prompt = f"{prompt2}: {segment}"
        response = self.model.generate_content(
            contents=[
                {
                    "parts": [
                        {"text": system_prompt, "role": "system"},
                        {"text": prompt, "role": "user"}
                    ]
                }
            ]
        )
        return response.candidates[0].content.parts[0].text

    def translate_document_to_english(self, text):
        response = self.model.generate_content(
            contents=[
                {
                    "parts": [
                        {"text": f"Translate the following text to English: {text}", "role": "user"}
                    ]
                }
            ]
        )
        return response.candidates[0].content.parts[0].text