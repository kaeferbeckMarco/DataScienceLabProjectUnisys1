import ollama

from Model import Model


class OllamaModel(Model):
    def extract_rules_from_text(self,text,prompt1,prompt2):
        # Step 1: Segment and preprocess the text
        segmentsResponse = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt1}: {text}"
                },
            ],
        )

        segments = segmentsResponse["message"]["content"].split("#")

        extracted_rules = []

        for segment in segments:
            # Step 2: Extract rules using contextual understanding
            prompt = f"{prompt2}: {segment}"
            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
            )

            extracted_rules.append(response["message"]["content"])

        return extracted_rules

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