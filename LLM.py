from enum import Enum


class LLM(Enum):
    """
    Enum class for the different LLM models
    """
    GPT = "gpt"
    OLLAMA = "ollama"
    CLAUDE = "claude"
    MISTRAL = "mistral"
    GEMINI = "gemini"
