import configparser

from GPTModel import GPTModel
from GeminiModel import GeminiModel
from LLM import LLM
from MistralModel import MistralModel
from OllamaModel import OllamaModel


class ModelFactory:
    def __init__(self, llm: LLM):
        self.llm = llm
        pass

    def create_model(self):
        config = configparser.ConfigParser()
        config.read("apiKey.properties")

        if self.llm == LLM.OLLAMA:
            return OllamaModel()
        if self.llm == LLM.MISTRAL:
            return MistralModel()
        if self.llm == LLM.GPT:
            return GPTModel(config.get("api_keys", "gpt"))
        if self.llm == LLM.GEMINI:
            return GeminiModel(config.get("api_keys", "gemini"))
        # Add other models as needed
        else:
            raise ValueError("Unsupported LLM model")