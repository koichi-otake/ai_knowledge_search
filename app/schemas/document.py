from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
