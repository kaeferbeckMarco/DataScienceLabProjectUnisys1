from GPTModel import GPTModel
from LLM import LLM
from MistralModel import MistralModel
from OllamaModel import OllamaModel
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

    def extract_business_rules_from_document(self, text):
        # get the correct LLM model based on the LLM enum
        model = self.get_model()
        # extract the business rules from the text
        segments = model.segment_text(text, self.prompt1,self.systemPrompt1)
        extracted_rules = []
        for segment in segments:
            extracted_rules.append(model.extract_rules_from_text(segment, self.prompt2,self.systemPrompt2))

        return extracted_rules

    def transalte_document_to_english(self, text):
        # get the correct LLM model based on the LLM enum
        model = self.get_model()
        # translate the document to english
        return model.translate_document_to_english(text)

    def get_model(self):

        config = configparser.ConfigParser()
        config.read("apiKey.properties")

        if self.llm == LLM.OLLAMA:
            return OllamaModel()
        if self.llm == LLM.MISTRAL:
            return MistralModel()
        if self.llm == LLM.GPT:
            return GPTModel(config.get("api_keys", "gpt"))
        # Add other models as needed
        else:
            raise ValueError("Unsupported LLM model")

