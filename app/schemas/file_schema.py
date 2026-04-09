from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional



class FileUploadResponse(BaseModel):
    """Respuesta al subir un archivo."""
    id: UUID
    original_name: str
    download_token: UUID
    expires_at: datetime
    size_bytes: int


class FileInfoResponse(BaseModel):
    """Respuesta al consultar info de un archivo."""
    id: UUID
    original_name: str
    mime_type: str
    size_bytes: int
    status: str
    expires_at: datetime
    created_at: datetime


class ErrorResponse(BaseModel):
    """Respuesta de error estándar."""
    detail: str