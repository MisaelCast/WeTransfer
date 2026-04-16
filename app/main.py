from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.limiter import limiter
from app.api.routes.file_routes import router
from app.services.expiration_service import start_scheduler
from app.config import settings
from contextlib import asynccontextmanager

# Definimos el lifespan 
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

# Creamos la aplicación FastAPI con el lifespan  
app = FastAPI(
    title="WeTransfer Clon",
    description="Servicio de transferencia de archivos con enlaces únicos y expiración automática.",
    version="1.0.0", 
    lifespan=lifespan
)


# Límite de tamaño de request a nivel de servidor
app.state.max_upload_size = settings.max_file_size_mb * 1024 * 1024

# Configuración del limitador de velocidad
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)

# --- MIDDLEWARE DE SEGURIDAD PARA LIMITAR TAMAÑO ---
@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    # 1. Solo nos interesa interceptar peticiones POST a la ruta /upload
    if request.url.path == "/upload" and request.method == "POST":
        
        # 2. Obtenemos el tamaño declarado por el navegador o cliente
        content_length = request.headers.get("content-length")
        
        if content_length:
            try:
                length = int(content_length)
                max_bytes = settings.max_file_size_mb * 1024 * 1024
                
                # 3. Si es mayor al límite, cortamos la conexión inmediatamente
                if length > max_bytes:
                    return JSONResponse(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        content={"detail": f"Petición rechazada: El archivo excede el límite de {settings.max_file_size_mb}MB."}
                    )
            except ValueError:
                # Si el header está corrupto o mal formado, lo dejamos pasar 
                # para que la ruta /upload lo rechace más adelante.
                pass

    # Si todo está bien, dejamos que la petición continúe su curso normal
    response = await call_next(request)
    return response
# ---------------------------------------------------

@app.get("/")
def root():
    return FileResponse("app/static/index.html")

@app.get("/config")
def get_config():
    return {
        "supabase_url": settings.supabase_url,
        "supabase_key": settings.supabase_key
    }