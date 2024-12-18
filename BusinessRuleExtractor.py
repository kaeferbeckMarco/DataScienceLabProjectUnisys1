from LLM import LLM
from ModelFactory import ModelFactory
import configparser


class BusinessRuleExtractor:

    def __init__(self, llm: LLM):
        config = configparser.ConfigParser()
        config.read("prompts.properties")

        self.business_rules = []
        self.llm = llm
        self.systemPrompt1 = config.get("Prompts", "systemPrompt1")

        self.prompt1 = config.get("Prompts", "prompt1")

        self.systemPrompt2 = config.get("Prompts", "systemPrompt2")

        self.prompt2 = config.get("Prompts", "prompt2")

        self.model = ModelFactory(llm).create_model()

    def extract_business_rules_from_document(self, text):
        # extract the business rules from the text
        segments = self.model.segment_text(text, self.prompt1,self.systemPrompt1)
        extracted_rules = []
        for segment in segments:
            extracted_rules.append(self.model.extract_rules_from_text(segment, self.prompt2,self.systemPrompt2))

        return extracted_rules

    def transalte_document_to_english(self, text):
        # translate the document to english
        return self.model.translate_document_to_english(text)

