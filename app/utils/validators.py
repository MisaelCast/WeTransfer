import filetype
import os
from fastapi import HTTPException, UploadFile
from app.config import settings

ALLOWED_MIME_TYPES = [
    # Imágenes
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml", 
    
    # Documentos de Office y PDF
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", # Excel (.xlsx)
    "application/vnd.ms-excel", # Excel antiguo (.xls)
    "application/msword", # Word antiguo (.doc)
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", # Word (.docx)
    "application/vnd.ms-powerpoint", # PowerPoint (.ppt)
    "application/vnd.openxmlformats-officedocument.presentationml.presentation", # PowerPoint (.pptx)
    
    # Archivos comprimidos
    "application/zip",
    "application/x-zip-compressed",
    "application/vnd.rar", # .rar
    "application/x-7z-compressed", # .7z
    
    # Texto y Datos
    "text/plain",
    "text/csv", # .csv
    "application/json", # .json
    "text/markdown", # .md
    
    # Multimedia
    "video/mp4",
    "video/quicktime", # .mov
    "video/webm", # .webm
    "audio/mpeg",
    "audio/wav", # .wav
]

BLOCKED_EXTENSIONS = [
    # Ejecutables y scripts de Windows (Protección de usuarios)
    ".exe", ".bat", ".cmd", ".ps1", ".vbs", ".msi", ".wsf", ".hta",
    
    # Ejecutables y scripts de Linux/Unix 
    ".sh", ".bin", ".elf", ".run",
    
    # Lenguajes de programación y scripts web (Prevención de ejecución remota)
    ".py", ".js", ".php", ".rb", ".pl", ".cgi", ".jsp", ".asp", ".aspx",
    
    # Otros binarios y paquetes ejecutables
    ".jar", ".apk", ".appimage"
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
