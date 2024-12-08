from abc import ABC, abstractmethod

class Model(ABC):

    @abstractmethod
    def segment_text(self,text,prompt,systemPrompt):
        pass

    @abstractmethod
    def extract_rules_from_text(self,text,prompt,systemPrompt):
        pass

    @abstractmethod
    def translate_document_to_english(self, text):
        pass

    @abstractmethod
    def method2(self, param):
        pass