import ollama

from LLM import LLM
from OllamaModel import OllamaModel


class BusinessRuleExtractionLibrary:

    def __init__(self, llm: LLM):
        self.business_rules = []
        self.llm = llm
        self.prompt1 = "Please divide the provided text into meaningful sections based on content and context. Use the '#' symbol to separate each section. Focus on identifying distinct topics, legal clauses, or thematic shifts to ensure each segment is coherent and self-contained"
        self.prompt2 = "From the following text segment, extract all explicit and implicit legal or business rules. Present each rule clearly and concisely, ensuring it is self-contained. If applicable, format the rules as a numbered list and include any conditions or exceptions associated with each rule"

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

