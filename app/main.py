from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.utils.limiter import limiter
from app.api.routes.file_routes import router
from app.services.expiration_service import start_scheduler

app = FastAPI(
    title="WeTransfer Clon",
    description="Servicio de transferencia de archivos con enlaces únicos y expiración automática.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.get("/")
def root():
    return FileResponse("app/static/index.html")