from app.supabase_client import supabase
from app.config import settings


def upload_file(file_bytes: bytes, filename: str, mime_type: str) -> str:
    """Sube un archivo a Supabase Storage y retorna el path."""
    path = f"{filename}"

    supabase.storage.from_(settings.supabase_bucket).upload(
        path=path,
        file=file_bytes,
        file_options={"content-type": mime_type}
    )

    return path


def delete_file(path: str) -> None:
    """Elimina un archivo de Supabase Storage."""
    supabase.storage.from_(settings.supabase_bucket).remove([path])


def get_file(path: str) -> bytes:
    """Descarga un archivo de Supabase Storage y retorna sus bytes."""
    response = supabase.storage.from_(settings.supabase_bucket).download(path)
    return response