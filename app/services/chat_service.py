import logging

from sqlalchemy.orm import Session

from app.services.llm_service import generate_answer
from app.services.prompt_service import build_rag_prompt
from app.services.search_service import search


logger = logging.getLogger(__name__)

NO_ANSWER_MESSAGE = (
    "社内文書から回答を確認できませんでした。"
    "担当部署へお問い合わせください。"
)


def ask(
    db: Session,
    question: str,
) -> dict:
    results = search(
        db=db,
        question=question,
        limit=5,
    )

    if not results:
        logger.warning(
            "RAG検索で関連文書が見つかりませんでした。question=%s",
            question,
        )

        return {
            "question": question,
            "answer": NO_ANSWER_MESSAGE,
            "sources": [],
        }

    chunks = [
        result["chunk"]
        for result in results
    ]

    contexts = [
        chunk.content
        for chunk in chunks
    ]

    prompt = build_rag_prompt(
        question=question,
        contexts=contexts,
    )

    answer = generate_answer(
        prompt=prompt,
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "document_id": chunk.document_id,
                "chunk_id": chunk.id,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in chunks
        ],
    }
