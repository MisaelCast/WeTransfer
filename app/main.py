from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes.file_routes import router
from app.services.expiration_service import start_scheduler

app = FastAPI(
    title="WeTransfer Clon",
    description="Servicio de transferencia de archivos con enlaces únicos y expiración automática.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.get("/")
def root():
    return FileResponse("app/static/index.html")