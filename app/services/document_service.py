from pathlib import Path
import shutil

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.repositories import chunk_repository
from app.repositories import document_repository
from app.services.embedding_service import create_embedding
from app.services.chunk_service import split_text, split_resume_words
from app.services.pdf_service import extract_text, extract_words

STORAGE_DIR = Path("storage/documents")


def get_documents(
    db: Session,
):
    return document_repository.get_documents(
        db=db,
    )


def upload_document(
    db: Session,
    file: UploadFile,
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PDFファイルのみアップロードできます。",
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ファイル名を取得できません。",
        )

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = STORAGE_DIR / file.filename

    try:
        # 1. PDFをディスクへ保存
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # 2. documentsテーブルへ登録
        document = document_repository.create_document(
            db=db,
            filename=file.filename,
            content_type=file.content_type,
        )

        # create_document() 内の flush() により
        # この時点で document.id が利用できる
        document_id = document.id

        # 3. PDFから文字を抽出
        text = extract_text(
            str(file_path)
        )

        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="PDFから文字を抽出できませんでした。",
            )

        # 4. PDFの単語情報を取得
        words = extract_words(
            str(file_path)
        )

        # 5. 履歴書を意味単位に分割
        chunks = split_resume_words(
            words
        )

        embeddings = [
            create_embedding(chunk) 
            for chunk in chunks
        ]

        # 6. chunksテーブルへ登録
        chunk_repository.create_chunks(
            db=db,
            document_id=document_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        # 7. 全部成功したら確定
        db.commit()

        # 8. DBの最新状態を取得
        db.refresh(document)

        return document

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise
