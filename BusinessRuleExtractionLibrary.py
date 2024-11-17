import ollama

from LLM import LLM
from OllamaModel import OllamaModel


class BusinessRuleExtractionLibrary:

    def __init__(self, llm: LLM):
        self.business_rules = []
        self.llm = llm
        self.prompt1 = "segment the text into logical segments use # to separate the segments"
        self.prompt2 = "Identify legal rules in the following segment"

    def extract_business_rules_from_document(self, text):
        # get the correct LLM model based on the LLM enum
        model = self.get_model()
        # extract the business rules from the text
        segments = model.segment_text(text, self.prompt1)
        extracted_rules = []
        for segment in segments:
            extracted_rules.append(model.extract_rules_from_text(segment, self.prompt2))

        return extracted_rules

    def transalte_document_to_english(self, text):
        # get the correct LLM model based on the LLM enum
        model = self.get_model()
        # translate the document to english
        return model.translate_document_to_english(text)

    def get_model(self):
        if self.llm == LLM.OLLAMA:
            return OllamaModel()
        # Add other models as needed
        else:
            raise ValueError("Unsupported LLM model")

    def extract_business_rules(self, text):
        # Extract business rules from text
        self.business_rules = text.split('\n')

    def get_business_rules(self):
        return self
