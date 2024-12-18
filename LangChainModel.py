from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import configparser
import langdetect


class BusinessRulesProcessor:
    def __init__(self, api_key_path="apiKey.properties", prompts_path="prompts.properties"):
        config = configparser.ConfigParser()
        config.read([api_key_path, prompts_path])
        self.api_key = config.get("api_keys", "gpt")
        self.system_prompt1 = config.get("Prompts", "systemPrompt1")
        self.prompt1 = config.get("Prompts", "prompt1")
        self.system_prompt2 = config.get("Prompts", "systemPrompt2")
        self.prompt2 = config.get("Prompts", "prompt2")


        self.llm = ChatOpenAI(api_key=self.api_key)


    def detect_and_translate(self, text):
        """Detect language and translate if not English"""
        try:
            lang = langdetect.detect(text)
            if lang != 'en':
                translation_prompt = ChatPromptTemplate.from_messages([
                    ("system",
                     "You are a professional translator. Translate the following text to English while preserving all technical terms and maintaining the original meaning:"),
                    ("user", "{text}")
                ])

                chain = (
                    translation_prompt
                    | self.llm
                )

                result = chain.invoke({"text": text})
                return result.content
            return text
        except:
            return text

    def structure_text(self, text):
        """Structure the text using system_prompt1 and prompt1"""
        structuring_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt1),
            ("user", self.prompt1 + "\n{text}")
        ])

        chain = (
            structuring_prompt
            | self.llm
        )

        result = chain.invoke({"text": text})
        return result.content  # Extrahiere den String-Inhalt

    def extract_prolog_rules(self, text):
        """Extract Prolog rules using system_prompt2 and prompt2"""
        prolog_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt2),
            ("user", self.prompt2 + "\n{text}")
        ])

        chain = (
            prolog_prompt
            | self.llm
        )

        result = chain.invoke({"text": text})
        return result.content

    def process_document(self, text):
        """Main processing pipeline"""
        # 1. load text
        legal_text = text

        # 2. Detect language and translate if needed
        print("Checking language and translating if needed...")
        english_text = self.detect_and_translate(legal_text)

        # 3. Structure the text
        print("Structuring text...")
        structured_text = self.structure_text(english_text)

        # 4. Extract Prolog rules from structured text
        print("Extracting Prolog rules...")
        if hasattr(structured_text, 'content'):
            structured_text = structured_text.content

        prolog_rules = self.extract_prolog_rules(structured_text)


        if hasattr(prolog_rules, 'content'):
            return prolog_rules.content
        return str(prolog_rules)

