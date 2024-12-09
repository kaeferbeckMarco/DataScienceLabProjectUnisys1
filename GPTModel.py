from openai import OpenAI

class GPTModel:

    def __init__(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def segment_text(self, text, prompt1, system_prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{prompt1}: {text}"}
            ]
        )
        return response.choices[0].message.content.split("#")

    def extract_rules_from_text(self, segment, prompt2, system_prompt):
        prompt = f"{prompt2}: {segment}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def translate_document_to_english(self, text):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": f"Translate the following text to English: {text}"}
            ]
        )
        return response.choices[0].message.content