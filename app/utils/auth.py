from fastapi import HTTPException, Request
from app.supabase_client import supabase


def get_current_user(request: Request) -> dict:
    """Extrae y valida el token JWT del header Authorization."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")

    token = auth_header.split(" ")[1]

    try:
        user = supabase.auth.get_user(token)
        if not user or not user.user:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user.user
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")