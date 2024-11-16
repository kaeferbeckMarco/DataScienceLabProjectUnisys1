import ollama

from LLM import LLM
from OllamaModel import OllamaModel


class BusinessRuleExtractionLibrary:

    llm:LLM

    def extract_business_rules_from_document(self, text,prompt1,prompt2):
        #get the correct LLM model based on the LLM enum
        model = self.get_model()
        #extract the business rules from the text
        return model.extract_rules_from_text(text,prompt1,prompt2)

    def transalte_document_to_english(self, text):
        #get the correct LLM model based on the LLM enum
        model = self.get_model()
        #translate the document to english
        return model.translate_document_to_english(text)

    def get_model(self):
        if self.llm == LLM.OLLAMA:
            return OllamaModel()
        # Add other models as needed
        else:
            raise ValueError("Unsupported LLM model")




    def __init__(self,llm:LLM):
        self.business_rules = []
        self.llm = llm

    def extract_business_rules(self, text):
        # Extract business rules from text
        self.business_rules = text.split('\n')

    def get_business_rules(self):
        return self

