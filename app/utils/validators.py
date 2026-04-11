import filetype
import os
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
    """Valida tamaño, extensión, path traversal y MIME type real del archivo."""

    filename = file.filename or ""
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo no válido")

    filename = os.path.basename(filename)
    if not filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo no válido")

    max_bytes = settings.max_file_size_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"El archivo excede el tamaño máximo de {settings.max_file_size_mb}MB"
        )

    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in BLOCKED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido: {ext}")

    kind = filetype.guess(file_bytes)
    if kind is not None:
        real_mime = kind.mime
    else:
        try:
            file_bytes.decode('utf-8')
            real_mime = "text/plain"
        except UnicodeDecodeError:
            real_mime = "application/octet-stream"

    if real_mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido: {real_mime}")