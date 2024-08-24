"""Module with response schemas for llm"""

from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# Create a structured output parser based on the schema
LIST_OUTPUT_PARSER = StructuredOutputParser.from_response_schemas(
    [
        ResponseSchema(
            name="german_words",
            description="A list of extracted German words/phrases separated by semicolons `;`.",
        )
    ]
)

# Create a structured output parser based on the schema
SENTENCE_OUTPUT_PARSER = StructuredOutputParser.from_response_schemas(
    [
        ResponseSchema(
            name="translations",
            description="""
            - A list of the sentences separated by semicolons `;`.
            - Do not repeat input in the output.
            - Output example: Sentence 1. ; Sentence 2. ; Sentence 3.
            """,
        )
    ]
)

# Create a structured output parser based on the schema
MAPPING_OUTPUT_PARSER = StructuredOutputParser.from_response_schemas(
    [
        ResponseSchema(
            name="mapping",
            description="""
            - A list of the mapped sentences separated by colons `:` and semicolons `;`.
            - Structure of the response: input word/phrase : output sentence ;
            - Output example: kennen : I kann ; der Hund : die Hunde
            """,
        )
    ]
)
