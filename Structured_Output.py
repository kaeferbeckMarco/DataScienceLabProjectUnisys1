from typing import List
from instructor import OpenAISchema
from pydantic import Field
import instructor
from openai import OpenAI
import configparser


config = configparser.ConfigParser()
config.read("apiKey.properties")
api_key = config.get("api_keys", "gpt")


class PrologCondition(OpenAISchema):
    """Represents a single condition in a Prolog rule"""
    predicate: str = Field(..., description="The predicate name (e.g., 'customer', 'valid_id')")
    arguments: List[str] = Field(..., description="List of arguments for the predicate")
    comparison: str | None = Field(None, description="Optional comparison operator (e.g., '>', '=<', '\\=')")
    comparison_value: str | None = Field(None, description="Optional value for comparison")


class PrologRule(OpenAISchema):
    """Represents a complete Prolog rule with metadata"""
    rule_id: str = Field(..., description="Unique identifier for the rule (e.g., 'R1', 'R2')")
    description: str = Field(..., description="Human-readable description of the rule from comments")
    head_predicate: str = Field(..., description="The head predicate name")
    head_arguments: List[str] = Field(..., description="Arguments for the head predicate")
    conditions: List[PrologCondition] = Field(..., description="List of conditions in the rule body")


class BusinessRules(OpenAISchema):
    """Collection of all Prolog rules extracted from the document"""
    rules: List[PrologRule] = Field(..., description="List of all extracted Prolog rules")





# Enable instructor
client = instructor.patch(OpenAI(api_key=api_key))


def extract_rules(llm_output: List[str]) -> BusinessRules:
    # Join the LLM output into a single string for processing
    combined_text = "\n".join(llm_output)

    # Use OpenAI with instructor to extract structured data
    response = client.chat.completions.create(
        model="gpt-4o",
        response_model=BusinessRules,
        messages=[
            {"role": "system", "content": "Extract Prolog rules from the given text into structured format."},
            {"role": "user", "content": combined_text}
        ],
    )

    return response


