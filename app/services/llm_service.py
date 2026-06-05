import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.metadata import LLMMetadata
from app.schemas.validation import ValidationResult

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

import json


def parse_json_response(content: str) -> dict:

    content = content.strip()

    match = re.search(
        r"\{.*\}",
        content,
        re.DOTALL,
    )

    if not match:
        raise ValueError(f"No JSON found in response: {content}")

    return json.loads(match.group())


from app.schemas.metadata import LLMMetadata


def extract_metadata_with_llm(
    text: str,
) -> LLMMetadata:

    preview = text[:8000]

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[
            {
                "role": "system",
                "content": """
You are an academic paper metadata extractor.

Return ONLY valid JSON.

Schema:

{
  "title": "...",
  "authors": "...",
  "institution": "...",
  "abstract": "...",
  "publication_year": 2024
}

Do not use markdown.
Do not wrap JSON in code fences.
""",
            },
            {"role": "user", "content": preview},
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    content = content.strip()

    match = re.search(
        r"\{.*\}",
        content,
        re.DOTALL,
    )

    if not match:
        raise ValueError(f"No JSON found in response: {content}")

    data = parse_json_response(content)

    return LLMMetadata(**data)


def test_openrouter():

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[{"role": "user", "content": "Reply with exactly: STUMI_OK"}],
        temperature=0,
    )

    return response.choices[0].message.content


def generate_answer(
    question: str,
    context: str,
) -> str:

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[
            {
                "role": "system",
                "content": """
You are a research assistant.

Answer only from the provided context.

If the answer is not contained in the context,
say that the information is not available.
""",
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:

{question}
""",
            },
        ],
        temperature=0,
    )

    return response.choices[0].message.content
