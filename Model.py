from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def extract_rules_from_text(self,text,prompt1,prompt2):
        pass

    @abstractmethod
    def method2(self, param):
        pass