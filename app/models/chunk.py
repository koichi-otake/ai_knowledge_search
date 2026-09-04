from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base

from pgvector.sqlalchemy import Vector


class ChunkORM(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),
        nullable=True,
    )

    document = relationship(
        "DocumentORM",
        back_populates="chunks",
    )

