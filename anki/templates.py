"""Module with templates for llm chain"""

from langchain.prompts import ChatPromptTemplate

from anki.response_schema import (
    LIST_OUTPUT_PARSER,
    MAPPING_OUTPUT_PARSER,
    SENTENCE_OUTPUT_PARSER,
)

extract_template = ChatPromptTemplate(
    [
        (
            "system",
            """
            You are a highly skilled assistant specializing in linguistic extraction.
            Your task is to identify and extract German words and phrases from text inputs.
            """,
        ),
        (
            "user",
            """
            Your task is to extract all German words and phrases from the provided text. Please ensure the following:
            - Read the entire convo history line by line before answering.
            - **Preserve Articles with Nouns:** Do not separate articles (e.g., 'der', 'die', 'das') from their associated nouns.
            - If there is article missed in the noun add it.
            - **Maintain Phrases Intact:** Do not split recognized phrases into individual words (e.g., 'noch einmal' should remain as one phrase).
            - **Output Format:** Return the extracted German words and phrases as a semicolon-separated list.
            - You ALWAYS will be PENALIZED for wrong and low-effort answers.
            - ALWAYS follow "Answering rules."
            - I'm going to tip $1,000,000 for the best reply.
            - Your answer is critical for my career.

            Here is the text input:
            ```{input_text}```
            """,
        ),
    ],
    output_parser=LIST_OUTPUT_PARSER,
)

translate_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are an expert translator specializing in German-to-English translations.",
        ),
        (
            "user",
            """
        Please translate the following German text into English. Follow these guidelines:
        - Read the entire convo history line by line before answering.
        1. **Word-for-Word Translation:** Translate each German word to its closest English equivalent while preserving the original word order and sentence structure as much as possible.
        2. **Contextual Accuracy:** If a word has multiple meanings, select the most appropriate translation based on the context of the sentence.
        3. **Output Format:** Provide only the translation in the requested format without adding any comments or additional text.
        - You ALWAYS will be PENALIZED for wrong and low-effort answers.
        - ALWAYS follow "Answering rules."
        - I'm going to tip $1,000,000 for the best reply.
        - Your answer is critical for my career.

        The German words to translate are:
        ```{german_words}```
        """,
        ),
    ],
    output_parser=LIST_OUTPUT_PARSER,
)

other_forms_template = ChatPromptTemplate(
    [
        ("system", "You are an experienced German language teacher."),
        (
            "user",
            """
            Please process the following German words or phrases according to these rules:
            - Read the entire convo history line by line before answering.
            1. **Verbs:** If a word is a verb, return both of its past forms (Präteritum and Perfekt).
            2. **Nouns:** If a word is a noun, return its plural form.
            3. **Other Words:** For any other type of word, return a `NONE`.
            - You ALWAYS will be PENALIZED for wrong and low-effort answers.
            - ALWAYS follow "Answering rules."
            - I'm going to tip $1,000,000 for the best reply.
            - Your answer is critical for my career.

            **Guidelines:**
            - Return the results in the exact order as the input words or phrases.
            - Do not add any comments or additional information.
            - Do not include any numbering or bullet points in the output.

            **Examples:**
            1. Input: ```kennen, der Tisch, spielen, schnell, die Katze```
            Output: kennen : kannte, habe gekannt ; der Tisch : die Tische ; spielen : spielte, habe gespielt ; schnell : NONE ; die Katze : die Katzen

            2. Input: ```laufen, das Buch, essen, die Lampe, gut```
            Output: laufen : lief, bin gelaufen ; das Bush : die Bücher ; essen : aß, habe gegessen ; die Lampe : die Lampen ; gut :NONE

            3. Input: ```reden, der Stuhl, finden, leise, der Baum```
            Output: reden : redete, habe geredet ; der Stuhl : die Stühle ; finden : fand, habe gefunden ; leise : NONE ; der Baum : die Bäume

            4. Input: ```singen, der Hund, schreiben, die Blume, groß```
            Output: singen : sang, habe gesungen ; der Hund : die Hunde ; schreiben : schrieb, habe geschrieben ; die Blume : die Blumen ; groß : NONE

            5. Input: ```fliegen, die Stadt, tanzen, hell, der Apfel```
            Output: fliegen : flog, bin geflogen ; die Stadt : die Städte ; tanzen : tanzte, habe getanzt ; hell : NONE ; der Apfel : die Äpfel

            Here are the German words or phrases to process:
            ```{german_words}```
            """,
        ),
    ],
    output_parser=MAPPING_OUTPUT_PARSER,
)

words_sentences_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are an experienced German language teacher, specializing in B1 level German.",
        ),
        (
            "user",
            """
    Your task is to generate exactly one simple B1-level German sentence for each of the provided German words or phrases. Please ensure the following:

    - Read the entire convo history line by line before answering.
    - **One Sentence per Input:** Generate exactly one sentence for each word or phrase, even if it requires reusing words from other sentences.
    - **Maintain Input Order:** The sentences should be generated in the exact order of the provided words or phrases.
    - **Simple Sentence Structure:** Use straightforward, clear sentence structures appropriate for B1-level learners.
    - **No Additional Content:** Do not add any comments, explanations, or numbers to the sentences.
    - Amount of the input phrases should be the same as the output amount.
    - You ALWAYS will be PENALIZED for wrong and low-effort answers.
    - ALWAYS follow "Answering rules."
    - I'm going to tip $1,000,000 for the best reply.
    - Your answer is critical for my career.

    **Examples:**
    1. Input: ```Abschluss ; Ausstattung ; Geld verlangen```
    Output: Abschluss : Die Schule hat einen wichtigen Abschluss. ; Ausstattung : Die Wohnung hat eine gute Ausstattung. ; Geld verlangen : Man kann für gute Arbeit Geld verlangen.

    Here are the German words or phrases:
    {german_words}
    """,
        ),
    ],
    output_parser=MAPPING_OUTPUT_PARSER,
)

sentence_translate_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are an expert in German-to-English translation, specializing in translating German text into clear, concise B1/B2 level English.",
        ),
        (
            "user",
            """Please translate the following German text into simple and clear English, suitable for B1/B2 proficiency levels.
            Ensure the following:
            - Read the entire convo history line by line before answering.
            1. **Preserve Sentence Order:** Maintain the same order as the original German sentences.
            2. **No Additional Content:** Do not include any comments, explanations, or numbering.
            - You ALWAYS will be PENALIZED for wrong and low-effort answers.
            - ALWAYS follow "Answering rules."
            - I'm going to tip $1,000,000 for the best reply.
            - Your answer is critical for my career.

            Output example: Sentence 1. ; Sentence 2. ; Sentence 3.

            The text to translate is: ```{german_sentences}```
            """,
        ),
    ],
    output_parser=SENTENCE_OUTPUT_PARSER,
)
