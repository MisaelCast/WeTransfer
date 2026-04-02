import magic
from fastapi import HTTPException, UploadFile
from app.config import settings

ALLOWED_MIME_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "application/pdf",
    "application/zip",
    "application/x-zip-compressed",
    "text/plain",
    "video/mp4",
    "audio/mpeg",
]

BLOCKED_EXTENSIONS = [
    ".exe", ".sh", ".bat", ".cmd", ".py",
    ".js", ".php", ".rb", ".pl", ".ps1"
]


def validate_file(file: UploadFile, file_bytes: bytes) -> None:
    """Valida tamaño, extensión y MIME type real del archivo."""

    # Validar tamaño
    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el tamaño máximo de {settings.max_file_size_mb}MB"
        )

    # Validar extensión
    filename = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in BLOCKED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {ext}"
        )

    # Validar MIME type real (no solo la extensión)
    real_mime = magic.from_buffer(file_bytes, mime=True)
    if real_mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {real_mime}"
        )