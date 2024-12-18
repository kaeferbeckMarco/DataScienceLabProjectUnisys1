import google.generativeai as genai

class GeminiModel:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)


    def segment_text(self, text, prompt1, system_prompt):
        # Send the system prompt
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )

        user_message = f"{prompt1}: {text}"
        response = model.generate_content(user_message)

        return response.text.split("#")

    def extract_rules_from_text(self, segment, prompt2, system_prompt):
        # Send the system prompt
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt
        )

        # Send the user message and receive the response
        user_message = f"{prompt2}: {segment}"
        response = model.generate_content(user_message)

        # Process the response
        return response.text

    def translate_document_to_english(self, text):
        # Send the system prompt
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
        )

        # Send the translation request and receive the response
        user_message = f"Translate the following text to English: {text}"
        response = model.generate_content(user_message)

        # Process the response
        return response.text