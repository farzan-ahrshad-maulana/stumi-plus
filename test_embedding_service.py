from app.services.embedding_service import (
    create_embedding,
)

embedding = create_embedding("Attention Is All You Need")

print("Dimension:", len(embedding))

print(embedding[:5])
