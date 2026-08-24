from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.document import DocumentResponse
from app.services import document_service


router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@router.post(
    "",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return document_service.upload_document(
        db=db,
        file=file,
    )

@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents(
    db: Session = Depends(get_db),
):
    return document_service.get_documents(
        db=db,
    )
