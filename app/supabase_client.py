from supabase import create_client, Client
from app.config import settings

"Inicializa el cliente de Supabase usando la URL y la clave del entorno."
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)