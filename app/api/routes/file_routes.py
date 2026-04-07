from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime, timedelta
from app.config import settings
from app.utils.validators import validate_file
from app.services.token_service import generate_token
from app.services.storage_service import upload_file, delete_file, get_file
from app.db.queries import insert_file, get_file_by_token, delete_file_by_id
from app.schemas.file_schema import FileUploadResponse, FileInfoResponse
from fastapi.responses import Response
import uuid

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
async def upload(file: UploadFile = File(...)):
    """Sube un archivo, lo guarda en Supabase y registra metadata en PostgreSQL."""

    # Leer bytes del archivo
    file_bytes = await file.read()

    # Validar archivo
    validate_file(file, file_bytes)

    # Generar token y path único
    token = generate_token()
    filename = f"{uuid.uuid4()}_{file.filename}"
    expires_at = datetime.utcnow() + timedelta(hours=settings.expiration_hours)

    # Subir a Supabase Storage
    storage_path = upload_file(file_bytes, filename, file.content_type)

    # Guardar metadata en PostgreSQL
    record = insert_file(
        original_name=file.filename,
        mime_type=file.content_type,
        size_bytes=len(file_bytes),
        storage_path=storage_path,
        expires_at=expires_at
    )

    return FileUploadResponse(
        id=record["id"],
        original_name=record["original_name"],
        download_token=record["download_token"],
        expires_at=record["expires_at"],
        size_bytes=record["size_bytes"]
    )


@router.get("/file/{token}", response_model=FileInfoResponse)
def file_info(token: str):
    """Retorna información de un archivo por su token."""
    record = get_file_by_token(token)

    if not record:
        raise HTTPException(status_code=404, detail="Archivo no encontrado o expirado")

    return FileInfoResponse(
        id=record["id"],
        original_name=record["original_name"],
        mime_type=record["mime_type"],
        size_bytes=record["size_bytes"],
        status=record["status"],
        expires_at=record["expires_at"],
        created_at=record["created_at"]
    )


@router.get("/download/{token}")
def download(token: str):
    """Descarga un archivo por su token."""
    record = get_file_by_token(token)

    if not record:
        raise HTTPException(status_code=404, detail="Archivo no encontrado o expirado")

    if record["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=410, detail="El enlace ha expirado")

    # Descargar desde Supabase Storage
    file_bytes = get_file(record["storage_path"])

    return Response(
        content=file_bytes,
        media_type=record["mime_type"],
        headers={
            "Content-Disposition": f'attachment; filename="{record["original_name"]}"'
        }
    )


@router.delete("/file/{token}")
def delete(token: str):
    """Elimina un archivo por su token."""
    record = get_file_by_token(token)

    if not record:
        raise HTTPException(status_code=404, detail="Archivo no encontrado o expirado")

    # Borrar de Supabase Storage
    delete_file(record["storage_path"])

    # Borrar de PostgreSQL
    delete_file_by_id(record["id"])

    return {"detail": "Archivo eliminado correctamente"}