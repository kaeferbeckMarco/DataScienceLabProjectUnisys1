import ollama

from Model import Model


class OllamaModel(Model):
    def extract_rules_from_text(self,text,prompt1,prompt2):
        # Step 1: Segment and preprocess the text
        #segments = ollama.segment_text(text)
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
            #response = ollama.generate(prompt)
            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
            )

            # Step 3: Parse the response to get conditions and consequences
            #parsed_rules = parse_response(response)
            extracted_rules.append(response["message"]["content"])

        return extracted_rules

    def method2(self, param):
        return "OllamaModel: method2"