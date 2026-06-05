import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

response = client.embeddings.create(
    model="baai/bge-m3",
    input="Attention Is All You Need",
)

embedding = response.data[0].embedding

print("Dimension:", len(embedding))
print("First 5 values:", embedding[:5])
