import ollama

from Model import Model

class MistralModel(Model):

    def segment_text(self, text, prompt1, system_prompt):

        segments = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"{prompt1}: {text}"
                },
            ],
        )

        return segments["message"]["content"].split("#")

    def extract_rules_from_text(self, segment, prompt2, system_prompt):
        prompt = f"{prompt2}: {segment}"
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )

        return response["message"]["content"]

    def translate_document_to_english(self, text):
        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text to English: {text}"
                },
            ],
        )
        return response["message"]["content"]

    def method2(self, param):
        # Correctly implemented abstract method from the Model class
        return f"MistralModel: method2 with param {param}"