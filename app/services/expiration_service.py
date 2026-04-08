from apscheduler.schedulers.background import BackgroundScheduler
from app.db.queries import get_expired_files, mark_file_expired, delete_file_by_id
from app.services.storage_service import delete_file


def delete_expired_files():
    """Busca archivos expirados, los elimina de Supabase y los marca en PostgreSQL."""
    print("[Expiration Job] Buscando archivos expirados...")
    expired = get_expired_files()

    if not expired:
        print("[Expiration Job] No hay archivos expirados.")
        return

    for file in expired:
        try:
            # Eliminar de Supabase Storage
            delete_file(file["storage_path"])
            # Marcar como expirado en PostgreSQL
            mark_file_expired(file["id"])
            print(f"[Expiration Job] Archivo eliminado: {file['original_name']}")
        except Exception as e:
            print(f"[Expiration Job] Error eliminando {file['original_name']}: {e}")


def start_scheduler():
    """Inicia el scheduler que corre el job cada hora."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_expired_files, "interval", hours=1)
    scheduler.start()
    print("[Expiration Job] Scheduler iniciado.")
    return scheduler