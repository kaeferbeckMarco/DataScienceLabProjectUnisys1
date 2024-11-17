import ollama

from Model import Model


class OllamaModel(Model):

    def segment_text(self, text, prompt1):
        segments = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt1}: {text}"
                },
            ],
        )

        return segments["message"]["content"].split("#")

    def extract_rules_from_text(self, segment, prompt):
        prompt = f"{prompt}: {segment}"
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
        )

        return response["message"]["content"]

    def translate_document_to_english(self, text):
        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text to English: {text}"
                },
            ],
        )
        return response["message"]["content"]


def method2(self, param):
    return "OllamaModel: method2"
