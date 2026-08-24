from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import DocumentORM


def create_document(
    db: Session,
    filename: str,
    content_type: str,
) -> DocumentORM:
    document = DocumentORM(
        filename=filename,
        content_type=content_type,
    )

    db.add(document)
    db.flush()

    return document


def get_documents(
    db: Session,
) -> list[DocumentORM]:
    statement = (
        select(DocumentORM)
        .order_by(DocumentORM.id)
    )

    return list(
        db.scalars(statement).all()
    )


def get_document_by_id(
    db: Session,
    document_id: int,
) -> DocumentORM | None:
    return db.get(
        DocumentORM,
        document_id,
    )


def delete_document(
    db: Session,
    document: DocumentORM,
) -> None:
    db.delete(document)
