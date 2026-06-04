import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

import json

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
Extract metadata from an academic paper.

Return ONLY valid JSON.

Fields:
- title
- authors
- institution
- abstract
- publication_year
""",
            },
            {
                "role": "user",
                "content": preview,
            },
        ],
        temperature=0,
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    return LLMMetadata(**data)


def test_openrouter():

    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3",
        messages=[{"role": "user", "content": "Reply with exactly: STUMI_OK"}],
        temperature=0,
    )

    return response.choices[0].message.content
