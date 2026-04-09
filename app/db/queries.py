from app.db.connection import get_connection
from datetime import datetime
import uuid


def insert_file(original_name: str, mime_type: str, size_bytes: int,
                storage_path: str, expires_at: datetime, user_id: str = None) -> dict:
    """Inserta un archivo en la base de datos y retorna el registro creado."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO files (original_name, mime_type, size_bytes, storage_path, expires_at, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (original_name, mime_type, size_bytes, storage_path, expires_at, user_id)
            )
            conn.commit()
            return cur.fetchone()
    finally:
        conn.close()


def get_file_by_token(token: str) -> dict | None:
    """Busca un archivo por su download_token."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM files WHERE download_token = %s AND status = 'active'",
                (token,)
            )
            return cur.fetchone()
    finally:
        conn.close()


def mark_file_expired(file_id: uuid.UUID) -> None:
    """Marca un archivo como expirado en la base de datos."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE files SET status = 'expired' WHERE id = %s",
                (str(file_id),)
            )
            conn.commit()
    finally:
        conn.close()


def get_expired_files() -> list:
    """Retorna todos los archivos activos que ya expiraron."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM files
                WHERE status = 'active' AND expires_at < NOW()
                """
            )
            return cur.fetchall()
    finally:
        conn.close()


def delete_file_by_id(file_id: uuid.UUID) -> None:
    """Elimina un archivo de la base de datos por su ID."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM files WHERE id = %s",
                (str(file_id),)
            )
            conn.commit()
    finally:
        conn.close()


def get_user_uploads_today(user_id: str) -> int:
    """Retorna cuántos archivos subió el usuario en las últimas 24 horas."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*) as total FROM files
                WHERE user_id = %s
                AND created_at >= NOW() - INTERVAL '24 hours'
                """,
                (user_id,)
            )
            result = cur.fetchone()
            return result["total"]
    finally:
        conn.close()