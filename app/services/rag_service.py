from sqlalchemy.orm import Session

from app.services.llm_service import (
    generate_answer,
)
from app.services.retrieval_service import (
    retrieve_chunks,
)
