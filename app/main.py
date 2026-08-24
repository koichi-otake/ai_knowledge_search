from fastapi import FastAPI

from app.core.config import settings
from app.routers.document import router as document_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(document_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "APIは正常に起動しています。",
        "app_name": settings.app_name,
        "version": settings.app_version,
    }

